#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "BedControl.h"
#include "BedDriver.h"
#include "BedService.h"
#include "NetworkManager.h"
#ifdef CONFIG_APP_ENABLE_MATTER
#include "MatterManager.h"
#endif
#include "Config.h"
#include "driver/gpio.h"
#include "driver/ledc.h"
#include "esp_log.h"
#include <math.h>
#include "esp_flash.h"
#include "esp_timer.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "nvs_flash.h"
#include <inttypes.h>
#include "StatusLed.h"

BedControl bed;
BedDriver* bedDriver = &bed;
NetworkManager net;

static const char* TAG_MAIN = "MAIN";
static bool s_dualOtaEnabled = false;

#ifdef CONFIG_APP_ENABLE_MATTER
#define APP_MATTER 1
#else
#define APP_MATTER 0
#endif

// LED channels match BedControl
#define LEDC_MODE               LEDC_LOW_SPEED_MODE
#define LEDC_TIMER              LEDC_TIMER_0
#define LEDC_CHANNEL_R          LEDC_CHANNEL_0
#define LEDC_CHANNEL_G          LEDC_CHANNEL_1
#define LEDC_CHANNEL_B          LEDC_CHANNEL_2

enum class LedState {
    IDLE,          // unprovisioned / not commissioned
    COMMISSIONING, // commissioning in progress
    COMMISSIONED,  // provisioned/connected
    RESETTING
};

static LedState g_led_state = LedState::IDLE;
struct LedOverride {
    bool active = false;
    bool persistent = false;
    uint64_t expiry_us = 0;
    uint8_t r = 0, g = 0, b = 0;
};
static LedOverride s_led_override;

void status_led_override(uint8_t r, uint8_t g, uint8_t b, uint32_t duration_ms) {
    s_led_override.active = true;
    s_led_override.persistent = (duration_ms == 0);
    s_led_override.expiry_us = esp_timer_get_time() + ((uint64_t)duration_ms * 1000ULL);
    s_led_override.r = r;
    s_led_override.g = g;
    s_led_override.b = b;
}

void status_led_clear_override() {
    s_led_override = {};
}

static void set_led_rgb(uint8_t r, uint8_t g, uint8_t b) {
    // Assume common anode; match BedControl logic
    uint32_t dR = LED_COMMON_ANODE ? (255 - r) : r;
    uint32_t dG = LED_COMMON_ANODE ? (255 - g) : g;
    uint32_t dB = LED_COMMON_ANODE ? (255 - b) : b;
    ledc_set_duty(LEDC_MODE, LEDC_CHANNEL_R, dR); ledc_update_duty(LEDC_MODE, LEDC_CHANNEL_R);
    ledc_set_duty(LEDC_MODE, LEDC_CHANNEL_G, dG); ledc_update_duty(LEDC_MODE, LEDC_CHANNEL_G);
    ledc_set_duty(LEDC_MODE, LEDC_CHANNEL_B, dB); ledc_update_duty(LEDC_MODE, LEDC_CHANNEL_B);
}

static void led_task(void* pv) {
    uint32_t t = 0;
    while (1) {
        bool applied_override = false;
        if (s_led_override.active) {
            uint64_t now = esp_timer_get_time();
            if (s_led_override.persistent || now < s_led_override.expiry_us) {
                set_led_rgb(s_led_override.r, s_led_override.g, s_led_override.b);
                applied_override = true;
            } else {
                s_led_override = {};
            }
        }

        if (!applied_override) {
            switch (g_led_state) {
                case LedState::IDLE: { // spec: slow blink when unprovisioned
                    bool on = ((t / 10) % 2) == 0; // 1 Hz, 50% duty
                    set_led_rgb(on ? 120 : 0, on ? 120 : 0, on ? 120 : 0);
                    break;
                }
                case LedState::COMMISSIONING: { // spec: fast blink during commissioning
                    bool on = ((t / 2) % 2) == 0; // 5 Hz, 50% duty
                    set_led_rgb(on ? 120 : 0, on ? 120 : 0, 0);
                    break;
                }
                case LedState::COMMISSIONED: { // spec: solid when provisioned
                    set_led_rgb(0, 120, 0);
                    break;
                }
                case LedState::RESETTING: { // fault/reset: red blink
                    bool on = ((t / 4) % 2) == 0;
                    set_led_rgb(on ? 180 : 0, 0, 0);
                    break;
                }
            }
        }
        t++;
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

static void button_task(void* pv) {
    const int64_t shortMs = 2000;
    const int64_t longMs = 5000;
    while (1) {
        if (gpio_get_level((gpio_num_t)COMMISSION_BUTTON_GPIO) == 0) {
            int64_t start = esp_timer_get_time() / 1000;
            ESP_LOGI(TAG_MAIN, "Button pressed");
            while (gpio_get_level((gpio_num_t)COMMISSION_BUTTON_GPIO) == 0) {
                vTaskDelay(pdMS_TO_TICKS(10));
            }
            int64_t dur = (esp_timer_get_time() / 1000) - start;
            if (dur >= longMs) {
#if APP_MATTER
                ESP_LOGW(TAG_MAIN, "Button long-press: factory reset");
                MatterManager::instance().factoryReset();
#else
                ESP_LOGW(TAG_MAIN, "Button long-press: Wi-Fi + NVS reset");
                g_led_state = LedState::RESETTING;
                esp_wifi_restore();
                nvs_flash_erase();
                esp_restart();
#endif
            } else if (dur >= shortMs) {
#if APP_MATTER
                ESP_LOGI(TAG_MAIN, "Button short-press: start commissioning");
                MatterManager::instance().startCommissioning();
                g_led_state = LedState::COMMISSIONING;
#else
                ESP_LOGI(TAG_MAIN, "Button short-press: Wi-Fi reset");
                g_led_state = LedState::RESETTING;
                esp_wifi_restore();
                esp_restart();
#endif
            }
        }
        vTaskDelay(pdMS_TO_TICKS(20));
    }
}

#if !APP_MATTER
static esp_event_handler_instance_t s_ip_handler = nullptr;
static esp_event_handler_instance_t s_disc_handler = nullptr;
static void wifi_status_handler(void*, esp_event_base_t event_base, int32_t event_id, void*) {
    if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        g_led_state = LedState::COMMISSIONED;
        ESP_LOGI(TAG_MAIN, "LED state: commissioned (Wi-Fi up)");
    } else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        g_led_state = LedState::IDLE;
        ESP_LOGW(TAG_MAIN, "LED state: idle (Wi-Fi disconnected)");
    }
}
#endif

void bed_task(void *pvParameter) {
    while (1) {
        bedDriver->update();
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}

extern "C" void app_main() {
    // Detect flash size to decide OTA strategy
    uint32_t flash_size_bytes = 0;
    if (esp_flash_get_size(NULL, &flash_size_bytes) == ESP_OK) {
        s_dualOtaEnabled = (flash_size_bytes >= 8 * 1024 * 1024);
        ESP_LOGI(TAG_MAIN, "Flash size: %" PRIu32 " bytes (%s OTA)", flash_size_bytes, s_dualOtaEnabled ? "dual" : "single");
    } else {
        ESP_LOGW(TAG_MAIN, "Could not read flash size; defaulting to single OTA");
        s_dualOtaEnabled = false;
    }

    // Configure button input
    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pin_bit_mask = (1ULL << COMMISSION_BUTTON_GPIO);
    io_conf.pull_up_en = GPIO_PULLUP_ENABLE;
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    gpio_config(&io_conf);

    BedService::instance().begin(bedDriver);
#if APP_MATTER
    MatterManager::instance().begin();
    g_led_state = MatterManager::instance().isCommissioned() ? LedState::COMMISSIONED : LedState::IDLE;
#endif
#if !APP_MATTER
    // Use status LED to mirror Wi-Fi provisioning state
    g_led_state = LedState::COMMISSIONING;
    esp_err_t loop_ret = esp_event_loop_create_default();
    if (loop_ret != ESP_OK && loop_ret != ESP_ERR_INVALID_STATE) {
        ESP_LOGW(TAG_MAIN, "Event loop create failed: %s", esp_err_to_name(loop_ret));
    }
    esp_event_handler_instance_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &wifi_status_handler, nullptr, &s_ip_handler);
    esp_event_handler_instance_register(WIFI_EVENT, WIFI_EVENT_STA_DISCONNECTED, &wifi_status_handler, nullptr, &s_disc_handler);
#endif
    net.begin();
    xTaskCreatePinnedToCore(bed_task, "bed_logic", 4096, NULL, 5, NULL, 1);

    xTaskCreatePinnedToCore(button_task, "matter_btn", 3072, NULL, 5, NULL, 1);
    xTaskCreatePinnedToCore(led_task, "matter_led", 3072, NULL, 5, NULL, 1);
}

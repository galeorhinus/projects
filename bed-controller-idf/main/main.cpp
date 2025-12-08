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
#include <inttypes.h>

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

#if APP_MATTER
// LED channels match BedControl
#define LEDC_MODE               LEDC_LOW_SPEED_MODE
#define LEDC_TIMER              LEDC_TIMER_0
#define LEDC_CHANNEL_R          LEDC_CHANNEL_0
#define LEDC_CHANNEL_G          LEDC_CHANNEL_1
#define LEDC_CHANNEL_B          LEDC_CHANNEL_2

enum class LedState {
    IDLE,
    COMMISSIONING,
    COMMISSIONED
};

static LedState g_led_state = LedState::IDLE;

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
        switch (g_led_state) {
            case LedState::IDLE: {
                // slow pulse blue
                uint8_t val = (uint8_t)((sinf(t / 50.0f) + 1.0f) * 60);
                set_led_rgb(0, 0, val);
                break;
            }
            case LedState::COMMISSIONING: {
                // fast blink cyan
                bool on = ((t / 10) % 2) == 0;
                set_led_rgb(0, on ? 120 : 0, on ? 120 : 0);
                break;
            }
            case LedState::COMMISSIONED: {
                // solid green
                set_led_rgb(0, 120, 0);
                break;
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
            while (gpio_get_level((gpio_num_t)COMMISSION_BUTTON_GPIO) == 0) {
                vTaskDelay(pdMS_TO_TICKS(10));
            }
            int64_t dur = (esp_timer_get_time() / 1000) - start;
            if (dur >= longMs) {
                MatterManager::instance().factoryReset();
            } else if (dur >= shortMs) {
                MatterManager::instance().startCommissioning();
                g_led_state = LedState::COMMISSIONING;
            }
        }
        vTaskDelay(pdMS_TO_TICKS(20));
    }
}
#endif  // APP_MATTER

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
    net.begin();
    xTaskCreatePinnedToCore(bed_task, "bed_logic", 4096, NULL, 5, NULL, 1);
#if APP_MATTER
    xTaskCreatePinnedToCore(button_task, "matter_btn", 3072, NULL, 5, NULL, 1);
    xTaskCreatePinnedToCore(led_task, "matter_led", 3072, NULL, 5, NULL, 1);
#endif
}

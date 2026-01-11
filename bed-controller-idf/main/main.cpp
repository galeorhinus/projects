#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "NetworkManager.h"
#ifdef CONFIG_APP_ENABLE_MATTER
#include "MatterManager.h"
#endif
#include "BoardConfig.h"
#include "driver/gpio.h"
#include "driver/ledc.h"
#include "driver/rmt_encoder.h"
#include "driver/rmt_tx.h"
#include "esp_adc/adc_oneshot.h"
#include "esp_adc/adc_cali.h"
#include "esp_adc/adc_cali_scheme.h"
#include "esp_log.h"
#include <math.h>
#include "esp_flash.h"
#include "esp_timer.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "nvs_flash.h"
#include <inttypes.h>
#include <sys/cdefs.h>

#if APP_ROLE_BED
#include "BedControl.h"
#include "BedDriver.h"
#include "BedService.h"

BedControl bed;
BedDriver* bedDriver = &bed;
#endif
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
#define LEDC_DUTY_RES           LEDC_TIMER_8_BIT
#define LEDC_FREQUENCY          5000
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
static rmt_channel_handle_t s_addressable_led_chan = nullptr;
static rmt_encoder_handle_t s_addressable_led_encoder = nullptr;
static bool s_addressable_led_ready = false;
static bool s_addressable_led_grb = ADDRESSABLE_LED_GRB;
static uint8_t s_status_pixel_r = 0;
static uint8_t s_status_pixel_g = 0;
static uint8_t s_status_pixel_b = 0;
#if APP_ROLE_BED && CONFIG_IDF_TARGET_ESP32S3
static adc_oneshot_unit_handle_t s_acs_adc = nullptr;
static adc_cali_handle_t s_acs_cali = nullptr;
static bool s_acs_cali_ready = false;
#endif

typedef struct {
    rmt_encoder_t base;
    rmt_encoder_t* bytes_encoder;
    rmt_encoder_t* copy_encoder;
    int state;
    rmt_symbol_word_t reset_code;
} rmt_led_strip_encoder_t;

IRAM_ATTR static size_t rmt_encode_led_strip(rmt_encoder_t* encoder,
                                             rmt_channel_handle_t channel,
                                             const void* primary_data,
                                             size_t data_size,
                                             rmt_encode_state_t* ret_state) {
    rmt_led_strip_encoder_t* led_encoder = __containerof(encoder, rmt_led_strip_encoder_t, base);
    rmt_encode_state_t session_state = RMT_ENCODING_RESET;
    uint32_t state_flags = 0;
    size_t encoded_symbols = 0;
    switch (led_encoder->state) {
    case 0:
        encoded_symbols += led_encoder->bytes_encoder->encode(
            led_encoder->bytes_encoder, channel, primary_data, data_size, &session_state);
        if (session_state & RMT_ENCODING_COMPLETE) {
            led_encoder->state = 1;
        }
        if (session_state & RMT_ENCODING_MEM_FULL) {
            state_flags |= static_cast<uint32_t>(RMT_ENCODING_MEM_FULL);
            goto out;
        }
        // fall-through
    case 1:
        encoded_symbols += led_encoder->copy_encoder->encode(
            led_encoder->copy_encoder, channel, &led_encoder->reset_code,
            sizeof(led_encoder->reset_code), &session_state);
        if (session_state & RMT_ENCODING_COMPLETE) {
            state_flags |= static_cast<uint32_t>(RMT_ENCODING_COMPLETE);
            led_encoder->state = RMT_ENCODING_RESET;
        }
        if (session_state & RMT_ENCODING_MEM_FULL) {
            state_flags |= static_cast<uint32_t>(RMT_ENCODING_MEM_FULL);
            goto out;
        }
    }
out:
    *ret_state = static_cast<rmt_encode_state_t>(state_flags);
    return encoded_symbols;
}

static esp_err_t rmt_del_led_strip_encoder(rmt_encoder_t* encoder) {
    rmt_led_strip_encoder_t* led_encoder = __containerof(encoder, rmt_led_strip_encoder_t, base);
    rmt_del_encoder(led_encoder->bytes_encoder);
    rmt_del_encoder(led_encoder->copy_encoder);
    free(led_encoder);
    return ESP_OK;
}

static esp_err_t rmt_led_strip_encoder_reset(rmt_encoder_t* encoder) {
    rmt_led_strip_encoder_t* led_encoder = __containerof(encoder, rmt_led_strip_encoder_t, base);
    rmt_encoder_reset(led_encoder->bytes_encoder);
    rmt_encoder_reset(led_encoder->copy_encoder);
    led_encoder->state = RMT_ENCODING_RESET;
    return ESP_OK;
}

static esp_err_t rmt_new_led_strip_encoder(rmt_encoder_handle_t* ret_encoder) {
    rmt_led_strip_encoder_t* led_encoder =
        static_cast<rmt_led_strip_encoder_t*>(rmt_alloc_encoder_mem(sizeof(rmt_led_strip_encoder_t)));
    if (!led_encoder) return ESP_ERR_NO_MEM;
    led_encoder->base.encode = rmt_encode_led_strip;
    led_encoder->base.del = rmt_del_led_strip_encoder;
    led_encoder->base.reset = rmt_led_strip_encoder_reset;
    // WS2812 timing with 10MHz resolution: T0H=0.3us, T0L=0.9us, T1H=0.9us, T1L=0.3us
    rmt_bytes_encoder_config_t bytes_encoder_config = {
        .bit0 = {
            .duration0 = 3,
            .level0 = 1,
            .duration1 = 9,
            .level1 = 0,
        },
        .bit1 = {
            .duration0 = 9,
            .level0 = 1,
            .duration1 = 3,
            .level1 = 0,
        },
    };
    bytes_encoder_config.flags.msb_first = 1;
    esp_err_t err = rmt_new_bytes_encoder(&bytes_encoder_config, &led_encoder->bytes_encoder);
    if (err != ESP_OK) {
        free(led_encoder);
        return err;
    }
    rmt_copy_encoder_config_t copy_encoder_config = {};
    err = rmt_new_copy_encoder(&copy_encoder_config, &led_encoder->copy_encoder);
    if (err != ESP_OK) {
        rmt_del_encoder(led_encoder->bytes_encoder);
        free(led_encoder);
        return err;
    }
    led_encoder->reset_code = (rmt_symbol_word_t){
        .duration0 = 250,
        .level0 = 0,
        .duration1 = 250,
        .level1 = 0,
    };
    *ret_encoder = &led_encoder->base;
    return ESP_OK;
}

static void init_addressable_led() {
    rmt_tx_channel_config_t tx_chan_config = {
        .gpio_num = static_cast<gpio_num_t>(ADDRESSABLE_LED_GPIO),
        .clk_src = RMT_CLK_SRC_DEFAULT,
        .resolution_hz = 10 * 1000 * 1000,
        .mem_block_symbols = 64,
        .trans_queue_depth = 4,
        .flags = { .invert_out = false, .with_dma = false }
    };
    esp_err_t err = rmt_new_tx_channel(&tx_chan_config, &s_addressable_led_chan);
    if (err != ESP_OK) {
        ESP_LOGW(TAG_MAIN, "Addressable LED channel init failed on GPIO %d: %s", ADDRESSABLE_LED_GPIO, esp_err_to_name(err));
        return;
    }
    err = rmt_new_led_strip_encoder(&s_addressable_led_encoder);
    if (err != ESP_OK) {
        ESP_LOGW(TAG_MAIN, "Addressable LED encoder init failed: %s", esp_err_to_name(err));
        return;
    }
    err = rmt_enable(s_addressable_led_chan);
    if (err != ESP_OK) {
        ESP_LOGW(TAG_MAIN, "Addressable LED channel enable failed: %s", esp_err_to_name(err));
        return;
    }
    s_addressable_led_ready = true;
    ESP_LOGI(TAG_MAIN, "Addressable LED initialized on GPIO %d (%s order)",
             ADDRESSABLE_LED_GPIO, s_addressable_led_grb ? "GRB" : "RGB");
    uint8_t off[3] = {0, 0, 0};
    rmt_transmit_config_t tx_cfg = {.loop_count = 0};
    rmt_transmit(s_addressable_led_chan, s_addressable_led_encoder, off, sizeof(off), &tx_cfg);
    rmt_tx_wait_all_done(s_addressable_led_chan, pdMS_TO_TICKS(100));
}

static inline void addressable_led_write_pixel(uint8_t* payload, size_t offset, uint8_t r, uint8_t g, uint8_t b) {
    if (s_addressable_led_grb) {
        payload[offset] = g;
        payload[offset + 1] = r;
        payload[offset + 2] = b;
    } else {
        payload[offset] = r;
        payload[offset + 1] = g;
        payload[offset + 2] = b;
    }
}

static void set_addressable_led(uint8_t r, uint8_t g, uint8_t b) {
    static bool s_logged_not_ready = false;
    if (!s_addressable_led_ready) {
        if (!s_logged_not_ready) {
            ESP_LOGW(TAG_MAIN, "Addressable LED not ready; skipping updates");
            s_logged_not_ready = true;
        }
        return;
    }
    uint8_t payload[3] = {0, 0, 0};
    addressable_led_write_pixel(payload, 0, r, g, b);
    rmt_transmit_config_t tx_cfg = {.loop_count = 0};
    rmt_transmit(s_addressable_led_chan, s_addressable_led_encoder, payload, sizeof(payload), &tx_cfg);
    rmt_tx_wait_all_done(s_addressable_led_chan, pdMS_TO_TICKS(100));
}

extern "C" void addressable_led_set_order(bool grb) {
    s_addressable_led_grb = grb;
    ESP_LOGI(TAG_MAIN, "Addressable LED order set to %s", grb ? "GRB" : "RGB");
    set_addressable_led(s_status_pixel_r, s_status_pixel_g, s_status_pixel_b);
}

extern "C" bool addressable_led_fill_strip(uint8_t r, uint8_t g, uint8_t b, uint16_t count) {
    if (!s_addressable_led_ready) {
        ESP_LOGW(TAG_MAIN, "Addressable LED not ready; strip update skipped");
        return false;
    }
    size_t total_pixels = static_cast<size_t>(count) + 1; // pixel 0 is status
    size_t buf_len = total_pixels * 3;
    uint8_t* payload = static_cast<uint8_t*>(malloc(buf_len));
    if (!payload) {
        ESP_LOGW(TAG_MAIN, "Addressable strip alloc failed (%u px)", (unsigned)total_pixels);
        return false;
    }
    auto write_pixel = [&](size_t idx, uint8_t pr, uint8_t pg, uint8_t pb) {
        addressable_led_write_pixel(payload, idx * 3, pr, pg, pb);
    };
    write_pixel(0, s_status_pixel_r, s_status_pixel_g, s_status_pixel_b);
    for (size_t i = 1; i < total_pixels; i++) {
        write_pixel(i, r, g, b);
    }
    rmt_transmit_config_t tx_cfg = {.loop_count = 0};
    rmt_transmit(s_addressable_led_chan, s_addressable_led_encoder, payload, buf_len, &tx_cfg);
    rmt_tx_wait_all_done(s_addressable_led_chan, pdMS_TO_TICKS(200));
    free(payload);
    return true;
}

extern "C" bool addressable_led_chase(uint8_t r, uint8_t g, uint8_t b, uint16_t count, uint16_t steps, uint16_t delay_ms) {
    if (!s_addressable_led_ready) {
        ESP_LOGW(TAG_MAIN, "Addressable LED not ready; chase skipped");
        return false;
    }
    if (count == 0 || steps == 0) {
        return false;
    }
    size_t total_pixels = static_cast<size_t>(count) + 1;
    size_t buf_len = total_pixels * 3;
    uint8_t* payload = static_cast<uint8_t*>(malloc(buf_len));
    if (!payload) {
        ESP_LOGW(TAG_MAIN, "Addressable chase alloc failed (%u px)", (unsigned)total_pixels);
        return false;
    }
    auto write_pixel = [&](size_t idx, uint8_t pr, uint8_t pg, uint8_t pb) {
        addressable_led_write_pixel(payload, idx * 3, pr, pg, pb);
    };
    rmt_transmit_config_t tx_cfg = {.loop_count = 0};
    size_t active_count = total_pixels - 1;
    for (uint16_t step = 0; step < steps; ++step) {
        size_t lit = 1 + (step % active_count);
        write_pixel(0, s_status_pixel_r, s_status_pixel_g, s_status_pixel_b);
        for (size_t i = 1; i < total_pixels; i++) {
            if (i == lit) {
                write_pixel(i, r, g, b);
            } else {
                write_pixel(i, 0, 0, 0);
            }
        }
        rmt_transmit(s_addressable_led_chan, s_addressable_led_encoder, payload, buf_len, &tx_cfg);
        rmt_tx_wait_all_done(s_addressable_led_chan, pdMS_TO_TICKS(200));
        if (delay_ms > 0) {
            vTaskDelay(pdMS_TO_TICKS(delay_ms));
        }
    }
    free(payload);
    return true;
}

extern "C" bool addressable_led_wipe(uint8_t r, uint8_t g, uint8_t b, uint16_t count, uint16_t delay_ms) {
    if (!s_addressable_led_ready) {
        ESP_LOGW(TAG_MAIN, "Addressable LED not ready; wipe skipped");
        return false;
    }
    if (count == 0) return false;
    size_t total_pixels = static_cast<size_t>(count) + 1;
    size_t buf_len = total_pixels * 3;
    uint8_t* payload = static_cast<uint8_t*>(malloc(buf_len));
    if (!payload) {
        ESP_LOGW(TAG_MAIN, "Addressable wipe alloc failed (%u px)", (unsigned)total_pixels);
        return false;
    }
    auto write_pixel = [&](size_t idx, uint8_t pr, uint8_t pg, uint8_t pb) {
        addressable_led_write_pixel(payload, idx * 3, pr, pg, pb);
    };
    rmt_transmit_config_t tx_cfg = {.loop_count = 0};
    for (size_t lit = 1; lit < total_pixels; ++lit) {
        write_pixel(0, s_status_pixel_r, s_status_pixel_g, s_status_pixel_b);
        for (size_t i = 1; i < total_pixels; i++) {
            if (i <= lit) {
                write_pixel(i, r, g, b);
            } else {
                write_pixel(i, 0, 0, 0);
            }
        }
        rmt_transmit(s_addressable_led_chan, s_addressable_led_encoder, payload, buf_len, &tx_cfg);
        rmt_tx_wait_all_done(s_addressable_led_chan, pdMS_TO_TICKS(200));
        if (delay_ms > 0) {
            vTaskDelay(pdMS_TO_TICKS(delay_ms));
        }
    }
    free(payload);
    return true;
}

extern "C" bool addressable_led_pulse(uint8_t r, uint8_t g, uint8_t b, uint16_t count, uint16_t steps, uint16_t delay_ms) {
    if (!s_addressable_led_ready) {
        ESP_LOGW(TAG_MAIN, "Addressable LED not ready; pulse skipped");
        return false;
    }
    if (count == 0 || steps == 0) return false;
    size_t total_pixels = static_cast<size_t>(count) + 1;
    size_t buf_len = total_pixels * 3;
    uint8_t* payload = static_cast<uint8_t*>(malloc(buf_len));
    if (!payload) {
        ESP_LOGW(TAG_MAIN, "Addressable pulse alloc failed (%u px)", (unsigned)total_pixels);
        return false;
    }
    auto write_pixel = [&](size_t idx, uint8_t pr, uint8_t pg, uint8_t pb) {
        addressable_led_write_pixel(payload, idx * 3, pr, pg, pb);
    };
    rmt_transmit_config_t tx_cfg = {.loop_count = 0};
    uint16_t half = steps / 2;
    if (half == 0) half = 1;
    for (uint16_t step = 0; step < steps; ++step) {
        uint16_t phase = (step <= half) ? step : (steps - 1 - step);
        uint32_t intensity = (static_cast<uint32_t>(phase) * 255u) / half;
        uint8_t pr = static_cast<uint8_t>((static_cast<uint32_t>(r) * intensity) / 255u);
        uint8_t pg = static_cast<uint8_t>((static_cast<uint32_t>(g) * intensity) / 255u);
        uint8_t pb = static_cast<uint8_t>((static_cast<uint32_t>(b) * intensity) / 255u);
        write_pixel(0, s_status_pixel_r, s_status_pixel_g, s_status_pixel_b);
        for (size_t i = 1; i < total_pixels; i++) {
            write_pixel(i, pr, pg, pb);
        }
        rmt_transmit(s_addressable_led_chan, s_addressable_led_encoder, payload, buf_len, &tx_cfg);
        rmt_tx_wait_all_done(s_addressable_led_chan, pdMS_TO_TICKS(200));
        if (delay_ms > 0) {
            vTaskDelay(pdMS_TO_TICKS(delay_ms));
        }
    }
    free(payload);
    return true;
}

static void hsv_to_rgb(uint8_t hue, uint8_t sat, uint8_t val, uint8_t *r, uint8_t *g, uint8_t *b) {
    if (sat == 0) {
        *r = val;
        *g = val;
        *b = val;
        return;
    }
    uint8_t region = hue / 43;
    uint8_t remainder = (hue - (region * 43)) * 6;
    uint8_t p = (val * (255 - sat)) >> 8;
    uint8_t q = (val * (255 - ((sat * remainder) >> 8))) >> 8;
    uint8_t t = (val * (255 - ((sat * (255 - remainder)) >> 8))) >> 8;
    switch (region) {
    case 0:
        *r = val; *g = t; *b = p;
        break;
    case 1:
        *r = q; *g = val; *b = p;
        break;
    case 2:
        *r = p; *g = val; *b = t;
        break;
    case 3:
        *r = p; *g = q; *b = val;
        break;
    case 4:
        *r = t; *g = p; *b = val;
        break;
    default:
        *r = val; *g = p; *b = q;
        break;
    }
}

extern "C" bool addressable_led_rainbow(uint16_t count, uint16_t steps, uint16_t delay_ms, uint8_t brightness) {
    if (!s_addressable_led_ready) {
        ESP_LOGW(TAG_MAIN, "Addressable LED not ready; rainbow skipped");
        return false;
    }
    if (count == 0 || steps == 0) return false;
    size_t total_pixels = static_cast<size_t>(count) + 1;
    size_t buf_len = total_pixels * 3;
    uint8_t* payload = static_cast<uint8_t*>(malloc(buf_len));
    if (!payload) {
        ESP_LOGW(TAG_MAIN, "Addressable rainbow alloc failed (%u px)", (unsigned)total_pixels);
        return false;
    }
    auto write_pixel = [&](size_t idx, uint8_t pr, uint8_t pg, uint8_t pb) {
        addressable_led_write_pixel(payload, idx * 3, pr, pg, pb);
    };
    rmt_transmit_config_t tx_cfg = {.loop_count = 0};
    uint8_t val = static_cast<uint8_t>((static_cast<uint32_t>(brightness) * 255u) / 100u);
    size_t active_count = total_pixels - 1;
    for (uint16_t step = 0; step < steps; ++step) {
        uint8_t shift = static_cast<uint8_t>((static_cast<uint32_t>(step) * 255u) / steps);
        write_pixel(0, s_status_pixel_r, s_status_pixel_g, s_status_pixel_b);
        for (size_t i = 1; i < total_pixels; ++i) {
            uint8_t hue = static_cast<uint8_t>((static_cast<uint32_t>(i - 1) * 255u) / active_count);
            hue = static_cast<uint8_t>(hue + shift);
            uint8_t pr = 0, pg = 0, pb = 0;
            hsv_to_rgb(hue, 255, val, &pr, &pg, &pb);
            write_pixel(i, pr, pg, pb);
        }
        rmt_transmit(s_addressable_led_chan, s_addressable_led_encoder, payload, buf_len, &tx_cfg);
        rmt_tx_wait_all_done(s_addressable_led_chan, pdMS_TO_TICKS(200));
        if (delay_ms > 0) {
            vTaskDelay(pdMS_TO_TICKS(delay_ms));
        }
    }
    free(payload);
    return true;
}

static void init_status_led_hw() {
    ledc_timer_config_t ledc_timer = {
        .speed_mode       = LEDC_MODE,
        .duty_resolution  = LEDC_DUTY_RES,
        .timer_num        = LEDC_TIMER,
        .freq_hz          = LEDC_FREQUENCY,
        .clk_cfg          = LEDC_AUTO_CLK,
        .deconfigure      = false
    };
    esp_err_t err = ledc_timer_config(&ledc_timer);
    if (err != ESP_OK) {
        ESP_LOGE(TAG_MAIN, "LED timer config failed: %s", esp_err_to_name(err));
        return;
    }
    ledc_channel_config_t c0 = { .gpio_num = LED_PIN_R, .speed_mode = LEDC_MODE, .channel = LEDC_CHANNEL_R, .intr_type = LEDC_INTR_DISABLE, .timer_sel = LEDC_TIMER, .duty = 0, .hpoint = 0, .flags = {} };
    ledc_channel_config_t c1 = { .gpio_num = LED_PIN_G, .speed_mode = LEDC_MODE, .channel = LEDC_CHANNEL_G, .intr_type = LEDC_INTR_DISABLE, .timer_sel = LEDC_TIMER, .duty = 0, .hpoint = 0, .flags = {} };
    ledc_channel_config_t c2 = { .gpio_num = LED_PIN_B, .speed_mode = LEDC_MODE, .channel = LEDC_CHANNEL_B, .intr_type = LEDC_INTR_DISABLE, .timer_sel = LEDC_TIMER, .duty = 0, .hpoint = 0, .flags = {} };
    ledc_channel_config(&c0);
    ledc_channel_config(&c1);
    ledc_channel_config(&c2);
    ESP_LOGI(TAG_MAIN, "Status LED LEDC initialized");
    init_addressable_led();
}

#if APP_ROLE_BED && CONFIG_IDF_TARGET_ESP32S3
static void init_acs712_adc() {
    adc_oneshot_unit_init_cfg_t unit_cfg = {
        .unit_id = ADC_UNIT_1,
        .clk_src = ADC_RTC_CLK_SRC_DEFAULT,
        .ulp_mode = ADC_ULP_MODE_DISABLE
    };
    esp_err_t err = adc_oneshot_new_unit(&unit_cfg, &s_acs_adc);
    if (err != ESP_OK) {
        ESP_LOGW(TAG_MAIN, "ACS712 ADC unit init failed: %s", esp_err_to_name(err));
        return;
    }
    adc_oneshot_chan_cfg_t chan_cfg = {
        .atten = ADC_ATTEN_DB_11,
        .bitwidth = ADC_BITWIDTH_DEFAULT
    };
    err = adc_oneshot_config_channel(s_acs_adc, ADC_CHANNEL_1, &chan_cfg);
    if (err != ESP_OK) {
        ESP_LOGW(TAG_MAIN, "ACS712 ADC channel config failed: %s", esp_err_to_name(err));
        return;
    }
#if ADC_CALI_SCHEME_CURVE_FITTING_SUPPORTED
    adc_cali_curve_fitting_config_t cali_cfg = {
        .unit_id = ADC_UNIT_1,
        .chan = ADC_CHANNEL_1,
        .atten = ADC_ATTEN_DB_11,
        .bitwidth = ADC_BITWIDTH_DEFAULT
    };
    err = adc_cali_create_scheme_curve_fitting(&cali_cfg, &s_acs_cali);
    if (err == ESP_OK) {
        s_acs_cali_ready = true;
    }
#elif ADC_CALI_SCHEME_LINE_FITTING_SUPPORTED
    adc_cali_line_fitting_config_t cali_cfg = {
        .unit_id = ADC_UNIT_1,
        .chan = ADC_CHANNEL_1,
        .atten = ADC_ATTEN_DB_11,
        .bitwidth = ADC_BITWIDTH_DEFAULT
    };
    err = adc_cali_create_scheme_line_fitting(&cali_cfg, &s_acs_cali);
    if (err == ESP_OK) {
        s_acs_cali_ready = true;
    }
#endif
    ESP_LOGI(TAG_MAIN, "ACS712 ADC ready on GPIO2 (ADC1_CH1)%s",
             s_acs_cali_ready ? " with calibration" : "");
}

static void acs712_log_task(void* pv) {
    const TickType_t delay = pdMS_TO_TICKS(200);
    const int kActiveOnMv = 30;
    const int kActiveOffMv = 20;
    const int64_t kIdleConfirmUs = 300 * 1000;
    const float kEmaAlpha = 0.25f;
    bool baseline_ready = false;
    float ema_mv = 0.0f;
    float baseline_mv = 0.0f;
    bool last_active = false;
    int64_t idle_since_us = 0;
    while (1) {
        if (s_acs_adc) {
            int raw = 0;
            if (adc_oneshot_read(s_acs_adc, ADC_CHANNEL_1, &raw) == ESP_OK) {
                if (s_acs_cali_ready) {
                    int mv = 0;
                    if (adc_cali_raw_to_voltage(s_acs_cali, raw, &mv) == ESP_OK) {
                        ema_mv = baseline_ready ? (kEmaAlpha * mv + (1.0f - kEmaAlpha) * ema_mv) : (float)mv;
                        if (!baseline_ready) {
                            baseline_mv = ema_mv;
                            baseline_ready = true;
                        }
                        float delta_mv = ema_mv - baseline_mv;
                        const int64_t now_us = esp_timer_get_time();
                        bool active = last_active ? (delta_mv > kActiveOffMv) : (delta_mv > kActiveOnMv);
                        if (last_active && !active) {
                            if (idle_since_us == 0) {
                                idle_since_us = now_us;
                            }
                            if (now_us - idle_since_us < kIdleConfirmUs) {
                                active = true;
                            }
                        } else if (active) {
                            idle_since_us = 0;
                        } else {
                            idle_since_us = 0;
                        }
                        if (!active) {
                            // Slowly track baseline when idle.
                            baseline_mv = 0.98f * baseline_mv + 0.02f * ema_mv;
                        }
                        if (active != last_active) {
                            ESP_LOGI(TAG_MAIN, "ACS712 state=%s mv=%.1f baseline=%.1f delta=%.1f raw=%d",
                                     active ? "ACTIVE" : "IDLE", ema_mv, baseline_mv, delta_mv, raw);
                            last_active = active;
                        }
                    } else {
                        ESP_LOGI(TAG_MAIN, "ACS712 raw=%d", raw);
                    }
                } else {
                    ESP_LOGI(TAG_MAIN, "ACS712 raw=%d", raw);
                }
            }
        }
        vTaskDelay(delay);
    }
}
#endif

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
    s_status_pixel_r = r;
    s_status_pixel_g = g;
    s_status_pixel_b = b;
    set_addressable_led(r, g, b);
}

static void status_led_boot_test() {
    set_led_rgb(255, 0, 0);
    vTaskDelay(pdMS_TO_TICKS(120));
    set_led_rgb(0, 255, 0);
    vTaskDelay(pdMS_TO_TICKS(120));
    set_led_rgb(0, 0, 255);
    vTaskDelay(pdMS_TO_TICKS(120));
    set_led_rgb(0, 0, 0);
}

static void led_task(void* pv) {
    uint32_t t = 0;
    LedState last_state = g_led_state;
    bool last_override = false;
    bool last_blink_on = false;
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
                    uint8_t v = on ? 7 : 0;
                    set_led_rgb(v, v, v);
                    last_blink_on = on;
                    break;
                }
                case LedState::COMMISSIONING: { // spec: fast blink during commissioning
                    bool on = ((t / 2) % 2) == 0; // 5 Hz, 50% duty
                    uint8_t v = on ? 7 : 0;
                    set_led_rgb(v, v, 0);
                    last_blink_on = on;
                    break;
                }
                case LedState::COMMISSIONED: { // spec: solid when provisioned
                    set_led_rgb(0, 16, 0);
                    break;
                }
                case LedState::RESETTING: { // fault/reset: red blink
                    bool on = ((t / 4) % 2) == 0;
                    uint8_t v = on ? 11 : 0;
                    set_led_rgb(v, 0, 0);
                    last_blink_on = on;
                    break;
                }
            }
        }

        if (last_override != applied_override) {
            last_override = applied_override;
        }
        if (last_state != g_led_state) {
            last_state = g_led_state;
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
    } else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        g_led_state = LedState::IDLE;
    }
}
#endif

#if APP_ROLE_BED
void bed_task(void *pvParameter) {
    while (1) {
        bedDriver->update();
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}
#endif

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
#if APP_ROLE_BED
    ESP_LOGI(TAG_MAIN, "Role: bed (bed_control enabled)");
#else
    ESP_LOGI(TAG_MAIN, "Role: non-bed (bed_control excluded)");
#endif

    ESP_LOGI(TAG_MAIN, "Status LED init");
    init_status_led_hw();
    status_led_boot_test();
#if APP_ROLE_BED && CONFIG_IDF_TARGET_ESP32S3
    init_acs712_adc();
#endif

    // Configure button input
    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pin_bit_mask = (1ULL << COMMISSION_BUTTON_GPIO);
    io_conf.pull_up_en = GPIO_PULLUP_ENABLE;
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    gpio_config(&io_conf);

    net.begin();
#if !APP_MATTER
    if (!APP_ROLE_BED) {
        // Use status LED to mirror Wi-Fi provisioning state (light build)
        g_led_state = LedState::COMMISSIONING;
        esp_err_t loop_ret = esp_event_loop_create_default();
        if (loop_ret != ESP_OK && loop_ret != ESP_ERR_INVALID_STATE) {
            ESP_LOGW(TAG_MAIN, "Event loop create failed: %s", esp_err_to_name(loop_ret));
        }
        esp_event_handler_instance_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &wifi_status_handler, nullptr, &s_ip_handler);
        esp_event_handler_instance_register(WIFI_EVENT, WIFI_EVENT_STA_DISCONNECTED, &wifi_status_handler, nullptr, &s_disc_handler);
    }
#endif
#if APP_ROLE_BED
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
    xTaskCreatePinnedToCore(bed_task, "bed_logic", 4096, NULL, 5, NULL, 1);
#endif

    xTaskCreatePinnedToCore(button_task, "matter_btn", 3072, NULL, 5, NULL, 1);
    BaseType_t led_task_ok = xTaskCreatePinnedToCore(led_task, "matter_led", 3072, NULL, 5, NULL, 1);
    if (led_task_ok != pdPASS) {
        ESP_LOGE(TAG_MAIN, "LED task create failed: %ld", (long)led_task_ok);
    }
#if APP_ROLE_BED && CONFIG_IDF_TARGET_ESP32S3
    xTaskCreatePinnedToCore(acs712_log_task, "acs712_log", 3072, NULL, 5, NULL, 1);
#endif

    // Keep app_main alive; avoid returning to main_task
    for (;;) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

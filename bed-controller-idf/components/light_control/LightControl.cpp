#include "LightControl.h"
#include "driver/ledc.h"
#include "esp_log.h"

static const char *TAG_LIGHT = "LIGHT_CTRL";
static const ledc_mode_t kLightSpeedMode = LEDC_LOW_SPEED_MODE;
static const ledc_timer_t kLightTimer = LEDC_TIMER_2;
static const ledc_channel_t kLightChannel = LEDC_CHANNEL_7;
static const ledc_timer_bit_t kLightDutyResolution = LEDC_TIMER_13_BIT;
static const uint32_t kLightFreqHz = 5000;

LightControl::LightControl()
    : pin_(GPIO_NUM_NC),
      activeHigh_(true),
      state_(false),
      initialized_(false),
      brightness_(0),
      last_nonzero_brightness_(100) {}

esp_err_t LightControl::begin(gpio_num_t pin, bool activeHigh) {
    pin_ = pin;
    activeHigh_ = activeHigh;

    ledc_timer_config_t timer_cfg = {};
    timer_cfg.speed_mode = kLightSpeedMode;
    timer_cfg.timer_num = kLightTimer;
    timer_cfg.duty_resolution = kLightDutyResolution;
    timer_cfg.freq_hz = kLightFreqHz;
    timer_cfg.clk_cfg = LEDC_AUTO_CLK;
    esp_err_t err = ledc_timer_config(&timer_cfg);
    if (err != ESP_OK) {
        ESP_LOGE(TAG_LIGHT, "ledc_timer_config failed: %s", esp_err_to_name(err));
        initialized_ = false;
        return err;
    }

    ledc_channel_config_t channel_cfg = {};
    channel_cfg.speed_mode = kLightSpeedMode;
    channel_cfg.channel = kLightChannel;
    channel_cfg.timer_sel = kLightTimer;
    channel_cfg.intr_type = LEDC_INTR_DISABLE;
    channel_cfg.gpio_num = pin_;
    channel_cfg.duty = 0;
    channel_cfg.hpoint = 0;
    err = ledc_channel_config(&channel_cfg);
    if (err != ESP_OK) {
        ESP_LOGE(TAG_LIGHT, "ledc_channel_config failed: %s", esp_err_to_name(err));
        initialized_ = false;
        return err;
    }
    initialized_ = true;
    setBrightness(0);
    ESP_LOGI(TAG_LIGHT, "Initialized light PWM GPIO %d (active %s)", pin_, activeHigh_ ? "high" : "low");
    return ESP_OK;
}

void LightControl::setState(bool on) {
    if (!initialized_) return;
    if (on) {
        if (brightness_ == 0) {
            setBrightness(last_nonzero_brightness_ > 0 ? last_nonzero_brightness_ : 100);
        } else {
            setBrightness(brightness_);
        }
    } else {
        if (brightness_ > 0) {
            last_nonzero_brightness_ = brightness_;
        }
        setBrightness(0);
    }
}

void LightControl::toggle() {
    setState(!state_);
}

void LightControl::setBrightness(uint8_t percent) {
    if (!initialized_) return;
    if (percent > 100) percent = 100;
    brightness_ = percent;
    if (percent > 0) {
        last_nonzero_brightness_ = percent;
    }
    state_ = (percent > 0);
    uint32_t max_duty = (1u << kLightDutyResolution) - 1;
    uint32_t duty = (max_duty * percent) / 100;
    if (!activeHigh_) {
        duty = max_duty - duty;
    }
    ledc_set_duty(kLightSpeedMode, kLightChannel, duty);
    ledc_update_duty(kLightSpeedMode, kLightChannel);
    ESP_LOGI(TAG_LIGHT, "Light brightness %u%% (GPIO %d)", percent, pin_);
}

void LightControl::setLastNonzeroBrightness(uint8_t percent) {
    if (percent > 100) percent = 100;
    last_nonzero_brightness_ = percent;
}

uint8_t LightControl::getBrightness() const {
    return brightness_;
}

bool LightControl::getState() const {
    return state_;
}

gpio_num_t LightControl::getPin() const {
    return pin_;
}

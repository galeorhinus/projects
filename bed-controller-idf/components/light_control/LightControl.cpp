#include "LightControl.h"
#include "esp_log.h"

static const char *TAG_LIGHT = "LIGHT_CTRL";

LightControl::LightControl()
    : pin_(GPIO_NUM_NC), activeHigh_(true), state_(false), initialized_(false) {}

esp_err_t LightControl::begin(gpio_num_t pin, bool activeHigh) {
    pin_ = pin;
    activeHigh_ = activeHigh;

    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = (1ULL << pin_);
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE;
    esp_err_t err = gpio_config(&io_conf);
    if (err != ESP_OK) {
        ESP_LOGE(TAG_LIGHT, "gpio_config failed: %s", esp_err_to_name(err));
        initialized_ = false;
        return err;
    }
    initialized_ = true;
    setState(false);
    ESP_LOGI(TAG_LIGHT, "Initialized light GPIO %d (active %s)", pin_, activeHigh_ ? "high" : "low");
    return ESP_OK;
}

void LightControl::setState(bool on) {
    if (!initialized_) return;
    state_ = on;
    int level = activeHigh_ ? (on ? 1 : 0) : (on ? 0 : 1);
    gpio_set_level(pin_, level);
    ESP_LOGI(TAG_LIGHT, "Light %s (GPIO %d)", on ? "ON" : "OFF", pin_);
}

void LightControl::toggle() {
    setState(!state_);
}

bool LightControl::getState() const {
    return state_;
}

gpio_num_t LightControl::getPin() const {
    return pin_;
}

#pragma once

#include "driver/gpio.h"
#include "esp_err.h"

class LightControl {
public:
    LightControl();
    esp_err_t begin(gpio_num_t pin, bool activeHigh = true);
    void setState(bool on);
    void toggle();
    void setBrightness(uint8_t percent);
    uint8_t getBrightness() const;
    bool getState() const;
    gpio_num_t getPin() const;

private:
    gpio_num_t pin_;
    bool activeHigh_;
    bool state_;
    bool initialized_;
    uint8_t brightness_;
    uint8_t last_nonzero_brightness_;
};

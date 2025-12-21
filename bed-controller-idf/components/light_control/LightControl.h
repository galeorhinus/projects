#pragma once

#include "driver/gpio.h"
#include "esp_err.h"

class LightControl {
public:
    LightControl();
    esp_err_t begin(gpio_num_t pin, bool activeHigh = true);
    void setState(bool on);
    void toggle();
    bool getState() const;
    gpio_num_t getPin() const;

private:
    gpio_num_t pin_;
    bool activeHigh_;
    bool state_;
    bool initialized_;
};

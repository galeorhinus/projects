#pragma once

#include "BoardConfig.h"

// Light control (single GPIO, active-high by default)
#if CONFIG_IDF_TARGET_ESP32
#define LIGHT_GPIO        32
#define LIGHT_RGB_GPIO_R  4
#define LIGHT_RGB_GPIO_G  5
#define LIGHT_RGB_GPIO_B  21
#elif CONFIG_IDF_TARGET_ESP32S3
#define LIGHT_GPIO        21
#define LIGHT_RGB_GPIO_R  13
#define LIGHT_RGB_GPIO_G  14
#define LIGHT_RGB_GPIO_B  18
#else
#error "Unsupported IDF target for light pin mapping"
#endif

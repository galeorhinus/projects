#pragma once

#include "BoardConfig.h"

// Light control (single GPIO, active-high by default)
#if CONFIG_IDF_TARGET_ESP32
#define LIGHT_GPIO        32
#elif CONFIG_IDF_TARGET_ESP32S3
#define LIGHT_GPIO        21
#else
#error "Unsupported IDF target for light pin mapping"
#endif

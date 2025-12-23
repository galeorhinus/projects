#pragma once

#include "BoardConfig.h"

// --- PINS ---
#if CONFIG_IDF_TARGET_ESP32
// ESP32 (classic) safe pins (avoid flash pins 6-11 and strapping pins for outputs)
#if CONFIG_SPIRAM
// ESP32 WROVER: GPIO16/17 are used by PSRAM, so avoid them.
#define HEAD_UP_PIN       21
#define HEAD_DOWN_PIN     22
#define FOOT_UP_PIN       18
#define FOOT_DOWN_PIN     19

#define TRANSFER_PIN      23  // single control for all transfer relays
#else
#define HEAD_UP_PIN       16
#define HEAD_DOWN_PIN     17
#define FOOT_UP_PIN       18
#define FOOT_DOWN_PIN     19

#define TRANSFER_PIN      23  // single control for all transfer relays
#endif

// Optocoupler inputs (input-only pins)
#define OPTO_IN_1         34
#define OPTO_IN_2         35
#define OPTO_IN_3         36
#define OPTO_IN_4         39

#elif CONFIG_IDF_TARGET_ESP32S3
// ESP32-S3 pinout (safe GPIOs; avoid USB D+/D-, strapping pins)
#define HEAD_UP_PIN       4
#define HEAD_DOWN_PIN     5
#define FOOT_UP_PIN       6
#define FOOT_DOWN_PIN     7

#define TRANSFER_PIN      10  // single control for all transfer relays

// Optocoupler inputs (remote sense)
#define OPTO_IN_1         35
#define OPTO_IN_2         36
#define OPTO_IN_3         37
#define OPTO_IN_4         38
#else
#error "Unsupported IDF target for bed pin mapping"
#endif

// Motor PWM (DRV8871)
#define MOTOR_PWM_FREQ_HZ   20000
#define MOTOR_PWM_DUTY_MAX  1023  // 10-bit
#define MOTOR_PWM_RAMP_STEP 64
#define MOTOR_PWM_TIMER     LEDC_TIMER_1

// --- LOGIC ---
#define RELAY_ON          0
#define RELAY_OFF         1

#define HEAD_MAX_MS_DEFAULT 25000
#define FOOT_MAX_MS_DEFAULT 40000
#define LIMIT_MIN_MS        5000    // Prevent unrealistically low limits
#define LIMIT_MAX_MS        60000   // Prevent runaway high limits
#define SYNC_EXTRA_MS     10000

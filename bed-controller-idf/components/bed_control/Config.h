#pragma once

#define DEBUG_LEVEL 1

// --- WIFI ---
#define WIFI_SSID         "galeasus24"
#define WIFI_PASS         "galeasus2.4"
#define MDNS_HOSTNAME     "elev8"

#ifdef CONFIG_APP_ROLE_BED
#define APP_ROLE_BED 1
#else
#define APP_ROLE_BED 0
#endif

#ifdef CONFIG_APP_ROLE_LIGHT
#define APP_ROLE_LIGHT 1
#else
#define APP_ROLE_LIGHT 0
#endif

#ifdef CONFIG_APP_ROLE_TRAY
#define APP_ROLE_TRAY 1
#else
#define APP_ROLE_TRAY 0
#endif

// --- PINS ---
#if CONFIG_IDF_TARGET_ESP32
// ESP32 (classic) safe pins (avoid flash pins 6-11 and strapping pins for outputs)
#define HEAD_UP_PIN       16
#define HEAD_DOWN_PIN     17
#define FOOT_UP_PIN       18
#define FOOT_DOWN_PIN     19

#define TRANSFER_PIN      23  // single control for all transfer relays

// Optocoupler inputs (input-only pins)
#define OPTO_IN_1         34
#define OPTO_IN_2         35
#define OPTO_IN_3         36
#define OPTO_IN_4         39

// Light control (single GPIO, active-high by default)
#define LIGHT_GPIO        32

// --- LEDS --- (LEDC capable GPIOs)
#define LED_PIN_R         25
#define LED_PIN_G         26
#define LED_PIN_B         27
#define LED_COMMON_ANODE  1

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

// Light control (single GPIO, active-high by default)
#define LIGHT_GPIO        21

// --- LEDS --- (LEDC capable GPIOs)
#define LED_PIN_R         15
#define LED_PIN_G         16
#define LED_PIN_B         17
#define LED_COMMON_ANODE  1
#else
#error "Unsupported IDF target for pin mapping"
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

// --- Provisioning / Matter toggles ---
#ifdef CONFIG_APP_ENABLE_MATTER
#define ENABLE_MATTER 1
#else
#define ENABLE_MATTER 0
#endif
#ifndef ENABLE_HTTP_PROVISIONING
#define ENABLE_HTTP_PROVISIONING 1
#endif

// Hardware hooks for commissioning / reset (adjust pins as wired)
#define COMMISSION_BUTTON_GPIO 0
#define COMMISSION_LED_R       LED_PIN_R
#define COMMISSION_LED_G       LED_PIN_G
#define COMMISSION_LED_B       LED_PIN_B

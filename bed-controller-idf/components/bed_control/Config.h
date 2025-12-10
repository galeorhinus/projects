#pragma once

#define DEBUG_LEVEL 1

// --- WIFI ---
#define WIFI_SSID         "galeasus24"
#define WIFI_PASS         "galeasus2.4"
#define MDNS_HOSTNAME     "elev8"

// --- PINS ---
// ESP32-S3 pinout (safe GPIOs; avoid USB D+/D-, strapping pins)
#define HEAD_UP_PIN       4
#define HEAD_DOWN_PIN     5
#define FOOT_UP_PIN       6
#define FOOT_DOWN_PIN     7

#define TRANSFER_PIN_1    9
#define TRANSFER_PIN_2    10
#define TRANSFER_PIN_3    11
#define TRANSFER_PIN_4    12

// --- LEDS --- (LEDC capable GPIOs)
#define LED_PIN_R         15
#define LED_PIN_G         16
#define LED_PIN_B         17
#define LED_COMMON_ANODE  1 

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

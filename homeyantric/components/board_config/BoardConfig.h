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

// --- LEDS / Commissioning ---
#if CONFIG_IDF_TARGET_ESP32
// ESP32 (classic) safe pins (avoid flash pins 6-11 and strapping pins for outputs)
#define LED_PIN_R         25
#define LED_PIN_G         26
#define LED_PIN_B         27
#define LED_COMMON_ANODE  1
#define ADDRESSABLE_LED_GPIO 13
#define ADDRESSABLE_LED_GRB 1
#elif CONFIG_IDF_TARGET_ESP32S3
// ESP32-S3 pinout (safe GPIOs; avoid USB D+/D-, strapping pins)
#define LED_PIN_R         15
#define LED_PIN_G         16
#define LED_PIN_B         17
#define LED_COMMON_ANODE  1
#define ADDRESSABLE_LED_GPIO 8
#define ADDRESSABLE_LED_GRB 1
#else
#error "Unsupported IDF target for board config"
#endif

// Hardware hooks for commissioning / reset (adjust pins as wired)
#define COMMISSION_BUTTON_GPIO 0
#define COMMISSION_LED_R       LED_PIN_R
#define COMMISSION_LED_G       LED_PIN_G
#define COMMISSION_LED_B       LED_PIN_B

// --- Provisioning / Matter toggles ---
#ifdef CONFIG_APP_ENABLE_MATTER
#define ENABLE_MATTER 1
#else
#define ENABLE_MATTER 0
#endif
#ifndef ENABLE_HTTP_PROVISIONING
#define ENABLE_HTTP_PROVISIONING 1
#endif

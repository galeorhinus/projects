#pragma once

#define DEBUG_LEVEL 1

// --- WIFI ---
#define WIFI_SSID         "galeasus24"
#define WIFI_PASS         "galeasus2.4"
#define MDNS_HOSTNAME     "elev8"

// --- PINS ---
#define HEAD_UP_PIN       22
#define HEAD_DOWN_PIN     23
#define FOOT_UP_PIN       18
#define FOOT_DOWN_PIN     19

#define TRANSFER_PIN_1    32
#define TRANSFER_PIN_2    33
#define TRANSFER_PIN_3    25
#define TRANSFER_PIN_4    26

// --- LEDS ---
#define LED_PIN_R         13
#define LED_PIN_G         27
#define LED_PIN_B         14
#define LED_COMMON_ANODE  1 

// --- LOGIC ---
#define RELAY_ON          0
#define RELAY_OFF         1

#define HEAD_MAX_MS_DEFAULT 25000
#define FOOT_MAX_MS_DEFAULT 40000
#define LIMIT_MIN_MS        5000    // Prevent unrealistically low limits
#define LIMIT_MAX_MS        60000   // Prevent runaway high limits
#define SYNC_EXTRA_MS     10000

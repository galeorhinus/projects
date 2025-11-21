#pragma once

// ==========================================
//               CONFIGURATION
// ==========================================

// --- DEBUG CONTROL ---
#define DEBUG_LEVEL 1

// --- WIFI CREDENTIALS (HARDCODED) ---
#define WIFI_SSID         "galeasus24"
#define WIFI_PASS         "galeasus2.4"

// --- NETWORK SETTINGS ---
#define MDNS_HOSTNAME     "elev8"
#define NTP_SERVER_1      "pool.ntp.org"
#define NTP_SERVER_2      "time.nist.gov"

// --- GPIO PIN DEFINITIONS ---
#define HEAD_UP_PIN       22
#define HEAD_DOWN_PIN     23
#define FOOT_UP_PIN       18
#define FOOT_DOWN_PIN     19

#define TRANSFER_PIN_1    32
#define TRANSFER_PIN_2    33
#define TRANSFER_PIN_3    25
#define TRANSFER_PIN_4    26

// --- LED PINS ---
#define LED_PIN_R         13
#define LED_PIN_G         27 
#define LED_PIN_B         14 

// --- LED LOGIC ---
#define LED_COMMON_ANODE  true 

// PWM Settings
#define LED_FREQ          5000
#define LED_RES           8
#define LED_CH_R          0
#define LED_CH_G          1
#define LED_CH_B          2

// --- LOGIC CONSTANTS ---
#define RELAY_ON          LOW   
#define RELAY_OFF         HIGH

// --- TIMING & SAFETY ---
const int HEAD_MAX_MS = 28000;
const int FOOT_MAX_MS = 43000;
const int THROTTLE_SAVE_MS = 2000;
const int SYNC_EXTRA_MS = 10000;
#pragma once

// ==========================================
//               CONFIGURATION
// ==========================================

// --- DEBUG CONTROL ---
// 0 = Silent
// 1 = Normal (Startup Info + 1s Status Heartbeat)
// 2 = Verbose (Detailed Math, Timer Events)
#define DEBUG_LEVEL 0

// --- NETWORK SETTINGS ---
#define WIFI_AP_NAME      "HomeYantric-Elev8"
#define MDNS_HOSTNAME     "elev8"
#define WIFI_TIMEOUT      180  // Seconds before falling back/booting
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

// --- LOGIC CONSTANTS ---
#define RELAY_ON          LOW   // Active Low relays
#define RELAY_OFF         HIGH

// --- TIMING & SAFETY ---
// Max travel time in milliseconds
const int HEAD_MAX_MS = 28000;
const int FOOT_MAX_MS = 43000;

// Minimum time between writes to flash memory
const int THROTTLE_SAVE_MS = 2000;

// Extra buffer added to MAX/FLAT commands to ensure full travel
const int SYNC_EXTRA_MS = 10000;
#pragma once
#include <stdint.h>

// Allow other components to temporarily override the status LED (e.g., during motor motion).
// If duration_ms is 0, the override is persistent until cleared.
void status_led_override(uint8_t r, uint8_t g, uint8_t b, uint32_t duration_ms = 0);
void status_led_clear_override();

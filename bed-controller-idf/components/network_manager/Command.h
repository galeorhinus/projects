#pragma once

#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"

// Simple POD so it can be safely copied into a FreeRTOS queue
typedef struct {
    char cmd[32];
    char label[64];
    SemaphoreHandle_t sync_sem;
} Command;

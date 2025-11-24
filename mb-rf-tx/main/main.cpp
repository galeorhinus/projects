#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "esp_rom_sys.h" 
#include "esp_timer.h" 

#define TX_PIN GPIO_NUM_19
#define TAG "BED_FINAL"

// ==========================================
//       --- CONFIGURATION ---
// 0 = HEAD UP   (Confirmed Working)
// 1 = HEAD DOWN (Confirmed Working)
// 2 = FOOT UP   (Re-transcribed)
// 3 = FOOT DOWN (Re-transcribed)
// 4 = FLAT      (Re-transcribed)
#define TEST_CMD 4
// ==========================================

// --- RE-NORMALIZED SIGNALS ---
// Timings: Sync=12875, Long=1250, Short=420

// [CONFIRMED WORKING]
unsigned int headUp[] = {
    12875, 1320, 350, 1320, 350, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 1250, 420, 1250, 420, 1250, 420, 420, 
    1250, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 
    420, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 1250, 420, 420, 1250, 420, 1250, 420
};

// [CONFIRMED WORKING]
unsigned int headDown[] = {
    12875, 1320, 420, 1250, 420, 350, 1320, 350, 1320, 420, 
    1250, 420, 1250, 1250, 420, 1250, 420, 1250, 420, 350, 
    1320, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 
    420, 350, 1320, 420, 1250, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 1250, 420, 420, 1250, 1250, 420, 420
};

// [FIXED] - Pulse-by-pulse correction from your data
unsigned int footUp[] = {
    12875, 1250, 420, 1250, 420, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 1250, 420, 1250, 420, 1250, 420, 420, 
    1250, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 
    420, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 420, 1250, 1250, 420, 1250, 420, 420
};

// [FIXED] - Pulse-by-pulse correction from your data
unsigned int footDown[] = {
    12875, 1250, 420, 1250, 420, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 1250, 420, 1250, 420, 1250, 420, 420, 
    1250, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 
    420, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 
    1250, 1250, 420, 1250, 420, 420, 1250, 420, 1250, 420
};

// [FIXED] - Pulse-by-pulse correction from your data
unsigned int flat[] = {
    12875, 1250, 420, 1250, 420, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 1250, 420, 1250, 420, 1250, 420, 420, 
    1250, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 
    420, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 
    1250, 1250, 420, 420, 1250, 1250, 420, 420, 1250, 420
};

// --- TRANSMISSION LOGIC ---

void send_raw_signal(int pin, unsigned int* data, int len) {
    gpio_set_level((gpio_num_t)pin, 0);
    esp_rom_delay_us(data[0]);

    for (int i = 1; i < len; i++) {
        int level = (i % 2 != 0) ? 1 : 0; 
        gpio_set_level((gpio_num_t)pin, level);
        esp_rom_delay_us(data[i]);
    }
    gpio_set_level((gpio_num_t)pin, 0);
}

extern "C" { void app_main(void); }

void app_main(void)
{
    gpio_reset_pin(TX_PIN);
    gpio_set_direction(TX_PIN, GPIO_MODE_OUTPUT);
    gpio_set_level(TX_PIN, 0);

    unsigned int* activeSignal = NULL;
    const char* name = "";

    switch(TEST_CMD) {
        case 0: activeSignal = headUp;   name = "HEAD UP"; break;
        case 1: activeSignal = headDown; name = "HEAD DOWN"; break;
        case 2: activeSignal = footUp;   name = "FOOT UP"; break;
        case 3: activeSignal = footDown; name = "FOOT DOWN"; break;
        case 4: activeSignal = flat;     name = "FLAT"; break;
        default: ESP_LOGE(TAG, "Invalid TEST_CMD!"); return;
    }

    ESP_LOGI(TAG, "NORMALIZED TEST: %s", name);
    vTaskDelay(pdMS_TO_TICKS(2000));

    while (1) {
        ESP_LOGI(TAG, "Sending %s...", name);
        
        int64_t start = esp_timer_get_time();
        while (esp_timer_get_time() - start < 3000000) { 
            send_raw_signal(TX_PIN, activeSignal, 50);
        }

        ESP_LOGI(TAG, "Done. Waiting 5s...");
        vTaskDelay(pdMS_TO_TICKS(5000));
    }
}
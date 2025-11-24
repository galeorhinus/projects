#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "esp_rom_sys.h" 
#include "esp_timer.h" 

#define TX_PIN GPIO_NUM_19
#define TAG "BED_EXP"

// ==========================================
//       --- CONFIGURATION ---
#define TEST_CMD 6

// TUNING PARAMETERS FOR "BOTH UP"
// Try decreasing BURST_COUNT to 2 or 3 for smoother movement.
// If it stops working, increase back to 4 or 5.
#define BURST_COUNT 3   
#define GAP_TIME_US 12000 
// ==========================================

// --- PROVEN NORMALIZED SIGNALS ---
// Sync=12875, Long=1250, Short=420

unsigned int headUp[] = {
    12875, 1320, 350, 1320, 350, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 1250, 420, 1250, 420, 1250, 420, 420, 
    1250, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 
    420, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 1250, 420, 420, 1250, 420, 1250, 420
};

unsigned int headDown[] = {
    12875, 1320, 420, 1250, 420, 350, 1320, 350, 1320, 420, 
    1250, 420, 1250, 1250, 420, 1250, 420, 1250, 420, 350, 
    1320, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 
    420, 350, 1320, 420, 1250, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 1250, 420, 420, 1250, 1250, 420, 420
};

unsigned int footUp[] = {
    12875, 1250, 420, 1250, 420, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 1250, 420, 1250, 420, 1250, 420, 420, 
    1250, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 
    420, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 420, 1250, 1250, 420, 1250, 420, 420
};

unsigned int footDown[] = {
    12875, 1250, 420, 1250, 420, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 1250, 420, 1250, 420, 1250, 420, 420, 
    1250, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 
    420, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 
    1250, 1250, 420, 1250, 420, 420, 1250, 420, 1250, 420
};

unsigned int flat[] = {
    12875, 1250, 420, 1250, 420, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 1250, 420, 1250, 420, 1250, 420, 420, 
    1250, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 
    420, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 
    1250, 1250, 420, 420, 1250, 1250, 420, 420, 1250, 420
};

// --- TRANSMISSION ENGINE ---

void send_raw_signal(int pin, unsigned int* data, int len) {
    // 1. Sync Pulse (Low)
    gpio_set_level((gpio_num_t)pin, 0);
    esp_rom_delay_us(data[0]);

    // 2. Data Pulses
    for (int i = 1; i < len; i++) {
        int level = (i % 2 != 0) ? 1 : 0; 
        gpio_set_level((gpio_num_t)pin, level);
        esp_rom_delay_us(data[i]);
    }
    
    // 3. End Low
    gpio_set_level((gpio_num_t)pin, 0);
}

// --- HELPER: Send a signal for X microseconds ---
void send_for_duration(int pin, unsigned int* data, int len, int64_t duration_us) {
    int64_t start = esp_timer_get_time();
    while (esp_timer_get_time() - start < duration_us) { 
        send_raw_signal(pin, data, len);
    }
}

extern "C" { void app_main(void); }

void app_main(void)
{
    gpio_reset_pin(TX_PIN);
    gpio_set_direction(TX_PIN, GPIO_MODE_OUTPUT);
    gpio_set_level(TX_PIN, 0);

    ESP_LOGI(TAG, "MASTER BED CONTROLLER STARTED");
    ESP_LOGI(TAG, "Mode: %d (BURST=%d, GAP=%d)", TEST_CMD, BURST_COUNT, GAP_TIME_US);
    vTaskDelay(pdMS_TO_TICKS(2000));

    while (1) {
        if (TEST_CMD == 6) {
            // --- MODE 6: TUNED "BOTH UP" EXPERIMENT ---
            ESP_LOGI(TAG, "Attempting Tuned Multiplexing...");
            
            int64_t start = esp_timer_get_time();
            while (esp_timer_get_time() - start < 4000000) { 
                
                // 1. Move Head (High Speed Burst)
                for(int i=0; i<BURST_COUNT; i++) {
                    send_raw_signal(TX_PIN, headUp, 50);
                }
                
                // Reset Gap
                gpio_set_level(TX_PIN, 0);
                esp_rom_delay_us(GAP_TIME_US); 

                // 2. Move Foot (High Speed Burst)
                for(int i=0; i<BURST_COUNT; i++) {
                    send_raw_signal(TX_PIN, footUp, 50);
                }

                // Reset Gap
                gpio_set_level(TX_PIN, 0);
                esp_rom_delay_us(GAP_TIME_US); 
            }
            
            ESP_LOGI(TAG, "Done. Waiting 5s...");
            vTaskDelay(pdMS_TO_TICKS(5000));
        } 
        else {
             // --- MODES 0-4: SINGLE BUTTON TEST ---
            unsigned int* activeSignal = NULL;
            const char* name = "";
            
            switch(TEST_CMD) {
                case 0: activeSignal = headUp;   name = "HEAD UP"; break;
                case 1: activeSignal = headDown; name = "HEAD DOWN"; break;
                case 2: activeSignal = footUp;   name = "FOOT UP"; break;
                case 3: activeSignal = footDown; name = "FOOT DOWN"; break;
                case 4: activeSignal = flat;     name = "FLAT"; break;
            }

            ESP_LOGI(TAG, "Sending %s...", name);
            send_for_duration(TX_PIN, activeSignal, 50, 3000000);
            ESP_LOGI(TAG, "Done. Waiting 5s...");
            vTaskDelay(pdMS_TO_TICKS(5000));
        }
    }
}
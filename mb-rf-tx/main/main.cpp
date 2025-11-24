#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "esp_rom_sys.h" // Required for precise microsecond delays

// --- CONFIGURATION ---
#define TX_PIN GPIO_NUM_19
#define TAG "TX_APP"

// The Raw Signal you captured
// Index 0 is the "Sync" or "Gap" (Low level)
// Index 1 is High, Index 2 is Low, Index 3 is High, etc.
unsigned int bed_remote_signal[] = {
    12875, 1326, 454, 1193, 497, 333, 1320, 363, 1295, 387, 
    1273, 403, 1227, 1285, 433, 1233, 443, 1200, 495, 342, 
    1313, 1236, 443, 1190, 478, 1197, 428, 1221, 517, 1166, 
    497, 357, 1276, 406, 1256, 422, 1225, 446, 1242, 430, 
    1239, 455, 1218, 1242, 436, 406, 1257, 1244, 434, 397
};

void send_raw_signal(int pin, unsigned int* data, int len) {
    // 1. The first number is the Sync/Gap. Ensure line is LOW and wait.
    gpio_set_level((gpio_num_t)pin, 0);
    esp_rom_delay_us(data[0]);

    // 2. Loop through the rest of the pulses
    for (int i = 1; i < len; i++) {
        // Odd index (1, 3, 5...) = HIGH
        // Even index (2, 4, 6...) = LOW
        int level = (i % 2 != 0) ? 1 : 0;
        
        gpio_set_level((gpio_num_t)pin, level);
        esp_rom_delay_us(data[i]);
    }
    
    // 3. Always end on LOW to prevent jamming
    gpio_set_level((gpio_num_t)pin, 0);
}

extern "C" { void app_main(void); }

void app_main(void)
{
    // Configure Transmitter Pin
    gpio_reset_pin(TX_PIN);
    gpio_set_direction(TX_PIN, GPIO_MODE_OUTPUT);
    gpio_set_level(TX_PIN, 0);

    ESP_LOGI(TAG, "Transmitter Initialized on GPIO %d", TX_PIN);
    ESP_LOGI(TAG, "Sending signal every 3 seconds...");

    while (1) {
        ESP_LOGI(TAG, "Sending...");
        
        // RF receivers usually need to see the signal repeated 4-10 times
        // to "lock on" and accept it as valid.
        for (int repeat = 0; repeat < 25; repeat++) {
            send_raw_signal(TX_PIN, bed_remote_signal, sizeof(bed_remote_signal)/sizeof(unsigned int));
            
            // Note: The "Sync" delay at data[0] acts as the gap between repeats,
            // so we don't need an extra vTaskDelay here.
        }

        ESP_LOGI(TAG, "Done.");
        
        // Wait 3 seconds before next trigger
        vTaskDelay(pdMS_TO_TICKS(3000));
    }
}
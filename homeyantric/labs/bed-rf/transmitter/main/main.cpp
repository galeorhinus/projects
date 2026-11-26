#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "esp_rom_sys.h" 
#include "esp_timer.h" 

#define TX_PIN GPIO_NUM_19
#define TAG "CLONE_SCAN"

// --- TIMINGS ---
#define SHORT 420
#define LONG 1250

// --- THE GOLDEN SOURCE ---
// This is the exact array from the working "Single Button" test.
// We will copy this to scanSignal so we start with a perfect packet.
unsigned int headUp_Source[50] = {
    12875, 1320, 350, 1320, 350, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 1250, 420, 1250, 420, 1250, 420, 420, 
    1250, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 
    420, 420, 1250, 420, 1250, 420, 1250, 420, 1250, 420, 
    1250, 420, 1250, 1250, 420, 420, 1250, 420, 1250, 420
};

// Active Array
unsigned int scanSignal[50];

// --- HELPER: Overwrite only the Command Bits ---
void update_command(uint8_t cmd) {
    // We modify the last 4 bits (8 pulses).
    // Array Length is 50.
    // Indices 0-40 are Sync/Address (Keep them!)
    // Indices 41-48 are the Command (Overwrite them!)
    // Index 49 is trailing pulse (Keep it!)
    
    int currentIdx = 41;

    for (int i = 3; i >= 0; i--) {
        if ((cmd >> i) & 1) {
            // Logic 1: Long, Short
            scanSignal[currentIdx]   = LONG;
            scanSignal[currentIdx+1] = SHORT;
        } else {
            // Logic 0: Short, Long
            scanSignal[currentIdx]   = SHORT;
            scanSignal[currentIdx+1] = LONG;
        }
        currentIdx += 2;
    }
}

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

    ESP_LOGI(TAG, "STARTING CLONE SCANNER (0-15)");
    ESP_LOGI(TAG, "Code 4 SHOULD move Head Up.");
    vTaskDelay(pdMS_TO_TICKS(3000));

    // 1. Clone the working signal
    memcpy(scanSignal, headUp_Source, sizeof(headUp_Source));

    for (int i = 0; i <= 15; i++) {
        
        // 2. Mutate the command part
        update_command((uint8_t)i);
        
        const char* hint = "";
        if(i==1) hint = "(Foot Up)";
        if(i==2) hint = "(Head Down)";
        if(i==3) hint = "(Both Down?)";
        if(i==4) hint = "(Head Up - CONTROL)";
        if(i==5) hint = "(Both Up?)";
        if(i==8) hint = "(Foot Down)";

        ESP_LOGI(TAG, "Testing: %d %s", i, hint);

        // 3. Transmit for 2 seconds
        int64_t start = esp_timer_get_time();
        while (esp_timer_get_time() - start < 2000000) { 
            send_raw_signal(TX_PIN, scanSignal, 50);
            vTaskDelay(pdMS_TO_TICKS(10)); // Safety yield
        }

        ESP_LOGI(TAG, "Wait...");
        vTaskDelay(pdMS_TO_TICKS(2000));
    }

    ESP_LOGI(TAG, "Scan Complete.");
}
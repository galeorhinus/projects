#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_timer.h"
#include "esp_log.h"

// --- SETTINGS ---
#define RX_PIN GPIO_NUM_18
#define TAG "SNIFFER"
#define MAX_PULSES 512

// --- Globals for Interrupt Handler ---
volatile uint32_t pulse_buffer[MAX_PULSES];
volatile int pulse_count = 0;
volatile uint64_t last_time = 0;
volatile bool capture_complete = false;

// --- Interrupt Service Routine ---
void IRAM_ATTR rx_isr_handler(void* arg) {
    if (capture_complete) return; 

    uint64_t now = esp_timer_get_time();
    uint32_t duration = (uint32_t)(now - last_time);
    last_time = now;

    // Filter noise
    if (duration < 50) return;

    // Detect signal breaks
    if (duration > 5000) {
        if (pulse_count > 20) {
            capture_complete = true;
            return; 
        } else {
            pulse_count = 0;
        }
    }

    // Store the timing (Split into two lines to fix C++ warning)
    if (pulse_count < MAX_PULSES) {
        pulse_buffer[pulse_count] = duration;
        pulse_count += 1;
    }
}

extern "C" { void app_main(void); }

void app_main(void)
{
    // 1. Setup GPIO
    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_ANYEDGE; 
    io_conf.pin_bit_mask = (1ULL << RX_PIN);
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE; 
    gpio_config(&io_conf);

    // 2. Setup Interrupts
    gpio_install_isr_service(0);
    gpio_isr_handler_add(RX_PIN, rx_isr_handler, NULL);

    ESP_LOGI(TAG, "Raw Sniffer Started. Press your remote button...");

    while (1) {
        if (capture_complete) {
            ESP_LOGI(TAG, "--- CAPTURED SIGNAL (%d pulses) ---", pulse_count);
            
            printf("unsigned int rawData[] = {");
            for (int i = 0; i < pulse_count; i++) {
                printf("%lu", pulse_buffer[i]);
                if (i < pulse_count - 1) printf(", ");
            }
            printf("};\n");

            ESP_LOGI(TAG, "--- END ---");
            
            vTaskDelay(pdMS_TO_TICKS(2000)); 
            
            pulse_count = 0;
            capture_complete = false;
            ESP_LOGI(TAG, "Listening...");
        }

        vTaskDelay(pdMS_TO_TICKS(20));
    }
}
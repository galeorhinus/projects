#include <string>
#include <cstring>

extern "C" {
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
}

#include "wifi_provisioning.h"

static const char *TAG = "MainApp";

void on_provisioning_success(const char* sta_ip) {
    ESP_LOGI(TAG, "Provisioning successful! Device IP: %s", sta_ip);
    // You can now start your main application logic, e.g., MQTT client, sensor readings, etc.
}

extern "C" void app_main(void)
{
    wifi_provisioning_config_t config = {
        .ap_ssid = "HomeYantric-Setup",
        .on_success = on_provisioning_success
    };
    wifi_provisioning_start(&config);
}

#include <string>
#include <cstring>

extern "C" {
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
}

#include "wifiProvisioning.h"

static const char *TAG = "MainApp";

void onProvisioningSuccess(const char* staIp)
{
    ESP_LOGI(TAG, "Provisioning successful! Device IP: %s", staIp);
    // You can now start your main application logic, e.g., MQTT client, sensor readings, etc.
}

extern "C" void app_main(void)
{
    wifiProvisioningConfig config = {
        .apSsid = "HomeYantric-Setup",
        .onSuccess = onProvisioningSuccess
    };
    wifiProvisioningStart(&config);
}

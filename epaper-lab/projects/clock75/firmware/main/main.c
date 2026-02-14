#include <stdio.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "wifiProvisioning.h"

static const char *TAG = "clock75";

static void on_provisioned(const char *sta_ip)
{
    ESP_LOGI(TAG, "Provisioned, IP: %s", sta_ip ? sta_ip : "(null)");
}

void app_main(void)
{
    wifiProvisioningConfig cfg = {
        .apSsid = "clock75-setup",
        .onSuccess = on_provisioned,
    };

    esp_err_t err = wifiProvisioningStart(&cfg);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Provisioning start failed: %s", esp_err_to_name(err));
    }

    while (1) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

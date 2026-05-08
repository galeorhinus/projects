#include <stdio.h>
#include <time.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "nvs.h"
#include "nvs_flash.h"
#include "mooncalc.h"
#include "wifiProvisioning.h"

static const char *TAG = "clock75";

static int get_moon_step_minutes(void)
{
    int32_t value = CONFIG_CLOCK75_MOON_STEP_MIN;
    nvs_handle_t nvs = 0;
    esp_err_t err = nvs_open("clock75", NVS_READWRITE, &nvs);
    if (err == ESP_OK) {
        int32_t stored = 0;
        err = nvs_get_i32(nvs, "moon_step_min", &stored);
        if (err == ESP_OK) {
            value = stored;
        } else if (err == ESP_ERR_NVS_NOT_FOUND) {
            nvs_set_i32(nvs, "moon_step_min", value);
            nvs_commit(nvs);
        }
        nvs_close(nvs);
    }

    if (value < 5) value = 5;
    if (value > 120) value = 120;
    return (int)value;
}

static void on_provisioned(const char *sta_ip)
{
    ESP_LOGI(TAG, "Provisioned, IP: %s", sta_ip ? sta_ip : "(null)");
}

static void log_moon_curve(int step_minutes)
{
    time_t now = time(NULL);
    if (now < 1672531200) { // 2023-01-01
        ESP_LOGW(TAG, "System time not set; skipping moon calc");
        return;
    }

    double lat = (double)CONFIG_CLOCK75_LAT_E6 / 1e6;
    double lon = (double)CONFIG_CLOCK75_LON_E6 / 1e6;

    time_t start = now;
    time_t end = now + 24 * 60 * 60;

    int max_points = (24 * 60) / step_minutes + 2;
    if (max_points < 4) max_points = 4;
    if (max_points > 600) max_points = 600;

    static mooncalc_point_t points[600];
    int count = mooncalc_build_curve(start, end, step_minutes, lat, lon, points, max_points);

    time_t rise = 0;
    time_t set = 0;
    int rise_set = mooncalc_find_rise_set(start, end, step_minutes, lat, lon, &rise, &set);

    ESP_LOGI(TAG, "Moon curve points: %d (step %d min)", count, step_minutes);
    if (count > 0) {
        ESP_LOGI(TAG, "Moon start elev: %.1f", points[0].elev_deg);
        ESP_LOGI(TAG, "Moon end elev: %.1f", points[count - 1].elev_deg);
    }
    if (rise_set == 0) {
        ESP_LOGI(TAG, "Moon rise: %ld set: %ld", (long)rise, (long)set);
    } else {
        ESP_LOGW(TAG, "Moon rise/set not found in window");
    }
}

void app_main(void)
{
    esp_err_t err = nvs_flash_init();
    if (err == ESP_ERR_NVS_NO_FREE_PAGES || err == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        nvs_flash_erase();
        err = nvs_flash_init();
    }
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "NVS init failed: %s", esp_err_to_name(err));
    }

    int moon_step_min = get_moon_step_minutes();
    ESP_LOGI(TAG, "Moon curve step: %d min", moon_step_min);
    log_moon_curve(moon_step_min);

    wifiProvisioningConfig cfg = {
        .apSsid = "clock75-setup",
        .onSuccess = on_provisioned,
    };

    err = wifiProvisioningStart(&cfg);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Provisioning start failed: %s", esp_err_to_name(err));
    }

    while (1) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

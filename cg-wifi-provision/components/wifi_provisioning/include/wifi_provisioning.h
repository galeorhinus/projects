#pragma once

#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Callback function type for when provisioning is complete.
 *
 * @param sta_ip The IP address assigned to the device in Station mode.
 */
typedef void (*wifi_provisioning_success_cb_t)(const char* sta_ip);

/**
 * @brief Configuration for the Wi-Fi provisioning component.
 */
typedef struct {
    const char* ap_ssid;                        /*!< SSID for the SoftAP */
    wifi_provisioning_success_cb_t on_success;  /*!< Callback for successful provisioning */
} wifi_provisioning_config_t;

esp_err_t wifi_provisioning_start(const wifi_provisioning_config_t *config);

#ifdef __cplusplus
}
#endif

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
typedef void (*wifiProvisioningSuccessCb)(const char* sta_ip);

/**
 * @brief Configuration for the Wi-Fi provisioning component.
 */
typedef struct {
    const char* apSsid;                        /*!< SSID for the SoftAP */
    wifiProvisioningSuccessCb onSuccess;  /*!< Callback for successful provisioning */
} wifiProvisioningConfig;

esp_err_t wifiProvisioningStart(const wifiProvisioningConfig *config);
void wifiProvisioningCloseAp(void);
const char* wifiProvisioningGetHostname(void);
const char* wifiProvisioningGetSsid(void);

#ifdef __cplusplus
}
#endif

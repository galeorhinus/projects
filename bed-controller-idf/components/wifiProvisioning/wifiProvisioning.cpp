#include "wifiProvisioning.h"
#include "Config.h"
#include "MatterManager.h"

#include <string>
#include <cstring>

extern "C" {
#include "freertos/FreeRTOS.h"
#include "freertos/event_groups.h"
#include "freertos/task.h"

#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "nvs_flash.h"
#include "esp_netif.h"
#include "esp_mac.h"

#include "lwip/inet.h"
#include "lwip/sockets.h"

#include "esp_http_server.h"
#include "mdns.h"

#include "cJSON.h"
}

static const char *TAG = "WiFiProvisioning";

// Wi-Fi event bits
static EventGroupHandle_t wifiEventGroup; static const int WIFI_CONNECTED_BIT = BIT0;

struct AppState {
    bool provisioningDone = false;
    bool wifiConnected = false;
    std::string staIpStr;
    std::string mdnsHostStr;
    std::string apIpStr = "192.168.4.1";
    bool wifiError = false;
    std::string wifiErrorReason;
    int wifiRetryCount = 0;
    std::string staSsid;
    const int WIFI_MAX_RETRY = 5;
    bool apStarted = false;
};
static AppState appState;

static wifiProvisioningConfig provConfig;

static esp_timer_handle_t apShutdownTimer = nullptr;
static bool dnsStop = false;
static int dnsSock = -1;

// Forward declarations
static void startSoftAP();
static void startDnsCaptivePortal();
static void startHttpServer();
static void startStaConnect(const char *ssid, const char *password);
static void initMdnsHostname();

// Embedded file handlers
extern const uint8_t provisioning_html_start[] asm("_binary_provisioning_html_start");
extern const uint8_t provisioning_html_end[] asm("_binary_provisioning_html_end");
extern const uint8_t app_html_start[] asm("_binary_app_html_start");
extern const uint8_t app_html_end[] asm("_binary_app_html_end");
extern const uint8_t styles_css_start[] asm("_binary_styles_css_start");
extern const uint8_t styles_css_end[] asm("_binary_styles_css_end");
static const char provisioning_js[] = R"rawliteral(
function scanNetworks() {
    const list = document.getElementById('wifi-list');
    if (list) list.innerHTML = 'Scanning...';
    fetch('/scan')
        .then(r => r.json())
        .then(networks => {
            if (!list) return;
            list.innerHTML = '';
            networks.sort((a,b)=>b.rssi-a.rssi);
            networks.forEach(net => {
                const el = document.createElement('div');
                el.className = 'wifi-item';
                el.innerText = `${net.ssid} (${net.rssi}dBm)`;
                el.onclick = () => selectNetwork(net.ssid);
                list.appendChild(el);
            });
        })
        .catch(() => { if (list) list.innerHTML = 'Scan failed'; });
}
function selectNetwork(ssid) {
    const sel = document.getElementById('selected-ssid');
    const pwd = document.getElementById('password');
    const pwc = document.getElementById('password-container');
    const nets = document.getElementById('networks-container');
    if (sel) sel.textContent = ssid;
    if (pwd) pwd.value = '';
    if (pwc) pwc.classList.remove('hidden');
    if (nets) nets.classList.add('hidden');
    const ssidInput = document.getElementById('ssid');
    if (ssidInput) ssidInput.value = ssid;
}
document.addEventListener('DOMContentLoaded', function() {
    const scanBtn = document.querySelector('button[onclick=\"openScanModal()\"]');
    if (scanBtn) {
        scanBtn.addEventListener('click', function(ev) {
            ev.preventDefault();
            const modal = document.getElementById('scan-modal');
            if (modal) modal.style.display = 'block';
            scanNetworks();
        });
    }
});
)rawliteral";

const char provisioning_html[] = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
    <title>Wi-Fi Setup</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>HomeYantric</h1>
        <h2>Wi-Fi Setup Portal</h2>
        <div id="loading" class="hidden">Scanning for networks...</div>
        <div id="error" class="hidden"></div>
        <div id="success" class="hidden"></div>
        <div id="networks-container" class="hidden">
            <ul id="networks-list"></ul>
            <button onclick="scanNetworks()">Rescan</button>
        </div>
        <div id="password-container" class="hidden">
            <p>Enter password for <strong id="selected-ssid"></strong>:</p>
            <input type="password" id="password" placeholder="Password">
            <button onclick="connectToWifi()">Connect</button>
            <button onclick="showNetworks()">Back</button>
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/js/all.min.js"></script>
    <script src="provisioning.js"></script>
</body>
</html>
)rawliteral";

// HTTP handler forward declarations
static esp_err_t rootGetHandler(httpd_req_t *req);
static esp_err_t scanGetHandler(httpd_req_t *req);
static esp_err_t wifiPostHandler(httpd_req_t *req);
static esp_err_t statusGetHandler(httpd_req_t *req);
static esp_err_t appGetHandler(httpd_req_t *req);
static esp_err_t captiveCatchallHandler(httpd_req_t *req);
static esp_err_t resetWifiHandler(httpd_req_t *req);
static esp_err_t closeApHandler(httpd_req_t *req);
static esp_err_t stylesCssGetHandler(httpd_req_t *req);
static esp_err_t matterInfoHandler(httpd_req_t *req);
static esp_err_t provisioningJsHandler(httpd_req_t *req);

static httpd_handle_t startWebserver();
static void stopWebserver();
static httpd_handle_t g_http_server = nullptr;

static void shutdownAP() {
    if (apShutdownTimer && esp_timer_is_active(apShutdownTimer)) {
        esp_timer_stop(apShutdownTimer);
        esp_timer_delete(apShutdownTimer);
        apShutdownTimer = nullptr;
    }
    ESP_LOGI(TAG, "Shutting down SoftAP");
    esp_wifi_set_mode(WIFI_MODE_STA);
    appState.apStarted = false;

    // Stop DNS captive portal
    dnsStop = true;
    if (dnsSock >= 0) {
        shutdown(dnsSock, SHUT_RDWR);
        close(dnsSock);
        dnsSock = -1;
    }
}

// -------------------- Wi-Fi + Events --------------------

static void wifiEventHandler(void *arg, esp_event_base_t event_base, int32_t event_id, void *event_data)
{
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        ESP_LOGI(TAG, "STA start -> connecting…");
        esp_wifi_connect();
    }
    else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        auto* disc = (wifi_event_sta_disconnected_t*) event_data;
        appState.wifiConnected = false;
        xEventGroupClearBits(wifiEventGroup, WIFI_CONNECTED_BIT);

        appState.wifiRetryCount++;
        ESP_LOGW(TAG, "STA disconnected, reason=%d, retry=%d", disc->reason, appState.wifiRetryCount);

        // Optionally generate a human-readable reason
        appState.wifiErrorReason.clear();
        switch (disc->reason) {
            case WIFI_REASON_AUTH_FAIL:
            case WIFI_REASON_HANDSHAKE_TIMEOUT:
                appState.wifiErrorReason = "Authentication failed (check password)";
                break;
            case WIFI_REASON_NO_AP_FOUND:
                appState.wifiErrorReason = "Network not found";
                break;
            default:
                appState.wifiErrorReason = "Wi-Fi disconnected (reason " + std::to_string(disc->reason) + ")";
                break;
        }

        if (appState.wifiRetryCount < appState.WIFI_MAX_RETRY) {
            appState.wifiError = false;
            ESP_LOGI(TAG, "Retrying Wi-Fi…");
            esp_wifi_connect();
        } else {
            appState.wifiError = true;
            ESP_LOGW(TAG, "Too many Wi-Fi failures, staying in provisioning mode");
            // Fallback to provisioning AP if not already running
            if (!appState.apStarted) {
                startSoftAP();
                startHttpServer();
                startDnsCaptivePortal();
            }
        }
    }
    else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        auto* event = (ip_event_got_ip_t*) event_data;
        char ip[16];
        inet_ntoa_r(event->ip_info.ip.addr, ip, sizeof(ip));
        appState.staIpStr = ip;

        ESP_LOGI(TAG, "Got IP: %s", ip);
        appState.wifiConnected = true;
        appState.wifiError = false;
        appState.wifiErrorReason.clear();
        appState.wifiRetryCount = 0;

        appState.provisioningDone = true;
        xEventGroupSetBits(wifiEventGroup, WIFI_CONNECTED_BIT);

        initMdnsHostname();

        // Stop the provisioning HTTP server before handing off to the main app
        stopWebserver();

        if (provConfig.onSuccess) {
            provConfig.onSuccess(appState.staIpStr.c_str());
        }

        // Start a 5-minute timer to automatically shut down the AP
        if (appState.apStarted) {
            const esp_timer_create_args_t ap_shutdown_timer_args = {
                .callback = [](void* arg) { shutdownAP(); },
                .arg = nullptr,
                .dispatch_method = ESP_TIMER_TASK,
                .name = "ap_shutdown",
                .skip_unhandled_events = false
            };
            esp_err_t err = esp_timer_create(&ap_shutdown_timer_args, &apShutdownTimer);
            if (err == ESP_OK) {
                // Start a one-shot timer for ~45 seconds (45,000,000 microseconds)
                esp_timer_start_once(apShutdownTimer, 45 * 1000 * 1000);
                ESP_LOGI(TAG, "SoftAP will be shut down automatically in ~45 seconds.");
            } else {
                ESP_LOGE(TAG, "Failed to create AP shutdown timer: %s", esp_err_to_name(err));
            }
        }
    }
}

static void startSoftAP()
{
    esp_netif_t *ap_netif = esp_netif_create_default_wifi_ap();

    esp_netif_ip_info_t ip_info;
    if (esp_netif_get_ip_info(ap_netif, &ip_info) == ESP_OK) {
        char ip[16];
        inet_ntoa_r(ip_info.ip.addr, ip, sizeof(ip));
        appState.apIpStr = ip;
    }

    wifi_config_t wifi_ap_config = {};
    strncpy((char *)wifi_ap_config.ap.ssid, provConfig.apSsid, sizeof(wifi_ap_config.ap.ssid));
    wifi_ap_config.ap.ssid_len = strlen(provConfig.apSsid);
    wifi_ap_config.ap.max_connection = 4;
    wifi_ap_config.ap.authmode = WIFI_AUTH_OPEN;

    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_APSTA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_AP, &wifi_ap_config));
    ESP_ERROR_CHECK(esp_wifi_start());

    ESP_LOGI(TAG, "SoftAP started, SSID: %s, IP: %s", provConfig.apSsid, appState.apIpStr.c_str());
    appState.apStarted = true;
}

static void initMdnsHostname()
{
    mdns_txt_item_t serviceTxtData[] = {
        {"board", "esp32-wrover"},
        {"app", "homeyantric"}
    };
    mdns_service_add("HomeYantric Web", "_http", "_tcp", 80, serviceTxtData, 2);

    ESP_LOGI(TAG, "mDNS service advertised for: %s.local", appState.mdnsHostStr.c_str());
}

static void startStaConnect(const char *ssid, const char *password)
{
    wifi_config_t wifi_sta_config = {};
    strncpy((char *)wifi_sta_config.sta.ssid, ssid, sizeof(wifi_sta_config.sta.ssid));
    strncpy((char *)wifi_sta_config.sta.password, password, sizeof(wifi_sta_config.sta.password));

    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_sta_config));

    appState.wifiConnected = false;
    appState.wifiError = false;
    appState.wifiErrorReason.clear();
    appState.wifiRetryCount = 0;

    xEventGroupClearBits(wifiEventGroup, WIFI_CONNECTED_BIT);

    ESP_LOGI(TAG, "Starting STA connect to SSID='%s'", ssid);
    ESP_ERROR_CHECK(esp_wifi_connect());
}

// -------------------- Captive Portal DNS --------------------

static void dnsServerTask(void *pvParameters)
{
    dnsStop = false;
    dnsSock = socket(AF_INET, SOCK_DGRAM, IPPROTO_IP);
    if (dnsSock < 0) {
        ESP_LOGE(TAG, "DNS socket failed");
        vTaskDelete(NULL);
        return;
    }

    struct sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    addr.sin_port = htons(53);

    if (bind(dnsSock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        ESP_LOGE(TAG, "DNS bind failed");
        close(dnsSock);
        dnsSock = -1;
        vTaskDelete(NULL);
        return;
    }

    ESP_LOGI(TAG, "DNS captive portal server started");

    uint8_t rx_buf[512];

    while (true) {
        struct sockaddr_in source_addr{};
        socklen_t socklen = sizeof(source_addr);
        int len = recvfrom(dnsSock, rx_buf, sizeof(rx_buf), 0,
                           (struct sockaddr *)&source_addr, &socklen);
        if (dnsStop || len <= 0) {
            break;
        }

        uint8_t tx_buf[512];
        if (len > (int)sizeof(tx_buf)) len = sizeof(tx_buf);

        memcpy(tx_buf, rx_buf, len);

        tx_buf[2] |= 0x80;
        tx_buf[3] |= 0x80;
        tx_buf[7] = 1;

        int pos = 12;
        while (pos < len && tx_buf[pos] != 0) {
            pos += tx_buf[pos] + 1;
        }
        pos += 5;

        if (pos + 16 > (int)sizeof(tx_buf)) continue;

        tx_buf[pos++] = 0xC0;
        tx_buf[pos++] = 0x0C;
        tx_buf[pos++] = 0x00;
        tx_buf[pos++] = 0x01;
        tx_buf[pos++] = 0x00;
        tx_buf[pos++] = 0x01;
        tx_buf[pos++] = 0x00;
        tx_buf[pos++] = 0x00;
        tx_buf[pos++] = 0x00;
        tx_buf[pos++] = 0x3C;
        tx_buf[pos++] = 0x00;
        tx_buf[pos++] = 0x04;

        inet_pton(AF_INET, appState.apIpStr.c_str(), &tx_buf[pos]);
        pos += 4;

        sendto(dnsSock, tx_buf, pos, 0, (struct sockaddr *)&source_addr, socklen);
    }

    if (dnsSock >= 0) {
        close(dnsSock);
        dnsSock = -1;
    }
    vTaskDelete(NULL);
}

static void startDnsCaptivePortal()
{
    xTaskCreate(&dnsServerTask, "dnsServerTask", 4096, NULL, 5, NULL);
}

// -------------------- HTTP Server + Handlers --------------------

static esp_err_t rootGetHandler(httpd_req_t *req)
{
    if (appState.provisioningDone) {
        httpd_resp_set_status(req, "302 Found");
        httpd_resp_set_hdr(req, "Location", "/app");
        httpd_resp_send(req, NULL, 0);
        return ESP_OK;
    } else {
        httpd_resp_set_type(req, "text/html");
        httpd_resp_send(req, (const char *)provisioning_html_start, provisioning_html_end - provisioning_html_start);
        return ESP_OK;
    }
}

static esp_err_t appGetHandler(httpd_req_t *req)
{
    httpd_resp_set_type(req, "text/html");
    return httpd_resp_send(req, (const char *)app_html_start, app_html_end - app_html_start);
}

static esp_err_t stylesCssGetHandler(httpd_req_t *req)
{
    httpd_resp_set_type(req, "text/css");
    httpd_resp_send(req, (const char *)styles_css_start, styles_css_end - styles_css_start);
    return ESP_OK;
}

static esp_err_t matterInfoHandler(httpd_req_t *req)
{
#if ENABLE_MATTER
    const char *qr = MatterManager::instance().getQrCode();
    const int pin = MatterManager::instance().getPinCode();
    const int disc = MatterManager::instance().getDiscriminator();
    const int vid = MatterManager::instance().getVid();
    const int pid = MatterManager::instance().getPid();
    const char *manual = MatterManager::instance().getManualCode();
    cJSON *root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "qr", qr);
    cJSON_AddStringToObject(root, "manual", manual);
    cJSON_AddNumberToObject(root, "pin", pin);
    cJSON_AddNumberToObject(root, "discriminator", disc);
    cJSON_AddNumberToObject(root, "vid", vid);
    cJSON_AddNumberToObject(root, "pid", pid);

    char *resp_str = cJSON_PrintUnformatted(root);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_sendstr(req, resp_str);

    cJSON_free(resp_str);
    cJSON_Delete(root);
    return ESP_OK;
#else
    httpd_resp_send_err(req, HTTPD_404_NOT_FOUND, "Matter disabled");
    return ESP_FAIL;
#endif
}

static esp_err_t provisioningJsHandler(httpd_req_t *req)
{
    httpd_resp_set_type(req, "application/javascript");
    return httpd_resp_send(req, provisioning_js, HTTPD_RESP_USE_STRLEN);
}

static esp_err_t scanGetHandler(httpd_req_t *req)
{
    ESP_LOGI(TAG, "Scan requested from HTTP client");
    wifi_scan_config_t scan_config = {};
    scan_config.show_hidden = true;
    esp_wifi_scan_start(&scan_config, true);

    uint16_t ap_num = 0;
    esp_wifi_scan_get_ap_num(&ap_num);

    wifi_ap_record_t *ap_records = (wifi_ap_record_t *)malloc(sizeof(wifi_ap_record_t) * ap_num);
    esp_wifi_scan_get_ap_records(&ap_num, ap_records);

    std::string json = "[";
    for (int i = 0; i < ap_num; ++i) {
        char ssid[33] = {0};
        memcpy(ssid, ap_records[i].ssid, 32);
        char entry[160];
        snprintf(entry, sizeof(entry), "%s{\"ssid\":\"%s\",\"rssi\":%d}", (i == 0 ? "" : ","), ssid, ap_records[i].rssi);
        json += entry;
    }
    json += "]";

    free(ap_records);

    httpd_resp_set_type(req, "application/json");
    return httpd_resp_sendstr(req, json.c_str());
}

static esp_err_t resetWifiHandler(httpd_req_t *req)
{
    ESP_LOGW(TAG, "Received reset Wi-Fi request");

    esp_wifi_restore();

    cJSON *root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "status", "ok");
    char *resp_str = cJSON_PrintUnformatted(root);

    httpd_resp_set_type(req, "application/json");
    httpd_resp_sendstr(req, resp_str);

    cJSON_free(resp_str);
    cJSON_Delete(root);

    vTaskDelay(pdMS_TO_TICKS(200));

    ESP_LOGW(TAG, "Restarting after Wi-Fi reset");
    esp_restart();

    return ESP_OK;
}

static esp_err_t closeApHandler(httpd_req_t *req)
{
    ESP_LOGI(TAG, "Received request to close AP");
    shutdownAP(); // Shut down AP and cancel the timer

    cJSON *root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "status", "ok");
    char *resp_str = cJSON_PrintUnformatted(root);

    httpd_resp_set_type(req, "application/json");
    httpd_resp_sendstr(req, resp_str);

    cJSON_free(resp_str);
    cJSON_Delete(root);

    return ESP_OK;
}

static esp_err_t wifiPostHandler(httpd_req_t *req)
{
    char buf[256];
    int len = httpd_req_recv(req, buf, sizeof(buf) - 1);
    if (len <= 0) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "No body");
        return ESP_FAIL;
    }
    buf[len] = 0;

    cJSON *root = cJSON_Parse(buf);
    if (!root) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Invalid JSON");
        return ESP_FAIL;
    }

    const cJSON *ssid = cJSON_GetObjectItem(root, "ssid");
    const cJSON *password = cJSON_GetObjectItem(root, "password");
    if (!cJSON_IsString(ssid) || !ssid->valuestring) {
        cJSON_Delete(root);
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Missing ssid");
        return ESP_FAIL;
    }

    const char *ssid_str = ssid->valuestring;
    const char *pass_str = (cJSON_IsString(password) && password->valuestring) ? password->valuestring : "";

    ESP_LOGI(TAG, "Received Wi-Fi credentials: ssid='%s'", ssid_str);
    appState.staSsid = ssid_str;

    startStaConnect(ssid_str, pass_str);

    cJSON *resp = cJSON_CreateObject();
    cJSON_AddStringToObject(resp, "status", "ok");
    char *resp_str = cJSON_PrintUnformatted(resp);

    httpd_resp_set_type(req, "application/json");
    httpd_resp_sendstr(req, resp_str);

    cJSON_free(resp_str);
    cJSON_Delete(resp);
    cJSON_Delete(root);

    return ESP_OK;
}

static esp_err_t statusGetHandler(httpd_req_t *req)
{
    cJSON *root = cJSON_CreateObject();

    if (appState.wifiConnected) {
        cJSON_AddStringToObject(root, "state", "connected");
        cJSON_AddStringToObject(root, "staIpStr", appState.staIpStr.c_str());
        cJSON_AddStringToObject(root, "mdnsHostStr", appState.mdnsHostStr.c_str());
        cJSON_AddStringToObject(root, "ssid", appState.staSsid.c_str());
    } else if (appState.wifiError) {
        cJSON_AddStringToObject(root, "state", "error");
        if (!appState.wifiErrorReason.empty()) {
            cJSON_AddStringToObject(root, "wifiErrorReason", appState.wifiErrorReason.c_str());
        }
    } else {
        cJSON_AddStringToObject(root, "state", "connecting");
    }

    char *resp_str = cJSON_PrintUnformatted(root);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_sendstr(req, resp_str);

    cJSON_free(resp_str);
    cJSON_Delete(root);
    return ESP_OK;
}

static esp_err_t captiveCatchallHandler(httpd_req_t *req)
{
    return rootGetHandler(req);
}

static httpd_handle_t startWebserver()
{
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    config.server_port = 80;
    config.max_uri_handlers = 32;
    config.uri_match_fn = httpd_uri_match_wildcard;

    httpd_handle_t server = nullptr;

    if (httpd_start(&server, &config) == ESP_OK)
    {
        ESP_LOGI(TAG, "Provisioning HTTP server started on port %d", config.server_port);
        static httpd_uri_t root_uri = { "/", HTTP_GET, rootGetHandler, nullptr };
        static httpd_uri_t scan_uri = { "/scan", HTTP_GET, scanGetHandler, nullptr };
        static httpd_uri_t wifi_uri = { "/wifi", HTTP_POST, wifiPostHandler, nullptr };
        static httpd_uri_t status_uri = { "/status", HTTP_GET, statusGetHandler, nullptr };
        static httpd_uri_t reset_wifi_uri = { "/reset_wifi", HTTP_POST, resetWifiHandler, nullptr };
        static httpd_uri_t close_ap_uri = { "/close_ap", HTTP_POST, closeApHandler, nullptr };
        static httpd_uri_t app_uri = { "/app", HTTP_GET, appGetHandler, nullptr };
        static httpd_uri_t css_uri = { "/styles.css", HTTP_GET, stylesCssGetHandler, nullptr };
        static httpd_uri_t matter_info_uri = { "/matter_info", HTTP_GET, matterInfoHandler, nullptr };
        static httpd_uri_t js_uri = { "/provisioning.js", HTTP_GET, provisioningJsHandler, nullptr };

        httpd_register_uri_handler(server, &app_uri);
        httpd_register_uri_handler(server, &root_uri);
        httpd_register_uri_handler(server, &scan_uri);
        httpd_register_uri_handler(server, &wifi_uri);
        httpd_register_uri_handler(server, &status_uri);
        httpd_register_uri_handler(server, &reset_wifi_uri);
        httpd_register_uri_handler(server, &close_ap_uri);
        httpd_register_uri_handler(server, &css_uri);
        httpd_register_uri_handler(server, &matter_info_uri);
        httpd_register_uri_handler(server, &js_uri);

        static httpd_uri_t apple_captive_uri = { "/hotspot-detect.html", HTTP_GET, rootGetHandler, nullptr };
        httpd_register_uri_handler(server, &apple_captive_uri);
        static httpd_uri_t android_generate_204 = { "/generate_204", HTTP_GET, rootGetHandler, nullptr };
        httpd_register_uri_handler(server, &android_generate_204);
        static httpd_uri_t android_gen_204 = { "/gen_204", HTTP_GET, rootGetHandler, nullptr };
        httpd_register_uri_handler(server, &android_gen_204);
        static httpd_uri_t windows_ncsi = { "/ncsi.txt", HTTP_GET, rootGetHandler, nullptr };
        httpd_register_uri_handler(server, &windows_ncsi);
        static httpd_uri_t windows_connecttest = { "/connecttest.txt", HTTP_GET, rootGetHandler, nullptr };
        httpd_register_uri_handler(server, &windows_connecttest);
        static httpd_uri_t firefox_canonical = { "/canonical.html", HTTP_GET, rootGetHandler, nullptr };
        httpd_register_uri_handler(server, &firefox_canonical);

        static httpd_uri_t catchall_uri = { "/*", HTTP_GET, captiveCatchallHandler, nullptr };
        httpd_register_uri_handler(server, &catchall_uri);
    }

    return server;
}

static void startHttpServer()
{
    g_http_server = startWebserver();
}

static void stopWebserver()
{
    if (g_http_server) {
        ESP_LOGI(TAG, "Stopping provisioning HTTP server");
        httpd_stop(g_http_server);
        g_http_server = nullptr;
    }
}

void wifiProvisioningCloseAp(void)
{
    shutdownAP();
}

const char* wifiProvisioningGetHostname(void)
{
    return appState.mdnsHostStr.c_str();
}

const char* wifiProvisioningGetSsid(void)
{
    return appState.staSsid.c_str();
}

esp_err_t wifiProvisioningStart(const wifiProvisioningConfig *config)
{
    if (!config || !config->apSsid) {
        return ESP_ERR_INVALID_ARG;
    }
    provConfig = *config;

    // Generate the hostname early so it's available for mDNS initialization
    uint8_t mac[6];
    esp_read_mac(mac, ESP_MAC_WIFI_STA);
    char host[32];
    snprintf(host, sizeof(host), "homeyantric-%02d", mac[5] % 100);
    appState.mdnsHostStr = host;
    ESP_LOGI(TAG, "Starting Wi-Fi Provisioning...");

    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    wifiEventGroup = xEventGroupCreate();

    esp_netif_create_default_wifi_sta();

    // Initialize mDNS service once after netif has been created
    ESP_ERROR_CHECK(mdns_init());
    ESP_ERROR_CHECK(mdns_hostname_set(appState.mdnsHostStr.c_str()));
    ESP_ERROR_CHECK(mdns_instance_name_set("HomeYantric Device"));

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &wifiEventHandler, NULL, NULL));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &wifiEventHandler, NULL, NULL));

    // Try existing STA credentials first
    wifi_config_t stored_cfg = {};
    esp_wifi_get_config(WIFI_IF_STA, &stored_cfg);
    bool hasCreds = stored_cfg.sta.ssid[0] != 0;
    if (hasCreds) {
        ESP_LOGI(TAG, "Found stored Wi-Fi credentials for '%s', trying STA first", stored_cfg.sta.ssid);
        ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
        ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &stored_cfg));
        ESP_ERROR_CHECK(esp_wifi_start());
        esp_err_t conn_ret = esp_wifi_connect();
        if (conn_ret == ESP_ERR_WIFI_CONN) {
            // Already connecting; continue without failing hard
            ESP_LOGW(TAG, "esp_wifi_connect returned ESP_ERR_WIFI_CONN, continuing");
        } else {
            ESP_ERROR_CHECK(conn_ret);
        }
        // If connection fails, wifiEventHandler will fall back to AP
        return ESP_OK;
    }

    startSoftAP();
    startHttpServer();
    startDnsCaptivePortal();

    ESP_LOGI(TAG, "Wi-Fi provisioning started.");
    return ESP_OK;
}

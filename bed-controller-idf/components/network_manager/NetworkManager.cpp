#include "NetworkManager.h"
#include "Config.h"
#include "esp_log.h"
#include "esp_ota_ops.h"
#include "cJSON.h"
#include "esp_sntp.h" 
#include "esp_timer.h"
#include "esp_netif.h"
#include "mdns.h"
#include "esp_wifi.h"
#include "esp_system.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "BedDriver.h"
#include "build_info.h"
#include "driver/gpio.h"
#include "LightControl.h"
#include <sys/stat.h>
#include <time.h>
#include <sys/time.h>
#include <string>
#include <cstring>
#include <algorithm> // Needed for std::transform
#include <sstream>

static const char *TAG = "NET_MGR";
#if APP_ROLE_BED
extern BedDriver* bedDriver;
#endif

// Shared Globals
extern std::string activeCommandLog; 
static time_t boot_epoch = 0;
static NetworkManager* s_instance = nullptr;
static bool s_light_initialized = false;
static bool s_light_state = false;
static LightControl s_light;

// Embedded (gzipped) web assets
extern const unsigned char _binary_index_html_gz_start[] asm("_binary_index_html_gz_start");
extern const unsigned char _binary_index_html_gz_end[] asm("_binary_index_html_gz_end");
extern const unsigned char _binary_app_js_gz_start[] asm("_binary_app_js_gz_start");
extern const unsigned char _binary_app_js_gz_end[] asm("_binary_app_js_gz_end");
extern const unsigned char _binary_bed_visualizer_js_gz_start[] asm("_binary_bed_visualizer_js_gz_start");
extern const unsigned char _binary_bed_visualizer_js_gz_end[] asm("_binary_bed_visualizer_js_gz_end");
extern const unsigned char _binary_style_css_gz_start[] asm("_binary_style_css_gz_start");
extern const unsigned char _binary_style_css_gz_end[] asm("_binary_style_css_gz_end");
extern const unsigned char _binary_sw_js_gz_start[] asm("_binary_sw_js_gz_start");
extern const unsigned char _binary_sw_js_gz_end[] asm("_binary_sw_js_gz_end");
extern const unsigned char _binary_branding_json_gz_start[] asm("_binary_branding_json_gz_start");
extern const unsigned char _binary_branding_json_gz_end[] asm("_binary_branding_json_gz_end");
extern const unsigned char _binary_favicon_png_gz_start[] asm("_binary_favicon_png_gz_start");
extern const unsigned char _binary_favicon_png_gz_end[] asm("_binary_favicon_png_gz_end");

// Forward declarations for HTTP handlers
static esp_err_t log_handler(httpd_req_t *req);
static esp_err_t file_server_handler(httpd_req_t *req);
static esp_err_t rpc_command_handler(httpd_req_t *req);
static esp_err_t rpc_status_handler(httpd_req_t *req);
static esp_err_t light_command_handler(httpd_req_t *req);
static esp_err_t light_status_handler(httpd_req_t *req);
static esp_err_t role_disabled_handler(httpd_req_t *req);
static esp_err_t legacy_status_handler(httpd_req_t *req);
static esp_err_t close_ap_handler(httpd_req_t *req);
static esp_err_t reset_wifi_handler(httpd_req_t *req);
static esp_err_t ota_upload_handler(httpd_req_t *req);

// Static URI handler definitions (must outlive httpd_start)
static const httpd_uri_t URI_IDX    = { .uri = "/",            .method = HTTP_GET,  .handler = file_server_handler, .user_ctx = NULL };
static const httpd_uri_t URI_INDEX  = { .uri = "/index.html",  .method = HTTP_GET,  .handler = file_server_handler, .user_ctx = NULL };
static const httpd_uri_t URI_APP    = { .uri = "/app",         .method = HTTP_GET,  .handler = file_server_handler, .user_ctx = NULL };
static const httpd_uri_t URI_STYLE  = { .uri = "/style.css",   .method = HTTP_GET,  .handler = file_server_handler, .user_ctx = NULL };
static const httpd_uri_t URI_JS     = { .uri = "/app.js",      .method = HTTP_GET,  .handler = file_server_handler, .user_ctx = NULL };
static const httpd_uri_t URI_VIS    = { .uri = "/bed-visualizer.js", .method = HTTP_GET, .handler = file_server_handler, .user_ctx = NULL };
static const httpd_uri_t URI_ICON   = { .uri = "/favicon.png", .method = HTTP_GET,  .handler = file_server_handler, .user_ctx = NULL };
static const httpd_uri_t URI_FAVICO = { .uri = "/favicon.ico", .method = HTTP_GET,  .handler = file_server_handler, .user_ctx = NULL };
static const httpd_uri_t URI_SW     = { .uri = "/sw.js", .method = HTTP_GET, .handler = file_server_handler, .user_ctx = NULL };
static const httpd_uri_t URI_BRAND  = { .uri = "/branding.json", .method = HTTP_GET, .handler = file_server_handler, .user_ctx = NULL };
static const httpd_uri_t URI_CMD    = { .uri = "/rpc/Bed.Command", .method = HTTP_POST, .handler = rpc_command_handler, .user_ctx = NULL };
static const httpd_uri_t URI_STATUS = { .uri = "/rpc/Bed.Status",  .method = HTTP_POST, .handler = rpc_status_handler,  .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_CMD = { .uri = "/rpc/Light.Command", .method = HTTP_POST, .handler = light_command_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_STATUS = { .uri = "/rpc/Light.Status", .method = HTTP_POST, .handler = light_status_handler, .user_ctx = NULL };
static const httpd_uri_t URI_BED_STATUS_DISABLED = { .uri = "/rpc/Bed.Status", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"bed" };
static const httpd_uri_t URI_BED_CMD_DISABLED = { .uri = "/rpc/Bed.Command", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"bed" };
static const httpd_uri_t URI_TRAY_STATUS_DISABLED = { .uri = "/rpc/Tray.Status", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"tray" };
static const httpd_uri_t URI_CURTAIN_STATUS_DISABLED = { .uri = "/rpc/Curtains.Status", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"curtains" };
static const httpd_uri_t URI_LEGACY_STATUS = { .uri = "/status", .method = HTTP_GET, .handler = legacy_status_handler, .user_ctx = NULL };
static const httpd_uri_t URI_CLOSE_AP = { .uri = "/close_ap", .method = HTTP_POST, .handler = close_ap_handler, .user_ctx = NULL };
static const httpd_uri_t URI_RESET_WIFI = { .uri = "/reset_wifi", .method = HTTP_POST, .handler = reset_wifi_handler, .user_ctx = NULL };
static const httpd_uri_t URI_OTA = { .uri = "/rpc/Bed.OTA", .method = HTTP_POST, .handler = ota_upload_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LOG = { .uri = "/rpc/Bed.Log", .method = HTTP_POST, .handler = log_handler, .user_ctx = NULL };

static void onProvisioned(const char* sta_ip) {
    ESP_LOGI(TAG, "Provisioning complete. STA IP: %s", sta_ip ? sta_ip : "unknown");
    if (s_instance) {
        ESP_LOGI(TAG, "Client connected via STA, starting main services");
        s_instance->startSntp();
        s_instance->startMdns();
        s_instance->startWebServer();
    }
}

// Forward declarations for HTTP handlers
static esp_err_t file_server_handler(httpd_req_t *req) {
    char path[64];
    const char *uri = req->uri;
    const char *q = strchr(uri, '?');
    size_t plen = q ? (size_t)(q - uri) : strlen(uri);
    if (plen >= sizeof(path)) plen = sizeof(path) - 1;
    memcpy(path, uri, plen);
    path[plen] = '\0';
    struct EmbeddedAsset {
        const char* path;
        const unsigned char* start;
        const unsigned char* end;
        const char* ctype;
    };
    static const EmbeddedAsset assets[] = {
        { "/", _binary_index_html_gz_start, _binary_index_html_gz_end, "text/html" },
        { "/index.html", _binary_index_html_gz_start, _binary_index_html_gz_end, "text/html" },
        { "/app", _binary_index_html_gz_start, _binary_index_html_gz_end, "text/html" },
        { "/style.css", _binary_style_css_gz_start, _binary_style_css_gz_end, "text/css" },
        { "/app.js", _binary_app_js_gz_start, _binary_app_js_gz_end, "application/javascript" },
        { "/bed-visualizer.js", _binary_bed_visualizer_js_gz_start, _binary_bed_visualizer_js_gz_end, "application/javascript" },
        { "/favicon.png", _binary_favicon_png_gz_start, _binary_favicon_png_gz_end, "image/png" },
        { "/favicon.ico", _binary_favicon_png_gz_start, _binary_favicon_png_gz_end, "image/png" },
        { "/sw.js", _binary_sw_js_gz_start, _binary_sw_js_gz_end, "application/javascript" },
        { "/branding.json", _binary_branding_json_gz_start, _binary_branding_json_gz_end, "application/json" },
    };

    const EmbeddedAsset* found = nullptr;
    for (auto &a : assets) {
        if (strcmp(path, a.path) == 0) { found = &a; break; }
    }
    if (!found) {
        httpd_resp_send_404(req);
        return ESP_FAIL;
    }

    httpd_resp_set_type(req, found->ctype);
    httpd_resp_set_hdr(req, "Content-Encoding", "gzip");
    httpd_resp_set_hdr(req, "Cache-Control", "no-cache, no-store, must-revalidate");

    size_t len = found->end - found->start;
    return httpd_resp_send(req, (const char*)found->start, len);
}

// Light control
static void light_apply_state(bool on) {
    if (!s_light_initialized) return;
    s_light_state = on;
    s_light.setState(on);
}

static esp_err_t light_command_handler(httpd_req_t *req) {
    char buf[128] = {0};
    int ret = httpd_req_recv(req, buf, sizeof(buf) - 1);
    if (ret > 0) buf[ret] = '\0';
    cJSON *root = cJSON_Parse(buf);
    if (!root) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad JSON");
        return ESP_FAIL;
    }
    cJSON *cmd = cJSON_GetObjectItem(root, "cmd");
    if (cJSON_IsString(cmd) && cmd->valuestring) {
        std::string s = cmd->valuestring;
        std::transform(s.begin(), s.end(), s.begin(), ::toupper);
        if (s == "ON") light_apply_state(true);
        else if (s == "OFF") light_apply_state(false);
        else if (s == "TOGGLE") light_apply_state(!s_light_state);
    }
    cJSON_Delete(root);

    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", "ok");
    cJSON_AddStringToObject(res, "state", s_light_state ? "on" : "off");
    cJSON_AddNumberToObject(res, "gpio", LIGHT_GPIO);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
}

static esp_err_t light_status_handler(httpd_req_t *req) {
    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", "ok");
    cJSON_AddStringToObject(res, "state", s_light_state ? "on" : "off");
    cJSON_AddNumberToObject(res, "gpio", LIGHT_GPIO);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
}

// Legacy status endpoint (used by provisioning captive portal); respond with ok to avoid 404 spam
static esp_err_t legacy_status_handler(httpd_req_t *req) {
    // Answer provisioning-era /status endpoint so clients don't spin
    char ip_str[16] = "0.0.0.0";
    esp_netif_t *sta = esp_netif_get_handle_from_ifkey("WIFI_STA_DEF");
    if (sta) {
        esp_netif_ip_info_t info;
        if (esp_netif_get_ip_info(sta, &info) == ESP_OK) {
            snprintf(ip_str, sizeof(ip_str), IPSTR, IP2STR(&info.ip));
        }
    }
    std::string hostStr = wifiProvisioningGetHostname();
    std::string ssidStr = wifiProvisioningGetSsid();
    char resp[256];
    int len = snprintf(resp, sizeof(resp),
                       "{\"state\":\"connected\",\"staIpStr\":\"%s\",\"mdnsHostStr\":\"%s\",\"ssid\":\"%s\"}",
                       ip_str, hostStr.c_str(), ssidStr.c_str());
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, resp, len);
    return ESP_OK;
}

// UI log sink: record client-side messages to serial
static esp_err_t log_handler(httpd_req_t *req) {
    char buf[256] = {0};
    int ret = httpd_req_recv(req, buf, sizeof(buf) - 1);
    if (ret <= 0) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "No body");
        return ESP_FAIL;
    }
    buf[ret] = '\0';
    cJSON *root = cJSON_Parse(buf);
    if (!root) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad JSON");
        return ESP_FAIL;
    }
    cJSON *msg = cJSON_GetObjectItem(root, "msg");
    const char *text = (cJSON_IsString(msg) && msg->valuestring) ? msg->valuestring : "";
    ESP_LOGI(TAG, "%s", text);
    cJSON_Delete(root);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_sendstr(req, "{\"status\":\"ok\"}");
    return ESP_OK;
}

// Allow provisioning UI to close AP after success
static esp_err_t close_ap_handler(httpd_req_t *req) {
    ESP_LOGI(TAG, "Received /close_ap request");
    wifiProvisioningCloseAp();
    const char resp[] = "{\"status\":\"ok\"}";
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, resp, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

// Reset Wi-Fi credentials and restart
static esp_err_t reset_wifi_handler(httpd_req_t *req) {
    ESP_LOGW(TAG, "Received /reset_wifi request");
    esp_wifi_restore();
    const char resp[] = "{\"status\":\"ok\"}";
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, resp, HTTPD_RESP_USE_STRLEN);
    vTaskDelay(pdMS_TO_TICKS(200));
    esp_restart();
    return ESP_OK;
}

static esp_err_t ota_upload_handler(httpd_req_t *req) {
    const esp_partition_t *update_partition = esp_ota_get_next_update_partition(NULL);
    if (update_partition == NULL) {
        httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "No OTA partition");
        return ESP_FAIL;
    }

    if (req->content_len <= 0) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "No firmware");
        return ESP_FAIL;
    }

    if ((size_t)req->content_len > update_partition->size) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Firmware too large for partition");
        return ESP_FAIL;
    }

    esp_ota_handle_t ota_handle = 0;
    esp_err_t err = esp_ota_begin(update_partition, req->content_len, &ota_handle);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "esp_ota_begin failed: %s", esp_err_to_name(err));
        httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "OTA begin failed");
        return ESP_FAIL;
    }

    int remaining = req->content_len;
    char buf[1024];
    while (remaining > 0) {
        int to_read = std::min<int>(remaining, sizeof(buf));
        int read = httpd_req_recv(req, buf, to_read);
        if (read <= 0) {
            if (read == HTTPD_SOCK_ERR_TIMEOUT) continue;
            ESP_LOGE(TAG, "OTA recv error");
            esp_ota_end(ota_handle);
            httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Recv error");
            return ESP_FAIL;
        }
        err = esp_ota_write(ota_handle, buf, read);
        if (err != ESP_OK) {
            ESP_LOGE(TAG, "esp_ota_write failed: %s", esp_err_to_name(err));
            esp_ota_end(ota_handle);
            httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Write failed");
            return ESP_FAIL;
        }
        remaining -= read;
    }

    err = esp_ota_end(ota_handle);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "esp_ota_end failed: %s", esp_err_to_name(err));
        httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Finalize failed");
        return ESP_FAIL;
    }

    err = esp_ota_set_boot_partition(update_partition);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "esp_ota_set_boot_partition failed: %s", esp_err_to_name(err));
        httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Set boot failed");
        return ESP_FAIL;
    }

    httpd_resp_set_type(req, "application/json");
    httpd_resp_sendstr(req, "{\"result\":\"ok\",\"reboot\":true}");
    ESP_LOGI(TAG, "OTA update written to %s, rebooting", update_partition->label);
    vTaskDelay(pdMS_TO_TICKS(200));
    esp_restart();
    return ESP_OK;
}

static esp_err_t rpc_command_handler(httpd_req_t *req) {
#if !APP_ROLE_BED
    httpd_resp_send_err(req, HTTPD_501_METHOD_NOT_IMPLEMENTED, "Bed role not enabled");
    return ESP_OK;
#else
    char buf[512];
    int ret = httpd_req_recv(req, buf, sizeof(buf) - 1);
    if (ret <= 0) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "No body");
        return ESP_FAIL;
    }
    buf[ret] = '\0';

    cJSON *root = cJSON_Parse(buf);
    if (root == nullptr) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad JSON");
        return ESP_FAIL;
    }

    cJSON *cmdItem = cJSON_GetObjectItem(root, "cmd");
    cJSON *lblItem = cJSON_GetObjectItem(root, "label");
    cJSON *headMaxItem = cJSON_GetObjectItem(root, "headMax");
    cJSON *footMaxItem = cJSON_GetObjectItem(root, "footMax");
    
    if (!cJSON_IsString(cmdItem)) {
        cJSON_Delete(root);
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Missing cmd");
        return ESP_FAIL;
    }

    std::string cmd = cmdItem->valuestring;
    std::string label = (cJSON_IsString(lblItem)) ? lblItem->valuestring : "";
    
    long maxWait = 0;
    std::string savedSlot = ""; // Track which slot was modified

    int32_t headMaxMs = 0, footMaxMs = 0;
    bedDriver->getLimits(headMaxMs, footMaxMs);

    // --- COMMAND LOGIC ---
    if (cmd == "STOP") { bedDriver->stop(); activeCommandLog = "IDLE"; } 
    else if (cmd == "HEAD_UP") { bedDriver->moveHead("UP"); activeCommandLog = "HEAD_UP"; }
    else if (cmd == "HEAD_DOWN") { bedDriver->moveHead("DOWN"); activeCommandLog = "HEAD_DOWN"; }
    else if (cmd == "FOOT_UP") { bedDriver->moveFoot("UP"); activeCommandLog = "FOOT_UP"; }
    else if (cmd == "FOOT_DOWN") { bedDriver->moveFoot("DOWN"); activeCommandLog = "FOOT_DOWN"; }
    else if (cmd == "ALL_UP") { bedDriver->moveAll("UP"); activeCommandLog = "ALL_UP"; }
    else if (cmd == "ALL_DOWN") { bedDriver->moveAll("DOWN"); activeCommandLog = "ALL_DOWN"; }
    
    // Fixed Presets
    else if (cmd == "FLAT") { maxWait = bedDriver->setTarget(0, 0); activeCommandLog = "FLAT"; }
    else if (cmd == "MAX") { maxWait = bedDriver->setTarget(headMaxMs, footMaxMs); activeCommandLog = "MAX"; }

    else if (cmd == "SET_LIMITS") {
        int32_t newHeadMs = headMaxMs;
        int32_t newFootMs = footMaxMs;
        if (cJSON_IsNumber(headMaxItem)) newHeadMs = (int32_t)(headMaxItem->valuedouble * 1000);
        if (cJSON_IsNumber(footMaxItem)) newFootMs = (int32_t)(footMaxItem->valuedouble * 1000);
        bedDriver->setLimits(newHeadMs, newFootMs);
        bedDriver->getLimits(headMaxMs, footMaxMs);
        activeCommandLog = "SET_LIMITS";
    }
    
    // Saved Presets
    else if (cmd == "ZERO_G") {
        maxWait = bedDriver->setTarget(bedDriver->getSavedPos("zg_head", 10000), bedDriver->getSavedPos("zg_foot", 40000));
        activeCommandLog = "ZERO_G";
    }
    else if (cmd == "ANTI_SNORE") {
        maxWait = bedDriver->setTarget(bedDriver->getSavedPos("snore_head", 10000), bedDriver->getSavedPos("snore_foot", 0));
        activeCommandLog = "ANTI_SNORE";
    }
    else if (cmd == "LEGS_UP") {
        maxWait = bedDriver->setTarget(bedDriver->getSavedPos("legs_head", 0), bedDriver->getSavedPos("legs_foot", 43000));
        activeCommandLog = "LEGS_UP";
    }
    else if (cmd == "P1") {
        maxWait = bedDriver->setTarget(bedDriver->getSavedPos("p1_head", 0), bedDriver->getSavedPos("p1_foot", 0));
        activeCommandLog = "P1";
    }
    else if (cmd == "P2") {
        maxWait = bedDriver->setTarget(bedDriver->getSavedPos("p2_head", 0), bedDriver->getSavedPos("p2_foot", 0));
        activeCommandLog = "P2";
    }

    // --- SAVE LOGIC ---
    else if (cmd.find("SET_") == 0) {
        // Example: SET_P1_POS or SET_ZG_LABEL
        // Extract Slot (e.g. "P1")
        size_t endPos = std::string::npos;
        if (cmd.find("_POS") != std::string::npos) endPos = cmd.find("_POS");
        else if (cmd.find("_LABEL") != std::string::npos) endPos = cmd.find("_LABEL");
        
        if (endPos != std::string::npos) {
            std::string slot = cmd.substr(4, endPos - 4);
            std::transform(slot.begin(), slot.end(), slot.begin(), ::tolower); // p1
            savedSlot = slot;

            if (cmd.find("_POS") != std::string::npos) {
                int32_t h, f;
                bedDriver->getLiveStatus(h, f);
                bedDriver->setSavedPos((slot + "_head").c_str(), h);
                bedDriver->setSavedPos((slot + "_foot").c_str(), f);
            } 
            else if (cmd.find("_LABEL") != std::string::npos) {
                // FIX: Now actually saving the label to NVS
                bedDriver->setSavedLabel((slot + "_label").c_str(), label);
            }
        }
    }
    
    // --- RESET LOGIC ---
    else if (cmd.find("RESET_") == 0) {
        std::string slot = cmd.substr(6); // Reset RESET_P1 -> P1
        std::transform(slot.begin(), slot.end(), slot.begin(), ::tolower);
        savedSlot = slot;
        
        bedDriver->setSavedPos((slot + "_head").c_str(), 0);
        bedDriver->setSavedPos((slot + "_foot").c_str(), 0);
        
        // Restore Default Labels
        std::string defLbl = "Preset";
        if(slot=="zg") defLbl="Zero G"; else if(slot=="snore") defLbl="Anti-Snore"; 
        else if(slot=="legs") defLbl="Legs Up"; else if(slot=="p1") defLbl="P1"; else if(slot=="p2") defLbl="P2";
        
        bedDriver->setSavedLabel((slot + "_label").c_str(), defLbl);
    }

    cJSON_Delete(root);

    // --- BUILD RESPONSE ---
    cJSON *res = cJSON_CreateObject();

    int32_t h, f;
    bedDriver->getLiveStatus(h, f);

    // Boot Time
    time_t now;
    time(&now);
    double bTime = (boot_epoch > 0) ? (double)boot_epoch : 1.0; 
    cJSON_AddNumberToObject(res, "bootTime", bTime);
    cJSON_AddNumberToObject(res, "uptime", esp_timer_get_time() / 1000000);

    cJSON_AddNumberToObject(res, "headPos", h / 1000.0);
    cJSON_AddNumberToObject(res, "footPos", f / 1000.0);
    cJSON_AddNumberToObject(res, "maxWait", maxWait);
    cJSON_AddNumberToObject(res, "headMax", headMaxMs / 1000.0);
    cJSON_AddNumberToObject(res, "footMax", footMaxMs / 1000.0);
    
    // FIX: Send back the saved data so the UI updates immediately
    if (!savedSlot.empty()) {
        // JS looks for 'saved_label' or 'saved_pos' to trigger updates
        if (cmd.find("_LABEL") != std::string::npos || cmd.find("RESET_") != std::string::npos) {
             cJSON_AddStringToObject(res, "saved_label", savedSlot.c_str());
        } else {
             cJSON_AddStringToObject(res, "saved_pos", savedSlot.c_str());
        }
        
        // Fetch the NEW values from NVS to confirm they stuck
        cJSON_AddNumberToObject(res, (savedSlot + "_head").c_str(), bedDriver->getSavedPos((savedSlot+"_head").c_str(), 0));
        cJSON_AddNumberToObject(res, (savedSlot + "_foot").c_str(), bedDriver->getSavedPos((savedSlot+"_foot").c_str(), 0));
        cJSON_AddStringToObject(res, (savedSlot + "_label").c_str(), bedDriver->getSavedLabel((savedSlot+"_label").c_str(), "Preset").c_str());
    }

    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);

    free(jsonStr);
    cJSON_Delete(res);

    return ESP_OK;
#endif
}

static esp_err_t rpc_status_handler(httpd_req_t *req) {
#if !APP_ROLE_BED
    httpd_resp_send_err(req, HTTPD_501_METHOD_NOT_IMPLEMENTED, "Bed role not enabled");
    return ESP_OK;
#else
    cJSON *res = cJSON_CreateObject();

    int32_t h, f;
    bedDriver->getLiveStatus(h, f);
    std::string hDir = "STOPPED", fDir = "STOPPED";
    bedDriver->getMotionDirs(hDir, fDir);
    int o1=1,o2=1,o3=1,o4=1;
    bedDriver->getOptoStates(o1,o2,o3,o4);
    int32_t headMaxMs = 0, footMaxMs = 0;
    bedDriver->getLimits(headMaxMs, footMaxMs);

    time_t now;
    time(&now);
    struct tm timeinfo;
    localtime_r(&now, &timeinfo);
    
    if (timeinfo.tm_year > (2020 - 1900) && boot_epoch == 0) {
        boot_epoch = now - (esp_timer_get_time() / 1000000);
    }
    
    double bTime = (boot_epoch > 0) ? (double)boot_epoch : 1.0; 
    cJSON_AddNumberToObject(res, "bootTime", bTime);

    cJSON_AddNumberToObject(res, "uptime", esp_timer_get_time() / 1000000);
    cJSON_AddNumberToObject(res, "headPos", h / 1000.0);
    cJSON_AddNumberToObject(res, "footPos", f / 1000.0);
    cJSON_AddNumberToObject(res, "headMax", headMaxMs / 1000.0);
    cJSON_AddNumberToObject(res, "footMax", footMaxMs / 1000.0);
    cJSON_AddStringToObject(res, "headDir", hDir.c_str());
    cJSON_AddStringToObject(res, "footDir", fDir.c_str());
    cJSON_AddNumberToObject(res, "opto1", o1);
    cJSON_AddNumberToObject(res, "opto2", o2);
    cJSON_AddNumberToObject(res, "opto3", o3);
    cJSON_AddNumberToObject(res, "opto4", o4);

    const char *slots[] = {"zg", "snore", "legs", "p1", "p2"};
    for (int i = 0; i < 5; ++i) {
        std::string base = slots[i];
        cJSON_AddNumberToObject(res, (base + "_head").c_str(), bedDriver->getSavedPos((base + "_head").c_str(), 0));
        cJSON_AddNumberToObject(res, (base + "_foot").c_str(), bedDriver->getSavedPos((base + "_foot").c_str(), 0));
        
        // Fetch Label from NVS
        std::string lbl = bedDriver->getSavedLabel((base + "_label").c_str(), "Preset");
        cJSON_AddStringToObject(res, (base + "_label").c_str(), lbl.c_str());
    }

    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);

    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
#endif
}

// Generic handler for disabled roles/endpoints to avoid 404 spam
static esp_err_t role_disabled_handler(httpd_req_t *req) {
    const char* name = (const char*)req->user_ctx;
    const char* role = name ? name : "disabled";
    httpd_resp_set_type(req, "application/json");
    char resp[64];
    int len = snprintf(resp, sizeof(resp), "{\"status\":\"disabled\",\"role\":\"%s\"}", role);
    httpd_resp_send(req, resp, len);
    return ESP_OK;
}

void NetworkManager::begin() {
    s_instance = this;
    ESP_LOGI(TAG, "Build: %s", UI_BUILD_TAG);
    esp_ota_mark_app_valid_cancel_rollback();

    // Initialize light GPIO (default OFF)
    if (s_light.begin((gpio_num_t)LIGHT_GPIO, true) == ESP_OK) {
        s_light_initialized = true;
        s_light_state = false;
    }

    wifiProvisioningConfig cfg = {
        .apSsid = "HomeYantric-Setup",
        .onSuccess = onProvisioned
    };
    esp_err_t err = wifiProvisioningStart(&cfg);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Provisioning start failed: %s", esp_err_to_name(err));
    }
}

void NetworkManager::startSntp() {
    esp_sntp_setoperatingmode(SNTP_OPMODE_POLL);
    esp_sntp_setservername(0, "pool.ntp.org");
    esp_sntp_init();
}

void NetworkManager::startWebServer() {
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    config.max_uri_handlers = 32; // allow extra endpoints
    config.uri_match_fn = httpd_uri_match_wildcard;
    config.lru_purge_enable = true;

    if (httpd_start(&server, &config) == ESP_OK) {
        ESP_LOGI(TAG, "Main HTTP server started on port %d", config.server_port);
        httpd_register_uri_handler(server, &URI_IDX);
        httpd_register_uri_handler(server, &URI_INDEX);
        httpd_register_uri_handler(server, &URI_APP);
        httpd_register_uri_handler(server, &URI_STYLE);
        httpd_register_uri_handler(server, &URI_JS);
        httpd_register_uri_handler(server, &URI_VIS);
        httpd_register_uri_handler(server, &URI_ICON);
        httpd_register_uri_handler(server, &URI_FAVICO);
        httpd_register_uri_handler(server, &URI_SW);
        httpd_register_uri_handler(server, &URI_BRAND);
#if APP_ROLE_BED
        httpd_register_uri_handler(server, &URI_CMD);
        httpd_register_uri_handler(server, &URI_STATUS);
#else
        httpd_register_uri_handler(server, &URI_BED_CMD_DISABLED);
        httpd_register_uri_handler(server, &URI_BED_STATUS_DISABLED);
#endif
#if APP_ROLE_LIGHT
        httpd_register_uri_handler(server, &URI_LIGHT_CMD);
        httpd_register_uri_handler(server, &URI_LIGHT_STATUS);
#endif
        // Absorb legacy tray/curtains polls from older UIs
        httpd_register_uri_handler(server, &URI_TRAY_STATUS_DISABLED);
        httpd_register_uri_handler(server, &URI_CURTAIN_STATUS_DISABLED);
        httpd_register_uri_handler(server, &URI_OTA);
        httpd_register_uri_handler(server, &URI_LOG);
        httpd_register_uri_handler(server, &URI_LEGACY_STATUS);
        httpd_register_uri_handler(server, &URI_CLOSE_AP);
        httpd_register_uri_handler(server, &URI_RESET_WIFI);
    }
}

void NetworkManager::startMdns() {
    // Init mDNS (may already be running from provisioning)
    esp_err_t err = mdns_init();
    if (err != ESP_OK && err != ESP_ERR_INVALID_STATE) {
        ESP_LOGE(TAG, "mDNS init failed: %s", esp_err_to_name(err));
        return;
    }
    std::string host = wifiProvisioningGetHostname();
    if (host.empty()) host = MDNS_HOSTNAME;
    mdns_hostname_set(host.c_str());
    esp_err_t svc_err = mdns_service_add(NULL, "_http", "_tcp", 80, NULL, 0);
    if (svc_err != ESP_OK && svc_err != ESP_ERR_INVALID_STATE && svc_err != ESP_ERR_INVALID_ARG) {
        ESP_LOGW(TAG, "mDNS http service add returned %s", esp_err_to_name(svc_err));
    }

    // Advertise custom service with role info
    svc_err = mdns_service_add(NULL, "_homeyantric", "_tcp", 80, NULL, 0);
    if (svc_err != ESP_OK && svc_err != ESP_ERR_INVALID_STATE && svc_err != ESP_ERR_INVALID_ARG) {
        ESP_LOGW(TAG, "mDNS homeyantric service add returned %s", esp_err_to_name(svc_err));
    }
    std::stringstream ss;
    bool first = true;
#if APP_ROLE_BED
    ss << (first ? "" : ",") << "bed";
    first = false;
#endif
#if APP_ROLE_LIGHT
    ss << (first ? "" : ",") << "light";
    first = false;
#endif
#if APP_ROLE_TRAY
    ss << (first ? "" : ",") << "tray";
    first = false;
#endif
    std::string roles = ss.str();
    if (roles.empty()) roles = "none";
    mdns_txt_item_t txt[] = {
        { (char *)"roles", (char *)roles.c_str() },
        { (char *)"fw", (char *)UI_BUILD_TAG }
    };
    mdns_service_txt_set("_homeyantric", "_tcp", txt, sizeof(txt)/sizeof(txt[0]));
    ESP_LOGI(TAG, "mDNS _homeyantric._tcp advertised host=%s roles=%s fw=%s", host.c_str(), roles.c_str(), UI_BUILD_TAG);
}

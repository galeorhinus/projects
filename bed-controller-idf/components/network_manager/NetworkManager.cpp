#include "NetworkManager.h"
#include "Config.h"
#include "esp_log.h"
#include "esp_spiffs.h"
#include "cJSON.h"
#include "esp_sntp.h" 
#include "esp_timer.h"
#include "esp_netif.h"
#include "mdns.h"
#include "esp_wifi.h"
#include "esp_system.h"
#include "BedDriver.h"
#include <sys/stat.h>
#include <time.h>
#include <sys/time.h>
#include <string>
#include <cstring>
#include <algorithm> // Needed for std::transform

static const char *TAG = "NET_MGR";
extern BedDriver* bedDriver;

// Shared Globals
extern std::string activeCommandLog; 
static time_t boot_epoch = 0;
static NetworkManager* s_instance = nullptr;

static void onProvisioned(const char* sta_ip) {
    ESP_LOGI(TAG, "Provisioning complete. STA IP: %s", sta_ip ? sta_ip : "unknown");
    if (s_instance) {
        ESP_LOGI(TAG, "Client connected via STA, starting main services");
        s_instance->startSntp();
        s_instance->startWebServer();
    }
}

// Forward declarations for HTTP handlers
static esp_err_t file_server_handler(httpd_req_t *req);
static esp_err_t rpc_command_handler(httpd_req_t *req);
static esp_err_t rpc_status_handler(httpd_req_t *req);
static esp_err_t tray_command_handler(httpd_req_t *req);
static esp_err_t tray_status_handler(httpd_req_t *req);
static esp_err_t curtains_command_handler(httpd_req_t *req);
static esp_err_t curtains_status_handler(httpd_req_t *req);
static esp_err_t legacy_status_handler(httpd_req_t *req);
static esp_err_t close_ap_handler(httpd_req_t *req);
static esp_err_t reset_wifi_handler(httpd_req_t *req);

// Static URI handler definitions (must outlive httpd_start)
static const char INDEX_PATH[] = "/spiffs/index.html";
static const char STYLE_PATH[] = "/spiffs/style.css";
static const char JS_PATH[]    = "/spiffs/app.js";
static const char VIS_PATH[]   = "/spiffs/bed-visualizer.js";
static const char ICON_PATH[]  = "/spiffs/favicon.png";
static const char MANIFEST_PATH[] = "/spiffs/manifest.webmanifest";
static const char SW_PATH[]    = "/spiffs/sw.js";
static const char BRANDING_PATH[] = "/spiffs/branding.json";

static const httpd_uri_t URI_IDX    = { .uri = "/",            .method = HTTP_GET,  .handler = file_server_handler, .user_ctx = (void*)INDEX_PATH };
static const httpd_uri_t URI_INDEX  = { .uri = "/index.html",  .method = HTTP_GET,  .handler = file_server_handler, .user_ctx = (void*)INDEX_PATH };
static const httpd_uri_t URI_APP    = { .uri = "/app",         .method = HTTP_GET,  .handler = file_server_handler, .user_ctx = (void*)INDEX_PATH };
static const httpd_uri_t URI_STYLE  = { .uri = "/style.css",   .method = HTTP_GET,  .handler = file_server_handler, .user_ctx = (void*)STYLE_PATH };
static const httpd_uri_t URI_JS     = { .uri = "/app.js",      .method = HTTP_GET,  .handler = file_server_handler, .user_ctx = (void*)JS_PATH };
static const httpd_uri_t URI_VIS    = { .uri = "/bed-visualizer.js", .method = HTTP_GET, .handler = file_server_handler, .user_ctx = (void*)VIS_PATH };
static const httpd_uri_t URI_ICON   = { .uri = "/favicon.png", .method = HTTP_GET,  .handler = file_server_handler, .user_ctx = (void*)ICON_PATH };
static const httpd_uri_t URI_FAVICO = { .uri = "/favicon.ico", .method = HTTP_GET,  .handler = file_server_handler, .user_ctx = (void*)ICON_PATH };
static const httpd_uri_t URI_MANIFEST = { .uri = "/manifest.webmanifest", .method = HTTP_GET, .handler = file_server_handler, .user_ctx = (void*)MANIFEST_PATH };
static const httpd_uri_t URI_SW     = { .uri = "/sw.js", .method = HTTP_GET, .handler = file_server_handler, .user_ctx = (void*)SW_PATH };
static const httpd_uri_t URI_BRAND  = { .uri = "/branding.json", .method = HTTP_GET, .handler = file_server_handler, .user_ctx = (void*)BRANDING_PATH };
static const httpd_uri_t URI_CMD    = { .uri = "/rpc/Bed.Command", .method = HTTP_POST, .handler = rpc_command_handler, .user_ctx = NULL };
static const httpd_uri_t URI_STATUS = { .uri = "/rpc/Bed.Status",  .method = HTTP_POST, .handler = rpc_status_handler,  .user_ctx = NULL };
static const httpd_uri_t URI_TRAY_CMD = { .uri = "/rpc/Tray.Command", .method = HTTP_POST, .handler = tray_command_handler, .user_ctx = NULL };
static const httpd_uri_t URI_TRAY_STATUS = { .uri = "/rpc/Tray.Status", .method = HTTP_POST, .handler = tray_status_handler, .user_ctx = NULL };
static const httpd_uri_t URI_CURTAIN_CMD = { .uri = "/rpc/Curtains.Command", .method = HTTP_POST, .handler = curtains_command_handler, .user_ctx = NULL };
static const httpd_uri_t URI_CURTAIN_STATUS = { .uri = "/rpc/Curtains.Status", .method = HTTP_POST, .handler = curtains_status_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LEGACY_STATUS = { .uri = "/status", .method = HTTP_GET, .handler = legacy_status_handler, .user_ctx = NULL };
static const httpd_uri_t URI_CLOSE_AP = { .uri = "/close_ap", .method = HTTP_POST, .handler = close_ap_handler, .user_ctx = NULL };
static const httpd_uri_t URI_RESET_WIFI = { .uri = "/reset_wifi", .method = HTTP_POST, .handler = reset_wifi_handler, .user_ctx = NULL };

static esp_err_t file_server_handler(httpd_req_t *req) {
    const char *filepath = (const char *)req->user_ctx;
    const char *ext = strrchr(filepath, '.');
    
    if (ext != NULL) {
        if (strcmp(ext, ".css") == 0) httpd_resp_set_type(req, "text/css");
        else if (strcmp(ext, ".js") == 0) httpd_resp_set_type(req, "application/javascript");
        else if (strcmp(ext, ".png") == 0) httpd_resp_set_type(req, "image/png");
        else if (strcmp(ext, ".html") == 0) httpd_resp_set_type(req, "text/html");
        else httpd_resp_set_type(req, "text/plain");
    } else {
        httpd_resp_set_type(req, "text/plain");
    }

    FILE *fd = fopen(filepath, "r");
    if (!fd) {
        httpd_resp_send_404(req);
        return ESP_FAIL;
    }

    // Attempt to send with Content-Length to avoid chunked encoding issues
    struct stat st;
    if (stat(filepath, &st) == 0 && st.st_size > 0 && st.st_size < 256 * 1024) {
        size_t fsize = st.st_size;
        char *buf = (char *)malloc(fsize);
        if (buf) {
            size_t read_sz = fread(buf, 1, fsize, fd);
            if (read_sz == fsize) {
                fclose(fd);
                esp_err_t res = httpd_resp_send(req, buf, fsize);
                free(buf);
                return res;
            }
            free(buf);
            fseek(fd, 0, SEEK_SET);
        }
    }

    // Fallback to chunked if needed
    char chunk[1024];
    size_t chunksize;
    while ((chunksize = fread(chunk, 1, sizeof(chunk), fd)) > 0) {
        httpd_resp_send_chunk(req, chunk, chunksize);
    }
    fclose(fd);
    httpd_resp_send_chunk(req, NULL, 0);
    return ESP_OK;
}

// Tray stubs: simple status/command for future module
static esp_err_t tray_command_handler(httpd_req_t *req) {
    char buf[128] = {0};
    int ret = httpd_req_recv(req, buf, sizeof(buf) - 1);
    if (ret > 0) buf[ret] = '\0';
    // Placeholder: no hardware side-effects yet
    const char resp[] = "{\"status\":\"ok\",\"note\":\"tray command stub\"}";
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, resp, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

static esp_err_t tray_status_handler(httpd_req_t *req) {
    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", "Ready");
    cJSON_AddNumberToObject(res, "position", 0);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
}

// Curtain stubs
static esp_err_t curtains_command_handler(httpd_req_t *req) {
    char buf[128] = {0};
    int ret = httpd_req_recv(req, buf, sizeof(buf) - 1);
    if (ret > 0) buf[ret] = '\0';
    const char resp[] = "{\"status\":\"ok\",\"note\":\"curtain command stub\"}";
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, resp, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

static esp_err_t curtains_status_handler(httpd_req_t *req) {
    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", "Ready");
    cJSON_AddNumberToObject(res, "online", 1);
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

static esp_err_t rpc_command_handler(httpd_req_t *req) {
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
}

static esp_err_t rpc_status_handler(httpd_req_t *req) {
    cJSON *res = cJSON_CreateObject();

    int32_t h, f;
    bedDriver->getLiveStatus(h, f);
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
}

void NetworkManager::begin() {
    s_instance = this;
    initSPIFFS();

    wifiProvisioningConfig cfg = {
        .apSsid = "HomeYantric-Setup",
        .onSuccess = onProvisioned
    };
    esp_err_t err = wifiProvisioningStart(&cfg);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Provisioning start failed: %s", esp_err_to_name(err));
    }
}

void NetworkManager::initSPIFFS() {
    esp_vfs_spiffs_conf_t conf = {
        .base_path = "/spiffs",
        .partition_label = "storage",
        .max_files = 5,
        .format_if_mount_failed = true
    };
    if (esp_vfs_spiffs_register(&conf) != ESP_OK) {
        ESP_LOGE(TAG, "SPIFFS Mount Failed");
    } else {
        ESP_LOGI(TAG, "SPIFFS mounted at %s", conf.base_path);
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
        httpd_register_uri_handler(server, &URI_MANIFEST);
        httpd_register_uri_handler(server, &URI_SW);
        httpd_register_uri_handler(server, &URI_BRAND);
        httpd_register_uri_handler(server, &URI_CMD);
        httpd_register_uri_handler(server, &URI_STATUS);
        httpd_register_uri_handler(server, &URI_TRAY_CMD);
        httpd_register_uri_handler(server, &URI_TRAY_STATUS);
        httpd_register_uri_handler(server, &URI_CURTAIN_CMD);
        httpd_register_uri_handler(server, &URI_CURTAIN_STATUS);
        httpd_register_uri_handler(server, &URI_LEGACY_STATUS);
        httpd_register_uri_handler(server, &URI_CLOSE_AP);
        httpd_register_uri_handler(server, &URI_RESET_WIFI);
    }
}

void NetworkManager::startMdns() {
    esp_err_t err = mdns_init();
    if (err != ESP_OK && err != ESP_ERR_INVALID_STATE) {
        ESP_LOGE(TAG, "mDNS init failed: %s", esp_err_to_name(err));
        return;
    }
    mdns_hostname_set(MDNS_HOSTNAME);
    mdns_service_add(NULL, "_http", "_tcp", 80, NULL, 0);
}

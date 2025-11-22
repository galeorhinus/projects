#include "NetworkManager.h"
#include "Config.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "mdns.h"
#include "esp_spiffs.h"
#include "cJSON.h"
#include "esp_sntp.h" 
#include "esp_timer.h"
#include <time.h>
#include <sys/time.h>
#include <string>

static const char *TAG = "NET_MGR";
extern BedControl bed;

// Shared Globals
extern std::string activeCommandLog; // Changed to std::string for IDF compatibility in this file

// Global variable to store when the system started
static time_t boot_epoch = 0;

static void wifi_event_handler(void* arg, esp_event_base_t event_base, int32_t event_id, void* event_data) {
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
    } else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        ESP_LOGI(TAG, "WiFi Disconnected. Retrying...");
        esp_wifi_connect();
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        ip_event_got_ip_t* event = (ip_event_got_ip_t*) event_data;
        ESP_LOGI(TAG, "Connected! IP: " IPSTR, IP2STR(&event->ip_info.ip));
    }
}

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

    char chunk[1024];
    size_t chunksize;
    while ((chunksize = fread(chunk, 1, sizeof(chunk), fd)) > 0) {
        httpd_resp_send_chunk(req, chunk, chunksize);
    }
    fclose(fd);
    httpd_resp_send_chunk(req, NULL, 0);
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
    
    if (!cJSON_IsString(cmdItem)) {
        cJSON_Delete(root);
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Missing cmd");
        return ESP_FAIL;
    }

    std::string cmd = cmdItem->valuestring;
    std::string label = (cJSON_IsString(lblItem)) ? lblItem->valuestring : "";

    long maxWait = 0;
    
    // --- COMMAND LOGIC ---
    
    if (cmd == "STOP") { 
        bed.stop(); 
        activeCommandLog = "IDLE";
    } 
    else if (cmd == "HEAD_UP") { bed.moveHead("UP"); activeCommandLog = "HEAD_UP"; }
    else if (cmd == "HEAD_DOWN") { bed.moveHead("DOWN"); activeCommandLog = "HEAD_DOWN"; }
    else if (cmd == "FOOT_UP") { bed.moveFoot("UP"); activeCommandLog = "FOOT_UP"; }
    else if (cmd == "FOOT_DOWN") { bed.moveFoot("DOWN"); activeCommandLog = "FOOT_DOWN"; }
    
    // Fixed Presets
    else if (cmd == "FLAT") { 
        maxWait = bed.setTarget(0, 0); 
        activeCommandLog = "FLAT"; 
    }
    else if (cmd == "MAX") { 
        maxWait = bed.setTarget(HEAD_MAX_MS, FOOT_MAX_MS); 
        activeCommandLog = "MAX"; 
    }
    
    // Saved Presets
    else if (cmd == "ZERO_G") {
        maxWait = bed.setTarget(bed.getSavedPos("zg_head", 10000), bed.getSavedPos("zg_foot", 40000));
        activeCommandLog = "ZERO_G";
    }
    else if (cmd == "ANTI_SNORE") {
        maxWait = bed.setTarget(bed.getSavedPos("snore_head", 10000), bed.getSavedPos("snore_foot", 0));
        activeCommandLog = "ANTI_SNORE";
    }
    else if (cmd == "LEGS_UP") {
        maxWait = bed.setTarget(bed.getSavedPos("legs_head", 0), bed.getSavedPos("legs_foot", 43000));
        activeCommandLog = "LEGS_UP";
    }
    else if (cmd == "P1") {
        maxWait = bed.setTarget(bed.getSavedPos("p1_head", 0), bed.getSavedPos("p1_foot", 0));
        activeCommandLog = "P1";
    }
    else if (cmd == "P2") {
        maxWait = bed.setTarget(bed.getSavedPos("p2_head", 0), bed.getSavedPos("p2_foot", 0));
        activeCommandLog = "P2";
    }

    // Save Positions (Logic handled by JS sending SET_XX_POS)
    // Note: In IDF version, we save CURRENT position to the slot
    else if (cmd.find("SET_") == 0 && cmd.find("_POS") != std::string::npos) {
        // Extract "p1" from "SET_P1_POS"
        std::string slot = cmd.substr(4, cmd.find("_POS") - 4);
        // Lowercase conversion manually
        for(char &c : slot) c = tolower(c);
        
        int32_t h, f;
        bed.getLiveStatus(h, f); // Get current position
        bed.setSavedPos((slot + "_head").c_str(), h);
        bed.setSavedPos((slot + "_foot").c_str(), f);
    }
    // Save Labels
    else if (cmd.find("SET_") == 0 && cmd.find("_LABEL") != std::string::npos) {
         // Not implemented in C++ NVS currently (strings are hard in NVS C-API), 
         // but acknowledged to prevent error.
         // Logic usually handled by JS storing mapping or similar.
    }

    cJSON_Delete(root);

    // --- BUILD RESPONSE ---
    cJSON *res = cJSON_CreateObject();
    int32_t h, f;
    bed.getLiveStatus(h, f);

    // Boot Time
    time_t now;
    time(&now);
    double bTime = (boot_epoch > 0) ? (double)boot_epoch : 1.0; 
    cJSON_AddNumberToObject(res, "bootTime", bTime);

    cJSON_AddNumberToObject(res, "headPos", h / 1000.0);
    cJSON_AddNumberToObject(res, "footPos", f / 1000.0);
    cJSON_AddNumberToObject(res, "maxWait", maxWait);
    
    // If it was a SET command, echo back info if needed
    // (Simplified for brevity)

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
    bed.getLiveStatus(h, f);

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

    const char *slots[] = {"zg", "snore", "legs", "p1", "p2"};
    for (int i = 0; i < 5; ++i) {
        std::string base = slots[i];
        cJSON_AddNumberToObject(res, (base + "_head").c_str(), bed.getSavedPos((base + "_head").c_str(), 0));
        cJSON_AddNumberToObject(res, (base + "_foot").c_str(), bed.getSavedPos((base + "_foot").c_str(), 0));
    }

    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);

    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
}

void NetworkManager::begin() {
    initSPIFFS();
    initWiFi();
    initmDNS();
    startWebServer();
}

void NetworkManager::initSPIFFS() {
    esp_vfs_spiffs_conf_t conf = {
        .base_path = "/spiffs",
        .partition_label = "storage",
        .max_files = 5,
        .format_if_mount_failed = true
    };
    esp_vfs_spiffs_register(&conf);
}

void NetworkManager::initWiFi() {
    esp_netif_init();
    esp_event_loop_create_default();
    esp_netif_create_default_wifi_sta();
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);

    esp_event_handler_instance_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &wifi_event_handler, NULL, NULL);
    esp_event_handler_instance_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &wifi_event_handler, NULL, NULL);

    wifi_config_t wifi_config = {};
    strcpy((char*)wifi_config.sta.ssid, WIFI_SSID);
    strcpy((char*)wifi_config.sta.password, WIFI_PASS);
    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_set_config(WIFI_IF_STA, &wifi_config);
    esp_wifi_start();

    esp_sntp_setoperatingmode(SNTP_OPMODE_POLL);
    esp_sntp_setservername(0, "pool.ntp.org");
    esp_sntp_init();
}

void NetworkManager::initmDNS() {
    mdns_init();
    mdns_hostname_set(MDNS_HOSTNAME);
    mdns_service_add(NULL, "_http", "_tcp", 80, NULL, 0);
}

void NetworkManager::startWebServer() {
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    config.uri_match_fn = httpd_uri_match_wildcard;

    if (httpd_start(&server, &config) == ESP_OK) {
        // Static Files
        httpd_uri_t idx = { .uri = "/", .method = HTTP_GET, .handler = file_server_handler, .user_ctx = (void*)"/spiffs/index.html" };
        httpd_uri_t index = { .uri = "/index.html", .method = HTTP_GET, .handler = file_server_handler, .user_ctx = (void*)"/spiffs/index.html" };
        httpd_uri_t style = { .uri = "/style.css", .method = HTTP_GET, .handler = file_server_handler, .user_ctx = (void*)"/spiffs/style.css" };
        httpd_uri_t js = { .uri = "/app.js", .method = HTTP_GET, .handler = file_server_handler, .user_ctx = (void*)"/spiffs/app.js" };
        httpd_uri_t icon = { .uri = "/favicon.png", .method = HTTP_GET, .handler = file_server_handler, .user_ctx = (void*)"/spiffs/favicon.png" };

        // API
        httpd_uri_t cmd = { .uri = "/rpc/Bed.Command", .method = HTTP_POST, .handler = rpc_command_handler, .user_ctx = NULL };
        httpd_uri_t status = { .uri = "/rpc/Bed.Status", .method = HTTP_POST, .handler = rpc_status_handler, .user_ctx = NULL };

        httpd_register_uri_handler(server, &idx);
        httpd_register_uri_handler(server, &index);
        httpd_register_uri_handler(server, &style);
        httpd_register_uri_handler(server, &js);
        httpd_register_uri_handler(server, &icon);
        httpd_register_uri_handler(server, &cmd);
        httpd_register_uri_handler(server, &status);
    }
}
#include "Command.h"
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
#include <cstring>
#include <algorithm> // Needed for std::transform
#include <cctype>

static const char *TAG = "NET_MGR";
extern BedControl bed;

static QueueHandle_t s_cmd_queue = NULL;
// Shared Globals
extern std::string activeCommandLog; 
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
    
    Command command = {};
    strlcpy(command.cmd, cmd.c_str(), sizeof(command.cmd));
    strlcpy(command.label, label.c_str(), sizeof(command.label));
    command.sync_sem = NULL;

    // If this is a SET command, create a semaphore to wait for completion
    if (cmd.rfind("SET_", 0) == 0) {
        command.sync_sem = xSemaphoreCreateBinary();
        if (command.sync_sem == NULL) {
            ESP_LOGE(TAG, "Failed to create sync semaphore");
            httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Semaphore creation failed");
            cJSON_Delete(root);
            return ESP_FAIL;
        }
    }


    if (xQueueSend(s_cmd_queue, &command, (TickType_t)0) != pdPASS) {
        ESP_LOGE(TAG, "Failed to post command to queue");
        httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Failed to process command");
        cJSON_Delete(root);
        return ESP_FAIL;
    }

    cJSON_Delete(root);

    // Wait for the command to be processed if it was a SET command
    // Also wait for preset commands to complete so the UI gets the final position.
    bool should_wait = (command.sync_sem != NULL) || 
                       (cmd == "FLAT" || cmd == "MAX" || cmd == "ZERO_G" || 
                        cmd == "ANTI_SNORE" || cmd == "LEGS_UP" || 
                        cmd == "P1" || cmd == "P2");

    if (command.sync_sem != NULL) {
        if (xSemaphoreTake(command.sync_sem, pdMS_TO_TICKS(2000)) == pdFALSE) {
            ESP_LOGE(TAG, "Timeout waiting for SET command to complete");
        }
        vSemaphoreDelete(command.sync_sem);
    }

    if (should_wait) {
        // Give time for the command_task to process and for presets to finish moving.
        vTaskDelay(pdMS_TO_TICKS(250));
    }

    // Identify if this was a save/reset operation so the response can tell the UI which slot to refresh
    std::string slotSignalKey;
    std::string slotValue;
    bool isSetLabelCommand = false;
    if (cmd.rfind("SET_", 0) == 0 || cmd.rfind("RESET_", 0) == 0) {
        size_t endPos = std::string::npos;
        if (cmd.find("_POS") != std::string::npos) endPos = cmd.find("_POS");
        else if (cmd.find("_LABEL") != std::string::npos) endPos = cmd.find("_LABEL");

        if (endPos != std::string::npos) {
            slotValue = cmd.substr(4, endPos - 4);
            std::transform(slotValue.begin(), slotValue.end(), slotValue.begin(), [](unsigned char c){ return std::tolower(c); });

            if (cmd.rfind("RESET_", 0) == 0) {
                slotSignalKey = "reset";
            } else if (cmd.find("_POS") != std::string::npos) {
                slotSignalKey = "saved_pos";
            } else if (cmd.find("_LABEL") != std::string::npos) {
                slotSignalKey = "saved_label";
                isSetLabelCommand = true;
            }
        }
    }

    // If a label save timed out, poll NVS briefly so the response carries the updated text
    if (isSetLabelCommand && !slotValue.empty()) {
        for (int i = 0; i < 10; ++i) { // up to ~500ms
            std::string current = bed.getSavedLabel((slotValue + "_label").c_str(), "");
            if (current == label) break;
            vTaskDelay(pdMS_TO_TICKS(50));
        }
    }

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
    cJSON_AddNumberToObject(res, "maxWait", 0); // This can be updated by the command handler if needed

    // Include current preset positions and labels so UI updates immediately after a SET_* command
    const char *slots[] = {"zg", "snore", "legs", "p1", "p2"};
    for (int i = 0; i < 5; ++i) {
        std::string base = slots[i];
        cJSON_AddNumberToObject(res, (base + "_head").c_str(), bed.getSavedPos((base + "_head").c_str(), 0));
        cJSON_AddNumberToObject(res, (base + "_foot").c_str(), bed.getSavedPos((base + "_foot").c_str(), 0));
        std::string lbl = bed.getSavedLabel((base + "_label").c_str(), "Preset");
        cJSON_AddStringToObject(res, (base + "_label").c_str(), lbl.c_str());
    }
    if (!slotSignalKey.empty() && !slotValue.empty()) {
        cJSON_AddStringToObject(res, slotSignalKey.c_str(), slotValue.c_str());
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
        
        // Fetch Label from NVS
        std::string lbl = bed.getSavedLabel((base + "_label").c_str(), "Preset");
        cJSON_AddStringToObject(res, (base + "_label").c_str(), lbl.c_str());
    }

    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);

    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
}

void NetworkManager::begin(QueueHandle_t cmd_queue) {
    s_cmd_queue = cmd_queue;
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
    if (esp_vfs_spiffs_register(&conf) != ESP_OK) {
        ESP_LOGE(TAG, "SPIFFS Mount Failed");
    }
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

#include "NetworkManager.h"
#include "Config.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "mdns.h"
#include "esp_spiffs.h"
#include "cJSON.h"

static const char *TAG = "NET_MGR";
extern BedControl bed;

// --- WIFI EVENTS ---
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

// --- HTTP HELPERS ---
static esp_err_t file_server_handler(httpd_req_t *req) {
    const char *filepath = (const char *)req->user_ctx;

    // Set Content-Type based on file extension
    const char *ext = strrchr(filepath, '.');
    if (ext != NULL) {
        if (strcmp(ext, ".css") == 0) {
            httpd_resp_set_type(req, "text/css");
        } else if (strcmp(ext, ".js") == 0) {
            httpd_resp_set_type(req, "application/javascript");
        } else if (strcmp(ext, ".png") == 0) {
            httpd_resp_set_type(req, "image/png");
        } else if (strcmp(ext, ".ico") == 0) {
            httpd_resp_set_type(req, "image/x-icon");
        } else if (strcmp(ext, ".html") == 0 || strcmp(ext, ".htm") == 0) {
            httpd_resp_set_type(req, "text/html");
        } else {
            // reasonable default
            httpd_resp_set_type(req, "text/plain");
        }
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
        ESP_LOGE(TAG, "Failed to read HTTP body");
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "No body");
        return ESP_FAIL;
    }
    buf[ret] = '\0';

    cJSON *root = cJSON_Parse(buf);
    if (root == nullptr) {
        ESP_LOGE(TAG, "JSON parse error");
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad JSON");
        return ESP_FAIL;
    }

    cJSON *cmdItem = cJSON_GetObjectItem(root, "cmd");
    if (!cJSON_IsString(cmdItem) || (cmdItem->valuestring == nullptr)) {
        ESP_LOGE(TAG, "JSON has no 'cmd' string");
        cJSON_Delete(root);
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Missing cmd");
        return ESP_FAIL;
    }

    std::string cmd = cmdItem->valuestring;

    long maxWait = 0;
    if (cmd == "STOP") {
        bed.stop();
    } else if (cmd == "HEAD_UP") {
        bed.moveHead("UP");
    } else if (cmd == "HEAD_DOWN") {
        bed.moveHead("DOWN");
    } else if (cmd == "FOOT_UP") {
        bed.moveFoot("UP");
    } else if (cmd == "FOOT_DOWN") {
        bed.moveFoot("DOWN");
    } else if (cmd == "ZERO_G") {
        maxWait = bed.setTarget(
            bed.getSavedPos("zg_head", 10000),
            bed.getSavedPos("zg_foot", 40000)
        );
    }
    // ... Add other presets here ...

    cJSON_Delete(root);  // done with request JSON

    cJSON *res = cJSON_CreateObject();

    int32_t h, f;
    bed.getLiveStatus(h, f);

    double headVal = h / 1000.0;
    double footVal = f / 1000.0;

    cJSON_AddNumberToObject(res, "headPos", headVal);
    cJSON_AddNumberToObject(res, "footPos", footVal);
    cJSON_AddNumberToObject(res, "maxWait", maxWait);

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

    double headVal = h / 1000.0;
    double footVal = f / 1000.0;

    cJSON_AddNumberToObject(res, "headPos", headVal);
    cJSON_AddNumberToObject(res, "footPos", footVal);
    cJSON_AddNumberToObject(res, "uptime",
                            xTaskGetTickCount() * portTICK_PERIOD_MS / 1000);

    const char *slots[] = {"zg", "snore", "legs", "p1", "p2"};
    for (int i = 0; i < 5; ++i) {
        const char *base = slots[i];

        char keyHead[32];
        char keyFoot[32];

        snprintf(keyHead, sizeof(keyHead), "%s_head", base);
        snprintf(keyFoot, sizeof(keyFoot), "%s_foot", base);

        int32_t savedHead = bed.getSavedPos(keyHead, 0);
        int32_t savedFoot = bed.getSavedPos(keyFoot, 0);

        cJSON_AddNumberToObject(res, keyHead, savedHead);
        cJSON_AddNumberToObject(res, keyFoot, savedFoot);
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
        .base_path              = "/spiffs",
        .partition_label        = "storage",   // <--- important
        .max_files              = 5,
        .format_if_mount_failed = true
    };

    esp_err_t ret = esp_vfs_spiffs_register(&conf);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to mount SPIFFS: %s", esp_err_to_name(ret));
    } else {
        size_t total = 0, used = 0;
        esp_spiffs_info("storage", &total, &used);
        ESP_LOGI(TAG, "SPIFFS mounted, total=%d, used=%d", (int)total, (int)used);
    }
}

void NetworkManager::initWiFi() {
    esp_netif_init();
    esp_event_loop_create_default();
    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);

    esp_event_handler_instance_t instance_any_id;
    esp_event_handler_instance_t instance_got_ip;
    esp_event_handler_instance_register(WIFI_EVENT, ESP_EVENT_ANY_ID,
                                        &wifi_event_handler, NULL, &instance_any_id);
    esp_event_handler_instance_register(IP_EVENT, IP_EVENT_STA_GOT_IP,
                                        &wifi_event_handler, NULL, &instance_got_ip);

    wifi_config_t wifi_config = {};
    strcpy((char*)wifi_config.sta.ssid, WIFI_SSID);
    strcpy((char*)wifi_config.sta.password, WIFI_PASS);

    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_set_config(WIFI_IF_STA, &wifi_config);
    esp_wifi_start();
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
        httpd_uri_t idx   = { .uri = "/",          .method = HTTP_GET, .handler = file_server_handler, .user_ctx = (void*)"/spiffs/index.html" };
        httpd_uri_t index = { .uri = "/index.html", .method = HTTP_GET, .handler = file_server_handler, .user_ctx = (void*)"/spiffs/index.html" };
        httpd_uri_t style = { .uri = "/style.css", .method = HTTP_GET, .handler = file_server_handler, .user_ctx = (void*)"/spiffs/style.css" };
        httpd_uri_t js    = { .uri = "/app.js",    .method = HTTP_GET, .handler = file_server_handler, .user_ctx = (void*)"/spiffs/app.js" };
        httpd_uri_t icon  = { .uri = "/favicon.png", .method = HTTP_GET, .handler = file_server_handler, .user_ctx = (void*)"/spiffs/favicon.png" };

        httpd_uri_t cmd    = { .uri = "/rpc/Bed.Command", .method = HTTP_POST, .handler = rpc_command_handler, .user_ctx = NULL };
        httpd_uri_t status = { .uri = "/rpc/Bed.Status",  .method = HTTP_POST, .handler = rpc_status_handler,  .user_ctx = NULL };

        httpd_register_uri_handler(server, &idx);
        httpd_register_uri_handler(server, &index);
        httpd_register_uri_handler(server, &style);
        httpd_register_uri_handler(server, &js);
        httpd_register_uri_handler(server, &icon);
        httpd_register_uri_handler(server, &cmd);
        httpd_register_uri_handler(server, &status);
    }
}

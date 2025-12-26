#include "NetworkManager.h"
#include "BoardConfig.h"
#include "LightConfig.h"
#include "esp_log.h"
#include "esp_ota_ops.h"
#include "cJSON.h"
#include "esp_sntp.h" 
#include "esp_timer.h"
#include "esp_netif.h"
#include "mdns.h"
#include "esp_wifi.h"
#include "esp_system.h"
#include "nvs.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#if APP_ROLE_BED
#include "BedDriver.h"
#endif
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

extern void status_led_override(uint8_t r, uint8_t g, uint8_t b, uint32_t duration_ms);

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
static uint8_t s_light_brightness = 0;

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
static esp_err_t peer_discover_handler(httpd_req_t *req);
static esp_err_t peer_lookup_handler(httpd_req_t *req);
static esp_err_t system_role_handler(httpd_req_t *req);
static esp_err_t system_labels_handler(httpd_req_t *req);
static esp_err_t light_brightness_handler(httpd_req_t *req);
static esp_err_t options_cors_handler(httpd_req_t *req);

// Simple CORS helper
static inline void add_cors(httpd_req_t *req) {
    httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
    httpd_resp_set_hdr(req, "Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    httpd_resp_set_hdr(req, "Access-Control-Allow-Headers", "Content-Type");
    httpd_resp_set_hdr(req, "Access-Control-Max-Age", "600");
}

static const char *kLabelNamespace = "labels";
static const char *kLabelKeyDeviceName = "device_name";
static const char *kLabelKeyRoom = "room";
static const size_t kLabelMaxLen = 32;
static const char *kLightNamespace = "light";
static const char *kLightKeyBrightness = "brightness";
static const char *kLightKeyLastOn = "last_on";
static const char *kLightKeyState = "state";
static const uint8_t kLightDefaultBrightness = 0;

static std::string label_default_device_name(const std::string &host) {
    std::string fallback = CONFIG_APP_LABEL_DEVICE_NAME;
    if (fallback.empty()) {
        return host;
    }
    return fallback;
}

static std::string build_roles_string() {
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
    return roles;
}

static std::string build_type_string() {
    std::string type = "multi";
#if APP_ROLE_BED && !APP_ROLE_LIGHT && !APP_ROLE_TRAY
    type = "bed";
#elif APP_ROLE_LIGHT && !APP_ROLE_BED && !APP_ROLE_TRAY
    type = "light";
#elif APP_ROLE_TRAY && !APP_ROLE_BED && !APP_ROLE_LIGHT
    type = "tray";
#endif
    return type;
}

static std::string label_from_nvs(const char *key, const std::string &fallback) {
    nvs_handle_t handle;
    esp_err_t err = nvs_open(kLabelNamespace, NVS_READONLY, &handle);
    if (err != ESP_OK) {
        return fallback;
    }
    size_t required_size = 0;
    err = nvs_get_str(handle, key, nullptr, &required_size);
    if (err != ESP_OK || required_size == 0 || required_size > (kLabelMaxLen + 1)) {
        nvs_close(handle);
        return fallback;
    }
    std::string value(required_size, '\0');
    err = nvs_get_str(handle, key, value.data(), &required_size);
    nvs_close(handle);
    if (err != ESP_OK) {
        return fallback;
    }
    if (!value.empty() && value.back() == '\0') {
        value.pop_back();
    }
    if (value.empty()) {
        return fallback;
    }
    return value;
}

static esp_err_t label_write_to_nvs(const char *key, const char *value) {
    nvs_handle_t handle;
    esp_err_t err = nvs_open(kLabelNamespace, NVS_READWRITE, &handle);
    if (err != ESP_OK) {
        return err;
    }
    if (!value || value[0] == '\0') {
        err = nvs_erase_key(handle, key);
        if (err == ESP_ERR_NVS_NOT_FOUND) {
            err = ESP_OK;
        }
    } else {
        err = nvs_set_str(handle, key, value);
    }
    if (err == ESP_OK) {
        err = nvs_commit(handle);
    }
    nvs_close(handle);
    return err;
}

static void load_labels(const std::string &host, std::string *device_name, std::string *room) {
    if (!device_name || !room) {
        return;
    }
    *device_name = label_from_nvs(kLabelKeyDeviceName, label_default_device_name(host));
    *room = label_from_nvs(kLabelKeyRoom, CONFIG_APP_LABEL_ROOM);
}

static uint8_t light_brightness_from_nvs(void) {
    nvs_handle_t handle;
    esp_err_t err = nvs_open(kLightNamespace, NVS_READONLY, &handle);
    if (err != ESP_OK) {
        return kLightDefaultBrightness;
    }
    uint8_t value = kLightDefaultBrightness;
    err = nvs_get_u8(handle, kLightKeyBrightness, &value);
    nvs_close(handle);
    if (err != ESP_OK) {
        return kLightDefaultBrightness;
    }
    if (value > 100) value = 100;
    return value;
}

static bool light_state_from_nvs(void) {
    nvs_handle_t handle;
    esp_err_t err = nvs_open(kLightNamespace, NVS_READONLY, &handle);
    if (err != ESP_OK) {
        return false;
    }
    uint8_t value = 0;
    err = nvs_get_u8(handle, kLightKeyState, &value);
    nvs_close(handle);
    if (err != ESP_OK) {
        return false;
    }
    return value != 0;
}

static bool light_last_on_from_nvs(uint8_t *out_value) {
    if (!out_value) return false;
    nvs_handle_t handle;
    esp_err_t err = nvs_open(kLightNamespace, NVS_READONLY, &handle);
    if (err != ESP_OK) {
        return false;
    }
    uint8_t value = 0;
    err = nvs_get_u8(handle, kLightKeyLastOn, &value);
    nvs_close(handle);
    if (err != ESP_OK) {
        return false;
    }
    if (value > 100) value = 100;
    if (value == 0) return false;
    *out_value = value;
    return true;
}

static void light_brightness_to_nvs(uint8_t value) {
    if (value > 100) value = 100;
    if (value == 0) {
        return;
    }
    nvs_handle_t handle;
    esp_err_t err = nvs_open(kLightNamespace, NVS_READWRITE, &handle);
    if (err != ESP_OK) {
        ESP_LOGW(TAG, "NVS open failed for light brightness: %s", esp_err_to_name(err));
        return;
    }
    err = nvs_set_u8(handle, kLightKeyBrightness, value);
    if (err == ESP_OK) {
        nvs_commit(handle);
    }
    nvs_close(handle);
}

static void light_last_on_to_nvs(uint8_t value) {
    if (value > 100) value = 100;
    if (value == 0) return;
    nvs_handle_t handle;
    esp_err_t err = nvs_open(kLightNamespace, NVS_READWRITE, &handle);
    if (err != ESP_OK) {
        ESP_LOGW(TAG, "NVS open failed for light last-on: %s", esp_err_to_name(err));
        return;
    }
    err = nvs_set_u8(handle, kLightKeyLastOn, value);
    if (err == ESP_OK) {
        nvs_commit(handle);
    }
    nvs_close(handle);
}

static void light_state_to_nvs(bool on) {
    nvs_handle_t handle;
    esp_err_t err = nvs_open(kLightNamespace, NVS_READWRITE, &handle);
    if (err != ESP_OK) {
        ESP_LOGW(TAG, "NVS open failed for light state: %s", esp_err_to_name(err));
        return;
    }
    uint8_t value = on ? 1 : 0;
    err = nvs_set_u8(handle, kLightKeyState, value);
    if (err == ESP_OK) {
        nvs_commit(handle);
    }
    nvs_close(handle);
}

static void light_set_brightness(uint8_t percent, bool persist) {
    if (!s_light_initialized) return;
    if (percent > 100) percent = 100;
    s_light.setBrightness(percent);
    s_light_brightness = s_light.getBrightness();
    s_light_state = s_light.getState();
    if (persist) {
        light_state_to_nvs(s_light_state);
        light_brightness_to_nvs(s_light_brightness);
        if (s_light_brightness > 0) {
            light_last_on_to_nvs(s_light_brightness);
        }
    }
}

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
static const httpd_uri_t URI_LIGHT_BRIGHTNESS_GET = { .uri = "/rpc/Light.Brightness", .method = HTTP_GET, .handler = light_brightness_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_BRIGHTNESS_SET = { .uri = "/rpc/Light.Brightness", .method = HTTP_POST, .handler = light_brightness_handler, .user_ctx = NULL };
static const httpd_uri_t URI_BED_STATUS_DISABLED = { .uri = "/rpc/Bed.Status", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"bed" };
static const httpd_uri_t URI_BED_CMD_DISABLED = { .uri = "/rpc/Bed.Command", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"bed" };
static const httpd_uri_t URI_LIGHT_STATUS_DISABLED = { .uri = "/rpc/Light.Status", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_CMD_DISABLED = { .uri = "/rpc/Light.Command", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_BRIGHTNESS_DISABLED = { .uri = "/rpc/Light.Brightness", .method = HTTP_GET, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_BRIGHTNESS_DISABLED_POST = { .uri = "/rpc/Light.Brightness", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_TRAY_STATUS_DISABLED = { .uri = "/rpc/Tray.Status", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"tray" };
static const httpd_uri_t URI_CURTAIN_STATUS_DISABLED = { .uri = "/rpc/Curtains.Status", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"curtains" };
static const httpd_uri_t URI_LEGACY_STATUS = { .uri = "/status", .method = HTTP_GET, .handler = legacy_status_handler, .user_ctx = NULL };
static const httpd_uri_t URI_CLOSE_AP = { .uri = "/close_ap", .method = HTTP_POST, .handler = close_ap_handler, .user_ctx = NULL };
static const httpd_uri_t URI_RESET_WIFI = { .uri = "/reset_wifi", .method = HTTP_POST, .handler = reset_wifi_handler, .user_ctx = NULL };
static const httpd_uri_t URI_OTA = { .uri = "/rpc/Bed.OTA", .method = HTTP_POST, .handler = ota_upload_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LOG = { .uri = "/rpc/Bed.Log", .method = HTTP_POST, .handler = log_handler, .user_ctx = NULL };
static const httpd_uri_t URI_PEER_DISCOVER = { .uri = "/rpc/Peer.Discover", .method = HTTP_GET, .handler = peer_discover_handler, .user_ctx = NULL };
static const httpd_uri_t URI_PEER_LOOKUP = { .uri = "/rpc/Peer.Lookup", .method = HTTP_GET, .handler = peer_lookup_handler, .user_ctx = NULL };
static const httpd_uri_t URI_SYSTEM_ROLE = { .uri = "/rpc/System.Role", .method = HTTP_GET, .handler = system_role_handler, .user_ctx = NULL };
static const httpd_uri_t URI_SYSTEM_LABELS_GET = { .uri = "/rpc/System.Labels", .method = HTTP_GET, .handler = system_labels_handler, .user_ctx = NULL };
static const httpd_uri_t URI_SYSTEM_LABELS_SET = { .uri = "/rpc/System.Labels", .method = HTTP_POST, .handler = system_labels_handler, .user_ctx = NULL };
static const httpd_uri_t URI_OPTIONS_ALL = { .uri = "/*", .method = HTTP_OPTIONS, .handler = options_cors_handler, .user_ctx = NULL };
static const httpd_uri_t URI_OPTIONS_BED_CMD = { .uri = "/rpc/Bed.Command", .method = HTTP_OPTIONS, .handler = options_cors_handler, .user_ctx = NULL };
static const httpd_uri_t URI_OPTIONS_BED_STATUS = { .uri = "/rpc/Bed.Status", .method = HTTP_OPTIONS, .handler = options_cors_handler, .user_ctx = NULL };
static const httpd_uri_t URI_OPTIONS_LIGHT_CMD = { .uri = "/rpc/Light.Command", .method = HTTP_OPTIONS, .handler = options_cors_handler, .user_ctx = NULL };
static const httpd_uri_t URI_OPTIONS_LIGHT_STATUS = { .uri = "/rpc/Light.Status", .method = HTTP_OPTIONS, .handler = options_cors_handler, .user_ctx = NULL };

static void onProvisioned(const char* sta_ip) {
    ESP_LOGI(TAG, "Provisioning complete. STA IP: %s", sta_ip ? sta_ip : "unknown");
    if (s_instance) {
        ESP_LOGI(TAG, "Client connected via STA, starting main services");
#if APP_ROLE_LIGHT
        uint8_t last_on = 0;
        bool has_last_on = light_last_on_from_nvs(&last_on);
        uint8_t saved_brightness = light_brightness_from_nvs();
        bool saved_state = light_state_from_nvs();
        ESP_LOGI(TAG, "Light NVS (online) last_on=%s %u brightness=%u", has_last_on ? "yes" : "no", last_on, saved_brightness);
        if (s_light_initialized) {
            uint8_t restore = has_last_on ? last_on : saved_brightness;
            if (saved_state && restore > 0) {
                light_set_brightness(restore, false);
            }
        }
#endif
        s_instance->startSntp();
        s_instance->startMdns();
        s_instance->startWebServer();
    }
}

// Forward declarations for HTTP handlers
static esp_err_t file_server_handler(httpd_req_t *req) {
    add_cors(req);
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
    uint8_t prev_brightness = s_light.getBrightness();
    if (on && prev_brightness == 0) {
        uint8_t last_on = 0;
        if (light_last_on_from_nvs(&last_on)) {
            s_light.setLastNonzeroBrightness(last_on);
        }
    }
    s_light.setState(on);
    s_light_state = s_light.getState();
    s_light_brightness = s_light.getBrightness();
    light_state_to_nvs(s_light_state);
    light_brightness_to_nvs(s_light_brightness);
    if (s_light_state && s_light_brightness > 0) {
        light_last_on_to_nvs(s_light_brightness);
    } else if (!s_light_state && prev_brightness > 0) {
        light_last_on_to_nvs(prev_brightness);
        s_light.setLastNonzeroBrightness(prev_brightness);
    }
}

static esp_err_t light_command_handler(httpd_req_t *req) {
    add_cors(req);
#if !APP_ROLE_LIGHT
    return role_disabled_handler(req);
#else
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
        if (s == "ON") {
            light_apply_state(true);
            status_led_override(0, 140, 0, 180); // green
        } else if (s == "OFF") {
            light_apply_state(false);
            status_led_override(140, 0, 0, 180); // red
        } else if (s == "TOGGLE") {
            light_apply_state(!s_light_state);
            if (s_light_state) {
                status_led_override(0, 140, 0, 180);
            } else {
                status_led_override(140, 0, 0, 180);
            }
        }
    }
    cJSON_Delete(root);

    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", "ok");
    cJSON_AddStringToObject(res, "state", s_light_state ? "on" : "off");
    cJSON_AddNumberToObject(res, "gpio", LIGHT_GPIO);
    cJSON_AddNumberToObject(res, "brightness", s_light_brightness);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
#endif
}

static esp_err_t light_status_handler(httpd_req_t *req) {
    add_cors(req);
#if !APP_ROLE_LIGHT
    return role_disabled_handler(req);
#else
    static bool s_last_status_state = false;
    static uint8_t s_last_status_brightness = 0;
    if (s_last_status_state != s_light_state || s_last_status_brightness != s_light_brightness) {
        ESP_LOGI(TAG, "Light.Status state=%s brightness=%u", s_light_state ? "on" : "off", s_light_brightness);
        s_last_status_state = s_light_state;
        s_last_status_brightness = s_light_brightness;
    }
    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", "ok");
    cJSON_AddStringToObject(res, "state", s_light_state ? "on" : "off");
    cJSON_AddNumberToObject(res, "gpio", LIGHT_GPIO);
    cJSON_AddNumberToObject(res, "brightness", s_light_brightness);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
#endif
}

static esp_err_t light_brightness_handler(httpd_req_t *req) {
    add_cors(req);
#if !APP_ROLE_LIGHT
    return role_disabled_handler(req);
#else
    if (req->method == HTTP_POST) {
        char buf[128] = {0};
        int ret = httpd_req_recv(req, buf, sizeof(buf) - 1);
        if (ret > 0) buf[ret] = '\0';
        cJSON *root = cJSON_Parse(buf);
        if (!root) {
            httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad JSON");
            return ESP_FAIL;
        }
        cJSON *val = cJSON_GetObjectItem(root, "brightness");
        if (cJSON_IsNumber(val)) {
            int level = val->valueint;
            if (level < 0) level = 0;
            if (level > 100) level = 100;
            uint8_t prev = s_light_brightness;
            light_set_brightness((uint8_t)level, true);
            if (s_light_brightness > prev) {
                status_led_override(150, 120, 0, 140); // yellow (warmer)
            } else if (s_light_brightness < prev) {
                status_led_override(0, 120, 140, 140); // cyan (cooler)
            }
        }
        cJSON_Delete(root);
    }

    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", "ok");
    cJSON_AddStringToObject(res, "state", s_light_state ? "on" : "off");
    cJSON_AddNumberToObject(res, "brightness", s_light_brightness);
    cJSON_AddNumberToObject(res, "gpio", LIGHT_GPIO);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
#endif
}

// Legacy status endpoint (used by provisioning captive portal); respond with ok to avoid 404 spam
static esp_err_t legacy_status_handler(httpd_req_t *req) {
    add_cors(req);
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
    add_cors(req);
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
    add_cors(req);
    ESP_LOGI(TAG, "Received /close_ap request");
    wifiProvisioningCloseAp();
    const char resp[] = "{\"status\":\"ok\"}";
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, resp, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

// Reset Wi-Fi credentials and restart
static esp_err_t reset_wifi_handler(httpd_req_t *req) {
    add_cors(req);
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
    add_cors(req);
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
    add_cors(req);
    httpd_resp_send_err(req, HTTPD_501_METHOD_NOT_IMPLEMENTED, "Bed role not enabled");
    return ESP_OK;
#else
    add_cors(req);
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
    add_cors(req);
    httpd_resp_send_err(req, HTTPD_501_METHOD_NOT_IMPLEMENTED, "Bed role not enabled");
    return ESP_OK;
#else
    add_cors(req);
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
    add_cors(req);
    const char* name = (const char*)req->user_ctx;
    const char* role = name ? name : "disabled";
    httpd_resp_set_type(req, "application/json");
    char resp[64];
    int len = snprintf(resp, sizeof(resp), "{\"status\":\"disabled\",\"role\":\"%s\"}", role);
    httpd_resp_send(req, resp, len);
    return ESP_OK;
}

// Peer discovery: report host/ip/roles/fw for other nodes on the LAN
static esp_err_t peer_discover_handler(httpd_req_t *req) {
    add_cors(req);
    char ip_str[16] = "0.0.0.0";
    esp_netif_t *netif = esp_netif_get_handle_from_ifkey("WIFI_STA_DEF");
    esp_netif_ip_info_t ip;
    if (netif && esp_netif_get_ip_info(netif, &ip) == ESP_OK) {
        ip4addr_ntoa_r((const ip4_addr_t *)&ip.ip, ip_str, sizeof(ip_str));
    }

    std::string host = wifiProvisioningGetHostname();
    if (host.empty()) host = MDNS_HOSTNAME;
    std::string device_name;
    std::string room;
    load_labels(host, &device_name, &room);

    std::string roles = build_roles_string();
    std::string type = build_type_string();

    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "host", host.c_str());
    cJSON_AddStringToObject(res, "ip", ip_str);
    cJSON_AddStringToObject(res, "type", type.c_str());
    cJSON_AddStringToObject(res, "roles", roles.c_str());
    cJSON_AddStringToObject(res, "device_name", device_name.c_str());
    cJSON_AddStringToObject(res, "room", room.c_str());
    cJSON_AddStringToObject(res, "fw", UI_BUILD_TAG);

    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    ESP_LOGI(TAG, "Peer.Discover served host=%s ip=%s type=%s roles=%s fw=%s",
             host.c_str(), ip_str, type.c_str(), roles.c_str(), UI_BUILD_TAG);

    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
}

// Report local role(s) for the UI
static esp_err_t system_role_handler(httpd_req_t *req) {
    add_cors(req);
    std::string roles = build_roles_string();
    std::string type = build_type_string();

    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "role", type.c_str());
    cJSON_AddStringToObject(res, "roles", roles.c_str());
    cJSON_AddStringToObject(res, "fw", UI_BUILD_TAG);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
}

static esp_err_t system_labels_handler(httpd_req_t *req) {
    add_cors(req);
    std::string host = wifiProvisioningGetHostname();
    if (host.empty()) host = MDNS_HOSTNAME;

    if (req->method == HTTP_POST) {
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
        cJSON *device = cJSON_GetObjectItem(root, "device_name");
        cJSON *room = cJSON_GetObjectItem(root, "room");
        if (cJSON_IsString(device)) {
            size_t len = strlen(device->valuestring);
            if (len > kLabelMaxLen) {
                cJSON_Delete(root);
                httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "device_name too long");
                return ESP_FAIL;
            }
            esp_err_t err = label_write_to_nvs(kLabelKeyDeviceName, device->valuestring);
            if (err != ESP_OK) {
                cJSON_Delete(root);
                httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Failed to save device_name");
                return ESP_FAIL;
            }
        }
        if (cJSON_IsString(room)) {
            size_t len = strlen(room->valuestring);
            if (len > kLabelMaxLen) {
                cJSON_Delete(root);
                httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "room too long");
                return ESP_FAIL;
            }
            esp_err_t err = label_write_to_nvs(kLabelKeyRoom, room->valuestring);
            if (err != ESP_OK) {
                cJSON_Delete(root);
                httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Failed to save room");
                return ESP_FAIL;
            }
        }
        cJSON_Delete(root);
        if (s_instance) {
            s_instance->startMdns();
        }
    }

    std::string device_name;
    std::string room;
    load_labels(host, &device_name, &room);

    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "device_name", device_name.c_str());
    cJSON_AddStringToObject(res, "room", room.c_str());
    cJSON_AddStringToObject(res, "hostname", host.c_str());
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
}

// Backend mDNS browse: return list of peers advertising _homeyantric._tcp
static esp_err_t peer_lookup_handler(httpd_req_t *req) {
    add_cors(req);
    mdns_result_t *results = nullptr;
    std::string self = wifiProvisioningGetHostname();
    if (self.empty()) self = MDNS_HOSTNAME;
    esp_err_t err = mdns_query_ptr("_homeyantric", "_tcp", 2000, 8, &results);
    if (err != ESP_OK && err != ESP_ERR_NOT_FOUND) {
        ESP_LOGW(TAG, "Peer.Lookup mDNS query failed: %s", esp_err_to_name(err));
    }

    cJSON *arr = cJSON_CreateArray();
    int count = 0;
    for (mdns_result_t *r = results; r != nullptr; r = r->next) {
        if (!r->hostname) continue;
        if (self == r->hostname) continue; // skip self
        cJSON *o = cJSON_CreateObject();
        cJSON_AddStringToObject(o, "host", r->hostname);
        char ip_str[16] = "0.0.0.0";
        if (r->addr && r->addr->addr.type == IPADDR_TYPE_V4) {
            ip4addr_ntoa_r((const ip4_addr_t *)&r->addr->addr.u_addr.ip4, ip_str, sizeof(ip_str));
            cJSON_AddStringToObject(o, "ip", ip_str);
        }
        if (r->txt_count > 0 && r->txt) {
            for (size_t i = 0; i < r->txt_count; ++i) {
                if (strcmp(r->txt[i].key, "type") == 0) {
                    cJSON_AddStringToObject(o, "type", r->txt[i].value);
                } else if (strcmp(r->txt[i].key, "roles") == 0) {
                    cJSON_AddStringToObject(o, "roles", r->txt[i].value);
                } else if (strcmp(r->txt[i].key, "fw") == 0) {
                    cJSON_AddStringToObject(o, "fw", r->txt[i].value);
                } else if (strcmp(r->txt[i].key, "room") == 0) {
                    cJSON_AddStringToObject(o, "room", r->txt[i].value);
                } else if (strcmp(r->txt[i].key, "device_name") == 0) {
                    cJSON_AddStringToObject(o, "device_name", r->txt[i].value);
                }
            }
        }
        cJSON_AddNumberToObject(o, "port", r->port);
        cJSON_AddItemToArray(arr, o);
        ++count;
    }
    mdns_query_results_free(results);

    char *jsonStr = cJSON_PrintUnformatted(arr);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    ESP_LOGI(TAG, "Peer.Lookup returned %d peer(s)", count);

    free(jsonStr);
    cJSON_Delete(arr);
    return ESP_OK;
}

// Respond to CORS preflight
static esp_err_t options_cors_handler(httpd_req_t *req) {
    add_cors(req);
    static int64_t s_last_preflight_log_us = 0;
    const int64_t now_us = esp_timer_get_time();
    if (now_us - s_last_preflight_log_us > 5000000) {
        s_last_preflight_log_us = now_us;
        ESP_LOGI(TAG, "CORS preflight %s", req->uri ? req->uri : "(null)");
    }
    httpd_resp_send(req, NULL, 0);
    return ESP_OK;
}

void NetworkManager::begin() {
    s_instance = this;
    ESP_LOGI(TAG, "Build: %s", UI_BUILD_TAG);
    esp_ota_mark_app_valid_cancel_rollback();

    // Initialize light GPIO (default OFF)
#if APP_ROLE_LIGHT
    if (s_light.begin((gpio_num_t)LIGHT_GPIO, true) == ESP_OK) {
        s_light_initialized = true;
        s_light_state = false;
        uint8_t last_on = 0;
        bool has_last_on = light_last_on_from_nvs(&last_on);
        uint8_t saved_brightness = light_brightness_from_nvs();
        bool saved_state = light_state_from_nvs();
        ESP_LOGI(TAG, "Light NVS last_on=%s %u", has_last_on ? "yes" : "no", last_on);
        ESP_LOGI(TAG, "Light NVS brightness=%u", saved_brightness);
        if (has_last_on) {
            s_light.setLastNonzeroBrightness(last_on);
            if (saved_state) {
                s_light_brightness = last_on;
                light_set_brightness(s_light_brightness, false);
            }
        } else {
            s_light_brightness = saved_brightness;
            if (saved_state) {
                light_set_brightness(s_light_brightness, false);
            }
        }
    }
#else
    s_light_initialized = false;
#endif

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
    config.max_uri_handlers = 64; // allow extra endpoints
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
        httpd_register_uri_handler(server, &URI_OPTIONS_BED_CMD);
        httpd_register_uri_handler(server, &URI_OPTIONS_BED_STATUS);
        httpd_register_uri_handler(server, &URI_OPTIONS_LIGHT_CMD);
        httpd_register_uri_handler(server, &URI_OPTIONS_LIGHT_STATUS);
#if APP_ROLE_BED
        httpd_register_uri_handler(server, &URI_CMD);
        httpd_register_uri_handler(server, &URI_STATUS);
#else
        httpd_register_uri_handler(server, &URI_BED_CMD_DISABLED);
        httpd_register_uri_handler(server, &URI_BED_STATUS_DISABLED);
#endif
#if APP_ROLE_LIGHT
#if APP_ROLE_LIGHT
        httpd_register_uri_handler(server, &URI_LIGHT_CMD);
        httpd_register_uri_handler(server, &URI_LIGHT_STATUS);
        httpd_register_uri_handler(server, &URI_LIGHT_BRIGHTNESS_GET);
        httpd_register_uri_handler(server, &URI_LIGHT_BRIGHTNESS_SET);
#else
        httpd_register_uri_handler(server, &URI_LIGHT_CMD_DISABLED);
        httpd_register_uri_handler(server, &URI_LIGHT_STATUS_DISABLED);
        httpd_register_uri_handler(server, &URI_LIGHT_BRIGHTNESS_DISABLED);
        httpd_register_uri_handler(server, &URI_LIGHT_BRIGHTNESS_DISABLED_POST);
#endif
#endif
        // Absorb legacy tray/curtains polls from older UIs
        httpd_register_uri_handler(server, &URI_TRAY_STATUS_DISABLED);
        httpd_register_uri_handler(server, &URI_CURTAIN_STATUS_DISABLED);
        httpd_register_uri_handler(server, &URI_OTA);
        httpd_register_uri_handler(server, &URI_LOG);
        httpd_register_uri_handler(server, &URI_LEGACY_STATUS);
        httpd_register_uri_handler(server, &URI_CLOSE_AP);
        httpd_register_uri_handler(server, &URI_RESET_WIFI);
        httpd_register_uri_handler(server, &URI_PEER_DISCOVER);
        httpd_register_uri_handler(server, &URI_PEER_LOOKUP);
        httpd_register_uri_handler(server, &URI_SYSTEM_ROLE);
        httpd_register_uri_handler(server, &URI_SYSTEM_LABELS_GET);
        httpd_register_uri_handler(server, &URI_SYSTEM_LABELS_SET);
        httpd_register_uri_handler(server, &URI_OPTIONS_ALL);
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
    // Avoid "service already exists" warnings by clearing any prior registrations.
    esp_err_t svc_err = mdns_service_remove("_http", "_tcp");
    if (svc_err == ESP_OK) {
        ESP_LOGI(TAG, "mDNS removed existing _http._tcp service");
    } else if (svc_err != ESP_ERR_NOT_FOUND && svc_err != ESP_ERR_INVALID_STATE) {
        ESP_LOGW(TAG, "mDNS remove _http._tcp returned %s", esp_err_to_name(svc_err));
    }
    svc_err = mdns_service_add(NULL, "_http", "_tcp", 80, NULL, 0);
    if (svc_err != ESP_OK && svc_err != ESP_ERR_INVALID_STATE && svc_err != ESP_ERR_INVALID_ARG) {
        ESP_LOGW(TAG, "mDNS http service add returned %s", esp_err_to_name(svc_err));
    }

    // Advertise custom service with role info
    svc_err = mdns_service_remove("_homeyantric", "_tcp");
    if (svc_err == ESP_OK) {
        ESP_LOGI(TAG, "mDNS removed existing _homeyantric._tcp service");
    } else if (svc_err != ESP_ERR_NOT_FOUND && svc_err != ESP_ERR_INVALID_STATE) {
        ESP_LOGW(TAG, "mDNS remove _homeyantric._tcp returned %s", esp_err_to_name(svc_err));
    }
    svc_err = mdns_service_add(NULL, "_homeyantric", "_tcp", 80, NULL, 0);
    if (svc_err != ESP_OK && svc_err != ESP_ERR_INVALID_STATE && svc_err != ESP_ERR_INVALID_ARG) {
        ESP_LOGW(TAG, "mDNS homeyantric service add returned %s", esp_err_to_name(svc_err));
    }
    std::string roles = build_roles_string();
    std::string type = build_type_string();
    std::string model = "unknown";
#if CONFIG_IDF_TARGET_ESP32
    model = "esp32";
#elif CONFIG_IDF_TARGET_ESP32S3
    model = "esp32s3";
#endif
    std::string device_name;
    std::string room;
    load_labels(host, &device_name, &room);
    mdns_txt_item_t txt[] = {
        { (char *)"type", (char *)type.c_str() },
        { (char *)"roles", (char *)roles.c_str() },
        { (char *)"model", (char *)model.c_str() },
        { (char *)"fw", (char *)UI_BUILD_TAG },
        { (char *)"device_name", (char *)device_name.c_str() },
        { (char *)"room", (char *)room.c_str() }
    };
    mdns_service_txt_set("_homeyantric", "_tcp", txt, sizeof(txt)/sizeof(txt[0]));
    ESP_LOGI(TAG, "mDNS _homeyantric._tcp advertised host=%s type=%s roles=%s model=%s fw=%s",
             host.c_str(), type.c_str(), roles.c_str(), model.c_str(), UI_BUILD_TAG);
}

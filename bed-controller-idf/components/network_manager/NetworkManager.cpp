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
#include "driver/ledc.h"
#include "LightControl.h"
#include <sys/stat.h>
#include <time.h>
#include <sys/time.h>
#include <string>
#include <cstring>
#include <algorithm> // Needed for std::transform
#include <sstream>

extern void status_led_override(uint8_t r, uint8_t g, uint8_t b, uint32_t duration_ms);
extern "C" bool addressable_led_fill_strip(uint8_t r, uint8_t g, uint8_t b, uint16_t count);
extern "C" bool addressable_led_chase(uint8_t r, uint8_t g, uint8_t b, uint16_t count, uint16_t steps, uint16_t delay_ms);
extern "C" bool addressable_led_wipe(uint8_t r, uint8_t g, uint8_t b, uint16_t count, uint16_t delay_ms);
extern "C" bool addressable_led_pulse(uint8_t r, uint8_t g, uint8_t b, uint16_t count, uint16_t steps, uint16_t delay_ms);
extern "C" bool addressable_led_rainbow(uint16_t count, uint16_t steps, uint16_t delay_ms, uint8_t brightness);
extern "C" void addressable_led_set_order(bool grb);

static const char *TAG = "NET_MGR";
#if APP_ROLE_BED
extern BedDriver* bedDriver;
#endif

struct LightWiringPreset {
    const char *type;
    const char *label;
    const char *terminals;
    uint8_t channels;
    const char *ui_mode;
};
struct LightRgbPreset {
    uint8_t r;
    uint8_t g;
    uint8_t b;
    uint8_t brightness;
};

// Shared Globals
extern std::string activeCommandLog; 
static time_t boot_epoch = 0;
static NetworkManager* s_instance = nullptr;
static bool s_light_initialized = false;
static bool s_light_state = false;
static LightControl s_light;
static uint8_t s_light_brightness = 0;
static const LightWiringPreset *s_light_wiring_preset = nullptr;
static bool s_light_wiring_configured = false;
static bool s_light_rgb_initialized = false;
static bool s_peer_log_enabled = false;
static uint8_t s_light_rgb[3] = {0, 0, 0};
static uint16_t s_light_digital_count = 90;
static const ledc_mode_t kLightRgbSpeedMode = LEDC_LOW_SPEED_MODE;
static const ledc_timer_t kLightRgbTimer = LEDC_TIMER_1;
static const ledc_timer_bit_t kLightRgbDutyResolution = LEDC_TIMER_13_BIT;
static const uint32_t kLightRgbFreqHz = 5000;
// Avoid status LED channels (0-2) used in main for light builds.
static const ledc_channel_t kLightRgbChannels[3] = {LEDC_CHANNEL_3, LEDC_CHANNEL_4, LEDC_CHANNEL_5};
static const int kLightRgbPins[3] = {LIGHT_RGB_GPIO_R, LIGHT_RGB_GPIO_G, LIGHT_RGB_GPIO_B};

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
static esp_err_t log_settings_handler(httpd_req_t *req);
static esp_err_t file_server_handler(httpd_req_t *req);
static esp_err_t rpc_command_handler(httpd_req_t *req);
static esp_err_t rpc_status_handler(httpd_req_t *req);
static esp_err_t rpc_events_handler(httpd_req_t *req);
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
static esp_err_t light_wiring_handler(httpd_req_t *req);
static esp_err_t light_rgb_test_handler(httpd_req_t *req);
static esp_err_t light_rgb_handler(httpd_req_t *req);
static esp_err_t light_preset_handler(httpd_req_t *req);
static esp_err_t light_digital_test_handler(httpd_req_t *req);
static esp_err_t light_digital_chase_handler(httpd_req_t *req);
static esp_err_t light_digital_wipe_handler(httpd_req_t *req);
static esp_err_t light_digital_pulse_handler(httpd_req_t *req);
static esp_err_t light_digital_rainbow_handler(httpd_req_t *req);
static esp_err_t options_cors_handler(httpd_req_t *req);
static esp_err_t light_rgb_init();
static void light_rgb_set_channel(int channel, uint8_t percent);
static void light_rgb_apply_outputs();
static void light_rgb_set_base(int channel, uint8_t percent);

// Simple CORS helper
static inline void add_cors(httpd_req_t *req) {
    httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
    httpd_resp_set_hdr(req, "Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    httpd_resp_set_hdr(req, "Access-Control-Allow-Headers",
                       "Content-Type, contenttype, Accept");
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
static const char *kLightKeyPresetPrefix = "preset";
static const int kLightPresetCount = 6;
static const uint8_t kLightDefaultBrightness = 0;
static const char *kLightWiringNamespace = "light_wiring";
static const char *kLightWiringKeyType = "type";
static const char *kLightWiringKeyOrder = "order";
static const char *kLightWiringDefaultType = "2wire-dim";

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

static std::string light_preset_key(int slot) {
    char key[16];
    snprintf(key, sizeof(key), "%s%d", kLightKeyPresetPrefix, slot);
    return std::string(key);
}

static bool light_preset_from_nvs(int slot, LightRgbPreset *out) {
    if (!out || slot < 1 || slot > kLightPresetCount) return false;
    nvs_handle_t handle;
    esp_err_t err = nvs_open(kLightNamespace, NVS_READONLY, &handle);
    if (err != ESP_OK) {
        return false;
    }
    size_t size = sizeof(LightRgbPreset);
    std::string key = light_preset_key(slot);
    err = nvs_get_blob(handle, key.c_str(), out, &size);
    nvs_close(handle);
    return (err == ESP_OK && size == sizeof(LightRgbPreset));
}

static bool light_preset_to_nvs(int slot, const LightRgbPreset &preset) {
    if (slot < 1 || slot > kLightPresetCount) return false;
    nvs_handle_t handle;
    esp_err_t err = nvs_open(kLightNamespace, NVS_READWRITE, &handle);
    if (err != ESP_OK) {
        ESP_LOGW(TAG, "NVS open failed for light preset: %s", esp_err_to_name(err));
        return false;
    }
    std::string key = light_preset_key(slot);
    err = nvs_set_blob(handle, key.c_str(), &preset, sizeof(preset));
    if (err == ESP_OK) {
        nvs_commit(handle);
    }
    nvs_close(handle);
    return (err == ESP_OK);
}

static bool light_preset_clear(int slot) {
    if (slot < 1 || slot > kLightPresetCount) return false;
    nvs_handle_t handle;
    esp_err_t err = nvs_open(kLightNamespace, NVS_READWRITE, &handle);
    if (err != ESP_OK) {
        ESP_LOGW(TAG, "NVS open failed for light preset clear: %s", esp_err_to_name(err));
        return false;
    }
    std::string key = light_preset_key(slot);
    err = nvs_erase_key(handle, key.c_str());
    if (err == ESP_OK) {
        nvs_commit(handle);
    }
    nvs_close(handle);
    return (err == ESP_OK);
}

static bool light_is_digital_mode() {
    return s_light_wiring_preset && strcmp(s_light_wiring_preset->ui_mode, "digital") == 0;
}

static bool light_is_pwm_rgb_mode() {
    return s_light_wiring_preset && strcmp(s_light_wiring_preset->ui_mode, "rgb") == 0;
}

static bool light_use_rgb_controls() {
    return s_light_wiring_preset &&
           (strcmp(s_light_wiring_preset->ui_mode, "rgb") == 0 ||
            strcmp(s_light_wiring_preset->ui_mode, "digital") == 0);
}

static uint8_t light_scale_level(uint8_t value, uint8_t brightness) {
    return static_cast<uint8_t>((static_cast<uint32_t>(value) * brightness + 50) / 100);
}

static uint8_t light_percent_to_u8(uint8_t percent) {
    return static_cast<uint8_t>((static_cast<uint32_t>(percent) * 255 + 50) / 100);
}

static void light_add_rgb_json(cJSON *res) {
    if (!light_use_rgb_controls() || !res) return;
    cJSON_AddNumberToObject(res, "r", s_light_rgb[0]);
    cJSON_AddNumberToObject(res, "g", s_light_rgb[1]);
    cJSON_AddNumberToObject(res, "b", s_light_rgb[2]);
}

static void light_set_brightness(uint8_t percent, bool persist) {
    if (light_use_rgb_controls()) {
        if (percent > 100) percent = 100;
        if (light_is_pwm_rgb_mode() && light_rgb_init() != ESP_OK) return;
        s_light_brightness = percent;
        s_light_state = (percent > 0);
        if (s_light_brightness > 0 && s_light_rgb[0] == 0 && s_light_rgb[1] == 0 && s_light_rgb[2] == 0) {
            s_light_rgb[0] = 100;
            s_light_rgb[1] = 100;
            s_light_rgb[2] = 100;
        }
        light_rgb_apply_outputs();
        if (persist) {
            light_state_to_nvs(s_light_state);
            light_brightness_to_nvs(s_light_brightness);
            if (s_light_brightness > 0) {
                light_last_on_to_nvs(s_light_brightness);
            }
        }
        return;
    }
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

static esp_err_t light_rgb_init() {
    if (s_light_rgb_initialized) return ESP_OK;
    for (int i = 0; i < 3; ++i) {
        if (kLightRgbChannels[i] <= LEDC_CHANNEL_2) {
            ESP_LOGW(TAG, "Light RGB channel %d overlaps status LED channels (0-2)", kLightRgbChannels[i]);
        }
    }
    ledc_timer_config_t timer_cfg = {};
    timer_cfg.speed_mode = kLightRgbSpeedMode;
    timer_cfg.timer_num = kLightRgbTimer;
    timer_cfg.duty_resolution = kLightRgbDutyResolution;
    timer_cfg.freq_hz = kLightRgbFreqHz;
    timer_cfg.clk_cfg = LEDC_AUTO_CLK;
    esp_err_t err = ledc_timer_config(&timer_cfg);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "light_rgb timer config failed: %s", esp_err_to_name(err));
        return err;
    }

    for (int i = 0; i < 3; ++i) {
        ledc_channel_config_t cfg = {};
        cfg.speed_mode = kLightRgbSpeedMode;
        cfg.channel = kLightRgbChannels[i];
        cfg.timer_sel = kLightRgbTimer;
        cfg.intr_type = LEDC_INTR_DISABLE;
        cfg.gpio_num = kLightRgbPins[i];
        cfg.duty = 0;
        cfg.hpoint = 0;
        err = ledc_channel_config(&cfg);
        if (err != ESP_OK) {
            ESP_LOGE(TAG, "light_rgb channel %d config failed: %s", i, esp_err_to_name(err));
            return err;
        }
    }

    s_light_rgb_initialized = true;
    s_light_rgb[0] = s_light_rgb[1] = s_light_rgb[2] = 0;
    ESP_LOGI(TAG, "Light RGB test initialized on GPIOs R=%d G=%d B=%d",
             kLightRgbPins[0], kLightRgbPins[1], kLightRgbPins[2]);
    return ESP_OK;
}

static void light_rgb_set_channel(int channel, uint8_t percent) {
    if (channel < 0 || channel >= 3) return;
    if (!s_light_rgb_initialized) return;
    if (percent > 100) percent = 100;
    static const uint8_t kGammaTable[101] = {
        0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 1, 1, 1, 1, 2, 2, 2, 2, 3,
        3, 3, 4, 4, 4, 5, 5, 6, 6, 7,
        7, 8, 8, 9, 9, 10, 11, 11, 12, 13,
        13, 14, 15, 16, 16, 17, 18, 19, 20, 21,
        22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
        33, 34, 35, 36, 37, 39, 40, 41, 43, 44,
        46, 47, 49, 50, 52, 53, 55, 56, 58, 60,
        61, 63, 65, 66, 68, 70, 72, 74, 75, 77,
        79, 81, 83, 85, 87, 89, 91, 94, 96, 98,
        100
    };
    uint8_t gamma_percent = kGammaTable[percent];
    uint32_t max_duty = (1u << kLightRgbDutyResolution) - 1;
    uint32_t duty = (max_duty * gamma_percent) / 100;
    ledc_set_duty(kLightRgbSpeedMode, kLightRgbChannels[channel], duty);
    ledc_update_duty(kLightRgbSpeedMode, kLightRgbChannels[channel]);
}

static void light_rgb_apply_outputs() {
    uint8_t scale = s_light_state ? s_light_brightness : 0;
    if (light_is_digital_mode()) {
        uint8_t r = light_scale_level(light_percent_to_u8(s_light_rgb[0]), scale);
        uint8_t g = light_scale_level(light_percent_to_u8(s_light_rgb[1]), scale);
        uint8_t b = light_scale_level(light_percent_to_u8(s_light_rgb[2]), scale);
        uint16_t count = s_light_digital_count ? s_light_digital_count : 90;
        addressable_led_fill_strip(r, g, b, count);
        return;
    }
    if (!s_light_rgb_initialized) return;
    for (int i = 0; i < 3; ++i) {
        uint32_t level = (static_cast<uint32_t>(s_light_rgb[i]) * scale) / 100;
        light_rgb_set_channel(i, static_cast<uint8_t>(level));
    }
}

static void light_rgb_set_base(int channel, uint8_t percent) {
    if (channel < 0 || channel >= 3) return;
    if (percent > 100) percent = 100;
    s_light_rgb[channel] = percent;
    light_rgb_apply_outputs();
}

static uint8_t light_prepare_digital_effect() {
    if (s_light_brightness == 0) {
        s_light_state = false;
        return 0;
    }
    s_light_state = true;
    return s_light_brightness;
}

static const LightWiringPreset kLightWiringPresets[] = {
    { "2wire-dim", "2-wire Dimmable (single)", "V+ / CH1", 1, "single" },
    { "2wire-cct-tied", "2-wire CCT (tied warm/cool)", "V+ / CH1 (CW+WW)", 1, "single" },
    { "3wire-cct", "3-wire CCT (warm + cool)", "V+ / CH1 (CW) / CH2 (WW)", 2, "cct" },
    { "4wire-rgb", "4-wire RGB", "V+ / CH1 (R) / CH2 (G) / CH3 (B)", 3, "rgb" },
    { "5wire-rgbw", "5-wire RGBW", "V+ / CH1 (R) / CH2 (G) / CH3 (B) / CH4 (W)", 4, "rgbw" },
    { "6wire-rgbcw", "6-wire RGB + CW + WW", "V+ / CH1 (R) / CH2 (G) / CH3 (B) / CH4 (CW) / CH5 (WW)", 5, "rgbcw" },
    { "generic-6ch", "Generic multi-channel (5 outputs)", "V+ / CH1 / CH2 / CH3 / CH4 / CH5", 5, "multi-channel" }
};
static const LightRgbPreset kLightRgbDefaultPresets[kLightPresetCount] = {
    { 100, 70, 40, 70 },  // Warm White
    { 60, 80, 100, 80 },  // Cool White
    { 100, 0, 0, 30 },    // Night Red
    { 100, 0, 100, 80 },  // Party RGB
    { 0, 100, 0, 40 },    // Green
    { 0, 0, 100, 40 }     // Blue
};

static const LightWiringPreset *light_find_wiring_preset(const char *type) {
    if (!type || type[0] == '\0') return nullptr;
    for (const auto &preset : kLightWiringPresets) {
        if (strcmp(preset.type, type) == 0) {
            return &preset;
        }
    }
    return nullptr;
}

static std::string light_wiring_type_from_nvs(bool *configured_out = nullptr) {
    nvs_handle_t handle;
    esp_err_t err = nvs_open(kLightWiringNamespace, NVS_READONLY, &handle);
    if (err != ESP_OK) {
        if (configured_out) *configured_out = false;
        return "";
    }
    size_t required_size = 0;
    err = nvs_get_str(handle, kLightWiringKeyType, nullptr, &required_size);
    if (err != ESP_OK || required_size == 0 || required_size > 64) {
        nvs_close(handle);
        if (configured_out) *configured_out = false;
        return "";
    }
    std::string value(required_size, '\0');
    err = nvs_get_str(handle, kLightWiringKeyType, value.data(), &required_size);
    nvs_close(handle);
    if (err != ESP_OK) {
        if (configured_out) *configured_out = false;
        return "";
    }
    if (!value.empty() && value.back() == '\0') {
        value.pop_back();
    }
    if (value.empty()) {
        if (configured_out) *configured_out = false;
        return "";
    }
    if (configured_out) *configured_out = true;
    return value;
}

static void light_wiring_type_to_nvs(const char *type) {
    if (!type || type[0] == '\0') return;
    nvs_handle_t handle;
    esp_err_t err = nvs_open(kLightWiringNamespace, NVS_READWRITE, &handle);
    if (err != ESP_OK) {
        ESP_LOGW(TAG, "NVS open failed for light wiring: %s", esp_err_to_name(err));
        return;
    }
    err = nvs_set_str(handle, kLightWiringKeyType, type);
    if (err == ESP_OK) {
        nvs_commit(handle);
    }
    nvs_close(handle);
}

static std::string light_wiring_order_from_nvs(bool *configured_out = nullptr) {
    nvs_handle_t handle;
    esp_err_t err = nvs_open(kLightWiringNamespace, NVS_READONLY, &handle);
    if (err != ESP_OK) {
        if (configured_out) *configured_out = false;
        return "";
    }
    size_t required_size = 0;
    err = nvs_get_str(handle, kLightWiringKeyOrder, nullptr, &required_size);
    if (err != ESP_OK || required_size == 0 || required_size > 16) {
        nvs_close(handle);
        if (configured_out) *configured_out = false;
        return "";
    }
    std::string value(required_size, '\0');
    err = nvs_get_str(handle, kLightWiringKeyOrder, value.data(), &required_size);
    nvs_close(handle);
    if (err != ESP_OK) {
        if (configured_out) *configured_out = false;
        return "";
    }
    if (!value.empty() && value.back() == '\0') {
        value.pop_back();
    }
    if (value.empty()) {
        if (configured_out) *configured_out = false;
        return "";
    }
    if (configured_out) *configured_out = true;
    return value;
}

static void light_wiring_order_to_nvs(const char *order) {
    if (!order || order[0] == '\0') return;
    nvs_handle_t handle;
    esp_err_t err = nvs_open(kLightWiringNamespace, NVS_READWRITE, &handle);
    if (err != ESP_OK) {
        ESP_LOGW(TAG, "NVS open failed for light wiring order: %s", esp_err_to_name(err));
        return;
    }
    err = nvs_set_str(handle, kLightWiringKeyOrder, order);
    if (err == ESP_OK) {
        nvs_commit(handle);
    }
    nvs_close(handle);
}

static std::string normalize_wiring_order(const char *order) {
    if (!order || order[0] == '\0') return "";
    std::string value = order;
    std::transform(value.begin(), value.end(), value.begin(), ::toupper);
    if (value == "RGB" || value == "GRB") {
        return value;
    }
    return "";
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
static const httpd_uri_t URI_EVENTS = { .uri = "/rpc/Events", .method = HTTP_GET, .handler = rpc_events_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_CMD = { .uri = "/rpc/Light.Command", .method = HTTP_POST, .handler = light_command_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_STATUS = { .uri = "/rpc/Light.Status", .method = HTTP_POST, .handler = light_status_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_BRIGHTNESS_GET = { .uri = "/rpc/Light.Brightness", .method = HTTP_GET, .handler = light_brightness_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_BRIGHTNESS_SET = { .uri = "/rpc/Light.Brightness", .method = HTTP_POST, .handler = light_brightness_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_WIRING_GET = { .uri = "/rpc/Light.Wiring", .method = HTTP_GET, .handler = light_wiring_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_WIRING_SET = { .uri = "/rpc/Light.Wiring", .method = HTTP_POST, .handler = light_wiring_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_RGB = { .uri = "/rpc/Light.Rgb", .method = HTTP_POST, .handler = light_rgb_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_RGB_TEST = { .uri = "/rpc/Light.RgbTest", .method = HTTP_POST, .handler = light_rgb_test_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_DIGITAL_TEST = { .uri = "/rpc/Light.DigitalTest", .method = HTTP_POST, .handler = light_digital_test_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_DIGITAL_CHASE = { .uri = "/rpc/Light.DigitalChase", .method = HTTP_POST, .handler = light_digital_chase_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_DIGITAL_WIPE = { .uri = "/rpc/Light.DigitalWipe", .method = HTTP_POST, .handler = light_digital_wipe_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_DIGITAL_PULSE = { .uri = "/rpc/Light.DigitalPulse", .method = HTTP_POST, .handler = light_digital_pulse_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_DIGITAL_RAINBOW = { .uri = "/rpc/Light.DigitalRainbow", .method = HTTP_POST, .handler = light_digital_rainbow_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_PRESET_GET = { .uri = "/rpc/Light.Preset", .method = HTTP_GET, .handler = light_preset_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LIGHT_PRESET_SET = { .uri = "/rpc/Light.Preset", .method = HTTP_POST, .handler = light_preset_handler, .user_ctx = NULL };
static const httpd_uri_t URI_BED_STATUS_DISABLED = { .uri = "/rpc/Bed.Status", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"bed" };
static const httpd_uri_t URI_BED_CMD_DISABLED = { .uri = "/rpc/Bed.Command", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"bed" };
static const httpd_uri_t URI_LIGHT_STATUS_DISABLED = { .uri = "/rpc/Light.Status", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_CMD_DISABLED = { .uri = "/rpc/Light.Command", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_BRIGHTNESS_DISABLED = { .uri = "/rpc/Light.Brightness", .method = HTTP_GET, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_BRIGHTNESS_DISABLED_POST = { .uri = "/rpc/Light.Brightness", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_WIRING_DISABLED = { .uri = "/rpc/Light.Wiring", .method = HTTP_GET, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_WIRING_DISABLED_POST = { .uri = "/rpc/Light.Wiring", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_RGB_DISABLED = { .uri = "/rpc/Light.Rgb", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_RGB_TEST_DISABLED = { .uri = "/rpc/Light.RgbTest", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_DIGITAL_TEST_DISABLED = { .uri = "/rpc/Light.DigitalTest", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_DIGITAL_CHASE_DISABLED = { .uri = "/rpc/Light.DigitalChase", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_DIGITAL_WIPE_DISABLED = { .uri = "/rpc/Light.DigitalWipe", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_DIGITAL_PULSE_DISABLED = { .uri = "/rpc/Light.DigitalPulse", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_DIGITAL_RAINBOW_DISABLED = { .uri = "/rpc/Light.DigitalRainbow", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_PRESET_DISABLED = { .uri = "/rpc/Light.Preset", .method = HTTP_GET, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_LIGHT_PRESET_DISABLED_POST = { .uri = "/rpc/Light.Preset", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"light" };
static const httpd_uri_t URI_TRAY_STATUS_DISABLED = { .uri = "/rpc/Tray.Status", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"tray" };
static const httpd_uri_t URI_CURTAIN_STATUS_DISABLED = { .uri = "/rpc/Curtains.Status", .method = HTTP_POST, .handler = role_disabled_handler, .user_ctx = (void*)"curtains" };
static const httpd_uri_t URI_LEGACY_STATUS = { .uri = "/status", .method = HTTP_GET, .handler = legacy_status_handler, .user_ctx = NULL };
static const httpd_uri_t URI_CLOSE_AP = { .uri = "/close_ap", .method = HTTP_POST, .handler = close_ap_handler, .user_ctx = NULL };
static const httpd_uri_t URI_RESET_WIFI = { .uri = "/reset_wifi", .method = HTTP_POST, .handler = reset_wifi_handler, .user_ctx = NULL };
static const httpd_uri_t URI_OTA = { .uri = "/rpc/Bed.OTA", .method = HTTP_POST, .handler = ota_upload_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LOG = { .uri = "/rpc/Bed.Log", .method = HTTP_POST, .handler = log_handler, .user_ctx = NULL };
static const httpd_uri_t URI_LOG_SETTINGS = { .uri = "/rpc/Log.Settings", .method = HTTP_POST, .handler = log_settings_handler, .user_ctx = NULL };
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
static const httpd_uri_t URI_OPTIONS_LIGHT_RGB = { .uri = "/rpc/Light.Rgb", .method = HTTP_OPTIONS, .handler = options_cors_handler, .user_ctx = NULL };
static const httpd_uri_t URI_OPTIONS_LIGHT_RGB_TEST = { .uri = "/rpc/Light.RgbTest", .method = HTTP_OPTIONS, .handler = options_cors_handler, .user_ctx = NULL };
static const httpd_uri_t URI_OPTIONS_LIGHT_DIGITAL_TEST = { .uri = "/rpc/Light.DigitalTest", .method = HTTP_OPTIONS, .handler = options_cors_handler, .user_ctx = NULL };
static const httpd_uri_t URI_OPTIONS_LIGHT_DIGITAL_CHASE = { .uri = "/rpc/Light.DigitalChase", .method = HTTP_OPTIONS, .handler = options_cors_handler, .user_ctx = NULL };
static const httpd_uri_t URI_OPTIONS_LIGHT_DIGITAL_WIPE = { .uri = "/rpc/Light.DigitalWipe", .method = HTTP_OPTIONS, .handler = options_cors_handler, .user_ctx = NULL };
static const httpd_uri_t URI_OPTIONS_LIGHT_DIGITAL_PULSE = { .uri = "/rpc/Light.DigitalPulse", .method = HTTP_OPTIONS, .handler = options_cors_handler, .user_ctx = NULL };
static const httpd_uri_t URI_OPTIONS_LIGHT_DIGITAL_RAINBOW = { .uri = "/rpc/Light.DigitalRainbow", .method = HTTP_OPTIONS, .handler = options_cors_handler, .user_ctx = NULL };
static const httpd_uri_t URI_OPTIONS_LIGHT_PRESET = { .uri = "/rpc/Light.Preset", .method = HTTP_OPTIONS, .handler = options_cors_handler, .user_ctx = NULL };

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
    if (light_use_rgb_controls()) {
        uint8_t prev_brightness = s_light_brightness;
        if (light_is_pwm_rgb_mode() && light_rgb_init() != ESP_OK) return;
        if (on) {
            if (prev_brightness == 0) {
                uint8_t last_on = 0;
                if (light_last_on_from_nvs(&last_on)) {
                    s_light_brightness = last_on;
                } else {
                    s_light_brightness = 100;
                }
            }
            s_light_state = true;
            if (s_light_rgb[0] == 0 && s_light_rgb[1] == 0 && s_light_rgb[2] == 0) {
                s_light_rgb[0] = 100;
                s_light_rgb[1] = 100;
                s_light_rgb[2] = 100;
            }
        } else {
            s_light_state = false;
        }
        light_rgb_apply_outputs();
        light_state_to_nvs(s_light_state);
        light_brightness_to_nvs(s_light_brightness);
        if (s_light_state && s_light_brightness > 0) {
            light_last_on_to_nvs(s_light_brightness);
        } else if (!s_light_state && prev_brightness > 0) {
            light_last_on_to_nvs(prev_brightness);
        }
        return;
    }
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
    cJSON_AddNumberToObject(res, "gpio", light_use_rgb_controls() ? -1 : LIGHT_GPIO);
    cJSON_AddNumberToObject(res, "brightness", s_light_brightness);
    light_add_rgb_json(res);
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
    cJSON_AddNumberToObject(res, "gpio", light_use_rgb_controls() ? -1 : LIGHT_GPIO);
    cJSON_AddNumberToObject(res, "brightness", s_light_brightness);
    light_add_rgb_json(res);
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
    cJSON_AddNumberToObject(res, "gpio", light_use_rgb_controls() ? -1 : LIGHT_GPIO);
    light_add_rgb_json(res);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
#endif
}

static esp_err_t light_rgb_handler(httpd_req_t *req) {
    add_cors(req);
#if !APP_ROLE_LIGHT
    return role_disabled_handler(req);
#else
    if (!light_use_rgb_controls()) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "RGB mode not active");
        return ESP_FAIL;
    }
    char buf[192] = {0};
    int ret = httpd_req_recv(req, buf, sizeof(buf) - 1);
    if (ret > 0) buf[ret] = '\0';
    cJSON *root = cJSON_Parse(buf);
    if (!root) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad JSON");
        return ESP_FAIL;
    }
    if (light_is_pwm_rgb_mode() && light_rgb_init() != ESP_OK) {
        cJSON_Delete(root);
        httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "RGB init failed");
        return ESP_FAIL;
    }
    bool updated = false;
    cJSON *rItem = cJSON_GetObjectItem(root, "r");
    cJSON *gItem = cJSON_GetObjectItem(root, "g");
    cJSON *bItem = cJSON_GetObjectItem(root, "b");
    cJSON *countItem = cJSON_GetObjectItem(root, "count");
    if (light_is_digital_mode() && cJSON_IsNumber(countItem)) {
        int count = countItem->valueint;
        if (count > 0 && count <= 600) {
            s_light_digital_count = static_cast<uint16_t>(count);
        }
    }
    if (cJSON_IsNumber(rItem)) { light_rgb_set_base(0, (uint8_t)rItem->valueint); updated = true; }
    if (cJSON_IsNumber(gItem)) { light_rgb_set_base(1, (uint8_t)gItem->valueint); updated = true; }
    if (cJSON_IsNumber(bItem)) { light_rgb_set_base(2, (uint8_t)bItem->valueint); updated = true; }
    cJSON_Delete(root);

    if (updated) {
        if (s_light_brightness == 0 && (s_light_rgb[0] || s_light_rgb[1] || s_light_rgb[2])) {
            s_light_brightness = 100;
        }
        s_light_state = (s_light_brightness > 0) && (s_light_rgb[0] || s_light_rgb[1] || s_light_rgb[2]);
        light_rgb_apply_outputs();
        light_state_to_nvs(s_light_state);
        light_brightness_to_nvs(s_light_brightness);
        if (s_light_state && s_light_brightness > 0) {
            light_last_on_to_nvs(s_light_brightness);
        }
    }

    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", "ok");
    cJSON_AddStringToObject(res, "state", s_light_state ? "on" : "off");
    cJSON_AddNumberToObject(res, "brightness", s_light_brightness);
    light_add_rgb_json(res);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
#endif
}

static esp_err_t light_rgb_test_handler(httpd_req_t *req) {
    add_cors(req);
#if !APP_ROLE_LIGHT
    return role_disabled_handler(req);
#else
    if (!light_is_pwm_rgb_mode()) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "RGB test not supported");
        return ESP_FAIL;
    }
    char buf[160] = {0};
    int ret = httpd_req_recv(req, buf, sizeof(buf) - 1);
    if (ret > 0) buf[ret] = '\0';
    cJSON *root = cJSON_Parse(buf);
    if (!root) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad JSON");
        return ESP_FAIL;
    }
    int channel = -1;
    cJSON *chItem = cJSON_GetObjectItem(root, "channel");
    cJSON *colorItem = cJSON_GetObjectItem(root, "color");
    if (cJSON_IsNumber(chItem)) {
        channel = chItem->valueint;
    } else if (cJSON_IsString(colorItem) && colorItem->valuestring) {
        std::string c = colorItem->valuestring;
        std::transform(c.begin(), c.end(), c.begin(), ::tolower);
        if (c == "r" || c == "red") channel = 0;
        else if (c == "g" || c == "green") channel = 1;
        else if (c == "b" || c == "blue") channel = 2;
    }
    cJSON *valItem = cJSON_GetObjectItem(root, "brightness");
    int level = cJSON_IsNumber(valItem) ? valItem->valueint : -1;
    cJSON_Delete(root);

    if (channel < 0 || channel > 2) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad channel");
        return ESP_FAIL;
    }
    if (level < 0 || level > 100) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad brightness");
        return ESP_FAIL;
    }
    esp_err_t err = light_rgb_init();
    if (err != ESP_OK) {
        httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "RGB init failed");
        return ESP_FAIL;
    }
    light_rgb_set_base(channel, (uint8_t)level);
    if (level > 0 && s_light_brightness == 0) {
        s_light_brightness = 100;
    }
    s_light_state = (s_light_brightness > 0) && (s_light_rgb[0] || s_light_rgb[1] || s_light_rgb[2]);
    light_rgb_apply_outputs();

    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", "ok");
    cJSON_AddNumberToObject(res, "channel", channel);
    cJSON_AddNumberToObject(res, "brightness", level);
    light_add_rgb_json(res);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
#endif
}

static esp_err_t light_digital_test_handler(httpd_req_t *req) {
    add_cors(req);
#if !APP_ROLE_LIGHT
    return role_disabled_handler(req);
#else
    char buf[160] = {0};
    int ret = httpd_req_recv(req, buf, sizeof(buf) - 1);
    if (ret > 0) buf[ret] = '\0';
    cJSON *root = cJSON_Parse(buf);
    if (!root) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad JSON");
        return ESP_FAIL;
    }
    cJSON *rItem = cJSON_GetObjectItem(root, "r");
    cJSON *gItem = cJSON_GetObjectItem(root, "g");
    cJSON *bItem = cJSON_GetObjectItem(root, "b");
    cJSON *countItem = cJSON_GetObjectItem(root, "count");
    int r = cJSON_IsNumber(rItem) ? rItem->valueint : 0;
    int g = cJSON_IsNumber(gItem) ? gItem->valueint : 0;
    int b = cJSON_IsNumber(bItem) ? bItem->valueint : 0;
    int count = cJSON_IsNumber(countItem) ? countItem->valueint : 90;
    cJSON_Delete(root);

    if (r < 0 || r > 255 || g < 0 || g > 255 || b < 0 || b > 255) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad color");
        return ESP_FAIL;
    }
    if (count <= 0 || count > 600) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad count");
        return ESP_FAIL;
    }
    s_light_digital_count = static_cast<uint16_t>(count);
    uint8_t brightness = light_prepare_digital_effect();
    uint8_t sr = light_scale_level(static_cast<uint8_t>(r), brightness);
    uint8_t sg = light_scale_level(static_cast<uint8_t>(g), brightness);
    uint8_t sb = light_scale_level(static_cast<uint8_t>(b), brightness);
    if (!addressable_led_fill_strip(sr, sg, sb, static_cast<uint16_t>(count))) {
        httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Digital test failed");
        return ESP_FAIL;
    }

    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", "ok");
    cJSON_AddNumberToObject(res, "count", count);
    cJSON_AddNumberToObject(res, "r", r);
    cJSON_AddNumberToObject(res, "g", g);
    cJSON_AddNumberToObject(res, "b", b);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
#endif
}

static esp_err_t light_digital_chase_handler(httpd_req_t *req) {
    add_cors(req);
#if !APP_ROLE_LIGHT
    return role_disabled_handler(req);
#else
    char buf[192] = {0};
    int ret = httpd_req_recv(req, buf, sizeof(buf) - 1);
    if (ret > 0) buf[ret] = '\0';
    cJSON *root = cJSON_Parse(buf);
    if (!root) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad JSON");
        return ESP_FAIL;
    }
    cJSON *rItem = cJSON_GetObjectItem(root, "r");
    cJSON *gItem = cJSON_GetObjectItem(root, "g");
    cJSON *bItem = cJSON_GetObjectItem(root, "b");
    cJSON *countItem = cJSON_GetObjectItem(root, "count");
    cJSON *stepsItem = cJSON_GetObjectItem(root, "steps");
    cJSON *delayItem = cJSON_GetObjectItem(root, "delay_ms");
    int r = cJSON_IsNumber(rItem) ? rItem->valueint : 0;
    int g = cJSON_IsNumber(gItem) ? gItem->valueint : 0;
    int b = cJSON_IsNumber(bItem) ? bItem->valueint : 0;
    int count = cJSON_IsNumber(countItem) ? countItem->valueint : 90;
    int steps = cJSON_IsNumber(stepsItem) ? stepsItem->valueint : count;
    int delay_ms = cJSON_IsNumber(delayItem) ? delayItem->valueint : 30;
    cJSON_Delete(root);

    if (r < 0 || r > 255 || g < 0 || g > 255 || b < 0 || b > 255) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad color");
        return ESP_FAIL;
    }
    if (count <= 0 || count > 600) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad count");
        return ESP_FAIL;
    }
    if (steps <= 0 || steps > 600) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad steps");
        return ESP_FAIL;
    }
    if (delay_ms < 0 || delay_ms > 1000) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad delay");
        return ESP_FAIL;
    }
    s_light_digital_count = static_cast<uint16_t>(count);
    uint8_t brightness = light_prepare_digital_effect();
    uint8_t sr = light_scale_level(static_cast<uint8_t>(r), brightness);
    uint8_t sg = light_scale_level(static_cast<uint8_t>(g), brightness);
    uint8_t sb = light_scale_level(static_cast<uint8_t>(b), brightness);
    if (!addressable_led_chase(sr,
                               sg,
                               sb,
                               static_cast<uint16_t>(count),
                               static_cast<uint16_t>(steps),
                               static_cast<uint16_t>(delay_ms))) {
        httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Digital chase failed");
        return ESP_FAIL;
    }

    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", "ok");
    cJSON_AddNumberToObject(res, "count", count);
    cJSON_AddNumberToObject(res, "steps", steps);
    cJSON_AddNumberToObject(res, "delay_ms", delay_ms);
    cJSON_AddNumberToObject(res, "r", r);
    cJSON_AddNumberToObject(res, "g", g);
    cJSON_AddNumberToObject(res, "b", b);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
#endif
}

static esp_err_t light_digital_wipe_handler(httpd_req_t *req) {
    add_cors(req);
#if !APP_ROLE_LIGHT
    return role_disabled_handler(req);
#else
    char buf[192] = {0};
    int ret = httpd_req_recv(req, buf, sizeof(buf) - 1);
    if (ret > 0) buf[ret] = '\0';
    cJSON *root = cJSON_Parse(buf);
    if (!root) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad JSON");
        return ESP_FAIL;
    }
    cJSON *rItem = cJSON_GetObjectItem(root, "r");
    cJSON *gItem = cJSON_GetObjectItem(root, "g");
    cJSON *bItem = cJSON_GetObjectItem(root, "b");
    cJSON *countItem = cJSON_GetObjectItem(root, "count");
    cJSON *delayItem = cJSON_GetObjectItem(root, "delay_ms");
    int r = cJSON_IsNumber(rItem) ? rItem->valueint : 0;
    int g = cJSON_IsNumber(gItem) ? gItem->valueint : 0;
    int b = cJSON_IsNumber(bItem) ? bItem->valueint : 0;
    int count = cJSON_IsNumber(countItem) ? countItem->valueint : 90;
    int delay_ms = cJSON_IsNumber(delayItem) ? delayItem->valueint : 20;
    cJSON_Delete(root);

    if (r < 0 || r > 255 || g < 0 || g > 255 || b < 0 || b > 255) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad color");
        return ESP_FAIL;
    }
    if (count <= 0 || count > 600) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad count");
        return ESP_FAIL;
    }
    if (delay_ms < 0 || delay_ms > 1000) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad delay");
        return ESP_FAIL;
    }
    s_light_digital_count = static_cast<uint16_t>(count);
    uint8_t brightness = light_prepare_digital_effect();
    uint8_t sr = light_scale_level(static_cast<uint8_t>(r), brightness);
    uint8_t sg = light_scale_level(static_cast<uint8_t>(g), brightness);
    uint8_t sb = light_scale_level(static_cast<uint8_t>(b), brightness);
    if (!addressable_led_wipe(sr, sg, sb, static_cast<uint16_t>(count), static_cast<uint16_t>(delay_ms))) {
        httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Digital wipe failed");
        return ESP_FAIL;
    }

    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", "ok");
    cJSON_AddNumberToObject(res, "count", count);
    cJSON_AddNumberToObject(res, "delay_ms", delay_ms);
    cJSON_AddNumberToObject(res, "r", r);
    cJSON_AddNumberToObject(res, "g", g);
    cJSON_AddNumberToObject(res, "b", b);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
#endif
}

static esp_err_t light_digital_pulse_handler(httpd_req_t *req) {
    add_cors(req);
#if !APP_ROLE_LIGHT
    return role_disabled_handler(req);
#else
    char buf[192] = {0};
    int ret = httpd_req_recv(req, buf, sizeof(buf) - 1);
    if (ret > 0) buf[ret] = '\0';
    cJSON *root = cJSON_Parse(buf);
    if (!root) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad JSON");
        return ESP_FAIL;
    }
    cJSON *rItem = cJSON_GetObjectItem(root, "r");
    cJSON *gItem = cJSON_GetObjectItem(root, "g");
    cJSON *bItem = cJSON_GetObjectItem(root, "b");
    cJSON *countItem = cJSON_GetObjectItem(root, "count");
    cJSON *stepsItem = cJSON_GetObjectItem(root, "steps");
    cJSON *delayItem = cJSON_GetObjectItem(root, "delay_ms");
    int r = cJSON_IsNumber(rItem) ? rItem->valueint : 0;
    int g = cJSON_IsNumber(gItem) ? gItem->valueint : 0;
    int b = cJSON_IsNumber(bItem) ? bItem->valueint : 0;
    int count = cJSON_IsNumber(countItem) ? countItem->valueint : 90;
    int steps = cJSON_IsNumber(stepsItem) ? stepsItem->valueint : 60;
    int delay_ms = cJSON_IsNumber(delayItem) ? delayItem->valueint : 20;
    cJSON_Delete(root);

    if (r < 0 || r > 255 || g < 0 || g > 255 || b < 0 || b > 255) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad color");
        return ESP_FAIL;
    }
    if (count <= 0 || count > 600) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad count");
        return ESP_FAIL;
    }
    if (steps <= 0 || steps > 600) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad steps");
        return ESP_FAIL;
    }
    if (delay_ms < 0 || delay_ms > 1000) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad delay");
        return ESP_FAIL;
    }
    s_light_digital_count = static_cast<uint16_t>(count);
    uint8_t brightness = light_prepare_digital_effect();
    uint8_t sr = light_scale_level(static_cast<uint8_t>(r), brightness);
    uint8_t sg = light_scale_level(static_cast<uint8_t>(g), brightness);
    uint8_t sb = light_scale_level(static_cast<uint8_t>(b), brightness);
    if (!addressable_led_pulse(sr,
                               sg,
                               sb,
                               static_cast<uint16_t>(count),
                               static_cast<uint16_t>(steps),
                               static_cast<uint16_t>(delay_ms))) {
        httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Digital pulse failed");
        return ESP_FAIL;
    }

    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", "ok");
    cJSON_AddNumberToObject(res, "count", count);
    cJSON_AddNumberToObject(res, "steps", steps);
    cJSON_AddNumberToObject(res, "delay_ms", delay_ms);
    cJSON_AddNumberToObject(res, "r", r);
    cJSON_AddNumberToObject(res, "g", g);
    cJSON_AddNumberToObject(res, "b", b);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
#endif
}

static esp_err_t light_digital_rainbow_handler(httpd_req_t *req) {
    add_cors(req);
#if !APP_ROLE_LIGHT
    return role_disabled_handler(req);
#else
    char buf[192] = {0};
    int ret = httpd_req_recv(req, buf, sizeof(buf) - 1);
    if (ret > 0) buf[ret] = '\0';
    cJSON *root = cJSON_Parse(buf);
    if (!root) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad JSON");
        return ESP_FAIL;
    }
    cJSON *countItem = cJSON_GetObjectItem(root, "count");
    cJSON *stepsItem = cJSON_GetObjectItem(root, "steps");
    cJSON *delayItem = cJSON_GetObjectItem(root, "delay_ms");
    int count = cJSON_IsNumber(countItem) ? countItem->valueint : 90;
    int steps = cJSON_IsNumber(stepsItem) ? stepsItem->valueint : 90;
    int delay_ms = cJSON_IsNumber(delayItem) ? delayItem->valueint : 20;
    cJSON_Delete(root);

    if (count <= 0 || count > 600) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad count");
        return ESP_FAIL;
    }
    if (steps <= 0 || steps > 1200) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad steps");
        return ESP_FAIL;
    }
    if (delay_ms < 0 || delay_ms > 1000) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad delay");
        return ESP_FAIL;
    }
    s_light_digital_count = static_cast<uint16_t>(count);
    uint8_t brightness = light_prepare_digital_effect();
    if (!addressable_led_rainbow(static_cast<uint16_t>(count),
                                 static_cast<uint16_t>(steps),
                                 static_cast<uint16_t>(delay_ms),
                                 brightness)) {
        httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Digital rainbow failed");
        return ESP_FAIL;
    }

    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", "ok");
    cJSON_AddNumberToObject(res, "count", count);
    cJSON_AddNumberToObject(res, "steps", steps);
    cJSON_AddNumberToObject(res, "delay_ms", delay_ms);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
#endif
}

static void light_preset_add_json(cJSON *obj, int slot, const LightRgbPreset *preset, bool set) {
    if (!obj) return;
    cJSON_AddNumberToObject(obj, "slot", slot);
    cJSON_AddBoolToObject(obj, "set", set);
    if (set && preset) {
        cJSON_AddNumberToObject(obj, "r", preset->r);
        cJSON_AddNumberToObject(obj, "g", preset->g);
        cJSON_AddNumberToObject(obj, "b", preset->b);
        cJSON_AddNumberToObject(obj, "brightness", preset->brightness);
    }
}

static esp_err_t light_preset_handler(httpd_req_t *req) {
    add_cors(req);
#if !APP_ROLE_LIGHT
    return role_disabled_handler(req);
#else
    if (!light_use_rgb_controls()) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "RGB mode not active");
        return ESP_FAIL;
    }
    if (req->method == HTTP_GET) {
        cJSON *res = cJSON_CreateObject();
        cJSON_AddStringToObject(res, "status", "ok");
        cJSON *arr = cJSON_AddArrayToObject(res, "presets");
        for (int slot = 1; slot <= kLightPresetCount; ++slot) {
            LightRgbPreset preset = {};
            bool set = light_preset_from_nvs(slot, &preset);
            if (!set) {
                preset = kLightRgbDefaultPresets[slot - 1];
                light_preset_to_nvs(slot, preset);
                set = true;
            }
            cJSON *item = cJSON_CreateObject();
            light_preset_add_json(item, slot, &preset, set);
            cJSON_AddItemToArray(arr, item);
        }
        char *jsonStr = cJSON_PrintUnformatted(res);
        httpd_resp_set_type(req, "application/json");
        httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
        free(jsonStr);
        cJSON_Delete(res);
        return ESP_OK;
    }

    char buf[160] = {0};
    int ret = httpd_req_recv(req, buf, sizeof(buf) - 1);
    if (ret > 0) buf[ret] = '\0';
    cJSON *root = cJSON_Parse(buf);
    if (!root) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad JSON");
        return ESP_FAIL;
    }
    cJSON *actionItem = cJSON_GetObjectItem(root, "action");
    cJSON *slotItem = cJSON_GetObjectItem(root, "slot");
    const char *actionStr = (cJSON_IsString(actionItem) && actionItem->valuestring) ? actionItem->valuestring : "";
    int slot = cJSON_IsNumber(slotItem) ? slotItem->valueint : 0;
    std::string action = actionStr;
    std::transform(action.begin(), action.end(), action.begin(), ::tolower);
    if (slot < 1 || slot > kLightPresetCount || (action != "save" && action != "apply" && action != "clear")) {
        cJSON_Delete(root);
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad preset action");
        return ESP_FAIL;
    }
    if (light_is_pwm_rgb_mode() && light_rgb_init() != ESP_OK) {
        cJSON_Delete(root);
        httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "RGB init failed");
        return ESP_FAIL;
    }

    LightRgbPreset preset = {};
    bool set = false;
    bool success = true;
    if (action == "save") {
        preset.r = s_light_rgb[0];
        preset.g = s_light_rgb[1];
        preset.b = s_light_rgb[2];
        preset.brightness = s_light_brightness;
        success = light_preset_to_nvs(slot, preset);
        set = success;
    } else if (action == "apply") {
        set = light_preset_from_nvs(slot, &preset);
        if (!set) {
            cJSON_Delete(root);
            httpd_resp_send_err(req, HTTPD_404_NOT_FOUND, "Preset not set");
            return ESP_FAIL;
        }
        s_light_rgb[0] = preset.r;
        s_light_rgb[1] = preset.g;
        s_light_rgb[2] = preset.b;
        s_light_brightness = preset.brightness;
        s_light_state = (s_light_brightness > 0) && (s_light_rgb[0] || s_light_rgb[1] || s_light_rgb[2]);
        light_rgb_apply_outputs();
        light_state_to_nvs(s_light_state);
        light_brightness_to_nvs(s_light_brightness);
        if (s_light_state && s_light_brightness > 0) {
            light_last_on_to_nvs(s_light_brightness);
        }
    } else if (action == "clear") {
        success = light_preset_clear(slot);
        set = false;
    }
    cJSON_Delete(root);

    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", success ? "ok" : "error");
    cJSON_AddStringToObject(res, "action", action.c_str());
    cJSON_AddStringToObject(res, "state", s_light_state ? "on" : "off");
    cJSON_AddNumberToObject(res, "brightness", s_light_brightness);
    light_add_rgb_json(res);
    cJSON *presetObj = cJSON_CreateObject();
    light_preset_add_json(presetObj, slot, &preset, set);
    cJSON_AddItemToObject(res, "preset", presetObj);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
    return ESP_OK;
#endif
}

static esp_err_t light_wiring_handler(httpd_req_t *req) {
    add_cors(req);
#if !APP_ROLE_LIGHT
    return role_disabled_handler(req);
#else
    if (req->method == HTTP_POST) {
        char buf[160] = {0};
        int ret = httpd_req_recv(req, buf, sizeof(buf) - 1);
        if (ret > 0) buf[ret] = '\0';
        cJSON *root = cJSON_Parse(buf);
        if (!root) {
            httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Bad JSON");
            return ESP_FAIL;
        }
        cJSON *typeItem = cJSON_GetObjectItem(root, "type");
        cJSON *orderItem = cJSON_GetObjectItem(root, "order");
        const char *typeStr = (cJSON_IsString(typeItem) && typeItem->valuestring) ? typeItem->valuestring : "";
        const char *orderStr = (cJSON_IsString(orderItem) && orderItem->valuestring) ? orderItem->valuestring : "";
        std::string order = normalize_wiring_order(orderStr);
        const LightWiringPreset *preset = light_find_wiring_preset(typeStr);
        if (!preset) {
            cJSON_Delete(root);
            httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Unknown wiring type");
            return ESP_FAIL;
        }
        light_wiring_type_to_nvs(preset->type);
        s_light_wiring_preset = preset;
        s_light_wiring_configured = true;
        if (strcmp(preset->ui_mode, "digital") == 0) {
            if (order.empty()) {
                bool order_configured = false;
                std::string existing = light_wiring_order_from_nvs(&order_configured);
                if (!order_configured || existing.empty()) {
                    order = ADDRESSABLE_LED_GRB ? "GRB" : "RGB";
                    light_wiring_order_to_nvs(order.c_str());
                } else {
                    order = existing;
                }
            } else {
                light_wiring_order_to_nvs(order.c_str());
            }
            if (!order.empty()) {
                addressable_led_set_order(order == "GRB");
            }
        }
        if (light_use_rgb_controls()) {
            if (s_light_initialized) {
                s_light.setBrightness(0);
                s_light_initialized = false;
            }
            s_light_state = false;
            s_light_brightness = 0;
            s_light_rgb[0] = s_light_rgb[1] = s_light_rgb[2] = 0;
            if (light_is_pwm_rgb_mode()) {
                if (light_rgb_init() == ESP_OK) {
                    light_rgb_apply_outputs();
                }
            } else {
                light_rgb_apply_outputs();
            }
        }
        cJSON_Delete(root);
    }

    bool configured = false;
    std::string type = light_wiring_type_from_nvs(&configured);
    const LightWiringPreset *preset = light_find_wiring_preset(type.c_str());
    if (!preset) {
        preset = light_find_wiring_preset(kLightWiringDefaultType);
    }
    s_light_wiring_preset = preset;
    s_light_wiring_configured = configured;
    if (!preset) {
        httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Missing wiring preset");
        return ESP_FAIL;
    }
    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "status", "ok");
    cJSON_AddStringToObject(res, "type", preset->type);
    cJSON_AddStringToObject(res, "label", preset->label);
    cJSON_AddStringToObject(res, "terminals", preset->terminals);
    cJSON_AddNumberToObject(res, "channels", preset->channels);
    cJSON_AddStringToObject(res, "ui_mode", preset->ui_mode);
    std::string wiring_order = light_wiring_order_from_nvs();
    if (wiring_order.empty()) {
        wiring_order = ADDRESSABLE_LED_GRB ? "GRB" : "RGB";
    }
    cJSON_AddStringToObject(res, "order", wiring_order.c_str());
    cJSON_AddNumberToObject(res, "version", 1);
    cJSON_AddBoolToObject(res, "configured", configured);
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

// Toggle server-side log categories (currently peer lookup/discover)
static esp_err_t log_settings_handler(httpd_req_t *req) {
    add_cors(req);
    char buf[128] = {0};
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
    cJSON *peer_log = cJSON_GetObjectItem(root, "peer_log");
    if (cJSON_IsBool(peer_log)) {
        s_peer_log_enabled = cJSON_IsTrue(peer_log);
    }
    cJSON_Delete(root);

    cJSON *res = cJSON_CreateObject();
    cJSON_AddBoolToObject(res, "peer_log", s_peer_log_enabled);
    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
    free(jsonStr);
    cJSON_Delete(res);
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

    const int64_t now_ms = esp_timer_get_time() / 1000;
    ESP_LOGI(TAG, "Bed.Command recv cmd=%s label=%s ts=%lld", cmd.c_str(), label.c_str(), (long long)now_ms);

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
    int64_t statusMs = esp_timer_get_time() / 1000;
    cJSON_AddNumberToObject(res, "uptime", (double)statusMs / 1000.0);
    cJSON_AddNumberToObject(res, "statusMs", (double)statusMs);

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
    int64_t remoteEventMs = 0;
    int32_t remoteDebounceMs = 0;
    int8_t remoteOptoIdx = -1;
    bedDriver->getRemoteEventInfo(remoteEventMs, remoteDebounceMs, remoteOptoIdx);
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

    int64_t statusMs = esp_timer_get_time() / 1000;
    cJSON_AddNumberToObject(res, "uptime", (double)statusMs / 1000.0);
    cJSON_AddNumberToObject(res, "statusMs", (double)statusMs);
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
    cJSON_AddNumberToObject(res, "remoteEventMs", (double)remoteEventMs);
    cJSON_AddNumberToObject(res, "remoteDebounceMs", remoteDebounceMs);
    cJSON_AddNumberToObject(res, "remoteOpto", remoteOptoIdx);

    static int64_t last_remote_event_ms = -1;
    if (remoteEventMs > 0 && remoteEventMs != last_remote_event_ms) {
        last_remote_event_ms = remoteEventMs;
    }

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

static esp_err_t send_sse_event(httpd_req_t *req, const char *event, const char *data) {
    std::string payload = "event: ";
    payload += event;
    payload += "\n";
    payload += "data: ";
    payload += data;
    payload += "\n\n";
    return httpd_resp_send_chunk(req, payload.c_str(), payload.size());
}

struct SseTaskCtx {
    httpd_req_t *req;
    volatile bool stop;
};

static SemaphoreHandle_t s_sse_mutex = nullptr;
static SseTaskCtx *s_sse_ctx = nullptr;

static void sse_task(void *arg) {
    SseTaskCtx *ctx = static_cast<SseTaskCtx*>(arg);
    const int64_t kPingIntervalMs = 15000;
    const int64_t kPollIntervalMs = 100;
    int64_t lastPingMs = 0;
    int64_t lastEventMs = -1;

    while (!ctx->stop) {
        int64_t nowMs = esp_timer_get_time() / 1000;
        if (nowMs - lastPingMs >= kPingIntervalMs) {
            cJSON *ping = cJSON_CreateObject();
            cJSON_AddStringToObject(ping, "type", "ping");
            cJSON_AddNumberToObject(ping, "statusMs", (double)nowMs);
            char *jsonStr = cJSON_PrintUnformatted(ping);
            esp_err_t err = send_sse_event(ctx->req, "ping", jsonStr);
            free(jsonStr);
            cJSON_Delete(ping);
            if (err != ESP_OK) break;
            lastPingMs = nowMs;
        }

#if APP_ROLE_BED
        if (bedDriver) {
            int64_t remoteEventMs = 0;
            int32_t remoteDebounceMs = 0;
            int8_t remoteOptoIdx = -1;
            bedDriver->getRemoteEventInfo(remoteEventMs, remoteDebounceMs, remoteOptoIdx);
            int64_t edgeEventMs = 0;
            int8_t edgeOptoIdx = -1;
            int8_t edgeOptoState = 1;
            bedDriver->getRemoteEdgeInfo(edgeEventMs, edgeOptoIdx, edgeOptoState);
            int ro1=1,ro2=1,ro3=1,ro4=1;
            bedDriver->getOptoRawStates(ro1, ro2, ro3, ro4);
            if (remoteEventMs > 0 && remoteEventMs != lastEventMs) {
                int o1=1,o2=1,o3=1,o4=1;
                bedDriver->getOptoStates(o1,o2,o3,o4);
                std::string hDir = "STOPPED", fDir = "STOPPED";
                bedDriver->getMotionDirs(hDir, fDir);

                cJSON *ev = cJSON_CreateObject();
                cJSON_AddStringToObject(ev, "type", "remote_event");
                cJSON_AddNumberToObject(ev, "eventMs", (double)remoteEventMs);
                cJSON_AddNumberToObject(ev, "debounceMs", remoteDebounceMs);
                cJSON_AddNumberToObject(ev, "statusMs", (double)nowMs);
                cJSON_AddNumberToObject(ev, "opto", remoteOptoIdx);
                cJSON_AddNumberToObject(ev, "opto1", o1);
                cJSON_AddNumberToObject(ev, "opto2", o2);
                cJSON_AddNumberToObject(ev, "opto3", o3);
                cJSON_AddNumberToObject(ev, "opto4", o4);
                cJSON_AddStringToObject(ev, "headDir", hDir.c_str());
                cJSON_AddStringToObject(ev, "footDir", fDir.c_str());

                char *jsonStr = cJSON_PrintUnformatted(ev);
                esp_err_t err = send_sse_event(ctx->req, "remote_event", jsonStr);
                free(jsonStr);
                cJSON_Delete(ev);
                if (err != ESP_OK) break;
                lastEventMs = remoteEventMs;
            }

            static int64_t lastEdgeMs = -1;
            if (edgeEventMs > 0 && edgeEventMs != lastEdgeMs) {
                cJSON *ev = cJSON_CreateObject();
                cJSON_AddStringToObject(ev, "type", "remote_edge");
                cJSON_AddNumberToObject(ev, "eventMs", (double)edgeEventMs);
                cJSON_AddNumberToObject(ev, "statusMs", (double)nowMs);
                cJSON_AddNumberToObject(ev, "opto", edgeOptoIdx);
                cJSON_AddNumberToObject(ev, "state", edgeOptoState);
                cJSON_AddNumberToObject(ev, "raw1", ro1);
                cJSON_AddNumberToObject(ev, "raw2", ro2);
                cJSON_AddNumberToObject(ev, "raw3", ro3);
                cJSON_AddNumberToObject(ev, "raw4", ro4);
                char *jsonStr = cJSON_PrintUnformatted(ev);
                esp_err_t err = send_sse_event(ctx->req, "remote_edge", jsonStr);
                free(jsonStr);
                cJSON_Delete(ev);
                if (err != ESP_OK) break;
                lastEdgeMs = edgeEventMs;
            }
        }
#endif

        vTaskDelay(pdMS_TO_TICKS(kPollIntervalMs));
    }

    httpd_resp_send_chunk(ctx->req, NULL, 0);
    httpd_req_async_handler_complete(ctx->req);

    if (s_sse_mutex) {
        if (xSemaphoreTake(s_sse_mutex, pdMS_TO_TICKS(100)) == pdTRUE) {
            if (s_sse_ctx == ctx) s_sse_ctx = nullptr;
            xSemaphoreGive(s_sse_mutex);
        }
    }
    free(ctx);
    vTaskDelete(nullptr);
}

static esp_err_t rpc_events_handler(httpd_req_t *req) {
#if !APP_ROLE_BED
    add_cors(req);
    httpd_resp_send_err(req, HTTPD_501_METHOD_NOT_IMPLEMENTED, "Bed role not enabled");
    return ESP_OK;
#else
    add_cors(req);
    httpd_req_t *async_req = nullptr;
    if (httpd_req_async_handler_begin(req, &async_req) != ESP_OK) {
        return ESP_FAIL;
    }

    httpd_resp_set_type(async_req, "text/event-stream");
    httpd_resp_set_hdr(async_req, "Cache-Control", "no-cache");
    httpd_resp_set_hdr(async_req, "Connection", "keep-alive");
    httpd_resp_set_hdr(async_req, "X-Accel-Buffering", "no");

    if (httpd_resp_send_chunk(async_req, ":\n\n", 3) != ESP_OK) {
        httpd_req_async_handler_complete(async_req);
        return ESP_FAIL;
    }

    if (!s_sse_mutex) {
        s_sse_mutex = xSemaphoreCreateMutex();
    }

    if (s_sse_mutex && xSemaphoreTake(s_sse_mutex, pdMS_TO_TICKS(100)) == pdTRUE) {
        if (s_sse_ctx) {
            s_sse_ctx->stop = true;
        }
        s_sse_ctx = (SseTaskCtx*)calloc(1, sizeof(SseTaskCtx));
        if (!s_sse_ctx) {
            xSemaphoreGive(s_sse_mutex);
            httpd_req_async_handler_complete(async_req);
            return ESP_FAIL;
        }
        s_sse_ctx->req = async_req;
        s_sse_ctx->stop = false;
        xSemaphoreGive(s_sse_mutex);
    } else {
        httpd_req_async_handler_complete(async_req);
        return ESP_FAIL;
    }

    if (xTaskCreate(sse_task, "sse_task", 4096, s_sse_ctx, 5, nullptr) != pdPASS) {
        if (s_sse_mutex && xSemaphoreTake(s_sse_mutex, pdMS_TO_TICKS(100)) == pdTRUE) {
            if (s_sse_ctx) {
                s_sse_ctx->stop = true;
                s_sse_ctx = nullptr;
            }
            xSemaphoreGive(s_sse_mutex);
        }
        httpd_req_async_handler_complete(async_req);
        return ESP_FAIL;
    }

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
    std::string wiring_type;
    bool wiring_configured = false;
    std::string wiring_order;
    bool wiring_order_configured = false;
#if APP_ROLE_LIGHT
    wiring_type = light_wiring_type_from_nvs(&wiring_configured);
    wiring_order = light_wiring_order_from_nvs(&wiring_order_configured);
#endif

    cJSON *res = cJSON_CreateObject();
    cJSON_AddStringToObject(res, "host", host.c_str());
    cJSON_AddStringToObject(res, "ip", ip_str);
    cJSON_AddStringToObject(res, "type", type.c_str());
    cJSON_AddStringToObject(res, "roles", roles.c_str());
    cJSON_AddStringToObject(res, "device_name", device_name.c_str());
    cJSON_AddStringToObject(res, "room", room.c_str());
    cJSON_AddStringToObject(res, "fw", UI_BUILD_TAG);
#if APP_ROLE_LIGHT
    if (wiring_configured) {
        cJSON_AddStringToObject(res, "wiring_type", wiring_type.c_str());
        if (wiring_order_configured && !wiring_order.empty()) {
            cJSON_AddStringToObject(res, "wiring_order", wiring_order.c_str());
        }
    }
#endif

    char *jsonStr = cJSON_PrintUnformatted(res);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_send(req, jsonStr, HTTPD_RESP_USE_STRLEN);
#if APP_ROLE_LIGHT
    if (s_peer_log_enabled) {
        if (wiring_configured) {
            ESP_LOGI(TAG, "Peer.Discover served host=%s ip=%s type=%s roles=%s wiring=%s order=%s fw=%s",
                     host.c_str(), ip_str, type.c_str(), roles.c_str(), wiring_type.c_str(),
                     wiring_order_configured ? wiring_order.c_str() : "-", UI_BUILD_TAG);
        } else {
            ESP_LOGI(TAG, "Peer.Discover served host=%s ip=%s type=%s roles=%s fw=%s",
                     host.c_str(), ip_str, type.c_str(), roles.c_str(), UI_BUILD_TAG);
        }
    }
#else
    if (s_peer_log_enabled) {
        ESP_LOGI(TAG, "Peer.Discover served host=%s ip=%s type=%s roles=%s fw=%s",
                 host.c_str(), ip_str, type.c_str(), roles.c_str(), UI_BUILD_TAG);
    }
#endif

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
    if (s_peer_log_enabled) {
        ESP_LOGI(TAG, "Peer.Lookup returned %d peer(s)", count);
    }

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
    bool wiring_configured = false;
    std::string wiring_type = light_wiring_type_from_nvs(&wiring_configured);
    const LightWiringPreset *preset = light_find_wiring_preset(wiring_type.c_str());
    if (!preset) {
        preset = light_find_wiring_preset(kLightWiringDefaultType);
    }
    s_light_wiring_preset = preset;
    s_light_wiring_configured = wiring_configured;
    bool use_rgb = light_use_rgb_controls();
    if (light_is_digital_mode()) {
        std::string order = light_wiring_order_from_nvs();
        if (order.empty()) {
            order = ADDRESSABLE_LED_GRB ? "GRB" : "RGB";
        }
        addressable_led_set_order(order == "GRB");
    }

    if (!use_rgb && s_light.begin((gpio_num_t)LIGHT_GPIO, true) == ESP_OK) {
        s_light_initialized = true;
    } else {
        s_light_initialized = false;
    }
    s_light_state = false;
    uint8_t last_on = 0;
    bool has_last_on = light_last_on_from_nvs(&last_on);
    uint8_t saved_brightness = light_brightness_from_nvs();
    bool saved_state = light_state_from_nvs();
    ESP_LOGI(TAG, "Light NVS last_on=%s %u", has_last_on ? "yes" : "no", last_on);
    ESP_LOGI(TAG, "Light NVS brightness=%u", saved_brightness);
    if (has_last_on) {
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
        httpd_register_uri_handler(server, &URI_OPTIONS_LIGHT_RGB);
        httpd_register_uri_handler(server, &URI_OPTIONS_LIGHT_RGB_TEST);
        httpd_register_uri_handler(server, &URI_OPTIONS_LIGHT_PRESET);
#if APP_ROLE_BED
        httpd_register_uri_handler(server, &URI_CMD);
        httpd_register_uri_handler(server, &URI_STATUS);
        httpd_register_uri_handler(server, &URI_EVENTS);
#else
        httpd_register_uri_handler(server, &URI_BED_CMD_DISABLED);
        httpd_register_uri_handler(server, &URI_BED_STATUS_DISABLED);
#endif
#if APP_ROLE_LIGHT
        httpd_register_uri_handler(server, &URI_LIGHT_CMD);
        httpd_register_uri_handler(server, &URI_LIGHT_STATUS);
        httpd_register_uri_handler(server, &URI_LIGHT_BRIGHTNESS_GET);
        httpd_register_uri_handler(server, &URI_LIGHT_BRIGHTNESS_SET);
        httpd_register_uri_handler(server, &URI_LIGHT_WIRING_GET);
        httpd_register_uri_handler(server, &URI_LIGHT_WIRING_SET);
        httpd_register_uri_handler(server, &URI_LIGHT_RGB);
        httpd_register_uri_handler(server, &URI_LIGHT_RGB_TEST);
        httpd_register_uri_handler(server, &URI_LIGHT_DIGITAL_TEST);
        httpd_register_uri_handler(server, &URI_LIGHT_DIGITAL_CHASE);
        httpd_register_uri_handler(server, &URI_LIGHT_DIGITAL_WIPE);
        httpd_register_uri_handler(server, &URI_LIGHT_DIGITAL_PULSE);
        httpd_register_uri_handler(server, &URI_LIGHT_DIGITAL_RAINBOW);
        httpd_register_uri_handler(server, &URI_LIGHT_PRESET_GET);
        httpd_register_uri_handler(server, &URI_LIGHT_PRESET_SET);
#else
        httpd_register_uri_handler(server, &URI_LIGHT_CMD_DISABLED);
        httpd_register_uri_handler(server, &URI_LIGHT_STATUS_DISABLED);
        httpd_register_uri_handler(server, &URI_LIGHT_BRIGHTNESS_DISABLED);
        httpd_register_uri_handler(server, &URI_LIGHT_BRIGHTNESS_DISABLED_POST);
        httpd_register_uri_handler(server, &URI_LIGHT_WIRING_DISABLED);
        httpd_register_uri_handler(server, &URI_LIGHT_WIRING_DISABLED_POST);
        httpd_register_uri_handler(server, &URI_LIGHT_RGB_DISABLED);
        httpd_register_uri_handler(server, &URI_LIGHT_RGB_TEST_DISABLED);
        httpd_register_uri_handler(server, &URI_LIGHT_DIGITAL_TEST_DISABLED);
        httpd_register_uri_handler(server, &URI_LIGHT_DIGITAL_CHASE_DISABLED);
        httpd_register_uri_handler(server, &URI_LIGHT_DIGITAL_WIPE_DISABLED);
        httpd_register_uri_handler(server, &URI_LIGHT_DIGITAL_PULSE_DISABLED);
        httpd_register_uri_handler(server, &URI_LIGHT_DIGITAL_RAINBOW_DISABLED);
        httpd_register_uri_handler(server, &URI_LIGHT_PRESET_DISABLED);
        httpd_register_uri_handler(server, &URI_LIGHT_PRESET_DISABLED_POST);
#endif
        // Absorb legacy tray/curtains polls from older UIs
        httpd_register_uri_handler(server, &URI_TRAY_STATUS_DISABLED);
        httpd_register_uri_handler(server, &URI_CURTAIN_STATUS_DISABLED);
        httpd_register_uri_handler(server, &URI_OTA);
        httpd_register_uri_handler(server, &URI_LOG);
        httpd_register_uri_handler(server, &URI_LOG_SETTINGS);
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

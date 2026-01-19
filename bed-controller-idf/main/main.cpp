#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "NetworkManager.h"
#ifdef CONFIG_APP_ENABLE_MATTER
#include "MatterManager.h"
#endif
#include "BoardConfig.h"
#include "driver/gpio.h"
#include "driver/ledc.h"
#include "driver/rmt_encoder.h"
#include "driver/rmt_tx.h"
#include "esp_adc/adc_oneshot.h"
#include "esp_adc/adc_cali.h"
#include "esp_adc/adc_cali_scheme.h"
#include "esp_log.h"
#include <math.h>
#include "esp_flash.h"
#include "esp_timer.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_spiffs.h"
#include "nvs_flash.h"
#include "nvs.h"
#include <ctime>
#include <string>
#include <inttypes.h>
#include <sys/cdefs.h>
#include <cstdio>
#include <unistd.h>

#if APP_ROLE_BED
#include "BedControl.h"
#include "BedDriver.h"
#include "BedService.h"

BedControl bed;
BedDriver* bedDriver = &bed;
#endif
NetworkManager net;

static const char* TAG_MAIN = "MAIN";
static bool s_dualOtaEnabled = false;
static const size_t kLogMinFreeBytes = 128 * 1024;
static vprintf_like_t s_log_prev_vprintf = nullptr;
static std::string s_log_buffer;
static size_t s_log_pending = 0;
static int s_log_day = -1;
static int64_t s_log_last_flush_us = 0;
static uint32_t s_log_dropped_queue = 0;
static uint32_t s_log_dropped_full = 0;
static const size_t kLogChunkSize = 8192;
static const size_t kLogChunksPerDay = 8;
static const size_t kLogMaxLen = kLogChunkSize * kLogChunksPerDay;
static const char *kLogBasePath = "/spiffs";
static const char *kLogPartitionLabel = "storage";
static bool s_log_spiffs_ready = false;
static const size_t kLogFlushThreshold = 512;
static const int64_t kLogFlushIntervalUs = 5 * 1000 * 1000;
static const size_t kLogLineMax = 192;
static const size_t kLogQueueDepth = 64;
static QueueHandle_t s_log_queue = nullptr;
static SemaphoreHandle_t s_log_mutex = nullptr;
struct LogItem {
    uint16_t len;
    char msg[kLogLineMax];
};

static bool log_is_digit(char c) {
    return c >= '0' && c <= '9';
}

static size_t log_strip_leading_timestamp(const char *buf, size_t len) {
    if (!buf || len < 4 || buf[0] != '[') return 0;
    if (len >= 21 &&
        log_is_digit(buf[1]) && log_is_digit(buf[2]) && log_is_digit(buf[3]) && log_is_digit(buf[4]) &&
        buf[5] == '-' &&
        log_is_digit(buf[6]) && log_is_digit(buf[7]) &&
        buf[8] == '-' &&
        log_is_digit(buf[9]) && log_is_digit(buf[10]) &&
        buf[11] == ' ' &&
        log_is_digit(buf[12]) && log_is_digit(buf[13]) &&
        buf[14] == ':' &&
        log_is_digit(buf[15]) && log_is_digit(buf[16]) &&
        buf[17] == ':' &&
        log_is_digit(buf[18]) && log_is_digit(buf[19]) &&
        buf[20] == ']') {
        size_t end = 21;
        if (end < len && buf[end] == ' ') {
            end++;
        }
        return end;
    }
    if (len >= 6 && buf[1] == '+') {
        size_t idx = 2;
        while (idx < len && log_is_digit(buf[idx])) {
            idx++;
        }
        if (idx > 2 && (idx + 2) < len && buf[idx] == 'm' && buf[idx + 1] == 's' && buf[idx + 2] == ']') {
            size_t end = idx + 3;
            if (end < len && buf[end] == ' ') {
                end++;
            }
            return end;
        }
    }
    return 0;
}

static size_t log_sanitize_line(const char *in, size_t len, char *out, size_t out_len) {
    if (!in || !out || out_len == 0) return 0;
    size_t w = 0;
    for (size_t i = 0; i < len; ) {
        unsigned char c = static_cast<unsigned char>(in[i]);
        if (c == 0x1b && (i + 1) < len && in[i + 1] == '[') {
            i += 2;
            while (i < len) {
                unsigned char end = static_cast<unsigned char>(in[i]);
                if (end >= '@' && end <= '~') {
                    i++;
                    break;
                }
                i++;
            }
            continue;
        }
        if (w + 1 < out_len) {
            out[w++] = in[i];
        }
        i++;
    }
    out[w] = '\0';
    size_t offset = log_strip_leading_timestamp(out, w);
    if (offset > 0) {
        if (offset >= w) {
            w = 0;
            out[0] = '\0';
        } else {
            memmove(out, out + offset, w - offset);
            w -= offset;
            out[w] = '\0';
        }
    }
    return w;
}

#ifdef CONFIG_APP_ENABLE_MATTER
#define APP_MATTER 1
#else
#define APP_MATTER 0
#endif

// LED channels match BedControl
#define LEDC_MODE               LEDC_LOW_SPEED_MODE
#define LEDC_TIMER              LEDC_TIMER_0
#define LEDC_DUTY_RES           LEDC_TIMER_8_BIT
#define LEDC_FREQUENCY          5000
#define LEDC_CHANNEL_R          LEDC_CHANNEL_0
#define LEDC_CHANNEL_G          LEDC_CHANNEL_1
#define LEDC_CHANNEL_B          LEDC_CHANNEL_2

enum class LedState {
    IDLE,          // unprovisioned / not commissioned
    COMMISSIONING, // commissioning in progress
    COMMISSIONED,  // provisioned/connected
    RESETTING
};

static LedState g_led_state = LedState::IDLE;
struct LedOverride {
    bool active = false;
    bool persistent = false;
    uint64_t expiry_us = 0;
    uint8_t r = 0, g = 0, b = 0;
};
static LedOverride s_led_override;
static rmt_channel_handle_t s_addressable_led_chan = nullptr;
static rmt_encoder_handle_t s_addressable_led_encoder = nullptr;
static bool s_addressable_led_ready = false;
static bool s_addressable_led_grb = ADDRESSABLE_LED_GRB;
static volatile bool s_addressable_led_abort = false;
static volatile uint32_t s_addressable_led_epoch = 0;
static volatile bool s_addressable_led_effect_active = false;
static uint8_t s_status_pixel_r = 0;
static uint8_t s_status_pixel_g = 0;
static uint8_t s_status_pixel_b = 0;
static SemaphoreHandle_t s_addressable_led_mutex = nullptr;
static const TickType_t kAddressableLedWaitTicks = pdMS_TO_TICKS(1000);
#if APP_ROLE_BED && CONFIG_IDF_TARGET_ESP32S3
static adc_oneshot_unit_handle_t s_acs_adc = nullptr;
static adc_cali_handle_t s_acs_cali = nullptr;
static bool s_acs_cali_ready = false;
#endif

typedef struct {
    rmt_encoder_t base;
    rmt_encoder_t* bytes_encoder;
    rmt_encoder_t* copy_encoder;
    int state;
    rmt_symbol_word_t reset_code;
} rmt_led_strip_encoder_t;

static bool log_time_valid(time_t now) {
    return now > 1600000000;
}

static inline bool addressable_led_should_abort() {
    return s_addressable_led_abort;
}

static inline uint32_t addressable_led_effect_epoch() {
    return s_addressable_led_epoch;
}

static inline bool addressable_led_epoch_changed(uint32_t epoch) {
    return s_addressable_led_epoch != epoch;
}

static int log_day_index() {
    time_t now = time(nullptr);
    if (!log_time_valid(now)) return -1;
    struct tm info = {};
    localtime_r(&now, &info);
    return info.tm_wday;
}

static void log_path_for_chunk(int day, int chunk, char *out, size_t out_len) {
    if (!out || out_len < 16) {
        if (out && out_len > 0) out[0] = '\0';
        return;
    }
    int idx = (day >= 0 && day <= 6) ? day : 0;
    int chunk_idx = (chunk >= 0) ? chunk : 0;
    snprintf(out, out_len, "%s/log_d%d_%d.txt", kLogBasePath, idx, chunk_idx);
}

static void log_spiffs_init() {
    if (s_log_spiffs_ready) return;
    esp_vfs_spiffs_conf_t conf = {};
    conf.base_path = kLogBasePath;
    conf.partition_label = kLogPartitionLabel;
    conf.max_files = 8;
    conf.format_if_mount_failed = false;
    esp_err_t err = esp_vfs_spiffs_register(&conf);
    if (err != ESP_OK) {
        ESP_LOGW(TAG_MAIN, "SPIFFS mount failed for logs: %s", esp_err_to_name(err));
        return;
    }
    s_log_spiffs_ready = true;
}

static bool log_spiffs_low_space(size_t *free_bytes_out = nullptr) {
    if (!s_log_spiffs_ready) return false;
    size_t total = 0;
    size_t used = 0;
    esp_err_t err = esp_spiffs_info(kLogPartitionLabel, &total, &used);
    if (err != ESP_OK || total <= used) {
        return false;
    }
    size_t free_bytes = total - used;
    if (free_bytes_out) {
        *free_bytes_out = free_bytes;
    }
    return free_bytes < kLogMinFreeBytes;
}

static bool log_store_clear_all_internal() {
    if (!s_log_spiffs_ready) return false;
    for (int day = 0; day < 7; ++day) {
        for (size_t i = 0; i < kLogChunksPerDay; ++i) {
            char path[40];
            log_path_for_chunk(day, static_cast<int>(i), path, sizeof(path));
            unlink(path);
        }
    }
    s_log_buffer.clear();
    s_log_pending = 0;
    int day = log_day_index();
    if (day < 0) day = 0;
    s_log_day = day;
    s_log_last_flush_us = 0;
    return true;
}

extern "C" bool log_store_clear_all() {
    if (s_log_mutex) xSemaphoreTake(s_log_mutex, portMAX_DELAY);
    bool ok = log_store_clear_all_internal();
    if (s_log_mutex) xSemaphoreGive(s_log_mutex);
    return ok;
}

extern "C" bool log_store_cleanup_if_low() {
    if (!s_log_spiffs_ready) {
        log_spiffs_init();
    }
    size_t free_bytes = 0;
    if (!log_spiffs_low_space(&free_bytes)) {
        return false;
    }
    ESP_LOGW(TAG_MAIN, "SPIFFS low on free bytes (%zu); clearing syslog", free_bytes);
    if (s_log_mutex) xSemaphoreTake(s_log_mutex, portMAX_DELAY);
    bool ok = log_store_clear_all_internal();
    if (s_log_mutex) xSemaphoreGive(s_log_mutex);
    return ok;
}

static void log_store_load_day(int day) {
    if (day < 0) return;
    if (!s_log_spiffs_ready) return;
    std::string combined;
    combined.reserve(kLogMaxLen);
    for (size_t i = 0; i < kLogChunksPerDay; ++i) {
        char path[40];
        log_path_for_chunk(day, static_cast<int>(i), path, sizeof(path));
        FILE *f = fopen(path, "rb");
        if (!f) {
            break;
        }
        char buf[256];
        size_t read_len = 0;
        while ((read_len = fread(buf, 1, sizeof(buf), f)) > 0) {
            if (combined.size() + read_len > kLogMaxLen) {
                size_t space = kLogMaxLen - combined.size();
                combined.append(buf, space);
                fclose(f);
                s_log_buffer = combined;
                return;
            }
            combined.append(buf, read_len);
        }
        fclose(f);
    }
    s_log_buffer = combined;
}

static void log_store_reset_day(int day) {
    if (!s_log_spiffs_ready) return;
    for (size_t i = 0; i < kLogChunksPerDay; ++i) {
        char path[40];
        log_path_for_chunk(day, static_cast<int>(i), path, sizeof(path));
        unlink(path);
    }
    s_log_buffer.clear();
    s_log_pending = 0;
    s_log_day = day;
    s_log_last_flush_us = 0;
}

static void log_store_flush_locked() {
    if (s_log_pending == 0 || s_log_day < 0) return;
    if (!s_log_spiffs_ready) return;
    if (log_spiffs_low_space()) {
        log_store_clear_all_internal();
    }
    size_t total = s_log_buffer.size();
    size_t offset = 0;
    size_t used_chunks = 0;
    while (offset < total && used_chunks < kLogChunksPerDay) {
        size_t chunk_len = total - offset;
        if (chunk_len > kLogChunkSize) {
            chunk_len = kLogChunkSize;
        }
        std::string chunk = s_log_buffer.substr(offset, chunk_len);
        char path[40];
        log_path_for_chunk(s_log_day, static_cast<int>(used_chunks), path, sizeof(path));
        FILE *f = fopen(path, "wb");
        if (!f) {
            break;
        }
        fwrite(chunk.data(), 1, chunk.size(), f);
        fclose(f);
        offset += chunk_len;
        used_chunks++;
    }
    for (size_t i = used_chunks; i < kLogChunksPerDay; ++i) {
        char path[40];
        log_path_for_chunk(s_log_day, static_cast<int>(i), path, sizeof(path));
        unlink(path);
    }
    s_log_pending = 0;
    s_log_last_flush_us = esp_timer_get_time();
}

static void log_store_append(const char *text, size_t len) {
    if (!text || len == 0) return;
    if (!s_log_spiffs_ready) return;
    if (log_spiffs_low_space()) {
        s_log_dropped_full++;
        return;
    }
    int day = log_day_index();
    if (day < 0) {
        day = (s_log_day >= 0) ? s_log_day : 0;
    }
    if (day != s_log_day) {
        log_store_reset_day(day);
    }
    if (s_log_buffer.size() + len > kLogMaxLen) {
        size_t trim = (s_log_buffer.size() + len) - kLogMaxLen;
        if (trim >= s_log_buffer.size()) {
            s_log_buffer.clear();
        } else {
            s_log_buffer.erase(0, trim);
        }
    }
    s_log_buffer.append(text, len);
    s_log_pending += len;
    int64_t now_us = esp_timer_get_time();
    if (s_log_pending >= kLogFlushThreshold ||
        (s_log_last_flush_us > 0 && (now_us - s_log_last_flush_us) >= kLogFlushIntervalUs)) {
        log_store_flush_locked();
    }
}

extern "C" uint32_t log_get_dropped_queue() {
    return s_log_dropped_queue;
}

extern "C" uint32_t log_get_dropped_full() {
    return s_log_dropped_full;
}

extern "C" size_t log_get_buffer_size() {
    return s_log_buffer.size();
}

extern "C" size_t log_get_max_size() {
    return kLogMaxLen;
}

extern "C" size_t log_get_chunk_size() {
    return kLogChunkSize;
}

extern "C" size_t log_get_chunks_per_day() {
    return kLogChunksPerDay;
}

static int log_vprintf(const char *fmt, va_list ap) {
    va_list ap_copy;
    va_copy(ap_copy, ap);
    int ret = s_log_prev_vprintf ? s_log_prev_vprintf(fmt, ap) : vprintf(fmt, ap);
    if (s_log_queue) {
        if (xPortInIsrContext()) {
            va_end(ap_copy);
            return ret;
        }
        const char *task_name = pcTaskGetName(nullptr);
        if (task_name && strcmp(task_name, "sys_evt") == 0) {
            va_end(ap_copy);
            return ret;
        }
        LogItem item = {};
        int len = vsnprintf(item.msg, sizeof(item.msg), fmt, ap_copy);
        if (len > 0) {
            size_t capped = (len > (int)(sizeof(item.msg) - 1)) ? (sizeof(item.msg) - 1) : (size_t)len;
            item.len = static_cast<uint16_t>(capped);
            if (xQueueSend(s_log_queue, &item, 0) != pdTRUE) {
                s_log_dropped_queue++;
            }
        }
    }
    va_end(ap_copy);
    return ret;
}

static void log_store_task(void *pv) {
    LogItem item = {};
    while (1) {
        while (s_log_queue && xQueueReceive(s_log_queue, &item, pdMS_TO_TICKS(200)) == pdTRUE) {
            if (item.len == 0) continue;
            char clean[kLogLineMax];
            size_t clean_len = log_sanitize_line(item.msg, item.len, clean, sizeof(clean));
            if (clean_len == 0) continue;
            char stamp[32];
            time_t now = time(nullptr);
            if (log_time_valid(now)) {
                struct tm info = {};
                localtime_r(&now, &info);
                strftime(stamp, sizeof(stamp), "[%Y-%m-%d %H:%M:%S] ", &info);
            } else {
                int64_t ms = esp_timer_get_time() / 1000;
                snprintf(stamp, sizeof(stamp), "[+%lldms] ", (long long)ms);
            }
            char buf[256];
            int prefix_len = snprintf(buf, sizeof(buf), "%s", stamp);
            size_t space = (prefix_len > 0 && (size_t)prefix_len < sizeof(buf)) ? (sizeof(buf) - (size_t)prefix_len - 1) : 0;
            size_t copy_len = (clean_len < space) ? clean_len : space;
            if (prefix_len > 0 && copy_len > 0) {
                memcpy(buf + prefix_len, clean, copy_len);
                buf[prefix_len + copy_len] = '\0';
                if (s_log_mutex) xSemaphoreTake(s_log_mutex, portMAX_DELAY);
                log_store_append(buf, prefix_len + copy_len);
                if (s_log_mutex) xSemaphoreGive(s_log_mutex);
            }
        }
        if (s_log_mutex) xSemaphoreTake(s_log_mutex, portMAX_DELAY);
        log_store_flush_locked();
        if (s_log_mutex) xSemaphoreGive(s_log_mutex);
    }
}

IRAM_ATTR static size_t rmt_encode_led_strip(rmt_encoder_t* encoder,
                                             rmt_channel_handle_t channel,
                                             const void* primary_data,
                                             size_t data_size,
                                             rmt_encode_state_t* ret_state) {
    rmt_led_strip_encoder_t* led_encoder = __containerof(encoder, rmt_led_strip_encoder_t, base);
    rmt_encode_state_t session_state = RMT_ENCODING_RESET;
    uint32_t state_flags = 0;
    size_t encoded_symbols = 0;
    switch (led_encoder->state) {
    case 0:
        encoded_symbols += led_encoder->bytes_encoder->encode(
            led_encoder->bytes_encoder, channel, primary_data, data_size, &session_state);
        if (session_state & RMT_ENCODING_COMPLETE) {
            led_encoder->state = 1;
        }
        if (session_state & RMT_ENCODING_MEM_FULL) {
            state_flags |= static_cast<uint32_t>(RMT_ENCODING_MEM_FULL);
            goto out;
        }
        // fall-through
    case 1:
        encoded_symbols += led_encoder->copy_encoder->encode(
            led_encoder->copy_encoder, channel, &led_encoder->reset_code,
            sizeof(led_encoder->reset_code), &session_state);
        if (session_state & RMT_ENCODING_COMPLETE) {
            state_flags |= static_cast<uint32_t>(RMT_ENCODING_COMPLETE);
            led_encoder->state = RMT_ENCODING_RESET;
        }
        if (session_state & RMT_ENCODING_MEM_FULL) {
            state_flags |= static_cast<uint32_t>(RMT_ENCODING_MEM_FULL);
            goto out;
        }
    }
out:
    *ret_state = static_cast<rmt_encode_state_t>(state_flags);
    return encoded_symbols;
}

static esp_err_t rmt_del_led_strip_encoder(rmt_encoder_t* encoder) {
    rmt_led_strip_encoder_t* led_encoder = __containerof(encoder, rmt_led_strip_encoder_t, base);
    rmt_del_encoder(led_encoder->bytes_encoder);
    rmt_del_encoder(led_encoder->copy_encoder);
    free(led_encoder);
    return ESP_OK;
}

static esp_err_t rmt_led_strip_encoder_reset(rmt_encoder_t* encoder) {
    rmt_led_strip_encoder_t* led_encoder = __containerof(encoder, rmt_led_strip_encoder_t, base);
    rmt_encoder_reset(led_encoder->bytes_encoder);
    rmt_encoder_reset(led_encoder->copy_encoder);
    led_encoder->state = RMT_ENCODING_RESET;
    return ESP_OK;
}

static esp_err_t rmt_new_led_strip_encoder(rmt_encoder_handle_t* ret_encoder) {
    rmt_led_strip_encoder_t* led_encoder =
        static_cast<rmt_led_strip_encoder_t*>(rmt_alloc_encoder_mem(sizeof(rmt_led_strip_encoder_t)));
    if (!led_encoder) return ESP_ERR_NO_MEM;
    led_encoder->base.encode = rmt_encode_led_strip;
    led_encoder->base.del = rmt_del_led_strip_encoder;
    led_encoder->base.reset = rmt_led_strip_encoder_reset;
    // WS2812 timing with 10MHz resolution: T0H=0.3us, T0L=0.9us, T1H=0.9us, T1L=0.3us
    rmt_bytes_encoder_config_t bytes_encoder_config = {
        .bit0 = {
            .duration0 = 3,
            .level0 = 1,
            .duration1 = 9,
            .level1 = 0,
        },
        .bit1 = {
            .duration0 = 9,
            .level0 = 1,
            .duration1 = 3,
            .level1 = 0,
        },
    };
    bytes_encoder_config.flags.msb_first = 1;
    esp_err_t err = rmt_new_bytes_encoder(&bytes_encoder_config, &led_encoder->bytes_encoder);
    if (err != ESP_OK) {
        free(led_encoder);
        return err;
    }
    rmt_copy_encoder_config_t copy_encoder_config = {};
    err = rmt_new_copy_encoder(&copy_encoder_config, &led_encoder->copy_encoder);
    if (err != ESP_OK) {
        rmt_del_encoder(led_encoder->bytes_encoder);
        free(led_encoder);
        return err;
    }
    led_encoder->reset_code = (rmt_symbol_word_t){
        .duration0 = 250,
        .level0 = 0,
        .duration1 = 250,
        .level1 = 0,
    };
    *ret_encoder = &led_encoder->base;
    return ESP_OK;
}

static void init_addressable_led() {
    rmt_tx_channel_config_t tx_chan_config = {
        .gpio_num = static_cast<gpio_num_t>(ADDRESSABLE_LED_GPIO),
        .clk_src = RMT_CLK_SRC_DEFAULT,
        .resolution_hz = 10 * 1000 * 1000,
        .mem_block_symbols = 64,
        .trans_queue_depth = 4,
        .flags = { .invert_out = false, .with_dma = false }
    };
    esp_err_t err = rmt_new_tx_channel(&tx_chan_config, &s_addressable_led_chan);
    if (err != ESP_OK) {
        ESP_LOGW(TAG_MAIN, "Addressable LED channel init failed on GPIO %d: %s", ADDRESSABLE_LED_GPIO, esp_err_to_name(err));
        return;
    }
    err = rmt_new_led_strip_encoder(&s_addressable_led_encoder);
    if (err != ESP_OK) {
        ESP_LOGW(TAG_MAIN, "Addressable LED encoder init failed: %s", esp_err_to_name(err));
        return;
    }
    err = rmt_enable(s_addressable_led_chan);
    if (err != ESP_OK) {
        ESP_LOGW(TAG_MAIN, "Addressable LED channel enable failed: %s", esp_err_to_name(err));
        return;
    }
    if (!s_addressable_led_mutex) {
        s_addressable_led_mutex = xSemaphoreCreateMutex();
    }
    s_addressable_led_ready = true;
    ESP_LOGI(TAG_MAIN, "Addressable LED initialized on GPIO %d (%s order)",
             ADDRESSABLE_LED_GPIO, s_addressable_led_grb ? "GRB" : "RGB");
    uint8_t off[3] = {0, 0, 0};
    rmt_transmit_config_t tx_cfg = {.loop_count = 0};
    if (!s_addressable_led_mutex || xSemaphoreTake(s_addressable_led_mutex, kAddressableLedWaitTicks) == pdTRUE) {
        rmt_transmit(s_addressable_led_chan, s_addressable_led_encoder, off, sizeof(off), &tx_cfg);
        rmt_tx_wait_all_done(s_addressable_led_chan, kAddressableLedWaitTicks);
        if (s_addressable_led_mutex) xSemaphoreGive(s_addressable_led_mutex);
    }
}

static inline void addressable_led_write_pixel(uint8_t* payload, size_t offset, uint8_t r, uint8_t g, uint8_t b) {
    if (s_addressable_led_grb) {
        payload[offset] = g;
        payload[offset + 1] = r;
        payload[offset + 2] = b;
    } else {
        payload[offset] = r;
        payload[offset + 1] = g;
        payload[offset + 2] = b;
    }
}

static bool addressable_led_transmit_blocking(const uint8_t *payload, size_t len) {
    rmt_transmit_config_t tx_cfg = {.loop_count = 0};
    esp_err_t err = rmt_transmit(s_addressable_led_chan, s_addressable_led_encoder, payload, len, &tx_cfg);
    if (err != ESP_OK) {
        ESP_LOGW(TAG_MAIN, "Addressable LED transmit failed: %s", esp_err_to_name(err));
        return false;
    }
    err = rmt_tx_wait_all_done(s_addressable_led_chan, kAddressableLedWaitTicks);
    if (err != ESP_OK) {
        ESP_LOGW(TAG_MAIN, "Addressable LED transmit timeout: %s", esp_err_to_name(err));
        return false;
    }
    return true;
}

static void set_addressable_led(uint8_t r, uint8_t g, uint8_t b) {
    static bool s_logged_not_ready = false;
    if (!s_addressable_led_ready) {
        if (!s_logged_not_ready) {
            ESP_LOGW(TAG_MAIN, "Addressable LED not ready; skipping updates");
            s_logged_not_ready = true;
        }
        return;
    }
    uint8_t payload[3] = {0, 0, 0};
    addressable_led_write_pixel(payload, 0, r, g, b);
    if (!s_addressable_led_mutex || xSemaphoreTake(s_addressable_led_mutex, kAddressableLedWaitTicks) == pdTRUE) {
        addressable_led_transmit_blocking(payload, sizeof(payload));
        if (s_addressable_led_mutex) xSemaphoreGive(s_addressable_led_mutex);
    }
}

extern "C" void addressable_led_set_order(bool grb) {
    s_addressable_led_grb = grb;
    ESP_LOGI(TAG_MAIN, "Addressable LED order set to %s", grb ? "GRB" : "RGB");
    set_addressable_led(s_status_pixel_r, s_status_pixel_g, s_status_pixel_b);
}

extern "C" void addressable_led_set_abort(bool abort) {
    s_addressable_led_abort = abort;
}

extern "C" void addressable_led_set_effect_active(bool active) {
    s_addressable_led_effect_active = active;
}

extern "C" uint32_t addressable_led_bump_epoch() {
    return ++s_addressable_led_epoch;
}

extern "C" uint32_t addressable_led_get_epoch() {
    return s_addressable_led_epoch;
}

extern "C" bool addressable_led_fill_strip(uint8_t r, uint8_t g, uint8_t b, uint16_t count) {
    if (!s_addressable_led_ready) {
        ESP_LOGW(TAG_MAIN, "Addressable LED not ready; strip update skipped");
        return false;
    }
    size_t total_pixels = static_cast<size_t>(count) + 1; // pixel 0 is status
    size_t buf_len = total_pixels * 3;
    uint8_t* payload = static_cast<uint8_t*>(malloc(buf_len));
    if (!payload) {
        ESP_LOGW(TAG_MAIN, "Addressable strip alloc failed (%u px)", (unsigned)total_pixels);
        return false;
    }
    auto write_pixel = [&](size_t idx, uint8_t pr, uint8_t pg, uint8_t pb) {
        addressable_led_write_pixel(payload, idx * 3, pr, pg, pb);
    };
    write_pixel(0, s_status_pixel_r, s_status_pixel_g, s_status_pixel_b);
    for (size_t i = 1; i < total_pixels; i++) {
        write_pixel(i, r, g, b);
    }
    if (s_addressable_led_mutex && xSemaphoreTake(s_addressable_led_mutex, kAddressableLedWaitTicks) != pdTRUE) {
        free(payload);
        return false;
    }
    if (!addressable_led_transmit_blocking(payload, buf_len)) {
        if (s_addressable_led_mutex) xSemaphoreGive(s_addressable_led_mutex);
        free(payload);
        return false;
    }
    if (s_addressable_led_mutex) xSemaphoreGive(s_addressable_led_mutex);
    free(payload);
    return true;
}

static bool addressable_led_chase_impl(uint8_t r, uint8_t g, uint8_t b, uint16_t count, uint16_t steps, uint16_t delay_ms, bool reverse) {
    if (!s_addressable_led_ready) {
        ESP_LOGW(TAG_MAIN, "Addressable LED not ready; chase skipped");
        return false;
    }
    if (count == 0 || steps == 0) {
        return false;
    }
    size_t total_pixels = static_cast<size_t>(count) + 1;
    size_t buf_len = total_pixels * 3;
    uint8_t* payload = static_cast<uint8_t*>(malloc(buf_len));
    if (!payload) {
        ESP_LOGW(TAG_MAIN, "Addressable chase alloc failed (%u px)", (unsigned)total_pixels);
        return false;
    }
    auto write_pixel = [&](size_t idx, uint8_t pr, uint8_t pg, uint8_t pb) {
        addressable_led_write_pixel(payload, idx * 3, pr, pg, pb);
    };
    if (s_addressable_led_mutex && xSemaphoreTake(s_addressable_led_mutex, kAddressableLedWaitTicks) != pdTRUE) {
        free(payload);
        return false;
    }
    size_t active_count = total_pixels - 1;
    uint32_t epoch = addressable_led_effect_epoch();
    bool aborted = false;
    for (uint16_t step = 0; step < steps; ++step) {
        if (addressable_led_should_abort() || addressable_led_epoch_changed(epoch)) {
            aborted = true;
            break;
        }
        size_t offset = (step % active_count);
        size_t lit = reverse ? (active_count - offset) : (1 + offset);
        write_pixel(0, s_status_pixel_r, s_status_pixel_g, s_status_pixel_b);
        for (size_t i = 1; i < total_pixels; i++) {
            if (i == lit) {
                write_pixel(i, r, g, b);
            } else {
                write_pixel(i, 0, 0, 0);
            }
        }
        if (!addressable_led_transmit_blocking(payload, buf_len)) {
            if (s_addressable_led_mutex) xSemaphoreGive(s_addressable_led_mutex);
            free(payload);
            return false;
        }
        if (delay_ms > 0) {
            vTaskDelay(pdMS_TO_TICKS(delay_ms));
            if (addressable_led_should_abort() || addressable_led_epoch_changed(epoch)) {
                aborted = true;
                break;
            }
        }
    }
    if (s_addressable_led_mutex) xSemaphoreGive(s_addressable_led_mutex);
    free(payload);
    return !aborted;
}

extern "C" bool addressable_led_chase(uint8_t r, uint8_t g, uint8_t b, uint16_t count, uint16_t steps, uint16_t delay_ms) {
    return addressable_led_chase_impl(r, g, b, count, steps, delay_ms, false);
}

extern "C" bool addressable_led_chase_dir(uint8_t r, uint8_t g, uint8_t b, uint16_t count, uint16_t steps, uint16_t delay_ms, bool reverse) {
    return addressable_led_chase_impl(r, g, b, count, steps, delay_ms, reverse);
}

static bool addressable_led_wipe_impl(uint8_t r, uint8_t g, uint8_t b, uint16_t count, uint16_t delay_ms, bool reverse) {
    if (!s_addressable_led_ready) {
        ESP_LOGW(TAG_MAIN, "Addressable LED not ready; wipe skipped");
        return false;
    }
    if (count == 0) return false;
    size_t total_pixels = static_cast<size_t>(count) + 1;
    size_t buf_len = total_pixels * 3;
    uint8_t* payload = static_cast<uint8_t*>(malloc(buf_len));
    if (!payload) {
        ESP_LOGW(TAG_MAIN, "Addressable wipe alloc failed (%u px)", (unsigned)total_pixels);
        return false;
    }
    auto write_pixel = [&](size_t idx, uint8_t pr, uint8_t pg, uint8_t pb) {
        addressable_led_write_pixel(payload, idx * 3, pr, pg, pb);
    };
    if (s_addressable_led_mutex && xSemaphoreTake(s_addressable_led_mutex, kAddressableLedWaitTicks) != pdTRUE) {
        free(payload);
        return false;
    }
    uint32_t epoch = addressable_led_effect_epoch();
    bool aborted = false;
    for (size_t lit = 1; lit < total_pixels; ++lit) {
        if (addressable_led_should_abort() || addressable_led_epoch_changed(epoch)) {
            aborted = true;
            break;
        }
        write_pixel(0, s_status_pixel_r, s_status_pixel_g, s_status_pixel_b);
        for (size_t i = 1; i < total_pixels; i++) {
            bool on = reverse ? (i >= (total_pixels - lit)) : (i <= lit);
            if (on) {
                write_pixel(i, r, g, b);
            } else {
                write_pixel(i, 0, 0, 0);
            }
        }
        if (!addressable_led_transmit_blocking(payload, buf_len)) {
            if (s_addressable_led_mutex) xSemaphoreGive(s_addressable_led_mutex);
            free(payload);
            return false;
        }
        if (delay_ms > 0) {
            vTaskDelay(pdMS_TO_TICKS(delay_ms));
            if (addressable_led_should_abort() || addressable_led_epoch_changed(epoch)) {
                aborted = true;
                break;
            }
        }
    }
    if (s_addressable_led_mutex) xSemaphoreGive(s_addressable_led_mutex);
    free(payload);
    return !aborted;
}

extern "C" bool addressable_led_wipe(uint8_t r, uint8_t g, uint8_t b, uint16_t count, uint16_t delay_ms) {
    return addressable_led_wipe_impl(r, g, b, count, delay_ms, false);
}

extern "C" bool addressable_led_wipe_dir(uint8_t r, uint8_t g, uint8_t b, uint16_t count, uint16_t delay_ms, bool reverse) {
    return addressable_led_wipe_impl(r, g, b, count, delay_ms, reverse);
}

extern "C" bool addressable_led_pulse(uint8_t r, uint8_t g, uint8_t b, uint16_t count, uint16_t steps, uint16_t delay_ms) {
    if (!s_addressable_led_ready) {
        ESP_LOGW(TAG_MAIN, "Addressable LED not ready; pulse skipped");
        return false;
    }
    if (count == 0 || steps == 0) return false;
    size_t total_pixels = static_cast<size_t>(count) + 1;
    size_t buf_len = total_pixels * 3;
    uint8_t* payload = static_cast<uint8_t*>(malloc(buf_len));
    if (!payload) {
        ESP_LOGW(TAG_MAIN, "Addressable pulse alloc failed (%u px)", (unsigned)total_pixels);
        return false;
    }
    auto write_pixel = [&](size_t idx, uint8_t pr, uint8_t pg, uint8_t pb) {
        addressable_led_write_pixel(payload, idx * 3, pr, pg, pb);
    };
    if (s_addressable_led_mutex && xSemaphoreTake(s_addressable_led_mutex, kAddressableLedWaitTicks) != pdTRUE) {
        free(payload);
        return false;
    }
    uint16_t half = steps / 2;
    if (half == 0) half = 1;
    uint32_t epoch = addressable_led_effect_epoch();
    bool aborted = false;
    for (uint16_t step = 0; step < steps; ++step) {
        if (addressable_led_should_abort() || addressable_led_epoch_changed(epoch)) {
            aborted = true;
            break;
        }
        uint16_t phase = (step <= half) ? step : (steps - 1 - step);
        uint32_t intensity = (static_cast<uint32_t>(phase) * 255u) / half;
        uint8_t pr = static_cast<uint8_t>((static_cast<uint32_t>(r) * intensity) / 255u);
        uint8_t pg = static_cast<uint8_t>((static_cast<uint32_t>(g) * intensity) / 255u);
        uint8_t pb = static_cast<uint8_t>((static_cast<uint32_t>(b) * intensity) / 255u);
        write_pixel(0, s_status_pixel_r, s_status_pixel_g, s_status_pixel_b);
        for (size_t i = 1; i < total_pixels; i++) {
            write_pixel(i, pr, pg, pb);
        }
        if (!addressable_led_transmit_blocking(payload, buf_len)) {
            if (s_addressable_led_mutex) xSemaphoreGive(s_addressable_led_mutex);
            free(payload);
            return false;
        }
        if (delay_ms > 0) {
            vTaskDelay(pdMS_TO_TICKS(delay_ms));
            if (addressable_led_should_abort() || addressable_led_epoch_changed(epoch)) {
                aborted = true;
                break;
            }
        }
    }
    if (s_addressable_led_mutex) xSemaphoreGive(s_addressable_led_mutex);
    free(payload);
    return !aborted;
}

static void hsv_to_rgb(uint8_t hue, uint8_t sat, uint8_t val, uint8_t *r, uint8_t *g, uint8_t *b) {
    if (sat == 0) {
        *r = val;
        *g = val;
        *b = val;
        return;
    }
    uint8_t region = hue / 43;
    uint8_t remainder = (hue - (region * 43)) * 6;
    uint8_t p = (val * (255 - sat)) >> 8;
    uint8_t q = (val * (255 - ((sat * remainder) >> 8))) >> 8;
    uint8_t t = (val * (255 - ((sat * (255 - remainder)) >> 8))) >> 8;
    switch (region) {
    case 0:
        *r = val; *g = t; *b = p;
        break;
    case 1:
        *r = q; *g = val; *b = p;
        break;
    case 2:
        *r = p; *g = val; *b = t;
        break;
    case 3:
        *r = p; *g = q; *b = val;
        break;
    case 4:
        *r = t; *g = p; *b = val;
        break;
    default:
        *r = val; *g = p; *b = q;
        break;
    }
}

static bool addressable_led_rainbow_impl(uint16_t count, uint16_t steps, uint16_t delay_ms, uint8_t brightness, bool reverse) {
    if (!s_addressable_led_ready) {
        ESP_LOGW(TAG_MAIN, "Addressable LED not ready; rainbow skipped");
        return false;
    }
    if (count == 0 || steps == 0) return false;
    size_t total_pixels = static_cast<size_t>(count) + 1;
    size_t buf_len = total_pixels * 3;
    uint8_t* payload = static_cast<uint8_t*>(malloc(buf_len));
    if (!payload) {
        ESP_LOGW(TAG_MAIN, "Addressable rainbow alloc failed (%u px)", (unsigned)total_pixels);
        return false;
    }
    auto write_pixel = [&](size_t idx, uint8_t pr, uint8_t pg, uint8_t pb) {
        addressable_led_write_pixel(payload, idx * 3, pr, pg, pb);
    };
    if (s_addressable_led_mutex && xSemaphoreTake(s_addressable_led_mutex, kAddressableLedWaitTicks) != pdTRUE) {
        free(payload);
        return false;
    }
    uint8_t val = static_cast<uint8_t>((static_cast<uint32_t>(brightness) * 255u) / 100u);
    size_t active_count = total_pixels - 1;
    uint32_t epoch = addressable_led_effect_epoch();
    bool aborted = false;
    for (uint16_t step = 0; step < steps; ++step) {
        if (addressable_led_should_abort() || addressable_led_epoch_changed(epoch)) {
            aborted = true;
            break;
        }
        uint8_t base_shift = static_cast<uint8_t>((static_cast<uint32_t>(step) * 255u) / steps);
        uint8_t shift = reverse ? static_cast<uint8_t>(255u - base_shift) : base_shift;
        write_pixel(0, s_status_pixel_r, s_status_pixel_g, s_status_pixel_b);
        for (size_t i = 1; i < total_pixels; ++i) {
            uint8_t hue = static_cast<uint8_t>((static_cast<uint32_t>(i - 1) * 255u) / active_count);
            hue = static_cast<uint8_t>(hue + shift);
            uint8_t pr = 0, pg = 0, pb = 0;
            hsv_to_rgb(hue, 255, val, &pr, &pg, &pb);
            write_pixel(i, pr, pg, pb);
        }
        if (!addressable_led_transmit_blocking(payload, buf_len)) {
            if (s_addressable_led_mutex) xSemaphoreGive(s_addressable_led_mutex);
            free(payload);
            return false;
        }
        if (delay_ms > 0) {
            vTaskDelay(pdMS_TO_TICKS(delay_ms));
            if (addressable_led_should_abort() || addressable_led_epoch_changed(epoch)) {
                aborted = true;
                break;
            }
        }
    }
    if (s_addressable_led_mutex) xSemaphoreGive(s_addressable_led_mutex);
    free(payload);
    return !aborted;
}

extern "C" bool addressable_led_rainbow(uint16_t count, uint16_t steps, uint16_t delay_ms, uint8_t brightness) {
    return addressable_led_rainbow_impl(count, steps, delay_ms, brightness, false);
}

extern "C" bool addressable_led_rainbow_dir(uint16_t count, uint16_t steps, uint16_t delay_ms, uint8_t brightness, bool reverse) {
    return addressable_led_rainbow_impl(count, steps, delay_ms, brightness, reverse);
}

extern "C" bool addressable_led_fill_palette(const uint8_t *colors, size_t color_count, uint16_t count) {
    if (!s_addressable_led_ready) {
        ESP_LOGW(TAG_MAIN, "Addressable LED not ready; palette skipped");
        return false;
    }
    if (!colors || color_count == 0 || count == 0) return false;
    size_t total_pixels = static_cast<size_t>(count) + 1;
    size_t buf_len = total_pixels * 3;
    uint8_t* payload = static_cast<uint8_t*>(malloc(buf_len));
    if (!payload) {
        ESP_LOGW(TAG_MAIN, "Addressable palette alloc failed (%u px)", (unsigned)total_pixels);
        return false;
    }
    auto write_pixel = [&](size_t idx, uint8_t pr, uint8_t pg, uint8_t pb) {
        addressable_led_write_pixel(payload, idx * 3, pr, pg, pb);
    };
    write_pixel(0, s_status_pixel_r, s_status_pixel_g, s_status_pixel_b);
    for (size_t i = 1; i < total_pixels; i++) {
        size_t color_idx = (i - 1) % color_count;
        const uint8_t *c = colors + (color_idx * 3);
        write_pixel(i, c[0], c[1], c[2]);
    }
    if (s_addressable_led_mutex && xSemaphoreTake(s_addressable_led_mutex, kAddressableLedWaitTicks) != pdTRUE) {
        free(payload);
        return false;
    }
    if (!addressable_led_transmit_blocking(payload, buf_len)) {
        if (s_addressable_led_mutex) xSemaphoreGive(s_addressable_led_mutex);
        free(payload);
        return false;
    }
    if (s_addressable_led_mutex) xSemaphoreGive(s_addressable_led_mutex);
    free(payload);
    return true;
}

static void init_status_led_hw() {
    ledc_timer_config_t ledc_timer = {
        .speed_mode       = LEDC_MODE,
        .duty_resolution  = LEDC_DUTY_RES,
        .timer_num        = LEDC_TIMER,
        .freq_hz          = LEDC_FREQUENCY,
        .clk_cfg          = LEDC_AUTO_CLK,
        .deconfigure      = false
    };
    esp_err_t err = ledc_timer_config(&ledc_timer);
    if (err != ESP_OK) {
        ESP_LOGE(TAG_MAIN, "LED timer config failed: %s", esp_err_to_name(err));
        return;
    }
    ledc_channel_config_t c0 = { .gpio_num = LED_PIN_R, .speed_mode = LEDC_MODE, .channel = LEDC_CHANNEL_R, .intr_type = LEDC_INTR_DISABLE, .timer_sel = LEDC_TIMER, .duty = 0, .hpoint = 0, .flags = {} };
    ledc_channel_config_t c1 = { .gpio_num = LED_PIN_G, .speed_mode = LEDC_MODE, .channel = LEDC_CHANNEL_G, .intr_type = LEDC_INTR_DISABLE, .timer_sel = LEDC_TIMER, .duty = 0, .hpoint = 0, .flags = {} };
    ledc_channel_config_t c2 = { .gpio_num = LED_PIN_B, .speed_mode = LEDC_MODE, .channel = LEDC_CHANNEL_B, .intr_type = LEDC_INTR_DISABLE, .timer_sel = LEDC_TIMER, .duty = 0, .hpoint = 0, .flags = {} };
    ledc_channel_config(&c0);
    ledc_channel_config(&c1);
    ledc_channel_config(&c2);
    ESP_LOGI(TAG_MAIN, "Status LED LEDC initialized");
    init_addressable_led();
}

#if APP_ROLE_BED && CONFIG_IDF_TARGET_ESP32S3
static void init_acs712_adc() {
    adc_oneshot_unit_init_cfg_t unit_cfg = {
        .unit_id = ADC_UNIT_1,
        .clk_src = ADC_RTC_CLK_SRC_DEFAULT,
        .ulp_mode = ADC_ULP_MODE_DISABLE
    };
    esp_err_t err = adc_oneshot_new_unit(&unit_cfg, &s_acs_adc);
    if (err != ESP_OK) {
        ESP_LOGW(TAG_MAIN, "ACS712 ADC unit init failed: %s", esp_err_to_name(err));
        return;
    }
    adc_oneshot_chan_cfg_t chan_cfg = {
        .atten = ADC_ATTEN_DB_11,
        .bitwidth = ADC_BITWIDTH_DEFAULT
    };
    err = adc_oneshot_config_channel(s_acs_adc, ADC_CHANNEL_1, &chan_cfg);
    if (err != ESP_OK) {
        ESP_LOGW(TAG_MAIN, "ACS712 ADC channel config failed: %s", esp_err_to_name(err));
        return;
    }
#if ADC_CALI_SCHEME_CURVE_FITTING_SUPPORTED
    adc_cali_curve_fitting_config_t cali_cfg = {
        .unit_id = ADC_UNIT_1,
        .chan = ADC_CHANNEL_1,
        .atten = ADC_ATTEN_DB_11,
        .bitwidth = ADC_BITWIDTH_DEFAULT
    };
    err = adc_cali_create_scheme_curve_fitting(&cali_cfg, &s_acs_cali);
    if (err == ESP_OK) {
        s_acs_cali_ready = true;
    }
#elif ADC_CALI_SCHEME_LINE_FITTING_SUPPORTED
    adc_cali_line_fitting_config_t cali_cfg = {
        .unit_id = ADC_UNIT_1,
        .chan = ADC_CHANNEL_1,
        .atten = ADC_ATTEN_DB_11,
        .bitwidth = ADC_BITWIDTH_DEFAULT
    };
    err = adc_cali_create_scheme_line_fitting(&cali_cfg, &s_acs_cali);
    if (err == ESP_OK) {
        s_acs_cali_ready = true;
    }
#endif
    ESP_LOGI(TAG_MAIN, "ACS712 ADC ready on GPIO2 (ADC1_CH1)%s",
             s_acs_cali_ready ? " with calibration" : "");
}

static void acs712_log_task(void* pv) {
    const TickType_t delay = pdMS_TO_TICKS(200);
    const int kActiveOnMv = 30;
    const int kActiveOffMv = 20;
    const int64_t kIdleConfirmUs = 300 * 1000;
    const float kEmaAlpha = 0.25f;
    bool baseline_ready = false;
    float ema_mv = 0.0f;
    float baseline_mv = 0.0f;
    bool last_active = false;
    int64_t idle_since_us = 0;
    while (1) {
        if (s_acs_adc) {
            int raw = 0;
            if (adc_oneshot_read(s_acs_adc, ADC_CHANNEL_1, &raw) == ESP_OK) {
                if (s_acs_cali_ready) {
                    int mv = 0;
                    if (adc_cali_raw_to_voltage(s_acs_cali, raw, &mv) == ESP_OK) {
                        ema_mv = baseline_ready ? (kEmaAlpha * mv + (1.0f - kEmaAlpha) * ema_mv) : (float)mv;
                        if (!baseline_ready) {
                            baseline_mv = ema_mv;
                            baseline_ready = true;
                        }
                        float delta_mv = ema_mv - baseline_mv;
                        const int64_t now_us = esp_timer_get_time();
                        bool active = last_active ? (delta_mv > kActiveOffMv) : (delta_mv > kActiveOnMv);
                        if (last_active && !active) {
                            if (idle_since_us == 0) {
                                idle_since_us = now_us;
                            }
                            if (now_us - idle_since_us < kIdleConfirmUs) {
                                active = true;
                            }
                        } else if (active) {
                            idle_since_us = 0;
                        } else {
                            idle_since_us = 0;
                        }
                        if (!active) {
                            // Slowly track baseline when idle.
                            baseline_mv = 0.98f * baseline_mv + 0.02f * ema_mv;
                        }
                        if (active != last_active) {
                            ESP_LOGI(TAG_MAIN, "ACS712 state=%s mv=%.1f baseline=%.1f delta=%.1f raw=%d",
                                     active ? "ACTIVE" : "IDLE", ema_mv, baseline_mv, delta_mv, raw);
                            last_active = active;
                        }
                    } else {
                        ESP_LOGI(TAG_MAIN, "ACS712 raw=%d", raw);
                    }
                } else {
                    ESP_LOGI(TAG_MAIN, "ACS712 raw=%d", raw);
                }
            }
        }
        vTaskDelay(delay);
    }
}
#endif

void status_led_override(uint8_t r, uint8_t g, uint8_t b, uint32_t duration_ms) {
    s_led_override.active = true;
    s_led_override.persistent = (duration_ms == 0);
    s_led_override.expiry_us = esp_timer_get_time() + ((uint64_t)duration_ms * 1000ULL);
    s_led_override.r = r;
    s_led_override.g = g;
    s_led_override.b = b;
}

void status_led_clear_override() {
    s_led_override = {};
}

static void set_led_rgb(uint8_t r, uint8_t g, uint8_t b) {
    // Assume common anode; match BedControl logic
    uint32_t dR = LED_COMMON_ANODE ? (255 - r) : r;
    uint32_t dG = LED_COMMON_ANODE ? (255 - g) : g;
    uint32_t dB = LED_COMMON_ANODE ? (255 - b) : b;
    ledc_set_duty(LEDC_MODE, LEDC_CHANNEL_R, dR); ledc_update_duty(LEDC_MODE, LEDC_CHANNEL_R);
    ledc_set_duty(LEDC_MODE, LEDC_CHANNEL_G, dG); ledc_update_duty(LEDC_MODE, LEDC_CHANNEL_G);
    ledc_set_duty(LEDC_MODE, LEDC_CHANNEL_B, dB); ledc_update_duty(LEDC_MODE, LEDC_CHANNEL_B);
    s_status_pixel_r = r;
    s_status_pixel_g = g;
    s_status_pixel_b = b;
    if (!s_addressable_led_effect_active) {
        set_addressable_led(r, g, b);
    }
}

static void status_led_boot_test() {
    set_led_rgb(31, 0, 0);
    vTaskDelay(pdMS_TO_TICKS(120));
    set_led_rgb(0, 31, 0);
    vTaskDelay(pdMS_TO_TICKS(120));
    set_led_rgb(0, 0, 31);
    vTaskDelay(pdMS_TO_TICKS(120));
    set_led_rgb(0, 0, 0);
}

static void led_task(void* pv) {
    uint32_t t = 0;
    LedState last_state = g_led_state;
    bool last_override = false;
    while (1) {
        bool applied_override = false;
        if (s_led_override.active) {
            uint64_t now = esp_timer_get_time();
            if (s_led_override.persistent || now < s_led_override.expiry_us) {
                set_led_rgb(s_led_override.r, s_led_override.g, s_led_override.b);
                applied_override = true;
            } else {
                s_led_override = {};
            }
        }

        if (!applied_override) {
            switch (g_led_state) {
                case LedState::IDLE: { // spec: slow blink when unprovisioned
                    bool on = ((t / 10) % 2) == 0; // 1 Hz, 50% duty
                    uint8_t v = on ? 7 : 0;
                    set_led_rgb(v, v, v);
                    break;
                }
                case LedState::COMMISSIONING: { // spec: fast blink during commissioning
                    bool on = ((t / 2) % 2) == 0; // 5 Hz, 50% duty
                    uint8_t v = on ? 7 : 0;
                    set_led_rgb(v, v, 0);
                    break;
                }
                case LedState::COMMISSIONED: { // spec: solid when provisioned
                    set_led_rgb(0, 16, 0);
                    break;
                }
                case LedState::RESETTING: { // fault/reset: red blink
                    bool on = ((t / 4) % 2) == 0;
                    uint8_t v = on ? 11 : 0;
                    set_led_rgb(v, 0, 0);
                    break;
                }
            }
        }

        if (last_override != applied_override) {
            last_override = applied_override;
        }
        if (last_state != g_led_state) {
            last_state = g_led_state;
        }
        t++;
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

static void button_task(void* pv) {
    const int64_t shortMs = 2000;
    const int64_t longMs = 5000;
    while (1) {
        if (gpio_get_level((gpio_num_t)COMMISSION_BUTTON_GPIO) == 0) {
            int64_t start = esp_timer_get_time() / 1000;
            ESP_LOGI(TAG_MAIN, "Button pressed");
            while (gpio_get_level((gpio_num_t)COMMISSION_BUTTON_GPIO) == 0) {
                vTaskDelay(pdMS_TO_TICKS(10));
            }
            int64_t dur = (esp_timer_get_time() / 1000) - start;
            if (dur >= longMs) {
#if APP_MATTER
                ESP_LOGW(TAG_MAIN, "Button long-press: factory reset");
                MatterManager::instance().factoryReset();
#else
                ESP_LOGW(TAG_MAIN, "Button long-press: Wi-Fi + NVS reset");
                g_led_state = LedState::RESETTING;
                esp_wifi_restore();
                nvs_flash_erase();
                esp_restart();
#endif
            } else if (dur >= shortMs) {
#if APP_MATTER
                ESP_LOGI(TAG_MAIN, "Button short-press: start commissioning");
                MatterManager::instance().startCommissioning();
                g_led_state = LedState::COMMISSIONING;
#else
                ESP_LOGI(TAG_MAIN, "Button short-press: Wi-Fi reset");
                g_led_state = LedState::RESETTING;
                esp_wifi_restore();
                esp_restart();
#endif
            }
        }
        vTaskDelay(pdMS_TO_TICKS(20));
    }
}

#if !APP_MATTER
static esp_event_handler_instance_t s_ip_handler = nullptr;
static esp_event_handler_instance_t s_disc_handler = nullptr;
static void wifi_status_handler(void*, esp_event_base_t event_base, int32_t event_id, void*) {
    if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        g_led_state = LedState::COMMISSIONED;
    } else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        g_led_state = LedState::IDLE;
    }
}
#endif

#if APP_ROLE_BED
void bed_task(void *pvParameter) {
    while (1) {
        bedDriver->update();
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}
#endif

extern "C" void app_main() {
    // Detect flash size to decide OTA strategy
    uint32_t flash_size_bytes = 0;
    if (esp_flash_get_size(NULL, &flash_size_bytes) == ESP_OK) {
        s_dualOtaEnabled = (flash_size_bytes >= 8 * 1024 * 1024);
        ESP_LOGI(TAG_MAIN, "Flash size: %" PRIu32 " bytes (%s OTA)", flash_size_bytes, s_dualOtaEnabled ? "dual" : "single");
    } else {
        ESP_LOGW(TAG_MAIN, "Could not read flash size; defaulting to single OTA");
        s_dualOtaEnabled = false;
    }
#if APP_ROLE_BED
    ESP_LOGI(TAG_MAIN, "Role: bed (bed_control enabled)");
#else
    ESP_LOGI(TAG_MAIN, "Role: non-bed (bed_control excluded)");
#endif

    ESP_LOGI(TAG_MAIN, "Status LED init");
    init_status_led_hw();
    status_led_boot_test();
#if APP_ROLE_BED && CONFIG_IDF_TARGET_ESP32S3
    init_acs712_adc();
#endif

    if (!s_log_mutex) {
        s_log_mutex = xSemaphoreCreateMutex();
        if (!s_log_mutex) {
            ESP_LOGW(TAG_MAIN, "Log mutex create failed");
        }
    }
    log_spiffs_init();

    // Configure button input
    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pin_bit_mask = (1ULL << COMMISSION_BUTTON_GPIO);
    io_conf.pull_up_en = GPIO_PULLUP_ENABLE;
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    gpio_config(&io_conf);

    net.begin();
    s_log_queue = xQueueCreate(kLogQueueDepth, sizeof(LogItem));
    int day = log_day_index();
    if (day < 0) day = 0;
    s_log_day = day;
    if (s_log_mutex) xSemaphoreTake(s_log_mutex, portMAX_DELAY);
    log_store_load_day(day);
    if (s_log_mutex) xSemaphoreGive(s_log_mutex);
    s_log_prev_vprintf = esp_log_set_vprintf(log_vprintf);
    xTaskCreatePinnedToCore(log_store_task, "log_store", 3072, NULL, 4, NULL, 1);
#if !APP_MATTER
    if (!APP_ROLE_BED) {
        // Use status LED to mirror Wi-Fi provisioning state (light build)
        g_led_state = LedState::COMMISSIONING;
        esp_err_t loop_ret = esp_event_loop_create_default();
        if (loop_ret != ESP_OK && loop_ret != ESP_ERR_INVALID_STATE) {
            ESP_LOGW(TAG_MAIN, "Event loop create failed: %s", esp_err_to_name(loop_ret));
        }
        esp_event_handler_instance_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &wifi_status_handler, nullptr, &s_ip_handler);
        esp_event_handler_instance_register(WIFI_EVENT, WIFI_EVENT_STA_DISCONNECTED, &wifi_status_handler, nullptr, &s_disc_handler);
    }
#endif
#if APP_ROLE_BED
    BedService::instance().begin(bedDriver);
#if APP_MATTER
    MatterManager::instance().begin();
    g_led_state = MatterManager::instance().isCommissioned() ? LedState::COMMISSIONED : LedState::IDLE;
#endif
#if !APP_MATTER
    // Use status LED to mirror Wi-Fi provisioning state
    g_led_state = LedState::COMMISSIONING;
    esp_err_t loop_ret = esp_event_loop_create_default();
    if (loop_ret != ESP_OK && loop_ret != ESP_ERR_INVALID_STATE) {
        ESP_LOGW(TAG_MAIN, "Event loop create failed: %s", esp_err_to_name(loop_ret));
    }
    esp_event_handler_instance_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &wifi_status_handler, nullptr, &s_ip_handler);
    esp_event_handler_instance_register(WIFI_EVENT, WIFI_EVENT_STA_DISCONNECTED, &wifi_status_handler, nullptr, &s_disc_handler);
#endif
    xTaskCreatePinnedToCore(bed_task, "bed_logic", 4096, NULL, 5, NULL, 1);
#endif

    xTaskCreatePinnedToCore(button_task, "matter_btn", 3072, NULL, 5, NULL, 1);
    BaseType_t led_task_ok = xTaskCreatePinnedToCore(led_task, "matter_led", 3072, NULL, 5, NULL, 1);
    if (led_task_ok != pdPASS) {
        ESP_LOGE(TAG_MAIN, "LED task create failed: %ld", (long)led_task_ok);
    }
#if APP_ROLE_BED && CONFIG_IDF_TARGET_ESP32S3
    xTaskCreatePinnedToCore(acs712_log_task, "acs712_log", 3072, NULL, 5, NULL, 1);
#endif

    // Keep app_main alive; avoid returning to main_task
    for (;;) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

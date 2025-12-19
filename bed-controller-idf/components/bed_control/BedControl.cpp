#include "BedControl.h"
#include "Config.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"

#include "driver/gpio.h"
#include "driver/ledc.h"
#include "StatusLed.h"

#include "esp_log.h"
#include "esp_timer.h"
#include "nvs_flash.h"
#include "nvs.h"
#include <cstring>
#include <cmath>
#include <algorithm>

static const char *TAG = "BED_CTRL";
static bool s_ledc_ready = false;
std::string activeCommandLog = "IDLE"; // Changed from String to std::string

#define LEDC_TIMER              LEDC_TIMER_0
#define LEDC_MODE               LEDC_LOW_SPEED_MODE
#define LEDC_DUTY_RES           LEDC_TIMER_8_BIT
#define LEDC_FREQUENCY          5000
#define CLAMP_LIMIT(val)        (std::max<int32_t>((int32_t)LIMIT_MIN_MS, std::min<int32_t>((int32_t)LIMIT_MAX_MS, (int32_t)(val))))

// Channels
#define LEDC_CHANNEL_R          LEDC_CHANNEL_0
#define LEDC_CHANNEL_G          LEDC_CHANNEL_1
#define LEDC_CHANNEL_B          LEDC_CHANNEL_2

int64_t BedControl::millis() {
    return esp_timer_get_time() / 1000;
}

// --- NVS STRING HELPERS ---
std::string BedControl::getSavedLabel(const char* key, const char* defaultVal) {
    size_t required_size;
    // First call to get length
    if (nvs_get_str(nvsHandle, key, NULL, &required_size) == ESP_OK) {
        char* buf = new char[required_size];
        // Second call to get data
        nvs_get_str(nvsHandle, key, buf, &required_size);
        std::string val = buf;
        delete[] buf;
        return val;
    }
    return std::string(defaultVal);
}

void BedControl::setSavedLabel(const char* key, std::string val) {
    nvs_set_str(nvsHandle, key, val.c_str());
    nvs_commit(nvsHandle);
}

// --- LIMITS ---
void BedControl::loadLimits() {
    int32_t h = getSavedPos("head_max_ms", HEAD_MAX_MS_DEFAULT);
    int32_t f = getSavedPos("foot_max_ms", FOOT_MAX_MS_DEFAULT);
    setLimits(h, f); // clamps and persists if needed
}

void BedControl::getLimits(int32_t &headMaxMs, int32_t &footMaxMs) {
    headMaxMs = state.headMaxMs;
    footMaxMs = state.footMaxMs;
}

void BedControl::getMotionDirs(std::string &headDir, std::string &footDir) {
    if (xSemaphoreTake(mutex, portMAX_DELAY)) {
        headDir = state.headDir;
        footDir = state.footDir;
        xSemaphoreGive(mutex);
    } else {
        headDir = "STOPPED";
        footDir = "STOPPED";
    }
}

void BedControl::getOptoStates(int &o1, int &o2, int &o3, int &o4) {
    if (xSemaphoreTake(mutex, portMAX_DELAY)) {
        o1 = state.optoStable[0];
        o2 = state.optoStable[1];
        o3 = state.optoStable[2];
        o4 = state.optoStable[3];
        xSemaphoreGive(mutex);
    } else {
        o1 = o2 = o3 = o4 = 1;
    }
}

void BedControl::setLimits(int32_t headMaxMs, int32_t footMaxMs) {
    headMaxMs = CLAMP_LIMIT(headMaxMs);
    footMaxMs = CLAMP_LIMIT(footMaxMs);
    state.headMaxMs = headMaxMs;
    state.footMaxMs = footMaxMs;
    setSavedPos("head_max_ms", headMaxMs);
    setSavedPos("foot_max_ms", footMaxMs);
}

// --- FACTORY DEFAULTS ---
void BedControl::initFactoryDefaults() {
    size_t required_size;
    // Check if "zg_label" exists (String check). 
    // If this fails, it means we have old NVS data or empty NVS.
    esp_err_t err = nvs_get_str(nvsHandle, "zg_label", NULL, &required_size);
    
    if (err == ESP_ERR_NVS_NOT_FOUND) {
        ESP_LOGI(TAG, "First Boot: Writing Factory Defaults...");
        
        setSavedPos("zg_head", 10000);    setSavedPos("zg_foot", 40000); setSavedLabel("zg_label", "Zero G");
        setSavedPos("snore_head", 10000); setSavedPos("snore_foot", 0); setSavedLabel("snore_label", "Anti-Snore");
        setSavedPos("legs_head", 0);      setSavedPos("legs_foot", 43000); setSavedLabel("legs_label", "Legs Up");
        setSavedPos("p1_head", 0);        setSavedPos("p1_foot", 0); setSavedLabel("p1_label", "P1");
        setSavedPos("p2_head", 0);        setSavedPos("p2_foot", 0); setSavedLabel("p2_label", "P2");

        setSavedPos("head_max_ms", HEAD_MAX_MS_DEFAULT);
        setSavedPos("foot_max_ms", FOOT_MAX_MS_DEFAULT);
    }
}

// --- INITIALIZATION ---
void BedControl::begin() {
    mutex = xSemaphoreCreateMutex();
    
    initGPIO();
    initOptoInputs();
    initPWM();
    initNVS();
    
    // Populate defaults if empty
    initFactoryDefaults();
    loadLimits();

    state.currentHeadPosMs = getSavedPos("headPos", 0);
    state.currentFootPosMs = getSavedPos("footPos", 0);
    state.headDir = "STOPPED";
    state.footDir = "STOPPED";
    state.isPresetActive = false;
    for (int i = 0; i < 4; ++i) {
        state.optoStable[i] = 1;  // pull-ups -> idle high
        state.optoCounter[i] = 0;
        state.optoLastRaw[i] = 1;
    }

    ESP_LOGI(TAG, "Bed Control Ready. H:%d F:%d", (int)state.currentHeadPosMs, (int)state.currentFootPosMs);
}

void BedControl::initGPIO() {
    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = (1ULL << HEAD_UP_PIN) | (1ULL << HEAD_DOWN_PIN) | 
                           (1ULL << FOOT_UP_PIN) | (1ULL << FOOT_DOWN_PIN) |
                           (1ULL << TRANSFER_PIN);
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE;
    gpio_config(&io_conf);

    stopHardware();
    setTransferSwitch(false);
}

void BedControl::initOptoInputs() {
    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    io_conf.pull_up_en = GPIO_PULLUP_ENABLE;
    io_conf.pin_bit_mask = (1ULL << OPTO_IN_1) | (1ULL << OPTO_IN_2) | (1ULL << OPTO_IN_3) | (1ULL << OPTO_IN_4);
    gpio_config(&io_conf);
}

void BedControl::initPWM() {
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
        ESP_LOGE(TAG, "ledc_timer_config failed: %s", esp_err_to_name(err));
        return;
    }

    ledc_channel_config_t c0 = { .gpio_num = LED_PIN_R, .speed_mode = LEDC_MODE, .channel = LEDC_CHANNEL_0, .intr_type = LEDC_INTR_DISABLE, .timer_sel = LEDC_TIMER, .duty = 0, .hpoint = 0, .flags = {} };
    ledc_channel_config_t c1 = { .gpio_num = LED_PIN_G, .speed_mode = LEDC_MODE, .channel = LEDC_CHANNEL_1, .intr_type = LEDC_INTR_DISABLE, .timer_sel = LEDC_TIMER, .duty = 0, .hpoint = 0, .flags = {} };
    ledc_channel_config_t c2 = { .gpio_num = LED_PIN_B, .speed_mode = LEDC_MODE, .channel = LEDC_CHANNEL_2, .intr_type = LEDC_INTR_DISABLE, .timer_sel = LEDC_TIMER, .duty = 0, .hpoint = 0, .flags = {} };

    ledc_channel_config(&c0);
    ledc_channel_config(&c1);
    ledc_channel_config(&c2);
    
    s_ledc_ready = true;

    // Boot Flash
    setLedColor(255, 255, 255);
    vTaskDelay(300 / portTICK_PERIOD_MS);
    setLedColor(0, 0, 0);
}

void BedControl::initNVS() {
    esp_err_t err = nvs_flash_init();
    if (err == ESP_ERR_NVS_NO_FREE_PAGES || err == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        nvs_flash_erase();
        nvs_flash_init();
    }
    nvs_open("storage", NVS_READWRITE, &nvsHandle);
}

// --- HARDWARE CONTROL ---

void BedControl::setLedColor(uint8_t r, uint8_t g, uint8_t b) {
    if (!s_ledc_ready) return;
    // If off, clear override so status LED patterns can resume.
    if (r == 0 && g == 0 && b == 0) {
        status_led_clear_override();
        return;
    }
    status_led_override(r, g, b, 0); // persistent until cleared
}

void BedControl::stopHardware() {
    // DRV8871: drive both inputs low to coast/stop
    gpio_set_level((gpio_num_t)HEAD_UP_PIN, 0); 
    gpio_set_level((gpio_num_t)HEAD_DOWN_PIN, 0);
    gpio_set_level((gpio_num_t)FOOT_UP_PIN, 0);
    gpio_set_level((gpio_num_t)FOOT_DOWN_PIN, 0);
    setLedColor(0, 0, 0);
    ESP_LOGI(TAG, "Relays: HEAD_UP=0 HEAD_DOWN=0 FOOT_UP=0 FOOT_DOWN=0 (stopHardware)");
}

int8_t BedControl::classifyLimit(int32_t pos, int32_t maxVal) {
    if (pos <= 0) return -1;
    if (pos >= maxVal) return 1;
    return 0;
}

void BedControl::logLimitTransitions() {
    int8_t headClass = classifyLimit(state.currentHeadPosMs, state.headMaxMs);
    int8_t footClass = classifyLimit(state.currentFootPosMs, state.footMaxMs);
    static int8_t prevHead = 0;
    static int8_t prevFoot = 0;
    if (headClass != prevHead) {
        if (headClass == -1) ESP_LOGI(TAG, "Head reached MIN limit (0ms)");
        else if (headClass == 1) ESP_LOGI(TAG, "Head reached MAX limit (%dms)", (int)state.headMaxMs);
        prevHead = headClass;
    }
    if (footClass != prevFoot) {
        if (footClass == -1) ESP_LOGI(TAG, "Foot reached MIN limit (0ms)");
        else if (footClass == 1) ESP_LOGI(TAG, "Foot reached MAX limit (%dms)", (int)state.footMaxMs);
        prevFoot = footClass;
    }
}

void BedControl::updateOptoInputs() {
    const int pins[4] = { OPTO_IN_1, OPTO_IN_2, OPTO_IN_3, OPTO_IN_4 };
    for (int i = 0; i < 4; ++i) {
        int raw = gpio_get_level((gpio_num_t)pins[i]);
        if (raw == state.optoLastRaw[i]) {
            if (state.optoCounter[i] < 3) state.optoCounter[i]++;
        } else {
            state.optoLastRaw[i] = raw;
            state.optoCounter[i] = 0;
        }
        if (state.optoCounter[i] >= 2) {
            state.optoStable[i] = raw;
        }
    }
}

void BedControl::setTransferSwitch(bool active) {
    int level = active ? RELAY_ON : !RELAY_ON;
    gpio_set_level((gpio_num_t)TRANSFER_PIN, level);
}

// --- NVS HELPERS ---

int32_t BedControl::getSavedPos(const char* key, int32_t defaultVal) {
    int32_t val = 0;
    if (nvs_get_i32(nvsHandle, key, &val) == ESP_OK) return val;
    return defaultVal;
}

void BedControl::setSavedPos(const char* key, int32_t val) {
    nvs_set_i32(nvsHandle, key, val);
    nvs_commit(nvsHandle);
}

// --- LOGIC & MOVEMENT ---

void BedControl::syncState() {
    int64_t now = millis();
    stopHardware();

    if (state.headStartTime != 0 && state.headDir != "STOPPED") {
        int32_t elapsed = (int32_t)(now - state.headStartTime);
        if (state.headDir == "UP") state.currentHeadPosMs += elapsed;
        else state.currentHeadPosMs -= elapsed;
        
        if (state.currentHeadPosMs > state.headMaxMs) state.currentHeadPosMs = state.headMaxMs;
        if (state.currentHeadPosMs < 0) state.currentHeadPosMs = 0;
        state.headDir = "STOPPED"; state.headStartTime = 0;
    }
    
    if (state.footStartTime != 0 && state.footDir != "STOPPED") {
        int32_t elapsed = (int32_t)(now - state.footStartTime);
        if (state.footDir == "UP") state.currentFootPosMs += elapsed;
        else state.currentFootPosMs -= elapsed;

        if (state.currentFootPosMs > state.footMaxMs) state.currentFootPosMs = state.footMaxMs;
        if (state.currentFootPosMs < 0) state.currentFootPosMs = 0;
        state.footDir = "STOPPED"; state.footStartTime = 0;
    }

    state.isPresetActive = false;
    setTransferSwitch(false);
    setSavedPos("headPos", state.currentHeadPosMs);
    setSavedPos("footPos", state.currentFootPosMs);
}

void BedControl::stop() {
    if (xSemaphoreTake(mutex, portMAX_DELAY)) {
        syncState();
        xSemaphoreGive(mutex);
    }
}

void BedControl::moveHead(std::string dir) {
    if (xSemaphoreTake(mutex, portMAX_DELAY)) {
        syncState(); 
        setTransferSwitch(true);
        state.headStartTime = millis();
        state.headDir = dir;
        state.isPresetActive = false; 
        
        // LED: Green (UP) / Red (DOWN)
        if (dir == "UP") {
            setLedColor(160, 64, 255); // Head up: violet
            gpio_set_level((gpio_num_t)HEAD_DOWN_PIN, 0);
            gpio_set_level((gpio_num_t)HEAD_UP_PIN, 1);
        } else {
            setLedColor(255, 140, 0); // Head down: amber
            gpio_set_level((gpio_num_t)HEAD_UP_PIN, 0);
            gpio_set_level((gpio_num_t)HEAD_DOWN_PIN, 1);
        }
        xSemaphoreGive(mutex);
    }
}

void BedControl::moveFoot(std::string dir) {
     if (xSemaphoreTake(mutex, portMAX_DELAY)) {
        syncState(); 
        setTransferSwitch(true);
        state.footStartTime = millis();
        state.footDir = dir;
        state.isPresetActive = false; 
        
        // LED: Cyan (UP) / Magenta (DOWN)
        if (dir == "UP") {
            setLedColor(0, 180, 255); // Foot up: sky blue
            gpio_set_level((gpio_num_t)FOOT_DOWN_PIN, 0);
            gpio_set_level((gpio_num_t)FOOT_UP_PIN, 1);
        } else {
            setLedColor(255, 0, 180); // Foot down: magenta
            gpio_set_level((gpio_num_t)FOOT_UP_PIN, 0);
            gpio_set_level((gpio_num_t)FOOT_DOWN_PIN, 1);
        }
        xSemaphoreGive(mutex);
    }
}

void BedControl::moveAll(std::string dir) {
    if (xSemaphoreTake(mutex, portMAX_DELAY)) {
        syncState();
        setTransferSwitch(true);
        state.headStartTime = millis();
        state.footStartTime = millis();
        state.headDir = dir;
        state.footDir = dir;
        state.isPresetActive = false;

        if (dir == "UP") {
            setLedColor(0, 200, 200); // All up: teal
            gpio_set_level((gpio_num_t)HEAD_DOWN_PIN, 0);
            gpio_set_level((gpio_num_t)FOOT_DOWN_PIN, 0);
            gpio_set_level((gpio_num_t)HEAD_UP_PIN, 1);
            gpio_set_level((gpio_num_t)FOOT_UP_PIN, 1);
        } else { // DOWN
            setLedColor(255, 120, 0); // All down: warm amber
            gpio_set_level((gpio_num_t)HEAD_UP_PIN, 0);
            gpio_set_level((gpio_num_t)FOOT_UP_PIN, 0);
            gpio_set_level((gpio_num_t)HEAD_DOWN_PIN, 1);
            gpio_set_level((gpio_num_t)FOOT_DOWN_PIN, 1);
        }
        xSemaphoreGive(mutex);
    }
}

int32_t BedControl::setTarget(int32_t tHead, int32_t tFoot) {
    int32_t maxDur = 0;
    if (xSemaphoreTake(mutex, portMAX_DELAY)) {
        syncState();
        setTransferSwitch(true);
        
        if (tHead < 0) tHead = 0;
        if (tFoot < 0) tFoot = 0;
        if (tHead > state.headMaxMs) tHead = state.headMaxMs;
        if (tFoot > state.footMaxMs) tFoot = state.footMaxMs;

        int32_t hDiff = tHead - state.currentHeadPosMs;
        int32_t fDiff = tFoot - state.currentFootPosMs;
        int64_t now = millis();

        if (std::abs(hDiff) > 100) {
            state.headStartTime = now;
            state.headTargetDuration = std::abs(hDiff);
            if (tHead == 0 || tHead == state.headMaxMs) state.headTargetDuration += SYNC_EXTRA_MS;
            if (state.headTargetDuration > maxDur) maxDur = state.headTargetDuration;
            
            if (hDiff > 0) { state.headDir = "UP"; gpio_set_level((gpio_num_t)HEAD_DOWN_PIN, 0); gpio_set_level((gpio_num_t)HEAD_UP_PIN, 1); }
            else { state.headDir = "DOWN"; gpio_set_level((gpio_num_t)HEAD_UP_PIN, 0); gpio_set_level((gpio_num_t)HEAD_DOWN_PIN, 1); }
        }

        if (std::abs(fDiff) > 100) {
            state.footStartTime = now;
            state.footTargetDuration = std::abs(fDiff);
            if (tFoot == 0 || tFoot == state.footMaxMs) state.footTargetDuration += SYNC_EXTRA_MS;
            if (state.footTargetDuration > maxDur) maxDur = state.footTargetDuration;

            if (fDiff > 0) { state.footDir = "UP"; gpio_set_level((gpio_num_t)FOOT_DOWN_PIN, 0); gpio_set_level((gpio_num_t)FOOT_UP_PIN, 1); }
            else { state.footDir = "DOWN"; gpio_set_level((gpio_num_t)FOOT_UP_PIN, 0); gpio_set_level((gpio_num_t)FOOT_DOWN_PIN, 1); }
        }

        if (maxDur > 0) {
            state.isPresetActive = true;
            setLedColor(255, 215, 0); // Preset active: gold
        } else {
            setTransferSwitch(false);
        }
        xSemaphoreGive(mutex);
    }
    return maxDur;
}

void BedControl::update() {
    if (xSemaphoreTake(mutex, portMAX_DELAY)) {
        int64_t now = millis();
        updateOptoInputs();

        if (state.isPresetActive) {
            bool headDone = true; bool footDone = true;

            if (state.headDir != "STOPPED") {
                int32_t elapsed = (int32_t)(now - state.headStartTime);
                if (elapsed >= state.headTargetDuration) {
                    gpio_set_level((gpio_num_t)HEAD_UP_PIN, 0);
                    gpio_set_level((gpio_num_t)HEAD_DOWN_PIN, 0);
                    
                    if (state.headDir == "UP") state.currentHeadPosMs += state.headTargetDuration;
                    else state.currentHeadPosMs -= state.headTargetDuration;
                    
                    if (state.currentHeadPosMs > state.headMaxMs) state.currentHeadPosMs = state.headMaxMs;
                    if (state.currentHeadPosMs < 0) state.currentHeadPosMs = 0;

                    state.headDir = "STOPPED"; state.headStartTime = 0; 
                } else headDone = false; 
            }

            if (state.footDir != "STOPPED") {
                int32_t elapsed = (int32_t)(now - state.footStartTime);
                if (elapsed >= state.footTargetDuration) {
                    gpio_set_level((gpio_num_t)FOOT_UP_PIN, 0);
                    gpio_set_level((gpio_num_t)FOOT_DOWN_PIN, 0);
                    
                    if (state.footDir == "UP") state.currentFootPosMs += state.footTargetDuration;
                    else state.currentFootPosMs -= state.footTargetDuration;

                    if (state.currentFootPosMs > state.footMaxMs) state.currentFootPosMs = state.footMaxMs;
                    if (state.currentFootPosMs < 0) state.currentFootPosMs = 0;

                    state.footDir = "STOPPED"; state.footStartTime = 0;
                } else footDone = false; 
            }

            if (headDone && footDone) {
                ESP_LOGI(TAG, "Preset movement complete; stopping hardware (head=%dms foot=%dms)", (int)state.currentHeadPosMs, (int)state.currentFootPosMs);
                syncState(); 
                ESP_LOGI(TAG, "Preset overrun stopped; state synced.");
            }
        }
        xSemaphoreGive(mutex);
    }
}

void BedControl::getLiveStatus(int32_t &head, int32_t &foot) {
    if (xSemaphoreTake(mutex, portMAX_DELAY)) {
        int64_t now = millis();
        head = state.currentHeadPosMs; foot = state.currentFootPosMs;

        if (state.headStartTime != 0 && state.headDir != "STOPPED") {
            int32_t el = (int32_t)(now - state.headStartTime);
            if (state.headDir == "UP") head += el; else head -= el;
            
            if (head > state.headMaxMs) head = state.headMaxMs; 
            if (head < 0) head = 0;
        }
        if (state.footStartTime != 0 && state.footDir != "STOPPED") {
            int32_t el = (int32_t)(now - state.footStartTime);
            if (state.footDir == "UP") foot += el; else foot -= el;
            
            if (foot > state.footMaxMs) foot = state.footMaxMs; 
            if (foot < 0) foot = 0;
        }
        xSemaphoreGive(mutex);
    }
}

#include "BedControl.h"
#include "Config.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"

#include "driver/gpio.h"
#include "driver/ledc.h"

#include "esp_log.h"
#include "esp_timer.h"
#include "nvs_flash.h"
#include "nvs.h"

static const char *TAG = "BED_CTRL";

static bool s_ledc_ready = false;

#define LEDC_TIMER              LEDC_TIMER_0
#define LEDC_MODE               LEDC_LOW_SPEED_MODE
#define LEDC_DUTY_RES           LEDC_TIMER_8_BIT
#define LEDC_FREQUENCY          5000

int64_t BedControl::millis() {
    return esp_timer_get_time() / 1000;
}

void BedControl::begin() {
    mutex = xSemaphoreCreateMutex();
    initGPIO();
    initPWM();
    initNVS();

    state.currentHeadPosMs = getSavedPos("headPos", 0);
    state.currentFootPosMs = getSavedPos("footPos", 0);
    state.headDir = "STOPPED";
    state.footDir = "STOPPED";
    state.isPresetActive = false;
    ESP_LOGI(TAG, "Bed Control Ready.");
}

void BedControl::initGPIO() {
    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = (1ULL << HEAD_UP_PIN) | (1ULL << HEAD_DOWN_PIN) |
                           (1ULL << FOOT_UP_PIN) | (1ULL << FOOT_DOWN_PIN) |
                           (1ULL << TRANSFER_PIN_1) | (1ULL << TRANSFER_PIN_2) |
                           (1ULL << TRANSFER_PIN_3) | (1ULL << TRANSFER_PIN_4);
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE;
    gpio_config(&io_conf);
    stopHardware();
    setTransferSwitch(false);
}

void BedControl::initPWM() {
    ledc_timer_config_t ledc_timer = {
        .speed_mode       = LEDC_MODE,
        .duty_resolution  = LEDC_DUTY_RES,
        .timer_num        = LEDC_TIMER,
        .freq_hz          = LEDC_FREQUENCY,
        .clk_cfg          = LEDC_AUTO_CLK,
        .deconfigure      = false,
    };

    esp_err_t err = ledc_timer_config(&ledc_timer);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "ledc_timer_config failed: %s", esp_err_to_name(err));
        return;
    }

    ledc_channel_config_t c0 = {
        .gpio_num   = LED_PIN_R,
        .speed_mode = LEDC_MODE,
        .channel    = LEDC_CHANNEL_0,
        .intr_type  = LEDC_INTR_DISABLE,
        .timer_sel  = LEDC_TIMER,
        .duty       = 0,
        .hpoint     = 0,
        .flags      = {}
    };
    ledc_channel_config_t c1 = {
        .gpio_num   = LED_PIN_G,
        .speed_mode = LEDC_MODE,
        .channel    = LEDC_CHANNEL_1,
        .intr_type  = LEDC_INTR_DISABLE,
        .timer_sel  = LEDC_TIMER,
        .duty       = 0,
        .hpoint     = 0,
        .flags      = {}
    };
    ledc_channel_config_t c2 = {
        .gpio_num   = LED_PIN_B,
        .speed_mode = LEDC_MODE,
        .channel    = LEDC_CHANNEL_2,
        .intr_type  = LEDC_INTR_DISABLE,
        .timer_sel  = LEDC_TIMER,
        .duty       = 0,
        .hpoint     = 0,
        .flags      = {}
    };

    err = ledc_channel_config(&c0);
    if (err != ESP_OK) { ESP_LOGE(TAG, "ledc_channel_config R failed: %s", esp_err_to_name(err)); return; }
    err = ledc_channel_config(&c1);
    if (err != ESP_OK) { ESP_LOGE(TAG, "ledc_channel_config G failed: %s", esp_err_to_name(err)); return; }
    err = ledc_channel_config(&c2);
    if (err != ESP_OK) { ESP_LOGE(TAG, "ledc_channel_config B failed: %s", esp_err_to_name(err)); return; }

    s_ledc_ready = true;

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
    // "storage" namespace, handle stored in member nvsHandle
    nvs_open("storage", NVS_READWRITE, &nvsHandle);
}

void BedControl::setLedColor(uint8_t r, uint8_t g, uint8_t b) {
    if (!s_ledc_ready) {
        return;  // avoid "LEDC is not initialized" spam
    }

    uint32_t dR = LED_COMMON_ANODE ? (255 - r) : r;
    uint32_t dG = LED_COMMON_ANODE ? (255 - g) : g;
    uint32_t dB = LED_COMMON_ANODE ? (255 - b) : b;

    ledc_set_duty(LEDC_MODE, LEDC_CHANNEL_0, dR);
    ledc_update_duty(LEDC_MODE, LEDC_CHANNEL_0);

    ledc_set_duty(LEDC_MODE, LEDC_CHANNEL_1, dG);
    ledc_update_duty(LEDC_MODE, LEDC_CHANNEL_1);

    ledc_set_duty(LEDC_MODE, LEDC_CHANNEL_2, dB);
    ledc_update_duty(LEDC_MODE, LEDC_CHANNEL_2);
}

void BedControl::stopHardware() {
    gpio_set_level((gpio_num_t)HEAD_UP_PIN,   !RELAY_ON);
    gpio_set_level((gpio_num_t)HEAD_DOWN_PIN, !RELAY_ON);
    gpio_set_level((gpio_num_t)FOOT_UP_PIN,   !RELAY_ON);
    gpio_set_level((gpio_num_t)FOOT_DOWN_PIN, !RELAY_ON);
    setLedColor(0, 0, 0);
}

void BedControl::setTransferSwitch(bool active) {
    int level = active ? RELAY_ON : !RELAY_ON;
    gpio_set_level((gpio_num_t)TRANSFER_PIN_1, level);
    gpio_set_level((gpio_num_t)TRANSFER_PIN_2, level);
    gpio_set_level((gpio_num_t)TRANSFER_PIN_3, level);
    gpio_set_level((gpio_num_t)TRANSFER_PIN_4, level);
}

int32_t BedControl::getSavedPos(const char* key, int32_t defaultVal) {
    int32_t val = 0;
    if (nvs_get_i32(nvsHandle, key, &val) == ESP_OK) {
        return val;
    }
    return defaultVal;
}

void BedControl::setSavedPos(const char* key, int32_t val) {
    nvs_set_i32(nvsHandle, key, val);
    nvs_commit(nvsHandle);
}

void BedControl::syncState() {
    int64_t now = millis();
    stopHardware();

    if (state.headStartTime != 0 && state.headDir != "STOPPED") {
        int32_t elapsed = (int32_t)(now - state.headStartTime);
        if (state.headDir == "UP") {
            state.currentHeadPosMs += elapsed;
        } else {
            state.currentHeadPosMs -= elapsed;
        }
        if (state.currentHeadPosMs > HEAD_MAX_MS) state.currentHeadPosMs = HEAD_MAX_MS;
        if (state.currentHeadPosMs < 0)          state.currentHeadPosMs = 0;
        state.headDir = "STOPPED";
        state.headStartTime = 0;
    }

    if (state.footStartTime != 0 && state.footDir != "STOPPED") {
        int32_t elapsed = (int32_t)(now - state.footStartTime);
        if (state.footDir == "UP") {
            state.currentFootPosMs += elapsed;
        } else {
            state.currentFootPosMs -= elapsed;
        }
        if (state.currentFootPosMs > FOOT_MAX_MS) state.currentFootPosMs = FOOT_MAX_MS;
        if (state.currentFootPosMs < 0)           state.currentFootPosMs = 0;
        state.footDir = "STOPPED";
        state.footStartTime = 0;
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

// OLD
// void BedControl::moveHead(const std::string &dir) {
void BedControl::moveHead(std::string dir) {
    if (xSemaphoreTake(mutex, portMAX_DELAY)) {
        syncState();
        setTransferSwitch(true);
        state.headStartTime = millis();
        state.headDir = dir;
        state.isPresetActive = false;

        if (dir == "UP") {
            setLedColor(0, 128, 0);
            gpio_set_level((gpio_num_t)HEAD_DOWN_PIN, !RELAY_ON);
            gpio_set_level((gpio_num_t)HEAD_UP_PIN,   RELAY_ON);
        } else {
            setLedColor(128, 0, 0);
            gpio_set_level((gpio_num_t)HEAD_UP_PIN,   !RELAY_ON);
            gpio_set_level((gpio_num_t)HEAD_DOWN_PIN, RELAY_ON);
        }
        xSemaphoreGive(mutex);
    }
}

// OLD
// void BedControl::moveFoot(const std::string &dir) {
void BedControl::moveFoot(std::string dir) {
    if (xSemaphoreTake(mutex, portMAX_DELAY)) {
        syncState();
        setTransferSwitch(true);
        state.footStartTime = millis();
        state.footDir = dir;
        state.isPresetActive = false;

        if (dir == "UP") {
            setLedColor(0, 128, 128);
            gpio_set_level((gpio_num_t)FOOT_DOWN_PIN, !RELAY_ON);
            gpio_set_level((gpio_num_t)FOOT_UP_PIN,   RELAY_ON);
        } else {
            setLedColor(128, 0, 128);
            gpio_set_level((gpio_num_t)FOOT_UP_PIN,   !RELAY_ON);
            gpio_set_level((gpio_num_t)FOOT_DOWN_PIN, RELAY_ON);
        }
        xSemaphoreGive(mutex);
    }
}


int32_t BedControl::setTarget(int32_t tHead, int32_t tFoot) {
    int32_t maxDur = 0;
    if (xSemaphoreTake(mutex, portMAX_DELAY)) {
        syncState();
        setTransferSwitch(true);

        int32_t hDiff = tHead - state.currentHeadPosMs;
        int32_t fDiff = tFoot - state.currentFootPosMs;
        int64_t now   = millis();

        if (std::abs(hDiff) > 100) {
            state.headStartTime      = now;
            state.headTargetDuration = std::abs(hDiff);
            if (tHead == 0 || tHead == HEAD_MAX_MS) {
                state.headTargetDuration += SYNC_EXTRA_MS;
            }
            if (state.headTargetDuration > maxDur) {
                maxDur = state.headTargetDuration;
            }

            if (hDiff > 0) {
                state.headDir = "UP";
                gpio_set_level((gpio_num_t)HEAD_DOWN_PIN, !RELAY_ON);
                gpio_set_level((gpio_num_t)HEAD_UP_PIN,   RELAY_ON);
            } else {
                state.headDir = "DOWN";
                gpio_set_level((gpio_num_t)HEAD_UP_PIN,   !RELAY_ON);
                gpio_set_level((gpio_num_t)HEAD_DOWN_PIN, RELAY_ON);
            }
        }

        if (std::abs(fDiff) > 100) {
            state.footStartTime      = now;
            state.footTargetDuration = std::abs(fDiff);
            if (tFoot == 0 || tFoot == FOOT_MAX_MS) {
                state.footTargetDuration += SYNC_EXTRA_MS;
            }
            if (state.footTargetDuration > maxDur) {
                maxDur = state.footTargetDuration;
            }

            if (fDiff > 0) {
                state.footDir = "UP";
                gpio_set_level((gpio_num_t)FOOT_DOWN_PIN, !RELAY_ON);
                gpio_set_level((gpio_num_t)FOOT_UP_PIN,   RELAY_ON);
            } else {
                state.footDir = "DOWN";
                gpio_set_level((gpio_num_t)FOOT_UP_PIN,   !RELAY_ON);
                gpio_set_level((gpio_num_t)FOOT_DOWN_PIN, RELAY_ON);
            }
        }

        if (maxDur > 0) {
            state.isPresetActive = true;
            setLedColor(0, 0, 128);
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
        if (state.isPresetActive) {
            bool headDone = true;
            bool footDone = true;

            if (state.headDir != "STOPPED") {
                int32_t elapsed = (int32_t)(now - state.headStartTime);
                if (elapsed >= state.headTargetDuration) {
                    gpio_set_level((gpio_num_t)HEAD_UP_PIN,   !RELAY_ON);
                    gpio_set_level((gpio_num_t)HEAD_DOWN_PIN, !RELAY_ON);
                    if (state.headDir == "UP") {
                        state.currentHeadPosMs += state.headTargetDuration;
                    } else {
                        state.currentHeadPosMs -= state.headTargetDuration;
                    }
                    if (state.currentHeadPosMs > HEAD_MAX_MS) state.currentHeadPosMs = HEAD_MAX_MS;
                    if (state.currentHeadPosMs < 0)          state.currentHeadPosMs = 0;
                    state.headDir = "STOPPED";
                    state.headStartTime = 0;
                } else {
                    headDone = false;
                }
            }

            if (state.footDir != "STOPPED") {
                int32_t elapsed = (int32_t)(now - state.footStartTime);
                if (elapsed >= state.footTargetDuration) {
                    gpio_set_level((gpio_num_t)FOOT_UP_PIN,   !RELAY_ON);
                    gpio_set_level((gpio_num_t)FOOT_DOWN_PIN, !RELAY_ON);
                    if (state.footDir == "UP") {
                        state.currentFootPosMs += state.footTargetDuration;
                    } else {
                        state.currentFootPosMs -= state.footTargetDuration;
                    }
                    if (state.currentFootPosMs > FOOT_MAX_MS) state.currentFootPosMs = FOOT_MAX_MS;
                    if (state.currentFootPosMs < 0)           state.currentFootPosMs = 0;
                    state.footDir = "STOPPED";
                    state.footStartTime = 0;
                } else {
                    footDone = false;
                }
            }

            if (headDone && footDone) {
                syncState();
            }
        }
        xSemaphoreGive(mutex);
    }
}

void BedControl::getLiveStatus(int32_t &head, int32_t &foot) {
    if (xSemaphoreTake(mutex, portMAX_DELAY)) {
        int64_t now = millis();
        head = state.currentHeadPosMs;
        foot = state.currentFootPosMs;

        if (state.headStartTime != 0 && state.headDir != "STOPPED") {
            int32_t el = (int32_t)(now - state.headStartTime);
            if (state.headDir == "UP") {
                head += el;
            } else {
                head -= el;
            }
            if (head > HEAD_MAX_MS) head = HEAD_MAX_MS;
            if (head < 0)           head = 0;
        }

        if (state.footStartTime != 0 && state.footDir != "STOPPED") {
            int32_t el = (int32_t)(now - state.footStartTime);
            if (state.footDir == "UP") {
                foot += el;
            } else {
                foot -= el;
            }
            if (foot > FOOT_MAX_MS) foot = FOOT_MAX_MS;
            if (foot < 0)           foot = 0;
        }

        xSemaphoreGive(mutex);
    }
}

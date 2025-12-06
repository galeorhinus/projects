#include "MatterManager.h"
#include "BedService.h"
#include "esp_log.h"
#include "esp_wifi.h"
#include "nvs_flash.h"
#include "nvs.h"

static const char* TAG = "MatterMgr";

#if ENABLE_MATTER
// Defaults for developer builds (esp-matter sample values)
static const char* DEFAULT_QR = "MT:YNJV7VSC00KA0648G00";
static const char* DEFAULT_MANUAL = "34970112332";
static const int DEFAULT_PIN = 20202021;
static const int DEFAULT_DISC = 3840;
static const int DEFAULT_VID = 0xFFF1;
static const int DEFAULT_PID = 0x8000;

static void commissioning_timeout_cb(void* arg);

MatterManager& MatterManager::instance() {
    static MatterManager mgr;
    return mgr;
}

void MatterManager::begin() {
    // Check persisted commissioned flag (stubbed)
    commissioned = false;
    state = commissioned ? MatterState::COMMISSIONED : MatterState::UNCOMMISSIONED;
    ESP_LOGI(TAG, "Matter stub init: commissioned=%d", commissioned);
}

void MatterManager::scheduleCommissioningWindowTimeout() {
    if (commissioningTimer) {
        esp_timer_stop(commissioningTimer);
        esp_timer_delete(commissioningTimer);
        commissioningTimer = nullptr;
    }
    const esp_timer_create_args_t args = {
        .callback = &commissioning_timeout_cb,
        .arg = nullptr,
        .dispatch_method = ESP_TIMER_TASK,
        .name = "matter_comm_window",
        .skip_unhandled_events = false
    };
    esp_timer_create(&args, &commissioningTimer);
    // 3 minutes commissioning window
    esp_timer_start_once(commissioningTimer, 3 * 60 * 1000000ULL);
}

void MatterManager::startCommissioning() {
    ESP_LOGI(TAG, "Start commissioning window (stub)");
    state = MatterState::COMMISSIONING;
    scheduleCommissioningWindowTimeout();
    // TODO: open esp-matter commissioning window
}

void MatterManager::onCommissioningTimeout() {
    ESP_LOGI(TAG, "Commissioning window timed out");
    state = commissioned ? MatterState::COMMISSIONED : MatterState::UNCOMMISSIONED;
    if (commissioningTimer) {
        esp_timer_stop(commissioningTimer);
        esp_timer_delete(commissioningTimer);
        commissioningTimer = nullptr;
    }
}

static void commissioning_timeout_cb(void* arg) {
    MatterManager::instance().onCommissioningTimeout();
}

void MatterManager::factoryReset() {
    ESP_LOGW(TAG, "Factory reset requested");
    // TODO: esp_matter_factory_reset() when linked
    esp_wifi_restore();
    nvs_flash_erase();
    esp_restart();
}

bool MatterManager::isCommissioned() const {
    return commissioned;
}

MatterState MatterManager::getState() const {
    return state;
}

const char* MatterManager::getQrCode() const { return DEFAULT_QR; }
const char* MatterManager::getManualCode() const { return DEFAULT_MANUAL; }
int MatterManager::getPinCode() const { return DEFAULT_PIN; }
int MatterManager::getDiscriminator() const { return DEFAULT_DISC; }
int MatterManager::getVid() const { return DEFAULT_VID; }
int MatterManager::getPid() const { return DEFAULT_PID; }

void MatterManager::markCommissioned() {
    commissioned = true;
    state = MatterState::COMMISSIONED;
    if (commissioningTimer) {
        esp_timer_stop(commissioningTimer);
        esp_timer_delete(commissioningTimer);
        commissioningTimer = nullptr;
    }
}
#endif

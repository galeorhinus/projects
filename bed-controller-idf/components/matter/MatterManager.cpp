#include "MatterManager.h"
#include "BedService.h"
#include "esp_log.h"
#include "esp_wifi.h"
#include "nvs_flash.h"
#include "nvs.h"
#include "esp_matter.h"
#include "esp_matter_attribute.h"
#include "esp_matter_endpoint.h"

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
using namespace esp_matter;

static node_t *s_node = nullptr;

static void app_event_cb(const chip::DeviceLayer::ChipDeviceEvent *event, intptr_t)
{
    if (event->Type == chip::DeviceLayer::DeviceEventType::kCommissioningComplete) {
        ESP_LOGI(TAG, "Matter commissioning complete");
        MatterManager::instance().markCommissioned();
    } else if (event->Type == chip::DeviceLayer::DeviceEventType::kCommissioningWindowOpened) {
        ESP_LOGI(TAG, "Matter commissioning window opened");
    } else if (event->Type == chip::DeviceLayer::DeviceEventType::kCommissioningWindowClosed) {
        ESP_LOGI(TAG, "Matter commissioning window closed");
    }
}

MatterManager& MatterManager::instance() {
    static MatterManager mgr;
    return mgr;
}

void MatterManager::begin() {
    // Check persisted commissioned flag (stubbed)
    commissioned = false;
    state = commissioned ? MatterState::COMMISSIONED : MatterState::UNCOMMISSIONED;
    ESP_LOGI(TAG, "Matter init: commissioned=%d", commissioned);

    node::config_t node_config;
    // Provisioning-only: rely on root node + network commissioning cluster on endpoint 0
    s_node = node::create(&node_config, nullptr, nullptr);
    if (!s_node) {
        ESP_LOGE(TAG, "Failed to create Matter node");
        return;
    }

    esp_err_t err = esp_matter::start(app_event_cb);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "esp_matter start failed: %d", err);
        return;
    }

    state = MatterState::COMMISSIONING;
    scheduleCommissioningWindowTimeout();
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

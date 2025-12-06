#include "BedService.h"
#include "esp_log.h"

static const char* TAG = "BedService";

BedService& BedService::instance() {
    static BedService svc;
    return svc;
}

void BedService::begin(BedDriver* drv) {
    driver = drv;
    if (!driver) {
        ESP_LOGE(TAG, "No driver bound");
        return;
    }
    driver->begin();
}

void BedService::stop() { if (driver) driver->stop(); }
void BedService::moveHead(const std::string& dir) { if (driver) driver->moveHead(dir); }
void BedService::moveFoot(const std::string& dir) { if (driver) driver->moveFoot(dir); }
void BedService::moveAll(const std::string& dir) { if (driver) driver->moveAll(dir); }
int32_t BedService::setTarget(int32_t headMs, int32_t footMs) { return driver ? driver->setTarget(headMs, footMs) : 0; }

void BedService::getLiveStatus(int32_t &headMs, int32_t &footMs) { if (driver) driver->getLiveStatus(headMs, footMs); }
void BedService::getLimits(int32_t &headMaxMs, int32_t &footMaxMs) { if (driver) driver->getLimits(headMaxMs, footMaxMs); }
void BedService::setLimits(int32_t headMaxMs, int32_t footMaxMs) { if (driver) driver->setLimits(headMaxMs, footMaxMs); }

int32_t BedService::getSavedPos(const char* key, int32_t def) { return driver ? driver->getSavedPos(key, def) : def; }
void BedService::setSavedPos(const char* key, int32_t val) { if (driver) driver->setSavedPos(key, val); }
std::string BedService::getSavedLabel(const char* key, const char* def) { return driver ? driver->getSavedLabel(key, def) : std::string(def); }
void BedService::setSavedLabel(const char* key, const std::string& val) { if (driver) driver->setSavedLabel(key, val); }

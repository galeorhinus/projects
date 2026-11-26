#pragma once
#include "BedDriver.h"
#include <string>

// Thin abstraction so Matter/HTTP/UI can share the same control surface.
class BedService {
public:
    static BedService& instance();

    void begin(BedDriver* driver);

    // Movement / presets
    void stop();
    void moveHead(const std::string& dir);
    void moveFoot(const std::string& dir);
    void moveAll(const std::string& dir);
    int32_t setTarget(int32_t headMs, int32_t footMs);

    // State
    void getLiveStatus(int32_t &headMs, int32_t &footMs);
    void getLimits(int32_t &headMaxMs, int32_t &footMaxMs);
    void setLimits(int32_t headMaxMs, int32_t footMaxMs);

    int32_t getSavedPos(const char* key, int32_t def);
    void setSavedPos(const char* key, int32_t val);
    std::string getSavedLabel(const char* key, const char* def);
    void setSavedLabel(const char* key, const std::string& val);

private:
    BedService() = default;
    BedDriver* driver = nullptr;
};

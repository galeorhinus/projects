#pragma once
#include <string>

// Abstract interface so different hardware backends (relay, WL101/102, mock)
// can be swapped without changing higher layers.
class BedDriver {
public:
    virtual ~BedDriver() = default;

    virtual void begin() = 0;
    virtual void update() = 0;

    virtual void stop() = 0;
    virtual void moveHead(std::string dir) = 0;
    virtual void moveFoot(std::string dir) = 0;
    virtual void moveAll(std::string dir) = 0;
    virtual int32_t setTarget(int32_t head, int32_t foot) = 0;

    virtual void getLiveStatus(int32_t &head, int32_t &foot) = 0;

    virtual int32_t getSavedPos(const char* key, int32_t defaultVal) = 0;
    virtual void setSavedPos(const char* key, int32_t val) = 0;

    virtual std::string getSavedLabel(const char* key, const char* defaultVal) = 0;
    virtual void setSavedLabel(const char* key, std::string val) = 0;

    // --- Limits ---
    virtual void getLimits(int32_t &headMaxMs, int32_t &footMaxMs) = 0;
    virtual void setLimits(int32_t headMaxMs, int32_t footMaxMs) = 0;
};

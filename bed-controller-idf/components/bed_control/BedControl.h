#pragma once
#include <string>
#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "nvs_flash.h"
#include "nvs.h"
#include "driver/gpio.h"
#include "BedDriver.h"

struct BedState {
    int32_t currentHeadPosMs;
    int32_t currentFootPosMs;
    int32_t headMaxMs;
    int32_t footMaxMs;
    int64_t headStartTime;
    int64_t footStartTime;
    std::string headDir; 
    std::string footDir; 
    int32_t headTargetDuration;
    int32_t footTargetDuration;
    bool isPresetActive;
    int optoStable[4];
    int optoCounter[4];
    int optoLastRaw[4];
    int64_t remoteLastMs;
    std::string remoteHeadDir;
    std::string remoteFootDir;
    int64_t remoteEventMs;
    int32_t remoteDebounceMs;
    int8_t remoteOptoIdx;
    int32_t headDuty;
    int32_t headDutyTarget;
    int32_t footDuty;
    int32_t footDutyTarget;
};

class BedControl : public BedDriver {
public:
    void begin() override;
    void update() override; 

    void stop() override;
    void moveHead(std::string dir) override;
    void moveFoot(std::string dir) override;
    void moveAll(std::string dir) override;
    int32_t setTarget(int32_t head, int32_t foot) override;

    void getLiveStatus(int32_t &head, int32_t &foot) override;
    
    int32_t getSavedPos(const char* key, int32_t defaultVal) override;
    void setSavedPos(const char* key, int32_t val) override;

    // --- NEW: String Handling ---
    std::string getSavedLabel(const char* key, const char* defaultVal) override;
    void setSavedLabel(const char* key, std::string val) override;

    // Limits
    void getLimits(int32_t &headMaxMs, int32_t &footMaxMs) override;
    void setLimits(int32_t headMaxMs, int32_t footMaxMs) override;
    void getMotionDirs(std::string &headDir, std::string &footDir) override;
    void getOptoStates(int &o1, int &o2, int &o3, int &o4) override;
    void getRemoteEventInfo(int64_t &eventMs, int32_t &debounceMs, int8_t &optoIdx) override;

private:
    BedState state;
    SemaphoreHandle_t mutex;
    nvs_handle_t nvsHandle;

    void initGPIO();
    void initPWM();
    void initNVS();
    void initFactoryDefaults();
    void loadLimits();
    
    void setLedColor(uint8_t r, uint8_t g, uint8_t b);
    void stopHardware();
    void syncState();
    void setTransferSwitch(bool active);
    int64_t millis(); 
    int8_t classifyLimit(int32_t pos, int32_t maxVal);
    void logLimitTransitions();
    void initOptoInputs();
    void updateOptoInputs();
};

#pragma once
#include <string>
#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "nvs_flash.h"
#include "nvs.h"
#include "driver/gpio.h"

struct BedState {
    int32_t currentHeadPosMs;
    int32_t currentFootPosMs;
    int64_t headStartTime;
    int64_t footStartTime;
    std::string headDir; 
    std::string footDir; 
    int32_t headTargetDuration;
    int32_t footTargetDuration;
    bool isPresetActive;
};

class BedControl {
public:
    void begin();
    void update(); 

    void stop();
    void moveHead(std::string dir);
    void moveFoot(std::string dir);
    int32_t setTarget(int32_t head, int32_t foot);

    void getLiveStatus(int32_t &head, int32_t &foot);
    
    int32_t getSavedPos(const char* key, int32_t defaultVal);
    void setSavedPos(const char* key, int32_t val);

    // --- NEW: String Handling ---
    std::string getSavedLabel(const char* key, const char* defaultVal);
    void setSavedLabel(const char* key, std::string val);

private:
    BedState state;
    SemaphoreHandle_t mutex;
    nvs_handle_t nvsHandle;

    void initGPIO();
    void initPWM();
    void initNVS();
    void initFactoryDefaults();
    
    void setLedColor(uint8_t r, uint8_t g, uint8_t b);
    void stopHardware();
    void syncState();
    void setTransferSwitch(bool active);
    int64_t millis(); 
};
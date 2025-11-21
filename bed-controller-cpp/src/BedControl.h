#pragma once
#include <Arduino.h>
#include <Preferences.h>
#include <ArduinoJson.h> 
#include "Config.h" // <--- This provides the constants

struct BedState {
    long currentHeadPosMs;
    long currentFootPosMs;
    unsigned long headStartTime;
    unsigned long footStartTime;
    String currentHeadDirection; 
    String currentFootDirection; 
    unsigned long headTargetDuration;
    unsigned long footTargetDuration;
    bool isPresetActive;
};

extern BedState bed;
extern SemaphoreHandle_t bedMutex;
extern Preferences preferences;
extern String activeCommandLog;
extern unsigned long lastSaveTime;

void initBedControl();
void saveState(bool force = false);
void setTransferSwitch(bool active);
void getLivePositionsForUI(long &head, long &foot);
void stopAndSyncMotors();

// Commands
void moveHead(String dir);
void moveFoot(String dir);
long executePresetMovement(long targetHead, long targetFoot);

// LED Control
void setLedColor(int r, int g, int b);

// JSON Helpers
void savePresetData(String slot, String label, DynamicJsonDocument &res);
void resetPresetData(String slot, int defHead, int defFoot, String defLabel, DynamicJsonDocument &res);
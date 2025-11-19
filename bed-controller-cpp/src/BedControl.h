#pragma once
#include <Arduino.h>
#include <Preferences.h>
#include <ArduinoJson.h> // Needed for JSON responses in helper functions
#include "Config.h"

// --- State Structure ---
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

// --- Globals (Shared with Main) ---
extern BedState bed;
extern SemaphoreHandle_t bedMutex;
extern Preferences preferences;
extern String activeCommandLog;
extern unsigned long lastSaveTime;

// --- Function Prototypes ---
void initBedControl();
void saveState(bool force = false);
void setTransferSwitch(bool active);
void getLivePositionsForUI(long &head, long &foot);
void stopAndSyncMotors();

// commands
void moveHead(String dir);
void moveFoot(String dir);
long executePresetMovement(long targetHead, long targetFoot);

// JSON Helpers (Moved here to keep main.cpp clean)
void savePresetData(String slot, String label, DynamicJsonDocument &res);
void resetPresetData(String slot, int defHead, int defFoot, String defLabel, DynamicJsonDocument &res);
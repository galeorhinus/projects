#include "BedControl.h"

// --- Define Globals ---
BedState bed;
SemaphoreHandle_t bedMutex;
Preferences preferences;
String activeCommandLog = "IDLE";
unsigned long lastSaveTime = 0;

void initFactoryDefaults() {
    if (!preferences.isKey("zg_label")) {
        if (DEBUG_LEVEL >= 1) Serial.println(">>> FIRST BOOT DETECTED: Saving Factory Defaults...");
        preferences.putString("zg_label", "Zero G");
        preferences.putString("snore_label", "Anti-Snore");
        preferences.putString("legs_label", "Legs Up");
        preferences.putString("p1_label", "P1");
        preferences.putString("p2_label", "P2");
        preferences.putInt("zg_head", 10000);    preferences.putInt("zg_foot", 40000);
        preferences.putInt("snore_head", 10000); preferences.putInt("snore_foot", 0);
        preferences.putInt("legs_head", 0);      preferences.putInt("legs_foot", 43000);
        preferences.putInt("p1_head", 0);        preferences.putInt("p1_foot", 0);
        preferences.putInt("p2_head", 0);        preferences.putInt("p2_foot", 0);
        if (DEBUG_LEVEL >= 1) Serial.println(">>> Defaults saved.");
    }
}

void initBedControl() {
    bedMutex = xSemaphoreCreateMutex();

    pinMode(HEAD_UP_PIN, OUTPUT); pinMode(HEAD_DOWN_PIN, OUTPUT);
    pinMode(FOOT_UP_PIN, OUTPUT); pinMode(FOOT_DOWN_PIN, OUTPUT);
    pinMode(TRANSFER_PIN_1, OUTPUT); pinMode(TRANSFER_PIN_2, OUTPUT);
    pinMode(TRANSFER_PIN_3, OUTPUT); pinMode(TRANSFER_PIN_4, OUTPUT);
    
    // Ensure OFF state
    digitalWrite(HEAD_UP_PIN, RELAY_OFF); digitalWrite(HEAD_DOWN_PIN, RELAY_OFF);
    digitalWrite(FOOT_UP_PIN, RELAY_OFF); digitalWrite(FOOT_DOWN_PIN, RELAY_OFF);
    setTransferSwitch(false);

    preferences.begin("bed_data", false);
    initFactoryDefaults();
    
    bed.currentHeadPosMs = preferences.getInt("headPos", 0);
    bed.currentFootPosMs = preferences.getInt("footPos", 0);
    
    if (DEBUG_LEVEL >= 1) {
        Serial.print("Loaded state: H="); Serial.print(bed.currentHeadPosMs);
        Serial.print(" F="); Serial.println(bed.currentFootPosMs);
    }
}

void saveState(bool force) {
    if (!force && (millis() - lastSaveTime < THROTTLE_SAVE_MS)) return;
    preferences.putInt("headPos", bed.currentHeadPosMs);
    preferences.putInt("footPos", bed.currentFootPosMs);
    lastSaveTime = millis();
}

void setTransferSwitch(bool active) {
    int state = active ? RELAY_ON : RELAY_OFF;
    digitalWrite(TRANSFER_PIN_1, state); digitalWrite(TRANSFER_PIN_2, state);
    digitalWrite(TRANSFER_PIN_3, state); digitalWrite(TRANSFER_PIN_4, state);
}

void getLivePositionsForUI(long &head, long &foot) {
    unsigned long now = millis();
    head = bed.currentHeadPosMs;
    foot = bed.currentFootPosMs;

    if (bed.headStartTime != 0 && bed.currentHeadDirection != "STOPPED") {
        long elapsed = now - bed.headStartTime;
        if (bed.currentHeadDirection == "UP") head += elapsed; else head -= elapsed;
        if (head > HEAD_MAX_MS) head = HEAD_MAX_MS; if (head < 0) head = 0;
    }
    if (bed.footStartTime != 0 && bed.currentFootDirection != "STOPPED") {
        long elapsed = now - bed.footStartTime;
        if (bed.currentFootDirection == "UP") foot += elapsed; else foot -= elapsed;
        if (foot > FOOT_MAX_MS) foot = FOOT_MAX_MS; if (foot < 0) foot = 0;
    }
}

void stopAndSyncMotors() {
    unsigned long now = millis();
    if (DEBUG_LEVEL >= 2) Serial.println(">>> DEBUG: stopAndSyncMotors() triggered.");

    digitalWrite(HEAD_UP_PIN, RELAY_OFF); digitalWrite(HEAD_DOWN_PIN, RELAY_OFF);
    digitalWrite(FOOT_UP_PIN, RELAY_OFF); digitalWrite(FOOT_DOWN_PIN, RELAY_OFF);

    if (bed.headStartTime != 0 && bed.currentHeadDirection != "STOPPED") {
        long elapsed = now - bed.headStartTime;
        if (bed.currentHeadDirection == "UP") bed.currentHeadPosMs += elapsed; else bed.currentHeadPosMs -= elapsed;
        if (bed.currentHeadPosMs > HEAD_MAX_MS) bed.currentHeadPosMs = HEAD_MAX_MS;
        if (bed.currentHeadPosMs < 0) bed.currentHeadPosMs = 0;
        bed.headStartTime = 0; bed.currentHeadDirection = "STOPPED";
    }

    if (bed.footStartTime != 0 && bed.currentFootDirection != "STOPPED") {
        long elapsed = now - bed.footStartTime;
        if (bed.currentFootDirection == "UP") bed.currentFootPosMs += elapsed; else bed.currentFootPosMs -= elapsed;
        if (bed.currentFootPosMs > FOOT_MAX_MS) bed.currentFootPosMs = FOOT_MAX_MS;
        if (bed.currentFootPosMs < 0) bed.currentFootPosMs = 0;
        bed.footStartTime = 0; bed.currentFootDirection = "STOPPED";
    }

    bed.isPresetActive = false;
    activeCommandLog = "IDLE";
    setTransferSwitch(false);
    saveState(true); 
    if (DEBUG_LEVEL >= 2) Serial.println(">>> DEBUG: stopAndSyncMotors() Finished. Saved to flash.");
}

void moveHead(String dir) {
    stopAndSyncMotors(); 
    activeCommandLog = "HEAD_" + dir;
    setTransferSwitch(true);
    
    bed.headStartTime = millis();
    bed.currentHeadDirection = dir;
    bed.isPresetActive = false; 

    if (dir == "UP") { digitalWrite(HEAD_DOWN_PIN, RELAY_OFF); digitalWrite(HEAD_UP_PIN, RELAY_ON); }
    else { digitalWrite(HEAD_UP_PIN, RELAY_OFF); digitalWrite(HEAD_DOWN_PIN, RELAY_ON); }
}

void moveFoot(String dir) {
    stopAndSyncMotors(); 
    activeCommandLog = "FOOT_" + dir;
    setTransferSwitch(true);

    bed.footStartTime = millis();
    bed.currentFootDirection = dir;
    bed.isPresetActive = false;

    if (dir == "UP") { digitalWrite(FOOT_DOWN_PIN, RELAY_OFF); digitalWrite(FOOT_UP_PIN, RELAY_ON); }
    else { digitalWrite(FOOT_UP_PIN, RELAY_OFF); digitalWrite(FOOT_DOWN_PIN, RELAY_ON); }
}

long executePresetMovement(long targetHead, long targetFoot) {
    if (DEBUG_LEVEL >= 2) Serial.printf(">>> DEBUG: Executing Preset. Target H: %ld, Target F: %ld\n", targetHead, targetFoot);
    stopAndSyncMotors(); 
    setTransferSwitch(true);
    
    long currentHead = bed.currentHeadPosMs;
    long currentFoot = bed.currentFootPosMs;
    long headDiff = targetHead - currentHead;
    long footDiff = targetFoot - currentFoot;
    unsigned long now = millis();
    long maxDuration = 0;

    if (abs(headDiff) > 100) { 
        bed.headStartTime = now;
        bed.headTargetDuration = abs(headDiff);
        if (targetHead == 0 || targetHead == HEAD_MAX_MS) bed.headTargetDuration += SYNC_EXTRA_MS;
        if (bed.headTargetDuration > maxDuration) maxDuration = bed.headTargetDuration;

        if (headDiff > 0) { bed.currentHeadDirection = "UP"; digitalWrite(HEAD_DOWN_PIN, RELAY_OFF); digitalWrite(HEAD_UP_PIN, RELAY_ON); }
        else { bed.currentHeadDirection = "DOWN"; digitalWrite(HEAD_UP_PIN, RELAY_OFF); digitalWrite(HEAD_DOWN_PIN, RELAY_ON); }
    }

    if (abs(footDiff) > 100) {
        bed.footStartTime = now;
        bed.footTargetDuration = abs(footDiff);
        if (targetFoot == 0 || targetFoot == FOOT_MAX_MS) bed.footTargetDuration += SYNC_EXTRA_MS;
        if (bed.footTargetDuration > maxDuration) maxDuration = bed.footTargetDuration;

        if (footDiff > 0) { bed.currentFootDirection = "UP"; digitalWrite(FOOT_DOWN_PIN, RELAY_OFF); digitalWrite(FOOT_UP_PIN, RELAY_ON); }
        else { bed.currentFootDirection = "DOWN"; digitalWrite(FOOT_UP_PIN, RELAY_OFF); digitalWrite(FOOT_DOWN_PIN, RELAY_ON); }
    }

    if (maxDuration > 0) bed.isPresetActive = true;
    else setTransferSwitch(false);
    
    return maxDuration;
}

void savePresetData(String slot, String label, DynamicJsonDocument &res) {
    stopAndSyncMotors(); 
    preferences.putInt((slot + "_head").c_str(), bed.currentHeadPosMs);
    preferences.putInt((slot + "_foot").c_str(), bed.currentFootPosMs);
    if (label.length() > 0) preferences.putString((slot + "_label").c_str(), label);
    res["saved_pos"] = slot;
    res[slot + "_head"] = bed.currentHeadPosMs;
    res[slot + "_foot"] = bed.currentFootPosMs;
    res[slot + "_label"] = preferences.getString((slot + "_label").c_str(), "Preset");
}

void resetPresetData(String slot, int defHead, int defFoot, String defLabel, DynamicJsonDocument &res) {
    preferences.putInt((slot + "_head").c_str(), defHead);
    preferences.putInt((slot + "_foot").c_str(), defFoot);
    preferences.putString((slot + "_label").c_str(), defLabel);
    res["reset"] = slot;
    res[slot + "_head"] = defHead;
    res[slot + "_foot"] = defFoot;
    res[slot + "_label"] = defLabel;
}
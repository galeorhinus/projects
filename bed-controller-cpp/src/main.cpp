#include <Arduino.h>
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h>
#include <LittleFS.h>
#include <Preferences.h>
#include <time.h>
#include <DNSServer.h>          
#include <ESPAsyncWiFiManager.h> 
#include <ESPmDNS.h>             

// ==========================================
//               CONFIGURATION
// ==========================================

// --- DEBUG CONTROL ---
#define DEBUG_LEVEL 1

// --- GPIO Definitions ---
#define HEAD_UP_PIN    22
#define HEAD_DOWN_PIN  23
#define FOOT_UP_PIN    18
#define FOOT_DOWN_PIN  19

#define TRANSFER_PIN_1 32
#define TRANSFER_PIN_2 33
#define TRANSFER_PIN_3 25
#define TRANSFER_PIN_4 26

// --- Logic Constants ---
#define RELAY_ON  LOW   
#define RELAY_OFF HIGH

const int HEAD_MAX_MS = 28000;
const int FOOT_MAX_MS = 43000;
const int THROTTLE_SAVE_MS = 2000;
const int SYNC_EXTRA_MS = 10000; 

// ==========================================
//               GLOBAL STATE
// ==========================================

AsyncWebServer server(80);
DNSServer dns; 
AsyncWiFiManager wifiManager(&server, &dns); 

Preferences preferences;

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

BedState bed;
unsigned long lastSaveTime = 0;
unsigned long bootEpoch = 0;
String activeCommandLog = "IDLE"; 
SemaphoreHandle_t bedMutex;

// --- NEW: Global variable to hold branding HTML in memory ---
String brandingHTML = ""; 

// ==========================================
//            HELPER FUNCTIONS
// ==========================================

void saveState(bool force = false) {
    if (!force && (millis() - lastSaveTime < THROTTLE_SAVE_MS)) return;
    preferences.putInt("headPos", bed.currentHeadPosMs);
    preferences.putInt("footPos", bed.currentFootPosMs);
    lastSaveTime = millis();
}

void setTransferSwitch(bool active) {
    int state = active ? RELAY_ON : RELAY_OFF;
    digitalWrite(TRANSFER_PIN_1, state);
    digitalWrite(TRANSFER_PIN_2, state);
    digitalWrite(TRANSFER_PIN_3, state);
    digitalWrite(TRANSFER_PIN_4, state);
}

void getLivePositionsForUI(long &head, long &foot) {
    unsigned long now = millis();
    head = bed.currentHeadPosMs;
    foot = bed.currentFootPosMs;

    if (bed.headStartTime != 0 && bed.currentHeadDirection != "STOPPED") {
        long elapsed = now - bed.headStartTime;
        if (bed.currentHeadDirection == "UP") head += elapsed;
        else head -= elapsed;
        if (head > HEAD_MAX_MS) head = HEAD_MAX_MS;
        if (head < 0) head = 0;
    }

    if (bed.footStartTime != 0 && bed.currentFootDirection != "STOPPED") {
        long elapsed = now - bed.footStartTime;
        if (bed.currentFootDirection == "UP") foot += elapsed;
        else foot -= elapsed;
        if (foot > FOOT_MAX_MS) foot = FOOT_MAX_MS;
        if (foot < 0) foot = 0;
    }
}

void stopAndSyncMotors() {
    unsigned long now = millis();
    if (DEBUG_LEVEL >= 2) Serial.println(">>> DEBUG: stopAndSyncMotors() triggered.");

    digitalWrite(HEAD_UP_PIN, RELAY_OFF);
    digitalWrite(HEAD_DOWN_PIN, RELAY_OFF);
    digitalWrite(FOOT_UP_PIN, RELAY_OFF);
    digitalWrite(FOOT_DOWN_PIN, RELAY_OFF);

    if (bed.headStartTime != 0 && bed.currentHeadDirection != "STOPPED") {
        long elapsed = now - bed.headStartTime;
        if (bed.currentHeadDirection == "UP") bed.currentHeadPosMs += elapsed;
        else bed.currentHeadPosMs -= elapsed;
        if (bed.currentHeadPosMs > HEAD_MAX_MS) bed.currentHeadPosMs = HEAD_MAX_MS;
        if (bed.currentHeadPosMs < 0) bed.currentHeadPosMs = 0;
        bed.headStartTime = 0;
        bed.currentHeadDirection = "STOPPED";
    }

    if (bed.footStartTime != 0 && bed.currentFootDirection != "STOPPED") {
        long elapsed = now - bed.footStartTime;
        if (bed.currentFootDirection == "UP") bed.currentFootPosMs += elapsed;
        else bed.currentFootPosMs -= elapsed;
        if (bed.currentFootPosMs > FOOT_MAX_MS) bed.currentFootPosMs = FOOT_MAX_MS;
        if (bed.currentFootPosMs < 0) bed.currentFootPosMs = 0;
        bed.footStartTime = 0;
        bed.currentFootDirection = "STOPPED";
    }

    bed.isPresetActive = false;
    activeCommandLog = "IDLE";
    setTransferSwitch(false);
    saveState(true); 
    if (DEBUG_LEVEL >= 2) Serial.println(">>> DEBUG: stopAndSyncMotors() Finished. Saved to flash.");
}

// ==========================================
//           MOVEMENT LOGIC
// ==========================================

void moveHead(String dir) {
    stopAndSyncMotors(); 
    activeCommandLog = "HEAD_" + dir;
    setTransferSwitch(true);
    
    bed.headStartTime = millis();
    bed.currentHeadDirection = dir;
    bed.isPresetActive = false; 

    if (dir == "UP") {
        digitalWrite(HEAD_DOWN_PIN, RELAY_OFF);
        digitalWrite(HEAD_UP_PIN, RELAY_ON);
    } else {
        digitalWrite(HEAD_UP_PIN, RELAY_OFF);
        digitalWrite(HEAD_DOWN_PIN, RELAY_ON);
    }
}

void moveFoot(String dir) {
    stopAndSyncMotors(); 
    activeCommandLog = "FOOT_" + dir;
    setTransferSwitch(true);

    bed.footStartTime = millis();
    bed.currentFootDirection = dir;
    bed.isPresetActive = false;

    if (dir == "UP") {
        digitalWrite(FOOT_DOWN_PIN, RELAY_OFF);
        digitalWrite(FOOT_UP_PIN, RELAY_ON);
    } else {
        digitalWrite(FOOT_UP_PIN, RELAY_OFF);
        digitalWrite(FOOT_DOWN_PIN, RELAY_ON);
    }
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

        if (headDiff > 0) {
            bed.currentHeadDirection = "UP";
            digitalWrite(HEAD_DOWN_PIN, RELAY_OFF);
            digitalWrite(HEAD_UP_PIN, RELAY_ON);
        } else {
            bed.currentHeadDirection = "DOWN";
            digitalWrite(HEAD_UP_PIN, RELAY_OFF);
            digitalWrite(HEAD_DOWN_PIN, RELAY_ON);
        }
    }

    if (abs(footDiff) > 100) {
        bed.footStartTime = now;
        bed.footTargetDuration = abs(footDiff);
        if (targetFoot == 0 || targetFoot == FOOT_MAX_MS) bed.footTargetDuration += SYNC_EXTRA_MS;
        if (bed.footTargetDuration > maxDuration) maxDuration = bed.footTargetDuration;

        if (footDiff > 0) {
            bed.currentFootDirection = "UP";
            digitalWrite(FOOT_DOWN_PIN, RELAY_OFF);
            digitalWrite(FOOT_UP_PIN, RELAY_ON);
        } else {
            bed.currentFootDirection = "DOWN";
            digitalWrite(FOOT_UP_PIN, RELAY_OFF);
            digitalWrite(FOOT_DOWN_PIN, RELAY_ON);
        }
    }

    if (maxDuration > 0) bed.isPresetActive = true;
    else setTransferSwitch(false);
    
    return maxDuration;
}

// ==========================================
//           JSON API HANDLERS
// ==========================================

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

String handleBedCommand(String jsonStr) {
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, jsonStr);
    if (error) return "{\"error\":\"Invalid JSON\"}";

    String cmd = doc["cmd"];
    String labelArg = doc["label"] | ""; 
    DynamicJsonDocument res(2048); 
    long maxWait = 0;

    // MUTEX LOCK
    if (xSemaphoreTake(bedMutex, portMAX_DELAY)) {
        
        if (cmd == "STOP") stopAndSyncMotors();
        else if (cmd == "RESET_NETWORK") {
             wifiManager.resetSettings();
             ESP.restart();
        }
        else if (cmd == "HEAD_UP") moveHead("UP");
        else if (cmd == "HEAD_DOWN") moveHead("DOWN");
        else if (cmd == "FOOT_UP") moveFoot("UP");
        else if (cmd == "FOOT_DOWN") moveFoot("DOWN");
        else if (cmd == "ALL_UP") {
            maxWait = executePresetMovement(HEAD_MAX_MS, FOOT_MAX_MS);
            if (maxWait > 0) activeCommandLog = "ALL_UP";
        }
        else if (cmd == "ALL_DOWN") {
            maxWait = executePresetMovement(0, 0);
            if (maxWait > 0) activeCommandLog = "ALL_DOWN";
        }
        else if (cmd == "FLAT") {
            maxWait = executePresetMovement(0, 0);
            if (maxWait > 0) activeCommandLog = "FLAT";
        }
        else if (cmd == "MAX") {
            maxWait = executePresetMovement(HEAD_MAX_MS, FOOT_MAX_MS);
            if (maxWait > 0) activeCommandLog = "MAX";
        }
        else if (cmd == "ZERO_G") {
            maxWait = executePresetMovement(preferences.getInt("zg_head", 10000), preferences.getInt("zg_foot", 40000));
            if (maxWait > 0) activeCommandLog = "ZERO_G";
        }
        else if (cmd == "ANTI_SNORE") {
            maxWait = executePresetMovement(preferences.getInt("snore_head", 10000), preferences.getInt("snore_foot", 0));
            if (maxWait > 0) activeCommandLog = "ANTI_SNORE";
        }
        else if (cmd == "LEGS_UP") {
            maxWait = executePresetMovement(preferences.getInt("legs_head", 0), preferences.getInt("legs_foot", 43000));
            if (maxWait > 0) activeCommandLog = "LEGS_UP";
        }
        else if (cmd == "P1") {
            maxWait = executePresetMovement(preferences.getInt("p1_head", 0), preferences.getInt("p1_foot", 0));
            if (maxWait > 0) activeCommandLog = "P1";
        }
        else if (cmd == "P2") {
            maxWait = executePresetMovement(preferences.getInt("p2_head", 0), preferences.getInt("p2_foot", 0));
            if (maxWait > 0) activeCommandLog = "P2";
        }
        // Sets & Resets
        else if (cmd == "SET_P1_POS") savePresetData("p1", "", res);
        else if (cmd == "SET_P2_POS") savePresetData("p2", "", res);
        else if (cmd == "SET_ZG_POS") savePresetData("zg", "", res);
        else if (cmd == "SET_SNORE_POS") savePresetData("snore", "", res);
        else if (cmd == "SET_LEGS_POS") savePresetData("legs", "", res);
        else if (cmd == "SET_P1_LABEL") savePresetData("p1", labelArg, res);
        else if (cmd == "SET_P2_LABEL") savePresetData("p2", labelArg, res);
        else if (cmd == "SET_ZG_LABEL") savePresetData("zg", labelArg, res);
        else if (cmd == "SET_SNORE_LABEL") savePresetData("snore", labelArg, res);
        else if (cmd == "SET_LEGS_LABEL") savePresetData("legs", labelArg, res);
        else if (cmd == "RESET_P1")    resetPresetData("p1", 0, 0, "P1", res);
        else if (cmd == "RESET_P2")    resetPresetData("p2", 0, 0, "P2", res);
        else if (cmd == "RESET_ZG")    resetPresetData("zg", 10000, 40000, "Zero G", res);
        else if (cmd == "RESET_SNORE") resetPresetData("snore", 10000, 0, "Anti-Snore", res);
        else if (cmd == "RESET_LEGS")  resetPresetData("legs", 0, 43000, "Legs Up", res);

        long lHead, lFoot;
        getLivePositionsForUI(lHead, lFoot);
        res["headPos"] = String(lHead / 1000.0, 2);
        res["footPos"] = String(lFoot / 1000.0, 2);
        xSemaphoreGive(bedMutex); 
    }
    
    res["bootTime"] = bootEpoch; 
    res["uptime"] = millis() / 1000;
    res["maxWait"] = maxWait;

    String responseStr;
    serializeJson(res, responseStr);
    return responseStr;
}

String getSystemStatus() {
    DynamicJsonDocument res(2048);
    long lHead, lFoot;
    
    if (xSemaphoreTake(bedMutex, portMAX_DELAY)) {
        getLivePositionsForUI(lHead, lFoot);
        xSemaphoreGive(bedMutex);
    }

    res["bootTime"] = bootEpoch;
    res["uptime"] = millis() / 1000;
    res["headPos"] = String(lHead / 1000.0, 2);
    res["footPos"] = String(lFoot / 1000.0, 2);

    String slots[] = {"p1", "p2", "zg", "snore", "legs"};
    String defLabels[] = {"P1", "P2", "Zero G", "Anti-Snore", "Legs Up"};
    
    for(int i=0; i<5; i++) {
        String s = slots[i];
        res[s + "_head"] = preferences.getInt((s + "_head").c_str(), 0);
        res[s + "_foot"] = preferences.getInt((s + "_foot").c_str(), 0);
        res[s + "_label"] = preferences.getString((s + "_label").c_str(), defLabels[i].c_str());
    }
    
    res["zg_head"] = preferences.getInt("zg_head", 10000);
    res["zg_foot"] = preferences.getInt("zg_foot", 40000);
    res["snore_head"] = preferences.getInt("snore_head", 10000);
    res["snore_foot"] = preferences.getInt("snore_foot", 0);
    res["legs_head"] = preferences.getInt("legs_head", 0);
    res["legs_foot"] = preferences.getInt("legs_foot", 43000);

    String responseStr;
    serializeJson(res, responseStr);
    return responseStr;
}

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

// ==========================================
//             MAIN SETUP
// ==========================================

void setup() {
    Serial.begin(115200);
    bedMutex = xSemaphoreCreateMutex();

    // Init GPIO
    pinMode(HEAD_UP_PIN, OUTPUT); pinMode(HEAD_DOWN_PIN, OUTPUT);
    pinMode(FOOT_UP_PIN, OUTPUT); pinMode(FOOT_DOWN_PIN, OUTPUT);
    pinMode(TRANSFER_PIN_1, OUTPUT); pinMode(TRANSFER_PIN_2, OUTPUT);
    pinMode(TRANSFER_PIN_3, OUTPUT); pinMode(TRANSFER_PIN_4, OUTPUT);
    stopAndSyncMotors(); 

    if(!LittleFS.begin(true)) Serial.println("LittleFS Mount Failed");

    preferences.begin("bed_data", false);
    initFactoryDefaults();
    bed.currentHeadPosMs = preferences.getInt("headPos", 0);
    bed.currentFootPosMs = preferences.getInt("footPos", 0);
    
    if (DEBUG_LEVEL >= 1) {
        Serial.print("Loaded state: H="); Serial.print(bed.currentHeadPosMs);
        Serial.print(" F="); Serial.println(bed.currentFootPosMs);
    }
    
    // --- WiFi Manager Setup ---
    wifiManager.setConfigPortalTimeout(180); // 3 minute timeout
    
    // --- NEW: Load Branding from File ---
    File file = LittleFS.open("/provision.html", "r");
    if (file) {
        brandingHTML = file.readString();
        file.close();
        wifiManager.setCustomHeadElement(brandingHTML.c_str());
        if (DEBUG_LEVEL >= 1) Serial.println("Branding HTML loaded from FS.");
    } else {
        Serial.println("Warning: /provision.html not found!");
    }
    
    // wifiManager.resetSettings(); // <--- ENSURE THIS IS COMMENTED OUT

    if (!wifiManager.autoConnect("HomeYantric-Elev8")) {
        Serial.println("Failed to connect and hit timeout. Continuing offline...");
    } else {
        Serial.println("WiFi Connected!");
        Serial.print("IP Address: "); Serial.println(WiFi.localIP());
        
        if (MDNS.begin("elev8")) {
            Serial.println("mDNS responder started. Access at http://elev8.local");
            MDNS.addService("http", "tcp", 80);
        }

        configTime(0, 0, "pool.ntp.org", "time.nist.gov");
        time_t now = time(nullptr);
        int retry = 0;
        while (now < 8 * 3600 * 2 && retry < 20) { delay(500); now = time(nullptr); retry++; }
        bootEpoch = now - (millis() / 1000);
    }

    // Setup Web Server
    server.serveStatic("/", LittleFS, "/").setDefaultFile("index.html");

    server.on("/rpc/Bed.Command", HTTP_POST, [](AsyncWebServerRequest *request){}, NULL, 
    [](AsyncWebServerRequest *request, uint8_t *data, size_t len, size_t index, size_t total){
        String body = "";
        for(size_t i=0; i<len; i++) body += (char)data[i];
        String response = handleBedCommand(body);
        request->send(200, "application/json", response);
    });
    
    server.on("/rpc/Bed.Status", HTTP_POST, [](AsyncWebServerRequest *request){
         String response = getSystemStatus(); 
         request->send(200, "application/json", response);
    });

    server.begin();
    if (DEBUG_LEVEL >= 1) Serial.println("HTTP Server started");
}

void loop() {
    unsigned long logTime = millis();
    static unsigned long lastLogTime = 0;

    if (DEBUG_LEVEL >= 1) {
        if (logTime - lastLogTime >= 1000) {
            lastLogTime = logTime;
            long liveHead, liveFoot;
            if (xSemaphoreTake(bedMutex, portMAX_DELAY)) {
                getLivePositionsForUI(liveHead, liveFoot);
                xSemaphoreGive(bedMutex);
            }
            Serial.printf("[STATUS] Time:%lu | Cmd:%s | H:%ld F:%ld\n", 
                logTime / 1000, activeCommandLog.c_str(), liveHead, liveFoot);
        }
    }

    if (xSemaphoreTake(bedMutex, portMAX_DELAY)) {
        unsigned long now = millis(); 

        if (bed.isPresetActive) {
            bool headDone = true;
            bool footDone = true;

            if (bed.currentHeadDirection != "STOPPED") {
                unsigned long elapsed = (now >= bed.headStartTime) ? (now - bed.headStartTime) : 0;
                if (elapsed >= bed.headTargetDuration) {
                    digitalWrite(HEAD_UP_PIN, RELAY_OFF);
                    digitalWrite(HEAD_DOWN_PIN, RELAY_OFF);
                    
                    if (DEBUG_LEVEL >= 2) Serial.printf(">>> DEBUG: Head Timer Done. Committing %lu ms.\n", bed.headTargetDuration);
                    
                    if (bed.currentHeadDirection == "UP") bed.currentHeadPosMs += bed.headTargetDuration;
                    else bed.currentHeadPosMs -= bed.headTargetDuration;
                    
                    if (bed.currentHeadPosMs > HEAD_MAX_MS) bed.currentHeadPosMs = HEAD_MAX_MS;
                    if (bed.currentHeadPosMs < 0) bed.currentHeadPosMs = 0;

                    bed.currentHeadDirection = "STOPPED";
                    bed.headStartTime = 0; 
                } else {
                    headDone = false; 
                }
            }

            if (bed.currentFootDirection != "STOPPED") {
                unsigned long elapsed = (now >= bed.footStartTime) ? (now - bed.footStartTime) : 0;
                if (elapsed >= bed.footTargetDuration) {
                    digitalWrite(FOOT_UP_PIN, RELAY_OFF);
                    digitalWrite(FOOT_DOWN_PIN, RELAY_OFF);

                    if (DEBUG_LEVEL >= 2) Serial.printf(">>> DEBUG: Foot Timer Done. Committing %lu ms.\n", bed.footTargetDuration);
                    
                    if (bed.currentFootDirection == "UP") bed.currentFootPosMs += bed.footTargetDuration;
                    else bed.currentFootPosMs -= bed.footTargetDuration;

                    if (bed.currentFootPosMs > FOOT_MAX_MS) bed.currentFootPosMs = FOOT_MAX_MS;
                    if (bed.currentFootPosMs < 0) bed.currentFootPosMs = 0;

                    bed.currentFootDirection = "STOPPED";
                    bed.footStartTime = 0;
                } else {
                    footDone = false; 
                }
            }

            if (headDone && footDone) {
                if (DEBUG_LEVEL >= 2) Serial.println(">>> DEBUG: All movements finished. Saving state.");
                stopAndSyncMotors(); 
            }
        }
        xSemaphoreGive(bedMutex); 
    }
}
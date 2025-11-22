#include "NetworkManager.h"
#include "Config.h"
#include <LittleFS.h>
#include <ESPmDNS.h>

// External globals
extern BedState bed; 
extern SemaphoreHandle_t bedMutex; 
extern String activeCommandLog; 
extern Preferences preferences; 

NetworkManager::NetworkManager() : server(80) {}

void NetworkManager::begin() {
    // 1. Filesystem
    if (!LittleFS.begin(true)) Serial.println("! FS Fail !");

    // 2. WiFi (Hardcoded)
    WiFi.mode(WIFI_STA);
    WiFi.setSleep(false);
    WiFi.begin(WIFI_SSID, WIFI_PASS);

    Serial.print("Connecting to "); Serial.println(WIFI_SSID);
    
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) { 
        delay(500); Serial.print("."); attempts++; 
    }
    Serial.println("");

    if (WiFi.status() == WL_CONNECTED) {
        Serial.print("Online! IP: "); Serial.println(WiFi.localIP());
        
        // mDNS & Time
        String host = String(MDNS_HOSTNAME) + "-" + WiFi.macAddress().substring(12);
        host.replace(":", ""); host.toLowerCase();
        if (MDNS.begin(host.c_str())) MDNS.addService("http", "tcp", 80);
        configTime(0, 0, NTP_SERVER_1, NTP_SERVER_2);
    } else {
        Serial.println("Offline Mode.");
    }

    // 3. Web Server
    server.on("/rpc/Bed.Command", HTTP_POST, [](AsyncWebServerRequest *r){}, NULL, 
    [this](AsyncWebServerRequest *r, uint8_t *data, size_t len, size_t idx, size_t tot){
        String body = ""; for(size_t i=0; i<len; i++) body += (char)data[i];
        r->send(200, "application/json", handleBedCommand(body));
    });
    
    server.on("/rpc/Bed.Status", HTTP_POST, [this](AsyncWebServerRequest *r){
         r->send(200, "application/json", getSystemStatus());
    });

    server.serveStatic("/", LittleFS, "/").setDefaultFile("index.html");
    server.onNotFound([](AsyncWebServerRequest *r) { r->send(404, "text/plain", "Not found"); });

    server.begin();
}

String NetworkManager::handleBedCommand(String jsonStr) {
    DynamicJsonDocument doc(1024); deserializeJson(doc, jsonStr);
    String cmd = doc["cmd"]; String label = doc["label"] | "";
    DynamicJsonDocument res(2048); long maxWait = 0;

    if (xSemaphoreTake(bedMutex, portMAX_DELAY)) {
        if (cmd == "STOP") { stopAndSyncMotors(); activeCommandLog = "IDLE"; }
        else if (cmd == "RESET_NETWORK") { ESP.restart(); }
        
        // Movement
        else if (cmd == "HEAD_UP") { moveHead("UP"); activeCommandLog = "HEAD_UP"; }
        else if (cmd == "HEAD_DOWN") { moveHead("DOWN"); activeCommandLog = "HEAD_DOWN"; }
        else if (cmd == "FOOT_UP") { moveFoot("UP"); activeCommandLog = "FOOT_UP"; }
        else if (cmd == "FOOT_DOWN") { moveFoot("DOWN"); activeCommandLog = "FOOT_DOWN"; }
        
        // Fixed Presets
        else if (cmd == "ALL_UP") { maxWait = executePresetMovement(HEAD_MAX_MS, FOOT_MAX_MS); activeCommandLog = "ALL_UP"; }
        else if (cmd == "ALL_DOWN") { maxWait = executePresetMovement(0, 0); activeCommandLog = "ALL_DOWN"; }
        else if (cmd == "FLAT") { maxWait = executePresetMovement(0, 0); activeCommandLog = "FLAT"; }
        else if (cmd == "MAX") { maxWait = executePresetMovement(HEAD_MAX_MS, FOOT_MAX_MS); activeCommandLog = "MAX"; }
        
        // Custom Presets
        else if (cmd == "ZERO_G") { maxWait = executePresetMovement(preferences.getInt("zg_head", 10000), preferences.getInt("zg_foot", 40000)); activeCommandLog = "ZERO_G"; }
        else if (cmd == "ANTI_SNORE") { maxWait = executePresetMovement(preferences.getInt("snore_head", 10000), preferences.getInt("snore_foot", 0)); activeCommandLog = "ANTI_SNORE"; }
        else if (cmd == "LEGS_UP") { maxWait = executePresetMovement(preferences.getInt("legs_head", 0), preferences.getInt("legs_foot", 43000)); activeCommandLog = "LEGS_UP"; }
        else if (cmd == "P1") { maxWait = executePresetMovement(preferences.getInt("p1_head", 0), preferences.getInt("p1_foot", 0)); activeCommandLog = "P1"; }
        else if (cmd == "P2") { maxWait = executePresetMovement(preferences.getInt("p2_head", 0), preferences.getInt("p2_foot", 0)); activeCommandLog = "P2"; }
        
        // Savings & Resets
        else if (cmd.startsWith("SET_") && cmd.endsWith("_POS")) {
            String s = cmd.substring(4, cmd.length()-4); s.toLowerCase(); savePresetData(s, "", res);
        }
        else if (cmd.startsWith("SET_") && cmd.endsWith("_LABEL")) {
            String s = cmd.substring(4, cmd.length()-6); s.toLowerCase(); savePresetData(s, label, res);
        }
        else if (cmd == "RESET_P1") resetPresetData("p1", 0, 0, "P1", res);
        else if (cmd == "RESET_P2") resetPresetData("p2", 0, 0, "P2", res);
        else if (cmd == "RESET_ZG") resetPresetData("zg", 10000, 40000, "Zero G", res);
        else if (cmd == "RESET_SNORE") resetPresetData("snore", 10000, 0, "Anti-Snore", res);
        else if (cmd == "RESET_LEGS") resetPresetData("legs", 0, 43000, "Legs Up", res);
        
        long h, f; getLivePositionsForUI(h, f);
        res["headPos"] = String(h/1000.0, 2); res["footPos"] = String(f/1000.0, 2); res["maxWait"] = maxWait;
        
        if (cmd.startsWith("SET_") || cmd.startsWith("RESET_")) {
            String slot = cmd.substring(4, cmd.indexOf("_", 4)); slot.toLowerCase();
            res["saved_pos"] = slot; 
            res[slot + "_head"] = preferences.getInt((slot+"_head").c_str(), 0);
            res[slot + "_foot"] = preferences.getInt((slot+"_foot").c_str(), 0);
            res[slot + "_label"] = preferences.getString((slot+"_label").c_str(), "Preset");
        }
        xSemaphoreGive(bedMutex);
    }
    String out; serializeJson(res, out); return out;
}

String NetworkManager::getSystemStatus() {
    DynamicJsonDocument res(2048);
    long h, f;
    if (xSemaphoreTake(bedMutex, portMAX_DELAY)) {
        getLivePositionsForUI(h, f);
        xSemaphoreGive(bedMutex);
    }
    
    // Calc boot time on the fly
    time_t now = time(nullptr);
    res["bootTime"] = (now > 10000) ? (now - (millis()/1000)) : 0;
    res["uptime"] = millis() / 1000;
    res["headPos"] = String(h/1000.0, 2);
    res["footPos"] = String(f/1000.0, 2);
    
    String slots[] = {"p1", "p2", "zg", "snore", "legs"};
    String defLabels[] = {"P1", "P2", "Zero G", "Anti-Snore", "Legs Up"};
    for(int i=0; i<5; i++) {
        res[slots[i] + "_head"] = preferences.getInt((slots[i] + "_head").c_str(), 0);
        res[slots[i] + "_foot"] = preferences.getInt((slots[i] + "_foot").c_str(), 0);
        res[slots[i] + "_label"] = preferences.getString((slots[i] + "_label").c_str(), defLabels[i].c_str());
    }
    String out; serializeJson(res, out); return out;
}
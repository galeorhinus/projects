#include "NetworkManager.h"
#include <LittleFS.h>
#include <ESPmDNS.h>
#include <time.h>

// Constructor: Initialize Server (port 80) and WiFiManager
NetworkManager::NetworkManager() : server(80), wifiManager(&server, &dns) {
    bootEpoch = 0;
}

void NetworkManager::begin() {
    // 1. Load Branding
    loadBranding();
    
    // 2. WiFi Manager Config
    wifiManager.setConfigPortalTimeout(WIFI_TIMEOUT);
    
    // 3. Connect
    if (!wifiManager.autoConnect(WIFI_AP_NAME)) {
        Serial.println("WiFi Connect Failed. Continuing offline...");
    } else {
        Serial.println("WiFi Connected! IP: " + WiFi.localIP().toString());
        
        // 4. mDNS
        if (MDNS.begin(MDNS_HOSTNAME)) {
            Serial.println("mDNS responder started: http://" MDNS_HOSTNAME ".local");
            MDNS.addService("http", "tcp", 80);
        }

        // 5. NTP Time
        configTime(0, 0, NTP_SERVER_1, NTP_SERVER_2);
        time_t now = time(nullptr);
        int retry = 0;
        while (now < 8 * 3600 * 2 && retry < 20) { delay(500); now = time(nullptr); retry++; }
        bootEpoch = now - (millis() / 1000);
    }

    // 6. Web Server Routes
    server.serveStatic("/", LittleFS, "/").setDefaultFile("index.html");

    server.on("/rpc/Bed.Command", HTTP_POST, [](AsyncWebServerRequest *request){}, NULL, 
    [this](AsyncWebServerRequest *request, uint8_t *data, size_t len, size_t index, size_t total){
        String body = ""; for(size_t i=0; i<len; i++) body += (char)data[i];
        request->send(200, "application/json", handleBedCommand(body));
    });
    
    server.on("/rpc/Bed.Status", HTTP_POST, [this](AsyncWebServerRequest *request){
         request->send(200, "application/json", getSystemStatus());
    });

    server.begin();
    Serial.println("HTTP Server started");
}

void NetworkManager::loadBranding() {
    if (LittleFS.begin(true)) {
        File file = LittleFS.open("/provision.html", "r");
        if (file) {
            brandingHTML = file.readString();
            file.close();
            wifiManager.setCustomHeadElement(brandingHTML.c_str());
            if (DEBUG_LEVEL >= 1) Serial.println("Branding Loaded.");
        }
    }
}

String NetworkManager::handleBedCommand(String jsonStr) {
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, jsonStr);
    if (error) return "{\"error\":\"Invalid JSON\"}";

    String cmd = doc["cmd"];
    String labelArg = doc["label"] | ""; 
    DynamicJsonDocument res(2048); 
    long maxWait = 0;

    // Acquire Mutex (Defined in BedControl.cpp)
    if (xSemaphoreTake(bedMutex, portMAX_DELAY)) {
        
        if (cmd == "STOP") { stopAndSyncMotors(); activeCommandLog = "IDLE"; }
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

String NetworkManager::getSystemStatus() {
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
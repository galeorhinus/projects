#include "NetworkManager.h"
#include "Config.h"
#include <LittleFS.h>
#include <ESPmDNS.h>
#include <ElegantOTA.h> 
#include <time.h>

// External globals
extern BedState bed; 
extern SemaphoreHandle_t bedMutex; 
extern String activeCommandLog; 
extern Preferences preferences; 

NetworkManager::NetworkManager() : server(80) {
    bootEpoch = 0;
}

void NetworkManager::begin() {
    // --- FIX: START FILESYSTEM ---
    if (!LittleFS.begin(true)) {
        Serial.println("!!! LittleFS Failed to Mount !!!");
    } else {
        Serial.println("LittleFS Mounted.");
    }
    // -----------------------------

    // 1. Setup Radio (Hardcoded Mode)
    WiFi.mode(WIFI_STA);
    WiFi.setSleep(false);
    
    // 2. Connect
    Serial.print("Connecting to WiFi: ");
    Serial.println(WIFI_SSID);
    
    WiFi.begin(WIFI_SSID, WIFI_PASS);

    // 3. Wait for connection (Blocking Loop)
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 40) { // Wait up to 20s
        delay(500);
        Serial.print(".");
        attempts++;
    }
    Serial.println("");

    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("\n!!! WiFi Failed !!!");
        Serial.println("Check credentials in Config.h");
    } else {
        Serial.println("\n--- WIFI CONNECTED ---");
        Serial.print("IP Address: "); Serial.println(WiFi.localIP());
        Serial.print("Signal: "); Serial.println(WiFi.RSSI());

        // 4. Unique Hostname
        String mac = WiFi.macAddress();
        mac.replace(":", ""); 
        String uniqueHost = MDNS_HOSTNAME;
        uniqueHost += "-" + mac.substring(8); 
        uniqueHost.toLowerCase();

        if (MDNS.begin(uniqueHost.c_str())) {
            Serial.print("mDNS responder started: http://");
            Serial.print(uniqueHost);
            Serial.println(".local");
            MDNS.addService("http", "tcp", 80);
        }

        configTime(0, 0, NTP_SERVER_1, NTP_SERVER_2);
        time_t now = time(nullptr);
        int retry = 0;
        while (now < 8 * 3600 * 2 && retry < 20) { delay(500); now = time(nullptr); retry++; }
        bootEpoch = now - (millis() / 1000);
    }

    ElegantOTA.begin(&server);

    server.on("/rpc/Bed.Command", HTTP_POST, [](AsyncWebServerRequest *request){}, NULL, 
    [this](AsyncWebServerRequest *request, uint8_t *data, size_t len, size_t index, size_t total){
        String body = ""; for(size_t i=0; i<len; i++) body += (char)data[i];
        request->send(200, "application/json", handleBedCommand(body));
    });
    
    server.on("/rpc/Bed.Status", HTTP_POST, [this](AsyncWebServerRequest *request){
         request->send(200, "application/json", getSystemStatus());
    });

    server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){ request->send(LittleFS, "/index.html"); });
    server.on("/index.html", HTTP_GET, [](AsyncWebServerRequest *request){ request->send(LittleFS, "/index.html"); });
    server.on("/style.css", HTTP_GET, [](AsyncWebServerRequest *request){ request->send(LittleFS, "/style.css", "text/css"); });
    server.on("/app.js", HTTP_GET, [](AsyncWebServerRequest *request){ request->send(LittleFS, "/app.js", "text/javascript"); });
    server.on("/favicon.png", HTTP_GET, [](AsyncWebServerRequest *request){ request->send(LittleFS, "/favicon.png", "image/png"); });
    server.on("/manifest.json", HTTP_GET, [](AsyncWebServerRequest *request){ request->send(LittleFS, "/manifest.json", "application/json"); });

    server.onNotFound([](AsyncWebServerRequest *request) {
        request->send(404, "text/plain", "Not found");
    });

    server.begin();
    Serial.println("HTTP Server started");
}

String NetworkManager::handleBedCommand(String jsonStr) {
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, jsonStr);
    String cmd = doc["cmd"];
    String label = doc["label"] | "";
    DynamicJsonDocument res(2048);
    long maxWait = 0;

    if (xSemaphoreTake(bedMutex, portMAX_DELAY)) {
        
        if (cmd == "STOP") { stopAndSyncMotors(); activeCommandLog = "IDLE"; }
        else if (cmd == "RESET_NETWORK") { ESP.restart(); } 
        
        else if (cmd == "HEAD_UP") { moveHead("UP"); activeCommandLog = "HEAD_UP"; }
        else if (cmd == "HEAD_DOWN") { moveHead("DOWN"); activeCommandLog = "HEAD_DOWN"; }
        else if (cmd == "FOOT_UP") { moveFoot("UP"); activeCommandLog = "FOOT_UP"; }
        else if (cmd == "FOOT_DOWN") { moveFoot("DOWN"); activeCommandLog = "FOOT_DOWN"; }
        
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
        
        else if (cmd == "SET_P1_POS") savePresetData("p1", "", res);
        else if (cmd == "SET_P2_POS") savePresetData("p2", "", res);
        else if (cmd == "SET_ZG_POS") savePresetData("zg", "", res);
        else if (cmd == "SET_SNORE_POS") savePresetData("snore", "", res);
        else if (cmd == "SET_LEGS_POS") savePresetData("legs", "", res);
        
        else if (cmd == "SET_P1_LABEL") savePresetData("p1", label, res);
        else if (cmd == "SET_P2_LABEL") savePresetData("p2", label, res);
        else if (cmd == "SET_ZG_LABEL") savePresetData("zg", label, res);
        else if (cmd == "SET_SNORE_LABEL") savePresetData("snore", label, res);
        else if (cmd == "SET_LEGS_LABEL") savePresetData("legs", label, res);
        
        else if (cmd == "RESET_P1")    resetPresetData("p1", 0, 0, "P1", res);
        else if (cmd == "RESET_P2")    resetPresetData("p2", 0, 0, "P2", res);
        else if (cmd == "RESET_ZG")    resetPresetData("zg", 10000, 40000, "Zero G", res);
        else if (cmd == "RESET_SNORE") resetPresetData("snore", 10000, 0, "Anti-Snore", res);
        else if (cmd == "RESET_LEGS")  resetPresetData("legs", 0, 43000, "Legs Up", res);
        
        long h, f;
        getLivePositionsForUI(h, f);
        res["headPos"] = String(h/1000.0, 2);
        res["footPos"] = String(f/1000.0, 2);
        res["maxWait"] = maxWait;
        
        if (cmd.startsWith("SET_") || cmd.startsWith("RESET_")) {
            String slot = cmd.substring(4, cmd.indexOf("_", 4));
            slot.toLowerCase();
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

    res["bootTime"] = bootEpoch;
    res["uptime"] = millis() / 1000;
    res["headPos"] = String(h/1000.0, 2);
    res["footPos"] = String(f/1000.0, 2);
    
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
    
    String out; serializeJson(res, out); return out;
}
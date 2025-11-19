#pragma once
#include <Arduino.h>
#include <ESPAsyncWebServer.h>
#include <DNSServer.h>
#include <ESPAsyncWiFiManager.h>
#include <ArduinoJson.h>
#include "BedControl.h" // Needs access to Bed globals (bedMutex, etc)

class NetworkManager {
public:
    NetworkManager(); // Constructor
    void begin();     // Setup WiFi, Server, mDNS
    // No update() needed as AsyncServer handles itself in background

private:
    AsyncWebServer server;
    DNSServer dns;
    AsyncWiFiManager wifiManager;
    
    unsigned long bootEpoch;
    String brandingHTML;

    // Internal helpers
    String handleBedCommand(String jsonStr);
    String getSystemStatus();
    void loadBranding();
};
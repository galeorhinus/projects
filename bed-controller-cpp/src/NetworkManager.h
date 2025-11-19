#pragma once
#include <Arduino.h>
#include <ESPAsyncWebServer.h>
#include <DNSServer.h>
#include <ESPAsyncWiFiManager.h>
#include <ArduinoJson.h>
#include "BedControl.h" // Include so we can call global functions

class NetworkManager {
public:
    NetworkManager(); 
    void begin();     

private:
    AsyncWebServer server;
    DNSServer dns;
    AsyncWiFiManager wifiManager;
    
    unsigned long bootEpoch;
    String brandingHTML;
    String activeCmd; // Moved here from global

    String handleBedCommand(String jsonStr);
    String getSystemStatus();
    void loadBranding();
};
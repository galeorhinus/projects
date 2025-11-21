#pragma once
#include <Arduino.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h>
#include "BedControl.h" 
#include "Config.h"

class NetworkManager {
public:
    NetworkManager(); 
    void begin();     

private:
    AsyncWebServer server;
    unsigned long bootEpoch;
    String activeCmd; 

    // Helpers
    String handleBedCommand(String jsonStr);
    String getSystemStatus();
};
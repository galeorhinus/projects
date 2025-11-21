#include <Arduino.h>
#include <esp_task_wdt.h>
#include "Config.h"
#include "BedControl.h"
#include "NetworkManager.h"

NetworkManager net;

void setup() {
    Serial.begin(115200);
    
    // 1. Init Physics & State
    initBedControl();
    
    // 2. Init Connectivity
    net.begin();
    
    // 3. Watchdog
    esp_task_wdt_init(8, true); 
    esp_task_wdt_add(NULL);
    
    if(DEBUG_LEVEL >= 1) Serial.println("System V1.3 Ready");
}

void loop() {
    // --- FIX: PET THE DOG FIRST ---
    // This ensures the board stays alive even if waiting for a lock
    esp_task_wdt_reset(); 
    // ------------------------------

    unsigned long logTime = millis();
    static unsigned long lastLogTime = 0;

    // --- 1-Second Heartbeat Log ---
    if (DEBUG_LEVEL >= 1) {
        if (logTime - lastLogTime >= 1000) {
            lastLogTime = logTime;
            long liveHead, liveFoot;
            if (xSemaphoreTake(bedMutex, portMAX_DELAY)) {
                getLivePositionsForUI(liveHead, liveFoot);
                xSemaphoreGive(bedMutex);
            }
            // Print IP to confirm connection
            String ip = (WiFi.status() == WL_CONNECTED) ? WiFi.localIP().toString() : "DISCONNECTED";
            Serial.printf("[STATUS] IP:%s | Time:%lu | Cmd:%s | H:%ld F:%ld\n", 
                ip.c_str(), logTime / 1000, activeCommandLog.c_str(), liveHead, liveFoot);
        }
    }

    // --- PHYSICS ENGINE LOOP ---
    if (xSemaphoreTake(bedMutex, portMAX_DELAY)) {
        unsigned long now = millis(); 

        if (bed.isPresetActive) {
            bool headDone = true; bool footDone = true;

            if (bed.currentHeadDirection != "STOPPED") {
                unsigned long elapsed = (now >= bed.headStartTime) ? (now - bed.headStartTime) : 0;
                if (elapsed >= bed.headTargetDuration) {
                    digitalWrite(HEAD_UP_PIN, RELAY_OFF); digitalWrite(HEAD_DOWN_PIN, RELAY_OFF);
                    if (DEBUG_LEVEL >= 2) Serial.printf(">>> DEBUG: Head Timer Done.\n");
                    
                    if (bed.currentHeadDirection == "UP") bed.currentHeadPosMs += bed.headTargetDuration;
                    else bed.currentHeadPosMs -= bed.headTargetDuration;
                    
                    if (bed.currentHeadPosMs > HEAD_MAX_MS) bed.currentHeadPosMs = HEAD_MAX_MS;
                    if (bed.currentHeadPosMs < 0) bed.currentHeadPosMs = 0;
                    bed.currentHeadDirection = "STOPPED"; bed.headStartTime = 0; 
                } else headDone = false; 
            }

            if (bed.currentFootDirection != "STOPPED") {
                unsigned long elapsed = (now >= bed.footStartTime) ? (now - bed.footStartTime) : 0;
                if (elapsed >= bed.footTargetDuration) {
                    digitalWrite(FOOT_UP_PIN, RELAY_OFF); digitalWrite(FOOT_DOWN_PIN, RELAY_OFF);
                    if (DEBUG_LEVEL >= 2) Serial.printf(">>> DEBUG: Foot Timer Done.\n");
                    
                    if (bed.currentFootDirection == "UP") bed.currentFootPosMs += bed.footTargetDuration;
                    else bed.currentFootPosMs -= bed.footTargetDuration;

                    if (bed.currentFootPosMs > FOOT_MAX_MS) bed.currentFootPosMs = FOOT_MAX_MS;
                    if (bed.currentFootPosMs < 0) bed.currentFootPosMs = 0;
                    bed.currentFootDirection = "STOPPED"; bed.footStartTime = 0;
                } else footDone = false; 
            }

            if (headDone && footDone) {
                if (DEBUG_LEVEL >= 2) Serial.println(">>> DEBUG: All movements finished. Saving state.");
                stopAndSyncMotors(); 
            }
        }
        xSemaphoreGive(bedMutex); 
    }
}
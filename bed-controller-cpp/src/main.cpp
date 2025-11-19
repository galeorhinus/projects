#include <Arduino.h>
#include <esp_task_wdt.h>
#include "Config.h"
#include "BedControl.h"
#include "NetworkManager.h"

// Global Manager Instance
NetworkManager net;

void setup() {
    Serial.begin(115200);
    
    // 1. Init Physics & State
    initBedControl();
    
    // 2. Init Connectivity (Blocking operation: Connects or starts AP)
    // The Watchdog must NOT be running yet, or it will kill the WiFi Scan.
    net.begin();
    
    // 3. Safety First: Start Watchdog ONLY after WiFi is settled
    // Increased to 8 seconds to be safe against network lag in the loop
    esp_task_wdt_init(8, true); 
    esp_task_wdt_add(NULL);
    
    if(DEBUG_LEVEL >= 1) Serial.println("System V1.3 Ready. Watchdog Active.");
}

void loop() {
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
            Serial.printf("[STATUS] Time:%lu | Cmd:%s | H:%ld F:%ld\n", 
                logTime / 1000, activeCommandLog.c_str(), liveHead, liveFoot);
        }
    }

    // --- PHYSICS ENGINE LOOP ---
    if (xSemaphoreTake(bedMutex, portMAX_DELAY)) {
        
        // Pet the dog inside the lock to ensure we are processing
        esp_task_wdt_reset(); 

        unsigned long now = millis(); 

        if (bed.isPresetActive) {
            bool headDone = true;
            bool footDone = true;

            // Check Head
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

            // Check Foot
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

            // Final Cleanup
            if (headDone && footDone) {
                if (DEBUG_LEVEL >= 2) Serial.println(">>> DEBUG: All movements finished. Saving state.");
                stopAndSyncMotors(); 
            }
        }
        xSemaphoreGive(bedMutex); 
    }
}
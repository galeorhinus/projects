#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "BedControl.h"
#include "NetworkManager.h"
#include "Command.h"
#include "Config.h"
#include <algorithm>
#include <string>

BedControl bed;
NetworkManager net;
QueueHandle_t cmd_queue;

extern std::string activeCommandLog;

void bed_task(void *pvParameter) {
    while (1) {
        bed.update();
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}

void command_task(void *pvParameter) {
    Command cmd = {};
    while(1) {
        if (xQueueReceive(cmd_queue, &cmd, portMAX_DELAY)) {
            std::string commandStr(cmd.cmd);
            std::string labelStr(cmd.label);
            TickType_t maxWait = 0;

            // --- COMMAND LOGIC ---
            if (commandStr == "STOP") { bed.stop(); activeCommandLog = "IDLE"; } 
            else if (commandStr == "HEAD_UP") { bed.moveHead("UP"); activeCommandLog = "HEAD_UP"; }
            else if (commandStr == "HEAD_DOWN") { bed.moveHead("DOWN"); activeCommandLog = "HEAD_DOWN"; }
            else if (commandStr == "FOOT_UP") { bed.moveFoot("UP"); activeCommandLog = "FOOT_UP"; }
            else if (commandStr == "FOOT_DOWN") { bed.moveFoot("DOWN"); activeCommandLog = "FOOT_DOWN"; }
            else if (commandStr == "ALL_UP") { bed.moveAll("UP"); activeCommandLog = "ALL_UP"; }
            else if (commandStr == "ALL_DOWN") { bed.moveAll("DOWN"); activeCommandLog = "ALL_DOWN"; }
            
            // Fixed Presets
            else if (commandStr == "FLAT") { maxWait = bed.setTarget(0, 0); activeCommandLog = "FLAT"; }
            else if (commandStr == "MAX") { maxWait = bed.setTarget(HEAD_MAX_MS, FOOT_MAX_MS); activeCommandLog = "MAX"; }
            
            // Saved Presets
            else if (commandStr == "ZERO_G") {
                maxWait = bed.setTarget(bed.getSavedPos("zg_head", 10000), bed.getSavedPos("zg_foot", 40000));
                activeCommandLog = "ZERO_G";
            }
            else if (commandStr == "ANTI_SNORE") {
                maxWait = bed.setTarget(bed.getSavedPos("snore_head", 10000), bed.getSavedPos("snore_foot", 0));
                activeCommandLog = "ANTI_SNORE";
            }
            else if (commandStr == "LEGS_UP") {
                maxWait = bed.setTarget(bed.getSavedPos("legs_head", 0), bed.getSavedPos("legs_foot", 43000));
                activeCommandLog = "LEGS_UP";
            }
            else if (commandStr == "P1") {
                maxWait = bed.setTarget(bed.getSavedPos("p1_head", 0), bed.getSavedPos("p1_foot", 0));
                activeCommandLog = "P1";
            }
            else if (commandStr == "P2") {
                maxWait = bed.setTarget(bed.getSavedPos("p2_head", 0), bed.getSavedPos("p2_foot", 0));
                activeCommandLog = "P2";
            }

            // --- SAVE LOGIC ---
            else if (commandStr.find("SET_") == 0) {
                size_t endPos = std::string::npos;
                if (commandStr.find("_POS") != std::string::npos) endPos = commandStr.find("_POS");
                else if (commandStr.find("_LABEL") != std::string::npos) endPos = commandStr.find("_LABEL");
                
                if (endPos != std::string::npos) {
                    std::string slot = commandStr.substr(4, endPos - 4);
                    std::transform(slot.begin(), slot.end(), slot.begin(), ::tolower);
                    if (commandStr.find("_POS") != std::string::npos) {
                        int32_t h, f;
                        bed.getLiveStatus(h, f);
                        bed.setSavedPos((slot + "_head").c_str(), h);
                        bed.setSavedPos((slot + "_foot").c_str(), f);
                    } else if (commandStr.find("_LABEL") != std::string::npos) {
                        bed.setSavedLabel((slot + "_label").c_str(), labelStr);
                    } 
                }
            }

            if (cmd.sync_sem != NULL) {
                xSemaphoreGive(cmd.sync_sem);
            } else if (maxWait > 0) {
                vTaskDelay(maxWait / portTICK_PERIOD_MS);
                activeCommandLog = "IDLE";
            }
        }
    }
}

extern "C" void app_main() {
    cmd_queue = xQueueCreate(10, sizeof(Command));
    bed.begin();
    net.begin(cmd_queue);
    bed.update();
    xTaskCreatePinnedToCore(bed_task, "bed_logic", 4096, NULL, 5, NULL, 1);
    xTaskCreatePinnedToCore(command_task, "command_task", 4096, NULL, 5, NULL, 1);
}

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "BedControl.h"
#include "BedDriver.h"
#include "NetworkManager.h"

BedControl bed;
BedDriver* bedDriver = &bed;
NetworkManager net;

void bed_task(void *pvParameter) {
    while (1) {
        bedDriver->update();
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}

extern "C" void app_main() {
    bedDriver->begin();
    net.begin();
    xTaskCreatePinnedToCore(bed_task, "bed_logic", 4096, NULL, 5, NULL, 1);
}

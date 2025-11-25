#pragma once
#include "esp_http_server.h"
#include "BedControl.h"
#include "freertos/queue.h"

class NetworkManager {
public:
    void begin(QueueHandle_t cmd_queue);

private:
    httpd_handle_t server = NULL;
    
    void initWiFi();
    void initmDNS();
    void initSPIFFS();
    void startWebServer();
};
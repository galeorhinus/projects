#pragma once
#include "esp_http_server.h"
#include "BedControl.h"

class NetworkManager {
public:
    void begin();

private:
    httpd_handle_t server = NULL;
    
    void initWiFi();
    void initmDNS();
    void initSPIFFS();
    void startWebServer();
};
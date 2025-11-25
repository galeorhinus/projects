#pragma once
#include "esp_http_server.h"
#include "BedControl.h"
#include "wifiProvisioning.h"

class NetworkManager {
public:
    void begin();
    void startWebServer();
    void startSntp();
    void startMdns();

private:
    httpd_handle_t server = NULL;
    
    void initSPIFFS();
};

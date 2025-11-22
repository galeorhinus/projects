idf_component_register(
    SRCS "main.cpp"
    "BedControl.cpp"
    "NetworkManager.cpp"
    INCLUDE_DIRS "."
    REQUIRES
        nvs_flash
        esp_wifi
        esp_netif
        esp_event
        esp_http_server
        driver
        mdns 
        esp_timer
        spiffs
        json
)
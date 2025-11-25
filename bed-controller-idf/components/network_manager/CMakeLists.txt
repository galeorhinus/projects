idf_component_register(
    SRCS "NetworkManager.cpp"
    INCLUDE_DIRS "."
    REQUIRES
        bed_control
        esp_wifi
        esp_netif
        esp_event
        esp_http_server
        mdns
        spiffs
        json
        nvs_flash
        esp_timer
)

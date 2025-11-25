idf_component_register(
    SRCS "NetworkManager.cpp"
    INCLUDE_DIRS "."
    PRIV_INCLUDE_DIRS "${CMAKE_CURRENT_LIST_DIR}/../../main"  # for BedControl.h and Config.h
    REQUIRES
        common
        driver
        esp_wifi
        esp_netif
        esp_event
        esp_http_server
        mdns
        spiffs
        json
        nvs_flash
        freertos
        esp_timer
)

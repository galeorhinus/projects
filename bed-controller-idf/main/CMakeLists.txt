idf_component_register(
    SRCS "main.cpp" "BedControl.cpp"
    INCLUDE_DIRS "."
    REQUIRES
        network_manager
        common
        freertos
        driver
        nvs_flash
        esp_timer
        spiffs
)
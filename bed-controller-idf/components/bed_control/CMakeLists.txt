idf_component_register(
    SRCS "BedControl.cpp" "BedService.cpp"
    INCLUDE_DIRS "."
    REQUIRES
        board_config
        freertos
        driver
        nvs_flash
        esp_timer
        spiffs
)

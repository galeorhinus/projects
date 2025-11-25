idf_component_register(
    SRCS "BedControl.cpp"
    INCLUDE_DIRS "."
    REQUIRES
        freertos
        driver
        nvs_flash
        esp_timer
        spiffs
)

idf_component_register(
    SRCS "MatterManager.cpp"
    INCLUDE_DIRS "."
    REQUIRES
        bed_control
        esp_wifi
        nvs_flash
        esp_timer
)

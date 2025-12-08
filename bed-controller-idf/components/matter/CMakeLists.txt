if(NOT CONFIG_APP_ENABLE_MATTER)
    # Matter support is disabled; register a stub so the build system is satisfied.
    idf_component_register(SRCS "")
    return()
endif()

idf_component_register(
    SRCS "MatterManager.cpp"
    INCLUDE_DIRS "."
    REQUIRES
        bed_control
        esp_wifi
        nvs_flash
        esp_timer
        esp-matter
)

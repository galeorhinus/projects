if(CONFIG_APP_ROLE_BED)
    idf_component_register(
        SRCS "BedControl.cpp" "BedService.cpp"
        INCLUDE_DIRS "."
        REQUIRES
            board_config
            freertos
            driver
            nvs_flash
            esp_timer
    )
    # Workaround: esp_timer headers aren't being exposed via REQUIRES/PRIV_REQUIRES in build_bed.
    target_link_libraries(${COMPONENT_LIB} PUBLIC idf::esp_timer)
else()
    # Headers-only when bed role is disabled to avoid linking bed logic.
    idf_component_register(
        SRCS ""
        INCLUDE_DIRS "."
        REQUIRES
            board_config
            freertos
            driver
            nvs_flash
    )
endif()

set(BED_CTRL_ENABLED OFF)
if(DEFINED SDKCONFIG AND EXISTS "${SDKCONFIG}")
    file(READ "${SDKCONFIG}" _cfg)
    if(_cfg MATCHES "CONFIG_APP_ROLE_BED=y")
        set(BED_CTRL_ENABLED ON)
    endif()
elseif(DEFINED SDKCONFIG_DEFAULTS)
    string(FIND "${SDKCONFIG_DEFAULTS}" "sdkconfig.defaults.bed" _bed_idx)
    if(NOT _bed_idx EQUAL -1)
        set(BED_CTRL_ENABLED ON)
    endif()
endif()

if(BED_CTRL_ENABLED)
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

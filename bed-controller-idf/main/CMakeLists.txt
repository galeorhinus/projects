set(MAIN_REQUIRES
    board_config
    network_manager
    matter
    freertos
)
set(MAIN_HAS_BED OFF)
if(DEFINED SDKCONFIG AND EXISTS "${SDKCONFIG}")
    file(READ "${SDKCONFIG}" _cfg)
    if(_cfg MATCHES "CONFIG_APP_ROLE_BED=y")
        set(MAIN_HAS_BED ON)
    endif()
elseif(DEFINED SDKCONFIG_DEFAULTS)
    string(FIND "${SDKCONFIG_DEFAULTS}" "sdkconfig.defaults.bed" _bed_idx)
    if(NOT _bed_idx EQUAL -1)
        set(MAIN_HAS_BED ON)
    endif()
endif()
if(MAIN_HAS_BED)
    list(APPEND MAIN_REQUIRES bed_control)
endif()
idf_component_register(
    SRCS "main.cpp"
    INCLUDE_DIRS "."
    REQUIRES ${MAIN_REQUIRES}
)

set(MAIN_REQUIRES
    board_config
    network_manager
    matter
    freertos
)
if(CONFIG_APP_ROLE_BED)
    list(APPEND MAIN_REQUIRES bed_control)
endif()
idf_component_register(
    SRCS "main.cpp"
    INCLUDE_DIRS "."
    REQUIRES ${MAIN_REQUIRES}
)

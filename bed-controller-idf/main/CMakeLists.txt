idf_component_register(
    SRCS "main.cpp"
    INCLUDE_DIRS "."
    REQUIRES
        board_config
        bed_control
        network_manager
        matter
        freertos
)

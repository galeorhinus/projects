set(COMPONENT_SRCS "main.cpp")
set(COMPONENT_ADD_INCLUDEDIRS ".")

set(COMPONENT_REQUIRES bed_control
                     network_manager
                     freertos
                     common)
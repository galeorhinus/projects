cmake_minimum_required(VERSION 3.16.0)

set(APP_ROLE_BED_CMAKE OFF)
if(DEFINED SDKCONFIG AND EXISTS "${SDKCONFIG}")
    file(READ "${SDKCONFIG}" _cfg)
    if(_cfg MATCHES "CONFIG_APP_ROLE_BED=y")
        set(APP_ROLE_BED_CMAKE ON)
    endif()
elseif(DEFINED SDKCONFIG_DEFAULTS)
    string(FIND "${SDKCONFIG_DEFAULTS}" "sdkconfig.defaults.bed" _bed_idx)
    if(NOT _bed_idx EQUAL -1)
        set(APP_ROLE_BED_CMAKE ON)
    endif()
endif()
set(APP_ROLE_BED_CMAKE ${APP_ROLE_BED_CMAKE} CACHE BOOL "Bed role enabled (CMake)" FORCE)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
# Force C++17 for compatibility with esp-matter/CHIP codebase
idf_build_set_property(CXX_COMPILE_OPTIONS "-std=gnu++17" APPEND)

# Exclude Matter components unless explicitly enabled
idf_build_set_property(EXCLUDE_COMPONENTS "esp-matter" APPEND)

project(elev8_controller)

if(NOT CONFIG_APP_ENABLE_MATTER)
    idf_build_set_property(EXCLUDE_COMPONENTS "esp-matter" APPEND)
endif()

if(NOT APP_ROLE_BED_CMAKE)
    idf_build_set_property(EXCLUDE_COMPONENTS "bed_control" APPEND)
endif()

# Light-only builds should skip bed_control entirely.
# Build a SPIFFS image from the "data" folder and flash it into
# the "storage" partition defined in partitions.csv
spiffs_create_partition_image(storage data FLASH_IN_PROJECT)

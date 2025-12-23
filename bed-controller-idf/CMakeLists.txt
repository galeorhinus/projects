cmake_minimum_required(VERSION 3.16.0)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
# Force C++17 for compatibility with esp-matter/CHIP codebase
idf_build_set_property(CXX_COMPILE_OPTIONS "-std=gnu++17" APPEND)

# Exclude Matter components unless explicitly enabled
idf_build_set_property(EXCLUDE_COMPONENTS "esp-matter" APPEND)

project(elev8_controller)

if(NOT CONFIG_APP_ENABLE_MATTER)
    idf_build_set_property(EXCLUDE_COMPONENTS "esp-matter" APPEND)
endif()

if(NOT CONFIG_APP_ROLE_BED)
    idf_build_set_property(EXCLUDE_COMPONENTS "bed_control" APPEND)
endif()

# Light-only builds should skip bed_control entirely.
# Build a SPIFFS image from the "data" folder and flash it into
# the "storage" partition defined in partitions.csv
spiffs_create_partition_image(storage data FLASH_IN_PROJECT)

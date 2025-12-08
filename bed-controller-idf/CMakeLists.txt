cmake_minimum_required(VERSION 3.16.0)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
# Force C++17 for compatibility with esp-matter/CHIP codebase
idf_build_set_property(CXX_COMPILE_OPTIONS "-std=gnu++17" APPEND)

# Exclude Matter components unless explicitly enabled
idf_build_set_property(EXCLUDE_COMPONENTS "esp-matter" APPEND)

project(elev8_controller)

# Build a SPIFFS image from the "data" folder and flash it into
# the "storage" partition defined in partitions.csv
spiffs_create_partition_image(storage data FLASH_IN_PROJECT)

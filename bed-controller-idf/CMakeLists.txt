cmake_minimum_required(VERSION 3.16.0)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(elev8_controller)

if(NOT CONFIG_APP_ENABLE_MATTER)
    idf_build_set_property(EXCLUDE_COMPONENTS "esp-matter" APPEND)
endif()

# Build a SPIFFS image from the "data" folder and flash it into
# the "storage" partition defined in partitions.csv
spiffs_create_partition_image(storage data FLASH_IN_PROJECT)

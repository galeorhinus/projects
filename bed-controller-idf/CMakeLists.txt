cmake_minimum_required(VERSION 3.16.0)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)


set(EXTRA_COMPONENT_DIRS ${CMAKE_SOURCE_DIR}/components)
project(elev8_controller)

# Build a SPIFFS image from the "data" folder and flash it into
# the "storage" partition defined in partitions.csv
spiffs_create_partition_image(storage data FLASH_IN_PROJECT)

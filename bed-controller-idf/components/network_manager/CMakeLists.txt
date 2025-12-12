idf_component_register(
    SRCS "NetworkManager.cpp"
    INCLUDE_DIRS "."
    REQUIRES
        bed_control
        wifiProvisioning
        esp_wifi
        esp_netif
        esp_event
        esp_http_server
        mdns
        spiffs
        json
        nvs_flash
        esp_timer
        app_update
)

set(ASSET_SCRIPT ${CMAKE_CURRENT_SOURCE_DIR}/embed_assets.py)
set(ASSET_OUT_DIR ${CMAKE_CURRENT_BINARY_DIR}/embedded)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
# Build tag with timestamp
string(TIMESTAMP UI_BUILD_TAG "UI_BUILD_%Y-%m-%d_%H%M%S")
set(ENV{UI_BUILD_TAG} "${UI_BUILD_TAG}")

# Generate build_info.h with the same tag
set(BUILD_INFO_H ${CMAKE_CURRENT_BINARY_DIR}/build_info.h)
add_custom_target(generate_build_info ALL
    COMMAND ${CMAKE_COMMAND} -DOUTPUT=${BUILD_INFO_H} -DUI_BUILD_TAG=${UI_BUILD_TAG} -P ${CMAKE_CURRENT_SOURCE_DIR}/write_build_info.cmake
    BYPRODUCTS ${BUILD_INFO_H}
    VERBATIM
)
add_dependencies(${COMPONENT_LIB} generate_build_info)
target_include_directories(${COMPONENT_LIB} PRIVATE ${CMAKE_CURRENT_BINARY_DIR})

execute_process(
    COMMAND ${CMAKE_COMMAND} -E env OUT_DIR=${ASSET_OUT_DIR} UI_BUILD_TAG=${UI_BUILD_TAG} ${Python3_EXECUTABLE} ${ASSET_SCRIPT}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    RESULT_VARIABLE EMBED_RES
)
if(NOT EMBED_RES EQUAL 0)
    message(FATAL_ERROR "Asset embedding failed")
endif()

target_add_binary_data(${COMPONENT_LIB} ${ASSET_OUT_DIR}/index.html.gz BINARY)
target_add_binary_data(${COMPONENT_LIB} ${ASSET_OUT_DIR}/app.js.gz BINARY)
target_add_binary_data(${COMPONENT_LIB} ${ASSET_OUT_DIR}/bed-visualizer.js.gz BINARY)
target_add_binary_data(${COMPONENT_LIB} ${ASSET_OUT_DIR}/style.css.gz BINARY)
target_add_binary_data(${COMPONENT_LIB} ${ASSET_OUT_DIR}/sw.js.gz BINARY)
target_add_binary_data(${COMPONENT_LIB} ${ASSET_OUT_DIR}/branding.json.gz BINARY)
target_add_binary_data(${COMPONENT_LIB} ${ASSET_OUT_DIR}/favicon.png.gz BINARY)

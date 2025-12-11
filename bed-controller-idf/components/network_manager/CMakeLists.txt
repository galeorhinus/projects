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
execute_process(
    COMMAND ${CMAKE_COMMAND} -E env OUT_DIR=${ASSET_OUT_DIR} ${Python3_EXECUTABLE} ${ASSET_SCRIPT}
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

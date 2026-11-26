set(NET_MGR_REQUIRES
    board_config
    light_control
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

set(NET_MGR_HAS_BED OFF)
if(DEFINED SDKCONFIG AND EXISTS "${SDKCONFIG}")
    file(READ "${SDKCONFIG}" _cfg)
    if(_cfg MATCHES "CONFIG_APP_ROLE_BED=y")
        set(NET_MGR_HAS_BED ON)
    endif()
elseif(DEFINED SDKCONFIG_DEFAULTS)
    string(FIND "${SDKCONFIG_DEFAULTS}" "sdkconfig.defaults.bed" _bed_idx)
    if(NOT _bed_idx EQUAL -1)
        set(NET_MGR_HAS_BED ON)
    endif()
endif()
if(NET_MGR_HAS_BED)
    list(APPEND NET_MGR_REQUIRES bed_control)
endif()

idf_component_register(
    SRCS "NetworkManager.cpp"
    INCLUDE_DIRS "."
    REQUIRES ${NET_MGR_REQUIRES}
)

set(ASSET_SCRIPT ${CMAKE_CURRENT_SOURCE_DIR}/embed_assets.py)
set(ASSET_OUT_DIR ${CMAKE_CURRENT_BINARY_DIR}/embedded)
set(ASSET_DATA_DIR ${CMAKE_SOURCE_DIR}/data)
set(UI_BUILD_TAG_FILE ${ASSET_OUT_DIR}/ui_build_tag.txt)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
# UI roles from Kconfig (comma-separated)
set(UI_ROLES "")
if(CONFIG_APP_ROLE_BED)
    list(APPEND UI_ROLES "bed")
endif()
if(CONFIG_APP_ROLE_LIGHT)
    list(APPEND UI_ROLES "light")
endif()
if(CONFIG_APP_ROLE_TRAY)
    list(APPEND UI_ROLES "tray")
endif()
list(JOIN UI_ROLES "," UI_ROLES_STR)
set(ENV{UI_ROLES} "${UI_ROLES_STR}")
set(UI_ROLE "unknown")
if(CONFIG_APP_ROLE_BED)
    set(UI_ROLE "bed")
elseif(CONFIG_APP_ROLE_LIGHT)
    set(UI_ROLE "light")
elseif(CONFIG_APP_ROLE_TRAY)
    set(UI_ROLE "tray")
endif()
set(ENV{UI_ROLE} "${UI_ROLE}")

# Generate build_info.h with a fresh tag every build
set(BUILD_INFO_H ${CMAKE_CURRENT_BINARY_DIR}/build_info.h)
add_custom_target(generate_build_info ALL
    COMMAND ${CMAKE_COMMAND} -DOUTPUT=${BUILD_INFO_H} -DUI_BUILD_TAG_FILE=${UI_BUILD_TAG_FILE} -P ${CMAKE_CURRENT_SOURCE_DIR}/write_build_info.cmake
    BYPRODUCTS ${BUILD_INFO_H} ${UI_BUILD_TAG_FILE}
    VERBATIM
)
add_dependencies(${COMPONENT_LIB} generate_build_info)
target_include_directories(${COMPONENT_LIB} PRIVATE ${CMAKE_CURRENT_BINARY_DIR})

set(ASSET_INPUTS
    ${ASSET_SCRIPT}
    ${ASSET_DATA_DIR}/index.html
    ${ASSET_DATA_DIR}/app.js
    ${ASSET_DATA_DIR}/bed-visualizer.js
    ${ASSET_DATA_DIR}/style.css
    ${ASSET_DATA_DIR}/sw.js
    ${ASSET_DATA_DIR}/branding.json
    ${ASSET_DATA_DIR}/favicon.png
)
set(ASSET_OUTPUTS
    ${ASSET_OUT_DIR}/index.html.gz
    ${ASSET_OUT_DIR}/app.js.gz
    ${ASSET_OUT_DIR}/bed-visualizer.js.gz
    ${ASSET_OUT_DIR}/style.css.gz
    ${ASSET_OUT_DIR}/sw.js.gz
    ${ASSET_OUT_DIR}/branding.json.gz
    ${ASSET_OUT_DIR}/favicon.png.gz
    ${ASSET_OUT_DIR}/assets.stamp
)
add_custom_command(
    OUTPUT ${ASSET_OUTPUTS}
    COMMAND ${CMAKE_COMMAND} -E env OUT_DIR=${ASSET_OUT_DIR} UI_BUILD_TAG_FILE=${UI_BUILD_TAG_FILE} UI_ROLE=${UI_ROLE} UI_ROLES=${UI_ROLES_STR} ${Python3_EXECUTABLE} ${ASSET_SCRIPT}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS ${ASSET_INPUTS} ${UI_BUILD_TAG_FILE}
    VERBATIM
)
add_custom_target(embed_assets ALL DEPENDS ${ASSET_OUTPUTS})
add_dependencies(embed_assets generate_build_info)
add_dependencies(${COMPONENT_LIB} embed_assets)

target_add_binary_data(${COMPONENT_LIB} ${ASSET_OUT_DIR}/index.html.gz BINARY)
target_add_binary_data(${COMPONENT_LIB} ${ASSET_OUT_DIR}/app.js.gz BINARY)
target_add_binary_data(${COMPONENT_LIB} ${ASSET_OUT_DIR}/bed-visualizer.js.gz BINARY)
target_add_binary_data(${COMPONENT_LIB} ${ASSET_OUT_DIR}/style.css.gz BINARY)
target_add_binary_data(${COMPONENT_LIB} ${ASSET_OUT_DIR}/sw.js.gz BINARY)
target_add_binary_data(${COMPONENT_LIB} ${ASSET_OUT_DIR}/branding.json.gz BINARY)
target_add_binary_data(${COMPONENT_LIB} ${ASSET_OUT_DIR}/favicon.png.gz BINARY)

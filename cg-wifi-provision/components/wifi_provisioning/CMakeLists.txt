# /Users/paragtope/projects/cg-wifi-provision/components/wifi_provisioning/CMakeLists.txt
idf_component_register(SRCS "wifi_provisioning.cpp"
                    INCLUDE_DIRS "include"
                    EMBED_TXTFILES "provisioning.html" "app.html" "styles.css"
                    REQUIRES
                        esp_wifi 
                        esp_http_server 
                        nvs_flash 
                        mdns 
                        cjson 
                        esp_netif 
                        esp_event 
                        lwip 
                        esp_timer
                        esp_system 
                        freertos)

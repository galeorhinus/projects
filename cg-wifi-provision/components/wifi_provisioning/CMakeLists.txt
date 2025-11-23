# /Users/paragtope/projects/cg-wifi-provision/components/wifi_provisioning/CMakeLists.txt
idf_component_register(SRCS "wifi_provisioning.cpp"
                    INCLUDE_DIRS "include"
                    REQUIRES
                        esp_wifi 
                        esp_http_server 
                        nvs_flash 
                        mdns 
                        cjson 
                        esp_netif 
                        esp_event 
                        lwip 
                        esp_system 
                        freertos)

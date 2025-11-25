idf_component_register(SRCS "NetworkManager.cpp"
                    REQUIRES 
                        common
                        bed_control
                        esp_wifi
                        esp_netif
                        esp_event
                        esp_http_server
                        mdns 
                        spiffs
                        json
                        nvs_flash
                        freertos
                        esp_timer
)
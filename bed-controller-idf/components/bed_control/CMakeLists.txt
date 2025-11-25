idf_component_register(SRCS "BedControl.cpp"
                    INCLUDE_DIRS "."
                    REQUIRES 
                        nvs_flash
                        esp_timer
                        driver
                        esp_hw_support
                        esp_system
                        freertos
)
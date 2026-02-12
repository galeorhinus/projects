#pragma once

#include <stdint.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    int mosi_gpio;
    int clk_gpio;
    int cs_gpio;
    int dc_gpio;
    int rst_gpio;
    int busy_gpio;
} epd_stub_pins_t;

esp_err_t epd_stub_init(const epd_stub_pins_t *pins);
void epd_stub_pulse_reset(const epd_stub_pins_t *pins);
int epd_stub_read_busy(const epd_stub_pins_t *pins);
void epd_stub_spi_send_byte(const epd_stub_pins_t *pins, uint8_t data);
void epd_stub_sanity_test(const epd_stub_pins_t *pins);

#ifdef __cplusplus
}
#endif

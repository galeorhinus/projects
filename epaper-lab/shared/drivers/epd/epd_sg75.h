#pragma once

#include "esp_err.h"
#include "epd_stub.h"

#ifdef __cplusplus
extern "C" {
#endif

#define EPD_SG75_WIDTH  800
#define EPD_SG75_HEIGHT 480

esp_err_t epd_sg75_init(const epd_stub_pins_t *pins);
void epd_sg75_clear_white(const epd_stub_pins_t *pins);
void epd_sg75_clear_black(const epd_stub_pins_t *pins);
void epd_sg75_draw_checkerboard(const epd_stub_pins_t *pins, int block_px);
void epd_sg75_draw_buffer(const epd_stub_pins_t *pins, const uint8_t *buffer, int length);
void epd_sg75_sleep(const epd_stub_pins_t *pins);

#ifdef __cplusplus
}
#endif

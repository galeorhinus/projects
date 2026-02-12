#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "sdkconfig.h"
#include "epd_stub.h"
#include "epd_sg75.h"

#ifndef CONFIG_HELLO75_NO_SLEEP
#define CONFIG_HELLO75_NO_SLEEP 0
#endif

static const char *TAG = "hello75";
static uint8_t s_framebuffer[EPD_SG75_WIDTH * EPD_SG75_HEIGHT / 8];

static void fb_clear(uint8_t color)
{
    memset(s_framebuffer, color ? 0xFF : 0x00, sizeof(s_framebuffer));
}

static void fb_set_pixel(int x, int y, int color)
{
    if (x < 0 || x >= EPD_SG75_WIDTH || y < 0 || y >= EPD_SG75_HEIGHT) {
        return;
    }
    int byte_index = (y * EPD_SG75_WIDTH + x) / 8;
    int bit = 7 - (x & 0x7);
    if (color) {
        s_framebuffer[byte_index] |= (uint8_t)(1U << bit);
    } else {
        s_framebuffer[byte_index] &= (uint8_t)~(1U << bit);
    }
}

static const uint8_t s_font_5x7[][5] = {
    {0x3E, 0x51, 0x49, 0x45, 0x3E}, // '0'
    {0x00, 0x42, 0x7F, 0x40, 0x00}, // '1'
    {0x62, 0x51, 0x49, 0x49, 0x46}, // '2'
    {0x22, 0x41, 0x49, 0x49, 0x36}, // '3'
    {0x18, 0x14, 0x12, 0x7F, 0x10}, // '4'
    {0x2F, 0x49, 0x49, 0x49, 0x31}, // '5'
    {0x3E, 0x49, 0x49, 0x49, 0x32}, // '6'
    {0x01, 0x71, 0x09, 0x05, 0x03}, // '7'
    {0x36, 0x49, 0x49, 0x49, 0x36}, // '8'
    {0x26, 0x49, 0x49, 0x49, 0x3E}, // '9'
    {0x00, 0x36, 0x36, 0x00, 0x00}, // ':'
};

static void fb_draw_char(int x, int y, char c, int scale)
{
    const uint8_t *glyph = NULL;
    if (c >= '0' && c <= '9') {
        glyph = s_font_5x7[c - '0'];
    } else if (c == ':') {
        glyph = s_font_5x7[10];
    }
    if (!glyph) {
        return;
    }

    for (int col = 0; col < 5; ++col) {
        uint8_t bits = glyph[col];
        for (int row = 0; row < 7; ++row) {
            int on = (bits >> row) & 0x1;
            if (on) {
                for (int sx = 0; sx < scale; ++sx) {
                    for (int sy = 0; sy < scale; ++sy) {
                        fb_set_pixel(x + col * scale + sx, y + row * scale + sy, 1);
                    }
                }
            }
        }
    }
}

static void fb_draw_text(int x, int y, const char *text, int scale)
{
    int cursor = 0;
    while (*text) {
        fb_draw_char(x + cursor, y, *text, scale);
        cursor += (6 * scale);
        ++text;
    }
}

void app_main(void)
{
    epd_stub_pins_t pins = {
        .mosi_gpio = CONFIG_HELLO75_PIN_MOSI,
        .clk_gpio = CONFIG_HELLO75_PIN_CLK,
        .cs_gpio = CONFIG_HELLO75_PIN_CS,
        .dc_gpio = CONFIG_HELLO75_PIN_DC,
        .rst_gpio = CONFIG_HELLO75_PIN_RST,
        .busy_gpio = CONFIG_HELLO75_PIN_BUSY,
    };

    if (epd_sg75_init(&pins) != ESP_OK) {
        ESP_LOGE(TAG, "EPD init failed");
    } else {
        int start_seconds = 0;
        while (1) {
            int seconds = start_seconds++;
            int minutes = seconds / 60;
            int hours = (minutes / 60) % 24;
            int mins = minutes % 60;

            char time_text[6];
            time_text[0] = '0' + (hours / 10);
            time_text[1] = '0' + (hours % 10);
            time_text[2] = ':';
            time_text[3] = '0' + (mins / 10);
            time_text[4] = '0' + (mins % 10);
            time_text[5] = '\0';

            fb_clear(0);
            int scale = 10;
            int text_width = 5 * scale * 5 + 4 * scale;
            int text_height = 7 * scale;
            int x = (EPD_SG75_WIDTH - text_width) / 2;
            int y = (EPD_SG75_HEIGHT - text_height) / 2;
            fb_draw_text(x, y, time_text, scale);

            ESP_LOGI(TAG, "Displaying %s", time_text);
            epd_sg75_draw_buffer(&pins, s_framebuffer, sizeof(s_framebuffer));

            vTaskDelay(pdMS_TO_TICKS(60000));
        }
    }

    ESP_LOGI(TAG, "Hello 7.5\" e-paper board!");
}

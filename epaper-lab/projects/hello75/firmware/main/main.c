#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "sdkconfig.h"
#include "epd_stub.h"
#include "epd_sg75.h"
#include "clock75_mockup.h"
#include "roboto_font.h"
#include "devanagari_line.h"

#ifndef CONFIG_HELLO75_NO_SLEEP
#define CONFIG_HELLO75_NO_SLEEP 0
#endif

static const char *TAG = "hello75";
static uint8_t s_framebuffer[EPD_SG75_WIDTH * EPD_SG75_HEIGHT / 8];

#define HELLO75_SHOW_MOCKUP 1
#define HELLO75_RENDER_LAYOUT 0

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

// 5x7 ASCII font (chars 32..126), column-major, LSB at top.
static const uint8_t s_font_5x7[95][5] = {
    {0x00,0x00,0x00,0x00,0x00}, // ' '
    {0x00,0x00,0x5F,0x00,0x00}, // '!'
    {0x00,0x07,0x00,0x07,0x00}, // '"'
    {0x14,0x7F,0x14,0x7F,0x14}, // '#'
    {0x24,0x2A,0x7F,0x2A,0x12}, // '$'
    {0x23,0x13,0x08,0x64,0x62}, // '%'
    {0x36,0x49,0x55,0x22,0x50}, // '&'
    {0x00,0x05,0x03,0x00,0x00}, // '''
    {0x00,0x1C,0x22,0x41,0x00}, // '('
    {0x00,0x41,0x22,0x1C,0x00}, // ')'
    {0x14,0x08,0x3E,0x08,0x14}, // '*'
    {0x08,0x08,0x3E,0x08,0x08}, // '+'
    {0x00,0x50,0x30,0x00,0x00}, // ','
    {0x08,0x08,0x08,0x08,0x08}, // '-'
    {0x00,0x60,0x60,0x00,0x00}, // '.'
    {0x20,0x10,0x08,0x04,0x02}, // '/'
    {0x3E,0x51,0x49,0x45,0x3E}, // '0'
    {0x00,0x42,0x7F,0x40,0x00}, // '1'
    {0x62,0x51,0x49,0x49,0x46}, // '2'
    {0x22,0x41,0x49,0x49,0x36}, // '3'
    {0x18,0x14,0x12,0x7F,0x10}, // '4'
    {0x2F,0x49,0x49,0x49,0x31}, // '5'
    {0x3E,0x49,0x49,0x49,0x32}, // '6'
    {0x01,0x71,0x09,0x05,0x03}, // '7'
    {0x36,0x49,0x49,0x49,0x36}, // '8'
    {0x26,0x49,0x49,0x49,0x3E}, // '9'
    {0x00,0x36,0x36,0x00,0x00}, // ':'
    {0x00,0x56,0x36,0x00,0x00}, // ';'
    {0x08,0x14,0x22,0x41,0x00}, // '<'
    {0x14,0x14,0x14,0x14,0x14}, // '='
    {0x00,0x41,0x22,0x14,0x08}, // '>'
    {0x02,0x01,0x59,0x09,0x06}, // '?'
    {0x3E,0x41,0x5D,0x59,0x4E}, // '@'
    {0x7C,0x12,0x11,0x12,0x7C}, // 'A'
    {0x7F,0x49,0x49,0x49,0x36}, // 'B'
    {0x3E,0x41,0x41,0x41,0x22}, // 'C'
    {0x7F,0x41,0x41,0x22,0x1C}, // 'D'
    {0x7F,0x49,0x49,0x49,0x41}, // 'E'
    {0x7F,0x09,0x09,0x09,0x01}, // 'F'
    {0x3E,0x41,0x49,0x49,0x7A}, // 'G'
    {0x7F,0x08,0x08,0x08,0x7F}, // 'H'
    {0x00,0x41,0x7F,0x41,0x00}, // 'I'
    {0x20,0x40,0x41,0x3F,0x01}, // 'J'
    {0x7F,0x08,0x14,0x22,0x41}, // 'K'
    {0x7F,0x40,0x40,0x40,0x40}, // 'L'
    {0x7F,0x02,0x0C,0x02,0x7F}, // 'M'
    {0x7F,0x04,0x08,0x10,0x7F}, // 'N'
    {0x3E,0x41,0x41,0x41,0x3E}, // 'O'
    {0x7F,0x09,0x09,0x09,0x06}, // 'P'
    {0x3E,0x41,0x51,0x21,0x5E}, // 'Q'
    {0x7F,0x09,0x19,0x29,0x46}, // 'R'
    {0x46,0x49,0x49,0x49,0x31}, // 'S'
    {0x01,0x01,0x7F,0x01,0x01}, // 'T'
    {0x3F,0x40,0x40,0x40,0x3F}, // 'U'
    {0x1F,0x20,0x40,0x20,0x1F}, // 'V'
    {0x3F,0x40,0x38,0x40,0x3F}, // 'W'
    {0x63,0x14,0x08,0x14,0x63}, // 'X'
    {0x07,0x08,0x70,0x08,0x07}, // 'Y'
    {0x61,0x51,0x49,0x45,0x43}, // 'Z'
    {0x00,0x7F,0x41,0x41,0x00}, // '['
    {0x02,0x04,0x08,0x10,0x20}, // '\\'
    {0x00,0x41,0x41,0x7F,0x00}, // ']'
    {0x04,0x02,0x01,0x02,0x04}, // '^'
    {0x40,0x40,0x40,0x40,0x40}, // '_'
    {0x00,0x01,0x02,0x04,0x00}, // '`'
    {0x20,0x54,0x54,0x54,0x78}, // 'a'
    {0x7F,0x48,0x44,0x44,0x38}, // 'b'
    {0x38,0x44,0x44,0x44,0x20}, // 'c'
    {0x38,0x44,0x44,0x48,0x7F}, // 'd'
    {0x38,0x54,0x54,0x54,0x18}, // 'e'
    {0x08,0x7E,0x09,0x01,0x02}, // 'f'
    {0x0C,0x52,0x52,0x52,0x3E}, // 'g'
    {0x7F,0x08,0x04,0x04,0x78}, // 'h'
    {0x00,0x44,0x7D,0x40,0x00}, // 'i'
    {0x20,0x40,0x44,0x3D,0x00}, // 'j'
    {0x7F,0x10,0x28,0x44,0x00}, // 'k'
    {0x00,0x41,0x7F,0x40,0x00}, // 'l'
    {0x7C,0x04,0x18,0x04,0x78}, // 'm'
    {0x7C,0x08,0x04,0x04,0x78}, // 'n'
    {0x38,0x44,0x44,0x44,0x38}, // 'o'
    {0x7C,0x14,0x14,0x14,0x08}, // 'p'
    {0x08,0x14,0x14,0x18,0x7C}, // 'q'
    {0x7C,0x08,0x04,0x04,0x08}, // 'r'
    {0x48,0x54,0x54,0x54,0x20}, // 's'
    {0x04,0x3F,0x44,0x40,0x20}, // 't'
    {0x3C,0x40,0x40,0x20,0x7C}, // 'u'
    {0x1C,0x20,0x40,0x20,0x1C}, // 'v'
    {0x3C,0x40,0x30,0x40,0x3C}, // 'w'
    {0x44,0x28,0x10,0x28,0x44}, // 'x'
    {0x0C,0x50,0x50,0x50,0x3C}, // 'y'
    {0x44,0x64,0x54,0x4C,0x44}, // 'z'
    {0x00,0x08,0x36,0x41,0x00}, // '{'
    {0x00,0x00,0x7F,0x00,0x00}, // '|'
    {0x00,0x41,0x36,0x08,0x00}, // '}'
    {0x08,0x08,0x2A,0x1C,0x08}, // '~'
};

static void fb_draw_char(int x, int y, char c, int scale)
{
    const uint8_t *glyph = NULL;
    if (c >= 32 && c <= 126) {
        glyph = s_font_5x7[c - 32];
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

static const roboto_font_t *fb_get_roboto_font(int px)
{
    if (px >= 80) return &roboto_80;
    if (px >= 48) return &roboto_48;
    if (px >= 32) return &roboto_32;
    return &roboto_16;
}

static void fb_draw_char_roboto(int x, int y, char c, const roboto_font_t *font)
{
    if (c < 32 || c > 126) {
        return;
    }

    int idx = c - 32;
    int width = font->widths[idx];
    int row_bytes = (width + 7) / 8;
    const uint8_t *bitmap = font->bitmaps + font->offsets[idx];

    for (int yy = 0; yy < font->height; ++yy) {
        const uint8_t *row = bitmap + yy * row_bytes;
        for (int xx = 0; xx < width; ++xx) {
            uint8_t byte = row[xx >> 3];
            if (byte & (uint8_t)(0x80 >> (xx & 7))) {
                fb_set_pixel(x + xx, y + yy, 1);
            }
        }
    }
}

static void fb_draw_text_roboto(int x, int y, const char *text, int px)
{
    const roboto_font_t *font = fb_get_roboto_font(px);
    int cursor = 0;
    while (*text) {
        char c = *text++;
        if (c == ' ') {
            cursor += font->space_width;
            continue;
        }
        fb_draw_char_roboto(x + cursor, y, c, font);
        cursor += font->widths[(int)c - 32] + 1;
    }
}

static void fb_blit_bitmap(int x, int y, int width, int height, const uint8_t *data)
{
    int row_bytes = (width + 7) / 8;
    for (int yy = 0; yy < height; ++yy) {
        const uint8_t *row = data + yy * row_bytes;
        for (int xx = 0; xx < width; ++xx) {
            uint8_t byte = row[xx >> 3];
            if (byte & (uint8_t)(0x80 >> (xx & 7))) {
                fb_set_pixel(x + xx, y + yy, 1);
            }
        }
    }
}

static void fb_draw_line(int x0, int y0, int x1, int y1, int color)
{
    int dx = abs(x1 - x0), sx = x0 < x1 ? 1 : -1;
    int dy = -abs(y1 - y0), sy = y0 < y1 ? 1 : -1;
    int err = dx + dy;
    for (;;) {
        fb_set_pixel(x0, y0, color);
        if (x0 == x1 && y0 == y1) break;
        int e2 = 2 * err;
        if (e2 >= dy) { err += dy; x0 += sx; }
        if (e2 <= dx) { err += dx; y0 += sy; }
    }
}

static void fb_draw_rect(int x, int y, int w, int h, int color)
{
    fb_draw_line(x, y, x + w, y, color);
    fb_draw_line(x, y + h, x + w, y + h, color);
    fb_draw_line(x, y, x, y + h, color);
    fb_draw_line(x + w, y, x + w, y + h, color);
}

static void fb_fill_rect(int x, int y, int w, int h, int color)
{
    for (int yy = y; yy <= y + h; ++yy) {
        for (int xx = x; xx <= x + w; ++xx) {
            fb_set_pixel(xx, yy, color);
        }
    }
}

static void fb_draw_circle(int cx, int cy, int r, int color)
{
    int x = r, y = 0;
    int err = 0;
    while (x >= y) {
        fb_set_pixel(cx + x, cy + y, color);
        fb_set_pixel(cx + y, cy + x, color);
        fb_set_pixel(cx - y, cy + x, color);
        fb_set_pixel(cx - x, cy + y, color);
        fb_set_pixel(cx - x, cy - y, color);
        fb_set_pixel(cx - y, cy - x, color);
        fb_set_pixel(cx + y, cy - x, color);
        fb_set_pixel(cx + x, cy - y, color);
        if (err <= 0) {
            y += 1;
            err += 2 * y + 1;
        }
        if (err > 0) {
            x -= 1;
            err -= 2 * x + 1;
        }
    }
}

static void fb_draw_polyline(const int *pts, int count, int color)
{
    for (int i = 0; i < count - 2; i += 2) {
        fb_draw_line(pts[i], pts[i + 1], pts[i + 2], pts[i + 3], color);
    }
}

static void render_clock75_layout(void)
{
    fb_clear(0);

    // Panels and separators
    fb_draw_rect(10, 10, 780, 234, 1);
    fb_draw_rect(10, 240, 780, 230, 1);
    fb_draw_line(410, 16, 410, 230, 1);
    fb_draw_line(640, 16, 640, 230, 1);
    fb_draw_line(10, 355, 530, 355, 1);
    fb_draw_line(530, 355, 790, 355, 1);
    fb_fill_rect(530, 240, 260, 230, 1); // night block

    // Top-left date/time
    fb_draw_text_roboto(24, 24, "WED 10/11", 48);
    fb_blit_bitmap(24, 86, DEVANAGARI_LINE_WIDTH, DEVANAGARI_LINE_HEIGHT, devanagari_line_bitmap);
    fb_draw_text_roboto(24, 124, "12:38", 80);
    fb_draw_text_roboto(300, 140, "PM", 16);
    fb_draw_text_roboto(300, 160, "EST", 16);

    // Outdoor / indoor
    fb_draw_text_roboto(420, 30, "OUTDOOR", 16);
    fb_draw_text_roboto(430, 62, "48", 32);
    fb_draw_text_roboto(520, 58, "F", 16);
    fb_draw_text_roboto(510, 100, "72", 32);
    fb_draw_text_roboto(600, 96, "F", 16);
    fb_draw_text_roboto(520, 140, "INDOOR", 16);

    // Axes labels
    fb_draw_text_roboto(16, 256, "TEMP F", 16);
    fb_draw_text_roboto(680, 256, "MOON ELEV", 16);

    // Y ticks left
    fb_draw_text_roboto(16, 286, "80", 16);
    fb_draw_text_roboto(16, 316, "70", 16);
    fb_draw_text_roboto(16, 346, "60", 16);
    fb_draw_text_roboto(16, 376, "50", 16);
    fb_draw_text_roboto(16, 406, "40", 16);
    fb_draw_text_roboto(16, 436, "30", 16);

    // Time ticks
    int ticks[] = {60,130,200,270,340,410,480,550,620,690,760};
    for (int i = 0; i < (int)(sizeof(ticks)/sizeof(ticks[0])); ++i) {
        int x = ticks[i];
        fb_draw_line(x, 350, x, 360, 1);
    }
    fb_draw_text_roboto(50, 336, "7A", 16);
    fb_draw_text_roboto(120, 336, "9A", 16);
    fb_draw_text_roboto(190, 336, "11A", 16);
    fb_draw_text_roboto(260, 336, "1P", 16);
    fb_draw_text_roboto(330, 336, "3P", 16);
    fb_draw_text_roboto(400, 336, "5P", 16);
    fb_draw_text_roboto(470, 336, "7P", 16);
    fb_draw_text_roboto(540, 336, "9P", 16);
    fb_draw_text_roboto(610, 336, "11P", 16);
    fb_draw_text_roboto(680, 336, "1A", 16);
    fb_draw_text_roboto(750, 336, "3A", 16);

    // Curves (polylines)
    int temp_actual[] = {40,420,120,400,200,370,280,340,360,320,440,310,520,320};
    int temp_fore[] = {520,320,600,345,680,370,760,400};
    int moon_curve[] = {40,430,120,390,200,330,280,290,360,270,440,280,520,320,600,380,680,430,760,460};
    fb_draw_polyline(temp_actual, sizeof(temp_actual)/sizeof(int), 1);
    fb_draw_polyline(temp_fore, sizeof(temp_fore)/sizeof(int), 1);
    fb_draw_polyline(moon_curve, sizeof(moon_curve)/sizeof(int), 1);
    fb_draw_circle(360, 270, 10, 1);
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
#if HELLO75_SHOW_MOCKUP
#if HELLO75_RENDER_LAYOUT
        ESP_LOGI(TAG, "Rendering clock75 layout...");
        render_clock75_layout();
#else
        ESP_LOGI(TAG, "Blitting clock75 mockup bitmap...");
        memcpy(s_framebuffer, CLOCK75_MOCKUP_DATA, sizeof(s_framebuffer));
#endif
        epd_sg75_draw_buffer(&pins, s_framebuffer, sizeof(s_framebuffer));
        if (!CONFIG_HELLO75_NO_SLEEP) {
            epd_sg75_sleep(&pins);
        }
        while (1) {
            vTaskDelay(pdMS_TO_TICKS(1000));
        }
#else
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
#endif
    }

    ESP_LOGI(TAG, "Hello 7.5\" e-paper board!");
}

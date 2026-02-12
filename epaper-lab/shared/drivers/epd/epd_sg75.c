#include "epd_sg75.h"

#include "driver/gpio.h"
#include "driver/spi_master.h"
#include "esp_log.h"
#include "esp_rom_sys.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "sdkconfig.h"

static const char *TAG = "epd_sg75";
static spi_device_handle_t s_spi;

#ifndef CONFIG_HELLO75_SPI_CLOCK_HZ
#define CONFIG_HELLO75_SPI_CLOCK_HZ 1000000
#endif
#ifndef CONFIG_HELLO75_BUSY_IDLE_HIGH
#define CONFIG_HELLO75_BUSY_IDLE_HIGH 1
#endif
#ifndef CONFIG_HELLO75_IGNORE_BUSY
#define CONFIG_HELLO75_IGNORE_BUSY 0
#endif

static void epd_sg75_wait_idle(const epd_stub_pins_t *pins, int timeout_ms)
{
    int waited = 0;
#if CONFIG_HELLO75_IGNORE_BUSY
    (void)pins;
    (void)timeout_ms;
    vTaskDelay(pdMS_TO_TICKS(200));
    return;
#else
    int idle_level = CONFIG_HELLO75_BUSY_IDLE_HIGH ? 1 : 0;
    while (gpio_get_level(pins->busy_gpio) != idle_level) {
        vTaskDelay(pdMS_TO_TICKS(10));
        waited += 10;
        if (timeout_ms > 0 && waited >= timeout_ms) {
            ESP_LOGW(TAG, "BUSY wait timeout");
            break;
        }
    }
#endif
}

static void epd_sg75_cmd(const epd_stub_pins_t *pins, uint8_t cmd)
{
    gpio_set_level(pins->dc_gpio, 0);
    spi_transaction_t t = {
        .length = 8,
        .tx_buffer = &cmd,
    };
    spi_device_polling_transmit(s_spi, &t);
}

static void epd_sg75_data(const epd_stub_pins_t *pins, uint8_t data)
{
    gpio_set_level(pins->dc_gpio, 1);
    spi_transaction_t t = {
        .length = 8,
        .tx_buffer = &data,
    };
    spi_device_polling_transmit(s_spi, &t);
}

static void epd_sg75_reset(const epd_stub_pins_t *pins)
{
    gpio_set_level(pins->rst_gpio, 0);
    vTaskDelay(pdMS_TO_TICKS(10));
    gpio_set_level(pins->rst_gpio, 1);
    vTaskDelay(pdMS_TO_TICKS(10));
}

esp_err_t epd_sg75_init(const epd_stub_pins_t *pins)
{
    if (!pins) {
        return ESP_ERR_INVALID_ARG;
    }

    gpio_config_t out_conf = {
        .pin_bit_mask = (1ULL << pins->mosi_gpio) |
                        (1ULL << pins->clk_gpio) |
                        (1ULL << pins->cs_gpio) |
                        (1ULL << pins->dc_gpio) |
                        (1ULL << pins->rst_gpio),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };

    gpio_config_t in_conf = {
        .pin_bit_mask = (1ULL << pins->busy_gpio),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };

    esp_err_t err = gpio_config(&out_conf);
    if (err != ESP_OK) {
        return err;
    }

    err = gpio_config(&in_conf);
    if (err != ESP_OK) {
        return err;
    }

    gpio_set_level(pins->cs_gpio, 1);
    gpio_set_level(pins->dc_gpio, 0);
    gpio_set_level(pins->clk_gpio, 0);
    gpio_set_level(pins->mosi_gpio, 0);
    gpio_set_level(pins->rst_gpio, 1);

    spi_bus_config_t buscfg = {
        .mosi_io_num = pins->mosi_gpio,
        .miso_io_num = -1,
        .sclk_io_num = pins->clk_gpio,
        .quadwp_io_num = -1,
        .quadhd_io_num = -1,
        .max_transfer_sz = 4,
    };

    esp_err_t spi_err = spi_bus_initialize(SPI2_HOST, &buscfg, SPI_DMA_CH_AUTO);
    if (spi_err != ESP_OK && spi_err != ESP_ERR_INVALID_STATE) {
        return spi_err;
    }

    spi_device_interface_config_t devcfg = {
        .clock_speed_hz = CONFIG_HELLO75_SPI_CLOCK_HZ,
        .mode = 0,
        .spics_io_num = pins->cs_gpio,
        .queue_size = 1,
    };

    spi_err = spi_bus_add_device(SPI2_HOST, &devcfg, &s_spi);
    if (spi_err != ESP_OK) {
        return spi_err;
    }

    epd_sg75_reset(pins);
    ESP_LOGI(TAG, "BUSY level on reset: %d", gpio_get_level(pins->busy_gpio));

    epd_sg75_cmd(pins, 0x01); // POWER SETTING
    epd_sg75_data(pins, 0x07);
    epd_sg75_data(pins, 0x07);
    epd_sg75_data(pins, 0x3F);
    epd_sg75_data(pins, 0x3F);

    epd_sg75_cmd(pins, 0x06); // BOOSTER SOFT START
    epd_sg75_data(pins, 0x17);
    epd_sg75_data(pins, 0x17);
    epd_sg75_data(pins, 0x28);
    epd_sg75_data(pins, 0x17);

    epd_sg75_cmd(pins, 0x04); // POWER ON
    vTaskDelay(pdMS_TO_TICKS(200));
    epd_sg75_wait_idle(pins, 5000);

    epd_sg75_cmd(pins, 0x00); // PANEL SETTING
    epd_sg75_data(pins, 0x1F);

    epd_sg75_cmd(pins, 0x61); // RESOLUTION
    epd_sg75_data(pins, 0x03);
    epd_sg75_data(pins, 0x20);
    epd_sg75_data(pins, 0x01);
    epd_sg75_data(pins, 0xE0);

    epd_sg75_cmd(pins, 0x15);
    epd_sg75_data(pins, 0x00);

    epd_sg75_cmd(pins, 0x50); // VCOM AND DATA INTERVAL
    epd_sg75_data(pins, 0x10);
    epd_sg75_data(pins, 0x07);

    epd_sg75_cmd(pins, 0x60); // TCON SETTING
    epd_sg75_data(pins, 0x22);

    ESP_LOGI(TAG, "EPD init complete");
    return ESP_OK;
}

static void epd_sg75_update(const epd_stub_pins_t *pins)
{
    epd_sg75_cmd(pins, 0x12); // DISPLAY REFRESH
    esp_rom_delay_us(200);
    epd_sg75_wait_idle(pins, 8000);
}

void epd_sg75_clear_white(const epd_stub_pins_t *pins)
{
    const int total = (EPD_SG75_WIDTH * EPD_SG75_HEIGHT) / 8;

    epd_sg75_cmd(pins, 0x10);
    for (int i = 0; i < total; ++i) {
        epd_sg75_data(pins, 0x00);
    }

    epd_sg75_cmd(pins, 0x13);
    for (int i = 0; i < total; ++i) {
        epd_sg75_data(pins, 0x00);
    }

    epd_sg75_update(pins);
}

void epd_sg75_clear_black(const epd_stub_pins_t *pins)
{
    const int total = (EPD_SG75_WIDTH * EPD_SG75_HEIGHT) / 8;

    epd_sg75_cmd(pins, 0x10);
    for (int i = 0; i < total; ++i) {
        epd_sg75_data(pins, 0x00);
    }

    epd_sg75_cmd(pins, 0x13);
    for (int i = 0; i < total; ++i) {
        epd_sg75_data(pins, 0xFF);
    }

    epd_sg75_update(pins);
}

void epd_sg75_draw_checkerboard(const epd_stub_pins_t *pins, int block_px)
{
    const int total = (EPD_SG75_WIDTH * EPD_SG75_HEIGHT) / 8;
    if (block_px <= 0) {
        block_px = 16;
    }

    epd_sg75_cmd(pins, 0x10);
    for (int i = 0; i < total; ++i) {
        epd_sg75_data(pins, 0x00);
    }

    epd_sg75_cmd(pins, 0x13);
    for (int y = 0; y < EPD_SG75_HEIGHT; ++y) {
        for (int x_byte = 0; x_byte < EPD_SG75_WIDTH / 8; ++x_byte) {
            uint8_t byte = 0;
            for (int bit = 0; bit < 8; ++bit) {
                int x = x_byte * 8 + bit;
                int block_x = x / block_px;
                int block_y = y / block_px;
                int is_black = (block_x + block_y) & 1;
                if (is_black) {
                    byte |= (uint8_t)(0x80 >> bit);
                }
            }
            epd_sg75_data(pins, byte);
        }
    }

    epd_sg75_update(pins);
}

void epd_sg75_draw_buffer(const epd_stub_pins_t *pins, const uint8_t *buffer, int length)
{
    if (!buffer || length <= 0) {
        return;
    }

    epd_sg75_cmd(pins, 0x10);
    for (int i = 0; i < length; ++i) {
        epd_sg75_data(pins, 0x00);
    }

    epd_sg75_cmd(pins, 0x13);
    for (int i = 0; i < length; ++i) {
        epd_sg75_data(pins, buffer[i]);
    }

    epd_sg75_update(pins);
}

void epd_sg75_sleep(const epd_stub_pins_t *pins)
{
    epd_sg75_cmd(pins, 0x50);
    epd_sg75_data(pins, 0xF7);

    epd_sg75_cmd(pins, 0x02); // POWER OFF
    epd_sg75_wait_idle(pins, 5000);

    epd_sg75_cmd(pins, 0x07); // DEEP SLEEP
    epd_sg75_data(pins, 0xA5);
}

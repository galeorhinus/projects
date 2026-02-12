#include "epd_stub.h"

#include "driver/gpio.h"
#include "driver/spi_master.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_rom_sys.h"
#include "sdkconfig.h"

static const char *TAG = "epd_stub";
static spi_device_handle_t s_spi;

#ifndef CONFIG_HELLO75_SPI_CLOCK_HZ
#define CONFIG_HELLO75_SPI_CLOCK_HZ 1000000
#endif

esp_err_t epd_stub_init(const epd_stub_pins_t *pins)
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

    return ESP_OK;
}

void epd_stub_pulse_reset(const epd_stub_pins_t *pins)
{
    if (!pins) {
        return;
    }

    gpio_set_level(pins->rst_gpio, 0);
    vTaskDelay(pdMS_TO_TICKS(10));
    gpio_set_level(pins->rst_gpio, 1);
    vTaskDelay(pdMS_TO_TICKS(10));
}

int epd_stub_read_busy(const epd_stub_pins_t *pins)
{
    if (!pins) {
        return -1;
    }

    return gpio_get_level(pins->busy_gpio);
}

void epd_stub_spi_send_byte(const epd_stub_pins_t *pins, uint8_t data)
{
    if (!pins) {
        return;
    }

    if (!s_spi) {
        return;
    }

    spi_transaction_t t = {
        .length = 8,
        .tx_buffer = &data,
    };

    spi_device_polling_transmit(s_spi, &t);
}

void epd_stub_sanity_test(const epd_stub_pins_t *pins)
{
    if (!pins) {
        return;
    }

    int busy_before = epd_stub_read_busy(pins);
    ESP_LOGI(TAG, "BUSY before reset: %d", busy_before);

    epd_stub_pulse_reset(pins);

    int busy_after = epd_stub_read_busy(pins);
    ESP_LOGI(TAG, "BUSY after reset: %d", busy_after);

    gpio_set_level(pins->dc_gpio, 0);
    vTaskDelay(pdMS_TO_TICKS(5));
    gpio_set_level(pins->dc_gpio, 1);
    vTaskDelay(pdMS_TO_TICKS(5));

    ESP_LOGI(TAG, "Toggling SPI test pattern");
    epd_stub_spi_send_byte(pins, 0xAA);
    epd_stub_spi_send_byte(pins, 0x55);

    int busy_end = epd_stub_read_busy(pins);
    ESP_LOGI(TAG, "BUSY after pattern: %d", busy_end);
}

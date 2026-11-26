# Projects

This repository contains the HomeYantric device projects and the writing workspace.

## Device projects

| Directory | Purpose |
| --- | --- |
| [bed-controller-idf](bed-controller-idf/docs/how-to-build.md) | Current ESP-IDF firmware for the adjustable bed and LED controller. The bed and light roles share Wi-Fi provisioning, network services, and a web UI. The build guide lists the ESP32 and ESP32-S3 configurations. |
| [epaper-lab](epaper-lab/README.md) | E-paper lab. The clock75 clock and weather app uses the lab's own port of Wi-Fi provisioning. The hello75 app exercises the display. |
| [cg-wifi-provision](cg-wifi-provision/) | Standalone ESP-IDF provisioning project. |
| [esp32-wifi-setup](esp32-wifi-setup/) and [esp32-accesspoint-js-fail](esp32-accesspoint-js-fail/) | Earlier Wi-Fi provisioning experiments. |
| [esp32-display-client](esp32-display-client/) | Arduino TFT client and calibration sketch. |
| [mb-rf-rx](mb-rf-rx/) and [mb-rf-tx](mb-rf-tx/) | Receiver and transmitter utilities for the bed remote. |

## Writing

[writing](writing/) contains the book projects, including [Atomic Sanskrit](writing/books/atomicSanskrit/), and writing style material.

## Archived firmware

Bed controller development started with [Mongoose OS](archive/bed-controller/), moved to [PlatformIO C++](archive/bed-controller-cpp/), and continues in ESP-IDF. The archive preserves the two retired implementations for reference.

The [ST7796S display driver](archive/hw/mgos-st7796s-driver/) and its [test app](archive/tft-driver-test-app/) preserve an unfinished Mongoose OS display experiment.

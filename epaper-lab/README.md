# E-Paper Lab

ESP32 e-paper projects and shared components.

## Structure
- projects/: individual builds (each contains firmware, UI, hardware)
- shared/: reusable drivers, widgets, and assets
- tools/: scripts and common resources

## Active Projects
- projects/clock75: 7.5-inch clock + weather + sensors

## Toolchain
- ESP-IDF v5.x (per-project)
- Python 3.x via ESP-IDF tools

## Build (example)
cd projects/clock75/firmware
idf.py build

## Hardware (initial target)
- Display: 7.5-inch e-paper (mono or tri-color)
- MCU: ESP32 / ESP32-S3
- Sensors: temperature + humidity (TBD)

## Notes
- Keep shared drivers in shared/drivers/epd
- Keep UI widgets in shared/ui/widgets
- Add wiring diagrams under each project hardware/

## Next Steps
- Add display driver wrapper
- Define baseline UI layout + fonts
- Add weather fetcher + cache

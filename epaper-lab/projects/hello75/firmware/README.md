# hello75 firmware

## Build
```sh
cd projects/hello75/firmware
idf.py set-target esp32s3
idf.py menuconfig
idf.py build
```

## Flash + monitor
```sh
idf.py -p /dev/ttyUSB0 flash monitor
```

## Notes
- If your serial port differs, replace `/dev/ttyUSB0`.
- First time setup requires ESP-IDF installed and `IDF_PATH` set.
- Pin mapping and SPI clock live under `hello75 pins` in `menuconfig`.

## Display test
- On boot, the app initializes the 7.5" 800x480 panel and renders a large HH:MM clock that updates once per minute.

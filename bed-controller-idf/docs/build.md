# Build & Flash Guide

## Prereqs
- ESP-IDF tools installed (matching this repo).
- Python env set by `idf.py` (run `idf.py --version` to confirm).

## 1) Pick target & flash layout
- Set the MCU target:
  - ESP32: `idf.py set-target esp32`
  - ESP32-S3: `idf.py set-target esp32s3`
- If you need a specific flash size/partition table, run the helper (adjust as needed):
  - `tools/config_target.sh esp32 4MB` (copies partitions/esp32_4MB_ota.csv and sets flash size)
  - or copy the desired `partitions/*.csv` to `partitions.csv` and ensure `configs/sdkconfig.defaults`/menuconfig matches.

## 2) Choose application role
- `idf.py menuconfig` → Application configuration → Application role: Bed / Light (Tray future).
- Role affects which server RPCs are built. UI stays unified, but embeds the role tag.

## 3) Reconfigure (after changing target/flash/role)
- `idf.py reconfigure`

## 4) Embed assets (build tag & role)
- `idf.py build` will embed assets with the current build tag/role.
- If you need to run the script directly, pass env vars:
  - `UI_BUILD_TAG=UI_BUILD_YYYY-MM-DD_HHMMSS UI_ROLES=bed python3 components/network_manager/embed_assets.py`

## 5) Build
- `idf.py build`

## 6) Flash
- First time on a new flash size/table: `idf.py -p <port> erase-flash`
- Then: `idf.py -p <port> flash monitor`

## Notes
- If switching between roles/targets, repeat steps 1–4 before building.
- Build tag and UI role are injected at asset embed time; re-run embed when either changes.
- Light control wiring uses an NPN low-side switch: emitter to GND, collector to LED negative, LED positive to 3.3V (with resistor if needed), GPIO to base through ~1k, and a shared GND.
- VS Code: built-in Markdown preview (`Cmd+Shift+V`) supports copy/paste, but for a copy button on code blocks install “Markdown Preview Enhanced”.

## Multi-build setup (separate build dirs)
Use separate build directories to keep role/target configs isolated. Set a per-build
`SDKCONFIG` so each build dir owns its config and does not collide with the repo
root `sdkconfig`. Include the base defaults plus the role defaults so the
partition table and shared settings are applied.

### Light build (ESP32)
- Configure:
  - `idf.py -B build_light -D IDF_TARGET=esp32 set-target esp32`
  - `idf.py -B build_light -D SDKCONFIG=build_light/sdkconfig -D SDKCONFIG_DEFAULTS="configs/sdkconfig.defaults;configs/sdkconfig.defaults.light" reconfigure`
  - `idf.py -B build_light -D IDF_TARGET=esp32 -D SDKCONFIG=build_light/sdkconfig -D SDKCONFIG_DEFAULTS="configs/sdkconfig.defaults;configs/sdkconfig.defaults.light" reconfigure`
  (combines the two commands above)
- Build/flash:
  - `idf.py -B build_light -p <port> build flash monitor`

### Bed build (ESP32-S3)
- Configure:
  - `idf.py -B build_bed -D IDF_TARGET=esp32s3 set-target esp32s3`
  - `idf.py -B build_bed -D SDKCONFIG=build_bed/sdkconfig -D SDKCONFIG_DEFAULTS="configs/sdkconfig.defaults;configs/sdkconfig.defaults.bed" reconfigure`
  - `idf.py -B build_bed -D IDF_TARGET=esp32s3 -D SDKCONFIG=build_bed/sdkconfig -D SDKCONFIG_DEFAULTS="configs/sdkconfig.defaults;configs/sdkconfig.defaults.bed" reconfigure`
  (combines the two commands above)
- Build/flash:
  - `idf.py -B build_bed -p <port> build flash monitor`

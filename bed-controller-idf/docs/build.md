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
  - or copy the desired `partitions/*.csv` to `partitions.csv` and ensure `sdkconfig.defaults`/menuconfig matches.

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

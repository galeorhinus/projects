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
  - Light-only builds exclude `bed_control` and light RPCs are enabled.
  - Bed-only builds exclude light GPIO init and light RPCs are disabled.

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
Use separate build directories per role + target + variant so configs never
collide. Recommended naming: `build_<role>_<target>[_variant]` (safe for
parallel builds). Always set a per-build `SDKCONFIG` in the build dir and include
base defaults + role defaults (+ variant defaults if needed).

Examples:

### Bed build (ESP32-S3)
- Configure:
  - `idf.py -B build_bed_esp32s3 -D IDF_TARGET=esp32s3 -D SDKCONFIG=build_bed_esp32s3/sdkconfig -D SDKCONFIG_DEFAULTS="configs/sdkconfig.defaults;configs/sdkconfig.defaults.bed;configs/sdkconfig.defaults.partitions.esp32s3" reconfigure`
- Notes:
  - S3 build defaults set flash size to 16MB via `configs/sdkconfig.defaults.partitions.esp32s3`.
- Build/flash:
  - `idf.py -B build_bed_esp32s3 -p /dev/cu.usbmodem5B140844241 build flash monitor`

### Bed build (ESP32 WROVER / PSRAM)
- Configure:
  - `idf.py -B build_bed_esp32_wrover -D IDF_TARGET=esp32 -D SDKCONFIG=build_bed_esp32_wrover/sdkconfig -D SDKCONFIG_DEFAULTS="configs/sdkconfig.defaults;configs/sdkconfig.defaults.bed;configs/sdkconfig.defaults.wrover;configs/sdkconfig.defaults.partitions.esp32_wrover" reconfigure`
- Build/flash:
  - `idf.py -B build_bed_esp32_wrover -p /dev/cu.usbserial-1410 build flash monitor`

### Light build (ESP32)
- Configure:
  - `idf.py -B build_light_esp32 -D IDF_TARGET=esp32 -D SDKCONFIG=build_light_esp32/sdkconfig -D SDKCONFIG_DEFAULTS="configs/sdkconfig.defaults;configs/sdkconfig.defaults.light" reconfigure`
- Build/flash:
  - `idf.py -B build_light_esp32 -p /dev/cu.usbserial-1410 build flash monitor`
- Notes:
  - Light-only builds exclude the `bed_control` component when `CONFIG_APP_ROLE_BED=n`.

### Light build (ESP32-S3)
- Configure:
  - `idf.py -B build_light_esp32s3 -D IDF_TARGET=esp32s3 -D SDKCONFIG=build_light_esp32s3/sdkconfig -D SDKCONFIG_DEFAULTS="configs/sdkconfig.defaults;configs/sdkconfig.defaults.light;configs/sdkconfig.defaults.partitions.esp32s3" reconfigure`
- Build/flash:
  - `idf.py -B build_light_esp32s3 -p /dev/cu.usbmodem5B140844241 build flash monitor`
- Notes:
  - S3 defaults set flash size to 16MB via `configs/sdkconfig.defaults.partitions.esp32s3`.

## Example flows
### Bed-only (ESP32-S3)
- Build with role=bed and flash the S3 board.
- UI defaults to Bed, and discovers light peers to add the Lights tab.

### Light-only (ESP32 / WROVER)
- Build with role=light and flash the light board.
- UI defaults to Lights, and shows Bed tabs only when bed peers are discovered.

### Multi-role (Bed + Light on one device)
- Enable both roles (bed + light) and flash a single board.
- UI shows both tabs locally; ensure GPIO mappings do not conflict.

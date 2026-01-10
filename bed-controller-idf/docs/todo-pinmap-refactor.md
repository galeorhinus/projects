# Pin Map Refactor TODO

Goal: centralize pin selection and support board + role overrides without scattering `#if CONFIG_IDF_TARGET...`.

## Plan
- Add `components/board_config/PinMap.h` with a `struct PinMap` that includes:
  - Status RGB LED pins
  - Light RGB pins
  - Addressable LED data pin
  - Opto input pins
  - Relay/transfer pins
  - ACS712 ADC pin
- Define per-board defaults (ESP32, ESP32-S3) in one place.
- Layer role-specific overrides (bed vs light) on top of board defaults.
- Replace direct `#define LED_PIN_R` style macros with a `getPinMap()` accessor.
- Update `BoardConfig.h`, `BedConfig.h`, `LightConfig.h` to use the shared map.
- Optional: add Kconfig overrides for per-pin customization in the future.

## Expected Outcome
- Clear visibility of all four combinations (s3-bed, s3-light, wrover-bed, wrover-light).
- Single source of truth for docs + code.
- Safer changes when a pin moves.

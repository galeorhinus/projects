# Pin Assignments

Reference mapping for the two boards we use. All GPIO numbers are ESP32 pin indices (not board silk aliases).

## ESP32-WROVER (original)
- Head Up: `22`
- Head Down: `23`
- Foot Up: `18`
- Foot Down: `19`
- Transfer relays: `32`, `33`, `25`, `26`
- RGB LED (LEDC): `25` (R), `26` (G), `27` (B)
- Commission button: `0` (input, pull-up)

## ESP32-S3 (current)
- Head Up: `4`
- Head Down: `5`
- Foot Up: `6`
- Foot Down: `7`
- Transfer relays: `10` (single control for all)
- RGB LED (LEDC): `15` (R), `16` (G), `17` (B)
- Commission button: `0` (input, pull-up)
- Opto inputs (remote sense): `35`, `36`, `37`, `38` (inputs with pull-up)
- Light (single GPIO for light control module): `21`

Notes:
- S3 avoids USB D+/D- (`19`, `20`) and strapping pins. LEDs on 15/16/17. Transfer relays now on a single control (10). Opto inputs for remote lines use safe GPIOs 35–38.
- Adjust if your harness requires different pins; update `components/bed_control/BedConfig.h` and `components/light_control/LightConfig.h` accordingly.
- Light control uses an NPN low-side switch: emitter to GND, collector to LED negative, LED positive to 3.3V (with resistor if needed), GPIO to base through ~1k, and a shared GND.

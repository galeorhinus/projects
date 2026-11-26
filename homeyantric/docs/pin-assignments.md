# Pin Assignments

Reference mapping for the two boards we use. All GPIO numbers are ESP32 pin indices (not board silk aliases).

## ESP32-WROVER (original)
- Head Up: `22`
- Head Down: `23`
- Foot Up: `18`
- Foot Down: `19`
- Transfer relays: `32`, `33`, `25`, `26`
- RGB LED (LEDC): `25` (R), `26` (G), `27` (B)
- Addressable LED (data): `13`
- Commission button: `0` (input, pull-up)
- Opto inputs (remote sense): `34`, `35`, `36`, `39` (inputs with pull-up)

## ESP32-S3 (current)
- Head Up: `4`
- Head Down: `5`
- Foot Up: `6`
- Foot Down: `7`
- Transfer relays: `9`, `10`, `11`, `12` (per-direction control)
- RGB LED (LEDC): `15` (R), `16` (G), `17` (B)
- Addressable LED (data): `8`
- Commission button: `0` (input, pull-up)
- Opto inputs (remote sense): `35`, `36`, `37`, `38` (inputs with pull-up)
- Light (single GPIO for light control module): `21`
- ACS712 current sense (ADC1): `2`

Notes:
- S3 avoids USB D+/D- (`19`, `20`) and strapping pins. LEDs on 15/16/17. Transfer relays now use four GPIOs (9–12). Opto inputs for remote lines use safe GPIOs 35–38.
- Adjust if your harness requires different pins; update `components/bed_control/BedConfig.h` and `components/light_control/LightConfig.h` accordingly.
- Light control uses an NPN low-side switch: emitter to GND, collector to LED negative, LED positive to 3.3V (with resistor if needed), GPIO to base through ~1k, and a shared GND.
- WROVER ADC1 pins are occupied by optos today; to add ACS712 on WROVER, reassign one opto to free `34`/`35`/`36`/`39`.
- ESP32-S3 DevKitC-1 `5VIN` is an input rail; it may not output 5V when USB-powered. Use `VBUS` (if broken out) or an external 5V supply for WS2812 tests, and always share GND.

### ACS712 wiring (ESP32-S3 GPIO2)
Use a resistor divider on the ACS712 OUT to keep ADC input < 3.3V.

Recommended values (ratio ~0.59):
- R_TOP: `47k` between ACS712 OUT and the ADC node
- R_BOTTOM: `68k` between the ADC node and GND

Diagram:
```
ACS712 OUT ──[47k]──●── GPIO2 (ADC1)
                    |
                  [68k]
                    |
                   GND
```

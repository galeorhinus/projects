# Pin Assignments

Reference mapping for the two boards we use. All GPIO numbers are ESP32 pin indices (not board silk aliases).

## ESP32-WROVER (original)
- Head Up: `22`
- Head Down: `23`
- Foot Up: `18`
- Foot Down: `19`
- Transfer relays: `32`, `33`, `25`, `26`
- RGB LED (LEDC): `13` (R), `27` (G), `14` (B)
- Commission button: `0` (input, pull-up)

## ESP32-S3 (current)
- Head Up: `4`
- Head Down: `5`
- Foot Up: `6`
- Foot Down: `7`
- Transfer relays: `9`, `10`, `11`, `12`
- RGB LED (LEDC): `15` (R), `16` (G), `17` (B)
- Commission button: `0` (input, pull-up)

Notes:
- S3 avoids USB D+/D- (`19`, `20`) and strapping pins. LEDs moved to 15/16/17, so transfer relays are on 9/10/11/12.
- Adjust if your harness requires different pins; update `components/bed_control/Config.h` accordingly.

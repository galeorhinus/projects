# LED Behavior and Color Map

Status (spec-like, shared LED on GPIO 15/16/17)
- Unprovisioned/idle: slow white blink (~1 Hz).
- Commissioning: fast yellow blink (~5 Hz).
- Provisioned: solid green.
- Reset/fault: blinking red.

Motion overrides (active while motors run; override status, then clear)
- Head Up: violet.
- Head Down: amber.
- Foot Up: sky blue.
- Foot Down: magenta.
- All Up: teal.
- All Down: warm amber.
- Preset active: gold.

Notes
- Avoid moving during commissioning to keep status patterns intact.
- Motion overrides clear when set to off; status patterns resume automatically.

# Digital (Addressable) Light Wiring Plan

This plan covers WS2811/WS2812-compatible addressable LED strips (3-wire: V+, GND, DATA).
For the bed/light builds, **pixel #0 is reserved as the status indicator**. The strip
content starts at pixel #1.

## 1. Typical Components

- 24V or 12V DC power supply sized for the strip length
- Level shifter (preferred): 74AHCT125 / 74HCT14
- Series resistor on DATA: 220–470 Ω (near controller)
- Bulk capacitor: 1000 µF+ across V+ and GND at strip input
- Thermal breaker on V+ (size to expected load)

## 2. Baseline Wiring

```
ESP32 GND ───────────────────────────────┐
                                         ├─ Strip GND
PSU GND  ────────────────────────────────┘

PSU V+  ────────────────┬────────── Strip V+
                         |
                      1000 µF
                         |
PSU GND  ────────────────┘

ESP32 GPIO (DATA) ──[220–470 Ω]──> Level Shifter ──> Strip DIN
```

## 3. Level-Shifter Hack (Using Status LED as Pixel #0)

If you have a **5V addressable status LED** on the controller (e.g., WS2812),
you can use it as a level shifter by treating it as pixel #0 in the chain.

```
ESP32 GPIO8 ──[220–470 Ω]──> Status LED DIN
Status LED DOUT ───────────> Strip DIN
```

Notes:
- The status LED **must be 5V-powered** and **addressable** (WS281x compatible).
- Grounds must be common between ESP32, status LED, and strip.
- Keep the GPIO-to-status LED wire **short**.
- Pixel #0 is reserved for status; real strip content starts at pixel #1.

## 4. Power Injection

For longer strips (5m+), inject power at both ends to reduce brightness drop.

## 5. Software Behavior

- Pixel #0 is reserved for device status.
- Pixel #1..N are the user-visible pixels.
*** End Patch"/>

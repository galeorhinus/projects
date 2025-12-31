# 12V Analog RGB Strip Wiring (ESP32)

Goal: Drive a 12V analog RGB LED strip with an ESP32 using low-side switching.

## Assumptions (confirm)
- LED strip is **12V analog RGB** (3 channels: R, G, B) with a **common +12V** (common anode).
- You have **logic-level N‑MOSFETs** (low‑side switching).
- Separate 12V supply for the strip; ESP32 powered via 5V converter or USB.

## Parts (typical)
- 3x logic‑level N‑MOSFETs (one per color channel) — example: **IRLZ44N**
- 3x gate resistors (e.g., 100–220Ω)
- 3x gate pulldown resistors (e.g., 10kΩ to GND)
- Optional: inline fuse on +12V supply

## Wiring Summary (low‑side switching)
- **Strip +12V** → 12V supply +
- **Strip R/G/B‑** → MOSFET **drain** (one per channel)
- **MOSFET source** → GND (shared ground)
- **MOSFET gate** → ESP32 PWM GPIO via gate resistor
- **Gate pulldown** → gate to GND
- **ESP32 GND** → 12V supply GND (common ground)

## ASCII Diagram (one channel)

```
12V+  ────────────────┐
                      │
                [RGB Strip]
                      │
Channel - ────────── Drain (MOSFET)
                      Source ─────── GND (shared)
ESP32 PWM GPIO ──[Rgate]── Gate
                      │
                   [Rpd]
                      │
                     GND
```

Repeat for R, G, B.

## Wiring in Words (one channel)
1) Connect the strip **+12V** to the 12V supply **+**.
2) Connect the strip **R/G/B‑** wire to the **drain** of its MOSFET.
3) Connect the MOSFET **source** to **GND** (shared ground).
4) Connect an ESP32 PWM GPIO to the MOSFET **gate** through a **100–220Ω** resistor.
5) Add a **10kΩ** pulldown from gate to **GND**.
6) Tie **ESP32 GND** to the **12V supply GND**.

Repeat for each color channel (R, G, B) with separate MOSFETs.

## ESP32 GPIOs
Pick 3 PWM-capable GPIOs (LEDC). Suggested sets based on our current board usage:

### ESP32-S3 (bed build pins already in use)
- Suggested RGB PWM pins: `13`, `14`, `18`
- Avoid: `0`, `4`, `5`, `6`, `7`, `9–12`, `15–17`, `21`, `35–38`, `19/20` (USB)

### ESP32-WROVER (bed build pins already in use)
- Suggested RGB PWM pins: `4`, `5`, `21`
- Avoid: `0`, `18`, `19`, `22`, `23`, `25–27`, `32–33`, strapping pins like `12`/`15`

## Notes / Safety
- Ensure MOSFETs are **logic‑level** at 3.3V gate drive.
- Tie **all grounds together** (ESP32, MOSFETs, 12V supply).
- Add a **fuse** sized for strip current if possible.
- At **16–32 ft**, expect higher current. Size the 12V supply for total strip load and consider **power injection** at both ends (and middle for longer runs) to reduce voltage drop.

## Open Questions (fill in)
- Strip current per channel (A) / total wattage?
- Preferred GPIOs?
- Common anode confirmed?

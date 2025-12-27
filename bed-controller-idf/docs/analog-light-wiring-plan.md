# Analog Light Wiring Wizard Plan

Goal: Support a generic light controller with fixed 6 output terminals and a user-facing provisioning wizard that maps analog/PWM outputs to common LED wiring types. The selection should drive UI labels and wiring guidance (not internal pin wiring).

## Scope
- Analog/PWM only (digital/addressable is out of scope for this plan).
- Wiring selection applies to Light and Bed builds (Bed wording may differ).
- Internal GPIO pin assignments remain fixed; only terminal labels/mapping change.

## Supported Wiring Types (Draft)
- 2-wire single channel (dimming)
- 2-wire CCT tied (CW/WW tied to one channel)
- 3-wire CCT (CW + WW)
- 4-wire RGB
- 5-wire RGBW
- 6-wire RGB + CW + WW
- Generic multi-channel 2–6 outputs (no color semantics)

## UX Flow (Draft)
1) Entry point: Settings → “Analog Light Wiring Wizard”
2) Step 1: Choose wiring type (2–6 wire + type)
3) Step 2: Show terminal labels and a minimal wiring map
4) Step 3: Save + confirm persistence

## UI Requirements
- Show selected mapping in the light controls (labels reflect selection).
- UI adapts to wiring type (2-wire single slider, CCT sliders, RGB sliders, RGBW/CW/WW, or generic channels).

## WLED-Inspired Ideas (for analog/PWM)
- Presets/scenes (save wiring-type-specific states).
- Smooth transitions/fades between states.
- Segments/zones (map outputs to zones).
- Nightlight timer (auto-fade to off).
- Schedules (time-based on/off or preset recall).
- Brightness limiter (max duty cap).
- Power-on behavior (restore last state vs default off vs preset).
- Provide a minimal wiring map card (text labels + optional diagram).
- Expose the wizard in both Bed and Light builds (copy can differ).

## Data + API
- Persist selection in NVS.
- Provide a read/write API at `/rpc/Light.Wiring`.

## Open Questions (keep in plan)
- Should 2-wire include both single-channel dim and “CCT tied” as separate options?
- Should channel labels drive UI controls (e.g., show only CW/WW sliders vs RGB sliders), or only display a wiring map?
- Should the wizard live under Light Settings only, or also appear under Bed Settings with different copy?
- Where should we store the selection: NVS only, or expose a `/rpc/Light.Wiring` endpoint (or extend `/rpc/System.Labels`)?
  - Decision: use `/rpc/Light.Wiring` (keep System.Labels for labels only).

## Test Checklist
- Choose each wiring type; verify labels/mapping are correct.
- Reboot device; confirm selection persists.
- Verify Bed + Light builds expose the wizard and summary as intended.

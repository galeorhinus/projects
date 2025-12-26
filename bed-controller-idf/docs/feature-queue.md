# Feature Queue and Test Checklist

This is a living list of upcoming features and how to validate each one. Update after every change.

## In queue

- [ ] **Analog Light Wiring Wizard**
  - **What**: Add the analog wiring wizard (see `docs/analog-light-wiring-plan.md`).
  - **Test**: Follow the checklist in `docs/analog-light-wiring-plan.md`.

- [ ] **Light Presets + Transitions (analog/PWM)**
  - **What**: Save wiring-type-specific presets and allow smooth fades between states.
  - **Test**:
    - Save 2–3 presets for the selected wiring type.
    - Recall presets and verify smooth transitions (no jumps/flicker).

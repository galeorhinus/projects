# Feature Queue and Test Checklist

This is a living list of upcoming features and how to validate each one. Update after every change.

## In progress

- [x] **Analog Light Wiring Wizard (Light build)**
  - **What**: Wire-type selection, NVS persistence, wiring badge, and first-run gate for lights.
  - **Test**:
    - Fresh boot: confirm the “Select Light Type” gate appears and disables controls.
    - Save a wiring type: gate disappears and badge reflects selection.
    - Reboot: wiring remains configured and badge stays correct.
    - `curl /rpc/Peer.Discover`: `wiring_type` appears only after configured.

- [ ] **Light Presets + Transitions (analog/PWM)**
  - **What**: Save wiring-type-specific presets and allow smooth fades between states.
  - **Test**:
    - Save 2–3 presets for the selected wiring type.
    - Recall presets and verify smooth transitions (no jumps/flicker).

## Later

- [ ] **Analog Light Wiring Wizard (Bed build)**
  - **What**: Add the same wiring wizard entry to the bed settings with bed-specific copy.
  - **Test**: Confirm wiring selection persists and labels render in the bed context.

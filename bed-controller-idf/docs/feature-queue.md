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
- [x] **Event Stream (SSE) + Remote Press UI**
  - **What**: `/rpc/Events` pushes remote opto events; UI reacts immediately with pulsing controls and shows LIVE/OFF badge.
  - **Test**:
    - Open bed UI: verify LIVE badge appears.
    - Press remote buttons: matching UI controls pulse immediately (ALL pulses when head+foot align).
    - Disconnect/reconnect network: LIVE badge flips to OFF and back.

- [ ] **Light Presets + Transitions (analog/PWM)**
  - **What**: Save wiring-type-specific presets and allow smooth fades between states.
  - **Test**:
    - Save 2–3 presets for the selected wiring type.
    - Recall presets and verify smooth transitions (no jumps/flicker).

## Upcoming (Analog RGB)

- [ ] **Analog RGB Core Controls**
  - **What**: Master on/off, master brightness, and per-channel sliders (R/G/B) for `ui_mode=rgb`.
  - **Test**:
    - Toggle master: lights turn on/off without losing channel values.
    - Move R/G/B sliders: channel output changes accordingly.
    - Master brightness scales all channels uniformly.
- [ ] **Analog RGB Color Picker**
  - **What**: Color picker mapped to R/G/B sliders.
  - **Test**:
    - Pick a color: sliders update and light matches selection.
    - Manual slider changes update the picker.
- [ ] **Analog RGB Presets**
  - **What**: Save/recall named RGB presets (e.g., Warm, Cool, Sunset).
  - **Test**:
    - Save presets, refresh page, and confirm they persist.
    - Recall each preset and confirm colors match.
- [ ] **Analog RGB Fade/Transition**
  - **What**: Optional fade time for on/off and preset changes.
  - **Test**:
    - Set fade time, toggle on/off, and confirm smooth transitions.
    - Recall a preset and observe the fade duration.
- [ ] **Analog RGB State Recall**
  - **What**: Persist last color + brightness in NVS; “Off” preserves last color.
  - **Test**:
    - Set a color, turn off, power-cycle, and confirm “Off” state with preserved color.
    - Turn on: restores prior color/brightness.
- [ ] **Analog RGB Group Actions**
  - **What**: All On/Off respects last color across RGB devices.
  - **Test**:
    - All On restores each device’s last color.
    - All Off turns all RGB devices off without losing color.
- [ ] **Analog RGB Diagnostics (Advanced)**
  - **What**: R/G/B test buttons moved under an “Advanced” toggle.
  - **Test**:
    - Expand Advanced and run R/G/B tests.
    - Collapse Advanced hides test controls.

## WLED-Inspired (Analog/PWM)

- [ ] **Scenes/Presets (RGB + Brightness)**
  - **What**: Save and recall color + master brightness combos.
  - **Test**: Save 2–3 presets; refresh and verify persistence; recall each preset.
- [ ] **Quick Actions**
  - **What**: All On/Off, Night Mode (low brightness), Warm White preset.
  - **Test**: Run each action and confirm expected output.
- [ ] **Scheduling (Basic)**
  - **What**: Time-based on/off or preset apply.
  - **Test**: Schedule a preset and confirm it applies at the set time.
- [ ] **Power-On Behavior**
  - **What**: Configure boot state (restore last, boot-off).
  - **Test**: Switch modes and power-cycle to verify behavior.
- [ ] **Room Favorites**
  - **What**: Pin favorite devices/rooms for quick access.
  - **Test**: Pin/unpin and confirm ordering persists.

## WLED-Inspired (Digital/Addressable LEDs - Later)

- [ ] **Effects Engine**
  - **What**: Basic animations and per-effect parameters.
- [ ] **Segments**
  - **What**: Split a strip into segments with independent control.
- [ ] **Palettes + Playlists**
  - **What**: Preset palette rotation and playlist scheduling.

## Later

- [ ] **Analog Light Wiring Wizard (Bed build)**
  - **What**: Add the same wiring wizard entry to the bed settings with bed-specific copy.
  - **Test**: Confirm wiring selection persists and labels render in the bed context.

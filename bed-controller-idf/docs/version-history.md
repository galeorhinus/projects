# Version History

## 0.6.0 – feature/s3-motor-drv8871-optolog
- Planning for DRV8871 motor driver swap (replacing four relay channels with two motor drivers).
- Single control signal for all transfer relays.
- New pin map for ESP32-S3-DevKitC-1 (including opto-sense inputs for the remote signals).
- Optocoupler inputs to observe remote-triggered movement (with internal pull-ups).

## 0.7.0 – peer discovery + light UI polish
- mDNS advertises `type` plus labels, and peer lookup/discover includes label metadata.
- Light UI: room grouping, adaptive All On/Off controls, brightness stepper with +/- and live slider updates.
- Light status chip in header and cached peer fallback on refresh failure.
- LED feedback pulses for light actions; light build uses Wi-Fi status LED state.
- Updated WROVER RGB LED pins to 25/26/27 in docs.

### Hardware Verification Checklist
- [ ] **Status LED**: boot-time RGB test flashes R/G/B once on light build.
- [ ] **Provisioning LED**: slow blink pre-provisioning, solid once STA is up.
- [ ] **Light GPIO**: toggle on/off from UI; confirm relay/transistor behavior.
- [ ] **Brightness**: slider adjusts brightness smoothly; +/- steps change by 10%.
- [ ] **mDNS**: `dns-sd -B _homeyantric._tcp` sees both boards and TXT labels.

Need codex to remind me to check the hardware.  tagged under:
"hardware verification checklist."

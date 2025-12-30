# Temporary: Bed Limit Detection + Auto Calibration

Purpose: Validate optocoupler readings during app-driven bed movement, detect limit reached events, and use them for auto-calibration.

## Steps
1) Log opto readings during app-driven head/foot movements (up/down). Include timestamps and direction.
2) Define and verify a “limit reached” signature (e.g., opto activity drops to idle for a sustained window) while motor command is still active.
3) Use that limit signal to auto-calibrate and store limits/travel timing to NVS.

## Open Questions
- What signature should count as “limit reached” (opto inactive for X ms, or a different pattern)?
- What debounce/hold time should we require to avoid false positives?
- Should auto-calibration run automatically on every full travel, or only when explicitly triggered in UI?

## Status
- Draft

## Test Checklist (Draft)
- Start head up via app; confirm opto log shows active and timestamps.
- Start head down via app; confirm opto log shows active and timestamps.
- Start foot up via app; confirm opto log shows active and timestamps.
- Start foot down via app; confirm opto log shows active and timestamps.
- Run to physical limit; verify opto activity drops to idle for the configured window while command remains active.
- Confirm no false positives during normal movement (short opto dips don’t trigger).

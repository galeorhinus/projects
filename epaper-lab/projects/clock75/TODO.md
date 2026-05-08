# Clock75 Todo

## Phase 1: Data Plumbing
- [x] Wi‑Fi provisioning stable (done)
- [ ] NTP time sync (timezone + DST handling)
- [ ] Persistent location config (lat/lon + timezone)
- [ ] Weather client (current + hourly + daily)
- [ ] Moon data (phase + elevation curve)
- [ ] On-device moon math (phase + limb orientation + elevation + rise/set), recompute every 30 minutes

## Phase 2: Rendering Hooks
- [ ] Define data model for UI fields
- [ ] Replace mock values with live values
- [ ] Plot temperature curves (actual + forecast)
- [ ] Plot moon elevation curve + phase icon

## Phase 3: Refresh & Caching
- [ ] Refresh cadence policy (minute, hourly, daily)
- [ ] Cache weather data in NVS (avoid repeated API calls)
- [ ] Partial refresh strategy vs full refresh

## Phase 4: Config UI
- [ ] Local web UI for:
  - Wi‑Fi status
  - Location + units
  - Display toggles
  - Refresh cadence

## Phase 5: Power & Diagnostics
- [ ] Quiet hours / low‑power mode
- [ ] Battery/voltage if available
- [ ] Status page with last update times

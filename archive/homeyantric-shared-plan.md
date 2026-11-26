# HomeYantric Shared Components

This repo will host shared, production‑ready components used across HomeYantric devices (bed controller, clock, lights, sensors). The goal is to centralize common code while keeping device‑specific repos stable and focused.

## Why this repo
- Avoid duplicating Wi‑Fi provisioning, ESP‑NOW messaging, sensor drivers, time sync, and settings UI.
- Keep experimental work in `epaper-lab` until it stabilizes.
- Preserve `bed-controller-idf` history and stability.

## Current Direction (Agreed Plan)
- **Option A (preferred)**: keep device repos separate and promote mature device projects into their own repos.
- Use this repo as the shared component source for all devices.
- When `clock75` matures, create a dedicated repo (e.g., `clock75-idf`) and consume shared components from here.

## Proposed Structure
```
homeyantric-shared/
  components/
    wifiProvisioning/
    espnow_bus/
    sensors/
    settings_ui/
    time_sync/
    weather_client/
  ui/
    icons/
    fonts/
    layout_helpers/
  tools/
    build_helpers/
    asset_pipeline/
  docs/
    api/
    integration/
```

## Component Guidelines
- **Stable APIs**: treat component headers as public contracts.
- **Configurable**: Kconfig options for all hardware‑specific settings.
- **Minimal dependencies**: avoid pulling in non‑essential components.
- **Versioning**: tag releases when a component is used in a production device.

## Integration Strategy
- **Short term**: copy components into device repos while designs evolve.
- **Long term**: consume via git submodule or ESP‑IDF component manager.

## Migration Plan (When Ready)
1. Audit shared code in `bed-controller-idf` and `epaper-lab`.
2. Extract stable pieces into `homeyantric-shared/components`.
3. Add compatibility shims to avoid breaking device builds.
4. Update device repos to consume shared components.
5. Tag a release once devices are validated.

## Near‑Term Candidates
- `wifiProvisioning` (already ported into `epaper-lab/shared/components`)
- `espnow_bus` (device‑to‑device comms)
- `time_sync` (NTP + RTC fallback)
- `weather_client` (API + caching)
- `settings_ui` (local web config)
- `sensor_drivers` (temp/humidity, light, etc.)

## Notes
- `bed-controller-idf` history must be preserved.
- `epaper-lab` remains the experimental sandbox until clock75 is production‑ready.

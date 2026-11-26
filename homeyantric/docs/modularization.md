# Bed Control Modularization (Relay vs RF/WL101/WL102)

These patterns keep the relay implementation intact while letting you swap in RF drivers later.

## Code Architecture
- **Driver interface**: Define a `BedDriver` contract with `begin/update/stop/moveHead/moveFoot/moveAll/setTarget/getLiveStatus` and `get/setSavedPos/Label`. The current `BedControl` is the relay implementation; add `Wl101BedDriver`, `Wl102BedDriver`, or a mock without touching RPC/UI layers.
- **Runtime selection**: Choose the driver at startup (Kconfig flag or small `device-config.json` in SPIFFS) and set `bedDriver` to the chosen implementation.
- **Capability flags**: Each driver exposes capabilities (supports presets, position feedback, max head/foot sec). Return these in `/rpc/Bed.Status` so the UI adapts.
- **Command map**: Keep a per-driver command map if RF backends need different low-level operations; avoid branching in the HTTP handlers.
- **Encapsulated timing/limits**: Keep debounce, max durations, and safety stops inside each driver, not in the network layer.
- **Mock driver**: Optional driver that logs actions only, useful for UI/dev testing.

## UI / UX Adaptation
- **Capability-driven UI**: On load, fetch status/capabilities and hide/disable unsupported controls (e.g., presets if not available; adjust max ranges based on driver limits).
- **Visualizer reuse**: Feed head/foot seconds from status regardless of driver; RF implementations can provide estimated values if exact positions aren’t available.
- **Config file**: Serve a small `device-config.json` alongside `branding.json` with `driverType`, `maxHeadSec`, `maxFootSec`, and `supportsPresets` for initial render before the first status poll.

## Multiple Modules (e.g., Side Tray Actuator)
- **Second driver**: Add a `TrayDriver` (or generic `AutomationDriver`) with its own interface and implementation; keep state/timing separate from the bed driver.
- **RPC endpoints**: Mirror the bed shape under new URIs, e.g., `/rpc/Tray.Command` and `/rpc/Tray.Status`. Use the same JSON shape (`{ cmd: "UP"|"DOWN"|"STOP"|... }`) for command posts and return status with position/limits/capabilities.
- **Config**: Extend `device-config.json` to list available modules (`["bed","tray"]`) and per-module limits/capabilities so the UI knows what to render before the first poll.
- **UI tabs/segments**: Add a Bed/Tray tab (or segment control). Each tab renders its own controls and visualizer/position indicator and targets the module-specific RPC endpoints. Keep shared styling/branding; avoid duplicating logic by parameterizing the sender with the module name.
- **Safety/priority**: If both actuators share power constraints, centralize scheduling/throttling in the drivers to avoid conflicting motions.

## Deployment Notes
- Keep the relay driver as default to avoid regressions.
- Add new driver components separately and list them in `REQUIRES` only where needed.
- Ensure new assets (config files) are in the SPIFFS image and routed by the HTTP server.

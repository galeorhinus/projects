# Peer Discovery and Light Control Plan

1. **Light On/Off Service (single GPIO)**
   - Implement a minimal Light service with one configurable GPIO pin.
   - Expose `/rpc/Light.Status` and `/rpc/Light.Command` (on/off/toggle).
   - Log state changes; keep GPIO selection per-board configurable.

2. **Bed Controller Isolation**
   - Keep existing bed pin mappings; do not reuse bed pins for light.
   - Ensure swapping to the light build does not affect bed GPIO assignments.
   - Add a build-time option/variant to exclude bed_control for light-only firmware.
   - Select pin maps per chip target at build time (e.g., `CONFIG_IDF_TARGET_ESP32` vs `CONFIG_IDF_TARGET_ESP32S3`) to avoid unsafe pins.

3. **Build-Time Role Flag (Bed / Light / Tray)**
   - Each firmware build selects a role (bed, light; tray later) to include only that role’s server RPCs and GPIO code.
   - The front-end remains unified (bed/light tabs stay present; peers discovered via mDNS are shown even if the local device does not host that role).
   - Example flow:
     - Build with role=bed, flash ESP32_BED: only bed RPCs are compiled; UI defaults to bed and discovers peers to add their tabs.
     - Build with role=light, flash ESP32_LIGHT: only light RPCs compiled; UI still shows both tabs and controls peers when found.
     - Add tray later with the same pattern.

4. **UI Role Awareness**
   - Expose the current build role to the UI (e.g., embed `UI_ROLE` and/or add `/rpc/System.Role`).
   - On load, default to the local role tab and skip status polling for non-local roles to avoid 501s.
   - Keep peer discovery; when peers are found, add their role tabs and route RPCs to the peer host.

5. **mDNS Advertise per Role**
   - Advertise `_homeyantric._tcp` with TXT: `type=light` (light build) or `type=bed` (bed build), plus model/fw tag (UI_BUILD_TAG).

6. **Peer Discovery Endpoint**
   - Add `/rpc/Peer.Discover` returning identity: name, host, port, type (bed/light), capabilities.

7. **Peer-Aware UI Tabs**
   - Dynamically render tabs per discovered peer (bed/light).
   - For lights: show a “Lights” tab with on/off/toggle and status polling.
   - Add a manual “Refresh peers” with sane timeouts/failure handling.

8. **Persistence & Fallback**
   - Cache last-known peers (NVS/localStorage); expire stale entries.
   - Handle offline peers gracefully (UI notice, no blocking).

9. **Tests & Docs**
   - Bench test light GPIO control on hardware.
   - Validate mDNS advertise/discover with at least two boards.
   - Update `docs/version-history.md` and pin map per app/chip; document how to pick the build per chip.

## Scaling Options (many roles)
- Limit roles per device; use peer discovery so other roles live on separate ESPs.
- Use I/O expanders/muxes to add pins for simple roles (relays/lights).
- Parameterize pins per build/board so roles can be mapped differently on different hardware.
- Only share pins when hardware is mutually exclusive and gated in software.

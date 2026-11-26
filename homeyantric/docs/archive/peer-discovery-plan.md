# Peer Discovery and Light Control Plan

- [x] **Light On/Off Service (single GPIO)**
  - [x] Implement a minimal Light service with one configurable GPIO pin.
  - [x] Expose `/rpc/Light.Status` and `/rpc/Light.Command` (on/off/toggle).
  - [x] Log state changes; keep GPIO selection per-board configurable.

- [x] **Bed Controller Isolation**
  - [x] Keep existing bed pin mappings; do not reuse bed pins for light.
  - [x] Ensure swapping to the light build does not affect bed GPIO assignments.
  - [x] Add a build-time option/variant to exclude bed_control for light-only firmware.
  - [x] Select pin maps per chip target at build time (e.g., `CONFIG_IDF_TARGET_ESP32` vs `CONFIG_IDF_TARGET_ESP32S3`) to avoid unsafe pins.

- [ ] **Build-Time Role Flag (Bed / Light / Tray)**
  - [x] Each firmware build selects one or more roles (bed, light; tray later) to include only those roles’ server RPCs and GPIO code (multi-role is allowed when pins do not conflict).
  - [x] The front-end remains unified (bed/light tabs stay present; peers discovered via mDNS are shown even if the local device does not host that role).
  - [ ] Example flow:
    - [x] Build with role=bed, flash ESP32_BED: only bed RPCs are compiled; UI defaults to bed and discovers peers to add their tabs.
    - [x] Build with role=light, flash ESP32_LIGHT: only light RPCs compiled; UI defaults to lights and shows bed tabs only when peers are discovered.
    - [ ] Add future roles with the same pattern.

- [x] **UI Role Awareness**
  - [x] Expose the current build role to the UI (e.g., embed `UI_ROLE` and/or add `/rpc/System.Role`).
  - [x] On load, default to the local role tab and skip status polling for non-local roles to avoid 501s.
  - [x] Keep peer discovery; when peers are found, add their role tabs and route RPCs to the peer host.

- [x] **mDNS Advertise per Role**
  - [x] Advertise `_homeyantric._tcp` with TXT: `type=light` (light build) or `type=bed` (bed build), plus model/fw tag (UI_BUILD_TAG) (partial: TXT uses `roles` + `fw` today).
  - [x] Add label metadata to TXT (e.g., `room`, `device_name`) once the schema is set.

- [x] **Peer Discovery Endpoint**
  - [x] Add `/rpc/Peer.Discover` returning identity: name, host, port, type (bed/light), capabilities.
  - [x] Extend identity payload to include `device_name` and `room` (defaults: `unknown`).

- [x] **mDNS Lookup Helper (auto host list)**
  - [x] Add `/rpc/Peer.Lookup` that mDNS-browses `_homeyantric._tcp`, filters out self, and returns a list of peers (host/ip/roles/fw).
  - [x] UI calls this to auto-populate peer hosts without manual `setPeerHosts`.

- [x] **Peer-Aware UI Tabs**
  - [x] Dynamically render tabs per discovered peer (bed/light).
  - [x] For lights: show a “Lights” tab with on/off/toggle and status polling.
  - [x] Add a manual “Refresh peers” with sane timeouts/failure handling.
  - [x] Add room-based grouping and labels for peers (bed tabs per device; light tiles grouped by room).

- [x] **Peer Roles With Multiple Devices**
  - [x] Define per-role UI behavior: `light` aggregates multiple peers on one page; `bed` stays separate tabs.
  - [x] Conflict rule: multiple lights are allowed/aggregated; beds are single-target per tab (user selects bed tab).
  - [x] Light UX extras: room filter chips, collapse/expand per room, and per-room “All off/on”.

- [x] **Auto-Discovery Behavior**
  - [x] Periodically auto-refresh peers so newly provisioned devices discover each other (currently 15s).
  - [x] Keep an explicit “Refresh peers” button for manual recovery when mDNS is flaky.

- [ ] **Room & Label Metadata**
  - [x] Define a `device_name` + `room` label schema (free-text with defaults).
  - [x] Provide build-time defaults (`CONFIG_APP_LABEL_ROOM`/`CONFIG_APP_LABEL_DEVICE_NAME`) and allow runtime override via `/rpc/System.Labels` (stored in NVS).
  - [x] Add a simple UI form to edit labels and persist them.
  - [x] Modularize Settings modal cards so each entry point (Bed Set vs Lights Labels) can include only relevant sections.
  - [x] Include labels in `/rpc/Peer.Discover` and `mDNS` TXT once available.

- [x] **Persistence & Fallback**
  - [x] Cache last-known peers (NVS/localStorage); expire stale entries (partial: localStorage write exists but is not used for refresh or expiry).
  - [x] Handle offline peers gracefully (UI notice, no blocking).

- [ ] **Tests & Docs**
  - [ ] Bench test light GPIO control on hardware.
  - [x] Validate mDNS advertise/discover with at least two boards.
  - [ ] Update `docs/version-history.md` and pin map per app/chip; document how to pick the build per chip.

## Build/Flash notes
- When assets change, regenerate (`python3 components/network_manager/embed_assets.py`), then clean build if needed (`rm -rf build`) so the updated gz is embedded.
- Use a free serial port for flashing (close monitor first).

## Scaling Options (many roles)
- Limit roles per device; use peer discovery so other roles live on separate ESPs.
- Use I/O expanders/muxes to add pins for simple roles (relays/lights).
- Parameterize pins per build/board so roles can be mapped differently on different hardware.
- Only share pins when hardware is mutually exclusive and gated in software.

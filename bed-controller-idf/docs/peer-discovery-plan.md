# Peer Discovery and Light Control Plan

- [x] **Light On/Off Service (single GPIO)**
  - [x] Implement a minimal Light service with one configurable GPIO pin.
  - [x] Expose `/rpc/Light.Status` and `/rpc/Light.Command` (on/off/toggle).
  - [x] Log state changes; keep GPIO selection per-board configurable.

- [ ] **Bed Controller Isolation**
  - [x] Keep existing bed pin mappings; do not reuse bed pins for light.
  - [x] Ensure swapping to the light build does not affect bed GPIO assignments.
  - [ ] Add a build-time option/variant to exclude bed_control for light-only firmware.
  - [x] Select pin maps per chip target at build time (e.g., `CONFIG_IDF_TARGET_ESP32` vs `CONFIG_IDF_TARGET_ESP32S3`) to avoid unsafe pins.

- [ ] **Build-Time Role Flag (Bed / Light / Tray)**
  - [ ] Each firmware build selects a role (bed, light; tray later) to include only that role’s server RPCs and GPIO code (partial: RPCs are gated; bed_control still builds; light GPIO init is always on).
  - [x] The front-end remains unified (bed/light tabs stay present; peers discovered via mDNS are shown even if the local device does not host that role).
  - [ ] Example flow:
    - [ ] Build with role=bed, flash ESP32_BED: only bed RPCs are compiled; UI defaults to bed and discovers peers to add their tabs.
    - [ ] Build with role=light, flash ESP32_LIGHT: only light RPCs compiled; UI still shows both tabs and controls peers when found (partial: bed tab is hidden unless a peer is discovered).
    - [ ] Add tray later with the same pattern.

- [ ] **UI Role Awareness**
  - [x] Expose the current build role to the UI (e.g., embed `UI_ROLE` and/or add `/rpc/System.Role`).
  - [x] On load, default to the local role tab and skip status polling for non-local roles to avoid 501s.
  - [ ] Keep peer discovery; when peers are found, add their role tabs and route RPCs to the peer host (partial: per-role routing exists, not per-peer tabs).

- [ ] **mDNS Advertise per Role**
  - [ ] Advertise `_homeyantric._tcp` with TXT: `type=light` (light build) or `type=bed` (bed build), plus model/fw tag (UI_BUILD_TAG) (partial: TXT uses `roles` + `fw` today).
  - [x] Add label metadata to TXT (e.g., `room`, `device_name`) once the schema is set.

- [x] **Peer Discovery Endpoint**
  - [x] Add `/rpc/Peer.Discover` returning identity: name, host, port, type (bed/light), capabilities.
  - [x] Extend identity payload to include `device_name` and `room` (defaults: `unknown`).

- [x] **mDNS Lookup Helper (auto host list)**
  - [x] Add `/rpc/Peer.Lookup` that mDNS-browses `_homeyantric._tcp`, filters out self, and returns a list of peers (host/ip/roles/fw).
  - [x] UI calls this to auto-populate peer hosts without manual `setPeerHosts`.

- [ ] **Peer-Aware UI Tabs**
  - [ ] Dynamically render tabs per discovered peer (bed/light).
  - [x] For lights: show a “Lights” tab with on/off/toggle and status polling.
  - [x] Add a manual “Refresh peers” with sane timeouts/failure handling.
  - [ ] Add room-based grouping and labels for peers (bed tabs per device; light tiles grouped by room) (partial: device/room labels exist for the light card).

- [ ] **Peer Roles With Multiple Devices**
  - [ ] Define per-role UI behavior: `light` can aggregate multiple peers on one page; `bed` stays separate tabs.
  - [ ] Add a conflict rule when multiple peers share the same role (multi allowed vs one-per-role).

- [ ] **Auto-Discovery Behavior**
  - [x] Periodically auto-refresh peers so newly provisioned devices discover each other (currently 15s).
  - [ ] Keep an explicit “Refresh peers” button for manual recovery when mDNS is flaky.

- [ ] **Room & Label Metadata**
  - [ ] Define a `device_name` + `room` label schema (free-text with defaults).
  - [ ] Store labels locally (NVS) with a default of `unknown` and allow editing later (RPC/UI).
  - [x] Include labels in `/rpc/Peer.Discover` and `mDNS` TXT once available.

- [ ] **Persistence & Fallback**
  - [ ] Cache last-known peers (NVS/localStorage); expire stale entries (partial: localStorage write exists but is not used for refresh or expiry).
  - [ ] Handle offline peers gracefully (UI notice, no blocking).

- [ ] **Tests & Docs**
  - [ ] Bench test light GPIO control on hardware.
  - [ ] Validate mDNS advertise/discover with at least two boards.
  - [ ] Update `docs/version-history.md` and pin map per app/chip; document how to pick the build per chip.

## Build/Flash notes
- When assets change, regenerate (`python3 components/network_manager/embed_assets.py`), then clean build if needed (`rm -rf build`) so the updated gz is embedded.
- Use a free serial port for flashing (close monitor first).

## Scaling Options (many roles)
- Limit roles per device; use peer discovery so other roles live on separate ESPs.
- Use I/O expanders/muxes to add pins for simple roles (relays/lights).
- Parameterize pins per build/board so roles can be mapped differently on different hardware.
- Only share pins when hardware is mutually exclusive and gated in software.

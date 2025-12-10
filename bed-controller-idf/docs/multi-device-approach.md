# Multi-Device Approach (ESP32 Fleet)

Goals
- One firmware for all devices; behavior driven by config (role/room).
- Simple LAN discovery; no cloud required.
- App can coordinate many devices (lights, curtains, tray, bed, etc.).

Device identity/config
- Store `role` and `room` in NVS (set via provisioning API or default).
- Expose `/info` (GET) returning id/role/room/firmware/app API version.
- Allow updating role/room via a small POST (auth as needed).
- Hostname: keep `homeyantric-XX.local` pattern; include role in mDNS TXT.

Discovery
- mDNS/Bonjour advert `_http._tcp` with TXT: `role=<role>`, `room=<room>`, `api=<ver>`.
- App browses mDNS, builds a device list grouped by role/room.
- Fallback: allow manual IP entry.

API contract
- Maintain a versioned API (`apiVersion` in `/info`).
- Core endpoints stay stable (`/rpc/Bed.*`, `/rpc/Tray.*`, `/rpc/Curtains.*`, add `/rpc/Lights.*`); if role-specific, return 404 for unsupported calls.
- OTA stays at `/rpc/Bed.OTA` (or alias `/rpc/Device.OTA`).

UI/app
- Tabs per role; devices populate dynamically from discovery.
- Allow selecting default device per role; support “all role” fan-out (e.g., all lights off).
- Cache device list; refresh on demand or periodically via mDNS.

Coordination
- Default: app sends commands to all devices of a role.
- Optional: designate a coordinator (by config) to relay “group” commands over HTTP to peers.

Firmware behavior
- Single binary; at boot read role/room and enable only the relevant drivers/endpoints.
- Unsupported features no-op or 404; keep logs clear on role.
- Preserve OTA, provisioning, status LED, and logging across roles.

Versioning/updates
- Embed firmware version and API version in `/info`.
- App warns if device API is older than minimum supported; offer OTA.
- Keep changelog mapping firmware versions to required app versions.

Security
- At minimum, keep provisioning and control on LAN; consider simple auth tokens if needed.
- If roles are changeable, gate that behind a basic auth/nonce to avoid casual tampering.

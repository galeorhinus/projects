# Feature Queue and Test Checklist

This is a living list of upcoming features and how to validate each one. Update after every change.

## In queue

- [x] **mDNS Advertise per Role**
  - **What**: Advertise `_homeyantric._tcp` with TXT `type=bed` or `type=light` (roles + fw already present).
  - **Test**:
    - Run `dns-sd -B _homeyantric._tcp` (or `avahi-browse -r _homeyantric._tcp`) from a laptop.
    - Verify TXT has `type=...` plus `roles`/`fw`.

- [x] **Light UX extras**
  - **What**: Room filter chips, per-room collapse, per-room “All off/on”.
  - **Test**:
    - Provision 2+ lights in different rooms.
    - Use filter chips to show a single room.
    - Collapse/expand a room group.
    - Click “All off” for a room and confirm all lights in that room go off.
    - Click “All on” for a room and confirm all lights in that room turn on.

- [x] **Auto-Discovery Manual Refresh**
  - **What**: Explicit refresh button for mDNS recovery (keep auto refresh).
  - **Test**:
    - Power-cycle a peer so it disappears.
    - Click “Refresh peers” and verify the UI updates without a page reload.

- [x] **Persistence & Fallback (Peers)**
  - **What**: Cache last-known peers and expire stale entries.
  - **Test**:
    - Bring peer online, then remove from network.
    - Confirm it stays listed with “stale” status, then expires after TTL.
    - Bring peer back; it should reappear via auto-refresh.

- [x] **Room & Label Edit UI + Settings Modal Modularization**
  - **What**: Modularize the Settings modal cards per entry point (Bed Set vs Lights Labels) and include a labels form to edit `device_name` and `room`, saved to NVS.
  - **Test**:
    - Bed Set shows only bed-related cards; Lights Labels shows only labels.
    - Change labels in UI and reboot device.
    - Confirm labels persist and show in `/rpc/Peer.Discover` + mDNS TXT.

- **Tests & Docs**
  - **What**: Hardware validation and documentation updates.
  - **Test**:
    - Bench test light GPIO on real hardware (toggle/brightness).
    - Validate mDNS advertise/discover between two boards.
    - Update `docs/version-history.md` and pin map docs after each release.

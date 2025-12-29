# Event Stream (SSE)

This document defines the proposed Server-Sent Events (SSE) stream at `/rpc/Events`.
The stream is designed to be general-purpose, so new event types can be added without
changing the transport.

## Transport
- URL: `/rpc/Events`
- Method: `GET`
- Content-Type: `text/event-stream`
- Reconnect: browser `EventSource` auto-reconnects

## Event Envelope
Each event uses SSE `event:` and `data:` fields.
- `event:` is a short type string (e.g. `remote_event`).
- `data:` is a compact JSON object.

## Implemented Events

### `remote_event`
Emitted when a remote optocoupler input changes to a new stable state.

Payload fields:
- `type`: `"remote_event"`
- `eventMs`: ms since boot when the opto became stable
- `debounceMs`: time between raw change and stable
- `statusMs`: ms since boot when the event was served
- `opto`: index 0-3 (matches opto input order)
- `opto1..opto4`: raw stable opto states (0 = active, 1 = idle)
- `headDir`: `"UP"|"DOWN"|"STOPPED"` (remote + local combined)
- `footDir`: `"UP"|"DOWN"|"STOPPED"` (remote + local combined)

### `remote_edge`
Emitted on raw opto input edge (pre-debounce) for immediate UI feedback.

Payload fields:
- `type`: `"remote_edge"`
- `eventMs`: ms since boot when the raw edge was observed
- `statusMs`: ms since boot when the event was served
- `opto`: index 0-3 (matches opto input order)
- `state`: raw state (0 = active, 1 = idle)
- `raw1..raw4`: raw opto states (0 = active, 1 = idle)

### `ping`
Periodic keepalive used by the stream.

Payload fields:
- `type`: `"ping"`
- `statusMs`: ms since boot when the ping was sent

## Candidate Events (Planned)

These are not implemented yet, but the stream is intended to carry them:

- `peer_update`
  - peer appeared/removed or changed labels/room/roles
- `device_online` / `device_offline`
  - availability transitions with timestamps and last-seen
- `bed_status`
  - head/foot positions, motion directions, limits
- `light_state`
  - on/off, brightness, wiring mode
- `schedule_updated`
  - schedule created/edited/deleted
- `schedule_fired`
  - schedule executed with action details
- `ota_available`
  - new firmware info
- `config_required`
  - device requires setup (e.g. wiring mode not configured)
- `provisioning`
  - Wi-Fi connected/disconnected, mDNS changes

## Client Usage

Use browser `EventSource` and handle `event` types:

```js
const es = new EventSource('/rpc/Events');
es.addEventListener('remote_event', (ev) => {
  const data = JSON.parse(ev.data);
  // Update UI using opto states and head/foot dirs.
});
```

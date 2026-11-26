# Light Migrations RPC

This document describes the manual migration endpoint for light devices. Use it to apply
one-time migration logic (for example, normalizing saved digital effect defaults) without
auto-migration at boot.

## Endpoint

`POST /rpc/Light.Migrate`

## Request

Optional JSON body:

```json
{"source":"ui"}
```

If omitted, the request source is treated as `unknown` for logging.

## Response

```json
{
  "status": "ok",
  "digital_state_found": true,
  "digital_state_migrated": true,
  "effect_mode": "loop",
  "effect_direction": "pingpong"
}
```

## Example

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"source":"ui"}' \
  http://homeyantric-08.local/rpc/Light.Migrate
```

## Notes

- The endpoint is intended for future migrations as the lighting design evolves.
- It only updates saved state when a migration rule applies.

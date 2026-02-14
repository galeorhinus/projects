# Clock75 Project Requirements

## Provisioning & Setup
- First boot: SoftAP + captive portal Wi‑Fi provisioning.
- After provisioning: serve a local config page on device IP.
- Persist settings in NVS and reload on boot.
- Optional OTA update capability.

## Time & Clock
- NTP time sync with fallback to last known time.
- 12/24‑hour format toggle.
- Timezone + DST configuration.

## Weather
- Configurable API provider (e.g., OpenWeather, Pirate, etc.).
- Location configuration (ZIP / lat‑lon / city).
- Update cadence with cache to minimize refresh + API calls.
- Offline fallback to last known data.

## Sensors
- Indoor temperature/humidity sensor support (configurable model).
- Calibration offsets for sensor readings.

## Display & Power
- Full refresh schedule with partial refreshes between.
- Quiet hours (no refresh at night).
- Battery/voltage indicator where available.
- Low‑power mode.

## UI Configuration (Web)
- Toggle sections on/off (moon/tithi, forecasts, indoor).
- Unit preferences (°F/°C).
- Forecast row counts (hourly + 7‑day).
- Font scale / density options.

## Diagnostics
- Status page: Wi‑Fi RSSI, IP, battery, last update times.
- Logs or debug output downloadable via local UI.

## Security (Optional)
- Optional AP password for provisioning.
- Optional local UI password (basic auth).

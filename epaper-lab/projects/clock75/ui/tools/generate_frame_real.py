#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import urllib.parse
import urllib.request
from datetime import datetime, timedelta


def fetch_open_meteo(lat: float, lon: float, units: str):
    params = {
        "latitude": f"{lat:.4f}",
        "longitude": f"{lon:.4f}",
        "timezone": "auto",
        "hourly": "temperature_2m",
        "daily": "temperature_2m_max,temperature_2m_min,sunrise,sunset",
        "current": "temperature_2m",
        "past_days": "1",
        "forecast_days": "7",
    }
    if units == "f":
        params["temperature_unit"] = "fahrenheit"
    url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


def hhmm(dt: datetime) -> str:
    return dt.strftime("%-I:%M%p").lower()


def dow_date(dt: datetime) -> str:
    return dt.strftime("%a %m/%d").upper()


def to_minutes(dt: datetime) -> int:
    return dt.hour * 60 + dt.minute


def interpolate_value(t0: datetime, v0: float, t1: datetime, v1: float, t: datetime) -> float:
    if t1 == t0:
        return v0
    frac = (t - t0).total_seconds() / (t1 - t0).total_seconds()
    return v0 + frac * (v1 - v0)


def build_curve(hourly_times, hourly_vals, start_dt: datetime, end_dt: datetime, *, include_start=True, include_end=True):
    raw = []
    for t_str, val in zip(hourly_times, hourly_vals):
        t = parse_dt(t_str)
        raw.append((t, float(val)))
    raw.sort(key=lambda p: p[0])

    # Find neighbors for interpolation at boundaries
    def interp_at(target: datetime):
        for i in range(1, len(raw)):
            t0, v0 = raw[i - 1]
            t1, v1 = raw[i]
            if t0 <= target <= t1:
                return target, interpolate_value(t0, v0, t1, v1, target)
        return None

    pts = []
    if include_start:
        start_interp = interp_at(start_dt)
        if start_interp:
            pts.append(start_interp)

    for t, v in raw:
        if t <= start_dt or t >= end_dt:
            continue
        pts.append((t, v))

    if include_end:
        end_interp = interp_at(end_dt)
        if end_interp:
            pts.append(end_interp)

    # Format for output
    out = []
    for t, v in pts:
        out.append({"t": t.strftime("%-I:%M%p").lower(), "v": round(v)})
    return out


def fake_moon_curve(start_dt: datetime, end_dt: datetime):
    pts = []
    total_min = int((end_dt - start_dt).total_seconds() / 60)
    for h in range(0, total_min + 1, 120):
        t = start_dt + timedelta(minutes=h)
        phase = h / max(1, total_min)
        elev = max(0, 90 * math.sin(math.pi * phase))
        pts.append({"t": t.strftime("%-I:%M%p").lower(), "elev": round(elev)})
    return pts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lat", type=float, default=18.5204)
    ap.add_argument("--lon", type=float, default=73.8567)
    ap.add_argument("--units", choices=["c", "f"], default="f")
    ap.add_argument("--out", default="projects/clock75/ui/frame_real.json")
    args = ap.parse_args()

    data = fetch_open_meteo(args.lat, args.lon, args.units)

    hourly = data.get("hourly", {})
    daily = data.get("daily", {})
    current = data.get("current", {})

    now = parse_dt(current["time"]) if "time" in current else parse_dt(daily["sunrise"][0])

    # pick sunrise/sunset for "today" based on current date
    sunrise_list = [parse_dt(s) for s in daily.get("sunrise", [])]
    sunset_list = [parse_dt(s) for s in daily.get("sunset", [])]
    idx_today = 0
    for i, dt in enumerate(sunrise_list):
        if dt.date() >= now.date():
            idx_today = i
            break
    sunrise0 = sunrise_list[idx_today]
    sunset0 = sunset_list[idx_today] if idx_today < len(sunset_list) else sunset_list[0]
    sunrise1 = sunrise_list[min(idx_today + 1, len(sunrise_list) - 1)]

    hourly_times = hourly.get("time", [])
    hourly_temps = hourly.get("temperature_2m", [])

    actual_start = sunrise0
    actual_end = now
    # build actual from sunrise to now using hourly points, then add exact "now" temperature
    actual = build_curve(hourly_times, hourly_temps, actual_start, actual_end, include_end=False)
    actual.append({
        "t": now.strftime("%-I:%M%p").lower(),
        "v": round(current.get("temperature_2m", actual[-1]["v"] if actual else 0)),
    })

    # forecast starts at now (using current temp), then hourly points after now, ending at sunrise_next (interpolated)
    forecast_start = now
    forecast = [{
        "t": now.strftime("%-I:%M%p").lower(),
        "v": round(current.get("temperature_2m", actual[-1]["v"] if actual else 0)),
    }]
    # include hourly points strictly after now
    forecast += build_curve(hourly_times, hourly_temps, forecast_start, sunrise1, include_start=False, include_end=True)

    temp_vals = [p["v"] for p in actual + forecast]
    if temp_vals:
        tmin = min(temp_vals)
        tmax = max(temp_vals)
        range_min = (tmin // 10) * 10
        range_max = ((tmax + 9) // 10) * 10
        if range_max == range_min:
            range_max += 10
    else:
        range_min, range_max = 30, 80

    daily_entries = []
    today_date = now.date()
    for d, h, l in zip(daily.get("time", []), daily.get("temperature_2m_max", []), daily.get("temperature_2m_min", [])):
        d_date = datetime.fromisoformat(d).date()
        if d_date < today_date:
            continue
        daily_entries.append({
            "dow": datetime.fromisoformat(d).strftime("%a"),
            "high": str(round(h)),
            "low": str(round(l)),
        })

    frame = {
        "header": {
            "dow_date": dow_date(now),
            "tithi_line": "कार्तिक शुक्ल एकादशी",
            "time": now.strftime("%-I:%M"),
            "ampm": now.strftime("%p"),
            "tz_abbrev": data.get("timezone_abbreviation", ""),
        },
        "temps": {
            "outdoor": {
                "current": str(round(current.get("temperature_2m", 0))),
            },
            "indoor": {
                "current": "72",
            },
        },
        "forecast": {
            "daily": daily_entries,
        },
        "charts": {
            "xaxis": {
                "sunrise_local": hhmm(sunrise0),
                "sunset_local": hhmm(sunset0),
                "sunrise_next_local": hhmm(sunrise1),
            },
            "temp": {
                "range_min": range_min,
                "range_max": range_max,
                "actual": actual,
                "forecast": forecast,
            },
            "moon": {
                "range_min": 0,
                "range_max": 90,
                "curve": fake_moon_curve(sunrise0, sunrise1),
                "current": {
                    "t": now.strftime("%-I:%M%p").lower(),
                    "elev": 30,
                    "phase": 0.5,
                },
            },
        },
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(frame, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()

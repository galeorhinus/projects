#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json
import xml.sax.saxutils as saxutils


def get_value(data, path):
    cur = data
    for part in path.split('.'):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def fmt_value(val):
    if val is None:
        return ""
    if isinstance(val, float):
        return f"{val:.1f}"
    return str(val)


def parse_hhmm(value: str) -> int | None:
    if not value:
        return None
    try:
        raw = value.strip().lower().replace(" ", "")
        is_pm = raw.endswith("pm")
        is_am = raw.endswith("am")
        if is_pm or is_am:
            raw = raw[:-2]
        if ":" not in raw:
            return None
        h_str, m_str = raw.split(":", 1)
        h = int(h_str)
        m = int(m_str)
        if is_pm and h != 12:
            h += 12
        if is_am and h == 12:
            h = 0
        return h * 60 + m
    except Exception:
        return None


def map_time_to_x_minutes(t_min, start_min, x0, x1, duration_minutes):
    if t_min is None or start_min is None or duration_minutes <= 0:
        return x0
    # handle wrap
    delta = t_min - start_min
    if delta < 0:
        delta += 24 * 60
    if delta > duration_minutes:
        delta = duration_minutes
    return x0 + (x1 - x0) * (delta / duration_minutes)


def map_val_to_y(v, y0, y1, vmin, vmax):
    if vmax == vmin:
        return y1
    t = (v - vmin) / (vmax - vmin)
    return y1 - t * (y1 - y0)


def format_tick_label(mins):
    h = (mins // 60) % 24
    if h == 0:
        return "12a"
    if h < 12:
        return f"{h}a"
    if h == 12:
        return "12p"
    return f"{h-12}p"


def format_time_label_from_minutes(mins):
    h = (mins // 60) % 24
    m = mins % 60
    suffix = "a"
    if h >= 12:
        suffix = "p"
    hr12 = h % 12
    if hr12 == 0:
        hr12 = 12
    return f"{hr12}:{m:02d}{suffix}"


def emit_svg(layout, frame):
    canvas = layout["canvas"]
    width = canvas["width"]
    height = canvas["height"]
    view_box = canvas.get("viewBox", f"0 0 {width} {height}")
    styles = layout.get("styles", "").rstrip()

    charts = layout.get("charts", {})
    start_min = None
    duration_minutes = 24 * 60
    night_x = charts.get("night", {}).get("x", 530)
    if "charts" in frame and "xaxis" in frame["charts"]:
        sunrise_str = frame["charts"]["xaxis"].get("sunrise_local")
        sunset_str = frame["charts"]["xaxis"].get("sunset_local")
        start_min = parse_hhmm(sunrise_str)
        end_min = parse_hhmm(frame["charts"]["xaxis"].get("sunrise_next_local"))
        if start_min is not None and end_min is not None:
            duration_minutes = (end_min - start_min) + 24 * 60
        if start_min is not None and sunset_str and charts.get("temp"):
            sunset_min = parse_hhmm(sunset_str)
            if sunset_min is not None:
                night_x = map_time_to_x_minutes(
                    sunset_min,
                    start_min,
                    charts["temp"]["x0"],
                    charts["temp"]["x1"],
                    duration_minutes,
                )

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="{view_box}">')
    if styles:
        lines.append("  <defs>")
        lines.append("    <style>")
        for sline in styles.splitlines():
            lines.append(f"      {sline}")
        lines.append("    </style>")
        lines.append("  </defs>")

    # rects
    for r in layout.get("static", {}).get("rects", []):
        rx = r["x"]
        ry = r["y"]
        rw = r["w"]
        rh = r["h"]
        if r.get("fill") == "#000" and charts:
            night = charts.get("night", {})
            temp = charts.get("temp", {})
            rx = int(night_x)
            ry = int(night.get("y", ry))
            if temp.get("x1") is not None:
                rw = int(temp["x1"] - night_x)
            rh = int(night.get("h", rh))
        attrs = {
            "x": str(rx),
            "y": str(ry),
            "width": str(rw),
            "height": str(rh),
        }
        if "class" in r:
            attrs["class"] = r["class"]
        if "fill" in r:
            attrs["fill"] = r["fill"]
        attr_str = " ".join(f'{k}="{v}"' for k, v in attrs.items())
        lines.append(f"  <rect {attr_str}/>")

    # lines
    for ln in layout.get("static", {}).get("lines", []):
        attrs = {
            "x1": str(ln["x1"]),
            "y1": str(ln["y1"]),
            "x2": str(ln["x2"]),
            "y2": str(ln["y2"]),
        }
        if "class" in ln:
            attrs["class"] = ln["class"]
        if "strokeWidth" in ln:
            attrs["stroke-width"] = str(ln["strokeWidth"])
        attr_str = " ".join(f'{k}="{v}"' for k, v in attrs.items())
        lines.append(f"  <line {attr_str}/>")

    # text
    for t in layout.get("text", []):
        cls = t.get("class")
        x = t.get("x")
        y = t.get("y")
        anchor = t.get("anchor")
        text = t.get("text")
        if "bind" in t:
            text = fmt_value(get_value(frame, t["bind"]))
        attrs = {"x": str(x), "y": str(y)}
        if cls:
            attrs["class"] = cls
        if anchor:
            attrs["text-anchor"] = anchor
        attr_str = " ".join(f'{k}="{saxutils.escape(v)}"' for k, v in attrs.items())
        lines.append(f"  <text {attr_str}>{saxutils.escape(text or '')}</text>")

    # Y-axis ticks/labels (dynamic for temp)
    charts = layout.get("charts", {})
    if charts and "charts" in frame:
        temp_chart = charts.get("temp")
        temp_data = frame["charts"].get("temp", {})
        if temp_chart and temp_data:
            vmin = temp_data.get("range_min", temp_chart["min"])
            vmax = temp_data.get("range_max", temp_chart["max"])
            step = 10
            steps = int((vmax - vmin) / step)
            if steps > 0:
                pixel_step = (temp_chart["y1"] - temp_chart["y0"]) / steps
                yaxis = layout.get("y_temp_axis", {})
                labelx = int(yaxis.get("labelx", 26))
                label_y_offset = int(yaxis.get("label_y_offset", 0))
                tick_len = int(yaxis.get("tick_len", 10))
                tick_x0 = int(yaxis.get("tick_x0", 10))
                tick_x1 = tick_x0 + tick_len
                for i in range(steps + 1):
                    val = vmin + i * step
                    y = int(temp_chart["y1"] - i * pixel_step)
                    # tick
                    lines.append(f"  <line class=\"divider\" x1=\"{tick_x0}\" y1=\"{y}\" x2=\"{tick_x1}\" y2=\"{y}\"/>")
                    # skip last label at the top
                    if i == steps:
                        continue
                    # skip first label
                    if i == 0:
                        continue
                    lines.append(f"  <text class=\"label-xs\" x=\"{labelx}\" y=\"{y + label_y_offset}\">{val}</text>")

    # Moon elevation ticks/labels (dynamic 0..90 by 30s)
    charts = layout.get("charts", {})
    if charts and "charts" in frame:
        moon_chart = charts.get("moon")
        moon_data = frame["charts"].get("moon", {})
        if moon_chart and moon_data is not None:
            vmin = max(0, moon_data.get("range_min", moon_chart["min"]))
            vmax = moon_data.get("range_max", moon_chart["max"])
            step = 30
            steps = int((vmax - vmin) / step)
            if steps > 0:
                pixel_step = (moon_chart["y1"] - moon_chart["y0"]) / steps
                yaxis = layout.get("y_moon_axis", {})
                labelx = int(yaxis.get("labelx", 774))
                label_y_offset = int(yaxis.get("label_y_offset", 0))
                temp_axis = layout.get("y_temp_axis", {})
                tick_len = int(yaxis.get("tick_len", temp_axis.get("tick_len", 10)))
                tick_x2 = int(yaxis.get("tick_x2", 790))
                tick_x1 = tick_x2 - tick_len
                for i in range(steps + 1):
                    val = vmin + i * step
                    y = int(moon_chart["y1"] - i * pixel_step)
                    # tick
                    lines.append(f"  <line class=\"divider-inv\" x1=\"{tick_x1}\" y1=\"{y}\" x2=\"{tick_x2}\" y2=\"{y}\"/>")
                    # label (skip first/last)
                    if i == 0 or i == steps:
                        continue
                    lines.append(f"  <text class=\"label-inv\" x=\"{labelx}\" y=\"{y + label_y_offset}\" text-anchor=\"end\">{val}</text>")

    # dynamic x-axis ticks/labels
    xaxis = layout.get("charts", {}).get("xaxis")
    if xaxis and frame.get("charts", {}).get("xaxis"):
        start_str = get_value(frame, xaxis["start_time_source"])
        start_min = parse_hhmm(start_str)
        end_str = frame["charts"]["xaxis"].get("sunrise_next_local")
        end_min = parse_hhmm(end_str) if end_str else None
        if start_min is not None and end_min is not None:
            # sunrise_next_local is next-day sunrise; add 24h to span full day window
            duration_minutes = (end_min - start_min) + 24 * 60
        else:
            duration_minutes = int(xaxis["duration_hours"]) * 60
        interval = int(xaxis["tick_interval_hours"]) * 60
        tick_y = int(xaxis["tick_y"])
        tick_len = int(xaxis["tick_len"])
        label_y = int(xaxis["label_y"])
        label_x_offset = int(xaxis.get("label_x_offset", 0))

        # chart bounds from layout
        chart = layout.get("charts", {}).get("temp")
        if chart:
            x0 = chart["x0"]
            x1 = chart["x1"]

            # Tick marks: every 2 hours across the full 24h window starting at sunrise
            tick_times = []
            t_tick = start_min
            while t_tick is not None and t_tick <= start_min + duration_minutes:
                tick_times.append(t_tick)
                t_tick += interval

            # Labels: start at sunrise + 2.5h (rounded), stop 3h before next sunrise
            label_start = start_min + 150
            label_start = int(round(label_start / 60) * 60)
            label_end = None
            if end_min is not None:
                label_end = start_min + duration_minutes - 180

            label_times = []
            t_label = label_start
            while t_label is not None and t_label <= start_min + duration_minutes:
                if label_end is not None and t_label > label_end:
                    break
                label_times.append(t_label)
                t_label += interval

            # Left sunrise label at start
            if start_min is not None:
                label = format_time_label_from_minutes(start_min)
                label_class = xaxis["label_class_day"]
                label_x = int(x0) -2
                lines.append(f"  <text class=\"{label_class}\" x=\"{label_x}\" y=\"{label_y}\">{label}</text>")

            # Draw ticks for all tick times
            for tmin in tick_times:
                x = map_time_to_x_minutes(tmin, start_min, x0, x1, duration_minutes)
                is_night = x >= night_x
                tick_class = xaxis["tick_class_night"] if is_night else xaxis["tick_class_day"]
                # bottom-justify ticks to the axis line
                lines.append(f"  <line class=\"{tick_class}\" x1=\"{int(x)}\" y1=\"{tick_y-tick_len}\" x2=\"{int(x)}\" y2=\"{tick_y}\"/>")

            # Draw labels only for the label times
            for tmin in label_times:
                x = map_time_to_x_minutes(tmin, start_min, x0, x1, duration_minutes)
                label_class = xaxis["label_class_day"]
                label = format_tick_label(tmin)
                label_x = int(x) - 15 + label_x_offset
                lines.append(f"  <text class=\"{label_class}\" x=\"{label_x}\" y=\"{label_y}\">{label}</text>")

            # Add explicit next-sunrise label at right edge
            if end_min is not None:
                x = x1
                label = format_time_label_from_minutes(end_min)
                label_class = xaxis["label_class_day"]
                # anchor to end and inset to avoid clipping
                label_x = int(x) - 6 + label_x_offset
                lines.append(f"  <text class=\"{label_class}\" x=\"{label_x}\" y=\"{label_y}\" text-anchor=\"end\">{label}</text>")

    # forecast
    forecast = layout.get("forecast")
    if forecast and "forecast" in frame:
        daily = frame["forecast"].get("daily", [])
        start_y = forecast["start_y"]
        row_h = forecast["row_h"]
        for i, day in enumerate(daily[: forecast["rows"]]):
            y = start_y + i * row_h
            dow = day.get("dow", "")
            temps = f"{day.get('high','')}/{day.get('low','')}"
            lines.append(f"  <text class=\"{forecast['class']}\" x=\"{forecast['dow_x']}\" y=\"{y}\" text-anchor=\"end\">{dow}</text>")
            lines.append(f"  <text class=\"{forecast['class']}\" x=\"{forecast['temp_x']}\" y=\"{y}\" text-anchor=\"start\">{temps}</text>")

    # charts
    if charts and "charts" in frame:
        start_str = frame["charts"]["xaxis"].get("sunrise_local")
        start_min = parse_hhmm(start_str)
        end_str = frame["charts"]["xaxis"].get("sunrise_next_local")
        end_min = parse_hhmm(end_str) if end_str else None
        if start_min is not None and end_min is not None:
            duration_minutes = (end_min - start_min) + 24 * 60
        else:
            duration_minutes = 24 * 60

        def emit_lines(pts, stroke, stroke_width=3, dash=None):
            if len(pts) < 2:
                return
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                attrs = {
                    "x1": str(int(x1)),
                    "y1": str(int(y1)),
                    "x2": str(int(x2)),
                    "y2": str(int(y2)),
                    "stroke": stroke,
                    "stroke-width": str(stroke_width),
                    "stroke-linecap": "round",
                    "stroke-linejoin": "round",
                }
                if dash:
                    attrs["stroke-dasharray"] = dash
                attr_str = " ".join(f'{k}="{v}"' for k, v in attrs.items())
                lines.append(f"  <line {attr_str}/>")

        def split_pts_at_x(pts, split_x):
            if len(pts) < 2:
                return pts, []
            day = []
            night = []
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                if x1 <= split_x and x2 <= split_x:
                    if not day:
                        day.append((x1, y1))
                    day.append((x2, y2))
                    continue
                if x1 >= split_x and x2 >= split_x:
                    if not night:
                        night.append((x1, y1))
                    night.append((x2, y2))
                    continue
                # Segment crosses boundary; interpolate
                if x2 != x1:
                    t = (split_x - x1) / (x2 - x1)
                else:
                    t = 0.0
                y_split = y1 + t * (y2 - y1)
                if x1 < split_x:
                    if not day:
                        day.append((x1, y1))
                    day.append((split_x, y_split))
                    night.append((split_x, y_split))
                    night.append((x2, y2))
                else:
                    if not night:
                        night.append((x1, y1))
                    night.append((split_x, y_split))
                    day.append((split_x, y_split))
                    day.append((x2, y2))
            return day, night

        # temp curve
        temp = charts.get("temp")
        if temp:
            actual = frame["charts"]["temp"].get("actual", [])
            forecast_curve = frame["charts"]["temp"].get("forecast", [])
            pts = []
            tmin = frame["charts"]["temp"].get("range_min", temp["min"])
            tmax = frame["charts"]["temp"].get("range_max", temp["max"])
            for p in actual:
                t_min = parse_hhmm(p["t"])
                x = map_time_to_x_minutes(t_min, start_min, temp["x0"], temp["x1"], duration_minutes)
                y = map_val_to_y(p["v"], temp["y0"], temp["y1"], tmin, tmax)
                pts.append((x, y))
            # sort by x and drop duplicate x to avoid vertical segments
            pts_sorted = []
            for x, y in sorted(pts, key=lambda p: p[0]):
                if pts_sorted and int(x) == int(pts_sorted[-1][0]):
                    pts_sorted[-1] = (x, y)
                else:
                    pts_sorted.append((x, y))
            day_pts, night_pts = split_pts_at_x(pts_sorted, night_x)
            emit_lines(day_pts, "#000", 3)
            emit_lines(night_pts, "#fff", 5)

            pts = []
            for p in forecast_curve:
                t_min = parse_hhmm(p["t"])
                x = map_time_to_x_minutes(t_min, start_min, temp["x0"], temp["x1"], duration_minutes)
                y = map_val_to_y(p["v"], temp["y0"], temp["y1"], tmin, tmax)
                pts.append((x, y))
            pts_sorted = []
            for x, y in sorted(pts, key=lambda p: p[0]):
                if pts_sorted and int(x) == int(pts_sorted[-1][0]):
                    pts_sorted[-1] = (x, y)
                else:
                    pts_sorted.append((x, y))
            day_pts, night_pts = split_pts_at_x(pts_sorted, night_x)
            emit_lines(day_pts, "#000", 3, dash="8,6")
            emit_lines(night_pts, "#fff", 5, dash="8,6")

        # moon curve
        moon = charts.get("moon")
        if moon:
            curve = frame["charts"]["moon"].get("curve", [])
            pts = []
            mmin = max(0, frame["charts"]["moon"].get("range_min", moon["min"]))
            mmax = frame["charts"]["moon"].get("range_max", moon["max"])
            for p in curve:
                t_min = parse_hhmm(p["t"])
                x = map_time_to_x_minutes(t_min, start_min, moon["x0"], moon["x1"], duration_minutes)
                y = map_val_to_y(p["elev"], moon["y0"], moon["y1"], mmin, mmax)
                pts.append((x, y))
            if len(pts) >= 2:
                pts_sorted = []
                for x, y in sorted(pts, key=lambda p: p[0]):
                    if pts_sorted and int(x) == int(pts_sorted[-1][0]):
                        pts_sorted[-1] = (x, y)
                    else:
                        pts_sorted.append((x, y))
                day_pts, night_pts = split_pts_at_x(pts_sorted, night_x)
                emit_lines(day_pts, "#000", 3, dash="3,4")
                emit_lines(night_pts, "#fff", 5)

            # Moon icon at current time (simple phase hint)
            current = frame["charts"]["moon"].get("current")
            if current and start_min is not None:
                t_min = parse_hhmm(current.get("t"))
                x = map_time_to_x_minutes(t_min, start_min, moon["x0"], moon["x1"], duration_minutes)
                y = map_val_to_y(current.get("elev", 0), moon["y0"], moon["y1"], mmin, mmax)
                r = 6
                lines.append(f"  <circle cx=\"{int(x)}\" cy=\"{int(y)}\" r=\"{r}\" fill=\"#000\"/>")
                phase = current.get("phase", 0.5)
                # offset white circle to suggest crescent; clamp to [-r, r]
                offset = max(-r, min(r, int((0.5 - phase) * 2 * r)))
                lines.append(f"  <circle cx=\"{int(x) + offset}\" cy=\"{int(y)}\" r=\"{r-1}\" fill=\"#fff\"/>")

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("layout_json")
    ap.add_argument("out_svg")
    ap.add_argument("--frame", default=None)
    args = ap.parse_args()

    layout = json.loads(Path(args.layout_json).read_text())
    frame = json.loads(Path(args.frame).read_text()) if args.frame else {}
    svg = emit_svg(layout, frame)
    Path(args.out_svg).write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()

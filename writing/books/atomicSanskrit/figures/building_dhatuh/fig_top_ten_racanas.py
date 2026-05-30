#!/usr/bin/env python3
"""Render the top-ten racana scaffolds figure as plain SVG.

The figure is dependency-free so the scaffold icons stay rebuildable even when
the local matplotlib/numpy stack is unavailable. Icon geometry mirrors
figures/icons/build_scaffold_icons.py: consonants stay on the upper rail,
vowels stay on the lower rail, and adjacent consonants are grouped into one
split timing envelope.
"""

from __future__ import annotations

import html
import math
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUT = PROJECT_ROOT / "figures" / "build" / "building_dhatuh_top_ten_racanas.svg"

FILL = "#222222"
ACCENT = "#888888"
TAIL_FILL = "#e0e0e0"
TAIL_EDGE = "#bbbbbb"
EDGE_COLOR = "#000000"
TEXT = "#1a1a1a"
MUTED = "#555555"
ICON = "#888888"
GRID = "#cccccc"


# --- Icon geometry, matched to figures/icons/build_scaffold_icons.py ---

ICON_H = 24.0
EDGE = ICON_H / math.sqrt(3)
WIDTH_BY_CLASS = {"C": EDGE / 2, "V1": EDGE, "V2": EDGE * 2}
AMP = ICON_H / 4
VYANJANA_RAIL_Y = -AMP
SVARA_RAIL_Y = AMP

PARTICLES_BY_TEMPLATE = {
    "CV1C": ["C", "V1", "C"],
    "CCV1C": ["C", "C", "V1", "C"],
    "CV1CC": ["C", "V1", "C", "C"],
    "CV2C": ["C", "V2", "C"],
    "CV2": ["C", "V2"],
    "V1C": ["V1", "C"],
    "CCV2C": ["C", "C", "V2", "C"],
    "CV1": ["C", "V1"],
    "CCV2": ["C", "C", "V2"],
    "CCV1CC": ["C", "C", "V1", "C", "C"],
}


def hex_points(cx: float, cy: float, w: float) -> list[tuple[float, float]]:
    e = EDGE
    return [
        (cx - w / 2, cy - ICON_H / 2),
        (cx + w / 2, cy - ICON_H / 2),
        (cx + w / 2 + e / 2, cy),
        (cx + w / 2, cy + ICON_H / 2),
        (cx - w / 2, cy + ICON_H / 2),
        (cx - w / 2 - e / 2, cy),
    ]


def display_units(particles: list[str]) -> list[dict]:
    units: list[dict] = []
    i = 0
    while i < len(particles):
        p = particles[i]
        if p == "C":
            run = [p]
            j = i + 1
            while j < len(particles) and particles[j] == "C":
                run.append(particles[j])
                j += 1
            if len(run) > 1:
                units.append({"kind": "cluster", "width": EDGE * len(run) / 2})
                i = j
                continue
        units.append({"kind": "particle", "class": p})
        i += 1
    return units


def unit_width(unit: dict) -> float:
    if unit["kind"] == "cluster":
        return unit["width"]
    return WIDTH_BY_CLASS[unit["class"]]


def unit_rail_y(unit: dict) -> float:
    if unit["kind"] == "cluster":
        return VYANJANA_RAIL_Y
    return VYANJANA_RAIL_Y if unit["class"] == "C" else SVARA_RAIL_Y


def icon_layout(template: str) -> tuple[list[tuple[float, float]], list[dict], tuple[float, float, float, float]]:
    units = display_units(PARTICLES_BY_TEMPLATE[template])
    positions: list[tuple[float, float]] = []
    for i, unit in enumerate(units):
        cy = unit_rail_y(unit)
        if i == 0:
            positions.append((0.0, cy))
            continue
        prev = units[i - 1]
        prev_w = unit_width(prev)
        prev_cy = positions[-1][1]
        w = unit_width(unit)
        rail_step = EDGE / 2 if prev_cy != cy else EDGE
        positions.append((positions[-1][0] + (prev_w + w) / 2 + rail_step, cy))

    xs: list[float] = []
    ys: list[float] = []
    for (cx, cy), unit in zip(positions, units):
        for x, y in hex_points(cx, cy, unit_width(unit)):
            xs.append(x)
            ys.append(y)
    return positions, units, (min(xs), min(ys), max(xs), max(ys))


def icon_render_size(template: str, target_h: float = 26.0) -> tuple[float, float]:
    _positions, _units, (xmin, ymin, xmax, ymax) = icon_layout(template)
    scale = target_h / (ymax - ymin)
    return (xmax - xmin) * scale, target_h


def render_icon(template: str, x: float, y: float, target_h: float = 26.0) -> str:
    positions, units, (xmin, ymin, _xmax, ymax) = icon_layout(template)
    scale = target_h / (ymax - ymin)
    parts = [f'<g transform="translate({x:.1f},{y:.1f}) scale({scale:.4f})">']
    for (cx, cy), unit in zip(positions, units):
        pts = " ".join(f"{px - xmin:.2f},{py - ymin:.2f}" for px, py in hex_points(cx, cy, unit_width(unit)))
        parts.append(f'<polygon points="{pts}" fill="{ICON}"/>')
    parts.append("</g>")
    return "\n".join(parts)


def render_icon_right(template: str, right_x: float, y: float, target_h: float = 26.0) -> str:
    icon_w, _icon_h = icon_render_size(template, target_h=target_h)
    return render_icon(template, right_x - icon_w, y, target_h=target_h)


# --- Bar chart data ---

TEMPLATES = [
    ("CV1C", "गमादि", "gamādi", "2", 926, 42.7),
    ("CCV1C", "स्पदादि", "spadādi", "2½", 232, 10.7),
    ("CV1CC", "मन्थादि", "manthādi", "2½", 216, 10.0),
    ("CV2C", "वाचादि", "vācādi", "3", 214, 9.9),
    ("CV2", "धादि", "dhādi", "2½", 89, 4.1),
    ("V1C", "इषादि", "iṣādi", "1½", 70, 3.2),
    ("CCV2C", "ह्रादादि", "hrādādi", "3½", 65, 3.0),
    ("CV1", "क्रादि", "krādi", "1½", 64, 3.0),
    ("CCV2", "स्थादि", "sthādi", "3", 49, 2.3),
    ("CCV1CC", "स्पर्धादि", "spardhādi", "3", 48, 2.2),
    ("(tail)", "", "59 other racanāḥ", "1 to 6", 195, 9.0),
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def text(x: float, y: float, content: str, size: int = 17, color: str = TEXT,
         anchor: str = "start", weight: str = "400", style: str = "normal") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" '
        f'font-family="Charter, Adobe Devanagari, Noto Sans Devanagari, Georgia, serif" '
        f'font-size="{size}" font-weight="{weight}" font-style="{style}" '
        f'text-anchor="{anchor}" dominant-baseline="middle">{esc(content)}</text>'
    )


def main() -> None:
    OUT.parent.mkdir(exist_ok=True)

    width = 870.38
    height = 680.51
    left = 82.0
    right = 22.0
    top = 34.0
    row_gap = 52.0
    bar_h = 38.0
    icon_right_x = 69.0
    bar_x = left
    max_count = 926
    bar_w_max = width - left - right - 4
    scale_x = bar_w_max / max_count

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.2f}pt" height="{height:.2f}pt" viewBox="0 0 {width:.2f} {height:.2f}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
    ]

    # Light bottom axis.
    axis_y = top + row_gap * len(TEMPLATES) + 14
    parts.append(f'<line x1="{bar_x:.1f}" y1="{axis_y:.1f}" x2="{width - right:.1f}" y2="{axis_y:.1f}" stroke="{EDGE_COLOR}" stroke-width="0.8"/>')
    for tick in (0, 250, 500, 750):
        tx = bar_x + tick * scale_x
        parts.append(f'<line x1="{tx:.1f}" y1="{axis_y:.1f}" x2="{tx:.1f}" y2="{axis_y + 5:.1f}" stroke="{EDGE_COLOR}" stroke-width="0.7"/>')
        parts.append(text(tx, axis_y + 21, str(tick), size=16, color="#333333", anchor="middle"))
        if tick:
            parts.append(f'<line x1="{tx:.1f}" y1="{top - 8:.1f}" x2="{tx:.1f}" y2="{axis_y:.1f}" stroke="{GRID}" stroke-width="0.35" opacity="0.45"/>')
    parts.append(text((bar_x + width - right) / 2, axis_y + 43, "Count in the Dhātupāṭha", size=20, anchor="middle"))

    for i, (template, deva, iast, matra, count, pct) in enumerate(TEMPLATES):
        y = top + i * row_gap
        y_mid = y + bar_h / 2
        bw = count * scale_x
        fill = FILL if i == 0 else (TAIL_FILL if template == "(tail)" else ACCENT)
        edge = FILL if i == 0 else (TAIL_EDGE if template == "(tail)" else EDGE_COLOR)
        parts.append(
            f'<rect x="{bar_x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bar_h:.1f}" '
            f'fill="{fill}" stroke="{edge}" stroke-width="0.5"/>'
        )

        if template != "(tail)":
            parts.append(render_icon_right(template, icon_right_x, y_mid - 13, target_h=26.0))
        else:
            parts.append(text(icon_right_x, y_mid, "Other", size=18, color=MUTED, anchor="end", style="italic"))

        count_text = f"{count} ({pct:.1f}%)"
        if deva:
            label = f"{deva} ({iast})  ·  {matra} mātrā"
        else:
            label = f"{iast}  ·  {matra} mātrā"

        if i == 0:
            parts.append(text(bar_x + bw / 2, y_mid, label, size=20, color="#ffffff", anchor="middle"))
            parts.append(text(bar_x + bw - 10, y_mid, count_text, size=17, color="#ffffff", anchor="end"))
        else:
            parts.append(text(bar_x + bw + 12, y_mid, count_text, size=17))
            label_color = MUTED if template == "(tail)" else TEXT
            label_style = "italic" if template == "(tail)" else "normal"
            parts.append(text(bar_x + bw + 160, y_mid, label, size=18, color=label_color, style=label_style))

    parts.append("</svg>\n")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()

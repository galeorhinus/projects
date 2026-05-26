#!/usr/bin/env python3
"""Render a foundry-style illustration for the dhatu scaffold discovery.

The figure shows the argument visually:

  47 varnah -> 47 racana scaffold-molds -> 2,168 measured dhatavah

The scaffold geometry mirrors the Ch10 icon convention: vyanjanas remain on
the upper rail, svaras remain on the lower rail, and adjacent consonants share
one split timing envelope.
"""

from __future__ import annotations

import html
import math
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUT = PROJECT_ROOT / "figures" / "build" / "building_dhatuh_scaffold_foundry.svg"

W = 1200
H = 820

TEXT = "#1a1a1a"
MUTED = "#555555"
LINE = "#333333"
GRID = "#d0d0d0"
PALE = "#f5f5f5"
MID = "#d9d9d9"
DARK = "#222222"
ICON = "#888888"


# --- Scaffold icon geometry, matched to figures/icons/build_scaffold_icons.py ---

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
    "CV2CV1": ["C", "V2", "C", "V1"],
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def text(
    x: float,
    y: float,
    content: str,
    size: int = 18,
    color: str = TEXT,
    anchor: str = "start",
    weight: str = "400",
    style: str = "normal",
    family: str | None = None,
) -> str:
    fam = family or "Charter, Adobe Devanagari, Noto Sans Devanagari, Georgia, serif"
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" '
        f'font-family="{fam}" font-size="{size}" font-weight="{weight}" '
        f'font-style="{style}" text-anchor="{anchor}" '
        f'dominant-baseline="middle">{esc(content)}</text>'
    )


def line(x1: float, y1: float, x2: float, y2: float, color: str = LINE, width: float = 2.0, opacity: float = 1.0) -> str:
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width:.1f}" opacity="{opacity:.2f}"/>'
    )


def rounded_rect(x: float, y: float, w: float, h: float, r: float = 14, fill: str = PALE, stroke: str = LINE, sw: float = 2.0) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw:.1f}"/>'
    )


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


def render_scaffold(
    template: str,
    x: float,
    y: float,
    target_h: float = 42,
    fill: str = "none",
    stroke: str = LINE,
    sw: float = 2.0,
    opacity: float = 1.0,
) -> str:
    positions, units, (xmin, ymin, _xmax, ymax) = icon_layout(template)
    scale = target_h / (ymax - ymin)
    parts = [f'<g transform="translate({x:.1f},{y:.1f}) scale({scale:.4f})" opacity="{opacity:.2f}">']
    for (cx, cy), unit in zip(positions, units):
        pts = " ".join(f"{px - xmin:.2f},{py - ymin:.2f}" for px, py in hex_points(cx, cy, unit_width(unit)))
        parts.append(
            f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw / scale:.2f}" '
            f'stroke-linejoin="round"/>'
        )
    parts.append("</g>")
    return "\n".join(parts)


def scaffold_size(template: str, target_h: float = 42) -> tuple[float, float]:
    _positions, _units, (xmin, ymin, xmax, ymax) = icon_layout(template)
    scale = target_h / (ymax - ymin)
    return (xmax - xmin) * scale, target_h


def render_scaffold_centered(template: str, cx: float, y: float, target_h: float = 42, **kwargs) -> str:
    w, _h = scaffold_size(template, target_h)
    return render_scaffold(template, cx - w / 2, y, target_h, **kwargs)


def funnel(cx: float, top_y: float, label: str, sublabel: str, template: str) -> str:
    top_w = 152
    bot_w = 62
    h = 126
    throat_h = 22
    x1 = cx - top_w / 2
    x2 = cx + top_w / 2
    bx1 = cx - bot_w / 2
    bx2 = cx + bot_w / 2
    y2 = top_y + h
    pts = f"{x1:.1f},{top_y:.1f} {x2:.1f},{top_y:.1f} {bx2:.1f},{y2:.1f} {bx1:.1f},{y2:.1f}"
    icon_y = y2 + 34
    parts = [
        f'<polygon points="{pts}" fill="#eeeeee" stroke="{LINE}" stroke-width="2.2" stroke-linejoin="round"/>',
        f'<rect x="{bx1:.1f}" y="{y2:.1f}" width="{bot_w:.1f}" height="{throat_h:.1f}" fill="#eeeeee" stroke="{LINE}" stroke-width="2.2"/>',
        text(cx, top_y - 18, label, 21, TEXT, "middle", "700"),
        text(cx, top_y + 28, sublabel, 15, MUTED, "middle", style="italic"),
        render_scaffold_centered(template, cx, icon_y, target_h=46, fill="#ffffff", stroke=LINE, sw=2.2),
    ]
    return "\n".join(parts)


def flow_path(x1: float, y1: float, x2: float, y2: float, label: str, dx: float = 0) -> str:
    c1x = x1 + dx
    c1y = y1 + 44
    c2x = x2 - dx
    c2y = y2 - 44
    path = (
        f'<path d="M {x1:.1f},{y1:.1f} C {c1x:.1f},{c1y:.1f} {c2x:.1f},{c2y:.1f} {x2:.1f},{y2:.1f}" '
        f'fill="none" stroke="{GRID}" stroke-width="2.0" stroke-dasharray="4 8" marker-end="url(#arrow)"/>'
    )
    midx = (x1 + x2) / 2 + dx * 0.15
    midy = (y1 + y2) / 2
    return path + "\n" + text(midx, midy, label, 22, DARK, "middle", family="Adobe Devanagari, Noto Sans Devanagari, serif")


def filled_example(cx: float, y: float, template: str, deva: str, iast: str) -> str:
    icon_y = y
    parts = [
        render_scaffold_centered(template, cx, icon_y, target_h=34, fill=ICON, stroke="none", sw=0),
        text(cx, icon_y + 58, deva, 25, DARK, "middle", weight="700"),
        text(cx, icon_y + 84, iast, 15, MUTED, "middle", style="italic"),
    ]
    return "\n".join(parts)


def tiny_atom(x: float, y: float, template: str, fill: str = "#777777") -> str:
    return render_scaffold(template, x, y, target_h=13, fill=fill, stroke="none", sw=0, opacity=0.75)


def jagged_break(x: float, y: float, h: float) -> str:
    pts = [
        (x, y), (x + 14, y + 22), (x - 8, y + 44), (x + 14, y + 66),
        (x - 8, y + 88), (x + 14, y + 110), (x, y + h)
    ]
    return f'<polyline points="{" ".join(f"{px:.1f},{py:.1f}" for px, py in pts)}" fill="none" stroke="{LINE}" stroke-width="2.5"/>'


def rotated_particle(char: str, x: float, y: float, angle: float, size: int = 24, color: str = DARK) -> str:
    return (
        f'<text x="0" y="0" fill="{color}" '
        f'font-family="Adobe Devanagari, Noto Sans Devanagari, serif" '
        f'font-size="{size}" font-weight="700" text-anchor="middle" dominant-baseline="middle" '
        f'transform="translate({x:.1f},{y:.1f}) rotate({angle:.1f})">{esc(char)}</text>'
    )


def atom_symbol(template: str, deva: str, cx: float, cy: float, angle: float = 0, target_h: float = 34) -> str:
    icon_w, icon_h = scaffold_size(template, target_h)
    parts = [f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({angle:.1f})">']
    parts.append(render_scaffold(template, -icon_w / 2, -icon_h / 2, target_h=target_h, fill=ICON, stroke="none", sw=0, opacity=0.9))
    parts.append(
        f'<text x="0" y="5" fill="{DARK}" font-family="Adobe Devanagari, Noto Sans Devanagari, serif" '
        f'font-size="{max(14, int(target_h * 0.48))}" font-weight="700" text-anchor="middle" '
        f'dominant-baseline="middle">{esc(deva)}</text>'
    )
    parts.append("</g>")
    return "\n".join(parts)


def filled_atom(
    template: str,
    labels: list[str],
    cx: float,
    cy: float,
    angle: float = 0,
    target_h: float = 46,
    fill: str = ICON,
) -> str:
    """Render a filled scaffold with Devanagari particles in their tiles."""
    positions, units, (xmin, ymin, xmax, ymax) = icon_layout(template)
    scale = target_h / (ymax - ymin)
    w = (xmax - xmin) * scale
    h = target_h
    parts = [
        f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({angle:.1f}) translate({-w / 2:.1f},{-h / 2:.1f})">'
    ]
    for (ux, uy), unit in zip(positions, units):
        pts = " ".join(
            f"{(px - xmin) * scale:.2f},{(py - ymin) * scale:.2f}"
            for px, py in hex_points(ux, uy, unit_width(unit))
        )
        parts.append(f'<polygon points="{pts}" fill="{fill}" stroke="none" opacity="0.92"/>')

    for label, (ux, uy), unit in zip(labels, positions, units):
        tx = (ux - xmin) * scale
        ty = (uy - ymin) * scale + target_h * 0.055
        fs = target_h * (0.24 if unit["kind"] == "cluster" else 0.30)
        parts.append(
            f'<text x="{tx:.2f}" y="{ty:.2f}" fill="{DARK}" '
            f'font-family="Adobe Devanagari, Noto Sans Devanagari, serif" '
            f'font-size="{fs:.1f}" font-weight="700" text-anchor="middle" '
            f'dominant-baseline="middle">{esc(label)}</text>'
        )
    parts.append("</g>")
    return "\n".join(parts)


def main() -> None:
    OUT.parent.mkdir(exist_ok=True)

    parts: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}pt" height="{H}pt" viewBox="0 0 {W} {H}">',
        "<defs>",
        '<marker id="arrow" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto" markerUnits="strokeWidth">',
        f'<path d="M0,0 L0,6 L8,3 z" fill="{GRID}"/>',
        "</marker>",
        "</defs>",
        '<rect width="100%" height="100%" fill="#ffffff"/>',
    ]

    # Title and source.
    parts.append(text(W / 2, 36, "47 varṇāḥ pass through 47 racanā scaffolds and produce 2,168 dhātavaḥ", 25, TEXT, "middle", "700"))

    source_x, source_y, source_w, source_h = 62, 82, 220, 116
    parts.append(rounded_rect(source_x, source_y, source_w, source_h, r=18, fill="#fbfbfb", stroke=LINE, sw=2.4))
    parts.append(text(source_x + source_w / 2, source_y + 47, "४७ वर्णाः", 35, DARK, "middle", "700", family="Adobe Devanagari, Noto Sans Devanagari, serif"))
    parts.append(text(source_x + source_w / 2, source_y + 84, "47 varṇāḥ", 21, MUTED, "middle", style="italic"))
    spout_x = source_x + source_w / 2 - 28
    spout_y = source_y + source_h - 1
    parts.append(
        f'<path d="M {spout_x:.1f},{spout_y:.1f} L {spout_x + 56:.1f},{spout_y:.1f} '
        f'L {spout_x + 56:.1f},{spout_y + 54:.1f} L {spout_x:.1f},{spout_y + 54:.1f} Z" '
        f'fill="#fbfbfb" stroke="{LINE}" stroke-width="2.4"/>'
    )

    # Broad stream behind particles. It enters each scaffold from the upper-left
    # and exits along the upper-right edge.
    stream = (
        "M 174,252 "
        "C 226,302 258,224 315,224 "
        "C 377,224 414,224 471,224 "
        "C 520,224 552,224 618,224 "
        "C 668,224 708,224 812,224 "
        "C 862,224 898,224 925,224 "
        "C 988,224 1035,224 1102,224"
    )
    parts.append(f'<path d="{stream}" fill="none" stroke="#eeeeee" stroke-width="54" stroke-linecap="round"/>')
    parts.append(f'<path d="{stream}" fill="none" stroke="#c9c9c9" stroke-width="2.0" stroke-dasharray="6 10"/>')
    parts.append(f'<path id="varna-flow" d="{stream}" fill="none" stroke="none"/>')

    # Scaffolds as unlabeled molds.
    scaffold_specs = [
        (395, 184, "CCV1C", "2½ mātrās"),
        (575, 184, "CV1", "1½ mātrās"),
        (750, 184, "CV1C", "2 mātrās"),
        (1000, 184, "CV2C", "3 mātrās"),
    ]
    for cx, y, template, matra_label in scaffold_specs:
        parts.append(render_scaffold_centered(template, cx, y, target_h=104, fill="#ffffff", stroke=LINE, sw=2.4, opacity=0.98))
        parts.append(text(cx, y + 124, matra_label, 17, MUTED, "middle", style="italic"))
    parts.append(text(873, 238, "…", 44, MUTED, "middle"))

    # The varnas themselves form the stream, following the path through the
    # scaffold-molds.
    varna_stream = (
        "अआइईउऊऋॠऌएऐओऔ"
        "कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह"
        "अआइईउऊऋॠऌएऐओऔ"
        "कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह"
    )
    parts.append(
        f'<text fill="{DARK}" font-family="Adobe Devanagari, Noto Sans Devanagari, serif" '
        f'font-size="30" font-weight="700" letter-spacing="1.2" dominant-baseline="middle">'
        f'<textPath href="#varna-flow" xlink:href="#varna-flow" startOffset="0%">{esc(varna_stream)}</textPath>'
        f'</text>'
    )

    # Small note for the hidden remainder without labeling the visible molds.
    parts.append(text(700, 348, "four scaffold-molds shown; the full measured set contains 47 racanāḥ", 17, MUTED, "middle", style="italic"))

    # Finished atoms drop from each scaffold into the bin.
    drop_paths = [
        "M 395,342 C 374,414 356,506 332,610",
        "M 575,342 C 572,420 576,512 586,610",
        "M 750,342 C 783,420 830,520 858,610",
        "M 1000,342 C 1028,414 1051,506 1012,610",
    ]
    for d in drop_paths:
        parts.append(f'<path d="{d}" fill="none" stroke="#eeeeee" stroke-width="34" stroke-linecap="round" opacity="0.72"/>')
        parts.append(f'<path d="{d}" fill="none" stroke="#c9c9c9" stroke-width="1.6" stroke-dasharray="5 9" opacity="0.8"/>')

    falling_groups = [
        [
            ("CCV1C", ["स्प", "अ", "द्"], 354, 372, -14),
            ("CCV1C", ["क्ल", "इ", "द्"], 430, 448, 12),
        ],
        [
            ("CV1", ["क्", "ऋ"], 548, 378, 9),
            ("CV1", ["ह्", "ऋ"], 615, 461, -11),
        ],
        [
            ("CV1C", ["ग", "अ", "म्"], 715, 375, -9),
            ("CV1C", ["प", "अ", "च्"], 780, 450, 14),
            ("CV1C", ["व", "अ", "द्"], 842, 517, -16),
        ],
        [
            ("CV2C", ["व्", "आ", "च्"], 981, 372, 13),
            ("CV2C", ["ध्", "आ", "व्"], 1045, 458, -12),
        ],
    ]
    for group in falling_groups:
        for template, labels, x, y, angle in group:
            parts.append(filled_atom(template, labels, x, y, angle=angle, target_h=46))

    # Bottom dhatu inventory bin.
    tray_x, tray_y, tray_w, tray_h = 96, 610, 1008, 170
    parts.append(rounded_rect(tray_x, tray_y, tray_w, tray_h, r=20, fill="#f4f4f4", stroke=LINE, sw=2.2))
    parts.append(text(tray_x + 34, tray_y + 42, "2,168 dhātavaḥ", 30, TEXT, weight="700"))
    parts.append(text(tray_x + 34, tray_y + 78, "filled scaffolds in the measured Dhātupāṭha inventory", 18, MUTED, style="italic"))

    bin_atoms = [
        ("CV1C", ["ग", "अ", "म्"]), ("CV1C", ["प", "अ", "च्"]), ("CV1C", ["व", "अ", "द्"]),
        ("CCV1C", ["स्प", "अ", "द्"]), ("CCV1C", ["क्ल", "इ", "द्"]), ("CV1CC", ["म", "अ", "न्थ्"]),
        ("CV1CC", ["क", "अ", "र्द्"]), ("CV2C", ["व्", "आ", "च्"]), ("CV2", ["ध्", "आ"]),
        ("CV1", ["क्", "ऋ"]), ("V1C", ["इ", "ष्"]), ("CCV2", ["स्थ", "आ"]),
        ("CCV2C", ["ह्र", "आ", "द्"]), ("CV2C", ["ध्", "आ", "व्"]), ("CCV1CC", ["स्प", "अ", "र्ध्"]),
        ("CV1C", ["न", "अ", "म्"]), ("CV1", ["ह्", "ऋ"]), ("CV2C", ["ग्", "आ", "ह्"]),
    ]
    x0, y0 = tray_x + 360, tray_y + 33
    for i, (template, labels) in enumerate(bin_atoms):
        row = i // 6
        col = i % 6
        x = x0 + col * 96 + (row % 2) * 14
        y = y0 + row * 43
        angle = [-7, 3, -3, 8, -10, 5][col]
        parts.append(filled_atom(template, labels, x, y, angle=angle, target_h=27, fill="#8a8a8a"))
    parts.append(text(tray_x + tray_w - 34, tray_y + tray_h - 28, "not a word-list; an atom inventory", 18, MUTED, "end"))

    parts.append("</svg>\n")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate Ch8 Figure 8.2: the mouth-to-varga control panel.

The figure links Sanskrit's 5x5 *sparśa* matrix to four physical controls:
contact station, breath effort, vocal-cord vibration, and nasal release.
It is schematic by design, not anatomical.
"""

from __future__ import annotations

import html
import math
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUT = Path(__file__).resolve().parent / "control_panel.from-py.svg"

DEV_FONT = (
    "Noto Sans Devanagari, Kohinoor Devanagari, Devanagari MT, "
    "Arial Unicode MS, sans-serif"
)
LATIN_FONT = "Charter, Georgia, Times, serif"

TEXT = "#1a1a1a"
MUTED = "#555555"
LIGHT = "#eeeeee"
MID = "#d6d6d6"
DARK = "#8a8a8a"
STROKE = "#333333"
GRID = "#bbbbbb"
WHITE = "#ffffff"


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def line(x1: float, y1: float, x2: float, y2: float, color: str = STROKE, width: float = 1.5, **attrs) -> str:
    extra = " ".join(f'{k.replace("_", "-")}="{esc(v)}"' for k, v in attrs.items())
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" {extra}/>'
    )


def path(d: str, fill: str = "none", stroke: str = STROKE, width: float = 1.5, **attrs) -> str:
    extra = " ".join(f'{k.replace("_", "-")}="{esc(v)}"' for k, v in attrs.items())
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>'


def rect(x: float, y: float, w: float, h: float, fill: str = WHITE, stroke: str = STROKE, width: float = 1.2, rx: float = 0) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
    )


def circle(cx: float, cy: float, r: float, fill: str = WHITE, stroke: str = STROKE, width: float = 1.2) -> str:
    return (
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{width}"/>'
    )


def text(
    x: float,
    y: float,
    content: str,
    size: float = 16,
    fill: str = TEXT,
    anchor: str = "middle",
    weight: str = "400",
    style: str = "normal",
    family: str = LATIN_FONT,
    baseline: str = "middle",
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" '
        f'font-size="{size}" font-weight="{weight}" font-style="{style}" '
        f'text-anchor="{anchor}" dominant-baseline="{baseline}" fill="{fill}">'
        f"{esc(content)}</text>"
    )


def multiline(
    x: float,
    y: float,
    lines: list[str],
    size: float = 14,
    leading: float = 17,
    fill: str = TEXT,
    anchor: str = "middle",
    weight: str = "400",
    family: str = LATIN_FONT,
) -> str:
    start = y - leading * (len(lines) - 1) / 2
    return "\n".join(
        text(x, start + i * leading, value, size=size, fill=fill, anchor=anchor, weight=weight, family=family)
        for i, value in enumerate(lines)
    )


def arrow(x1: float, y1: float, x2: float, y2: float, color: str = MUTED, width: float = 1.5, dashed: bool = False) -> str:
    dash = ' stroke-dasharray="5,4"' if dashed else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" marker-end="url(#arrow)"{dash}/>'
    )


def draw_mouth() -> list[str]:
    parts: list[str] = []

    parts.append(text(292, 34, "मुख — mouth schematic", size=20, weight="700"))
    parts.append(text(292, 58, "five selected contact stations", size=14, fill=MUTED))

    # Side-view outline: nose, lips, chin, throat.
    parts.append(path(
        "M 202 88 C 260 56, 360 62, 426 111 "
        "C 462 137, 462 169, 428 184 "
        "C 472 194, 468 229, 423 236 "
        "C 387 305, 320 346, 238 326 "
        "C 171 310, 136 257, 145 194 "
        "C 153 135, 171 105, 202 88 Z",
        fill="#f7f7f7",
        stroke=STROKE,
        width=2.0,
    ))

    # Nasal canal and oral cavity as inner tracks.
    parts.append(path("M 207 146 C 263 111, 354 112, 417 147", stroke=MUTED, width=2.2))
    parts.append(path("M 195 200 C 252 156, 352 155, 426 196", stroke=MUTED, width=2.2))
    parts.append(path("M 182 253 C 234 216, 316 211, 389 237", stroke="#777777", width=3.2))
    parts.append(path("M 181 254 C 236 287, 320 287, 393 245", stroke="#777777", width=3.2))

    # Lungs / breath.
    parts.append(path("M 203 402 C 156 372, 158 306, 214 286 C 263 308, 264 375, 203 402 Z", fill="#eeeeee", stroke=STROKE, width=1.4))
    parts.append(path("M 288 402 C 335 372, 333 306, 277 286 C 228 308, 227 375, 288 402 Z", fill="#eeeeee", stroke=STROKE, width=1.4))
    parts.append(line(246, 290, 246, 255, color=MUTED, width=2.0))
    parts.append(arrow(246, 377, 246, 265, color=MUTED, width=2.0))
    parts.append(text(98, 355, "प्राण", size=16, family=DEV_FONT, weight="700", anchor="start"))
    parts.append(text(98, 376, "breath from lungs", size=13, fill=MUTED, anchor="start"))

    # Vocal cords.
    parts.append(line(216, 271, 238, 263, color=STROKE, width=2.5))
    parts.append(line(238, 263, 260, 271, color=STROKE, width=2.5))
    for i in range(3):
        x = 224 + i * 13
        parts.append(path(f"M {x} 283 q 5 -10 10 0", stroke=MUTED, width=1.1))
    parts.append(text(78, 253, "घोष", size=16, family=DEV_FONT, weight="700", anchor="start"))
    parts.append(text(78, 274, "voice vibration", size=13, fill=MUTED, anchor="start"))

    # Nasal gate.
    parts.append(line(371, 147, 391, 126, color=STROKE, width=2.3))
    parts.append(circle(378, 139, 4.5, fill=TEXT, stroke=TEXT))
    parts.append(text(446, 91, "नासिका", size=16, family=DEV_FONT, weight="700", anchor="start"))
    parts.append(text(446, 112, "nasal passage", size=13, fill=MUTED, anchor="start"))
    parts.append(arrow(439, 112, 383, 138, color=MUTED, width=1.2))

    # Five contact stations.
    stations = [
        ("कण्ठ्य", "throat / back", 197, 238),
        ("तालव्य", "palate", 246, 203),
        ("मूर्धन्य", "curled tongue", 300, 186),
        ("दन्त्य", "teeth", 361, 190),
        ("ओष्ठ्य", "lips", 430, 210),
    ]
    for idx, (dev, english, x, y) in enumerate(stations, 1):
        parts.append(circle(x, y, 6, fill=TEXT, stroke=TEXT))
        label_x = 36
        label_y = 82 + idx * 44
        parts.append(circle(label_x, label_y, 9, fill=TEXT, stroke=TEXT))
        parts.append(text(label_x, label_y, f"{idx}", size=11, fill=WHITE, anchor="middle", weight="700"))
        parts.append(text(label_x + 17, label_y - 8, dev, size=15, anchor="start", family=DEV_FONT, weight="700"))
        parts.append(text(label_x + 17, label_y + 12, english, size=12.5, anchor="start", fill=MUTED))
        parts.append(arrow(label_x + 130, label_y, x - 8, y, color="#777777", width=0.9, dashed=True))

    return parts


def switch_box(x: float, y: float, title_dev: str, title_english: str, values: list[str], height: float = 82) -> list[str]:
    parts = [rect(x, y, 190, height, fill="#f7f7f7", stroke="#777777", width=1.0, rx=4)]
    parts.append(text(x + 14, y + 20, title_dev, size=17, anchor="start", family=DEV_FONT, weight="700"))
    parts.append(text(x + 14, y + 42, title_english, size=12.5, anchor="start", fill=MUTED))
    if len(values) == 2:
        parts.append(rect(x + 18, y + 56, 68, 17, fill=LIGHT, stroke="#999999", width=0.7, rx=8))
        parts.append(rect(x + 105, y + 56, 68, 17, fill=MID, stroke="#999999", width=0.7, rx=8))
        parts.append(text(x + 52, y + 65, values[0], size=10.5, fill=TEXT))
        parts.append(text(x + 139, y + 65, values[1], size=10.5, fill=TEXT))
    else:
        parts.append(text(x + 95, y + 65, values[0], size=11.5, fill=TEXT))
    return parts


def draw_controls() -> list[str]:
    parts: list[str] = []
    x = 620
    parts.append(text(x + 205, 34, "physical controls", size=20, weight="700"))
    parts.append(text(x + 205, 58, "how one station becomes five sounds", size=14, fill=MUTED))
    parts.extend(switch_box(x, 86, "स्थान", "mouth station", ["5 positions"], height=82))
    parts.extend(switch_box(x + 220, 86, "प्राण", "breath effort", ["low", "high"], height=82))
    parts.extend(switch_box(x, 198, "घोष", "voice vibration", ["off", "on"], height=82))
    parts.extend(switch_box(x + 220, 198, "नासिका", "nasal release", ["closed", "open"], height=82))

    parts.append(rect(x + 12, 318, 396, 54, fill="#f7f7f7", stroke="#dddddd", width=0.8, rx=4))
    parts.append(text(x + 210, 337, "2 × 2 oral settings + nasal release", size=15, weight="700"))
    parts.append(text(x + 210, 358, "at each mouth station", size=13, fill=MUTED))
    return parts


def draw_grid() -> list[str]:
    parts: list[str] = []
    grid_x = 72
    grid_y = 430
    cell_w = 150
    cell_h = 52
    header_h = 78
    row_label_w = 142

    rows = [
        ("कण्ठ्य", "throat / back", ["क", "ख", "ग", "घ", "ङ"]),
        ("तालव्य", "palate", ["च", "छ", "ज", "झ", "ञ"]),
        ("मूर्धन्य", "curled tongue", ["ट", "ठ", "ड", "ढ", "ण"]),
        ("दन्त्य", "teeth", ["त", "थ", "द", "ध", "न"]),
        ("ओष्ठ्य", "lips", ["प", "फ", "ब", "भ", "म"]),
    ]
    cols = [
        ["अघोष", "अल्पप्राण", "unvoiced", "low breath"],
        ["अघोष", "महाप्राण", "unvoiced", "high breath"],
        ["घोष", "अल्पप्राण", "voiced", "low breath"],
        ["घोष", "महाप्राण", "voiced", "high breath"],
        ["अनुनासिक", "नासिका", "nasal", "release"],
    ]

    title_x = grid_x + row_label_w + cell_w * 2.5
    parts.append(text(title_x, grid_y - 37, "स्पर्श — contact sonomers", size=20, weight="700"))
    parts.append(text(title_x, grid_y - 14, "five mouth stations crossed with breath, voice, and nasal release", size=14, fill=MUTED))

    # Column headers.
    for c, col in enumerate(cols):
        x = grid_x + row_label_w + c * cell_w
        fill = "#efefef" if c < 4 else "#d8d8d8"
        parts.append(rect(x, grid_y, cell_w, header_h, fill=fill, stroke=GRID, width=0.9))
        parts.append(text(x + cell_w / 2, grid_y + 18, col[0], size=13, family=DEV_FONT, weight="700"))
        parts.append(text(x + cell_w / 2, grid_y + 36, col[1], size=13, family=DEV_FONT, weight="700"))
        parts.append(text(x + cell_w / 2, grid_y + 56, f"{col[2]} / {col[3]}", size=11, fill=MUTED))

    # Row labels and cells.
    for r, (dev, english, values) in enumerate(rows):
        y = grid_y + header_h + r * cell_h
        parts.append(rect(grid_x, y, row_label_w, cell_h, fill="#f5f5f5", stroke=GRID, width=0.9))
        parts.append(text(grid_x + 12, y + 19, dev, size=15, anchor="start", family=DEV_FONT, weight="700"))
        parts.append(text(grid_x + 12, y + 37, english, size=11.5, anchor="start", fill=MUTED))
        for c, dev_cell in enumerate(values):
            x = grid_x + row_label_w + c * cell_w
            fill = WHITE if c < 4 else "#eeeeee"
            parts.append(rect(x, y, cell_w, cell_h, fill=fill, stroke=GRID, width=0.9))
            parts.append(text(x + cell_w / 2, y + cell_h / 2, dev_cell, size=26, family=DEV_FONT, weight="700"))

    # Attribute braces.
    oral_x1 = grid_x + row_label_w
    oral_x2 = grid_x + row_label_w + 4 * cell_w
    nasal_x1 = oral_x2
    y_brace = grid_y + header_h + cell_h * 5 + 18
    parts.append(line(oral_x1, y_brace, oral_x2, y_brace, color=TEXT, width=1.2))
    parts.append(line(oral_x1, y_brace - 5, oral_x1, y_brace + 5, color=TEXT, width=1.2))
    parts.append(line(oral_x2, y_brace - 5, oral_x2, y_brace + 5, color=TEXT, width=1.2))
    parts.append(text((oral_x1 + oral_x2) / 2, y_brace + 18, "voice × breath", size=12, fill=MUTED))
    parts.append(line(nasal_x1, y_brace, nasal_x1 + cell_w, y_brace, color=TEXT, width=1.2))
    parts.append(line(nasal_x1, y_brace - 5, nasal_x1, y_brace + 5, color=TEXT, width=1.2))
    parts.append(line(nasal_x1 + cell_w, y_brace - 5, nasal_x1 + cell_w, y_brace + 5, color=TEXT, width=1.2))
    parts.append(text(nasal_x1 + cell_w / 2, y_brace + 18, "nasal", size=12, fill=MUTED))

    return parts


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    width = 1040
    height = 870
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}pt" height="{height}pt" viewBox="0 0 {width} {height}">',
        "<defs>",
        '<marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="strokeWidth">',
        f'<path d="M 0 0 L 8 4 L 0 8 z" fill="{MUTED}"/>',
        "</marker>",
        "</defs>",
        f'<rect width="{width}" height="{height}" fill="{WHITE}"/>',
    ]

    parts.extend(draw_mouth())
    parts.extend(draw_controls())
    parts.extend(draw_grid())

    # Bottom formula / caption-strip inside the figure.
    parts.append(rect(54, 832, 932, 28, fill="#f7f7f7", stroke="#dddddd", width=0.8, rx=3))
    parts.append(text(520, 847, "5 mouth stations × (2 breath states × 2 voice states + nasal release) = 25 contact sonomers", size=15, weight="700"))
    parts.append("</svg>")

    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()

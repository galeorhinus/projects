#!/usr/bin/env python3
"""Generate Chapter 9's consonant-plane and teaching-axis sound volume."""

from __future__ import annotations

import html
import math
from pathlib import Path


OUT = Path(__file__).with_name("sound_volume.from-py.svg")
DEV = (
    "Noto Serif Devanagari, Adobe Devanagari, Kohinoor Devanagari, "
    "Devanagari MT, serif"
)
SERIF = "STIX Two Text, Gentium Book Plus, Georgia, serif"

INK = "#29282a"
MUTED = "#666368"
PAPER = "#f7f7f4"
WHITE = "#ffffff"
LINE = "#c9c3b8"
GOLD = "#a77a31"
GOLD_LIGHT = "#efe2ca"
GHOST = "#deddd8"


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def text(
    x: float,
    y: float,
    value: str,
    size: float,
    *,
    family: str = SERIF,
    anchor: str = "middle",
    weight: int = 400,
    fill: str = INK,
) -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" dominant-baseline="middle" '
        f'fill="{fill}">{esc(value)}</text>'
    )


def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: str = WHITE,
    stroke: str = LINE,
    rx: float = 4,
) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>'
    )


def mini_hex(
    cx: float,
    cy: float,
    *,
    fill: str,
    stroke: str,
    dash: str | None = None,
    height: float = 40,
) -> str:
    h = height
    w = h * 2 / math.sqrt(3)
    points = [
        (cx - w / 2, cy),
        (cx - w / 4, cy - h / 2),
        (cx + w / 4, cy - h / 2),
        (cx + w / 2, cy),
        (cx + w / 4, cy + h / 2),
        (cx - w / 4, cy + h / 2),
    ]
    values = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polygon points="{values}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="1.2"{extra}/>'
    )


def draw_plane(x: float, y: float) -> list[str]:
    parts: list[str] = []
    for offset_x, offset_y, opacity in [(24, -22, 0.35), (12, -11, 0.58)]:
        parts.append(
            f'<rect x="{x + offset_x}" y="{y + offset_y}" width="360" height="400" '
            f'rx="5" fill="{GHOST}" stroke="{LINE}" stroke-width="1" opacity="{opacity}"/>'
        )
    parts.append(rect(x, y, 360, 400, fill=WHITE, stroke=INK, rx=5))
    for row in range(7):
        for col in range(5):
            cx = x + 50 + col * 65
            cy = y + 47 + row * 50
            missing = (row == 5 and col == 0) or (row == 6 and col == 4)
            if missing:
                parts.append(mini_hex(cx, cy, fill=WHITE, stroke=GOLD, dash="4 3"))
                parts.append(text(cx, cy + 1, "1" if col == 0 else "2", 30, weight=700, fill=GOLD))
            else:
                parts.append(mini_hex(cx, cy, fill=GHOST, stroke=MUTED))
    return parts


def main() -> None:
    width, height = 1040, 930
    forms = ["क", "का", "कि", "की", "कु", "कू", "कृ", "कॄ", "कॢ", "कॣ", "के", "कै", "को", "कौ"]
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="{PAPER}"/>',
    ]

    parts.append(text(220, 47, "THE CONSONANT PLANE", 30, weight=700, fill=MUTED))
    parts.extend(draw_plane(40, 92))
    parts.append(text(220, 540, "5 places × 7 rows", 32, weight=600))
    parts.append(text(220, 580, "35 possible addresses", 30, fill=MUTED))

    parts.append(text(430, 292, "×", 44, weight=600, fill=GOLD))

    parts.append(rect(460, 92, 540, 400, fill=WHITE, stroke=LINE, rx=6))
    parts.append(text(730, 130, "THE FOURTEEN-POSITION", 30, weight=700, fill=MUTED))
    parts.append(text(730, 165, "TEACHING AXIS", 30, weight=700, fill=MUTED))
    for index, form in enumerate(forms):
        row, col = divmod(index, 7)
        cx = 500 + col * 76
        cy = 245 + row * 125
        parts.append(mini_hex(cx, cy, fill=GOLD_LIGHT, stroke=GOLD, height=56))
        parts.append(text(cx, cy - 1, form, 34, family=DEV, weight=600))
    parts.append(text(730, 455, "one consonant address extends", 30, fill=MUTED))
    parts.append(text(730, 485, "through all fourteen positions", 30, fill=MUTED))

    parts.append(rect(40, 630, 960, 235, fill=WHITE, stroke=LINE, rx=6))
    parts.append(text(520, 670, "THE MULTIPLICATION", 30, weight=700, fill=MUTED))
    parts.append(text(200, 730, "35 × 14", 40, weight=600))
    parts.append(text(200, 777, "490 possible", 30, fill=MUTED))
    parts.append(text(200, 812, "positions", 30, fill=MUTED))
    parts.append(text(520, 730, "−  2 × 14", 40, weight=600, fill=GOLD))
    parts.append(text(520, 777, "28 positions", 30, fill=MUTED))
    parts.append(text(520, 812, "remain empty", 30, fill=MUTED))
    parts.append(text(840, 730, "33 × 14 = 462", 40, weight=700))
    parts.append(text(840, 770, "addressed teaching", 30, fill=MUTED))
    parts.append(text(840, 805, "combinations", 30, fill=MUTED))

    parts.append(text(520, 910, "A classroom row unrolls one fiber of the volume.", 30, fill=MUTED))
    parts.append("</svg>")
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

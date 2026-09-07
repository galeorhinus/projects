#!/usr/bin/env python3
"""Generate Chapter 9's consonant-plane and teaching-axis sound volume."""

from __future__ import annotations

import html
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
) -> str:
    w, h = 48, 30
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
            f'<rect x="{x + offset_x}" y="{y + offset_y}" width="310" height="266" '
            f'rx="5" fill="{GHOST}" stroke="{LINE}" stroke-width="1" opacity="{opacity}"/>'
        )
    parts.append(rect(x, y, 310, 266, fill=WHITE, stroke=INK, rx=5))
    for row in range(7):
        for col in range(5):
            cx = x + 35 + col * 60
            cy = y + 26 + row * 36
            missing = (row == 5 and col == 0) or (row == 6 and col == 4)
            if missing:
                parts.append(mini_hex(cx, cy, fill=WHITE, stroke=GOLD, dash="4 3"))
                parts.append(text(cx, cy + 1, "1" if col == 0 else "2", 11, weight=700, fill=GOLD))
            else:
                parts.append(mini_hex(cx, cy, fill=GHOST, stroke=MUTED))
    return parts


def main() -> None:
    width, height = 1040, 640
    forms = ["क", "का", "कि", "की", "कु", "कू", "कृ", "कॄ", "कॢ", "कॣ", "के", "कै", "को", "कौ"]
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="{PAPER}"/>',
    ]

    parts.append(text(215, 44, "THE CONSONANT PLANE", 15, weight=700, fill=MUTED))
    parts.extend(draw_plane(58, 82))
    parts.append(text(213, 381, "5 places × 7 rows", 19, weight=600))
    parts.append(text(213, 411, "35 possible addresses", 16, fill=MUTED))

    parts.append(text(423, 217, "×", 40, weight=600, fill=GOLD))

    parts.append(rect(490, 82, 492, 266, fill=WHITE, stroke=LINE, rx=6))
    parts.append(text(736, 116, "THE FOURTEEN-POSITION TEACHING AXIS", 15, weight=700, fill=MUTED))
    for index, form in enumerate(forms):
        row, col = divmod(index, 7)
        cx = 532 + col * 68
        cy = 174 + row * 93
        parts.append(mini_hex(cx, cy, fill=GOLD_LIGHT, stroke=GOLD))
        parts.append(text(cx, cy - 1, form, 20, family=DEV, weight=600))
    parts.append(text(736, 330, "one consonant address extends through all fourteen positions", 16, fill=MUTED))

    parts.append(rect(58, 462, 924, 126, fill=WHITE, stroke=LINE, rx=6))
    parts.append(text(520, 490, "THE MULTIPLICATION", 15, weight=700, fill=MUTED))
    parts.append(text(225, 535, "35 × 14", 30, weight=600))
    parts.append(text(225, 567, "490 possible positions", 15, fill=MUTED))
    parts.append(text(520, 535, "−  2 × 14", 30, weight=600, fill=GOLD))
    parts.append(text(520, 567, "28 positions remain empty", 15, fill=MUTED))
    parts.append(text(815, 535, "33 × 14 = 462", 30, weight=700))
    parts.append(text(815, 567, "addressed teaching combinations", 15, fill=MUTED))

    parts.append(text(520, 618, "A classroom row unrolls one fiber of the volume.", 17, fill=MUTED))
    parts.append("</svg>")
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate Chapter 9's back-to-front mouth-place arc."""

from __future__ import annotations

import html
from pathlib import Path


OUT = Path(__file__).with_name("superset_place_arc_columns.from-py.svg")
DEV = (
    "Noto Serif Devanagari, Adobe Devanagari, Kohinoor Devanagari, "
    "Devanagari MT, serif"
)
SERIF = "STIX Two Text, Gentium Book Plus, Georgia, serif"

INK = "#29282a"
MUTED = "#666368"
PAPER = "#f7f7f4"
WHITE = "#ffffff"
LINE = "#c8c0b1"
GOLD = "#a77a31"
ARC_LINE = "#b6a27a"
ARC = ["#ded9ce", "#d2cec4", "#e0ddd5", "#d2cec4", "#ded9ce"]


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


def rect(x: float, y: float, w: float, h: float) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" '
        f'fill="{WHITE}" stroke="{LINE}" stroke-width="1.2"/>'
    )


def main() -> None:
    width, height = 1040, 500
    places = [
        ("कण्ठ्य", "kaṇṭhya", "back of tongue", "soft-palate region", 120, 265),
        ("तालव्य", "tālavya", "tongue body", "toward hard palate", 320, 170),
        ("मूर्धन्य", "mūrdhanya", "tongue-tip curled", "toward palate ridge", 520, 130),
        ("दन्त्य", "dantya", "tongue-tip", "against the teeth", 720, 170),
        ("ओष्ठ्य", "oṣṭhya", "contact", "at the lips", 920, 265),
    ]

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="{PAPER}"/>',
        '<path d="M55 297 C210 64 830 64 985 297" fill="none" '
        f'stroke="{ARC_LINE}" stroke-width="68" stroke-linecap="round"/>',
        '<path d="M55 297 C210 64 830 64 985 297" fill="none" '
        f'stroke="{PAPER}" stroke-width="39" stroke-linecap="round"/>',
        text(50, 19, "BACK OF MOUTH", 14, anchor="start", weight=700, fill=MUTED),
        text(990, 19, "LIPS", 14, anchor="end", weight=700, fill=MUTED),
        f'<line x1="50" y1="40" x2="990" y2="40" stroke="{GOLD}" stroke-width="1.5"/>',
        '<path d="M980 34 L990 40 L980 46" fill="none" '
        f'stroke="{GOLD}" stroke-width="1.5"/>',
    ]

    for index, (dev, iast, line1, line2, x, y) in enumerate(places):
        parts.append(
            f'<circle cx="{x}" cy="{y}" r="11" fill="{GOLD}" stroke="{PAPER}" stroke-width="3"/>'
        )
        parts.append(text(x, y - 55, dev, 27, family=DEV, weight=600))
        parts.append(text(x, y - 28, iast, 16, weight=600, fill=MUTED))
        card_y = 340
        parts.append(
            f'<line x1="{x}" y1="{y + 13}" x2="{x}" y2="{card_y}" '
            f'stroke="{GOLD}" stroke-width="1.4"/>'
        )
        parts.append(rect(x - 88, card_y, 176, 104))
        parts.append(text(x, card_y + 37, line1, 16, fill=INK))
        parts.append(text(x, card_y + 67, line2, 16, fill=INK))
        if index < len(ARC):
            parts.append(
                f'<circle cx="{x}" cy="{card_y + 91}" r="3" fill="{ARC[index]}"/>'
            )

    parts.append(text(520, 477, "The address sequence follows the vocal tract from back to front.", 17, fill=MUTED))
    parts.append("</svg>")
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

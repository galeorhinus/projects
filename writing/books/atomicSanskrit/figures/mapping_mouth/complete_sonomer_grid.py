#!/usr/bin/env python3
"""Generate Chapter 9's complete 33-of-35 consonant address grid.

The sonomer tiles use the exact one-matra geometry established in Chapter 10.
All type sizes are specified as print sizes for a 4.5-inch-wide figure.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "working" / "50_projects" / "dhatu_hexagons"))
sys.path.insert(0, str(REPO_ROOT / "figures" / "_shared"))

import matra_style as ms  # noqa: E402
from dhatu_hexagon import EDGE_LENGTH as EDGE_BASE, HEX_HEIGHT as HEX_BASE  # noqa: E402


OUT = Path(__file__).with_name("complete_sonomer_grid.from-py.svg")

CANVAS_W = 384
CANVAS_H = 488
TILE_SCALE = 0.5
EDGE = EDGE_BASE * TILE_SCALE
HEX_HEIGHT = HEX_BASE * TILE_SCALE
SLANT = EDGE / 2
MATRA_UNIT = 72 * TILE_SCALE
HEX_FLAT = ms.matra_width(1, matra_unit=MATRA_UNIT, slant=SLANT)


def fs(points: float) -> float:
    """Convert the intended print size to SVG units at 4.5 inches wide."""
    return ms.pt_to_px(points, CANVAS_W)


def sonomer(cx: float, cy: float, devanagari: str, iast: str) -> str:
    tile = (
        f'<polygon points="{ms.hex_points(cx, cy, HEX_FLAT, slant=SLANT, hex_height=HEX_HEIGHT)}" '
        f'fill="{ms.LIGHT_FILL}" stroke="{ms.STROKE}" stroke-width="{ms.STROKE_W}" '
        f'stroke-linejoin="round"/>'
    )
    label = ms.varna_label(
        cx,
        cy,
        devanagari,
        iast,
        ink=ms.INK_DARK,
        fs_dev=fs(11.5),
        fs_iast=fs(8.5),
    )
    return f"{tile}\n{label}"


def vacancy(cx: float, cy: float, number: int) -> str:
    return "\n".join([
        f'<polygon points="{ms.hex_points(cx, cy, HEX_FLAT, slant=SLANT, hex_height=HEX_HEIGHT)}" '
        f'fill="{ms.BG}" stroke="{ms.GOLD}" stroke-width="1.2" stroke-dasharray="4,3" '
        f'stroke-linejoin="round"/>',
        ms.text(cx, cy, str(number), fs(11.5), weight="600", fill=ms.GOLD),
    ])


def main() -> None:
    columns = [
        ("कण्ठ्य", "kaṇṭhya"),
        ("तालव्य", "tālavya"),
        ("मूर्धन्य", "mūrdhanya"),
        ("दन्त्य", "dantya"),
        ("ओष्ठ्य", "oṣṭhya"),
    ]
    rows = [
        (("अघोष-अल्पप्राण", "aghoṣa-alpaprāṇa", "voiceless-unaspirated"), [("क", "ka"), ("च", "ca"), ("ट", "ṭa"), ("त", "ta"), ("प", "pa")]),
        (("अघोष-महाप्राण", "aghoṣa-mahāprāṇa", "voiceless-aspirated"), [("ख", "kha"), ("छ", "cha"), ("ठ", "ṭha"), ("थ", "tha"), ("फ", "pha")]),
        (("घोष-अल्पप्राण", "ghoṣa-alpaprāṇa", "voiced-unaspirated"), [("ग", "ga"), ("ज", "ja"), ("ड", "ḍa"), ("द", "da"), ("ब", "ba")]),
        (("घोष-महाप्राण", "ghoṣa-mahāprāṇa", "voiced-aspirated"), [("घ", "gha"), ("झ", "jha"), ("ढ", "ḍha"), ("ध", "dha"), ("भ", "bha")]),
        (("अनुनासिक", "anunāsika", "nasal"), [("ङ", "ṅa"), ("ञ", "ña"), ("ण", "ṇa"), ("न", "na"), ("म", "ma")]),
        (("अन्तःस्थ", "antaḥstha", "approximant"), [None, ("य", "ya"), ("र", "ra"), ("ल", "la"), ("व", "va")]),
        (("ऊष्मन्", "ūṣman", "fricative"), [("ह", "ha"), ("श", "śa"), ("ष", "ṣa"), ("स", "sa"), None]),
    ]

    column_x = [144, 195, 246, 297, 348]
    row_y = [113, 163, 213, 263, 313, 369, 419]
    parts = [
        ms.text(246, 14, "PLACE OF ARTICULATION", fs(9), weight="600", fill=ms.MUTED),
        ms.text(112, 43, "प्रयत्न", fs(10.5), anchor="end", weight="600", family=ms.DEV_FONT),
        ms.text(112, 60, "prayatna", fs(8.5), anchor="end", style="italic", fill=ms.MUTED),
        ms.text(112, 77, "manner", fs(8.5), anchor="end", fill=ms.MUTED),
        f'<line x1="121" y1="29" x2="371" y2="29" stroke="{ms.GOLD}" stroke-width="1"/>',
        f'<path d="M365 25 L371 29 L365 33" fill="none" stroke="{ms.GOLD}" stroke-width="1"/>',
    ]

    western_places = ["velar", "palatal", "retroflex", "dental", "labial"]
    for x, (devanagari, iast), western in zip(column_x, columns, western_places):
        parts.append(ms.text(x, 43, devanagari, fs(10.5), weight="600", family=ms.DEV_FONT))
        parts.append(ms.text(x, 60, iast, fs(8.5), style="italic", fill=ms.MUTED))
        parts.append(ms.text(x, 77, western, fs(8.5), fill=ms.MUTED))

    missing_number = 0
    for y, (labels, cells) in zip(row_y, rows):
        parts.append(ms.text(112, y - 16, labels[0], fs(9.5), anchor="end",
                             weight="600", family=ms.DEV_FONT))
        parts.append(ms.text(112, y, labels[1], fs(8.5), anchor="end",
                             style="italic", fill=ms.MUTED))
        parts.append(ms.text(112, y + 16, labels[2], fs(8.5), anchor="end",
                             fill=ms.MUTED))
        for x, cell in zip(column_x, cells):
            if cell is None:
                missing_number += 1
                parts.append(vacancy(x, y, missing_number))
            else:
                parts.append(sonomer(x, y, *cell))

    parts.extend([
        f'<line x1="12" y1="341" x2="372" y2="341" stroke="{ms.GUIDE}" '
        'stroke-width="0.8" stroke-dasharray="3,3"/>',
        f'<line x1="12" y1="453" x2="372" y2="453" stroke="{ms.GUIDE}" stroke-width="0.8"/>',
        ms.text(12, 474, "33 addressed sonances", fs(9), anchor="start", weight="600"),
        ms.text(372, 474, "2 positions remain empty", fs(9), anchor="end",
                weight="600", fill=ms.GOLD),
    ])

    OUT.write_text(
        ms.svg(CANVAS_W, CANVAS_H, "\n".join(parts), title="The complete sonomer grid"),
        encoding="utf-8",
    )
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

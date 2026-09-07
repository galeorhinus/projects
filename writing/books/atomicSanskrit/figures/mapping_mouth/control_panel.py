#!/usr/bin/env python3
"""Generate Chapter 9's one-place, five-output control diagram.

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


OUT = Path(__file__).with_name("control_panel.from-py.svg")

CANVAS_W = 384
CANVAS_H = 260
TILE_SCALE = 0.5
EDGE = EDGE_BASE * TILE_SCALE
HEX_HEIGHT = HEX_BASE * TILE_SCALE
SLANT = EDGE / 2
MATRA_UNIT = 72 * TILE_SCALE
HEX_FLAT = ms.matra_width(1, matra_unit=MATRA_UNIT, slant=SLANT)


def fs(points: float) -> float:
    """Convert the intended print size to SVG units at 4.5 inches wide."""
    return ms.pt_to_px(points, CANVAS_W)


def rule(x1: float, y1: float, x2: float, y2: float, *, color: str = ms.GUIDE,
         width: float = 0.9) -> str:
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}"/>'
    )


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


def main() -> None:
    columns = [(167, "LIGHT", "अल्पप्राण", "alpaprāṇa"),
               (246, "HEAVY", "महाप्राण", "mahāprāṇa")]
    rows = [(143, "अघोष", "aghoṣa · voice off"),
            (195, "घोष", "ghoṣa · voice on")]

    parts = [
        ms.text(12, 20, "ONE MOUTH-PLACE", fs(9), anchor="start", weight="600", fill=ms.MUTED),
        ms.text(116, 20, "कण्ठ्य", fs(12), anchor="start", weight="600", family=ms.DEV_FONT),
        ms.text(157, 20, "kaṇṭhya", fs(9.5), anchor="start", style="italic"),
        ms.text(372, 20, "back of tongue against the soft palate", fs(8.5),
                anchor="end", fill=ms.MUTED),
        rule(12, 39, 372, 39, color=ms.STROKE, width=1.0),
        ms.text(207, 55, "BREATH RELEASE", fs(9), weight="600", fill=ms.MUTED),
    ]

    for x, english, devanagari, iast in columns:
        parts.append(ms.text(x, 72, english, fs(9), weight="600", fill=ms.MUTED))
        parts.append(ms.text(x, 89, devanagari, fs(10), weight="600", family=ms.DEV_FONT))
        parts.append(ms.text(x, 105, iast, fs(8.5), style="italic", fill=ms.MUTED))

    for y, devanagari, explanation in rows:
        parts.append(ms.text(112, y - 5, devanagari, fs(10), anchor="end",
                             weight="600", family=ms.DEV_FONT))
        parts.append(ms.text(112, y + 11, explanation, fs(8.5), anchor="end",
                             style="italic", fill=ms.MUTED))

    for x, y, devanagari, iast in [
        (167, 143, "क", "ka"),
        (246, 143, "ख", "kha"),
        (167, 195, "ग", "ga"),
        (246, 195, "घ", "gha"),
    ]:
        parts.append(sonomer(x, y, devanagari, iast))

    parts.extend([
        ms.text(291, 169, "+", fs(15), fill=ms.GOLD),
        ms.text(326, 92, "अनुनासिक", fs(10), weight="600", family=ms.DEV_FONT),
        ms.text(326, 108, "anunāsika", fs(8.5), style="italic", fill=ms.MUTED),
        sonomer(326, 169, "ङ", "ṅa"),
        ms.text(326, 201, "nasal passage open", fs(8.5), fill=ms.MUTED),
        rule(12, 226, 372, 226, color=ms.GUIDE, width=0.8),
        ms.text(192, 244, "2 voice states × 2 breath states + nasal release = 5 sonomers",
                fs(9.5), weight="600"),
    ])

    OUT.write_text(
        ms.svg(CANVAS_W, CANVAS_H, "\n".join(parts),
               title="One mouth-place, five contact sonomers"),
        encoding="utf-8",
    )
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

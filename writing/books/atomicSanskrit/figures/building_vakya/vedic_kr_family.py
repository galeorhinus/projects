#!/usr/bin/env python3
"""Generate the compact Chapter 12 Vedic ⟪कृ⟫ family figure."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIGURES = HERE.parent
sys.path.insert(0, str(FIGURES / "_shared"))

import matra_style as ms  # noqa: E402


W = 900.0
H = 570.0
WIDTH_IN = 4.5


def pt(points: float) -> float:
    return ms.pt_to_px(points, W, WIDTH_IN)


def rect(x: float, y: float, w: float, h: float, fill: str, *,
         stroke: str = ms.STROKE, radius: float = 5, stroke_w: float = 1.3) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="{radius:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>'
    )


def text(x: float, y: float, content: str, points: float, *,
         fill: str = ms.TEXT, anchor: str = "middle", weight: str = "400",
         style: str = "normal", family: str = ms.LATIN_FONT) -> str:
    return ms.text(
        x, y, content, pt(points), fill=fill, anchor=anchor,
        weight=weight, style=style, family=family,
    )


def main() -> None:
    body = [
        rect(330, 24, 240, 82, ms.LIGHT_FILL, radius=5),
        text(450, 55, "⟪कृ⟫", 14, family=ms.DEV_FONT, weight="600"),
        text(450, 84, "kṛ · to do, make, act", 9.5, fill=ms.MUTED, style="italic"),
    ]

    rows = [
        ("कृतम्", "kṛtam", "something done or completed", "RV 3.29.1b"),
        ("कर्मणः", "karmaṇaḥ", "of the deed or action", "RV 1.11.4c"),
        ("कर्तृभिः", "kartṛbhiḥ", "by the doers or makers", "RV 1.55.8c"),
        ("संस्कृतम्", "saṃskṛtam", "prepared or brought to completion", "RV 5.76.2a"),
    ]

    start_y = 138.0
    row_h = 94.0
    for i, (deva, iast, meaning, passage) in enumerate(rows):
        y = start_y + i * row_h
        fill = "#fbf9f4" if i % 2 == 0 else "#f4efe4"
        body.append(rect(30, y, 840, 78, fill, stroke=ms.GUIDE, radius=4, stroke_w=1.0))
        body.append(rect(48, y + 9, 230, 60, ms.DARK_FILL, radius=4))
        body.append(text(163, y + 28, deva, 11.5, fill=ms.INK_LIGHT,
                         family=ms.DEV_FONT, weight="600"))
        body.append(text(163, y + 53, iast, 9.3, fill=ms.INK_LIGHT, style="italic"))
        body.append(text(310, y + 29, meaning, 10.2, anchor="start", weight="600"))
        body.append(text(310, y + 56, passage, 9, fill=ms.MUTED, anchor="start"))

    svg = ms.svg(W, H, "\n".join(body), title="Four Vedic forms generated from the atom kṛ", width_in=WIDTH_IN)
    path = HERE / "vedic_kr_family.from-py.svg"
    path.write_text(svg, encoding="utf-8")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()

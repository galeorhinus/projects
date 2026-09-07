#!/usr/bin/env python3
"""Generate Chapter 9's five-place by five-setting contact matrix.

Axis labels always lead with Sanskrit, followed by IAST and the corresponding
modern phonetic term. All type sizes are print sizes for a 4.5-inch figure.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "figures" / "_shared"))

import matra_style as ms  # noqa: E402


OUT = Path(__file__).with_name("superset_varga_matrix_feature_rails.from-py.svg")

CANVAS_W = 384
CANVAS_H = 402
CELL_W = 42
CELL_H = 40

PLACE_X = [159, 207, 255, 303, 351]
ROW_Y = [151, 205, 259, 313, 367]

PLACES = [
    ("कण्ठ्य", "kaṇṭhya", "velar"),
    ("तालव्य", "tālavya", "palatal"),
    ("मूर्धन्य", "mūrdhanya", "retroflex"),
    ("दन्त्य", "dantya", "dental"),
    ("ओष्ठ्य", "oṣṭhya", "labial"),
]

SETTINGS = [
    ("अघोष-अल्पप्राण", "aghoṣa-alpaprāṇa", "voiceless-unaspirated"),
    ("अघोष-महाप्राण", "aghoṣa-mahāprāṇa", "voiceless-aspirated"),
    ("घोष-अल्पप्राण", "ghoṣa-alpaprāṇa", "voiced-unaspirated"),
    ("घोष-महाप्राण", "ghoṣa-mahāprāṇa", "voiced-aspirated"),
    ("अनुनासिक", "anunāsika", "nasal"),
]

SONOMERS = [
    ["क", "च", "ट", "त", "प"],
    ["ख", "छ", "ठ", "थ", "फ"],
    ["ग", "ज", "ड", "द", "ब"],
    ["घ", "झ", "ढ", "ध", "भ"],
    ["ङ", "ञ", "ण", "न", "म"],
]

ROW_FILLS = ["#f6f2e8", "#ece4d3", "#ddd2ba", "#c7b99c", "#aa9a7a"]


def fs(points: float) -> float:
    return ms.pt_to_px(points, CANVAS_W)


def label_stack(x: float, center_y: float, devanagari: str, iast: str,
                western: str, *, anchor: str = "middle") -> str:
    return "\n".join([
        ms.text(x, center_y - 16, devanagari, fs(9.5), anchor=anchor,
                weight="600", family=ms.DEV_FONT),
        ms.text(x, center_y, iast, fs(8.5), anchor=anchor,
                style="italic", fill=ms.MUTED),
        ms.text(x, center_y + 16, western, fs(8.5), anchor=anchor,
                fill=ms.MUTED),
    ])


def main() -> None:
    parts = [
        ms.text(12, 18, "Five Places, Five Settings", fs(11), anchor="start",
                weight="600"),
        ms.text(12, 37, "Mouth-place across; voice, breath, and nasal release down.",
                fs(8.5), anchor="start", fill=ms.MUTED),
        f'<line x1="12" y1="52" x2="372" y2="52" stroke="{ms.STROKE}" stroke-width="1"/>',
        ms.text(255, 64, "स्थान · sthāna", fs(8.5), weight="600", fill=ms.GOLD,
                family=ms.DEV_FONT),
        ms.text(124, 88, "प्रयत्न", fs(9.5), anchor="end", weight="600",
                family=ms.DEV_FONT),
        ms.text(124, 104, "prayatna", fs(8.5), anchor="end", style="italic",
                fill=ms.MUTED),
        ms.text(124, 120, "manner", fs(8.5), anchor="end", fill=ms.MUTED),
    ]

    for x, labels in zip(PLACE_X, PLACES):
        parts.append(label_stack(x, 96, *labels))

    parts.append(f'<line x1="12" y1="129" x2="372" y2="129" stroke="{ms.GUIDE}" stroke-width="0.8"/>')

    for index, (y, labels, sonomers, fill) in enumerate(
        zip(ROW_Y, SETTINGS, SONOMERS, ROW_FILLS)
    ):
        if index % 2:
            parts.append(
                f'<rect x="12" y="{y - 27}" width="360" height="54" fill="#f5f2eb"/>'
            )
        parts.append(label_stack(124, y, *labels, anchor="end"))
        for x, sonomer in zip(PLACE_X, sonomers):
            parts.append(
                f'<rect x="{x - CELL_W / 2:.1f}" y="{y - CELL_H / 2:.1f}" '
                f'width="{CELL_W}" height="{CELL_H}" rx="2" fill="{fill}" '
                f'stroke="{ms.GUIDE}" stroke-width="0.7"/>'
            )
            parts.append(ms.text(x, y, sonomer, fs(14), weight="600", family=ms.DEV_FONT))

    parts.append(f'<line x1="12" y1="394" x2="372" y2="394" stroke="{ms.STROKE}" stroke-width="1"/>')

    OUT.write_text(
        ms.svg(CANVAS_W, CANVAS_H, "\n".join(parts),
               title="Five places and five contact settings"),
        encoding="utf-8",
    )
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

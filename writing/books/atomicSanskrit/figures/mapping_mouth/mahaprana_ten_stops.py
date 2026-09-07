#!/usr/bin/env python3
"""Generate the unnumbered Chapter 9 teaching aid for ten mahaprana stops."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "figures" / "_shared"))

import matra_style as ms  # noqa: E402


OUT = Path(__file__).with_name("mahaprana_ten_stops.from-py.svg")

CANVAS_W = 384
CANVAS_H = 174
LEFT = 12
RIGHT = 372
MID = 192
CELL_W = 36

SONOMERS = [
    ("ख", "kha"),
    ("छ", "cha"),
    ("ठ", "ṭha"),
    ("थ", "tha"),
    ("फ", "pha"),
    ("घ", "gha"),
    ("झ", "jha"),
    ("ढ", "ḍha"),
    ("ध", "dha"),
    ("भ", "bha"),
]


def fs(points: float) -> float:
    return ms.pt_to_px(points, CANVAS_W)


def group_label(cx: float, devanagari: str, iast: str, western: str) -> str:
    return "\n".join([
        ms.text(cx, 63, devanagari, fs(9.5), weight="600", family=ms.DEV_FONT),
        ms.text(cx, 77, iast, fs(8.5), style="italic", fill=ms.MUTED),
        ms.text(cx, 90, western, fs(8.5), fill=ms.MUTED),
    ])


def main() -> None:
    parts = [
        ms.text(LEFT, 17, "Ten Mahāprāṇa Stops", fs(11), anchor="start", weight="600"),
        ms.text(LEFT, 35, "Five voiceless stops followed by five voiced stops.",
                fs(8.5), anchor="start", fill=ms.MUTED),
        f'<line x1="{LEFT}" y1="48" x2="{RIGHT}" y2="48" '
        f'stroke="{ms.STROKE}" stroke-width="1"/>',
        f'<rect x="{LEFT}" y="53" width="{MID - LEFT}" height="43" '
        'fill="#eee7d8"/>',
        f'<rect x="{MID}" y="53" width="{RIGHT - MID}" height="43" '
        'fill="#ddd2ba"/>',
        group_label(102, "अघोष", "aghoṣa", "voiceless"),
        group_label(282, "घोष", "ghoṣa", "voiced"),
    ]

    for index, (devanagari, iast) in enumerate(SONOMERS):
        x = LEFT + index * CELL_W
        fill = "#e8dfca" if index < 5 else "#cdbf9e"
        parts.extend([
            f'<rect x="{x}" y="96" width="{CELL_W}" height="43" fill="{fill}" '
            f'stroke="{ms.GUIDE}" stroke-width="0.7"/>',
            f'<rect x="{x}" y="139" width="{CELL_W}" height="28" fill="#f4f4f3" '
            f'stroke="{ms.GUIDE}" stroke-width="0.7"/>',
            ms.text(x + CELL_W / 2, 118, devanagari, fs(14), weight="600",
                    family=ms.DEV_FONT),
            ms.text(x + CELL_W / 2, 153, iast, fs(8.5), style="italic", fill=ms.MUTED),
        ])

    parts.append(
        f'<line x1="{LEFT}" y1="167" x2="{RIGHT}" y2="167" '
        f'stroke="{ms.STROKE}" stroke-width="1"/>'
    )

    OUT.write_text(
        ms.svg(CANVAS_W, CANVAS_H, "\n".join(parts),
               title="Ten mahaprana stops", bg="#f4f4f3"),
        encoding="utf-8",
    )
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

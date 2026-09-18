#!/usr/bin/env python3
"""Show why both Vedic instrumental-plural endings are metrically useful.

The two transmitted Rgvedic padas each contain eleven aksaras and share the
same laghu-guru pattern. The counterfactual third row imposes the narrower
Laukika -aih ending on the second line and exposes the missing guru aksara.
"""

from __future__ import annotations

import html
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
sys.path.insert(0, str(REPO_ROOT / "figures" / "_shared"))

import matra_style as ms  # noqa: E402


OUT = HERE / "rudrai_rudrebhih_matra_alignment.from-py.svg"

WIDTH = 1200
HEIGHT = 1040
X0 = 78
MATRA_UNIT = 52
SLANT = 12
HEX_HEIGHT = 58
UPPER_RAIL = -HEX_HEIGHT / 4
LOWER_RAIL = HEX_HEIGHT / 4

PAPER = "#f7f4ed"
INK = ms.TEXT
MUTED = ms.MUTED
GOLD = ms.GOLD
LAGHU_FILL = ms.LAGHU_FILL
GURU_FILL = ms.GURU_FILL
LAGHU_TEXT = ms.LAGHU_TEXT
GURU_TEXT = ms.GURU_TEXT
RED = "#9c493f"
RED_PALE = "#f0dfdb"
DEV_FONT = "Tiro Devanagari Sanskrit, Noto Serif Devanagari, serif"
LATIN_FONT = "STIX Two Text, Georgia, serif"


ROWS = [
    {
        "ref": "Ṛgveda 3.32.2d",
        "accented": "स॒जोषा॑ रु॒द्रैस्तृ॒पदा वृ॑षस्व",
        "syllables": ["स", "जो", "षा", "रु", "द्रैस्", "तृ", "प", "दा", "वृ", "ष", "स्व"],
        "weights": [1, 2, 2, 2, 2, 1, 1, 2, 1, 2, "X"],
        "target": range(3, 5),
        "target_label": "रुद्रैः · 2 अक्षराणि",
        "line_y": 170,
        "mantra_y": 218,
        "tile_y": 285,
        "number_y": 337,
        "label_y": 376,
    },
    {
        "ref": "Ṛgveda 3.32.3d",
        "accented": "पिबा॑ रु॒द्रेभिः॒ सग॑णः सुशिप्र",
        "syllables": ["पि", "बा", "रु", "द्रे", "भिः", "स", "ग", "णः", "सु", "शि", "प्र"],
        "weights": [1, 2, 2, 2, 2, 1, 1, 2, 1, 2, "X"],
        "target": range(2, 5),
        "target_label": "रुद्रेभिः · 3 अक्षराणि",
        "line_y": 425,
        "mantra_y": 473,
        "tile_y": 540,
        "number_y": 592,
        "label_y": 631,
    },
]

COUNTERFACTUAL = {
    "ref": "लौकिक -ऐः imposed on 3.32.3d",
    "accented": "पिबा रुद्रैः सगणः सुशिप्र",
    "syllables": ["पि", "बा", "रु", "द्रैः", "स", "ग", "णः", "सु", "शि", "प्र"],
    "weights": [1, 2, 2, 2, 1, 1, 2, 1, 2, "X"],
    "target": range(2, 4),
    "target_label": "रुद्रैः · 2 अक्षराणि",
    "line_y": 742,
    "mantra_y": 790,
    "tile_y": 857,
    "number_y": 909,
    "label_y": 948,
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text(
    x: float,
    y: float,
    value: str,
    *,
    size: float,
    color: str = INK,
    weight: int = 400,
    anchor: str = "start",
    italic: bool = False,
    family: str = LATIN_FONT,
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{esc(family)}" '
        f'font-size="{size:.1f}" font-weight="{weight}" '
        f'font-style="{"italic" if italic else "normal"}" fill="{color}" '
        f'text-anchor="{anchor}" dominant-baseline="middle">{esc(value)}</text>'
    )


def hex_points(cx: float, cy: float, flat_width: float) -> str:
    return ms.hex_points(cx, cy, flat_width, slant=SLANT, hex_height=HEX_HEIGHT)


def metrical_width(weight: int | str) -> int:
    # The final position is anceps. Guru width preserves visual alignment;
    # the X label prevents the diagram from assigning it a fixed weight.
    return 2 if weight == "X" else weight


def layout(weights: list[int | str]) -> list[dict[str, float]]:
    units: list[dict[str, float]] = []
    for index, raw_weight in enumerate(weights):
        width = metrical_width(raw_weight) * MATRA_UNIT - SLANT
        cy = LOWER_RAIL if (len(weights) - 1 - index) % 2 == 0 else UPPER_RAIL
        if index == 0:
            cx = 0.0
        else:
            previous = units[-1]
            cx = previous["cx"] + (previous["width"] + width) / 2 + SLANT
        units.append({"cx": cx, "cy": cy, "width": width})
    first = units[0]
    offset = X0 - (first["cx"] - first["width"] / 2 - SLANT / 2)
    for unit in units:
        unit["cx"] += offset
    return units


def render_row(row: dict[str, object], *, counterfactual: bool = False) -> list[str]:
    syllables = row["syllables"]
    weights = row["weights"]
    target = set(row["target"])
    units = layout(weights)
    tile_y = float(row["tile_y"])
    accent = RED if counterfactual else GOLD
    status = "10 अक्षराणि · off meter" if counterfactual else "11 अक्षराणि · meter complete"
    status_color = RED if counterfactual else MUTED

    parts = []
    if counterfactual:
        parts.append(f'<rect x="24" y="700" width="1152" height="320" rx="8" fill="{RED_PALE}"/>')
    parts.extend(
        [
            text(42, float(row["line_y"]), str(row["ref"]), size=32, color=status_color, weight=600, family=DEV_FONT if counterfactual else LATIN_FONT),
            text(1158, float(row["line_y"]), status, size=32, color=status_color, weight=650, anchor="end", family=DEV_FONT),
            text(360, float(row["mantra_y"]), str(row["accented"]), size=35, weight=500, family=DEV_FONT),
        ]
    )

    for index, (syllable, raw_weight, unit) in enumerate(zip(syllables, weights, units)):
        cx = unit["cx"]
        cy = tile_y + unit["cy"]
        display_weight = metrical_width(raw_weight)
        fill = GURU_FILL if display_weight == 2 else LAGHU_FILL
        ink = GURU_TEXT if display_weight == 2 else LAGHU_TEXT
        stroke = accent if index in target else ms.STROKE
        stroke_width = 4 if index in target else 1.5
        parts.append(
            f'<polygon points="{hex_points(cx, cy, unit["width"])}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{stroke_width}" stroke-linejoin="round"/>'
        )
        parts.append(text(cx, cy + 1, str(syllable), size=32, color=ink, weight=600, anchor="middle", family=DEV_FONT))
        if raw_weight == "X":
            parts.append(text(cx, cy - 48, "x", size=32, color=MUTED, weight=600, anchor="middle", italic=True))
        parts.append(text(cx, float(row["number_y"]), str(index + 1), size=32, color=MUTED, anchor="middle"))

    target_units = [units[index] for index in sorted(target)]
    left = target_units[0]["cx"] - target_units[0]["width"] / 2 - SLANT / 2
    right = target_units[-1]["cx"] + target_units[-1]["width"] / 2 + SLANT / 2
    parts.extend(
        [
            f'<path d="M {left:.1f},{float(row["label_y"]) - 18:.1f} '
            f'L {left:.1f},{float(row["label_y"]) - 7:.1f} '
            f'L {right:.1f},{float(row["label_y"]) - 7:.1f} '
            f'L {right:.1f},{float(row["label_y"]) - 18:.1f}" '
            f'fill="none" stroke="{accent}" stroke-width="2.5"/>',
            text((left + right) / 2, float(row["label_y"]) + 13, str(row["target_label"]), size=32, color=accent, weight=600, anchor="middle", family=DEV_FONT),
        ]
    )
    return parts


def render() -> str:
    transmitted_break_x = X0 + 9 * MATRA_UNIT
    transmitted_end_x = X0 + 18 * MATRA_UNIT
    counterfactual_end_x = X0 + 16 * MATRA_UNIT
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="4.5in" height="3.9in" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" preserveAspectRatio="xMidYMid meet">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{PAPER}"/>',
        text(42, 47, "What the Laukika Constraint Would Break", size=40, weight=650),
        text(42, 91, "numbered hexagons = akṣaras · width and shade = laghu or guru", size=32, color=MUTED, italic=True),
        text(42, 127, "वैदिक selection · both transmitted lines complete Triṣṭubh", size=32, color=GOLD, weight=650, family=DEV_FONT),
        f'<line x1="{transmitted_break_x:.1f}" y1="246" x2="{transmitted_break_x:.1f}" y2="582" '
        f'stroke="{GOLD}" stroke-width="2.5" stroke-dasharray="8 7"/>',
        text(transmitted_break_x, 676, "word boundary after position 5", size=32, color=GOLD, weight=600, anchor="middle"),
    ]

    for row in ROWS:
        parts.extend(render_row(row))

    parts.extend(render_row(COUNTERFACTUAL, counterfactual=True))
    parts.extend(
        [
            f'<line x1="{counterfactual_end_x:.1f}" y1="818" x2="{counterfactual_end_x:.1f}" y2="911" '
            f'stroke="{RED}" stroke-width="3" stroke-dasharray="8 7"/>',
            f'<line x1="{transmitted_end_x:.1f}" y1="818" x2="{transmitted_end_x:.1f}" y2="911" '
            f'stroke="{GOLD}" stroke-width="3" stroke-dasharray="8 7"/>',
            f'<line x1="{counterfactual_end_x + 8:.1f}" y1="961" x2="{transmitted_end_x - 8:.1f}" y2="961" '
            f'stroke="{RED}" stroke-width="3" marker-end="url(#arrow)"/>',
            text((counterfactual_end_x + transmitted_end_x) / 2, 998, "missing 1 गुरु अक्षर · −2 मात्राः", size=32, color=RED, weight=650, anchor="middle", family=DEV_FONT),
            '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">'
            f'<path d="M0,0 L0,6 L9,3 z" fill="{RED}"/></marker></defs>',
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    OUT.write_text(render(), encoding="utf-8")
    print(OUT)

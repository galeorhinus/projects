#!/usr/bin/env python3
"""Generate the compact Chapter 11 Vedic-summary figures."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIGURES = HERE.parent
sys.path.insert(0, str(FIGURES / "_shared"))

import matra_style as ms  # noqa: E402


W = 900.0
WIDTH_IN = 4.5
DEV = ms.DEV_FONT
LATIN = ms.LATIN_FONT


def pt(points: float) -> float:
    return ms.pt_to_px(points, W, WIDTH_IN)


def rect(x: float, y: float, w: float, h: float, fill: str, *,
         stroke: str = ms.STROKE, radius: float = 5, stroke_w: float = 1.4) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="{radius:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>'
    )


def line(x1: float, y1: float, x2: float, y2: float, *,
         color: str = ms.GUIDE, width: float = 1.2) -> str:
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}"/>'
    )


def label(x: float, y: float, content: str, points: float, *,
          fill: str = ms.TEXT, anchor: str = "middle", weight: str = "400",
          style: str = "normal", family: str = LATIN) -> str:
    return ms.text(
        x, y, content, pt(points), fill=fill, anchor=anchor,
        weight=weight, style=style, family=family,
    )


def multiline(x: float, y: float, lines: list[str], points: float, *,
              fill: str = ms.TEXT, anchor: str = "middle", weight: str = "400",
              family: str = LATIN, gap: float = 1.22) -> str:
    fs = pt(points)
    start = y - (len(lines) - 1) * fs * gap / 2
    return "\n".join(
        label(x, start + i * fs * gap, text, points, fill=fill,
              anchor=anchor, weight=weight, family=family)
        for i, text in enumerate(lines)
    )


def wrap_svg(height: float, title: str, body: list[str]) -> str:
    return ms.svg(W, height, "\n".join(body), title=title, width_in=WIDTH_IN)


def activation_procedures() -> str:
    height = 610.0
    body = [
        label(34, 40, "ATOM", 9.5, fill=ms.MUTED, anchor="start", weight="700"),
        label(220, 40, "PREPARATION", 9.5, fill=ms.MUTED, anchor="start", weight="700"),
        label(860, 40, "COMPLETED VERB", 9.5, fill=ms.MUTED, anchor="end", weight="700"),
        line(30, 65, 870, 65, color=ms.STROKE, width=1.5),
    ]

    rows = [
        ("⟪इ⟫", "i", ["vowel change"], "एति", "eti"),
        ("⟪भू⟫", "bhū", ["vowel change", "and insertion"], "भवति", "bhavati"),
        ("⟪दा⟫", "dā", ["repetition"], "ददाति", "dadāti"),
        ("⟪रुध्⟫", "rudh", ["nasal insertion", "inside the atom"], "रुणद्धि", "ruṇaddhi"),
        ("⟪सु⟫", "su", ["nasal extension", "after the atom"], "सुनोति", "sunoti"),
    ]

    top = 82.0
    row_h = 96.0
    for i, (atom, atom_iast, procedure, verb, verb_iast) in enumerate(rows):
        y = top + i * row_h
        fill = "#fbf9f4" if i % 2 == 0 else "#f4efe4"
        body.append(rect(30, y, 840, 80, fill, stroke=ms.GUIDE, radius=4, stroke_w=1.0))
        body.append(rect(48, y + 10, 142, 60, ms.LIGHT_FILL, radius=4))
        body.append(label(119, y + 30, atom, 12, family=DEV, weight="600"))
        body.append(label(119, y + 55, atom_iast, 9.5, fill=ms.MUTED, style="italic"))
        body.append(multiline(235, y + 40, procedure, 10.5, anchor="start", weight="600"))
        body.append(label(615, y + 40, "→", 15, fill=ms.GOLD, weight="700"))
        body.append(rect(675, y + 10, 177, 60, ms.DARK_FILL, radius=4))
        body.append(label(764, y + 29, verb, 12, fill=ms.INK_LIGHT, family=DEV, weight="600"))
        body.append(label(764, y + 54, verb_iast, 9.5, fill=ms.INK_LIGHT, style="italic"))

    return wrap_svg(height, "Five Vedic activation procedures", body)


def verbal_breadth() -> str:
    height = 690.0
    body = [
        label(30, 42, "WHO ACTS?", 10, fill=ms.MUTED, anchor="start", weight="700"),
        label(870, 42, "ONE ATOM: ⟪इ⟫ (i), TO GO", 10, fill=ms.MUTED, anchor="end", weight="700"),
    ]

    x0, y0, row_h = 30.0, 70.0, 84.0
    widths = [230.0, 305.0, 305.0]
    headers = ["PERSON", "SINGULAR", "PLURAL"]
    x = x0
    for width, header in zip(widths, headers):
        body.append(rect(x, y0, width, 54, ms.DARK_FILL, radius=3))
        body.append(label(x + width / 2, y0 + 29, header, 9.5, fill=ms.INK_LIGHT, weight="700"))
        x += width

    persons = [
        ("speaker", "एमि", "emi · I go", "इमः", "imaḥ · we go"),
        ("addressed", "एषि", "eṣi · you go", "इथ", "itha · you all go"),
        ("described", "एति", "eti · he, she, or it goes", "यन्ति", "yanti · they go"),
    ]
    for i, row in enumerate(persons):
        y = y0 + 54 + i * row_h
        cells = [
            (widths[0], row[0], "", False),
            (widths[1], row[1], row[2], True),
            (widths[2], row[3], row[4], True),
        ]
        x = x0
        for j, (width, main, sub, deva) in enumerate(cells):
            fill = "#fbf9f4" if i % 2 == 0 else "#f4efe4"
            body.append(rect(x, y, width, row_h, fill, stroke=ms.GUIDE, radius=0, stroke_w=1.0))
            if deva:
                body.append(label(x + width / 2, y + 28, main, 11.5, family=DEV, weight="600"))
                body.append(label(x + width / 2, y + 58, sub, 9.2, fill=ms.MUTED, style="italic"))
            else:
                body.append(label(x + 20, y + row_h / 2, main, 10.5, anchor="start", weight="600"))
            x += width

    lower_top = 408.0
    body.extend([
        label(30, lower_top, "WHAT THE ACTION EXPRESSES", 10, fill=ms.MUTED, anchor="start", weight="700"),
        line(30, lower_top + 25, 870, lower_top + 25, color=ms.STROKE, width=1.5),
    ])
    forms = [
        ("present", "भवति", "bhavati", "becomes", "RV 1.17.5"),
        ("past", "आसीत्", "āsīt", "was", "RV 10.129.1"),
        ("future", "करिष्यति", "kariṣyati", "will do", "RV 1.164.39"),
        ("command", "भव", "bhava", "become", "RV 1.1.9"),
        ("possibility|or desire", "स्याम", "syāma", "may we be", "RV 1.4.6"),
    ]
    card_gap = 10.0
    card_w = (840.0 - card_gap * 4) / 5
    card_y = lower_top + 45
    for i, (kind, deva, iast, meaning, passage) in enumerate(forms):
        x = 30 + i * (card_w + card_gap)
        body.append(rect(x, card_y, card_w, 190, "#f4efe4", stroke=ms.GUIDE, radius=4, stroke_w=1.0))
        body.append(multiline(x + card_w / 2, card_y + 28, kind.split("|"), 8.7,
                              fill=ms.MUTED, weight="700"))
        body.append(label(x + card_w / 2, card_y + 82, deva, 11.2, family=DEV, weight="600"))
        body.append(label(x + card_w / 2, card_y + 112, iast, 9.2, style="italic"))
        body.append(label(x + card_w / 2, card_y + 142, meaning, 9.3, weight="600"))
        body.append(label(x + card_w / 2, card_y + 169, passage, 8.5, fill=ms.MUTED))

    return wrap_svg(height, "The grammatical breadth carried by completed Sanskrit verbs", body)


def main() -> None:
    outputs = {
        "five_vedic_activations.from-py.svg": activation_procedures(),
        "vedic_verbal_breadth.from-py.svg": verbal_breadth(),
    }
    for filename, content in outputs.items():
        path = HERE / filename
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()

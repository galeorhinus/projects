#!/usr/bin/env python3
"""Render the selected and excluded one- and two-matra vowel forms."""

from __future__ import annotations

import html
from pathlib import Path


OUT = Path(__file__).with_name("svara_selected_excluded_forms.from-py.svg")

WIDTH = 1200
HEIGHT = 700

PAPER = "#f7f4ed"
INK = "#29251f"
MUTED = "#6e675d"
GOLD = "#9d7c36"
GOLD_LIGHT = "#e8dfcc"
GRID = "#cfc6b5"
ROW_ALT = "#f0ece3"
EXCLUDED = "#e4e1da"
RED = "#8b4b3d"

LATIN = "EB Garamond, Charter, Georgia, serif"
DEVA = "Adobe Devanagari, Noto Serif Devanagari, serif"

ROWS = [
    ("संवृत अवर्ण", "saṃvṛta avarṇa", ("अ", "Selected"), ("long contracted a", "Excluded")),
    ("विवृत अवर्ण", "vivṛta avarṇa", ("short open a", "Excluded"), ("आ", "Selected")),
    ("एकार", "ekāra", ("one-mātrā e", "Excluded"), ("ए", "Selected")),
    ("ओकार", "okāra", ("one-mātrā o", "Excluded"), ("ओ", "Selected")),
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text(
    x: float,
    y: float,
    value: str,
    *,
    size: int,
    color: str = INK,
    weight: int = 400,
    anchor: str = "start",
    italic: bool = False,
    family: str = LATIN,
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{esc(family)}" '
        f'font-size="{size}" font-weight="{weight}" '
        f'font-style="{"italic" if italic else "normal"}" fill="{color}" '
        f'text-anchor="{anchor}">{esc(value)}</text>'
    )


def check(x: float, y: float) -> str:
    return (
        f'<path d="M {x - 11:.1f},{y:.1f} L {x - 3:.1f},{y + 9:.1f} '
        f'L {x + 14:.1f},{y - 12:.1f}" fill="none" stroke="{GOLD}" '
        'stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def cross(x: float, y: float) -> str:
    return (
        f'<path d="M {x - 10},{y - 10} L {x + 10},{y + 10} '
        f'M {x + 10},{y - 10} L {x - 10},{y + 10}" fill="none" '
        f'stroke="{RED}" stroke-width="3" stroke-linecap="round"/>'
    )


def cell(x: float, y: float, width: float, height: float, content: tuple[str, str]) -> list[str]:
    label, status = content
    selected = status == "Selected"
    fill = GOLD_LIGHT if selected else EXCLUDED
    symbol_x = x + 48
    center_y = y + height / 2
    label_family = DEVA if selected else LATIN
    label_size = 34 if selected else 21
    return [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'fill="{fill}" stroke="{GRID}" stroke-width="1"/>',
        check(symbol_x, center_y) if selected else cross(symbol_x, center_y),
        text(
            x + width / 2 + 16,
            center_y - 3,
            label,
            size=label_size,
            weight=600 if selected else 500,
            anchor="middle",
            family=label_family,
        ),
        text(
            x + width / 2 + 16,
            center_y + 24,
            status,
            size=16,
            color=GOLD if selected else RED,
            italic=True,
            anchor="middle",
        ),
    ]


def render() -> str:
    x0 = 54
    table_y = 190
    label_w = 454
    cell_w = 346
    header_h = 62
    row_h = 82
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{PAPER}"/>',
        text(54, 67, "Selected and Excluded Vowel Forms", size=47, weight=600),
        text(
            54,
            109,
            "How Sanskrit pairs vowel quality with one- and two-mātrā duration",
            size=25,
            color=MUTED,
            italic=True,
        ),
        f'<line x1="54" y1="134" x2="{WIDTH - 54}" y2="134" '
        f'stroke="{GRID}" stroke-width="2"/>',
    ]

    headers = [
        (x0, label_w, "Vowel quality or family"),
        (x0 + label_w, cell_w, "1 mātrā"),
        (x0 + label_w + cell_w, cell_w, "2 mātrās"),
    ]
    for x, width, label in headers:
        parts.extend(
            [
                f'<rect x="{x}" y="{table_y}" width="{width}" height="{header_h}" '
                f'fill="{INK}" stroke="{PAPER}" stroke-width="2"/>',
                text(
                    x + (22 if x == x0 else width / 2),
                    table_y + 40,
                    label,
                    size=23,
                    color=PAPER,
                    weight=600,
                    anchor="start" if x == x0 else "middle",
                ),
            ]
        )

    for index, (deva, iast, one, two) in enumerate(ROWS):
        y = table_y + header_h + index * row_h
        fill = PAPER if index % 2 == 0 else ROW_ALT
        parts.extend(
            [
                f'<rect x="{x0}" y="{y}" width="{label_w}" height="{row_h}" '
                f'fill="{fill}" stroke="{GRID}" stroke-width="1"/>',
                text(x0 + 22, y + 38, deva, size=25, weight=600, family=DEVA),
                text(x0 + 220, y + 38, iast, size=21, color=MUTED, italic=True),
            ]
        )
        parts.extend(cell(x0 + label_w, y, cell_w, row_h, one))
        parts.extend(cell(x0 + label_w + cell_w, y, cell_w, row_h, two))

    callout_y = table_y + header_h + len(ROWS) * row_h + 28
    parts.extend(
        [
            f'<rect x="54" y="{callout_y}" width="{WIDTH - 108}" height="76" rx="4" '
            f'fill="{GOLD_LIGHT}" stroke="{GRID}" stroke-width="1"/>',
            text(76, callout_y + 31, "Lineage-Bounded:", size=20, color=GOLD, weight=600),
            text(
                232,
                callout_y + 31,
                "half-ए and half-ओ are preserved in named Sāmavedic lineages.",
                size=20,
                family=DEVA,
            ),
            text(
                76,
                callout_y + 58,
                "They do not become generally reusable one-mātrā forms.",
                size=19,
                color=MUTED,
            ),
            "</svg>",
        ]
    )
    return "\n".join(parts)


def main() -> None:
    OUT.write_text(render(), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

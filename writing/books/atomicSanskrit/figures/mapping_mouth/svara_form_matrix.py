#!/usr/bin/env python3
"""Render the 9 x 9 x 2 Sanskrit svara form matrix."""

from __future__ import annotations

import html
from pathlib import Path


OUT = Path(__file__).with_name("svara_form_matrix.from-py.svg")

WIDTH = 1200
HEIGHT = 1160

PAPER = "#f7f4ed"
INK = "#29251f"
MUTED = "#6e675d"
GOLD = "#9d7c36"
GOLD_LIGHT = "#e8dfcc"
GRID = "#cfc6b5"
SELECTED = "#eee9de"
SELECTED_ALT = "#e3dac7"
RESTRICTED = "#d4c6a8"
EXCLUDED = "#e4e1da"
RED = "#8b4b3d"

LATIN = "EB Garamond, Charter, Georgia, serif"
DEVA = "Adobe Devanagari, Noto Serif Devanagari, serif"

FAMILIES = ["अ", "इ", "उ", "ऋ", "ऌ", "ए", "ऐ", "ओ", "औ"]
PITCHES = [("उ", "udātta"), ("अ", "anudātta"), ("स्व", "svarita")]


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
    style = "italic" if italic else "normal"
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{esc(family)}" '
        f'font-size="{size}" font-weight="{weight}" font-style="{style}" '
        f'fill="{color}" text-anchor="{anchor}">{esc(value)}</text>'
    )


def line(x1: float, y1: float, x2: float, y2: float, **attrs: object) -> str:
    properties = " ".join(f'{key}="{esc(value)}"' for key, value in attrs.items())
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {properties}/>'


def check(x: float, y: float, color: str = INK) -> str:
    return (
        f'<path d="M {x - 8:.1f},{y:.1f} L {x - 2:.1f},{y + 7:.1f} '
        f'L {x + 10:.1f},{y - 9:.1f}" fill="none" stroke="{color}" '
        'stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def is_selected(row: int, duration: int) -> bool:
    if duration == 1:
        return row <= 4
    if duration == 2:
        return row != 4
    return True


def render() -> str:
    left = 104
    top = 252
    cell_w = 102
    cell_h = 68
    grid_w = cell_w * 9
    grid_h = cell_h * 9
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{PAPER}"/>',
        text(54, 66, "The Svara Form Matrix", size=47, weight=600),
        text(
            54,
            108,
            "Nine vowel families × three durations × three pitch relations × two nasal states",
            size=25,
            color=MUTED,
            italic=True,
        ),
        line(54, 134, WIDTH - 54, 134, stroke=GRID, **{"stroke-width": 2}),
    ]

    for duration in range(1, 4):
        group_x = left + (duration - 1) * cell_w * 3
        fill = RESTRICTED if duration == 3 else GOLD_LIGHT
        parts.append(
            f'<rect x="{group_x}" y="154" width="{cell_w * 3}" height="48" '
            f'fill="{fill}" stroke="{GRID}" stroke-width="1"/>'
        )
        label = f"{duration} mātrā" if duration == 1 else f"{duration} mātrās"
        parts.append(
            text(
                group_x + cell_w * 1.5,
                186,
                label,
                size=25,
                weight=600,
                anchor="middle",
            )
        )
        if duration == 3:
            parts.append(
                text(
                    group_x + cell_w * 3 - 12,
                    186,
                    "Restricted",
                    size=16,
                    color=RED,
                    italic=True,
                    anchor="end",
                )
            )

    for col in range(9):
        pitch_short, pitch_long = PITCHES[col % 3]
        x = left + col * cell_w
        parts.extend(
            [
                f'<rect x="{x}" y="202" width="{cell_w}" height="50" '
                f'fill="{PAPER}" stroke="{GRID}" stroke-width="1"/>',
                text(
                    x + cell_w / 2,
                    224,
                    pitch_short,
                    size=20,
                    weight=600,
                    anchor="middle",
                    family=DEVA,
                ),
                text(
                    x + cell_w / 2,
                    244,
                    pitch_long,
                    size=12,
                    color=MUTED,
                    anchor="middle",
                    italic=True,
                ),
            ]
        )

    parts.extend(
        [
            text(72, 238, "family", size=18, color=MUTED, anchor="middle"),
            text(left + grid_w + 50, 238, "total", size=18, color=MUTED, anchor="middle"),
        ]
    )

    selected_count = 0
    excluded_count = 0
    for row, family in enumerate(FAMILIES):
        y = top + row * cell_h
        parts.append(
            f'<rect x="40" y="{y}" width="64" height="{cell_h}" '
            f'fill="{GOLD_LIGHT}" stroke="{GRID}" stroke-width="1"/>'
        )
        parts.append(
            text(72, y + 45, family, size=31, weight=600, anchor="middle", family=DEVA)
        )
        row_total = 0
        for col in range(9):
            duration = col // 3 + 1
            x = left + col * cell_w
            selected = is_selected(row, duration)
            fill = RESTRICTED if duration == 3 else (SELECTED_ALT if row % 2 else SELECTED)
            if not selected:
                fill = EXCLUDED
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" '
                f'fill="{fill}" stroke="{GRID}" stroke-width="1"/>'
            )
            parts.append(
                line(
                    x + cell_w / 2,
                    y,
                    x + cell_w / 2,
                    y + cell_h,
                    stroke=GRID,
                    **{"stroke-width": 1},
                )
            )
            for half in range(2):
                center_x = x + cell_w * (0.25 if half == 0 else 0.75)
                if selected:
                    parts.append(check(center_x, y + cell_h / 2, GOLD if duration < 3 else INK))
                    selected_count += 1
                    row_total += 1
                else:
                    parts.extend(
                        [
                            line(
                                center_x - 10,
                                y + cell_h / 2 - 10,
                                center_x + 10,
                                y + cell_h / 2 + 10,
                                stroke=RED,
                                **{"stroke-width": 2},
                            ),
                            line(
                                center_x + 10,
                                y + cell_h / 2 - 10,
                                center_x - 10,
                                y + cell_h / 2 + 10,
                                stroke=RED,
                                **{"stroke-width": 2},
                            ),
                        ]
                    )
                    excluded_count += 1
        parts.append(
            text(
                left + grid_w + 50,
                y + 44,
                str(row_total),
                size=25,
                weight=600,
                anchor="middle",
            )
        )

    legend_y = top + grid_h + 44
    parts.extend(
        [
            check(68, legend_y - 4, GOLD),
            text(88, legend_y + 4, "selected form", size=19),
            line(307, legend_y - 14, 327, legend_y + 6, stroke=RED, **{"stroke-width": 2}),
            line(327, legend_y - 14, 307, legend_y + 6, stroke=RED, **{"stroke-width": 2}),
            text(339, legend_y + 4, "Excluded", size=19),
            f'<rect x="492" y="{legend_y - 24}" width="28" height="28" fill="{RESTRICTED}" '
            f'stroke="{GRID}" stroke-width="1"/>',
            text(532, legend_y + 4, "Restricted: pluta", size=19),
            f'<rect x="747" y="{legend_y - 24}" width="28" height="28" fill="{SELECTED}" '
            f'stroke="{GRID}" stroke-width="1"/>',
            line(761, legend_y - 24, 761, legend_y + 4, stroke=GRID, **{"stroke-width": 1}),
            text(787, legend_y - 5, "oral", size=15),
            text(787, legend_y + 14, "nasal", size=15, color=MUTED),
        ]
    )

    callout_y = legend_y + 38
    parts.extend(
        [
            f'<rect x="54" y="{callout_y}" width="{WIDTH - 108}" height="66" rx="4" '
            f'fill="{GOLD_LIGHT}" stroke="{GRID}" stroke-width="1"/>',
            text(76, callout_y + 28, "Lineage-Bounded:", size=19, color=GOLD, weight=600),
            text(
                222,
                callout_y + 28,
                "half-ए and half-ओ remain outside the regular matrix.",
                size=19,
                family=DEVA,
            ),
            text(
                76,
                callout_y + 52,
                "They are preserved where the inherited Sāmavedic lineages require them.",
                size=18,
                color=MUTED,
            ),
        ]
    )

    arithmetic_y = callout_y + 98
    parts.extend(
        [
            f'<rect x="54" y="{arithmetic_y}" width="{WIDTH - 108}" height="64" '
            f'fill="{INK}"/>',
            text(
                WIDTH / 2,
                arithmetic_y + 41,
                f"162 possible positions − {excluded_count} Excluded = {selected_count} selected forms",
                size=28,
                color=PAPER,
                weight=600,
                anchor="middle",
            ),
            text(
                WIDTH / 2,
                HEIGHT - 18,
                "A check marks an analytically selected form, not a claim of surviving textual occurrence.",
                size=17,
                color=MUTED,
                italic=True,
                anchor="middle",
            ),
            "</svg>",
        ]
    )
    assert selected_count == 132
    assert excluded_count == 30
    return "\n".join(parts)


def main() -> None:
    OUT.write_text(render(), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

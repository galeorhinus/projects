#!/usr/bin/env python3
"""Render the designed-variation and composition-permission matrix."""

from __future__ import annotations

import html
from pathlib import Path


OUT = Path(__file__).with_name("two_domain_permissions_matrix.from-py.svg")

WIDTH = 1200
HEIGHT = 1020

PAPER = "#f7f4ed"
INK = "#29251f"
MUTED = "#6e675d"
GOLD = "#9d7c36"
GOLD_LIGHT = "#e8dfcc"
SAGE = "#dfe5d9"
SAGE_DARK = "#52634d"
ROSE = "#eadbd6"
ROSE_DARK = "#824d43"
STONE = "#e7e3da"
GRID = "#bdb4a5"

LATIN = "EB Garamond, Charter, Georgia, serif"
DEVA = "Adobe Devanagari, Noto Serif Devanagari, serif"


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
    letter_spacing: float = 0,
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{esc(family)}" '
        f'font-size="{size}" font-weight="{weight}" '
        f'font-style="{"italic" if italic else "normal"}" fill="{color}" '
        f'letter-spacing="{letter_spacing}" text-anchor="{anchor}">{esc(value)}</text>'
    )


def multiline(
    x: float,
    y: float,
    lines: list[str],
    *,
    size: int,
    line_height: int,
    color: str = INK,
    weight: int = 400,
    anchor: str = "middle",
    italic: bool = False,
    family: str = LATIN,
) -> list[str]:
    return [
        text(
            x,
            y + index * line_height,
            line,
            size=size,
            color=color,
            weight=weight,
            anchor=anchor,
            italic=italic,
            family=family,
        )
        for index, line in enumerate(lines)
    ]


def scope_mark(x: float, y: float, *, selected: bool) -> list[str]:
    color = GOLD if selected else ROSE_DARK
    parts = [f'<circle cx="{x}" cy="{y}" r="18" fill="{color}"/>']
    if selected:
        parts.append(
            f'<path d="M {x - 9},{y} L {x - 2},{y + 8} L {x + 11},{y - 10}" '
            f'fill="none" stroke="{PAPER}" stroke-width="4" stroke-linecap="round" '
            'stroke-linejoin="round"/>'
        )
    else:
        parts.extend(
            [
                f'<line x1="{x - 8}" y1="{y - 8}" x2="{x + 8}" y2="{y + 8}" '
                f'stroke="{PAPER}" stroke-width="4" stroke-linecap="round"/>',
                f'<line x1="{x + 8}" y1="{y - 8}" x2="{x - 8}" y2="{y + 8}" '
                f'stroke="{PAPER}" stroke-width="4" stroke-linecap="round"/>',
            ]
        )
    return parts


def cell(
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    fill: str,
    stroke: str,
    heading: str,
    heading_family: str = LATIN,
    heading_color: str = INK,
    premise: list[str],
    detail: list[str],
    strong: bool = False,
    selected: bool = False,
) -> list[str]:
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{4 if strong else 2}"/>',
        text(
            x + width / 2,
            y + 62,
            heading,
            size=34 if strong else 29,
            color=heading_color,
            weight=600,
            anchor="middle",
            family=heading_family,
        ),
    ]
    parts.extend(scope_mark(x + 35, y + 35, selected=selected))
    parts.extend(
        multiline(
            x + width / 2,
            y + 113,
            premise,
            size=27,
            line_height=30,
            color=INK,
            weight=600 if strong else 500,
        )
    )
    divider_y = y + 178
    parts.append(
        f'<line x1="{x + 55}" y1="{divider_y}" x2="{x + width - 55}" '
        f'y2="{divider_y}" stroke="{stroke}" stroke-width="1.5"/>'
    )
    parts.extend(
        multiline(
            x + width / 2,
            y + 210,
            detail,
            size=28,
            line_height=30,
            color=MUTED,
        )
    )
    return parts


def render() -> str:
    plot_x = 197
    plot_y = 230
    cell_w = 466
    cell_h = 292
    plot_w = cell_w * 2
    plot_h = cell_h * 2

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{PAPER}"/>',
        text(54, 68, "One Architecture, Two Complementary Domains", size=46, weight=600),
        text(
            54,
            109,
            "Designed variation and permission to compose",
            size=25,
            color=MUTED,
            italic=True,
        ),
        *scope_mark(817, 101, selected=True),
        text(844, 108, "selected scope", size=19, color=MUTED, weight=600),
        *scope_mark(1013, 101, selected=False),
        text(1040, 108, "rejected", size=19, color=MUTED, weight=600),
        f'<rect x="54" y="137" width="{WIDTH - 108}" height="49" fill="{GOLD_LIGHT}"/>',
        text(
            WIDTH / 2,
            169,
            "The two domains select different balances from the same Sanskrit architecture",
            size=22,
            weight=600,
            anchor="middle",
        ),
    ]

    # Quadrants: extended variation above, restricted variation below;
    # read-only composition at left, generative composition at right.
    parts.extend(
        cell(
            plot_x,
            plot_y,
            cell_w,
            cell_h,
            fill=GOLD_LIGHT,
            stroke=GOLD,
            heading="वैदिक · vaidika",
            heading_family=DEVA,
            heading_color=INK,
            premise=["Extended designed variation", "Read-only content"],
            detail=[
                "Pitch · additional forms · leṭ",
                "Fixed words and inherited meaning",
                "contain collisions within each passage",
            ],
            strong=True,
            selected=True,
        )
    )
    parts.extend(
        cell(
            plot_x + cell_w,
            plot_y,
            cell_w,
            cell_h,
            fill=ROSE,
            stroke=ROSE_DARK,
            heading="Collision-prone composition",
            heading_color=ROSE_DARK,
            premise=["Laukika with Vedic variation", "Generative content"],
            detail=[
                "Overlapping forms enter",
                "newly composed sentences without",
                "fixed context to clarify them",
            ],
            selected=False,
        )
    )
    parts.extend(
        cell(
            plot_x,
            plot_y + cell_h,
            cell_w,
            cell_h,
            fill=STONE,
            stroke=GRID,
            heading="Insufficient calibrant",
            heading_color=ROSE_DARK,
            premise=["Vaidika without its extended range", "Read-only content"],
            detail=[
                "Stable enough for a small corpus,",
                "but too narrow to display Sanskrit's",
                "full calibrating architecture",
            ],
            selected=False,
        )
    )
    parts.extend(
        cell(
            plot_x + cell_w,
            plot_y + cell_h,
            cell_w,
            cell_h,
            fill=SAGE,
            stroke=SAGE_DARK,
            heading="लौकिक · laukika",
            heading_family=DEVA,
            heading_color=INK,
            premise=["Restricted designed variation", "Generative content"],
            detail=[
                "A reusable kernel supports new words,",
                "sciences, stories, arguments,",
                "and compositions in every age",
            ],
            strong=True,
            selected=True,
        )
    )

    # Axes and endpoint labels.
    axis_x = 166
    axis_bottom = plot_y + plot_h
    parts.extend(
        [
            f'<line x1="{axis_x}" y1="{axis_bottom}" x2="{axis_x}" y2="{plot_y - 18}" '
            f'stroke="{INK}" stroke-width="3"/>',
            f'<path d="M {axis_x - 8},{plot_y - 7} L {axis_x},{plot_y - 20} '
            f'L {axis_x + 8},{plot_y - 7}" fill="none" stroke="{INK}" stroke-width="3"/>',
            text(151, plot_y + 36, "EXTENDED", size=21, color=GOLD, weight=600, anchor="end"),
            text(151, axis_bottom - 14, "RESTRICTED", size=21, color=MUTED, weight=600, anchor="end"),
            f'<text x="52" y="{plot_y + plot_h / 2}" font-family="{LATIN}" font-size="22" '
            f'font-weight="600" fill="{INK}" text-anchor="middle" '
            f'transform="rotate(-90 52 {plot_y + plot_h / 2})">DESIGNED VARIATION</text>',
            f'<line x1="{plot_x}" y1="{axis_bottom + 33}" x2="{plot_x + plot_w + 18}" '
            f'y2="{axis_bottom + 33}" stroke="{INK}" stroke-width="3"/>',
            f'<path d="M {plot_x + plot_w + 6},{axis_bottom + 25} '
            f'L {plot_x + plot_w + 20},{axis_bottom + 33} '
            f'L {plot_x + plot_w + 6},{axis_bottom + 41}" fill="none" '
            f'stroke="{INK}" stroke-width="3"/>',
            text(plot_x, axis_bottom + 66, "READ-ONLY", size=21, color=MUTED, weight=600),
            text(
                plot_x + plot_w,
                axis_bottom + 66,
                "GENERATIVE",
                size=21,
                color=GOLD,
                weight=600,
                anchor="end",
            ),
            text(
                plot_x + plot_w / 2,
                axis_bottom + 103,
                "PERMISSION TO COMPOSE NEW CONTENT",
                size=22,
                weight=600,
                anchor="middle",
            ),
        ]
    )

    # Closing statement.
    parts.extend(
        [
            f'<rect x="54" y="{HEIGHT - 72}" width="{WIDTH - 108}" height="54" fill="{INK}"/>',
            text(
                WIDTH / 2,
                HEIGHT - 37,
                "Each domain accepts the range needed for its purpose.",
                size=25,
                color=PAPER,
                weight=600,
                anchor="middle",
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

#!/usr/bin/env python3
"""Render the shared svara architecture across the vaidika and laukika domains."""

from __future__ import annotations

import html
from pathlib import Path


OUT = Path(__file__).with_name("svara_two_domains.from-py.svg")

WIDTH = 1200
HEIGHT = 875

PAPER = "#f7f4ed"
INK = "#29251f"
MUTED = "#6e675d"
GOLD = "#9d7c36"
GOLD_LIGHT = "#e8dfcc"
GRID = "#cfc6b5"
ROW_ALT = "#f0ece3"
RESTRICTED = "#d4c6a8"
RED = "#8b4b3d"

LATIN = "EB Garamond, Charter, Georgia, serif"
DEVA = "Adobe Devanagari, Noto Serif Devanagari, serif"

ROWS = [
    ("Vowel families and ordinary duration", True, True, "Shared"),
    ("Vedic pitch layer: udātta · anudātta · svarita", True, False, "Vaidika"),
    ("Exact lineage-preserved form", True, False, "Lineage-Bounded"),
    ("New composition through the shared system", False, True, "Laukika"),
    ("Pluta under stated conditions", "restricted", "restricted", "Restricted"),
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


def check(x: float, y: float, color: str = GOLD) -> str:
    return (
        f'<path d="M {x - 12:.1f},{y:.1f} L {x - 3:.1f},{y + 10:.1f} '
        f'L {x + 15:.1f},{y - 13:.1f}" fill="none" stroke="{color}" '
        'stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def domain_mark(x: float, y: float, value: object) -> list[str]:
    if value is True:
        return [
            f'<circle cx="{x}" cy="{y}" r="29" fill="{GOLD_LIGHT}" stroke="{GOLD}" stroke-width="2"/>',
            check(x, y),
        ]
    if value == "restricted":
        return [
            f'<circle cx="{x}" cy="{y}" r="29" fill="{RESTRICTED}" stroke="{GOLD}" stroke-width="2"/>',
            f'<path d="M {x - 13},{y + 2} L {x - 3},{y + 12} L {x + 8},{y - 2}" '
            f'fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" '
            'stroke-linejoin="round"/>',
            f'<path d="M {x + 8},{y - 2} L {x + 16},{y - 13}" fill="none" '
            f'stroke="{MUTED}" stroke-width="3" stroke-dasharray="4 4"/>',
        ]
    return [
        f'<circle cx="{x}" cy="{y}" r="29" fill="{PAPER}" stroke="{GRID}" stroke-width="2"/>'
    ]


def render() -> str:
    x0 = 54
    feature_w = 610
    domain_w = 160
    scope_w = 216
    table_y = 214
    header_h = 78
    row_h = 86
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{PAPER}"/>',
        text(54, 68, "One Svara Architecture, Two Domains", size=48, weight=600),
        text(
            54,
            111,
            "How Vaidika preservation and Laukika composition use the same vowel system",
            size=25,
            color=MUTED,
            italic=True,
        ),
        f'<rect x="54" y="142" width="{WIDTH - 108}" height="46" fill="{GOLD_LIGHT}"/>',
        text(
            WIDTH / 2,
            173,
            "Nine vowel families · duration · pitch · nasality",
            size=23,
            color=INK,
            weight=600,
            anchor="middle",
        ),
    ]

    headers = [
        (x0, feature_w, "Feature"),
        (x0 + feature_w, domain_w, "वैदिक · vaidika"),
        (x0 + feature_w + domain_w, domain_w, "लौकिक · laukika"),
        (x0 + feature_w + domain_w * 2, scope_w, "Scope"),
    ]
    for x, width, label in headers:
        parts.extend(
            [
                f'<rect x="{x}" y="{table_y}" width="{width}" height="{header_h}" '
                f'fill="{INK}" stroke="{PAPER}" stroke-width="2"/>',
                text(
                    x + (24 if label == "Feature" else width / 2),
                    table_y + 49,
                    label,
                    size=23,
                    color=PAPER,
                    weight=600,
                    anchor="start" if label == "Feature" else "middle",
                    family=DEVA if "·" in label else LATIN,
                ),
            ]
        )

    for index, (feature, vaidika, laukika, scope) in enumerate(ROWS):
        y = table_y + header_h + index * row_h
        fill = ROW_ALT if index % 2 else PAPER
        for x, width in [
            (x0, feature_w),
            (x0 + feature_w, domain_w),
            (x0 + feature_w + domain_w, domain_w),
            (x0 + feature_w + domain_w * 2, scope_w),
        ]:
            parts.append(
                f'<rect x="{x}" y="{y}" width="{width}" height="{row_h}" '
                f'fill="{fill}" stroke="{GRID}" stroke-width="1"/>'
            )
        parts.append(text(x0 + 24, y + 52, feature, size=23, weight=500))
        parts.extend(domain_mark(x0 + feature_w + domain_w / 2, y + row_h / 2, vaidika))
        parts.extend(
            domain_mark(
                x0 + feature_w + domain_w + domain_w / 2,
                y + row_h / 2,
                laukika,
            )
        )
        scope_color = GOLD if scope in {"Shared", "Vaidika", "Laukika"} else RED
        parts.append(
            text(
                x0 + feature_w + domain_w * 2 + scope_w / 2,
                y + 51,
                scope,
                size=21,
                color=scope_color,
                weight=600,
                anchor="middle",
            )
        )

    bottom_y = table_y + header_h + len(ROWS) * row_h + 34
    parts.extend(
        [
            text(54, bottom_y, "The domains share a vowel system.", size=22, weight=600),
            text(
                54,
                bottom_y + 31,
                "Their permissions differ because preservation and new composition serve different purposes.",
                size=21,
                color=MUTED,
            ),
            f'<rect x="54" y="{bottom_y + 56}" width="{WIDTH - 108}" height="62" fill="{INK}"/>',
            text(
                WIDTH / 2,
                bottom_y + 96,
                "One vowel system. Different permissions.",
                size=29,
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

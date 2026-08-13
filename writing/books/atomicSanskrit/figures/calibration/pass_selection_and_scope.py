#!/usr/bin/env python3
"""Render the Principle of Architectural Selection and Scope figure."""

from __future__ import annotations

import html
from pathlib import Path


OUT = Path(__file__).with_name("pass_selection_and_scope.from-py.svg")

WIDTH = 1200
HEIGHT = 900

PAPER = "#f7f4ed"
INK = "#29251f"
MUTED = "#6e675d"
GOLD = "#9d7c36"
GOLD_LIGHT = "#e8dfcc"
GRID = "#cfc6b5"
ROW_ALT = "#f0ece3"
RED = "#8b4b3d"
GREEN = "#65715b"

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
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{esc(family)}" '
        f'font-size="{size}" font-weight="{weight}" '
        f'font-style="{"italic" if italic else "normal"}" fill="{color}" '
        f'text-anchor="{anchor}">{esc(value)}</text>'
    )


def multiline(
    x: float,
    y: float,
    lines: list[str],
    *,
    size: int,
    color: str = INK,
    weight: int = 400,
    anchor: str = "start",
    leading: int = 27,
    italic: bool = False,
) -> list[str]:
    result = [
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{LATIN}" '
        f'font-size="{size}" font-weight="{weight}" '
        f'font-style="{"italic" if italic else "normal"}" fill="{color}" '
        f'text-anchor="{anchor}">'
    ]
    for index, line in enumerate(lines):
        result.append(
            f'<tspan x="{x:.1f}" dy="{0 if index == 0 else leading}">'
            f"{esc(line)}</tspan>"
        )
    result.append("</text>")
    return result


def arrow(x1: float, y1: float, x2: float, y2: float) -> str:
    return (
        f'<path d="M {x1},{y1} L {x2},{y2}" stroke="{GOLD}" '
        'stroke-width="4" fill="none" marker-end="url(#arrowhead)"/>'
    )


def box(
    x: float,
    y: float,
    width: float,
    height: float,
    number: str,
    heading: str,
    prompt: list[str],
) -> list[str]:
    return [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="5" '
        f'fill="{ROW_ALT}" stroke="{GRID}" stroke-width="2"/>',
        f'<circle cx="{x + 31}" cy="{y + 31}" r="18" fill="{INK}"/>',
        text(x + 31, y + 38, number, size=20, color=PAPER, weight=600, anchor="middle"),
        text(x + 58, y + 38, heading, size=23, weight=600),
        *multiline(x + 22, y + 78, prompt, size=19, color=MUTED, leading=23),
    ]


def scope_pill(x: float, y: float, width: float, label: str, color: str) -> list[str]:
    return [
        f'<rect x="{x}" y="{y}" width="{width}" height="43" rx="21.5" '
        f'fill="{color}"/>',
        text(x + width / 2, y + 29, label, size=18, color=PAPER, weight=600, anchor="middle"),
    ]


def comparison_row(
    y: float,
    candidate: str,
    candidate_note: str,
    restricted: str,
    restricted_note: str,
) -> list[str]:
    left_x = 72
    right_x = 620
    box_w = 508
    box_h = 112
    return [
        f'<rect x="{left_x}" y="{y}" width="{box_w}" height="{box_h}" rx="5" '
        f'fill="{PAPER}" stroke="{RED}" stroke-width="2"/>',
        text(left_x + 22, y + 38, candidate, size=27, color=RED, weight=600),
        *multiline(left_x + 22, y + 71, [candidate_note], size=18, color=MUTED),
        f'<rect x="{right_x}" y="{y}" width="{box_w}" height="{box_h}" rx="5" '
        f'fill="{PAPER}" stroke="{GREEN}" stroke-width="2"/>',
        text(right_x + 22, y + 38, restricted, size=27, color=GREEN, weight=600),
        *multiline(right_x + 22, y + 71, [restricted_note], size=18, color=MUTED),
    ]


def render() -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">',
        "<defs>",
        f'<marker id="arrowhead" markerWidth="10" markerHeight="10" refX="8" '
        f'refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{GOLD}"/></marker>',
        "</defs>",
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{PAPER}"/>',
        text(52, 66, "What Earns a Place in the Architecture", size=44, weight=600),
        text(
            52,
            107,
            "The Principle of Architectural Selection and Scope",
            size=25,
            color=MUTED,
            italic=True,
        ),
    ]

    y = 145
    w = 245
    h = 118
    gap = 43
    xs = [52 + index * (w + gap) for index in range(4)]
    prompts = [
        ("1", "Contribution", ["What does it add?"]),
        ("2", "Load", ["What collision or", "duplication follows?"]),
        ("3", "Bounding support", ["What contains", "that load?"]),
        ("4", "Scope", ["Where can it operate?"]),
    ]
    for x, values in zip(xs, prompts):
        parts.extend(box(x, y, w, h, *values))
    for index in range(3):
        parts.append(arrow(xs[index] + w + 6, y + h / 2, xs[index + 1] - 8, y + h / 2))

    scope_y = 290
    parts.append(text(52, scope_y + 27, "Possible scopes", size=20, color=MUTED, weight=600))
    pills = [
        ("Included", 154, GREEN),
        ("Restricted", 168, GOLD),
        ("Vaidika", 143, GOLD),
        ("Lineage-Bounded", 224, GOLD),
        ("Excluded", 154, RED),
    ]
    px = 222
    for label, width, color in pills:
        parts.extend(scope_pill(px, scope_y, width, label, color))
        px += width + 13

    parts.extend(
        [
            f'<line x1="52" y1="365" x2="1148" y2="365" stroke="{GRID}" stroke-width="2"/>',
            text(52, 407, "Physical possibility does not by itself create a sonomer.", size=27, weight=600),
            text(
                52,
                439,
                "Sanskrit can leave a grid address unassigned while preserving a nearby sound under a stated condition.",
                size=20,
                color=MUTED,
            ),
            text(72, 486, "Independent grid address", size=20, color=RED, weight=600),
            text(620, 486, "Restricted articulation", size=20, color=GREEN, weight=600),
        ]
    )

    parts.extend(
        comparison_row(
            505,
            "[ɰ] · kaṇṭhya–antaḥstha",
            "No fifth vowel-to-glide operation; independent scope adds load.",
            "जिह्वामूलीय · jihvāmūlīya",
            "Generated from visarga before क / ख; Restricted scope.",
        )
    )
    parts.extend(
        comparison_row(
            637,
            "[ɸ] · oṣṭhya–ūṣman",
            "No independent recurring contrast; crowds the field beside फ.",
            "उपध्मानीय · upadhmānīya",
            "Generated from visarga before प / फ; Restricted scope.",
        )
    )

    parts.extend(
        [
            f'<rect x="52" y="785" width="1096" height="76" fill="{INK}"/>',
            text(
                600,
                820,
                "The same principle operates across scale:",
                size=21,
                color=GOLD_LIGHT,
                weight=600,
                anchor="middle",
            ),
            text(
                600,
                848,
                "sound-field → sonomer grid → Vaidika and Laukika scope",
                size=24,
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

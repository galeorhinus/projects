#!/usr/bin/env python3
"""Render the shared architecture of the vaidika and laukika domains."""

from __future__ import annotations

import html
from pathlib import Path


OUT = Path(__file__).with_name("shared_architecture_overlap.from-py.svg")

WIDTH = 1500
HEIGHT = 900

PAPER = "#f7f4ed"
INK = "#29251f"
MUTED = "#6e675d"
GOLD = "#9d7c36"
GOLD_LIGHT = "#e8dfcc"
SAGE = "#dfe5d9"
SAGE_DARK = "#52634d"
BLEND = "#d9d4bd"
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
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{esc(family)}" '
        f'font-size="{size}" font-weight="{weight}" '
        f'font-style="{"italic" if italic else "normal"}" fill="{color}" '
        f'letter-spacing="0" text-anchor="{anchor}">{esc(value)}</text>'
    )


def rule(x1: float, y: float, x2: float, color: str) -> str:
    return (
        f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" '
        f'stroke="{color}" stroke-width="1.5"/>'
    )


def render() -> str:
    # Both rectangles share their left and lower edges. The resulting right-hand
    # strip makes the small laukika-only extension visible without exaggerating it.
    x = 60
    bottom = 780
    vaidika_w = 1000
    vaidika_h = 600
    laukika_w = 1020
    laukika_h = 470
    vaidika_y = bottom - vaidika_h
    laukika_y = bottom - laukika_h
    right = x + laukika_w
    overlap_w = vaidika_w
    overlap_h = laukika_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{PAPER}"/>',
        text(54, 68, "One Sanskrit Architecture, Two Domains", size=47, weight=600),
        text(
            54,
            111,
            "A large shared engine with smaller domain-specific extensions",
            size=25,
            color=MUTED,
            italic=True,
        ),
        # Base fills are drawn separately so the overlap has a deliberate color.
        f'<rect x="{x}" y="{vaidika_y}" width="{vaidika_w}" height="{vaidika_h}" '
        f'fill="{GOLD_LIGHT}" stroke="{GOLD}" stroke-width="4"/>',
        f'<rect x="{x}" y="{laukika_y}" width="{laukika_w}" height="{laukika_h}" '
        f'fill="{SAGE}" stroke="{SAGE_DARK}" stroke-width="4"/>',
        f'<rect x="{x + 2}" y="{laukika_y + 2}" width="{overlap_w - 4}" '
        f'height="{overlap_h - 4}" fill="{BLEND}"/>',
        # Restore the visible boundaries after painting the overlap.
        f'<rect x="{x}" y="{vaidika_y}" width="{vaidika_w}" height="{vaidika_h}" '
        f'fill="none" stroke="{GOLD}" stroke-width="4"/>',
        f'<rect x="{x}" y="{laukika_y}" width="{laukika_w}" height="{laukika_h}" '
        f'fill="none" stroke="{SAGE_DARK}" stroke-width="4"/>',
    ]

    # Vaidika-only upper extension.
    parts.extend(
        [
            text(
                x + vaidika_w / 2,
                vaidika_y + 34,
                "वैदिक · vaidika",
                size=31,
                weight=600,
                anchor="middle",
                family=DEVA,
            ),
            text(
                x + vaidika_w / 2,
                vaidika_y + 66,
                "Vaidika Only",
                size=25,
                color=GOLD,
                weight=600,
                anchor="middle",
            ),
            text(
                x + vaidika_w / 2,
                vaidika_y + 92,
                "pitch · leṭ · additional endings",
                size=27,
                color=MUTED,
                anchor="middle",
            ),
            text(
                x + vaidika_w / 2,
                vaidika_y + 118,
                "contextual sounds · movable upasargāḥ",
                size=27,
                color=MUTED,
                anchor="middle",
            ),
        ]
    )

    # Shared architecture.
    shared_cx = x + overlap_w / 2
    parts.extend(
        [
            text(
                shared_cx,
                laukika_y + 46,
                "वैदिक + लौकिक · vaidika + laukika",
                size=30,
                weight=600,
                anchor="middle",
                family=DEVA,
            ),
            text(
                shared_cx,
                laukika_y + 88,
                "Shared Sanskrit Architecture",
                size=40,
                weight=600,
                anchor="middle",
            ),
            text(
                shared_cx,
                laukika_y + 124,
                "Most of both domains",
                size=28,
                color=MUTED,
                italic=True,
                anchor="middle",
            ),
            rule(x + 58, laukika_y + 151, x + overlap_w - 58, GOLD),
        ]
    )

    left_x = x + 145
    right_x = x + 585
    row_y = laukika_y + 204
    rows = [
        ("Sonomers and svaras", "Dhātavaḥ"),
        ("Upasarga · pratyaya", "Vibhakti · liṅga · vacana"),
        ("Shared lakāras", "Sandhi"),
        ("Samāsa", "Sentence architecture"),
    ]
    for index, (left, right_label) in enumerate(rows):
        y = row_y + index * 58
        parts.extend(
            [
                f'<circle cx="{left_x - 22}" cy="{y - 7}" r="5" fill="{GOLD}"/>',
                text(left_x, y, left, size=34, weight=500),
                f'<circle cx="{right_x - 22}" cy="{y - 7}" r="5" fill="{GOLD}"/>',
                text(right_x, y, right_label, size=34, weight=500),
            ]
        )

    # The laukika-only strip remains unlabelled; the leader line names it outside.
    extension_cy = laukika_y + laukika_h / 2

    # Explanatory copy sits outside the geometry so it does not enlarge the domain.
    callout_x = right + 45
    callout_y = laukika_y + 76
    parts.extend(
        [
            f'<path d="M {right} {extension_cy} H {callout_x - 28} V {callout_y + 7}" '
            f'fill="none" stroke="{GRID}" stroke-width="2"/>',
            text(
                callout_x,
                callout_y,
                "Laukika-only extension",
                size=27,
                color=SAGE_DARK,
                weight=600,
            ),
            rule(callout_x, callout_y + 20, WIDTH - 54, SAGE_DARK),
            text(
                callout_x,
                callout_y + 67,
                "bhāṣāyām-specific forms",
                size=24,
                color=MUTED,
                italic=True,
            ),
            text(
                callout_x,
                callout_y + 135,
                "niṣaṇṇa · sṛtā",
                size=26,
                color=MUTED,
            ),
            text(
                callout_x,
                callout_y + 177,
                "suṣuve · soḍhvā",
                size=26,
                color=MUTED,
            ),
            text(
                callout_x,
                callout_y + 219,
                "upasedivān",
                size=26,
                color=MUTED,
            ),
        ]
    )

    parts.extend(
        [
            f'<rect x="54" y="{HEIGHT - 70}" width="{WIDTH - 108}" height="52" fill="{INK}"/>',
            text(
                WIDTH / 2,
                HEIGHT - 36,
                "The shared architecture dominates both domains.",
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

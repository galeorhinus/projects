#!/usr/bin/env python3
"""matra_tiles.py — Chandas mātrā-tile figures for Chapter 14 §14.4.

Visualizes the laghu / guru filling of a fixed metrical measure using the
book's hex-tile grammar (Ch 10/11/12):

    L (laghu) = 1-mātrā tile  → a V1-width hexagon (flat top = EDGE_LENGTH)
    G (guru)  = 2-mātrā tile  → a V2-width hexagon (flat top = 2·EDGE_LENGTH)

The tiles interlock through the constant slanted edge the way every other
hexagon figure in the book does, so a strip's flat-top span is *exactly* its
total mātrā count. For a given measure of n mātrās the script lays out every
valid filling (the Virahāṅka / Hemachandra count — 1, 2, 3, 5, 8, 13 …),
left-aligned to a shared measure, with one half-mātrā ruler beneath the stack
so the eye reads "different tilings, same measure."

Usage:
    python3 figures/calibration/matra_tiles.py            # n = 4 and 5 (the §14.4 cases)
    python3 figures/calibration/matra_tiles.py 4 5 6      # any measures

Output: figures/calibration/matra_tiles_<n>.svg
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(REPO_ROOT / "working" / "dhatu_hexagons"))
from dhatu_hexagon import EDGE_LENGTH, HEX_HEIGHT  # noqa: E402

# --- Geometry --------------------------------------------------------------

MATRA_PX = EDGE_LENGTH          # px of flat-top width per mātrā (V1 = 1, V2 = 2)
SLANT = EDGE_LENGTH / 2         # horizontal projection of each slanted edge

# --- Palette / type --------------------------------------------------------

LAGHU_FILL = "#dcdcdc"          # light gray — the lighter weight
GURU_FILL = "#aaaaaa"           # medium gray — the heavier weight
STROKE = "#333333"
TEXT = "#1a1a1a"
MUTED = "#555555"
RULER = "#888888"
GUIDE = "#c8c8c8"

DEV_FONT = "Noto Sans Devanagari, Mangal, Devanagari Sangam MN, sans-serif"
LATIN_FONT = "Charter, Georgia, Times, serif"

# --- Layout ----------------------------------------------------------------

MARGIN = 28
TITLE_H = 64
LEFT_LABEL_W = 78               # room for the "GLL" letter string on the left
STRIP_X = MARGIN + LEFT_LABEL_W
ROW_GAP = 30                    # vertical gap between hex strips
RIGHT_LABEL_GAP = 22            # gap from strip end to the arithmetic label
RIGHT_LABEL_W = 96
RULER_GAP = 18                  # gap from the lowest strip to the shared ruler


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x: float, y: float, content: str, size: float, *, fill: str = TEXT,
         anchor: str = "middle", weight: str = "400", style: str = "normal",
         family: str = LATIN_FONT, halo: float = 0.0) -> str:
    # halo > 0 paints a white outline behind the glyph so it reads over the
    # interlocking tile seams.
    halo_attr = (
        f'paint-order="stroke" stroke="#ffffff" stroke-width="{halo}" '
        f'stroke-linejoin="round" ' if halo else ""
    )
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" font-style="{style}" text-anchor="{anchor}" '
        f'dominant-baseline="middle" {halo_attr}fill="{fill}">{esc(content)}</text>'
    )


def hex_vertices(cx: float, cy: float, w: float) -> str:
    """Flat-top hexagon of flat-width w, slant projection SLANT each side."""
    h = HEX_HEIGHT
    pts = [
        (cx - w / 2, cy - h / 2),
        (cx + w / 2, cy - h / 2),
        (cx + w / 2 + SLANT, cy),
        (cx + w / 2, cy + h / 2),
        (cx - w / 2, cy + h / 2),
        (cx - w / 2 - SLANT, cy),
    ]
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


# --- Combinatorics ---------------------------------------------------------

def fillings(n: int) -> list[list[str]]:
    """Every laghu/guru filling of an n-mātrā measure.

    Ordered to match §14.4: most gurus first, then by position.
    """
    out: list[list[str]] = []

    def rec(rem: int, acc: list[str]) -> None:
        if rem == 0:
            out.append(acc[:])
            return
        if rem >= 1:
            acc.append("L")
            rec(rem - 1, acc)
            acc.pop()
        if rem >= 2:
            acc.append("G")
            rec(rem - 2, acc)
            acc.pop()

    rec(n, [])
    out.sort(key=lambda p: (-p.count("G"), "".join(p)))  # 'G' < 'L' sorts as in §14.4
    return out


def matra_of(token: str) -> int:
    return 2 if token == "G" else 1


def arithmetic(tokens: list[str]) -> str:
    return " + ".join(str(matra_of(t)) for t in tokens)


# --- Rendering -------------------------------------------------------------

def render_strip(tokens: list[str], x_flat_left: float, cy: float) -> str:
    """One metrical line as an interlocking L/G hex strip.

    x_flat_left = x of the first tile's top-left flat corner; flat tops abut,
    slant points interlock, so the strip's flat span = total mātrās × MATRA_PX.
    """
    # Two passes: tiles interlock (slant points overlap), so every polygon is
    # laid first and the labels go on top — otherwise a tile clips its
    # neighbour's letter.
    polys: list[str] = []
    labels: list[str] = []
    cursor = x_flat_left
    for t in tokens:
        w = matra_of(t) * MATRA_PX
        cx = cursor + w / 2
        fill = GURU_FILL if t == "G" else LAGHU_FILL
        polys.append(
            f'<polygon points="{hex_vertices(cx, cy, w)}" fill="{fill}" '
            f'stroke="{STROKE}" stroke-width="1.5" stroke-linejoin="round"/>'
        )
        labels.append(text(cx, cy - 5, t, 24, weight="700", halo=4.0))
        labels.append(text(cx, cy + 17, f"{matra_of(t)}", 11, fill=MUTED, style="italic", halo=3.0))
        cursor += w
    return "\n  ".join(polys + labels)


def render_ruler(x_flat_left: float, y: float, n: int) -> str:
    """Half-mātrā ruler (Ch 10/11 style) spanning the shared measure."""
    end_x = x_flat_left + n * MATRA_PX
    frags = [
        f'<line x1="{x_flat_left:.1f}" y1="{y:.1f}" x2="{end_x:.1f}" y2="{y:.1f}" '
        f'stroke="{RULER}" stroke-width="1.2"/>'
    ]
    for i in range(n * 2 + 1):
        x = x_flat_left + i * MATRA_PX / 2
        major = i % 2 == 0
        tick = 8 if major else 4
        frags.append(
            f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y - tick:.1f}" '
            f'stroke="{RULER}" stroke-width="{1.2 if major else 1.0}"/>'
        )
        if major:
            frags.append(text(x, y + 14, f"{i // 2}", 10, fill=MUTED))
    frags.append(text((x_flat_left + end_x) / 2, y + 30, "mātrā", 11, fill=MUTED, style="italic"))
    return "\n  ".join(frags)


def build(n: int) -> tuple[str, float, float]:
    rows = fillings(n)
    row_h = HEX_HEIGHT + ROW_GAP
    end_x = STRIP_X + n * MATRA_PX

    frags: list[str] = []

    # Title.
    count = len(rows)
    measure_word = {4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}.get(n, str(n))
    frags.append(text(MARGIN, 26, f"{measure_word} mātrās — {count} patterns",
                      20, anchor="start", weight="700"))
    frags.append(text(MARGIN, 48,
                      "L (laghu) = 1 mātrā   ·   G (guru) = 2 mātrās",
                      12, fill=MUTED, anchor="start", style="italic"))

    top = TITLE_H + HEX_HEIGHT / 2
    # Measure-boundary guides spanning the whole stack.
    stack_bottom = top + (count - 1) * row_h + HEX_HEIGHT / 2
    for gx in (STRIP_X, end_x):
        frags.append(
            f'<line x1="{gx:.1f}" y1="{TITLE_H + 4:.1f}" x2="{gx:.1f}" '
            f'y2="{stack_bottom + RULER_GAP:.1f}" stroke="{GUIDE}" '
            f'stroke-width="1" stroke-dasharray="3,4"/>'
        )

    for idx, tokens in enumerate(rows):
        cy = top + idx * row_h
        # Left: the L/G letter string.
        frags.append(text(MARGIN, cy, "".join(tokens), 18, anchor="start",
                          weight="600", family=LATIN_FONT))
        # The strip.
        frags.append(render_strip(tokens, STRIP_X, cy))
        # Right: the arithmetic.
        frags.append(text(end_x + RIGHT_LABEL_GAP, cy, arithmetic(tokens), 14,
                          fill=MUTED, anchor="start", style="italic"))

    # Shared ruler under the stack.
    ruler_y = stack_bottom + RULER_GAP
    frags.append(render_ruler(STRIP_X, ruler_y, n))

    width = end_x + RIGHT_LABEL_GAP + RIGHT_LABEL_W + MARGIN
    height = ruler_y + 44
    return "\n  ".join(frags), width, height


def write_svg(n: int) -> None:
    body, width, height = build(n)
    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" '
        f'height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">\n'
        f'<title>Chandas mātrā tiles — {n} mātrās</title>\n'
        '<rect width="100%" height="100%" fill="white"/>\n'
        f'{body}\n</svg>\n'
    )
    out = BUILD_DIR / f"matra_tiles_{n}.svg"
    out.write_text(doc, encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO_ROOT)}  ({len(fillings(n))} patterns)")


def main() -> None:
    args = sys.argv[1:]
    measures = [int(a) for a in args] if args else [4, 5]
    for n in measures:
        write_svg(n)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""matra_envelope.py — ten dhātu hexagon strips across the mātrā envelope
(1 → 5½ mātrās), in the shared calibration-style hex grammar.

Style (colours, ruler, gridlines, SVG, fonts) comes from
figures/_shared/matra_style.py — the single source of truth, so a palette change
there updates this figure too. Varṇa data (Devanagari, IAST, class) comes from
working/50_projects/dhatu_hexagons/dhatu_hexagon.py.

Geometry uses the ruler-aligned convention (width = mātrā·unit − slant), so the
per-column mātrā ruler and the dashed gridlines line up with the tiles.

5-row × 2-column grid: left column 1–3 mātrās, right column 3½–5½ mātrās. Each
column carries its own gridlines (behind the hexes) and a bottom ruler.

Output: figures/build/matra_envelope.from-py.svg
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "working" / "dhatu_hexagons"))
sys.path.insert(0, str(REPO_ROOT / "figures" / "_shared"))

import matra_style as ms  # noqa: E402
from dhatu_hexagon import (  # noqa: E402
    EDGE_LENGTH as EDGE_BASE,
    HEX_HEIGHT as HEX_BASE,
    VARNAS,
    devanagari_label,
    parse_dhatu_string,
)

# --- Geometry (ruler-aligned convention, scaled down like matra_tiles) ------

TILE_SCALE = 0.5
EDGE = EDGE_BASE * TILE_SCALE
HEX_HEIGHT = HEX_BASE * TILE_SCALE
SLANT = EDGE / 2
MATRA_UNIT = 72 * TILE_SCALE              # px per mātrā
UPPER_RAIL = -HEX_HEIGHT / 4              # consonant rail
LOWER_RAIL = HEX_HEIGHT / 4              # vowel rail

# --- Fonts (px; tuned after measuring so labels print 9–11 pt at 4.5 in) ----

# px sizes ≈ pt × (canvas_w / 324); canvas_w ≈ 384 → ×1.185. Targets 9–11 pt.
FS_DEV = 11.9          # varṇa Devanagari in the hexes (≈10 pt)
FS_IAST = 10.7         # varṇa IAST sub-label (≈9 pt)
FS_LABEL = 13.0        # cell label, mātrā · dhātu (≈11 pt)
FS_RULER = 11.9        # ruler numbers (≈10 pt)
FS_AXIS = 11.9         # "mātrā" axis label (≈10 pt)

# --- Layout ----------------------------------------------------------------

MARGIN = 16
COL_GAP = 26
LABEL_DY = 30          # label baseline above the strip midline
ROW_GAP = 30           # gap between rows
RULER_GAP = 22

PIPE = None            # (unused here; envelope shows varṇa letters, not pipes)

# (mātrā, devanagari, IAST, particle-string)
DHATUS = [
    ("1",  "ऋ",      "ṛ",     "R"),
    ("1½", "कृ",     "kṛ",    "k,R"),
    ("2",  "गम्",    "gam",   "g,a,m"),
    ("2½", "धा",     "dhā",   "dh,A"),
    ("3",  "वाच्",   "vāc",   "v,A,c"),
    ("3½", "स्वाद्", "svād",  "s,v,A,d"),
    ("4",  "बाधृ",   "bādhṛ", "b,A,dh,R"),
    ("4½", "कुमार्", "kumār", "k,u,m,A,r"),
    ("5",  "दीपी",   "dīpī",  "d,I,p,I"),
    ("5½", "ह्लादी", "hlādī", "h,l,A,d,I"),
]


def matra_of(cls: str) -> float:
    return {"C": 0.5, "V1": 1.0, "V2": 2.0}.get(cls, 1.0)


def units_of(dhatu_str: str) -> list[dict]:
    """Parse a dhātu string into display units, grouping consonant runs into a
    single split cluster tile (each vyañjana keeps its half-mātrā)."""
    particles = parse_dhatu_string(dhatu_str)
    units, i = [], 0
    while i < len(particles):
        cur = particles[i]
        if cur["class"] == "C":
            run = [cur]
            j = i + 1
            while j < len(particles) and particles[j]["class"] == "C":
                run.append(particles[j]); j += 1
            units.append({"kind": "cluster" if len(run) > 1 else "C",
                          "parts": run, "matra": 0.5 * len(run)})
            i = j
            continue
        units.append({"kind": cur["class"], "parts": [cur], "matra": matra_of(cur["class"])})
        i += 1
    return units


def layout(units: list[dict]) -> list[dict]:
    """Staggered positions: consonant/cluster on the upper rail, vowel on the
    lower rail (they alternate, so every gap is one slant → ruler aligns)."""
    out = []
    for i, u in enumerate(units):
        w = ms.matra_width(u["matra"], matra_unit=MATRA_UNIT, slant=SLANT)
        cy = LOWER_RAIL if u["kind"].startswith("V") else UPPER_RAIL
        if i == 0:
            cx = 0.0
        else:
            prev = out[-1]
            cx = prev["cx"] + (prev["w"] + w) / 2 + SLANT
        out.append({**u, "cx": cx, "cy": cy, "w": w})
    return out


def render_tile(u: dict, cx: float, cy: float) -> str:
    """One varṇa hex (or split cluster) with Devanagari + IAST labels."""
    is_vowel = u["kind"].startswith("V")
    fill = ms.LIGHT_FILL if is_vowel else ms.DARK_FILL
    ink = ms.INK_DARK if is_vowel else ms.INK_LIGHT
    w = u["w"]
    parts = [
        f'<polygon points="{ms.hex_points(cx, cy, w, slant=SLANT, hex_height=HEX_HEIGHT)}" '
        f'fill="{fill}" stroke="{ms.STROKE}" stroke-width="{ms.STROKE_W}" stroke-linejoin="round"/>'
    ]
    n = len(u["parts"])
    sub_w = w / n
    for k in range(1, n):                       # cluster dividers
        dx = cx - w / 2 + k * sub_w
        parts.append(
            f'<line x1="{dx:.1f}" y1="{cy - HEX_HEIGHT / 2 + 5:.1f}" '
            f'x2="{dx:.1f}" y2="{cy + HEX_HEIGHT / 2 - 5:.1f}" '
            f'stroke="{ink}" stroke-width="0.8" stroke-linecap="round" opacity="0.5"/>'
        )
    for k, p in enumerate(u["parts"]):
        lx = cx - w / 2 + sub_w * (k + 0.5)
        parts.append(ms.varna_label(lx, cy, devanagari_label(p), p["iast"],
                                    ink=ink, fs_dev=FS_DEV, fs_iast=FS_IAST))
    return "\n  ".join(parts)


def render_strip(units, measure_x, row_cy):
    lay = layout(units)
    first = lay[0]
    dx = measure_x - (first["cx"] - first["w"] / 2 - SLANT / 2)
    return "\n  ".join(render_tile(u, u["cx"] + dx, u["cy"] + row_cy) for u in lay)


def main() -> None:
    n_rows = (len(DHATUS) + 1) // 2
    cols = [DHATUS[:n_rows], DHATUS[n_rows:]]
    col_maxn = [3.0, 5.5]                       # max mātrā per column

    # x: each column left-aligned to its own mātrā-0.
    measure_x, x = [], MARGIN
    for mx in col_maxn:
        measure_x.append(x + SLANT / 2)
        x += mx * MATRA_UNIT + SLANT + COL_GAP
    canvas_w = measure_x[-1] + col_maxn[-1] * MATRA_UNIT + SLANT / 2 + MARGIN

    strip_half = 3 * HEX_HEIGHT / 4
    row_pitch = 2 * strip_half + ROW_GAP
    top = MARGIN + 6
    row_cy0 = top + LABEL_DY + strip_half
    ruler_y = row_cy0 + (n_rows - 1) * row_pitch + strip_half + RULER_GAP
    canvas_h = ruler_y + 46

    grids, strips, chrome = [], [], []
    for c, (column, mx, maxn) in enumerate(zip(cols, measure_x, col_maxn)):
        grids.append(ms.gridlines(mx, math.floor(maxn), top, ruler_y, matra_unit=MATRA_UNIT))
        for r, (matra, deva, iast, dstr) in enumerate(column):
            cy = row_cy0 + r * row_pitch
            chrome.append(ms.text(mx - SLANT / 2, cy - strip_half - 12,
                                  f"{matra} mātrā · {deva} — {iast}", FS_LABEL,
                                  fill=ms.TEXT, anchor="start", family=ms.DEV_FONT))
            strips.append(render_strip(units_of(dstr), mx, cy))
        chrome.append(ms.render_ruler(mx, ruler_y, maxn, matra_unit=MATRA_UNIT,
                                      fs_num=FS_RULER, fs_label=FS_AXIS))

    body = "\n".join(grids + strips + chrome)
    out = REPO_ROOT / "figures" / "build" / "matra_envelope.from-py.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(ms.svg(canvas_w, canvas_h, body,
                          title="Mātrā envelope across ten dhātavaḥ"), encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO_ROOT)}  ({canvas_w:.0f}x{canvas_h:.0f}px = "
          f"{ms.WIDTH_IN}in x {canvas_h / canvas_w * ms.WIDTH_IN:.2f}in)")


if __name__ == "__main__":
    main()

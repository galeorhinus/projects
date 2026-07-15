#!/usr/bin/env python3
"""Starting-point icon for the ENGINEERED behavior (four-language-behaviors set).
Abstract dhātu-molecule shape in the book's hex language — no glyphs:

    [ 1-mātrā hex · HIGH ]  [ 0.5-mātrā hex · LOW ]  [ 1-mātrā hex · HIGH ]

Staggered on alternating rails (the dhātu convention — interlocking honeycomb),
warm matra_style palette, vakya_figures geometry. Hand-off to Claude Design as a
starting point; refine into a clean icon.
"""
import sys
from pathlib import Path
REPO = Path("/Users/paragtope/projects/writing/books/atomicSanskrit")
sys.path.insert(0, str(REPO / "figures" / "building_vakya"))
sys.path.insert(0, str(REPO / "figures" / "_shared"))
sys.path.insert(0, str(REPO / "working" / "dhatu_hexagons"))
import vakya_figures as vf
import matra_style as ms

# (width, rail):  1-mātrā = WIDTH_V1 ; 0.5-mātrā = WIDTH_C ; high = UPPER, low = LOWER
specs = [
    (vf.WIDTH_V1, vf.UPPER_RAIL_Y),   # 1-mātrā, high
    (vf.WIDTH_C,  vf.LOWER_RAIL_Y),   # 0.5-mātrā, low
    (vf.WIDTH_V1, vf.UPPER_RAIL_Y),   # 1-mātrā, high
]
e, h = vf.EDGE_LENGTH, vf.HEX_HEIGHT

placed = []
for i, (w, cy) in enumerate(specs):
    if i == 0:
        cx = 0.0
    else:                                     # different-rail neighbours interlock at e/2
        pw = specs[i - 1][0]
        cx = placed[-1]["cx"] + (pw + w) / 2 + e / 2
    placed.append({"cx": cx, "cy": cy, "w": w})

xs, ys = [], []
for u in placed:
    xs += [u["cx"] - u["w"] / 2 - e / 2, u["cx"] + u["w"] / 2 + e / 2]
    ys += [u["cy"] - h / 2, u["cy"] + h / 2]
mnx, mxx, mny, mxy = min(xs), max(xs), min(ys), max(ys)
pad = 16
W, H = (mxx - mnx) + 2 * pad, (mxy - mny) + 2 * pad
dx, dy = -mnx + pad, -mny + pad

def hexonly(cx, cy, w):
    return (f'<polygon points="{vf.points(vf.hex_vertices(cx, cy, w))}" fill="{ms.LIGHT_FILL}" '
            f'stroke="{ms.STROKE}" stroke-width="2" stroke-linejoin="round"/>')

body = [hexonly(u["cx"] + dx, u["cy"] + dy, u["w"]) for u in placed]
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
       f'width="{W:.0f}" height="{H:.0f}">\n' + "\n".join(body) + "\n</svg>\n")

dst = REPO / "figures" / "_shared" / "icons" / "ic-engineered.from-py.svg"
dst.write_text(svg, encoding="utf-8")
print("wrote", dst, f"({W:.0f}x{H:.0f})")

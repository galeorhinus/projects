#!/usr/bin/env python3
"""Render the Ch11 racanā × gaṇa matrix as a dependency-free SVG heatmap.

Designed for the 4.5in trade text block: the viewBox is ~500 px wide so every
font lands in the 8–11 pt band at that width. Gaṇa column headers are angled so
they can carry the row-label font size without overflowing the narrow columns.
"""

from __future__ import annotations

import csv
import html
import math
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_IN = PROJECT_ROOT / "analysis" / "dhatupatha" / "data" / "derived" / "racana_by_gana.csv"
SVG_OUT = Path(__file__).resolve().parent / "racana_gana_matrix.from-py.svg"
ICON_DIR = PROJECT_ROOT / "figures" / "_shared" / "icons"

sys.path.insert(0, str(PROJECT_ROOT / "figures" / "_shared"))
import matra_style as ms  # noqa: E402

WIDTH_IN = 4.5
SCAFFOLD_FILL = ms.GOLD          # warm colour for the scaffold icons

TOP_TEN = [
    ("CV1C", "gamādi", "scaffold_cv1c_gray.svg"),
    ("CCV1C", "spadādi", "scaffold_ccv1c_gray.svg"),
    ("CV1CC", "manthādi", "scaffold_cv1cc_gray.svg"),
    ("CV2C", "vācādi", "scaffold_cv2c_gray.svg"),
    ("CV2", "dhādi", "scaffold_cv2_gray.svg"),
    ("V1C", "iṣādi", "scaffold_v1c_gray.svg"),
    ("CCV2C", "hrādādi", "scaffold_ccv2c_gray.svg"),
    ("CV1", "krādi", "scaffold_cv1_gray.svg"),
    ("CCV2", "sthādi", "scaffold_ccv2_gray.svg"),
    ("CCV1CC", "spardhādi", "scaffold_ccv1cc_gray.svg"),
]

GANA_NAMES = {
    "1": "bhvādi", "2": "adādi", "3": "juhotyādi", "4": "divādi", "5": "svādi",
    "6": "tudādi", "7": "rudhādi", "8": "tanādi", "9": "kryādi", "10": "curādi",
}


def esc(s: object) -> str:
    return html.escape(str(s), quote=True)


def read_matrix():
    rows, totals = {}, {}
    with CSV_IN.open() as fh:
        for row in csv.DictReader(fh):
            racana = row["racana"]
            if racana == "TOTAL":
                totals = {str(i): int(row[str(i)]) for i in range(1, 11)}
                continue
            rows[racana] = {str(i): int(row[str(i)]) for i in range(1, 11)}
            rows[racana]["row_total"] = int(row["row_total"])
    sorted_ganas = sorted(totals, key=lambda g: -totals[g])
    return rows, totals, sorted_ganas


def shade(value: int, max_value: int) -> str:
    if value <= 0:
        return "#f7f7f7"
    t = math.log(value + 1) / math.log(max_value + 1)
    v = int(245 - t * 185)
    return f"#{v:02x}{v:02x}{v:02x}"


def text_color(value: int, max_value: int) -> str:
    """White on medium-gray-and-darker cells, dark ink otherwise."""
    if value <= 0:
        return "#9a9a9a"
    t = math.log(value + 1) / math.log(max_value + 1)
    v = 245 - t * 185                              # the cell's gray value (see shade)
    return "#ffffff" if v < 140 else "#202020"     # invert on the cell's own darkness


def render_icon(icon_name: str, x: float, y: float, width: float, height: float,
                fill: str) -> str:
    root = ET.parse(ICON_DIR / icon_name).getroot()
    vx, vy, vw, vh = (float(p) for p in root.attrib["viewBox"].split())
    scale = min(width / vw, height / vh)
    cx, cy = x + width / 2, y + height / 2
    pieces = [
        f'<g transform="translate({cx:.1f} {cy:.1f}) scale({scale:.4f}) '
        f'translate({-(vx + vw / 2):.2f} {-(vy + vh / 2):.2f})">'
    ]
    for elem in root.iter():
        if elem.tag.endswith("polygon"):
            pieces.append(f'<polygon points="{esc(elem.attrib.get("points", ""))}" fill="{fill}"/>')
    pieces.append("</g>")
    return "\n".join(pieces)


def main() -> int:
    rows, totals, sorted_ganas = read_matrix()
    n = len(sorted_ganas)
    max_cell = max(rows[r][g] for r, _name, _icon in TOP_TEN for g in sorted_ganas)

    # --- layout (viewBox px; ~500 wide → 8–11 pt at 4.5 in) -----------------
    MARGIN = 12
    ICON_W, ICON_H = 36, 20
    LABEL_RIGHT = 126                # row labels right-justify here (tight to icon)
    LEFT = 138                       # cells start
    CELL_W, CELL_H = 28, 24
    COL_GAP, ROW_GAP = 2, 2
    TOTAL_GAP, TOTAL_W = 8, 40

    # Widen the two busiest columns (bhvādi, curādi) for their big 3-digit cells.
    col_scale = [1.2, 1.1] + [1.0] * (n - 2)
    col_w = [CELL_W * s for s in col_scale]
    col_x, x = [], LEFT
    for cw in col_w:
        col_x.append(x)
        x += cw + COL_GAP
    total_x = x - COL_GAP + TOTAL_GAP
    w = total_x + TOTAL_W + MARGIN

    # Fonts (px). pt = px * 324 / w  (≈ px * 0.64 at w≈505).
    fs_title, fs_sub = 16, 13
    fs_head, fs_row = 15, 15         # gaṇa headers == row labels
    fs_cell, fs_total = 14, 14

    title_y, sub_y = 16, 31          # title/subtitle near the top
    cells_top = 114                  # leaves room for the angled gaṇa headers
    cells_bottom = cells_top + n * (CELL_H + ROW_GAP)
    gtot_y = cells_bottom + 8
    h = gtot_y + CELL_H + MARGIN     # ends at the gaṇa-total row (no source note)

    P: list[str] = []
    P.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">')
    P.append(f"""
<style>
  text {{ font-family: Charter, "DejaVu Serif", serif; fill: #222; }}
  .title {{ font-size: {fs_title}px; font-weight: 700; }}
  .subtitle {{ font-size: {fs_sub}px; fill: #555; font-style: italic; }}
  .ghead {{ font-size: {fs_head}px; font-weight: 700; }}
  .rowlabel {{ font-size: {fs_row}px; font-weight: 700; text-anchor: end; }}
  .cell {{ font-size: {fs_cell}px; font-weight: 700; text-anchor: middle; dominant-baseline: central; }}
  .total {{ font-size: {fs_total}px; font-weight: 700; text-anchor: middle; dominant-baseline: central; }}
</style>
""")
    P.append(f'<rect x="0" y="0" width="100%" height="100%" fill="{ms.BG}"/>')
    P.append(f'<text x="{MARGIN}" y="{title_y}" class="title">Racanā × Gaṇa Matrix</text>')
    P.append(f'<text x="{MARGIN}" y="{sub_y}" class="subtitle">Top ten scaffolds across Pāṇini’s ten operational classes</text>')

    # --- angled column headers (gaṇa name · class number) -------------------
    def angled(text: str, cx: float) -> str:
        ay = cells_top - 4
        return (f'<text x="{cx:.1f}" y="{ay:.1f}" class="ghead" text-anchor="end" '
                f'transform="rotate(45 {cx:.1f} {ay:.1f})">{esc(text)}</text>')

    for j, gana in enumerate(sorted_ganas):
        cx = col_x[j] + col_w[j] / 2
        P.append(angled(f"{GANA_NAMES[gana]} · {gana}", cx))
    P.append(angled("total racanā", total_x + TOTAL_W / 2))

    # --- heatmap rows -------------------------------------------------------
    for i, (racana, name, icon_name) in enumerate(TOP_TEN):
        y = cells_top + i * (CELL_H + ROW_GAP)
        mid = y + CELL_H / 2
        P.append("  " + render_icon(icon_name, MARGIN, y + (CELL_H - ICON_H) / 2,
                                    ICON_W, ICON_H, SCAFFOLD_FILL))
        P.append(f'<text x="{LABEL_RIGHT}" y="{mid:.1f}" class="rowlabel" dominant-baseline="central">{esc(name)}</text>')

        for j, gana in enumerate(sorted_ganas):
            value = rows[racana][gana]
            x, cw = col_x[j], col_w[j]
            P.append(f'<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{CELL_H}" rx="2" '
                     f'fill="{shade(value, max_cell)}" stroke="#dddddd"/>')
            label = "—" if value == 0 else str(value)
            P.append(f'<text x="{x + cw / 2:.1f}" y="{mid:.1f}" class="cell" '
                     f'fill="{text_color(value, max_cell)}">{label}</text>')

        rt = rows[racana]["row_total"]
        P.append(f'<rect x="{total_x}" y="{y}" width="{TOTAL_W}" height="{CELL_H}" rx="2" '
                 f'fill="#eeeeee" stroke="#dddddd"/>')
        P.append(f'<text x="{total_x + TOTAL_W / 2:.1f}" y="{mid:.1f}" class="total">{rt}</text>')

    # --- gaṇa-total row -----------------------------------------------------
    gmid = gtot_y + CELL_H / 2
    P.append(f'<text x="{LABEL_RIGHT}" y="{gmid:.1f}" class="rowlabel" dominant-baseline="central">gaṇa total</text>')
    for j, gana in enumerate(sorted_ganas):
        x, cw = col_x[j], col_w[j]
        P.append(f'<rect x="{x:.1f}" y="{gtot_y}" width="{cw:.1f}" height="{CELL_H}" rx="2" '
                 f'fill="#eeeeee" stroke="#dddddd"/>')
        P.append(f'<text x="{x + cw / 2:.1f}" y="{gmid:.1f}" class="total">{totals[gana]}</text>')

    top10_total = sum(rows[r]["row_total"] for r, _n, _i in TOP_TEN)
    P.append(f'<rect x="{total_x}" y="{gtot_y}" width="{TOTAL_W}" height="{CELL_H}" rx="2" '
             f'fill="#dddddd" stroke="#cccccc"/>')
    P.append(f'<text x="{total_x + TOTAL_W / 2:.1f}" y="{gmid:.1f}" class="total">{top10_total}</text>')

    P.append("</svg>\n")

    SVG_OUT.write_text("\n".join(P), encoding="utf-8")
    print(f"Wrote {SVG_OUT.relative_to(PROJECT_ROOT)}  ({w}x{h}px = {WIDTH_IN}in x {h / w * WIDTH_IN:.2f}in)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

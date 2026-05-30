#!/usr/bin/env python3
"""Render the Ch11 racanā × gaṇa matrix as a dependency-free SVG heatmap."""

from __future__ import annotations

import csv
import html
import math
from pathlib import Path
from xml.etree import ElementTree as ET


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_IN = PROJECT_ROOT / "analysis" / "dhatupatha" / "data" / "derived" / "racana_by_gana.csv"
SVG_OUT = PROJECT_ROOT / "figures" / "build" / "ganah_racana_gana_matrix.svg"
ICON_DIR = PROJECT_ROOT / "figures" / "icons"

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
    "1": "bhvādi",
    "2": "adādi",
    "3": "juhotyādi",
    "4": "divādi",
    "5": "svādi",
    "6": "tudādi",
    "7": "rudhādi",
    "8": "tanādi",
    "9": "kryādi",
    "10": "curādi",
}


def esc(s: object) -> str:
    return html.escape(str(s), quote=True)


def read_matrix():
    rows = {}
    totals = {}
    with CSV_IN.open() as fh:
        reader = csv.DictReader(fh)
        for row in reader:
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
    # Log scale keeps the central corridor visible without blacking out one cell.
    t = math.log(value + 1) / math.log(max_value + 1)
    v = int(245 - t * 185)
    return f"#{v:02x}{v:02x}{v:02x}"


def text_color(value: int, max_value: int) -> str:
    if value <= 0:
        return "#888888"
    t = math.log(value + 1) / math.log(max_value + 1)
    return "#ffffff" if t > 0.58 else "#202020"


def render_icon(icon_name: str, x: float, y: float, width: float, height: float) -> str:
    root = ET.parse(ICON_DIR / icon_name).getroot()
    view_box = [float(part) for part in root.attrib["viewBox"].split()]
    vx, vy, vw, vh = view_box
    scale = min(width / vw, height / vh)
    cx = x + width / 2
    cy = y + height / 2
    vcx = vx + vw / 2
    vcy = vy + vh / 2
    pieces = [
        (
            f'<g transform="translate({cx:.1f} {cy:.1f}) scale({scale:.4f}) '
            f'translate({-vcx:.2f} {-vcy:.2f})">'
        )
    ]
    for elem in root.iter():
        if not elem.tag.endswith("polygon"):
            continue
        points = elem.attrib.get("points", "")
        fill = elem.attrib.get("fill", "#888888")
        pieces.append(f'<polygon points="{esc(points)}" fill="{esc(fill)}"/>')
    pieces.append("</g>")
    return "\n".join(pieces)


def main() -> int:
    rows, totals, sorted_ganas = read_matrix()
    max_cell = max(rows[r][g] for r, _name, _icon in TOP_TEN for g in sorted_ganas)

    left = 190
    top = 78
    cell_w = 66
    cell_h = 42
    row_gap = 2
    col_gap = 2
    label_w = left - 18
    total_w = 76
    total_gap = 12
    title_h = 54
    w = left + 10 * (cell_w + col_gap) + total_gap + total_w + 36
    h = top + 10 * (cell_h + row_gap) + title_h

    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}">'
    )
    parts.append("""
<style>
  text { font-family: Charter, "DejaVu Serif", serif; fill: #222; }
  .title { font-size: 22px; font-weight: 700; }
  .subtitle { font-size: 13px; fill: #555; font-style: italic; }
  .axis { font-size: 12px; font-weight: 700; }
  .small { font-size: 11px; fill: #555; }
  .rowlabel { font-size: 14px; font-weight: 700; }
  .cell { font-size: 13px; font-weight: 700; text-anchor: middle; dominant-baseline: central; }
  .total { font-size: 13px; font-weight: 700; text-anchor: middle; dominant-baseline: central; }
  .grid { stroke: #dddddd; stroke-width: 1; }
</style>
""")

    parts.append('<rect x="0" y="0" width="100%" height="100%" fill="#ffffff"/>')
    parts.append(f'<text x="24" y="30" class="title">Racanā × Gaṇa Matrix</text>')
    parts.append(
        "<text x=\"24\" y=\"51\" class=\"subtitle\">Top ten scaffolds across Pāṇini's ten operational classes</text>"
    )

    # Column labels.
    for j, gana in enumerate(sorted_ganas):
        x = left + j * (cell_w + col_gap) + cell_w / 2
        parts.append(
            f'<text x="{x:.1f}" y="{top - 28}" class="axis" text-anchor="middle">{esc(gana)}</text>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{top - 12}" class="small" text-anchor="middle">{esc(GANA_NAMES[gana])}</text>'
        )

    total_x = left + 10 * (cell_w + col_gap) + total_gap + total_w / 2
    parts.append(f'<text x="{total_x:.1f}" y="{top - 28}" class="axis" text-anchor="middle">total</text>')
    parts.append(f'<text x="{total_x:.1f}" y="{top - 12}" class="small" text-anchor="middle">racanā</text>')

    # Heatmap rows.
    for i, (racana, name, icon_name) in enumerate(TOP_TEN):
        y = top + i * (cell_h + row_gap)
        label_y = y + cell_h / 2 + 1
        parts.append("  " + render_icon(icon_name, 26, y + 7, 48, 28))
        parts.append(
            f'<text x="{label_w}" y="{label_y:.1f}" class="rowlabel" text-anchor="end">{esc(name)}</text>'
        )

        for j, gana in enumerate(sorted_ganas):
            value = rows[racana][gana]
            x = left + j * (cell_w + col_gap)
            fill = shade(value, max_cell)
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="2" '
                f'fill="{fill}" class="grid"/>'
            )
            label = "—" if value == 0 else str(value)
            parts.append(
                f'<text x="{x + cell_w / 2:.1f}" y="{y + cell_h / 2:.1f}" '
                f'class="cell" fill="{text_color(value, max_cell)}">{label}</text>'
            )

        # Row total.
        row_total = rows[racana]["row_total"]
        tx = left + 10 * (cell_w + col_gap) + total_gap
        parts.append(
            f'<rect x="{tx}" y="{y}" width="{total_w}" height="{cell_h}" rx="2" '
            f'fill="#eeeeee" stroke="#dddddd"/>'
        )
        parts.append(
            f'<text x="{tx + total_w / 2:.1f}" y="{y + cell_h / 2:.1f}" '
            f'class="total">{row_total}</text>'
        )

    # Column totals.
    y = top + 10 * (cell_h + row_gap) + 10
    parts.append(f'<text x="{label_w}" y="{y + 24}" class="axis" text-anchor="end">gaṇa total</text>')
    for j, gana in enumerate(sorted_ganas):
        x = left + j * (cell_w + col_gap)
        parts.append(
            f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="2" '
            f'fill="#eeeeee" stroke="#dddddd"/>'
        )
        parts.append(
            f'<text x="{x + cell_w / 2:.1f}" y="{y + cell_h / 2:.1f}" '
            f'class="total">{totals[gana]}</text>'
        )

    tx = left + 10 * (cell_w + col_gap) + total_gap
    top10_total = sum(rows[r]["row_total"] for r, _name, _icon in TOP_TEN)
    parts.append(
        f'<rect x="{tx}" y="{y}" width="{total_w}" height="{cell_h}" rx="2" '
        f'fill="#dddddd" stroke="#cccccc"/>'
    )
    parts.append(
        f'<text x="{tx + total_w / 2:.1f}" y="{y + cell_h / 2:.1f}" class="total">{top10_total}</text>'
    )

    parts.append(
        f'<text x="24" y="{h - 16}" class="small">Source: analysis/dhatupatha/data/derived/racana_by_gana.csv. '
        f'Top ten racanāḥ cover {top10_total}/2168 = 91.01% of the Dhātupāṭha inventory.</text>'
    )
    parts.append("</svg>\n")

    SVG_OUT.parent.mkdir(parents=True, exist_ok=True)
    SVG_OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {SVG_OUT.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

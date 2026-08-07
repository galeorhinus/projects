#!/usr/bin/env python3
"""Generate scaffold actual-use share figure as SVG/PDF.

Four 100% horizontal bars showing Top-10 vs Tail share across the four
measures the chapter reports (inventory, dhātavaḥ in use, measured bonds,
counted uses). The figure's only job is to make the headline claim
visually obvious: the top ten *racanā* scaffolds carry the inventory,
and the same concentration survives prayoga. The per-scaffold roster
already lives in the §10.6 table; the figure does not re-list it.

Script writes SVG directly instead of using matplotlib so the project
builds cleanly even when the local NumPy/matplotlib install is out of
sync.
"""

from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SUMMARY = PROJECT_ROOT / "analysis" / "ganah" / "data" / "derived" / "scaffold_reactivity_summary.csv"
OUT_DIR = Path(__file__).resolve().parent
OUT_SVG = OUT_DIR / "scaffold_deployment.from-py.svg"
OUT_PDF = OUT_DIR / "scaffold_deployment.from-py.pdf"

# Top-ten scaffolds — kept in sync with template_distribution.csv (post
# Pāṇinian-1.3.2 strict anubandha stripping). The chart aggregates these
# vs the tail rather than plotting each.
TOP_TEN = {
    "CV1C", "CCV1C", "CV1CC", "CV2C", "CV2",
    "V1C", "CCV2C", "CV1", "CCV2", "CCV1CC",
}

# (csv_key, row_label) — order top-to-bottom in the figure.
ROWS = [
    ("inventory_share_pct",              "Inventory"),
    ("text_visible_dhatu_share_pct",     "Dhātavaḥ in use"),
    ("valency_share_pct",                "Measured bonds"),
    ("token_share_pct",                  "Counted uses"),
]

TOP_FILL = "#222222"
TAIL_FILL = "#d8d8d8"
STROKE = "#111111"


def esc(text: object) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def load_data() -> list[tuple[str, float, float]]:
    """Return [(row_label, top_pct, tail_pct), ...] for the four rows."""
    if not SUMMARY.exists():
        raise SystemExit(f"missing input: {SUMMARY}")

    by_scaffold: dict[str, dict[str, float]] = {}
    with SUMMARY.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            by_scaffold[row["racana_scaffold"]] = {
                key: float(row[key]) for key, _label in ROWS
            }

    data: list[tuple[str, float, float]] = []
    for key, label in ROWS:
        top = sum(by_scaffold[s][key] for s in TOP_TEN if s in by_scaffold)
        tail = max(0.0, 100.0 - top)
        data.append((label, top, tail))
    return data


def render() -> str:
    data = load_data()

    # Layout
    width = 920
    height = 360
    margin_left = 200       # room for row labels (Dhātavaḥ in use is widest)
    margin_right = 32
    margin_top = 52
    margin_bottom = 56
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom
    bar_h = 42
    row_count = len(data)
    row_gap = plot_height / row_count

    font = "Charter, Adobe Devanagari, DejaVu Serif, serif"
    small_font = "font-size:13px;font-family:" + font
    row_font = "font-size:16px;font-family:" + font
    inbar_font = "font-size:15px;font-weight:bold;font-family:" + font
    tail_font = "font-size:14px;font-family:" + font
    legend_font = "font-size:13px;font-family:" + font

    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">'
    )
    parts.append('<rect x="0" y="0" width="100%" height="100%" fill="white"/>')

    # Legend at top
    legend_y = 24
    legend_x = margin_left
    swatch_w = 22
    swatch_h = 12
    parts.append(
        f'<rect x="{legend_x}" y="{legend_y - swatch_h + 2}" '
        f'width="{swatch_w}" height="{swatch_h}" fill="{TOP_FILL}" '
        f'stroke="{STROKE}" stroke-width="0.6"/>'
    )
    parts.append(
        f'<text x="{legend_x + swatch_w + 8}" y="{legend_y}" '
        f'style="{legend_font}">Top-10 scaffolds</text>'
    )
    legend_x2 = legend_x + 180
    parts.append(
        f'<rect x="{legend_x2}" y="{legend_y - swatch_h + 2}" '
        f'width="{swatch_w}" height="{swatch_h}" fill="{TAIL_FILL}" '
        f'stroke="{STROKE}" stroke-width="0.6"/>'
    )
    parts.append(
        f'<text x="{legend_x2 + swatch_w + 8}" y="{legend_y}" '
        f'style="{legend_font}">Long tail (59 other scaffolds)</text>'
    )

    # Bars
    for row_index, (label, top_pct, tail_pct) in enumerate(data):
        row_center = margin_top + row_index * row_gap + row_gap / 2
        y = row_center - bar_h / 2

        # Row label on the left
        parts.append(
            f'<text x="{margin_left - 16}" y="{row_center + 5:.1f}" '
            f'text-anchor="end" style="{row_font}">{esc(label)}</text>'
        )

        # Top-10 segment
        top_w = top_pct / 100.0 * plot_width
        parts.append(
            f'<rect x="{margin_left}" y="{y:.1f}" '
            f'width="{top_w:.2f}" height="{bar_h}" '
            f'fill="{TOP_FILL}" stroke="{STROKE}" stroke-width="0.6"/>'
        )

        # Tail segment
        tail_w = tail_pct / 100.0 * plot_width
        parts.append(
            f'<rect x="{margin_left + top_w:.2f}" y="{y:.1f}" '
            f'width="{tail_w:.2f}" height="{bar_h}" '
            f'fill="{TAIL_FILL}" stroke="{STROKE}" stroke-width="0.6"/>'
        )

        # In-bar top-10 label (white text on dark fill)
        top_label_x = margin_left + top_w / 2
        parts.append(
            f'<text x="{top_label_x:.1f}" y="{row_center + 5:.1f}" '
            f'text-anchor="middle" fill="white" style="{inbar_font}">'
            f'{top_pct:.1f}%</text>'
        )

        # Tail label (dark text on light fill, or just past the right edge
        # if the tail is very narrow)
        tail_label_x = margin_left + top_w + tail_w / 2
        if tail_w >= 60:
            parts.append(
                f'<text x="{tail_label_x:.1f}" y="{row_center + 5:.1f}" '
                f'text-anchor="middle" fill="#222222" style="{tail_font}">'
                f'{tail_pct:.1f}%</text>'
            )
        else:
            # Place tail % just past the right edge of the bar
            parts.append(
                f'<text x="{margin_left + plot_width + 6:.1f}" y="{row_center + 5:.1f}" '
                f'text-anchor="start" fill="#222222" style="{tail_font}">'
                f'{tail_pct:.1f}%</text>'
            )

    # X-axis label
    parts.append(
        f'<text x="{margin_left + plot_width / 2:.1f}" '
        f'y="{height - 18}" text-anchor="middle" style="{row_font}">'
        f'Share of total (%)</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    OUT_DIR.mkdir(exist_ok=True)
    OUT_SVG.write_text(render(), encoding="utf-8")
    print(f"Wrote {OUT_SVG.relative_to(PROJECT_ROOT)}")

    converter = shutil.which("rsvg-convert")
    if converter:
        subprocess.run(
            [converter, "-f", "pdf", "-o", str(OUT_PDF), str(OUT_SVG)],
            check=True,
        )
        print(f"Wrote {OUT_PDF.relative_to(PROJECT_ROOT)}")
    else:
        print("WARNING: rsvg-convert not found; PDF not written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

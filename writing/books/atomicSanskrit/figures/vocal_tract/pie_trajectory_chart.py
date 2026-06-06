#!/usr/bin/env python3
"""PIE reconstruction trajectory chart — Sanskrit + Tamil containment.

Single-figure deliverable for Ch 9 showing how the orthodoxy's PIE
reconstruction has DRIFTED AWAY from Sanskrit (and from Tamil) over
the 150 years of revision since Schleicher 1862.

Renders a grayscale bar chart with:
  - Filled gray bars   = Sanskrit ⊇ PIE
  - Outlined bars      = Tamil ⊇ PIE
  - 5 x-axis groups, one per milestone (1862 / 1897 / 1927 / 1973 / 2020)
  - y-axis 0–1, the coverage fraction
  - reference line at the 1862 Sanskrit value (the Schleicher baseline)

Run as a standalone script — pulls metric values from a hard-coded
table at the top of this file (regenerate by running the overlay
script's pairwise table).
"""
from __future__ import annotations

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Data — Sanskrit ⊇ PIE and Tamil ⊇ PIE coverage at each milestone.
# These match the metrics printed by vocal_tract_overlay.py against the
# scatter_pie_<year>.json configs as of commit 35adcda.
# ---------------------------------------------------------------------------

YEARS     = [1862, 1897, 1927, 1973, 2020]
THEORISTS = ["Schleicher", "Brugmann", "Standard", "Glottalic", "Modern"]
SK_VALS   = [0.81, 0.73, 0.64, 0.48, 0.64]
TA_VALS   = [0.56, 0.45, 0.40, 0.40, 0.40]

PALETTE = {
    "background":   "#f4f4f3",
    "data_fill":    "#2b2b2d",
    "data_stroke":  "#2b2b2d",
    "grid":         "#cdccc8",
    "grid_strong":  "#9a9892",
    "axis":         "#9a9892",
    "label":        "#2b2b2d",
    "baseline":     "#8f8d86",
}

FONT = "'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"


def _xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


def build_chart() -> str:
    W, H = 6.0, 4.4

    left_margin   = 0.65
    right_margin  = 0.30
    top_margin    = 0.65
    bottom_margin = 1.00

    plot_x0 = left_margin
    plot_y0 = top_margin
    plot_w  = W - left_margin - right_margin
    plot_h  = H - top_margin - bottom_margin

    n = len(YEARS)
    group_w        = plot_w / n
    bar_w          = 0.30
    gap_in_group   = 0.06

    body: list[str] = []

    # 1. Background
    body.append(
        f'  <rect x="0" y="0" width="{W:.4f}" height="{H:.4f}" '
        f'fill="{PALETTE["background"]}" />\n'
    )

    # 2. Title block
    body.append(
        f'  <text x="{W/2:.4f}" y="0.36" text-anchor="middle" '
        f'font-size="0.17" font-weight="bold" fill="{PALETTE["label"]}" '
        f'font-family="{FONT}">'
        f'Sanskrit ⊇ PIE — 150 years of revision</text>\n'
    )
    body.append(
        f'  <text x="{W/2:.4f}" y="0.55" text-anchor="middle" '
        f'font-size="0.115" fill="{PALETTE["grid_strong"]}" '
        f'font-family="{FONT}">'
        f'fraction of PIE phonemes contained in Sanskrit (filled) '
        f'and in Tamil (outlined)</text>\n'
    )

    # 3. Horizontal gridlines + y-axis tick labels
    def y_at(v: float) -> float:
        return plot_y0 + plot_h * (1.0 - v)

    for gv in [0.00, 0.25, 0.50, 0.75, 1.00]:
        yy = y_at(gv)
        body.append(
            f'  <line x1="{plot_x0:.4f}" y1="{yy:.4f}" '
            f'x2="{plot_x0 + plot_w:.4f}" y2="{yy:.4f}" '
            f'stroke="{PALETTE["grid"]}" stroke-width="0.006" />\n'
        )
        body.append(
            f'  <text x="{plot_x0 - 0.08:.4f}" y="{yy + 0.04:.4f}" '
            f'text-anchor="end" font-size="0.10" '
            f'fill="{PALETTE["grid_strong"]}" font-family="{FONT}">'
            f'{gv:.2f}</text>\n'
        )

    # 4. Reference baseline at Schleicher's value
    baseline_y = y_at(SK_VALS[0])
    body.append(
        f'  <line x1="{plot_x0:.4f}" y1="{baseline_y:.4f}" '
        f'x2="{plot_x0 + plot_w:.4f}" y2="{baseline_y:.4f}" '
        f'stroke="{PALETTE["baseline"]}" stroke-width="0.008" '
        f'stroke-dasharray="0.08 0.05" />\n'
    )
    body.append(
        f'  <text x="{plot_x0 + plot_w - 0.10:.4f}" '
        f'y="{baseline_y - 0.06:.4f}" text-anchor="end" '
        f'font-size="0.09" fill="{PALETTE["baseline"]}" font-style="italic" '
        f'font-family="{FONT}">'
        f'Schleicher baseline (0.81)</text>\n'
    )

    # 5. Bars + per-bar value labels + x-axis group labels
    for i, (year, name, sk_v, ta_v) in enumerate(
        zip(YEARS, THEORISTS, SK_VALS, TA_VALS)
    ):
        center_x = plot_x0 + (i + 0.5) * group_w
        sk_bar_x = center_x - bar_w - 0.5 * gap_in_group
        ta_bar_x = center_x + 0.5 * gap_in_group

        # Sanskrit (filled gray)
        sk_y = y_at(sk_v)
        sk_h = plot_y0 + plot_h - sk_y
        body.append(
            f'  <rect x="{sk_bar_x:.4f}" y="{sk_y:.4f}" '
            f'width="{bar_w:.4f}" height="{sk_h:.4f}" '
            f'fill="{PALETTE["data_fill"]}" />\n'
        )
        body.append(
            f'  <text x="{sk_bar_x + bar_w/2:.4f}" y="{sk_y - 0.07:.4f}" '
            f'text-anchor="middle" font-size="0.105" font-weight="bold" '
            f'fill="{PALETTE["data_fill"]}" font-family="{FONT}">'
            f'{sk_v:.2f}</text>\n'
        )

        # Tamil (outlined)
        ta_y = y_at(ta_v)
        ta_h = plot_y0 + plot_h - ta_y
        body.append(
            f'  <rect x="{ta_bar_x:.4f}" y="{ta_y:.4f}" '
            f'width="{bar_w:.4f}" height="{ta_h:.4f}" '
            f'fill="none" stroke="{PALETTE["data_stroke"]}" '
            f'stroke-width="0.014" />\n'
        )
        body.append(
            f'  <text x="{ta_bar_x + bar_w/2:.4f}" y="{ta_y - 0.07:.4f}" '
            f'text-anchor="middle" font-size="0.105" '
            f'fill="{PALETTE["data_fill"]}" font-family="{FONT}">'
            f'{ta_v:.2f}</text>\n'
        )

        # x-axis group label: year on line 1 (bold), theorist on line 2
        body.append(
            f'  <text x="{center_x:.4f}" '
            f'y="{plot_y0 + plot_h + 0.20:.4f}" text-anchor="middle" '
            f'font-size="0.115" font-weight="bold" '
            f'fill="{PALETTE["label"]}" font-family="{FONT}">{year}</text>\n'
        )
        body.append(
            f'  <text x="{center_x:.4f}" '
            f'y="{plot_y0 + plot_h + 0.36:.4f}" text-anchor="middle" '
            f'font-size="0.10" fill="{PALETTE["grid_strong"]}" '
            f'font-family="{FONT}">{_xml_escape(name)}</text>\n'
        )

    # 6. X-axis line
    body.append(
        f'  <line x1="{plot_x0:.4f}" y1="{plot_y0 + plot_h:.4f}" '
        f'x2="{plot_x0 + plot_w:.4f}" y2="{plot_y0 + plot_h:.4f}" '
        f'stroke="{PALETTE["axis"]}" stroke-width="0.012" />\n'
    )

    # 7. Y-axis label (rotated)
    y_axis_label_x = 0.20
    y_axis_label_y = plot_y0 + plot_h / 2
    body.append(
        f'  <text x="{y_axis_label_x:.4f}" y="{y_axis_label_y:.4f}" '
        f'text-anchor="middle" font-size="0.105" '
        f'fill="{PALETTE["grid_strong"]}" font-family="{FONT}" '
        f'transform="rotate(-90 {y_axis_label_x:.4f} {y_axis_label_y:.4f})">'
        f'coverage fraction (Sk⊇PIE or Ta⊇PIE)</text>\n'
    )

    # 8. Footer caption
    body.append(
        f'  <text x="{W/2:.4f}" y="{H - 0.18:.4f}" text-anchor="middle" '
        f'font-size="0.095" fill="{PALETTE["grid_strong"]}" font-style="italic" '
        f'font-family="{FONT}">'
        f'Sanskrit’s containment of the orthodoxy’s reconstructed PIE has DECLINED from 0.81 to 0.48–0.64 '
        f'across 150 years of philological revision.</text>\n'
    )

    # 9. Inline legend (top-right of plot area)
    legend_x = plot_x0 + plot_w - 1.30
    legend_y = plot_y0 + 0.04
    body.append(
        f'  <rect x="{legend_x:.4f}" y="{legend_y:.4f}" '
        f'width="0.14" height="0.14" fill="{PALETTE["data_fill"]}" />\n'
    )
    body.append(
        f'  <text x="{legend_x + 0.22:.4f}" y="{legend_y + 0.12:.4f}" '
        f'font-size="0.10" fill="{PALETTE["label"]}" font-family="{FONT}">'
        f'Sanskrit ⊇ PIE</text>\n'
    )
    body.append(
        f'  <rect x="{legend_x:.4f}" y="{legend_y + 0.22:.4f}" '
        f'width="0.14" height="0.14" fill="none" '
        f'stroke="{PALETTE["data_stroke"]}" stroke-width="0.014" />\n'
    )
    body.append(
        f'  <text x="{legend_x + 0.22:.4f}" y="{legend_y + 0.34:.4f}" '
        f'font-size="0.10" fill="{PALETTE["label"]}" font-family="{FONT}">'
        f'Tamil ⊇ PIE</text>\n'
    )

    svg = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n',
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{W:.4f}in" height="{H:.4f}in" '
        f'viewBox="0 0 {W:.4f} {H:.4f}">\n',
    ]
    svg.extend(body)
    svg.append('</svg>\n')
    return "".join(svg)


def main() -> int:
    svg = build_chart()
    out = (
        Path(__file__).resolve().parent.parent
        / "build" / "vocal_tract" / "pie_trajectory_bar_chart.svg"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    print(f"Wrote {out} ({len(svg)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

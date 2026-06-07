#!/usr/bin/env python3
"""PIE reconstruction trajectory — line chart + 3-lane historical timeline.

Single-figure deliverable for Ch 9 showing how the orthodoxy's
reconstructed PIE has moved AROUND Sanskrit over 150 years:

  - 1862 Schleicher: close to Sanskrit (Sk⊇PIE = 0.81)
  - 1973 Glottalic: farthest break          (Sk⊇PIE = 0.48)
  - 2020 Modern eclectic: Sanskrit-like reload (Sk⊇PIE = 0.64)

Top panel: line chart of Sk⊇PIE with five markers; Tamil ⊇ PIE
shown as a thin dotted control underneath.

Bottom panel: three horizontal lanes of event ticks sharing the
same time axis as the line chart, exposing the temporal context:

  Lane 1  PIE revisions (the same five milestones, callout below
          the line for direct alignment)
  Lane 2  Western / European intellectual context (Darwin's tree
          metaphor 1859; German unification 1871; Neogrammarian
          program 1878; Hittite enters IE 1915; post-WWII shift;
          PIE migrates into popular reference machinery)
  Lane 3  Indian / Sanskrit civilisational context (Independence
          1947; Saṃskṛta Bhāratī 1981; economic opening 1991;
          civilisational assertion 1998; BJP majority 2014;
          genetics + AIT debates 2019-20; Proto-style public-
          facing PIE relaunch 2025)

The lanes show context, not causation. PIE keeps changing inside
Western philology while Sanskrit reassertion moves on its own track.

Run as a standalone script — pulls metric values from the hard-coded
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

# Phase callouts attached to specific milestones.
PHASE_LABELS = {
    1862: "close to Sanskrit",
    1973: "farthest break",
    2020: "Sanskrit-like reload",
}

# Bottom-panel event lanes.  Each event is (year, short_label).

LANE_1_PIE = [
    (1862, "Schleicher"),
    (1897, "Brugmann"),
    (1927, "Standard / Hittite"),
    (1973, "Glottalic turn"),
    (2020, "Modern reload"),
]

LANE_2_WEST = [
    (1859, "Darwin · tree metaphor"),
    (1871, "German unification"),
    (1878, "Neogrammarian sound-law"),
    (1915, "Hittite enters IE"),
    (1945, "post-WWII shift"),
    (1995, "PIE → popular reference"),
]

LANE_3_INDIA = [
    (1947, "Independence"),
    (1981, "Saṃskṛta Bhāratī"),
    (1991, "economic opening"),
    (1998, "civilisational assertion"),
    (2014, "Hindu civilisational assertion"),
    (2019, "AIT / genetics debates"),
    (2025, "PIE relaunch (Proto)"),
]

# Time axis range — covers earliest event (1859) through 2025.
X_MIN = 1855
X_MAX = 2030

PALETTE = {
    "background":   "#f4f4f3",
    "data":         "#2b2b2d",
    "tamil":        "#8f8d86",
    "grid":         "#cdccc8",
    "grid_strong":  "#9a9892",
    "axis":         "#9a9892",
    "label":        "#2b2b2d",
    "phase":        "#6a6a6a",
    "lane_track":   "#cdccc8",
    "lane_pie":     "#2b2b2d",
    "lane_west":    "#5e5e60",
    "lane_india":   "#3a3a3c",
    "footer":       "#9a9892",
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
    W, H = 8.0, 5.6

    # Outer margins
    left_margin   = 1.05
    right_margin  = 0.35
    top_margin    = 0.78
    bottom_margin = 0.40

    plot_x0 = left_margin
    plot_w  = W - left_margin - right_margin

    # Line chart vertical extent
    chart_y0 = top_margin
    chart_h  = 1.55

    # Gap between line chart and timeline
    panel_gap = 0.42

    # Timeline (three lanes)
    lanes_y0 = chart_y0 + chart_h + panel_gap
    lane_h   = 0.62
    lane_gap = 0.10
    total_lane_h = 3 * lane_h + 2 * lane_gap

    footer_y = lanes_y0 + total_lane_h + 0.28

    def x_at(year: float) -> float:
        return plot_x0 + (year - X_MIN) / (X_MAX - X_MIN) * plot_w

    def y_at_val(v: float) -> float:
        return chart_y0 + chart_h * (1.0 - v)

    body: list[str] = []

    # ----- Background -----
    body.append(
        f'  <rect x="0" y="0" width="{W:.4f}" height="{H:.4f}" '
        f'fill="{PALETTE["background"]}" />\n'
    )

    # ----- Title + subtitle -----
    body.append(
        f'  <text x="{W/2:.4f}" y="0.38" text-anchor="middle" '
        f'font-size="0.20" font-weight="bold" fill="{PALETTE["label"]}" '
        f'font-family="{FONT}">'
        f'PIE Keeps Returning to Sanskrit</text>\n'
    )
    body.append(
        f'  <text x="{W/2:.4f}" y="0.62" text-anchor="middle" '
        f'font-size="0.115" fill="{PALETTE["grid_strong"]}" font-style="italic" '
        f'font-family="{FONT}">'
        f'Share of reconstructed PIE consonants present in Sanskrit, '
        f'across 150 years of revision.'
        f'</text>\n'
    )

    # ----- Horizontal gridlines and y-axis labels -----
    for gv in [0.00, 0.25, 0.50, 0.75, 1.00]:
        yy = y_at_val(gv)
        body.append(
            f'  <line x1="{plot_x0:.4f}" y1="{yy:.4f}" '
            f'x2="{plot_x0 + plot_w:.4f}" y2="{yy:.4f}" '
            f'stroke="{PALETTE["grid"]}" stroke-width="0.006" />\n'
        )
        body.append(
            f'  <text x="{plot_x0 - 0.09:.4f}" y="{yy + 0.038:.4f}" '
            f'text-anchor="end" font-size="0.095" '
            f'fill="{PALETTE["grid_strong"]}" font-family="{FONT}">'
            f'{int(gv * 100)}%</text>\n'
        )

    # Subtle vertical guide at each PIE milestone year (very pale,
    # extending from top of chart down through the lanes).
    for year in YEARS:
        x = x_at(year)
        body.append(
            f'  <line x1="{x:.4f}" y1="{chart_y0:.4f}" '
            f'x2="{x:.4f}" y2="{lanes_y0 + total_lane_h:.4f}" '
            f'stroke="{PALETTE["grid"]}" stroke-width="0.005" '
            f'opacity="0.65" />\n'
        )

    # ----- Tamil control: thin dotted gray line (drawn FIRST so the Sk
    # line overlays it).
    ta_path = " ".join(
        f"{'M' if i == 0 else 'L'} {x_at(y):.4f} {y_at_val(v):.4f}"
        for i, (y, v) in enumerate(zip(YEARS, TA_VALS))
    )
    body.append(
        f'  <path d="{ta_path}" fill="none" '
        f'stroke="{PALETTE["tamil"]}" stroke-width="0.009" '
        f'stroke-dasharray="0.05 0.05" stroke-linecap="round" />\n'
    )
    # Small open Tamil markers
    for y, v in zip(YEARS, TA_VALS):
        body.append(
            f'  <circle cx="{x_at(y):.4f}" cy="{y_at_val(v):.4f}" '
            f'r="0.040" fill="{PALETTE["background"]}" '
            f'stroke="{PALETTE["tamil"]}" stroke-width="0.008" />\n'
        )
    # Tamil-control label, anchored near the rightmost Tamil point
    last_y = YEARS[-1]
    last_v = TA_VALS[-1]
    body.append(
        f'  <text x="{x_at(last_y) + 0.10:.4f}" '
        f'y="{y_at_val(last_v) + 0.035:.4f}" '
        f'text-anchor="start" font-size="0.092" '
        f'fill="{PALETTE["tamil"]}" font-style="italic" '
        f'font-family="{FONT}">Tamil control</text>\n'
    )

    # ----- Sanskrit ⊇ PIE: solid black line + filled markers + value
    # labels.
    sk_path = " ".join(
        f"{'M' if i == 0 else 'L'} {x_at(y):.4f} {y_at_val(v):.4f}"
        for i, (y, v) in enumerate(zip(YEARS, SK_VALS))
    )
    body.append(
        f'  <path d="{sk_path}" fill="none" '
        f'stroke="{PALETTE["data"]}" stroke-width="0.018" '
        f'stroke-linecap="round" stroke-linejoin="round" />\n'
    )
    for y, v in zip(YEARS, SK_VALS):
        body.append(
            f'  <circle cx="{x_at(y):.4f}" cy="{y_at_val(v):.4f}" '
            f'r="0.060" fill="{PALETTE["data"]}" />\n'
        )
        body.append(
            f'  <text x="{x_at(y):.4f}" y="{y_at_val(v) - 0.10:.4f}" '
            f'text-anchor="middle" font-size="0.105" font-weight="bold" '
            f'fill="{PALETTE["data"]}" font-family="{FONT}">'
            f'{int(round(v * 100))}%</text>\n'
        )

    # ----- Phase labels above the line (1862, 1973, 2020) -----
    for year, text in PHASE_LABELS.items():
        x = x_at(year)
        # Place phase labels at a consistent y above the highest part of the
        # data line so they don't clash with the value labels.
        phase_y = chart_y0 - 0.08
        body.append(
            f'  <text x="{x:.4f}" y="{phase_y:.4f}" '
            f'text-anchor="middle" font-size="0.092" font-style="italic" '
            f'fill="{PALETTE["phase"]}" font-family="{FONT}">'
            f'{_xml_escape(text)}</text>\n'
        )

    # ----- Y-axis label (rotated) -----
    body.append(
        f'  <text x="0.22" y="{chart_y0 + chart_h/2:.4f}" '
        f'text-anchor="middle" font-size="0.105" '
        f'fill="{PALETTE["grid_strong"]}" font-family="{FONT}" '
        f'transform="rotate(-90 0.22 {chart_y0 + chart_h/2:.4f})">'
        f'PIE consonants covered</text>\n'
    )

    # ----- Bottom timeline panel: 3 lanes -----
    lane_specs = [
        ("PIE revisions",         LANE_1_PIE,   PALETTE["lane_pie"]),
        ("Western · European",    LANE_2_WEST,  PALETTE["lane_west"]),
        ("Indic · Sanskrit",      LANE_3_INDIA, PALETTE["lane_india"]),
    ]

    for li, (lane_name, events, lane_color) in enumerate(lane_specs):
        lane_y_top = lanes_y0 + li * (lane_h + lane_gap)
        track_y = lane_y_top + lane_h * 0.55

        # Lane track (subtle horizontal line)
        body.append(
            f'  <line x1="{plot_x0:.4f}" y1="{track_y:.4f}" '
            f'x2="{plot_x0 + plot_w:.4f}" y2="{track_y:.4f}" '
            f'stroke="{PALETTE["lane_track"]}" stroke-width="0.008" />\n'
        )

        # Lane label (left of track)
        body.append(
            f'  <text x="{plot_x0 - 0.10:.4f}" y="{track_y + 0.04:.4f}" '
            f'text-anchor="end" font-size="0.10" font-weight="bold" '
            f'fill="{lane_color}" font-family="{FONT}">'
            f'{_xml_escape(lane_name)}</text>\n'
        )

        # Events
        # Stagger labels above/below in case of horizontal crowding.
        for ei, (year, label) in enumerate(events):
            x = x_at(year)
            # Tick (small vertical line through the track)
            tick_half = 0.09
            body.append(
                f'  <line x1="{x:.4f}" y1="{track_y - tick_half:.4f}" '
                f'x2="{x:.4f}" y2="{track_y + tick_half:.4f}" '
                f'stroke="{lane_color}" stroke-width="0.012" />\n'
            )
            # Year (above tick)
            body.append(
                f'  <text x="{x:.4f}" y="{track_y - 0.14:.4f}" '
                f'text-anchor="middle" font-size="0.085" font-weight="bold" '
                f'fill="{lane_color}" font-family="{FONT}">'
                f'{year}</text>\n'
            )
            # Short description (below tick); alternate angle for crowded
            # clusters by staggering vertically.
            stagger = 0.0 if ei % 2 == 0 else 0.13
            body.append(
                f'  <text x="{x:.4f}" '
                f'y="{track_y + 0.22 + stagger:.4f}" '
                f'text-anchor="middle" font-size="0.082" '
                f'fill="{lane_color}" font-family="{FONT}">'
                f'{_xml_escape(label)}</text>\n'
            )

    # ----- Footer caption -----
    body.append(
        f'  <text x="{W/2:.4f}" y="{H - 0.15:.4f}" text-anchor="middle" '
        f'font-size="0.095" fill="{PALETTE["footer"]}" font-style="italic" '
        f'font-family="{FONT}">'
        f'The lanes show context, not causation: PIE keeps changing '
        f'inside Western philology while Sanskrit reassertion moves '
        f'on its own track.</text>\n'
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

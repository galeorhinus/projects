"""JSON-driven scatter overlay on a vocal-tract ribbon.

Renders a scatter chart where each consonant of a writing system is
drawn as a small filled circle at a position determined by:
    - column index  → theta (angular position around the vocal-tract ellipse)
    - row index     → r (radial distance from the ellipse centerline)

The vocal-tract ribbon (a thin arc) is drawn underneath as a visual anchor.

Two modes:
    "grid"   — each (col, row) maps to a precise (theta, r); dots align
               on a regular polar grid
    "jitter" — adds small random offsets to theta and r; with semi-
               transparent fills, denser articulatory zones darken
               into a visible cloud

CLI
---
    python3 vocal_tract_scatter.py configs/scatter_sanskrit.json
    python3 vocal_tract_scatter.py configs/scatter_sanskrit.json --mode jitter
    python3 vocal_tract_scatter.py configs/scatter_sanskrit.json -o /path/out.svg

JSON schema (top-level)
-----------------------
    {
      "name":         "scatter_sanskrit",
      "description":  "free text",
      "geometry":     { "r1": 2.5, "r2": 2.5, "w": 0.35 },
      "canvas":       { "width": 4.5, "height": 3.0 },
      "base_ribbon":  { "t1": 135, "t2": 225,
                        "stroke_color": "#666666", ... },
      "scatter": {
        "mode": "grid" | "jitter",
        "angular_range": {
          "center":    180,
          "half_width_deg": 45     // OR "half_width_x": 1.0 (inches)
        },
        "rows": {
          "r_center":  2.5,
          "delta_r":   0.1
        },
        "jitter": {
          "theta_deg": 3.0,
          "r":         0.04,
          "seed":      42
        },
        "circle_radius": 0.06,
        "fill_color":    "#666666",
        "opacity":       0.5,
        "matrix": [
          ["क", "च", "ट", "त", "प"],
          ["ख", "छ", "ठ", "थ", "फ"],
          ...
        ]
      }
    }

Cells in ``matrix`` are strings; non-empty strings render as a filled
circle.  The string itself is not rendered (per project convention —
the dots are positional markers).  Empty string or null = no circle.
Rows are top-to-bottom from the reader's perspective AND row 0 sits
at the OUTERMOST radius (above the centerline at the top of the
ellipse — closest to the reader looking down at the diagram).
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from vocal_tract_schematics import build_ribbon_path_d, point_at
from vocal_tract_regions import (
    BUILT_IN_DEFAULTS,
    _xml_escape,
    build_region_svg,
)


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = SCRIPT_DIR.parent / "build" / "vocal_tract"


SCATTER_DEFAULTS = {
    "circle_radius": 0.06,
    "fill_color": "#666666",
    "opacity": 0.5,
    "stroke_color": "none",
}


def _column_thetas(angular_range: dict, r_center: float, n_cols: int
                   ) -> list[float]:
    """Compute the theta value for each column.

    ``angular_range.center`` is the angle of the middle column (typically 180°
    for top-of-mouth).  Half-width may be specified either as ``half_width_deg``
    or as a horizontal distance in inches via ``half_width_x`` (the latter is
    converted using the centerline radius ``r_center``).

    If ``thetas`` is given explicitly, it overrides the calculation.
    """
    if "thetas" in angular_range:
        thetas = list(angular_range["thetas"])
        if len(thetas) != n_cols:
            raise ValueError(
                f"angular_range.thetas length ({len(thetas)}) does not match "
                f"the column count from matrix ({n_cols})"
            )
        return thetas

    center = float(angular_range.get("center", 180.0))
    if "half_width_x" in angular_range:
        hx = float(angular_range["half_width_x"])
        ratio = min(max(hx / r_center, -1.0), 1.0)
        half_deg = math.degrees(math.asin(ratio))
    else:
        half_deg = float(angular_range.get("half_width_deg", 45.0))

    if n_cols == 1:
        return [center]
    start = center - half_deg
    end = center + half_deg
    step = (end - start) / (n_cols - 1)
    return [start + i * step for i in range(n_cols)]


def _row_radii(rows: dict, n_rows: int) -> list[float]:
    """Compute the r value for each row, centered around ``r_center``."""
    r_center = float(rows["r_center"])
    delta_r = float(rows["delta_r"])
    # Row 0 is OUTERMOST (largest r); row N-1 is innermost.
    # Offsets go from +(n-1)/2 * delta_r down to -(n-1)/2 * delta_r.
    half_count = (n_rows - 1) / 2.0
    return [r_center + (half_count - i) * delta_r for i in range(n_rows)]


def _render_scatter(scatter: dict, mode: str
                    ) -> tuple[str, list[tuple[float, float]]]:
    """Build the SVG fragment for the scatter dots and return bbox samples."""
    matrix = scatter.get("matrix", [])
    if not matrix:
        return "", []

    n_rows = len(matrix)
    n_cols = max(len(row) for row in matrix)

    rows_cfg = scatter["rows"]
    r_center = float(rows_cfg["r_center"])

    column_thetas = _column_thetas(
        scatter.get("angular_range", {}), r_center, n_cols
    )
    row_radii = _row_radii(rows_cfg, n_rows)

    circle_radius = float(scatter.get(
        "circle_radius", SCATTER_DEFAULTS["circle_radius"]
    ))
    fill_color = scatter.get("fill_color", SCATTER_DEFAULTS["fill_color"])
    stroke_color = scatter.get("stroke_color", SCATTER_DEFAULTS["stroke_color"])
    opacity = float(scatter.get("opacity", SCATTER_DEFAULTS["opacity"]))

    if mode == "jitter":
        jitter_cfg = scatter.get("jitter", {})
        theta_jitter = float(jitter_cfg.get("theta_deg", 3.0))
        r_jitter = float(jitter_cfg.get("r", 0.04))
        seed = int(jitter_cfg.get("seed", 42))
    else:
        theta_jitter = 0.0
        r_jitter = 0.0
        seed = 0
    rng = random.Random(seed)

    opacity_attr = f' opacity="{opacity:.4f}"' if opacity != 1.0 else ""

    body_parts = []
    samples = []
    for ri, row in enumerate(matrix):
        for ci, cell in enumerate(row):
            if ci >= n_cols:
                continue
            if not cell:
                continue
            theta = column_thetas[ci]
            r = row_radii[ri]
            if theta_jitter > 0:
                theta += rng.uniform(-theta_jitter, theta_jitter)
            if r_jitter > 0:
                r += rng.uniform(-r_jitter, r_jitter)
            x, y = point_at(r, r, theta)
            body_parts.append(
                f'  <circle cx="{x:.4f}" cy="{y:.4f}" '
                f'r="{circle_radius:.4f}" fill="{fill_color}" '
                f'stroke="{stroke_color}"{opacity_attr} />\n'
            )
            samples.append((x - circle_radius, y - circle_radius))
            samples.append((x + circle_radius, y + circle_radius))

    return "".join(body_parts), samples


def render_scatter_svg(config: dict, mode_override: str | None = None) -> str:
    """Build the full SVG document from a parsed config dict.

    Layers (back to front):
      1. base ribbon (an open elliptical-ribbon arc as visual anchor)
      2. optional varga / region bands (same machinery as regions.py)
      3. scatter dots
    """
    geometry = config["geometry"]
    r1 = float(geometry["r1"])
    r2 = float(geometry["r2"])
    w = float(geometry["w"])

    defaults = dict(BUILT_IN_DEFAULTS)
    defaults.update(config.get("defaults", {}))

    bodies: list[str] = []
    defs_blocks: list[str] = []
    all_samples: list[tuple[float, float]] = []

    # 1. Base ribbon.
    base = config.get("base_ribbon")
    if base is not None:
        bt1 = float(base["t1"])
        bt2 = float(base["t2"])
        path_d, ribbon_samples = build_ribbon_path_d(r1, r2, w, bt1, bt2)
        bop = float(base.get("opacity", 1.0))
        bop_attr = f' opacity="{bop:.4f}"' if bop != 1.0 else ""
        bodies.append(
            f'  <path d="{path_d}" '
            f'fill="{base.get("fill_color", "none")}" '
            f'stroke="{base.get("stroke_color", "#999999")}" '
            f'stroke-width="{base.get("stroke_size", 0.012)}" '
            f'stroke-linejoin="miter" stroke-linecap="butt"{bop_attr} />\n'
        )
        all_samples.extend(ribbon_samples)

    # 2. Regions (optional varga bands etc.).
    for idx, region in enumerate(config.get("regions", [])):
        body_svg, defs_svg, samples = build_region_svg(
            region, geometry, defaults, region_idx=idx,
        )
        bodies.append(body_svg)
        if defs_svg:
            defs_blocks.append(defs_svg)
        all_samples.extend(samples)

    # 3. Scatter dots.
    scatter = config.get("scatter")
    if scatter is not None:
        mode = mode_override or scatter.get("mode", "grid")
        scatter_svg, scatter_samples = _render_scatter(scatter, mode)
        bodies.append(scatter_svg)
        all_samples.extend(scatter_samples)

    if not all_samples:
        raise ValueError("config produced no content to render")

    cx_min = min(p[0] for p in all_samples)
    cx_max = max(p[0] for p in all_samples)
    cy_min = min(p[1] for p in all_samples)
    cy_max = max(p[1] for p in all_samples)

    canvas_block = config.get("canvas")
    if canvas_block is not None:
        width_in = float(canvas_block["width"])
        height_in = float(canvas_block["height"])
        if "viewbox_origin" in canvas_block:
            xmin = float(canvas_block["viewbox_origin"]["x"])
            ymin = float(canvas_block["viewbox_origin"]["y"])
        else:
            content_cx = (cx_min + cx_max) / 2.0
            content_cy = (cy_min + cy_max) / 2.0
            xmin = content_cx - width_in / 2.0
            ymin = content_cy - height_in / 2.0
    else:
        margin = float(geometry.get("margin", 0.1))
        xmin = cx_min - margin
        xmax = cx_max + margin
        ymin = cy_min - margin
        ymax = cy_max + margin
        width_in = xmax - xmin
        height_in = ymax - ymin

    defs_section = ""
    if defs_blocks:
        defs_section = "  <defs>\n" + "".join(defs_blocks) + "  </defs>\n"

    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width_in:.4f}in" height="{height_in:.4f}in" '
        f'viewBox="{xmin:.4f} {ymin:.4f} {width_in:.4f} {height_in:.4f}">\n'
        + defs_section
        + "".join(bodies)
        + "</svg>\n"
    )


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("config", help="path to JSON config")
    parser.add_argument(
        "--mode", choices=("grid", "jitter"),
        help="override the mode in the JSON config",
    )
    parser.add_argument(
        "--output", "-o",
        help="output SVG path; default is ../build/vocal_tract/<name>.svg "
             "(with _grid or _jitter suffix if --mode is set)",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))

    if args.output:
        out_path = Path(args.output)
    else:
        name = config.get("name", config_path.stem)
        if args.mode:
            name = f"{name}_{args.mode}"
        out_path = DEFAULT_OUTPUT_DIR / f"{name}.svg"

    svg = render_scatter_svg(config, mode_override=args.mode)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg, encoding="utf-8")
    print(f"Wrote {out_path}  ({len(svg)} bytes)")


if __name__ == "__main__":
    main()

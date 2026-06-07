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

from .schematics import build_ribbon_path_d, point_at
from .regions import (
    BUILT_IN_DEFAULTS,
    _xml_escape,
    build_region_svg,
)


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "output"


SCATTER_DEFAULTS = {
    "circle_radius": 0.06,
    "fill_color": "#666666",
    "opacity": 0.5,
    "stroke_color": "none",
}


def _column_thetas(angular_range: dict, r_center: float, n_cols: int,
                   mode_override: str | None = None,
                   ) -> list[float]:
    """Compute the theta value for each column.

    Three distribution modes (``angular_range.mode``):
      - ``"uniform"``     equal angular spacing (default)
      - ``"anatomical"``  linear by distance from lips
                          (uses ``angular_range.distances``)
      - ``"sqrt"``        by √distance — front spread wider, back compressed

    ``angular_range.center`` is the midpoint of the angular range.
    Half-width via ``half_width_deg`` or ``half_width_x`` (inches).

    Explicit ``thetas`` overrides everything.
    """
    if "thetas" in angular_range:
        thetas = list(angular_range["thetas"])
        if len(thetas) != n_cols:
            raise ValueError(
                f"angular_range.thetas length ({len(thetas)}) does not match "
                f"the column count from matrix ({n_cols})"
            )
        return thetas

    mode = mode_override or angular_range.get("mode", "uniform")
    center = float(angular_range.get("center", 180.0))
    if "half_width_x" in angular_range:
        hx = float(angular_range["half_width_x"])
        ratio = min(max(hx / r_center, -1.0), 1.0)
        half_deg = math.degrees(math.asin(ratio))
    else:
        half_deg = float(angular_range.get("half_width_deg", 45.0))
    start = center - half_deg
    end = center + half_deg

    if mode in ("anatomical", "sqrt"):
        distances = angular_range.get("distances")
        if distances is None:
            raise ValueError(
                f"angular_range.mode={mode!r} requires angular_range.distances"
            )
        if len(distances) != n_cols:
            raise ValueError(
                f"angular_range.distances length ({len(distances)}) does not "
                f"match the column count from matrix ({n_cols})"
            )
        d = [float(x) for x in distances]
        if mode == "sqrt":
            d = [math.sqrt(max(x, 0.0)) for x in d]
        d_min, d_max = min(d), max(d)
        rng = d_max - d_min if d_max > d_min else 1.0
        return [start + (x - d_min) / rng * (end - start) for x in d]

    # uniform
    if n_cols == 1:
        return [center]
    step = (end - start) / (n_cols - 1)
    return [start + i * step for i in range(n_cols)]


def _row_radii(rows: dict, n_rows: int) -> list[float]:
    """Compute the r value for each row.

    Three layouts:
      - ``r_inner``  — innermost row (last index) sits at r_inner; each
                       earlier row steps OUTWARD by delta_r.  Preferred
                       when the chart should grow outward from a fixed
                       inner anchor.
      - ``r_max``    — outermost row (index 0) sits at r_max; each
                       later row steps INWARD by delta_r.
      - ``r_center`` — rows centered around r_center (legacy).
    Precedence: r_inner → r_max → r_center.
    """
    delta_r = float(rows["delta_r"])
    if "r_inner" in rows:
        r_inner = float(rows["r_inner"])
        return [r_inner + (n_rows - 1 - i) * delta_r for i in range(n_rows)]
    if "r_max" in rows:
        r_max = float(rows["r_max"])
        return [r_max - i * delta_r for i in range(n_rows)]
    r_center = float(rows["r_center"])
    half_count = (n_rows - 1) / 2.0
    return [r_center + (half_count - i) * delta_r for i in range(n_rows)]


def _effective_radius(rows: dict) -> float:
    """Return the radius used for the half_width_x → angular conversion."""
    if "r_inner" in rows:
        return float(rows["r_inner"])
    if "r_max" in rows:
        return float(rows["r_max"])
    return float(rows["r_center"])


def _render_place_labels(
    labels: list[str],
    column_thetas: list[float],
    matrix: list[list[str]],
    rows_cfg: dict,
    config: dict,
    default_font_family: str,
    canvas_height: float = 3.0,
) -> tuple[str, list[tuple[float, float]]]:
    """Render leader lines + number callouts at the chart's bottom.

    Two-segment leader per filled column:
      - radial from (innermost_filled_r − leader_gap) inward to
        leader_inner_r along the column's theta;
      - vertical down (constant x) to the leader's bottom endpoint
        at y_label.

    The number callout sits ``label_gap`` inches below the leader
    endpoint, centered horizontally on the leader.

    ``y_label`` is derived dynamically (so the endpoint lands
    ``bottom_margin`` above the auto-centered canvas bottom) unless
    overridden by the config.
    """
    parts: list[str] = []
    samples: list[tuple[float, float]] = []

    leader_inner_r = float(config.get("leader_inner_r", 1.5))
    leader_gap = float(config.get("leader_gap", 0.05))
    leader_color = config.get("leader_stroke_color", "#888888")
    leader_width = float(config.get("leader_stroke_width", 0.005))

    font_size = float(config.get("font_size", 0.1528))
    color = config.get("color", "#222222")
    font_family = config.get("font_family", default_font_family)
    show_numbers = bool(config.get("show_numbers", True))
    label_gap = float(config.get("label_gap", 0.05))

    n_rows = len(matrix) if matrix else 0
    row_radii_list = _row_radii(rows_cfg, n_rows) if n_rows > 0 else []

    def innermost_filled_r(col_idx: int) -> float | None:
        max_row = -1
        for i, row in enumerate(matrix):
            if col_idx < len(row) and row[col_idx]:
                max_row = i
        if max_row == -1:
            return None
        return row_radii_list[max_row]

    # Resolve y_label.  Explicit config value wins; otherwise derive
    # so the leader endpoint sits ``bottom_margin`` above canvas bottom
    # after content-centroid auto-centering.
    y_label_cfg = config.get("y_label")
    if y_label_cfg is not None:
        y_label = float(y_label_cfg)
    else:
        bottom_margin = float(config.get("bottom_margin", 0.5))
        chart_y_top = 0.0
        for ci, theta in enumerate(column_thetas):
            for ri, row in enumerate(matrix):
                if ci < len(row) and row[ci]:
                    y_dot = math.cos(math.radians(theta)) * row_radii_list[ri]
                    if y_dot < chart_y_top:
                        chart_y_top = y_dot
        # content y range goes from chart_y_top to text_bottom =
        # y_label + label_gap + font_size.  Auto-centering puts
        # canvas_bottom at centroid + canvas_height/2.  Solving
        # canvas_bottom − y_label = bottom_margin gives:
        y_label = (
            chart_y_top + label_gap + font_size
            + (canvas_height - 2.0 * bottom_margin)
        )

    for col_idx, theta in enumerate(column_thetas):
        innermost_r = innermost_filled_r(col_idx)
        if innermost_r is None:
            continue

        start_r = innermost_r - leader_gap
        x_start, y_radial_start = point_at(start_r, start_r, theta)
        x_inner, y_inner = point_at(leader_inner_r, leader_inner_r, theta)

        parts.append(
            f'  <path d="M {x_start:.4f} {y_radial_start:.4f} '
            f'L {x_inner:.4f} {y_inner:.4f} '
            f'L {x_inner:.4f} {y_label:.4f}" '
            f'fill="none" stroke="{leader_color}" '
            f'stroke-width="{leader_width}" stroke-linecap="round" />\n'
        )

        if show_numbers:
            label_text = str(col_idx + 1)
        elif col_idx < len(labels) and labels[col_idx]:
            label_text = labels[col_idx]
        else:
            label_text = ""

        if label_text:
            # label_gap between leader endpoint and text top edge;
            # dominant-baseline=middle means text_y is the center,
            # so center sits at y_label + label_gap + font_size/2.
            text_y = y_label + label_gap + font_size * 0.5
            parts.append(
                f'  <text x="{x_inner:.4f}" y="{text_y:.4f}" '
                f'text-anchor="middle" dominant-baseline="middle" '
                f'font-size="{font_size}" fill="{color}" '
                f'font-family="{_xml_escape(font_family)}">'
                f'{_xml_escape(label_text)}</text>\n'
            )
            text_w = max(len(label_text), 1) * font_size * 0.55
            text_h = font_size * 0.65
            samples.append((x_inner - text_w / 2.0, text_y - text_h))
            samples.append((x_inner + text_w / 2.0, text_y + text_h))

        samples.append((x_start, y_radial_start))
        samples.append((x_inner, y_inner))
        samples.append((x_inner, y_label))

    return "".join(parts), samples


def _render_scatter(scatter: dict, mode: str,
                    default_font_family: str = BUILT_IN_DEFAULTS["label_font_family"],
                    angular_mode_override: str | None = None,
                    canvas_height: float = 3.0,
                    ) -> tuple[str, list[tuple[float, float]]]:
    """Build the SVG fragment for the scatter dots and return bbox samples."""
    matrix = scatter.get("matrix", [])
    if not matrix:
        return "", []

    n_rows = len(matrix)
    n_cols = max(len(row) for row in matrix)

    rows_cfg = scatter["rows"]
    column_thetas = _column_thetas(
        scatter.get("angular_range", {}), _effective_radius(rows_cfg), n_cols,
        mode_override=angular_mode_override,
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

    # Place labels — leader lines + number callouts at the chart bottom.
    place_labels_cfg = scatter.get("place_labels")
    if place_labels_cfg is not None:
        labels = place_labels_cfg.get("labels", [])
        label_svg, label_samples = _render_place_labels(
            labels=labels,
            column_thetas=column_thetas,
            matrix=matrix,
            rows_cfg=rows_cfg,
            config=place_labels_cfg,
            default_font_family=default_font_family,
            canvas_height=canvas_height,
        )
        body_parts.append(label_svg)
        samples.extend(label_samples)

    return "".join(body_parts), samples


def render_scatter_svg(config: dict, mode_override: str | None = None,
                       angular_mode_override: str | None = None) -> str:
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

    # Pre-read canvas height so _render_scatter can use it for the
    # dynamic y_label calculation in place_labels.
    _canvas = config.get("canvas") or {}
    canvas_height_for_labels = float(_canvas.get("height", 3.0))

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

    # 3. Scatter dots (+ optional place labels).
    scatter = config.get("scatter")
    if scatter is not None:
        mode = mode_override or scatter.get("mode", "grid")
        scatter_svg, scatter_samples = _render_scatter(
            scatter, mode,
            default_font_family=defaults.get(
                "label_font_family", BUILT_IN_DEFAULTS["label_font_family"],
            ),
            angular_mode_override=angular_mode_override,
            canvas_height=canvas_height_for_labels,
        )
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

    # Explicit background — defaults to white so viewers with dark themes
    # (VS Code, GitHub dark, etc.) don't render the canvas as black.  Set
    # canvas.background to "none" or "transparent" for transparent output.
    bg = "#ffffff"
    if canvas_block is not None and "background" in canvas_block:
        bg = canvas_block["background"]
    bg_section = ""
    if bg and bg.lower() not in ("none", "transparent"):
        bg_section = (
            f'  <rect x="{xmin:.4f}" y="{ymin:.4f}" '
            f'width="{width_in:.4f}" height="{height_in:.4f}" '
            f'fill="{bg}" />\n'
        )

    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width_in:.4f}in" height="{height_in:.4f}in" '
        f'viewBox="{xmin:.4f} {ymin:.4f} {width_in:.4f} {height_in:.4f}">\n'
        + bg_section
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
        help="override the dot mode in the JSON config",
    )
    parser.add_argument(
        "--angular-mode", choices=("uniform", "anatomical", "sqrt"),
        help="override the angular distribution mode for column thetas",
    )
    parser.add_argument(
        "--output", "-o",
        help="output SVG path; default is output/<name>.svg "
             "(with mode suffixes if --mode or --angular-mode are set)",
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
        if args.angular_mode and args.angular_mode != "uniform":
            name = f"{name}_{args.angular_mode}"
        out_path = DEFAULT_OUTPUT_DIR / f"{name}.svg"

    svg = render_scatter_svg(
        config, mode_override=args.mode,
        angular_mode_override=args.angular_mode,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg, encoding="utf-8")
    print(f"Wrote {out_path}  ({len(svg)} bytes)")


if __name__ == "__main__":
    main()

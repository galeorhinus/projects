"""JSON-driven vocal-tract region atlas.

Reads a region-atlas config from a JSON file and renders all regions as
a single SVG.  Each region is an elliptical ribbon arc (same geometry
as ``vocal_tract_schematics.py`` — same shared (r1, r2, w) ellipse with
different angular ranges) optionally annotated with a label.

Usage
-----
    python3 vocal_tract_regions.py configs/example_vargas.json

The output path defaults to ``../build/vocal_tract/<config-name>.svg``
(relative to this script) but can be overridden with ``--output``.

JSON schema
-----------
Each config carries shared geometry, shared defaults, and a list of
regions.  Any field in a region overrides the corresponding default.

    {
      "name": "example_vargas",
      "description": "Free-form notes.",
      "geometry": { "r1": 3.0, "r2": 3.0, "w": 0.5, "margin": 0.2 },
      "defaults": {
        "stroke_color": "#222222",
        "stroke_size": 0.02,
        "fill_color": "none",
        "opacity": 1.0,
        "label_font_size": 0.15,
        "label_color": "#333333"
      },
      "regions": [
        {
          "name": "osthya",
          "t1": -120, "t2": -100,
          "fill_color": "#cc3333",
          "label": {
            "text": ["ओष्ठ्य", "(labial)"],
            "offset": {"x": 0, "y": 0.35},
            "rotation": 0
          }
        }
      ]
    }

Angle convention (inherited from vocal_tract_schematics.py)
----------------------------------------------------------
    0°   = 6 o'clock (chin)
    90°  = 9 o'clock (left)
    180° = 12 o'clock (top of head)
    270° = 3 o'clock (right)
Angles increase clockwise.

Label coordinate system
-----------------------
The label sits at the angular midpoint of the region.

If ``rotation == 0`` (the default), the label follows the ribbon's
curve — each text line is laid out along an elliptical-arc <textPath>.
For labels whose midpoint lands on the lower half of the ellipse, the
path is reversed automatically so the text reads right-side-up.

If ``rotation != 0``, the label is rendered as straight text rotated
by the tangent angle of the ribbon at the midpoint plus the explicit
``rotation`` value.  Same auto-flip rule keeps it readable.

In both modes:
  ``offset.y`` shifts the label outward (away from the ellipse center).
                Curved mode: shifts the path radius.
                Straight mode: shifts the position along the outward
                normal.
  ``offset.x`` shifts the label along the ribbon, in the direction of
                increasing θ (visually clockwise).
                Curved mode: shifts the textPath ``startOffset``.
                Straight mode: shifts the position along the tangent.

Multi-line labels: pass ``text`` as a list of strings.
  Curved mode: each line gets its own arc path at a slightly different
                radius; lines stack outward-to-inward (or inward-to-
                outward when the path is reversed) so visually-top
                line reads first.
  Straight mode: lines are stacked vertically around the position point.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from vocal_tract_schematics import (
    build_ribbon_path_d,
    outward_normal_at,
    point_at,
    tangent_at,
)


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = SCRIPT_DIR.parent / "build" / "vocal_tract"


# --- Defaults --------------------------------------------------------

BUILT_IN_DEFAULTS = {
    "stroke_color": "#222222",
    "stroke_size": 0.02,
    "fill_color": "none",
    "opacity": 1.0,
    "label_font_size": 0.15,
    "label_color": "#333333",
    # Matches the font stack used by the book's other Claude-generated
    # SVGs (e.g. strategic_three_pillars_containment.svg).  Gentium Book
    # Plus carries full IAST + Devanagari coverage; Charter matches the
    # book's body font set in as_book.yaml (mainfont: Charter).
    "label_font_family": (
        "'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"
    ),
}

DEFAULT_LABEL_OFFSET = {"x": 0.0, "y": 0.0}
DEFAULT_LABEL_ROTATION = 0.0


# --- Label geometry --------------------------------------------------


def _normalize_angle_deg(a: float) -> float:
    """Normalize an angle to (-180, 180]."""
    a = ((a + 180.0) % 360.0) - 180.0
    if a <= -180.0:
        a += 360.0
    return a


def _sanitize_id(name: str) -> str:
    """Convert a name into a safe SVG id (alphanumeric and hyphens only)."""
    safe = "".join(c if (c.isalnum() or c == "-") else "-" for c in name)
    return safe or "region"


def _arc_path_d(rx: float, ry: float, t1: float, t2: float,
                reverse: bool = False) -> str:
    """SVG path 'd' for an open elliptical arc (no fill).

    Under the clockwise angle convention, going from t1 → t2 (with t2 > t1)
    traces CW visually, which is SVG sweep_flag = 1.  When reverse=True the
    path runs t2 → t1 instead, tracing CCW visually (sweep_flag = 0).
    """
    if reverse:
        p_start = point_at(rx, ry, t2)
        p_end = point_at(rx, ry, t1)
        sweep_flag = 0
    else:
        p_start = point_at(rx, ry, t1)
        p_end = point_at(rx, ry, t2)
        sweep_flag = 1
    large_arc = 1 if abs(t2 - t1) > 180.0 else 0
    return (
        f"M {p_start[0]:.4f} {p_start[1]:.4f} "
        f"A {rx:.4f} {ry:.4f} 0 {large_arc} {sweep_flag} "
        f"{p_end[0]:.4f} {p_end[1]:.4f}"
    )


def compute_label_transform(
    r1: float,
    r2: float,
    theta_mid_deg: float,
    offset_x: float,
    offset_y: float,
    extra_rotation_deg: float,
) -> tuple[float, float, float]:
    """Return (final_x, final_y, rotation_deg) for a label.

    The label sits at the angular midpoint of the region on the centerline
    ellipse (r1, r2).  Offset is in world-aligned semantic coords:
    +x along the tangent (direction of increasing θ), +y outward from
    the ellipse center.  Rotation defaults to the tangent angle (flipped
    if upside-down), plus the caller's extra rotation.
    """
    bx, by = point_at(r1, r2, theta_mid_deg)
    tx, ty = tangent_at(r1, r2, theta_mid_deg)
    ox, oy = outward_normal_at(r1, r2, theta_mid_deg)

    final_x = bx + offset_x * tx + offset_y * ox
    final_y = by + offset_x * ty + offset_y * oy

    tangent_angle_deg = math.degrees(math.atan2(ty, tx))
    # Flip 180° if the tangent would put text upside-down.
    if abs(_normalize_angle_deg(tangent_angle_deg)) > 90.0:
        tangent_angle_deg = _normalize_angle_deg(tangent_angle_deg + 180.0)

    rotation_deg = tangent_angle_deg + extra_rotation_deg
    return final_x, final_y, rotation_deg


# --- SVG fragments ---------------------------------------------------


def _xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _normalize_label(label_block: dict | None) -> dict | None:
    """Coerce a label block into a normalized form, or None if missing."""
    if label_block is None:
        return None
    text = label_block.get("text")
    if text is None:
        return None
    if isinstance(text, str):
        lines = [text]
    elif isinstance(text, list):
        lines = [str(line) for line in text]
    else:
        raise ValueError(
            f"label.text must be a string or list of strings; got {type(text)}"
        )
    offset = label_block.get("offset", DEFAULT_LABEL_OFFSET)
    rotation = float(label_block.get("rotation", DEFAULT_LABEL_ROTATION))
    return {
        "lines": lines,
        "offset_x": float(offset.get("x", 0.0)),
        "offset_y": float(offset.get("y", 0.0)),
        "rotation": rotation,
    }


def _build_label_straight(
    label: dict,
    r1: float,
    r2: float,
    theta_mid_deg: float,
    font_size: float,
    color: str,
    font_family: str,
) -> tuple[str, list[tuple[float, float]]]:
    """Straight-text label.  Returns (text_svg, bbox_samples)."""
    final_x, final_y, rotation_deg = compute_label_transform(
        r1=r1, r2=r2, theta_mid_deg=theta_mid_deg,
        offset_x=label["offset_x"], offset_y=label["offset_y"],
        extra_rotation_deg=label["rotation"],
    )

    lines = label["lines"]
    n = len(lines)
    line_em = 1.2  # baseline-to-baseline distance (em units)
    first_dy_em = -((n - 1) / 2.0) * line_em
    tspans = []
    for i, line in enumerate(lines):
        dy_em = first_dy_em if i == 0 else line_em
        tspans.append(
            f'<tspan x="0" dy="{dy_em:.4f}em">{_xml_escape(line)}</tspan>'
        )
    tspan_block = "".join(tspans)

    transform = (
        f"translate({final_x:.4f} {final_y:.4f}) "
        f"rotate({rotation_deg:.4f})"
    )
    text_svg = (
        f'  <text transform="{transform}" '
        f'text-anchor="middle" dominant-baseline="middle" '
        f'font-size="{font_size}" fill="{color}" '
        f'font-family="{_xml_escape(font_family)}">{tspan_block}</text>\n'
    )

    longest = max((len(line) for line in lines), default=0)
    half_w = 0.5 * font_size * longest * 0.6
    half_h = 0.5 * font_size * (n * line_em)
    cos_r = math.cos(math.radians(rotation_deg))
    sin_r = math.sin(math.radians(rotation_deg))
    samples = []
    for dx, dy in [(-half_w, -half_h), (half_w, -half_h),
                   (half_w, half_h), (-half_w, half_h)]:
        wx = final_x + dx * cos_r - dy * sin_r
        wy = final_y + dx * sin_r + dy * cos_r
        samples.append((wx, wy))
    return text_svg, samples


def _build_label_curved(
    label: dict,
    r1: float,
    r2: float,
    t1: float,
    t2: float,
    font_size: float,
    color: str,
    font_family: str,
    region_id: str,
) -> tuple[str, str, list[tuple[float, float]]]:
    """Curved-text label using SVG <textPath>.

    Each line gets its own elliptical-arc path so multi-line labels stack
    radially.  If the angular midpoint puts text upside-down (tangent
    angle outside [-90°, 90°]), the path is reversed so the text reads
    right-side-up.

    Returns (text_svg, defs_svg, bbox_samples).
    """
    lines = label["lines"]
    n = len(lines)
    theta_mid = (t1 + t2) / 2.0

    tx, ty = tangent_at(r1, r2, theta_mid)
    tangent_angle = math.degrees(math.atan2(ty, tx))
    reverse_path = abs(_normalize_angle_deg(tangent_angle)) > 90.0

    line_em = 1.2
    line_spacing = line_em * font_size  # inches

    # Line stacking: line 0 is visually on top.  In the upper half of the
    # ellipse, that means a larger radius (further from center).  In the
    # lower half (with the path reversed), it means a smaller radius
    # (closer to center) — the ribbon is above the reader's view, so the
    # top line is closer to the ribbon.
    if reverse_path:
        first_radial = label["offset_y"] - ((n - 1) / 2.0) * line_spacing
        line_step = line_spacing
    else:
        first_radial = label["offset_y"] + ((n - 1) / 2.0) * line_spacing
        line_step = -line_spacing

    # offset.x along the path: positive means "in direction of increasing
    # θ" (visually CW).  Under a reversed path the parametric direction
    # of the path is opposite, so we negate.
    effective_offset_x = (
        -label["offset_x"] if reverse_path else label["offset_x"]
    )

    defs_parts = []
    text_parts = []
    samples = []

    for i, line in enumerate(lines):
        radial = first_radial + i * line_step
        line_r1 = r1 + radial
        line_r2 = r2 + radial
        # Bail out if the radial offset would invert the ellipse.
        if line_r1 <= 0 or line_r2 <= 0:
            raise ValueError(
                f"label radius for region '{region_id}' would be non-positive "
                f"(r1={r1}, r2={r2}, radial={radial}); reduce offset_y or font size"
            )

        path_id = f"label-{region_id}-l{i}"
        path_d = _arc_path_d(line_r1, line_r2, t1, t2, reverse=reverse_path)
        defs_parts.append(
            f'    <path id="{path_id}" d="{path_d}" fill="none" />\n'
        )

        # Center the text on the arc; shift by offset.x in inches if set.
        avg_r = (line_r1 + line_r2) / 2.0
        arc_length = avg_r * math.radians(abs(t2 - t1))
        if arc_length > 0:
            center_pos = arc_length / 2.0 + effective_offset_x
            center_pos = max(0.0, min(arc_length, center_pos))
            start_offset_attr = f' startOffset="{center_pos:.4f}"'
        else:
            start_offset_attr = ' startOffset="50%"'

        text_parts.append(
            f'  <text font-size="{font_size}" fill="{color}" '
            f'font-family="{_xml_escape(font_family)}">'
            f'<textPath href="#{path_id}"{start_offset_attr} '
            f'text-anchor="middle">'
            f'{_xml_escape(line)}</textPath></text>\n'
        )

        # Bounding-box samples — endpoints + midpoint of the arc; add a
        # small radial padding to account for character extent.
        pad = font_size * line_em * 0.75
        for theta in (t1, theta_mid, t2):
            samples.append(point_at(line_r1 + pad, line_r2 + pad, theta))
            samples.append(point_at(line_r1 - pad, line_r2 - pad, theta))

    return "".join(text_parts), "".join(defs_parts), samples


def build_label_svg(
    label: dict,
    r1: float,
    r2: float,
    t1: float,
    t2: float,
    font_size: float,
    color: str,
    font_family: str,
    region_id: str,
) -> tuple[str, str, list[tuple[float, float]]]:
    """Dispatch to curved or straight label rendering based on rotation.

    rotation == 0  → curved text on an elliptical-arc path
    rotation != 0  → straight text rotated by the rotation value

    Returns (text_svg, defs_svg, bbox_samples).  defs_svg is empty in
    straight mode.
    """
    if label["rotation"] == 0:
        return _build_label_curved(
            label, r1, r2, t1, t2, font_size, color, font_family, region_id,
        )
    theta_mid = (t1 + t2) / 2.0
    text_svg, samples = _build_label_straight(
        label, r1, r2, theta_mid, font_size, color, font_family,
    )
    return text_svg, "", samples


# --- Per-region rendering --------------------------------------------


def _merge_defaults(defaults: dict, region: dict) -> dict:
    """Return a dict with defaults merged under region overrides."""
    merged = dict(defaults)
    for k, v in region.items():
        if k != "label":
            merged[k] = v
    return merged


def build_region_svg(
    region: dict, geometry: dict, defaults: dict, region_idx: int,
) -> tuple[str, str, list[tuple[float, float]]]:
    """Return (body_svg, defs_svg, bbox_samples) for one region.

    body_svg contains the ribbon <path> and any label <text> elements;
    defs_svg contains any <path> definitions needed for curved labels
    (empty when no curved labels are used).
    """
    merged = _merge_defaults(defaults, region)
    t1 = float(region["t1"])
    t2 = float(region["t2"])
    r1 = float(geometry["r1"])
    r2 = float(geometry["r2"])
    w = float(geometry["w"])

    path_d, ribbon_samples = build_ribbon_path_d(r1, r2, w, t1, t2)

    opacity = float(merged.get("opacity", 1.0))
    if not 0.0 <= opacity <= 1.0:
        raise ValueError(
            f"region '{region.get('name', '?')}' opacity must be in [0, 1]; got {opacity}"
        )
    opacity_attr = f' opacity="{opacity:.4f}"' if opacity != 1.0 else ""

    name = region.get("name", "")
    name_attr = f' data-name="{_xml_escape(name)}"' if name else ""

    path_svg = (
        f'  <path{name_attr} d="{path_d}" '
        f'fill="{merged.get("fill_color", "none")}" '
        f'stroke="{merged.get("stroke_color", "#222222")}" '
        f'stroke-width="{merged.get("stroke_size", 0.02)}" '
        f'stroke-linejoin="miter" stroke-linecap="butt"{opacity_attr} />\n'
    )

    all_samples = list(ribbon_samples)

    label_norm = _normalize_label(region.get("label"))
    if label_norm is not None:
        region_id = f"{_sanitize_id(name)}-{region_idx}" if name else f"region-{region_idx}"
        label_text_svg, label_defs_svg, label_samples = build_label_svg(
            label=label_norm,
            r1=r1, r2=r2, t1=t1, t2=t2,
            font_size=float(merged.get("label_font_size", 0.15)),
            color=str(merged.get("label_color", "#333333")),
            font_family=str(merged.get(
                "label_font_family",
                BUILT_IN_DEFAULTS["label_font_family"],
            )),
            region_id=region_id,
        )
        all_samples.extend(label_samples)
        return path_svg + label_text_svg, label_defs_svg, all_samples

    return path_svg, "", all_samples


# --- Top-level rendering ---------------------------------------------


def render_atlas(config: dict) -> str:
    """Build the full SVG document from a parsed config dict.

    Canvas behavior:
      - If ``config["canvas"]`` is absent, the SVG auto-sizes to the
        content bounding box plus ``geometry.margin``.
      - If ``config["canvas"] = {"width": W, "height": H}`` is given,
        the SVG's outer width and height are fixed at W × H inches and
        the viewBox is sized identically (1 user unit = 1 inch).  This
        means font-size values in inches render at their physical size
        (e.g. 11pt → 0.1528 in renders as 11pt).  The viewBox is
        positioned to centre on the content's centroid by default;
        provide ``canvas.viewbox_origin = {"x": ..., "y": ...}`` to
        override.  Content extending beyond the viewBox is clipped.
    """
    geometry = config["geometry"]
    defaults = dict(BUILT_IN_DEFAULTS)
    defaults.update(config.get("defaults", {}))

    bodies: list[str] = []
    defs_blocks: list[str] = []
    all_samples: list[tuple[float, float]] = []
    for idx, region in enumerate(config["regions"]):
        body_svg, defs_svg, samples = build_region_svg(
            region, geometry, defaults, region_idx=idx,
        )
        bodies.append(body_svg)
        if defs_svg:
            defs_blocks.append(defs_svg)
        all_samples.extend(samples)

    if not all_samples:
        raise ValueError("config produced no regions to render")

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


# --- CLI -------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Render a vocal-tract region atlas from a JSON config.",
    )
    parser.add_argument("config", help="path to the JSON config file")
    parser.add_argument(
        "--output", "-o",
        help="output SVG path; default is ../build/vocal_tract/<config-name>.svg",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))

    if args.output:
        out_path = Path(args.output)
    else:
        name = config.get("name", config_path.stem)
        out_path = DEFAULT_OUTPUT_DIR / f"{name}.svg"

    svg = render_atlas(config)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg, encoding="utf-8")
    print(f"Wrote {out_path}  ({len(svg)} bytes)")


if __name__ == "__main__":
    main()

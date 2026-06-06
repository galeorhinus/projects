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
The label sits at the angular midpoint of the region on the centerline
ellipse (r1, r2), rotated to be parallel to the ribbon, and centered on
that point (``dominant-baseline="middle"``, ``text-anchor="middle"``).

If the tangent angle would put the text upside-down, the script flips
it by 180° to keep it readable.

``offset.x`` and ``offset.y`` move the label in world-aligned semantic
coordinates: ``+x`` runs along the ribbon (direction of increasing θ,
i.e. visually clockwise), ``+y`` runs outward from the ellipse center.
``rotation`` is added on top of the auto-computed (and possibly flipped)
tangent angle.

Multi-line labels: pass ``text`` as a list of strings.  The lines are
balanced vertically around the position point.
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


def build_label_svg(
    label: dict,
    r1: float,
    r2: float,
    theta_mid_deg: float,
    font_size: float,
    color: str,
    font_family: str,
) -> tuple[str, list[tuple[float, float]]]:
    """Return SVG <text> fragment for a label, plus sample points for bbox."""
    final_x, final_y, rotation_deg = compute_label_transform(
        r1=r1, r2=r2, theta_mid_deg=theta_mid_deg,
        offset_x=label["offset_x"], offset_y=label["offset_y"],
        extra_rotation_deg=label["rotation"],
    )

    lines = label["lines"]
    n = len(lines)
    line_em = 1.2  # baseline-to-baseline distance (em units)
    # Stack the n lines balanced vertically around y=0 in the local frame.
    # First line's dy gets us to the top baseline; subsequent dy=1.2em each.
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

    # Bounding-box samples: rough estimate of the label box.  Width is hard
    # to estimate without text metrics; use a heuristic based on longest
    # line and font size.
    longest = max((len(line) for line in lines), default=0)
    half_w = 0.5 * font_size * longest * 0.6  # 0.6 ≈ avg glyph width / em
    half_h = 0.5 * font_size * (n * line_em)

    # Sample the four corners of the (unrotated) label box, then rotate.
    cos_r = math.cos(math.radians(rotation_deg))
    sin_r = math.sin(math.radians(rotation_deg))
    samples = []
    for dx, dy in [(-half_w, -half_h), (half_w, -half_h),
                   (half_w, half_h), (-half_w, half_h)]:
        wx = final_x + dx * cos_r - dy * sin_r
        wy = final_y + dx * sin_r + dy * cos_r
        samples.append((wx, wy))
    return text_svg, samples


# --- Per-region rendering --------------------------------------------


def _merge_defaults(defaults: dict, region: dict) -> dict:
    """Return a dict with defaults merged under region overrides."""
    merged = dict(defaults)
    for k, v in region.items():
        if k != "label":
            merged[k] = v
    return merged


def build_region_svg(
    region: dict, geometry: dict, defaults: dict,
) -> tuple[str, list[tuple[float, float]]]:
    """Return SVG fragment (path + optional label) for one region."""
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
        theta_mid = (t1 + t2) / 2.0
        label_svg, label_samples = build_label_svg(
            label=label_norm,
            r1=r1, r2=r2, theta_mid_deg=theta_mid,
            font_size=float(merged.get("label_font_size", 0.15)),
            color=str(merged.get("label_color", "#333333")),
            font_family=str(merged.get(
                "label_font_family",
                BUILT_IN_DEFAULTS["label_font_family"],
            )),
        )
        all_samples.extend(label_samples)
        return path_svg + label_svg, all_samples

    return path_svg, all_samples


# --- Top-level rendering ---------------------------------------------


def render_atlas(config: dict) -> str:
    """Build the full SVG document from a parsed config dict."""
    geometry = config["geometry"]
    defaults = dict(BUILT_IN_DEFAULTS)
    defaults.update(config.get("defaults", {}))

    margin = float(geometry.get("margin", 0.1))

    fragments: list[str] = []
    all_samples: list[tuple[float, float]] = []
    for region in config["regions"]:
        frag, samples = build_region_svg(region, geometry, defaults)
        fragments.append(frag)
        all_samples.extend(samples)

    if not all_samples:
        raise ValueError("config produced no regions to render")

    xmin = min(p[0] for p in all_samples) - margin
    xmax = max(p[0] for p in all_samples) + margin
    ymin = min(p[1] for p in all_samples) - margin
    ymax = max(p[1] for p in all_samples) + margin
    width_in = xmax - xmin
    height_in = ymax - ymin

    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width_in:.4f}in" height="{height_in:.4f}in" '
        f'viewBox="{xmin:.4f} {ymin:.4f} {width_in:.4f} {height_in:.4f}">\n'
        + "".join(fragments)
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

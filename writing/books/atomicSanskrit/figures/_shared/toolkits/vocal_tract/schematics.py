"""Shape primitives for vocal-tract schematics.

The book's vocal-tract schematics (Ch 7 adivadya, Ch 8 mapping the
mouth, Appendix Part 3 audiography, and adjacent figures) are built
from a small set of geometric primitives.  This script generates one
of them: an elliptical ribbon arc — a band of width w that traces an
arc along an ellipse with semi-axes (r1, r2).  Suitable for hard
palate, soft palate, tongue surfaces, pharyngeal wall, lip outlines,
and other organ-shape arcs that read naturally as portions of ellipses.

Inputs are in inches (so SVGs render at physical size when opened in
Illustrator or a browser); angles are in degrees.

Add additional primitive generators to this file as new shapes are
needed (straight-edge ribbons, blob shapes, dot markers, etc.) so the
vocal-tract schematic kit stays in one place.

Angle convention
----------------
    0°    = 6 o'clock (straight down)
    90°   = 9 o'clock (left)
    180°  = 12 o'clock (top)
    270°  = 3 o'clock (right)
Angles increase clockwise (matches a wall-clock face read in the natural
direction; 0° is the chin position on a head-cross-section diagram).

For an ellipse with semi-axes (a, b), the point at angle θ (parametric)
is (-a·sin θ, b·cos θ) in SVG y-down coordinates.  The angle equals the
polar angle when a = b (circle); for a ≠ b they differ but the
construction stays simple.

Ribbon width
------------
The inner and outer edges are concentric scaled ellipses:
    inner: (r1 - w/2, r2 - w/2)
    outer: (r1 + w/2, r2 + w/2)
For a circle (r1 = r2), the perpendicular width is exactly w everywhere.
For an ellipse, the perpendicular width equals w along the semi-axes
and varies slightly elsewhere — radial scaling is not the same as a
true perpendicular offset (which would not be representable with SVG
arc commands).

Example
-------
    python3 schematics.py --r1 3.25 --r2 3.25 --w 0.5 \\
        --t1 120 --t2 240 --output output/upper_arch.svg
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path


def point_at(rx: float, ry: float, theta_deg: float) -> tuple[float, float]:
    """SVG-coord point on the ellipse (rx, ry) at angle theta.

    theta is measured in degrees CLOCKWISE from 6 o'clock.  In SVG y-down
    coords the point is (-rx·sin θ, ry·cos θ):

        θ=0   → (0, +ry)   (6 o'clock — down)
        θ=90  → (-rx, 0)   (9 o'clock — left)
        θ=180 → (0, -ry)   (12 o'clock — top)
        θ=270 → (+rx, 0)   (3 o'clock — right)
    """
    theta = math.radians(theta_deg)
    return (-rx * math.sin(theta), ry * math.cos(theta))


def tangent_at(rx: float, ry: float, theta_deg: float) -> tuple[float, float]:
    """Unit tangent vector to the ellipse (rx, ry) at angle theta.

    Tangent direction = d/dθ of (-rx·sin θ, ry·cos θ) = (-rx·cos θ, -ry·sin θ),
    then normalized.  In SVG y-down coords.  Tangent points in the
    direction of increasing θ (visually clockwise).
    """
    theta = math.radians(theta_deg)
    tx = -rx * math.cos(theta)
    ty = -ry * math.sin(theta)
    mag = math.hypot(tx, ty)
    if mag == 0:
        return (0.0, 0.0)
    return (tx / mag, ty / mag)


def outward_normal_at(rx: float, ry: float, theta_deg: float) -> tuple[float, float]:
    """Unit outward-normal vector to the ellipse at angle theta.

    Computed as the 90° CCW rotation of the tangent in SVG y-down coords:
    (tx, ty) → (ty, -tx).  Points away from the ellipse center.

    (For the clockwise angle convention, the curve runs in the opposite
    direction along the ellipse compared to a CCW parametrization, so
    "outward" sits on the 90° CCW side of the tangent rather than the
    90° CW side.)
    """
    tx, ty = tangent_at(rx, ry, theta_deg)
    return (ty, -tx)


def build_ribbon_path_d(
    r1: float, r2: float, w: float, t1: float, t2: float,
) -> tuple[str, list[tuple[float, float]]]:
    """Build the SVG path 'd' attribute for an elliptical ribbon arc.

    Returns (path_d, bbox_samples).  bbox_samples is a list of points on
    the ribbon's outer envelope, suitable for bounding-box computation by
    the caller (so multiple ribbons can be composed and unioned).
    """
    # Normalize so t1 < t2 (increasing angle goes CCW from t1 to t2).
    if t2 < t1:
        t1, t2 = t2, t1
    if w < 0:
        raise ValueError("ribbon width w must be non-negative")
    if r1 - w / 2 <= 0 or r2 - w / 2 <= 0:
        raise ValueError(
            f"inner ellipse would have non-positive semi-axis "
            f"(r1={r1}, r2={r2}, w={w}); reduce w or increase r1/r2"
        )

    in_rx, in_ry = r1 - w / 2, r2 - w / 2
    out_rx, out_ry = r1 + w / 2, r2 + w / 2

    sweep_deg = t2 - t1
    large_arc = 1 if sweep_deg > 180 else 0
    # In SVG y-down, sweep_flag=1 traces visually clockwise.
    # Under the clockwise angle convention, t1 → t2 (increasing θ) is CW.
    sweep_inner = 1  # t1 → t2 (CW)
    sweep_outer = 0  # t2 → t1 (CCW back)

    p_inner_start = point_at(in_rx, in_ry, t1)
    p_inner_end = point_at(in_rx, in_ry, t2)
    p_outer_start = point_at(out_rx, out_ry, t1)
    p_outer_end = point_at(out_rx, out_ry, t2)

    # Sample arc extremes for bounding box.
    samples: list[tuple[float, float]] = []
    for theta in (t1, t2):
        samples.append(point_at(in_rx, in_ry, theta))
        samples.append(point_at(out_rx, out_ry, theta))
    for angle in (0, 90, 180, 270, 360, 450, 540, 630, 720):
        if t1 <= angle <= t2:
            samples.append(point_at(in_rx, in_ry, angle))
            samples.append(point_at(out_rx, out_ry, angle))

    path_d = (
        f"M {p_inner_start[0]:.4f} {p_inner_start[1]:.4f} "
        f"A {in_rx:.4f} {in_ry:.4f} 0 {large_arc} {sweep_inner} "
        f"{p_inner_end[0]:.4f} {p_inner_end[1]:.4f} "
        f"L {p_outer_end[0]:.4f} {p_outer_end[1]:.4f} "
        f"A {out_rx:.4f} {out_ry:.4f} 0 {large_arc} {sweep_outer} "
        f"{p_outer_start[0]:.4f} {p_outer_start[1]:.4f} Z"
    )
    return path_d, samples


def elliptical_ribbon_svg(
    r1: float,
    r2: float,
    w: float,
    t1: float,
    t2: float,
    *,
    stroke_color: str = "#cc3333",
    stroke_size: float = 0.02,
    fill_color: str = "none",
    opacity: float = 1.0,
    margin: float = 0.1,
) -> str:
    """Build the full SVG document for a single elliptical ribbon arc."""
    if not 0.0 <= opacity <= 1.0:
        raise ValueError(f"opacity must be in [0, 1]; got {opacity}")

    path_d, samples = build_ribbon_path_d(r1, r2, w, t1, t2)

    xmin = min(p[0] for p in samples) - margin
    xmax = max(p[0] for p in samples) + margin
    ymin = min(p[1] for p in samples) - margin
    ymax = max(p[1] for p in samples) + margin
    width_in = xmax - xmin
    height_in = ymax - ymin

    opacity_attr = f' opacity="{opacity:.4f}"' if opacity != 1.0 else ""
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width_in:.4f}in" height="{height_in:.4f}in" '
        f'viewBox="{xmin:.4f} {ymin:.4f} {width_in:.4f} {height_in:.4f}">\n'
        f'  <path d="{path_d}" '
        f'fill="{fill_color}" stroke="{stroke_color}" '
        f'stroke-width="{stroke_size}" '
        f'stroke-linejoin="miter" stroke-linecap="butt"{opacity_attr} />\n'
        f'</svg>\n'
    )


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--r1", type=float, required=True,
                        help="horizontal semi-axis of the centerline ellipse (inches)")
    parser.add_argument("--r2", type=float, required=True,
                        help="vertical semi-axis of the centerline ellipse (inches)")
    parser.add_argument("--w", type=float, required=True,
                        help="ribbon width (inches)")
    parser.add_argument("--t1", type=float, required=True,
                        help="start angle (degrees, CCW from 6 o'clock)")
    parser.add_argument("--t2", type=float, required=True,
                        help="end angle (degrees, CCW from 6 o'clock)")
    parser.add_argument("--output", "-o", required=True,
                        help="output SVG file path")
    parser.add_argument("--stroke-color", default="#cc3333",
                        help="stroke color, any CSS color or hex (default: #cc3333)")
    parser.add_argument("--stroke-size", type=float, default=0.02,
                        help="stroke width in inches (default: 0.02)")
    parser.add_argument("--fill-color", default="none",
                        help="fill color, any CSS color or hex (default: none)")
    parser.add_argument("--opacity", type=float, default=1.0,
                        help="overall opacity, 0.0 transparent to 1.0 opaque (default: 1.0)")
    parser.add_argument("--margin", type=float, default=0.1,
                        help="margin around shape in inches (default: 0.1)")
    args = parser.parse_args()

    svg = elliptical_ribbon_svg(
        r1=args.r1, r2=args.r2, w=args.w, t1=args.t1, t2=args.t2,
        stroke_color=args.stroke_color, stroke_size=args.stroke_size,
        fill_color=args.fill_color, opacity=args.opacity,
        margin=args.margin,
    )
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg, encoding="utf-8")
    print(f"Wrote {out_path}  ({len(svg)} bytes)")


if __name__ == "__main__":
    main()

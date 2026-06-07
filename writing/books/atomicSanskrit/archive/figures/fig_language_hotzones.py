"""Render Ch7 Figure 7.2: language hotzones along the vocal tract.

The figure collapses the existing place/manner scatter matrices into a
place-only bubble chart.  Each bubble's area is proportional to the number
of consonants selected at that place of articulation.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_DIR = SCRIPT_DIR / "configs"
OUTPUT_PATH = (
    SCRIPT_DIR.parent
    / "build"
    / "vocal_tract"
    / "language_hotzones_along_vocal_tract.svg"
)

FONT = "'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"

PLACES = [
    "bilabial",
    "labio-dental",
    "interdental",
    "dental",
    "alveolar",
    "post-alveolar",
    "retroflex",
    "palatal",
    "velar",
    "uvular",
    "pharyngeal",
    "glottal",
]

AXIS_LABELS = [
    ("lips", 0.0),
    ("teeth", 1.25),
    ("alveolar", 2.5),
    ("retroflex", 3.8),
    ("palatal", 5.5),
    ("velar", 9.0),
    ("pharynx", 13.5),
    ("glottis", 17.0),
]

RIBBON_LABELS = [
    ("BILAB",),
    ("LABIO", "DENT"),
    ("INTER", "DENT"),
    ("DENT",),
    ("ALV",),
    ("POST", "ALV"),
    ("RETRO",),
    ("PAL",),
    ("VELAR",),
    ("UV",),
    ("PHAR",),
    ("GLOT",),
]

# Average adult vocal-tract distance model from the scatter configs, in cm-ish
# relative units from lips to glottis.  Used only for proportional spacing.
DISTANCES_FROM_LIPS = [
    0.0,
    0.5,
    1.0,
    1.5,
    2.5,
    3.5,
    3.8,
    5.5,
    9.0,
    11.5,
    13.5,
    17.0,
]

PANELS = [
    {
        "title": "English",
        "config": "scatter_english.json",
        "note": "front/mid selection",
    },
    {
        "title": "Arabic",
        "config": "scatter_arabic.json",
        "note": "deep-field spread",
    },
    {
        "title": "Mandarin",
        "config": "scatter_mandarin.json",
        "note": "coronal-palatal density",
    },
    {
        "title": "Zulu",
        "config": "scatter_zulu.json",
        "note": "click mechanisms",
    },
]


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def load_counts(config_name: str) -> list[int]:
    data = json.loads((CONFIG_DIR / config_name).read_text(encoding="utf-8"))
    matrix = data["scatter"]["matrix"]
    width = max(len(row) for row in matrix)
    counts = [0] * width
    for row in matrix:
        for idx, cell in enumerate(row):
            if cell:
                counts[idx] += 1
    return counts


def x_for_distance(distance: float, x0: float, x1: float) -> float:
    return x0 + (distance / max(DISTANCES_FROM_LIPS)) * (x1 - x0)


def x_for_place(index: int, x0: float, x1: float) -> float:
    width = (x1 - x0) / len(PLACES)
    return x0 + (index + 0.5) * width


def arc_point(x: float, x0: float, x1: float, y: float) -> tuple[float, float]:
    """Return a shallow-arc point for the shared axis."""
    return x, arc_y(x, x0, x1, y, 12.0)


def arc_y(x: float, x0: float, x1: float, y: float, amp: float) -> float:
    t = (x - x0) / (x1 - x0)
    return y - amp * math.sin(math.pi * t)


def curve_path(
    xa: float,
    xb: float,
    y: float,
    amp: float,
    global_x0: float | None = None,
    global_x1: float | None = None,
) -> str:
    """Return a sampled shallow-curve SVG path."""
    gx0 = xa if global_x0 is None else global_x0
    gx1 = xb if global_x1 is None else global_x1
    samples = 8
    points = []
    for i in range(samples + 1):
        x = xa + (xb - xa) * (i / samples)
        points.append((x, arc_y(x, gx0, gx1, y, amp)))
    d = f"M {points[0][0]:.1f} {points[0][1]:.1f}"
    for x, yy in points[1:]:
        d += f" L {x:.1f} {yy:.1f}"
    return d


def ribbon_segment_path(
    xa: float,
    xb: float,
    y: float,
    amp: float,
    half_height: float,
    global_x0: float,
    global_x1: float,
) -> str:
    samples = 8
    upper = []
    lower = []
    for i in range(samples + 1):
        x = xa + (xb - xa) * (i / samples)
        yy = arc_y(x, global_x0, global_x1, y, amp)
        upper.append((x, yy - half_height))
        lower.append((x, yy + half_height))
    d = f"M {upper[0][0]:.1f} {upper[0][1]:.1f}"
    for x, yy in upper[1:]:
        d += f" L {x:.1f} {yy:.1f}"
    for x, yy in reversed(lower):
        d += f" L {x:.1f} {yy:.1f}"
    return d + " Z"


def render_ribbon(x0: float, x1: float, y: float) -> str:
    parts: list[str] = []
    col_w = (x1 - x0) / len(PLACES)

    for idx, labels in enumerate(RIBBON_LABELS):
        xa = x0 + idx * col_w
        xb = xa + col_w
        fill = "#e8e8e5" if idx % 2 == 0 else "#dcdcd8"
        parts.append(
            f'<path d="{ribbon_segment_path(xa, xb, y, 5.0, 14.5, x0, x1)}" '
            f'fill="{fill}" stroke="#b4b4b0" stroke-width="0.75" />'
        )

    for idx, labels in enumerate(RIBBON_LABELS):
        xa = x0 + idx * col_w
        xb = xa + col_w
        cx = (xa + xb) / 2.0
        t = (cx - x0) / (x1 - x0)
        cy = arc_y(cx, x0, x1, y, 5.0)
        slope = -5.0 * math.pi / (x1 - x0) * math.cos(math.pi * t)
        angle = math.degrees(math.atan(slope))
        label_offsets = (-3.4, 4.0) if len(labels) > 1 else (0.8,)
        for line_idx, label in enumerate(labels):
            font_size = "7.7" if len(labels) > 1 else "8.5"
            parts.append(
                f'<text x="{cx:.1f}" y="{cy + label_offsets[line_idx]:.1f}" '
                f'transform="rotate({angle:.2f} {cx:.1f} '
                f'{cy + label_offsets[line_idx]:.1f})" '
                f'text-anchor="middle" dominant-baseline="middle" '
                f'font-family="{FONT}" font-size="{font_size}" '
                f'font-weight="700" letter-spacing="0.25" fill="#3d3d3c">'
                f'{esc(label)}</text>'
            )
    parts.append(
        f'<path d="{curve_path(x0, x1, y, 5.0, x0, x1)}" fill="none" '
        f'stroke="#777" stroke-width="0.8" />'
    )
    return "\n".join(parts)


def render_panel_background(idx: int, y: float, panel_x: float, panel_w: float, panel_h: float) -> str:
    # Alternating panel guide, subtle enough to stay book-like.
    fill = "#f2f2f1" if idx % 2 == 0 else "#f7f7f6"
    return (
        f'<rect x="{panel_x:.1f}" y="{y - panel_h / 2:.1f}" '
        f'width="{panel_w:.1f}" height="{panel_h:.1f}" '
        f'fill="{fill}" stroke="#e2e2df" stroke-width="0.65" />'
    )


def render_panel_content(panel: dict, idx: int, y: float, x0: float, x1: float) -> str:
    counts = load_counts(panel["config"])
    max_count = max(counts) or 1

    parts: list[str] = []
    parts.append(
        f'<text x="33" y="{y - 8:.1f}" font-family="{FONT}" '
        f'font-size="15.5" font-weight="700" fill="#2b2b2d">'
        f'{esc(panel["title"])}</text>'
    )
    parts.append(
        f'<text x="33" y="{y + 10:.1f}" font-family="{FONT}" '
        f'font-size="9.8" font-style="italic" fill="#777">'
        f'{esc(panel["note"])}</text>'
    )

    axis_d = (
        f"M {x0:.1f} {y:.1f} "
        f"C {x0 + 84:.1f} {y - 21:.1f}, {x1 - 84:.1f} {y - 21:.1f}, "
        f"{x1:.1f} {y:.1f}"
    )
    parts.append(
        f'<path d="{axis_d}" fill="none" stroke="#b8b8b4" '
        f'stroke-width="1.6" stroke-linecap="round" />'
    )

    for place_idx, (count, place) in enumerate(zip(counts, PLACES)):
        if count <= 0:
            continue
        x = x_for_place(place_idx, x0, x1)
        px, py = arc_point(x, x0, x1, y)
        radius = 3.2 + 11.8 * math.sqrt(count / max_count)
        opacity = 0.34 + 0.36 * (count / max_count)
        parts.append(
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{radius:.2f}" '
            f'fill="#2f3031" opacity="{opacity:.3f}" '
            f'stroke="#2b2b2d" stroke-width="0.8" />'
        )
        parts.append(
            f'<title>{esc(panel["title"])}: {count} at {esc(place)}</title>'
        )

    return "\n".join(parts)


def render_svg() -> str:
    width = 450
    height = 600
    x0, x1 = 134.0, 432.0
    ribbon_y = 91.0
    panel_h = 80.0
    panel_x = 24.0
    panel_w = 412.0
    panel_y = [166.0, 256.0, 346.0, 436.0]

    parts: list[str] = []
    parts.append(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="4.5in" height="6.0in" viewBox="0 0 {width} {height}">'
    )
    parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff" />')

    parts.append(
        f'<text x="{width / 2:.1f}" y="36" text-anchor="middle" '
        f'font-family="{FONT}" font-size="21" font-weight="700" '
        f'fill="#2b2b2d">Language Hotzones Along the Vocal Tract</text>'
    )
    parts.append(
        f'<text x="{width / 2:.1f}" y="57" text-anchor="middle" '
        f'font-family="{FONT}" font-size="11.5" font-style="italic" '
        f'fill="#777">same instrument, different selections</text>'
    )
    parts.append('<line x1="95" y1="67" x2="355" y2="67" stroke="#d2d2ce" />')
    parts.append(render_ribbon(x0, x1, ribbon_y))

    for idx in range(len(PANELS)):
        parts.append(render_panel_background(idx, panel_y[idx], panel_x, panel_w, panel_h))

    guide_start_y = ribbon_y + 15.0
    guide_end_y = panel_y[-1] + panel_h / 2.0
    for place_idx in range(len(PLACES)):
        x = x_for_place(place_idx, x0, x1)
        parts.append(
            f'<line x1="{x:.1f}" y1="{guide_start_y:.1f}" '
            f'x2="{x:.1f}" y2="{guide_end_y:.1f}" '
            f'stroke="#b7b7b3" stroke-width="0.7" '
            f'stroke-dasharray="2 4" opacity="0.72" />'
        )

    for idx, panel in enumerate(PANELS):
        parts.append(render_panel_content(panel, idx, panel_y[idx], x0, x1))

    parts.append(
        f'<circle cx="48" cy="565" r="5.5" fill="#2f3031" opacity="0.42" '
        f'stroke="#2b2b2d" stroke-width="0.7" />'
        f'<circle cx="75" cy="565" r="12.5" fill="#2f3031" opacity="0.56" '
        f'stroke="#2b2b2d" stroke-width="0.7" />'
        f'<text x="96" y="569" font-family="{FONT}" font-size="9.8" '
        f'font-style="italic" fill="#777">'
        f'bubble area tracks consonant count at that region</text>'
    )
    parts.append("</svg>\n")
    return "\n".join(parts)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_svg(), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

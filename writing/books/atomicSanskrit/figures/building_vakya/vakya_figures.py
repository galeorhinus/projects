#!/usr/bin/env python3
"""Generate Chapter 12 SVG figures.

The figures extend the Ch10/Ch11 hexagon grammar into the *śabda*,
*padam*, and *vākya* scale. They intentionally stay schematic where full
Pāṇinian derivation would distract from the chapter's procedural claim.
"""

from __future__ import annotations

import html
import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_DIR = Path(__file__).resolve().parent
# working/50_projects/dhatu_hexagons since the 2026-08-17 reorg; the old
# working/dhatu_hexagons path left here was stale and would have failed on a
# clean checkout (it only kept working because a stale __pycache__ satisfied
# the import locally).
sys.path.insert(0, str(REPO_ROOT / "working" / "50_projects" / "dhatu_hexagons"))
sys.path.insert(0, str(REPO_ROOT / "figures" / "_shared"))

import matra_style as ms  # noqa: E402
from dhatu_hexagon import EDGE_LENGTH, HEX_HEIGHT, VARNAS, is_ayogavaha  # noqa: E402

# ---------------------------------------------------------------------------
# Type sizing. Every Ch12 figure is authored on a 900-unit-wide viewBox and
# rendered at 4.5in, so one point is 900 / (4.5 * 72) = 2.778 units and the
# sizes below are literal points on the printed page. The previous figures
# were built with raw unit sizes that worked out to 4.3-8.6pt -- legible on a
# screen at full width, too small in the book. Author sizes in POINTS here and
# let pt_to_px do the conversion, so the intent survives a geometry change.
FIG_W = 900.0
FIG_IN = 4.5


def pt(points: float) -> float:
    """Points on the printed page -> user units on a 900-wide viewBox."""
    return ms.pt_to_px(points, FIG_W, FIG_IN)


PT_DEVA = 11.0    # Devanagari inside tiles
PT_IAST = 10.0    # IAST under each tile
PT_HEAD = 12.0    # figure titles
PT_LABEL = 10.0   # box labels, row labels -- the 10pt floor
PT_GLOSS = 10.0   # secondary glosses; never below PT_LABEL

FS_DEVA = pt(PT_DEVA)
FS_IAST = pt(PT_IAST)
FS_HEAD = pt(PT_HEAD)
FS_LABEL = pt(PT_LABEL)
FS_GLOSS = pt(PT_GLOSS)

# Tile geometry scales with the type so the glyphs keep their margins inside
# the hexagons. EDGE_LENGTH/HEX_HEIGHT are rebound in THIS module only --
# dhatu_hexagon keeps its own values, and figures/building_kriya imports them
# independently, so nothing else moves.
GEOM_SCALE = FS_DEVA / 22.0   # 22 was the old hard-coded Devanagari size
EDGE_LENGTH = EDGE_LENGTH * GEOM_SCALE
HEX_HEIGHT = HEX_HEIGHT * GEOM_SCALE

# Vertical placement of the two labels inside a tile, measured from the tile
# centre. Both glyphs are near their own font size tall, so the offsets have
# to clear half of each plus a gap -- at 11pt/10pt the earlier 0.18/0.72
# multipliers put the IAST inside the Devanagari's descender and the two
# collided. Derived from the sizes rather than hand-tuned so they stay correct
# if PT_DEVA or PT_IAST changes.
DEVA_DY = -(FS_DEVA * 0.52)
IAST_DY = FS_DEVA * 0.30 + FS_IAST * 0.55


DEV_FONT = (
    "Noto Sans Devanagari, Kohinoor Devanagari, Devanagari MT, "
    "Arial Unicode MS, sans-serif"
)
LATIN_FONT = "Charter, Georgia, Times, serif"
HALANT = "्"

# Geometry is locked to the Ch11 timing convention: the visible midpoint
# span of each tile tracks its mātrā value. Scaled with the type (GEOM_SCALE)
# so the mātrā ruler underneath stays proportional to the tiles above it.
MATRA_UNIT = 60 * GEOM_SCALE
WIDTH_C = 10 * GEOM_SCALE
WIDTH_V1 = 40 * GEOM_SCALE
WIDTH_V2 = 100 * GEOM_SCALE

UPPER_RAIL_Y = -HEX_HEIGHT / 4
LOWER_RAIL_Y = HEX_HEIGHT / 4

# Warm palette shared with Chapter 11 (figures/_shared/matra_style.py), adopted
# 2026-08-20 in place of this file's own grayscale set. The four role fills are
# chosen so their *lightness* still separates cleanly when the page is printed
# in grayscale, which is why the figures read correctly either way: tan is
# light, gold is mid, mid-brown is darker, dark-brown is darkest.
TEXT = ms.TEXT            # dark-brown ink for titles
MUTED = ms.MUTED          # secondary brown for glosses and labels
LIGHT = ms.LIGHT_FILL     # tan   — the atom's own varṇas
MID = ms.GOLD             # gold  — transformed / added material
DARK = ms.DARK_FILL       # dark brown — endings and tail-bonds
BLACK = ms.DARK_FILL      # head-bonds share the darkest fill
WHITE = ms.INK_LIGHT      # cream ink on the dark fills
STROKE = ms.STROKE        # tile outline
DASH = ms.RULER

ROLE_FILL = {
    "original": LIGHT,
    "transform": MID,
    "head": BLACK,
    "tail": DARK,
    "role": MID,
    "sentence": "#eeeeee",
    "seed": "#f5f5f5",
    "root": "#cfcfcf",
}

ROLE_TEXT = {
    "original": TEXT,
    "transform": TEXT,
    "head": WHITE,
    "tail": WHITE,
    "role": WHITE,
    "sentence": TEXT,
    "seed": TEXT,
    "root": TEXT,
}

ALIASES = {
    "A": "ā",
    "I": "ī",
    "U": "ū",
    "R": "ṛ",
    "RR": "ṝ",
    "lR": "ḷ",
    "T": "ṭ",
    "Th": "ṭh",
    "D": "ḍ",
    "Dh": "ḍh",
    "N": "ṇ",
    "G": "ṅ",
    "J": "ñ",
    "S": "ṣ",
    "z": "ś",
    # Ch12 uses sonomeric rendering rather than scribal shorthand:
    # anusvāra resolves to the nasal being represented, so the default
    # shortcut M renders as ordinary म्. Use a specific nasal token when the
    # homorganic nasal differs.
    "M": "m",
    "H": "ḥ",
}


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def varna(token: str) -> dict:
    key = ALIASES.get(token, token)
    if key not in VARNAS:
        raise ValueError(f"Unknown varṇa token: {token}")
    return dict(VARNAS[key])


def dev_label(v: dict) -> str:
    if v["class"] == "C" and not is_ayogavaha(v):
        return v["deva"] + HALANT
    return v["deva"]


def width_for(v: dict) -> float:
    if v["class"] == "C":
        return WIDTH_C
    if v["class"] == "V1":
        return WIDTH_V1
    if v["class"] == "V2":
        return WIDTH_V2
    return WIDTH_V1


def rail_for(v: dict) -> float:
    return LOWER_RAIL_Y if v["class"].startswith("V") or is_ayogavaha(v) else UPPER_RAIL_Y


def hex_vertices(cx: float, cy: float, w: float) -> list[tuple[float, float]]:
    e = EDGE_LENGTH
    h = HEX_HEIGHT
    return [
        (cx - w / 2, cy - h / 2),
        (cx + w / 2, cy - h / 2),
        (cx + w / 2 + e / 2, cy),
        (cx + w / 2, cy + h / 2),
        (cx - w / 2, cy + h / 2),
        (cx - w / 2 - e / 2, cy),
    ]


def points(vertices: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in vertices)


def ayogavaha_vertices(cx: float, cy: float) -> dict[str, tuple[float, float]]:
    e = EDGE_LENGTH
    h = HEX_HEIGHT
    return {
        "top_right": (cx + 3 * e / 4, cy - h / 2),
        "bottom_right": (cx + 3 * e / 4, cy + h / 2),
        "top_outer": (cx - 3 * e / 4, cy - h / 2),
        "socket": (cx - e / 4, cy),
        "bottom_outer": (cx - 3 * e / 4, cy + h / 2),
    }


def render_text(
    x: float,
    y: float,
    content: str,
    size: float,
    fill: str = TEXT,
    anchor: str = "middle",
    weight: str = "400",
    style: str = "normal",
    family: str = LATIN_FONT,
    baseline: str = "middle",
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" '
        f'font-size="{size}" font-weight="{weight}" font-style="{style}" '
        f'text-anchor="{anchor}" dominant-baseline="{baseline}" fill="{fill}">'
        f"{esc(content)}</text>"
    )


def render_arrow(x1: float, y1: float, x2: float, y2: float, dashed: bool = False) -> str:
    dash = ' stroke-dasharray="5,4"' if dashed else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arrow)"{dash}/>'
    )


def varna_fill(v: dict) -> tuple[str, str]:
    """(fill, ink) for a varṇa by class, following the Ch10 convention in
    figures/building_dhatuh/matra_envelope.py and racana_scaffold.py:
    vowels take the light tan, consonants the dark brown, and the ink flips
    to stay legible on each. The two fills also separate by lightness in
    grayscale, so the vowel/consonant reading survives a mono print."""
    is_v = v["class"].startswith("V") or is_ayogavaha(v)
    return (ms.LIGHT_FILL, ms.INK_DARK) if is_v else (ms.DARK_FILL, ms.INK_LIGHT)


def render_hex(cx: float, cy: float, v: dict, role: str = "original") -> str:
    if is_ayogavaha(v):
        return render_ayogavaha(cx, cy, v, role)
    # `original` means "no special provenance to signal", so the tile falls
    # back to the vowel/consonant colouring. Any other role (head-bond,
    # tail-bond, transformed material) still overrides it, because there the
    # provenance is the point the figure is making.
    if role == "original":
        fill, text_fill = varna_fill(v)
    else:
        fill = ROLE_FILL.get(role, LIGHT)
        text_fill = ROLE_TEXT.get(role, TEXT)
    w = width_for(v)
    fragments = [
        f'<polygon points="{points(hex_vertices(cx, cy, w))}" fill="{fill}" '
        f'stroke="{STROKE}" stroke-width="1.5" stroke-linejoin="round"/>',
        render_text(cx, cy + DEVA_DY, dev_label(v), FS_DEVA, text_fill,
                    family=DEV_FONT, weight="600"),
        render_text(cx, cy + IAST_DY, v["iast"], FS_IAST, text_fill,
                    style="italic"),
    ]
    return "\n  ".join(fragments)


def render_ayogavaha(cx: float, cy: float, v: dict, role: str = "original") -> str:
    verts = ayogavaha_vertices(cx, cy)
    tr = verts["top_right"]
    br = verts["bottom_right"]
    to = verts["top_outer"]
    socket = verts["socket"]
    bo = verts["bottom_outer"]
    fill = ROLE_FILL.get(role, LIGHT)
    text_fill = ROLE_TEXT.get(role, TEXT)
    mark_x = cx + EDGE_LENGTH / 4
    path_start = (
        f"M {tr[0]:.1f},{tr[1]:.1f} "
        f"L {to[0]:.1f},{to[1]:.1f} "
        f"L {socket[0]:.1f},{socket[1]:.1f} "
        f"L {bo[0]:.1f},{bo[1]:.1f} "
        f"L {br[0]:.1f},{br[1]:.1f} "
    )
    if v["voicing"] == "anusvara":
        right_x = tr[0]
        path = (
            path_start
            + f"C {right_x + 8:.1f},{cy + HEX_HEIGHT / 4:.1f} "
            + f"{right_x - 8:.1f},{cy + HEX_HEIGHT / 8:.1f} "
            + f"{right_x:.1f},{cy:.1f} "
            + f"C {right_x + 8:.1f},{cy - HEX_HEIGHT / 8:.1f} "
            + f"{right_x - 8:.1f},{cy - HEX_HEIGHT / 4:.1f} "
            + f"{tr[0]:.1f},{tr[1]:.1f} Z"
        )
    else:
        path = path_start + "Z"
    fragments = [
        f'<path d="{path}" fill="{fill}" stroke="{STROKE}" '
        f'stroke-width="1.5" stroke-linejoin="round"/>',
    ]
    dot_fill = WHITE if role in ("head", "tail", "role") else TEXT
    if v["voicing"] == "anusvara":
        fragments.append(f'<circle cx="{mark_x:.1f}" cy="{cy - HEX_HEIGHT / 7:.1f}" r="5.0" fill="{dot_fill}"/>')
    else:
        fragments.append(f'<circle cx="{mark_x:.1f}" cy="{cy - 8:.1f}" r="4.5" fill="{dot_fill}"/>')
        fragments.append(f'<circle cx="{mark_x:.1f}" cy="{cy + 8:.1f}" r="4.5" fill="{dot_fill}"/>')
    fragments.append(render_text(mark_x, cy + 23, v["iast"], 11, text_fill, style="italic"))
    return "\n  ".join(fragments)


def display_units(tokens: list[str], role: str) -> list[dict]:
    units: list[dict] = []
    particles = [varna(t) for t in tokens]
    i = 0
    while i < len(particles):
        current = particles[i]
        if current["class"] == "C" and not is_ayogavaha(current):
            run = [current]
            j = i + 1
            while j < len(particles) and particles[j]["class"] == "C" and not is_ayogavaha(particles[j]):
                run.append(particles[j])
                j += 1
            if len(run) > 1:
                units.append({"kind": "cluster", "parts": run, "role": role})
                i = j
                continue
        units.append({"kind": "particle", "particle": current, "role": role})
        i += 1
    return units


def unit_width(unit: dict) -> float:
    if unit["kind"] == "cluster":
        n = len(unit["parts"])
        return n * 0.5 * MATRA_UNIT - EDGE_LENGTH / 2
    return width_for(unit["particle"])


def unit_rail(unit: dict) -> float:
    if unit["kind"] == "cluster":
        return UPPER_RAIL_Y
    return rail_for(unit["particle"])


def unit_is_ayogavaha(unit: dict) -> bool:
    return unit["kind"] == "particle" and is_ayogavaha(unit["particle"])


def layout_units(units: list[dict]) -> list[dict]:
    out: list[dict] = []
    for i, unit in enumerate(units):
        cy = unit_rail(unit)
        w = unit_width(unit)
        if i == 0:
            cx = 0.0
        else:
            prev = out[-1]
            spacing = EDGE_LENGTH / 2 if (prev["cy"] != cy or unit_is_ayogavaha(unit)) else EDGE_LENGTH
            cx = prev["cx"] + (prev["w"] + w) / 2 + spacing
        out.append({**unit, "cx": cx, "cy": cy, "w": w})
    return out


def render_cluster(cx: float, cy: float, parts: list[dict], role: str) -> str:
    w = EDGE_LENGTH * len(parts) / 2
    # A cluster is consonants by definition, so it takes the consonant fill
    # from the same vowel/consonant convention render_hex follows.
    if role == "original":
        fill, ink = ms.DARK_FILL, ms.INK_LIGHT
    else:
        fill, ink = ROLE_FILL.get(role, LIGHT), ROLE_TEXT.get(role, TEXT)
    fragments = [
        f'<polygon points="{points(hex_vertices(cx, cy, w))}" fill="{fill}" '
        f'stroke="{STROKE}" stroke-width="1.5" stroke-linejoin="round"/>'
    ]

    # A cluster is ONE timing envelope holding MORE THAN ONE sonomer, so it
    # is drawn as one wide hexagon divided internally: the divider shows the
    # count, the conjunct shows the spelling. The envelope carries the timing
    # (total_matras counts 0.5 per part). Changed 2026-08-20.
    n = len(parts)
    left = cx - w / 2 - EDGE_LENGTH / 2
    right = cx + w / 2 + EDGE_LENGTH / 2
    span = right - left
    for i in range(1, n):
        # Divider stops short of the outline top and bottom so it reads as an
        # internal division of one tile, not as separate tiles butted
        # together. It carries the sonomer count -- two half-mātrā slots --
        # while the conjunct below carries the orthography.
        dx = left + span * i / n
        inset = HEX_HEIGHT * 0.30
        fragments.append(
            f'<line x1="{dx:.1f}" y1="{cy - HEX_HEIGHT / 2 + inset:.1f}" '
            f'x2="{dx:.1f}" y2="{cy + HEX_HEIGHT / 2 - inset:.1f}" '
            f'stroke="{ink}" stroke-width="0.9" stroke-dasharray="3 2" opacity="0.55"/>'
        )
    # The written form is the conjunct, so it is drawn as one ligature
    # centred across the whole envelope rather than as per-half glyphs with
    # visible halants: ष्य, not ष् | य्. Devanagari joins these consonants,
    # and a figure that pulled them apart on the page would be showing a
    # spelling Sanskrit does not use. The divider above already tells the
    # reader the envelope holds two sonomers.
    conjunct_dev = HALANT.join(p["deva"] for p in parts) + HALANT
    conjunct_iast = "".join(p["iast"] for p in parts)
    fragments.append(
        render_text(cx, cy + DEVA_DY, conjunct_dev, FS_DEVA, ink,
                    family=DEV_FONT, weight="600")
    )
    fragments.append(
        render_text(cx, cy + IAST_DY, conjunct_iast, FS_IAST, ink, style="italic")
    )
    return "\n  ".join(fragments)


def render_unit(unit: dict, dx: float, dy: float, role_override: str | None = None) -> str:
    cx = unit["cx"] + dx
    cy = unit["cy"] + dy
    role = role_override or unit["role"]
    if unit["kind"] == "cluster":
        return render_cluster(cx, cy, unit["parts"], role)
    return render_hex(cx, cy, unit["particle"], role)


def strip_extent(layout: list[dict]) -> tuple[float, float, float, float]:
    xs: list[float] = []
    ys: list[float] = []
    for unit in layout:
        xs.extend([unit["cx"] - unit["w"] / 2 - EDGE_LENGTH / 2, unit["cx"] + unit["w"] / 2 + EDGE_LENGTH / 2])
        ys.extend([unit["cy"] - HEX_HEIGHT / 2, unit["cy"] + HEX_HEIGHT / 2])
    return min(xs), min(ys), max(xs), max(ys)


def total_matras(units: list[dict]) -> float:
    total = 0.0
    for unit in units:
        if unit["kind"] == "cluster":
            total += 0.5 * len(unit["parts"])
            continue
        particle = unit["particle"]
        if particle["class"] == "V2":
            total += 2.0
        elif particle["class"] == "V1":
            total += 1.0
        else:
            total += 0.5
    return total


def render_matra_line(left_tip_x: float, line_y: float, n_matras: float) -> tuple[str, float]:
    """Render the Ch10/Ch11 half-mātrā ruler under a word strip."""
    if n_matras <= 0:
        return "", left_tip_x
    start_x = left_tip_x + EDGE_LENGTH / 4
    end_x = start_x + n_matras * MATRA_UNIT
    color = "#888888"
    fragments = [
        f'<line x1="{start_x:.1f}" y1="{line_y:.1f}" '
        f'x2="{end_x:.1f}" y2="{line_y:.1f}" '
        f'stroke="{color}" stroke-width="1.2"/>'
    ]
    for i in range(int(round(n_matras * 2)) + 1):
        x = start_x + i * MATRA_UNIT / 2
        major = i % 2 == 0
        tick_len = 8 if major else 4
        tick_w = 1.2 if major else 1.0
        fragments.append(
            f'<line x1="{x:.1f}" y1="{line_y:.1f}" '
            f'x2="{x:.1f}" y2="{line_y - tick_len:.1f}" '
            f'stroke="{color}" stroke-width="{tick_w}"/>'
        )
    return "\n  ".join(fragments), end_x


def render_strip(
    words: list[list[str]],
    x: float,
    y: float,
    role: str = "original",
    word_gap: float = 46,
    labels: list[str] | None = None,
    label_size: float = 20,
    show_matra: bool = True,
) -> tuple[str, tuple[float, float, float, float]]:
    fragments: list[str] = []
    cursor = x
    total_min_x = math.inf
    total_min_y = math.inf
    total_max_x = -math.inf
    total_max_y = -math.inf
    for idx, tokens in enumerate(words):
        layout = layout_units(display_units(tokens, role))
        min_x, min_y, max_x, max_y = strip_extent(layout)
        dx = cursor - min_x
        for unit in layout:
            fragments.append(render_unit(unit, dx, y))
        if show_matra:
            matra_line, matra_end = render_matra_line(min_x + dx, max_y + y + 12, total_matras(layout))
            fragments.append(matra_line)
            total_max_x = max(total_max_x, matra_end + 6)
        if labels:
            label_y = max_y + y + (32 if show_matra else 26)
            fragments.append(
                render_text(
                    (min_x + max_x) / 2 + dx,
                    label_y,
                    labels[idx],
                    label_size,
                    MUTED,
                    weight="600",
                    style="italic",
                    family=DEV_FONT,
                )
            )
            total_max_y = max(total_max_y, label_y + 10)
        total_min_x = min(total_min_x, min_x + dx)
        total_max_x = max(total_max_x, max_x + dx)
        total_min_y = min(total_min_y, min_y + y)
        total_max_y = max(total_max_y, max_y + y + (20 if show_matra else 0))
        cursor += (max_x - min_x) + word_gap
    return "\n  ".join(fragments), (total_min_x, total_min_y, total_max_x, total_max_y)


def defs() -> str:
    return (
        "<defs>"
        '<marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" '
        'orient="auto" markerUnits="strokeWidth">'
        f'<path d="M0,0 L9,4.5 L0,9 Z" fill="{MUTED}"/>'
        "</marker>"
        "</defs>"
    )


def svg_doc(width: float, height: float, body: str, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}">\n'
        f"<title>{esc(title)}</title>\n"
        f"{defs()}\n"
        '<rect width="100%" height="100%" fill="white"/>\n'
        f"{body}\n"
        "</svg>\n"
    )


def write_svg(name: str, width: float, height: float, body: str, title: str) -> None:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    out = BUILD_DIR / f"{name.removeprefix("building_vakya_")}.from-py.svg"
    out.write_text(svg_doc(width, height, body, title), encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO_ROOT)}")


def label_box(x: float, y: float, w: float, h: float,
              dev: str, iast: str, english: str) -> str:
    """A named stage in three registers: Devanagari, IAST, plain English.

    The three slots are at fixed heights in every box, so the Devanagari sits
    on one line across the figure, the IAST on the next, and the English on
    the third. `dev` may be empty -- the sonomer tile is the book's own
    English coinage and gets no Devanagari line -- and the slot stays
    reserved so the other two registers still line up with its neighbours.
    """
    parts = [
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="5" '
        f'fill="{ms.BG}" stroke="{STROKE}" stroke-width="1.2"/>',
    ]
    pad = FS_DEVA * 0.62
    y_dev = y + pad
    y_iast = y_dev + FS_DEVA * 0.52 + FS_IAST * 0.62
    y_eng = y_iast + FS_IAST * 1.18
    if dev:
        parts.append(render_text(x + w / 2, y_dev, dev, FS_DEVA, TEXT,
                                 family=DEV_FONT, weight="600"))
    parts.append(render_text(x + w / 2, y_iast, iast, FS_IAST, TEXT,
                             weight="700", style="italic"))
    parts.append(render_text(x + w / 2, y_eng, english, FS_GLOSS, MUTED))
    return "\n  ".join(parts)


def fig_pipeline_scales() -> None:
    """Figure 12.1a -- the five scales, named. No example, no tiles.

    Split out of the former single `pipeline` figure 2026-08-20. That figure
    tried to carry the abstract scale-chain and a worked ⟪कृ⟫ example in one
    900x330 frame; at 4.5in the labels came out between 4.3pt and 8.6pt and
    "śabda / kriyāpada" overflowed its box in both directions. Two figures let
    each part hold type at the sizes the chapter specifies.
    """
    # (Devanagari, IAST, English). The Devanagari forms match the manuscript's
    # own usage in Ch11-12. The English line is kept to one short word: five
    # boxes across 4.5in leaves roughly 150 units each, and at the 10pt floor
    # that holds about nine characters, so "semantic atom" and "role-marked"
    # overflowed. The fuller glosses live in the caption and the prose.
    # The śabda / kriyāpada box carries only क्रियापदम् -- the alternative
    # made the widest box in the row and the chapter reaches the sentence
    # through the verb anyway.
    items = [
        ("", "varṇāḥ", "sonomers"),
        ("धातुः", "dhātuḥ", "atom"),
        ("क्रियापद", "kriyāpada", "molecule"),
        ("पदम्", "padam", "marked"),
        ("वाक्यम्", "vākyam", "sentence"),
    ]
    body: list[str] = [
        render_text(FIG_W / 2, pt(20), "Assembly without loss", FS_HEAD, TEXT, weight="700")
    ]
    n = len(items)
    box_w = 140.0
    gap = (FIG_W - 2 * 26 - n * box_w) / (n - 1)   # even arrow gutters
    y = pt(36)
    box_h = pt(40)   # three registers now, not a title plus gloss
    for i, (dev, iast, english) in enumerate(items):
        x = 26 + i * (box_w + gap)
        body.append(label_box(x, y, box_w, box_h, dev, iast, english))
        if i < n - 1:
            body.append(render_arrow(x + box_w + gap * 0.18, y + box_h / 2,
                                     x + box_w + gap * 0.82, y + box_h / 2))
    write_svg("building_vakya_pipeline_scales", FIG_W, y + box_h + pt(14),
              "\n".join(body), "Ch12 assembly scales")


def fig_pipeline_example() -> None:
    """Figure 12.1b -- the same chain instantiated on one atom.

    ⟪कृ⟫ becomes करिष्यति. The ष्य् cluster is one timing envelope divided
    into two halves (see render_cluster), so the reader can still count the
    sonomers inside it.
    """
    body: list[str] = [
        render_text(FIG_W / 2, pt(20), "The same assembly on one atom",
                    FS_HEAD, TEXT, weight="700")
    ]
    # The two words are placed in separate calls so the arrow can sit in the
    # measured gap between them. Rendering both in one call returns only the
    # combined extent, which is what put the arrow on top of करिष्यति's first
    # tile.
    y = pt(58)
    atom, e_atom = render_strip([["k", "R"]], 40, y, "original",
                                labels=["कृ"], label_size=FS_IAST)
    gap = pt(30)
    x2 = e_atom[2] + gap
    word, e_word = render_strip([["k", "a", "r", "i", "S", "y", "a", "t", "i"]],
                                x2, y, "original",
                                labels=["करिष्यति"], label_size=FS_IAST)
    mid = (e_atom[2] + x2) / 2
    body.append(atom)
    body.append(render_arrow(mid - gap * 0.34, y, mid + gap * 0.34, y))
    body.append(word)
    bottom = max(e_atom[3], e_word[3])
    write_svg("building_vakya_pipeline_example", FIG_W, bottom + pt(12),
              "\n".join(body), "Ch12 assembly example: kṛ becomes kariṣyati")


def fig_visual_key() -> None:
    body: list[str] = [
        render_text(FIG_W / 2, pt(20), "Ch12 visual key", FS_HEAD, TEXT, weight="700")
    ]
    # The first and last two samples use "original" so they demonstrate the
    # vowel/consonant colouring the reader meets in Figure 12.2. The middle
    # three keep their role fills, because the fill IS what those samples are
    # showing.
    samples = [
        ("dhātuḥ atom", [["k", "R"]], "original"),
        ("head-bond", [["p", "r", "a"]], "head"),
        ("tail-bond", [["t", "R"]], "tail"),
        ("role-marker", [["A"]], "role"),
        ("nasal consonant", [["a", "M"]], "original"),
        ("visarga", [["a", "H"]], "original"),
    ]
    col_w = FIG_W / 3
    row_h = HEX_HEIGHT + pt(34)
    y0 = pt(62) + HEX_HEIGHT / 2   # clears the centred title above
    max_bottom = 0.0
    for idx, (label, words, role) in enumerate(samples):
        col, row = idx % 3, idx // 3
        sy = y0 + row * row_h
        strip, extent = render_strip(words, 0, sy, role, word_gap=pt(11), show_matra=False)
        # Centre the sample in its column, then hang the label above the tiles
        # measured from the strip's own extent. The old fixed -70 offset was
        # tuned to the smaller tiles and the labels now sat on top of them.
        dx = col * col_w + (col_w - (extent[2] - extent[0])) / 2 - extent[0]
        body.append(f'<g transform="translate({dx:.1f},0)">{strip}</g>')
        body.append(render_text(col * col_w + col_w / 2, extent[1] - pt(7),
                                label, FS_LABEL, TEXT, weight="700"))
        max_bottom = max(max_bottom, extent[3])
    write_svg("building_vakya_visual_key", FIG_W, max_bottom + pt(12),
              "\n".join(body), "Ch12 hexagon visual key")


def fig_kr_hlad() -> None:
    body: list[str] = [render_text(370, 34, "One flagship atom, one contrast atom", 24, TEXT, weight="700")]
    kr, _ = render_strip([["k", "R"]], 140, 135, "original", labels=["कृ  kṛ"])
    hlad, _ = render_strip([["h", "l", "A", "d"]], 430, 135, "original", labels=["ह्लाद्  hlād"])
    body.extend([kr, hlad])
    body.append(render_text(205, 255, "high deployment", 15, MUTED, style="italic"))
    body.append(render_text(520, 255, "specialized deployment", 15, MUTED, style="italic"))
    write_svg("building_vakya_kr_hlad", 740, 310, "\n".join(body), "Kṛ and hlād contrast atoms")


def fig_head_bonds() -> None:
    body: list[str] = [render_text(470, 32, "Head-bonds redirect the kṛ field", 24, TEXT, weight="700")]
    rows = [
        ("प्र + कृ", [["p", "r", "a"], ["k", "R"]], [["p", "r", "a", "k", "R", "t", "i"]], "prakṛti"),
        ("वि + कृ", [["v", "i"], ["k", "R"]], [["v", "i", "k", "R", "t", "i"]], "vikṛti"),
        ("सम् + कृ field", [["s", "a", "M"], ["k", "R"]], [["s", "a", "M", "s", "k", "R", "t", "i"]], "saṃskṛti"),
    ]
    y = 100
    for label, left_words, out_words, gloss in rows:
        body.append(render_text(78, y + 5, label, 17, TEXT, anchor="start", weight="700"))
        left, _ = render_strip(left_words, 210, y, "head", word_gap=25)
        body.append(left)
        body.append(render_arrow(420, y, 465, y))
        out, _ = render_strip(out_words, 500, y, "original", word_gap=25, labels=[gloss])
        body.append(out)
        y += 145
    write_svg("building_vakya_head_bonds", 940, 515, "\n".join(body), "Kṛ head-bond triptych")


def fig_tail_bonds() -> None:
    body: list[str] = [render_text(500, 32, "Tail-bonds stabilize molecule class", 24, TEXT, weight="700")]
    rows = [
        ("obligation", [["k", "A", "r", "y", "a"]], "kārya"),
        ("deed", [["k", "a", "r", "m", "a"]], "karma"),
        ("agent", [["k", "a", "r", "t", "R"]], "kartṛ"),
        ("refined formation", [["s", "a", "M", "s", "k", "R", "t", "i"]], "saṃskṛti"),
        ("refining act", [["s", "a", "M", "s", "k", "A", "r", "a"]], "saṃskāra"),
    ]
    y = 125
    for label, words, gloss in rows:
        body.append(render_text(70, y + 6, label, 15, MUTED, anchor="start", style="italic"))
        strip, _ = render_strip(words, 245, y, "original", word_gap=25, labels=[gloss])
        body.append(strip)
        y += 145
    write_svg("building_vakya_tail_bonds", 1000, 845, "\n".join(body), "Kṛ tail-bond molecules")


def fig_bonding_matrix() -> None:
    # The table was authored at width=980 while its own columns needed
    # 35 + 6*178 = 1103, so the final "agent" column fell off the right edge
    # and rendered as an empty strip. Widths are now derived from FIG_W so
    # the table cannot outgrow its frame: a narrow head-bond column plus five
    # equal content columns, all inside the 900-unit figure.
    width = FIG_W
    left = pt(7)
    top = pt(34)
    head_w = pt(50)   # must fit the word 'head-bond' at the 10pt floor
    cell_w = (width - 2 * left - head_w) / 5
    cell_h = pt(31)
    # Headers trimmed to fit: at the 10pt floor a 54pt column holds about ten
    # characters, and "state / formation" and "act / mode" overran into their
    # neighbours. The full column senses are given in the caption.
    headers = ["head-bond", "state", "act", "obligation", "deed", "agent"]
    rows = [
        ("none", ["", "", "कार्य kārya", "कर्म karma", "कर्तृ kartṛ"]),
        ("प्र pra-", ["प्रकृति prakṛti", "प्रकार prakāra", "", "", ""]),
        ("वि vi-", ["विकृति vikṛti", "विकार vikāra", "", "", ""]),
        ("सम् sam-", ["संस्कृति saṃskṛti", "संस्कार saṃskāra", "", "", ""]),
    ]
    def col_x(c: int) -> tuple[float, float]:
        """(x, width) for column c; column 0 is the narrow head-bond column."""
        return (left, head_w) if c == 0 else (left + head_w + (c - 1) * cell_w, cell_w)

    body: list[str] = [
        render_text(width / 2, pt(20), "The kṛ bonding matrix", FS_HEAD, TEXT, weight="700")
    ]
    head_h = cell_h * 0.72
    for c, header in enumerate(headers):
        x, w = col_x(c)
        body.append(f'<rect x="{x:.1f}" y="{top:.1f}" width="{w:.1f}" height="{head_h:.1f}" '
                    f'fill="{ms.SAND if hasattr(ms, "SAND") else "#efe7d6"}" stroke="{STROKE}" stroke-width="1"/>')
        body.append(render_text(x + w / 2, top + head_h / 2, header, FS_GLOSS, TEXT, weight="700"))
    for r, (head, cells) in enumerate(rows):
        y = top + head_h + r * cell_h
        x, w = col_x(0)
        body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{cell_h:.1f}" '
                    f'fill="#faf6ee" stroke="{STROKE}" stroke-width="1"/>')
        body.append(render_text(x + w / 2, y + cell_h / 2, head, FS_GLOSS, TEXT, weight="700"))
        for c, value in enumerate(cells):
            x, w = col_x(c + 1)
            fill = ms.BG if value else "#faf8f4"
            body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{cell_h:.1f}" '
                        f'fill="{fill}" stroke="{STROKE}" stroke-width="1"/>')
            if value:
                parts = value.split(" ", 1)
                body.append(render_text(x + w / 2, y + cell_h / 2 - FS_DEVA * 0.34,
                                        parts[0], FS_DEVA, TEXT, family=DEV_FONT, weight="600"))
                if len(parts) > 1:
                    body.append(render_text(x + w / 2, y + cell_h / 2 + FS_IAST * 0.72,
                                            parts[1], FS_IAST, MUTED, style="italic"))
            else:
                body.append(render_text(x + w / 2, y + cell_h / 2, "—", FS_DEVA, ms.GUIDE))
    height = top + head_h + len(rows) * cell_h + pt(10)
    write_svg("building_vakya_kr_bonding_matrix", width, height, "\n".join(body), "Kṛ bonding matrix")


def fig_rca_role_marker() -> None:
    body: list[str] = [render_text(420, 32, "A śabda becomes a padam", 24, TEXT, weight="700")]
    left, _ = render_strip([["R", "c"]], 105, 125, "original", labels=["ऋच्  ṛc"])
    marker, _ = render_strip([["A"]], 375, 125, "role", labels=["instrumental role-marker"])
    right, _ = render_strip([["R", "c", "A"]], 590, 125, "original", labels=["ऋचा  ṛcā"])
    body.extend([left, marker, right])
    body.append(render_text(315, 125, "+", 34, TEXT, weight="700"))
    body.append(render_arrow(450, 125, 520, 125))
    write_svg("building_vakya_rca_role_marker", 840, 250, "\n".join(body), "Ṛc to ṛcā role marker")


def fig_sentence_full_hex() -> None:
    """One word per row, stacked.

    The four words hold about 27 sonomers between them. Laid end to end on
    one line they forced a viewBox over 1500 units wide, which at 4.5in put
    every glyph near 4pt -- the figure was unreadable in the book even though
    it looked fine on screen at full width. Stacking gives each word a row of
    at most nine tiles, the same density as Figure 12.2, so the type can hold
    11pt/10pt. Reading down the rows also matches how the sentence is parsed
    in the prose, word by word.
    """
    body: list[str] = [
        render_text(FIG_W / 2, pt(20), "यस्तन्न वेद किमृचा करिष्यति",
                    FS_HEAD, TEXT, family=DEV_FONT, weight="700")
    ]
    words = [
        (["y", "a", "s", "t", "a", "n", "n", "a"], "यस्तन्न", "yastanna"),
        (["v", "e", "d", "a"], "वेद", "veda"),
        (["k", "i", "m", "R", "c", "A"], "किमृचा", "kimṛcā"),
        (["k", "a", "r", "i", "S", "y", "a", "t", "i"], "करिष्यति", "kariṣyati"),
    ]
    y = pt(48) + HEX_HEIGHT / 2
    bottom = y
    for tokens, dev, iast in words:
        strip, extent = render_strip([tokens], pt(78), y, "original")
        body.append(strip)
        # Row label sits in the left margin, vertically centred on the tiles,
        # so the strips all start from the same x and stay comparable.
        body.append(render_text(pt(70), y - FS_DEVA * 0.34, dev, FS_DEVA, TEXT,
                                anchor="end", family=DEV_FONT, weight="600"))
        body.append(render_text(pt(70), y + FS_IAST * 0.80, iast, FS_IAST, MUTED,
                                anchor="end", style="italic"))
        bottom = extent[3]
        y = extent[3] + HEX_HEIGHT * 0.62
    write_svg("building_vakya_sentence_full_hex", FIG_W, bottom + pt(12),
              "\n".join(body), "Full hexagon sentence experiment")


def fig_vivimorphosis() -> None:
    """The boundary crossing, read downward.

    Rebuilt 2026-08-20. The previous version ran four stages left to right
    across a 1080-unit frame: the stage labels sat on top of the tiles, the
    strips overlapped each other, and the last word fell outside the
    viewBox. Reading DOWN also puts the boundary where it belongs -- a
    horizontal rule the eye actually crosses, with the calibrant above it
    and the contact language below.

    The two sides are drawn in different shapes on purpose. Above the rule
    Sanskrit is hexagonal, sonomer by sonomer, coloured by the same
    vowel/consonant convention as the rest of the chapter. Below it the
    receiving language is a soft rounded form with a dashed edge and no
    internal divisions, because the contact language does not preserve the
    constituent boundaries -- that loss is the content of the figure, so it
    is drawn rather than asserted. Both readings survive grayscale, since
    the contrast is shape and outline, not hue.
    """
    body: list[str] = [
        render_text(FIG_W / 2, pt(18), "Boundary crossing: apabhraṃśa / vivimorphosis",
                    FS_HEAD, TEXT, weight="700")
    ]
    label_x = pt(76)
    strip_x = pt(86)

    def stage_label(y: float, dev: str, iast: str) -> None:
        body.append(render_text(label_x, y - FS_DEVA * 0.34, dev, FS_DEVA, TEXT,
                                anchor="end", family=DEV_FONT, weight="600"))
        body.append(render_text(label_x, y + FS_IAST * 0.80, iast, FS_IAST, MUTED,
                                anchor="end", style="italic"))

    # --- above the rule: the engineered calibrant -------------------------
    y = pt(46) + HEX_HEIGHT / 2
    dhatu, e_dhatu = render_strip([["d", "i", "v"]], strip_x, y, "original")
    body.append(dhatu)
    stage_label(y, "धातुः", "dhātuḥ")
    body.append(render_text(e_dhatu[2] + pt(12), y, "“to shine”", FS_IAST, MUTED,
                            anchor="start", style="italic"))

    y2 = e_dhatu[3] + HEX_HEIGHT * 0.58
    sabda, e_sabda = render_strip([["d", "e", "v", "a", "H"]], strip_x, y2, "original")
    body.append(sabda)
    stage_label(y2, "शब्दः", "śabdaḥ")
    body.append(render_text(e_sabda[2] + pt(12), y2, "the calibrated form", FS_IAST, MUTED,
                            anchor="start", style="italic"))

    # --- the rule ---------------------------------------------------------
    rule_y = e_sabda[3] + pt(20)
    body.append(f'<line x1="{pt(8):.1f}" y1="{rule_y:.1f}" x2="{FIG_W - pt(8):.1f}" '
                f'y2="{rule_y:.1f}" stroke="{DASH}" stroke-width="1.4" stroke-dasharray="6,5"/>')
    body.append(render_text(pt(8), rule_y - pt(6), "Sanskrit calibrant — preserved", FS_GLOSS,
                            MUTED, anchor="start", style="italic"))
    body.append(render_text(FIG_W - pt(8), rule_y + pt(11), "contact language — organic",
                            FS_GLOSS, MUTED, anchor="end", style="italic"))

    # --- below the rule: the seed and the organic form --------------------
    def soft_form(cx: float, cy: float, w: float, h: float, main: str, sub: str,
                  dashed: bool = True) -> None:
        dash = ' stroke-dasharray="5,4"' if dashed else ""
        body.append(
            f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{h / 2:.1f}" fill="{ms.SAND if hasattr(ms, "SAND") else "#f2ece0"}" '
            f'stroke="{ms.STROKE}" stroke-width="1.2"{dash} opacity="0.95"/>'
        )
        body.append(render_text(cx, cy, main, FS_DEVA, TEXT, weight="600"))
        # Descriptor sits OUTSIDE the form, on the same right-hand column as
        # the two above the rule. Inside, it overran the pill and collided
        # with the stage label in the left margin.
        body.append(render_text(cx + w / 2 + pt(12), cy, sub, FS_IAST, MUTED,
                                anchor="start", style="italic"))

    y3 = rule_y + pt(26) + HEX_HEIGHT / 2
    seed_w, form_h = pt(52), HEX_HEIGHT * 0.82
    seed_cx = strip_x + seed_w / 2
    soft_form(seed_cx, y3, seed_w, form_h, "देव-", "the seed a listener keeps")
    stage_label(y3, "बीजम्", "bījam")

    y4 = y3 + form_h + pt(16)
    apa_w = pt(52)
    apa_cx = strip_x + apa_w / 2
    soft_form(apa_cx, y4, apa_w, form_h, "deus", "Latin — no longer divisible")
    stage_label(y4, "अपशब्दः", "apaśabdaḥ")

    # One arrow across the rule carries the crossing; the arrow between the
    # two Sanskrit rows would only repeat what the stacking already says.
    body.append(render_arrow(seed_cx, e_sabda[3] + pt(4), seed_cx, y3 - form_h / 2 - pt(3)))
    body.append(render_arrow(apa_cx, y3 + form_h / 2 + pt(3), apa_cx, y4 - form_h / 2 - pt(3)))

    write_svg("building_vakya_vivimorphosis", FIG_W, y4 + form_h / 2 + pt(12),
              "\n".join(body), "Vivimorphosis boundary diagram")


def main() -> None:
    fig_pipeline_scales()
    fig_pipeline_example()
    fig_visual_key()
    fig_kr_hlad()
    fig_head_bonds()
    fig_tail_bonds()
    fig_bonding_matrix()
    fig_rca_role_marker()
    fig_sentence_full_hex()
    fig_vivimorphosis()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
dhatu_hexagon.py — Hexagonal-tile SVG visualization of Sanskrit dhātus.

v1 (standalone, no manuscript linkage). Encodes:
    - Shape (top/bottom edge length): mātrā duration (½ / 1 / 2)
    - Fill color: place of articulation (sthāna)
    - Fill saturation: voicing class (light = aghoṣa, dark = ghoṣa, etc.)
    - Stroke weight: aspiration (thin = alpaprāṇa, thick = mahāprāṇa / ūṣman)
    - Inscribed marks: anusvāra (·), visarga (· ·), nasal bindu on top of hex
    - Vertical zigzag tiling: each hexagon shares slanted edges with neighbors

Geometry note (Option B per design notes):
    - All hexagons have the SAME height (h = e · √3 where e is the slanted-edge
      length, constant for every particle).
    - Top and bottom edges are HORIZONTAL and vary in length per mātrā class:
      C = e/2  (½ mātrā),  V1 = e  (1 mātrā),  V2 = 2e  (2 mātrā).
    - The four slanted edges are all length e, at ±60° from horizontal.
    - Adjacent hexagons abut by sharing one slanted edge → mandatory vertical
      stagger of h/2; this is the zigzag.

Usage:
    python dhatu_hexagon.py "k,R" -o output/kr.svg            # कृ
    python dhatu_hexagon.py "g,a,m" -o output/gam.svg         # गम्
    python dhatu_hexagon.py "j,v,a,l" -o output/jval.svg      # ज्वल्

Each particle is looked up in the VARNAS table (Devanagari + IAST + class +
sthāna + voicing + aspiration). The class can be overridden with "label:CLASS"
syntax (e.g., "k:C") but is auto-detected by default.

ASCII aliases (Harvard-Kyoto style) are supported for IAST diacritics:
    A=ā  I=ī  U=ū  R=ṛ  RR=ṝ  T=ṭ  Th=ṭh  D=ḍ  Dh=ḍh  N=ṇ
    G=ṅ  J=ñ  S=ṣ  z=ś  M=ṃ  H=ḥ

Future work: JSON input, upasargas (left tiles), pratyayas (right tiles),
gaṇa modifications, kriyā / śabda extensions.
"""

import argparse
import math
import sys
from pathlib import Path


# --- Geometry constants ---

EDGE_LENGTH = 40                            # slanted-edge length (px), constant for all hexagons
HEX_HEIGHT = EDGE_LENGTH * math.sqrt(3)     # full hexagon height (constant)
WIDTH_BY_CLASS = {                          # top / bottom edge length per mātrā class
    "C":  EDGE_LENGTH / 2,                  # ½ mātrā (vyañjana)
    "V1": EDGE_LENGTH,                      # 1 mātrā (hrasva)
    "V2": EDGE_LENGTH * 2,                  # 2 mātrā (dīrgha)
}


# --- Color palette for sthāna (place of articulation) ---

STHANA_COLORS = {
    "kanthya":        "#e85d5d",   # guttural — red
    "talavya":        "#f59f3a",   # palatal — orange
    "murdhanya":      "#e8c547",   # retroflex — yellow
    "dantya":         "#65c97e",   # dental — green
    "ostyha":         "#5da8e8",   # labial — blue
    "kanthatalavya":  "#f06fb8",   # guttural-palatal (e, ai) — pink
    "kanthostyha":    "#9f7be8",   # guttural-labial (o, au) — purple
    "dantostyha":     "#6fbcd9",   # dento-labial (v) — light blue
    "default":        "#bcbcbc",   # neutral
}


# --- Voicing class → fill lightening amount ---
# 0.0 = full saturation, 1.0 = white

VOICING_LIGHTEN = {
    "ghosha":     0.05,    # voiced — nearly full saturation
    "anunasika":  0.20,    # nasal — slight lightening
    "antahstha":  0.30,    # semivowel — medium
    "vowel":      0.35,    # vowel — medium
    "ushman":     0.45,    # fricative — light
    "aghosha":    0.55,    # voiceless — light
    "anusvara":   0.60,    # ayogavāha (neutral fill, marked inside)
    "visarga":    0.60,
    "default":    0.40,
}


# --- Stroke weight → aspiration ---

STROKE_WEIGHT_BY_ASPIRATION = {
    "mahaprana":  3.5,     # aspirated → thick
    "alpaprana":  1.5,     # unaspirated → thin
    "n/a":        1.5,     # not-applicable → thin
}


# --- Simple style (two-shade gray, no voicing/aspiration encoding) ---
# Used for chapter figures where the focus is the mātrā envelope itself,
# not the full place-of-articulation × voicing × aspiration matrix.

SIMPLE_FILL_CONSONANT = "#aaaaaa"   # medium gray
SIMPLE_FILL_VOWEL     = "#dcdcdc"   # light gray
SIMPLE_STROKE         = "#333333"
SIMPLE_STROKE_WIDTH   = 1.5


# --- The varṇa table ---
# Each entry: deva (Devanagari), iast (IAST), class (C/V1/V2), sthana, voicing, aspiration.
# Keyed by IAST (with Harvard-Kyoto ASCII aliases added below).

VARNAS = {
    # --- Vowels (svara) ---
    "a":  {"deva": "अ",  "iast": "a",  "class": "V1", "sthana": "kanthya",       "voicing": "vowel", "aspiration": "n/a"},
    "ā":  {"deva": "आ",  "iast": "ā",  "class": "V2", "sthana": "kanthya",       "voicing": "vowel", "aspiration": "n/a"},
    "i":  {"deva": "इ",  "iast": "i",  "class": "V1", "sthana": "talavya",       "voicing": "vowel", "aspiration": "n/a"},
    "ī":  {"deva": "ई",  "iast": "ī",  "class": "V2", "sthana": "talavya",       "voicing": "vowel", "aspiration": "n/a"},
    "u":  {"deva": "उ",  "iast": "u",  "class": "V1", "sthana": "ostyha",        "voicing": "vowel", "aspiration": "n/a"},
    "ū":  {"deva": "ऊ",  "iast": "ū",  "class": "V2", "sthana": "ostyha",        "voicing": "vowel", "aspiration": "n/a"},
    "ṛ":  {"deva": "ऋ",  "iast": "ṛ",  "class": "V1", "sthana": "murdhanya",     "voicing": "vowel", "aspiration": "n/a"},
    "ṝ":  {"deva": "ॠ",  "iast": "ṝ",  "class": "V2", "sthana": "murdhanya",     "voicing": "vowel", "aspiration": "n/a"},
    "ḷ":  {"deva": "ऌ",  "iast": "ḷ",  "class": "V1", "sthana": "dantya",        "voicing": "vowel", "aspiration": "n/a"},
    "e":  {"deva": "ए",  "iast": "e",  "class": "V2", "sthana": "kanthatalavya", "voicing": "vowel", "aspiration": "n/a"},
    "ai": {"deva": "ऐ",  "iast": "ai", "class": "V2", "sthana": "kanthatalavya", "voicing": "vowel", "aspiration": "n/a"},
    "o":  {"deva": "ओ",  "iast": "o",  "class": "V2", "sthana": "kanthostyha",   "voicing": "vowel", "aspiration": "n/a"},
    "au": {"deva": "औ",  "iast": "au", "class": "V2", "sthana": "kanthostyha",   "voicing": "vowel", "aspiration": "n/a"},

    # --- K-varga (kaṇṭhya / guttural) ---
    "k":  {"deva": "क",  "iast": "k",  "class": "C", "sthana": "kanthya", "voicing": "aghosha",   "aspiration": "alpaprana"},
    "kh": {"deva": "ख",  "iast": "kh", "class": "C", "sthana": "kanthya", "voicing": "aghosha",   "aspiration": "mahaprana"},
    "g":  {"deva": "ग",  "iast": "g",  "class": "C", "sthana": "kanthya", "voicing": "ghosha",    "aspiration": "alpaprana"},
    "gh": {"deva": "घ",  "iast": "gh", "class": "C", "sthana": "kanthya", "voicing": "ghosha",    "aspiration": "mahaprana"},
    "ṅ":  {"deva": "ङ",  "iast": "ṅ",  "class": "C", "sthana": "kanthya", "voicing": "anunasika", "aspiration": "alpaprana"},

    # --- C-varga (tālavya / palatal) ---
    "c":  {"deva": "च",  "iast": "c",  "class": "C", "sthana": "talavya", "voicing": "aghosha",   "aspiration": "alpaprana"},
    "ch": {"deva": "छ",  "iast": "ch", "class": "C", "sthana": "talavya", "voicing": "aghosha",   "aspiration": "mahaprana"},
    "j":  {"deva": "ज",  "iast": "j",  "class": "C", "sthana": "talavya", "voicing": "ghosha",    "aspiration": "alpaprana"},
    "jh": {"deva": "झ",  "iast": "jh", "class": "C", "sthana": "talavya", "voicing": "ghosha",    "aspiration": "mahaprana"},
    "ñ":  {"deva": "ञ",  "iast": "ñ",  "class": "C", "sthana": "talavya", "voicing": "anunasika", "aspiration": "alpaprana"},

    # --- Ṭ-varga (mūrdhanya / retroflex) ---
    "ṭ":  {"deva": "ट",  "iast": "ṭ",  "class": "C", "sthana": "murdhanya", "voicing": "aghosha",   "aspiration": "alpaprana"},
    "ṭh": {"deva": "ठ",  "iast": "ṭh", "class": "C", "sthana": "murdhanya", "voicing": "aghosha",   "aspiration": "mahaprana"},
    "ḍ":  {"deva": "ड",  "iast": "ḍ",  "class": "C", "sthana": "murdhanya", "voicing": "ghosha",    "aspiration": "alpaprana"},
    "ḍh": {"deva": "ढ",  "iast": "ḍh", "class": "C", "sthana": "murdhanya", "voicing": "ghosha",    "aspiration": "mahaprana"},
    "ṇ":  {"deva": "ण",  "iast": "ṇ",  "class": "C", "sthana": "murdhanya", "voicing": "anunasika", "aspiration": "alpaprana"},

    # --- T-varga (dantya / dental) ---
    "t":  {"deva": "त",  "iast": "t",  "class": "C", "sthana": "dantya", "voicing": "aghosha",   "aspiration": "alpaprana"},
    "th": {"deva": "थ",  "iast": "th", "class": "C", "sthana": "dantya", "voicing": "aghosha",   "aspiration": "mahaprana"},
    "d":  {"deva": "द",  "iast": "d",  "class": "C", "sthana": "dantya", "voicing": "ghosha",    "aspiration": "alpaprana"},
    "dh": {"deva": "ध",  "iast": "dh", "class": "C", "sthana": "dantya", "voicing": "ghosha",    "aspiration": "mahaprana"},
    "n":  {"deva": "न",  "iast": "n",  "class": "C", "sthana": "dantya", "voicing": "anunasika", "aspiration": "alpaprana"},

    # --- P-varga (oṣṭhya / labial) ---
    "p":  {"deva": "प",  "iast": "p",  "class": "C", "sthana": "ostyha", "voicing": "aghosha",   "aspiration": "alpaprana"},
    "ph": {"deva": "फ",  "iast": "ph", "class": "C", "sthana": "ostyha", "voicing": "aghosha",   "aspiration": "mahaprana"},
    "b":  {"deva": "ब",  "iast": "b",  "class": "C", "sthana": "ostyha", "voicing": "ghosha",    "aspiration": "alpaprana"},
    "bh": {"deva": "भ",  "iast": "bh", "class": "C", "sthana": "ostyha", "voicing": "ghosha",    "aspiration": "mahaprana"},
    "m":  {"deva": "म",  "iast": "m",  "class": "C", "sthana": "ostyha", "voicing": "anunasika", "aspiration": "alpaprana"},

    # --- Antaḥstha (semivowels / approximants) ---
    "y":  {"deva": "य",  "iast": "y",  "class": "C", "sthana": "talavya",    "voicing": "antahstha", "aspiration": "alpaprana"},
    "r":  {"deva": "र",  "iast": "r",  "class": "C", "sthana": "murdhanya",  "voicing": "antahstha", "aspiration": "alpaprana"},
    "l":  {"deva": "ल",  "iast": "l",  "class": "C", "sthana": "dantya",     "voicing": "antahstha", "aspiration": "alpaprana"},
    "v":  {"deva": "व",  "iast": "v",  "class": "C", "sthana": "dantostyha", "voicing": "antahstha", "aspiration": "alpaprana"},

    # --- Ūṣmāṇaḥ (sibilants / fricatives) ---
    "ś":  {"deva": "श",  "iast": "ś",  "class": "C", "sthana": "talavya",   "voicing": "ushman", "aspiration": "mahaprana"},
    "ṣ":  {"deva": "ष",  "iast": "ṣ",  "class": "C", "sthana": "murdhanya", "voicing": "ushman", "aspiration": "mahaprana"},
    "s":  {"deva": "स",  "iast": "s",  "class": "C", "sthana": "dantya",    "voicing": "ushman", "aspiration": "mahaprana"},
    "h":  {"deva": "ह",  "iast": "h",  "class": "C", "sthana": "kanthya",   "voicing": "ushman", "aspiration": "mahaprana"},

    # --- Ayogavāha (anusvāra, visarga) ---
    "ṃ":  {"deva": "ं",   "iast": "ṃ",  "class": "C", "sthana": "default", "voicing": "anusvara", "aspiration": "n/a"},
    "ḥ":  {"deva": "ः",   "iast": "ḥ",  "class": "C", "sthana": "default", "voicing": "visarga",  "aspiration": "n/a"},
}

# ASCII aliases for IAST diacritics (Harvard-Kyoto style)
ASCII_ALIAS = {
    "A": "ā",   "I": "ī",   "U": "ū",
    "R": "ṛ",   "RR": "ṝ",  "lR": "ḷ",
    "T": "ṭ",   "Th": "ṭh", "D": "ḍ",   "Dh": "ḍh", "N": "ṇ",
    "G": "ṅ",   "J": "ñ",   "S": "ṣ",   "z": "ś",
    "M": "ṃ",   "H": "ḥ",
}


# --- Geometry helpers ---

def hex_vertices(cx, cy, w, e=EDGE_LENGTH):
    """Return the 6 vertices of a flat-top stretched hexagon centered at (cx, cy).

    The top and bottom edges have length w (horizontal). The four slanted edges
    each have length e (slanted at ±60° from horizontal). The hexagon height
    is constant: h = e · √3.

    Vertices, in clockwise order starting from top-left:
        P1 top-left, P2 top-right, P3 right, P4 bottom-right, P5 bottom-left, P6 left.
    """
    h = e * math.sqrt(3)
    return [
        (cx - w/2,         cy - h/2),     # P1 top-left
        (cx + w/2,         cy - h/2),     # P2 top-right
        (cx + w/2 + e/2,   cy),           # P3 right (vertex)
        (cx + w/2,         cy + h/2),     # P4 bottom-right
        (cx - w/2,         cy + h/2),     # P5 bottom-left
        (cx - w/2 - e/2,   cy),           # P6 left (vertex)
    ]


def lighten(hex_color, amount):
    """Mix `hex_color` with white. amount=0 → no change, 1 → full white."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r + (255 - r) * amount)
    g = int(g + (255 - g) * amount)
    b = int(b + (255 - b) * amount)
    return f"#{r:02x}{g:02x}{b:02x}"


def fill_for_varna(v):
    """Choose fill color: base sthāna hue, lightened by voicing class."""
    base = STHANA_COLORS.get(v["sthana"], STHANA_COLORS["default"])
    amount = VOICING_LIGHTEN.get(v["voicing"], VOICING_LIGHTEN["default"])
    return lighten(base, amount)


def stroke_for_varna(v):
    """Stroke weight encodes aspiration."""
    return STROKE_WEIGHT_BY_ASPIRATION.get(v["aspiration"], 1.5)


# --- SVG rendering ---

HALANT = "्"   # ्  — DEVANAGARI SIGN VIRAMA (suppresses the inherent vowel)


def devanagari_label(v):
    """Return the Devanagari label for a varṇa, with halant appended for pure
    consonants. Vowels render bare; anusvāra (ं) and visarga (ः) are themselves
    diacritics so they never carry a halant.
    """
    base = v["deva"]
    is_consonant = v["class"] == "C"
    is_ayogavaha = v["voicing"] in ("anusvara", "visarga")
    if is_consonant and not is_ayogavaha:
        return base + HALANT
    return base


def render_hexagon(cx, cy, v, style="full"):
    """Render one varṇa as a hexagon with labels and any inscribed marks.

    `style` controls the visual encoding:
        "full"   — sthāna / voicing / aspiration encoded by fill / saturation / stroke.
        "simple" — two-shade gray for consonant vs vowel; no voicing or aspiration
                   encoding. Used for chapter figures where the focus is the mātrā
                   envelope itself.

    Returns a multi-line SVG fragment.
    """
    w = WIDTH_BY_CLASS[v["class"]]
    verts = hex_vertices(cx, cy, w)
    points_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in verts)

    if style == "simple":
        fill = SIMPLE_FILL_CONSONANT if v["class"] == "C" else SIMPLE_FILL_VOWEL
        stroke = SIMPLE_STROKE
        stroke_w = SIMPLE_STROKE_WIDTH
    else:
        fill = fill_for_varna(v)
        stroke = "#1a1a1a"
        stroke_w = stroke_for_varna(v)

    parts = []
    parts.append(
        f'<polygon points="{points_str}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}" stroke-linejoin="round"/>'
    )

    # Devanagari label (centered, slightly above center). Consonants carry halant.
    parts.append(
        f'<text x="{cx:.1f}" y="{cy - 1:.1f}" '
        f'font-family="Noto Sans Devanagari, Kohinoor Devanagari, Devanagari MT, Arial Unicode MS, sans-serif" '
        f'font-size="22" font-weight="500" text-anchor="middle" dominant-baseline="middle" fill="#1a1a1a">'
        f'{devanagari_label(v)}</text>'
    )
    # IAST label (centered, below)
    parts.append(
        f'<text x="{cx:.1f}" y="{cy + 18:.1f}" '
        f'font-family="Charter, Georgia, Times, serif" '
        f'font-size="11" font-style="italic" text-anchor="middle" dominant-baseline="middle" fill="#333">'
        f'{v["iast"]}</text>'
    )

    # Voicing-class inscribed marks (nasal bindu, anusvāra, visarga) — full style only.
    if style == "full":
        if v["voicing"] == "anunasika":
            bindu_y = cy - HEX_HEIGHT/2 - 5
            parts.append(f'<circle cx="{cx:.1f}" cy="{bindu_y:.1f}" r="2.5" fill="#1a1a1a"/>')
        if v["voicing"] == "anusvara":
            parts.append(f'<circle cx="{cx:.1f}" cy="{cy + 4:.1f}" r="3.5" fill="#1a1a1a"/>')
        if v["voicing"] == "visarga":
            parts.append(f'<circle cx="{cx - 5:.1f}" cy="{cy + 4:.1f}" r="2.8" fill="#1a1a1a"/>')
            parts.append(f'<circle cx="{cx + 5:.1f}" cy="{cy + 4:.1f}" r="2.8" fill="#1a1a1a"/>')

    return "\n  ".join(parts)


def compute_layout(particles):
    """Compute (cx, cy) for each hexagon in the zigzag.

    Hexagon i shares its top-left slanted edge with hexagon i-1's bottom-right
    slanted edge, OR its bottom-left with i-1's top-right, alternating.

    Starting hexagon at (0, -h/4) so the strip's midline is at y=0.
    """
    h = HEX_HEIGHT
    positions = []
    cx = 0.0
    cy = -h/4    # start slightly up so zigzag is centered around y=0

    for i, v in enumerate(particles):
        w = WIDTH_BY_CLASS[v["class"]]
        if i == 0:
            positions.append((cx, cy))
            continue
        prev = particles[i - 1]
        prev_w = WIDTH_BY_CLASS[prev["class"]]
        cx_new = positions[-1][0] + (prev_w + w) / 2 + EDGE_LENGTH / 2
        # Alternate vertical position: zigzag amplitude is h/2 around midline
        cy_new = (-h/4) if positions[-1][1] > -h/4 else (h/4)
        positions.append((cx_new, cy_new))

    return positions


def render_dhatu(particles, output_path, scale=2, style="full",
                 title_dev=None, title_iast=None):
    """Render a dhātu (list of varṇa dicts) as SVG to output_path.

    Args:
        particles: list of varṇa dicts.
        output_path: where to write the SVG.
        scale: pixel-dimension multiplier on the geometry-defined viewBox.
        style: "full" (default) or "simple" (two-shade gray, no voicing/aspiration
            encoding — see render_hexagon).
        title_dev, title_iast: optional dhātu name in Devanagari and IAST. If
            provided, rendered as a centered title above the hexagon strip.
    """
    if not particles:
        raise ValueError("No particles to render")

    positions = compute_layout(particles)
    h = HEX_HEIGHT

    # Compute viewBox (geometry bounds)
    xs, ys = [], []
    for (cx, cy), v in zip(positions, particles):
        w = WIDTH_BY_CLASS[v["class"]]
        xs.extend([cx - w/2 - EDGE_LENGTH/2, cx + w/2 + EDGE_LENGTH/2])
        ys.extend([cy - h/2, cy + h/2])

    margin_x, margin_top, margin_bot = 24, 24, 28
    title_height = 44 if (title_dev or title_iast) else 0
    xmin = min(xs) - margin_x
    xmax = max(xs) + margin_x
    ymin = min(ys) - margin_top - title_height
    ymax = max(ys) + margin_bot
    width = xmax - xmin
    height = ymax - ymin

    # Title for SVG metadata (joins IAST labels)
    title_meta = title_iast if title_iast else "".join(p["iast"] for p in particles)

    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{xmin:.1f} {ymin:.1f} {width:.1f} {height:.1f}" '
        f'width="{int(width * scale)}" height="{int(height * scale)}">'
    )
    svg_parts.append(f'  <title>{title_meta}</title>')
    svg_parts.append(
        f'  <rect x="{xmin:.1f}" y="{ymin:.1f}" '
        f'width="{width:.1f}" height="{height:.1f}" fill="white"/>'
    )

    # Visible title above the hexagon strip (Devanagari + Roman, em-dash separated)
    if title_dev or title_iast:
        # Center title horizontally across the hexagon strip
        title_cx = (min(xs) + max(xs)) / 2
        title_y = ymin + 28  # baseline near the top
        if title_dev and title_iast:
            title_text = f'{title_dev} — <tspan font-family="Charter, Georgia, Times, serif" font-style="italic">{title_iast}</tspan>'
        else:
            title_text = title_dev or title_iast
        svg_parts.append(
            f'  <text x="{title_cx:.1f}" y="{title_y:.1f}" '
            f'font-family="Noto Sans Devanagari, Kohinoor Devanagari, Devanagari MT, Charter, Georgia, Times, serif" '
            f'font-size="22" font-weight="500" text-anchor="middle" fill="#1a1a1a">'
            f'{title_text}</text>'
        )

    for (cx, cy), v in zip(positions, particles):
        svg_parts.append("  " + render_hexagon(cx, cy, v, style=style))

    svg_parts.append("</svg>")

    Path(output_path).write_text("\n".join(svg_parts), encoding="utf-8")
    return output_path


# --- Input parsing ---

def resolve_label(raw_label):
    """Resolve a CLI label to a VARNAS key.

    Tries direct lookup, then ASCII aliases (Harvard-Kyoto). Raises if unknown.
    """
    if raw_label in VARNAS:
        return raw_label
    if raw_label in ASCII_ALIAS:
        return ASCII_ALIAS[raw_label]
    raise ValueError(
        f"Unknown varṇa: '{raw_label}'. "
        f"Use IAST (e.g. 'kh', 'ṛ') or Harvard-Kyoto alias (A=ā, I=ī, R=ṛ, S=ṣ, etc.)."
    )


def parse_dhatu_string(s):
    """Parse 'k,a,m' or 'k:C,ṛ:V1' into a list of varṇa dicts."""
    particles = []
    for token in s.split(","):
        token = token.strip()
        if not token:
            continue
        if ":" in token:
            label_raw, cls = token.split(":", 1)
            label_raw = label_raw.strip()
            cls = cls.strip()
        else:
            label_raw = token
            cls = None
        key = resolve_label(label_raw)
        v = dict(VARNAS[key])    # copy so per-call class overrides don't mutate the table
        if cls:
            if cls not in WIDTH_BY_CLASS:
                raise ValueError(f"Unknown class '{cls}'. Valid: C, V1, V2.")
            v["class"] = cls
        particles.append(v)
    return particles


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(
        description="Generate hexagonal-tile SVG of a Sanskrit dhātu.",
        epilog="Example: python dhatu_hexagon.py 'k,R' -o output/kr.svg",
    )
    parser.add_argument(
        "dhatu",
        help="Comma-separated varṇa list. Use IAST or Harvard-Kyoto aliases. "
             "Optional ':CLASS' suffix (C, V1, V2) overrides auto-detection. "
             "Example: 'g,a,m' or 'k:C,ṛ:V1,t:C'.",
    )
    parser.add_argument("-o", "--output", default="dhatu.svg", help="Output SVG path.")
    parser.add_argument("--scale", type=int, default=2, help="Pixel scale multiplier (default 2).")
    parser.add_argument(
        "--style", choices=["full", "simple"], default="full",
        help="Visual encoding: 'full' = sthāna/voicing/aspiration encoded by "
             "fill/saturation/stroke (default); 'simple' = two-shade gray for "
             "C vs V, no voicing/aspiration encoding (chapter-figure mode).",
    )
    parser.add_argument(
        "--title-dev", default=None,
        help="Optional Devanagari title shown above the hexagon strip "
             "(e.g., 'कृ').",
    )
    parser.add_argument(
        "--title-iast", default=None,
        help="Optional IAST title shown above the hexagon strip (e.g., 'kṛ'). "
             "Pairs with --title-dev to produce 'कृ — kṛ'.",
    )
    args = parser.parse_args()

    particles = parse_dhatu_string(args.dhatu)
    output = render_dhatu(
        particles, args.output, scale=args.scale,
        style=args.style,
        title_dev=args.title_dev, title_iast=args.title_iast,
    )
    iast = "".join(p["iast"] for p in particles)
    deva = "".join(p["deva"] for p in particles)
    print(f"Wrote {output}  ({deva} / {iast}, {len(particles)} particles, style={args.style})")


if __name__ == "__main__":
    main()

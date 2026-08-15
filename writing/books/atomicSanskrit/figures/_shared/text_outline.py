#!/usr/bin/env python3
"""text_outline.py — shape text with HarfBuzz and outline it to SVG paths,
for two independent instances of the same underlying bug.

rsvg-convert's PDF backend (Cairo + Pango) mismaps glyph clusters when one
shaped glyph corresponds to more than one input character — it loses track
of the correct text position for whatever comes after. Two triggers found
so far:

1. Devanagari words with a pre-base reordering vowel sign (ि, U+093F) or
   certain conjuncts — the glyph reorders visually before its consonant,
   and Cairo's PDF output loses the following character(s).
2. A specific Latin font stack (`'Gentium Book Plus', Charter, 'Charis
   SIL', Georgia, serif` — Gentium/Charis aren't installed, so this
   resolves to Charter) has contextual ligature-like substitutions after
   "f" (confirmed: "left" -> "lef", "from" -> "fom", "field" -> "feld",
   and "of articulation" -> "ofarticulation" — even a following space can
   vanish) that hit the same cluster-mapping bug.

Both are specific to vector-PDF text output — the same SVG rasterizes to
PNG correctly, and short/simple runs (single Devanagari letters, ordinary
Latin words without "f") are unaffected.

The fix is the same for both: shape the text correctly ourselves
(HarfBuzz resolves reordering/ligatures the same way a browser would),
extract the resulting glyph outlines from the font (fontTools), and bake
them into the SVG as `<path>` geometry instead of a live `<text>` run. A
pre-shaped outline can't be mis-shaped downstream — there's no shaping
left for Cairo's PDF backend to get wrong.

Scope: Devanagari text is always outlined. Latin text is only outlined
when its `<text>`/`<tspan>` uses the known-buggy Gentium-Book-Plus-first
font stack (`contains_risky_latin_font`) — ordinary figures using other
fonts keep live, selectable Latin text.

A third trigger, found 2026-08-13: `<textPath>` — text curving along an
arc-band label (place-of-articulation names on the vocal-tract figures,
PIE-overlay labels, etc.) — was never covered by the two fixes above at
all. It isn't a milder case of the same bug; in the confirmed failure
(the varṇamālā garland and vocal-tract-anatomy figures, Ch7/Ch9), the
whole label disappears rather than losing a character, and it's exposed
to the same risky-Latin-font trigger since none of these labels were
ever outlined. `outline_textpath_in_svg` below flattens the referenced
path (polyline and/or elliptical-arc segments — every textPath href in
this repo resolves to one or the other, confirmed by audit; no cubic/
quadratic Bezier commands appear) into an arc-length-parameterized
polyline, then places each shaped glyph at its own arc-length position
along it with a rotation matching the local tangent — the same
shape-then-bake approach as straight text, just walking a curve instead
of the x-axis for glyph placement.

Requires `uharfbuzz` (shaping) and `fontTools` (outline extraction) — both
live in the project's `.venv-figures/` virtualenv, not the system Python.
"""

from __future__ import annotations

import html
import math
import re
from dataclasses import dataclass
from functools import lru_cache

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

DEVANAGARI_RE = re.compile(r"[ऀ-ॿ]")
_DEVANAGARI_CHAR_RE = re.compile(r"[ऀ-ॿ]")

# The book's own body-text Devanagari face (see build/devanagari-preamble.tex,
# \newfontfamily{\devanagarifont}{Adobe Devanagari}) — outlining with the same
# font keeps figures visually consistent with the manuscript's running text.
_FONT_VARIANTS = {
    (False, False): "/Library/Fonts/AdobeDevanagari-Regular.otf",
    (True, False): "/Library/Fonts/AdobeDevanagari-Bold.otf",
    (False, True): "/Library/Fonts/AdobeDevanagari-Italic.otf",
    (True, True): "/Library/Fonts/AdobeDevanagari-BoldItalic.otf",
}
DEFAULT_FONT_PATH = _FONT_VARIANTS[(False, False)]

# Used only to *measure* non-Devanagari runs (punctuation, arrows, Latin)
# interspersed in the same <text> element, so mixed-script lines position
# correctly — never used to outline anything. A full-coverage font keeps
# stray symbols like U+2192 (→) from failing to measure.
_MEASURE_FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

# The Latin font stack confirmed to trigger the Cairo PDF ligature/cluster
# bug (see module docstring). Substring-matched against a <text>/<tspan>'s
# own font-family attribute — deliberately narrow, so ordinary figures
# using other fonts are never touched.
RISKY_LATIN_FONT_MARKER = "Gentium Book Plus"

# fontconfig resolves 'Gentium Book Plus'/'Charis SIL' to a generic
# fallback on this system (neither is installed) — Charter IS installed
# and is the stack's next preference, so that's what actually renders and
# what we outline with. Charter.ttc is a collection; each style is a
# separate face index within the one file.
_LATIN_FONT_PATH = "/System/Library/Fonts/Supplemental/Charter.ttc"
_LATIN_FACE_INDEX = {
    (False, False): 0,  # Roman
    (True, False): 3,  # Bold
    (False, True): 1,  # Italic
    (True, True): 2,  # Bold Italic
}


def resolve_font_path(font_weight: str = "", font_style: str = "") -> str:
    """Map SVG font-weight/font-style values to the matching Adobe Devanagari
    file. Weight is bold at 600+ or the literal 'bold'; anything else is
    treated as regular."""
    is_bold = font_weight.strip().lower() == "bold" or (
        font_weight.strip().isdigit() and int(font_weight.strip()) >= 600
    )
    is_italic = font_style.strip().lower() == "italic"
    return _FONT_VARIANTS[(is_bold, is_italic)]


def resolve_latin_font(font_weight: str = "", font_style: str = "") -> tuple[str, int]:
    """Same idea as resolve_font_path, but for the Charter.ttc collection
    used to outline risky Latin runs — returns (path, face_index)."""
    is_bold = font_weight.strip().lower() == "bold" or (
        font_weight.strip().isdigit() and int(font_weight.strip()) >= 600
    )
    is_italic = font_style.strip().lower() == "italic"
    return _LATIN_FONT_PATH, _LATIN_FACE_INDEX[(is_bold, is_italic)]


def contains_risky_latin_font(font_family: str) -> bool:
    return RISKY_LATIN_FONT_MARKER in font_family


def contains_devanagari(text: str) -> bool:
    return bool(DEVANAGARI_RE.search(text))


# Live text can carry an arrow or similar symbol under a Devanagari-named
# font-family (e.g. '⟫ →' set in 'Noto Serif Devanagari','Adobe
# Devanagari',serif so it sits flush against an adjacent Devanagari atom
# bracket) without containing any actual Devanagari codepoints and without
# matching RISKY_LATIN_FONT_MARKER -- neither existing trigger catches it,
# so it stays live and inherits whatever glyph each machine's fontconfig
# resolution happens to pick for that font stack. Confirmed real
# 2026-08-15 on gana_mechanisms_activation.svg: the same "⟫ →" text
# rendered a correct arrowhead locally (Noto Serif Devanagari isn't
# installed on this Mac, so Adobe Devanagari renders it) but a bare dash
# with no head on amrut (which has both fonts, and Noto Serif Devanagari
# -- listed first in the stack -- has an inadequate glyph for it). A
# character in this set forces outlining regardless of font-family or
# script content, so the correct fallback-font-baked glyph (see
# _split_by_font_coverage) is what ships, independent of either
# machine's live font resolution.
_RISKY_SYMBOL_CHARS = "→↔⟶"


def contains_risky_symbol(text: str) -> bool:
    return any(ch in _RISKY_SYMBOL_CHARS for ch in text)


@dataclass
class _FontResources:
    ttfont: TTFont
    hb_font: hb.Font
    units_per_em: int
    ascender: float
    descender: float
    glyph_set: object


@lru_cache(maxsize=16)
def _load_font(font_path: str, face_index: int = 0) -> _FontResources:
    ttfont = TTFont(font_path, fontNumber=face_index) if font_path.lower().endswith((".ttc", ".otc")) else TTFont(font_path)
    units_per_em = ttfont["head"].unitsPerEm
    os2 = ttfont["OS/2"]
    ascender = os2.sTypoAscender
    descender = os2.sTypoDescender  # negative, per spec

    with open(font_path, "rb") as f:
        font_data = f.read()
    hb_face = hb.Face(font_data, face_index)
    hb_font = hb.Font(hb_face)

    return _FontResources(
        ttfont=ttfont,
        hb_font=hb_font,
        units_per_em=units_per_em,
        ascender=ascender,
        descender=descender,
        glyph_set=ttfont.getGlyphSet(),
    )


def _shape(text: str, font_path: str, face_index: int = 0) -> tuple[list, list, _FontResources]:
    res = _load_font(font_path, face_index)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(res.hb_font, buf)
    return buf.glyph_infos, buf.glyph_positions, res


# Charter.ttc has no glyph at all for → and a handful of other symbols
# routinely used as the book's own notation (transformation arrows in
# derivation chains, etc.) -- HarfBuzz reports glyph 0 (.notdef) for
# them, which fontTools draws as a literal box, baked permanently into
# the outlined <path>. Confirmed real 2026-08-15 on
# figures/building_kriya/gana_mechanisms_activation.svg: every 'pac →
# pacati'-style arrow in the IAST derivation column outlined as a solid
# tofu box. Apple Symbols.ttf carries broad arrow/math-symbol coverage
# and only needs to be present on this authoring machine at bake time --
# outlining runs once, locally, and produces static vector paths that
# render identically everywhere afterward, so the fallback font itself
# never needs to ship or be installed on amrut.
_FALLBACK_SYMBOL_FONT_PATH = "/System/Library/Fonts/Apple Symbols.ttf"


def _has_glyph(ch: str, font_path: str, face_index: int = 0) -> bool:
    res = _load_font(font_path, face_index)
    return ord(ch) in res.ttfont.getBestCmap()


def _split_by_font_coverage(
    text: str, font_path: str, face_index: int = 0
) -> list[tuple[str, bool]]:
    """Split into maximal runs of (substring, needs_fallback) -- mirrors
    _split_runs' Devanagari/Latin split, one layer further in: within a
    single Latin run, some characters (arrows, math symbols) aren't in
    the primary font at all. Charter has a space glyph, so plain spaces
    stay in whichever run they fall between rather than forcing a split."""
    if not text:
        return []
    runs: list[tuple[str, bool]] = []
    cur = text[0]
    cur_fallback = not _has_glyph(text[0], font_path, face_index)
    for ch in text[1:]:
        needs_fallback = not _has_glyph(ch, font_path, face_index)
        if needs_fallback == cur_fallback:
            cur += ch
        else:
            runs.append((cur, cur_fallback))
            cur = ch
            cur_fallback = needs_fallback
    runs.append((cur, cur_fallback))
    return runs


def _glyph_path_d(glyph_name: str, glyph_set, scale: float) -> str:
    pen = SVGPathPen(glyph_set)
    glyph_set[glyph_name].draw(pen)
    d = pen.getCommands()
    if not d:
        return ""
    # fontTools emits path data in font units (Y-up). SVG text runs Y-down
    # and our scale already carries the em->pixel conversion, so flip Y here.
    return d


def _run_advance_px(text: str, font_path: str, font_size: float, face_index: int = 0) -> float:
    """Total shaped advance of `text` in this font, in pixels at font_size.
    Re-splits by font coverage (see _split_by_font_coverage) so a
    character the primary font lacks measures against the fallback
    font's own advance instead of silently contributing zero width."""
    total_px = 0.0
    for sub_text, use_fallback in _split_by_font_coverage(text, font_path, face_index):
        sub_font_path = _FALLBACK_SYMBOL_FONT_PATH if use_fallback else font_path
        sub_face_index = 0 if use_fallback else face_index
        _, positions, res = _shape(sub_text, sub_font_path, sub_face_index)
        scale = font_size / res.units_per_em
        total_px += sum(p.x_advance for p in positions) * scale
    return total_px


def _outline_run(
    text: str,
    start_x_px: float,
    y: float,
    font_size: float,
    fill: str,
    font_path: str,
    baseline_shift_units: float,
    face_index: int = 0,
) -> str:
    """Outline one same-script run, placed with its first glyph's pen
    origin at `start_x_px` (already resolved — no anchor math in here).

    Internally re-splits by font coverage: a character missing from
    `font_path` (an arrow, a math symbol -- Charter.ttc has neither)
    routes through _FALLBACK_SYMBOL_FONT_PATH instead of baking that
    font's .notdef glyph, which fontTools draws as a solid box with no
    possible recovery once it's permanent path geometry. Each sub-run
    is shaped and scaled against its own font's metrics, then placed in
    a shared pixel-space cursor so mixed-font runs still line up.
    baseline_shift_units is in the *primary* font's units (that's the
    font its caller measured ascender/descender from for a middle-
    baseline segment) and is converted to pixels once, up front, so it
    applies uniformly regardless of which font placed a given glyph."""
    primary_res = _load_font(font_path, face_index)
    baseline_shift_px = baseline_shift_units * (font_size / primary_res.units_per_em)

    paths = []
    cursor_px = 0.0
    for sub_text, use_fallback in _split_by_font_coverage(text, font_path, face_index):
        sub_font_path = _FALLBACK_SYMBOL_FONT_PATH if use_fallback else font_path
        sub_face_index = 0 if use_fallback else face_index
        infos, positions, res = _shape(sub_text, sub_font_path, sub_face_index)
        scale = font_size / res.units_per_em

        run_cursor_x = 0.0
        run_cursor_y = 0.0
        order = res.ttfont.getGlyphOrder()
        for info, pos in zip(infos, positions):
            glyph_name = order[info.codepoint]
            gx = run_cursor_x + pos.x_offset
            gy = run_cursor_y + pos.y_offset
            d = _glyph_path_d(glyph_name, res.glyph_set, scale)
            if d:
                px = start_x_px + cursor_px + gx * scale
                # Font space is Y-up; SVG is Y-down, and glyph outlines
                # are drawn with the origin at the glyph's own baseline,
                # so flip the scale's sign for Y and shift by the
                # already-pixel-converted baseline offset.
                py = y - gy * scale + baseline_shift_px
                paths.append(
                    f'<path transform="translate({px:.2f},{py:.2f}) scale({scale:.6f},{-scale:.6f})" d="{d}"/>'
                )
            run_cursor_x += pos.x_advance
            run_cursor_y += pos.y_advance
        cursor_px += run_cursor_x * scale
    return "".join(paths)


# --- textPath support: flatten the referenced path, walk it by arc-length ---

_PATH_TOKEN_RE = re.compile(r"[MLAZmlaz]|-?\d*\.?\d+(?:[eE][-+]?\d+)?")


def _sample_arc(
    p0: tuple[float, float],
    rx: float,
    ry: float,
    x_axis_rotation_deg: float,
    large_arc_flag: float,
    sweep_flag: float,
    p1: tuple[float, float],
    n_samples: int = 24,
) -> list[tuple[float, float]]:
    """Endpoint-to-center conversion for one SVG elliptical-arc command
    (W3C SVG 1.1 Appendix F.6.5), then sampled at n_samples evenly-spaced
    points. Every `A` command found in this repo's textPath-referenced
    paths is a single arc (confirmed by audit), so exactness beyond
    visual smoothness isn't needed — this is deliberately a sampled
    approximation, not an exact arc-length parameterization."""
    x0, y0 = p0
    x1, y1 = p1
    if rx == 0 or ry == 0 or (x0 == x1 and y0 == y1):
        return [p1]
    phi = math.radians(x_axis_rotation_deg)
    cos_phi, sin_phi = math.cos(phi), math.sin(phi)
    dx2, dy2 = (x0 - x1) / 2.0, (y0 - y1) / 2.0
    x1p = cos_phi * dx2 + sin_phi * dy2
    y1p = -sin_phi * dx2 + cos_phi * dy2
    rx, ry = abs(rx), abs(ry)
    lam = (x1p ** 2) / (rx ** 2) + (y1p ** 2) / (ry ** 2)
    if lam > 1:
        s = math.sqrt(lam)
        rx *= s
        ry *= s
    sign = -1.0 if large_arc_flag == sweep_flag else 1.0
    num = rx ** 2 * ry ** 2 - rx ** 2 * y1p ** 2 - ry ** 2 * x1p ** 2
    den = rx ** 2 * y1p ** 2 + ry ** 2 * x1p ** 2
    co = sign * math.sqrt(max(num / den, 0.0)) if den else 0.0
    cxp = co * (rx * y1p / ry)
    cyp = co * (-ry * x1p / rx)
    cx = cos_phi * cxp - sin_phi * cyp + (x0 + x1) / 2.0
    cy = sin_phi * cxp + cos_phi * cyp + (y0 + y1) / 2.0

    def _angle(ux: float, uy: float, vx: float, vy: float) -> float:
        length = math.sqrt((ux ** 2 + uy ** 2) * (vx ** 2 + vy ** 2))
        if not length:
            return 0.0
        dot = max(-1.0, min(1.0, (ux * vx + uy * vy) / length))
        ang = math.acos(dot)
        return -ang if ux * vy - uy * vx < 0 else ang

    theta1 = _angle(1.0, 0.0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dtheta = _angle((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not sweep_flag and dtheta > 0:
        dtheta -= 2 * math.pi
    elif sweep_flag and dtheta < 0:
        dtheta += 2 * math.pi

    points = []
    for k in range(1, n_samples + 1):
        t = theta1 + dtheta * k / n_samples
        ex = cx + rx * math.cos(t) * cos_phi - ry * math.sin(t) * sin_phi
        ey = cy + rx * math.cos(t) * sin_phi + ry * math.sin(t) * cos_phi
        points.append((ex, ey))
    return points


def _parse_path_d(d: str) -> list[tuple[float, float]]:
    """Flatten an SVG path's `d=` string into a polyline dense enough for
    linear interpolation between consecutive points to look smooth,
    including through elliptical-arc segments (sampled via _sample_arc).
    Only M/L/A/Z are implemented — the full command set isn't needed
    here, since every path a textPath references in this repo uses only
    those (confirmed by audit; see module docstring)."""
    tokens = _PATH_TOKEN_RE.findall(d)
    points: list[tuple[float, float]] = []
    cur = (0.0, 0.0)
    start = (0.0, 0.0)
    cmd = ""
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in "MLAZmlaz":
            cmd = tok
            i += 1
            continue
        if cmd in ("M", "m"):
            x, y = float(tokens[i]), float(tokens[i + 1])
            if cmd == "m" and points:
                x += cur[0]
                y += cur[1]
            cur = (x, y)
            start = cur
            points.append(cur)
            i += 2
            cmd = "L" if cmd == "M" else "l"  # implicit lineto per SVG spec
        elif cmd in ("L", "l"):
            x, y = float(tokens[i]), float(tokens[i + 1])
            if cmd == "l":
                x += cur[0]
                y += cur[1]
            cur = (x, y)
            points.append(cur)
            i += 2
        elif cmd in ("A", "a"):
            rx, ry, xrot, large, sweep, x, y = (float(tokens[i + k]) for k in range(7))
            if cmd == "a":
                x += cur[0]
                y += cur[1]
            points.extend(_sample_arc(cur, rx, ry, xrot, large, sweep, (x, y)))
            cur = (x, y)
            i += 7
        elif cmd in ("Z", "z"):
            points.append(start)
            cur = start
            i += 1
        else:
            i += 1  # defensive: skip an unrecognized token rather than loop forever
    return points


@dataclass
class _PathGeom:
    points: list[tuple[float, float]]
    cum_lengths: list[float]  # cum_lengths[i] = distance from points[0] through points[i]

    @property
    def total_length(self) -> float:
        return self.cum_lengths[-1] if self.cum_lengths else 0.0

    def point_and_angle_at(self, s: float) -> tuple[float, float, float]:
        """Position and tangent angle (radians) at arc-length s, clamped
        to the path's own extent (a textPath's shaped text can slightly
        overrun a very short path; clamping keeps that a visual nudge
        rather than an index error)."""
        if not self.points:
            return (0.0, 0.0, 0.0)
        if len(self.points) == 1:
            return (*self.points[0], 0.0)
        s = max(0.0, min(s, self.total_length))
        lo, hi = 0, len(self.cum_lengths) - 1
        while lo < hi - 1:
            mid = (lo + hi) // 2
            if self.cum_lengths[mid] <= s:
                lo = mid
            else:
                hi = mid
        seg_len = self.cum_lengths[hi] - self.cum_lengths[lo]
        t = (s - self.cum_lengths[lo]) / seg_len if seg_len > 1e-9 else 0.0
        x0, y0 = self.points[lo]
        x1, y1 = self.points[hi]
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        angle = math.atan2(y1 - y0, x1 - x0)
        return (x, y, angle)


@lru_cache(maxsize=64)
def _build_path_geom(d: str) -> _PathGeom:
    points = _parse_path_d(d)
    cum = [0.0]
    for i in range(1, len(points)):
        x0, y0 = points[i - 1]
        x1, y1 = points[i]
        cum.append(cum[-1] + math.hypot(x1 - x0, y1 - y0))
    return _PathGeom(points, cum)


def _outline_run_on_path(
    text: str,
    geom: _PathGeom,
    start_s: float,
    font_size: float,
    font_path: str,
    face_index: int = 0,
) -> str:
    """Same shape-then-bake approach as _outline_run, but each glyph's
    origin is placed at the path point for its own cumulative advance
    from start_s (SVG's own textPath placement rule) instead of walking
    the x-axis, and rotated to the path's local tangent there — this is
    what makes the outlined glyphs actually follow the curve."""
    infos, positions, res = _shape(text, font_path, face_index)
    scale = font_size / res.units_per_em
    order = res.ttfont.getGlyphOrder()

    cursor_px = 0.0
    paths = []
    for info, pos in zip(infos, positions):
        glyph_name = order[info.codepoint]
        s = start_s + cursor_px + pos.x_offset * scale
        px, py, angle = geom.point_and_angle_at(s)
        cursor_px += pos.x_advance * scale
        d = _glyph_path_d(glyph_name, res.glyph_set, scale)
        if not d:
            continue
        angle_deg = math.degrees(angle)
        paths.append(
            f'<path transform="translate({px:.2f},{py:.2f}) rotate({angle_deg:.3f}) '
            f'scale({scale:.6f},{-scale:.6f})" d="{d}"/>'
        )
    return "".join(paths)


def _split_runs(text: str) -> list[tuple[str, bool]]:
    """Split into maximal runs of (substring, is_devanagari).

    text arrives here straight from a regex capture on the raw SVG
    source, so it's still XML-escaped -- an apostrophe written as
    &#39; (valid, common XML/SVG-authoring-tool output) shapes and
    outlines as the literal six characters '&#39;' if not unescaped
    first. Confirmed real 2026-08-15: korean_extracted_engineered_
    script.svg baked "k&#39;" instead of "k'" onto the page, on both
    local and amrut renders identically -- not a version artifact,
    a genuine missing unescape. html.unescape() correctly handles
    both named (&amp;, &lt;) and numeric (&#39;, &#x2019;) references,
    which covers the whole XML entity set this file ever needs to
    round-trip. The live-text output path in _render_segments()
    re-escapes before writing back out, so this doesn't leave
    invalid XML behind for any segment that ends up staying live."""
    if not text:
        return []
    text = html.unescape(text)
    runs: list[tuple[str, bool]] = []
    cur = text[0]
    cur_is_deva = bool(_DEVANAGARI_CHAR_RE.match(text[0]))
    for ch in text[1:]:
        is_deva = bool(_DEVANAGARI_CHAR_RE.match(ch))
        if is_deva == cur_is_deva:
            cur += ch
        else:
            runs.append((cur, cur_is_deva))
            cur = ch
            cur_is_deva = is_deva
    runs.append((cur, cur_is_deva))
    return runs


@dataclass
class Segment:
    text: str
    font_path: str  # the outline font to use — empty string means "leave live"
    live_font_family: str  # the font-family to render live, if not outlined
    font_size: float  # this segment's own size — a tspan's font-size="" override
    # wins over its parent <text>'s; every construction site must pass one
    # explicitly rather than falling back to a module-level default, so a
    # missing value fails loudly instead of silently baking the wrong size
    # (confirmed real 2026-08-15: a tspan's font-size="28" override was
    # dropped in favor of its parent <text>'s font-size="38" because
    # nothing on this class carried a per-segment size at all).
    font_style: str = "normal"  # carried through to live <text> for italics
    extra_dx: float = 0.0  # a tspan's own dx="" — manual kerning, not a space char
    face_index: int = 0  # sub-font index, for TTC collections like Charter.ttc


def _render_segments(
    segments: list[Segment],
    x: float,
    y: float,
    *,
    fill: str,
    text_anchor: str,
    dominant_baseline: str,
    extra_attrs: str = "",
) -> str:
    """Shared placement core: measure every segment at its own font_size
    (outlining Devanagari ones against their own font, measuring live ones
    against the universal coverage font), then walk them left-to-right
    applying text-anchor once across the whole combined width."""
    segments = [s for s in segments if s.text]
    if not segments:
        return ""

    widths_px = []
    for seg in segments:
        fp = seg.font_path if seg.font_path else _MEASURE_FONT_PATH
        fi = seg.face_index if seg.font_path else 0
        widths_px.append(seg.extra_dx + _run_advance_px(seg.text, fp, seg.font_size, fi))
    total_width_px = sum(widths_px)

    if text_anchor == "middle":
        anchor_shift_px = -total_width_px / 2.0
    elif text_anchor == "end":
        anchor_shift_px = -total_width_px
    else:
        anchor_shift_px = 0.0

    pieces = []
    cursor_px = x + anchor_shift_px
    for seg, width_px in zip(segments, widths_px):
        cursor_px += seg.extra_dx
        width_px -= seg.extra_dx
        if seg.font_path:
            baseline_shift_units = 0.0
            if dominant_baseline == "middle":
                res = _load_font(seg.font_path, seg.face_index)
                baseline_shift_units = (res.ascender + res.descender) / 2.0
            pieces.append(
                _outline_run(
                    seg.text, cursor_px, y, seg.font_size, fill, seg.font_path,
                    baseline_shift_units, seg.face_index,
                )
            )
        else:
            style_attr = f' font-style="{seg.font_style}"' if seg.font_style != "normal" else ""
            # seg.text was unescaped in _split_runs for correct shaping/
            # measurement even on segments that end up here, live rather
            # than outlined -- re-escape & and < (the two that are ever
            # mandatory inside XML text content) before writing it back
            # out, or an unescaped &amp; source entity would round-trip
            # into a bare & here and corrupt the SVG.
            safe_text = seg.text.replace("&", "&amp;").replace("<", "&lt;")
            pieces.append(
                f'<text x="{cursor_px:.2f}" y="{y:.2f}" font-family="{seg.live_font_family}" '
                f'font-size="{seg.font_size:.2f}" fill="{fill}" dominant-baseline="{dominant_baseline}"'
                f'{style_attr} xml:space="preserve">{safe_text}</text>'
            )
        cursor_px += width_px

    return f'<g fill="{fill}"{extra_attrs}>{"".join(pieces)}</g>'


def outlined_text_svg(
    text: str,
    x: float,
    y: float,
    font_size: float,
    *,
    fill: str = "#000000",
    text_anchor: str = "start",
    dominant_baseline: str = "auto",
    font_path: str = DEFAULT_FONT_PATH,
    live_font_family: str = "sans-serif",
    extra_attrs: str = "",
    force_latin: bool = False,
    font_weight: str = "",
    font_style: str = "",
) -> str:
    """Return SVG markup equivalent to a `<text x=x y=y font-size=font_size
    text-anchor=text_anchor dominant-baseline=dominant_baseline>text</text>`
    element, with every Devanagari run baked to outlined `<path>` geometry
    (immune to the Cairo/PDF Devanagari shaping bug — see module docstring).
    Non-Devanagari runs stay live UNLESS force_latin is set (the element's
    own font-family matched the known-buggy Latin stack), in which case
    they're outlined too, using font_weight/font_style to pick the right
    Charter face.
    """
    latin_font_path, latin_face_index = (
        resolve_latin_font(font_weight, font_style) if force_latin else ("", 0)
    )
    segments = []
    for run_text, is_deva in _split_runs(text):
        if not run_text:
            continue
        if is_deva:
            segments.append(Segment(run_text, font_path, live_font_family, font_size))
        elif force_latin:
            segments.append(Segment(run_text, latin_font_path, live_font_family, font_size, face_index=latin_face_index))
        else:
            segments.append(Segment(run_text, "", live_font_family, font_size))
    return _render_segments(
        segments, x, y,
        fill=fill, text_anchor=text_anchor, dominant_baseline=dominant_baseline,
        extra_attrs=extra_attrs,
    )


# --- Whole-SVG substitution: <text>devanagari</text> -> outlined <g> -------

_TEXT_EL_RE = re.compile(r'<text\b(?P<attrs>[^>]*)>(?P<content>[^<]*)</text>')
_TEXT_WITH_TSPANS_RE = re.compile(
    r'<text\b(?P<attrs>[^>]*)>(?P<inner>(?:(?!</text>).)*<tspan\b(?:(?!</text>).)*)</text>',
    re.DOTALL,
)
_TSPAN_RE = re.compile(r'<tspan\b(?P<attrs>[^>]*)>(?P<content>[^<]*)</tspan>')
_ATTR_RE = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')

# <text ATTRS><textPath TP_ATTRS>CONTENT</textPath></text> — arc-band labels
# (place-of-articulation names on the vocal-tract figures, PIE-overlay
# group labels, etc; see module docstring). Matches the one shape every
# real instance in this repo actually takes: a single plain-text run, no
# nested <tspan>. A textPath wrapping something more complex than that
# doesn't match this regex and is left untouched, same as the dy=... case
# above — better to skip than mis-transform.
_TEXT_TEXTPATH_RE = re.compile(
    r'<text\b(?P<attrs>[^>]*)>\s*<textPath\b(?P<tp_attrs>[^>]*)>(?P<content>[^<]*)</textPath>\s*</text>'
)
_PATH_WITH_ID_RE = re.compile(r'<path\b(?P<attrs>[^>]*)/?>')


def _parse_attrs(attrs_str: str) -> dict[str, str]:
    return dict(_ATTR_RE.findall(attrs_str))


# Attributes that must survive onto the replacement <g> unchanged — losing
# any of these silently breaks the figure. transform is the one that bit
# us first (rotated column headers piled up at the wrong angle once their
# <text> was replaced by an untransformed <g>); the rest are cheap
# insurance against the same class of bug.
_PASSTHROUGH_ATTRS = ("transform", "opacity", "clip-path", "class")


def _build_passthrough_attrs(attrs: dict[str, str]) -> str:
    parts = []
    for name in _PASSTHROUGH_ATTRS:
        if name in attrs:
            parts.append(f' {name}="{attrs[name]}"')
    return "".join(parts)


def _segments_from_text_element(base_attrs: dict[str, str], inner: str) -> list[Segment]:
    """Parse a `<text>` element's inner content — a mix of bare text nodes
    and `<tspan>` children, each with attributes that override the parent's
    — into a flat, ordered Segment list. Each node is further split into
    Devanagari/non-Devanagari runs, same as the plain-string case."""
    segments: list[Segment] = []

    def add_node(text: str, weight: str, style: str, family: str, size: float, dx: float = 0.0) -> None:
        deva_font_path = resolve_font_path(weight, style)
        outline_latin_too = contains_risky_latin_font(family) or contains_risky_symbol(text)
        latin_font_path, latin_face_index = (
            resolve_latin_font(weight, style) if outline_latin_too else ("", 0)
        )
        first = True
        for run_text, is_deva in _split_runs(text):
            if not run_text:
                continue
            if is_deva:
                fp, fi = deva_font_path, 0
            elif outline_latin_too:
                fp, fi = latin_font_path, latin_face_index
            else:
                fp, fi = "", 0
            segments.append(
                Segment(
                    run_text,
                    fp,
                    family,
                    size,
                    font_style=style if style else "normal",
                    extra_dx=dx if first else 0.0,
                    face_index=fi,
                )
            )
            first = False

    base_weight = base_attrs.get("font-weight", "")
    base_style = base_attrs.get("font-style", "")
    base_family = base_attrs.get("font-family", "sans-serif")
    base_size = float(base_attrs.get("font-size", 16))

    pos = 0
    for m in _TSPAN_RE.finditer(inner):
        # Bare text between the previous tspan (or start) and this one —
        # note: a lone space here is meaningful (e.g. between two tspans)
        # and must not be dropped just because .strip() would empty it.
        leading = inner[pos:m.start()]
        if leading:
            add_node(leading, base_weight, base_style, base_family, base_size)
        tspan_attrs = _parse_attrs(m.group("attrs"))
        # A tspan's own dx="" is manual kerning (no space character in the
        # source), e.g. `<tspan ... dx="10">sparśa</tspan>` right after a
        # Devanagari word — without it, the two runs visually collide.
        dx = float(tspan_attrs.get("dx", 0) or 0)
        # A tspan's own font-size="" override — e.g. a smaller status word
        # appended after a larger akṣara in the same cell — must win over
        # the parent <text>'s size; falling back to it silently (as this
        # used to) bakes the wrong size with no warning.
        size = float(tspan_attrs.get("font-size", base_size) or base_size)
        add_node(
            m.group("content"),
            tspan_attrs.get("font-weight", base_weight),
            tspan_attrs.get("font-style", base_style),
            tspan_attrs.get("font-family", base_family),
            size,
            dx=dx,
        )
        pos = m.end()
    trailing = inner[pos:]
    if trailing:
        add_node(trailing, base_weight, base_style, base_family, base_size)

    return segments


_TSPAN_DY_RE = re.compile(r'<tspan\b(?P<attrs>[^>]*)>(?P<content>[^<]*)</tspan>')


def _outline_multiline_text_element(attrs: dict[str, str], inner: str) -> str | None:
    """Handle the "each tspan is one full line" shape — either `dy="..."`
    (relative, accumulates from the previous line, SVG's normal line-
    wrapping idiom) or absolute `y="..."` per tspan (each line's own
    final position, no accumulation) — the case `replace_with_tspans`
    used to skip outright. Renders each line with the same per-line
    placement core the single-line path uses, then wraps the lines in
    one outer <g> carrying the original element's transform/passthrough
    attrs.

    Confirmed real 2026-08-15 on stha_vivimorphosis.svg: three cognate
    labels ('Afghāni-stān', 'Uzbeki-stān', 'Turkmeni-stān') set as
    `<tspan x="0" y="0">`/`y="9.7"`/`y="19.4"` under one <text> rendered
    correctly as long as the block stayed live (native SVG respects a
    tspan's own y), then collapsed onto a single overlapping line the
    moment something else made the block eligible for outlining -- this
    function previously recognized only the dy convention, so a y-only
    block fell through to the single-line path, which has no per-
    segment y at all and just concatenates every tspan horizontally at
    the parent's one y.

    Returns None if `inner` doesn't actually match either shape this
    handles (bare text between tspans, or a tspan with neither dy nor
    y) — the caller then falls back to skip-and-warn rather than
    mis-render."""
    tspans = list(_TSPAN_DY_RE.finditer(inner))
    if not tspans:
        return None
    # Reject if there's non-whitespace text outside or between the tspans —
    # the parser only understands "each line is its own tspan, back to back".
    gaps = [inner[:tspans[0].start()]] + [
        inner[a.end():b.start()] for a, b in zip(tspans, tspans[1:])
    ] + [inner[tspans[-1].end():]]
    if any(gap.strip() for gap in gaps):
        return None
    for m in tspans:
        tspan_attrs = _parse_attrs(m.group("attrs"))
        if "dy" not in tspan_attrs and "y" not in tspan_attrs:
            return None

    base_x = float(attrs.get("x", 0))
    base_y = float(attrs.get("y", 0))
    font_size = float(attrs.get("font-size", 16))
    fill = attrs.get("fill", "#000000")
    text_anchor = attrs.get("text-anchor", "start")
    dominant_baseline = attrs.get("dominant-baseline", "auto")

    y_cursor = base_y
    lines = []
    for m in tspans:
        tspan_attrs = _parse_attrs(m.group("attrs"))
        if "dy" in tspan_attrs:
            y_cursor += float(tspan_attrs["dy"])
        else:
            # Absolute y, per the SVG spec, overrides rather than adds —
            # not base_y + y, just y.
            y_cursor = float(tspan_attrs["y"])
        line_x = float(tspan_attrs.get("x", base_x))
        line_attrs = dict(attrs)
        line_attrs["font-weight"] = tspan_attrs.get("font-weight", attrs.get("font-weight", ""))
        line_attrs["font-style"] = tspan_attrs.get("font-style", attrs.get("font-style", ""))
        line_attrs["font-family"] = tspan_attrs.get("font-family", attrs.get("font-family", "sans-serif"))
        line_attrs["font-size"] = tspan_attrs.get("font-size", attrs.get("font-size", str(font_size)))
        segments = _segments_from_text_element(line_attrs, m.group("content"))
        rendered = _render_segments(
            segments, line_x, y_cursor,
            fill=fill, text_anchor=text_anchor, dominant_baseline=dominant_baseline,
        )
        if rendered:
            lines.append(rendered)

    extra_attrs = _build_passthrough_attrs(attrs)
    return f'<g fill="{fill}"{extra_attrs}>{"".join(lines)}</g>'


_STYLE_BLOCK_RE = re.compile(r'<style\b[^>]*>(.*?)</style>', re.DOTALL)
_CSS_CLASS_RULE_RE = re.compile(r'\.([\w-]+)\s*\{([^}]*)\}')
_CSS_DECL_RE = re.compile(r'([\w-]+)\s*:\s*([^;]+);?')
_CLASS_ATTR_RE = re.compile(r'\bclass="([^"]*)"')
_CSS_TO_SVG_ATTR = {"font-family", "font-size", "font-weight", "font-style", "fill"}
_CLASS_BEARING_TAG_RE = re.compile(r'<(text|tspan)\b(?P<attrs>[^>]*)>')


def _inline_css_classes(svg_content: str) -> str:
    """Resolve `class="..."` styling on <text>/<tspan> elements against
    the file's own <style> block and write the result back as literal
    inline attributes, before any other pass runs.

    Every risky-font / Devanagari check in this module reads font-family
    (and friends) off an element's own attributes -- none of them know
    CSS classes exist. A hand-authored SVG that styles text purely
    through `.serif { font-family: ... }`-style classes (no inline
    font-family anywhere) is therefore completely invisible to every fix
    in this file, Devanagari-shaping and arrow-glyph alike. Confirmed
    real 2026-08-15 on mapping_mouth/sound_volume.svg (lineage:
    manual-svg, not a design-tool export): 48 of its 64 text elements
    carry Devanagari, styled entirely via class, none of it ever
    protected by anything in this module. Only font-family, font-size,
    font-weight, font-style, and fill are inlined -- the properties the
    rest of this file actually reads; layout-affecting CSS (transform,
    etc.) is left alone. Only classes actually referencing one of those
    five properties trigger a rewrite, so files with class="" used
    purely for non-text styling (a rect's fill, say) are untouched."""
    style_match = _STYLE_BLOCK_RE.search(svg_content)
    if not style_match:
        return svg_content

    class_props: dict[str, dict[str, str]] = {}
    for rule in _CSS_CLASS_RULE_RE.finditer(style_match.group(1)):
        name, body = rule.group(1), rule.group(2)
        props = {
            prop: val.strip()
            for prop, val in _CSS_DECL_RE.findall(body)
            if prop.strip() in _CSS_TO_SVG_ATTR
        }
        if props:
            class_props[name] = props

    if not class_props:
        return svg_content

    def replace(m: re.Match) -> str:
        tag_name, attrs_str = m.group(1), m.group("attrs")
        class_m = _CLASS_ATTR_RE.search(attrs_str)
        if not class_m:
            return m.group(0)
        existing = _parse_attrs(attrs_str)
        merged: dict[str, str] = {}
        for cls in class_m.group(1).split():
            merged.update(class_props.get(cls, {}))
        # font-size downstream (base_size = float(attrs.get("font-size",
        # ...))) expects a bare number; CSS's own "19px" fails that
        # float() outright. Every other property this function inlines is
        # already bare-value-compatible (font-family/font-weight/font-
        # style/fill don't get float()'d anywhere).
        if "font-size" in merged:
            merged["font-size"] = merged["font-size"].removesuffix("px").strip()
        if "font-family" in merged:
            # CSS font-family quotes multi-word names in double quotes
            # ("Gentium Book Plus", Georgia, serif) -- injecting that
            # verbatim into a double-quoted XML attribute breaks the tag
            # at the first embedded quote. Every other font-family value
            # already in this codebase uses single quotes for exactly
            # this reason; match that convention rather than introducing
            # a second one.
            merged["font-family"] = merged["font-family"].replace('"', "'")
        to_add = {k: v for k, v in merged.items() if k not in existing}
        if not to_add:
            return m.group(0)
        insert = "".join(f' {k}="{v}"' for k, v in to_add.items())
        return f'<{tag_name}{attrs_str}{insert}>'

    return _CLASS_BEARING_TAG_RE.sub(replace, svg_content)


_G_FONT_FAMILY_OPEN_RE = re.compile(r'<g\b[^>]*\bfont-family="([^"]*)"[^>]*>')
_G_TAG_RE = re.compile(r'<g\b[^>]*?(/?)>|</g>')
_TEXT_NO_FONT_FAMILY_OPEN_RE = re.compile(r'<text\b(?![^>]*\bfont-family=)[^>]*>')


def _push_down_ancestor_font_family(svg_content: str) -> str:
    """Make an inherited font-family explicit on every `<text>` that
    doesn't declare its own.

    A `<g font-family="...">` wrapping a flat run of `<text>` children is
    valid, ordinary SVG — the children inherit the family via normal CSS
    cascade rules, same as a `<g fill="...">` wrapper elsewhere in this
    module's own shadow-fix output. But every risky-font / Devanagari
    check in this file inspects only an individual `<text>`/`<tspan>`
    element's own attributes (defaulting to "sans-serif" when absent) —
    it never walks up to an ancestor. A group using this pattern with the
    confirmed-buggy RISKY_LATIN_FONT_MARKER stack is therefore invisible
    to outline_devanagari_in_svg() even when its text contains exactly
    the letter sequences ('fo', 'ft') the bug corrupts. Confirmed
    2026-08-14 on fourth_abrahamic_eschatology.svg: 'Four' and 'before'
    sat unprotected inside such a wrapper.

    Runs once, before every other pass, so the existing per-element
    detection just works afterward without needing to know about
    ancestors at all."""
    out = svg_content
    idx = 0
    while True:
        m = _G_FONT_FAMILY_OPEN_RE.search(out, idx)
        if not m:
            break
        family = m.group(1)
        open_end = m.end()
        depth = 1
        i = open_end
        while depth > 0:
            tm = _G_TAG_RE.search(out, i)
            if not tm:
                raise RuntimeError("unbalanced <g> in _push_down_ancestor_font_family")
            if tm.group(0) == '</g>':
                depth -= 1
                close_start, close_end = tm.start(), tm.end()
            else:
                if not tm.group(1):
                    depth += 1
                close_start = close_end = None
            i = tm.end()
        inner = out[open_end:close_start]
        pushed = _TEXT_NO_FONT_FAMILY_OPEN_RE.sub(
            lambda tm: tm.group(0)[:-1] + f' font-family="{family}">',
            inner,
        )
        out = out[:open_end] + pushed + out[close_start:]
        idx = close_end
    return out


def outline_devanagari_in_svg(svg_content: str) -> tuple[str, int, list[str]]:
    """Replace every `<text>` element that needs it with an equivalent
    outlined `<g>` — either because it contains Devanagari (including ones
    with `<tspan>` children mixing Devanagari and Latin runs, e.g. a word
    beside its italic IAST translit), or because it uses the confirmed-buggy
    Latin font stack (RISKY_LATIN_FONT_MARKER) regardless of script.

    Returns (new_content, count_outlined, warnings).
    """
    warnings: list[str] = []
    count = 0
    svg_content = _inline_css_classes(svg_content)
    svg_content = _push_down_ancestor_font_family(svg_content)

    # --- textPath pass (arc-band labels) — runs first, on the untouched
    # original content, since a <text><textPath>...</textPath></text>
    # element never matches the two passes below (neither looks for a
    # <textPath> child) and doesn't need to interact with them.
    path_ds: dict[str, str] = {}
    for pm in _PATH_WITH_ID_RE.finditer(svg_content):
        pattrs = _parse_attrs(pm.group("attrs"))
        pid = pattrs.get("id")
        pd = pattrs.get("d")
        if pid and pd:
            path_ds[pid] = pd

    def replace_textpath(m: re.Match) -> str:
        nonlocal count
        whole = m.group(0)
        content = m.group("content")
        attrs = _parse_attrs(m.group("attrs"))
        tp_attrs = _parse_attrs(m.group("tp_attrs"))
        live_font_family = attrs.get("font-family", "sans-serif")
        risky_latin = contains_risky_latin_font(live_font_family) or contains_risky_symbol(content)
        has_deva = contains_devanagari(content)
        if not has_deva and not risky_latin:
            return whole
        # Every real instance is single-script (all-Devanagari or all-
        # Latin) — confirmed by audit. A hypothetical mixed run would need
        # the multi-segment placement _render_segments does for straight
        # text, which _outline_run_on_path doesn't implement; skip rather
        # than mis-render if one ever shows up.
        if has_deva and _split_runs(content) != [(content, True)]:
            warnings.append(
                "Skipped a mixed-script <textPath> (only single-script runs "
                "are supported) — outline it by hand if it needs the fix: "
                + whole[:120] + "..."
            )
            return whole

        href = tp_attrs.get("href", "").lstrip("#")
        d = path_ds.get(href)
        if not d:
            warnings.append(
                f"Skipped a <textPath> — href=\"#{href}\" has no matching "
                f"<path id> in this file: " + whole[:120] + "..."
            )
            return whole

        font_weight = attrs.get("font-weight", "")
        font_style = attrs.get("font-style", "")
        if has_deva:
            font_path, face_index = resolve_font_path(font_weight, font_style), 0
        else:
            font_path, face_index = resolve_latin_font(font_weight, font_style)

        font_size = float(attrs.get("font-size", 16))
        geom = _build_path_geom(d)
        offset_raw = tp_attrs.get("startOffset", "0")
        offset_frac = float(offset_raw.rstrip("%")) / 100.0 if offset_raw.endswith("%") else float(offset_raw) / geom.total_length if geom.total_length else 0.0
        raw_s = offset_frac * geom.total_length
        text_width_px = _run_advance_px(content, font_path, font_size, face_index)
        text_anchor = tp_attrs.get("text-anchor", attrs.get("text-anchor", "start"))
        if text_anchor == "middle":
            start_s = raw_s - text_width_px / 2.0
        elif text_anchor == "end":
            start_s = raw_s - text_width_px
        else:
            start_s = raw_s

        count += 1
        fill = attrs.get("fill", "#000000")
        extra_attrs = _build_passthrough_attrs(attrs)
        run = _outline_run_on_path(content, geom, start_s, font_size, font_path, face_index)
        return f'<g fill="{fill}"{extra_attrs}>{run}</g>'

    svg_content = _TEXT_TEXTPATH_RE.sub(replace_textpath, svg_content)

    def replace_with_tspans(m: re.Match) -> str:
        nonlocal count
        whole = m.group(0)
        if (
            not contains_devanagari(m.group("inner"))
            and not contains_risky_latin_font(whole)
            and not contains_risky_symbol(m.group("inner"))
        ):
            return whole
        # Multi-line paragraphs use `dy` on each new-line tspan (plus a
        # reset `x`) to wrap text, or give each line its own absolute
        # `y` directly — either way, a structurally different layout
        # than the "one word + its tspan gloss on the same line" case
        # this parser actually handles. Attempting to place multi-line
        # tspans as one horizontal run smashes them together, which is
        # worse than leaving the element untouched. Skip and flag for
        # manual review. A lone tspan carrying its own y (no siblings)
        # isn't this shape — require at least two before treating y as
        # a line-per-tspan signal, so ordinary single-position tspans
        # keep going through the normal path.
        attrs = _parse_attrs(m.group("attrs"))
        has_dy = bool(re.search(r'<tspan\b[^>]*\bdy\s*=', m.group("inner")))
        y_tspans = re.findall(r'<tspan\b[^>]*\by\s*=', m.group("inner"))
        has_multi_y = len(y_tspans) >= 2
        if has_dy or has_multi_y:
            multiline = _outline_multiline_text_element(attrs, m.group("inner"))
            if multiline is None:
                warnings.append(
                    "Skipped a multi-line <text> (tspan dy=... line-wrapping, "
                    "shape not recognized) — outline it by hand if it needs "
                    "the fix: " + whole[:120] + "..."
                )
                return whole
            count += 1
            return multiline
        segments = _segments_from_text_element(attrs, m.group("inner"))
        count += 1
        return _render_segments(
            segments,
            float(attrs.get("x", 0)),
            float(attrs.get("y", 0)),
            fill=attrs.get("fill", "#000000"),
            text_anchor=attrs.get("text-anchor", "start"),
            dominant_baseline=attrs.get("dominant-baseline", "auto"),
            extra_attrs=_build_passthrough_attrs(attrs),
        )

    svg_content = _TEXT_WITH_TSPANS_RE.sub(replace_with_tspans, svg_content)

    def replace(m: re.Match) -> str:
        nonlocal count
        attrs = _parse_attrs(m.group("attrs"))
        content = m.group("content")
        live_font_family = attrs.get("font-family", "sans-serif")
        risky_latin = contains_risky_latin_font(live_font_family) or contains_risky_symbol(content)
        if not contains_devanagari(content) and not risky_latin:
            return m.group(0)

        x = float(attrs.get("x", 0))
        y = float(attrs.get("y", 0))
        font_size = float(attrs.get("font-size", 16))
        fill = attrs.get("fill", "#000000")
        text_anchor = attrs.get("text-anchor", "start")
        dominant_baseline = attrs.get("dominant-baseline", "auto")
        font_weight = attrs.get("font-weight", "")
        font_style = attrs.get("font-style", "")
        font_path = resolve_font_path(font_weight, font_style)
        count += 1
        return outlined_text_svg(
            content,
            x,
            y,
            font_size,
            fill=fill,
            text_anchor=text_anchor,
            dominant_baseline=dominant_baseline,
            font_path=font_path,
            live_font_family=live_font_family,
            force_latin=risky_latin,
            font_weight=font_weight,
            font_style=font_style,
            extra_attrs=_build_passthrough_attrs(attrs),
        )

    new_content = _TEXT_EL_RE.sub(replace, svg_content)
    return new_content, count, warnings

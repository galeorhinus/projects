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

Requires `uharfbuzz` (shaping) and `fontTools` (outline extraction) — both
live in the project's `.venv-figures/` virtualenv, not the system Python.
"""

from __future__ import annotations

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
    """Total shaped advance of `text` in this font, in pixels at font_size."""
    _, positions, res = _shape(text, font_path, face_index)
    scale = font_size / res.units_per_em
    return sum(p.x_advance for p in positions) * scale


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
    origin at `start_x_px` (already resolved — no anchor math in here)."""
    infos, positions, res = _shape(text, font_path, face_index)
    scale = font_size / res.units_per_em

    cursor_x = 0.0
    cursor_y = 0.0
    placements = []
    order = res.ttfont.getGlyphOrder()
    for info, pos in zip(infos, positions):
        glyph_name = order[info.codepoint]
        placements.append((glyph_name, cursor_x + pos.x_offset, cursor_y + pos.y_offset))
        cursor_x += pos.x_advance
        cursor_y += pos.y_advance

    paths = []
    for glyph_name, gx, gy in placements:
        d = _glyph_path_d(glyph_name, res.glyph_set, scale)
        if not d:
            continue
        px = start_x_px + gx * scale
        # Font space is Y-up; SVG is Y-down, and glyph outlines are drawn
        # with the origin at the glyph's own baseline, so flip the scale's
        # sign for Y and shift by the (already-flipped) baseline offset.
        py = y - (gy - baseline_shift_units) * scale
        paths.append(
            f'<path transform="translate({px:.2f},{py:.2f}) scale({scale:.6f},{-scale:.6f})" d="{d}"/>'
        )
    return "".join(paths)


def _split_runs(text: str) -> list[tuple[str, bool]]:
    """Split into maximal runs of (substring, is_devanagari)."""
    if not text:
        return []
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
    font_style: str = "normal"  # carried through to live <text> for italics
    extra_dx: float = 0.0  # a tspan's own dx="" — manual kerning, not a space char
    face_index: int = 0  # sub-font index, for TTC collections like Charter.ttc


def _render_segments(
    segments: list[Segment],
    x: float,
    y: float,
    font_size: float,
    *,
    fill: str,
    text_anchor: str,
    dominant_baseline: str,
    extra_attrs: str = "",
) -> str:
    """Shared placement core: measure every segment (outlining Devanagari
    ones against their own font, measuring live ones against the universal
    coverage font), then walk them left-to-right applying text-anchor once
    across the whole combined width."""
    segments = [s for s in segments if s.text]
    if not segments:
        return ""

    widths_px = []
    for seg in segments:
        fp = seg.font_path if seg.font_path else _MEASURE_FONT_PATH
        fi = seg.face_index if seg.font_path else 0
        widths_px.append(seg.extra_dx + _run_advance_px(seg.text, fp, font_size, fi))
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
                    seg.text, cursor_px, y, font_size, fill, seg.font_path,
                    baseline_shift_units, seg.face_index,
                )
            )
        else:
            style_attr = f' font-style="{seg.font_style}"' if seg.font_style != "normal" else ""
            pieces.append(
                f'<text x="{cursor_px:.2f}" y="{y:.2f}" font-family="{seg.live_font_family}" '
                f'font-size="{font_size:.2f}" fill="{fill}" dominant-baseline="{dominant_baseline}"'
                f'{style_attr} xml:space="preserve">{seg.text}</text>'
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
            segments.append(Segment(run_text, font_path, live_font_family))
        elif force_latin:
            segments.append(Segment(run_text, latin_font_path, live_font_family, face_index=latin_face_index))
        else:
            segments.append(Segment(run_text, "", live_font_family))
    return _render_segments(
        segments, x, y, font_size,
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

    def add_node(text: str, weight: str, style: str, family: str, dx: float = 0.0) -> None:
        deva_font_path = resolve_font_path(weight, style)
        outline_latin_too = contains_risky_latin_font(family)
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
                    font_style=style if style else "normal",
                    extra_dx=dx if first else 0.0,
                    face_index=fi,
                )
            )
            first = False

    base_weight = base_attrs.get("font-weight", "")
    base_style = base_attrs.get("font-style", "")
    base_family = base_attrs.get("font-family", "sans-serif")

    pos = 0
    for m in _TSPAN_RE.finditer(inner):
        # Bare text between the previous tspan (or start) and this one —
        # note: a lone space here is meaningful (e.g. between two tspans)
        # and must not be dropped just because .strip() would empty it.
        leading = inner[pos:m.start()]
        if leading:
            add_node(leading, base_weight, base_style, base_family)
        tspan_attrs = _parse_attrs(m.group("attrs"))
        # A tspan's own dx="" is manual kerning (no space character in the
        # source), e.g. `<tspan ... dx="10">sparśa</tspan>` right after a
        # Devanagari word — without it, the two runs visually collide.
        dx = float(tspan_attrs.get("dx", 0) or 0)
        add_node(
            m.group("content"),
            tspan_attrs.get("font-weight", base_weight),
            tspan_attrs.get("font-style", base_style),
            tspan_attrs.get("font-family", base_family),
            dx=dx,
        )
        pos = m.end()
    trailing = inner[pos:]
    if trailing:
        add_node(trailing, base_weight, base_style, base_family)

    return segments


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

    def replace_with_tspans(m: re.Match) -> str:
        nonlocal count
        whole = m.group(0)
        if not contains_devanagari(m.group("inner")) and not contains_risky_latin_font(whole):
            return whole
        # Multi-line paragraphs use `dy` on each new-line tspan (plus a
        # reset `x`) to wrap text — a structurally different layout than
        # the "one word + its tspan gloss on the same line" case this
        # parser actually handles. Attempting to place dy-separated lines
        # as one horizontal run smashes them together, which is worse than
        # leaving the element untouched. Skip and flag for manual review.
        if re.search(r'<tspan\b[^>]*\bdy\s*=', m.group("inner")):
            warnings.append(
                "Skipped a multi-line <text> (tspan dy=... line-wrapping) — "
                "outline it by hand if it needs the fix: " + whole[:120] + "..."
            )
            return whole
        attrs = _parse_attrs(m.group("attrs"))
        segments = _segments_from_text_element(attrs, m.group("inner"))
        count += 1
        return _render_segments(
            segments,
            float(attrs.get("x", 0)),
            float(attrs.get("y", 0)),
            float(attrs.get("font-size", 16)),
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
        risky_latin = contains_risky_latin_font(live_font_family)
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

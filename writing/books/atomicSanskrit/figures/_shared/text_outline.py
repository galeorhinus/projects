#!/usr/bin/env python3
"""text_outline.py — shape Devanagari text with HarfBuzz and outline it to SVG paths.

Why this exists: rsvg-convert's PDF backend (Cairo + Pango) mishandles certain
Devanagari glyph clusters — specifically words containing a pre-base
reordering vowel sign (ि, U+093F) or certain conjuncts — when emitting live
PDF text. The corruption is specific to vector-PDF text output: the same SVG
rasterizes to PNG correctly, and single-letter Devanagari is unaffected. See
`working/40_reference/decisions/devanagari_pdf_outline_fix.md` for the full
diagnosis and reproduction steps.

The fix: shape the text correctly ourselves (HarfBuzz resolves the reordering
the same way a browser would), extract the resulting glyph outlines from the
font (fontTools), and bake them into the SVG as `<path>` geometry instead of
a live `<text>` run. A pre-shaped outline can't be mis-shaped downstream —
there's no shaping left for Cairo's PDF backend to get wrong.

Scope: only Devanagari `<text>` content should be outlined. Latin/IAST text
is unaffected by this bug and should stay live (selectable, copyable, and
much smaller in the SVG source).

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


def resolve_font_path(font_weight: str = "", font_style: str = "") -> str:
    """Map SVG font-weight/font-style values to the matching Adobe Devanagari
    file. Weight is bold at 600+ or the literal 'bold'; anything else is
    treated as regular."""
    is_bold = font_weight.strip().lower() == "bold" or (
        font_weight.strip().isdigit() and int(font_weight.strip()) >= 600
    )
    is_italic = font_style.strip().lower() == "italic"
    return _FONT_VARIANTS[(is_bold, is_italic)]


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


@lru_cache(maxsize=8)
def _load_font(font_path: str) -> _FontResources:
    ttfont = TTFont(font_path)
    units_per_em = ttfont["head"].unitsPerEm
    os2 = ttfont["OS/2"]
    ascender = os2.sTypoAscender
    descender = os2.sTypoDescender  # negative, per spec

    with open(font_path, "rb") as f:
        font_data = f.read()
    hb_face = hb.Face(font_data)
    hb_font = hb.Font(hb_face)

    return _FontResources(
        ttfont=ttfont,
        hb_font=hb_font,
        units_per_em=units_per_em,
        ascender=ascender,
        descender=descender,
        glyph_set=ttfont.getGlyphSet(),
    )


def _shape(text: str, font_path: str) -> tuple[list, list, _FontResources]:
    res = _load_font(font_path)
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


def _run_advance_px(text: str, font_path: str, font_size: float) -> float:
    """Total shaped advance of `text` in this font, in pixels at font_size."""
    _, positions, res = _shape(text, font_path)
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
) -> str:
    """Outline one pure-Devanagari run, placed with its first glyph's pen
    origin at `start_x_px` (already resolved — no anchor math in here)."""
    infos, positions, res = _shape(text, font_path)
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
    font_path: str  # the outline font to use, if this segment is Devanagari
    live_font_family: str  # the font-family to render live, if not
    font_style: str = "normal"  # carried through to live <text> for italics
    extra_dx: float = 0.0  # a tspan's own dx="" — manual kerning, not a space char


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
        widths_px.append(seg.extra_dx + _run_advance_px(seg.text, fp, font_size))
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
                res = _load_font(seg.font_path)
                baseline_shift_units = (res.ascender + res.descender) / 2.0
            pieces.append(
                _outline_run(seg.text, cursor_px, y, font_size, fill, seg.font_path, baseline_shift_units)
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
) -> str:
    """Return SVG markup equivalent to a `<text x=x y=y font-size=font_size
    text-anchor=text_anchor dominant-baseline=dominant_baseline>text</text>`
    element, but with every Devanagari run baked to outlined `<path>`
    geometry (immune to the Cairo/PDF Devanagari shaping bug — see module
    docstring) while non-Devanagari runs (punctuation, arrows, Latin/IAST
    mixed into the same run) stay live text, positioned to match.
    """
    segments = [
        Segment(run_text, font_path if is_deva else "", live_font_family)
        for run_text, is_deva in _split_runs(text)
        if run_text
    ]
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


def _segments_from_text_element(base_attrs: dict[str, str], inner: str) -> list[Segment]:
    """Parse a `<text>` element's inner content — a mix of bare text nodes
    and `<tspan>` children, each with attributes that override the parent's
    — into a flat, ordered Segment list. Each node is further split into
    Devanagari/non-Devanagari runs, same as the plain-string case."""
    segments: list[Segment] = []

    def add_node(text: str, weight: str, style: str, family: str, dx: float = 0.0) -> None:
        font_path = resolve_font_path(weight, style)
        first = True
        for run_text, is_deva in _split_runs(text):
            if not run_text:
                continue
            segments.append(
                Segment(
                    run_text,
                    font_path if is_deva else "",
                    family,
                    font_style=style if style else "normal",
                    extra_dx=dx if first else 0.0,
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
    """Replace every `<text>` element whose content contains Devanagari —
    including ones with `<tspan>` children mixing Devanagari and Latin runs
    (e.g. a Devanagari word beside its italic IAST translit) — with an
    equivalent outlined `<g>`.

    Returns (new_content, count_outlined, warnings).
    """
    warnings: list[str] = []
    count = 0

    def replace_with_tspans(m: re.Match) -> str:
        nonlocal count
        if not contains_devanagari(m.group("inner")):
            return m.group(0)
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
        )

    svg_content = _TEXT_WITH_TSPANS_RE.sub(replace_with_tspans, svg_content)

    def replace(m: re.Match) -> str:
        nonlocal count
        attrs = _parse_attrs(m.group("attrs"))
        content = m.group("content")
        if not contains_devanagari(content):
            return m.group(0)

        x = float(attrs.get("x", 0))
        y = float(attrs.get("y", 0))
        font_size = float(attrs.get("font-size", 16))
        fill = attrs.get("fill", "#000000")
        text_anchor = attrs.get("text-anchor", "start")
        dominant_baseline = attrs.get("dominant-baseline", "auto")
        font_path = resolve_font_path(
            attrs.get("font-weight", ""), attrs.get("font-style", "")
        )
        live_font_family = attrs.get("font-family", "sans-serif")
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
        )

    new_content = _TEXT_EL_RE.sub(replace, svg_content)
    return new_content, count, warnings

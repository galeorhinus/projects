#!/usr/bin/env python3
"""
build_book.py — Atomic Sanskrit book assembly + PDF pipeline.

Phases (run any one, or `all` for the full pipeline):
  stubs    — create placeholder draft files for missing chapters
  assemble — concatenate all chapter files into build/atomic_sanskrit.md
  pdf      — render the assembled markdown to PDF via pandoc + xelatex
  all      — run stubs → assemble → pdf (default)
  reference — build the Source and Reference Companion PDF
              (technical appendices + full long-form endnotes;
              reads as_reference_front.md and as_reference.yaml; emits
             build/atomic_sanskrit_reference.{layout}.pdf)

Usage:
  python3 build_book.py                              # full pipeline (default layout)
  python3 build_book.py stubs                        # just generate missing stubs
  python3 build_book.py assemble                     # just concatenate
  python3 build_book.py pdf                          # just render the PDF
  python3 build_book.py stubs --force                # overwrite existing stub files
  python3 build_book.py promote-svgs                 # promote newer figures/**/*.from*.svg
  python3 build_book.py grayscale-images             # create/update figures/*.gray.png
  python3 build_book.py grayscale-images --force     # recreate all figures/*.gray.png
  python3 build_book.py pdf --layout book-on-letter  # book-mock layout on letter paper
  python3 build_book.py pdf --layout trade           # true 6×9 trim size
  python3 build_book.py pdf --layout trade-crop      # 6×9 trim on letter paper with crop marks
  python3 build_book.py pdf --layout phone           # 3×6 phone-reading trim
  python3 build_book.py pdf --endnotes short         # short-form endnotes (printed-book mode)
  python3 build_book.py pdf --endnotes full          # full-form endnotes (default — reference-grade)
  python3 build_book.py pdf --progress-pages 10      # progress line every 10 typeset pages (default 20)
  python3 build_book.py reference --layout trade     # Source and Reference Companion as standalone PDF
  python3 build_book.py convert reference/as_thesis_summary.md        # any .md → build/<name>.pdf (letter)
  python3 build_book.py convert notes.md --layout a4                  # A4 page size
  python3 build_book.py convert notes.md --layout review-a4           # A4 review handout
  python3 build_book.py convert notes.md -o out.pdf                   # custom output path

Layouts:
  letter           8.5×11 paper, 1in margins. Manuscript review.
  book-on-letter   8.5×11 paper with a centered ~4.5×7.5 text block — looks
                   like a 6×9 book page printed inside letter margins.
  trade            True 6×9 trim. For print-on-demand uploads.
  trade-crop       Letter paper with centered 6×9 trim box and crop marks.
  phone            3×6 trim with 0.2in margins. Sized for phone-screen reading.

Endnote modes:
  full             Emits the complete long-form body of each entry from
                   as_endnotes.md (default). Reference-grade content.
  short            Emits only the one-sentence **Short:** field per entry,
                   for the printed-book apparatus. Falls back to full body
                   when the Short field is missing or carries a [TBD: ...]
                   placeholder. Output files are suffixed with .short so the
                   two modes can coexist (e.g., atomic_sanskrit.trade.short.pdf).

Grayscale images:
  grayscale-images scans figures/**/*.png, skips *.gray.png sources, and writes
                   sibling *.gray.png files. Existing grayscale files are
                   regenerated only when missing, older than the color source,
                   or --force is passed. PDF assembly prefers current
                   *.gray.png when present, then current *.png, then the
                   original SVG link.

SVG source promotion:
  promote-svgs scans figures/**/*.from*.svg and promotes the newest source
                   variant to its sibling canonical *.svg when the source is
                   newer than the canonical. The build pipeline runs this
                   preflight automatically before assemble/pdf/reference, so
                   manuscript Markdown can keep linking to stable plain SVGs.

Dependencies:
  - pandoc  (brew install pandoc)
  - xelatex (brew install --cask basictex   or full mactex)
  - Fonts: see as_book.yaml (currently STIX Two Text + Tiro Devanagari Sanskrit)

Canonical metadata source:
  as_book.yaml — title, subtitle, author, fonts, document structure. Edit
values there; this script reads from it via pandoc's --metadata-file.
"""

from __future__ import annotations

import argparse
import datetime
import os
import pty
import json
import re
import select
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Force line-buffered stdout even when it isn't a real terminal (redirected
# to a file, piped to `tee`, captured by a background-task runner). Without
# this every print() in the script sits in a block buffer and only appears
# in one dump when the process exits — the same defect run_pandoc_with_
# progress() works around for the xelatex subprocess, just one level up.
sys.stdout.reconfigure(line_buffering=True)

BOOK_DIR = Path(__file__).resolve().parent
BUILD_DIR = BOOK_DIR / "build"
FIGURES_DIR = BOOK_DIR / "figures"
DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")
METADATA_FILE = BOOK_DIR / "as_book.yaml"
REFERENCE_METADATA_FILE = BOOK_DIR / "as_reference.yaml"
REFERENCE_FRONT_FILE = BOOK_DIR / "companion" / "as_reference_front.md"
REFERENCE_APPENDIX_GLOB = "companion/as_reference_*.md"
PREAMBLE_TEMPLATE = BOOK_DIR / "templates" / "devanagari-preamble.tex.in"
LATEX_STRIKEOUT_FILTER = BOOK_DIR / "filters" / "latex-strikeout.lua"
LATEX_SHORT_FIGURE_CAPTIONS_FILTER = BOOK_DIR / "filters" / "latex-short-figure-captions.lua"

# Reuse the existing figure lineage comment writer. The helper lives under
# figures/_shared, so expose figures/ as an import root for this script.
if str(FIGURES_DIR) not in sys.path:
    sys.path.insert(0, str(FIGURES_DIR))
from _shared.lineage import inject_lineage_comment

# Make sure common macOS TeX install locations are in PATH — some shells
# (especially non-login zsh sessions) don't pick up /Library/TeX/texbin
# from /etc/paths.d, and subprocess inherits whatever PATH we have.
for _texdir in (
    "/Library/TeX/texbin",
    "/usr/local/texlive/2026basic/bin/universal-darwin",
    "/usr/local/texlive/2026/bin/universal-darwin",
    "/usr/local/texlive/2025basic/bin/universal-darwin",
    "/usr/local/texlive/2025/bin/universal-darwin",
):
    if Path(_texdir).is_dir() and _texdir not in os.environ.get("PATH", "").split(":"):
        os.environ["PATH"] = f"{_texdir}:{os.environ.get('PATH', '')}"

# ASSEMBLY data lives in as_book.yaml under the `assembly:` key. Loaded at
# module-import time via parse_assembly_yaml() below. CLAUDE.md names
# as_book.yaml as the single source of truth for document-structure metadata;
# the assembly list belongs there alongside the other structural settings.
# To change reading order, edit as_book.yaml — not this file.
#
# Each entry is a dict:
#   kind      one of {"dedication", "front", "part", "chapter", "end"}
#   file      manuscript filename (None for "part" entries that emit a
#             \part{} break only; otherwise optional prose after \part{})
#   title     canonical title rendered into the assembled markdown
#   subtitle  optional one-line italic subtitle below \part{} for "part"
#             entries — the eclipse-arc map (see
#             working/40_reference/decisions/eclipse_spine_conversion_plan.md). None when
#             absent.


# Stub content sourced from as_toc_annotated.md. Keys are the filenames that
# do not yet have a draft; values are the canonical title and the TOC summary
# that will be planted as placeholder prose.
STUB_FILES = {
    "as_1_10_building_dhatuh.md": {
        "title": "Chapter 10 — Building the *Dhātuḥ*",
        "summary": "The foundational synthesis: how subatomic particles (*varṇāḥ*) combine into elemental atoms (*dhātavaḥ*). *Svarāḥ* (vowels) as protons, *vyañjanāni* (consonants) as electrons; the principle of structural compression that places the thermodynamic threshold at five constituent particles.",
    },
    "as_1_11_building_kriya.md": {
        "title": "Chapter 11 — Building the *Kriyā* (क्रिया): Sanskrit's Molecule",
        "summary": "How the dhātu enters operation. The *gaṇāḥ* as operational classes; the *vikaraṇāni* as the class-signatures that put atoms into motion; the dhātu + vikaraṇa + tiṅ-ending pipeline producing the verbal molecule. Procedural construction first; the reactivity audit (three tiers, cross-corpus invariance, structural axes) lands as evidence the construction leaves the signature of an engineered system.",
    },
    "as_1_12_building_vakya.md": {
        "title": "Chapter 12 — Building the *Vākya* (वाक्य): Sanskrit's Molecular Assembly",
        "summary": "The bonding chemistry that assembles molecules into sentences. The 22 *upasargāḥ* (prefixes) as catalytic functional groups; the *pratyayāḥ* (suffixes) as valence-shell stabilizers. The full pipeline: *varṇaḥ → dhātuḥ → śabdaḥ → padam → vākyam* — complete molecular saturation produces syntactic fluidity.",
    },
}


# PDF page layouts. Each entry is a pandoc -V geometry:... value.
# ── Presentation settings ────────────────────────────────────────────────
#
# Three axes: publication x layout x setting. Everything that varies by page
# size or by which book is being produced lives here, in one table, instead of
# in a parallel dict per setting. Resolution runs most-general to most-
# specific, each step overriding the last:
#
#     PRESENTATION_DEFAULTS
#       -> LAYOUTS[layout]                      (properties of the page)
#       -> PUBLICATIONS[pub]                    (properties of the volume)
#       -> PUBLICATIONS[pub]["by_layout"][layout]   (one volume, one page size)
#
# so a setting is stated once at the broadest level that is true, and restated
# only where it actually differs. Read `setting()` below for the lookup.
#
# This replaced five parallel dicts (LAYOUTS, LAYOUT_FONTSIZES,
# LAYOUT_LINESTRETCH, REFERENCE_LAYOUT_LINESTRETCH, LAYOUT_CHAPTER_FOLIO),
# which covered different subsets of the axes and had to be kept in step by
# hand. They were not: REFERENCE_LAYOUT_LINESTRETCH was missing "b5", so
# `reference --layout b5` assembled the entire companion and then died on a
# bare KeyError. Defaults make that failure mode structurally impossible —
# every lookup resolves.

PRESENTATION_DEFAULTS = {
    "linestretch": "1.10",
    # Back matter is consulted, not read straight through, so a layout may set
    # it smaller than the body without touching the reading experience. None
    # means "follow the body". Appendices and endnotes are a third of the b5
    # book's 526 pages, so this buys more pages than shrinking the body would,
    # and pays for them out of pages nobody reads linearly. Do not go below
    # 9pt: the Devanagari loses its conjuncts and matra strokes before the
    # Latin looks small.
    "appendix_fontsize": None,
    "endnotes_fontsize": None,
    "endnotes_linestretch": None,
    # Print the folio on chapter/part/contents openers. See
    # _SUPPRESS_PLAIN_FOLIO for what turning this off does.
    "chapter_folio": True,
    # Defer LaTeX's \mainmatter until an explicit marker, so front matter
    # keeps roman numerals and the body restarts at arabic 1. A volume that
    # has no front matter to speak of wants this off — see PUBLICATIONS.
    "defer_mainmatter": True,
}

# Per-page-size settings. `geometry` is a pandoc -V geometry:... value.
# A publication may override any of these; see PUBLICATIONS["companion"].
LAYOUTS = {
    "letter": {
        "geometry": "letterpaper,margin=1in",
        "fontsize": "11pt",
    },
    # A4 with 1in margins — for the `convert` subcommand / non-US page size.
    "a4": {
        "geometry": "a4paper,inner=20mm,outer=10mm,top=15mm,bottom=10mm",
        "fontsize": "10.5pt",
        "linestretch": "1.2",
        "chapter_folio": False,
    },
    # Comfortable A4 handout for pre-publication readers. The wider margins
    # keep the line length readable when the PDF is printed at full size.
    "review-a4": {
        "geometry": "a4paper,left=30mm,right=30mm,top=24mm,bottom=24mm",
        "fontsize": "11.5pt",
        "linestretch": "1.15",
    },
    "b5": {
        "geometry": "b5paper,inner=20mm,outer=10mm,top=15mm,bottom=10mm",
        "fontsize": "10.5pt",
        "linestretch": "1.10",
        "appendix_fontsize": "9.75pt",
        "appendix__linestretch": "1.05",
        "endnotes_fontsize": "9pt",
        "endnotes_linestretch": "1.0",
        "chapter_folio": False,
    },
    # ~4.5x7.5 text block centered on 8.5x11 — book-page mock-up on letter paper.
    "book-on-letter": {
        "geometry": "paperwidth=8.5in,paperheight=11in,textwidth=4.75in,textheight=8.0in,centering",
        "fontsize": "10.5pt",
    },
    # True 6x9 trim with book-style asymmetric margins (inner > outer for binding).
    "trade": {
        "geometry": "paperwidth=6in,paperheight=9in,inner=0.75in,outer=0.5in,top=0.5in,bottom=0.75in",
        "fontsize": "10.5pt",
    },
    # 6x9 trim centered on letter paper, with crop marks for local proof printing.
    "trade-crop": {
        "geometry": "paperwidth=8.5in,paperheight=11in,layoutwidth=6in,layoutheight=9in,layouthoffset=1.25in,layoutvoffset=1in,inner=0.75in,outer=0.5in,top=0.5in,bottom=0.75in,showcrop",
        "fontsize": "11pt",
    },
    # Narrow 3x6 trim with minimal margins — sized for phone-screen reading.
    "phone": {
        "geometry": "paperwidth=3.5in,paperheight=7in,margin=0.1in",
        "fontsize": "11pt",
        "chapter_folio": False,
    },
}

# Per-volume settings, and the point at which a second book stops being a
# special case in the code and becomes one entry here. A third (the concise
# edition planned in working/10_active/) is another entry, not another set of
# parallel tables.
PUBLICATIONS = {
    "book": {
        # Nothing to override — the book is what the layout defaults describe.
    },
    "companion": {
        "linestretch": "1.15",
        # The companion sets one size for every page size; give it a layout
        # entry under by_layout to differ.
        "fontsize": "10pt",
        # 426 pages. Roman numerals throughout a volume this size are not
        # front matter, they are the whole book, so number it in arabic from
        # page 1 and let \mainmatter run normally.
        "defer_mainmatter": False,
        "by_layout": {
            "b5": {"linestretch": "1.10"},
            "a4": { "geometry": "a4paper,inner=1.125in,outer=0.4in,top=0.60in,bottom=0.40in",
                    "fontsize": "10pt",
                },
        },
    },
}

_MISSING = object()


def setting(publication: str, layout: str, key: str):
    """Resolve one presentation setting for a publication at a page size.

    Later sources override earlier ones; see the table comments above for the
    order. Raises with a message naming the publication, layout and key rather
    than surfacing a bare KeyError from whichever dict happened to be short."""
    if publication not in PUBLICATIONS:
        raise SystemExit(
            f"build_book.py: unknown publication {publication!r}. "
            f"Known: {', '.join(sorted(PUBLICATIONS))}"
        )
    if layout not in LAYOUTS:
        raise SystemExit(
            f"build_book.py: unknown layout {layout!r}. "
            f"Known: {', '.join(sorted(LAYOUTS))}"
        )
    pub = PUBLICATIONS[publication]
    value = _MISSING
    for source in (
        PRESENTATION_DEFAULTS,
        LAYOUTS[layout],
        pub,
        pub.get("by_layout", {}).get(layout, {}),
    ):
        if key in source:
            value = source[key]
    if value is _MISSING:
        raise SystemExit(
            f"build_book.py: no value for setting {key!r} "
            f"(publication={publication}, layout={layout}). Add it to "
            f"PRESENTATION_DEFAULTS, LAYOUTS[{layout!r}], or "
            f"PUBLICATIONS[{publication!r}]."
        )
    return value


def _assert_presentation_tables_sane() -> None:
    """Fail at import if the tables reference a layout that does not exist, or
    if a layout is missing a setting that has no default.

    Adding a page size used to mean remembering four satellite dicts, and
    nothing said otherwise until a build crashed partway through. Checking
    here turns that into an immediate, named failure."""
    problems = []
    for pub_name, pub in PUBLICATIONS.items():
        for layout in pub.get("by_layout", {}):
            if layout not in LAYOUTS:
                problems.append(
                    f"  PUBLICATIONS[{pub_name!r}]['by_layout'] refers to "
                    f"unknown layout {layout!r}"
                )
    required = ("geometry", "fontsize", "linestretch", "chapter_folio",
                "defer_mainmatter")
    for pub_name in PUBLICATIONS:
        for layout in LAYOUTS:
            for key in required:
                try:
                    setting(pub_name, layout, key)
                except SystemExit as exc:
                    problems.append(f"  {exc}")
    if problems:
        raise SystemExit(
            "build_book.py: presentation tables are inconsistent.\n"
            + "\n".join(problems)
        )


_SUPPRESS_PLAIN_FOLIO = r"\makeatletter\let\ps@plain\ps@empty\makeatother"

# Per-layout base font size (pandoc -V fontsize:...), for the main book build
# (cmd_pdf / cmd_convert). Moved out of as_book.yaml (2026-08-27) for the same
# reason geometry lives here rather than in YAML: font size is layout-
# specific, not a fixed book property — a phone-trim page needs smaller type
# than a full letter page. Every entry defaults to the book's historical
# 12pt; adjust individual layouts here as needed. (as_reference.yaml's own
# `fontsize:` for the Source and Reference Companion is untouched — cmd_reference
# still reads it directly, so the two publications can size independently.)
# Decimal values such as "10.5pt" and "11.25pt" are supported: the build keeps
# a valid class option underneath and uses KOMA-Script's `scrextend` package to
# recalculate the complete LaTeX size ladder from the requested base size.


_WRAPPED_SPAN_RE = re.compile(r"`\{\\[a-zA-Z]+font\s(.*?)\}`\{=latex\}", re.S)


# Font-name -> declaration in the preamble template, so the coverage check can
# ask the same face xelatex will. A placeholder like __DEVANAGARIFONT__ is
# resolved from the book's metadata, the way render_devanagari_preamble() does.
_FONT_DECL_RE = re.compile(
    r"\\newfontfamily\{(\\[a-z]+font)\}(?:\[[^\]]*\])?\{([^}]*)\}"
)
# Same spans as _WRAPPED_SPAN_RE, but keeping the font macro as well as the body.
_WRAPPED_SPAN_FONT_RE = re.compile(
    r"`\{(\\[a-zA-Z]+font)\s(.*?)\}`\{=latex\}", re.S
)


def _resolve_font_file(name: str, metadata_file: Path) -> str:
    """Absolute path to a face, given either a filename or a family name.

    The main font is loaded by path (as_book.yaml's `mainfont` +
    `mainfontdir`), so handing its *filename* to fc-match would silently match
    some unrelated installed family and check coverage against the wrong face.
    Try the declared directory first; fall back to fontconfig for the script
    fonts, which are named by family."""
    import subprocess
    if Path(name).suffix.lower() in {".otf", ".ttf", ".ttc"}:
        directory = read_yaml_value_opt(metadata_file, "mainfontdir")
        if directory:
            candidate = BOOK_DIR / directory / name
            if candidate.exists():
                return str(candidate)
    return subprocess.run(
        ["fc-match", "-f", "%{file}", name],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def _font_coverage(name: str, metadata_file: Path) -> set[int]:
    """Codepoints a face can draw. Cached — assembly asks for the same handful."""
    from fontTools.ttLib import TTCollection, TTFont
    cache = _font_coverage.__dict__.setdefault("_cache", {})
    if name not in cache:
        path = _resolve_font_file(name, metadata_file)
        font = (TTCollection(path).fonts[0] if path.lower().endswith(".ttc")
                else TTFont(path, fontNumber=0))
        cache[name] = set(font.getBestCmap())
    return cache[name]


def _script_font_families(metadata_file: Path) -> dict[str, str]:
    """Map each wrap macro to the family the preamble binds it to."""
    text = PREAMBLE_TEMPLATE.read_text()
    families: dict[str, str] = {}
    for macro, family in _FONT_DECL_RE.findall(text):
        if family.startswith("__") and family.endswith("__"):
            family = read_yaml_value_opt(
                metadata_file, family.strip("_").lower()
            ) or family
        families[macro] = family
    # \latinfont is \rmfamily, i.e. whatever the document's main font is.
    if "\\newcommand{\\latinfont}" in text:
        families["\\latinfont"] = read_yaml_value(metadata_file, "mainfont")
    return families


def _warn_uncovered_script_characters(md_text: str, metadata_file: Path) -> None:
    """Warn when a wrap routes a character to a font that cannot draw it.

    warn_uncovered_characters() strips every wrapped span before checking,
    because those spans are precisely the text the main font does NOT have to
    draw. That leaves a blind spot: a character sent to a script font the
    wrap's own face lacks is invisible to it. On 2026-09-05 Greek, IPA, and
    the click letters were reaching Tiro Devanagari Sanskrit and printing as
    .notdef boxes, and nothing flagged it at assembly -- the evidence was a
    wall of xelatex "Missing character" lines nobody reads. Check the inside
    of the spans too."""
    families = _script_font_families(metadata_file)
    missing: dict[tuple[str, str], dict[str, int]] = {}
    for macro, body in _WRAPPED_SPAN_FONT_RE.findall(md_text):
        family = families.get(macro)
        if not family:
            continue  # _assert_script_fonts_declared already covers this
        try:
            covered = _font_coverage(family, metadata_file)
        except Exception:
            continue  # unresolvable face — the main-font check reports the tooling
        for ch in body:
            if ord(ch) < 0x00A0 or ord(ch) in covered or ch.isspace():
                continue
            slot = missing.setdefault((macro, family), {})
            slot[ch] = slot.get(ch, 0) + 1
    if not missing:
        return
    for (macro, family), chars in sorted(missing.items()):
        print(f"  WARNING: {len(chars)} character(s) are routed to {macro} "
              f"({family}),")
        print("           which cannot draw them — XeLaTeX will DROP them:")
        for ch, n in sorted(chars.items(), key=lambda kv: -kv[1]):
            print(f"             U+{ord(ch):04X} {ch!r}  x{n}")
        print("           Move them to a wrap whose face covers them.")


def warn_uncovered_characters(md_text: str, metadata_file: Path) -> None:
    """Warn about characters the main font cannot draw and no wrap rescues.

    XeLaTeX does not fail on a glyph it lacks — it emits a "Missing character"
    line into a log nobody reads and drops the character from the page. That
    is how the companion shipped Greek ἐστί as στί, and how ≥ vanished from
    the reactivity thresholds: both fonts differ per book (EB Garamond for the
    manuscript, STIX Two Text for the companion), so a character can be fine
    in one and missing from the other.

    Checks what is left after removing every span already routed to a script
    or symbol font, which is exactly the text the main font has to draw.
    Skips silently, with a note, when fontTools or fontconfig is unavailable —
    the same graceful degradation the figure checks use."""
    try:
        import subprocess
        from fontTools.ttLib import TTCollection, TTFont
    except ImportError:
        print("  (skipping font-coverage check — pip install fonttools to enable)")
        return
    try:
        family = read_yaml_value(metadata_file, "mainfont")
        path = _resolve_font_file(family, metadata_file)
        font = TTCollection(path).fonts[0] if path.lower().endswith(".ttc") else TTFont(path, fontNumber=0)
        covered = set(font.getBestCmap())
    except Exception as exc:
        print(f"  (skipping font-coverage check — {type(exc).__name__}: {exc})")
        return

    unwrapped = _WRAPPED_SPAN_RE.sub(" ", md_text)
    missing: dict[str, int] = {}
    for ch in unwrapped:
        o = ord(ch)
        if o < 0x00A0 or o in covered or ch.isspace():
            continue
        missing[ch] = missing.get(ch, 0) + 1
    if missing:
        print(f"  WARNING: {len(missing)} character(s) are not in {family} and are not")
        print("           routed to any script/symbol font — XeLaTeX will DROP them:")
        for ch, n in sorted(missing.items(), key=lambda kv: -kv[1]):
            print(f"             U+{ord(ch):04X} {ch!r}  x{n}")
        print("           Add them to a SCRIPT_WRAPS entry in this file.")
    _warn_uncovered_script_characters(md_text, metadata_file)


_assert_presentation_tables_sane()

# Standard LaTeX classes implement only 10/11/12pt. `extbook` and `extarticle`
# add 8/9/14/17/20pt. Any other numeric size must NOT be passed directly as a
# class option: LaTeX accepts it, prints only an "Unused global option" warning,
# and silently renders at 10pt. For an arbitrary size, the build gives the class
# its nearest supported 10/11/12pt option and loads `scrextend` with the actual
# requested size. `scrextend` recalculates normalsize, notes, captions, lists,
# and the full heading-size ladder without replacing the book/article class.
_BOOK_SIZES = {"10pt", "11pt", "12pt"}
_EXTBOOK_SIZES = {"8pt", "9pt", "14pt", "17pt", "20pt"}
_FONTSIZE_RE = re.compile(r"^(?P<points>(?:\d+(?:\.\d*)?|\.\d+))pt$")
_DECIMAL_FONTSIZE_MIN = 6.0
_DECIMAL_FONTSIZE_MAX = 24.0


def render_decimal_fontsize_header(fontsize: str) -> Path:
    """Write the generated LaTeX header that activates an arbitrary size."""
    BUILD_DIR.mkdir(exist_ok=True)
    safe_name = fontsize.replace(".", "_")
    out = BUILD_DIR / f"fontsize-{safe_name}.tex"
    out.write_text(
        "% Generated by build_book.py; do not edit.\n"
        f"\\usepackage[fontsize={fontsize}]{{scrextend}}\n"
    )
    return out


def fontsize_cli_args(fontsize: str, class_kind: str) -> list[str]:
    """Return safe Pandoc arguments for a requested base font size.

    ``class_kind`` selects the extended class only for exact sizes that
    extsizes implements. Arbitrary integer and decimal sizes retain the
    configured standard class and receive a generated `scrextend` header.
    """
    fontsize = fontsize.strip()
    if class_kind not in {"book", "article"}:
        raise ValueError(f"Unknown document class kind: {class_kind!r}")
    if fontsize in _BOOK_SIZES:
        return ["-V", f"fontsize={fontsize}"]
    if fontsize in _EXTBOOK_SIZES:
        extclass = "extbook" if class_kind == "book" else "extarticle"
        return ["-V", f"fontsize={fontsize}", "-V", f"documentclass={extclass}"]

    match = _FONTSIZE_RE.fullmatch(fontsize)
    if not match:
        raise SystemExit(
            f"Invalid fontsize {fontsize!r}. Use a numeric point value such as "
            '"10.5pt" or "11.25pt".'
        )
    points = float(match.group("points"))
    if not _DECIMAL_FONTSIZE_MIN <= points <= _DECIMAL_FONTSIZE_MAX:
        raise SystemExit(
            f"Unsupported fontsize {fontsize!r}; expected "
            f"{_DECIMAL_FONTSIZE_MIN:g}pt-{_DECIMAL_FONTSIZE_MAX:g}pt."
        )

    # Give the class its nearest supported size, preferring the larger one on
    # an exact tie (10.5 -> 11), then let scrextend replace the full size ladder.
    base_points = min((10, 11, 12), key=lambda value: (abs(value - points), -value))
    header = render_decimal_fontsize_header(fontsize)
    return ["-V", f"fontsize={base_points}pt", "-H", str(header)]


# Regexes for cleaning chapter files before assembly
DRAFT_NOTES_RE   = re.compile(r"\n(?:---\s*\n+)?##+\s+Draft notes(?:\s*\([^)]*\))?.*\Z", re.DOTALL)
DRAFT_HEADER_RE  = re.compile(r"^\*Draft v.*?\*\n+", re.DOTALL | re.MULTILINE)
CHAPTER_HEADER_RE = re.compile(r"^#\s+[^\n]+\n*", re.MULTILINE)
# Part-opener files carry a `# Part X — Title` h1 + italic subtitle + `---`
# rule so Caddy / static-HTML renderers can serve them as standalone pages.
# A Finale bookend may follow the same convention without using a Part number.
# The PDF assembler already emits the title via the LaTeX \part{} directive,
# so strip the duplicate header before inlining the opener prose.
PART_HEADER_RE   = re.compile(
    r"^#\s+(?:Part\s+[0-9IVX]+|Finale)[^\n]*\n+"
    r"(?:\*[^*\n]+\*\s*\n+)?"
    r"(?:---\s*\n+)?",
    re.MULTILINE,
)

# Per-script Unicode ranges for explicit font wrapping. Each entry is
# (font command, regex of script's character range).
# Why wrap: ucharclasses transitions silently fail in many xelatex contexts
# (TOC entries, headings, math-adjacent positions like √मा); the workaround
# is to wrap each script's runs in raw-LaTeX `{\<fontname> …}` so the font
# switch is unconditional inside the wrap group.
SCRIPT_WRAPS: list[tuple[str, re.Pattern]] = [
    # Sindhi implosives (U+097B–U+097F): ॻ ॼ ॽ ॾ ॿ. The configured Sanskrit
    # face has no glyphs for these letters. Ordering alone cannot separate
    # this from the Devanagari rule below — every rule is applied to the
    # whole text, so whichever runs second re-matches the codepoint sitting
    # inside the first one's wrap and nests a second one around it
    # (confirmed: `{\sindhifont `{\devanagarifont ॿ}`{=latex}}` -> "Too many
    # }'s"). The two ranges must therefore be disjoint: the Devanagari rule
    # below stops at U+097A rather than running to the end of the block.
    (r"\sindhifont",      re.compile(r"[ॻ-ॿ]+")),
    # Devanagari block up to U+097A + ZWJ/ZWNJ joiners. See above for why
    # this stops short of ॿ (U+097F) instead of covering the whole block.
    (r"\devanagarifont",  re.compile(r"[ऀ-ॺ‌‍]+")),
    # Vedic Extensions (U+1CD0–U+1CFF). Kept separate because the configured
    # Adobe Devanagari face does not contain signs such as upadhmānīya (ᳶ).
    (r"\vedicfont",       re.compile(r"[᳀-᳿]+")),
    # Arabic block (covers Arabic letters + diacritics)
    (r"\arabicfont",      re.compile(r"[؀-ۿ]+")),
    # Hebrew block (covers Hebrew letters, vowel points, cantillation marks)
    (r"\hebrewfont",      re.compile(r"[֐-׿]+")),
    # Tamil block
    (r"\tamilfont",       re.compile(r"[஀-௿]+")),
    # Telugu block
    (r"\telugufont",      re.compile(r"[ఀ-౿]+")),
    # Kannada block
    (r"\kannadafont",     re.compile(r"[ಀ-೿]+")),
    # Malayalam block
    (r"\malayalamfont",   re.compile(r"[ഀ-ൿ]+")),
    # Hiragana + Katakana (Japanese kana — used in Yenpro / Appendix Part 4)
    (r"\jpfont",          re.compile(r"[぀-ヿ]+")),
    # CJK Unified Ideographs (Chinese characters used in Ch 18 contrast case)
    (r"\cjkfont",         re.compile(r"[一-鿿]+")),
    # Old Persian cuneiform (Mitanni / Indo-Iranian references)
    (r"\oldpersianfont",  re.compile(r"[\U000103A0-\U000103DF]+")),
    # Gothic (used for the Gothic reflex of Sanskrit ⟪युज्⟫ in Chapter 18)
    (r"\gothicfont",      re.compile(r"[\U00010330-\U0001034F]+")),
    # Avestan (Indo-Iranian comparisons)
    (r"\avestanfont",     re.compile(r"[\U00010B00-\U00010B3F]+")),
    # Brāhmī — the Prakrit forms quoted from the pyramid's descent chain in
    # the gaya-gavi endnote. Without a wrap these reach xelatex as ordinary
    # body text and the configured Latin face drops them with only a warning.
    (r"\brahmifont",      re.compile(r"[\U00011000-\U0001107F]+")),
    # Stragglers — specific characters the configured Latin face lacks. Kept
    # narrow so common IAST diacritics (ṃ ṛ ṣ ā ī ū ḥ ñ ṅ etc.) are NOT
    # switched mid-word. The list is the closed set of characters the
    # assembled book uses that STIX Two Text cannot render.
    # Characters STIX Two Text DOES have, but which the full-book build drew
    # from a leaked script font -- Greek printed as .notdef boxes on the page
    # while xelatex reported them "missing" from Tiro Devanagari Sanskrit.
    # Building the same chapter alone renders them correctly, so the fault is
    # ambient font state at book scale, not markup or coverage. Selecting the
    # family explicitly makes the run immune to whatever leaked. Greek
    # Extended is deliberately NOT here: STIX lacks all five forms the book
    # uses, so those stay on \symbolfont below.
    # Characters a leaked Devanagari run would DROP: the ones Tiro Devanagari
    # Sanskrit cannot draw. \latinfont is \rmfamily, so wrapping selects the
    # main family explicitly and the run survives whatever font is current.
    #
    # The set is chosen by that test rather than by which characters happened
    # to warn -- enumerating warnings is whack-a-mole, since the leak hits
    # anything the leaked face lacks. It is also deliberately NOT "everything
    # STIX covers": Tiro has the punctuation, Latin-1 accents and IAST
    # diacritics, so wrapping those bought no protection while putting 1,208
    # raw-LaTeX spans into captions, part titles and TOC entries -- one of
    # which printed as "Part IV '---'=latex The Sun's Atoms".
    #
    # Greek Extended stays on \symbolfont below: STIX lacks all five forms
    # the book uses, so those need DejaVu, not the main family.
    (r"\latinfont",       re.compile(
        "(?:["
        "\u0370-\u03FF"                      # Greek block (ζυγόν, ἀπό's tail)
        "\u01C0\u01C1\u01C3"                 # ǀ ǁ ǃ  click letters
        "\u0105"                             # ą
        "\u0250\u0255\u0263\u026D"          # ɐ ɕ ɣ ɭ
        "\u026F\u0270\u0278"                 # ɯ ɰ ɸ
        "\u0283\u028B\u0291"                 # ʃ ʋ ʑ
        "\u02B0\u02D0"                       # ʰ ː
        "]"
        # Keep a combining mark inside its base's group -- splitting the two
        # across a font switch breaks the composition.
        "[\u0300-\u036F]*)+"
        # An ASCII base carrying a combining mark (r̥, r̩, m̐) needs the same
        # protection: Tiro has no U+0329, so a leaked run drops the mark and
        # silently changes the phonetic form. The + is load-bearing -- without
        # it this branch would match every ordinary letter in the book.
        "|[A-Za-z][\u0300-\u036F]+"
    )),
    (r"\symbolfont",      re.compile(
        r"["
        r"←→"      # ← →
        r"↔"       # left-right arrow
        r"✓✗"      # ✓ ✗ (table cell glyphs)
        r"₀-₉"     # subscript digits ₀-₉
        r"ʷʾʿ"     # modifier letters ʷ ʾ ʿ
        r"ɑɓɗʄɠʈʂʔ"  # rare phonetic symbols used in inventory/endnote examples
        r"ēō"      # ē ō (Latin with macron)
        r"ḱẓǵǎ"    # Latin Extended forms used in comparisons
        r"ἀὑἸὁᾷἐἔ" # polytonic Greek forms absent from STIX Two Text
        r"⟪⟫"      # atomic sound-form brackets
        r"∞"       # infinity
        r"⊇"       # superset-or-equal (Ch 18 §18.x: Sanskrit ⊇ PIE) —
                   # Charter Bold lacks U+2287; Arial Unicode MS has it
        r"≥≤≈"     # comparison operators — the companion's STIX Two Text
                   # lacks all three, and they carry the tier thresholds in
                   # the reactivity tables (">= 50" etc.)
        r"]+"
    )),
]


# Devanagari marks that attach to the preceding base: matras, nukta,
# anusvara/visarga/candrabindu, the accent signs, and the virama itself.
# None may begin a line, and a virama binds the consonant that follows it,
# so neither is ever a break opportunity.
_DEV_VIRAMA = "\u094d"
_DEV_COMBINING = (
    set(range(0x0900, 0x0904))          # candrabindu, anusvara, visarga
    | {0x093A, 0x093B, 0x093C}          # oe matra, ooe matra, nukta
    | set(range(0x093E, 0x094E))        # matras + virama
    | set(range(0x094E, 0x0951))        # prishthamatra e, aw
    | set(range(0x0951, 0x0958))        # vedic accents, stress signs
    | {0x0962, 0x0963}                  # vocalic l/ll matras
    | {0x0964, 0x0965}                  # danda, double danda — keep with the word
)

# Runs shorter than this always fit a line, so leave them untouched rather
# than scattering penalties through every ordinary Sanskrit term.
_DEV_BREAK_MIN_CHARS = 15


def _devanagari_aksaras(run: str) -> list[str]:
    """Split a Devanagari run into aksara clusters — the only legal line-break
    boundaries. A cluster is a base plus everything bound to it, and a virama
    joins its consonant to the next, so conjuncts stay whole."""
    clusters: list[str] = []
    cur = ""
    for ch in run:
        if not cur:
            cur = ch
        elif ord(ch) in _DEV_COMBINING or cur[-1] == _DEV_VIRAMA:
            cur += ch
        else:
            clusters.append(cur)
            cur = ch
    if cur:
        clusters.append(cur)
    return clusters


def _devanagari_with_breaks(run: str) -> str:
    """Insert \\allowbreak between aksaras of a long Devanagari run.

    Devanagari has no hyphenation and a samasa carries no spaces, so a long
    compound is one unbreakable box: TeX cannot split it and it runs past the
    measure. Confirmed on lauhapathagaminisucaka... (39 chars), which
    overflowed the trade text block in Ch 1. XeTeX's own
    \\XeTeXlinebreaklocale was tried first and had no effect here — with
    locale "sa", "hi", or unset the overfull box was identical to the pt.

    Breaking mid-word without a hyphen is correct for Devanagari; what must
    never happen is a break inside a conjunct or before a matra, which is
    what _devanagari_aksaras guarantees."""
    if len(run) < _DEV_BREAK_MIN_CHARS:
        return run
    return "\\allowbreak{}".join(_devanagari_aksaras(run))


# A wrap must never fire inside a markdown code span. The emitted form is
# itself backtick-delimited, so wrapping a character that already sits between
# backticks nests them: pandoc then reads the whole region as inline code and
# escapes the braces, leaving `\devanagarifont` as a live command with no group
# to close it. That switch never reverts, and every later character the
# Devanagari face lacks is dropped from the page -- which is exactly how Greek,
# IPA, and the click letters were vanishing from the full-book build while a
# chapter-alone build of the same source stayed clean (traced 2026-09-05 to
# `∞` in Ch 9 and Ch 13). Matching code spans in the same pass and returning
# them untouched is what keeps the emitted spans from being re-wrapped too.
_MD_CODE_SPAN = r"```.*?```|`+[^`\n]*`+"


def wrap_scripts_for_latex(md_text: str) -> str:
    """Wrap every non-Latin script run in raw-LaTeX `{\\<fontname> …}`.
    Applied during assembly so the rendered PDF has unconditional font
    selection regardless of surrounding TeX context."""
    fired: set[str] = set()
    for font_cmd, pattern in SCRIPT_WRAPS:
        prep = _devanagari_with_breaks if font_cmd == r"\devanagarifont" else (lambda t: t)
        counted = [0]

        def replace(m, _f=font_cmd, _p=prep, _n=counted):
            if m.group("code") is not None:
                return m.group(0)
            _n[0] += 1
            return f"`{{{_f} {_p(m.group('hit'))}}}`{{=latex}}"

        md_text = re.compile(
            f"(?P<code>{_MD_CODE_SPAN})|(?P<hit>{pattern.pattern})", re.S
        ).sub(replace, md_text)
        if counted[0]:
            fired.add(font_cmd)
    _assert_script_fonts_declared(fired)
    return md_text


def _assert_script_fonts_declared(fired: set[str]) -> None:
    """Fail at assembly time if a script wrap emits a font macro the preamble
    never defines.

    This list and the \\newfontfamily block in
    templates/devanagari-preamble.tex.in have to stay in step, and nothing
    enforced that. On 2026-08-10 the Kannada and Malayalam families were
    dropped from the preamble because the manuscript contained neither script,
    while their SCRIPT_WRAPS entries stayed. A single Malayalam character
    added to an endnote months later therefore emitted \\malayalamfont with
    no definition behind it, and xelatex failed 619 pages in with
    "Undefined control sequence" — which points at the symptom, not at the
    two files that disagree. Catch it here instead, before pandoc runs.
    """
    declared = set(
        re.findall(
            r"\\(?:newfontfamily|newcommand)\{(\\[a-z]+font)\}",
            PREAMBLE_TEMPLATE.read_text(),
        )
    )
    missing = sorted(f for f in fired if f not in declared)
    if missing:
        raise SystemExit(
            "Script font(s) used by the manuscript but not declared in\n"
            f"  {PREAMBLE_TEMPLATE.relative_to(BOOK_DIR)}:\n"
            + "".join(f"    {f}\n" for f in missing)
            + "Either add a \\newfontfamily line for each (and confirm the face is\n"
            "installed on every build host), or remove the characters that triggered\n"
            "them. Ranges are listed in SCRIPT_WRAPS in this file."
        )


PDF_IMAGE_RE = re.compile(r"(!\[[^\]]*\]\()([^)\s]+\.(?:svg|png))(\)(?:\{[^}\n]*\})?)")
PDF_IMAGE_MAX_WIDTH_PX = 1800
FROM_SVG_RE = re.compile(r"^(?P<base>.+)\.from[-_](?P<chain>[A-Za-z0-9_-]+)\.svg$")


# Inline scaffold icons (CLAUDE.md "Scaffold-icon deployment in body text")
# are authored as raw HTML <img> so they render in Markdown/HTML preview.
# Pandoc's LaTeX writer drops raw HTML wholesale, so they simply vanish from
# the PDF build with no warning. Fix it at assembly time: parse height /
# vertical-align / scale off the style attribute, ensure a vector-PDF
# sibling of the icon SVG exists, and emit the same raw-LaTeX inline-
# attribute pattern already used for `\hfill` elsewhere in this pipeline.
SCAFFOLD_ICON_IMG_RE = re.compile(
    r'<img\s+src="(?P<src>figures/_shared/icons/scaffold_[a-z0-9]+_(?:gray|black)\.svg)"'
    r'\s+style="(?P<style>[^"]*)"'
    r'\s+alt="[^"]*"\s*/?>'
)


def _css_prop(style: str, prop: str, default: str = "") -> str:
    m = re.search(rf"{prop}\s*:\s*([^;]+)", style)
    return m.group(1).strip() if m else default


def ensure_icon_pdf(svg_path: Path) -> Path | None:
    """Return a cached vector-PDF sibling of an icon SVG, regenerating via
    rsvg-convert when missing or stale. Returns None if rsvg-convert isn't
    on PATH; the caller then leaves the icon as raw HTML (silently dropped
    by pandoc, same as today) rather than failing the whole build."""
    pdf_path = svg_path.with_suffix(".pdf")
    if pdf_path.exists() and pdf_path.stat().st_mtime >= svg_path.stat().st_mtime:
        return pdf_path
    rsvg = shutil.which("rsvg-convert")
    if not rsvg:
        return None
    result = subprocess.run(
        [rsvg, "-f", "pdf", "-o", str(pdf_path), str(svg_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(
            f"  WARNING: rsvg-convert failed for {svg_path.relative_to(BOOK_DIR)}: "
            f"{result.stderr.strip()}",
            file=sys.stderr,
        )
        return None
    return pdf_path


def render_scaffold_icons_for_pdf(md_text: str) -> str:
    """Replace raw-HTML inline scaffold icons with a raw-LaTeX
    \\includegraphics call, so they survive into the PDF instead of being
    silently dropped by pandoc's non-HTML writers."""
    def replace(m: re.Match) -> str:
        svg_path = BOOK_DIR / m.group("src")
        if not svg_path.exists():
            return m.group(0)
        pdf_path = ensure_icon_pdf(svg_path)
        if pdf_path is None:
            return m.group(0)
        style = m.group("style")
        height = _css_prop(style, "height", "1em")
        valign = _css_prop(style, "vertical-align", "0pt")
        scale_m = re.search(r"scale\(([\d.]+)\)", style)
        pdf_rel = pdf_path.relative_to(BOOK_DIR).as_posix()
        inner = f"\\includegraphics[height={height}]{{{pdf_rel}}}"
        if scale_m and scale_m.group(1) != "1":
            inner = f"\\scalebox{{{scale_m.group(1)}}}{{{inner}}}"
        latex = f"\\raisebox{{{valign}}}{{{inner}}}"
        return f"`{latex}`{{=latex}}"

    return SCAFFOLD_ICON_IMG_RE.sub(replace, md_text)


def parse_from_svg_source(path: Path) -> tuple[Path, str] | None:
    """Return (canonical_path, lineage_chain) for a figures/*.from*.svg source.

    The repository has both hyphen and underscore variants in circulation:
    `name.from-cd.svg`, `name.from-py-cd.svg`, and a few `name.from_cd.svg`
    files. Treat both separators as source-stage markers while writing the
    same lineage comment the existing manual promoter uses.
    """
    match = FROM_SVG_RE.match(path.name)
    if not match:
        return None
    base = match.group("base")
    chain = re.sub(r"[-_]+", " → ", match.group("chain"))
    return path.parent / f"{base}.svg", chain


def cmd_promote_svgs(force: bool = False) -> int:
    """Promote newer figures/**/*.from*.svg files to canonical sibling SVGs."""
    if not FIGURES_DIR.exists():
        print(f"Missing: {FIGURES_DIR.relative_to(BOOK_DIR)}", file=sys.stderr)
        return 1

    grouped: dict[Path, list[tuple[Path, str]]] = {}
    for source in sorted(FIGURES_DIR.rglob("*.from*.svg")):
        parsed = parse_from_svg_source(source)
        if parsed is None:
            continue
        canonical, chain = parsed
        grouped.setdefault(canonical, []).append((source, chain))

    promoted = skipped = 0
    needs_outlining: list[Path] = []
    for canonical, candidates in sorted(grouped.items()):
        source, chain = max(candidates, key=lambda item: item[0].stat().st_mtime)
        if (
            not force
            and canonical.exists()
            and canonical.stat().st_mtime >= source.stat().st_mtime
        ):
            skipped += 1
            continue

        content = source.read_text(encoding="utf-8")
        date = datetime.date.today().isoformat()
        promoted_content = inject_lineage_comment(content, chain, source.name, date)
        canonical.write_text(promoted_content, encoding="utf-8")
        promoted += 1
        # This phase does NOT outline Devanagari; figures/_shared/lineage.py's
        # promote() does. Two promotion routes with different results is what
        # let vedic_yajati.svg ship with live Devanagari text while its four
        # siblings were outlined — the live one then rendered in whatever
        # Devanagari face the viewer had (Sangam MN on macOS, ~1.24x the ink
        # height of Adobe Devanagari at the same nominal size), so it looked
        # a size larger than figures set at identical pt. Warn rather than
        # outline here: this phase runs under the system interpreter, which
        # has no uharfbuzz/fontTools, so it cannot do the job itself.
        if DEVANAGARI_RE.search(promoted_content) and "<text" in promoted_content:
            needs_outlining.append(canonical.relative_to(BOOK_DIR))
        print(
            f"  promote {source.relative_to(BOOK_DIR)}"
            f" -> {canonical.relative_to(BOOK_DIR)}"
        )

    print(f"SVG promotion: {promoted} updated, {skipped} already current.")
    if needs_outlining:
        print(
            f"\n  WARNING: {len(needs_outlining)} promoted figure(s) still "
            "contain live Devanagari <text>. This phase cannot outline it.\n"
            "  Run, from figures/:\n"
            "      ../.venv-figures/bin/python3 -m _shared.lineage promote "
            "<path-to>.from-py.svg"
        )
        for path in needs_outlining:
            print(f"    - {path}")
    return 0


def gray_png_path(path: Path) -> Path:
    return path.with_suffix(".gray.png")


def prefer_png_images_for_pdf(md_text: str) -> str:
    """Use grayscale/raster siblings for PDF builds when available.

    Manuscript sources stay canonical with SVG links. The assembled Markdown
    handed to Pandoc uses `figure.gray.png` when it exists, then `figure.png`
    when it exists beside `figure.svg`, preserving the caption and any trailing
    Pandoc image attributes. File modification times are deliberately ignored:
    Git operations can make a paired SVG appear newer than its PNG even when
    both belong to the same committed figure revision.
    """
    def replace(match: re.Match) -> str:
        prefix, image_path, suffix = match.groups()
        source_path = BOOK_DIR / image_path
        if source_path.name.endswith(".gray.png"):
            return match.group(0)
        gray_path = gray_png_path(source_path)
        if gray_path.exists():
            return f"{prefix}{gray_path.relative_to(BOOK_DIR).as_posix()}{suffix}"
        if source_path.suffix.lower() == ".svg":
            png_path = source_path.with_suffix(".png")
            gray_png = gray_png_path(png_path)
            if gray_png.exists():
                return f"{prefix}{gray_png.relative_to(BOOK_DIR).as_posix()}{suffix}"
            if png_path.exists():
                return f"{prefix}{png_path.relative_to(BOOK_DIR).as_posix()}{suffix}"
        return match.group(0)

    return PDF_IMAGE_RE.sub(replace, md_text)


def grayscale_command(source: Path, target: Path) -> list[str] | None:
    if magick := shutil.which("magick"):
        return [
            magick,
            str(source),
            "-colorspace", "Gray",
            "-resize", f"{PDF_IMAGE_MAX_WIDTH_PX}x>",
            "-strip",
            str(target),
        ]
    if convert := shutil.which("convert"):
        return [
            convert,
            str(source),
            "-colorspace", "Gray",
            "-resize", f"{PDF_IMAGE_MAX_WIDTH_PX}x>",
            "-strip",
            str(target),
        ]
    if sips := shutil.which("sips"):
        gray_profile = Path("/System/Library/ColorSync/Profiles/Generic Gray Profile.icc")
        if gray_profile.exists():
            return [
                sips,
                "--resampleWidth", str(PDF_IMAGE_MAX_WIDTH_PX),
                "-s", "format", "png",
                "-m", str(gray_profile),
                str(source),
                "--out", str(target),
            ]
    return None


def cmd_grayscale_images(force: bool = False) -> int:
    """Create/update grayscale sibling PNGs under figures/."""
    figures_dir = BOOK_DIR / "figures"
    if not figures_dir.exists():
        print(f"Missing: {figures_dir.relative_to(BOOK_DIR)}", file=sys.stderr)
        return 1

    sources = sorted(
        path for path in figures_dir.rglob("*.png")
        if not path.name.endswith(".gray.png")
    )
    if not sources:
        print("No figure PNGs found.")
        return 0

    converted = skipped = 0
    for source in sources:
        target = gray_png_path(source)
        if (
            not force
            and target.exists()
            and target.stat().st_mtime >= source.stat().st_mtime
        ):
            skipped += 1
            continue

        cmd = grayscale_command(source, target)
        if cmd is None:
            print(
                "No grayscale converter found. Install ImageMagick (`magick`) "
                "or run on macOS with `sips` and the Generic Gray profile.",
                file=sys.stderr,
            )
            return 1

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Grayscale conversion failed: {source.relative_to(BOOK_DIR)}", file=sys.stderr)
            print(result.stderr or result.stdout, file=sys.stderr)
            return result.returncode
        converted += 1
        print(f"  gray {target.relative_to(BOOK_DIR)}")

    print(f"Grayscale images: {converted} updated, {skipped} already current.")
    return 0


# Inline note-marker handling. Each `[NOTE: stub-name]` in chapter prose is
# replaced with a provisional numbered reference `[N]`. Repeated uses of the
# same stub reuse the number assigned at its first appearance, so one source
# produces one endnote even when several passages cite it.
# Numerical conversion is the chapter-lock convention from CLAUDE.md; doing
# it at build time produces a clean draft PDF without verbose inline markers
# until the expanded prose is drafted.
NOTE_MARKER_RE = re.compile(r"\[NOTE:\s*([a-z0-9_-]+)\s*\]")


# Written by the book build, read by the companion build. The companion never
# assembles the book's body, so it cannot derive these numbers itself: they
# come from the order [NOTE: ...] markers first appear in the running text.
NOTE_NUMBER_MAP = BUILD_DIR / "note_numbers.json"


def write_note_number_map(notes: list[tuple[int, str]]) -> None:
    """Record stub -> printed note number so the companion can cite the same
    numbers the book prints."""
    NOTE_NUMBER_MAP.parent.mkdir(parents=True, exist_ok=True)
    NOTE_NUMBER_MAP.write_text(json.dumps({
        "generated": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "count": len(notes),
        "notes": {stub: number for number, stub in notes},
    }, indent=2) + "\n")


def number_note_markers(md_text: str, start: int = 1) -> tuple[str, list[tuple[int, str]]]:
    """Replace inline [NOTE: stub-name] markers with numbered references.
    Repeated stub names reuse their first number. Returns processed text and
    one ``(number, stub-name)`` tuple per unique stub, in first-use order.
    """
    notes: list[tuple[int, str]] = []
    counter = [start - 1]
    assigned: dict[str, int] = {}

    def replace(match: re.Match) -> str:
        stub = match.group(1)
        number = assigned.get(stub)
        if number is None:
            counter[0] += 1
            number = counter[0]
            assigned[stub] = number
            notes.append((number, stub))
        return f"`\\textsuperscript{{[{number}]}}`{{=latex}}"

    return NOTE_MARKER_RE.sub(replace, md_text), notes


# Parsers for the two content sources keyed by stub-name:
#  - as_endnotes.md          drafted prose (each entry under ### `stub-name`)
#  - as_todo.md Section E    stub descriptions (each `[NOTE: stub-name]` bullet)
# Both feed the unified Endnotes section.

TODO_SECTION_E_RE = re.compile(
    r"^## E\. SCHOLARLY VERIFICATIONS.*?(?=^## F\.|\Z)",
    re.MULTILINE | re.DOTALL,
)
ENDNOTES_ENTRY_RE = re.compile(
    r"^### `([a-z0-9_-]+)`\s*\n(.*?)(?=^### `|^---|\Z)",
    re.MULTILINE | re.DOTALL,
)
# The **Short:** field in each as_endnotes.md entry — the one-sentence
# editorial compression used by --endnotes=short. Always sits on the line
# directly after the heading.
SHORT_FIELD_RE = re.compile(r"^\*\*Short:\*\*\s*(.+?)$", re.MULTILINE)
# Private verification metadata may sit beside an endnote in the source file,
# but it must never enter either the printed book or the reference companion.
SOURCE_RECORDS_BLOCK_RE = re.compile(
    r"<!--\s*SOURCE-RECORDS\b.*?-->",
    re.DOTALL,
)
TODO_STUB_LINE_RE = re.compile(
    r"^\s*-\s*\[[ x~!]\]\s*\*\*(?:\[P[0-3]\]\s*)?`\[NOTE:\s*([a-z0-9_-]+)\s*\]`\.?\*\*\s*(.*?)$",
    re.MULTILINE,
)


def load_drafted_endnotes(mode: str = "full") -> dict[str, str]:
    """Parse as_endnotes.md and return { stub-name: drafted prose }.

    mode='full'  — return the entire entry body (default; reference-grade).
    mode='short' — return only the content of the **Short:** field per entry.
                   Falls back to the full body when the Short field is
                   missing or carries a [TBD: ...] placeholder, so the
                   build still produces something useful per-entry even
                   while editorial passes are in flight.
    """
    path = BOOK_DIR / "manuscript" / "as_endnotes.md"
    if not path.exists():
        return {}
    text = path.read_text()
    result: dict[str, str] = {}
    for m in ENDNOTES_ENTRY_RE.finditer(text):
        stub = m.group(1)
        body = SOURCE_RECORDS_BLOCK_RE.sub("", m.group(2)).strip()
        if mode == "short":
            short_m = SHORT_FIELD_RE.search(body)
            if short_m:
                short_content = short_m.group(1).strip()
                if not short_content.startswith("[TBD:"):
                    result[stub] = short_content
                    continue
            # Fallback: Short field missing or TBD — emit the full body
            # so the build still produces useful content for the entry.
        result[stub] = body
    return result


def load_stub_descriptions() -> dict[str, str]:
    """Parse working/10_active/as_todo.md Section E and return { stub-name: description }."""
    path = BOOK_DIR / "working" / "10_active" / "as_todo.md"
    if not path.exists():
        return {}
    section = TODO_SECTION_E_RE.search(path.read_text())
    if not section:
        return {}
    return {
        m.group(1): m.group(2).strip()
        for m in TODO_STUB_LINE_RE.finditer(section.group(0))
    }


def render_unified_endnotes(notes: list[tuple[int, str]], mode: str = "full") -> str:
    """Render a single unified Endnotes section. Each numbered entry carries
    drafted prose if available, otherwise the stub description from as_todo,
    otherwise a verification-pending placeholder. Replaces the earlier
    three-section split (Endnote References / Pending Stubs / Endnotes).

    mode='full'  — emit the complete long-form body per entry (default).
    mode='short' — emit only the one-sentence **Short:** field per entry."""
    if not notes:
        return ""
    drafted = load_drafted_endnotes(mode=mode)
    stubs = load_stub_descriptions()
    drafted_count = sum(1 for _, s in notes if s in drafted)
    described_count = sum(1 for _, s in notes if s not in drafted and s in stubs)
    pending_count = len(notes) - drafted_count - described_count

    if mode == "short":
        intro = (
            f"*Numbered list of every inline note reference in the manuscript "
            f"({len(notes)} total). Each entry carries the **short form** — the "
            f"one-sentence editorial compression of the source citation. The "
            f"full long-form citation, verification trail, and source-history "
            f"discussion lives in the *Source and Reference Companion*. "
            f"*The numbered references in the body of the book — the **[N]** "
            f"superscripts — point here.*"
        )
    else:
        intro = (
            f"*Numbered list of every inline note reference in the manuscript "
            f"({len(notes)} total: {drafted_count} drafted, {described_count} stub-described, "
            f"{pending_count} verification-pending). Each entry carries the fullest content "
            f"currently available — drafted prose where the verification has completed, "
            f"the verification-stub description where the citation is identified but "
            f"the note prose is not yet drafted, or a verification-pending placeholder "
            f"otherwise. The numbered references in the body of the book — the **[N]** "
            f"superscripts — point here.*"
        )

    lines = [
        "# Endnotes",
        "",
        intro,
        "",
    ]
    for n, stub in notes:
        if stub in drafted:
            content = drafted[stub]
        elif stub in stubs:
            content = f"*[Verification stub — citation identified, prose not yet drafted.]* {stubs[stub]}"
        else:
            content = "*[Verification pending — citation not yet identified.]*"
        lines.append(f"**[{n}] `{stub}`.**  {content}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def make_stub(title: str, summary: str) -> str:
    """Build a visibly-flagged stub file for an undrafted chapter."""
    return (
        f"# {title}\n"
        "\n"
        "> **[STUB — NOT YET DRAFTED]** Placeholder content extracted from "
        "`reference/as_toc_annotated.md`. Replace with full draft prose before final build.\n"
        "\n"
        "## Chapter summary\n"
        "\n"
        f"*{summary}*\n"
        "\n"
        "---\n"
        "\n"
        "*[Full prose to be drafted.]*\n"
    )


def cmd_stubs(force: bool = False) -> int:
    created, skipped = 0, 0
    for fname, info in STUB_FILES.items():
        # Manuscript prose has lived in manuscript/ since the 2026-08-17
        # reorg, and this resolution was never updated. Against BOOK_DIR the
        # existence check missed the real chapter every time, so `stubs` wrote
        # a "NOT YET DRAFTED" placeholder at the repo root for three chapters
        # that were long since finished — 400, 187, and 217 lines. Nothing
        # downstream read them, because as_book.yaml's assembly entries are
        # directory-qualified, but the build left three misleading files in
        # the working tree on every run.
        path = BOOK_DIR / "manuscript" / fname
        if path.exists() and not force:
            print(f"  skip   {fname}")
            skipped += 1
            continue
        path.write_text(make_stub(info["title"], info["summary"]))
        print(f"  create {fname}")
        created += 1
    print(f"\nStubs: {created} created, {skipped} skipped.")
    return 0


def read_yaml_value_opt(path: Path, key: str, default: str = "") -> str:
    """read_yaml_value, but returns `default` instead of raising when the key
    is absent — for optional metadata a book file may simply not carry."""
    try:
        return read_yaml_value(path, key)
    except KeyError:
        return default


_DEFER_MAINMATTER_TEX = (
    "\\let\\bookmainmatter\\mainmatter\n\\renewcommand{\\mainmatter}{}"
)


def _backmatter_size_tex(appendix_fontsize: str | None,
                         endnotes_fontsize: str | None,
                         endnotes_linestretch: str | None) -> str:
    """Define the markers cmd_assemble() emits at the back-matter boundaries.

    The assembled markdown is shared by every page size, so it cannot carry a
    point value — b5 wants 9.5pt appendices and `phone` at 3.5in wide does
    not. It emits a named marker instead, and the preamble, which IS rendered
    per build, decides what the marker does.

    \\changefontsizes comes from scrextend and recalculates the whole size
    ladder — headings, captions, notes, lists — where a bare \\small would
    only shrink body text. It is referenced, not required: the macro body is
    expanded in the document, long after fontsize_cli_args() has had its
    chance to load scrextend, and falls back to a plain size switch for a
    layout on a standard class size that never loads it."""
    def switch(size: str) -> str:
        points = float(_FONTSIZE_RE.fullmatch(size.strip()).group("points"))
        return f"\\atomicsetsize{{{size.strip()}}}{{{round(points * 1.2, 2)}pt}}"

    lines = [
        r"\makeatletter",
        r"\newcommand{\atomicsetsize}[2]{%",
        r"  \@ifundefined{changefontsizes}{\fontsize{#1}{#2}\selectfont}%",
        r"                                {\changefontsizes[#2]{#1}}%",
        r"}",
        r"\makeatother",
    ]
    appendix = switch(appendix_fontsize) if appendix_fontsize else r"\relax"
    endnotes = switch(endnotes_fontsize) if endnotes_fontsize else r"\relax"
    if endnotes_linestretch:
        endnotes += f"\\setstretch{{{endnotes_linestretch}}}"
    lines += [
        f"\\newcommand{{\\atomicappendixmatter}}{{{appendix}}}",
        f"\\newcommand{{\\atomicendnotematter}}{{{endnotes}}}",
    ]
    return "\n".join(lines)


def render_devanagari_preamble(
    metadata_file: Path,
    chapter_folio: bool = True,
    defer_mainmatter: bool = True,
    appendix_fontsize: str | None = None,
    endnotes_fontsize: str | None = None,
    endnotes_linestretch: str | None = None,
) -> Path:
    """Substitute the Devanagari font name and its fontspec options into the
    preamble template, writing the rendered build artifact.

    The options list is data (as_book.yaml's `devanagarifontoptions`) because
    it is font-specific: Tiro Devanagari Sanskrit ships no bold weight and
    needs AutoFakeBold for the book's Devanagari headings, whereas a face with
    a real bold must not have one synthesized over it."""
    font = read_yaml_value(metadata_file, "devanagarifont")
    opts = read_yaml_value_opt(metadata_file, "devanagarifontoptions")
    text = PREAMBLE_TEMPLATE.read_text()
    text = text.replace("__DEVANAGARIFONTOPTS__", f",{opts}" if opts else "")
    text = text.replace("__DEVANAGARIFONT__", font)
    text = text.replace(
        "__CHAPTER_OPENING_FOLIO__", "" if chapter_folio else _SUPPRESS_PLAIN_FOLIO
    )
    text = text.replace(
        "__MAINMATTER_DEFERRAL__", _DEFER_MAINMATTER_TEX if defer_mainmatter else ""
    )
    text = text.replace(
        "__BACKMATTER_SIZES__",
        _backmatter_size_tex(appendix_fontsize, endnotes_fontsize,
                             endnotes_linestretch),
    )
    out = BUILD_DIR / "devanagari-preamble.tex"
    out.write_text(text)
    return out


def read_yaml_value(path: Path, key: str) -> str:
    """Extract a single top-level scalar value from a YAML file.
    Minimal no-dependency reader — handles `key: value` lines, optional
    surrounding quotes, and trailing comments. Not a general YAML parser."""
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith(f"{key}:"):
            value = stripped.split(":", 1)[1]
            # Strip trailing comment
            if "#" in value:
                value = value.split("#", 1)[0]
            value = value.strip()
            # Strip optional surrounding quotes
            if len(value) >= 2 and value[0] in ('"', "'") and value[-1] == value[0]:
                value = value[1:-1]
            return value
    raise KeyError(f"{key!r} not found in {path}")


def mainfont_cli_args(metadata_file: Path) -> list[str]:
    """Return Pandoc CLI variables for the configured Latin font.

    Complex fontspec options must travel through ``-V``. Pandoc escapes the
    braces when the same value comes from a YAML metadata string, which turns
    STIX's variable-weight declaration into invalid fontspec syntax.
    """
    font = read_yaml_value(metadata_file, "mainfont")
    options = read_yaml_value_opt(metadata_file, "mainfontoptionsraw")
    fontdir = read_yaml_value_opt(metadata_file, "mainfontdir")
    # `mainfontdir` switches fontspec from looking the family up by name to
    # loading exact files, and it is the only arrangement that produces bold
    # on both machines.
    #
    # Asking the system for "STIX Two Text" gets macOS's system-installed
    # VARIABLE build, which XeTeX will not render bold from under any option
    # tried: the +axis={wght=700} raw feature this file used to pass, a plain
    # \setmainfont, BoldFont={STIX Two Text Bold}, or the two combined. Every
    # one silently produced regular weight, so every **bold** in Latin text
    # had been flat since the switch to STIX — visible in a 430dpi crop of
    # "Sanātan evaluates the action, not the faction." against the line above
    # it. (Bold Devanagari always worked, via Tiro's AutoFakeBold, which is
    # what made the page look correct.) On Linux the same variable file is
    # worse: fontconfig hands xdvipdfmx a face index it rejects outright with
    # "Invalid font: -1", so the build dies rather than losing bold quietly.
    #
    # Installing static faces does not help while lookup is by name, because
    # the system copy still wins. Naming the files directly skips lookup, and
    # the fonts ship in the repo so both machines load identical bytes.
    if fontdir:
        abs_dir = (BOOK_DIR / fontdir).resolve()
        if not abs_dir.is_dir():
            raise SystemExit(
                f"build_book.py: mainfontdir {fontdir!r} does not exist at {abs_dir}."
            )
        options = f"Path={abs_dir}/" + (f",{options}" if options else "")
    args = ["-V", f"mainfont={font}"]
    if options:
        args += ["-V", f"mainfontoptions={options}"]
    return args


def _parse_yaml_scalar(s: str) -> str | None:
    """Parse one yaml scalar — strip surrounding quotes, treat null/~/empty
    as None, strip trailing comments (when not inside quotes)."""
    s = s.strip()
    if not s:
        return None
    # If the value isn't quoted, strip trailing comments
    if not (s.startswith('"') or s.startswith("'")):
        if "#" in s:
            s = s.split("#", 1)[0].rstrip()
    if s in ("", "null", "~"):
        return None
    # Strip surrounding quotes
    if len(s) >= 2 and s[0] in ('"', "'") and s[-1] == s[0]:
        s = s[1:-1]
    return s


def parse_assembly_yaml(path: Path) -> list[dict]:
    """Parse the `assembly:` block from as_book.yaml.
    Minimal no-dependency block-style parser specialized for the assembly
    structure: a list of dicts where each dict has scalar keys (kind, file,
    title, subtitle). Not a general YAML parser. Reading order is preserved
    by list order in the YAML file."""
    entries: list[dict] = []
    current: dict | None = None
    in_assembly = False

    for line in path.read_text().splitlines():
        # Skip pure-comment and blank lines
        if not line.strip() or line.strip().startswith("#"):
            continue

        # Detect a new top-level key (no leading whitespace). If we're already
        # inside `assembly:` and hit a different top-level key, the assembly
        # block has ended.
        if not line.startswith(" ") and not line.startswith("\t"):
            if line.strip() == "assembly:":
                in_assembly = True
                continue
            else:
                if in_assembly:
                    # Assembly block ended before EOF
                    in_assembly = False
                    if current is not None:
                        entries.append(current)
                        current = None
                continue

        if not in_assembly:
            continue

        # We're inside `assembly:`; line is indented.
        stripped = line.strip()

        if stripped.startswith("- "):
            # New entry — flush current if any, then start fresh.
            if current is not None:
                entries.append(current)
            current = {}
            rest = stripped[2:]
            if ":" in rest:
                k, _, v = rest.partition(":")
                current[k.strip()] = _parse_yaml_scalar(v)
        elif ":" in stripped and current is not None:
            # Continuation key-value for the current entry.
            k, _, v = stripped.partition(":")
            current[k.strip()] = _parse_yaml_scalar(v)

    # Flush the final entry.
    if current is not None:
        entries.append(current)

    # Normalize: ensure every entry has all four keys (defaulting to None).
    for entry in entries:
        for key in ("kind", "file", "title", "subtitle"):
            entry.setdefault(key, None)

    return entries


# ASSEMBLY is loaded once at module-import time from as_book.yaml. Edit reading
# order in the YAML — not here.
#
# An entry may carry `draft: true` to hold it out of every build (PDF and
# HTML alike — build_html.py imports this same ASSEMBLY) without deleting
# it from as_book.yaml or the manuscript file itself. Filtered here, once,
# at the shared load point, rather than at each of ASSEMBLY's several
# consumers across both scripts — a spot missed in even one of them would
# leak the draft entry into a build the others correctly excluded it from.
# _parse_yaml_scalar returns plain strings (no bool coercion), so the check
# is a string comparison, not `is True`.
_RAW_ASSEMBLY = parse_assembly_yaml(METADATA_FILE)
_DRAFT_ENTRIES = [e for e in _RAW_ASSEMBLY if e.get("draft") == "true"]
for _e in _DRAFT_ENTRIES:
    print(f"  DRAFT — excluded from build: {_e['file']} ({_e['title']})")
ASSEMBLY = [e for e in _RAW_ASSEMBLY if e.get("draft") != "true"]


def clean_chapter(text: str, canonical_title: str) -> str:
    """Strip draft scaffolding and replace the top-level heading with the canonical title."""
    text = DRAFT_NOTES_RE.sub("", text)
    text = text.strip()

    # A few chapter sources place the epigraph before their own H1. Remove the
    # source H1 wherever it occurs, then place the canonical title once at the
    # beginning so Pandoc emits exactly one LaTeX chapter command.
    text = CHAPTER_HEADER_RE.sub("", text, count=1).strip()
    text = DRAFT_HEADER_RE.sub("", text.lstrip()).strip()
    text = f"# {canonical_title}\n\n{text}"

    return text.strip() + "\n"


def cmd_assemble(endnotes_mode: str = "full", promote_svgs: bool = True) -> int:
    if promote_svgs:
        rc = cmd_promote_svgs(force=False)
        if rc != 0:
            return rc

    BUILD_DIR.mkdir(exist_ok=True)
    # Suffix the assembled .md with the endnotes mode so full and short
    # variants can coexist as separate intermediate artifacts.
    notes_suffix = "" if endnotes_mode == "full" else f".{endnotes_mode}"
    out_path = BUILD_DIR / f"atomic_sanskrit{notes_suffix}.md"

    chunks: list[str] = []
    # Metadata is no longer injected inline — pandoc reads it from
    # as_book.yaml at PDF render time via --metadata-file. Keeping
    # the assembled markdown pure content avoids duplication / drift.

    missing: list[str] = []
    # The per-file "include ..." lines were 40-odd rows of scrollback that
    # pushed the warnings the build actually wants read off the screen.
    # Count them instead and report one summary line.
    counts = {"chapter": 0, "part opener": 0, "dedication": 0}
    endnote_summary = ""
    appendix_started = False
    for entry in ASSEMBLY:
        if entry.get("html_only") == "true":
            continue
        kind = entry["kind"]
        filename = entry["file"]
        title = entry["title"]
        subtitle = entry.get("subtitle")
        if kind == "dedication":
            path = BOOK_DIR / filename
            if not path.exists():
                print(f"  MISSING: {filename}", file=sys.stderr)
                missing.append(filename)
                continue
            text = path.read_text().strip()
            if text:
                chunks.append(text + "\n\n")
                counts["dedication"] += 1
            continue
        if kind == "part":
            # Raw-LaTeX part break (pandoc passes through inside this fence).
            # When a subtitle is present, embed it INSIDE the \partopener[...]{...}
            # so it appears (a) in the TOC entry — via the optional argument
            # — and (b) on the part-title page — via the mandatory argument's
            # \\[...] line break. \normalfont and \itshape reset bold to
            # medium-italic so the subtitle reads as a subordinate line
            # beneath the bold title.
            #
            # \partopener (defined in templates/devanagari-preamble.tex.in) is
            # a modified \part that suppresses the trailing \cleardoublepage,
            # so the opener prose (read from `file:` below) flows on the same
            # page as the title rather than being pushed to the next page.
            if subtitle:
                # The optional arg becomes the TOC entry; the mandatory arg
                # is what the part page displays. \partopener wraps the
                # mandatory arg in \huge\bfseries.
                toc_text = f"{title} — \\textit{{{subtitle}}}"
                page_text = (
                    f"{title}\\\\[2ex]"
                    f"{{\\Large\\normalfont\\itshape {subtitle}}}"
                )
                chunks.append(
                    f"\n```{{=latex}}\n"
                    f"\\partopener[{toc_text}]{{{page_text}}}\n"
                    f"```\n\n"
                )
            else:
                chunks.append(f"\n```{{=latex}}\n\\partopener{{{title}}}\n```\n\n")
            if filename:
                path = BOOK_DIR / filename
                if not path.exists():
                    print(f"  MISSING: {filename}", file=sys.stderr)
                    missing.append(filename)
                    continue
                text = path.read_text()
                text = DRAFT_NOTES_RE.sub("", text).strip()
                text = DRAFT_HEADER_RE.sub("", text.lstrip()).strip()
                text = PART_HEADER_RE.sub("", text.lstrip(), count=1).strip()
                if text:
                    chunks.append(text + "\n\n")
                    counts["part opener"] += 1
            continue

        # When we reach as_endnotes.md, replace the three-section endnote
        # cluster (Endnote References / Pending Endnote Stubs / Endnotes)
        # with one unified Endnotes section: number every inline note marker
        # in the chapter chunks so far, then render a single numbered Endnotes
        # section that pulls content from as_endnotes.md (drafted prose) and
        # as_todo.md Section E (stub descriptions), with a verification-pending
        # placeholder where neither is available.
        # Basename: assembly paths are directory-qualified since the
        # 2026-08-17 restructure (manuscript/as_endnotes.md).
        if Path(filename).name == "as_endnotes.md":
            body_so_far = "".join(chunks)
            numbered_body, notes = number_note_markers(body_so_far)
            write_note_number_map(notes)
            chunks[:] = [numbered_body]
            unified = render_unified_endnotes(notes, mode=endnotes_mode)
            if unified:
                # Keep a complete Markdown block boundary after the generated
                # notes. Back matter may follow the Endnotes entry, and a
                # single newline would fold its H1 into the final note.
                # Everything from here to the end of the volume is back
                # matter, so the size set here is not restored: "About the
                # Author" follows the Endnotes and belongs at the same size.
                chunks.append("\n\n```{=latex}\n\\atomicendnotematter\n```\n\n")
                chunks.append("\n\n" + unified.rstrip() + "\n\n")
                mode_label = "short" if endnotes_mode == "short" else "full"
                endnote_summary = (f"  endnotes: {len(notes)} entries "
                                   f"(mode={mode_label})")
            # Skip the as_endnotes.md raw include — its content is now folded
            # into the unified Endnotes by load_drafted_endnotes().
            continue

        path = BOOK_DIR / filename
        if not path.exists():
            print(f"  MISSING: {filename}", file=sys.stderr)
            missing.append(filename)
            continue

        # The appendix parts are `kind: end` like the other back matter, so
        # the filename zone prefix is what identifies them (see CLAUDE.md's
        # filename convention: zone 3 is the appendix).
        if not appendix_started and Path(filename).name.startswith("as_3_"):
            appendix_started = True
            chunks.append("\n```{=latex}\n\\atomicappendixmatter\n```\n\n")

        cleaned = clean_chapter(path.read_text(), title)
        chunks.append(cleaned + "\n")
        counts["chapter"] += 1

    detail = ", ".join(f"{n} {label}{'s' if n != 1 and not label.endswith('s') else ''}"
                       for label, n in counts.items() if n)
    print(f"  included {sum(counts.values())} files ({detail})")
    if endnote_summary:
        print(endnote_summary)

    assembled = "".join(chunks)
    assembled = prefer_png_images_for_pdf(assembled)
    # Raw-HTML <img> scaffold icons are otherwise dropped outright by
    # pandoc's LaTeX writer — convert them to a raw-LaTeX \includegraphics
    # call before the script-wrapping pass below.
    assembled = render_scaffold_icons_for_pdf(assembled)
    # Count the assembled content before font wrappers add LaTeX commands
    # containing spaces. Those commands are typesetting instructions, not
    # words in the manuscript.
    word_count = len(assembled.split())
    # Wrap non-Latin scripts in raw-LaTeX font-switch commands. See
    # wrap_scripts_for_latex / SCRIPT_WRAPS for the per-script ranges.
    assembled = wrap_scripts_for_latex(assembled)
    out_path.write_text(assembled)
    print(f"\nAssembled → {out_path.relative_to(BOOK_DIR)} ({word_count:,} words)")
    warn_uncovered_characters(assembled, METADATA_FILE)
    if missing:
        print(f"WARNING: {len(missing)} file(s) missing.")
    return 0


_FLOAT_WARN_RE = re.compile(r"Float too large for page by ([\d.]+)pt on input line (\d+)")


def report_oversized_floats(stderr: str, cmd: list[str]) -> None:
    """Name the figures behind LaTeX's "Float too large for page" warnings.

    The warning identifies the offender only by a line number into the LaTeX
    pandoc generated internally and then deleted, so the build printed three
    anonymous overflow amounts and left you to find them by hand. Regenerating
    that LaTeX is cheap -- the 160s is xelatex's four passes, not the markdown
    conversion -- and the same input through the same filters and options
    produces the same line numbering, so the numbers map exactly.

    Predicting overflow instead of reading it back was the tempting shortcut
    and the wrong one: LaTeX's float arithmetic folds in caption reflow,
    \\textfloatsep and float-page fractions, and an estimate that disagrees
    with the real warning is worse than no estimate."""
    # Two things have to be flattened before the line number can be read off.
    # pandoc wraps its warnings ("... on\n  input line 79."), and the run is
    # captured through a pty, so lines end \r\n -- rejoining on \n alone
    # leaves the \r sitting inside "on\r input line" and the match fails.
    # Collapse every whitespace run instead.
    flat = re.sub(r"\s+", " ", stderr)
    hits = _FLOAT_WARN_RE.findall(flat)
    if not hits:
        return
    print(f"  {len(hits)} figure(s) overflow the page:")

    tex_cmd, tex_path = [], BOOK_DIR / "build" / "_float_report.tex"
    skip = False
    for arg in cmd:
        if skip:
            skip = False
            continue
        if arg == "-o":
            skip = True
            continue
        if arg.startswith("--pdf-engine"):
            continue
        tex_cmd.append(arg)
    tex_cmd += ["-s", "-o", str(tex_path)]
    try:
        subprocess.run(tex_cmd, capture_output=True, check=True)
        lines = tex_path.read_text().splitlines()
    except Exception as exc:
        for over, line in hits:
            print(f"     {over}pt over (LaTeX line {line})")
        print(f"     (could not name them — {type(exc).__name__}: {exc})")
        return

    for over, line in sorted(hits, key=lambda h: -float(h[0])):
        # LaTeX reports the line where it noticed the overflow, which may be
        # the \begin{figure} or the \end{figure}. Bound the block by the
        # environment in both directions rather than by a fixed window: a
        # caption wraps across several lines, and a window that clips the
        # closing bracket makes the caption unmatchable.
        n = int(line) - 1
        start = next((i for i in range(min(n, len(lines) - 1), max(0, n - 200), -1)
                      if lines[i].startswith(r"\begin{figure}")), None)
        stop = next((i for i in range(n, min(len(lines), n + 200))
                     if lines[i].startswith(r"\end{figure}")), None)
        block = ("\n".join(lines[start:(stop + 1) if stop is not None else n + 40])
                 if start is not None else "")
        cap = re.search(r"\\caption\[([^\]]*)\]", block) or \
              re.search(r"\\caption\{(.{0,90})", block, re.S)
        src = re.search(r"\\include(?:graphics|svg)(?:\[[^\]]*\])?\{([^}]*)\}", block)
        name = " ".join(cap.group(1).split()) if cap else f"LaTeX line {line}"
        print(f"     {float(over):6.1f}pt over  {name[:64]}")
        if src:
            print(f"                   {src.group(1)}")
    tex_path.unlink(missing_ok=True)


def prefer_local_texlive() -> str | None:
    """Put a /usr/local/texlive install ahead of the system TeX on PATH.

    amrut carries two: Ubuntu's apt TeX Live 2022 on /usr/bin, and an
    upstream 2026 under /usr/local/texlive installed without touching the
    system PATH. A build run there picks up 2022 unless something says
    otherwise, and the two are not interchangeable — 2022 is four years of
    fixes behind, and nothing in the output announces which one produced it.

    Only /usr/local/texlive is considered, so a system TeX that is already
    the newest (the Mac, where /Library/TeX/texbin is current) is left alone
    unless an upstream install is genuinely present. Highest version wins.
    Returns the directory prepended, or None."""
    roots = sorted(Path("/usr/local/texlive").glob("*/bin/*"),
                   key=lambda p: p.parent.parent.name, reverse=True)
    for bindir in roots:
        if (bindir / "xelatex").exists():
            current = os.environ.get("PATH", "")
            if str(bindir) in current.split(os.pathsep):
                return None
            os.environ["PATH"] = f"{bindir}{os.pathsep}{current}"
            return str(bindir)
    return None


def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


DEFAULT_PROGRESS_PAGES = 20
PAGE_BRACKET_RE = re.compile(r"\[(\d+)\]")
LATEX_RUN_RE = re.compile(r"\[INFO\] \[makePDF\] LaTeX run number (\d+)")
# A pandoc warning can continue onto following indented lines, and TeX
# wraps its log at ~79 columns, so "Float too large for page by 47.8pt on"
# and "input line 4156." arrive as two lines. Keeping only the [WARNING]
# line threw away every line number, which is the one part of the warning
# that identifies which figure overflowed.
WARNING_LINE_RE = re.compile(r"^.*\[WARNING\].*(?:\n[ \t]+\S.*)*$", re.MULTILINE)


class ProcResult:
    """Minimal stand-in for subprocess.CompletedProcess's .returncode/.stderr,
    so run_pandoc_with_progress() is a drop-in replacement for the plain
    subprocess.run(cmd, capture_output=True) calls it supersedes."""
    __slots__ = ("returncode", "stderr")

    def __init__(self, returncode: int, stderr: str):
        self.returncode = returncode
        self.stderr = stderr


SPINNER_FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
CLEAR_LINE = "\x1b[K"


def run_pandoc_with_progress(cmd: list[str], page_interval: int = DEFAULT_PROGRESS_PAGES,
                              label: str = "PDF") -> ProcResult:
    """Run a pandoc/xelatex command, showing a live progress readout instead
    of blocking silently for minutes.

    Three things defeat plain output-watching by default. (1) xelatex's
    per-page `[N]` markers are folded into pandoc's own diagnostic stream
    only when --verbose is passed, so this adds it if missing. (2) that
    stream gets fully block-buffered — nothing arrives until the whole run
    finishes — whenever pandoc's output isn't attached to a real terminal;
    attaching the child to a pty (rather than a plain pipe) restores
    incremental delivery (confirmed empirically: a plain pipe delivered
    zero bytes for 60+ seconds on a 750-page build; a pty delivered the
    same run's progress throughout). (3) even through a pty, pandoc relays
    the underlying xelatex subprocess's output in its own internal
    batches — a bare xelatex process streams in a steady trickle of small
    chunks over the same kind of pty, so this batching is pandoc's own
    relay, one layer below anything reachable from here — so page-count
    updates still arrive in bursts of dozens of pages at a time, with
    20-40s gaps between bursts, rather than one by one.

    Display: when stdout is a real terminal, progress renders as one
    self-overwriting line — spinner, highest page seen, LaTeX run number,
    elapsed seconds — refreshed every ~1s via a heartbeat tick even when no
    new page-count data has arrived, so the elapsed-seconds readout keeps
    moving through the silent gaps between bursts instead of appearing
    frozen. Each LaTeX run's final state is left behind as its own line
    before the next run's live line begins, so the run history stays
    readable without scrolling once per page bracket. A closing line
    reports total elapsed time and run count. When stdout is not a
    terminal (piped to a file/log), falls back to one printed line every
    `page_interval` pages, matching the original non-interactive behavior,
    with every read matched against the FULL output seen so far — not just
    the newest chunk — because pandoc's "LaTeX run number N" marker (used
    to detect a fresh compile pass and reset the page count) can itself
    land split across two reads and get silently missed otherwise.
    """
    if "--verbose" not in cmd:
        cmd = [*cmd, "--verbose"]
    master_fd, slave_fd = pty.openpty()
    start = time.time()
    proc = subprocess.Popen(cmd, stdout=slave_fd, stderr=slave_fd, close_fds=True)
    os.close(slave_fd)
    buf = bytearray()
    last_reported = 0
    highest_seen = 0
    current_run = 1
    run_start_pos = 0  # index into the decoded buffer where the current run's own output begins
    live = sys.stdout.isatty()
    spin_idx = 0
    line_open = False

    def refresh() -> None:
        nonlocal spin_idx, line_open
        elapsed = time.time() - start
        spin = SPINNER_FRAMES[spin_idx]
        spin_idx = (spin_idx + 1) % len(SPINNER_FRAMES)
        text = f"  {spin} {label}: ~page {highest_seen} typeset (run {current_run}, {elapsed:.0f}s elapsed)"
        print(f"\r{text}{CLEAR_LINE}", end="", flush=True)
        line_open = True

    while True:
        ready, _, _ = select.select([master_fd], [], [], 1.0)
        if master_fd in ready:
            try:
                chunk = os.read(master_fd, 65536)
            except OSError:
                break
            if not chunk:
                break
            buf += chunk
            # Full buffer, not just this chunk: a run marker can land split
            # across two reads and get silently missed otherwise.
            text = buf.decode("utf-8", errors="replace")
            run_matches = list(LATEX_RUN_RE.finditer(text))
            if run_matches:
                last_match = run_matches[-1]
                seen_run = int(last_match.group(1))
                if seen_run != current_run:
                    if live and line_open:
                        print()  # leave the finished run's line behind as history
                    current_run = seen_run
                    last_reported = 0
                    highest_seen = 0
                    line_open = False
                run_start_pos = last_match.end()
            # Only the current run's own slice — otherwise a finished run's
            # page numbers would leak into the next run's count, since the
            # full buffer never shrinks.
            pages = [int(p) for p in PAGE_BRACKET_RE.findall(text[run_start_pos:])]
            if pages:
                highest_seen = max(highest_seen, max(pages))
            if live:
                refresh()
            elif highest_seen > last_reported and highest_seen - last_reported >= page_interval:
                last_reported = highest_seen
                elapsed = time.time() - start
                print(f"  {label}: ~page {highest_seen} typeset (run {current_run}, {elapsed:.0f}s elapsed)")
        elif proc.poll() is not None:
            break
        elif live:
            refresh()  # heartbeat: keep the elapsed-seconds readout moving between bursts
    if live and line_open:
        print()
    os.close(master_fd)
    proc.wait()
    full_output = bytes(buf).decode("utf-8", errors="replace")
    if live:
        total_elapsed = time.time() - start
        status = "failed" if proc.returncode != 0 else "done"
        run_word = "run" if current_run == 1 else "runs"
        print(f"  {label}: {status} in {total_elapsed:.0f}s ({current_run} {run_word})")
    if proc.returncode != 0:
        return ProcResult(proc.returncode, full_output)
    return ProcResult(proc.returncode, "\n".join(WARNING_LINE_RE.findall(full_output)))


FIGURE_CAPTION_RE = re.compile(r"!\[(.*?)\]\(")


def verify_figures_present(pdf_path: Path, md_text: str) -> None:
    """Post-build safety net against a real, observed failure mode: pandoc's
    per-image SVG-to-PDF conversion can silently drop a figure from a large
    multi-hundred-page book without failing the build or printing a clear
    error. Confirmed 2026-08-13 — the varṇamālā garland figure (Ch9) was
    completely absent from one build (zero drawings, caption unsearchable
    anywhere in the PDF) and fully present in the very next build from the
    identical source and command; a stray 'LaTeX Warning: Float too large
    for page' was the only trace pandoc surfaced.

    Extracts every markdown image caption and confirms a recognizable
    fragment of it is searchable in the rendered PDF's text layer, printing
    a loud warning for any that aren't — rather than relying on someone
    noticing a missing figure by eye while paging through hundreds of
    pages.

    Requires PyMuPDF (`pip install pymupdf`); skips silently, with a note,
    when unavailable — the same graceful-degradation pattern
    figures/_shared/text_outline.py uses for uharfbuzz/fontTools."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("  (skipping figure-presence check — pip install pymupdf to enable)")
        return

    captions = FIGURE_CAPTION_RE.findall(md_text)
    if not captions:
        return

    doc = fitz.open(str(pdf_path))
    full_text = "\n".join(page.get_text() for page in doc)
    doc.close()

    def alnum_squash(s: str) -> str:
        # Collapses out everything but letters/digits (lowercased). LaTeX's
        # microtype/smart-quotes machinery rewrites straight quotes to
        # curly ones, hyphenation can insert line-break hyphens, and
        # ligatures/dash-length can shift — none of that is a sign the
        # figure is broken, so comparing squashed alphanumerics sidesteps
        # the whole class of punctuation/typography false alarms at once
        # instead of chasing each substitution individually.
        return re.sub(r"[^a-z0-9]+", "", s.lower())

    text_squashed = alnum_squash(full_text)

    missing = []
    skipped = 0
    for caption in captions:
        # md_text is the fully-assembled, post-wrap_scripts_for_latex source
        # — any Devanagari in the caption is already wrapped as raw-LaTeX
        # inline spans (`...`{=latex}), which xelatex replaces with actual
        # glyphs at render time. Those glyphs are then usually OUTLINED to
        # paths (figures/_shared/text_outline.py), not left as searchable
        # text. Comparing the literal `\devanagarifont ...` source against
        # extracted PDF text would never match even for a perfectly fine
        # figure, so strip those spans first — the leftover plain-Latin
        # text is what's actually reliable to check.
        plain = re.sub(r"`[^`]*`\{=latex\}", " ", caption)
        plain = re.sub(r"[ऀ-ॿ]+", " ", plain)  # stray unwrapped Devanagari
        plain = re.sub(r"\*\*|\*|`", "", plain)
        plain = re.sub(r"\s+", " ", plain).strip()

        # Captions read "Figure N.M — actual description..."; the em-dash
        # segment is the distinctive part. Require a reasonably long,
        # mostly-alphabetic signature — a short or symbol-heavy leftover
        # after stripping isn't a reliable enough test either way, so skip
        # rather than risk a false alarm.
        m = re.search(r"—\s*(.{20,60})", plain)
        signature = m.group(1).strip() if m else plain[:40].strip()
        letters = re.sub(r"[^A-Za-z]", "", signature)
        if len(letters) < 15:
            skipped += 1
            continue

        if alnum_squash(signature) not in text_squashed:
            missing.append(caption[:80])

    checked = len(captions) - skipped
    if missing:
        print(f"\n  WARNING: {len(missing)} of {checked} checked figure caption(s) not found "
              f"anywhere in {pdf_path.name} — this matches a known intermittent pandoc "
              f"SVG-conversion failure, not necessarily a problem with the source figure. "
              f"Rebuild and recheck before assuming the figure itself is broken:")
        for m in missing:
            print(f"    - {m}")
    else:
        print(f"  Verified {checked} figure caption(s) present in {pdf_path.name}"
              f"{f' ({skipped} skipped — signature too short/symbol-heavy to check reliably)' if skipped else ''}")


def cmd_pdf(layout: str = "letter", endnotes_mode: str = "full",
            progress_pages: int = DEFAULT_PROGRESS_PAGES,
            chapter_folio: bool | None = None) -> int:
    # The intermediate .md and the output PDF are both suffixed with the
    # endnotes mode (when short) so full and short variants coexist.
    notes_suffix = "" if endnotes_mode == "full" else f".{endnotes_mode}"
    md_path = BUILD_DIR / f"atomic_sanskrit{notes_suffix}.md"
    layout_suffix = "" if layout == "letter" else f".{layout}"
    pdf_path = BUILD_DIR / f"atomic_sanskrit{layout_suffix}{notes_suffix}.pdf"

    print("Refreshing canonical SVGs before PDF render.")
    rc = cmd_promote_svgs(force=False)
    if rc != 0:
        return rc

    print("Refreshing grayscale figure PNGs before PDF render.")
    rc = cmd_grayscale_images(force=False)
    if rc != 0:
        return rc

    # Always reassemble before rendering. Assembly is cheap, and the image
    # preference pass depends on sibling figure files (*.gray.png, *.png) whose
    # timestamps are not represented in the chapter source list.
    print("Refreshing assembled markdown before PDF render.")
    rc = cmd_assemble(endnotes_mode=endnotes_mode, promote_svgs=False)
    if rc != 0:
        return rc

    if not have("pandoc"):
        print("pandoc not found. Install via: brew install pandoc", file=sys.stderr)
        return 1
    if not have("xelatex"):
        print("xelatex not found. Install via: brew install --cask basictex   (then `sudo tlmgr install xetex`)", file=sys.stderr)
        return 1

    # Generate the Devanagari preamble by substituting the font name from
    # as_book.yaml into the template. The rendered file is a build artifact.
    if chapter_folio is None:
        chapter_folio = setting("book", layout, "chapter_folio")
    generated_preamble = render_devanagari_preamble(
        METADATA_FILE, chapter_folio,
        defer_mainmatter=setting("book", layout, "defer_mainmatter"),
        appendix_fontsize=setting("book", layout, "appendix_fontsize"),
        endnotes_fontsize=setting("book", layout, "endnotes_fontsize"),
        endnotes_linestretch=setting("book", layout, "endnotes_linestretch"),
    )

    geometry = setting("book", layout, "geometry")
    fontsize = setting("book", layout, "fontsize")
    linestretch = setting("book", layout, "linestretch")
    cmd = [
        "pandoc",
        str(md_path),
        "-o", str(pdf_path),
        "--pdf-engine=xelatex",
        "--metadata-file", str(METADATA_FILE),
        "--include-before-body", str(BOOK_DIR / "templates" / "review-frontmatter.tex"),
        "--lua-filter", str(LATEX_SHORT_FIGURE_CAPTIONS_FILTER),
        "--lua-filter", str(LATEX_STRIKEOUT_FILTER),
        # Layout geometry and fontsize are layout-specific (CLI-driven), so
        # they stay outside YAML.
        "-V", f"geometry:{geometry}",
        "-V", f"linestretch={linestretch}",
        "-H", str(generated_preamble),
    ]
    if layout == "review-a4":
        cmd += ["-H", str(BOOK_DIR / "templates" / "review-packet-preamble.tex")]
    cmd += fontsize_cli_args(fontsize, "book")
    cmd += mainfont_cli_args(METADATA_FILE)

    print(
        f"Rendering PDF (layout={layout}, fontsize={fontsize}, "
        f"linestretch={linestretch}, progress every {progress_pages} pages)..."
    )
    result = run_pandoc_with_progress(cmd, page_interval=progress_pages, label="PDF")
    if result.returncode != 0:
        print("PDF rendering FAILED. pandoc stderr:\n", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return result.returncode
    if result.stderr.strip():
        print("pandoc warnings:")
        print(result.stderr[:1000])
        report_oversized_floats(result.stderr, cmd)
    print(f"PDF rendered → {pdf_path.relative_to(BOOK_DIR)}")
    verify_figures_present(pdf_path, md_path.read_text())
    return 0


def section_join(sections: list[str]) -> list[str]:
    if not sections:
        return []
    joined: list[str] = []
    for section in sections:
        if not section.strip():
            continue
        joined.extend([section.rstrip(), ""])
    return joined


def cmd_reference(layout: str = "letter", progress_pages: int = DEFAULT_PROGRESS_PAGES) -> int:
    """Build the Source and Reference Companion as a standalone PDF.

    Reads four sources:
      - as_reference_front.md  — front matter prose (preface + navigation)
      - as_reference_*.md    — reference-only technical appendices
      - as_endnotes.md       — endnote entries in their topical-cluster order
      - as_reference.yaml    — companion-specific pandoc metadata (title, etc.)

    Promotes the entry headings from ### (subsection) to ## (section) so the
    PDF hierarchy under the Endnotes chapter is clean. Writes
    build/atomic_sanskrit_reference.md and renders the PDF.
    """
    rc = cmd_promote_svgs(force=False)
    if rc != 0:
        return rc

    BUILD_DIR.mkdir(exist_ok=True)
    if not REFERENCE_FRONT_FILE.exists():
        print(f"Missing: {REFERENCE_FRONT_FILE.name}", file=sys.stderr)
        return 1
    if not REFERENCE_METADATA_FILE.exists():
        print(f"Missing: {REFERENCE_METADATA_FILE.name}", file=sys.stderr)
        return 1
    endnotes_path = BOOK_DIR / "manuscript" / "as_endnotes.md"
    if not endnotes_path.exists():
        print(f"Missing: {endnotes_path.name}", file=sys.stderr)
        return 1

    front = REFERENCE_FRONT_FILE.read_text().rstrip()
    reference_files = sorted(
        path for path in BOOK_DIR.glob(REFERENCE_APPENDIX_GLOB)
        if path != REFERENCE_FRONT_FILE
    )
    reference_sections = [
        DRAFT_NOTES_RE.sub("", path.read_text()).rstrip()
        for path in reference_files
    ]

    # Read endnotes source as-is, then strip its existing top-line header note
    # (the `# Atomic Sanskrit — Endnotes (Expanded Prose)` heading and the
    # status blockquote that follows it) so the companion's own front matter
    # supplies the opening. Everything from the first `### \`stub\`` onward
    # is the entry corpus.
    endnotes_raw = endnotes_path.read_text()
    first_entry = re.search(r"^### `", endnotes_raw, re.MULTILINE)
    if not first_entry:
        print("No endnote entries found in as_endnotes.md", file=sys.stderr)
        return 1
    entries_body = endnotes_raw[first_entry.start():]

    # Promote ### entry headings → ## section headings within the Endnotes
    # chapter so the level hierarchy is # Endnotes → ## stub-name, not the
    # gapped # Endnotes → ### stub-name. Use a careful regex that only
    # matches entry headings (`### \`stub\``), not arbitrary ### usage.
    # Cite the same numbers the book prints. A reader holding the printed
    # volume has a number, not a stub name, and hunting a hyphenated slug
    # through 200-odd pages is not a cross-reference. The book's numbering is
    # authoritative, so read its map rather than re-deriving it here: the
    # numbers come from marker order in the assembled body, which this build
    # never produces.
    if not NOTE_NUMBER_MAP.exists():
        print(f"Missing {NOTE_NUMBER_MAP.relative_to(BOOK_DIR)} — the note "
              "numbers come from the book build.\n"
              "Run:  python build_book.py assemble   (or any book pdf build)\n"
              "first, then rebuild the companion.", file=sys.stderr)
        return 1
    number_map = json.loads(NOTE_NUMBER_MAP.read_text())
    numbers = number_map["notes"]
    uncited = []

    def promote(match: re.Match) -> str:
        stub = match.group(1).strip("`")
        number = numbers.get(stub)
        if number is None:
            # An entry the book never cites has no number to share. Print it
            # rather than failing — the corpus is allowed to hold material the
            # main text does not point at — but say how many, so a marker that
            # went missing from a chapter does not pass unnoticed.
            uncited.append(stub)
            return f"## {match.group(1)}"
        return f"## [{number}] {match.group(1)}"

    entries_body = re.sub(
        r"^### (`[a-z0-9_-]+`)\s*$",
        promote,
        entries_body,
        flags=re.MULTILINE,
    )
    print(f"  note numbers: {len(numbers)} from the book build of "
          f"{number_map['generated']}")
    if uncited:
        print(f"  {len(uncited)} entr{'y' if len(uncited) == 1 else 'ies'} not "
              f"cited by the book — printed unnumbered: "
              f"{', '.join(uncited[:4])}{' …' if len(uncited) > 4 else ''}")

    # The source uses thematic breaks to delimit endnote records. In the
    # reference PDF, the promoted entry heading and its vertical spacing
    # already provide that separation; printing the rule duplicates it.
    entries_body = re.sub(
        r"^---\s*$\n?",
        "\n",
        entries_body,
        flags=re.MULTILINE,
    )

    assembled = "\n".join([
        front,
        "",
        *section_join(reference_sections),
        "# Endnotes",
        "",
        entries_body.rstrip(),
        "",
    ])
    assembled = prefer_png_images_for_pdf(assembled)
    # Count source content before typesetting-only font wrappers inflate the
    # whitespace-delimited total.
    word_count = len(assembled.split())
    # Wrap non-Latin scripts in raw-LaTeX font-switch commands per the same
    # convention cmd_assemble uses.
    assembled = wrap_scripts_for_latex(assembled)

    layout_suffix = "" if layout == "letter" else f".{layout}"
    md_path = BUILD_DIR / "atomic_sanskrit_reference.md"
    pdf_path = BUILD_DIR / f"atomic_sanskrit_reference{layout_suffix}.pdf"
    md_path.write_text(assembled)
    print(f"Assembled companion → {md_path.relative_to(BOOK_DIR)} ({word_count:,} words)")
    warn_uncovered_characters(assembled, REFERENCE_METADATA_FILE)

    if not have("pandoc"):
        print("pandoc not found. Install via: brew install pandoc", file=sys.stderr)
        return 1
    if not have("xelatex"):
        print("xelatex not found. Install via: brew install --cask basictex", file=sys.stderr)
        return 1

    # Same Devanagari-preamble template substitution as cmd_pdf, but using
    # the companion's font name (which currently matches the book's; the
    # template substitution still goes through so the two pipelines are
    # symmetric).
    generated_preamble = render_devanagari_preamble(
        REFERENCE_METADATA_FILE,
        setting("companion", layout, "chapter_folio"),
        defer_mainmatter=setting("companion", layout, "defer_mainmatter"),
        appendix_fontsize=setting("companion", layout, "appendix_fontsize"),
        endnotes_fontsize=setting("companion", layout, "endnotes_fontsize"),
        endnotes_linestretch=setting("companion", layout, "endnotes_linestretch"),
    )

    geometry = setting("companion", layout, "geometry")
    fontsize = setting("companion", layout, "fontsize")
    linestretch = setting("companion", layout, "linestretch")
    cmd = [
        "pandoc",
        str(md_path),
        "-o", str(pdf_path),
        "--pdf-engine=xelatex",
        "--metadata-file", str(REFERENCE_METADATA_FILE),
        "--lua-filter", str(LATEX_STRIKEOUT_FILTER),
        "-V", f"geometry:{geometry}",
        "-V", f"linestretch={linestretch}",
        "-H", str(generated_preamble),
    ]
    cmd += fontsize_cli_args(fontsize, "book")
    cmd += mainfont_cli_args(REFERENCE_METADATA_FILE)

    print(
        f"Rendering companion PDF (layout={layout}, fontsize={fontsize}, "
        f"linestretch={linestretch}, "
        f"progress every {progress_pages} pages)..."
    )
    result = run_pandoc_with_progress(cmd, page_interval=progress_pages, label="Companion")
    if result.returncode != 0:
        print("Companion PDF rendering FAILED. pandoc stderr:\n", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return result.returncode
    if result.stderr.strip():
        print("pandoc warnings:")
        print(result.stderr[:1000])
    print(f"Companion PDF rendered → {pdf_path.relative_to(BOOK_DIR)}")
    return 0


def cmd_convert(input_arg: str | None, layout: str = "letter", output_arg: str | None = None,
                 progress_pages: int = DEFAULT_PROGRESS_PAGES) -> int:
    """Convert an arbitrary Markdown file to PDF using the book's font stack
    (STIX Two Text for Latin/IAST + the Devanagari preamble) — WITHOUT the book's
    title-page metadata, so no "Atomic Sanskrit" title block is stamped on the
    document. Output lands in build/ by default; override with -o."""
    if not input_arg:
        print("convert requires an input file, e.g.:  python3 build_book.py convert FILE.md", file=sys.stderr)
        return 1
    src = Path(input_arg)
    if not src.is_absolute():
        src = BOOK_DIR / src
    if not src.exists():
        print(f"Input not found: {input_arg}", file=sys.stderr)
        return 1
    if not have("pandoc"):
        print("pandoc not found. Install via: brew install pandoc", file=sys.stderr)
        return 1
    if not have("xelatex"):
        print("xelatex not found. Install via: brew install --cask basictex", file=sys.stderr)
        return 1

    BUILD_DIR.mkdir(exist_ok=True)
    if output_arg:
        pdf_path = Path(output_arg)
        if not pdf_path.is_absolute():
            pdf_path = BOOK_DIR / pdf_path
    else:
        pdf_path = BUILD_DIR / f"{src.stem}.pdf"

    # Devanagari preamble (same substitution the book render uses), so
    # देवनागरी renders with the configured font.
    generated_preamble = render_devanagari_preamble(METADATA_FILE)

    # Pull only the font from as_book.yaml (not the full metadata) — the Latin
    # font carries the IAST diacritics; the title/header-includes are left
    # out. Font size is layout-specific rather than a fixed book property —
    # see the presentation tables at the top of this file.
    fontsize = setting("book", layout, "fontsize")
    linestretch = setting("book", layout, "linestretch")

    # Wrap non-Latin script runs (Devanagari, Tamil, …) in raw-LaTeX font
    # groups — the same pass the book/reference builds run. The preamble only
    # *defines* the script fonts; wrap_scripts_for_latex is what applies them,
    # so without this step Devanagari falls back to the Latin mainfont.
    tmp_md = BUILD_DIR / f"{src.stem}.for-pdf.md"
    tmp_md.write_text(wrap_scripts_for_latex(src.read_text()))

    cmd = [
        "pandoc", str(tmp_md),
        "-o", str(pdf_path),
        "--pdf-engine=xelatex",
        "--lua-filter", str(LATEX_STRIKEOUT_FILTER),
        "-V", f"geometry:{setting('book', layout, 'geometry')}",
        "-V", f"linestretch={linestretch}",
        "-H", str(generated_preamble),
    ]
    if layout == "review-a4":
        cmd += ["-H", str(BOOK_DIR / "templates" / "review-packet-preamble.tex")]
    cmd += fontsize_cli_args(fontsize, "article")
    cmd += mainfont_cli_args(METADATA_FILE)
    print(
        f"Converting {src.name} → {pdf_path.relative_to(BOOK_DIR)} "
        f"(layout={layout}, fontsize={fontsize}, linestretch={linestretch})..."
    )
    result = run_pandoc_with_progress(cmd, page_interval=progress_pages, label="PDF")
    if result.returncode != 0:
        print("PDF conversion FAILED. pandoc stderr:\n", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return result.returncode
    if result.stderr.strip():
        print("pandoc warnings:")
        print(result.stderr[:1000])
    print(f"PDF → {pdf_path.relative_to(BOOK_DIR)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Atomic Sanskrit book builder.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "phase",
        choices=["stubs", "assemble", "pdf", "all", "reference", "promote-svgs", "grayscale-images", "convert"],
        nargs="?",
        default="all",
        help="Pipeline phase to run (default: all). 'reference' builds the "
             "Source and Reference Companion as a standalone PDF. 'convert' "
             "renders an arbitrary .md file to PDF (see the 'input' argument).",
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=None,
        help="For 'convert': the Markdown file to render to PDF (output goes to build/<name>.pdf).",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="For 'convert': output PDF path (default: build/<name>.pdf).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing stub files or regenerate all grayscale images",
    )
    parser.add_argument(
        "--layout",
        choices=list(LAYOUTS),
        default="letter",
        help="PDF page layout (default: letter). Applies to pdf/all/reference/convert. "
             "For 'convert', review-a4 is intended for printable reader packets.",
    )
    parser.add_argument(
        "--endnotes",
        choices=["full", "short"],
        default="full",
        help="Endnote rendering mode (default: full). 'short' emits the one-sentence "
             "Short field from as_endnotes.md per entry, for the printed-book apparatus; "
             "'full' emits the complete long-form body per entry, for the companion. "
             "Output filenames are suffixed with .short in short mode so the two "
             "variants coexist.",
    )
    folio = parser.add_mutually_exclusive_group()
    folio.add_argument(
        "--no-chapter-folio",
        dest="chapter_folio",
        action="store_false",
        default=None,
        help="Suppress the page number on chapter, part and contents opening "
             "pages (the bottom-centre folio LaTeX's 'plain' style prints). "
             "Does not change the page count. Overrides the layout default in "
             "the presentation tables.",
    )
    folio.add_argument(
        "--chapter-folio",
        dest="chapter_folio",
        action="store_true",
        default=None,
        help="Force the chapter-opening folio on, overriding the layout default.",
    )
    parser.add_argument(
        "--progress-pages",
        type=int,
        default=DEFAULT_PROGRESS_PAGES,
        help=f"Print a progress line every N pages xelatex typesets, instead of "
             f"blocking silently until the whole PDF is done (default: {DEFAULT_PROGRESS_PAGES}). "
             "Applies to pdf/all/reference/convert.",
    )
    args = parser.parse_args()

    # Before any subprocess inherits the environment.
    if bindir := prefer_local_texlive():
        print(f"  using TeX Live at {bindir}")

    if args.phase == "stubs":
        return cmd_stubs(force=args.force)
    if args.phase == "assemble":
        return cmd_assemble(endnotes_mode=args.endnotes)
    if args.phase == "pdf":
        return cmd_pdf(layout=args.layout, endnotes_mode=args.endnotes, progress_pages=args.progress_pages,
                       chapter_folio=args.chapter_folio)
    if args.phase == "reference":
        return cmd_reference(layout=args.layout, progress_pages=args.progress_pages)
    if args.phase == "convert":
        return cmd_convert(args.input, layout=args.layout, output_arg=args.output,
                            progress_pages=args.progress_pages)
    if args.phase == "promote-svgs":
        return cmd_promote_svgs(force=args.force)
    if args.phase == "grayscale-images":
        return cmd_grayscale_images(force=args.force)
    # all
    if (rc := cmd_stubs(force=args.force)) != 0:
        return rc
    if (rc := cmd_assemble(endnotes_mode=args.endnotes)) != 0:
        return rc
    return cmd_pdf(layout=args.layout, endnotes_mode=args.endnotes, progress_pages=args.progress_pages,
                       chapter_folio=args.chapter_folio)


if __name__ == "__main__":
    sys.exit(main())

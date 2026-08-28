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
  - Fonts: see as_book.yaml (currently EB Garamond + Adobe Devanagari)

Canonical metadata source:
  as_book.yaml — title, subtitle, author, fonts, document structure. Edit
values there; this script reads from it via pandoc's --metadata-file.
"""

from __future__ import annotations

import argparse
import datetime
import os
import pty
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
LAYOUTS = {
    "letter": "letterpaper,margin=1in",
    # A4 with 1in margins — for the `convert` subcommand / non-US page size.
    "a4": "a4paper,inner=0.85in,outer=0.5in,top=0.75in,bottom=0.75in",
    # ~4.5×7.5 text block centered on 8.5×11 — book-page mock-up on letter paper.
    "book-on-letter": "paperwidth=8.5in,paperheight=11in,textwidth=4.5in,textheight=7.5in,centering",
    # True 6×9 trim with book-style asymmetric margins (inner > outer for binding).
    "trade": "paperwidth=6in,paperheight=9in,inner=0.75in,outer=0.5in,top=0.5in,bottom=0.75in",
    # 6×9 trim centered on letter paper, with crop marks for local proof printing.
    "trade-crop": "paperwidth=8.5in,paperheight=11in,layoutwidth=6in,layoutheight=9in,layouthoffset=1.25in,layoutvoffset=1in,inner=0.75in,outer=0.5in,top=0.5in,bottom=0.75in,showcrop",
    # Narrow 3×6 trim with minimal margins — sized for phone-screen reading.
    # ~2.6×5.6 text block (~81% of page area is text) maximizes readable area.
    "phone": "paperwidth=3.5in,paperheight=7in,margin=0.1in",
}

# Per-layout base font size (pandoc -V fontsize:...), for the main book build
# (cmd_pdf / cmd_convert). Moved out of as_book.yaml (2026-08-27) for the same
# reason geometry lives here rather than in YAML: font size is layout-
# specific, not a fixed book property — a phone-trim page needs smaller type
# than a full letter page. Every entry defaults to the book's historical
# 12pt; adjust individual layouts here as needed. (as_reference.yaml's own
# `fontsize:` for the Source and Reference Companion is untouched — cmd_reference
# still reads it directly, so the two publications can size independently.)
LAYOUT_FONTSIZES = {
    "letter": "12pt",
    "a4": "12pt",
    "book-on-letter": "11pt",
    "trade": "11pt",
    "trade-crop": "11pt",
    "phone": "11pt",
}


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
    # Devanagari block + ZWJ/ZWNJ joiners.
    (r"\devanagarifont",  re.compile(r"[ऀ-ॿ‌‍]+")),
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
    # body text and EB Garamond drops them with only a warning.
    (r"\brahmifont",      re.compile(r"[\U00011000-\U0001107F]+")),
    # Stragglers — specific characters Charter Roman lacks. Kept narrow so
    # that common IAST diacritics Charter does carry (ṃ ṛ ṣ ā ī ū ḥ ñ ṅ etc.)
    # are NOT switched mid-word — that would look jarring against the Charter
    # body prose. List below is the closed set of characters the assembled
    # book actually contains that Charter cannot render.
    (r"\symbolfont",      re.compile(
        r"["
        r"←→"      # ← →
        r"✓✗"      # ✓ ✗ (table cell glyphs)
        r"₀-₉"     # subscript digits ₀-₉
        r"ʷʾʿ"     # modifier letters ʷ ʾ ʿ
        r"ɑɓɗʄɠʈʂʔ"  # rare phonetic symbols used in inventory/endnote examples
        r"ēō"      # ē ō (Latin with macron)
        r"ḱẓ"      # ḱ ẓ
        r"⊇"       # superset-or-equal (Ch 18 §18.x: Sanskrit ⊇ PIE) —
                   # Charter Bold lacks U+2287; Arial Unicode MS has it
        r"]+"
    )),
]


def wrap_scripts_for_latex(md_text: str) -> str:
    """Wrap every non-Latin script run in raw-LaTeX `{\\<fontname> …}`.
    Applied during assembly so the rendered PDF has unconditional font
    selection regardless of surrounding TeX context."""
    fired: set[str] = set()
    for font_cmd, pattern in SCRIPT_WRAPS:
        md_text, n = pattern.subn(
            lambda m, _f=font_cmd: f"`{{{_f} {m.group(0)}}}`{{=latex}}",
            md_text,
        )
        if n:
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
        re.findall(r"\\newfontfamily\{(\\[a-z]+font)\}", PREAMBLE_TEMPLATE.read_text())
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
# replaced with a provisional numbered reference `[N]`; the collected pairs
# are rendered as an "Endnote References" section at the end of the book.
# Numerical conversion is the chapter-lock convention from CLAUDE.md; doing
# it at build time produces a clean draft PDF without verbose inline markers
# until the expanded prose is drafted.
NOTE_MARKER_RE = re.compile(r"\[NOTE:\s*([a-z0-9_-]+)\s*\]")


def number_note_markers(md_text: str, start: int = 1) -> tuple[str, list[tuple[int, str]]]:
    """Replace inline [NOTE: stub-name] markers with numbered references.
    Returns (processed_text, list of (number, stub-name) tuples in encounter
    order)."""
    notes: list[tuple[int, str]] = []
    counter = [start - 1]

    def replace(match: re.Match) -> str:
        counter[0] += 1
        stub = match.group(1)
        notes.append((counter[0], stub))
        return f"`\\textsuperscript{{[{counter[0]}]}}`{{=latex}}"

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
        body = m.group(2).strip()
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
    for entry in ASSEMBLY:
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
                print(f"  include {filename} (dedication)")
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
                    print(f"  include {filename} (part opener)")
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
            chunks[:] = [numbered_body]
            unified = render_unified_endnotes(notes, mode=endnotes_mode)
            if unified:
                chunks.append("\n" + unified)
                mode_label = "short" if endnotes_mode == "short" else "full"
                print(f"  include unified Endnotes ({len(notes)} entries, "
                      f"mode={mode_label})")
            # Skip the as_endnotes.md raw include — its content is now folded
            # into the unified Endnotes by load_drafted_endnotes().
            continue

        path = BOOK_DIR / filename
        if not path.exists():
            print(f"  MISSING: {filename}", file=sys.stderr)
            missing.append(filename)
            continue

        cleaned = clean_chapter(path.read_text(), title)
        chunks.append(cleaned + "\n")
        print(f"  include {filename}")

    assembled = "".join(chunks)
    assembled = prefer_png_images_for_pdf(assembled)
    # Raw-HTML <img> scaffold icons are otherwise dropped outright by
    # pandoc's LaTeX writer — convert them to a raw-LaTeX \includegraphics
    # call before the script-wrapping pass below.
    assembled = render_scaffold_icons_for_pdf(assembled)
    # Wrap non-Latin scripts in raw-LaTeX font-switch commands. See
    # wrap_scripts_for_latex / SCRIPT_WRAPS for the per-script ranges.
    assembled = wrap_scripts_for_latex(assembled)
    out_path.write_text(assembled)
    word_count = len(assembled.split())
    print(f"\nAssembled → {out_path.relative_to(BOOK_DIR)} ({word_count:,} words)")
    if missing:
        print(f"WARNING: {len(missing)} file(s) missing.")
    return 0


def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


DEFAULT_PROGRESS_PAGES = 20
PAGE_BRACKET_RE = re.compile(r"\[(\d+)\]")
LATEX_RUN_RE = re.compile(r"\[INFO\] \[makePDF\] LaTeX run number (\d+)")
WARNING_LINE_RE = re.compile(r"^.*\[WARNING\].*$", re.MULTILINE)


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
            progress_pages: int = DEFAULT_PROGRESS_PAGES) -> int:
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
    devanagari_font = read_yaml_value(METADATA_FILE, "devanagarifont")
    preamble_text = PREAMBLE_TEMPLATE.read_text().replace("__DEVANAGARIFONT__", devanagari_font)
    generated_preamble = BUILD_DIR / "devanagari-preamble.tex"
    generated_preamble.write_text(preamble_text)

    geometry = LAYOUTS[layout]
    fontsize = LAYOUT_FONTSIZES[layout]
    cmd = [
        "pandoc",
        str(md_path),
        "-o", str(pdf_path),
        "--pdf-engine=xelatex",
        "--metadata-file", str(METADATA_FILE),
        "--lua-filter", str(LATEX_STRIKEOUT_FILTER),
        # Layout geometry and fontsize are layout-specific (CLI-driven), so
        # they stay outside YAML.
        "-V", f"geometry:{geometry}",
        "-V", f"fontsize={fontsize}",
        "-H", str(generated_preamble),
    ]

    print(f"Rendering PDF (layout={layout}, fontsize={fontsize}, progress every {progress_pages} pages)...")
    result = run_pandoc_with_progress(cmd, page_interval=progress_pages, label="PDF")
    if result.returncode != 0:
        print("PDF rendering FAILED. pandoc stderr:\n", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return result.returncode
    if result.stderr.strip():
        print("pandoc warnings:")
        print(result.stderr[:1000])
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
    reference_sections = [path.read_text().rstrip() for path in reference_files]

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
    entries_body = re.sub(
        r"^### (`[a-z0-9_-]+`)\s*$",
        r"## \1",
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
    # Wrap non-Latin scripts in raw-LaTeX font-switch commands per the same
    # convention cmd_assemble uses.
    assembled = wrap_scripts_for_latex(assembled)

    layout_suffix = "" if layout == "letter" else f".{layout}"
    md_path = BUILD_DIR / "atomic_sanskrit_reference.md"
    pdf_path = BUILD_DIR / f"atomic_sanskrit_reference{layout_suffix}.pdf"
    md_path.write_text(assembled)
    word_count = len(assembled.split())
    print(f"Assembled companion → {md_path.relative_to(BOOK_DIR)} ({word_count:,} words)")

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
    devanagari_font = read_yaml_value(REFERENCE_METADATA_FILE, "devanagarifont")
    preamble_text = PREAMBLE_TEMPLATE.read_text().replace("__DEVANAGARIFONT__", devanagari_font)
    generated_preamble = BUILD_DIR / "devanagari-preamble.tex"
    generated_preamble.write_text(preamble_text)

    geometry = LAYOUTS[layout]
    cmd = [
        "pandoc",
        str(md_path),
        "-o", str(pdf_path),
        "--pdf-engine=xelatex",
        "--metadata-file", str(REFERENCE_METADATA_FILE),
        "--lua-filter", str(LATEX_STRIKEOUT_FILTER),
        "-V", f"geometry:{geometry}",
        "-H", str(generated_preamble),
    ]

    print(f"Rendering companion PDF (layout={layout}, progress every {progress_pages} pages)...")
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
    (EB Garamond for Latin/IAST + the Devanagari preamble) — WITHOUT the book's
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
    devanagari_font = read_yaml_value(METADATA_FILE, "devanagarifont")
    preamble_text = PREAMBLE_TEMPLATE.read_text().replace("__DEVANAGARIFONT__", devanagari_font)
    generated_preamble = BUILD_DIR / "devanagari-preamble.tex"
    generated_preamble.write_text(preamble_text)

    # Pull only the font from as_book.yaml (not the full metadata) — the Latin
    # font carries the IAST diacritics; the title/header-includes are left
    # out. Font size comes from LAYOUT_FONTSIZES (layout-specific, not a
    # fixed book property — see the comment beside that dict above).
    mainfont = read_yaml_value(METADATA_FILE, "mainfont")
    fontsize = LAYOUT_FONTSIZES[layout]

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
        "-V", f"geometry:{LAYOUTS[layout]}",
        "-V", f"mainfont={mainfont}",
        "-V", f"fontsize={fontsize}",
        "-H", str(generated_preamble),
    ]
    print(f"Converting {src.name} → {pdf_path.relative_to(BOOK_DIR)} (layout={layout})...")
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
             "For 'convert', letter and a4 are the usual page sizes.",
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
    parser.add_argument(
        "--progress-pages",
        type=int,
        default=DEFAULT_PROGRESS_PAGES,
        help=f"Print a progress line every N pages xelatex typesets, instead of "
             f"blocking silently until the whole PDF is done (default: {DEFAULT_PROGRESS_PAGES}). "
             "Applies to pdf/all/reference/convert.",
    )
    args = parser.parse_args()

    if args.phase == "stubs":
        return cmd_stubs(force=args.force)
    if args.phase == "assemble":
        return cmd_assemble(endnotes_mode=args.endnotes)
    if args.phase == "pdf":
        return cmd_pdf(layout=args.layout, endnotes_mode=args.endnotes, progress_pages=args.progress_pages)
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
    return cmd_pdf(layout=args.layout, endnotes_mode=args.endnotes, progress_pages=args.progress_pages)


if __name__ == "__main__":
    sys.exit(main())

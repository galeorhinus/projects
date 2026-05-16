#!/usr/bin/env python3
"""
build_book.py — Atomic Sanskrit book assembly + PDF pipeline.

Phases (run any one, or `all` for the full pipeline):
  stubs    — create placeholder draft files for missing chapters
  assemble — concatenate all chapter files into build/atomic_sanskrit.md
  pdf      — render the assembled markdown to PDF via pandoc + xelatex
  all      — run stubs → assemble → pdf (default)

Usage:
  python3 build_book.py                              # full pipeline (default layout)
  python3 build_book.py stubs                        # just generate missing stubs
  python3 build_book.py assemble                     # just concatenate
  python3 build_book.py pdf                          # just render the PDF
  python3 build_book.py stubs --force                # overwrite existing stub files
  python3 build_book.py pdf --layout book-on-letter  # book-mock layout on letter paper
  python3 build_book.py pdf --layout trade           # true 6×9 trim size
  python3 build_book.py pdf --layout phone           # 3×6 phone-reading trim

Layouts:
  letter           8.5×11 paper, 1in margins. Manuscript review.
  book-on-letter   8.5×11 paper with a centered ~4.5×7.5 text block — looks
                   like a 6×9 book page printed inside letter margins.
  trade            True 6×9 trim. For print-on-demand uploads.
  phone            3×6 trim with 0.2in margins. Sized for phone-screen reading.

Dependencies:
  - pandoc  (brew install pandoc)
  - xelatex (brew install --cask basictex   or full mactex)
  - Fonts: see as_book.yaml (currently Charter + Adobe Devanagari)

Canonical metadata source:
  as_book.yaml — title, subtitle, author, fonts, document structure. Edit
  values there; this script reads from it via pandoc's --metadata-file.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

BOOK_DIR = Path(__file__).resolve().parent
BUILD_DIR = BOOK_DIR / "build"
METADATA_FILE = BOOK_DIR / "as_book.yaml"
PREAMBLE_TEMPLATE = BOOK_DIR / "templates" / "devanagari-preamble.tex.in"

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

# Assembly order: (kind, filename, canonical-title)
# kind ∈ {"front", "part", "chapter", "end"}
# kind=="part" entries carry filename=None; they emit a \part{} break only.
ASSEMBLY = [
    ("front",   "as_00_0preface_draft.md",               "Preface"),
    ("front",   "as_00_chapter_draft.md",                "Chapter 0 — A Language for Seekers, of Freedom, of Infinity"),

    ("part",    None,                                     "Part I — The Wrong Metaphor"),
    ("chapter", "as_01_chapter_draft.md",                 "Chapter 1 — The Botanical Fallacy"),
    ("chapter", "as_02_chapter_draft.md",                 "Chapter 2 — The Strategic Necessity"),
    ("chapter", "as_03_chapter_draft.md",                 "Chapter 3 — The Fourth Abrahamic Religion"),

    ("part",    None,                                     "Part II — The Sanskrit Self-Conception"),
    ("chapter", "as_04_chapter_draft.md",                 "Chapter 4 — Siddha and Kārya"),
    ("chapter", "as_05_chapter_draft.md",                 "Chapter 5 — Apabhraṃśa and Entropy"),
    ("chapter", "as_06_chapter_draft.md",                 "Chapter 6 — Reclaiming the Dhātuḥ"),

    ("part",    None,                                     "Part III — The Sound-Field"),
    ("chapter", "as_07_chapter_draft.md",                 "Chapter 7 — Ādivādya: The World's First Instrument"),
    ("chapter", "as_08_chapter_draft.md",                 "Chapter 8 — Mapping the Mouth"),
    ("chapter", "as_09_chapter_draft.md",                 "Chapter 9 — Flexing the Retroflex"),
    ("chapter", "as_10_chapter_draft.md",                 "Chapter 10 — The Subcontinental Superset"),

    ("part",    None,                                     "Part IV — The Atomic Architecture"),
    ("chapter", "as_11_chapter_draft.md",                 "Chapter 11 — Building the Dhātuḥ"),
    ("chapter", "as_12_chapter_draft.md",                 "Chapter 12 — The Periodic Table of Gaṇāḥ"),
    ("chapter", "as_13_chapter_draft.md",                 "Chapter 13 — The Chemistry of Affixation"),

    ("part",    None,                                     "Part V — Anti-Entropy in Practice"),
    ("chapter", "as_14_chapter_draft.md",                 "Chapter 14 — The Problem of Preservation"),
    ("chapter", "as_15_chapter_draft.md",                 "Chapter 15 — The Calibration Matrix"),
    ("chapter", "as_16_chapter_draft.md",                 "Chapter 16 — Aural Architecture"),

    ("part",    None,                                     "Part VI — Killing PIE"),
    ("chapter", "as_17_chapter_draft.md",                 "Chapter 17 — The Wrong Question"),
    ("chapter", "as_18_chapter_draft.md",                 "Chapter 18 — PIE in the Sky"),
    ("chapter", "as_19_chapter_draft.md",                 "Chapter 19 — Life After PIE"),

    ("end",     "as_90_epilogue_draft.md",                "Epilogue — The Atomic Corollary Going Forward"),
    ("end",     "as_91_appendix.md",                      "Appendix Part 1 — Baking the Mother Tongue"),
    ("end",     "as_92_appendix.md",                      "Appendix Part 2 — The Encyclopaedic Confirmation"),
    ("end",     "as_93_appendix.md",                      "Appendix Part 3 — The Imperishable Audiograph"),
    ("end",     "as_94_appendix.md",                      "Appendix Part 4 — The Language Factory"),
    ("end",     "as_endnotes.md",                         "Endnotes"),
]


# Stub content sourced from as_toc_annotated.md. Keys are the filenames that
# do not yet have a draft; values are the canonical title and the TOC summary
# that will be planted as placeholder prose.
STUB_FILES = {
    "as_11_chapter_draft.md": {
        "title": "Chapter 11 — Building the *Dhātuḥ*",
        "summary": "The foundational synthesis: how subatomic particles (*varṇāḥ*) combine into elemental atoms (*dhātavaḥ*). *Svarāḥ* (vowels) as protons, *vyañjanāni* (consonants) as electrons; the principle of structural compression that places the thermodynamic threshold at five constituent particles.",
    },
    "as_12_chapter_draft.md": {
        "title": "Chapter 12 — The Periodic Table of गणाः (*Gaṇāḥ*)",
        "summary": "The central architectural claim. Pāṇini's ten *gaṇāḥ* function as the vertical columns of a periodic table. Three reactivity tiers — polyvalent, bivalent, monovalent — map the *dhātavaḥ* into the engineering grid. Valency defined as quantifiable chemical yield rather than subjective utility.",
    },
    "as_13_chapter_draft.md": {
        "title": "Chapter 13 — The Chemistry of Affixation",
        "summary": "The bonding chemistry. The 22 *upasargāḥ* (prefixes) as catalytic functional groups; the *pratyayāḥ* (suffixes) as valence-shell stabilizers. The full pipeline: *varṇaḥ → dhātuḥ → śabdaḥ → padam → vākyam* — complete molecular saturation produces syntactic fluidity.",
    },
}


# PDF page layouts. Each entry is a pandoc -V geometry:... value.
LAYOUTS = {
    "letter": "margin=1in",
    # ~4.5×7.5 text block centered on 8.5×11 — book-page mock-up on letter paper.
    "book-on-letter": "paperwidth=8.5in,paperheight=11in,textwidth=4.5in,textheight=7.5in,centering",
    # True 6×9 trim with book-style asymmetric margins (inner > outer for binding).
    "trade": "paperwidth=6in,paperheight=9in,inner=0.875in,outer=0.625in,top=0.75in,bottom=0.875in",
    # Narrow 3×6 trim with minimal margins — sized for phone-screen reading.
    # ~2.6×5.6 text block (~81% of page area is text) maximizes readable area.
    "phone": "paperwidth=3in,paperheight=6in,margin=0.2in",
}


# Regexes for cleaning chapter files before assembly
DRAFT_NOTES_RE   = re.compile(r"\n---\s*\n+##+\s+Draft notes.*\Z", re.DOTALL)
DRAFT_HEADER_RE  = re.compile(r"^\*Draft v.*?\*\n+", re.DOTALL | re.MULTILINE)

# Per-script Unicode ranges for explicit font wrapping. Each entry is
# (font command, regex of script's character range).
# Why wrap: ucharclasses transitions silently fail in many xelatex contexts
# (TOC entries, headings, math-adjacent positions like √मा); the workaround
# is to wrap each script's runs in raw-LaTeX `{\<fontname> …}` so the font
# switch is unconditional inside the wrap group.
SCRIPT_WRAPS: list[tuple[str, re.Pattern]] = [
    # Devanagari block + ZWJ/ZWNJ joiners
    (r"\devanagarifont",  re.compile(r"[ऀ-ॿ‌‍]+")),
    # Arabic block (covers Arabic letters + diacritics)
    (r"\arabicfont",      re.compile(r"[؀-ۿ]+")),
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
    # CJK Unified Ideographs (Chinese characters used in Ch 19 contrast case)
    (r"\cjkfont",         re.compile(r"[一-鿿]+")),
    # Old Persian cuneiform (Mitanni / Indo-Iranian references)
    (r"\oldpersianfont",  re.compile(r"[\U000103A0-\U000103DF]+")),
    # Avestan (Indo-Iranian comparisons)
    (r"\avestanfont",     re.compile(r"[\U00010B00-\U00010B3F]+")),
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
        r"ēō"      # ē ō (Latin with macron)
        r"ḱẓ"      # ḱ ẓ
        r"]+"
    )),
]


def wrap_scripts_for_latex(md_text: str) -> str:
    """Wrap every non-Latin script run in raw-LaTeX `{\\<fontname> …}`.
    Applied during assembly so the rendered PDF has unconditional font
    selection regardless of surrounding TeX context."""
    for font_cmd, pattern in SCRIPT_WRAPS:
        md_text = pattern.sub(
            lambda m, _f=font_cmd: f"`{{{_f} {m.group(0)}}}`{{=latex}}",
            md_text,
        )
    return md_text


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
TODO_STUB_LINE_RE = re.compile(
    r"^\s*-\s*\[[ x~!]\]\s*\*\*(?:\[P[0-3]\]\s*)?`\[NOTE:\s*([a-z0-9_-]+)\s*\]`\.?\*\*\s*(.*?)$",
    re.MULTILINE,
)


def load_drafted_endnotes() -> dict[str, str]:
    """Parse as_endnotes.md and return { stub-name: drafted prose }."""
    path = BOOK_DIR / "as_endnotes.md"
    if not path.exists():
        return {}
    text = path.read_text()
    return {
        m.group(1): m.group(2).strip()
        for m in ENDNOTES_ENTRY_RE.finditer(text)
    }


def load_stub_descriptions() -> dict[str, str]:
    """Parse as_todo.md Section E and return { stub-name: description }."""
    path = BOOK_DIR / "as_todo.md"
    if not path.exists():
        return {}
    section = TODO_SECTION_E_RE.search(path.read_text())
    if not section:
        return {}
    return {
        m.group(1): m.group(2).strip()
        for m in TODO_STUB_LINE_RE.finditer(section.group(0))
    }


def render_unified_endnotes(notes: list[tuple[int, str]]) -> str:
    """Render a single unified Endnotes section. Each numbered entry carries
    drafted prose if available, otherwise the stub description from as_todo,
    otherwise a verification-pending placeholder. Replaces the earlier
    three-section split (Endnote References / Pending Stubs / Endnotes)."""
    if not notes:
        return ""
    drafted = load_drafted_endnotes()
    stubs = load_stub_descriptions()
    drafted_count = sum(1 for _, s in notes if s in drafted)
    described_count = sum(1 for _, s in notes if s not in drafted and s in stubs)
    pending_count = len(notes) - drafted_count - described_count

    lines = [
        "# Endnotes",
        "",
        f"*Numbered list of every inline note reference in the manuscript "
        f"({len(notes)} total: {drafted_count} drafted, {described_count} stub-described, "
        f"{pending_count} verification-pending). Each entry carries the fullest content "
        f"currently available — drafted prose where the verification has completed, "
        f"the verification-stub description where the citation is identified but "
        f"the note prose is not yet drafted, or a verification-pending placeholder "
        f"otherwise. The numbered references in the body of the book — the **[N]** "
        f"superscripts — point here.*",
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
        "`as_toc_annotated.md`. Replace with full draft prose before final build.\n"
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
        path = BOOK_DIR / fname
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


def clean_chapter(text: str, canonical_title: str) -> str:
    """Strip draft scaffolding and replace the top-level heading with the canonical title."""
    text = DRAFT_NOTES_RE.sub("", text)
    text = text.strip()

    # Replace the chapter's own # heading with the assembly's canonical title
    lines = text.split("\n", 1)
    if lines and lines[0].startswith("# "):
        rest = lines[1] if len(lines) > 1 else ""
        rest = DRAFT_HEADER_RE.sub("", rest.lstrip())
        text = f"# {canonical_title}\n\n{rest}"
    else:
        text = f"# {canonical_title}\n\n{text}"

    return text.strip() + "\n"


def cmd_assemble() -> int:
    BUILD_DIR.mkdir(exist_ok=True)
    out_path = BUILD_DIR / "atomic_sanskrit.md"

    chunks: list[str] = []
    # Metadata is no longer injected inline — pandoc reads it from
    # as_book.yaml at PDF render time via --metadata-file. Keeping
    # the assembled markdown pure content avoids duplication / drift.

    missing: list[str] = []
    for kind, filename, title in ASSEMBLY:
        if kind == "part":
            # Raw-LaTeX part break (pandoc passes through inside this fence)
            chunks.append(f"\n```{{=latex}}\n\\part{{{title}}}\n```\n\n")
            continue

        # When we reach as_endnotes.md, replace the three-section endnote
        # cluster (Endnote References / Pending Endnote Stubs / Endnotes)
        # with one unified Endnotes section: number every inline note marker
        # in the chapter chunks so far, then render a single numbered Endnotes
        # section that pulls content from as_endnotes.md (drafted prose) and
        # as_todo.md Section E (stub descriptions), with a verification-pending
        # placeholder where neither is available.
        if filename == "as_endnotes.md":
            body_so_far = "".join(chunks)
            numbered_body, notes = number_note_markers(body_so_far)
            chunks[:] = [numbered_body]
            unified = render_unified_endnotes(notes)
            if unified:
                chunks.append("\n" + unified)
                print(f"  include unified Endnotes ({len(notes)} entries; "
                      f"drafted prose + verification stubs + pending placeholders)")
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


def cmd_pdf(layout: str = "letter") -> int:
    md_path = BUILD_DIR / "atomic_sanskrit.md"
    # Suffix the PDF filename with the layout so multiple variants can coexist
    suffix = "" if layout == "letter" else f".{layout}"
    pdf_path = BUILD_DIR / f"atomic_sanskrit{suffix}.pdf"

    # Auto-assemble before rendering if the assembled markdown is missing or
    # any source chapter is newer than the assembled file. Cheap (assembly
    # is just concatenation) and guarantees the PDF reflects current sources.
    needs_assemble = not md_path.exists()
    if md_path.exists():
        md_mtime = md_path.stat().st_mtime
        for _kind, filename, _title in ASSEMBLY:
            if filename is None:
                continue
            source = BOOK_DIR / filename
            if source.exists() and source.stat().st_mtime > md_mtime:
                needs_assemble = True
                break
        if not needs_assemble and METADATA_FILE.exists() and METADATA_FILE.stat().st_mtime > md_mtime:
            needs_assemble = True
    if needs_assemble:
        print("Sources newer than assembled markdown — running assemble first.")
        rc = cmd_assemble()
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
    cmd = [
        "pandoc",
        str(md_path),
        "-o", str(pdf_path),
        "--pdf-engine=xelatex",
        "--metadata-file", str(METADATA_FILE),
        # Layout geometry is layout-specific (CLI flag), so it stays outside YAML.
        "-V", f"geometry:{geometry}",
        "-H", str(generated_preamble),
    ]

    print(f"Rendering PDF (layout={layout}, this may take a minute)...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("PDF rendering FAILED. pandoc stderr:\n", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return result.returncode
    if result.stderr.strip():
        print("pandoc warnings:")
        print(result.stderr[:1000])
    print(f"PDF rendered → {pdf_path.relative_to(BOOK_DIR)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Atomic Sanskrit book builder.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "phase",
        choices=["stubs", "assemble", "pdf", "all"],
        nargs="?",
        default="all",
        help="Pipeline phase to run (default: all)",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing stub files")
    parser.add_argument(
        "--layout",
        choices=list(LAYOUTS),
        default="letter",
        help="PDF page layout (default: letter). Only applies to pdf/all phases.",
    )
    args = parser.parse_args()

    if args.phase == "stubs":
        return cmd_stubs(force=args.force)
    if args.phase == "assemble":
        return cmd_assemble()
    if args.phase == "pdf":
        return cmd_pdf(layout=args.layout)
    # all
    if (rc := cmd_stubs(force=args.force)) != 0:
        return rc
    if (rc := cmd_assemble()) != 0:
        return rc
    return cmd_pdf(layout=args.layout)


if __name__ == "__main__":
    sys.exit(main())

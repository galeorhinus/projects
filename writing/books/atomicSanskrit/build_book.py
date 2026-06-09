#!/usr/bin/env python3
"""
build_book.py — Atomic Sanskrit book assembly + PDF pipeline.

Phases (run any one, or `all` for the full pipeline):
  stubs    — create placeholder draft files for missing chapters
  assemble — concatenate all chapter files into build/atomic_sanskrit.md
  pdf      — render the assembled markdown to PDF via pandoc + xelatex
  all      — run stubs → assemble → pdf (default)
  dossier  — build the companion Source & Verification Dossier PDF
             (the full long-form endnotes as a standalone artifact;
             reads as_dossier_front.md and as_dossier.yaml; emits
             build/atomic_sanskrit_dossier.{layout}.pdf)

Usage:
  python3 build_book.py                              # full pipeline (default layout)
  python3 build_book.py stubs                        # just generate missing stubs
  python3 build_book.py assemble                     # just concatenate
  python3 build_book.py pdf                          # just render the PDF
  python3 build_book.py stubs --force                # overwrite existing stub files
  python3 build_book.py pdf --layout book-on-letter  # book-mock layout on letter paper
  python3 build_book.py pdf --layout trade           # true 6×9 trim size
  python3 build_book.py pdf --layout phone           # 3×6 phone-reading trim
  python3 build_book.py pdf --endnotes short         # short-form endnotes (printed-book mode)
  python3 build_book.py pdf --endnotes full          # full-form endnotes (default — dossier-grade)
  python3 build_book.py dossier --layout trade       # companion dossier as standalone PDF

Layouts:
  letter           8.5×11 paper, 1in margins. Manuscript review.
  book-on-letter   8.5×11 paper with a centered ~4.5×7.5 text block — looks
                   like a 6×9 book page printed inside letter margins.
  trade            True 6×9 trim. For print-on-demand uploads.
  phone            3×6 trim with 0.2in margins. Sized for phone-screen reading.

Endnote modes:
  full             Emits the complete long-form body of each entry from
                   as_endnotes.md (default). Dossier-grade content.
  short            Emits only the one-sentence **Short:** field per entry,
                   for the printed-book apparatus. Falls back to full body
                   when the Short field is missing or carries a [TBD: ...]
                   placeholder. Output files are suffixed with .short so the
                   two modes can coexist (e.g., atomic_sanskrit.trade.short.pdf).

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
DOSSIER_METADATA_FILE = BOOK_DIR / "as_dossier.yaml"
DOSSIER_FRONT_FILE = BOOK_DIR / "as_dossier_front.md"
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

# ASSEMBLY data lives in as_book.yaml under the `assembly:` key. Loaded at
# module-import time via parse_assembly_yaml() below. CLAUDE.md names
# as_book.yaml as the single source of truth for document-structure metadata;
# the assembly list belongs there alongside the other structural settings.
# To change reading order, edit as_book.yaml — not this file.
#
# Each entry is a dict:
#   kind      one of {"front", "part", "chapter", "end"}
#   file      manuscript filename (None for "part" entries that emit a
#             \part{} break only; otherwise optional prose after \part{})
#   title     canonical title rendered into the assembled markdown
#   subtitle  optional one-line italic subtitle below \part{} for "part"
#             entries — the courtroom-arc map (locked in
#             working/courtroom_framing/implementation_plan.md). None when
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
    "letter": "margin=1in",
    # ~4.5×7.5 text block centered on 8.5×11 — book-page mock-up on letter paper.
    "book-on-letter": "paperwidth=8.5in,paperheight=11in,textwidth=4.5in,textheight=7.5in,centering",
    # True 6×9 trim with book-style asymmetric margins (inner > outer for binding).
    "trade": "paperwidth=6in,paperheight=9in,inner=0.875in,outer=0.625in,top=0.75in,bottom=0.875in",
    # Narrow 3×6 trim with minimal margins — sized for phone-screen reading.
    # ~2.6×5.6 text block (~81% of page area is text) maximizes readable area.
    "phone": "paperwidth=3.5in,paperheight=7in,margin=0.1in",
}


# Regexes for cleaning chapter files before assembly
DRAFT_NOTES_RE   = re.compile(r"\n(?:---\s*\n+)?##+\s+Draft notes(?:\s*\([^)]*\))?.*\Z", re.DOTALL)
DRAFT_HEADER_RE  = re.compile(r"^\*Draft v.*?\*\n+", re.DOTALL | re.MULTILINE)

# Per-script Unicode ranges for explicit font wrapping. Each entry is
# (font command, regex of script's character range).
# Why wrap: ucharclasses transitions silently fail in many xelatex contexts
# (TOC entries, headings, math-adjacent positions like √मा); the workaround
# is to wrap each script's runs in raw-LaTeX `{\<fontname> …}` so the font
# switch is unconditional inside the wrap group.
SCRIPT_WRAPS: list[tuple[str, re.Pattern]] = [
    # Devanagari block + Vedic Extensions + ZWJ/ZWNJ joiners.
    # Vedic Extensions (U+1CD0–U+1CFF) carries the jihvāmūlīya (᳚) and
    # upadhmānīya (᳛) marks used in the Ayogavāha endnote.
    (r"\devanagarifont",  re.compile(r"[ऀ-ॿ᳀-᳿‌‍]+")),
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

    mode='full'  — return the entire entry body (default; dossier-grade).
    mode='short' — return only the content of the **Short:** field per entry.
                   Falls back to the full body when the Short field is
                   missing or carries a [TBD: ...] placeholder, so the
                   build still produces something useful per-entry even
                   while editorial passes are in flight.
    """
    path = BOOK_DIR / "as_endnotes.md"
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
    """Parse working/as_todo.md Section E and return { stub-name: description }."""
    path = BOOK_DIR / "working" / "as_todo.md"
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
            f"discussion live in the companion* Source & Verification Dossier. "
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
ASSEMBLY = parse_assembly_yaml(METADATA_FILE)


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


def cmd_assemble(endnotes_mode: str = "full") -> int:
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
        if kind == "part":
            # Raw-LaTeX part break (pandoc passes through inside this fence).
            # When a subtitle is present, embed it INSIDE the \part[...]{...}
            # so it appears (a) in the TOC entry — via the optional argument
            # — and (b) on the part-title page — via the mandatory argument's
            # \\[...] line break. \normalfont and \itshape reset bold to
            # medium-italic so the subtitle reads as a subordinate line
            # beneath the bold title.
            if subtitle:
                # The optional arg becomes the TOC entry; the mandatory arg
                # is what the part page displays. The book class wraps the
                # mandatory arg in \huge\bfseries by default.
                toc_text = f"{title} — \\textit{{{subtitle}}}"
                page_text = (
                    f"{title}\\\\[2ex]"
                    f"{{\\Large\\normalfont\\itshape {subtitle}}}"
                )
                chunks.append(
                    f"\n```{{=latex}}\n"
                    f"\\part[{toc_text}]{{{page_text}}}\n"
                    f"```\n\n"
                )
            else:
                chunks.append(f"\n```{{=latex}}\n\\part{{{title}}}\n```\n\n")
            if filename:
                path = BOOK_DIR / filename
                if not path.exists():
                    print(f"  MISSING: {filename}", file=sys.stderr)
                    missing.append(filename)
                    continue
                text = path.read_text()
                text = DRAFT_NOTES_RE.sub("", text).strip()
                text = DRAFT_HEADER_RE.sub("", text.lstrip()).strip()
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
        if filename == "as_endnotes.md":
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


def cmd_pdf(layout: str = "letter", endnotes_mode: str = "full") -> int:
    # The intermediate .md and the output PDF are both suffixed with the
    # endnotes mode (when short) so full and short variants coexist.
    notes_suffix = "" if endnotes_mode == "full" else f".{endnotes_mode}"
    md_path = BUILD_DIR / f"atomic_sanskrit{notes_suffix}.md"
    layout_suffix = "" if layout == "letter" else f".{layout}"
    pdf_path = BUILD_DIR / f"atomic_sanskrit{layout_suffix}{notes_suffix}.pdf"

    # Auto-assemble before rendering if the assembled markdown is missing or
    # any source chapter is newer than the assembled file. Cheap (assembly
    # is just concatenation) and guarantees the PDF reflects current sources.
    needs_assemble = not md_path.exists()
    if md_path.exists():
        md_mtime = md_path.stat().st_mtime
        for entry in ASSEMBLY:
            filename = entry["file"]
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
        rc = cmd_assemble(endnotes_mode=endnotes_mode)
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


def cmd_dossier(layout: str = "letter") -> int:
    """Build the companion Source & Verification Dossier as a standalone PDF.

    Reads three sources:
      - as_dossier_front.md  — front matter prose (preface + navigation)
      - as_endnotes.md       — endnote entries in their topical-cluster order
      - as_dossier.yaml      — dossier-specific pandoc metadata (title, etc.)

    Promotes the entry headings from ### (subsection) to ## (section) so the
    PDF hierarchy under the Endnotes chapter is clean. Writes
    build/atomic_sanskrit_dossier.md and renders the PDF.
    """
    BUILD_DIR.mkdir(exist_ok=True)
    if not DOSSIER_FRONT_FILE.exists():
        print(f"Missing: {DOSSIER_FRONT_FILE.name}", file=sys.stderr)
        return 1
    if not DOSSIER_METADATA_FILE.exists():
        print(f"Missing: {DOSSIER_METADATA_FILE.name}", file=sys.stderr)
        return 1
    endnotes_path = BOOK_DIR / "as_endnotes.md"
    if not endnotes_path.exists():
        print(f"Missing: {endnotes_path.name}", file=sys.stderr)
        return 1

    front = DOSSIER_FRONT_FILE.read_text().rstrip()

    # Read endnotes source as-is, then strip its existing top-line header note
    # (the `# Atomic Sanskrit — Endnotes (Expanded Prose)` heading and the
    # status blockquote that follows it) so the dossier's own front matter
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
        "# Endnotes",
        "",
        entries_body.rstrip(),
        "",
    ])
    # Wrap non-Latin scripts in raw-LaTeX font-switch commands per the same
    # convention cmd_assemble uses.
    assembled = wrap_scripts_for_latex(assembled)

    layout_suffix = "" if layout == "letter" else f".{layout}"
    md_path = BUILD_DIR / "atomic_sanskrit_dossier.md"
    pdf_path = BUILD_DIR / f"atomic_sanskrit_dossier{layout_suffix}.pdf"
    md_path.write_text(assembled)
    word_count = len(assembled.split())
    print(f"Assembled dossier → {md_path.relative_to(BOOK_DIR)} ({word_count:,} words)")

    if not have("pandoc"):
        print("pandoc not found. Install via: brew install pandoc", file=sys.stderr)
        return 1
    if not have("xelatex"):
        print("xelatex not found. Install via: brew install --cask basictex", file=sys.stderr)
        return 1

    # Same Devanagari-preamble template substitution as cmd_pdf, but using
    # the dossier's font name (which currently matches the book's; the
    # template substitution still goes through so the two pipelines are
    # symmetric).
    devanagari_font = read_yaml_value(DOSSIER_METADATA_FILE, "devanagarifont")
    preamble_text = PREAMBLE_TEMPLATE.read_text().replace("__DEVANAGARIFONT__", devanagari_font)
    generated_preamble = BUILD_DIR / "devanagari-preamble.tex"
    generated_preamble.write_text(preamble_text)

    geometry = LAYOUTS[layout]
    cmd = [
        "pandoc",
        str(md_path),
        "-o", str(pdf_path),
        "--pdf-engine=xelatex",
        "--metadata-file", str(DOSSIER_METADATA_FILE),
        "-V", f"geometry:{geometry}",
        "-H", str(generated_preamble),
    ]

    print(f"Rendering dossier PDF (layout={layout}, this may take a minute)...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Dossier PDF rendering FAILED. pandoc stderr:\n", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return result.returncode
    if result.stderr.strip():
        print("pandoc warnings:")
        print(result.stderr[:1000])
    print(f"Dossier PDF rendered → {pdf_path.relative_to(BOOK_DIR)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Atomic Sanskrit book builder.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "phase",
        choices=["stubs", "assemble", "pdf", "all", "dossier"],
        nargs="?",
        default="all",
        help="Pipeline phase to run (default: all). 'dossier' builds the companion "
             "Source & Verification Dossier as a standalone PDF.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing stub files")
    parser.add_argument(
        "--layout",
        choices=list(LAYOUTS),
        default="letter",
        help="PDF page layout (default: letter). Only applies to pdf/all phases.",
    )
    parser.add_argument(
        "--endnotes",
        choices=["full", "short"],
        default="full",
        help="Endnote rendering mode (default: full). 'short' emits the one-sentence "
             "Short field from as_endnotes.md per entry, for the printed-book apparatus; "
             "'full' emits the complete long-form body per entry, for the dossier. "
             "Output filenames are suffixed with .short in short mode so the two "
             "variants coexist.",
    )
    args = parser.parse_args()

    if args.phase == "stubs":
        return cmd_stubs(force=args.force)
    if args.phase == "assemble":
        return cmd_assemble(endnotes_mode=args.endnotes)
    if args.phase == "pdf":
        return cmd_pdf(layout=args.layout, endnotes_mode=args.endnotes)
    if args.phase == "dossier":
        return cmd_dossier(layout=args.layout)
    # all
    if (rc := cmd_stubs(force=args.force)) != 0:
        return rc
    if (rc := cmd_assemble(endnotes_mode=args.endnotes)) != 0:
        return rc
    return cmd_pdf(layout=args.layout, endnotes_mode=args.endnotes)


if __name__ == "__main__":
    sys.exit(main())

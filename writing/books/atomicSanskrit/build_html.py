#!/usr/bin/env python3
"""
build_html.py — Atomic Sanskrit web book builder.

Reads as_book.yaml's `assembly:` block as the canonical chapter sequence,
renders each chapter as a standalone HTML page via pandoc, generates a
contents page, and copies the shared CSS + figures into build/html/.

Output layout (served from /var/www/as/ by Caddy at /as/):

  build/html/
    index.html                       contents page (served at /as/)
    css/book.css
    figures/build/*.svg              (copied from figures/build/)
    preface/index.html               (served at /as/preface/)
    seekers/index.html               (served at /as/seekers/)
    building-dhatuh/index.html       (served at /as/building-dhatuh/)
    endnotes/index.html              (anchors at /as/endnotes/#<stub>)
    ...

URL slug rule:
  filename minus the `as_<zone>_<seq>_` prefix and `.md` suffix, with
  underscores → hyphens. as_endnotes.md (no zone-seq prefix) gets slug
  "endnotes" by stripping the bare `as_` prefix.

Markdown preprocessing per chapter:
  - strip the `*Draft v...*` scaffolding line below the # heading
  - replace `[NOTE: stub-name]` markers with HTML superscript links pointing
    to /as/endnotes/#stub-name
  - rewrite `figures/build/foo.svg` image refs to `/as/figures/build/foo.svg`
    (root-relative under the /as/ mount)

Run with:  python3 build_html.py
"""

import datetime
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Reuse the assembly parser + clean_chapter from build_book.py — it parses
# as_book.yaml's `assembly:` block and strips draft-scaffolding headers.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_book import (  # noqa: E402
    ASSEMBLY,
    METADATA_FILE,
    BOOK_DIR,
    clean_chapter,
    read_yaml_value,
)

HTML_OUT = BOOK_DIR / "build" / "html"
HTML_OUT_BOOK = HTML_OUT / "book"
HTML_OUT_ESSAYS = HTML_OUT / "essays"
HTML_OUT_PRIVATE = HTML_OUT / "private"
HTML_OUT_JACKET = HTML_OUT / "jacket-copy"

TEMPLATE_CHAPTER = BOOK_DIR / "templates" / "html_chapter.html"
TEMPLATE_INDEX = BOOK_DIR / "templates" / "html_index.html"
TEMPLATE_ESSAY = BOOK_DIR / "templates" / "html_essay.html"
TEMPLATE_LANDING = BOOK_DIR / "templates" / "landing.html"
TEMPLATE_404 = BOOK_DIR / "templates" / "error_404.html"

# Single source of truth for the landing page's "About the book" copy.
# render_landing() below converts it to HTML the same way a chapter's
# markdown becomes a page, so a jacket-copy edit + `python3
# build_html.py` + deploy is the whole pipeline, with no separate
# hardcoded copy to keep in sync. Set to the "question-led" variant as
# of 2026-08-14 — swap this path to promote a different variant to
# default; whichever file was previously here should move into
# JACKET_COPY_VARIANTS below so it stays reachable as a reviewer
# alternate rather than disappearing.
#
# Lives in cover/ (top level, alongside the manuscript sources) rather
# than under outreach/: jacket copy is text that ships ON the book, not
# material sent out ABOUT it, and it may later be bundled into the PDF
# by build_book.py. Moved there 2026-08-17.
COVER_DIR = BOOK_DIR / "cover"
JACKET_COPY_SRC = COVER_DIR / "jacket_copy_question_led.md"

# The three alternates to JACKET_COPY_SRC, reviewed 2026-08-12 against the
# version live on the landing page. Each renders to its own gated page
# under /as/jacket-copy/<slug>/ via render_jacket_copy_variant(), behind
# the same oauth2-proxy gate as /as/private/* (see Caddyfile), with
# Hypothesis annotation enabled (same restricted-groups allowlist as the
# book chapters — see templates/html_essay.html) so invited readers can
# comment directly in place. Not linked from site navigation for casual
# visitors — the landing page reveals links to authorized sessions only
# (see the reviewer-links script in templates/landing.html). Add/remove
# entries here to add/retire a variant.
JACKET_COPY_VARIANTS = [
    {"slug": "statement-led", "src": COVER_DIR / "jacket_copy_statement_led.md"},
    {"slug": "revelations", "src": COVER_DIR / "jacket_copy_revelations.md"},
    {"slug": "website-version", "src": COVER_DIR / "website_copy_questions_answers.md"},
]

BOOK_CSS_SRC = BOOK_DIR / "templates" / "book.css"
ESSAYS_CSS_SRC = BOOK_DIR / "templates" / "essays.css"

# Favicons. Live under the public-facing web assets rather than templates/
# because they may be regenerated / iterated on independently of the CSS
# templates. The build copies them to the /as/ URL root so browsers get
# them at /as/favicon.ico and /as/favicon.svg regardless of which page a
# visitor lands on.
FAVICON_SRC_DIR = BOOK_DIR / "web" / "public" / "as"
FAVICON_FILES = ("favicon.ico", "favicon.svg", "ic-calibration-favicon.svg")

# Figures repository. After the 2026-06-07 reorg, figures live in chapter-
# slug subdirectories (figures/<chapter>/<file>.svg) and in figures/_shared/
# (icons/ and toolkits/<x>/output/). The build copies every image file under
# figures/ recursively, preserving the directory structure, into
# build/html/book/figures/. Image-extension filtering keeps Python sources,
# CSV data files, and the migration doc out of the deploy.
FIGURES_SRC = BOOK_DIR / "figures"
FIGURE_EXTS = {".svg", ".png", ".jpg", ".jpeg", ".gif", ".pdf"}

ESSAYS_PUBLIC_SRC = BOOK_DIR / "web" / "public"
ESSAYS_PRIVATE_SRC = BOOK_DIR / "web" / "private"

URL_BASE = "/as/book"   # the book is mounted at https://secondshanti.org/as/book/

# Pattern for the filename prefix `as_<zone>_<seq>_` (regular chapter /
# front / end files) or `as_part_<seq>_` (Part-opener files added in
# 2026-06-07's bbb1821 commit). When matched, strip it and the .md suffix;
# underscores in the remaining slug become hyphens. Both `as_1_01_botanical.md`
# and `as_part_01_wrong_metaphor.md` end up with a clean topic slug
# (`botanical`, `wrong-metaphor`).
SLUG_PREFIX_RE = re.compile(r"^as_(?:\d+_\d+|part_\d+)_")
# Fallback for files like as_endnotes.md that lack the numeric prefix.
SLUG_FALLBACK_PREFIX_RE = re.compile(r"^as_")

# Inline note marker — same shape as build_book.py's NOTE_MARKER_RE.
NOTE_MARKER_RE = re.compile(r"\[NOTE:\s*([a-z0-9_-]+)\s*\]")

# Image path rewriter — change relative `figures/build/...` (or
# `./figures/build/...`) to root-relative `/as/figures/build/...`.
# Matches inside markdown image syntax `![alt](path){...}` and bare paths.
# Markdown image syntax: ![alt](figures/<subdir>/<rest>). Match any subdir
# under figures/ (build/, icons/, mapping_mouth/, ...) so the rewrite picks
# up all of them, not just figures/build/.
IMAGE_REF_RE = re.compile(r"(\]\()(?:\./)?figures/")
# Raw HTML inline images: <img src="figures/<subdir>/<rest>" ...>. The
# chapters use these for inline scaffold icons embedded mid-paragraph and
# in table cells; same rewrite rule applies.
HTML_IMG_REF_RE = re.compile(r'(src=")(?:\./)?figures/')

# Draft-scaffolding line we strip from chapter sources (analogous to
# build_book.py's DRAFT_HEADER_RE but applied after the first heading).
DRAFT_LINE_RE = re.compile(r"^\*Draft v[^\n]*\*\s*\n+", re.MULTILINE)

# Top-level section headings in pandoc's own rendered output — read back
# post-render rather than reimplementing pandoc's auto-identifier slug
# algorithm, so the extracted anchors are guaranteed to match what's
# actually in the page. Feeds both the in-chapter "Contents" disclosure
# and the TOC's per-chapter accordion.
H2_HEADING_RE = re.compile(r'<h2 id="([^"]+)">(.*?)</h2>', re.DOTALL)


def git_metadata() -> dict[str, str]:
    """Capture build provenance for the page footer: most recent git tag,
    short commit SHA, working-tree dirty flag, and the build date."""
    def _run(cmd: list[str]) -> str:
        try:
            r = subprocess.run(cmd, cwd=BOOK_DIR, capture_output=True, text=True, check=False)
            return r.stdout.strip() if r.returncode == 0 else ""
        except FileNotFoundError:
            return ""

    tag = _run(["git", "describe", "--tags", "--abbrev=0"]) or "untagged"
    sha = _run(["git", "rev-parse", "--short", "HEAD"]) or "unknown"
    dirty = bool(_run(["git", "status", "--porcelain"]))
    if dirty:
        sha = f"{sha}-dirty"
    return {
        "git_tag": tag,
        "git_sha": sha,
        "build_date": datetime.date.today().isoformat(),
    }


def slug_for(filename: str) -> str:
    """Derive the URL slug from a manuscript filename.

    Part-opener files get a `part-` prefix on the slug so they don't collide
    with chapters that share the same topic name — e.g.,
    as_part_07_life_after_pie.md (Part VII opener) → `part-life-after-pie`
    coexists with as_1_19_life_after_pie.md (Chapter 19) → `life-after-pie`."""
    is_part = filename.startswith("as_part_")
    if SLUG_PREFIX_RE.match(filename):
        stem = SLUG_PREFIX_RE.sub("", filename)
    else:
        stem = SLUG_FALLBACK_PREFIX_RE.sub("", filename)
    stem = stem.removesuffix(".md")
    slug = stem.replace("_", "-")
    return ("part-" + slug) if is_part else slug


def collect_content_entries() -> list[dict]:
    """Filter the assembly to content-bearing entries.

    Includes every entry with a `file:` field — that means front/chapter/end
    entries, AND `kind: part` entries that carry a Part-opener file (added
    in commit bbb1821). Pure title-only Part dividers (no `file:`) still
    get skipped here; they live only in the TOC's group structure."""
    entries = []
    for entry in ASSEMBLY:
        if not entry.get("file"):
            continue
        e = dict(entry)
        e["slug"] = slug_for(entry["file"])
        e["url"] = f"{URL_BASE}/{e['slug']}/"
        entries.append(e)
    return entries


def preprocess_markdown(text: str, canonical_title: str) -> str:
    """Clean the chapter source for HTML rendering.

    1. Reuse clean_chapter to replace the top-line `# ...` heading with the
       canonical title from as_book.yaml and strip the Draft-notes appendix.
    2. Strip the `*Draft v...*` scaffolding line that sits beneath the
       heading in many chapter files.
    3. Drop the leading `# Title` line entirely — the HTML template emits
       the chapter title via $pagetitle$, so leaving the markdown heading
       in produces a duplicate h1.
    4. Rewrite figure image paths to /as/figures/build/...
    5. Convert [NOTE: stub] markers to HTML superscript links pointing at
       /as/endnotes/#stub.
    """
    text = clean_chapter(text, canonical_title)
    text = DRAFT_LINE_RE.sub("", text, count=1)

    # Drop the leading `# canonical_title` line — the template renders it.
    lines = text.split("\n", 1)
    if lines and lines[0].startswith("# "):
        text = lines[1] if len(lines) > 1 else ""
    text = text.lstrip("\n")

    # Rewrite image paths
    text = IMAGE_REF_RE.sub(lambda m: m.group(1) + f"{URL_BASE}/figures/", text)
    text = HTML_IMG_REF_RE.sub(lambda m: m.group(1) + f"{URL_BASE}/figures/", text)

    # Convert [NOTE: stub] → superscript HTML link
    def note_repl(m: re.Match) -> str:
        stub = m.group(1)
        return f'<sup class="endnote-ref"><a href="{URL_BASE}/endnotes/#{stub}" title="{stub}">note</a></sup>'
    text = NOTE_MARKER_RE.sub(note_repl, text)

    return text


def run_pandoc(md_path: Path, out_path: Path, metadata: dict[str, str]) -> None:
    """Render one markdown file to HTML via pandoc with the chapter template."""
    cmd = [
        "pandoc",
        "--from=markdown+raw_html+pipe_tables+yaml_metadata_block+tex_math_dollars+raw_attribute+bracketed_spans+fenced_divs",
        "--to=html5",
        "--standalone",
        f"--template={TEMPLATE_CHAPTER}",
        f"--output={out_path}",
    ]
    for k, v in metadata.items():
        cmd.append(f"--metadata={k}={v}")
    cmd.append(str(md_path))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  pandoc FAILED on {md_path.name}:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(1)
    if result.stderr.strip():
        # Pandoc emits non-fatal warnings (e.g., duplicate heading IDs) to stderr.
        for line in result.stderr.splitlines()[:5]:
            print(f"    [pandoc] {line}")


def render_chapter(entry: dict, prev: dict | None, next_: dict | None,
                   book_title: str, build_meta: dict[str, str]) -> list[tuple[str, str]]:
    """Render one chapter to build/html/book/<slug>/index.html.

    Returns the chapter's (id, inner_html) section headings — used by
    render_index() to build that chapter's TOC accordion entry. Splices a
    "Contents" dropdown into the sticky sitebar (replacing the
    <!--CHAPTER-TOC-SLOT--> placeholder in html_chapter.html) so a reader
    can jump to any of the chapter's own sections from anywhere on the
    page, not just from the top."""
    src = BOOK_DIR / entry["file"]
    if not src.exists():
        print(f"  MISSING: {entry['file']}", file=sys.stderr)
        return []

    raw = src.read_text()
    processed = preprocess_markdown(raw, entry["title"])

    slug_dir = HTML_OUT_BOOK / entry["slug"]
    slug_dir.mkdir(parents=True, exist_ok=True)
    out_path = slug_dir / "index.html"

    # Write the processed markdown to a temp file pandoc can read.
    tmp_md = HTML_OUT_BOOK / f".tmp_{entry['slug']}.md"
    tmp_md.write_text(processed)

    metadata = {
        "pagetitle": entry["title"],
        "title": entry["title"],
        "booktitle": book_title,
        "site_base": URL_BASE,
        **build_meta,
    }
    if prev:
        metadata["prevurl"] = prev["url"]
        # prevtitle_plain: markdown emphasis stripped, for the sitebar
        # arrow's title=/aria-label= attributes, which can't render markup
        # anyway. The nav cards' visible {{PREVTITLE_HTML}} marker is
        # filled in below, post-render — pandoc's own $var$ template
        # substitution HTML-escapes metadata strings (confirmed: wrapping
        # a title in <em> for a $prevtitle$ placeholder came out as the
        # literal text "&lt;em&gt;"), so injecting real markup has to
        # happen after pandoc has already written its output, the same
        # way the sitebar Contents dropdown is spliced in below.
        metadata["prevtitle_plain"] = _strip_md_emphasis(prev["title"])
    if next_:
        metadata["nexturl"] = next_["url"]
        metadata["nexttitle_plain"] = _strip_md_emphasis(next_["title"])

    run_pandoc(tmp_md, out_path, metadata)
    tmp_md.unlink()

    original = out_path.read_text()
    html_text = original
    if prev:
        html_text = html_text.replace("{{PREVTITLE_HTML}}", _md_inline_to_html(prev["title"]))
    if next_:
        html_text = html_text.replace("{{NEXTTITLE_HTML}}", _md_inline_to_html(next_["title"]))
    headings = H2_HEADING_RE.findall(html_text)
    toc_slot = _build_sitebar_toc_html(headings) if headings else ""
    html_text = html_text.replace("<!--CHAPTER-TOC-SLOT-->", toc_slot, 1)
    if html_text != original:
        out_path.write_text(html_text)

    print(f"  rendered  /book/{entry['slug']}/  ({entry['file']})")
    return headings


def _build_sitebar_toc_html(headings: list[tuple[str, str]]) -> str:
    """"Contents" dropdown spliced into the sticky sitebar in place of the
    <!--CHAPTER-TOC-SLOT--> placeholder. Collapsed by default (native
    <details>, no JS) — persistently reachable while scrolling, unlike a
    one-time block placed after the chapter title."""
    items = "\n".join(
        f'<li><a href="#{hid}">{text}</a></li>' for hid, text in headings
    )
    return (
        '<details class="toc-drop">\n'
        '<summary>Contents</summary>\n'
        f'<ul>\n{items}\n</ul>\n'
        '</details>'
    )


def _md_inline_to_html(s: str) -> str:
    """Convert *italic* / **bold** markdown to HTML — used for metadata
    fields (title-block subtitle/series, chapter-nav prev/next titles)
    that pandoc would otherwise render as literal text via $variable$
    interpolation, since template variable substitution is plain string
    injection, not a markdown pass."""
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s


def _strip_md_emphasis(s: str) -> str:
    """Plain-text version of a title for title=/aria-label= attributes —
    removes markdown emphasis markers without adding HTML, since attribute
    values can't render markup and a literal asterisk would just look like
    a typo in the tooltip."""
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\*(.+?)\*", r"\1", s)
    return s


def render_index(entries: list[dict], book_title: str, subtitle: str,
                 series: str, author: str, build_meta: dict[str, str],
                 chapter_headings: dict[str, list[tuple[str, str]]]) -> None:
    """Generate build/html/index.html — the contents page, grouped by
    the assembly's `part` entries.

    Group ordering:
      Front Matter & Prologue   — all `front` entries (incl. Chapter 0)
      Part I … Part VII         — under each `part` heading
      Epilogue                  — `end` entries from zone 2 (as_2_*)
      Appendices                — `end` entries from zone 3 (as_3_*)
      Back Matter               — `end` entries from zone 0 (as_0_*, e.g.
                                   Acknowledgments, A Note on the Notes)
      Notes                     — as_endnotes.md
    """

    groups: list[dict] = []
    current = {"title": None, "subtitle": None, "entries": []}
    end_groups = {
        "epilogue":   {"title": "Epilogue", "subtitle": None, "entries": []},
        "appendix":   {"title": "Appendices", "subtitle": None, "entries": []},
        # Zone-0 end-matter (Acknowledgments, A Note on the Notes) — as_book.yaml
        # already places these after the appendices in ASSEMBLY order, but their
        # as_0_ filenames don't match the as_2_/as_3_ prefix checks below, so
        # without their own group they fell through to the "append to current"
        # fallback and got attached to whichever Part was still active (Part
        # VII) instead of appearing after the Appendices. Fixed 2026-08-12.
        "backmatter": {"title": "Back Matter", "subtitle": None, "entries": []},
        "notes":      {"title": "Notes", "subtitle": None, "entries": []},
    }

    for entry in ASSEMBLY:
        if not entry.get("file") and entry["kind"] != "part":
            continue
        if entry["kind"] == "part":
            if current["entries"]:
                groups.append(current)
            # Carry the part-opener URL when the entry has a `file:` field
            # (commit bbb1821 added Part-opener .md files). The TOC heading
            # emitter wraps the title in <a href> when this is set.
            part_url = (
                f"{URL_BASE}/{slug_for(entry['file'])}/"
                if entry.get("file") else None
            )
            current = {
                "title": entry["title"],
                "subtitle": entry.get("subtitle"),
                "url": part_url,
                "entries": [],
            }
        elif entry["kind"] == "end":
            fname = entry["file"]
            if fname == "as_endnotes.md":
                end_groups["notes"]["entries"].append(entry)
            elif fname.startswith("as_2_"):
                end_groups["epilogue"]["entries"].append(entry)
            elif fname.startswith("as_3_"):
                end_groups["appendix"]["entries"].append(entry)
            elif fname.startswith("as_0_"):
                end_groups["backmatter"]["entries"].append(entry)
            else:
                # Fallback — append to current group rather than drop.
                current["entries"].append(entry)
        else:
            current["entries"].append(entry)
    if current["entries"]:
        groups.append(current)

    # Append the end-matter groups (in fixed order) after the parts.
    for key in ("epilogue", "appendix", "backmatter", "notes"):
        if end_groups[key]["entries"]:
            groups.append(end_groups[key])

    # If the very first group has no `title` (content before the first
    # `part`), call it "Front Matter".
    if groups and groups[0]["title"] is None:
        groups[0]["title"] = "Front Matter & Prologue"

    # Build the index body as markdown — pandoc will wrap it through the
    # template and convert into proper HTML. The title block is emitted as
    # raw HTML at the top so the subtitle / series markdown formatting is
    # preserved (pandoc would HTML-escape it if passed via --metadata).
    lines: list[str] = []
    lines.append('<header class="title-block">')
    lines.append(f'  <h1 class="book-title">{book_title}</h1>')
    if subtitle:
        lines.append(f'  <p class="book-subtitle">{_md_inline_to_html(subtitle)}</p>')
    if series:
        lines.append(f'  <p class="book-series">{_md_inline_to_html(series)}</p>')
    if author:
        lines.append(f'  <p class="book-author">{author}</p>')
    lines.append('</header>')
    lines.append('<nav class="toc">')
    lines.append('')
    slug_to_url = {e["file"]: f"{URL_BASE}/{slug_for(e['file'])}/" for e in entries}
    for group in groups:
        # Wrap the Part title in a link to its opener page when the group
        # carries one (Part I…VII after commit bbb1821). Plain text for
        # synthetic groups like Front Matter / Epilogue / Appendices / Notes.
        title_md = (
            f"[{group['title']}]({group['url']})"
            if group.get("url") else group["title"]
        )
        if group["subtitle"]:
            lines.append(f"## {title_md} <span class=\"part-subtitle\">— *{group['subtitle']}*</span>")
        else:
            lines.append(f"## {title_md}")
        lines.append("")
        # Raw HTML, not markdown bullets: a chapter with section headings
        # gets a <details> accordion (its own section links jump straight
        # to that chapter's anchors); a chapter with none (short front-
        # matter pages, single-section notes) falls back to a plain link.
        # Titles run through _md_inline_to_html since pandoc won't parse
        # markdown emphasis inside a raw HTML block.
        lines.append('<ul>')
        for e in group["entries"]:
            url = slug_to_url[e["file"]]
            title_html = _md_inline_to_html(e["title"])
            headings = chapter_headings.get(e["file"], [])
            if headings:
                section_items = "\n".join(
                    f'<li><a href="{url}#{hid}">{text}</a></li>'
                    for hid, text in headings
                )
                lines.append(
                    '<li><details class="chapter-acc">\n'
                    f'<summary><a href="{url}">{title_html}</a></summary>\n'
                    f'<ul class="section-list">\n{section_items}\n</ul>\n'
                    '</details></li>'
                )
            else:
                lines.append(f'<li><a href="{url}">{title_html}</a></li>')
        lines.append('</ul>')
        lines.append("")
    lines.append('</nav>')
    # Build-provenance footer mirrors the chapter pages. No leading
    # whitespace inside the block — pandoc would otherwise parse indented
    # content as a code block.
    lines.append('<footer class="site-footer">')
    lines.append('<div class="build-info">')
    lines.append(
        f'Built {build_meta["build_date"]} · '
        f'commit <code>{build_meta["git_sha"]}</code> · '
        f'tag <code>{build_meta["git_tag"]}</code>'
    )
    lines.append('</div>')
    lines.append('</footer>')
    body_md = "\n".join(lines)

    tmp_md = HTML_OUT_BOOK / ".tmp_index.md"
    tmp_md.write_text(body_md)
    out_path = HTML_OUT_BOOK / "index.html"
    cmd = [
        "pandoc",
        "--from=markdown+raw_html",
        "--to=html5",
        "--standalone",
        f"--template={TEMPLATE_INDEX}",
        f"--output={out_path}",
        f"--metadata=booktitle={book_title}",
        f"--metadata=subtitle={_md_inline_to_html(subtitle)}",
        f"--metadata=series={_md_inline_to_html(series)}",
        f"--metadata=author={author}",
        f"--metadata=title={book_title}",
        f"--metadata=site_base={URL_BASE}",
        str(tmp_md),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("  pandoc FAILED on /book/index.html:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(1)
    tmp_md.unlink()
    print("  rendered  /book/  (book contents)")


def copy_static() -> None:
    """Copy book.css and the figures/build/ tree into build/html/book/, and
    essays.css into build/html/essays/ (shared by /as/essays/, /as/private/,
    and the /as/ landing page)."""
    book_css_dst = HTML_OUT_BOOK / "css" / "book.css"
    book_css_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BOOK_CSS_SRC, book_css_dst)
    print(f"  copied    /book/css/book.css")

    essays_css_dst = HTML_OUT_ESSAYS / "style.css"
    essays_css_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ESSAYS_CSS_SRC, essays_css_dst)
    print(f"  copied    /essays/style.css")

    # Favicons at the /as/ URL root — both bare (favicon.ico + favicon.svg)
    # are placed at the site's URL root so they're findable at
    # /as/favicon.ico (referenced by templates) and can be surfaced at the
    # secondshanti.org apex via a Caddy rewrite when desired.
    for fname in FAVICON_FILES:
        src = FAVICON_SRC_DIR / fname
        if src.exists():
            shutil.copy2(src, HTML_OUT / fname)
            print(f"  copied    /{fname}")
        else:
            print(f"  (skipped: {src} not found)")

    # Wipe the figures destination tree, then walk figures/ recursively and
    # copy every image-extension file, preserving relative paths. The
    # extension filter keeps Python sources, CSVs, notes, and the migration
    # markdown out of the deploy.
    fig_root_dst = HTML_OUT_BOOK / "figures"
    if fig_root_dst.exists():
        shutil.rmtree(fig_root_dst)
    fig_root_dst.mkdir(parents=True)
    counts: dict[str, int] = {}
    for f in FIGURES_SRC.rglob("*"):
        if not f.is_file():
            continue
        if f.suffix.lower() not in FIGURE_EXTS:
            continue
        rel = f.relative_to(FIGURES_SRC)
        dst = fig_root_dst / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dst)
        top = rel.parts[0]
        counts[top] = counts.get(top, 0) + 1
    for top in sorted(counts):
        print(f"  copied    /book/figures/{top}/  ({counts[top]} files)")


# ----------------------------------------------------------------------------
# Essay + landing rendering
# ----------------------------------------------------------------------------

# Parse a YAML frontmatter block at the top of an essay markdown file.
# Returns (frontmatter_dict, body_text) — frontmatter is empty when absent.
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n+", re.DOTALL)


def parse_essay_source(path: Path) -> tuple[dict, str]:
    """Read an essay markdown source and split frontmatter from body.

    The frontmatter block (when present) is a minimal `key: value` list
    delimited by `---` lines at the top of the file. The body that follows
    may itself start with an `# H1 Title` line, which the caller strips
    before passing to pandoc (pandoc's --metadata title produces the page
    title; keeping the markdown # heading would yield two h1s)."""
    raw = path.read_text()
    fm: dict = {}
    m = FRONTMATTER_RE.match(raw)
    if m:
        for line in m.group(1).splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            k, _, v = line.partition(":")
            v = v.strip()
            # Strip surrounding quotes if present
            if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
                v = v[1:-1]
            fm[k.strip()] = v
        body = raw[m.end():]
    else:
        body = raw
    return fm, body


def discover_essays(src_dir: Path) -> list[dict]:
    """Scan an essay source directory, parse frontmatter, derive each
    essay's slug (from frontmatter or filename) and title (from frontmatter
    or the first markdown h1). Returns a list of dicts sorted by filename
    for deterministic build order."""
    essays = []
    if not src_dir.exists():
        return essays
    for path in sorted(src_dir.glob("*.md")):
        fm, body = parse_essay_source(path)
        slug = fm.get("slug") or path.stem
        title = fm.get("title")
        if not title:
            for line in body.splitlines():
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
        if not title:
            title = slug.replace("-", " ").title()
        description = fm.get("description", "")
        essays.append({
            "src": path,
            "slug": slug,
            "title": title,
            "description": description,
            "body": body,
        })
    return essays


def render_essay(essay: dict, out_dir: Path, shelf_link: str,
                 shelf_link_label: str, build_meta: dict[str, str]) -> None:
    """Render one essay to <out_dir>/<slug>/index.html via pandoc with the
    shared essay template."""
    slug_dir = out_dir / essay["slug"]
    slug_dir.mkdir(parents=True, exist_ok=True)
    out_path = slug_dir / "index.html"

    # Strip the leading "# Title" line from the body — the template emits
    # the title via $pagetitle$ and we don't want two h1s.
    body = essay["body"]
    lines = body.split("\n", 1)
    if lines and lines[0].startswith("# "):
        body = lines[1] if len(lines) > 1 else ""
    body = body.lstrip("\n")

    tmp_md = out_dir / f".tmp_{essay['slug']}.md"
    tmp_md.write_text(body)

    metadata = {
        "pagetitle": essay["title"],
        "title": essay["title"],
        "shelf_link": shelf_link,
        "shelf_link_label": shelf_link_label,
        **build_meta,
    }
    cmd = [
        "pandoc",
        "--from=markdown+raw_html+pipe_tables+yaml_metadata_block+tex_math_dollars+bracketed_spans",
        "--to=html5",
        "--standalone",
        f"--template={TEMPLATE_ESSAY}",
        f"--output={out_path}",
    ]
    for k, v in metadata.items():
        cmd.append(f"--metadata={k}={v}")
    cmd.append(str(tmp_md))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  pandoc FAILED on essay {essay['slug']}:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(1)
    tmp_md.unlink()
    rel = out_path.relative_to(HTML_OUT)
    print(f"  rendered  /{rel.with_suffix('').parent}/  (essay: {essay['slug']})")


def render_essay_shelf(out_dir: Path, shelf_title: str, intro_md: str,
                       essays: list[dict], shelf_link: str,
                       shelf_link_label: str,
                       build_meta: dict[str, str]) -> None:
    """Render an essay-shelf index page listing the essays under out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append(intro_md.strip())
    lines.append("")
    if essays:
        for e in essays:
            url = f"{shelf_link}{e['slug']}"
            lines.append('<div class="shelf-entry">')
            lines.append(
                f'  <a class="title" href="{url}">{e["title"]}</a>'
            )
            if e["description"]:
                # Description may contain *italic* etc. — convert inline.
                desc = _md_inline_to_html(e["description"])
                lines.append(f'  <div class="description">{desc}</div>')
            lines.append('</div>')
            lines.append('')
    else:
        lines.append('*(No essays yet.)*')

    body_md = "\n".join(lines)
    tmp_md = out_dir / ".tmp_shelf.md"
    tmp_md.write_text(body_md)
    out_path = out_dir / "index.html"

    metadata = {
        "pagetitle": shelf_title,
        "title": shelf_title,
        "shelf_link": shelf_link,
        "shelf_link_label": shelf_link_label,
        **build_meta,
    }
    cmd = [
        "pandoc",
        "--from=markdown+raw_html",
        "--to=html5",
        "--standalone",
        f"--template={TEMPLATE_ESSAY}",
        f"--output={out_path}",
    ]
    for k, v in metadata.items():
        cmd.append(f"--metadata={k}={v}")
    cmd.append(str(tmp_md))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  pandoc FAILED on shelf {shelf_title}:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(1)
    tmp_md.unlink()
    rel = out_path.relative_to(HTML_OUT)
    print(f"  rendered  /{rel.parent}/  (shelf: {shelf_title})")


JACKET_COPY_TEASER_PARAGRAPHS = 2


def render_jacket_copy() -> str:
    """Convert JACKET_COPY_SRC's markdown body to the <p> markup the
    landing page's .jacket div expects. Drops the leading `# ...` title
    line and blank lines; each remaining paragraph gets *italic*/**bold**
    converted via _md_inline_to_html (the same lightweight inline pass
    used elsewhere for metadata strings, not a full pandoc run — the
    source file uses only italics, so this is sufficient).

    The first JACKET_COPY_TEASER_PARAGRAPHS paragraphs (the opening
    question + its direct answer, for the current revelations-style
    source) render as plain always-visible <p> tags; everything after
    that is wrapped in a <details> so a first-time mobile visitor gets a
    short, complete-feeling hook instead of the full ~300-word block —
    landing.html's CSS styles the <summary> as a "Read the rest ▾"
    control matching the site's existing accordion pattern. A source
    short enough to fit within the teaser count alone renders with no
    <details> at all, rather than an empty, pointless toggle."""
    raw = JACKET_COPY_SRC.read_text(encoding="utf-8")
    paragraphs = [
        line.strip() for line in raw.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    teaser = paragraphs[:JACKET_COPY_TEASER_PARAGRAPHS]
    rest = paragraphs[JACKET_COPY_TEASER_PARAGRAPHS:]

    def as_p(p: str) -> str:
        return f"      <p>{_md_inline_to_html(p)}</p>"

    html = "\n".join(as_p(p) for p in teaser)
    if rest:
        rest_html = "\n".join(as_p(p) for p in rest)
        html += (
            "\n      <details class=\"jacket-more\">\n"
            "        <summary>Read the rest</summary>\n"
            f"{rest_html}\n"
            "      </details>"
        )
    return html


def render_landing(build_meta: dict[str, str]) -> None:
    """Write the public landing page at build/html/index.html by reading
    the static templates/landing.html and substituting the build-info and
    jacket-copy placeholders."""
    text = TEMPLATE_LANDING.read_text()
    build_html = (
        f'  <div class="build-info">\n'
        f'    Built {build_meta["build_date"]} · '
        f'commit <code>{build_meta["git_sha"]}</code> · '
        f'tag <code>{build_meta["git_tag"]}</code>\n'
        f'  </div>'
    )
    text = text.replace("<!--BUILD_INFO-->", build_html)
    text = text.replace("<!--JACKET_COPY-->", render_jacket_copy())
    (HTML_OUT / "index.html").write_text(text)
    print("  rendered  /  (landing page)")


def render_jacket_copy_variant(variant: dict, build_meta: dict[str, str]) -> None:
    """Render one JACKET_COPY_VARIANTS entry to
    build/html/jacket-copy/<slug>/index.html via pandoc + the essay
    template, with Hypothesis annotation switched on. Unlike render_essay(),
    the title comes from the source file's own leading `# ...` line (these
    aren't part of the essay-frontmatter system) rather than YAML
    frontmatter."""
    src = variant["src"]
    slug = variant["slug"]
    raw = src.read_text(encoding="utf-8")
    lines = raw.split("\n", 1)
    # Strip markdown emphasis — this becomes a literal <title>/<h1> string
    # via pandoc's --metadata substitution, which does not run a markdown
    # pass over metadata values (same reasoning as _strip_md_emphasis()'s
    # other callers).
    title = _strip_md_emphasis(lines[0][2:].strip()) if lines[0].startswith("# ") else slug
    body = lines[1].lstrip("\n") if len(lines) > 1 else ""

    out_dir = HTML_OUT_JACKET / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    tmp_md = out_dir / ".tmp_variant.md"
    tmp_md.write_text(body)

    metadata = {
        "pagetitle": title,
        "title": title,
        "hypothesis": "true",
        **build_meta,
    }
    cmd = [
        "pandoc",
        "--from=markdown+raw_html+pipe_tables+yaml_metadata_block+tex_math_dollars+bracketed_spans",
        "--to=html5",
        "--standalone",
        "--wrap=none",
        f"--template={TEMPLATE_ESSAY}",
        f"--output={out_path}",
    ]
    for k, v in metadata.items():
        cmd.append(f"--metadata={k}={v}")
    cmd.append(str(tmp_md))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  pandoc FAILED on jacket-copy variant {slug}:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(1)
    tmp_md.unlink()
    print(f"  rendered  /jacket-copy/{slug}/  (unlisted review page)")


def render_404() -> None:
    """Copy the static templates/error_404.html to build/html/404.html.
    No substitution needed — it carries no per-build or per-page data.
    Caddy's handle_errors rewrites 404 responses to /as/404.html, which
    this ends up at once deploy.sh rsyncs build/html/ -> /var/www/as/."""
    shutil.copy2(TEMPLATE_404, HTML_OUT / "404.html")
    print("  rendered  /404.html  (error page)")


def main() -> int:
    if HTML_OUT.exists():
        shutil.rmtree(HTML_OUT)
    HTML_OUT.mkdir(parents=True)
    HTML_OUT_BOOK.mkdir(parents=True)
    HTML_OUT_ESSAYS.mkdir(parents=True)
    HTML_OUT_PRIVATE.mkdir(parents=True)
    HTML_OUT_JACKET.mkdir(parents=True)

    book_title = read_yaml_value(METADATA_FILE, "title")
    subtitle = read_yaml_value(METADATA_FILE, "subtitle")
    series = read_yaml_value(METADATA_FILE, "series")
    author = read_yaml_value(METADATA_FILE, "author")

    entries = collect_content_entries()
    public_essays = discover_essays(ESSAYS_PUBLIC_SRC)
    private_essays = discover_essays(ESSAYS_PRIVATE_SRC)
    build_meta = git_metadata()
    print(f"Build provenance: tag={build_meta['git_tag']} sha={build_meta['git_sha']} "
          f"date={build_meta['build_date']}")
    print(f"Book chapters:    {len(entries)}")
    print(f"Public essays:    {len(public_essays)} ({', '.join(e['slug'] for e in public_essays) or '—'})")
    print(f"Private essays:   {len(private_essays)} ({', '.join(e['slug'] for e in private_essays) or '—'})")
    print()

    # ----- Book -------------------------------------------------------
    print("Rendering book under /book/ ...")
    chapter_headings: dict[str, list[tuple[str, str]]] = {}
    for i, entry in enumerate(entries):
        prev = entries[i - 1] if i > 0 else None
        next_ = entries[i + 1] if i + 1 < len(entries) else None
        chapter_headings[entry["file"]] = render_chapter(entry, prev, next_, book_title, build_meta)
    render_index(entries, book_title, subtitle, series, author, build_meta, chapter_headings)

    # ----- Public essays + shelf -------------------------------------
    if public_essays:
        print("\nRendering public essays under /essays/ ...")
        for essay in public_essays:
            render_essay(essay, HTML_OUT_ESSAYS,
                         shelf_link="/as/essays/",
                         shelf_link_label="← All essays",
                         build_meta=build_meta)
    render_essay_shelf(
        HTML_OUT_ESSAYS,
        shelf_title="Essays — Atomic Sanskrit",
        intro_md=(
            "Short pieces from the forthcoming book *Atomic Sanskrit* by Parag Tope. "
            "Longer, in-progress essays are available by advance-reader access at "
            "[/as/private/](/as/private/). The full book is at [/as/book/](/as/book/)."
        ),
        essays=public_essays,
        shelf_link="/as/essays/",
        shelf_link_label="← All essays",
        build_meta=build_meta,
    )

    # ----- Private essays + shelf ------------------------------------
    if private_essays:
        print("\nRendering private essays under /private/ ...")
        for essay in private_essays:
            render_essay(essay, HTML_OUT_PRIVATE,
                         shelf_link="/as/private/",
                         shelf_link_label="← All advance-reader essays",
                         build_meta=build_meta)
    render_essay_shelf(
        HTML_OUT_PRIVATE,
        shelf_title="Advance-reader essays — Atomic Sanskrit",
        intro_md=(
            "Longer, in-progress essays from the forthcoming book "
            "*Atomic Sanskrit* by Parag Tope. "
            "Public-facing pieces are at [/as/essays/](/as/essays/); "
            "the full book is at [/as/book/](/as/book/)."
        ),
        essays=private_essays,
        shelf_link="/as/private/",
        shelf_link_label="← All advance-reader essays",
        build_meta=build_meta,
    )

    # ----- Landing + static files ------------------------------------
    print()
    render_landing(build_meta)

    # ----- Jacket-copy review variants (unlisted, direct-link only) --
    print("\nRendering jacket-copy review variants under /jacket-copy/ ...")
    for variant in JACKET_COPY_VARIANTS:
        render_jacket_copy_variant(variant, build_meta)

    render_404()
    copy_static()

    print()
    print(f"Done → {HTML_OUT.relative_to(BOOK_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

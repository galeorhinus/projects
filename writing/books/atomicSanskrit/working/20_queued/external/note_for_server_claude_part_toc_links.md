# Note for server-side Claude — Part entries in the TOC need to become clickable links

**Date:** 2026-06-08
**Branch state:** `main` at `fc9b171` (or later)
**Audience:** Whoever maintains the HTML renderer that Caddy serves.

## What the user sees

The TOC page renders Front Matter and Chapters as clickable links, but
**Part headings are plain text** — small-caps `PART I — THE WRONG
METAPHOR  — *The charge.*` with no underline, no `<a>`. The Part-opener
pages exist and render fine if you hit their URLs directly; only the
TOC entry is missing the anchor.

## What changed upstream (recent commits)

Three commits landed that the renderer needs to know about:

| Commit  | Change |
|---------|--------|
| `bbb1821` | New `as_part_01_..07_*.md` files (Part-opener prose). `as_book.yaml`: each `kind: part` entry now carries a `file:` field pointing at its opener. `build_book.py`: assembler loads opener prose and inlines it under the LaTeX `\part{}` directive. |
| `fc9b171` | Each Part-opener file got a `# Part X — Title` h1 + italic subtitle + `---` rule (so standalone HTML renders with a real title). `build_book.py` gained `PART_HEADER_RE` that strips that header before inlining (so the LaTeX `\part{}` title isn't doubled). |

So the manifest now looks like this for Part entries:

```yaml
- kind: part
  file: as_part_01_wrong_metaphor.md   # <-- new
  title: "Part I — The Wrong Metaphor"
  subtitle: The charge.
```

Where `kind: part` previously had no `file:` field (the Part directive
was title-only), it now has one for every Part I–VII.

## The fix

Find the TOC-rendering function and teach it: **when a `kind: part`
entry has a `file:` field, wrap the title in an `<a href>` pointing at
the rendered Part-opener page; when it doesn't (legacy / future
title-only Parts), render the title as plain text (current behavior).**

Pseudocode:

```python
# inside the entry-loop that walks as_book.yaml
if entry["kind"] == "part":
    title = entry["title"]
    subtitle = entry.get("subtitle")
    if entry.get("file"):
        href = url_for_rendered_page(entry["file"])  # same slug rule as chapters
        title_html = f'<a href="{href}">{escape(title)}</a>'
    else:
        title_html = escape(title)
    emit_part_divider(title_html, subtitle)
    continue
```

The chapter case already builds an `<a href>` from the `file:` field —
reuse that same slug rule for Parts. Whatever turns
`as_1_01_botanical.md` into `as_1_01_botanical.html` (or `…/botanical/`,
or whatever the URL scheme is) should turn `as_part_01_wrong_metaphor.md`
into the parallel URL for that Part-opener.

## Where the renderer lives

I don't see an HTML build script in the manuscript repo — the renderer
is server-side only. Likely candidates to grep for, in order:

1. A Python script that reads `as_book.yaml` and writes `index.html` /
   the TOC fragment. Grep: `as_book.yaml`, `kind.*part`, `kind.*chapter`,
   `emit.*toc`, `render.*toc`.
2. A Caddy template (`*.tmpl` / `*.gohtml`) — if Caddy itself is doing
   the templating via `templates` directive in the Caddyfile.
3. A static-site generator config (Hugo, 11ty, Jekyll) that has a
   custom data file loader for `as_book.yaml`.

If the manuscript repo grows an HTML pipeline later, commit it next to
`build_book.py` so it tracks with the manifest. Today the manifest and
the renderer live in separate trees and that's how this got missed.

## Verification

After the patch:

1. Pull `main` (must be at `fc9b171` or later) so the seven
   `as_part_NN_*.md` files exist with their headers.
2. Rerun whatever produces the TOC HTML.
3. Load the TOC page. Each Part header — `PART I — THE WRONG METAPHOR`,
   `PART II — THE SANSKRIT SELF-CONCEPTION`, … through `PART VII — LIFE
   AFTER PIE` — should be a clickable link to its Part-opener page.
4. Click `PART I`. The opened page should show the `# Part I — The
   Wrong Metaphor` h1, the *The charge.* subtitle, the `---` rule, then
   the three paragraphs of opener prose. (The h1 + subtitle + rule
   are intentionally in the .md file — they're what makes the
   standalone HTML page have a title bar. `build_book.py` strips them
   on the PDF path; the HTML renderer should keep them.)
5. Sanity-check that chapter links still work (the chapter case
   shouldn't be touched).

## What NOT to do

- **Don't modify `as_book.yaml`.** The `file:` field is the contract;
  the renderer should consume it, not require the manifest to change.
- **Don't strip the `# Part X — …` h1 from the `.md` files.** That
  header is what makes the standalone Part-opener HTML have a real
  title. The PDF path strips it via `PART_HEADER_RE` in `build_book.py`
  — the HTML path needs to keep it.
- **Don't rebuild the PDFs** as part of this fix. PDF assembly already
  handles Part-openers correctly (see `build_book.py` lines around the
  `part opener` log message). This is an HTML-only issue.
- **Don't add the linking via JavaScript.** Server-side HTML is fine
  and matches the chapter-link pattern.

## If the link target is ambiguous

If the renderer is generating chapter URLs from the `file:` field via a
specific slug rule (e.g., strip `.md`, strip the `as_` prefix, replace
underscores with hyphens, etc.), apply the **same rule** to the Part
`file:` value. Don't invent a new scheme for Parts.

Example mapping (if the rule is "strip `.md`, keep filename as-is"):

| `file:` value | URL |
|---------------|-----|
| `as_1_01_botanical.md` | `as_1_01_botanical.html` |
| `as_part_01_wrong_metaphor.md` | `as_part_01_wrong_metaphor.html` |

If the chapter URL is `botanical/` (stripped prefix), the Part URL
should be `wrong_metaphor/` by the same rule. Match whatever the
chapter rule already does.

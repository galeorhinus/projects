# Atomic Sanskrit: A Reader's Guide

A separate orientation booklet in A5 and A4. This is a review draft. Part I explains the author's argument in accessible English; Part II introduces the chapters and invites further reading. All 101 invitations appear once across the two parts. It is not the planned 20,000-word concise book and does not replace the Source and Reference Companion.

**PDFs rebuilt, 21 September 2026:** both editions include the wording updates, Devanagari accessibility sweep, named actors and mechanisms of control, and the containment/concealment/control introduction. The subtitle pairs सनातन (*Sanātan*) without changing the book's canonical metadata. See the [voice-sweep comparison](voice_sweep_20260921.md). All 28 tests pass, and the page sheets and covers have been visually inspected.

Both editions include the content revision authorized on 20 September and the subsequent source updates. A5 has 70 interior pages at 11 pt; A4 has 44 at 12 pt. Each interior includes one final blank page for duplex printing and has a separate four-face cover. The 47 source markers identify shared sections; each layout controls its own page breaks without changing the prose or invitation placements.

The revision adds explicit explanations of the book's challenge, the fourth-Abrahamic-religion thesis, and institutional custody. It strengthens the PIE and radiance arguments while keeping the inside-out architecture and worked language examples central. See the [change log](content_revision_change_log.md), [exact before-and-after record](content_revision_before_after.md), and [audit and plan](content_revision_plan.md).

Both editions include the sonomer introduction and terms entry, the new hex-node inside-out diagram, and the shared `ic-authority` and `ic-architecture` icons. The inside-out diagram appears on the front cover, interior title page, and "From Sound to Order" page. In A5, that explanation continues on a separately headed page. Both editions use neutral pronouns for generic people where straightforward, while retaining named-person references and grammatical examples.

The subtitle sits directly below *Atomic Sanskrit*, above the smaller *A Reader's Guide* label. It is 17 pt in A5 and 18 pt in A4; the guide label is 14 pt. Subtitle words do not hyphenate. These settings apply to the front cover and interior title page.

## Read or Revise

The guide uses the book's argumentative voice with simpler vocabulary. Name the pyramid, Western philologists, editors, or the responsible institution where they make, teach, or enforce a claim. Do not replace them with impersonal actors such as "the familiar account." Explain the action and its consequence; stronger adjectives and repeated slogans are not substitutes. Preserve numerical scope, source attribution, and the distinction between personal speculation and evidence. Neutral pronouns concern gender, not the book's stance.

- `manuscript/readers_guide.md`: introductory narrative and final terms page. Page markers keep the current storyboard explicit.
- `manuscript/explore_book.md`: chapter-by-chapter exploration, inserted before the terms page.
- `invitations.json`: canonical wording, printed destinations, and manuscript source paths for all 101 invitations. `{{invite:ID}}` markers place each invitation once.
- `readers_guide.yaml`: booklet settings and separate A5/A4 profiles for font size, leading, mirrored margins, expected physical pages, paragraph splits, and sections sharing a page. Title, subtitle, author, and fonts are read from the root `as_book.yaml`; the author biography is read from `cover/_shared/parag_bio.md`.
- `production_record.md`: pass status, thesis map, source anchors, evidence boundaries, and later review needs.
- [curiosity_map.md](curiosity_map.md): original question bank and editorial rationale. The published wording now lives in `invitations.json`; actual placements are in the two manuscripts and `build/a5/qa_report.json` or `build/a4/qa_report.json`.
- `make_figures.py` and `figures/*.svg`: ten canonical booklet diagrams. `two_chains_hex_nodes.from-cd.svg` is the untouched design source for `inside_out.svg`; promotion retains its geometry, uses local STIX/Tiro fonts, and enlarges and darkens IAST labels for print. Other diagrams use shared book icons and scaffold geometry. These do not replace figures in the main book.
- `build_readers_guide.py`: the reversible, isolated page-directed build. It reuses the main build's script-font routing and does not assemble or edit the full manuscript.

## Build

Rebuild PDFs only when the author requests or approves it. After source edits, remind the author that the PDF needs updating or ask whether to render it; do not run the build automatically. See the project-wide PDF Build Approval rule in `CLAUDE.md`.

From the Atomic Sanskrit project root:

```sh
.venv-figures/bin/python -m pip install -r booklet/readers_guide/requirements.txt
.venv-figures/bin/python booklet/readers_guide/build_readers_guide.py --layout all
.venv-figures/bin/python -m unittest discover -s booklet/readers_guide/tests -v
```

System dependencies: Pandoc, XeLaTeX, Inkscape, the installed Tiro Devanagari Sanskrit and DejaVu Sans fonts, and the repository's STIX Two Text files. The Mac Inkscape application path is a fallback when its command is not on `PATH`.

Use `--layout a5` or `--layout a4` to build just one edition; A5 remains the default. Use `--skip-figures` only when no figure or destination URL has changed. Normal builds regenerate SVG sources from the figure script and export outlined, vector PDFs. Edit the script to make durable figure changes. Both profiles use the same outlined figure exports; the build verifies label sizes at each layout's printed width.

After an A4-only rebuild, run `GUIDE_TEST_LAYOUT=a4 .venv-figures/bin/python -m unittest discover -s booklet/readers_guide/tests -v`. This checks the shared sources and A4 outputs without treating the older A5 PDFs as current. The default test command checks both editions and will flag stale reports. Imported `.from-*` design sources are not separately exported or counted as published figures.

## Outputs

Artifacts are in `output/pdf/readers_guide/` at the project root:

| File | Use |
|---|---|
| `atomic_sanskrit_readers_guide.a5.pdf` | 70-page A5 interior, including one final blank page. |
| `atomic_sanskrit_readers_guide.a5.print.pdf` | Identical A5 interior for printing. |
| `atomic_sanskrit_readers_guide.a5.cover.pdf` | Four A5 cover faces: front, inside front, inside back, back. |
| `atomic_sanskrit_readers_guide.a5.complete.pdf` | 74-page A5 reading copy, with covers and bookmarks. |
| `atomic_sanskrit_readers_guide.a4.pdf` | 44-page A4 interior, including one final blank page. |
| `atomic_sanskrit_readers_guide.a4.print.pdf` | Identical A4 interior for printing. |
| `atomic_sanskrit_readers_guide.a4.cover.pdf` | Four A4 cover faces in the same order. |
| `atomic_sanskrit_readers_guide.a4.complete.pdf` | 48-page A4 reading copy, with covers and bookmarks. |

`atomic_sanskrit_readers_guide.cover.pdf` remains an alias of the A5 cover for existing links. New handoffs should use the size-qualified cover filenames.

The `.print.pdf` suffix does not indicate PDF/X certification or an imposed signature. A5 is 148 × 210 mm; A4 is 210 × 297 mm. Files have no bleed or crop marks. Print at actual size, double-sided, flipping on the long edge. Give the printer the matching `.print.pdf` and `.cover.pdf`, with the covers printed on separate stock. Both interiors have even page counts. The complete PDF is convenient for review; do not also append its covers to the separate print files.

Mirrored inner margins reserve 20 mm for A5 binding and 25 mm for A4 binding; outer margins are 12 mm and 25 mm respectively. Have the printer confirm its spiral-punch clearance, paper, cover stock, and color handling before ordering. These files are prepared for a physical proof, not a guarantee of compatibility with an unspecified punch or binding machine.

The shared source and both editions contain 12,095 words. Counts include headings, invitations, and destinations and exclude figure labels and cover copy. Body type is STIX Two Text: 11 pt / 14.4 pt leading in A5, 12 pt / 16 pt in A4. Sanskrit uses Tiro Devanagari Sanskrit. Current source figures have minimum labels of 8.81 pt at the A5 figure width of 116 mm and 12.15 pt at the A4 width of 160 mm. Reflow pages rather than shrinking type or compressing explanations to retain a page count.

## Checks

The build rejects duplicate or missing invitations, missing source paths, the wrong page count or trim size, missing glyph warnings, overfull TeX boxes, text beyond page bounds, live text remaining in outlined figure exports, and figure labels below 8.5 points at final width. Tests also check section destinations, shared hex proportions, generative totals, both layouts, bookmarks, duplex padding, and unplanned continuation pages. Each layout has its own `build/<layout>/qa_report.json`, TeX files, logs, and `qa/` images. The report includes the figure-size manifest and actual bookmark destinations. Older reports directly under `build/` describe superseded renders.

After an approved PDF rebuild, inspect the PNGs for layout changes. Automated tests are not a substitute for checking glyph shaping, collisions inside vector diagrams, paragraph flow, and page balance. Recheck the chapter references and generated totals when the full book changes.

Author review and physical A5/A4 proofs remain open. This build does not deploy the PDFs to the website or send them to a printer.

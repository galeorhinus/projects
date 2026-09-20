# Atomic Sanskrit: A Reader's Guide

A separate A5 orientation booklet, last rendered with 44 interior pages plus four cover faces. This is a review draft. Part I explains the author's argument in accessible English; Part II introduces the chapters and invites further reading. All 101 invitations appear once across the two parts. It is not the planned 20,000-word concise book and does not replace the Source and Reference Companion.

The prose was expanded after that render on 20 September 2026. The Markdown and invitation bank are current; the PDFs and generated QA report do not yet include this expansion. The next render requires author approval and a new pagination check. The 44 source page markers are the previous storyboard, not a verified page count for the expanded prose.

## Read or Revise

- `manuscript/readers_guide.md`: introductory narrative and final terms page. Page markers keep the current storyboard explicit.
- `manuscript/explore_book.md`: chapter-by-chapter exploration, inserted before the terms page.
- `invitations.json`: canonical wording, printed destinations, and manuscript source paths for all 101 invitations. `{{invite:ID}}` markers place each invitation once.
- `readers_guide.yaml`: booklet settings. Title, subtitle, author, and fonts are read from the root `as_book.yaml`; the author biography is read from `cover/_shared/parag_bio.md`.
- `production_record.md`: pass status, thesis map, source anchors, evidence boundaries, and later review needs.
- [curiosity_map.md](curiosity_map.md): original question bank and editorial rationale. The published wording now lives in `invitations.json`; actual placements are in the two manuscripts and `build/qa_report.json`.
- `make_figures.py` and `figures/*.svg`: ten booklet-specific diagrams using shared book icons and scaffold geometry. These do not replace figures in the main book.
- `build_readers_guide.py`: the reversible, isolated page-directed build. It reuses the main build's script-font routing and does not assemble or edit the full manuscript.

## Build

Rebuild PDFs only when the author requests or approves it. After source edits, remind the author that the PDF needs updating or ask whether to render it; do not run the build automatically. See the project-wide PDF Build Approval rule in `CLAUDE.md`.

From the Atomic Sanskrit project root:

```sh
.venv-figures/bin/python -m pip install -r booklet/readers_guide/requirements.txt
.venv-figures/bin/python booklet/readers_guide/build_readers_guide.py
.venv-figures/bin/python -m unittest discover -s booklet/readers_guide/tests -v
```

System dependencies: Pandoc, XeLaTeX, Inkscape, the installed Tiro Devanagari Sanskrit and DejaVu Sans fonts, and the repository's STIX Two Text files. The Mac Inkscape application path is a fallback when its command is not on `PATH`.

Use `--skip-figures` only when no figure or destination URL has changed. Normal builds regenerate SVG sources from the figure script and export outlined, vector PDFs. Edit the script to make durable figure changes.

## Outputs

The last-rendered artifacts are in `output/pdf/readers_guide/` at the project root:

| File | Use |
|---|---|
| `atomic_sanskrit_readers_guide.a5.pdf` | 44-page numbered interior. |
| `atomic_sanskrit_readers_guide.a5.print.pdf` | The same interior in normal reading order, for the printer to impose. |
| `atomic_sanskrit_readers_guide.cover.pdf` | Four A5 cover faces: front, inside front, inside back, back. |
| `atomic_sanskrit_readers_guide.a5.complete.pdf` | 48-page reading copy: covers surrounding the interior, with PDF bookmarks. |

The `.print.pdf` suffix does not indicate PDF/X certification or an imposed signature. Files are 148 × 210 mm, without bleed or crop marks; all artwork stays within the margins. Have the printer confirm binding, color handling, and imposition. Physical print testing has not been performed.

The last-rendered interior contains 8,427 words. The expanded source contains 9,481 words, an increase of 1,054. Both counts include headings, invitations, and destinations and exclude figure labels and cover copy. The configured body type remains STIX Two Text 11 pt with 14.4 pt leading; Sanskrit uses Tiro Devanagari Sanskrit. Figure labels in the last render are at least 9.29 pt at the printed width. Reflow the pages rather than shrinking type or compressing the explanations to retain the previous page count.

## Checks

The build rejects duplicate or missing invitations, missing source paths, the wrong page count or trim size, missing glyph warnings, overfull TeX boxes, text beyond page bounds, live text remaining in outlined figure exports, and figure labels below 8.5 points at final width. Fourteen tests also check section destinations, shared hex proportions, generative totals, bookmarks, and output metadata. The build writes `build/qa_report.json`, a figure manifest, individual page PNGs, and contact sheets under `build/qa/`.

After an approved PDF rebuild, inspect the PNGs for layout changes. Automated tests are not a substitute for checking glyph shaping, collisions inside vector diagrams, paragraph flow, and page balance. Recheck the chapter references and generated totals when the full book changes.

Author review and a physical A5 proof remain open. Nothing here has been deployed to the website or sent to a printer.

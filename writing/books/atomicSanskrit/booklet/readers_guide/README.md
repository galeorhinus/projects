# Atomic Sanskrit: A Reader's Guide

A separate 42-page A5 orientation booklet, plus four cover faces. This is a review draft. Part I explains the author's argument in accessible English; Part II introduces the chapters and invites further reading. All 101 invitations appear once across the two parts. It is not the planned 20,000-word concise book and does not replace the Source and Reference Companion.

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

From the Atomic Sanskrit project root:

```sh
.venv-figures/bin/python -m pip install -r booklet/readers_guide/requirements.txt
.venv-figures/bin/python booklet/readers_guide/build_readers_guide.py
.venv-figures/bin/python -m unittest discover -s booklet/readers_guide/tests -v
```

System dependencies: Pandoc, XeLaTeX, Inkscape, the installed Tiro Devanagari Sanskrit and DejaVu Sans fonts, and the repository's STIX Two Text files. The Mac Inkscape application path is a fallback when its command is not on `PATH`.

Use `--skip-figures` only when no figure or destination URL has changed. Normal builds regenerate SVG sources from the figure script and export outlined, vector PDFs. Edit the script to make durable figure changes.

## Outputs

Final artifacts are in `output/pdf/readers_guide/` at the project root:

| File | Use |
|---|---|
| `atomic_sanskrit_readers_guide.a5.pdf` | 42-page numbered interior. |
| `atomic_sanskrit_readers_guide.a5.print.pdf` | The same interior in normal reading order, for the printer to impose. |
| `atomic_sanskrit_readers_guide.cover.pdf` | Four A5 cover faces: front, inside front, inside back, back. |
| `atomic_sanskrit_readers_guide.a5.complete.pdf` | 46-page reading copy: covers surrounding the interior, with PDF bookmarks. |

The `.print.pdf` suffix does not indicate PDF/X certification or an imposed signature. Files are 148 × 210 mm, without bleed or crop marks; all artwork stays within the margins. Have the printer confirm binding, color handling, and imposition. Physical print testing has not been performed.

The interior contains 8,367 words including headings, invitations, and destinations. Figure labels and cover copy are excluded. Body type remains STIX Two Text 11 pt with 14.4 pt leading; Sanskrit uses Tiro Devanagari Sanskrit. Figure labels are at least 9.29 pt at the printed width.

## Checks

The build rejects duplicate or missing invitations, missing source paths, the wrong page count or trim size, missing glyph warnings, overfull TeX boxes, text beyond page bounds, live text remaining in outlined figure exports, and figure labels below 8.5 points at final width. Fourteen tests also check section destinations, shared hex proportions, generative totals, bookmarks, and output metadata. The build writes `build/qa_report.json`, a figure manifest, individual page PNGs, and contact sheets under `build/qa/`.

Inspect the PNGs after every layout change. Automated tests are not a substitute for checking glyph shaping, collisions inside vector diagrams, paragraph flow, and page balance. Recheck the chapter references and generated totals when the full book changes.

Author review and a physical A5 proof remain open. Nothing here has been deployed to the website or sent to a printer.

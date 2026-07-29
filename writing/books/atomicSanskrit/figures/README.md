# Atomic Sanskrit — Figure Pipeline

Every figure for the book lives under this directory.  This README is the
**front door** — it tells you the layout, the lifecycle, and where to look
for the deeper convention doc.

**If you're Codex (or any new collaborator) reading this first time:**
read this whole file, then read [`_shared/README.md`](_shared/README.md)
for the lineage-naming convention in full detail.  Together they're under
400 lines.

---

## Layout

```
figures/
├── README.md                        ← this file
├── _shared/                         ← cross-chapter resources
│   ├── README.md                    ← FULL CONVENTION DOC (read after this one)
│   ├── lineage.py                   ← lineage helper (promote / list / verify)
│   ├── style.py                     ← typography + matplotlib savefig() helper
│   ├── icons/                       ← scaffold-shape SVG icons
│   ├── toolkits/                    ← multi-chapter importable Python modules
│   │   └── vocal_tract/             ← geometry, scatter, overlay renderers + configs + output
│   └── design_system/               ← Claude Design house style + CSS tokens
│
└── <chapter_slug>/                  ← per-chapter figure folders
    ├── <fig>.py                     ← Python source (when applicable)
    ├── <fig>.from-py.svg            ← stage variant: Python's raw output
    ├── <fig>.from-py-cd.svg         ← stage variant: → Claude Design
    ├── <fig>.from-hand.svg          ← stage variant: hand-drawn
    ├── <fig>.svg                    ← CANONICAL — what the manuscript references
    ├── briefs/                      ← optional: design briefs + reference imagery
    └── design_iterations/           ← optional: numbered draft snapshots
```

Chapter folders currently in the tree: `about_series`, `adivadya` (Ch 7),
`apabhramsa` (Ch 5), `audiography` (App Part 3), `building_dhatuh` (Ch 10),
`building_kriya` (Ch 11), `building_vakya` (Ch 12), `fourth_abrahamic`
(Ch 3), `ganah` (Ch 11), `mapping_mouth` (Ch 8), `pie_in_sky` (Ch 19),
`preface_modes` (Preface), `siddha_grammar` (Ch 4), `strategic` (Ch 2).

There is **no `figures/build/`** directory.  Outputs live in the chapter
folder beside their source.

---

## The naming convention — `.from-<chain>.svg`

Each figure has a stable `<base>` name.  Stage variants are tracked by a
`.from-<chain>` suffix; the canonical is the bare `.svg`.

| File | Role |
|---|---|
| `<base>.py` | Python source (if Python-generated) |
| `<base>.from-py.svg` | Python's raw output |
| `<base>.from-py-cd.svg` | Python's output → Claude Design |
| `<base>.from-py-cd-edit.svg` | Python → CD → manual vector-tool edit |
| `<base>.from-hand.svg` | Hand-drawn from scratch (no Python) |
| `<base>.from-hand-cd.svg` | Hand-drawn → Claude Design |
| `<base>.svg` | **CANONICAL** — copy of whichever stage is shipping; manuscript references this |

**Stage tokens:** `py` (Python), `cd` (Claude Design), `edit` (manual edit), `hand` (hand-drawn).
Chain reads left to right.

Full details + rationale: [`_shared/README.md`](_shared/README.md).

---

## Lifecycle — what to do, when

### A: Python-generated figure (e.g., `figures/adivadya/hotzones_panels.svg`)

```bash
# 1. Run the script.  It writes <base>.from-py.svg in the chapter folder.
python3 figures/adivadya/hotzones_panels.py

# 2. Promote the snapshot to canonical.  This injects the lineage XML
#    comment and writes <base>.svg.
cd figures
python3 -m _shared.lineage promote adivadya/hotzones_panels.from-py.svg
```

Iterate the script and repeat as needed.  Each promote overwrites the
canonical and bumps its `updated:` date.

### B: Send Python output to Claude Design

```bash
# 1. Upload figures/adivadya/hotzones_panels.from-py.svg to Claude Design.
# 2. Save the returned SVG as figures/adivadya/hotzones_panels.from-py-cd.svg
#    in the SAME chapter folder.
# 3. Promote it to canonical.
cd figures
python3 -m _shared.lineage promote adivadya/hotzones_panels.from-py-cd.svg
```

Now the canonical's lineage reads `py → cd`.  The Python stage variant
is **still kept** — you can always fork back to it later.

### C: Hand-drawn figure (no Python at all)

```bash
# 1. Draw in Illustrator / Inkscape, export as
#    figures/<chapter>/<base>.from-hand.svg
# 2. Promote.
cd figures
python3 -m _shared.lineage promote <chapter>/<base>.from-hand.svg
```

Lineage: `hand`.

### D: Manual edit after Claude Design

```bash
# 1. Open figures/<chapter>/<base>.from-py-cd.svg in a vector tool.
# 2. Save the edited version as figures/<chapter>/<base>.from-py-cd-edit.svg
# 3. Promote.
cd figures
python3 -m _shared.lineage promote <chapter>/<base>.from-py-cd-edit.svg
```

Lineage: `py → cd → edit`.

---

## The lineage helper

```bash
cd figures   # always run from the figures/ directory

# Inject the lineage comment + write canonical
python3 -m _shared.lineage promote <chapter>/<base>.from-<chain>.svg

# Print a table of every canonical in a chapter folder with its lineage
python3 -m _shared.lineage list <chapter>/

# Confirm a canonical's content still matches the recorded canonical-source
python3 -m _shared.lineage verify <chapter>/<base>.svg
```

`promote` is the only command that writes anything.  `list` and `verify`
are read-only.  Run `verify` before a build if you're paranoid about
hand-edits sneaking into a canonical.

---

## Writing a new Python figure script

Two patterns:

### Direct SVG generation (stdlib only — preferred for new work)

```python
#!/usr/bin/env python3
"""Figure description."""
from pathlib import Path

def build_svg() -> str:
    return "<?xml version='1.0'?><svg …></svg>"

def main() -> int:
    svg = build_svg()
    out = Path(__file__).resolve().parent / "<fig>.from-py.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"Wrote {out} ({len(svg)} bytes)")
    return 0

if __name__ == "__main__":
    import sys; sys.exit(main())
```

### Matplotlib-based (uses `_shared.style.savefig`)

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _shared.style import setup, savefig

fig, ax = setup()
# ... matplotlib drawing on `ax` ...

# Write to <name>.from-py.{svg,pdf} in this script's folder
savefig("<name>", dir=Path(__file__).resolve().parent)
```

After running, promote the result.

---

## Importing the shared toolkits

```python
# style helpers
from _shared.style import setup, savefig, FILL, ACCENT

# scaffold-shape SVG icons live at _shared/icons/

# vocal-tract toolkit
from _shared.toolkits.vocal_tract.schematics import point_at, build_ribbon_path_d
from _shared.toolkits.vocal_tract import CONFIGS_DIR    # holds 40 scatter_<lang>.json
```

All chapter scripts add `figures/` to `sys.path` before these imports
(`sys.path.insert(0, str(Path(__file__).resolve().parent.parent))`).

---

## Embedding figures in the manuscript

Chapter markdown references the canonical (no `.from-*` suffix):

```markdown
![Figure 7.2 — Language Hotzones Along the Vocal Tract.](figures/adivadya/hotzones_panels.svg){#fig:adivadya-language-hotzones width=90%}
```

`build_book.py` (via pandoc + xelatex) consumes the SVG directly.  `librsvg`
handles SVG → PDF conversion for LaTeX embedding.

---

## For Codex (and any AI collaborator)

Operating rules when you touch this directory:

1. **Never write to `figures/build/`.**  It doesn't exist anymore.  All
   outputs land in chapter folders.
2. **Stage variants are sacred.**  When advancing a stage (e.g. CD →
   manual edit), create a NEW `from-*` variant with the longer chain.
   Don't overwrite an existing stage's snapshot.
3. **Canonicals are not hand-edited.**  They're always a promote target.
   If you find yourself wanting to edit `<base>.svg`, edit the source
   `from-*` variant and re-promote.
4. **Filenames inside a chapter folder drop the chapter prefix.**
   Inside `figures/adivadya/`, the file is `hotzones_panels.py`, not
   `ch07_adivadya_hotzones_panels.py`.  The folder gives the context.
5. **Cross-chapter shared assets (icons, toolkit modules, design tokens,
   shared overlay/scatter outputs) live under `_shared/`.**  When in
   doubt about whether something belongs in a chapter folder or
   `_shared/`, ask: *if this chapter were deleted tomorrow, would the
   thing also go?*  If yes, chapter folder.  If no, `_shared/`.
6. **`from-*` token vocabulary is fixed.**  Use only `py`, `cd`, `edit`,
   `hand`.  Don't invent new tokens.  If the situation needs one,
   propose it in `_shared/README.md` first.

If you're about to do something the convention doesn't cover, read
`_shared/README.md` first.  If that doesn't answer it, ask the user
before improvising.

---

## Migration notes (2026-06-07)

The structure above replaces a flat `figures/build/<chapter>_<fig>.svg`
layout.  Every manuscript markdown reference has been swept; the old
build directory is gone.  Migration history: `git log --oneline figures/`
shows the 25-commit Phases 1–Final sequence.

If you're operating a Caddy server (or any other path-aware tool) that
was serving the old layout, see `_shared/CADDY_PATH_MIGRATION.md` for the
full path-mapping table.

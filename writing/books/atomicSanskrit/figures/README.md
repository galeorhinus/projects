# Atomic Sanskrit — Figure Pipeline

Programmatic figures for the book. Python + matplotlib generates vector
PDF + SVG outputs that the LaTeX build embeds via `\includegraphics{}`.

## Structure

```
figures/
├── README.md              ← this file
├── style.py               ← shared typography, palette, output paths
├── building_dhatuh/                  ← per-chapter figure scripts
│   └── fig_particle_count.py
├── ch12/                  ← (planned)
└── build/                 ← generated PDF + SVG outputs (commit-tracked)
    └── building_dhatuh_particle_count.pdf
    └── building_dhatuh_particle_count.svg
```

Each chapter's figures sit in `figures/ch<N>/` as standalone Python scripts.
Each script imports `style.setup()` for matplotlib configuration and
`style.savefig(name)` to write a paired PDF (for the build) + SVG (for
manual editing in Inkscape / Illustrator if needed).

## Running a figure script

The book uses matplotlib via Homebrew's `python-matplotlib` formula, which
bundles its own Python under `libexec/`. Invoke the bundled Python directly:

```bash
/usr/local/Cellar/python-matplotlib/*/libexec/bin/python3 figures/building_dhatuh/fig_particle_count.py
```

Or, more conveniently, create a shell alias:

```bash
alias bookpy='/usr/local/Cellar/python-matplotlib/*/libexec/bin/python3'
bookpy figures/building_dhatuh/fig_particle_count.py
```

The script writes `figures/build/<name>.pdf` and `figures/build/<name>.svg`.

## Embedding in the manuscript

In the chapter markdown, replace the figure placeholder with a standard
markdown image link pointing at the build **SVG** (not PDF):

```markdown
![Particle-count distribution across the 2,168 *dhātavaḥ*.](figures/build/building_dhatuh_particle_count.svg){#fig:building-dhatuh-particle-count width=80%}
```

Why SVG and not PDF:

- **IDE markdown preview** renders SVG natively. PDFs require external
  conversion (pdf2svg or similar) and many previewers fail silently.
- **LaTeX build** handles SVG via `rsvg-convert` (already installed
  via the `librsvg` brew formula); pandoc invokes it transparently to
  convert SVG → PDF for xelatex embedding.

The PDF sidecar in `figures/build/` is kept for manual sharing or
pre-press handoff to designers using InDesign / Affinity, but the
markdown should point at the SVG.

## Fonts

`style.py` resolves a font fallback chain:

- **Latin**: Charter (matches book body text) → Bitstream Charter → Charis SIL → DejaVu Serif.
- **Devanagari**: Adobe Devanagari (matches book) → Noto Sans Devanagari → Mangal → Kohinoor Devanagari.

If neither preferred font is installed, matplotlib falls back to its
defaults and emits a warning. To match the book exactly, install Adobe
Devanagari (via Adobe Fonts) and Charter.

## Palette

Print-monochrome by default: `FILL` (dark gray) for emphasis,
`ACCENT` (lighter gray) for non-emphasis. Adjust `style.py` if the
publisher allows a color accent.

## Adding a new figure

1. Create `figures/ch<N>/fig_<name>.py` modeled on
   `figures/building_dhatuh/fig_particle_count.py`.
2. Import `setup, savefig` from `style`.
3. Define data inline (or load from `analysis/<bundle>/derived/...`).
4. Use `setup()` to get a configured `(fig, ax)`.
5. Use `savefig("ch<N>_<name>")` to write PDF + SVG outputs.
6. Reference the PDF in the chapter markdown as shown above.

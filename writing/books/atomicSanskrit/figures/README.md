# Atomic Sanskrit — Figure Pipeline

Programmatic figures for the book. Python + matplotlib generates vector
PDF + SVG outputs that the LaTeX build embeds via `\includegraphics{}`.

## Structure

```
figures/
├── README.md              ← this file
├── style.py               ← shared typography, palette, output paths
├── ch11/                  ← per-chapter figure scripts
│   └── fig_particle_count.py
├── ch12/                  ← (planned)
└── build/                 ← generated PDF + SVG outputs (commit-tracked)
    └── ch11_particle_count.pdf
    └── ch11_particle_count.svg
```

Each chapter's figures sit in `figures/ch<N>/` as standalone Python scripts.
Each script imports `style.setup()` for matplotlib configuration and
`style.savefig(name)` to write a paired PDF (for the build) + SVG (for
manual editing in Inkscape / Illustrator if needed).

## Running a figure script

The book uses matplotlib via Homebrew's `python-matplotlib` formula, which
bundles its own Python under `libexec/`. Invoke the bundled Python directly:

```bash
/usr/local/Cellar/python-matplotlib/*/libexec/bin/python3 figures/ch11/fig_particle_count.py
```

Or, more conveniently, create a shell alias:

```bash
alias bookpy='/usr/local/Cellar/python-matplotlib/*/libexec/bin/python3'
bookpy figures/ch11/fig_particle_count.py
```

The script writes `figures/build/<name>.pdf` and `figures/build/<name>.svg`.

## Embedding in the manuscript

In the chapter markdown, replace the figure placeholder with a standard
markdown image link pointing at the build PDF:

```markdown
![Particle-count distribution across the 2,168 *dhātavaḥ*.](figures/build/ch11_particle_count.pdf){#fig:ch11-particle-count width=100%}
```

Pandoc converts this to `\includegraphics{...}` at PDF build time. The
figure is vector and scales cleanly to any trim size.

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
   `figures/ch11/fig_particle_count.py`.
2. Import `setup, savefig` from `style`.
3. Define data inline (or load from `analysis/<bundle>/derived/...`).
4. Use `setup()` to get a configured `(fig, ax)`.
5. Use `savefig("ch<N>_<name>")` to write PDF + SVG outputs.
6. Reference the PDF in the chapter markdown as shown above.

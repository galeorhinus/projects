"""Shared figure-rendering style for Atomic Sanskrit.

Centralizes:
- Devanagari + Latin font resolution (matches the book's xelatex setup
  when those fonts are available locally; falls back gracefully).
- Print-monochrome palette (the book is black-and-white).
- Default figure size for the trade 6x9 book layout.
- Output paths under figures/_shared/build/ (or chapter folders post-migration).

Usage:
    from _shared.style import setup, savefig
    fig, ax = setup()
    # ... matplotlib drawing on `ax` ...
    savefig("ch11_particle_count")

Each figure script lives at figures/<chapter>/<name>.py and adds
figures/ to sys.path so the `_shared` package is importable from the subdir.
"""

from pathlib import Path
import warnings

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager

# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = Path(__file__).resolve().parent
BUILD_DIR = FIGURES_DIR / "build"

# --- Fonts ---
# Match as_book.yaml when available: mainfont=Charter, devanagarifont=Adobe
# Devanagari. Fall back to Noto / DejaVu when the book's chosen fonts aren't
# installed on the machine running the script.
LATIN_FONTS = ["Charter", "Bitstream Charter", "Charis SIL", "DejaVu Serif"]
DEVANAGARI_FONTS = ["Adobe Devanagari", "Noto Sans Devanagari", "Mangal", "Kohinoor Devanagari"]

# --- Palette (print-monochrome) ---
FILL = "#222222"       # dark fill (modal / emphasis)
ACCENT = "#888888"     # lighter fill (non-modal bars)
EDGE = "#000000"       # axis lines + bar edges
GRID = "#cccccc"       # axis grid

# --- Default figure size (inches) ---
# Trade book trim is 6x9; the text block sits at ~4.5 inches wide. Default
# figure width matches the text block so figures fill the column cleanly.
DEFAULT_FIGSIZE = (4.5, 2.8)


def _resolve_font(candidates):
    """Return the first installed font name from candidates, or None."""
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in installed:
            return name
    return None


def setup(figsize=None):
    """Configure matplotlib for a book-style figure; return (fig, ax)."""
    latin = _resolve_font(LATIN_FONTS)
    devanagari = _resolve_font(DEVANAGARI_FONTS)

    if latin is None:
        warnings.warn(
            f"No Latin font from {LATIN_FONTS} installed; matplotlib default in use."
        )
    if devanagari is None:
        warnings.warn(
            f"No Devanagari font from {DEVANAGARI_FONTS} installed; Devanagari "
            "glyphs may render as boxes. Install Noto Sans Devanagari "
            "(`brew install --cask font-noto-sans-devanagari` on macOS) or your "
            "preferred Devanagari font."
        )

    family_chain = [f for f in (latin, devanagari) if f]
    if family_chain:
        matplotlib.rcParams["font.family"] = family_chain

    matplotlib.rcParams.update({
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "axes.edgecolor": EDGE,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "grid.color": GRID,
        "grid.linewidth": 0.4,
        "legend.frameon": False,
    })

    fig, ax = plt.subplots(figsize=figsize or DEFAULT_FIGSIZE)
    return fig, ax


def savefig(name, fig=None, *, dir=None):
    """Write current (or given) figure as both PDF and SVG.

    Two modes:

    - LEGACY (default): writes to figures/build/<name>.{svg,pdf}.
      Kept for chapter scripts not yet migrated to the chapter-folder
      layout.

    - CHAPTER LAYOUT (`dir` provided): writes to <dir>/<name>.from-py.{svg,pdf}.
      This is the canonical-source snapshot per the convention; run
      `python3 -m _shared.lineage promote <dir>/<name>.from-py.svg`
      to produce the manuscript-referenced `<dir>/<name>.svg`.

    Args:
        name: file basename without extension.  Examples:
            "ch11_particle_count"          (legacy mode)
            "particle_count"               (chapter mode; prefix dropped)
        fig: optional matplotlib Figure (defaults to plt.gcf()).
        dir: optional chapter folder.  When set, switches to chapter
             mode and appends ".from-py" to the basename.
    """
    fig = fig or plt.gcf()
    if dir is None:
        out_dir = BUILD_DIR
        stem = name
    else:
        out_dir = Path(dir)
        stem = f"{name}.from-py"
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / f"{stem}.pdf"
    svg_path = out_dir / f"{stem}.svg"
    fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.05)
    fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.05)
    print(f"Wrote {pdf_path.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {svg_path.relative_to(PROJECT_ROOT)}")
    return pdf_path, svg_path

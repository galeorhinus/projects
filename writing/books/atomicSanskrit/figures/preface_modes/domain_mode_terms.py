"""Preface figures for Sanskrit domain/mode terminology.

Generates two SVGs directly:

  1. preface_domains_modes_matrix.svg
     The Indic two-axis vocabulary: vaidika/laukika as domains,
     chandas/bhasha as modes.

  2. preface_orthodoxy_flattening.svg
     The orthodoxy's one-axis flattening: Vedic -> Classical -> drift.

Run:
    python3 figures/preface_modes/fig_domain_mode_terms.py
"""

from pathlib import Path
from xml.sax.saxutils import escape


FONT = "Charter, Bitstream Charter, DejaVu Serif, Noto Sans Devanagari, serif"
OUT_DIR = Path(__file__).resolve().parent

INK = "#111111"
MUTED = "#5f6368"
GRID = "#C9CDD2"
BLUE = "#1F4E79"
GREEN = "#2D6A4F"
RED = "#822529"
GOLD = "#8A6A00"
PANEL = "#F7F8FA"


def text(x, y, content, size=16, fill=INK, weight="normal", anchor="middle",
         style="normal", opacity=None):
    attrs = [
        f'x="{x}"',
        f'y="{y}"',
        f'font-size="{size}"',
        f'fill="{fill}"',
        f'font-weight="{weight}"',
        f'text-anchor="{anchor}"',
        f'font-style="{style}"',
    ]
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    return f'<text {" ".join(attrs)}>{escape(content)}</text>'


def rect(x, y, w, h, fill="white", stroke=GRID, sw=1.0, rx=6):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
        f'rx="{rx}" ry="{rx}"/>'
    )


def line(x1, y1, x2, y2, stroke=INK, sw=1.5, marker=None, dash=None):
    attrs = [
        f'x1="{x1}"', f'y1="{y1}"', f'x2="{x2}"', f'y2="{y2}"',
        f'stroke="{stroke}"', f'stroke-width="{sw}"'
    ]
    if marker:
        attrs.append(f'marker-end="{marker}"')
    if dash:
        attrs.append(f'stroke-dasharray="{dash}"')
    return f'<line {" ".join(attrs)}/>'


def svg_open(width, height):
    return [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
            f'font-family="{FONT}">'
        ),
        '<rect width="100%" height="100%" fill="white"/>',
    ]


def write_svg(name, parts):
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / name
    out.write_text("\n".join(parts) + "\n")
    print(f"Wrote {out.relative_to(Path(__file__).resolve().parents[2])}")


def add_matrix_cell(svg, x, y, w, h, color, title, dev, gloss, note):
    svg.append(rect(x, y, w, h, fill=PANEL, stroke=color, sw=1.4, rx=7))
    svg.append(text(x + w / 2, y + 34, title, size=22, fill=color, weight="bold"))
    svg.append(text(x + w / 2, y + 62, dev, size=20, fill=INK))
    svg.append(text(x + w / 2, y + 94, gloss, size=13, fill=INK, weight="bold"))
    svg.append(text(x + w / 2, y + 119, note, size=11, fill=MUTED))


def build_domains_modes_matrix():
    width, height = 720, 470
    svg = svg_open(width, height)

    svg.append(text(width / 2, 42, "Indic Two-Axis Vocabulary", size=24, weight="bold"))
    svg.append(text(
        width / 2, 68,
        "Domains name where Sanskrit operates. Modes name how the architecture runs.",
        size=13, fill=MUTED,
    ))

    x0, y0 = 110, 105
    cell_w, cell_h = 250, 140
    gap = 28

    svg.append(text(64, y0 + 77, "Domains", size=16, fill=BLUE, weight="bold", anchor="middle"))
    svg.append(text(64, y0 + cell_h + gap + 77, "Modes", size=16, fill=GREEN, weight="bold", anchor="middle"))

    add_matrix_cell(
        svg, x0, y0, cell_w, cell_h, BLUE,
        "vaidika", "वैदिक",
        "Vedic domain",
        "the śruti / Veda domain",
    )
    add_matrix_cell(
        svg, x0 + cell_w + gap, y0, cell_w, cell_h, BLUE,
        "laukika", "लौकिक",
        "worldly learned domain",
        "śāstra, kāvya, discourse",
    )
    add_matrix_cell(
        svg, x0, y0 + cell_h + gap, cell_w, cell_h, GREEN,
        "chandas", "छन्दस्",
        "metrical-corpus mode",
        "meter-bound operation",
    )
    add_matrix_cell(
        svg, x0 + cell_w + gap, y0 + cell_h + gap, cell_w, cell_h, GREEN,
        "bhāṣā", "भाषा",
        "productive speech-literary mode",
        "generative learned usage",
    )

    svg.append(line(98, y0 + cell_h + gap / 2, width - 92, y0 + cell_h + gap / 2, stroke=GRID, sw=1.1))
    svg.append(line(x0 + cell_w + gap / 2, y0 - 10, x0 + cell_w + gap / 2, y0 + 2 * cell_h + gap + 10, stroke=GRID, sw=1.1))

    svg.append(text(
        width / 2, height - 38,
        "Domain is not chronology. Mode is not drift.",
        size=18, fill=INK, weight="bold",
    ))
    svg.append("</svg>")
    write_svg("domains_modes_matrix.from-py.svg", svg)


def build_orthodoxy_flattening():
    width, height = 780, 420
    svg = svg_open(width, height)

    svg.append(
        '<defs>'
        '<marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" '
        'orient="auto" markerUnits="strokeWidth">'
        '<path d="M0,0 L0,6 L9,3 z" fill="#111111"/>'
        '</marker>'
        '</defs>'
    )

    svg.append(text(width / 2, 40, "The Orthodoxy Turns Domain and Mode Into Chronology", size=21, weight="bold"))
    svg.append(text(
        width / 2, 66,
        "Pāṇini becomes the rupture point: pre-Pāṇini = Vedic, post-Pāṇini = Classical.",
        size=13, fill=MUTED,
    ))

    axis_x1, axis_x2 = 90, 700
    panini_x = 395
    top_y = 98
    band_h = 96
    ortho_y = 230
    row_h = 58
    axis_y = 326

    # Continuous architecture band.
    svg.append(rect(axis_x1, top_y, axis_x2 - axis_x1, band_h, fill="#EAF1F8", stroke=BLUE, sw=1.6, rx=8))
    svg.append(text(width / 2, top_y + 28, "Sanskrit architecture", size=20, fill=BLUE, weight="bold"))
    svg.append(text(width / 2, top_y + 54, "one engineered system across both sides of Pāṇini", size=13, fill=INK))
    svg.append(text(width / 2, top_y + 78, "domains: vaidika / laukika · modes: chandas / bhāṣā", size=12, fill=MUTED))

    # Orthodoxy split row.
    svg.append(rect(axis_x1, ortho_y, panini_x - axis_x1, row_h, fill="#FFF8F8", stroke=RED, sw=1.2, rx=6))
    svg.append(rect(panini_x, ortho_y, axis_x2 - panini_x, row_h, fill="#FFF8F8", stroke=RED, sw=1.2, rx=6))
    svg.append(text(axis_x1 + (panini_x - axis_x1) / 2, ortho_y + 25, "orthodoxy's invention", size=11, fill=RED, weight="bold"))
    svg.append(text(axis_x1 + (panini_x - axis_x1) / 2, ortho_y + 47, "“Vedic”", size=20, fill=INK, weight="bold"))
    svg.append(text(panini_x + (axis_x2 - panini_x) / 2, ortho_y + 25, "orthodoxy's invention", size=11, fill=RED, weight="bold"))
    svg.append(text(panini_x + (axis_x2 - panini_x) / 2, ortho_y + 47, "“Classical”", size=20, fill=INK, weight="bold"))
    svg.append(text(axis_x1 - 18, ortho_y + 36, "split", size=12, fill=RED, weight="bold", anchor="end"))

    # Pāṇini marker.
    svg.append(line(panini_x, axis_y + 18, panini_x, 214, stroke=INK, sw=1.4, dash="4 4"))
    svg.append(rect(panini_x - 54, 184, 108, 30, fill="white", stroke=INK, sw=1.0, rx=5))
    svg.append(text(panini_x, 205, "Pāṇini", size=15, fill=INK, weight="bold"))

    # Time axis.
    svg.append(line(axis_x1, axis_y, axis_x2, axis_y, stroke=INK, sw=1.8, marker="url(#arrow)"))
    svg.append(text(axis_x1, axis_y + 28, "pre-Pāṇini", size=13, fill=MUTED, anchor="start"))
    svg.append(text(axis_x2, axis_y + 28, "post-Pāṇini", size=13, fill=MUTED, anchor="end"))
    svg.append(text(width / 2, axis_y + 46, "time", size=12, fill=MUTED, style="italic"))

    # Bottom verdict strip.
    svg.append(rect(88, 368, 604, 34, fill="white", stroke=GOLD, sw=1.4, rx=7))
    svg.append(text(
        width / 2, 390,
        "The orthodoxy makes Pāṇini a rupture. The architecture makes him a witness.",
        size=15, fill=GOLD, weight="bold",
    ))

    svg.append("</svg>")
    write_svg("orthodoxy_flattening.from-py.svg", svg)


def main():
    build_domains_modes_matrix()
    build_orthodoxy_flattening()


if __name__ == "__main__":
    main()

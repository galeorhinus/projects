#!/usr/bin/env python3
"""Generate Ch11 reactivity-tier chart as SVG/PDF.

Two 100% horizontal bars compare:

- share of distinct verbal atoms visible in the DCS record
- share of verb-token use carried by those same tiers

The figure lands the main claim in §11.8 without making the prose carry
every number: a small polyvalent tier carries most actual deployment,
while the long tail remains preserved but specialized.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT_ROOT / "figures" / "build"
OUT_SVG = OUT_DIR / "ganah_reactivity_tiers.svg"
OUT_PDF = OUT_DIR / "ganah_reactivity_tiers.pdf"

ROWS = [
    ("Verbal atoms in use", [("Polyvalent", 3.8), ("Bivalent", 27.6), ("Monovalent", 68.6)]),
    ("Verb-token use", [("Polyvalent", 67.6), ("Bivalent", 30.5), ("Monovalent", 1.9)]),
]

COLORS = {
    "Polyvalent": "#222222",
    "Bivalent": "#777777",
    "Monovalent": "#d8d8d8",
}

TEXT = "#111111"
STROKE = "#111111"


def esc(text: object) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render() -> str:
    width = 920
    height = 290
    margin_left = 190
    margin_right = 34
    margin_top = 72
    bar_h = 48
    row_gap = 82
    plot_w = width - margin_left - margin_right
    font = "Charter, Adobe Devanagari, DejaVu Serif, serif"

    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">'
    )
    parts.append('<rect x="0" y="0" width="100%" height="100%" fill="white"/>')

    # Legend
    x = margin_left
    y = 30
    for label in ("Polyvalent", "Bivalent", "Monovalent"):
        parts.append(
            f'<rect x="{x}" y="{y - 12}" width="24" height="14" '
            f'fill="{COLORS[label]}" stroke="{STROKE}" stroke-width="0.6"/>'
        )
        fill_text = TEXT
        parts.append(
            f'<text x="{x + 32}" y="{y}" fill="{fill_text}" '
            f'style="font-family:{font};font-size:14px">{esc(label)}</text>'
        )
        x += 150

    for i, (row_label, values) in enumerate(ROWS):
        cy = margin_top + i * row_gap
        y = cy - bar_h / 2
        parts.append(
            f'<text x="{margin_left - 18}" y="{cy + 5}" '
            f'text-anchor="end" style="font-family:{font};font-size:16px">'
            f'{esc(row_label)}</text>'
        )

        cursor = margin_left
        for label, pct in values:
            w = pct / 100.0 * plot_w
            parts.append(
                f'<rect x="{cursor:.2f}" y="{y:.2f}" width="{w:.2f}" '
                f'height="{bar_h}" fill="{COLORS[label]}" '
                f'stroke="{STROKE}" stroke-width="0.6"/>'
            )

            # Label if there is room inside; otherwise place just beyond segment.
            if w > 58:
                fill = "white" if label != "Monovalent" else TEXT
                parts.append(
                    f'<text x="{cursor + w / 2:.2f}" y="{cy + 5}" '
                    f'text-anchor="middle" fill="{fill}" '
                    f'style="font-family:{font};font-size:15px;font-weight:bold">'
                    f'{pct:.1f}%</text>'
                )
            else:
                parts.append(
                    f'<text x="{cursor + w + 7:.2f}" y="{cy + 5}" '
                    f'text-anchor="start" fill="{TEXT}" '
                    f'style="font-family:{font};font-size:14px">'
                    f'{pct:.1f}%</text>'
                )
            cursor += w

    parts.append(
        f'<text x="{margin_left + plot_w / 2}" y="{height - 24}" '
        f'text-anchor="middle" style="font-family:{font};font-size:15px">'
        f'Share of total (%)</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    OUT_DIR.mkdir(exist_ok=True)
    OUT_SVG.write_text(render(), encoding="utf-8")
    print(f"Wrote {OUT_SVG.relative_to(PROJECT_ROOT)}")

    converter = shutil.which("rsvg-convert")
    if converter:
        subprocess.run(
            [converter, "-f", "pdf", "-o", str(OUT_PDF), str(OUT_SVG)],
            check=True,
        )
        print(f"Wrote {OUT_PDF.relative_to(PROJECT_ROOT)}")
    else:
        print("WARNING: rsvg-convert not found; PDF not written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

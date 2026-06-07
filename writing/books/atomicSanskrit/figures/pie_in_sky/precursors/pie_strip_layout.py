#!/usr/bin/env python3
"""5-up strip layout: Sanskrit-vs-PIE polished overlays side-by-side.

Composes the five Sanskrit-vs-PIE polished overlay SVGs into a
single wide figure showing the PIE-revision trajectory at a glance.

Each panel is one milestone reconstruction; reading left to right
walks the reader through 150 years of philological revision.

The composite is sized 22 in × 4.5 in (book-trim landscape spread
or large appendix figure).  Each panel is 4.4 in × 4.0 in with a
0.2-in gap; a thin year stripe above each panel.
"""
from __future__ import annotations

import sys
from pathlib import Path


YEARS     = [1862, 1897, 1927, 1973, 2020]
THEORISTS = ["Schleicher", "Brugmann", "Standard", "Glottalic", "Modern"]
SK_VALS   = [0.81, 0.73, 0.64, 0.48, 0.64]

PALETTE = {
    "background":   "#f4f4f3",
    "label":        "#2b2b2d",
    "muted":        "#8f8d86",
}

FONT = "'Gentium Book Plus', Charter, 'Charis SIL', Georgia, serif"


def _xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


def build_strip() -> str:
    panel_w   = 4.40
    panel_h   = 4.00
    panel_gap = 0.20
    label_h   = 0.60   # year label band above each panel
    footer_h  = 0.45   # caption strip below

    n = 5
    W = n * panel_w + (n - 1) * panel_gap
    H = label_h + panel_h + footer_h

    body: list[str] = []

    # 1. Background
    body.append(
        f'  <rect x="0" y="0" width="{W:.4f}" height="{H:.4f}" '
        f'fill="{PALETTE["background"]}" />\n'
    )

    # 2. Per-panel label band + embedded overlay
    for i, (year, name, sk_v) in enumerate(zip(YEARS, THEORISTS, SK_VALS)):
        x = i * (panel_w + panel_gap)

        # Year (bold) and theorist (muted) above panel
        label_cx = x + 0.5 * panel_w
        body.append(
            f'  <text x="{label_cx:.4f}" y="0.30" '
            f'text-anchor="middle" font-size="0.20" font-weight="bold" '
            f'fill="{PALETTE["label"]}" font-family="{FONT}">'
            f'{year} · {_xml_escape(name)}</text>\n'
        )
        body.append(
            f'  <text x="{label_cx:.4f}" y="0.52" '
            f'text-anchor="middle" font-size="0.135" '
            f'fill="{PALETTE["muted"]}" font-family="{FONT}">'
            f'Sk ⊇ PIE = {sk_v:.2f}</text>\n'
        )

        # Embed the polished overlay SVG by reference
        href = f"overlay_sanskrit_vs_pie_{year}_polished.svg"
        body.append(
            f'  <image href="{href}" x="{x:.4f}" y="{label_h:.4f}" '
            f'width="{panel_w:.4f}" height="{panel_h:.4f}" '
            f'preserveAspectRatio="xMidYMid meet" />\n'
        )

    # 3. Footer caption
    body.append(
        f'  <text x="{W/2:.4f}" y="{H - 0.12:.4f}" text-anchor="middle" '
        f'font-size="0.16" fill="{PALETTE["muted"]}" font-style="italic" '
        f'font-family="{FONT}">'
        f'Sanskrit-vs-PIE pairwise overlay across 150 years of reconstruction '
        f'(left → right).  Sanskrit ⊇ PIE declines as the orthodox '
        f'reconstruction moves AWAY from the language it was originally '
        f'walked-backward from.</text>\n'
    )

    svg = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n',
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{W:.4f}in" height="{H:.4f}in" '
        f'viewBox="0 0 {W:.4f} {H:.4f}">\n',
    ]
    svg.extend(body)
    svg.append('</svg>\n')
    return "".join(svg)


def main() -> int:
    svg = build_strip()
    out = (
        Path(__file__).resolve().parent.parent
        / "build" / "vocal_tract" / "pie_strip_layout.svg"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    print(f"Wrote {out} ({len(svg)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

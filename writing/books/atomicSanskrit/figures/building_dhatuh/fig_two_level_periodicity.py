"""Two-Level Periodicity bridge — conceptual diagram (Codex Figure 5).

Three vertically stacked panels showing the levels at which periodicity
appears in Sanskrit's architecture:

    Subatomic periodicity (Ch 10) — varṇāḥ sorted by position-role valency
                ↓
    Atomic periodicity (Ch 11, pending Path C) — dhātavaḥ sorted by gaṇa
                ↓
    Molecular chemistry — śabdāḥ generated through bonding rules

Generates an SVG directly (no matplotlib dependency).

Run: python3 figures/building_dhatuh/fig_two_level_periodicity.py
"""

from pathlib import Path


# Colors
PANEL_TOP = "#1F4E79"     # deep blue — established (Ch 10)
PANEL_MID = "#888888"     # gray — pending (Ch 11, Path C dependent)
PANEL_BOT = "#2D6A4F"     # dark green — implied by bonding chapters
ARROW = "#222222"
TEXT_LIGHT = "white"
TEXT_DARK = "#222222"


def main():
    width = 540
    panel_w = 360
    panel_h = 95
    gap = 50
    margin_top = 40
    margin_left = (width - panel_w) // 2

    n_panels = 3
    height = margin_top + n_panels * panel_h + (n_panels - 1) * gap + 60

    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="Charter, &quot;Bitstream Charter&quot;, &quot;DejaVu Serif&quot;, serif">'
    )
    svg.append(f'<rect width="{width}" height="{height}" fill="white"/>')

    panels = [
        {
            "color": PANEL_TOP,
            "title": "Subatomic periodicity",
            "subtitle": "(Ch 10 — established)",
            "body": "varṇāḥ sorted by position-role valency",
            "detail": "column · place · row · closure · bonding signatures",
        },
        {
            "color": PANEL_MID,
            "title": "Atomic periodicity",
            "subtitle": "(Ch 11 — pending Path C empirical validation)",
            "body": "dhātavaḥ sorted by gaṇa / derivational valency",
            "detail": "combining behavior · reactivity tiers",
        },
        {
            "color": PANEL_BOT,
            "title": "Molecular chemistry",
            "subtitle": "(Ch 12 — bonding chemistry)",
            "body": "śabdāḥ generated through bonding rules",
            "detail": "upasarga + dhātu + pratyaya combinatorics",
        },
    ]

    # Draw panels and arrows
    for i, p in enumerate(panels):
        y = margin_top + i * (panel_h + gap)

        # Panel box
        svg.append(
            f'<rect x="{margin_left}" y="{y}" '
            f'width="{panel_w}" height="{panel_h}" '
            f'fill="{p["color"]}" stroke="black" stroke-width="0.6" '
            f'rx="4" ry="4"/>'
        )

        # Title
        svg.append(
            f'<text x="{width/2}" y="{y + 24}" '
            f'font-size="14" font-weight="bold" fill="white" '
            f'text-anchor="middle">{p["title"]}</text>'
        )
        # Subtitle
        svg.append(
            f'<text x="{width/2}" y="{y + 40}" '
            f'font-size="9.5" fill="white" opacity="0.85" '
            f'text-anchor="middle" font-style="italic">{p["subtitle"]}</text>'
        )
        # Body
        svg.append(
            f'<text x="{width/2}" y="{y + 62}" '
            f'font-size="11" fill="white" '
            f'text-anchor="middle">{p["body"]}</text>'
        )
        # Detail
        svg.append(
            f'<text x="{width/2}" y="{y + 80}" '
            f'font-size="9" fill="white" opacity="0.75" '
            f'text-anchor="middle">{p["detail"]}</text>'
        )

        # Arrow between panels
        if i < len(panels) - 1:
            ax = width / 2
            ay1 = y + panel_h + 4
            ay2 = y + panel_h + gap - 4
            svg.append(
                f'<line x1="{ax}" y1="{ay1}" x2="{ax}" y2="{ay2 - 8}" '
                f'stroke="{ARROW}" stroke-width="2"/>'
            )
            # Arrowhead
            svg.append(
                f'<polygon points="'
                f'{ax - 6},{ay2 - 8} '
                f'{ax + 6},{ay2 - 8} '
                f'{ax},{ay2}" '
                f'fill="{ARROW}"/>'
            )

    svg.append("</svg>")

    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "building_dhatuh_two_level_periodicity.svg"
    out_path.write_text("\n".join(svg))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
The Dhātu Foundry — Ch 10 §10.7 figure (Claude version).

Visualizes Sanskrit's varṇa → racanā → dhātu architecture as a foundry:
- Varṇamālā box (top-left) feeds varṇas through an outlet
- Four representative scaffolds in a horizontal row (CV1, CV1C, CCV2, CCV1CC)
  with the "...and 43 more" gap between scaffolds 3 and 4
- Varṇas flow along a continuous path, rotating to align with the local
  flow direction (option (b) — letters orient to tangent)
- Each scaffold drops mini-dhātus below it (randomly rotated, like assembly-line output)

No external dependencies — pure stdlib + hand-rolled SVG.

Output: figures/build/claude_dhatu_foundry.svg
"""

import random
from pathlib import Path

# Reproducible scatter for the mini-dhātus
random.seed(42)

# ===========================================================================
# Configuration
# ===========================================================================

WIDTH = 1600
HEIGHT = 1000

# Palette — monochrome, matches book style
COLOR_FRAME = "#222222"
COLOR_SCAFFOLD = "#888888"
COLOR_SCAFFOLD_FILL = "#f6f6f6"
COLOR_STREAM_LINE = "#cccccc"
COLOR_VARNA = "#222222"
COLOR_DHATU_FILL = "#eeeeee"
COLOR_LABEL = "#222222"
COLOR_SUBTLE = "#888888"

# Varṇamālā box (top-left)
BOX_X = 80
BOX_Y = 90
BOX_W = 250
BOX_H = 120
OUTLET_W = 35
OUTLET_DROP = 35

# Scaffold row geometry
SCAFFOLD_Y_CENTER = 530
SCAFFOLD_H = 130

SCAFFOLDS = [
    {"name": "CV1",    "adi": "krādi",     "w": 140},
    {"name": "CV1C",   "adi": "gamādi",    "w": 200},
    {"name": "CCV2",   "adi": "sthādi",    "w": 240},
    {"name": "CCV1CC", "adi": "spardhādi", "w": 280},
]

SCAFFOLD_GAP_SHORT = 60
SCAFFOLD_GAP_DOTS = 130  # extended gap before scaffold 4 to hold "...and 43 more"

# Compute x positions for each scaffold left-edge
SCAFFOLD_X = []
x = 380
for i, spec in enumerate(SCAFFOLDS):
    SCAFFOLD_X.append(x)
    gap = SCAFFOLD_GAP_DOTS if i == 2 else SCAFFOLD_GAP_SHORT
    x += spec["w"] + gap

# Devanagari glyphs streaming through the path
VARNAS_DEV = [
    "क", "ख", "ग", "घ", "च", "छ", "ज", "ट", "ड", "त", "थ", "द", "ध", "न",
    "प", "फ", "ब", "भ", "म", "य", "र", "ल", "व", "श", "ष", "स", "ह",
    "अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ए", "ऐ", "ओ", "औ",
]

# Sample finished dhātus that fall out of each scaffold
DHATU_SAMPLES = {
    "CV1":    ["कृ", "भृ", "हृ", "धृ", "सृ", "मृ"],
    "CV1C":   ["गम्", "पच्", "वद्", "यज्", "हन्", "नम्"],
    "CCV2":   ["स्था", "ज्ञा", "ग्ला", "स्ना", "श्रा"],
    "CCV1CC": ["स्पर्ध्", "स्वर्द्", "स्यन्द्", "क्रुञ्च्"],
}

# Font stacks — prefer Devanagari-capable fonts where Sanskrit appears
DEVANAGARI_FONT = "'Noto Sans Devanagari', 'Sanskrit 2003', 'Lohit Devanagari', serif"
LABEL_FONT = "Georgia, 'Times New Roman', serif"


# ===========================================================================
# SVG helpers
# ===========================================================================

def hexagon_path(cx, cy, w, h):
    """Return an SVG path-d string for a horizontal hexagon centred at (cx, cy)."""
    nick = w * 0.13
    return (f"M{cx - w/2 + nick:.1f},{cy - h/2:.1f} "
            f"L{cx + w/2 - nick:.1f},{cy - h/2:.1f} "
            f"L{cx + w/2:.1f},{cy:.1f} "
            f"L{cx + w/2 - nick:.1f},{cy + h/2:.1f} "
            f"L{cx - w/2 + nick:.1f},{cy + h/2:.1f} "
            f"L{cx - w/2:.1f},{cy:.1f} Z")


def title_svg():
    return (
        f'<text x="{WIDTH/2}" y="48" text-anchor="middle" '
        f'font-family="{LABEL_FONT}" font-size="28" font-weight="bold" '
        f'fill="{COLOR_LABEL}">The Dhātu Foundry</text>\n'
        f'<text x="{WIDTH/2}" y="72" text-anchor="middle" '
        f'font-family="{LABEL_FONT}" font-style="italic" font-size="15" '
        f'fill="{COLOR_LABEL}">47 varṇāḥ flow through 47 racanāḥ to produce 2,168 dhātavaḥ</text>'
    )


def box_svg():
    cx = BOX_X + BOX_W / 2
    cy = BOX_Y + BOX_H / 2
    outlet_top_y = BOX_Y + BOX_H
    outlet_bot_y = outlet_top_y + OUTLET_DROP
    parts = []
    parts.append(
        f'<rect x="{BOX_X}" y="{BOX_Y}" width="{BOX_W}" height="{BOX_H}" '
        f'fill="{COLOR_SCAFFOLD_FILL}" stroke="{COLOR_FRAME}" stroke-width="2.5" rx="6"/>'
    )
    parts.append(
        f'<text x="{cx}" y="{cy - 4}" text-anchor="middle" '
        f'font-family="{DEVANAGARI_FONT}" font-size="30" font-weight="bold" '
        f'fill="{COLOR_LABEL}">वर्णमाला</text>'
    )
    parts.append(
        f'<text x="{cx}" y="{cy + 24}" text-anchor="middle" '
        f'font-family="{LABEL_FONT}" font-style="italic" font-size="14" '
        f'fill="{COLOR_LABEL}">varṇamālā (47)</text>'
    )
    parts.append(
        f'<polygon points="'
        f'{cx - OUTLET_W},{outlet_top_y} '
        f'{cx + OUTLET_W},{outlet_top_y} '
        f'{cx + OUTLET_W * 0.5},{outlet_bot_y} '
        f'{cx - OUTLET_W * 0.5},{outlet_bot_y}" '
        f'fill="{COLOR_SCAFFOLD_FILL}" stroke="{COLOR_FRAME}" stroke-width="2"/>'
    )
    return "\n".join(parts), cx, outlet_bot_y


def flow_path_data(outlet_x, outlet_y):
    """Continuous SVG path: outlet → curve down → through scaffolds → exit right."""
    cmds = [f"M{outlet_x:.1f},{outlet_y:.1f}"]

    s1_x = SCAFFOLD_X[0]
    s1_y = SCAFFOLD_Y_CENTER

    # Cubic curve from outlet to scaffold-1 left edge
    cmds.append(
        f"C{outlet_x:.1f},{outlet_y + 150:.1f} "
        f"{s1_x - 80:.1f},{s1_y - 80:.1f} "
        f"{s1_x:.1f},{s1_y:.1f}"
    )

    # Through each scaffold (subtle bow) and across the gap to the next
    for i, spec in enumerate(SCAFFOLDS):
        s_left = SCAFFOLD_X[i]
        s_right = SCAFFOLD_X[i] + spec["w"]
        s_y = SCAFFOLD_Y_CENTER
        mid_x = (s_left + s_right) / 2
        cmds.append(f"Q{mid_x:.1f},{s_y + 12:.1f} {s_right:.1f},{s_y:.1f}")
        if i < len(SCAFFOLDS) - 1:
            next_left = SCAFFOLD_X[i + 1]
            cmds.append(f"L{next_left:.1f},{s_y:.1f}")

    # Exit right with a downward slope
    last_right = SCAFFOLD_X[-1] + SCAFFOLDS[-1]["w"]
    cmds.append(f"L{last_right + 80:.1f},{SCAFFOLD_Y_CENTER + 50:.1f}")

    return " ".join(cmds)


def scaffolds_svg():
    parts = []
    for i, spec in enumerate(SCAFFOLDS):
        x = SCAFFOLD_X[i]
        cx = x + spec["w"] / 2
        cy = SCAFFOLD_Y_CENTER
        w = spec["w"]
        h = SCAFFOLD_H
        parts.append(
            f'<path d="{hexagon_path(cx, cy, w, h)}" '
            f'fill="{COLOR_SCAFFOLD_FILL}" stroke="{COLOR_SCAFFOLD}" stroke-width="2.5"/>'
        )
        parts.append(
            f'<text x="{cx}" y="{cy + h/2 + 26}" text-anchor="middle" '
            f'font-family="{LABEL_FONT}" font-size="15" font-weight="bold" '
            f'fill="{COLOR_LABEL}">{spec["name"]}</text>'
        )
        parts.append(
            f'<text x="{cx}" y="{cy + h/2 + 46}" text-anchor="middle" '
            f'font-family="{LABEL_FONT}" font-style="italic" font-size="13" '
            f'fill="{COLOR_LABEL}">{spec["adi"]}</text>'
        )
    return "\n".join(parts)


def dots_svg():
    s3_right = SCAFFOLD_X[2] + SCAFFOLDS[2]["w"]
    s4_left = SCAFFOLD_X[3]
    y = SCAFFOLD_Y_CENTER
    parts = []
    n_dots = 5
    for i in range(n_dots):
        cx = s3_right + (s4_left - s3_right) * (i + 1) / (n_dots + 1)
        parts.append(
            f'<circle cx="{cx:.1f}" cy="{y:.1f}" r="4" '
            f'fill="{COLOR_SUBTLE}" opacity="0.6"/>'
        )
    mid_x = (s3_right + s4_left) / 2
    parts.append(
        f'<text x="{mid_x:.1f}" y="{y + 42:.1f}" text-anchor="middle" '
        f'font-family="{LABEL_FONT}" font-style="italic" font-size="12" '
        f'fill="{COLOR_SUBTLE}">and 43 more</text>'
    )
    return "\n".join(parts)


def stream_text_svg():
    """Devanagari varṇa stream along the flow path.

    textPath rotates each glyph to align with the local tangent, so glyphs
    fall sideways through the drop, stand upright through the horizontal flow,
    and rotate smoothly through the curve — that's option (b).
    """
    glyphs = (VARNAS_DEV * 4)[:90]
    text_content = "  ".join(glyphs)  # two spaces between glyphs for breathing room
    return (
        f'<text font-family="{DEVANAGARI_FONT}" font-size="22" font-weight="bold" '
        f'fill="{COLOR_VARNA}">\n'
        f'  <textPath href="#flow-path" startOffset="2%">{text_content}</textPath>\n'
        f'</text>'
    )


def mini_dhatus_svg():
    """Each scaffold sheds mini-dhātus below it, randomly rotated."""
    parts = []
    for i, spec in enumerate(SCAFFOLDS):
        cx_scaffold = SCAFFOLD_X[i] + spec["w"] / 2
        samples = DHATU_SAMPLES[spec["name"]]
        n_drops = 4
        for j in range(n_drops):
            dx = random.uniform(-spec["w"] * 0.4, spec["w"] * 0.4)
            dy = random.uniform(70, 240)
            rotation = random.uniform(-30, 30)
            cx = cx_scaffold + dx
            cy = SCAFFOLD_Y_CENTER + SCAFFOLD_H / 2 + 60 + dy
            mini_w = 64
            mini_h = 46
            parts.append(f'<g transform="rotate({rotation:.1f} {cx:.1f} {cy:.1f})">')
            parts.append(
                f'<path d="{hexagon_path(cx, cy, mini_w, mini_h)}" '
                f'fill="{COLOR_DHATU_FILL}" stroke="{COLOR_FRAME}" stroke-width="1.3"/>'
            )
            glyph = samples[j % len(samples)]
            parts.append(
                f'<text x="{cx:.1f}" y="{cy + 7:.1f}" text-anchor="middle" '
                f'font-family="{DEVANAGARI_FONT}" font-weight="bold" font-size="20" '
                f'fill="{COLOR_VARNA}">{glyph}</text>'
            )
            parts.append('</g>')
    return "\n".join(parts)


# ===========================================================================
# Composition
# ===========================================================================

def build_svg():
    box, outlet_x, outlet_y = box_svg()
    path_d = flow_path_data(outlet_x, outlet_y)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{WIDTH}" height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}">

<rect width="100%" height="100%" fill="white"/>

{title_svg()}

{box}

<defs>
  <path id="flow-path" d="{path_d}" fill="none"/>
</defs>

<use href="#flow-path" stroke="{COLOR_STREAM_LINE}" stroke-width="2"
     fill="none" stroke-dasharray="4,3" opacity="0.45"/>

{scaffolds_svg()}

{dots_svg()}

{stream_text_svg()}

{mini_dhatus_svg()}

</svg>
'''


def main():
    svg_content = build_svg()
    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "claude_dhatu_foundry.svg"
    out_path.write_text(svg_content, encoding="utf-8")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate Chapter 12 SVG figures.

The figures extend the Ch10/Ch11 hexagon grammar into the *śabda*,
*padam*, and *vākya* scale. They intentionally stay schematic where full
Pāṇinian derivation would distract from the chapter's procedural claim.
"""

from __future__ import annotations

import html
import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_DIR = REPO_ROOT / "figures" / "build"
sys.path.insert(0, str(REPO_ROOT / "working" / "dhatu_hexagons"))

from dhatu_hexagon import EDGE_LENGTH, HEX_HEIGHT, VARNAS, is_ayogavaha  # noqa: E402


DEV_FONT = (
    "Noto Sans Devanagari, Kohinoor Devanagari, Devanagari MT, "
    "Arial Unicode MS, sans-serif"
)
LATIN_FONT = "Charter, Georgia, Times, serif"
HALANT = "्"

# Geometry is locked to the Ch11 timing convention: the visible midpoint
# span of each tile tracks its mātrā value.
MATRA_UNIT = 60
WIDTH_C = 10
WIDTH_V1 = 40
WIDTH_V2 = 100

UPPER_RAIL_Y = -HEX_HEIGHT / 4
LOWER_RAIL_Y = HEX_HEIGHT / 4

TEXT = "#1a1a1a"
MUTED = "#555555"
LIGHT = "#dcdcdc"
MID = "#888888"
DARK = "#555555"
BLACK = "#1a1a1a"
WHITE = "#f7f7f7"
STROKE = "#333333"
DASH = "#777777"

ROLE_FILL = {
    "original": LIGHT,
    "transform": MID,
    "head": BLACK,
    "tail": DARK,
    "role": MID,
    "sentence": "#eeeeee",
    "seed": "#f5f5f5",
    "root": "#cfcfcf",
}

ROLE_TEXT = {
    "original": TEXT,
    "transform": TEXT,
    "head": WHITE,
    "tail": WHITE,
    "role": WHITE,
    "sentence": TEXT,
    "seed": TEXT,
    "root": TEXT,
}

ALIASES = {
    "A": "ā",
    "I": "ī",
    "U": "ū",
    "R": "ṛ",
    "RR": "ṝ",
    "lR": "ḷ",
    "T": "ṭ",
    "Th": "ṭh",
    "D": "ḍ",
    "Dh": "ḍh",
    "N": "ṇ",
    "G": "ṅ",
    "J": "ñ",
    "S": "ṣ",
    "z": "ś",
    # Ch12 uses sonomeric rendering rather than scribal shorthand:
    # anusvāra resolves to the nasal being represented, so the default
    # shortcut M renders as ordinary म्. Use a specific nasal token when the
    # homorganic nasal differs.
    "M": "m",
    "H": "ḥ",
}


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def varna(token: str) -> dict:
    key = ALIASES.get(token, token)
    if key not in VARNAS:
        raise ValueError(f"Unknown varṇa token: {token}")
    return dict(VARNAS[key])


def dev_label(v: dict) -> str:
    if v["class"] == "C" and not is_ayogavaha(v):
        return v["deva"] + HALANT
    return v["deva"]


def width_for(v: dict) -> float:
    if v["class"] == "C":
        return WIDTH_C
    if v["class"] == "V1":
        return WIDTH_V1
    if v["class"] == "V2":
        return WIDTH_V2
    return WIDTH_V1


def rail_for(v: dict) -> float:
    return LOWER_RAIL_Y if v["class"].startswith("V") or is_ayogavaha(v) else UPPER_RAIL_Y


def hex_vertices(cx: float, cy: float, w: float) -> list[tuple[float, float]]:
    e = EDGE_LENGTH
    h = HEX_HEIGHT
    return [
        (cx - w / 2, cy - h / 2),
        (cx + w / 2, cy - h / 2),
        (cx + w / 2 + e / 2, cy),
        (cx + w / 2, cy + h / 2),
        (cx - w / 2, cy + h / 2),
        (cx - w / 2 - e / 2, cy),
    ]


def points(vertices: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in vertices)


def ayogavaha_vertices(cx: float, cy: float) -> dict[str, tuple[float, float]]:
    e = EDGE_LENGTH
    h = HEX_HEIGHT
    return {
        "top_right": (cx + 3 * e / 4, cy - h / 2),
        "bottom_right": (cx + 3 * e / 4, cy + h / 2),
        "top_outer": (cx - 3 * e / 4, cy - h / 2),
        "socket": (cx - e / 4, cy),
        "bottom_outer": (cx - 3 * e / 4, cy + h / 2),
    }


def render_text(
    x: float,
    y: float,
    content: str,
    size: float,
    fill: str = TEXT,
    anchor: str = "middle",
    weight: str = "400",
    style: str = "normal",
    family: str = LATIN_FONT,
    baseline: str = "middle",
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" '
        f'font-size="{size}" font-weight="{weight}" font-style="{style}" '
        f'text-anchor="{anchor}" dominant-baseline="{baseline}" fill="{fill}">'
        f"{esc(content)}</text>"
    )


def render_arrow(x1: float, y1: float, x2: float, y2: float, dashed: bool = False) -> str:
    dash = ' stroke-dasharray="5,4"' if dashed else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arrow)"{dash}/>'
    )


def render_hex(cx: float, cy: float, v: dict, role: str = "original") -> str:
    if is_ayogavaha(v):
        return render_ayogavaha(cx, cy, v, role)
    fill = ROLE_FILL.get(role, LIGHT)
    text_fill = ROLE_TEXT.get(role, TEXT)
    w = width_for(v)
    fragments = [
        f'<polygon points="{points(hex_vertices(cx, cy, w))}" fill="{fill}" '
        f'stroke="{STROKE}" stroke-width="1.5" stroke-linejoin="round"/>',
        render_text(cx, cy - 7, dev_label(v), 23, text_fill, family=DEV_FONT, weight="600"),
        render_text(cx, cy + 19, v["iast"], 11, text_fill, style="italic"),
    ]
    return "\n  ".join(fragments)


def render_ayogavaha(cx: float, cy: float, v: dict, role: str = "original") -> str:
    verts = ayogavaha_vertices(cx, cy)
    tr = verts["top_right"]
    br = verts["bottom_right"]
    to = verts["top_outer"]
    socket = verts["socket"]
    bo = verts["bottom_outer"]
    fill = ROLE_FILL.get(role, LIGHT)
    text_fill = ROLE_TEXT.get(role, TEXT)
    mark_x = cx + EDGE_LENGTH / 4
    path_start = (
        f"M {tr[0]:.1f},{tr[1]:.1f} "
        f"L {to[0]:.1f},{to[1]:.1f} "
        f"L {socket[0]:.1f},{socket[1]:.1f} "
        f"L {bo[0]:.1f},{bo[1]:.1f} "
        f"L {br[0]:.1f},{br[1]:.1f} "
    )
    if v["voicing"] == "anusvara":
        right_x = tr[0]
        path = (
            path_start
            + f"C {right_x + 8:.1f},{cy + HEX_HEIGHT / 4:.1f} "
            + f"{right_x - 8:.1f},{cy + HEX_HEIGHT / 8:.1f} "
            + f"{right_x:.1f},{cy:.1f} "
            + f"C {right_x + 8:.1f},{cy - HEX_HEIGHT / 8:.1f} "
            + f"{right_x - 8:.1f},{cy - HEX_HEIGHT / 4:.1f} "
            + f"{tr[0]:.1f},{tr[1]:.1f} Z"
        )
    else:
        path = path_start + "Z"
    fragments = [
        f'<path d="{path}" fill="{fill}" stroke="{STROKE}" '
        f'stroke-width="1.5" stroke-linejoin="round"/>',
    ]
    dot_fill = WHITE if role in ("head", "tail", "role") else TEXT
    if v["voicing"] == "anusvara":
        fragments.append(f'<circle cx="{mark_x:.1f}" cy="{cy - HEX_HEIGHT / 7:.1f}" r="5.0" fill="{dot_fill}"/>')
    else:
        fragments.append(f'<circle cx="{mark_x:.1f}" cy="{cy - 8:.1f}" r="4.5" fill="{dot_fill}"/>')
        fragments.append(f'<circle cx="{mark_x:.1f}" cy="{cy + 8:.1f}" r="4.5" fill="{dot_fill}"/>')
    fragments.append(render_text(mark_x, cy + 23, v["iast"], 11, text_fill, style="italic"))
    return "\n  ".join(fragments)


def display_units(tokens: list[str], role: str) -> list[dict]:
    units: list[dict] = []
    particles = [varna(t) for t in tokens]
    i = 0
    while i < len(particles):
        current = particles[i]
        if current["class"] == "C" and not is_ayogavaha(current):
            run = [current]
            j = i + 1
            while j < len(particles) and particles[j]["class"] == "C" and not is_ayogavaha(particles[j]):
                run.append(particles[j])
                j += 1
            if len(run) > 1:
                units.append({"kind": "cluster", "parts": run, "role": role})
                i = j
                continue
        units.append({"kind": "particle", "particle": current, "role": role})
        i += 1
    return units


def unit_width(unit: dict) -> float:
    if unit["kind"] == "cluster":
        n = len(unit["parts"])
        return n * 0.5 * MATRA_UNIT - EDGE_LENGTH / 2
    return width_for(unit["particle"])


def unit_rail(unit: dict) -> float:
    if unit["kind"] == "cluster":
        return UPPER_RAIL_Y
    return rail_for(unit["particle"])


def unit_is_ayogavaha(unit: dict) -> bool:
    return unit["kind"] == "particle" and is_ayogavaha(unit["particle"])


def layout_units(units: list[dict]) -> list[dict]:
    out: list[dict] = []
    for i, unit in enumerate(units):
        cy = unit_rail(unit)
        w = unit_width(unit)
        if i == 0:
            cx = 0.0
        else:
            prev = out[-1]
            spacing = EDGE_LENGTH / 2 if (prev["cy"] != cy or unit_is_ayogavaha(unit)) else EDGE_LENGTH
            cx = prev["cx"] + (prev["w"] + w) / 2 + spacing
        out.append({**unit, "cx": cx, "cy": cy, "w": w})
    return out


def render_cluster(cx: float, cy: float, parts: list[dict], role: str) -> str:
    w = EDGE_LENGTH * len(parts) / 2
    fill = ROLE_FILL.get(role, LIGHT)
    text_fill = ROLE_TEXT.get(role, TEXT)
    fragments = [
        f'<polygon points="{points(hex_vertices(cx, cy, w))}" fill="{fill}" '
        f'stroke="{STROKE}" stroke-width="1.5" stroke-linejoin="round"/>'
    ]

    # Same-provenance clusters render as a single Devanagari conjunct,
    # centered in the shared timing envelope. If a future figure needs mixed
    # provenance inside a cluster, split the cluster into provenance-specific
    # render passes before calling this function.
    conjunct_dev = "".join(p["deva"] + HALANT for p in parts)
    conjunct_iast = "".join(p["iast"] for p in parts)
    dev_size = 22 if len(parts) == 2 else 19
    iast_size = 10 if len(parts) == 2 else 9
    fragments.append(render_text(cx, cy - 7, conjunct_dev, dev_size, text_fill, family=DEV_FONT, weight="600"))
    fragments.append(render_text(cx, cy + 19, conjunct_iast, iast_size, text_fill, style="italic"))
    return "\n  ".join(fragments)


def render_unit(unit: dict, dx: float, dy: float, role_override: str | None = None) -> str:
    cx = unit["cx"] + dx
    cy = unit["cy"] + dy
    role = role_override or unit["role"]
    if unit["kind"] == "cluster":
        return render_cluster(cx, cy, unit["parts"], role)
    return render_hex(cx, cy, unit["particle"], role)


def strip_extent(layout: list[dict]) -> tuple[float, float, float, float]:
    xs: list[float] = []
    ys: list[float] = []
    for unit in layout:
        xs.extend([unit["cx"] - unit["w"] / 2 - EDGE_LENGTH / 2, unit["cx"] + unit["w"] / 2 + EDGE_LENGTH / 2])
        ys.extend([unit["cy"] - HEX_HEIGHT / 2, unit["cy"] + HEX_HEIGHT / 2])
    return min(xs), min(ys), max(xs), max(ys)


def total_matras(units: list[dict]) -> float:
    total = 0.0
    for unit in units:
        if unit["kind"] == "cluster":
            total += 0.5 * len(unit["parts"])
            continue
        particle = unit["particle"]
        if particle["class"] == "V2":
            total += 2.0
        elif particle["class"] == "V1":
            total += 1.0
        else:
            total += 0.5
    return total


def render_matra_line(left_tip_x: float, line_y: float, n_matras: float) -> tuple[str, float]:
    """Render the Ch10/Ch11 half-mātrā ruler under a word strip."""
    if n_matras <= 0:
        return "", left_tip_x
    start_x = left_tip_x + EDGE_LENGTH / 4
    end_x = start_x + n_matras * MATRA_UNIT
    color = "#888888"
    fragments = [
        f'<line x1="{start_x:.1f}" y1="{line_y:.1f}" '
        f'x2="{end_x:.1f}" y2="{line_y:.1f}" '
        f'stroke="{color}" stroke-width="1.2"/>'
    ]
    for i in range(int(round(n_matras * 2)) + 1):
        x = start_x + i * MATRA_UNIT / 2
        major = i % 2 == 0
        tick_len = 8 if major else 4
        tick_w = 1.2 if major else 1.0
        fragments.append(
            f'<line x1="{x:.1f}" y1="{line_y:.1f}" '
            f'x2="{x:.1f}" y2="{line_y - tick_len:.1f}" '
            f'stroke="{color}" stroke-width="{tick_w}"/>'
        )
    return "\n  ".join(fragments), end_x


def render_strip(
    words: list[list[str]],
    x: float,
    y: float,
    role: str = "original",
    word_gap: float = 46,
    labels: list[str] | None = None,
    label_size: float = 20,
    show_matra: bool = True,
) -> tuple[str, tuple[float, float, float, float]]:
    fragments: list[str] = []
    cursor = x
    total_min_x = math.inf
    total_min_y = math.inf
    total_max_x = -math.inf
    total_max_y = -math.inf
    for idx, tokens in enumerate(words):
        layout = layout_units(display_units(tokens, role))
        min_x, min_y, max_x, max_y = strip_extent(layout)
        dx = cursor - min_x
        for unit in layout:
            fragments.append(render_unit(unit, dx, y))
        if show_matra:
            matra_line, matra_end = render_matra_line(min_x + dx, max_y + y + 12, total_matras(layout))
            fragments.append(matra_line)
            total_max_x = max(total_max_x, matra_end + 6)
        if labels:
            label_y = max_y + y + (32 if show_matra else 26)
            fragments.append(
                render_text(
                    (min_x + max_x) / 2 + dx,
                    label_y,
                    labels[idx],
                    label_size,
                    MUTED,
                    weight="600",
                    style="italic",
                    family=DEV_FONT,
                )
            )
            total_max_y = max(total_max_y, label_y + 10)
        total_min_x = min(total_min_x, min_x + dx)
        total_max_x = max(total_max_x, max_x + dx)
        total_min_y = min(total_min_y, min_y + y)
        total_max_y = max(total_max_y, max_y + y + (20 if show_matra else 0))
        cursor += (max_x - min_x) + word_gap
    return "\n  ".join(fragments), (total_min_x, total_min_y, total_max_x, total_max_y)


def defs() -> str:
    return (
        "<defs>"
        '<marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" '
        'orient="auto" markerUnits="strokeWidth">'
        f'<path d="M0,0 L9,4.5 L0,9 Z" fill="{MUTED}"/>'
        "</marker>"
        "</defs>"
    )


def svg_doc(width: float, height: float, body: str, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}">\n'
        f"<title>{esc(title)}</title>\n"
        f"{defs()}\n"
        '<rect width="100%" height="100%" fill="white"/>\n'
        f"{body}\n"
        "</svg>\n"
    )


def write_svg(name: str, width: float, height: float, body: str, title: str) -> None:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    out = BUILD_DIR / f"{name}.svg"
    out.write_text(svg_doc(width, height, body, title), encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO_ROOT)}")


def label_box(x: float, y: float, w: float, h: float, title: str, subtitle: str = "") -> str:
    parts = [
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="5" '
        f'fill="#f7f7f7" stroke="{STROKE}" stroke-width="1.2"/>',
        render_text(x + w / 2, y + h / 2 - (7 if subtitle else 0), title, 16, TEXT, weight="700"),
    ]
    if subtitle:
        parts.append(render_text(x + w / 2, y + h / 2 + 15, subtitle, 11, MUTED, style="italic"))
    return "\n  ".join(parts)


def fig_pipeline() -> None:
    items = [
        ("sonomers", "varṇāḥ"),
        ("dhātuḥ", "semantic atom"),
        ("śabda / kriyāpada", "molecule"),
        ("padam", "role-marked"),
        ("vākya", "assembly"),
    ]
    body: list[str] = [render_text(450, 34, "Assembly without loss", 24, TEXT, weight="700")]
    x0 = 50
    y = 88
    for i, (title, subtitle) in enumerate(items):
        x = x0 + i * 170
        body.append(label_box(x, y, 130, 76, title, subtitle))
        if i < len(items) - 1:
            body.append(render_arrow(x + 134, y + 38, x + 166, y + 38))
    sample, _ = render_strip([["k", "R"], ["k", "a", "r", "i", "S", "y", "a", "t", "i"]], 160, 230, "original", labels=["कृ", "करिष्यति"])
    body.append(sample)
    write_svg("building_vakya_pipeline", 900, 330, "\n".join(body), "Ch12 molecular assembly pipeline")


def fig_visual_key() -> None:
    body: list[str] = [render_text(380, 34, "Ch12 visual key", 24, TEXT, weight="700")]
    x = 60
    y = 145
    samples = [
        ("dhātuḥ atom", [["k", "R"]], "original"),
        ("head-bond", [["p", "r", "a"]], "head"),
        ("tail-bond", [["t", "R"]], "tail"),
        ("role-marker", [["A"]], "role"),
        ("nasal consonant", [["a", "M"]], "sentence"),
        ("visarga", [["a", "H"]], "sentence"),
    ]
    for idx, (label, words, role) in enumerate(samples):
        col = idx % 3
        row = idx // 3
        sx = x + col * 240
        sy = y + row * 170
        body.append(render_text(sx + 75, sy - 70, label, 16, TEXT, weight="700"))
        strip, _ = render_strip(words, sx + 32, sy, role, word_gap=30)
        body.append(strip)
    write_svg("building_vakya_visual_key", 760, 430, "\n".join(body), "Ch12 hexagon visual key")


def fig_kr_hlad() -> None:
    body: list[str] = [render_text(370, 34, "One flagship atom, one contrast atom", 24, TEXT, weight="700")]
    kr, _ = render_strip([["k", "R"]], 140, 135, "original", labels=["कृ  kṛ"])
    hlad, _ = render_strip([["h", "l", "A", "d"]], 430, 135, "original", labels=["ह्लाद्  hlād"])
    body.extend([kr, hlad])
    body.append(render_text(205, 255, "high deployment", 15, MUTED, style="italic"))
    body.append(render_text(520, 255, "specialized deployment", 15, MUTED, style="italic"))
    write_svg("building_vakya_kr_hlad", 740, 310, "\n".join(body), "Kṛ and hlād contrast atoms")


def fig_head_bonds() -> None:
    body: list[str] = [render_text(470, 32, "Head-bonds redirect the kṛ field", 24, TEXT, weight="700")]
    rows = [
        ("प्र + कृ", [["p", "r", "a"], ["k", "R"]], [["p", "r", "a", "k", "R", "t", "i"]], "prakṛti"),
        ("वि + कृ", [["v", "i"], ["k", "R"]], [["v", "i", "k", "R", "t", "i"]], "vikṛti"),
        ("सम् + कृ field", [["s", "a", "M"], ["k", "R"]], [["s", "a", "M", "s", "k", "R", "t", "i"]], "saṃskṛti"),
    ]
    y = 100
    for label, left_words, out_words, gloss in rows:
        body.append(render_text(78, y + 5, label, 17, TEXT, anchor="start", weight="700"))
        left, _ = render_strip(left_words, 210, y, "head", word_gap=25)
        body.append(left)
        body.append(render_arrow(420, y, 465, y))
        out, _ = render_strip(out_words, 500, y, "original", word_gap=25, labels=[gloss])
        body.append(out)
        y += 145
    write_svg("building_vakya_head_bonds", 940, 515, "\n".join(body), "Kṛ head-bond triptych")


def fig_tail_bonds() -> None:
    body: list[str] = [render_text(500, 32, "Tail-bonds stabilize molecule class", 24, TEXT, weight="700")]
    rows = [
        ("obligation", [["k", "A", "r", "y", "a"]], "kārya"),
        ("deed", [["k", "a", "r", "m", "a"]], "karma"),
        ("agent", [["k", "a", "r", "t", "R"]], "kartṛ"),
        ("refined formation", [["s", "a", "M", "s", "k", "R", "t", "i"]], "saṃskṛti"),
        ("refining act", [["s", "a", "M", "s", "k", "A", "r", "a"]], "saṃskāra"),
    ]
    y = 125
    for label, words, gloss in rows:
        body.append(render_text(70, y + 6, label, 15, MUTED, anchor="start", style="italic"))
        strip, _ = render_strip(words, 245, y, "original", word_gap=25, labels=[gloss])
        body.append(strip)
        y += 145
    write_svg("building_vakya_tail_bonds", 1000, 845, "\n".join(body), "Kṛ tail-bond molecules")


def fig_bonding_matrix() -> None:
    width = 980
    height = 500
    left = 35
    top = 82
    cell_w = 178
    cell_h = 92
    headers = ["head-bond", "state / formation", "act / mode", "obligation", "deed", "agent"]
    rows = [
        ("none", ["", "", "कार्य kārya", "कर्म karma", "कर्तृ kartṛ"]),
        ("प्र pra-", ["प्रकृति prakṛti", "प्रकार prakāra", "", "", ""]),
        ("वि vi-", ["विकृति vikṛti", "विकार vikāra", "", "", ""]),
        ("सम् sam-", ["संस्कृति saṃskṛti", "संस्कार saṃskāra", "", "", ""]),
    ]
    body: list[str] = [render_text(width / 2, 34, "The kṛ bonding matrix", 24, TEXT, weight="700")]
    for col, header in enumerate(headers):
        x = left + col * cell_w
        body.append(f'<rect x="{x}" y="{top}" width="{cell_w}" height="{cell_h * 0.72}" fill="#f0f0f0" stroke="{STROKE}" stroke-width="1"/>')
        body.append(render_text(x + cell_w / 2, top + cell_h * 0.36, header, 13, TEXT, weight="700"))
    for r, (head, cells) in enumerate(rows):
        y = top + cell_h * 0.72 + r * cell_h
        x = left
        body.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="#f7f7f7" stroke="{STROKE}" stroke-width="1"/>')
        body.append(render_text(x + cell_w / 2, y + cell_h / 2, head, 14, TEXT, weight="700"))
        for c, value in enumerate(cells):
            x = left + (c + 1) * cell_w
            fill = "#ffffff" if value else "#fbfbfb"
            body.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="{fill}" stroke="{STROKE}" stroke-width="1"/>')
            if value:
                parts = value.split(" ", 1)
                body.append(render_text(x + cell_w / 2, y + cell_h / 2 - 9, parts[0], 18, TEXT, family=DEV_FONT, weight="600"))
                if len(parts) > 1:
                    body.append(render_text(x + cell_w / 2, y + cell_h / 2 + 17, parts[1], 12, MUTED, style="italic"))
            else:
                body.append(render_text(x + cell_w / 2, y + cell_h / 2, "—", 18, "#aaaaaa"))
    write_svg("building_vakya_kr_bonding_matrix", width, height, "\n".join(body), "Kṛ bonding matrix")


def fig_rca_role_marker() -> None:
    body: list[str] = [render_text(420, 32, "A śabda becomes a padam", 24, TEXT, weight="700")]
    left, _ = render_strip([["R", "c"]], 105, 125, "original", labels=["ऋच्  ṛc"])
    marker, _ = render_strip([["A"]], 375, 125, "role", labels=["instrumental role-marker"])
    right, _ = render_strip([["R", "c", "A"]], 590, 125, "original", labels=["ऋचा  ṛcā"])
    body.extend([left, marker, right])
    body.append(render_text(315, 125, "+", 34, TEXT, weight="700"))
    body.append(render_arrow(450, 125, 520, 125))
    write_svg("building_vakya_rca_role_marker", 840, 250, "\n".join(body), "Ṛc to ṛcā role marker")


def fig_sentence_full_hex() -> None:
    body: list[str] = [render_text(760, 34, "यस्तन्न वेद किमृचा करिष्यति", 27, TEXT, family=DEV_FONT, weight="700")]
    words = [
        ["y", "a", "s", "t", "a", "n", "n", "a"],
        ["v", "e", "d", "a"],
        ["k", "i", "m", "R", "c", "A"],
        ["k", "a", "r", "i", "S", "y", "a", "t", "i"],
    ]
    labels = ["yastanna", "veda", "kimṛcā", "kariṣyati"]
    strip, extent = render_strip(words, 70, 145, "sentence", word_gap=72, labels=labels)
    body.append(strip)
    body.append(render_text(760, 290, "full sonomeric sentence experiment", 15, MUTED, style="italic"))
    width = max(1520, extent[2] + 80)
    write_svg("building_vakya_sentence_full_hex", width, 335, "\n".join(body), "Full hexagon sentence experiment")


def fig_vivimorphosis() -> None:
    body: list[str] = [render_text(540, 34, "Boundary crossing: apabhraṃśa / vivimorphosis", 24, TEXT, weight="700")]
    stages = [
        ("धातु", "dhātuḥ", [["d", "i", "v"]], "original"),
        ("शब्द", "śabda", [["d", "e", "v", "a", "H"]], "sentence"),
        ("बीज", "bīja", [["d", "e", "v"]], "seed"),
        ("अपशब्द", "apaśabda", [["d", "e", "u", "s"]], "root"),
    ]
    x = 60
    y = 150
    for idx, (dev, iast, words, role) in enumerate(stages):
        sx = x + idx * 255
        body.append(render_text(sx + 95, 83, dev, 22, TEXT, family=DEV_FONT, weight="700"))
        body.append(render_text(sx + 95, 108, iast, 13, MUTED, style="italic"))
        strip, _ = render_strip(words, sx + 40, y, role, word_gap=30)
        body.append(strip)
        if idx < len(stages) - 1:
            body.append(render_arrow(sx + 215, y, sx + 255, y))
    body.append(render_text(305, 263, "Sanskrit calibrant side", 15, MUTED, style="italic"))
    body.append(render_text(815, 263, "contact-language side", 15, MUTED, style="italic"))
    body.append(f'<line x1="570" y1="72" x2="570" y2="250" stroke="{DASH}" stroke-width="1.4" stroke-dasharray="6,5"/>')
    write_svg("building_vakya_vivimorphosis", 1080, 310, "\n".join(body), "Vivimorphosis boundary diagram")


def main() -> None:
    fig_pipeline()
    fig_visual_key()
    fig_kr_hlad()
    fig_head_bonds()
    fig_tail_bonds()
    fig_bonding_matrix()
    fig_rca_role_marker()
    fig_sentence_full_hex()
    fig_vivimorphosis()


if __name__ == "__main__":
    main()

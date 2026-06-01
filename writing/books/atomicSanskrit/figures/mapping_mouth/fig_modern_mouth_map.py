#!/usr/bin/env python3
"""Generate Ch8 modern speech-science mouth map.

This figure is intentionally Sanskrit-neutral. It shows the side-view mouth
and an extracted articulation arc using modern English terminology. Later Ch8
figures can reuse the arc geometry to show Sanskrit's selected grid.
"""

from __future__ import annotations

import html
import math
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUT = PROJECT_ROOT / "figures" / "build" / "mapping_mouth_modern_speech_map.svg"

LATIN_FONT = "Charter, Georgia, Times, serif"

TEXT = "#1a1a1a"
MUTED = "#555555"
LIGHT = "#f4f4f4"
MID = "#d9d9d9"
MOUTH = "#e7c79a"
MOUTH_DARK = "#b9834f"
TONGUE = "#777777"
TONGUE_DARK = "#333333"
STROKE = "#333333"
GUIDE = "#777777"
WHITE = "#ffffff"


@dataclass(frozen=True)
class Region:
    name: str
    start: float
    end: float
    target: tuple[float, float]
    selected: bool = False


REGIONS = [
    Region("glottal", 205, 218, (540, 465)),
    Region("pharyngeal", 218, 231, (520, 405)),
    Region("uvular", 231, 244, (465, 350)),
    Region("velar", 244, 258, (405, 324), selected=True),
    Region("palatal", 258, 273, (345, 298), selected=True),
    Region("retroflex", 273, 288, (296, 284), selected=True),
    Region("postalveolar", 288, 303, (255, 278)),
    Region("alveolar", 303, 318, (221, 281)),
    Region("dental", 318, 333, (191, 294), selected=True),
    Region("labiodental", 333, 346, (168, 307)),
    Region("bilabial", 346, 360, (145, 326), selected=True),
]


ARC_CX = 345
ARC_CY = 332
ARC_R_INNER = 228
ARC_R_OUTER = 254
ARC_LABEL_R = 284


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def polar(angle_deg: float, radius: float, cx: float = ARC_CX, cy: float = ARC_CY) -> tuple[float, float]:
    a = math.radians(angle_deg)
    return cx + radius * math.cos(a), cy - radius * math.sin(a)


def arc_path(r1: float, r2: float, start: float, end: float) -> str:
    x1, y1 = polar(start, r2)
    x2, y2 = polar(end, r2)
    x3, y3 = polar(end, r1)
    x4, y4 = polar(start, r1)
    large = 1 if abs(end - start) > 180 else 0
    return (
        f"M {x1:.1f},{y1:.1f} "
        f"A {r2:.1f},{r2:.1f} 0 {large} 0 {x2:.1f},{y2:.1f} "
        f"L {x3:.1f},{y3:.1f} "
        f"A {r1:.1f},{r1:.1f} 0 {large} 1 {x4:.1f},{y4:.1f} Z"
    )


def path(d: str, fill: str = "none", stroke: str = STROKE, width: float = 1.5, **attrs) -> str:
    extra = " ".join(f'{k.replace("_", "-")}="{esc(v)}"' for k, v in attrs.items())
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>'


def line(x1: float, y1: float, x2: float, y2: float, color: str = STROKE, width: float = 1.5, **attrs) -> str:
    extra = " ".join(f'{k.replace("_", "-")}="{esc(v)}"' for k, v in attrs.items())
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" {extra}/>'
    )


def circle(cx: float, cy: float, r: float, fill: str = WHITE, stroke: str = STROKE, width: float = 1.2) -> str:
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def rect(x: float, y: float, w: float, h: float, fill: str = WHITE, stroke: str = STROKE, width: float = 1.2, rx: float = 0) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
    )


def text(
    x: float,
    y: float,
    content: str,
    size: float = 14,
    fill: str = TEXT,
    anchor: str = "middle",
    weight: str = "400",
    style: str = "normal",
    family: str = LATIN_FONT,
    rotate: float | None = None,
) -> str:
    transform = f' transform="rotate({rotate:.1f} {x:.1f} {y:.1f})"' if rotate is not None else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" font-style="{style}" text-anchor="{anchor}" '
        f'dominant-baseline="middle" fill="{fill}"{transform}>{esc(content)}</text>'
    )


def draw_head() -> list[str]:
    parts: list[str] = []

    # Head/neck mass.
    parts.append(path(
        "M 155 284 C 202 222, 292 218, 384 248 "
        "C 451 270, 514 320, 557 388 "
        "C 587 436, 590 509, 558 566 "
        "L 407 566 C 377 526, 353 487, 314 463 "
        "C 276 438, 220 438, 178 414 "
        "C 136 390, 121 334, 155 284 Z",
        fill=MOUTH,
        stroke="none",
    ))
    # Back-of-head / neck shadow.
    parts.append(path(
        "M 486 292 C 535 338, 570 400, 575 469 "
        "C 578 510, 565 543, 546 566 L 475 566 "
        "C 498 502, 499 398, 486 292 Z",
        fill=MOUTH_DARK,
        stroke="none",
        opacity="0.75",
    ))

    # Nose / lips profile.
    parts.append(path(
        "M 134 326 C 112 337, 103 356, 113 373 "
        "C 127 366, 144 358, 158 358 "
        "C 147 377, 147 389, 161 398 "
        "C 144 404, 132 419, 139 436 "
        "C 159 432, 179 421, 194 408",
        fill="none",
        stroke=MOUTH_DARK,
        width=8,
        stroke_linecap="round",
        stroke_linejoin="round",
    ))

    # Oral and nasal cavities.
    parts.append(path("M 170 322 C 232 279, 349 283, 449 327", stroke=WHITE, width=18, stroke_linecap="round"))
    parts.append(path("M 174 369 C 252 325, 360 328, 443 382", stroke=WHITE, width=30, stroke_linecap="round"))
    parts.append(path("M 184 406 C 241 383, 338 384, 418 422", stroke=MOUTH, width=22, stroke_linecap="round"))

    # Tongue.
    parts.append(path(
        "M 176 423 C 228 386, 312 378, 389 409 "
        "C 361 438, 296 451, 230 440 "
        "C 202 435, 184 430, 176 423 Z",
        fill=TONGUE,
        stroke=TONGUE_DARK,
        width=1.5,
    ))

    # Hard-palate contour and airway guide.
    parts.append(path("M 181 360 C 242 313, 344 315, 438 365", stroke=STROKE, width=2.0))
    parts.append(path("M 208 471 C 262 450, 343 451, 430 485", stroke=MOUTH_DARK, width=4.0, stroke_linecap="round"))

    # Vocal-cord/glottal marker.
    parts.append(path("M 489 508 C 503 497, 526 497, 541 508", stroke=STROKE, width=2.2, fill="none"))
    parts.append(path("M 493 518 C 510 507, 528 507, 539 518", stroke=STROKE, width=2.2, fill="none"))

    return parts


def draw_arc() -> list[str]:
    parts: list[str] = []

    fills = ["#efefef", "#e8e8e8"]
    for idx, region in enumerate(REGIONS):
        fill = fills[idx % 2]
        parts.append(path(arc_path(ARC_R_INNER, ARC_R_OUTER, region.start, region.end), fill=fill, stroke=WHITE, width=1.1))

        # Boundary guide from arc to anatomical target.
        mid = (region.start + region.end) / 2
        sx, sy = polar(mid, ARC_R_INNER - 6)
        tx, ty = region.target
        dash = "2,4" if not region.selected else "2,3"
        parts.append(line(sx, sy, tx, ty, color=GUIDE, width=1.2 if region.selected else 1.0, stroke_dasharray=dash, opacity="0.85"))
        parts.append(circle(tx, ty, 3.5 if region.selected else 2.8, fill=TEXT if region.selected else WHITE, stroke=TEXT, width=1.0))

        lx, ly = polar(mid, ARC_LABEL_R)
        rotation = 90 - mid
        if rotation < -85:
            rotation += 180
        parts.append(text(lx, ly, region.name, size=13, fill=TEXT, anchor="middle", rotate=rotation))

    # Inner and outer arc strokes make the extracted arc reusable visually.
    start = REGIONS[0].start
    end = REGIONS[-1].end
    x1, y1 = polar(start, ARC_R_OUTER)
    x2, y2 = polar(end, ARC_R_OUTER)
    x3, y3 = polar(start, ARC_R_INNER)
    x4, y4 = polar(end, ARC_R_INNER)
    parts.append(path(f"M {x1:.1f},{y1:.1f} A {ARC_R_OUTER},{ARC_R_OUTER} 0 0 0 {x2:.1f},{y2:.1f}", stroke=STROKE, width=1.5))
    parts.append(path(f"M {x3:.1f},{y3:.1f} A {ARC_R_INNER},{ARC_R_INNER} 0 0 0 {x4:.1f},{y4:.1f}", stroke=STROKE, width=1.1))

    # Subtle note: five filled dots correspond to Sanskrit-selected regions, but no special color.
    parts.append(rect(63, 612, 340, 34, fill="#f7f7f7", stroke="#dddddd", width=0.8, rx=3))
    parts.append(circle(82, 629, 3.5, fill=TEXT, stroke=TEXT, width=1.0))
    parts.append(text(98, 630, "filled dots mark the five regions Sanskrit selects later", size=12, fill=MUTED, anchor="start"))

    return parts


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    width = 690
    height = 660
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}pt" height="{height}pt" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="{WHITE}"/>',
        text(345, 28, "Modern speech-science mouth map", size=22, weight="700"),
        text(345, 52, "articulation regions along the vocal tract", size=14, fill=MUTED),
    ]
    parts.extend(draw_arc())
    parts.extend(draw_head())
    parts.append("</svg>")

    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()

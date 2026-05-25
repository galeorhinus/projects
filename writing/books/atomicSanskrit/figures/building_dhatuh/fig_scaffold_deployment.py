#!/usr/bin/env python3
"""Generate scaffold actual-use share figure as SVG/PDF.

This script writes SVG directly instead of using matplotlib. The project can
then build the figure even when the local NumPy/matplotlib installation is out
of sync.
"""

from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SUMMARY = PROJECT_ROOT / "analysis" / "ganah" / "data" / "derived" / "scaffold_reactivity_summary.csv"
OUT_DIR = PROJECT_ROOT / "figures" / "build"
OUT_SVG = OUT_DIR / "building_dhatuh_scaffold_deployment.svg"
OUT_PDF = OUT_DIR / "building_dhatuh_scaffold_deployment.pdf"

TOP_TEN = [
    "CV1C",
    "CCV1C",
    "CV1CC",
    "CV2CV1",
    "CV2C",
    "CV2",
    "V1C",
    "CV1",
    "CV1CV2",
    "CCV2",
]

METRICS = [
    ("inventory_share_pct", "inventory", "#222222", ""),
    ("text_visible_dhatu_share_pct", "dhātavaḥ in texts", "#666666", "diagonal"),
    ("valency_share_pct", "combinations", "#999999", ""),
    ("token_share_pct", "occurrences", "#c9c9c9", "backdiagonal"),
]


def esc(text: object) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def load_data() -> list[tuple[str, dict[str, float]]]:
    if not SUMMARY.exists():
        raise SystemExit(f"missing input: {SUMMARY}")
    by_scaffold: dict[str, dict[str, float]] = {}
    with SUMMARY.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            by_scaffold[row["racana_scaffold"]] = {
                key: float(row[key])
                for key, _label, _color, _pattern in METRICS
            }

    data: list[tuple[str, dict[str, float]]] = []
    for scaffold in TOP_TEN:
        data.append((scaffold, by_scaffold[scaffold]))

    tail = {
        key: max(0.0, 100.0 - sum(values[key] for _label, values in data))
        for key, _label, _color, _pattern in METRICS
    }
    data.append(("tail", tail))
    return data


def pattern_id(kind: str) -> str:
    return {
        "diagonal": "diag",
        "backdiagonal": "backdiag",
    }.get(kind, "")


def render() -> str:
    data = load_data()

    width = 920
    height = 575
    margin_left = 86
    margin_right = 32
    margin_top = 58
    margin_bottom = 70
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom
    max_pct = 45.0
    row_gap = plot_height / len(data)
    bar_h = 8
    offsets = [-15, -5, 5, 15]

    def x_for(value: float) -> float:
        return margin_left + (value / max_pct) * plot_width

    parts: list[str] = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    parts.append("<defs>")
    parts.append('<pattern id="diag" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(45)">')
    parts.append('<line x1="0" y1="0" x2="0" y2="6" stroke="#222222" stroke-width="1"/>')
    parts.append("</pattern>")
    parts.append('<pattern id="backdiag" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(-45)">')
    parts.append('<line x1="0" y1="0" x2="0" y2="6" stroke="#222222" stroke-width="1"/>')
    parts.append("</pattern>")
    parts.append("</defs>")
    parts.append('<rect x="0" y="0" width="100%" height="100%" fill="white"/>')

    font = "Charter, Adobe Devanagari, DejaVu Serif, serif"
    small_font = "font-size:11px;font-family:" + font
    label_font = "font-size:13px;font-family:" + font

    for pct in range(0, 46, 5):
        x = x_for(pct)
        stroke = "#d8d8d8" if pct else "#111111"
        parts.append(f'<line x1="{x:.1f}" y1="{margin_top - 4}" x2="{x:.1f}" y2="{height - margin_bottom}" stroke="{stroke}" stroke-width="0.7"/>')
        parts.append(f'<text x="{x:.1f}" y="{height - margin_bottom + 22}" text-anchor="middle" style="{small_font}">{pct}</text>')

    for row_index, (scaffold, values) in enumerate(data):
        row_center = margin_top + row_index * row_gap + row_gap / 2
        parts.append(f'<text x="{margin_left - 14}" y="{row_center + 4:.1f}" text-anchor="end" style="{label_font}">{esc(scaffold)}</text>')
        for (key, metric_label, color, pattern), offset in zip(METRICS, offsets):
            value = values[key]
            bar_width = max(0.0, x_for(value) - margin_left)
            y = row_center + offset - bar_h / 2
            fill = color
            parts.append(f'<rect x="{margin_left}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_h}" fill="{fill}" stroke="#111111" stroke-width="0.45"/>')
            pid = pattern_id(pattern)
            if pid:
                parts.append(f'<rect x="{margin_left}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_h}" fill="url(#{pid})" opacity="0.45"/>')
            if value >= 3.5:
                parts.append(f'<text x="{x_for(value) + 5:.1f}" y="{y + bar_h - 0.5:.1f}" style="{small_font}">{value:.1f}%</text>')

    legend_x = margin_left
    legend_y = 24
    for i, (_key, label, color, pattern) in enumerate(METRICS):
        x = legend_x + i * 172
        parts.append(f'<rect x="{x}" y="{legend_y - 11}" width="18" height="8" fill="{color}" stroke="#111111" stroke-width="0.45"/>')
        pid = pattern_id(pattern)
        if pid:
            parts.append(f'<rect x="{x}" y="{legend_y - 11}" width="18" height="8" fill="url(#{pid})" opacity="0.45"/>')
        parts.append(f'<text x="{x + 25}" y="{legend_y - 3}" style="{small_font}">{esc(label)}</text>')

    parts.append(f'<text x="{margin_left + plot_width / 2:.1f}" y="{height - 18}" text-anchor="middle" style="{label_font}">Share of total (%)</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    OUT_DIR.mkdir(exist_ok=True)
    OUT_SVG.write_text(render(), encoding="utf-8")
    print(f"Wrote {OUT_SVG.relative_to(PROJECT_ROOT)}")

    converter = shutil.which("rsvg-convert")
    if converter:
        subprocess.run([converter, "-f", "pdf", "-o", str(OUT_PDF), str(OUT_SVG)], check=True)
        print(f"Wrote {OUT_PDF.relative_to(PROJECT_ROOT)}")
    else:
        print("WARNING: rsvg-convert not found; PDF not written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

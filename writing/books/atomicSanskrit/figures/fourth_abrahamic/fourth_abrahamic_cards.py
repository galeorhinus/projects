#!/usr/bin/env python3
"""Generate the seven unnumbered comparison cards used in Chapter 4."""

from __future__ import annotations

import html
import os
import re
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT_ROOT / "figures/fourth_abrahamic"
FIGURES_DIR = PROJECT_ROOT / "figures"

WIDTH = 1200
MARGIN = 34
LABEL_X = 48
LABEL_WIDTH = 218
TEXT_X = 292
TEXT_WIDTH_CHARS = 70
FONT_SIZE = 29
LINE_HEIGHT = 36
ROW_PAD = 15
TOP_PAD = 48
BOTTOM_PAD = 14

INK = "#29251f"
MUTED = "#4a4136"
GOLD = "#9a7833"
PAPER = "#f7f4ed"
GRID = "#cfc6b5"
FONT = "STIX Two Text, Georgia, serif"

LABEL_STYLES = {
    "Judaism": ("#ede5d1", INK),
    "Christianity": ("#d9caa8", INK),
    "Islam": ("#ad9b76", "#ffffff"),
    "Progressivism": ("#4a4033", "#ffffff"),
}

CARDS = [
    (
        "01",
        "chosen_community",
        [
            ("Judaism", "Israel, the chosen people."),
            ("Christianity", "The Church and the saved."),
            ("Islam", "The *ummat* or *ummah*, the community of believers."),
            (
                "Progressivism",
                "The academy, civil society, certified intellectuals, and the self-declared enlightened, including the contemporary “woke.”",
            ),
        ],
    ),
    (
        "02",
        "authorized_doctrine",
        [
            ("Judaism", "The Torah and Halakha."),
            (
                "Christianity",
                "The Bible, creeds, and authorized ecclesiastical interpretation.",
            ),
            (
                "Islam",
                "The Quran, Hadith, and the schools of jurisprudence built around them.",
            ),
            (
                "Progressivism",
                "Secular consensus, linear upward progress, and discipline-specific articles of faith such as PIE and the Racial Arya Thesis.",
            ),
        ],
    ),
    (
        "03",
        "boundary",
        [
            ("Judaism", "Israel and the nations; Jew and Gentile."),
            (
                "Christianity",
                "Believer and heathen; orthodox and heretic; saved and damned.",
            ),
            (
                "Islam",
                "Believer and *kāfir*; in classical jurisprudence, *dār al-Islām* and *dār al-ḥarb*.",
            ),
            (
                "Progressivism",
                "Rational and objective versus mythological and unscientific; mainstream versus fringe; expert versus denier.",
            ),
        ],
    ),
    (
        "04",
        "expansionary_form",
        [
            (
                "Judaism",
                "The covenant joins a people to promised territory and collective survival. It does not impose a universal conversion mandate; the structure is later globalized.",
            ),
            (
                "Christianity",
                "The Great Commission commands universal evangelization. Missionary expansion repeatedly joined imperial rule, crusade, and colonial administration.",
            ),
            (
                "Islam",
                "*Daʿwah* extends the doctrine through invitation and instruction; *jihād* supplies the category under which struggle and historical conquest were authorized.",
            ),
            (
                "Progressivism",
                "Western education, development policy, credential systems, and universalized academic categories carry the doctrine into civilizations that possess their own categories.",
            ),
        ],
    ),
    (
        "05",
        "origin",
        [
            ("Judaism", "Genesis: God creates the heavens and the earth."),
            (
                "Christianity",
                "Creation through the Word; all things begin through Christ.",
            ),
            ("Islam", "Allah commands creation: “Be,” and it is."),
            (
                "Progressivism",
                "The Big Bang: time and space emerge under impersonal physical law.",
            ),
        ],
    ),
    (
        "06",
        "utopia",
        [
            ("Judaism", "The Messianic Age and promised restoration."),
            (
                "Christianity",
                "The Kingdom of Heaven, Second Coming, and New Jerusalem.",
            ),
            ("Islam", "*Jannah*, paradise for the faithful."),
            (
                "Progressivism",
                "Total emancipation, perfect equity, technological transcendence, or the end of history.",
            ),
        ],
    ),
    (
        "07",
        "apocalypse",
        [
            (
                "Judaism",
                "The Day of the Lord, judgment, and defeat of those obstructing restoration.",
            ),
            (
                "Christianity",
                "Revelation, final judgment, and destruction before the perfected replacement.",
            ),
            (
                "Islam",
                "*Yawm al-Qiyāmah*, judgment, and punishment in *Jahannam*.",
            ),
            (
                "Progressivism",
                "Climate catastrophe becomes judgment day. One prescribed “solution” promises salvation; anyone who questions it becomes a denier.",
            ),
        ],
    ),
]


def styled_words(value: str) -> list[tuple[str, bool]]:
    """Return whitespace-delimited words while retaining *italic* spans."""
    words: list[tuple[str, bool]] = []
    italic = False
    for part in re.split(r"(\*)", value):
        if part == "*":
            italic = not italic
            continue
        for word in part.split():
            if words and re.fullmatch(r"[,.;:!?]+", word):
                previous, previous_italic = words[-1]
                words[-1] = (previous + word, previous_italic)
            else:
                words.append((word, italic))
    return words


def wrap_styled(value: str) -> list[list[tuple[str, bool]]]:
    lines: list[list[tuple[str, bool]]] = []
    current: list[tuple[str, bool]] = []
    width = 0
    for word, italic in styled_words(value):
        extra = len(word) + (1 if current else 0)
        if current and width + extra > TEXT_WIDTH_CHARS:
            lines.append(current)
            current = []
            width = 0
        current.append((word, italic))
        width += len(word) + (1 if width else 0)
    if current:
        lines.append(current)
    return lines


def text_line(x: int, y: int, words: list[tuple[str, bool]]) -> str:
    spans: list[str] = []
    for index, (word, italic) in enumerate(words):
        value = ("" if index == 0 else " ") + word
        style = ' font-style="italic"' if italic else ""
        spans.append(f"<tspan{style}>{html.escape(value)}</tspan>")
    return (
        f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{FONT_SIZE}" '
        f'fill="{MUTED}">{"".join(spans)}</text>'
    )


def render_card(number: str, slug: str, rows: list[tuple[str, str]]) -> Path:
    wrapped = [(label, wrap_styled(description)) for label, description in rows]
    row_heights = [max(55, len(lines) * LINE_HEIGHT + ROW_PAD) for _, lines in wrapped]
    height = TOP_PAD + sum(row_heights) + BOTTOM_PAD

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" '
            f'width="4.8in" height="{4.8 * height / WIDTH:.3f}in" '
            'preserveAspectRatio="xMidYMid meet" xml:space="preserve">'
        ),
        f'<rect width="{WIDTH}" height="{height}" fill="{PAPER}"/>',
        (
            f'<text x="{WIDTH - MARGIN}" y="34" text-anchor="end" '
            f'font-family="{FONT}" font-size="27" fill="{GOLD}">{number}</text>'
        ),
    ]

    y = TOP_PAD
    for (label, lines), row_height in zip(wrapped, row_heights):
        label_fill, label_ink = LABEL_STYLES[label]
        parts.append(
            f'<rect x="{MARGIN}" y="{y + 3}" width="{LABEL_WIDTH}" height="40" '
            f'rx="2" fill="{label_fill}"/>'
        )
        parts.append(
            f'<text x="{LABEL_X}" y="{y + 32}" font-family="{FONT}" font-size="28" '
            f'font-weight="700" fill="{label_ink}">{label}</text>'
        )
        line_y = y + 31
        for line in lines:
            parts.append(text_line(TEXT_X, line_y, line))
            line_y += LINE_HEIGHT
        y += row_height

    parts.extend(
        [
            (
                f'<line x1="{MARGIN}" y1="{height - 1}" x2="{WIDTH - MARGIN}" '
                f'y2="{height - 1}" stroke="{GRID}" stroke-width="1"/>'
            ),
            "</svg>",
        ]
    )

    source = OUT_DIR / f"fourth_abrahamic_{slug}_card.from-py.svg"
    source.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return source


def promote_and_preview(source: Path) -> None:
    figure_python = PROJECT_ROOT / ".venv-figures/bin/python3"
    python = str(figure_python) if figure_python.exists() else sys.executable
    env = {**os.environ, "PYTHONPATH": str(FIGURES_DIR)}
    subprocess.run(
        [python, "-m", "_shared.lineage", "promote", str(source)],
        cwd=PROJECT_ROOT,
        env=env,
        check=True,
    )
    canonical = source.with_name(source.name.replace(".from-py.svg", ".svg"))
    preview = canonical.with_suffix(".png")
    subprocess.run(
        ["rsvg-convert", "-w", "1800", "-o", str(preview), str(canonical)],
        check=True,
    )


def main() -> None:
    for number, slug, rows in CARDS:
        source = render_card(number, slug, rows)
        promote_and_preview(source)
        print(source.relative_to(PROJECT_ROOT))


if __name__ == "__main__":
    main()

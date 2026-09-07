#!/usr/bin/env python3
"""Render the complete Designed Variations record as book-width SVGs."""

from __future__ import annotations

import csv
import html
import re
import subprocess
import sys
import textwrap
from collections import OrderedDict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MASTER = (
    PROJECT_ROOT
    / "working/10_active/as_vaidika_laukika_designed_variations_master.csv"
)
OUT_DIR = PROJECT_ROOT / "figures/vaidika_laukika"
LINEAGE_DIR = PROJECT_ROOT / "figures"

WIDTH = 1200
MARGIN = 34
TOP_PAD = 22
BOTTOM_PAD = 22

INK = "#29251f"
MUTED = "#6e675d"
GOLD = "#9d7c36"
PAPER = "#f7f4ed"
GRID = "#cfc6b5"
OPEN = "#8b8377"
RED = "#8b4b3d"

LATIN_FONT = "STIX Two Text, Georgia, serif"
IAST_VOWELS = {
    "ai": ("ऐ", "ै"),
    "au": ("औ", "ौ"),
    "a": ("अ", ""),
    "ā": ("आ", "ा"),
    "i": ("इ", "ि"),
    "ī": ("ई", "ी"),
    "u": ("उ", "ु"),
    "ū": ("ऊ", "ू"),
    "ṛ": ("ऋ", "ृ"),
    "ṝ": ("ॠ", "ॄ"),
    "ḷ": ("ऌ", "ॢ"),
    "e": ("ए", "े"),
    "o": ("ओ", "ो"),
}
IAST_CONSONANTS = {
    "kh": "ख",
    "gh": "घ",
    "ch": "छ",
    "jh": "झ",
    "ṭh": "ठ",
    "ḍh": "ढ",
    "th": "थ",
    "dh": "ध",
    "ph": "फ",
    "bh": "भ",
    "k": "क",
    "g": "ग",
    "ṅ": "ङ",
    "c": "च",
    "j": "ज",
    "ñ": "ञ",
    "ṭ": "ट",
    "ḍ": "ड",
    "ṇ": "ण",
    "t": "त",
    "d": "द",
    "n": "न",
    "p": "प",
    "b": "ब",
    "m": "म",
    "y": "य",
    "r": "र",
    "l": "ल",
    "v": "व",
    "ś": "श",
    "ṣ": "ष",
    "s": "स",
    "h": "ह",
}
IAST_TOKENS = sorted(
    [*IAST_VOWELS, *IAST_CONSONANTS], key=len, reverse=True
)
SANSKRIT_ITALIC_TERMS = {"pragṛhya", "vibhakti"}

GROUP_SPECS = [
    ("SG", 29),
    ("DU", 12),
    ("PL", 21),
    ("CL", 10),
    ("NU", 7),
    ("AC", 4),
]


def clean_markdown(value: str) -> str:
    value = re.sub(r"<br\s*/?>", " ", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("***", "").replace("**", "").replace("`", "")
    value = value.replace("*", "")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def iast_word_to_devanagari(value: str) -> str:
    """Transliterate one IAST form used in the inventory."""
    prefix = "-" if value.startswith("-") else ""
    source = value[1:] if prefix else value
    source = source.lower()
    tokens: list[str] = []
    index = 0
    while index < len(source):
        if source[index] in {"ṃ", "ṁ", "ḥ", "'"}:
            tokens.append(source[index])
            index += 1
            continue
        token = next(
            (candidate for candidate in IAST_TOKENS if source.startswith(candidate, index)),
            None,
        )
        if token is None:
            return value
        tokens.append(token)
        index += len(token)

    output: list[str] = []
    for index, token in enumerate(tokens):
        if not token:
            continue
        if token in IAST_VOWELS:
            output.append(IAST_VOWELS[token][0])
            continue
        if token in {"ṃ", "ṁ"}:
            output.append("ं")
            continue
        if token == "ḥ":
            output.append("ः")
            continue
        if token == "'":
            output.append("ऽ")
            continue

        output.append(IAST_CONSONANTS[token])
        following = tokens[index + 1] if index + 1 < len(tokens) else None
        if following in IAST_VOWELS:
            output.append(IAST_VOWELS[following][1])
            tokens[index + 1] = ""
        elif following not in {"ṃ", "ṁ", "ḥ"}:
            output.append("्")
    return prefix + "".join(output)


def iast_phrase_to_devanagari(value: str) -> str:
    pattern = re.compile(r"-?[A-Za-zāīūṛṝḷṅñṭḍṇśṣṃṁḥ]+")
    return pattern.sub(lambda match: iast_word_to_devanagari(match.group()), value)


def devanagari_only(value: str) -> str:
    """Render marked Sanskrit forms in Devanagari without IAST duplication."""
    protected: dict[str, str] = {}

    def hold(rendered: str) -> str:
        key = f"@@PAIR{len(protected)}@@"
        protected[key] = rendered
        return key

    def render_span(content: str) -> str:
        plain = clean_markdown(content)
        if re.search(r"[\u0900-\u097F]", plain):
            return re.sub(r"\s*\([^()]*\)", "", plain).strip()
        if re.fullmatch(r"[-/,. ;A-Za-zāīūṛṝḷṅñṭḍṇśṣṃṁḥ]+", plain):
            return iast_phrase_to_devanagari(plain)
        return plain

    value = re.sub(r"\*\*\*(.+?)\*\*\*", lambda m: hold(render_span(m.group(1))), value)
    value = re.sub(
        r"(?<!\*)\*\*(?!\*)(.+?)(?<!\*)\*\*(?!\*)",
        lambda m: hold(render_span(m.group(1))),
        value,
    )

    def render_single(match: re.Match[str]) -> str:
        plain = clean_markdown(match.group(1))
        if (
            plain.lower() in SANSKRIT_ITALIC_TERMS
            or re.fullmatch(r"[-/,. ;a-zāīūṛṝḷṅñṭḍṇśṣṃṁḥ]+", plain)
        ):
            return hold(iast_phrase_to_devanagari(plain))
        return plain

    value = re.sub(
        r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", render_single, value
    )
    for key, rendered in protected.items():
        value = value.replace(key, rendered)
    value = re.sub(
        r"-?[A-Za-zāīūṛṝḷṅñṭḍṇśṣṃṁḥ]*[āīūṛṝḷṅñṭḍṇśṣṃṁḥ][A-Za-zāīūṛṝḷṅñṭḍṇśṣṃṁḥ]*",
        lambda match: iast_word_to_devanagari(match.group()),
        value,
    )
    return value


def wrapped(value: str, width: int, *, scripts: bool = False) -> list[str]:
    if scripts:
        value = devanagari_only(value)
    value = clean_markdown(value)
    if not value:
        return []
    return textwrap.wrap(
        value,
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    )


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text(
    x: float,
    y: float,
    value: str,
    *,
    size: int = 30,
    color: str = INK,
    weight: int = 400,
    anchor: str = "start",
    italic: bool = False,
    deva: bool = False,
) -> str:
    # Canonical cards outline every run. STIX supplies the English shapes;
    # the shared promotion helper substitutes Adobe Devanagari for Devanagari.
    family = LATIN_FONT
    style = "italic" if italic else "normal"
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{esc(family)}" '
        f'font-size="{size}" font-weight="{weight}" font-style="{style}" '
        f'fill="{color}" text-anchor="{anchor}" data-outline-all="true">'
        f'{esc(value)}</text>'
    )


def evidence_label(row: dict[str, str]) -> str:
    evidence = clean_markdown(row["evidence"])
    labels = []
    if "PASSAGE" in evidence:
        labels.append("passage checked")
    if "FUNCTION" in evidence:
        labels.append("function shown")
    if not labels:
        labels.append("form recorded")
    if "OPEN" in evidence:
        labels.append("question open")
    return " · ".join(labels)


def prevalence_label(row: dict[str, str]) -> str:
    status = row["plot_status"]
    unit = (row["unit"] or "measure").replace("_", " ")
    numerator = row["numerator"]
    denominator = row["denominator"]
    percentage = row["percentage"]
    relation = row["relation"]
    grade = row["grade"]
    if status == "unknown" or relation in {
        "unknown",
        "source_corpus_conflict",
        "source_annotation_conflict",
    }:
        return f"open · grade {grade}"
    if status == "no_plot" and not numerator:
        return f"open · grade {grade}"
    if percentage:
        prefix = ""
        if relation == "upper_bound":
            prefix = "<"
        elif relation == "lower_bound":
            prefix = ">"
        elif relation in {"approximate", "approximate_counts"}:
            prefix = "≈"
        ratio = (
            f" ({numerator}/{denominator} {unit})"
            if numerator and denominator
            else f" {unit}"
        )
        return f"{prefix}{percentage}%{ratio} · grade {grade}"
    if numerator:
        if numerator == "1" and unit.endswith("s"):
            unit = unit[:-1]
        qualifier = "≈" if relation.startswith("approximate") else ""
        return f"{qualifier}{numerator} {unit} · grade {grade}"
    if status == "zero":
        return f"0 {unit} · grade {grade}"
    return f"open · grade {grade}"


def contribution_label(row: dict[str, str]) -> str:
    codes = re.findall(
        r"\b(?:SON|MAT|SVR|REL|ARR|SEM|RES|REC|AUD|FUN)\b",
        clean_markdown(row["confirmed_dv"]),
    )
    return " · ".join(dict.fromkeys(codes)) if codes else "open"


def visible_prevalence(subrows: list[dict[str, str]]) -> str:
    labels = [
        prevalence_label(row)
        for row in subrows
        if row["plot_status"] != "duplicate"
    ]
    return " | ".join(labels) if labels else "open"


def load_master() -> OrderedDict[str, list[dict[str, str]]]:
    grouped: OrderedDict[str, list[dict[str, str]]] = OrderedDict()
    with MASTER.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            grouped.setdefault(row["row_id"], []).append(row)
    if len(grouped) != 83:
        raise ValueError(f"Expected 83 grouped rows, found {len(grouped)}")
    return grouped


def record_lines(
    subrows: list[dict[str, str]],
) -> list[tuple[str, str, int, str, bool, int]]:
    row = subrows[0]
    records: list[tuple[str, str, int, str, bool, int]] = []

    class_lines = wrapped(row["ending_or_word_class"], 54, scripts=True) or ["Unlabelled class"]
    for index, line in enumerate(class_lines):
        records.append(("class", line, 31, INK, True, 38 if index == 0 else 35))

    relation = row["vibhakti_or_operation"] or row["category_level"]
    for line in wrapped(f"Relation: {relation}", 92, scripts=True):
        records.append(("detail", line, 27, MUTED, True, 33))
    vaidika = re.sub(r"^Vedic\s+", "", row["vaidika_form_or_range"])
    for line in wrapped(f"वैदिक: {vaidika}", 82, scripts=True):
        records.append(("detail", line, 29, INK, True, 35))
    laukika = row["laukika_form_or_range"] or "No separate laukika form recorded"
    laukika = re.sub(r"^Laukika\s+", "", laukika)
    for line in wrapped(f"लौकिक: {laukika}", 82, scripts=True):
        records.append(("detail", line, 29, INK, True, 35))

    qualification = clean_markdown(row["qualification"])
    if qualification and qualification not in {"—", "N/A"}:
        for line in wrapped(f"Qualification: {qualification}", 94, scripts=True):
            records.append(("qualification", line, 26, RED, False, 32))

    summary = (
        f"Contribution: {contribution_label(row)}   ·   "
        f"Evidence: {evidence_label(row)}"
    )
    for line in wrapped(summary, 98):
        records.append(("meta", line, 26, GOLD, False, 32))
    for line in wrapped(f"Prevalence: {visible_prevalence(subrows)}", 98, scripts=True):
        records.append(("meta", line, 25, MUTED, False, 31))
    return records


def record_height(lines: list[tuple[str, str, int, str, bool, int]]) -> int:
    return TOP_PAD + sum(item[5] for item in lines) + BOTTOM_PAD


def render_card(
    row_id: str,
    grouped: OrderedDict[str, list[dict[str, str]]],
) -> Path:
    lines = record_lines(grouped[row_id])
    height = record_height(lines)
    filename = f"designed_variation_{row_id.lower().replace('-', '_')}"
    description = " | ".join(value for _, value, _, _, _, _ in lines)

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="4.75in" '
            f'height="{height / WIDTH * 4.75:.3f}in" viewBox="0 0 {WIDTH} {height}">'
        ),
        f'<title>Designed variation {esc(row_id)}</title>',
        f'<desc>{esc(description)}</desc>',
        f'<rect width="{WIDTH}" height="{height}" fill="{PAPER}"/>',
        (
            f'<line x1="{MARGIN}" y1="1" x2="{WIDTH - MARGIN}" y2="1" '
            f'stroke="{GOLD}" stroke-width="3"/>'
        ),
        text(
            WIDTH - MARGIN,
            TOP_PAD + 25,
            row_id,
            size=27,
            color=GOLD,
            weight=400,
            anchor="end",
        ),
    ]

    cursor = TOP_PAD + 25
    for role, value, size, color, deva, line_height in lines:
        parts.append(
            text(
                MARGIN,
                cursor,
                value,
                size=size,
                color=color,
                weight=400,
                italic=False,
                deva=deva,
            )
        )
        cursor += line_height
    parts.append(
        f'<line x1="{MARGIN}" y1="{height - 1}" x2="{WIDTH - MARGIN}" y2="{height - 1}" '
        f'stroke="{GRID}" stroke-width="1"/>'
    )
    parts.append("</svg>")

    source = OUT_DIR / f"{filename}.from-py.svg"
    source.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return source


def promote_and_preview(source: Path) -> tuple[Path, Path]:
    env = {"PYTHONPATH": str(LINEAGE_DIR)}
    subprocess.run(
        [sys.executable, "-m", "_shared.lineage", "promote", str(source)],
        cwd=PROJECT_ROOT,
        env={**__import__("os").environ, **env},
        check=True,
    )
    canonical = source.with_name(source.name.replace(".from-py.svg", ".svg"))
    preview = canonical.with_suffix(".png")
    subprocess.run(
        ["rsvg-convert", "-w", "1800", "-o", str(preview), str(canonical)],
        check=True,
    )
    return canonical, preview


def main() -> None:
    grouped = load_master()
    expected_ids = [
        f"{prefix}-{number:02d}"
        for prefix, count in GROUP_SPECS
        for number in range(1, count + 1)
    ]
    if len(expected_ids) != 83 or len(set(expected_ids)) != 83:
        raise ValueError("Group specifications must cover all 83 rows exactly once")
    if set(expected_ids) != set(grouped):
        raise ValueError("Group specifications do not match master row IDs")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for row_id in expected_ids:
        source = render_card(row_id, grouped)
        canonical, preview = promote_and_preview(source)
        print(f"Wrote {source.relative_to(PROJECT_ROOT)}")
        print(f"Promoted {canonical.relative_to(PROJECT_ROOT)}")
        print(f"Previewed {preview.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()

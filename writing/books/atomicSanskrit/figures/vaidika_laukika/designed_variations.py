#!/usr/bin/env python3
"""Render the complete Designed Variations figure series as book-width SVGs."""

from __future__ import annotations

import csv
import html
import re
import subprocess
import sys
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
MARGIN = 28
TITLE_H = 122
HEADER_H = 86
ROW_H = 90
FOOTER_H = 92

INK = "#29251f"
MUTED = "#6e675d"
GOLD = "#9d7c36"
GOLD_LIGHT = "#e8dfcc"
PAPER = "#f7f4ed"
ROW_ALT = "#f0ece3"
GRID = "#cfc6b5"
OPEN = "#8b8377"
RED = "#8b4b3d"

LATIN_FONT = "EB Garamond, Charter, Georgia, serif"
DEVA_FONT = "Adobe Devanagari, Noto Serif Devanagari, serif"

PAGE_SPECS = [
    (
        "designed_variations_ekavacanam_01",
        "Designed Variations: Ekavacanam",
        "SG-01 through SG-15",
        [f"SG-{number:02d}" for number in range(1, 16)],
    ),
    (
        "designed_variations_ekavacanam_02",
        "Designed Variations: Ekavacanam",
        "SG-16 through SG-29",
        [f"SG-{number:02d}" for number in range(16, 30)],
    ),
    (
        "designed_variations_dvivacanam",
        "Designed Variations: Dvivacanam",
        "DU-01 through DU-12",
        [f"DU-{number:02d}" for number in range(1, 13)],
    ),
    (
        "designed_variations_bahuvacanam_01",
        "Designed Variations: Bahuvacanam",
        "PL-01 through PL-11",
        [f"PL-{number:02d}" for number in range(1, 12)],
    ),
    (
        "designed_variations_bahuvacanam_02",
        "Designed Variations: Bahuvacanam",
        "PL-12 through PL-21",
        [f"PL-{number:02d}" for number in range(12, 22)],
    ),
    (
        "designed_variations_word_classes",
        "Designed Variations: Word Classes",
        "CL-01 through CL-10",
        [f"CL-{number:02d}" for number in range(1, 11)],
    ),
    (
        "designed_variations_numerals",
        "Designed Variations: Numerals",
        "NU-01 through NU-07",
        [f"NU-{number:02d}" for number in range(1, 8)],
    ),
    (
        "designed_variations_accent_recitation",
        "Designed Variations: Accent and Recitation",
        "AC-01 through AC-04",
        [f"AC-{number:02d}" for number in range(1, 5)],
    ),
]


def clean_markdown(value: str) -> str:
    value = re.sub(r"<br\s*/?>", " ", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("***", "").replace("**", "").replace("`", "")
    value = value.replace("*", "")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def shorten(value: str, limit: int) -> str:
    value = clean_markdown(value)
    if len(value) <= limit:
        return value
    return value[: max(1, limit - 1)].rstrip(" ,;/") + "…"


def marked_terms(value: str) -> list[str]:
    terms = []
    for match in re.finditer(r"\*{2,3}(.+?)\*{2,3}", value):
        term = clean_markdown(match.group(1))
        if term and term not in terms:
            terms.append(term)
    return terms


def compact_forms(value: str, fallback: str, limit: int = 18) -> str:
    terms = marked_terms(value)
    if terms:
        return shorten(" · ".join(terms[:4]), limit)
    cleaned = clean_markdown(value)
    replacements = {
        "No corresponding productive laukika series": "no productive counterpart",
        "No corresponding productive": "no productive counterpart",
        "Laukika requires": "",
        "Laukika uses": "",
        "Laukika principally uses": "",
        "Laukika permits": "",
        "Vedic uses": "",
        "Vedic preserves": "",
    }
    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)
    cleaned = cleaned.strip(" ;:,")
    return shorten(cleaned or fallback, limit)


def compact_class(row: dict[str, str]) -> str:
    value = clean_markdown(row["ending_or_word_class"])
    value = value.replace("monosyllabic ", "mono. ")
    value = value.replace("Polysyllabic ", "poly. ")
    value = value.replace("first/second-person", "1st/2nd-person")
    value = value.replace("demonstratives and relatives", "demonstrative / relative")
    return shorten(value, 25)


def compact_relation(row: dict[str, str]) -> str:
    value = clean_markdown(row["vibhakti_or_operation"])
    if not value:
        value = clean_markdown(row["category_level"])
    replacements = {
        "प्रथमा": "प्रथमा",
        "द्वितीया": "द्वितीया",
        "तृतीया": "तृतीया",
        "चतुर्थी": "चतुर्थी",
        "पञ्चमी": "पञ्चमी",
        "षष्ठी": "षष्ठी",
        "सप्तमी": "सप्तमी",
        "संबोधन": "संबोधन",
        "एकवचनम्": "",
        "द्विवचनम्": "",
        "बहुवचनम्": "",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    value = re.sub(r"\s+", " ", value).strip(" ·,")
    return shorten(value, 22)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text(
    x: float,
    y: float,
    value: str,
    *,
    size: int = 29,
    color: str = INK,
    weight: int = 400,
    anchor: str = "start",
    italic: bool = False,
    deva: bool = False,
) -> str:
    family = DEVA_FONT if deva else LATIN_FONT
    style = "italic" if italic else "normal"
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{esc(family)}" '
        f'font-size="{size}" font-weight="{weight}" font-style="{style}" '
        f'fill="{color}" text-anchor="{anchor}">{esc(value)}</text>'
    )


def evidence_label(row: dict[str, str]) -> str:
    evidence = clean_markdown(row["evidence"])
    passage = "PASSAGE" in evidence
    function = "FUNCTION" in evidence
    open_item = "OPEN" in evidence
    if passage and function and open_item:
        return "P + FN · OPEN"
    if passage and function:
        return "P + FN"
    if passage and open_item:
        return "P · OPEN"
    if function and open_item:
        return "FN · OPEN"
    if passage:
        return "P"
    if function:
        return "FN"
    if open_item:
        return "OPEN"
    return "FORM"


def prevalence_lines(subrows: list[dict[str, str]]) -> list[dict[str, str]]:
    visible = []
    for row in subrows:
        if row["plot_status"] == "duplicate":
            continue
        visible.append(row)
    return visible[:3] or subrows[:1]


def prevalence_label(row: dict[str, str]) -> str:
    status = row["plot_status"]
    unit = row["unit"]
    numerator = row["numerator"]
    denominator = row["denominator"]
    percentage = row["percentage"]
    relation = row["relation"]
    grade = row["grade"]
    unit_short = {
        "tokens": "tok",
        "lexemes": "lex",
        "lexeme": "lex",
        "forms": "forms",
        "passages": "pass",
        "examples": "ex",
        "worked_examples": "ex",
        "paradigm": "paradigm",
    }.get(unit, unit)
    if status == "unknown" or relation in {"unknown", "source_corpus_conflict", "source_annotation_conflict"}:
        return f"open · {grade}"
    if status == "no_plot" and not numerator:
        return f"open · {grade}"
    if percentage:
        prefix = ""
        if relation == "upper_bound":
            prefix = "<"
        elif relation == "lower_bound":
            prefix = ">"
        elif relation in {"approximate", "approximate_counts"}:
            prefix = "≈"
        ratio = f" {numerator}/{denominator}" if numerator and denominator else ""
        return f"{prefix}{percentage}%{ratio} {unit_short} · {grade}".strip()
    if numerator:
        qualifier = "≈" if relation.startswith("approximate") else ""
        return f"{qualifier}{numerator} {unit_short} · {grade}".strip()
    if status == "zero":
        return f"0 {unit_short} · {grade}".strip()
    return f"open · {grade}"


def prevalence_mark(
    x: float,
    y: float,
    row: dict[str, str],
    additional_count: int = 0,
) -> list[str]:
    status = row["plot_status"]
    relation = row["relation"]
    percentage = row["percentage"]
    py = y
    parts: list[str] = []
    mark_x = x
    if status == "plot" and percentage:
        bar_w = 54
        parts.append(
            f'<rect x="{mark_x}" y="{py - 12}" width="{bar_w}" height="9" '
            f'rx="4.5" fill="{GOLD_LIGHT}"/>'
        )
        pct = max(0.0, min(100.0, float(percentage)))
        fill_w = max(2.0, bar_w * pct / 100.0)
        if relation in {"upper_bound", "lower_bound", "approximate", "approximate_counts"}:
            parts.append(
                f'<rect x="{mark_x}" y="{py - 12}" width="{fill_w:.1f}" height="9" '
                f'rx="4.5" fill="none" stroke="{GOLD}" stroke-width="2"/>'
            )
        else:
            parts.append(
                f'<rect x="{mark_x}" y="{py - 12}" width="{fill_w:.1f}" height="9" '
                f'rx="4.5" fill="{GOLD}"/>'
            )
        mark_x += 64
    elif status in {"dot", "raw_only", "paradigm"}:
        fill = GOLD if status == "dot" else "none"
        parts.append(
            f'<circle cx="{mark_x + 8}" cy="{py - 8}" r="7" fill="{fill}" '
            f'stroke="{GOLD}" stroke-width="2"/>'
        )
        mark_x += 24
    elif status == "zero":
        parts.append(
            f'<rect x="{mark_x}" y="{py - 14}" width="18" height="13" fill="none" '
            f'stroke="{INK}" stroke-width="2"/>'
        )
        parts.append(
            f'<line x1="{mark_x + 3}" y1="{py - 3}" x2="{mark_x + 15}" '
            f'y2="{py - 12}" stroke="{INK}" stroke-width="2"/>'
        )
        mark_x += 28
    else:
        parts.append(
            f'<rect x="{mark_x}" y="{py - 15}" width="22" height="15" fill="none" '
            f'stroke="{OPEN}" stroke-width="2" stroke-dasharray="4 3"/>'
        )
        mark_x += 30
    parts.append(
        text(
            mark_x,
            py,
            shorten(prevalence_label(row), 27),
            size=25,
            color=MUTED if "open" not in prevalence_label(row) else OPEN,
        )
    )
    if additional_count:
        parts.append(
            text(
                x + 264,
                py,
                f"+{additional_count}",
                size=23,
                color=MUTED,
                italic=True,
            )
        )
    return parts


def load_master() -> OrderedDict[str, list[dict[str, str]]]:
    grouped: OrderedDict[str, list[dict[str, str]]] = OrderedDict()
    with MASTER.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            grouped.setdefault(row["row_id"], []).append(row)
    if len(grouped) != 83:
        raise ValueError(f"Expected 83 grouped rows, found {len(grouped)}")
    return grouped


def render_page(
    filename: str,
    title_value: str,
    subtitle: str,
    row_ids: list[str],
    grouped: OrderedDict[str, list[dict[str, str]]],
) -> Path:
    height = TITLE_H + HEADER_H + ROW_H * len(row_ids) + FOOTER_H
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="4.75in" '
            f'height="{height / WIDTH * 4.75:.3f}in" viewBox="0 0 {WIDTH} {height}">'
        ),
        f'<rect width="{WIDTH}" height="{height}" fill="{PAPER}"/>',
        text(MARGIN, 54, title_value, size=42, weight=600),
        text(MARGIN, 91, subtitle, size=27, color=MUTED, italic=True),
        (
            f'<line x1="{MARGIN}" y1="108" x2="{WIDTH - MARGIN}" y2="108" '
            f'stroke="{GOLD}" stroke-width="3"/>'
        ),
    ]

    columns = {
        "id": MARGIN,
        "class": 122,
        "relation": 462,
        "qualification": 704,
        "dv": 946,
        "evidence": 1180,
        "forms": 122,
        "prevalence": 800,
    }
    header_y = TITLE_H + 39
    headers = [
        ("ID", columns["id"]),
        ("Ending / class", columns["class"]),
        ("Relation", columns["relation"]),
        ("Qualification", columns["qualification"]),
        ("DV", columns["dv"]),
        ("Evidence", columns["evidence"]),
    ]
    for label, x in headers:
        parts.append(text(x, header_y, label, size=25, color=MUTED, weight=600))
    parts.append(
        text(
            columns["forms"],
            header_y + 35,
            "Vaidika range · laukika productive form",
            size=23,
            color=MUTED,
            italic=True,
        )
    )
    parts.append(
        text(
            columns["prevalence"],
            header_y + 35,
            "Prevalence",
            size=23,
            color=MUTED,
            italic=True,
        )
    )

    row_top = TITLE_H + HEADER_H
    for index, row_id in enumerate(row_ids):
        subrows = grouped[row_id]
        row = subrows[0]
        y = row_top + index * ROW_H
        if index % 2:
            parts.append(
                f'<rect x="{MARGIN}" y="{y}" width="{WIDTH - 2 * MARGIN}" '
                f'height="{ROW_H}" fill="{ROW_ALT}"/>'
            )
        parts.append(
            f'<line x1="{MARGIN}" y1="{y}" x2="{WIDTH - MARGIN}" y2="{y}" '
            f'stroke="{GRID}" stroke-width="1"/>'
        )
        baseline = y + 32
        parts.append(text(columns["id"], baseline, row_id, size=28, weight=600, color=GOLD))
        parts.append(text(columns["class"], baseline, compact_class(row), size=28, deva=True))
        qualification = clean_markdown(row["qualification"])
        if qualification and qualification != "—":
            parts.append(
                text(
                    columns["qualification"],
                    baseline,
                    shorten(qualification, 17),
                    size=25,
                    color=RED if "DOUBTFUL" in qualification else MUTED,
                    italic=True,
                )
            )
        parts.append(
            text(
                columns["relation"],
                baseline,
                compact_relation(row),
                size=27,
                deva=True,
            )
        )
        vaidika = compact_forms(row["vaidika_form_or_range"], "Vedic form")
        laukika = compact_forms(row["laukika_form_or_range"], "—")
        parts.append(
            text(
                columns["forms"],
                baseline + 39,
                f"V: {vaidika}  ·  L: {laukika}",
                size=27,
                deva=True,
            )
        )
        dv_codes = re.findall(
            r"\b(?:SON|MAT|SVR|REL|ARR|SEM|RES|REC|AUD|FUN)\b",
            clean_markdown(row["confirmed_dv"]),
        )
        dv = "·".join(dict.fromkeys(dv_codes))
        parts.append(
            text(
                columns["dv"],
                baseline,
                "—" if not dv or dv == "—" else shorten(dv, 12),
                size=20 if len(dv) > 7 else 26,
                color=GOLD if dv and dv != "—" else OPEN,
                weight=600,
            )
        )
        measures = prevalence_lines(subrows)
        parts.extend(
            prevalence_mark(
                columns["prevalence"],
                baseline + 39,
                measures[0],
                max(0, len(measures) - 1),
            )
        )
        ev = evidence_label(row)
        ev_color = OPEN if "OPEN" in ev else INK
        parts.append(
            text(
                columns["evidence"],
                baseline,
                shorten(ev, 12),
                size=22,
                color=ev_color,
                anchor="middle",
                weight=600,
            )
        )

    bottom = row_top + ROW_H * len(row_ids)
    parts.append(
        f'<line x1="{MARGIN}" y1="{bottom}" x2="{WIDTH - MARGIN}" y2="{bottom}" '
        f'stroke="{GRID}" stroke-width="1"/>'
    )
    legend_y = bottom + 37
    parts.append(text(MARGIN, legend_y, "Measures:", size=24, color=MUTED, weight=600))
    parts.append(
        f'<rect x="139" y="{legend_y - 12}" width="45" height="8" rx="4" fill="{GOLD}"/>'
    )
    parts.append(text(192, legend_y, "% bar", size=23, color=MUTED))
    parts.append(
        f'<circle cx="287" cy="{legend_y - 8}" r="7" fill="{GOLD}" stroke="{GOLD}"/>'
    )
    parts.append(text(302, legend_y, "count", size=23, color=MUTED))
    parts.append(
        f'<rect x="380" y="{legend_y - 14}" width="43" height="11" rx="4" '
        f'fill="none" stroke="{GOLD}" stroke-width="2"/>'
    )
    parts.append(text(431, legend_y, "bound / ≈", size=23, color=MUTED))
    parts.append(
        f'<rect x="558" y="{legend_y - 16}" width="22" height="15" fill="none" '
        f'stroke="{OPEN}" stroke-width="2" stroke-dasharray="4 3"/>'
    )
    parts.append(text(590, legend_y, "open", size=23, color=MUTED))
    parts.append(
        text(
            WIDTH - MARGIN,
            legend_y,
            "A–D = evidence grade · P = passage · FN = function",
            size=22,
            color=MUTED,
            anchor="end",
        )
    )
    parts.append(
        text(
            MARGIN,
            bottom + 72,
            "Percentages, counts, bounds, and open cells measure different kinds of evidence.",
            size=23,
            color=MUTED,
            italic=True,
        )
    )
    parts.append("</svg>")

    source = OUT_DIR / f"{filename}.from-py.svg"
    source.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return source


def promote_and_preview(source: Path) -> tuple[Path, Path]:
    env = {
        "PYTHONPATH": str(LINEAGE_DIR),
    }
    subprocess.run(
        [
            sys.executable,
            "-m",
            "_shared.lineage",
            "promote",
            str(source),
        ],
        cwd=PROJECT_ROOT,
        env={**__import__("os").environ, **env},
        check=True,
    )
    canonical = source.with_name(source.name.replace(".from-py.svg", ".svg"))
    preview = canonical.with_suffix(".png")
    subprocess.run(
        [
            "rsvg-convert",
            "-w",
            "1800",
            "-o",
            str(preview),
            str(canonical),
        ],
        check=True,
    )
    return canonical, preview


def main() -> None:
    grouped = load_master()
    expected_ids = [row_id for _, _, _, ids in PAGE_SPECS for row_id in ids]
    if len(expected_ids) != 83 or len(set(expected_ids)) != 83:
        raise ValueError("Page specifications must cover all 83 rows exactly once")
    if set(expected_ids) != set(grouped):
        raise ValueError("Page specifications do not match master row IDs")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, title_value, subtitle, row_ids in PAGE_SPECS:
        source = render_page(filename, title_value, subtitle, row_ids, grouped)
        canonical, preview = promote_and_preview(source)
        print(f"Wrote {source.relative_to(PROJECT_ROOT)}")
        print(f"Promoted {canonical.relative_to(PROJECT_ROOT)}")
        print(f"Previewed {preview.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()

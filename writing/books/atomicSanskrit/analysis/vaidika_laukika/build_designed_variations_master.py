#!/usr/bin/env python3
"""Build the joined source used by the Designed Variations figure series.

The inventory, evidence overlay, and prevalence export remain the authoritative
research files. This script joins them by inventory ID and emits one record for
each prevalence subclaim. Rows without a numerical measure are retained with
empty prevalence fields.
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INVENTORY = (
    PROJECT_ROOT
    / "working/40_reference/source_material/"
    "vaidika_laukika_declensional_variations_complete.md"
)
OVERLAY = (
    PROJECT_ROOT
    / "working/10_active/as_vaidika_laukika_declensional_figure_source_data.md"
)
PREVALENCE = (
    PROJECT_ROOT
    / "working/10_active/as_vaidika_laukika_prevalence_figure_data.csv"
)
OUTPUT = (
    PROJECT_ROOT
    / "working/10_active/as_vaidika_laukika_designed_variations_master.csv"
)

ROW_ID_RE = re.compile(r"^(SG|DU|PL|CL|NU|AC)-\d{2}$")
PASSAGE_RE = re.compile(
    r"\b(?:RV|AV|VS|TS|ŚB|AB|TB|JB)\s+\d+(?:\.\d+){1,2}[a-d]?\b"
)


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def clean_markdown(value: str) -> str:
    value = re.sub(r"<br\s*/?>", " ", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("***", "").replace("**", "").replace("`", "")
    value = value.replace("*", "")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def parse_id_tables(path: Path) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = split_table_row(line)
        if cells and ROW_ID_RE.match(cells[0]):
            if cells[0] in rows:
                raise ValueError(f"Duplicate row {cells[0]} in {path}")
            rows[cells[0]] = cells
    return rows


def inventory_fields(row_id: str, cells: list[str]) -> dict[str, str]:
    prefix = row_id[:2]
    if prefix in {"SG", "DU", "PL"}:
        if len(cells) != 8:
            raise ValueError(f"{row_id}: expected 8 inventory cells, found {len(cells)}")
        return {
            "ending_or_word_class": cells[1],
            "gender": cells[2],
            "vibhakti_or_operation": cells[3],
            "vaidika_form_or_range": cells[4],
            "laukika_form_or_range": cells[5],
            "category_level": cells[6],
            "initial_placement": cells[7],
        }
    if prefix in {"CL", "NU"}:
        if len(cells) != 6:
            raise ValueError(f"{row_id}: expected 6 inventory cells, found {len(cells)}")
        return {
            "ending_or_word_class": cells[1],
            "gender": "",
            "vibhakti_or_operation": "",
            "vaidika_form_or_range": cells[2],
            "laukika_form_or_range": cells[3],
            "category_level": cells[4],
            "initial_placement": cells[5],
        }
    if prefix == "AC":
        if len(cells) != 4:
            raise ValueError(f"{row_id}: expected 4 inventory cells, found {len(cells)}")
        return {
            "ending_or_word_class": cells[1],
            "gender": "",
            "vibhakti_or_operation": cells[3],
            "vaidika_form_or_range": cells[2],
            "laukika_form_or_range": "",
            "category_level": cells[3],
            "initial_placement": "Appendix",
        }
    raise ValueError(f"Unknown inventory prefix: {row_id}")


def overlay_fields(row_id: str, cells: list[str]) -> dict[str, str]:
    if len(cells) != 5:
        raise ValueError(f"{row_id}: expected 5 overlay cells, found {len(cells)}")
    refs = PASSAGE_RE.findall(clean_markdown(cells[4]))
    return {
        "evidence": cells[1],
        "qualification": cells[2],
        "confirmed_dv": cells[3],
        "figure_instruction": cells[4],
        "passage_references": "; ".join(dict.fromkeys(refs)),
    }


def main() -> None:
    inventory_rows = parse_id_tables(INVENTORY)
    overlay_rows = parse_id_tables(OVERLAY)

    expected = set(inventory_rows)
    if len(expected) != 83:
        raise ValueError(f"Expected 83 inventory rows, found {len(expected)}")
    if set(overlay_rows) != expected:
        missing = sorted(expected - set(overlay_rows))
        extra = sorted(set(overlay_rows) - expected)
        raise ValueError(f"Overlay mismatch; missing={missing}, extra={extra}")

    prevalence_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    with PREVALENCE.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            prevalence_by_id[row["row_id"]].append(row)
    if set(prevalence_by_id) != expected:
        missing = sorted(expected - set(prevalence_by_id))
        extra = sorted(set(prevalence_by_id) - expected)
        raise ValueError(f"Prevalence mismatch; missing={missing}, extra={extra}")

    prevalence_columns = [
        "subclaim",
        "numerator",
        "denominator",
        "percentage",
        "relation",
        "unit",
        "label",
        "grade",
        "plot_status",
        "note",
    ]
    fieldnames = [
        "row_id",
        "figure_family",
        "ending_or_word_class",
        "gender",
        "vibhakti_or_operation",
        "vaidika_form_or_range",
        "laukika_form_or_range",
        "category_level",
        "initial_placement",
        "evidence",
        "qualification",
        "confirmed_dv",
        "figure_instruction",
        "passage_references",
        *prevalence_columns,
    ]

    family = {
        "SG": "Ekavacanam",
        "DU": "Dvivacanam",
        "PL": "Bahuvacanam",
        "CL": "Word Classes",
        "NU": "Numerals",
        "AC": "Accent and Recitation",
    }

    output_rows: list[dict[str, str]] = []
    for row_id in sorted(expected, key=lambda item: (item[:2], int(item[3:]))):
        base = {
            "row_id": row_id,
            "figure_family": family[row_id[:2]],
            **inventory_fields(row_id, inventory_rows[row_id]),
            **overlay_fields(row_id, overlay_rows[row_id]),
        }
        for prevalence in prevalence_by_id[row_id]:
            output_rows.append(
                {
                    **base,
                    **{column: prevalence.get(column, "") for column in prevalence_columns},
                }
            )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)

    print(
        f"Wrote {OUTPUT.relative_to(PROJECT_ROOT)}: "
        f"{len(output_rows)} subrows covering {len(expected)} inventory rows"
    )


if __name__ == "__main__":
    main()

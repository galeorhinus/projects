#!/usr/bin/env python3
"""Validate the Vaidika-Laukika prevalence figure dataset."""

from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path


EXPECTED_GROUPS = {
    "SG": 29,
    "DU": 12,
    "PL": 21,
    "CL": 10,
    "NU": 7,
    "AC": 4,
}

REQUIRED_COLUMNS = {
    "row_id",
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
}

VALID_PLOT_STATUSES = {
    "plot",
    "dot",
    "raw_only",
    "unknown",
    "no_plot",
    "paradigm",
    "zero",
    "duplicate",
}


def expected_ids() -> set[str]:
    return {
        f"{prefix}-{number:02d}"
        for prefix, count in EXPECTED_GROUPS.items()
        for number in range(1, count + 1)
    }


def main() -> int:
    default_path = (
        Path(__file__).resolve().parents[2]
        / "working/10_active/as_vaidika_laukika_prevalence_figure_data.csv"
    )
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_path

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if set(reader.fieldnames or []) != REQUIRED_COLUMNS:
            missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            extra = set(reader.fieldnames or []) - REQUIRED_COLUMNS
            raise SystemExit(f"column mismatch: missing={sorted(missing)} extra={sorted(extra)}")
        rows = list(reader)

    by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for line_number, row in enumerate(rows, start=2):
        by_id[row["row_id"]].append(row)

        if row["plot_status"] not in VALID_PLOT_STATUSES:
            raise SystemExit(
                f"{path}:{line_number}: invalid plot_status {row['plot_status']!r}"
            )

        if row["percentage"]:
            percentage = float(row["percentage"])
            if not 0 <= percentage <= 100:
                raise SystemExit(
                    f"{path}:{line_number}: percentage outside 0-100: {percentage}"
                )

        if row["plot_status"] == "plot" and not row["percentage"]:
            raise SystemExit(
                f"{path}:{line_number}: plotted row lacks a percentage"
            )

        if row["plot_status"] == "zero" and row["numerator"] != "0":
            raise SystemExit(
                f"{path}:{line_number}: zero row must preserve numerator 0"
            )

    missing_ids = expected_ids() - set(by_id)
    extra_ids = set(by_id) - expected_ids()
    if missing_ids or extra_ids:
        raise SystemExit(
            f"ID mismatch: missing={sorted(missing_ids)} extra={sorted(extra_ids)}"
        )

    percentage_ids = {
        row_id
        for row_id, subrows in by_id.items()
        if any(
            row["plot_status"] == "plot" and row["percentage"]
            for row in subrows
        )
    }
    zero_ids = {
        row_id
        for row_id, subrows in by_id.items()
        if any(row["plot_status"] == "zero" for row in subrows)
    }
    numerical_ids = {
        row_id
        for row_id, subrows in by_id.items()
        if any(
            row["numerator"] or row["denominator"] or row["percentage"]
            for row in subrows
        )
    }
    graphable_ids = percentage_ids | zero_ids
    absolute_only_ids = numerical_ids - graphable_ids
    unmeasured_ids = set(by_id) - numerical_ids

    expected_summary = {
        "inventory": 83,
        "numbered": 76,
        "graphable": 39,
        "absolute_only": 37,
        "unmeasured": 7,
    }
    actual_summary = {
        "inventory": len(by_id),
        "numbered": len(numerical_ids),
        "graphable": len(graphable_ids),
        "absolute_only": len(absolute_only_ids),
        "unmeasured": len(unmeasured_ids),
    }
    if actual_summary != expected_summary:
        raise SystemExit(
            f"coverage summary changed: expected={expected_summary} actual={actual_summary}"
        )

    group_counts = Counter(row_id.split("-", 1)[0] for row_id in by_id)
    if dict(group_counts) != EXPECTED_GROUPS:
        raise SystemExit(
            f"group count mismatch: expected={EXPECTED_GROUPS} actual={dict(group_counts)}"
        )

    print(f"validated {len(rows)} figure subrows covering {len(by_id)} inventory rows")
    print(
        "coverage: "
        f"{len(graphable_ids)} graphable, "
        f"{len(absolute_only_ids)} absolute-only, "
        f"{len(unmeasured_ids)} unmeasured"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

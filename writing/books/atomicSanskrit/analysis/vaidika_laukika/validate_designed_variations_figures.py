#!/usr/bin/env python3
"""Validate the master dataset and the complete Designed Variations SVG series."""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MASTER = (
    PROJECT_ROOT
    / "working/10_active/as_vaidika_laukika_designed_variations_master.csv"
)
FIGURE_DIR = PROJECT_ROOT / "figures/vaidika_laukika"
ROW_ID_RE = re.compile(r">((?:SG|DU|PL|CL|NU|AC)-\d{2})</text>")
EXPECTED_COUNTS = {
    "SG": 29,
    "DU": 12,
    "PL": 21,
    "CL": 10,
    "NU": 7,
    "AC": 4,
}
KNOWN_PLOT_STATUSES = {
    "plot",
    "dot",
    "no_plot",
    "unknown",
    "raw_only",
    "paradigm",
    "zero",
    "duplicate",
}
FIGURES = [
    "designed_variations_ekavacanam_01.svg",
    "designed_variations_ekavacanam_02.svg",
    "designed_variations_dvivacanam.svg",
    "designed_variations_bahuvacanam_01.svg",
    "designed_variations_bahuvacanam_02.svg",
    "designed_variations_word_classes.svg",
    "designed_variations_numerals.svg",
    "designed_variations_accent_recitation.svg",
]


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> None:
    with MASTER.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 107:
        fail(f"Expected 107 master subrows, found {len(rows)}")

    by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_id[row["row_id"]].append(row)
        if row["plot_status"] not in KNOWN_PLOT_STATUSES:
            fail(f"{row['row_id']}: unknown plot status {row['plot_status']!r}")
        if not row["grade"]:
            fail(f"{row['row_id']}: missing evidence grade")
        if not row["unit"] and row["plot_status"] not in {"no_plot", "unknown", "duplicate"}:
            fail(f"{row['row_id']}: plotted or counted subrow has no unit")
        if (
            row["percentage"]
            and (not row["numerator"] or not row["denominator"])
            and row["relation"] not in {"upper_bound", "lower_bound"}
        ):
            fail(f"{row['row_id']}: percentage lacks numerator or denominator")
        if row["plot_status"] == "zero" and row["numerator"] not in {"", "0"}:
            fail(f"{row['row_id']}: measured zero has a nonzero numerator")
        if not row["figure_instruction"]:
            fail(f"{row['row_id']}: missing figure instruction")

    if len(by_id) != 83:
        fail(f"Expected 83 grouped inventory rows, found {len(by_id)}")
    prefix_counts = Counter(row_id[:2] for row_id in by_id)
    if dict(prefix_counts) != EXPECTED_COUNTS:
        fail(f"Unexpected category counts: {dict(prefix_counts)}")

    figure_occurrences: Counter[str] = Counter()
    for name in FIGURES:
        path = FIGURE_DIR / name
        if not path.exists():
            fail(f"Missing canonical figure {path}")
        content = path.read_text(encoding="utf-8")
        figure_occurrences.update(ROW_ID_RE.findall(content))
        source = path.with_name(path.name.replace(".svg", ".from-py.svg"))
        if not source.exists():
            fail(f"Missing canonical source {source}")
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "_shared.lineage",
                "verify",
                str(path),
            ],
            cwd=PROJECT_ROOT,
            env={**__import__("os").environ, "PYTHONPATH": str(PROJECT_ROOT / "figures")},
            capture_output=True,
            text=True,
        )
        if result.returncode:
            fail(result.stdout + result.stderr)

    missing = sorted(set(by_id) - set(figure_occurrences))
    extra = sorted(set(figure_occurrences) - set(by_id))
    repeated = sorted(row_id for row_id, count in figure_occurrences.items() if count != 1)
    if missing or extra or repeated:
        fail(
            "Figure coverage mismatch: "
            f"missing={missing}, extra={extra}, repeated={repeated}"
        )

    open_subrows = [
        row
        for row in rows
        if row["plot_status"] in {"no_plot", "unknown"}
        or row["relation"] in {
            "unknown",
            "source_corpus_conflict",
            "source_annotation_conflict",
        }
    ]
    zero_subrows = [row for row in rows if row["plot_status"] == "zero"]
    if not open_subrows:
        fail("Expected at least one open measurement")
    if not zero_subrows:
        fail("Expected at least one measured zero")

    print(
        "validated "
        f"{len(rows)} master subrows, {len(by_id)} inventory rows, "
        f"{len(FIGURES)} SVG pages, {len(open_subrows)} open subrows, "
        f"and {len(zero_subrows)} measured zeros"
    )


if __name__ == "__main__":
    main()

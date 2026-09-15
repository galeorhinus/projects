#!/usr/bin/env python3
"""Tinanta pass 8: keep pada series as output alternatives, not meanings."""

from __future__ import annotations

import csv
import json
from collections import Counter

from tinanta_common import RESULTS


def main() -> None:
    with (RESULTS / "tinanta_citation_sample.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    profile = Counter()
    by_layer = Counter()
    for row in rows:
        p = bool(row["parasmaipada_forms_slp1"])
        a = bool(row["atmanepada_forms_slp1"])
        label = "both" if p and a else "parasmaipada_only" if p else "atmanepada_only" if a else "neither"
        profile[label] += 1; by_layer[(row["source_layer"], label)] += 1
    report = {
        "date": "2026-09-14", "sample_cells": len(rows),
        "sample_profile": dict(profile),
        "pada_policy": "A semantic person-number-lakara cell is counted once. All generated parasmaipada and atmanepada forms remain attached as alternatives.",
        "automatic_pada_multiplier": 1,
        "meaning_sensitive_pada_analysis_deferred": True,
    }
    (RESULTS / "tinanta_pada_classification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# तिङन्त Pass 8: पद Output Policy", "", "| Sample output profile | Citation cells |", "|---|---:|"]
    for label in ("parasmaipada_only", "atmanepada_only", "both", "neither"):
        lines.append(f"| {label} | {profile[label]} |")
    lines.extend(["", "The two पद series do not automatically create two meanings. This analysis counts the tense-or-mood and person-number function once, then attaches every generated पद form to that cell. A later semantic study may separate a पद contrast only where the construction itself changes meaning.", ""])
    (RESULTS / "tinanta_pada_classification.md").write_text("\n".join(lines))
    print("Classified pada outputs without applying a two-series multiplier.")


if __name__ == "__main__":
    main()

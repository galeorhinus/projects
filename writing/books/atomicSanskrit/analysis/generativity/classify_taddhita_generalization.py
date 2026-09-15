#!/usr/bin/env python3
"""Classify recovered plain-taddhita families by generalization status."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
SOURCE = RESULTS / "plain_taddhita_semantic_classification.csv"
CONFIG = HERE / "taddhita_generalization_operations.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    rows = list(csv.DictReader(SOURCE.open(newline="", encoding="utf-8")))
    positive = [row for row in rows if row["assertion_status"] == "positive"]
    by_family: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in positive:
        by_family[row["semantic_family"]].append(row)

    selected = {"superlative", "comparative"}
    already_generalized = {"state_or_quality", "possession"}
    exact_input = {
        "means_of_crossing", "equality_in_age", "means_of_attainment",
        "means_of_killing", "price_relation", "price_equivalence",
        "field_measure", "measured_equivalence", "cognitive_instrument_or_act",
        "community_speech", "means_of_ploughing",
    }
    lexical = {
        "specified_association", "listed_lexical_quality",
        "listed_lexical_formation", "same_referent_derivative",
    }

    classified = []
    for family in sorted(by_family):
        family_rows = by_family[family]
        if family in selected:
            status = "selected_for_semantic_class_generalization"
            reason = "The governing rule supplies a general comparative relation; 5.3.58 supplies the narrower quality condition for the vowel-initial suffixes."
        elif family in already_generalized:
            status = "already_generalized_in_prior_ledger"
            reason = "A prior broad ledger already applies this relation to its declared input scope."
        elif family in exact_input:
            status = "source_input_bounded"
            reason = "The source defines the relation for a named input rather than for an independently identified nominal class."
        elif family in lexical:
            status = "source_list_bounded"
            reason = "The rule or commentary supplies a lexical list whose membership cannot be inferred from the present nominal metadata."
        else:
            status = "semantic_class_not_yet_identified"
            reason = "The relation is productive only for a narrower class such as names, places, times, materials, measures, persons, directions, or numbers; that class is not independently identified across the inventory."
        classified.append({
            "semantic_family": family,
            "positive_source_assertions": len(family_rows),
            "active_positive_source_assertions": sum(row["test_status"] == "active_test" for row in family_rows),
            "governing_rules": ";".join(sorted({row["semantic_rule_ref"] for row in family_rows})),
            "generalization_status": status,
            "reason": reason,
        })

    output = RESULTS / "taddhita_generalization_classification.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(classified[0]))
        writer.writeheader()
        writer.writerows(classified)

    counts = Counter(row["generalization_status"] for row in classified)
    report = {
        "date": "2026-09-14",
        "semantic_families_reviewed": len(classified),
        "family_dispositions": dict(counts),
        "selected_families": sorted(selected),
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (SOURCE, CONFIG, Path(__file__))
        },
        "publication_status": "research_classification_not_deployed",
    }
    (RESULTS / "taddhita_generalization_classification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lines = [
        "# तद्धित Generalization Classification", "",
        "This pass asks which recovered semantic relations can extend beyond their source examples using the nominal metadata already present. A suffix is not generalized merely because the engine can construct a form.", "",
        "| Disposition | Families |", "|---|---:|",
    ]
    for status, count in sorted(counts.items()):
        lines.append(f"| {status.replace('_', ' ')} | {count} |")
    lines.extend([
        "", "The comparative and superlative families proceed. State or quality and possession were already generalized. Every other family remains available but source-bounded until its required nominal class can be identified independently.", "",
    ])
    (RESULTS / "taddhita_generalization_classification.md").write_text("\n".join(lines))
    print(f"Classified {len(classified)} semantic families; selected {len(selected)} for generalization.")


if __name__ == "__main__":
    main()

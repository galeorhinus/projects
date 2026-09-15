#!/usr/bin/env python3
"""Classify the 87 deferred krt identifiers by executable construction path."""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path

from vidyut.prakriya import Data, Krt, Pratipadika, Vyakarana


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "manifest.json"
KRT_CLASSIFICATION = RESULTS / "krt_classification.csv"
UPASARGAS = HERE / "upasarga_inventory.csv"
CONFIG = HERE / "conditioned_krt_operations.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This classification requires Vidyut 0.4.0")
    manifest = json.loads(MANIFEST.read_text())
    source_record = next(row for row in manifest["sources"] if row["filename"] == "vidyut-krt-basic.rs")
    if sha256(ARCHIVE / source_record["filename"]) != source_record["sha256"]:
        raise ValueError("Archived krt implementation changed")
    deferred = [
        row for row in read_csv(KRT_CLASSIFICATION)
        if row["primary_classification"] == "root_or_construction_conditioned_deferred"
    ]
    if len(deferred) != 87:
        raise ValueError(f"Expected 87 deferred krt identifiers; found {len(deferred)}")
    config = json.loads(CONFIG.read_text())
    operations = config["operations"]
    selected = {row["source_variant"] for row in operations}
    known = {row["source_variant"] for row in deferred}
    if not selected.issubset(known):
        raise ValueError(f"Selected non-deferred identifiers: {sorted(selected - known)}")
    operations_by_variant = Counter(row["source_variant"] for row in operations)

    entries = Data(str(ARCHIVE)).load_dhatu_entries()
    prefixes = [row["engine_input_slp1"] for row in read_csv(UPASARGAS)]
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    rows = []
    for item in deferred:
        variant = item["source_variant"]
        krt = getattr(Krt, variant)
        direct = 0
        for entry in entries:
            direct += bool(grammar.derive(Pratipadika.krdanta(entry.dhatu, krt)))
        prefixed_pairs = 0
        if direct == 0:
            for prefix in prefixes:
                for entry in entries:
                    dhatu = entry.dhatu.with_prefixes([prefix])
                    prefixed_pairs += bool(grammar.derive(Pratipadika.krdanta(dhatu, krt)))
        if direct == len(entries):
            engine_path = "direct_full_source_entry_coverage"
        elif direct:
            engine_path = "direct_root_conditioned_coverage"
        elif prefixed_pairs:
            engine_path = "prefix_conditioned_coverage"
        else:
            engine_path = "upapada_other_construction_or_engine_gap"
        rows.append({
            "source_variant": variant,
            "visible_suffix": item["visible_suffix"],
            "engine_path_classification": engine_path,
            "direct_source_entries_with_output": str(direct),
            "one_prefix_source_entry_pairs_with_output": str(prefixed_pairs),
            "selected_semantic_operations": str(operations_by_variant[variant]),
            "count_status": "selected_for_bounded_semantic_generation" if variant in selected else "deferred_pending_semantic_or_construction_model",
        })

    rows.sort(key=lambda row: row["source_variant"])
    with (RESULTS / "conditioned_krt_classification.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    paths = Counter(row["engine_path_classification"] for row in rows)
    report = {
        "date": config["date"],
        "scope": config["scope"],
        "deferred_identifiers_classified": len(rows),
        "engine_path_classification_counts": dict(sorted(paths.items())),
        "selected_identifiers": len(selected),
        "selected_semantic_operations": len(operations),
        "selected_operations": operations,
        "classification_boundary": "The engine path is a coverage diagnostic, not a grammatical license. Only operations with an explicit semantic relation and source rule enter the next ledger. Zero output does not prove prohibition.",
        "vocabulary_total": None,
        "publication_status": "classification_only_not_deployed",
        "engine": {"name": "Vidyut", "version": importlib.metadata.version("vidyut"), "commit": manifest["generator_commit"]},
        "source": source_record,
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (
            KRT_CLASSIFICATION, UPASARGAS, CONFIG, MANIFEST, Path(__file__)
        )},
    }
    (RESULTS / "conditioned_krt_classification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Conditioned कृत्प्रत्यय Classification", "",
        "This pass classifies all 87 identifiers that remained after the first bounded कृदन्त selection. The executable path shows where the pinned engine can construct a form. It does not by itself authorize a meaning.", "",
        "| Executable path | Identifiers |", "|---|---:|",
    ]
    for label, count in sorted(paths.items()):
        lines.append(f"| {label.replace('_', ' ')} | {count} |")
    lines.extend([
        "", f"Seven identifiers carrying **{len(operations)} source-defined semantic operations** enter the next bounded generation pass. The other identifiers remain in the classification ledger with their engine coverage and are not lost or treated as impossible.", "",
        "A zero-output row means that direct or one-prefix construction did not activate the identifier in Vidyut 0.4.0. It may require an उपपदम्, another construction, a source condition not exposed through the Python binding, or missing engine coverage.", "",
    ])
    (RESULTS / "conditioned_krt_classification.md").write_text("\n".join(lines))
    print(f"Classified {len(rows)} deferred krt identifiers; selected {len(selected)} identifiers carrying {len(operations)} semantic operations.")


if __name__ == "__main__":
    main()

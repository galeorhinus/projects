#!/usr/bin/env python3
"""Classify all pinned ordinary krt identifiers for bounded generation."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "manifest.json"
INVENTORY = RESULTS / "operation_inventory.csv"
CONFIG = HERE / "krt_classification.json"
SOURCE = ARCHIVE / "vidyut-args-krt.rs"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    source_record = next(row for row in manifest["sources"] if row["filename"] == SOURCE.name)
    if sha256(SOURCE) != source_record["sha256"]:
        raise ValueError("Archived krt source changed")
    config = json.loads(CONFIG.read_text())
    inventory = [row for row in read_csv(INVENTORY) if row["family"] == "krt"]
    if len(inventory) != 122:
        raise ValueError(f"Expected 122 ordinary krt identifiers; found {len(inventory)}")
    known = {row["source_variant"] for row in inventory}
    vedic = set(config["vedic_only"])
    avyaya = set(config["avyaya"])
    duplicate = set(config["near_duplicates"])
    operations_by_variant: dict[str, list[dict]] = defaultdict(list)
    for operation in config["bounded_laukika_operations"]:
        operations_by_variant[operation["source_variant"]].append(operation)
    selected = set(operations_by_variant)
    for label, values in (("vedic", vedic), ("avyaya", avyaya), ("duplicate", duplicate), ("selected", selected)):
        if not values.issubset(known):
            raise ValueError(f"Unknown {label} krt identifiers: {sorted(values - known)}")
    if selected & (vedic | avyaya | duplicate):
        raise ValueError("A bounded laukika identifier also appears in a deferred class")

    rows = []
    for item in inventory:
        variant = item["source_variant"]
        if variant in selected:
            primary = "bounded_laukika_generation"
        elif variant in vedic:
            primary = "vedic_only_deferred"
        elif variant in avyaya:
            primary = "laukika_avyaya_deferred"
        elif variant in duplicate:
            primary = "near_duplicate_deferred"
        else:
            primary = "root_or_construction_conditioned_deferred"
        operations = operations_by_variant.get(variant, [])
        rows.append({
            "source_variant": variant,
            "engine_id": item["engine_id"],
            "visible_suffix": item["visible_suffix"],
            "is_vedic_only": str(variant in vedic).lower(),
            "is_avyaya": str(variant in avyaya).lower(),
            "is_near_duplicate": str(variant in duplicate).lower(),
            "primary_classification": primary,
            "bounded_operation_ids": ";".join(row["operation_id"] for row in operations),
            "bounded_semantic_operation_count": str(len(operations)),
            "count_status": "eligible_for_bounded_generation" if operations else "not_admitted_in_current_pass",
            "source_description": item["source_description"],
        })

    with (RESULTS / "krt_classification.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    primary = Counter(row["primary_classification"] for row in rows)
    report = {
        "date": config["date"],
        "scope": config["scope"],
        "ordinary_krt_identifiers": len(rows),
        "classification_counts": dict(sorted(primary.items())),
        "property_counts": {
            "vedic_only": len(vedic),
            "avyaya": len(avyaya),
            "near_duplicate": len(duplicate),
        },
        "bounded_laukika_identifiers": len(selected),
        "bounded_laukika_semantic_operations": len(config["bounded_laukika_operations"]),
        "bounded_operations": config["bounded_laukika_operations"],
        "classification_policy": {
            "selected": "General laukika nominal formations whose semantic relation and governing rule are explicit enough for the current bounded count.",
            "vedic_only": "Preserved for a separate vaidika-domain count.",
            "avyaya": "Preserved for the separate avyaya pass.",
            "near_duplicate": "Not counted when the pinned source says it always duplicates another result except for accent.",
            "conditioned": "Preserved for root-, prefix-, upapada-, sense-, or other construction-level review; absence from a dictionary is not the reason for deferral.",
        },
        "vocabulary_total": None,
        "publication_status": "classification_only_not_deployed",
        "source": source_record,
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (INVENTORY, CONFIG, SOURCE, MANIFEST, Path(__file__))},
    }
    (RESULTS / "krt_classification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "krt_classification.md").write_text("\n".join([
        "# कृदन्त-Pratyaya Classification", "",
        "The pinned engine exposes 122 ordinary कृत्प्रत्यय identifiers. They are not 122 universal multipliers. This pass classifies every identifier before any कृदन्त word-meaning enters the count.", "",
        "## Classification", "",
        "| Primary class | Identifiers | Disposition |", "|---|---:|---|",
        f"| Bounded laukika generation | {primary['bounded_laukika_generation']} | Generates {len(config['bounded_laukika_operations'])} explicit semantic operations in the next pass |",
        f"| Vedic-only | {primary['vedic_only_deferred']} | Separate vaidika-domain count |",
        f"| Laukika अव्यय | {primary['laukika_avyaya_deferred']} | Separate अव्यय pass |",
        f"| Near duplicate | {primary['near_duplicate_deferred']} | Excluded where the source says only accent differs |",
        f"| Root- or construction-conditioned | {primary['root_or_construction_conditioned_deferred']} | Requires its own eligibility model |", "",
        f"The selected **{len(selected)} identifiers** carry **{len(config['bounded_laukika_operations'])} semantic operations**. ल्युट् contributes action, instrument, and location meanings; each is counted separately even when the same form carries them. The remaining identifiers stay visible in the classification ledger rather than disappearing into an undefined remainder.", "",
        "The detailed CSV records all property overlaps. For example, several Vedic-only identifiers are also indeclinable or near-duplicates. The primary classes above are mutually exclusive only to make the current disposition clear.", "",
    ]))
    print(f"Classified {len(rows)} krt identifiers; selected {len(selected)} identifiers and {len(config['bounded_laukika_operations'])} semantic operations.")


if __name__ == "__main__":
    main()

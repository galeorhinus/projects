#!/usr/bin/env python3
"""Capacity pass 2: inventory current laukika nominal meanings without duplication."""

from __future__ import annotations

from collections import Counter
import csv
import json

from samasa_capacity_common import RESULTS, SOURCE_PATHS, iter_compoundable_members, project_path, sha256, split_forms


SAMPLE_SIZE_PER_LAYER = 4


def main() -> None:
    counts = Counter()
    variant_counts = Counter()
    samples: dict[str, list[dict]] = {}
    for row in iter_compoundable_members():
        if row["domain"] != "laukika":
            raise ValueError(f"Non-laukika member entered capacity inventory: {row['member_id']}")
        forms = split_forms(row["forms_slp1"])
        if not forms:
            raise ValueError(f"Member has no form: {row['member_id']}")
        layer = row["source_layer"]
        counts[layer] += 1
        variant_counts[layer] += len(forms)
        bucket = samples.setdefault(layer, [])
        if len(bucket) < SAMPLE_SIZE_PER_LAYER:
            bucket.append({**row, "forms_slp1": ";".join(forms), "form_variant_count": len(forms)})

    sample_rows = [record for layer in sorted(samples) for record in samples[layer]]
    output = RESULTS / "samasa_capacity_member_sample.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(sample_rows[0]))
        writer.writeheader()
        writer.writerows(sample_rows)
    total = sum(counts.values())
    report = {
        "date": "2026-09-14",
        "compoundable_nominal_word_meanings": total,
        "member_form_variants": sum(variant_counts.values()),
        "counts_by_source_layer": dict(counts),
        "form_variants_by_source_layer": dict(variant_counts),
        "inventory_storage": "normalized virtual view over existing reconciled ledgers",
        "materialized_records": len(sample_rows),
        "full_inventory_duplicated": False,
        "identity_boundary": "Source-layer prefixes keep identities disjoint; uniqueness inside each source ledger is inherited from its completed reconciliation pass.",
        "domain_boundary": "Only laukika nominal meanings enter this capacity inventory; Vedic plain-taddhita outputs remain in their own domain.",
        "known_vaidika_nominal_outputs_excluded": 1,
        "confirmed_prior_feminine_overlaps_excluded": 2,
        "inputs": {project_path(path): sha256(path) for path in SOURCE_PATHS.values()},
    }
    (RESULTS / "samasa_capacity_member_inventory.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    lines = [
        "# समासः Member Inventory", "",
        "The compound pass reads the already reconciled nominal ledgers as one normalized virtual inventory. It does not create a second eight-million-row copy.", "",
        "| Source layer | Nominal meanings | Form variants |", "|---|---:|---:|",
    ]
    for layer in sorted(counts):
        lines.append(f"| {layer} | {counts[layer]:,} | {variant_counts[layer]:,} |")
    lines.extend([
        f"| **Total** | **{total:,}** | **{sum(variant_counts.values()):,}** |", "",
        "The count follows word-meaning identities. Alternative generated forms remain attached to one meaning.", "",
    ])
    (RESULTS / "samasa_capacity_member_inventory.md").write_text("\n".join(lines))
    print(f"Inventoried {total:,} compoundable nominal meanings.")


if __name__ == "__main__":
    main()

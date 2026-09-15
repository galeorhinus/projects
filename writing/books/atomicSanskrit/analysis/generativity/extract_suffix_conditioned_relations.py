#!/usr/bin/env python3
"""Materialize helper-expanded and constructed-input suffix relations."""

from __future__ import annotations

from collections import Counter
import csv
import json
from pathlib import Path

from taddhita_conditioned_common import ARCHIVE, HERE, RESULTS, sha256, stable_id


CONFIG = HERE / "suffix_conditioned_operations.json"
CLASSIFICATION = RESULTS / "suffix_productivity_classification.csv"


def main() -> None:
    config = json.loads(CONFIG.read_text())
    with CLASSIFICATION.open(newline="", encoding="utf-8") as handle:
        classified = {row["source_variant"]: row for row in csv.DictReader(handle)}

    rows = []
    source_paths = set()
    for family in config["families"]:
        source = ARCHIVE / family["source_file"]
        source_paths.add(source)
        source_lines = source.read_text().splitlines()
        for call in family["calls"]:
            call_line = source_lines[call["source_line"] - 1]
            if family["source_kind"] == "expanded_local_helper":
                helper_start = family["helper_definition_line"] - 1
                helper_block = "\n".join(source_lines[helper_start:helper_start + 8])
                if "fn " not in source_lines[helper_start] or family["semantic_context"] not in helper_block:
                    raise ValueError(f"Helper condition missing at {source.name}:{family['helper_definition_line']}")
                for suffix in family["suffixes"]:
                    if f"T::{suffix['source_variant']}" not in helper_block:
                        raise ValueError(f"Helper suffix {suffix['source_variant']} missing at {source.name}:{family['helper_definition_line']}")
                for token in [call["input_form_slp1"], *call["outputs_slp1"]]:
                    if f'"{token}"' not in call_line:
                        raise ValueError(f"Source token {token!r} missing at {source.name}:{call['source_line']}")
            else:
                for token in call["outputs_slp1"]:
                    if f'"{token}"' not in call_line:
                        raise ValueError(f"Output token {token!r} missing at {source.name}:{call['source_line']}")
                construction = source_lines[call["input_construction_line"] - 1]
                if "artha_taddhitanta" not in construction or "Parimana" not in construction:
                    raise ValueError(f"Constructed input not found at {source.name}:{call['input_construction_line']}")
                if family["semantic_context"] not in call_line:
                    raise ValueError(f"Semantic condition missing at {source.name}:{call['source_line']}")
                for suffix in family["suffixes"]:
                    if f"T::{suffix['source_variant']}" not in call_line:
                        raise ValueError(f"Suffix {suffix['source_variant']} missing at {source.name}:{call['source_line']}")

            for suffix in family["suffixes"]:
                variant = suffix["source_variant"]
                if classified[variant]["productivity_class"] != "conditioned_inputs_only":
                    raise ValueError(f"Expected conditioned suffix classification for {variant}")
                if family["source_kind"] == "expanded_local_helper":
                    outputs = [call["outputs_slp1"][suffix["output_argument"]]]
                else:
                    outputs = call["outputs_slp1"]
                rows.append({
                    "relation_id": stable_id("suffix-conditioned", family["family_id"], call["input_form_slp1"], variant),
                    "family_id": family["family_id"],
                    "input_form_slp1": call["input_form_slp1"],
                    "semantic_context": family["semantic_context"],
                    "semantic_relation": family["semantic_relation"],
                    "taddhita_source_variant": variant,
                    "visible_suffix": classified[variant]["visible_suffix"],
                    "expected_output_forms_slp1": ";".join(outputs),
                    "expected_output_variant_count": len(outputs),
                    "rule_ref": family["rule_ref"],
                    "source_file": family["source_file"],
                    "source_line": call["source_line"],
                    "source_kind": family["source_kind"],
                    "eligibility_status": "source_condition_satisfied",
                })

    output = RESULTS / "suffix_conditioned_relations.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    report = {
        "date": "2026-09-13",
        "eligible_relations": len(rows),
        "semantic_families": len({row["family_id"] for row in rows}),
        "suffix_identifiers": len({row["taddhita_source_variant"] for row in rows}),
        "by_family": dict(Counter(row["family_id"] for row in rows)),
        "by_visible_suffix": dict(Counter(row["visible_suffix"] for row in rows)),
        "inputs": {str(path.relative_to(HERE.parents[1])): sha256(path) for path in (CONFIG, CLASSIFICATION, *sorted(source_paths), Path(__file__))},
        "publication_status": "research_inventory_only_not_deployed",
    }
    (RESULTS / "suffix_conditioned_relations.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Additional Source-Conditioned Suffix Relations", "",
        f"Local source helpers and resolved constructed inputs supply **{len(rows)} additional relations** across {report['semantic_families']} semantic families and {report['suffix_identifiers']} suffix identifiers.", "",
        "Each row names its meaning before generation. No row enters merely because its finished form ends in -क or -य.", "",
    ]
    (RESULTS / "suffix_conditioned_relations.md").write_text("\n".join(lines))
    print(f"Materialized {len(rows)} source-conditioned suffix relations.")


if __name__ == "__main__":
    main()

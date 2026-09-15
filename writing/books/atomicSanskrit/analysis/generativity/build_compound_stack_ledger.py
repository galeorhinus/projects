#!/usr/bin/env python3
"""Pass 3: generate one additional operation from each eligible compound."""

from __future__ import annotations

from collections import Counter
import csv
import importlib.metadata
import json

from vidyut.prakriya import Dhatu, Pratipadika, Sanadi, Taddhita, Vyakarana

from compound_stack_common import (
    CONFIG, ELIGIBILITY, ELIGIBILITY_ROWS, RESULTS, project_path, read_csv,
    read_json, sha256, stable_id,
)
from nan_common import nan_surface


LEDGER = RESULTS / "compound_stack_candidates.csv"
EXCLUSIONS = RESULTS / "compound_stack_generation_exclusions.csv"
FIELDS = (
    "derived_word_meaning_id", "candidate_relation_id", "compound_word_meaning_id",
    "compound_type", "input_forms_slp1", "input_semantic_relation",
    "operation_family", "operation_id", "source_variant", "semantic_context",
    "semantic_branch_id", "semantic_relation", "rule_refs", "derivational_depth",
    "output_forms_slp1", "output_variant_count", "output_form_class",
    "generation_method", "admission_basis", "count_status",
)
EXCLUSION_FIELDS = FIELDS[:-7] + ("reason", "count_status")


def derive_forms(grammar: Vyakarana, row: dict[str, str]) -> tuple[str, ...]:
    outputs = set()
    for form in row["input_forms_slp1"].split(";"):
        base = Pratipadika.basic(form)
        if row["operation_family"] == "taddhita":
            suffix = getattr(Taddhita, row["source_variant"])
            request = Pratipadika.taddhitanta(base, suffix)
            outputs.update(result.text for result in grammar.derive(request))
        elif row["operation_family"] == "namadhatu":
            suffix = getattr(Sanadi, row["source_variant"])
            request = Dhatu.nama(base, nama_sanadi=suffix)
            outputs.update(result.text for result in grammar.derive(request))
        elif row["operation_family"] == "nan":
            outputs.add(nan_surface(form)[0])
        else:
            raise ValueError(f"Unknown operation family: {row['operation_family']}")
    return tuple(sorted(outputs))


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This ledger requires Vidyut 0.4.0")
    eligibility = read_json(ELIGIBILITY)
    rows = read_csv(ELIGIBILITY_ROWS)
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    admitted = Counter()
    excluded = Counter()
    variants = Counter()
    with LEDGER.open("w", newline="", encoding="utf-8") as good, EXCLUSIONS.open("w", newline="", encoding="utf-8") as bad:
        writer = csv.DictWriter(good, fieldnames=FIELDS)
        exclusion_writer = csv.DictWriter(bad, fieldnames=EXCLUSION_FIELDS)
        writer.writeheader()
        exclusion_writer.writeheader()
        for row in rows:
            try:
                outputs = derive_forms(grammar, row)
            except Exception as exc:
                outputs = ()
                reason = f"{type(exc).__name__}: {exc}"
            else:
                reason = "Pinned engine produced no form." if not outputs else ""
            if not outputs:
                exclusion_writer.writerow({
                    **{key: row[key] for key in EXCLUSION_FIELDS if key in row},
                    "reason": reason,
                    "count_status": "not_admitted_engine_zero_or_input_error",
                })
                excluded[row["operation_id"]] += 1
                continue
            output_class = "derived_verbal_base" if row["operation_family"] == "namadhatu" else "derived_nominal_base"
            writer.writerow({
                "derived_word_meaning_id": stable_id("compound-stack-output", row["candidate_relation_id"]),
                **row,
                "output_forms_slp1": ";".join(outputs),
                "output_variant_count": len(outputs),
                "output_form_class": output_class,
                "generation_method": "classified_surface_rules" if row["operation_family"] == "nan" else "vidyut_0_4_0_python",
                "admission_basis": "source_compound_meaning_plus_established_semantic_operation_plus_reproduced_form",
                "count_status": "candidate_generated_pending_reconciliation",
            })
            admitted[row["operation_id"]] += 1
            variants[row["operation_id"]] += len(outputs)
    if sum(admitted.values()) + sum(excluded.values()) != eligibility["eligible_relations"]:
        raise ValueError("Generation does not reconcile to eligibility")
    report = {
        "date": "2026-09-14",
        "eligible_relations": eligibility["eligible_relations"],
        "generated_candidate_relations": sum(admitted.values()),
        "engine_zero_or_error_relations": sum(excluded.values()),
        "generated_by_operation": dict(admitted),
        "excluded_by_operation": dict(excluded),
        "output_variants_by_operation": dict(variants),
        "engine_verified_relations": sum(value for key, value in admitted.items() if key != "nan_privative"),
        "classified_nan_surface_relations": admitted["nan_privative"],
        "inputs": {project_path(path): sha256(path) for path in (CONFIG, ELIGIBILITY, ELIGIBILITY_ROWS, __import__("pathlib").Path(__file__))},
        "publication_status": "candidate_ledger_not_yet_reconciled",
    }
    (RESULTS / "compound_stack_generation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Generated {report['generated_candidate_relations']} compound-input stack relations; excluded {report['engine_zero_or_error_relations']}.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate the eligible comparative and superlative word-meanings."""

from __future__ import annotations

from collections import Counter
import csv
import gzip
import hashlib
import importlib.metadata
import io
import json
from pathlib import Path

from vidyut.prakriya import Pratipadika, Taddhita, Vyakarana


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
INVENTORY = RESULTS / "nominal_input_inventory.csv.gz"
ELIGIBILITY = RESULTS / "taddhita_generalization_eligibility.json"
CONFIG = HERE / "taddhita_generalization_operations.json"
MANIFEST = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot/manifest.json"

FIELDS = (
    "derived_word_meaning_id", "nominal_word_meaning_id", "source_layer",
    "source_operation_id", "input_forms_slp1", "input_semantic_branch_id",
    "input_semantic_relation", "taddhita_operation_id", "taddhita_source_variant",
    "semantic_context", "semantic_branch_id", "semantic_relation", "rule_refs",
    "output_forms_slp1", "output_variant_count", "admission_basis", "count_status",
)
EXCLUSION_FIELDS = (
    "nominal_word_meaning_id", "input_forms_slp1", "input_semantic_branch_id",
    "taddhita_operation_id", "taddhita_source_variant", "rule_refs", "reason",
    "count_status",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def deterministic_writer(path: Path, fields: tuple[str, ...]):
    raw = path.open("wb")
    zipped = gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=6, mtime=0)
    text = io.TextIOWrapper(zipped, encoding="utf-8", newline="")
    writer = csv.DictWriter(text, fieldnames=fields)
    writer.writeheader()
    return raw, text, writer


def inventory_rows():
    with gzip.open(INVENTORY, "rt", newline="", encoding="utf-8") as handle:
        yield from csv.DictReader(handle)


def derive(grammar: Vyakarana, form: str, constructor: str, suffix) -> tuple[str, ...]:
    base = Pratipadika.nyap(form) if constructor == "nyap" else Pratipadika.basic(form)
    return tuple(sorted({
        result.text for result in grammar.derive(Pratipadika.taddhitanta(base, suffix))
    }))


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This ledger requires Vidyut 0.4.0")
    config = json.loads(CONFIG.read_text())
    eligibility = json.loads(ELIGIBILITY.read_text())
    eligible_counts = {
        row["operation_id"]: int(row["eligible_candidate_word_meanings"])
        for row in eligibility["operations"]
    }
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)

    ledger_path = RESULTS / "taddhita_generalization_candidates.csv.gz"
    exclusion_path = RESULTS / "taddhita_generalization_exclusions.csv.gz"
    lr, lt, lw = deterministic_writer(ledger_path, FIELDS)
    er, et, ew = deterministic_writer(exclusion_path, EXCLUSION_FIELDS)
    admitted: Counter[str] = Counter()
    excluded: Counter[str] = Counter()
    requests: Counter[str] = Counter()
    variants: Counter[str] = Counter()
    try:
        for operation in config["operations"]:
            op_id = operation["operation_id"]
            suffix = getattr(Taddhita, operation["source_variant"])
            cache: dict[tuple[str, str], tuple[tuple[str, ...], str]] = {}
            candidates = 0
            for row in inventory_rows():
                candidates += 1
                outputs: set[str] = set()
                errors: set[str] = set()
                for form in row["input_forms_slp1"].split(";"):
                    key = (row["constructor"], form)
                    if key not in cache:
                        try:
                            cache[key] = (derive(grammar, form, row["constructor"], suffix), "")
                        except Exception as exc:
                            cache[key] = ((), f"{type(exc).__name__}: {exc}")
                        requests[op_id] += 1
                    forms, error = cache[key]
                    outputs.update(forms)
                    if error:
                        errors.add(error)
                common = {
                    "nominal_word_meaning_id": row["nominal_word_meaning_id"],
                    "input_forms_slp1": row["input_forms_slp1"],
                    "input_semantic_branch_id": row["source_semantic_branch_id"],
                    "taddhita_operation_id": op_id,
                    "taddhita_source_variant": operation["source_variant"],
                    "rule_refs": ";".join(operation["rule_refs"]),
                }
                if outputs:
                    output_forms = sorted(outputs)
                    lw.writerow({
                        "derived_word_meaning_id": stable_id("taddhita-generalized", row["nominal_word_meaning_id"], op_id),
                        **common,
                        "source_layer": row["source_layer"],
                        "source_operation_id": row["source_operation_id"],
                        "input_semantic_relation": row["source_semantic_relation"],
                        "semantic_context": operation["semantic_context"],
                        "semantic_branch_id": operation["semantic_branch_id"],
                        "semantic_relation": operation["semantic_relation"],
                        "output_forms_slp1": ";".join(output_forms),
                        "output_variant_count": len(output_forms),
                        "admission_basis": "general_rule_plus_independently_classified_input_scope_plus_pinned_engine_output",
                        "count_status": "candidate_verified_by_engine",
                    })
                    admitted[op_id] += 1
                    variants[op_id] += len(output_forms)
                else:
                    ew.writerow({
                        **common,
                        "reason": "; ".join(sorted(errors)) if errors else "Pinned engine produced no form.",
                        "count_status": "not_admitted_engine_zero_or_input_error",
                    })
                    excluded[op_id] += 1
                if candidates % 250000 == 0:
                    print(f"{op_id}: processed {candidates:,}", flush=True)
            if candidates != eligible_counts[op_id]:
                raise ValueError(f"Eligibility mismatch for {op_id}: {candidates} != {eligible_counts[op_id]}")
    finally:
        lt.flush(); lt.close(); lr.close()
        et.flush(); et.close(); er.close()

    manifest = json.loads(MANIFEST.read_text())
    report = {
        "date": "2026-09-14",
        "eligible_operation_relations": sum(eligible_counts.values()),
        "engine_verified_candidate_relations": sum(admitted.values()),
        "engine_zero_or_error_relations": sum(excluded.values()),
        "verified_by_operation": dict(admitted),
        "excluded_by_operation": dict(excluded),
        "engine_requests_after_form_cache": dict(requests),
        "generated_output_variants_by_operation": dict(variants),
        "engine": {"name": "Vidyut", "version": "0.4.0", "commit": manifest["generator_commit"]},
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (INVENTORY, ELIGIBILITY, CONFIG, MANIFEST, Path(__file__))
        },
        "publication_status": "candidate_ledger_not_yet_reconciled",
    }
    (RESULTS / "taddhita_generalization_generation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        f"Engine verified {report['engine_verified_candidate_relations']:,} relations; "
        f"excluded {report['engine_zero_or_error_relations']:,}."
    )


if __name__ == "__main__":
    main()

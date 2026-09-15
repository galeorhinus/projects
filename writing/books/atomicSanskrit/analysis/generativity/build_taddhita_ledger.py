#!/usr/bin/env python3
"""Materialize the first broad taddhita word-meaning ledger."""

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
ELIGIBILITY = RESULTS / "taddhita_eligibility.json"
CONFIG = HERE / "taddhita_operations.json"
MANIFEST = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot/manifest.json"
TADDHITA_MANIFEST = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot/taddhita_manifest.json"

LEDGER_FIELDS = (
    "derived_word_meaning_id", "nominal_word_meaning_id", "source_layer",
    "source_operation_id", "input_forms_slp1", "taddhita_operation_id",
    "taddhita_source_variant", "operation_display", "semantic_context",
    "semantic_branch_id", "semantic_relation", "source_semantic_relation",
    "rule_refs", "output_forms_slp1", "output_variant_count",
    "admission_basis", "count_status",
)
EXCLUSION_FIELDS = (
    "nominal_word_meaning_id", "source_layer", "input_forms_slp1",
    "taddhita_operation_id", "taddhita_source_variant", "semantic_context",
    "semantic_relation", "rule_refs", "reason", "count_status",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:20]


def deterministic_gzip_writer(path: Path, fields: tuple[str, ...]):
    raw = path.open("wb")
    zipped = gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=6, mtime=0)
    text = io.TextIOWrapper(zipped, encoding="utf-8", newline="")
    writer = csv.DictWriter(text, fieldnames=fields)
    writer.writeheader()
    return raw, text, writer


def inventory_rows():
    with gzip.open(INVENTORY, "rt", newline="", encoding="utf-8") as handle:
        yield from csv.DictReader(handle)


def derive_forms(grammar: Vyakarana, input_form: str, constructor: str, suffix) -> tuple[str, ...]:
    base = Pratipadika.nyap(input_form) if constructor == "nyap" else Pratipadika.basic(input_form)
    return tuple(sorted({
        result.text
        for result in grammar.derive(Pratipadika.taddhitanta(base, suffix))
    }))


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This ledger requires Vidyut 0.4.0")
    eligibility = json.loads(ELIGIBILITY.read_text())
    operations = json.loads(CONFIG.read_text())["operations"]
    eligible_counts = {
        row["operation_id"]: int(row["eligible_candidate_word_meanings"])
        for row in eligibility["operations"]
    }
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    ledger_path = RESULTS / "taddhita_ledger.csv.gz"
    exclusions_path = RESULTS / "taddhita_exclusions.csv.gz"
    ledger_raw, ledger_text, ledger_writer = deterministic_gzip_writer(ledger_path, LEDGER_FIELDS)
    excluded_raw, excluded_text, excluded_writer = deterministic_gzip_writer(exclusions_path, EXCLUSION_FIELDS)

    admitted = Counter()
    excluded = Counter()
    engine_requests = Counter()
    output_variants = Counter()
    try:
        for operation in operations:
            operation_id = operation["operation_id"]
            suffix = getattr(Taddhita, operation["source_variant"])
            listed = set(operation.get("eligible_nominal_ids", []))
            cache: dict[tuple[str, str], tuple[tuple[str, ...], str]] = {}
            candidates = 0
            for row in inventory_rows():
                if operation["eligibility_scope"] == "listed_nominal_ids" and row["nominal_word_meaning_id"] not in listed:
                    continue
                candidates += 1
                outputs: set[str] = set()
                errors: list[str] = []
                for input_form in row["input_forms_slp1"].split(";"):
                    key = (row["constructor"], input_form)
                    cached = cache.get(key)
                    if cached is None:
                        try:
                            forms = derive_forms(grammar, input_form, row["constructor"], suffix)
                            cached = (forms, "")
                        except Exception as exc:  # Preserve an engine/input failure as unresolved evidence.
                            cached = ((), f"{type(exc).__name__}: {exc}")
                        cache[key] = cached
                        engine_requests[operation_id] += 1
                    outputs.update(cached[0])
                    if cached[1]:
                        errors.append(cached[1])

                common = {
                    "nominal_word_meaning_id": row["nominal_word_meaning_id"],
                    "source_layer": row["source_layer"],
                    "input_forms_slp1": row["input_forms_slp1"],
                    "taddhita_operation_id": operation_id,
                    "taddhita_source_variant": operation["source_variant"],
                    "semantic_context": operation["semantic_context"],
                    "semantic_relation": operation["semantic_relation"],
                    "rule_refs": ";".join(operation["rule_refs"]),
                }
                if outputs:
                    forms = sorted(outputs)
                    ledger_writer.writerow({
                        "derived_word_meaning_id": stable_id("taddhita", row["nominal_word_meaning_id"], operation_id),
                        **common,
                        "source_operation_id": row["source_operation_id"],
                        "operation_display": operation["operation_display"],
                        "semantic_branch_id": operation["semantic_branch_id"],
                        "source_semantic_relation": row["source_semantic_relation"],
                        "output_forms_slp1": ";".join(forms),
                        "output_variant_count": len(forms),
                        "admission_basis": "admitted_nominal_word_meaning_plus_sourced_semantic_relation_plus_pinned_engine_output",
                        "count_status": "admitted_research_ledger",
                    })
                    admitted[operation_id] += 1
                    output_variants[operation_id] += len(forms)
                else:
                    excluded_writer.writerow({
                        **common,
                        "reason": "; ".join(sorted(set(errors))) if errors else "Pinned engine produced no form for this eligible operation relation.",
                        "count_status": "not_admitted_engine_zero_or_input_error_unresolved",
                    })
                    excluded[operation_id] += 1
                if candidates % 250000 == 0:
                    print(f"{operation_id}: processed {candidates:,}", flush=True)
            if candidates != eligible_counts[operation_id]:
                raise ValueError(f"Eligibility mismatch for {operation_id}: {candidates} != {eligible_counts[operation_id]}")
    finally:
        ledger_text.flush()
        ledger_text.close()
        ledger_raw.close()
        excluded_text.flush()
        excluded_text.close()
        excluded_raw.close()

    manifest = json.loads(MANIFEST.read_text())
    taddhita_manifest = json.loads(TADDHITA_MANIFEST.read_text())
    source_names = {
        "vidyut-args-taddhita.rs", "rule-4.1.92.html", "rule-4.1.120.html",
        "rule-5.1.119.html", "rule-5.2.94.html",
    }
    report = {
        "date": "2026-09-13",
        "scope": json.loads(CONFIG.read_text())["scope"],
        "eligible_operation_candidates": sum(eligible_counts.values()),
        "admitted_taddhita_word_meanings": sum(admitted.values()),
        "not_admitted_total": sum(excluded.values()),
        "admitted_by_operation": dict(admitted),
        "not_admitted_by_operation": dict(excluded),
        "engine_requests_after_form_cache": dict(engine_requests),
        "generated_output_variants_by_operation": dict(output_variants),
        "engine": {"name": "Vidyut", "version": "0.4.0", "commit": manifest["generator_commit"]},
        "sources": [row for row in manifest["sources"] if row["filename"] in source_names]
        + taddhita_manifest["sources"],
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (INVENTORY, ELIGIBILITY, CONFIG, MANIFEST, TADDHITA_MANIFEST, Path(__file__))},
        "publication_status": "bounded_research_subtotal_not_deployed",
    }
    (RESULTS / "taddhita_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# First Broad तद्धित Generation", "",
        "This pass applies three general तद्धित relations to the declared लौकिक nominal word-meaning inventory and retains the three bounded ढक् descent examples. A semantic relation enters the ledger only when its source condition admits the input and the pinned engine constructs at least one form.", "",
        "| Operation | Eligible relations | Admitted word-meanings | Unresolved engine zero or input error |", "|---|---:|---:|---:|",
    ]
    for operation in operations:
        op = operation["operation_id"]
        lines.append(f"| {op} | {eligible_counts[op]:,} | {admitted[op]:,} | {excluded[op]:,} |")
    lines.extend([
        f"| **Total** | **{sum(eligible_counts.values()):,}** | **{sum(admitted.values()):,}** | **{sum(excluded.values()):,}** |", "",
        "Alternative outputs produced from alternative forms of one nominal word-meaning remain attached to one तद्धित word-meaning. Coincident output spellings do not merge distinct input meanings or semantic operations.", "",
        "The remaining तद्धित identifiers are not rejected. Their rules require narrower nominal classes or contexts and remain available for later conditioned passes.", "",
    ])
    (RESULTS / "taddhita_summary.md").write_text("\n".join(lines))
    print(f"Admitted {sum(admitted.values())} taddhita word-meanings; left {sum(excluded.values())} unresolved.")


if __name__ == "__main__":
    main()

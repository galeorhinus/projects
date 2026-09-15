#!/usr/bin/env python3
"""Pass 3: reconstruct and generate broader lexical feminine relations."""

from __future__ import annotations

from collections import Counter
import csv
import gzip
import importlib.metadata
import json
from pathlib import Path

from vidyut.prakriya import Data, Krt, Linga, Pada, Pratipadika, Sanadi, Vacana, Vibhakti, Vyakarana

from stri_generalization_common import (
    ARCHIVE, ELIGIBILITY, EXCLUSIONS, LEDGER, RESULTS,
    close_gzip_writer, deterministic_gzip_writer, project_path, sha256, stable_id,
)


UPASARGAS = Path(__file__).resolve().parent / "upasarga_inventory.csv"
STRI_MANIFEST = ARCHIVE / "stri_manifest.json"
CORE_MANIFEST = ARCHIVE / "manifest.json"
STRI_SUFFIXES = {"cAp", "wAp", "qAp", "NIn", "NIp", "NIz", "UN"}
SANADI_STACKS = {
    "causative": [Sanadi.Ric],
    "desiderative": [Sanadi.san],
    "intensive": [Sanadi.yaN],
    "intensive_luk": [Sanadi.yaNluk],
    "curadi_true_causative": [Sanadi.Ric, Sanadi.Ric],
}
FIELDS = [
    "generated_word_meaning_id", "nominal_word_meaning_id", "source_layer",
    "source_word_meaning_id", "source_operation_id", "krt_source_variant",
    "base_count_key", "base_source_codes", "input_forms_slp1",
    "source_semantic_relation", "feminine_semantic_relation", "upasarga_id",
    "source_sanadi_operation_id", "sanadi_stack", "generated_forms_slp1",
    "generated_variant_count", "applied_stri_suffixes", "applied_rule_refs",
    "rule_refs", "admission_basis", "count_status",
]
EXCLUSION_FIELDS = [
    "nominal_word_meaning_id", "source_operation_id", "base_count_key",
    "base_source_codes", "reason", "count_status",
]


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This generation requires Vidyut 0.4.0")
    for manifest_path in (STRI_MANIFEST, CORE_MANIFEST):
        manifest = json.loads(manifest_path.read_text())
        for record in manifest["sources"]:
            path = ARCHIVE / record["filename"]
            if path.exists() and sha256(path) != record["sha256"]:
                raise ValueError(f"Archived source changed: {record['filename']}")

    entries = {entry.code: entry for entry in Data(str(ARCHIVE)).load_dhatu_entries()}
    with open(UPASARGAS, encoding="utf-8", newline="") as handle:
        prefix_map = {row["upasarga_id"]: row["engine_input_slp1"] for row in csv.DictReader(handle)}
    with gzip.open(ELIGIBILITY, "rt", encoding="utf-8", newline="") as handle:
        candidates = list(csv.DictReader(handle))

    grammar = Vyakarana(log_steps=True, is_chandasi=False, use_svaras=False, nlp_mode=False)
    cache = {}
    admitted = excluded = 0
    by_operation = Counter()
    suffix_counts = Counter()
    rule_counts = Counter()
    ledger_raw, ledger_text, ledger_writer = deterministic_gzip_writer(LEDGER, FIELDS)
    exclusion_raw, exclusion_text, exclusion_writer = deterministic_gzip_writer(EXCLUSIONS, EXCLUSION_FIELDS)
    try:
        for candidate in candidates:
            forms = set()
            suffixes = set()
            rules = set()
            codes = [code for code in candidate["base_source_codes"].split(";") if code]
            for code in codes:
                key = (
                    candidate["source_layer"], candidate["source_operation_id"], code,
                    candidate["upasarga_id"], candidate["source_sanadi_operation_id"],
                )
                cached = cache.get(key)
                if cached is None:
                    dhatu = entries[code].dhatu
                    if candidate["upasarga_id"]:
                        dhatu = dhatu.with_prefixes([prefix_map[candidate["upasarga_id"]]])
                    if candidate["source_sanadi_operation_id"]:
                        dhatu = dhatu.with_sanadi(SANADI_STACKS[candidate["source_sanadi_operation_id"]])
                    base = Pratipadika.krdanta(dhatu, getattr(Krt, candidate["krt_source_variant"]))
                    generated = []
                    for result in grammar.derive(Pada.Subanta(base, Linga.Stri, Vibhakti.Prathama, Vacana.Eka)):
                        result_suffixes = set()
                        result_rules = set()
                        previous_terms = Counter()
                        for step in result.history:
                            current_terms = Counter(step.result)
                            inserted_terms = current_terms - previous_terms
                            found = STRI_SUFFIXES.intersection(inserted_terms)
                            if found and step.code.startswith("4.1"):
                                result_suffixes.update(found)
                                result_rules.add(step.code)
                            previous_terms = current_terms
                        if result_suffixes:
                            generated.append((result.text, result_suffixes, result_rules))
                    cached = generated
                    cache[key] = cached
                for form, found_suffixes, found_rules in cached:
                    forms.add(form)
                    suffixes.update(found_suffixes)
                    rules.update(found_rules)

            if not forms:
                exclusion_writer.writerow({
                    "nominal_word_meaning_id": candidate["nominal_word_meaning_id"],
                    "source_operation_id": candidate["source_operation_id"],
                    "base_count_key": candidate["base_count_key"],
                    "base_source_codes": candidate["base_source_codes"],
                    "reason": "The reconstructed source operation produced no feminine path carrying a स्त्रीप्रत्यय in Vidyut 0.4.0.",
                    "count_status": "not_admitted_engine_or_rule_condition_unmet",
                })
                excluded += 1
                continue
            ledger_writer.writerow({
                "generated_word_meaning_id": stable_id("stri-generalized", candidate["nominal_word_meaning_id"]),
                **{field: candidate[field] for field in (
                    "nominal_word_meaning_id", "source_layer", "source_word_meaning_id",
                    "source_operation_id", "krt_source_variant", "base_count_key",
                    "base_source_codes", "input_forms_slp1", "source_semantic_relation",
                    "feminine_semantic_relation", "upasarga_id",
                    "source_sanadi_operation_id", "sanadi_stack", "rule_refs",
                )},
                "generated_forms_slp1": ";".join(sorted(forms)),
                "generated_variant_count": len(forms),
                "applied_stri_suffixes": ";".join(sorted(suffixes)),
                "applied_rule_refs": ";".join(sorted(rules)),
                "admission_basis": "lexical_agent_semantics_plus_reconstructed_source_operation_plus_pinned_engine_stri_derivation",
                "count_status": "admitted_generalized_stri_word_meaning",
            })
            admitted += 1
            by_operation[candidate["source_operation_id"]] += 1
            suffix_counts.update(suffixes)
            rule_counts.update(rules)
    finally:
        close_gzip_writer(ledger_raw, ledger_text)
        close_gzip_writer(exclusion_raw, exclusion_text)

    report = {
        "date": "2026-09-14",
        "eligible_candidates": len(candidates),
        "engine_verified_relations": admitted,
        "engine_zero_or_no_stri_suffix_relations": excluded,
        "generated_by_source_operation": dict(sorted(by_operation.items())),
        "applied_stri_suffix_counts": dict(sorted(suffix_counts.items())),
        "applied_rule_counts": dict(sorted(rule_counts.items())),
        "cached_source_constructions": len(cache),
        "engine": {"name": "Vidyut", "version": importlib.metadata.version("vidyut")},
        "inputs": {
            project_path(path): sha256(path)
            for path in (ELIGIBILITY, UPASARGAS, STRI_MANIFEST, CORE_MANIFEST, Path(__file__))
        },
        "publication_status": "research_generation_only_not_deployed",
    }
    (RESULTS / "stri_generalization_generation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(f"Generated {admitted:,} lexical feminine relations; excluded {excluded:,}.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Pass 4: materialize broad and source-conditioned namadhatu meanings."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import gzip
import importlib.metadata
import io
import json

from vidyut.prakriya import (
    Dhatu, DhatuPada, Lakara, Pada, Pratipadika, Prayoga, Purusha,
    Sanadi, Vacana, Vyakarana,
)

from namadhatu_common import (
    CORE_MANIFEST, NAMADHATU_MANIFEST, NOMINAL_INVENTORY, RESULTS,
    project_path, sha256, stable_id,
)


HERE = __import__("pathlib").Path(__file__).resolve().parent
CONFIG = HERE / "namadhatu_operations.json"
ELIGIBILITY = RESULTS / "namadhatu_eligibility.json"
EXAMPLES = RESULTS / "namadhatu_source_examples.csv"

LEDGER_FIELDS = (
    "derived_word_meaning_id", "source_kind", "nominal_word_meaning_id",
    "source_layer", "input_forms_slp1", "prefixes_slp1",
    "namadhatu_operation_id", "constructor", "operation_display",
    "semantic_branch_id", "semantic_relation", "rule_refs",
    "output_base_forms_slp1", "output_variant_count", "source_example_id",
    "admission_basis", "form_status", "count_status",
)
EXCLUSION_FIELDS = (
    "source_kind", "nominal_word_meaning_id", "input_forms_slp1",
    "prefixes_slp1", "namadhatu_operation_id", "constructor",
    "semantic_relation", "rule_refs", "source_example_id", "reason",
    "count_status",
)


def deterministic_gzip_writer(path, fields):
    raw = path.open("wb")
    zipped = gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=6, mtime=0)
    text = io.TextIOWrapper(zipped, encoding="utf-8", newline="")
    writer = csv.DictWriter(text, fieldnames=fields)
    writer.writeheader()
    return raw, text, writer


def nominal_rows():
    with gzip.open(NOMINAL_INVENTORY, "rt", newline="", encoding="utf-8") as handle:
        yield from csv.DictReader(handle)


def pratipadika(form: str, constructor: str):
    return Pratipadika.nyap(form) if constructor == "nyap" else Pratipadika.basic(form)


def derive_base_forms(grammar, form: str, nominal_constructor: str, namadhatu_constructor: str, prefixes=()):
    suffix = None if namadhatu_constructor == "auto" else getattr(Sanadi, namadhatu_constructor)
    dhatu = Dhatu.nama(pratipadika(form, nominal_constructor), nama_sanadi=suffix)
    if prefixes:
        dhatu = dhatu.with_prefixes(list(prefixes))
    return dhatu, tuple(sorted({result.text for result in grammar.derive(dhatu)}))


def derive_present_forms(grammar, dhatu):
    forms = set()
    for pada in (DhatuPada.Parasmaipada, DhatuPada.Atmanepada):
        request = Pada.Tinanta(
            dhatu, Prayoga.Kartari, Lakara.Lat, Purusha.Prathama,
            Vacana.Eka, dhatu_pada=pada,
        )
        forms.update(result.text for result in grammar.derive(request))
    return forms


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This ledger requires Vidyut 0.4.0")
    config = json.loads(CONFIG.read_text())
    eligibility = json.loads(ELIGIBILITY.read_text())
    expected_broad = eligibility["broad_candidate_relations"]
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)

    ledger_path = RESULTS / "namadhatu_ledger.csv.gz"
    exclusions_path = RESULTS / "namadhatu_exclusions.csv.gz"
    ledger_raw, ledger_text, ledger_writer = deterministic_gzip_writer(ledger_path, LEDGER_FIELDS)
    exclusion_raw, exclusion_text, exclusion_writer = deterministic_gzip_writer(exclusions_path, EXCLUSION_FIELDS)
    admitted = Counter()
    excluded = Counter()
    engine_requests = Counter()
    output_variants = Counter()
    source_finite_verifications = 0
    try:
        by_constructor = defaultdict(list)
        for operation in config["broad_operations"]:
            by_constructor[operation["constructor"]].append(operation)
        processed_broad = 0
        for constructor, operations in by_constructor.items():
            cache = {}
            for index, row in enumerate(nominal_rows(), start=1):
                outputs = set()
                errors = []
                for form in row["input_forms_slp1"].split(";"):
                    key = (row["constructor"], form)
                    if key not in cache:
                        try:
                            _, forms = derive_base_forms(grammar, form, row["constructor"], constructor)
                            cache[key] = (forms, "")
                        except Exception as exc:
                            cache[key] = ((), f"{type(exc).__name__}: {exc}")
                        engine_requests[constructor] += 1
                    outputs.update(cache[key][0])
                    if cache[key][1]:
                        errors.append(cache[key][1])
                for operation in operations:
                    operation_id = operation["operation_id"]
                    common = {
                        "source_kind": "broad_productive_relation",
                        "nominal_word_meaning_id": row["nominal_word_meaning_id"],
                        "input_forms_slp1": row["input_forms_slp1"],
                        "prefixes_slp1": "",
                        "namadhatu_operation_id": operation_id,
                        "constructor": constructor,
                        "semantic_relation": operation["semantic_relation"],
                        "rule_refs": ";".join(operation["rule_refs"]),
                        "source_example_id": "",
                    }
                    if outputs:
                        forms = sorted(outputs)
                        ledger_writer.writerow({
                            "derived_word_meaning_id": stable_id("namadhatu", row["nominal_word_meaning_id"], operation_id),
                            **common,
                            "source_layer": row["source_layer"],
                            "operation_display": operation["operation_display"],
                            "semantic_branch_id": operation["semantic_branch_id"],
                            "output_base_forms_slp1": ";".join(forms),
                            "output_variant_count": len(forms),
                            "admission_basis": "admitted_nominal_meaning_plus_productive_semantic_relation_plus_pinned_engine_output",
                            "form_status": "derived_verbal_base_not_inflected_tinanta",
                            "count_status": "admitted_research_ledger",
                        })
                        admitted[operation_id] += 1
                        output_variants[operation_id] += len(forms)
                    else:
                        exclusion_writer.writerow({
                            **common,
                            "reason": "; ".join(sorted(set(errors))) if errors else "Pinned engine produced no derived verbal base.",
                            "count_status": "not_admitted_engine_zero_or_input_error_unresolved",
                        })
                        excluded[operation_id] += 1
                    processed_broad += 1
                if index % 100000 == 0:
                    print(f"{constructor}: processed {index:,} nominal meanings", flush=True)
            cache.clear()
        if processed_broad != expected_broad:
            raise ValueError(f"Broad eligibility mismatch: {processed_broad} != {expected_broad}")

        with EXAMPLES.open(newline="", encoding="utf-8") as handle:
            examples = [row for row in csv.DictReader(handle) if row["source_test_status"] == "active" and row["operation_scope"] == "conditioned_example"]
        for row in examples:
            prefixes = tuple(x for x in row["prefixes_slp1"].split(";") if x)
            try:
                dhatu, base_forms = derive_base_forms(grammar, row["input_form_slp1"], "basic", row["constructor"], prefixes)
                present_forms = derive_present_forms(grammar, dhatu)
                expected_present = set(row["expected_present_forms_slp1"].split(";"))
                finite_verified = expected_present <= present_forms
            except Exception as exc:
                base_forms = ()
                finite_verified = False
                error = f"{type(exc).__name__}: {exc}"
            else:
                error = ""
            operation_id = f"conditioned_{row['rule_ref'].replace('.', '_')}_{row['source_example_id']}"
            common = {
                "source_kind": "source_demonstrated_conditioned_relation",
                "nominal_word_meaning_id": f"source-example:{row['source_example_id']}",
                "input_forms_slp1": row["input_form_slp1"],
                "prefixes_slp1": row["prefixes_slp1"],
                "namadhatu_operation_id": operation_id,
                "constructor": row["constructor"],
                "semantic_relation": row["semantic_relation"],
                "rule_refs": row["rule_ref"],
                "source_example_id": row["source_example_id"],
            }
            if base_forms and finite_verified:
                ledger_writer.writerow({
                    "derived_word_meaning_id": stable_id("namadhatu-conditioned", row["source_example_id"]),
                    **common,
                    "source_layer": "direct_source_example",
                    "operation_display": f"Rule {row['rule_ref']} conditioned नामधातुः",
                    "semantic_branch_id": f"conditioned_{row['rule_ref'].replace('.', '_')}",
                    "output_base_forms_slp1": ";".join(base_forms),
                    "output_variant_count": len(base_forms),
                    "admission_basis": "source_located_relation_plus_expected_present_form_plus_pinned_engine_reproduction",
                    "form_status": "derived_verbal_base_not_inflected_tinanta",
                    "count_status": "admitted_research_ledger",
                })
                admitted["conditioned_source_relations"] += 1
                output_variants["conditioned_source_relations"] += len(base_forms)
                source_finite_verifications += 1
            else:
                reason = error or "Pinned engine did not reproduce the source's present-tense evidence for this relation."
                exclusion_writer.writerow({
                    **common,
                    "reason": reason,
                    "count_status": "not_admitted_source_example_verification_failed",
                })
                excluded["conditioned_source_relations"] += 1
    finally:
        ledger_text.flush(); ledger_text.close(); ledger_raw.close()
        exclusion_text.flush(); exclusion_text.close(); exclusion_raw.close()

    core = json.loads(CORE_MANIFEST.read_text())
    report = {
        "date": "2026-09-13",
        "eligible_candidate_relations": eligibility["total_candidate_relations"],
        "admitted_namadhatu_word_meanings": sum(admitted.values()),
        "not_admitted_total": sum(excluded.values()),
        "admitted_by_operation": dict(admitted),
        "not_admitted_by_operation": dict(excluded),
        "engine_requests_after_form_cache": dict(engine_requests),
        "generated_output_variants_by_operation": dict(output_variants),
        "source_present_form_verifications": source_finite_verifications,
        "engine": {"name": "Vidyut", "version": "0.4.0", "commit": core["generator_commit"]},
        "form_status": "Every admitted row is a derived verbal base meaning. No finite tinanta form is counted in this ledger.",
        "inputs": {project_path(path): sha256(path) for path in (
            NOMINAL_INVENTORY, CONFIG, ELIGIBILITY, EXAMPLES, CORE_MANIFEST,
            NAMADHATU_MANIFEST, __import__("pathlib").Path(__file__)
        )},
        "publication_status": "bounded_research_subtotal_not_deployed",
    }
    (RESULTS / "namadhatu_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# नामधातुः Generation", "",
        "The productive layer converts each admitted nominal meaning into four verbal meanings: two formations of self-related desire, treatment of an object by comparison, and conduct of an agent by comparison. Narrower rules contribute only source-demonstrated relations.", "",
        "| Operation | Admitted meanings | Unresolved |", "|---|---:|---:|",
    ]
    for operation in config["broad_operations"]:
        op = operation["operation_id"]
        lines.append(f"| {op} | {admitted[op]:,} | {excluded[op]:,} |")
    lines.extend([
        f"| Source-conditioned relations | {admitted['conditioned_source_relations']:,} | {excluded['conditioned_source_relations']:,} |",
        f"| **Total** | **{sum(admitted.values()):,}** | **{sum(excluded.values()):,}** |", "",
        "The generated object is a derived verbal base, not a finite तिङन्त word. The source examples' present-tense forms verify the operation but do not enter this lexical subtotal.", "",
    ])
    (RESULTS / "namadhatu_summary.md").write_text("\n".join(lines))
    print(f"Admitted {sum(admitted.values())} namadhatu word-meanings; left {sum(excluded.values())} unresolved.")


if __name__ == "__main__":
    main()

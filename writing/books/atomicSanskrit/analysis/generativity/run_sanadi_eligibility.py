#!/usr/bin/env python3
"""Run a bounded verbal-base sanadi census without admitting candidates to the count."""

from __future__ import annotations

from collections import defaultdict
import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path

from vidyut.prakriya import Data, Sanadi, Vyakarana


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
RESULTS = HERE / "results"
ASSIGNMENTS = RESULTS / "current_base_assignments.csv"
CURRENT_COUNT = RESULTS / "current_base_meanings.json"
MANIFEST = ARCHIVE / "manifest.json"

OPERATIONS = (
    {
        "operation_id": "causative",
        "display_label": "णिजन्त (ṇijanta), causative",
        "sanadi": "Ric",
        "relation": "cause the base action or state",
        "rule_refs": "3.1.26",
    },
    {
        "operation_id": "desiderative",
        "display_label": "सन्नन्त (sannanta), desiderative",
        "sanadi": "san",
        "relation": "desire to perform the base action by the same agent",
        "rule_refs": "3.1.7",
    },
    {
        "operation_id": "intensive",
        "display_label": "यङन्त (yaṅanta), intensive",
        "sanadi": "yaN",
        "relation": "perform the base action repeatedly or intensely",
        "rule_refs": "3.1.22",
    },
    {
        "operation_id": "intensive_luk",
        "display_label": "यङ्लुगन्त (yaṅluganta), intensive with luk",
        "sanadi": "yaNluk",
        "relation": "perform the base action repeatedly or intensely through the luk formation",
        "rule_refs": "3.1.22;2.4.74",
    },
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sources() -> dict:
    manifest = json.loads(MANIFEST.read_text())
    for record in manifest["sources"]:
        path = ARCHIVE / record["filename"]
        if sha256(path) != record["sha256"]:
            raise ValueError(f"Archived source changed: {path}")
    return manifest


def load_assignments() -> tuple[list[dict[str, str]], dict[str, list[dict[str, str]]]]:
    with ASSIGNMENTS.open() as handle:
        rows = list(csv.DictReader(handle))
    lexical = [row for row in rows if row["record_kind"] == "lexical"]
    by_code: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in lexical:
        by_code[row["source_code"]].append(row)
    return lexical, by_code


def run_engine(entries, grammar: Vyakarana) -> list[dict[str, str]]:
    rows = []
    for operation in OPERATIONS:
        sanadi = getattr(Sanadi, operation["sanadi"])
        for entry in entries:
            outputs = sorted({p.text for p in grammar.derive(entry.dhatu.with_sanadi([sanadi]))})
            rows.append({
                **operation,
                "source_code": entry.code,
                "gana": str(entry.dhatu.gana),
                "aupadeshika_slp1": entry.dhatu.aupadeshika,
                "source_artha_slp1": entry.artha,
                "engine_status": "generated" if outputs else "zero_output_unresolved",
                "output_count": str(len(outputs)),
                "output_forms_slp1": ";".join(outputs),
                "eligibility_status": "candidate_semantic_review_pending" if outputs else "not_admitted_cause_unresolved",
                "count_status": "not_admitted",
            })
    return rows


def candidate_rows(engine_rows, assignments_by_code) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], dict[str, set[str] | str]] = {}
    for engine_row in engine_rows:
        outputs = [value for value in engine_row["output_forms_slp1"].split(";") if value]
        for base in assignments_by_code.get(engine_row["source_code"], []):
            if outputs:
                key = (engine_row["operation_id"], base["normalized_count_key"])
                item = grouped.setdefault(key, {
                    "operation_id": engine_row["operation_id"],
                    "sanadi": engine_row["sanadi"],
                    "relation": engine_row["relation"],
                    "rule_refs": engine_row["rule_refs"],
                    "base_count_key": base["normalized_count_key"],
                    "base_meaning_slp1": set(),
                    "base_meaning_display": set(),
                    "base_source_codes": set(),
                    "base_citations_slp1": set(),
                    "output_forms_slp1": set(),
                    "semantic_eligibility_status": "pending",
                    "count_status": "not_admitted",
                })
                item["base_meaning_slp1"].add(base["normalized_meaning_slp1"])
                item["base_meaning_display"].add(base["meaning_display"])
                item["base_source_codes"].add(base["source_code"])
                item["base_citations_slp1"].add(base["normalized_citation_slp1"])
                item["output_forms_slp1"].update(outputs)
    rows = []
    for item in grouped.values():
        row = {key: ";".join(sorted(value)) if isinstance(value, set) else value
               for key, value in item.items()}
        row["output_variant_count"] = str(len(item["output_forms_slp1"]))
        rows.append(row)
    return sorted(rows, key=lambda row: (row["operation_id"], row["base_count_key"]))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def build_report(engine_rows, candidates, lexical, entries, manifest) -> dict:
    current = json.loads(CURRENT_COUNT.read_text())
    represented_codes = {row["source_code"] for row in lexical}
    by_operation = []
    for operation in OPERATIONS:
        operation_id = operation["operation_id"]
        engine = [row for row in engine_rows if row["operation_id"] == operation_id]
        candidate = [row for row in candidates if row["operation_id"] == operation_id]
        by_operation.append({
            **operation,
            "source_entries_tested": len(engine),
            "source_entries_with_output": sum(row["engine_status"] == "generated" for row in engine),
            "source_entries_with_zero_output": sum(row["engine_status"] != "generated" for row in engine),
            "base_word_meanings_with_output": len({row["base_count_key"] for row in candidate}),
            "candidate_derived_word_meanings": len(candidate),
            "distinct_output_spellings_diagnostic": len({output for row in candidate for output in row["output_forms_slp1"].split(";")}),
            "admitted_derived_word_meanings": 0,
        })
    source_names = {"vidyut-args-dhatu.rs", "rule-3.1.7.html", "rule-3.1.22.html", "rule-3.1.26.html", "rule-2.4.74.html"}
    records = {row["filename"]: row for row in manifest["sources"]}
    return {
        "date": "2026-09-13",
        "scope": "One sanadi-pratyaya operation, no upasarga, applied to each pinned dhatu source entry; pratipadika-input sanadi operations deferred.",
        "engine": {"name": "Vidyut", "version": importlib.metadata.version("vidyut"), "commit": manifest["generator_commit"]},
        "counting_unit": "A candidate is keyed by operation and reconciled base word-meaning. Coincident spellings do not merge different meanings; alternative generated forms remain attached to the same candidate unless separate evidence establishes different words or meanings.",
        "current_base_word_meanings": current["current_provisional_assignments"],
        "preserved_assignment_rows": current["preserved_source_rows"],
        "lexical_assignment_rows": len(lexical),
        "source_entries_tested": len(entries),
        "source_entries_without_admitted_meaning": sorted({entry.code for entry in entries} - represented_codes),
        "verbal_operations": by_operation,
        "nominal_input_operations_deferred": ["kAmyac", "kyaN", "kyac"],
        "vocabulary_total": None,
        "candidate_rows_are_not_a_count": True,
        "known_semantic_control": {
            "rule": "3.1.22",
            "source_statement": "The Kashika commentary excludes the general yan formation of shobhate and rocate through anabhidhana.",
            "engine_outputs": {
                "01.0847 ruc": ["rorucya", "roruc"],
                "06.0046 shubh": ["SoSuBya", "SoSuB"],
            },
            "disposition": "Retain as generated candidates but do not admit them without semantic review.",
        },
        "limits": [
            "Engine output establishes software generation, not semantic eligibility or attested lexical use.",
            "Zero output is retained as unresolved; it is not automatically called a grammatical prohibition.",
            "The three nominal-input sanadi identifiers require a separately bounded nominal inventory.",
            "No prefixes, operation stacking, inflection, Vedic-only extensions, or compounds enter this run.",
        ],
        "sources": [records[name] for name in sorted(source_names)],
        "inputs": {str(path.relative_to(ROOT)): sha256(path) for path in (
            ASSIGNMENTS, CURRENT_COUNT, HERE / "operations.csv", MANIFEST, Path(__file__))},
    }


def write_markdown(report: dict) -> None:
    lines = [
        "# Bounded सनादि (sanādi) Eligibility Pass", "",
        "This pass applies one सनादिप्रत्ययः (sanādipratyayaḥ) at a time, without an उपसर्गः (upasargaḥ), to every धातुः (dhātuḥ) entry in the pinned engine's Dhātupāṭha. It records generated candidates. It does not add them to the Sanskrit word count.", "",
        "## Inputs", "",
        f"The engine tested **{report['source_entries_tested']} source entries**. The reconciled ledger contains **{report['current_base_word_meanings']} provisional base word-meanings** across **{report['lexical_assignment_rows']} lexical assignment rows**. Three source entries have no admitted lexical meaning: `01.0900` and `01.0951` retain unenumerated meaning lists, while `01.0930` is classified as grammatical metadata.", "",
        "## धातुः (Dhātuḥ) Results", "",
        "| Operation | Engine entries with output | Zero output | Base meanings represented | Candidate derived word-meanings | Distinct spellings | Admitted |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in report["verbal_operations"]:
        lines.append(f"| {row['display_label']} (`{row['sanadi']}`) | {row['source_entries_with_output']} | {row['source_entries_with_zero_output']} | {row['base_word_meanings_with_output']} | {row['candidate_derived_word_meanings']} | {row['distinct_output_spellings_diagnostic']} | 0 |")
    lines.extend([
        "", "A candidate derived word-meaning combines one operation with one reconciled base meaning. Two meanings carried by the same spelling remain separate. Alternative surface forms produced for the same derivation remain attached to that candidate and do not multiply it. The spelling column is only a diagnostic.", "",
        "The णिजन्त (*ṇijanta*), causative, and सन्नन्त (*sannanta*), desiderative, operations produced at least one output for every engine entry. The यङन्त (*yaṅanta*) and यङ्लुगन्त (*yaṅluganta*) operations produced output for 1,775 entries and no output for 454. The primary rule restricts यङन्त (*yaṅanta*) to a one-vowel, consonant-initial धातुः (*dhātuḥ*) and to repeated or intense action; the present report does not assume that every generated रूपम् (*rūpam*), form, satisfies the intended meaning in actual use.", "",
        "One checked example proves why generation and eligibility must remain separate. The Kāśikā commentary under 3.1.22 says that the general यङन्त (*yaṅanta*) formation is not used for *śobhate* and *rocate* because of *anabhidhāna*. Vidyut nevertheless returns `SoSuBya` / `SoSuB` and `rorucya` / `roruc` for the corresponding entries. The engine has completed a formal derivation; the semantic witness has not admitted the resulting word-meaning.", "",
        "## Deferred प्रातिपदिकम् (Prātipadikam) Inputs", "",
        "The engine also exposes `kAmyac`, `kyaN`, and `kyac`, which create a नामधातुः (*nāmadhātuḥ*) from a प्रातिपदिकम् (*prātipadikam*). They are not applied here because the project has not yet fixed the प्रातिपदिकम् (*prātipadikam*) input inventory. Adding a few familiar examples would not establish a count.", "",
        "## Next Eligibility Decision", "",
        "Review the four धातुः (*dhātuḥ*) relations in this order: णिजन्त (*ṇijanta*), सन्नन्त (*sannanta*), यङन्त (*yaṅanta*), and यङ्लुगन्त (*yaṅluganta*). For each one, determine whether the grammatical condition licenses a productive word-meaning for every represented base meaning or whether lexical exclusions require a narrower set. Only approved rows can move from `candidate` to `admitted`.", "",
        "Row-level records are in `sanadi_engine_results.csv` and `sanadi_candidate_meanings.csv`. The JSON report stores the scope, sources, checksums, and exact summary counts.", "",
    ])
    (RESULTS / "sanadi_eligibility.md").write_text("\n".join(lines))


def main() -> None:
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("This pass requires Vidyut 0.4.0")
    manifest = verify_sources()
    lexical, assignments_by_code = load_assignments()
    entries = Data(str(ARCHIVE)).load_dhatu_entries()
    grammar = Vyakarana(log_steps=False, is_chandasi=False, use_svaras=False, nlp_mode=False)
    engine_rows = run_engine(entries, grammar)
    candidates = candidate_rows(engine_rows, assignments_by_code)
    report = build_report(engine_rows, candidates, lexical, entries, manifest)
    RESULTS.mkdir(exist_ok=True)
    write_csv(RESULTS / "sanadi_engine_results.csv", engine_rows)
    write_csv(RESULTS / "sanadi_candidate_meanings.csv", candidates)
    (RESULTS / "sanadi_eligibility.json").write_text(json.dumps(report, indent=2) + "\n")
    write_markdown(report)
    print(f"Tested {len(engine_rows)} source-entry operations; wrote {len(candidates)} candidate rows; admitted 0.")


if __name__ == "__main__":
    main()

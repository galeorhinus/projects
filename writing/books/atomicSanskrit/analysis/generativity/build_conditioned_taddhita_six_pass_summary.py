#!/usr/bin/env python3
"""Reconcile and present the six conditioned taddhita passes."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from vidyut.lipi import Scheme, transliterate

from taddhita_conditioned_common import HERE, RESULTS, sha256


INPUTS = (
    RESULTS / "conditioned_taddhita_source_examples.json",
    RESULTS / "conditioned_taddhita_semantic_classification.json",
    RESULTS / "conditioned_taddhita_inputs.json",
    RESULTS / "conditioned_taddhita_verification.json",
    RESULTS / "conditioned_taddhita_reconciliation.json",
)
LEDGER = RESULTS / "conditioned_taddhita_ledger.csv"


def deva(text: str) -> str:
    return transliterate(text, Scheme.Slp1, Scheme.Devanagari)


def iast(text: str) -> str:
    return transliterate(text, Scheme.Slp1, Scheme.Iast)


def main() -> None:
    extraction, semantics, inputs, verification, reconciliation = [json.loads(path.read_text()) for path in INPUTS]
    if extraction["positive_source_examples"] != semantics["conditioned_candidates"]:
        raise ValueError("Extraction and semantic candidate counts disagree")
    if inputs["unique_conditioned_relations"] != verification["candidate_relations"]:
        raise ValueError("Input and verification counts disagree")
    if verification["verified_relations"] != (
        reconciliation["additional_conditioned_taddhita_word_meanings"]
        + reconciliation["existing_broad_relation_overlaps_not_added"]
    ):
        raise ValueError("Verified relations do not reconcile")

    with LEDGER.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    selected = {}
    wanted = {
        ("aditi", "TasyaApatyam", "Rya"),
        ("aditi", "SaAsyaDevata", "Rya"),
        ("garga", "Gotra", "yaY"),
        ("go", "TasyaVikara", "mayaw"),
        ("paYcAla", "Janapada", "aY"),
        ("Sukla", "AbhutaTadbhava", "cvi"),
    }
    for row in rows:
        key = (row["input_form_slp1"], row["semantic_context"], row["taddhita_source_variant"])
        if key in wanted:
            selected[key] = row
    if set(selected) != wanted:
        raise ValueError(f"Missing reporting examples: {wanted - set(selected)}")

    report = {
        "date": "2026-09-13",
        "passes_completed": 6,
        "positive_source_assertions": extraction["positive_source_examples"],
        "semantic_contexts": semantics["distinct_candidate_contexts"],
        "unique_conditioned_relations": inputs["unique_conditioned_relations"],
        "verified_relations": verification["verified_relations"],
        "engine_mismatches_not_admitted": verification["engine_mismatches_not_admitted"],
        "broad_ledger_overlaps_not_added": reconciliation["existing_broad_relation_overlaps_not_added"],
        "additional_conditioned_taddhita_word_meanings": reconciliation["additional_conditioned_taddhita_word_meanings"],
        "combined_bounded_word_meaning_subtotal": reconciliation["combined_bounded_word_meaning_subtotal"],
        "inputs": {str(path.relative_to(HERE.parents[1])): sha256(path) for path in (*INPUTS, LEDGER, Path(__file__))},
        "publication_status": "research_subtotal_only_not_deployed",
    }
    (RESULTS / "conditioned_taddhita_six_pass_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    examples = [
        ("aditi", "TasyaApatyam", "Rya", "a descendant of Aditi"),
        ("aditi", "SaAsyaDevata", "Rya", "having Aditi as its devatā"),
        ("garga", "Gotra", "yaY", "belonging to the Garga lineage"),
        ("go", "TasyaVikara", "mayaw", "a transformation of cow-material; cow-dung"),
        ("paYcAla", "Janapada", "aY", "the Pañcāla country or people"),
        ("Sukla", "AbhutaTadbhava", "cvi", "becoming white when it was not white before"),
    ]
    lines = [
        "# Six-Pass Conditioned तद्धित Expansion", "",
        "This block extends the broad nominal pass with relations that cannot be treated as universal multipliers. Each counted row begins with a meaning-conditioned Kāśikā test and must reproduce its expected form through the pinned engine.", "",
        "| Pass | Result |", "|---:|---|",
        f"| 1 | Extract {extraction['positive_source_examples']:,} positive and {extraction['negative_source_examples']:,} negative literal meaning-conditioned assertions from eight pinned test files. |",
        f"| 2 | Retain {semantics['conditioned_candidates']:,} candidates across {semantics['distinct_candidate_contexts']} source-named semantic contexts; negative assertions remain exclusions. |",
        f"| 3 | Collapse exact repetition into {inputs['unique_conditioned_relations']:,} unique base-context-suffix relations. |",
        f"| 4 | Vidyut 0.4.0 reproduces {verification['verified_relations']:,}; {verification['engine_mismatches_not_admitted']:,} Python-binding mismatches remain uncounted. |",
        f"| 5 | Remove {reconciliation['existing_broad_relation_overlaps_not_added']:,} overlaps with the broad तद्धित ledger, leaving {reconciliation['additional_conditioned_taddhita_word_meanings']:,} additions. |",
        f"| 6 | The combined bounded subtotal becomes **{reconciliation['combined_bounded_word_meaning_subtotal']:,} word-meanings**. |", "",
        "## Examples", "",
        "| Input | Output | Conditioned word-meaning |", "|---|---|---|",
    ]
    for base, context, suffix, meaning in examples:
        row = selected[(base, context, suffix)]
        outputs = row["expected_output_forms_slp1"].split(";")
        output_display = ", ".join(f"{deva(form)} (*{iast(form)}*)" for form in outputs)
        lines.append(f"| {deva(base)} (*{iast(base)}*) | {output_display} | {meaning} |")
    lines.extend([
        "", "आदित्य (*āditya*) appears twice because the same written form carries two explicitly tested relations: descent from Aditi and having Aditi as its देवता (*devatā*). The counting unit is the word-meaning, not the spelling.", "",
        "## Boundary", "",
        "This is a source-example expansion, not a full multiplication of conditioned suffixes across the 794,078 nominal inputs. It does not count source nouns independently, helper-generated test cases, self-meaning suffixes without an explicit semantic relation, compounds, feminine formations, nominally derived verbs, or inflection.", "",
    ])
    (RESULTS / "conditioned_taddhita_six_pass_summary.md").write_text("\n".join(lines))
    print(f"Six conditioned taddhita passes complete; combined bounded subtotal {report['combined_bounded_word_meaning_subtotal']}.")


if __name__ == "__main__":
    main()

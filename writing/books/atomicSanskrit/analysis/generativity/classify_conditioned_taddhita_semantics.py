#!/usr/bin/env python3
"""Attach source-defined semantic descriptions to conditioned examples."""

from __future__ import annotations

from collections import Counter
import csv
import json
from pathlib import Path

from taddhita_conditioned_common import ARGS, HERE, RESULTS, context_descriptions, sha256


SOURCE = RESULTS / "conditioned_taddhita_source_examples.csv"


def main() -> None:
    descriptions = context_descriptions()
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))

    rows = []
    for row in source_rows:
        context = row["semantic_context"]
        description = descriptions.get(context, "")
        if row["source_assertion_status"] == "negative":
            disposition = "source_negative_not_admitted"
        elif context not in descriptions:
            disposition = "unresolved_context_token_not_admitted"
        else:
            disposition = "source_conditioned_candidate"
        rows.append({
            **row,
            "semantic_description": description,
            "semantic_description_status": "documented_english_gloss" if description else "source_context_identifier_only",
            "semantic_disposition": disposition,
        })

    output = RESULTS / "conditioned_taddhita_semantic_classification.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    by_disposition = Counter(row["semantic_disposition"] for row in rows)
    candidates = [row for row in rows if row["semantic_disposition"] == "source_conditioned_candidate"]
    report = {
        "date": "2026-09-13",
        "source_rows": len(rows),
        "conditioned_candidates": len(candidates),
        "candidate_rows_with_documented_english_gloss": sum(bool(row["semantic_description"]) for row in candidates),
        "candidate_rows_with_source_context_identifier_only": sum(not bool(row["semantic_description"]) for row in candidates),
        "distinct_candidate_contexts": len({row["semantic_context"] for row in candidates}),
        "by_disposition": dict(by_disposition),
        "inputs": {str(path.relative_to(HERE.parents[1])): sha256(path) for path in (SOURCE, ARGS, Path(__file__))},
        "publication_status": "research_classification_only_not_deployed",
    }
    (RESULTS / "conditioned_taddhita_semantic_classification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Conditioned तद्धित Semantic Classification", "",
        f"The pass admits **{report['conditioned_candidates']:,} source-conditioned candidates** for form verification. Their source assertions name {report['distinct_candidate_contexts']} distinct semantic contexts.", "",
        f"The pinned engine source supplies an English description for {report['candidate_rows_with_documented_english_gloss']:,} candidate rows. Another {report['candidate_rows_with_source_context_identifier_only']:,} retain the exact Sanskrit-semantic enum identifier but no supplied English prose; the missing gloss does not erase the explicit semantic condition in the source test.", "",
        "A source-negative assertion remains an exclusion. An unknown context token would remain unresolved rather than being inferred from its expected spelling.", "",
    ]
    (RESULTS / "conditioned_taddhita_semantic_classification.md").write_text("\n".join(lines))
    print(f"Classified {len(rows)} rows; {len(candidates)} conditioned candidates proceed.")


if __name__ == "__main__":
    main()

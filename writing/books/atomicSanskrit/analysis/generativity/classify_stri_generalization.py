#!/usr/bin/env python3
"""Pass 1: classify the semantic boundary for broader feminine derivation."""

from __future__ import annotations

import json
from pathlib import Path

from stri_generalization_common import CONFIG, RESULTS, project_path, sha256


def main() -> None:
    config = json.loads(CONFIG.read_text())
    selected = config["selected_operations"]
    if len(selected) != 4 or len({row["source_operation_id"] for row in selected}) != 4:
        raise ValueError("Expected four distinct lexical-agent operations")
    report = {
        "date": config["date"],
        "selected_source_operations": [row["source_operation_id"] for row in selected],
        "selected_semantic_operations": len(selected),
        "deferred_classes": config["deferred_classes"],
        "classification_policy": "Count a feminine formation only when the source nominal already denotes an agent and the feminine operation adds the distinct meaning 'female agent.' Do not count ordinary adjectival or participial agreement as another lexical meaning.",
        "source_interpretation": "Aṣṭādhyāyī 4.1.3 places the following rules under स्त्रियाम्; its Kāśikā explains स्त्रीत्व as suffix meaning or as qualifying the base meaning. Rules 4.1.4 and 4.1.5 supply the regular paths used by the selected agent nouns.",
        "inputs": {project_path(path): sha256(path) for path in (CONFIG, Path(__file__))},
        "publication_status": "research_classification_only_not_deployed",
    }
    (RESULTS / "stri_generalization_classification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    (RESULTS / "stri_generalization_classification.md").write_text("\n".join([
        "# Broader स्त्रीप्रत्ययः Classification", "",
        "This pass selects four source operations that already denote agents. Their feminine counterparts add a lexical relation: a female agent who performs the same action.", "",
        "Present participles, completed-action adjectives, obligation forms, and descriptive nominals remain outside the count. A feminine form required by agreement is a grammatical form, not another dictionary-level meaning in this analysis.", "",
    ]))
    print("Selected 4 lexical-agent operations; deferred agreement and non-agent classes.")


if __name__ == "__main__":
    main()

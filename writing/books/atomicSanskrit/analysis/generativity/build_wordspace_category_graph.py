#!/usr/bin/env python3
"""Build a reader-facing category graph from the completed count reports."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"


def load(name: str) -> dict:
    return json.loads((RESULTS / name).read_text())


def main() -> None:
    final = load("tinanta_twelve_pass_summary.json")
    name_forms = load("subanta_twelve_pass_summary.json")
    vaidika = load("vaidika_laukika_reconciliation.json")
    verbal = load("tinanta_verbal_inventory.json")
    classes = load("subanta_word_class_reconciliation.json")

    total = final["materialized_lexical_word_meaning_subtotal"]
    vaidika_total = vaidika["bounded_vaidika_subtotal"]
    ordinary_total = total - vaidika_total
    action_meanings = verbal["laukika_verbal_word_meanings"]
    name_meanings = classes["laukika_name_meanings"]
    unchanging_meanings = classes["laukika_unchanging_meanings"]

    citation_capacity = final["third_person_singular_citation_cells"]
    full_action_capacity = final["full_kartari_person_number_cells"]
    name_citation_capacity = name_forms["citation_semantic_cells"]
    full_name_capacity = name_forms["full_relation_number_semantic_cells"]

    if total != vaidika_total + ordinary_total:
        raise ValueError("Domain partition does not reconcile")
    if ordinary_total != action_meanings + name_meanings + unchanging_meanings:
        raise ValueError("Ordinary-domain category partition does not reconcile")

    nodes = [
        {
            "id": "all_word_meanings",
            "label": "समस्ताः शब्दार्थाः",
            "english": "all currently counted word-meanings",
            "count": total,
            "count_role": "lexical_subtotal",
        },
        {
            "id": "vedic_word_meanings",
            "label": "वैदिकाः शब्दार्थाः",
            "english": "Vedic-domain word-meanings",
            "count": vaidika_total,
            "count_role": "lexical_partition",
        },
        {
            "id": "ordinary_word_meanings",
            "label": "लौकिकाः शब्दार्थाः",
            "english": "ordinary-domain word-meanings",
            "count": ordinary_total,
            "count_role": "lexical_partition",
        },
        {
            "id": "action_meanings",
            "label": "क्रियार्थाः",
            "english": "action and process meanings",
            "count": action_meanings,
            "count_role": "lexical_partition",
        },
        {
            "id": "name_meanings",
            "label": "नामार्थाः",
            "english": "name, thing, quality, state, and relation meanings",
            "count": name_meanings,
            "count_role": "lexical_partition",
        },
        {
            "id": "unchanging_meanings",
            "label": "अव्ययानि",
            "english": "complete word-meanings whose forms do not change",
            "count": unchanging_meanings,
            "count_role": "lexical_partition",
        },
        {
            "id": "ten_time_mood_forms",
            "label": "दश कालभावेषु सः-सा-तत् रूपाणि",
            "english": "he, she, or it forms across ten time-and-mood settings",
            "count": citation_capacity,
            "count_role": "non_additive_grammatical_capacity",
        },
        {
            "id": "all_action_forms",
            "label": "सर्वाणि कर्तृ-संख्यारूपाणि",
            "english": "all speaker-role and number forms",
            "count": full_action_capacity,
            "count_role": "non_additive_grammatical_capacity",
        },
        {
            "id": "name_citation_forms",
            "label": "एकं नामरूपम्",
            "english": "one citation form per name meaning",
            "count": name_citation_capacity,
            "count_role": "non_additive_grammatical_capacity",
        },
        {
            "id": "all_name_forms",
            "label": "सम्बन्ध-संख्यारूपाणि",
            "english": "all relation and number forms",
            "count": full_name_capacity,
            "count_role": "non_additive_grammatical_capacity",
        },
    ]
    edges = [
        {"from": "all_word_meanings", "to": "vedic_word_meanings", "role": "partition"},
        {"from": "all_word_meanings", "to": "ordinary_word_meanings", "role": "partition"},
        {"from": "ordinary_word_meanings", "to": "action_meanings", "role": "partition"},
        {"from": "ordinary_word_meanings", "to": "name_meanings", "role": "partition"},
        {"from": "ordinary_word_meanings", "to": "unchanging_meanings", "role": "partition"},
        {"from": "action_meanings", "to": "ten_time_mood_forms", "role": "non_additive_expansion"},
        {"from": "ten_time_mood_forms", "to": "all_action_forms", "role": "non_additive_expansion"},
        {"from": "name_meanings", "to": "name_citation_forms", "role": "non_additive_expansion"},
        {"from": "name_citation_forms", "to": "all_name_forms", "role": "non_additive_expansion"},
    ]
    report = {
        "date": "2026-09-15",
        "terminology_policy": "reader-facing Sanskrit descriptions without Paninian category labels",
        "nodes": nodes,
        "edges": edges,
        "reconciliation": {
            "all_word_meanings": total,
            "vedic_plus_ordinary": vaidika_total + ordinary_total,
            "ordinary_word_meanings": ordinary_total,
            "ordinary_partition": action_meanings + name_meanings + unchanging_meanings,
        },
        "capacity_policy": (
            "The action-form and name-form totals are grammatical capacities and are not added to the "
            "12,846,458 lexical subtotal."
        ),
    }
    (RESULTS / "wordspace_category_graph.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )

    text_graph = f"""समस्ताः शब्दार्थाः — {total:,}
├── वैदिकाः शब्दार्थाः — {vaidika_total:,}
└── लौकिकाः शब्दार्थाः — {ordinary_total:,}
    ├── क्रियार्थाः — {action_meanings:,}
    │   └── दश कालभावेषु सः-सा-तत् रूपाणि — {citation_capacity:,}
    │       └── सर्वाणि कर्तृ-संख्यारूपाणि — {full_action_capacity:,}
    ├── नामार्थाः — {name_meanings:,}
    │   └── एकं नामरूपम् — {name_citation_capacity:,}
    │       └── सम्बन्ध-संख्यारूपाणि — {full_name_capacity:,}
    └── अव्ययानि — {unchanging_meanings:,}
"""
    markdown = f"""# Sanskrit Word-Space by Meaning Class

```text
{text_graph}```

## Plain-English Key

- **समस्ताः शब्दार्थाः**: all word-meanings in the current bounded lexical subtotal.
- **वैदिकाः शब्दार्थाः**: meanings currently assigned to the Vedic domain.
- **लौकिकाः शब्दार्थाः**: meanings currently assigned to the ordinary domain.
- **क्रियार्थाः**: meanings expressing actions, processes, becoming, desire, comparison, and related activity.
- **नामार्थाः**: meanings naming people, things, qualities, states, and relations.
- **अव्ययानि**: complete words whose forms do not change and therefore do not enter a relation-number expansion.

The larger numbers below **क्रियार्थाः** and **नामार्थाः** are expansions, not additions to the lexical subtotal. **45,408,480** counts one familiar singular action-form across ten time-and-mood settings, and **408,676,320** expands those meanings across all speaker roles and number forms. **194,022,888** counts eight relations and three number values for each name meaning.

The reader-facing labels intentionally avoid **प्रातिपदिकम्**, **तिङन्तम्**, **सुबन्तम्**, **लकारः**, **पुरुषः**, and **वचनम्**. The underlying technical reports retain those categories where exact reconstruction requires them.
"""
    (RESULTS / "wordspace_category_graph.md").write_text(markdown)

    mermaid = f"""flowchart TB
    all["समस्ताः शब्दार्थाः<br/>{total:,}<br/><small>all word-meanings</small>"]
    vedic["वैदिकाः शब्दार्थाः<br/>{vaidika_total:,}<br/><small>Vedic domain</small>"]
    ordinary["लौकिकाः शब्दार्थाः<br/>{ordinary_total:,}<br/><small>ordinary domain</small>"]
    action["क्रियार्थाः<br/>{action_meanings:,}<br/><small>actions and processes</small>"]
    names["नामार्थाः<br/>{name_meanings:,}<br/><small>names, things, and qualities</small>"]
    unchanging["अव्ययानि<br/>{unchanging_meanings:,}<br/><small>complete words whose forms do not change</small>"]
    citation["दश कालभावेषु सः-सा-तत् रूपाणि<br/>{citation_capacity:,}"]
    full["सर्वाणि कर्तृ-संख्यारूपाणि<br/>{full_action_capacity:,}"]
    namecitation["एकं नामरूपम्<br/>{name_citation_capacity:,}"]
    nameforms["सम्बन्ध-संख्यारूपाणि<br/>{full_name_capacity:,}"]

    all --> vedic
    all --> ordinary
    ordinary --> action
    ordinary --> names
    ordinary --> unchanging
    action -. grammatical expansion .-> citation
    citation -. grammatical expansion .-> full
    names -. grammatical expansion .-> namecitation
    namecitation -. grammatical expansion .-> nameforms

    classDef total fill:#eadfca,stroke:#5b4a35,stroke-width:2px,color:#221f1a;
    classDef lexical fill:#fff,stroke:#5b4a35,color:#221f1a;
    classDef capacity fill:#f7f5f0,stroke:#5b4a35,stroke-dasharray:5 4,color:#221f1a;
    classDef pending fill:#fff,stroke:#9f6b20,stroke-dasharray:3 3,color:#221f1a;
    class all total;
    class vedic,ordinary,action,names,unchanging lexical;
    class citation,full,namecitation,nameforms capacity;
"""
    (RESULTS / "wordspace_category_graph.mmd").write_text(mermaid)
    print(f"Built reconciled category graph for {total:,} word-meanings.")


if __name__ == "__main__":
    main()

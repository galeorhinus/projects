#!/usr/bin/env python3
"""Synthesis pass 3: build the reader-facing generativity cascade."""

from __future__ import annotations

from capacity_synthesis_common import DATE, RESULTS, project_path, read_json, sha256, write_json


INPUTS = (
    RESULTS / "generation_stage_graph.json",
    RESULTS / "integrated_grammatical_capacity.json",
    RESULTS / "vaidika_capacity_boundary.json",
)


STAGES = (
    {
        "id": "atoms", "count": 2_634,
        "label": "Recorded semantic atoms and their meanings",
        "operation": "starting inventory",
        "examples": ["⟪गम्⟫ (gam), to go", "⟪दृश्⟫ (dṛś), to see"],
    },
    {
        "id": "first_verbal_expansion", "count": 318_285,
        "label": "Verbal meanings after prefixes and transformations",
        "operation": "redirect an action; express causation, desire, repetition, or intensity",
        "examples": ["आ + ⟪गम्⟫ redirects going toward coming", "the causative makes an agent cause the action"],
    },
    {
        "id": "two_prefixes", "count": 1_369_625,
        "label": "Verbal meanings after two ordered prefixes",
        "operation": "apply a second ordered redirection",
        "examples": ["सम् + आ + ⟪गम्⟫ produces समागम्, the base behind समागम (samāgama), coming together"],
    },
    {
        "id": "first_derivatives", "count": 2_174_721,
        "label": "Actions, agents, instruments, qualities, and obligations",
        "operation": "turn verbal meanings into further kinds of meaning",
        "examples": ["दर्शन (darśana), seeing", "कर्तव्य (kartavya), what ought to be done"],
    },
    {
        "id": "noun_relations", "count": 4_762_664,
        "label": "Quality, state, possession, descent, origin, use, and measure",
        "operation": "make a generated noun the input to another relation",
        "examples": ["कर्तृत्व (kartṛtva), agency", "कौन्तेय (Kaunteya), a son or descendant of Kuntī"],
    },
    {
        "id": "nouns_back_to_verbs", "count": 7_939_066,
        "label": "Nouns returned to the verbal engine",
        "operation": "turn a nominal meaning into a new action",
        "examples": ["नमस्यति (namasyati), offers honor or worship", "श्येनायते (śyenāyate), acts like a falcon"],
    },
    {
        "id": "negative_counterparts", "count": 11_116_406,
        "label": "Negative counterparts",
        "operation": "express absence, non-occurrence, or negation once per eligible meaning",
        "examples": ["ज्ञान (jñāna) → अज्ञान (ajñāna)", "कर्तृत्व (kartṛtva) → अकर्तृत्व (akartṛtva)"],
    },
    {
        "id": "bounded_lexical_subtotal", "count": 12_846_458,
        "label": "Bounded word-meaning subtotal before inflection",
        "operation": "add comparison, female-agent meanings, bounded compounds, and one post-compound step",
        "examples": ["महापुरुष (mahāpuruṣa) → महापुरुषत्व (mahāpuruṣatva)"],
    },
    {
        "id": "laukika_grammatical_capacity", "count": 602_707_133,
        "label": "Complete declared लौकिक grammatical capacity",
        "operation": "carry action meanings through 10 × 3 × 3 and name meanings through 8 × 3; retain unchanging words once",
        "examples": ["भवति, भवतः, भवन्ति", "कौन्तेयः, कौन्तेयौ, कौन्तेयाः"],
    },
)


def main() -> None:
    graph, integrated, boundary = [read_json(path) for path in INPUTS]
    cumulative = {node["id"]: node.get("cumulative_count") for node in graph["nodes"]}
    expected = {
        "dhatu_meanings": 2_634,
        "curadi_causative": 318_285,
        "two_upasarga": 1_369_625,
        "wider_krdanta": 2_174_721,
        "conditioned_taddhita": 4_762_664,
        "namadhatu": 7_939_066,
        "nan_privative": 11_116_406,
        "compound_input_stacks": 12_846_458,
    }
    for node_id, count in expected.items():
        if cumulative.get(node_id) != count:
            raise ValueError(f"Stage {node_id} no longer equals {count:,}")
    if STAGES[-1]["count"] != integrated["integrated_laukika_grammatical_cells"]:
        raise ValueError("The publication endpoint does not match the integrated capacity")

    report = {
        "date": DATE,
        "pass": 3,
        "stages": list(STAGES),
        "vedic_branch": {
            "count": boundary["vaidika_lexical_word_meanings"],
            "unit": "lexical_word_meaning",
            "enters_final_laukika_capacity": False,
        },
        "recursive_compound_capacity_enters_headline": False,
        "inputs": {project_path(path): sha256(path) for path in INPUTS},
    }
    write_json(RESULTS / "publication_capacity_cascade.json", report)

    lines = ["# Synthesis Pass 3: Publication Capacity Cascade", ""]
    for index, stage in enumerate(STAGES, 1):
        lines.extend([
            f"## {index}. {stage['count']:,} — {stage['label']}", "",
            f"**Operation:** {stage['operation']}.", "",
            "**Examples:** " + "; ".join(stage["examples"]) + ".", "",
        ])
    lines.extend([
        "## The Domain Fork", "",
        f"The {STAGES[-2]['count']:,} lexical word-meanings divide into {boundary['laukika_lexical_word_meanings']:,} लौकिक meanings and {boundary['vaidika_lexical_word_meanings']:,} Vedic meanings. Only the लौकिक branch enters the {STAGES[-1]['count']:,}-cell grammatical model. The Vedic branch stays visible but separate.", "",
        "## Reporting Boundary", "",
        "The cascade stops before unrestricted recursive compounding. The separate compound-capacity experiment demonstrates why that operation cannot supply a finite vocabulary ceiling, but its virtual slots do not enter this publication headline.", "",
    ])
    (RESULTS / "publication_capacity_cascade.md").write_text("\n".join(lines))

    mermaid = ["flowchart LR"]
    for stage in STAGES[:-2]:
        mermaid.append(f"    {stage['id']}[\"{stage['label']}<br/>{stage['count']:,}\"]")
    mermaid.extend([
        f"    bounded_lexical_subtotal[\"Bounded word-meanings<br/>{STAGES[-2]['count']:,}\"]",
        f"    vaidika_branch[\"Vedic meanings held separate<br/>{boundary['vaidika_lexical_word_meanings']:,}\"]",
        f"    laukika_branch[\"Laukika meanings<br/>{boundary['laukika_lexical_word_meanings']:,}\"]",
        f"    laukika_grammatical_capacity[\"Declared laukika grammatical cells<br/>{STAGES[-1]['count']:,}\"]",
    ])
    ids = [stage["id"] for stage in STAGES[:-2]] + ["bounded_lexical_subtotal"]
    for left, right in zip(ids, ids[1:]):
        mermaid.append(f"    {left} --> {right}")
    mermaid.extend([
        "    bounded_lexical_subtotal --> vaidika_branch",
        "    bounded_lexical_subtotal --> laukika_branch",
        "    laukika_branch --> laukika_grammatical_capacity",
    ])
    (RESULTS / "publication_capacity_cascade.mmd").write_text("\n".join(mermaid) + "\n")
    print("Built the reader-facing capacity cascade and examples.")


if __name__ == "__main__":
    main()

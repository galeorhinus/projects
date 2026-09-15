#!/usr/bin/env python3
"""Review the semantic branches of yaN and yaN-luk without changing the count."""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "manifest.json"
ENGINE_RESULTS = RESULTS / "sanadi_engine_results.csv"
ASSIGNMENTS = RESULTS / "current_base_assignments.csv"

# Vidyut 0.4.0 selects these source entries through rule 3.1.24. The list is
# retained explicitly so an upstream implementation change cannot silently alter
# the semantic classification.
RULE_3124_CODES = {
    "01.0150", "01.0453", "01.0463", "01.0640", "01.0990", "01.1146",
    "04.0150", "06.0146", "06.0163", "06.0167", "09.0033", "10.0368",
}

# These entries take the special shape path identified by Vidyut as varttika
# 3.1.22.1. This affects form, not the semantic branch assigned here.
VARTTIKA_3122_1_CODES = {
    "01.0332", "01.1086", "02.0034", "03.0017", "05.0020", "09.0059",
    "10.0412", "10.0450", "10.0451",
}

# This deliberately broad screen creates a review queue only. It does not decide
# that a meaning falls under 3.1.23. Each match must be checked in Sanskrit.
MOVEMENT_PATTERNS = (
    ("gati", re.compile(r"gat(?:i|O|y|v|A)|gaman")),
    ("movement", re.compile(r"calan|caraR|saYcAr|vical|pracal")),
    ("going", re.compile(r"yAn|vrajan|awana|paryaWan")),
    ("stepping", re.compile(r"kramaR|atikrama|laN[Gg]|laG")),
    ("flowing", re.compile(r"saraR|prasaraR|syand|drav")),
    ("flying/falling", re.compile(r"plavan|patana|utpat")),
    ("reaching", re.compile(r"prApaR|Apane|avApt|prApt")),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_manifest() -> tuple[dict, dict[str, dict]]:
    manifest = json.loads(MANIFEST.read_text())
    records = {row["filename"]: row for row in manifest["sources"]}
    for record in records.values():
        path = ARCHIVE / record["filename"]
        if sha256(path) != record["sha256"]:
            raise ValueError(f"Archived source changed: {path}")
    return manifest, records


def classify_engine_paths(engine_rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], Counter]:
    rows = []
    counts: Counter = Counter()
    for row in engine_rows:
        if row["operation_id"] != "intensive":
            continue
        code = row["source_code"]
        if row["engine_status"] != "generated":
            path = "zero_output"
        elif code in RULE_3124_CODES:
            path = "3.1.24"
        elif code in VARTTIKA_3122_1_CODES:
            path = "varttika_3.1.22.1"
        else:
            path = "3.1.22"
        counts[path] += 1
        rows.append({**row, "engine_rule_path": path})
    return rows, counts


def movement_candidates(
    engine_rows: list[dict[str, str]], assignments: list[dict[str, str]]
) -> list[dict[str, str]]:
    generated = {
        row["source_code"]: row
        for row in engine_rows
        if row["engine_status"] == "generated"
        and row["engine_rule_path"] in {"3.1.22", "varttika_3.1.22.1"}
    }
    candidates = []
    seen = set()
    for base in assignments:
        if base["record_kind"] != "lexical" or base["source_code"] not in generated:
            continue
        meaning = base["normalized_meaning_slp1"]
        for label, pattern in MOVEMENT_PATTERNS:
            match = pattern.search(meaning)
            if not match:
                continue
            key = (base["source_code"], base["normalized_count_key"], label, match.group(0))
            if key in seen:
                continue
            seen.add(key)
            engine = generated[base["source_code"]]
            candidates.append({
                "source_code": base["source_code"],
                "normalized_citation_slp1": base["normalized_citation_slp1"],
                "base_count_key": base["normalized_count_key"],
                "base_meaning_slp1": meaning,
                "base_meaning_display": base["meaning_display"],
                "matched_screen": label,
                "matched_token": match.group(0),
                "engine_rule_path": engine["engine_rule_path"],
                "output_forms_slp1": engine["output_forms_slp1"],
                "semantic_status": "review_required_not_counted",
            })
    return sorted(candidates, key=lambda row: (row["source_code"], row["base_count_key"], row["matched_screen"]))


def build_report(
    manifest: dict,
    records: dict[str, dict],
    engine_rows: list[dict[str, str]],
    path_counts: Counter,
    assignments: list[dict[str, str]],
    movement_rows: list[dict[str, str]],
) -> dict:
    generated_codes = {row["source_code"] for row in engine_rows if row["engine_status"] == "generated"}
    lexical = [row for row in assignments if row["record_kind"] == "lexical"]
    base_meanings_by_path: dict[str, set[str]] = {
        "3.1.22": set(),
        "3.1.24": set(),
        "varttika_3.1.22.1": set(),
        "zero_output": set(),
    }
    for row in lexical:
        code = row["source_code"]
        if code not in generated_codes:
            path = "zero_output"
        elif code in RULE_3124_CODES:
            path = "3.1.24"
        elif code in VARTTIKA_3122_1_CODES:
            path = "varttika_3.1.22.1"
        else:
            path = "3.1.22"
        base_meanings_by_path[path].add(row["normalized_count_key"])

    source_files = [
        "rule-2.4.74.html", "rule-3.1.22.html", "rule-3.1.23.html",
        "rule-3.1.24.html", "sutrapatha.tsv", "vidyut-sanadi.rs",
    ]
    return {
        "date": "2026-09-13",
        "status": "semantic_proposals_only_not_applied",
        "vocabulary_total": None,
        "published_total_changed": False,
        "terms": {
            "yaN": "यङन्त (yaṅanta), repeated or intensive formation",
            "yaNluk": "यङ्लुगन्त (yaṅluganta), yaṅ formation with लुक् (luk)",
        },
        "primary_rule_findings": [
            {
                "rule": "3.1.22",
                "finding": "The Kashika explains kriyasamabhihara as paunahpunya, repetition, or bhrshartha, intensity. These are two semantic relations, not two spellings.",
            },
            {
                "rule": "3.1.23",
                "finding": "For a movement-denoting dhatu meaning, yan is obligatory when crooked movement is meant and is not licensed there merely for general repetition or intensity.",
            },
            {
                "rule": "3.1.24",
                "finding": "For the listed dhatus, yan expresses disparagement of the action itself. Disparagement of the agent or instrument is insufficient.",
            },
            {
                "rule": "2.4.74",
                "finding": "Luk deletes the audible yan suffix before the stated environment while pratyayalakshana retains consequences of the formation; the resulting dhatu is assigned to adadi in the pinned implementation.",
            },
        ],
        "engine_coverage": {
            "source_entries": dict(sorted(path_counts.items())),
            "reconciled_base_meanings": {
                key: len(value) for key, value in sorted(base_meanings_by_path.items())
            },
            "rule_3.1.23_engine_path_entries": 0,
            "rule_3.1.23_gap": "Vidyut 0.4.0 does not implement a separate semantic selection path for 3.1.23 in the pinned sanadi module. Movement meanings therefore require a source-led review.",
            "movement_screen_rows": len(movement_rows),
            "movement_screen_unique_base_meanings": len({row["base_count_key"] for row in movement_rows}),
            "movement_screen_status": "review_required_not_counted",
        },
        "known_anabhidhana_control": {
            "rule": "3.1.22",
            "source_entries": ["01.0847 ruc", "06.0046 shubh"],
            "finding": "The Kashika excludes the general yan use for shobhate and rocate through anabhidhana even though the engine generates forms.",
            "count_status": "not_admitted",
        },
        "proposals": [
            {
                "id": "YAN-P1",
                "status": "pending_author_approval",
                "proposal": "Represent repetition and intensity as two different meanings under general 3.1.22 eligibility. Do not assume that both are lexically available for every generated base meaning.",
            },
            {
                "id": "YAN-P2",
                "status": "pending_author_approval",
                "proposal": "For movement-denoting base meanings governed by 3.1.23, use one crooked-movement relation instead of the two general 3.1.22 relations.",
            },
            {
                "id": "YAN-P3",
                "status": "pending_author_approval",
                "proposal": "For base meanings governed by 3.1.24, use one disparaged-action relation instead of the two general 3.1.22 relations.",
            },
            {
                "id": "YAN-P4",
                "status": "pending_author_approval",
                "proposal": "Apply attested anabhidhana exclusions before admission. Exclude the known shubh and ruc controls from the general yan candidate set unless contrary lexical evidence is found.",
            },
            {
                "id": "YAN-P5",
                "status": "pending_author_approval",
                "proposal": "Treat a licensed yaN-luk formation as a separate derived verbal word because its formation and paradigm differ, but let it inherit the corresponding yaN semantic branch. Luk does not create another meaning multiplier.",
            },
        ],
        "limits": [
            "The movement screen is a retrieval aid based on source gloss strings. It is not a grammatical classification.",
            "The nine varttika 3.1.22.1 entries identify a special formal path, not a separate meaning.",
            "Engine generation does not establish lexical use or semantic eligibility.",
            "No proposed semantic branch is admitted by this pass.",
        ],
        "sources": [records[name] for name in source_files],
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (ENGINE_RESULTS, ASSIGNMENTS, MANIFEST, Path(__file__))
        },
        "manifest_source_count": len(manifest["sources"]),
    }


def write_markdown(report: dict) -> None:
    coverage = report["engine_coverage"]
    lines = [
        "# यङन्त (Yaṅanta) Semantic Review", "",
        "This pass decides what must be reviewed before यङन्त (*yaṅanta*) and यङ्लुगन्त (*yaṅluganta*) can enter the generativity count. It changes no count and no manuscript claim.", "",
        "## What the Rules Distinguish", "",
        "Aṣṭādhyāyī 3.1.22 supplies the general यङन्त (*yaṅanta*) operation. The Kāśikā explains its semantic field through **पौनःपुन्यम् (*paunaḥpunyam*)**, repetition, and **भृशार्थः (*bhṛśārthaḥ*)**, intensity. Under this project's counting rule, those are two different meanings even when one derived form can carry either one.", "",
        "Two following rules narrow that general field. Rule 3.1.23 assigns movement-denoting धातुः (*dhātuḥ*) meanings to crooked movement and excludes the general repetition/intensity reading there. Rule 3.1.24 assigns its listed धातवः (*dhātavaḥ*) to disparagement of the action itself; criticism of the agent or instrument does not satisfy the condition.", "",
        "The same commentary also supplies a lexical control. It rejects the general यङन्त (*yaṅanta*) use of *śobhate* and *rocate* through **अनभिधानम् (*anabhidhānam*)**, although Vidyut produces formal outputs for the corresponding entries. A derivation engine can show that a form is constructible. It cannot by itself show that speakers use the resulting word with the proposed meaning.", "",
        "## What the Engine Covers", "",
        "| Engine path | Source entries | Reconciled base meanings | Treatment |",
        "|---|---:|---:|---|",
        f"| 3.1.22 general path | {coverage['source_entries']['3.1.22']} | {coverage['reconciled_base_meanings']['3.1.22']} | repetition/intensity review |",
        f"| Vārttika 3.1.22.1 shape path | {coverage['source_entries']['varttika_3.1.22.1']} | {coverage['reconciled_base_meanings']['varttika_3.1.22.1']} | same semantic review; special form |",
        f"| 3.1.24 disparaged action | {coverage['source_entries']['3.1.24']} | {coverage['reconciled_base_meanings']['3.1.24']} | exclusive semantic branch |",
        f"| No engine output | {coverage['source_entries']['zero_output']} | {coverage['reconciled_base_meanings']['zero_output']} | unresolved, not admitted |", "",
        "The pinned Vidyut 0.4.0 module has no separate 3.1.23 selection path. Its ordinary formal path therefore includes possible movement meanings without determining whether crooked movement is intended. The broad source-gloss screen places "
        f"**{coverage['movement_screen_unique_base_meanings']} base meanings** in a review queue. Those rows are retrieval candidates, not 3.1.23 decisions and not countable results.", "",
        "## यङ्लुगन्त (Yaṅluganta)", "",
        "Aṣṭādhyāyī 2.4.74 applies **लुक् (*luk*)** to यङ् (*yaṅ*) in the stated environment. The commentary retains consequences of the deleted प्रत्ययः (*pratyayaḥ*) through **प्रत्ययलक्षणम् (*pratyayalakṣaṇam*)**, and the pinned implementation assigns the resulting धातुः (*dhātuḥ*) to अदादिगणः (*adādigaṇaḥ*). The operation therefore creates a distinct derived verbal word and paradigm. It does not independently create a new meaning: the यङ्लुगन्त (*yaṅluganta*) inherits whichever repetition, intensity, crooked-movement, or disparaged-action branch licensed the corresponding यङन्त (*yaṅanta*).", "",
        "## Decisions Proposed", "",
    ]
    for proposal in report["proposals"]:
        lines.append(f"- **{proposal['id']} — pending:** {proposal['proposal']}")
    lines.extend([
        "", "## Count Status", "",
        "No यङन्त (*yaṅanta*) or यङ्लुगन्त (*yaṅluganta*) candidate is admitted. Exact totals require approval of the semantic model, manual classification of the 3.1.23 queue, and a wider lexical-exclusion check. The current published and research totals remain unchanged.", "",
        "The row-level movement queue is `yan_movement_candidates.csv`. The JSON report preserves source URLs, retrieval records, hashes, engine-path counts, and all pending proposals.", "",
    ])
    (RESULTS / "yan_semantic_review.md").write_text("\n".join(lines))


def main() -> None:
    manifest, records = load_manifest()
    engine = read_csv(ENGINE_RESULTS)
    assignments = read_csv(ASSIGNMENTS)
    yan_engine, path_counts = classify_engine_paths(engine)
    movement = movement_candidates(yan_engine, assignments)
    report = build_report(manifest, records, yan_engine, path_counts, assignments, movement)
    RESULTS.mkdir(exist_ok=True)
    write_csv(
        RESULTS / "yan_movement_candidates.csv",
        movement,
        [
            "source_code", "normalized_citation_slp1", "base_count_key",
            "base_meaning_slp1", "base_meaning_display", "matched_screen",
            "matched_token", "engine_rule_path", "output_forms_slp1",
            "semantic_status",
        ],
    )
    (RESULTS / "yan_semantic_review.json").write_text(json.dumps(report, indent=2) + "\n")
    write_markdown(report)
    print(
        f"Reviewed {len(yan_engine)} yan engine rows; queued {len(movement)} movement-screen rows; admitted 0."
    )


if __name__ == "__main__":
    main()

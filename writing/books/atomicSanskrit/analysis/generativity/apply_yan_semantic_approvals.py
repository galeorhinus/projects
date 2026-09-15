#!/usr/bin/env python3
"""Apply approved yaN semantic policy to the movement-review queue."""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
APPROVALS = HERE / "approved_yan_semantics.json"
REVIEW = RESULTS / "yan_semantic_review.json"
QUEUE = RESULTS / "yan_movement_candidates.csv"


DIRECT_MOVEMENT = {
    "ASugamane", "CadmagatO", "aBigamane", "agragamane", "calane", "gatO",
    "gatyAm", "kiYciccalane", "kutsite gamane", "mandAyAM gatO", "nIcErgatO",
    "plavagatO", "plavane", "plutagatO", "prApaRe", "saYcalane", "saYcaraRe",
    "vihAyasA gatO",
}

NOT_MOVEMENT = {
    "ADyAne", "avagamane", "dravIkaraRe", "dravyavinimaye", "gatinivfttO",
    "gatipratiGAte", "gativEkalye", "gaticAturye", "gatitvaraRe", "gatyAkzepe",
    "gatyAramBe", "prAptO", "praKyAne", "saMstyAne", "saNKyAne", "saNgatikaraRe",
}

DEFERRED_SCOPE: set[str] = set()

RATIONALES = {
    "direct_movement": "The source meaning itself denotes going, movement, motion, flight, swimming, or reaching; classify under 3.1.23 pending lexical admission.",
    "not_movement": "The source meaning does not denote movement itself. It names an action at the edge of movement, mentions movement as an object, or contains a coincidental search substring; return it to general 3.1.22 review.",
    "deferred_scope": "The gloss concerns an edge of movement such as beginning, hastening, dexterity, objection, or attainment. Rule 3.1.23 scope needs a direct lexical or grammatical witness before classification.",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def validate_approvals(review: dict, approvals: dict) -> None:
    proposed = {row["id"] for row in review["proposals"]}
    approved = set(approvals["approved_proposal_ids"])
    if proposed != approved:
        raise ValueError(f"Approval set differs from proposal set: proposed={proposed}, approved={approved}")
    if approvals["approval_basis"] != "Author message: approved":
        raise ValueError("Approval basis is missing")


def collapse_queue(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, dict] = {}
    for row in rows:
        key = row["base_count_key"]
        item = grouped.setdefault(key, {**row, "matched_screens": set(), "matched_tokens": set()})
        item["matched_screens"].add(row["matched_screen"])
        item["matched_tokens"].add(row["matched_token"])

    classified = []
    for item in grouped.values():
        meaning = item["base_meaning_slp1"]
        if meaning in DIRECT_MOVEMENT:
            decision = "direct_movement"
            rule_treatment = "3.1.23_crooked_movement_candidate"
            next_status = "lexical_admission_review_pending"
        elif meaning in NOT_MOVEMENT:
            decision = "not_movement"
            rule_treatment = "return_to_3.1.22_repetition_intensity_review"
            next_status = "lexical_admission_review_pending"
        elif meaning in DEFERRED_SCOPE:
            decision = "deferred_scope"
            rule_treatment = "3.1.23_scope_unresolved"
            next_status = "source_review_required_not_counted"
        else:
            raise ValueError(f"Unclassified movement-screen meaning: {meaning}")
        classified.append({
            "source_code": item["source_code"],
            "normalized_citation_slp1": item["normalized_citation_slp1"],
            "base_count_key": item["base_count_key"],
            "base_meaning_slp1": meaning,
            "base_meaning_display": item["base_meaning_display"],
            "matched_screens": ";".join(sorted(item["matched_screens"])),
            "matched_tokens": ";".join(sorted(item["matched_tokens"])),
            "output_forms_slp1": item["output_forms_slp1"],
            "classification": decision,
            "rule_treatment": rule_treatment,
            "rationale": RATIONALES[decision],
            "count_status": next_status,
        })
    return sorted(classified, key=lambda row: (row["classification"], row["source_code"], row["base_count_key"]))


def build_report(review: dict, approvals: dict, rows: list[dict[str, str]]) -> dict:
    counts = Counter(row["classification"] for row in rows)
    meanings = {
        decision: sorted({row["base_meaning_slp1"] for row in rows if row["classification"] == decision})
        for decision in counts
    }
    return {
        "date": "2026-09-13",
        "status": "five_semantic_decisions_approved_movement_queue_reviewed",
        "approved_proposal_ids": approvals["approved_proposal_ids"],
        "movement_queue": {
            "unique_base_meanings_reviewed": len(rows),
            "classification_counts": dict(sorted(counts.items())),
            "source_meanings_by_classification": dict(sorted(meanings.items())),
            "deferred_rows_remain_uncounted": True,
        },
        "semantic_model": {
            "3.1.22": ["repetition", "intensity"],
            "3.1.23": ["crooked movement"],
            "3.1.24": ["disparagement of the action"],
            "yaNluk": "A separate derived verbal word inheriting its licensed yaN meaning; no additional meaning multiplier.",
            "anabhidhana": "Established lexical exclusions override formal engine generation.",
        },
        "count_status": {
            "vocabulary_total": None,
            "derived_word_meanings_admitted": 0,
            "reason": "Rule 3.1.23 classification is complete for all 312 rows, but base-level lexical admission remains a separate step.",
            "published_total_changed": False,
        },
        "next_pass": "Apply the approved admission standard to the four verbal-base sanadi operations.",
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (APPROVALS, REVIEW, QUEUE, Path(__file__))
        },
    }


def write_markdown(report: dict) -> None:
    counts = report["movement_queue"]["classification_counts"]
    deferred = report["movement_queue"]["source_meanings_by_classification"].get("deferred_scope", [])
    lines = [
        "# Approved यङन्त (Yaṅanta) Semantic Model", "",
        "The author approved YAN-P1 through YAN-P5 on 2026-09-13. This record applies those decisions to the 3.1.23 movement-screen queue. It does not admit a derived word-meaning or change the manuscript total.", "",
        "## Approved Model", "",
        "1. General 3.1.22 eligibility distinguishes **पौनःपुन्यम् (*paunaḥpunyam*)**, repetition, from **भृशार्थः (*bhṛśārthaḥ*)**, intensity.",
        "2. A movement meaning governed by 3.1.23 receives the crooked-movement relation instead of those two general meanings.",
        "3. A listed meaning governed by 3.1.24 receives disparagement of the action instead of the two general meanings.",
        "4. **अनभिधानम् (*anabhidhānam*)** can exclude a formally generated result.",
        "5. A licensed यङ्लुगन्त (*yaṅluganta*) is a separate derived verbal word. It inherits the corresponding यङन्त (*yaṅanta*) meaning and creates no additional semantic multiplier.", "",
        "## Movement Review", "",
        "| Classification | Base meanings | Consequence |",
        "|---|---:|---|",
        f"| Direct movement | {counts['direct_movement']} | Candidate for 3.1.23 crooked movement; lexical admission still pending |",
        f"| Not movement | {counts['not_movement']} | Return to the 3.1.22 repetition/intensity review |",
        f"| Scope deferred | {counts.get('deferred_scope', 0)} | Keep outside every count pending a direct witness |", "",
        "The direct group uses meanings that themselves denote going, movement, flight, swimming, or reaching. The other group includes contemplation, comprehension, liquefaction, exchange of goods, obstruction or cessation of movement, enumeration, proclamation, and association. It also includes the seven former edge cases: beginning, hastening, or skill in movement; objection to movement; and attainment. The Kāśikā describes 3.1.23 as applying to a धातुः (*dhātuḥ*) that itself expresses movement. Mentioning movement or naming an action around it does not satisfy that condition.", "",
        "## Count Status", "",
        "This pass reviews all 312 possible movement meanings: 289 enter the 3.1.23 crooked-movement path and 23 return to general 3.1.22 review. No row enters the vocabulary count merely because its rule path has been classified.", "",
        "The complete row-level record is `yan_movement_classification.csv`; the JSON report preserves approvals and input hashes.", "",
    ]
    (RESULTS / "yan_semantic_approval.md").write_text("\n".join(lines))


def main() -> None:
    review = json.loads(REVIEW.read_text())
    approvals = json.loads(APPROVALS.read_text())
    validate_approvals(review, approvals)
    rows = collapse_queue(read_csv(QUEUE))
    report = build_report(review, approvals, rows)
    write_csv(RESULTS / "yan_movement_classification.csv", rows)
    (RESULTS / "yan_semantic_approval.json").write_text(json.dumps(report, indent=2) + "\n")
    write_markdown(report)
    counts = report["movement_queue"]["classification_counts"]
    print(f"Reviewed {len(rows)} movement candidates: {dict(sorted(counts.items()))}; admitted 0.")


if __name__ == "__main__":
    main()

"""Apply approved research decisions as an overlay, preserving every source row."""

import copy
import csv
import json

from review_reconciliation import build_report
from run_pilot import HERE, RESULTS, sha

APPROVAL = HERE / "approved_reconciliation.json"


def count(rows):
    return len({r["normalized_count_key"] for r in rows if r["record_kind"] == "lexical"})


def normalize(approval=None):
    approval = copy.deepcopy(approval if approval is not None else json.loads(APPROVAL.read_text()))
    evidence = build_report()
    cases = {c["id"]: c for c in evidence["cases"]}
    with (RESULTS / "base_meaning_assignments.csv").open() as handle:
        originals = list(csv.DictReader(handle))
    rows = [dict(r, normalized_citation_slp1=r["citation_slp1"],
                 normalized_meaning_slp1=r["meaning_slp1"], normalized_count_key=r["count_key"],
                 record_kind="lexical", reconciliation_id="") for r in originals]
    index = {(r["source_code"], r["meaning_slp1"]): r for r in rows}
    if len(index) != len(rows):
        raise ValueError("Original source/meaning selectors must be unique")
    if count(rows) != approval["baseline"]:
        raise ValueError("Approved baseline no longer matches")
    decisions, seen = [], set()
    for decision in approval["decisions"]:
        rid = decision["review_id"]
        if rid in seen:
            raise ValueError("Duplicate approved decision")
        seen.add(rid)
        case = cases[rid]
        allowed = {(code, m) for code, meanings in case["original_entries"].items() for m in meanings}

        def select(selector):
            key = tuple(selector)
            if key not in allowed:
                raise ValueError(f"{rid}: target is outside the reviewed group")
            return index[key]

        before = count(rows)
        for correction in decision.get("corrections", []):
            row = select(correction["target"])
            for field in ("citation_slp1", "meaning_slp1"):
                if field in correction:
                    row["normalized_" + field] = correction[field]
            row["reconciliation_id"] = rid
        for merger in decision.get("merges", []):
            if merger["canonical"] not in merger["members"]:
                raise ValueError("Canonical assignment must be a merger member")
            canonical = select(merger["canonical"])
            members = [select(m) for m in merger["members"]]
            old_keys = {r["normalized_count_key"] for r in members}
            if len(old_keys) < 2:
                raise ValueError("Merger must consolidate separate counting keys")
            for row in rows:
                if row["normalized_count_key"] in old_keys:
                    if (row["source_code"], row["meaning_slp1"]) not in allowed:
                        raise ValueError("Merger would alter an unreviewed shared assignment")
                    row["normalized_count_key"] = canonical["normalized_count_key"]
                    row["reconciliation_id"] = rid
        for selector in decision.get("grammar_only", []):
            row = select(selector)
            row["record_kind"] = "grammatical_metadata"
            row["reconciliation_id"] = rid
        delta = count(rows) - before
        if delta != decision["delta"] or delta != case["delta"]:
            raise ValueError(f"{rid}: approved count effect does not match")
        decisions.append(dict(decision, before=before, after=count(rows), evidence=case["evidence"],
                              explanation=case["after"]))
    if count(rows) != approval["expected_after"]:
        raise ValueError("Final subtotal differs from approval")
    report = dict(date=approval["date"], status="applied", baseline=approval["baseline"],
                  current_provisional_assignments=count(rows), vocabulary_total=None,
                  preserved_source_rows=len(rows), lexical_rows=sum(r["record_kind"] == "lexical" for r in rows),
                  grammatical_metadata_rows=sum(r["record_kind"] != "lexical" for r in rows), decisions=decisions,
                  inputs=dict(evidence["inputs"], approved_reconciliation=sha(APPROVAL)))
    return rows, report


def main():
    rows, report = normalize()
    with (RESULTS / "normalized_base_assignments.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (RESULTS / "normalized_base_meanings.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Current Research Count", "", f"Approved and applied {report['date']}: **2,653 -> 2,649**.", "",
             "This is a provisional base-meaning subtotal, not a vocabulary total. No prefix, derivational, "
             "or inflectional multiplier has been applied. The manuscript and its older calculation are unchanged.", "",
             "All 2,741 original assignment rows survive in `normalized_base_assignments.csv`, "
             "with their original fields intact. New `normalized_*` fields carry the approved corrections. "
             "One row is classified as grammatical metadata and is excluded from the lexical subtotal; "
             "the other three reductions use shared counting keys. The nine earlier batches remain reproducible.", "",
             "| Decision | Before | After |", "|---|---:|---:|"]
    for d in report["decisions"]:
        lines.append(f"| [{d['review_id']}](reconciliation_review_01.md) | {d['before']:,} | {d['after']:,} |")
    lines.extend(["", "## Next Review", "",
                  "The next ten-case report reviews corrected ay plus IR01, IR04, IR07, IR08, IR10, IR11, IR12, "
                  "IR13, and IR14. Its proposals remain separate from this applied count.", "",
                  "Machine-readable evidence and provenance: `normalized_base_meanings.json`. "
                  "Never feed `grammatical_metadata` rows into a lexical generator or use original fields "
                  "instead of the normalized fields when building on these corrections.", ""])
    (RESULTS / "current_research_count.md").write_text("\n".join(lines))
    print(f"Preserved {len(rows)} source rows; current provisional subtotal {count(rows)}.")


if __name__ == "__main__":
    main()

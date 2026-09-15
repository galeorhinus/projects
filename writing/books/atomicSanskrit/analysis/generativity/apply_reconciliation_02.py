"""Apply the second approval without rewriting the first normalized snapshot."""

import csv
import json

from apply_reconciliation import normalize as first_normalize
from review_followups_02 import build_report
from run_pilot import HERE, RESULTS, sha

APPROVAL = HERE / "approved_reconciliation_02.json"


def normalize():
    approval = json.loads(APPROVAL.read_text())
    rows, first = first_normalize()
    review = build_report()
    cases = {c["id"]: c for c in review["cases"]}
    index = {(r["source_code"], r["normalized_meaning_slp1"]): r for r in rows}

    def total():
        return len({r["normalized_count_key"] for r in rows if r["record_kind"] == "lexical"})

    if total() != approval["baseline"]:
        raise ValueError("Second approved baseline differs")
    applied = []
    for action in approval["merges"] + approval["exclude"]:
        case = cases[action["case"]]
        allowed = {(code, m) for code, meanings in case["entries"].items() for m in meanings}
        selectors = action.get("members", [action.get("target")])
        if any(tuple(s) not in allowed for s in selectors):
            raise ValueError("Action exceeds reviewed scope")
        before = total()
        selected = [index[tuple(s)] for s in selectors]
        if "members" in action:
            old_keys = {r["normalized_count_key"] for r in selected}
            canonical = selected[0]["normalized_count_key"]
            for row in rows:
                if row["normalized_count_key"] in old_keys:
                    if (row["source_code"], row["normalized_meaning_slp1"]) not in allowed:
                        raise ValueError("Merger crosses review boundary")
                    row["normalized_count_key"] = canonical
                    row["reconciliation_id"] = case["id"]
        else:
            selected[0]["record_kind"] = action["classification"]
            selected[0]["reconciliation_id"] = case["id"]
        if total() - before != case["delta"]:
            raise ValueError("Applied change differs from reviewed effect")
        applied.append(dict(action, before=before, after=total(), evidence=case["evidence"]))
    if total() != approval["expected_after"]:
        raise ValueError("Second approved total differs")
    report = dict(date=approval["date"], status="applied", current_provisional_assignments=total(),
                  baseline=approval["baseline"], vocabulary_total=None, preserved_source_rows=len(rows),
                  decisions=applied, inputs=dict(review["inputs"], approval_02=sha(APPROVAL)))
    return rows, report


def main():
    rows, report = normalize()
    with (RESULTS / "current_base_assignments.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (RESULTS / "current_base_meanings.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    with (RESULTS / "reconciliation_02_base_assignments.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (RESULTS / "reconciliation_02_base_meanings.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Current Research Count", "", f"Updated {report['date']}.", "",
             f"Applied provisional base-meaning assignments: **{report['current_provisional_assignments']:,}**.", "",
             "The second approved reconciliation changes 2,649 to 2,645. All 2,741 source-assignment rows are retained; "
             "original fields and the earlier 2,653 and 2,649 snapshots remain unchanged.", "",
             "| Approved decision | Before | After |", "|---|---:|---:|"]
    for c in report["decisions"]:
        lines.append(f"| {c['case']} | {c['before']:,} | {c['after']:,} |")
    lines.extend(["", "[Current dataset](current_base_assignments.csv) · [Applied decisions and source records](current_base_meanings.json)", "",
                  "[Eight-pass follow-up](eight_pass_consolidation.md) contains new proposals, not applied changes. "
                  "This is a base-identity research subtotal, not a complete vocabulary count. "
                  "The published calculation and manuscript remain unchanged.", ""])
    (RESULTS / "current_research_count.md").write_text("\n".join(lines))
    print(f"Second approval applied: 2649 -> {report['current_provisional_assignments']}; all source rows retained.")


if __name__ == "__main__":
    main()

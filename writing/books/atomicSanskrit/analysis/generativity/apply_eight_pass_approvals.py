"""Apply approved eight-pass proposals without rewriting earlier snapshots."""

import csv
import json

from apply_reconciliation_02 import normalize as second_normalize
from review_remaining_followups import build_report
from run_pilot import HERE, RESULTS, sha

APPROVAL = HERE / "approved_eight_passes_01.json"


def normalize():
    approval = json.loads(APPROVAL.read_text())
    rows, previous = second_normalize()
    review = build_report()
    cases = {case["id"]: case for case in review["cases"]}
    if len(set(approval["cases"])) != len(approval["cases"]):
        raise ValueError("Duplicate approved case")

    def total():
        return len({row["normalized_count_key"] for row in rows if row["record_kind"] == "lexical"})

    if total() != approval["baseline"]:
        raise ValueError("Approved baseline differs")
    applied = []
    for case_id in approval["cases"]:
        case = cases[case_id]
        if not case.get("proposed_merges") or case["delta"] >= 0:
            raise ValueError(f"{case_id} has no count-reducing proposal")
        allowed = {(code, meaning) for code, meanings in case["entries"].items() for meaning in meanings}
        index = {(row["source_code"], row["normalized_meaning_slp1"]): row for row in rows}
        before = total()
        for merger in case["proposed_merges"]:
            members = [tuple(member) for member in merger]
            if not set(members) <= allowed:
                raise ValueError("Approved merger exceeds reviewed scope")
            selected = [index[member] for member in members]
            old_keys = {row["normalized_count_key"] for row in selected}
            if len(old_keys) < 2:
                raise ValueError("Approved merger no longer reduces the count")
            for row in rows:
                if row["normalized_count_key"] in old_keys:
                    selector = (row["source_code"], row["normalized_meaning_slp1"])
                    if selector not in allowed:
                        raise ValueError("Approved merger crosses reviewed scope")
                    row["normalized_count_key"] = selected[0]["normalized_count_key"]
                    row["reconciliation_id"] = case_id
        if total() - before != case["delta"]:
            raise ValueError("Applied change differs from reviewed proposal")
        applied.append(dict(case=case_id, before=before, after=total(), evidence=case["evidence"]))
    if total() != approval["expected_after"]:
        raise ValueError("Approved total differs")
    report = dict(date=approval["date"], status="applied", current_provisional_assignments=total(),
                  baseline=approval["baseline"], vocabulary_total=None, preserved_source_rows=len(rows),
                  decisions=applied, remaining_eight_pass_proposed_delta=review["proposed_delta"] - sum(cases[x]["delta"] for x in approval["cases"]),
                  inputs=dict(previous["inputs"], approved_eight_passes_01=sha(APPROVAL),
                              remaining_review=sha(HERE / "remaining_followup_review.json")))
    return rows, report


def main():
    rows, report = normalize()
    for name in ("approved_eight_pass_assignments_01.csv", "current_base_assignments.csv"):
        with (RESULTS / name).open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    (RESULTS / "approved_eight_pass_meanings_01.json").write_text(payload)
    (RESULTS / "current_base_meanings.json").write_text(payload)
    lines = ["# Current Research Count", "", f"Updated {report['date']}.", "",
             f"Applied provisional base-meaning assignments: **{report['current_provisional_assignments']:,}**.", "",
             "The ten approved eight-pass records contain eleven duplicate reductions, changing 2,645 to 2,634. "
             "All 2,741 source-assignment rows remain available, and every earlier snapshot is preserved.", "",
             "| Approved decision | Before | After |", "|---|---:|---:|"]
    for decision in report["decisions"]:
        lines.append(f"| {decision['case']} | {decision['before']:,} | {decision['after']:,} |")
    lines.extend(["", "[Current dataset](current_base_assignments.csv) · [Applied decisions](current_base_meanings.json)", "",
                  "The remaining eight-pass changes are proposals until separately approved. "
                  "This is not a complete vocabulary count; derivation and inflection remain separate stages.", ""])
    (RESULTS / "current_research_count.md").write_text("\n".join(lines))
    print(f"Eight-pass approval applied: {report['baseline']} -> {report['current_provisional_assignments']}; all source rows retained.")


if __name__ == "__main__":
    main()

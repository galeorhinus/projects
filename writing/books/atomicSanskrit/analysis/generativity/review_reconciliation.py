"""Validate and render proposed follow-ups without applying count changes."""

import copy
import csv
import json

from read_dhatu_concordance import source_text
from run_pilot import ARCHIVE, HERE, RESULTS, sha, verify_sources

REVIEW = HERE / "reconciliation_review_01.json"


def build_report(review=None):
    review = copy.deepcopy(review if review is not None else json.loads(REVIEW.read_text()))
    if review["status"] != "proposed_not_applied":
        raise ValueError("This reporter cannot apply decisions")
    sources = {s["filename"]: s for s in verify_sources()["sources"]}
    history = json.loads((HERE / "identity_review.json").read_text())
    groups = {g["id"]: g for g in history["groups"]}
    baseline = json.loads((RESULTS / "base_meanings.json").read_text())
    with (RESULTS / "base_meaning_assignments.csv").open() as handle:
        rows = list(csv.DictReader(handle))
    keys = {(r["source_code"], r["meaning_slp1"]): r["count_key"] for r in rows}
    if baseline["assignments_after_documented_merges"] != review["baseline"]:
        raise ValueError("Baseline changed; reconcile proposals before regenerating")
    if len(set(keys.values())) != review["baseline"]:
        raise ValueError("Assignment keys disagree with the baseline")
    seen = set()
    affected_keys = set()
    for case in review["cases"]:
        if case["id"] in seen:
            raise ValueError("Duplicate review case")
        seen.add(case["id"])
        original = groups[case["id"]]
        current_keys = {keys[code, meaning]
                        for code, meanings in original["entries"].items() for meaning in meanings}
        if len(current_keys) != case["before_count"]:
            raise ValueError(f"{case['id']}: current count no longer matches")
        if affected_keys & current_keys:
            raise ValueError("Overlapping cases would double-count the proposed effect")
        affected_keys.update(current_keys)
        if type(case["proposed_count"]) is not int or case["proposed_count"] < 0:
            raise ValueError("Proposed count must be a nonnegative integer")
        if not case["evidence"]:
            raise ValueError("Every decision needs evidence")
        for evidence in case["evidence"]:
            if not evidence["anchor"] or evidence["anchor"] not in source_text(evidence["source"]):
                raise ValueError(f"{case['id']}: missing anchor in {evidence['source']}")
            evidence["record"] = sources[evidence["source"]]
        case["original_entries"] = original["entries"]
        case["original_decision"] = original["decision"]
        case["delta"] = case["proposed_count"] - case["before_count"]
    review["proposed_delta"] = sum(c["delta"] for c in review["cases"])
    review["proposed_subtotal"] = review["baseline"] + review["proposed_delta"]
    review["vocabulary_total"] = None
    review["archive_records"] = len(sources)
    review["commentary_records"] = sum(name.startswith("dhatu-") and name != "dhatu-concordance-gana.html"
                                      for name in sources)
    paths = [REVIEW, HERE / "identity_review.json", RESULTS / "base_meanings.json",
             RESULTS / "base_meaning_assignments.csv", ARCHIVE / "dhatupatha.tsv",
             ARCHIVE / "manifest.json"]
    review["inputs"] = {str(p.relative_to(HERE.parents[1])): sha(p) for p in paths}
    return review


def render(report):
    applied = (RESULTS / "normalized_base_meanings.json").exists()
    lines = ["# First Reconciliation Pass: Ten Cases", "",
             f"Date: {report['date']}. **Historical proposal record.**" if applied else
             f"Date: {report['date']}. **Proposals only; not applied.**", "",
             "The author approved the supported changes. See [the applied record and current count](current_research_count.md). "
             "The before/after proposals below are retained for comparison." if applied else
             "The decisions below await author review.", "",
             report["scope"], "", report["policy"], "",
             f"Provisional subtotal before this pass: **{report['baseline']:,}**. "
             f"Subtotal specified by these proposals: **{report['proposed_subtotal']:,}** "
             f"({report['proposed_delta']:+d}). Neither number is a final vocabulary total.", "",
             "The original 2,741 assignment rows and all nine batch reports remain unchanged. "
             "Source corrections below are proposed normalization records, not edits to the archived dataset. "
             "The four reductions concern leading, anger, gleaning, and a grammatical restriction.", "",
             "| Case | Current | Proposed | Difference |", "|---|---:|---:|---:|"]
    for c in report["cases"]:
        lines.append(f"| {c['id']}: {c['label']} | {c['before_count']} | {c['proposed_count']} | {c['delta']:+d} |")
    for c in report["cases"]:
        entries = "; ".join(f"`{code}`: {', '.join(meanings)}"
                            for code, meanings in c["original_entries"].items())
        lines.extend(["", f"## {c['id']}: {c['label']}", "", f"Source entries: {entries}.", "",
                      "### Before", "", c["before"], "", "### Proposed", "", c["after"], "",
                      f"**Count:** {c['before_count']} -> {c['proposed_count']} ({c['delta']:+d}).", "",
                      "### Evidence", ""])
        for e in c["evidence"]:
            lines.append(f"- [{e['source']}]({e['record']['url']}): {e['anchor']}\n\n  {e['role']}")
        lines.extend(["", "### What Remains", "", c["remaining"]])
    lines.extend(["", "## Record and Next Step", "",
                  "The applied decisions are recorded separately; this document retains their proposal-stage evidence. " if applied else
                  "Review the four count reductions and the ay headword correction before applying them. ",
                  "",
                  "Keep the lal, paksh, rat, and vr questions open. The push division/nourishment mismatch "
                  "was an incorrect source alignment, not an incorrect meaning in the input.", "",
                  "The accompanying JSON stores each original decision, current entries, proposed treatment, "
                  "exact source phrases, URLs, access timestamps, and checksums. The source manifest now "
                  f"contains {report['archive_records']} records, including {report['commentary_records']} commentary pages. Twenty-nine snapshots were added "
                  "for this pass; retrieval alone does not mark a passage verified.", "",
                  "The original 84-record follow-up list remains the historical queue. This report supplements "
                  "ten of those records; the separate normalized dataset records the applied decisions.", ""])
    return "\n".join(lines)


def main():
    report = build_report()
    (RESULTS / "reconciliation_review_01.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "reconciliation_review_01.md").write_text(render(report))
    print(f"{len(report['cases'])} cases validated; proposed {report['baseline']} -> "
          f"{report['proposed_subtotal']}; baseline unchanged.")


if __name__ == "__main__":
    main()

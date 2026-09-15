"""Review the next ten cases against the approved normalized baseline."""

import copy
import json

from apply_reconciliation import normalize
from read_dhatu_concordance import source_text
from run_pilot import ARCHIVE, HERE, RESULTS, sha, verify_sources

REVIEW = HERE / "reconciliation_review_02.json"


def build_report(review=None):
    review = copy.deepcopy(review if review is not None else json.loads(REVIEW.read_text()))
    if review["status"] != "proposed_not_applied":
        raise ValueError("Follow-up reporter cannot apply decisions")
    rows, applied = normalize()
    if applied["current_provisional_assignments"] != review["baseline"]:
        raise ValueError("Normalized baseline changed")
    sources = {s["filename"]: s for s in verify_sources()["sources"]}
    index = {(r["source_code"], r["normalized_meaning_slp1"]): r for r in rows}
    if len(index) != len(rows):
        raise ValueError("Normalized selectors need disambiguation")
    seen, affected = set(), set()
    for case in review["cases"]:
        if case["id"] in seen:
            raise ValueError("Duplicate follow-up case")
        seen.add(case["id"])
        selected = [index[code, m] for code, meanings in case["entries"].items() for m in meanings]
        if any(r["record_kind"] != "lexical" for r in selected):
            raise ValueError("A grammatical record cannot be counted as lexical")
        keys = {r["normalized_count_key"] for r in selected}
        if affected & keys:
            raise ValueError("Cases overlap in the normalized count")
        affected.update(keys)
        if len(keys) != case["before_count"]:
            raise ValueError(f"{case['id']}: count drift")
        if type(case["proposed_count"]) is not int or case["proposed_count"] < 0:
            raise ValueError("Invalid proposed count")
        if not case["evidence"]:
            raise ValueError("Missing evidence")
        for e in case["evidence"]:
            if not e["anchor"] or e["anchor"] not in source_text(e["source"]):
                raise ValueError(f"{case['id']}: missing anchor in {e['source']}")
            e["record"] = sources[e["source"]]
        case["original_rows"] = selected
        case["delta"] = case["proposed_count"] - case["before_count"]
    review["proposed_delta"] = sum(c["delta"] for c in review["cases"])
    review["proposed_subtotal"] = review["baseline"] + review["proposed_delta"]
    review["vocabulary_total"] = None
    review["archive_records"] = len(sources)
    historical = json.loads((RESULTS / "identity_followups.json").read_text())["groups"]
    first = json.loads((HERE / "reconciliation_review_01.json").read_text())["cases"]
    revisited = {c["id"] for c in first} | {c["prior_id"] for c in review["cases"]}
    untouched = [g["id"] for g in historical if g["id"] not in revisited]
    review["followup_coverage"] = {"historical_records": len(historical), "records_revisited": len(revisited),
                                   "not_revisited": len(untouched), "next_unreviewed_ids": untouched[:10]}
    review["inputs"] = dict(applied["inputs"], followup_review=sha(REVIEW))
    return review


def render(report):
    lines = ["# Second Reconciliation Pass: Ten Cases", "",
             f"Date: {report['date']}. **Proposals only; not applied.**", "",
             f"The first reconciliation is now applied: the working provisional subtotal is **{report['baseline']:,}**. "
             f"The changes proposed below would produce **{report['proposed_subtotal']:,}** "
             f"({report['proposed_delta']:+d}). No manuscript changes.", "",
             report["selection"], "",
             "The count concerns a different word or meaning, not different spelling, English gloss wording, "
             "or repeated grammatical documentation. Alternative readings remain attributed to their sources. "
             "Neither subtotal is a final vocabulary count.", "",
             "| Case | Current | Proposed | Change |", "|---|---:|---:|---:|"]
    for c in report["cases"]:
        lines.append(f"| {c['id']}: {c['label']} | {c['before_count']} | {c['proposed_count']} | {c['delta']:+d} |")
    for c in report["cases"]:
        entries = "; ".join(f"`{code}`: {', '.join(meanings)}" for code, meanings in c["entries"].items())
        lines.extend(["", f"## {c['id']}: {c['label']}", "", f"Earlier record: {c['prior_id']}. Entries: {entries}.", "",
                      "### Before", "", c["before"], "", "### Proposed", "", c["after"], "",
                      f"**Count:** {c['before_count']} -> {c['proposed_count']} ({c['delta']:+d}).", "",
                      "### Evidence", ""])
        for e in c["evidence"]:
            lines.extend([f"- [{e['source']}]({e['record']['url']}): {e['anchor']}", "", f"  {e['role']}"])
        lines.extend(["", "### What Remains", "", c["remaining"]])
    lines.extend(["", "## Review Decisions", "",
                  "Three proposed mergers: bhram's movement, dhvan's sound, and jharjh's shared rebuking/threatening "
                  "meaning. One proposed exclusion: the unsupported binding assignment under dhri-ng, which "
                  "would remain in the source-reading record. That fourth change removes an unverified assignment "
                  "from the admitted count; it does not establish that no binding reading exists anywhere.", "",
                  "The ay identity remains open. Bhu's declined heading is explained, and mixing has a concrete "
                  "example. The dhup and ghat alternatives are recorded without adding them automatically. "
                  "Ghri retains its separate meanings; ghush now has a concrete non-declaring example.", "",
                  f"The archive contains {report['archive_records']} records. Twenty-four snapshots were added "
                  "in this pass. Exact URLs, access times, checksums, original rows, normalized rows, and quoted "
                  "locator phrases are stored in the matching JSON report and archive manifest. Retrieval is "
                  "not itself a verification decision. The reports compare digital transcriptions, not freshly "
                  "collated print editions.", "",
                  "[Applied first pass and current subtotal](current_research_count.md). "
                  "[Historical 84-record follow-up list](identity_followups.md). "
                  "The new review supplements that list; it does not erase earlier decisions.", ""])
    coverage = report["followup_coverage"]
    lines.extend([f"Across the two targeted passes, {coverage['records_revisited']} of the "
                  f"{coverage['historical_records']} historical follow-up records have been revisited; "
                  f"{coverage['not_revisited']} have not. Revisited does not mean resolved. "
                  "The corrected ay case deliberately returns to IR210.", ""])
    return "\n".join(lines)


def main():
    report = build_report()
    (RESULTS / "reconciliation_review_02.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (RESULTS / "reconciliation_review_02.md").write_text(render(report))
    print(f"{len(report['cases'])} cases validated; proposed {report['baseline']} -> "
          f"{report['proposed_subtotal']}; applied count unchanged.")


if __name__ == "__main__":
    main()

"""Render the seven bounded follow-up batches and their consolidation record."""

from collections import Counter
from copy import deepcopy
import json

from apply_reconciliation_02 import normalize
from prepare_followup_packets import remaining
from read_dhatu_concordance import source_text
from review_base_identities import display
from run_pilot import ARCHIVE, HERE, RESULTS, ROOT, sha, verify_sources

REVIEW = HERE / "remaining_followup_review.json"
TRACKER = ROOT / "working/10_active/as_generativity_eight_passes_codex.md"


def build_report(review=None):
    review = deepcopy(review if review is not None else json.loads(REVIEW.read_text()))
    queue = remaining()
    decisions = {c["id"]: c for c in review["cases"]}
    if len(decisions) != len(review["cases"]):
        raise ValueError("Duplicate review case")
    if list(decisions) != [g["id"] for g in queue[:len(decisions)]]:
        raise ValueError("Decisions must follow the declared remaining queue")
    rows, applied = normalize()
    if applied["current_provisional_assignments"] != review["baseline"]:
        raise ValueError("Baseline no longer matches")
    index = {(r["source_code"], r["meaning_slp1"]): r for r in rows}
    sources = {s["filename"]: s for s in verify_sources()["sources"]}
    result, affected = [], set()
    for i, original in enumerate(queue):
        if original["id"] not in decisions:
            break
        c = dict(decisions[original["id"]])
        selected = {(code, m): index[code, m] for code, meanings in original["entries"].items() for m in meanings}
        keys = {key: row["normalized_count_key"] for key, row in selected.items() if row["record_kind"] == "lexical"}
        if affected & set(keys.values()):
            raise ValueError("Overlapping count groups")
        affected.update(keys.values())
        before = len(set(keys.values()))
        for merger in c.get("proposed_merges", []):
            members = [tuple(m) for m in merger]
            if not set(members) <= keys.keys():
                raise ValueError("Proposed merger is outside reviewed scope")
            old = {keys[m] for m in members}
            if len(old) < 2:
                raise ValueError("Proposed merger does not reduce the current count")
            canonical = keys[members[0]]
            keys = {k: canonical if v in old else v for k, v in keys.items()}
        for item in c.get("proposed_exclusions", []):
            if tuple(item) not in keys:
                raise ValueError("Proposed exclusion is outside reviewed scope")
            del keys[tuple(item)]
        for e in c["evidence"]:
            if not e["anchor"] or e["anchor"] not in source_text(e["source"]):
                raise ValueError(f"{c['id']}: missing anchor in {e['source']}: {e['anchor']}")
            e["record"] = sources[e["source"]]
        if not c["evidence"] or not c["remaining"]:
            raise ValueError("Evidence and disposition are required")
        c.update(batch=i // 10 + 1, label=display(original["headword"]), entries=original["entries"],
                 before=original["decision"], original_followup=original["remaining"],
                 before_count=before, proposed_count=len(set(keys.values())), delta=len(set(keys.values()))-before)
        result.append(c)
    return dict(date=review["date"], baseline=review["baseline"], status="proposals_not_applied",
                cases=result, queued_records=len(queue), reviewed_records=len(result),
                complete=len(result)==len(queue), proposed_delta=sum(c["delta"] for c in result),
                archive_records=len(sources), vocabulary_total=None,
                inputs=dict(applied["inputs"], remaining_review=sha(REVIEW), source_manifest=sha(ARCHIVE / "manifest.json")))


def consolidate(report):
    if not report["complete"] or report["reviewed_records"] != 65:
        raise ValueError("All 65 follow-ups must be reviewed before consolidation")
    first = json.loads((RESULTS / "reconciliation_review_01.json").read_text())
    second = json.loads((RESULTS / "reconciliation_review_02.json").read_text())
    approval_first = HERE / "approved_reconciliation.json"
    approval_second = HERE / "approved_reconciliation_02.json"
    approval_new = HERE / "approved_eight_passes_01.json"
    approved_ids = {c["review_id"] for c in json.loads(approval_first.read_text())["decisions"]}
    second_actions = json.loads(approval_second.read_text())
    approved_ids.update(c["case"] for c in second_actions["merges"] + second_actions["exclude"])
    history = json.loads((RESULTS / "identity_followups.json").read_text())["groups"]
    latest = {}
    for filename, cases in [("reconciliation_review_01.md", first["cases"]),
                            ("reconciliation_review_02.md", second["cases"])]:
        for c in cases:
            identifier = c.get("prior_id", c["id"])
            latest[identifier] = dict(id=identifier, review_id=c["id"], report=filename,
                                      disposition="approved_applied" if c["id"] in approved_ids else c["outcome"],
                                      original_review_disposition=c["outcome"], decision=c["after"], remaining=c["remaining"])
    if len(latest) != 19:
        raise ValueError("Earlier reviews must cover 19 unique historical records")
    if set(latest) & {c["id"] for c in report["cases"]}:
        raise ValueError("Remaining queue repeats earlier records")
    for c in report["cases"]:
        latest[c["id"]] = dict(id=c["id"], review_id=c["id"],
                              report=f"remaining_followup_batch_{c['batch']:02d}.md",
                              disposition=c["status"], decision=c["decision"], remaining=c["remaining"])
    if len(history) != 84 or set(latest) != {g["id"] for g in history}:
        raise ValueError("Historical follow-up coverage is incomplete")
    newly_approved = set(json.loads(approval_new.read_text())["cases"]) if approval_new.exists() else set()
    available_proposals = {c["id"] for c in report["cases"] if c["delta"]}
    if not newly_approved <= available_proposals:
        raise ValueError("New approval is outside the eight-pass proposals")
    newly_approved_delta = sum(c["delta"] for c in report["cases"] if c["id"] in newly_approved)
    for item in latest.values():
        if item["id"] in newly_approved:
            item["original_review_disposition"] = item["disposition"]
            item["disposition"] = "approved_applied"
    remaining_delta = report["proposed_delta"] - newly_approved_delta
    return dict(date=report["date"],
                status="bounded_sweep_complete_all_proposals_applied" if remaining_delta == 0 else "bounded_sweep_complete_partial_approval",
                pre_eight_pass_subtotal=report["baseline"], applied_subtotal=report["baseline"] + newly_approved_delta,
                approved_new_cases=sorted(newly_approved), approved_new_delta=newly_approved_delta,
                remaining_proposed_delta=remaining_delta,
                proposed_delta=report["proposed_delta"],
                proposed_subtotal=report["baseline"] + report["proposed_delta"], vocabulary_total=None,
                historical_records=84, previously_revisited=19, newly_reviewed=65,
                new_dispositions=dict(Counter(c["status"] for c in report["cases"])),
                archive_records=report["archive_records"],
                historical_coverage=[latest[g["id"]] for g in history],
                proposals=[c for c in report["cases"] if c["delta"]],
                inputs=dict(report["inputs"], first_report=sha(RESULTS / "reconciliation_review_01.json"),
                            second_report=sha(RESULTS / "reconciliation_review_02.json"),
                            historical_followups=sha(RESULTS / "identity_followups.json"),
                            first_approval=sha(approval_first), second_approval=sha(approval_second),
                            new_approval=sha(approval_new) if approval_new.exists() else None))


def render_consolidation(summary, report):
    lines = ["# Eight-pass Consolidation", "", f"Completed {summary['date']}. Research only; no manuscript changes.", "",
             "## Counts", "", "| Stage | Provisional assignments |", "|---|---:|",
             "| Historical nine-batch result | 2,653 |", "| First approved reconciliation | 2,649 |",
             f"| Second approved reconciliation | {summary['pre_eight_pass_subtotal']:,} |",
             f"| Current subtotal after {len(summary['approved_new_cases'])} newly approved records | {summary['applied_subtotal']:,} |",
             f"| Approved eight-pass endpoint | {summary['proposed_subtotal']:,} |", "",
             "All 2,741 source-assignment rows remain in the research dataset. Neither subtotal is a final vocabulary count. "
             "No derivational or inflectional multiplier has been applied.", "",
             "## Eight-pass Count Changes", "", f"Ten records support eleven duplicate reductions. {len(summary['approved_new_cases'])} records are now approved; "
             f"{len(summary['proposals']) - len(summary['approved_new_cases'])} remain proposals.", "",
             "| Record | Before | Proposed | Status | Evidence and decision |", "|---|---:|---:|---|---|"]
    for c in summary["proposals"]:
        status = "Approved and applied" if c["id"] in summary["approved_new_cases"] else "Awaiting review"
        lines.append(f"| {c['id']}: {c['label']} | {c['before_count']} | {c['proposed_count']} | {status} | "
                     f"[Pass {c['batch']}](remaining_followup_batch_{c['batch']:02d}.md) |")
    lines.extend(["", "## Dispositions", "", "These categories describe the 65 newly reviewed records, not the entire vocabulary.", "",
                  "| Disposition | Records | Meaning |", "|---|---:|---|"])
    descriptions = dict(propose_merge="Count change awaiting approval", retain_distinction="Keep different words or meanings",
                        retain_readings="Keep the selected reading; preserve alternatives", defer_reading="Exact citation or meaning reading unresolved",
                        defer_identity="Word identity unresolved", defer_senses="Finer meaning segmentation unresolved",
                        defer_formation="Lexical decision retained; move grammar or cross-spelling work to its proper stage")
    for status, count in summary["new_dispositions"].items():
        lines.append(f"| `{status}` | {count} | {descriptions[status]} |")
    lines.extend(["", "## Deferred Work", "",
                  "The bounded sweep is finished. It does not authorize another automatic cycle of source searches.", "",
                  "1. Reconcile disputed citations and readings against a chosen edition. Keep unsupported annotations identifiable rather than silently correcting them.",
                  "2. Test unresolved word identities and finer meanings only with a declared case list and contextual examples.",
                  "3. Carry marker, pada, vowel, and spelling restrictions into formation eligibility. Treat IR220/IR221 as one shared cross-spelling question.",
                  "4. Preserve the three partial meaning lists and two unenumerated entries from the earlier interpretation audit. This sweep does not complete those lists.",
                  "5. Build the named derivation and affix-eligibility stages separately; then count conjugation and declension. These stages remain outside the present base-identity subtotal.", "",
                  "## Evidence", "",
                  f"The archive contains {summary['archive_records']} records, including 234 commentary pages added for this sweep. "
                  "Candidate retrieval is not verification: only the exact excerpts attached to decisions serve as evidence. "
                  "The batch JSON files retain source URLs, retrieval timestamps, and SHA-256 hashes. "
                  "Quoted material from the extended discussion under 7.4.68 is attributed to Bala-manorama, not to the sutra's wording.", "",
                  "## Coverage Ledger", "",
                  "All 84 historical follow-ups are accounted for: 19 previously revisited and 65 reviewed here. "
                  "This is coverage, not a claim that every issue is resolved. The latest recorded disposition and remainder follow. "
                  "Entries marked approved_applied retain their original review wording below; any proposal wording there is historical, not awaiting approval again."])
    for c in summary["historical_coverage"]:
        lines.extend(["", f"### {c['id']}", "", f"[Latest review: {c['review_id']}]({c['report']}) · `{c['disposition']}`", "",
                      c["decision"], "", "Remaining: " + c["remaining"]])
    return "\n".join(lines) + "\n"


def render_batch(report, batch):
    cases = [c for c in report["cases"] if c["batch"] == batch]
    earlier = sum(c["delta"] for c in report["cases"] if c["batch"] < batch)
    delta = sum(c["delta"] for c in cases)
    lines = [f"# Remaining Follow-ups: Pass {batch}", "", f"Reviewed {report['date']}. New count changes are proposals, not applied.", "",
             f"Applied baseline: **{report['baseline']:,}**. This batch's proposed change: **{delta:+d}**. "
             f"Cumulative scenario after this batch: **{report['baseline']+earlier+delta:,}**.", "",
             "| Record | Before | Proposed | Change |", "|---|---:|---:|---:|"]
    for c in cases:
        lines.append(f"| {c['id']}: {c['label']} | {c['before_count']} | {c['proposed_count']} | {c['delta']:+d} |")
    for c in cases:
        lines.extend(["", f"## {c['id']}: {c['label']}", "", "### Before", "", c["before"], "",
                      "### After Review", "", c["decision"], "",
                      f"Count: **{c['before_count']} -> {c['proposed_count']}**. Disposition: `{c['status']}`.", "",
                      "### Evidence", ""])
        for e in c["evidence"]:
            lines.extend([f"- [{e['source']}]({e['record']['url']}): {e['anchor']}", "", f"  {e['role']}"])
        lines.extend(["", "### Remaining Work", "", c["remaining"]])
    return "\n".join(lines) + "\n"


def main():
    report = build_report()
    (RESULTS / "remaining_followup_review.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    summary = consolidate(report) if report["complete"] else None
    current = summary["applied_subtotal"] if summary else report["baseline"]
    progress = ["# Generativity Follow-up: Eight Passes", "",
                f"Authorized 2026-09-13. Current applied research subtotal: **{current:,}**. "
                "Unapproved count changes remain proposals. No manuscript edits.", "",
                "| Pass | Scope | Status | Report |", "|---|---|---|---|"]
    for batch in range(1, 8):
        selected = [c for c in report["cases"] if c["batch"] == batch]
        expected = 5 if batch == 7 else 10
        status = "Complete" if len(selected) == expected else "In progress" if selected else "Pending"
        name = f"remaining_followup_batch_{batch:02d}"
        if selected:
            (RESULTS / (name + ".md")).write_text(render_batch(report, batch))
            (RESULTS / (name + ".json")).write_text(json.dumps(dict(report, scope="batch", batch=batch,
                                                                      batch_reviewed_records=len(selected), cases=selected),
                                                                 ensure_ascii=False, indent=2) + "\n")
        link = f"[Before/after](../../analysis/generativity/results/{name}.md)" if selected else "Pending"
        progress.append(f"| {batch} | {expected} records | {status} | {link} |")
    if report["complete"]:
        name = "eight_pass_consolidation"
        (RESULTS / (name + ".json")).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
        (RESULTS / (name + ".md")).write_text(render_consolidation(summary, report))
        progress.append(f"| 8 | Consolidation and integrity checks | Complete | [Summary](../../analysis/generativity/results/{name}.md) |")
    else:
        progress.append("| 8 | Consolidation and integrity checks | Pending | Pending |")
    remaining_delta = summary["remaining_proposed_delta"] if summary else report["proposed_delta"]
    progress.extend(["", f"{report['reviewed_records']} of 65 records reviewed. Remaining proposed change: "
                     f"{remaining_delta:+d}. Reviewed does not mean resolved; every case has an explicit disposition.", ""])
    TRACKER.write_text("\n".join(progress))
    print(f"Reviewed {report['reviewed_records']}/65; additional proposed delta {report['proposed_delta']:+d}.")


if __name__ == "__main__":
    main()

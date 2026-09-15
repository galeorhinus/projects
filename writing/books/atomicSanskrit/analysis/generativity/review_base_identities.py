"""Apply source-backed identity decisions to individual meaning assignments."""

from collections import Counter
import json

from read_dhatu_concordance import source_text
from run_pilot import HERE, RESULTS
from vidyut import lipi

IDENTITY_REVIEW = HERE / "identity_review.json"


def apply_review(entries, assignments, identities, sources, review=None):
    review = review if review is not None else json.loads(IDENTITY_REVIEW.read_text())
    by_code = {row["source_code"]: row for row in entries}
    by_assignment = {(row["source_code"], row["meaning_slp1"]): row for row in assignments}
    groups = {}
    for row in identities:
        groups.setdefault(row["group_id"], set()).add(row["source_code"])
    legacy_groups = {row["group_id"] for row in identities if row["review_id"]}
    for row in entries:
        row["identity_batch_review_id"] = ""
    for row in assignments:
        # Start with the earlier documented identities; preserve the original row keys.
        row["count_key"] = json.dumps([row["provisional_word_id"], row["meaning_id"]])
        row["identity_batch_review_id"] = ""
    for row in identities:
        row["batch_outcome"] = ""
        row["assignment_reductions"] = 0
    before = len({row["count_key"] for row in assignments})
    if before != review["baseline_adjusted_assignments"]:
        raise ValueError("Identity review baseline changed; reconcile the batch before rebuilding")

    seen_ids, seen_groups, redirected, reviewed = set(), set(), set(), []
    for item in review["groups"]:
        group_id, codes = item["group_id"], set(item["entries"])
        if item["id"] in seen_ids or group_id in seen_groups or group_id in legacy_groups:
            raise ValueError(f"Repeated identity review: {item['id']}")
        seen_ids.add(item["id"])
        seen_groups.add(group_id)
        if groups.get(group_id) != codes:
            raise ValueError(f"Identity group membership changed: {item['id']}")
        for code, units in item["entries"].items():
            if by_code[code]["citation_slp1"] != item["citation"] or by_code[code]["units_slp1"] != units:
                raise ValueError(f"Reviewed citation or meanings changed: {code}")
        if item["outcome"] not in ("merge_shared_meanings", "retain_distinct_meanings", "open"):
            raise ValueError(f"Unknown identity outcome: {item['id']}")
        if bool(item["merges"]) != (item["outcome"] == "merge_shared_meanings"):
            raise ValueError(f"Outcome and merges disagree: {item['id']}")
        if item["outcome"] == "open" and not item.get("remaining"):
            raise ValueError(f"Open identity needs a next check: {item['id']}")
        if not item["evidence"]:
            raise ValueError(f"Identity review needs evidence: {item['id']}")
        evidence = []
        for witness in item["evidence"]:
            name = witness["source"]
            if name not in sources or not witness.get("anchor") or witness["anchor"] not in source_text(name):
                raise ValueError(f"Identity evidence not found: {item['id']} / {name}")
            evidence.append({**sources[name], **witness})

        members = [row for row in assignments if row["source_code"] in codes]
        count_before = len({row["count_key"] for row in members})
        used = set()
        for merge in item["merges"]:
            keys = [tuple(key) for key in merge["members"]]
            canonical = tuple(merge["canonical"])
            if len(keys) < 2 or len(set(keys)) != len(keys) or canonical not in keys:
                raise ValueError(f"Invalid meaning merge: {item['id']}")
            if used.intersection(keys) or any(code not in codes or (code, unit) not in by_assignment
                                              for code, unit in keys):
                raise ValueError(f"Overlapping or unknown meaning merge: {item['id']}")
            used.update(keys)
            target = by_assignment[canonical]["count_key"]
            for key in keys:
                row = by_assignment[key]
                if row["count_key"] != target:
                    redirected.add(key)
                row["count_key"] = target
        count_after = len({row["count_key"] for row in members})
        for row in members:
            row["identity_batch_review_id"] = item["id"]
        for code in codes:
            by_code[code]["identity_batch_review_id"] = item["id"]
            by_code[code]["identity_review"] = item["outcome"]
        for row in identities:
            if row["group_id"] == group_id:
                row["review_id"] = item["id"]
                row["batch_outcome"] = item["outcome"]
                row["decision"] = item["outcome"]
                affected = sum((row["source_code"], unit) in redirected
                               for unit in item["entries"][row["source_code"]])
                row["assignment_reductions"] = affected
                row["merged"] = affected == len(item["entries"][row["source_code"]])
        reviewed.append({**item, "source_records": evidence,
                         "before": count_before, "after": count_after,
                         "reduction": count_before - count_after})
    after = len({row["count_key"] for row in assignments})
    if before - after != sum(row["reduction"] for row in reviewed):
        raise ValueError("Identity reductions do not reconcile")
    outcomes = Counter(row["outcome"] for row in reviewed)
    declared = review["batches"]
    numbers = [batch["number"] for batch in declared]
    group_batches = [row.get("batch", 1) for row in reviewed]
    if numbers != sorted(set(numbers)) or set(numbers) != set(group_batches) or group_batches != sorted(group_batches):
        raise ValueError("Identity batch order or declarations changed")
    batches, running_total, reviewed_count = [], before, len(legacy_groups)
    for config in declared:
        selected = [row for row in reviewed if row.get("batch", 1) == config["number"]]
        if config["before"] != running_total or config["group_count"] != len(selected):
            raise ValueError(f"Identity batch baseline or membership changed: {config['number']}")
        batch_outcomes = Counter(row["outcome"] for row in selected)
        reduction = sum(row["reduction"] for row in selected)
        batches.append({
            "number": config["number"], "before": running_total, "after": running_total - reduction,
            "reduction": reduction, "reviewed_groups": len(selected),
            "reviewed_entries": sum(len(row["entries"]) for row in selected),
            "merge_groups": batch_outcomes["merge_shared_meanings"],
            "retained_groups": batch_outcomes["retain_distinct_meanings"],
            "open_groups": batch_outcomes["open"], "previously_reviewed_groups": reviewed_count,
            "unreviewed_groups": len(groups) - reviewed_count - len(selected),
            "group_ids": [row["id"] for row in selected],
        })
        running_total -= reduction
        reviewed_count += len(selected)
    if running_total != after:
        raise ValueError("Identity batch totals do not reconcile")
    return {
        "date": review["date"], "selection": review["selection"], "policy": review["policy"],
        "reviewed_groups": len(reviewed), "reviewed_entries": sum(len(r["entries"]) for r in reviewed),
        "merge_groups": outcomes["merge_shared_meanings"],
        "retained_groups": outcomes["retain_distinct_meanings"], "open_groups": outcomes["open"],
        "before": before, "after": after, "reduction": before - after,
        "previously_reviewed_groups": len(legacy_groups),
        "unreviewed_groups": len(groups.keys() - seen_groups - legacy_groups),
        "groups": reviewed, "batches": batches,
    }


def display(slp):
    return (lipi.transliterate(slp, lipi.Scheme.Slp1, lipi.Scheme.Devanagari) +
            " (" + lipi.transliterate(slp, lipi.Scheme.Slp1, lipi.Scheme.Iast) + ")")


def write_report(report):
    number = report.get("batch_number")
    suffix = f": Batch {number}" if number else ""
    stem = f"identity_review_batch_{number:02d}" if number else "identity_review"
    lines = [f"# Word-Meaning Identity Review{suffix}", "", f"Date: {report['date']}.", "",
             "## Result", "",
             f"Reviewed **{report['reviewed_groups']} groups / {report['reviewed_entries']} source entries**. "
             f"{report['merge_groups']} groups support consolidations, {report['retained_groups']} retain "
             f"different words or meanings, and {report['open_groups']} remain open.", "",
             f"**{report['before']:,} → {report['after']:,} provisional assignments:** "
             f"{report['reduction']} duplicate assignments consolidated. No source row or original gloss was deleted. "
             "No new meaning, prefix, derivation, or inflection was added.", "",
             report["selection"], "", report["policy"], ""]
    if not number:
        lines += ["## Batches", "", "| Batch | Groups | Before | After | Open groups |", "|---|---:|---:|---:|---:|"]
        for batch in report["batches"]:
            lines.append(f"| [Batch {batch['number']}](identity_review_batch_{batch['number']:02d}.md) | "
                         f"{batch['reviewed_groups']} | {batch['before']:,} | {batch['after']:,} | {batch['open_groups']} |")
        lines.append("")
    lines += ["## Before and After", "",
             "| Group | Source entries | Before | After | Decision |", "|---|---|---:|---:|---|"]
    for row in report["groups"]:
        lines.append(f"| {display(row['headword'])} | {', '.join(row['entries'])} | "
                     f"{row['before']} | {row['after']} | {row['decision']} |")
    lines += ["", "An unchanged count is not necessarily a closed decision: the open groups below "
              "remain provisional. Retaining different meanings also does not assert that they are unrelated words.",
              "", "## Decisions and Evidence", ""]
    for row in report["groups"]:
        lines += [f"### {row['id']}: {display(row['headword'])}", "", row["decision"], "",
                  "Current assignments: " + "; ".join(
                      f"{code}: {', '.join(display(unit) for unit in units)}"
                      for code, units in row["entries"].items()) + ".", ""]
        for merge in row["merges"]:
            lines += ["Count together: " + "; ".join(f"{code}: {display(unit)}" for code, unit in merge["members"]) +
                      f". Counting representative: {merge['canonical'][0]}.", ""]
        for witness in row["source_records"]:
            lines.append(f"- [{witness['filename']}]({witness['url']}): {witness['anchor']}. {witness['role']}")
        if row.get("remaining"):
            lines += ["", "Remaining check: " + row["remaining"]]
        if row.get("eligibility"):
            lines += ["", "For generation: " + row["eligibility"]]
        lines.append("")
    lines += ["## Audit Record", "",
              "The [decision ledger](../identity_review.json) records exact group membership, original meaning "
              "units, locator phrases, and each accepted assignment-level merge. The build rejects changed "
              "membership, missing evidence, overlapping merges, or a changed pre-batch subtotal. "
              "The JSON report retains full source URLs, retrieval timestamps, and checksums.", "",
              "The assignment CSV preserves the original source and meaning IDs alongside a separate `count_key`. "
              "Only the documented shared meaning receives the same counting key. Other meanings attached "
              "to the same source entries retain their independent keys.", "",
              "## Next", "",
              f"The queue contains **{report['unreviewed_groups']} unreviewed citation groups**. "
              f"Keep the {report['open_groups']} open groups covered here and the recorded meaning/eligibility "
              "follow-ups in the queue, together with open cases from earlier batches. "
              "The earlier three partial lists and two unenumerated entries also remain tracked. "
              "The manuscript and its existing total remain unchanged."]
    (RESULTS / f"{stem}.md").write_text("\n".join(lines) + "\n")
    (RESULTS / f"{stem}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    if not number:
        for batch in report["batches"]:
            write_report({**report, **batch, "batch_number": batch["number"],
                          "selection": f"Next {batch['reviewed_groups']} unreviewed groups in the established SLP1 ledger order.",
                          "groups": [row for row in report["groups"] if row["id"] in batch["group_ids"]],
                          "batches": []})
        write_followups(report)


def write_followups(report):
    groups = [row for row in report["groups"] if row.get("remaining")]
    payload = {"date": report["date"], "inputs": report["inputs"], "groups": groups,
               "unreviewed_groups": report["unreviewed_groups"],
               "open_groups": report["open_groups"],
               "other_groups_with_followups": len(groups) - report["open_groups"]}
    (RESULTS / "identity_followups.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Identity Follow-ups", "",
             "This list includes questions left within partly consolidated or retained groups, "
             "not only groups labeled open. A retained assignment is not a claim that every finer sense has been resolved.", "",
             f"Unreviewed exact-citation groups: **{report['unreviewed_groups']}**. "
             f"Wholly open groups: **{report['open_groups']}**. "
             f"Other groups with a recorded follow-up: **{payload['other_groups_with_followups']}**.", "",
             "The three partial meaning lists and two unenumerated entries remain separately in "
             "[the meaning review](meaning_review.md). This exact-citation pass does not discover all "
             "identities between different citation spellings or settle every finer sense of a single entry.", ""]
    for row in groups:
        batch = row.get("batch", 1)
        lines += [f"## {row['id']}: {display(row['headword'])}", "",
                  f"[Batch {batch}](identity_review_batch_{batch:02d}.md); "
                  f"source entries: {', '.join(row['entries'])}.", "",
                  "Decision retained: " + row["decision"], "",
                  "Next check: " + row["remaining"], ""]
        lines += [f"- [{s['filename']}]({s['url']}): {s['anchor']}" for s in row["source_records"]]
        lines.append("")
    (RESULTS / "identity_followups.md").write_text("\n".join(lines) + "\n")

    if report["unreviewed_groups"]:
        return
    batches = [batch for batch in report["batches"] if batch["number"] >= 4]
    lines = ["# Remaining Identity Passes: Results", "", f"Date: {report['date']}", "",
             f"All **{sum(b['reviewed_groups'] for b in batches)} remaining groups** "
             f"({sum(b['reviewed_entries'] for b in batches)} source entries) have been examined in six batches. "
             "No manuscript, companion prose, or published endnote was edited.", "",
             "## Before and After", "",
             "These are provisional source-meaning assignments after documented duplicate consolidation, "
             "not a Sanskrit vocabulary total. All 2,741 original assignment rows remain in the CSV.", "",
             "| Batch | Groups | Before | After | Duplicate reductions | Wholly open |",
             "|---|---:|---:|---:|---:|---:|"]
    for batch in batches:
        lines.append(f"| [Batch {batch['number']}](identity_review_batch_{batch['number']:02d}.md) | "
                     f"{batch['reviewed_groups']} | {batch['before']:,} | {batch['after']:,} | "
                     f"{batch['reduction']} | {batch['open_groups']} |")
    lines += ["", f"The six batches reduce **{batches[0]['before']:,} to {report['after']:,}**, "
              f"removing {sum(b['reduction'] for b in batches)} duplicate counts. "
              "Including the two earlier consolidations and Batches 1-3, the original 2,741 assignments "
              f"have {2741 - report['after']} documented duplicate reductions.", "",
              "## What Changed", "",
              "- Repetition for accent, grammatical class, or a particular form no longer produces another "
              "count when the commentary establishes the shared word-meaning. Plush's two burning entries "
              "and the repeated sad entries are examples.",
              "- A partial overlap only removes the duplicate portion. Protecting stays separate "
              "from filling, and gathering stays separate from casting.",
              "- Different words remain separate even when their meanings match. The four tup/tump/tuph/tumph "
              "words each keep their own harming meaning; only the repeated listing of each word is consolidated.",
              "- Conflicting readings remain recorded. Examples include the fourth-class push and rush glosses, "
              "initial u in udhras, and the grammatical restriction attached to yam.", "",
              "## What Remains", "",
              f"All 223 exact-citation groups have now been examined, including the two earlier groups. "
              f"**{report['open_groups']} remain wholly open**, and "
              f"**{payload['other_groups_with_followups']} other groups have recorded follow-ups**. "
              "The [follow-up list](identity_followups.md) preserves every one, with source URLs and exact locators. "
              "The three partial lists and two unenumerated entries are additional meaning work.", "",
              "Next, resolve the reading differences that affect the base count, examine identities across "
              "different citation spellings, and establish eligibility for the named derivational operations. "
              "Verbal, nominal, and indeclinable formations will be counted separately; person, number, "
              "and case expansions still belong to the subsequent inflection stage.", "",
              "## Evidence and Reproduction", "",
              "The [complete decision record](identity_review.json) contains source URLs, retrieval timestamps, "
              "checksums, and exact quoted locators. Each batch also has its own Markdown and JSON report. "
              "The archived transcriptions have not been silently corrected, and they have not been freshly "
              "collated against printed editions. Downloaded candidate pages are not all counted as verified evidence.", "",
              "Run the commands in the [analysis README](../README.md) to regenerate the counts and reports. "
              "The original source and meaning IDs remain intact; only an explicit shared counting key changes."]
    (RESULTS / "identity_passes_complete.md").write_text("\n".join(lines) + "\n")

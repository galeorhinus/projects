#!/usr/bin/env python3
"""Extract source meaning assignments, keeping lexical identity review separate."""

from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re

from vidyut import lipi

from run_pilot import ARCHIVE, HERE, RESULTS, ROOT, LOCAL_DATA, crosswalk, sha, verify_sources
from read_dhatu_concordance import source_text
from review_base_identities import IDENTITY_REVIEW, apply_review, write_report as write_identity_report

ANALYSIS = HERE / "meaning_analysis.json"
REVIEW = HERE / "meaning_review.json"
GANA_NAMES = {
    1: "BvAdi", 2: "adAdi", 3: "juhotyAdi", 4: "divAdi", 5: "svAdi",
    6: "tudAdi", 7: "ruDAdi", 8: "tanAdi", 9: "kryAdi", 10: "curAdi",
}


def display(text):
    dev = lipi.transliterate(text, lipi.Scheme.Slp1, lipi.Scheme.Devanagari)
    iast = lipi.transliterate(text, lipi.Scheme.Slp1, lipi.Scheme.Iast)
    return f"{dev} ({iast})"


def classify(gloss, rules):
    text = " ".join(gloss.split())
    deferred = rules["deferred_glosses"]
    if text in deferred:
        return {"status": "needs_interpretation", "units": [], "reason": deferred[text]}
    expansions = {**rules["compound_expansions"], **rules["whole_gloss_expansions"]}
    if text in expansions:
        return {"status": "enumerated_glosses", "units": expansions[text],
                "reason": "Explicit analyst segmentation; retain the original compound for review."}
    phrases = rules["phrase_units"]
    if text in phrases:
        return {"status": "single_gloss", "units": [text],
                "reason": "A qualified phrase, not one meaning per word."}
    # Only separate visible lists. Unrecognized sandhied compounds stay unresolved.
    tokens = text.replace(",", " , ").split()
    if "ca" in tokens or "," in tokens:
        units = []
        i = 0
        sorted_phrases = sorted((p.split() for p in phrases), key=len, reverse=True)
        while i < len(tokens):
            if tokens[i] in ("ca", ","):
                i += 1
                continue
            matched = next((p for p in sorted_phrases if tokens[i:i + len(p)] == p), None)
            if matched:
                units.append(" ".join(matched))
                i += len(matched)
                continue
            part = classify(tokens[i], rules)
            if part["status"] == "needs_interpretation":
                return {"status": "needs_interpretation", "units": [],
                        "reason": f"Unresolved list member {tokens[i]}: {part['reason']}"}
            units.extend(part["units"])
            i += 1
        if len(units) < 2 or len(set(units)) != len(units):
            return {"status": "needs_interpretation", "units": [],
                    "reason": "Incomplete list or repeated member; review the intended meanings."}
        return {"status": "enumerated_glosses", "units": units,
                "reason": "Visible enumeration; semantic overlap still belongs to lexical review."}
    if re.fullmatch(r"[A-Za-z]+", text) and text.endswith(("e", "Am", "AM", "O", "i")):
        return {"status": "single_gloss", "units": [text],
                "reason": "One source gloss; no attempt to invent finer senses within it."}
    return {"status": "needs_interpretation", "units": [],
            "reason": "Compound, cross-reference, or phrasing needs an explicit analysis."}


def load_source(path):
    entries, placeholders, seen = [], [], set()
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            code = row["code"]
            if code in seen or not re.fullmatch(r"(?:0[1-9]|10)\.\d{4}", code):
                raise ValueError(f"Invalid or duplicate source code: {code}")
            seen.add(code)
            row = {**row, "source_line": reader.line_num}
            if row["dhatu"] == "-":
                placeholders.append(row)
            elif not row["dhatu"] or not row["artha"].strip():
                raise ValueError(f"Missing citation or meaning: {code}")
            else:
                entries.append(row)
    return entries, placeholders


def identity_groups(entries):
    groups = defaultdict(list)
    for row in entries:
        groups[row["dhatu"]].append(row)
    result = []
    for form, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        glosses = {" ".join(row["artha"].split()) for row in members}
        decision = ("same_gloss_identity_unresolved" if len(glosses) == 1
                    else "different_glosses_preserve_pending_sense_review")
        group_id = "citation-" + hashlib.sha256(form.encode()).hexdigest()[:12]
        for row in members:
            result.append({"group_id": group_id, "citation_slp1": form,
                           "source_code": row["code"], "gana": int(row["code"][:2]),
                           "source_gloss_slp1": row["artha"], "decision": decision,
                           "merged": False})
    return result


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def review_index(review, entries, sources):
    valid_codes = {r["code"] for r in entries}
    by_code = {r["code"]: r for r in entries}
    resolved, opened, aliases = {}, {}, {}
    for category in ("decisions", "open_reviews", "identity_decisions"):
        for item in review[category]:
            if not set(item["codes"]) <= valid_codes:
                raise ValueError(f"Unknown reviewed entry: {item['codes']}")
            for name in item["sources"]:
                if name not in sources:
                    raise ValueError(f"Unarchived review source: {name}")
            if item.get("anchor") and not any(item["anchor"] in source_text(name)
                                              for name in item["sources"]):
                raise ValueError(f"Review anchor not found: {item['id']}")
            if category == "decisions":
                if not item["units"] or len(set(item["units"])) != len(item["units"]):
                    raise ValueError(f"Invalid meaning units: {item['id']}")
                if item.get("completeness") == "partial" and not item.get("remaining"):
                    raise ValueError(f"Partial decision needs an explicit gap: {item['id']}")
                evidence = item.get("unit_evidence", {})
                if evidence and set(evidence) != set(item["units"]):
                    raise ValueError(f"Incomplete per-meaning evidence: {item['id']}")
                for witness in list(evidence.values()) + ([item["cross_reference"]]
                                                          if "cross_reference" in item else []):
                    if witness["source"] not in item["sources"]:
                        raise ValueError(f"Unlisted meaning witness: {item['id']}")
                    if not witness.get("anchor") or witness["anchor"] not in source_text(witness["source"]):
                        raise ValueError(f"Meaning witness not found: {item['id']}")
                if "cross_reference" in item and item["cross_reference"]["code"] not in item["codes"]:
                    raise ValueError(f"Cross-reference entry not reviewed: {item['id']}")
                for code in item["codes"]:
                    if code in resolved or code in opened:
                        raise ValueError(f"Repeated interpretation decision: {code}")
                    resolved[code] = item
            elif category == "open_reviews":
                for code in item["codes"]:
                    if code in resolved or code in opened:
                        raise ValueError(f"Repeated interpretation decision: {code}")
                    opened[code] = item
            else:
                if item["canonical_code"] not in item["codes"]:
                    raise ValueError(f"Canonical entry missing: {item['id']}")
                if len({by_code[code]["dhatu"] for code in item["codes"]}) != 1:
                    raise ValueError(f"Citation changed in reviewed identity group: {item['id']}")
                for code in item["codes"]:
                    if by_code[code]["artha"] != item["meaning"]:
                        raise ValueError(f"Meaning changed in reviewed identity group: {item['id']}")
                    if code in aliases:
                        raise ValueError(f"Overlapping identity decisions: {code}")
                    aliases[code] = item
    return resolved, opened, aliases


def build():
    manifest = verify_sources()
    source_meta = next(s for s in manifest["sources"] if s["filename"] == "dhatupatha.tsv")
    source_path = ARCHIVE / "dhatupatha.tsv"
    entries, placeholders = load_source(source_path)
    rules = json.loads(ANALYSIS.read_text())
    review = json.loads(REVIEW.read_text())
    source_records = {r["filename"]: r for r in manifest["sources"]}
    resolved, opened, aliases = review_index(review, entries, source_records)
    mapping = crosswalk()
    local_by_remote = defaultdict(list)
    for row in mapping:
        if row["selected_code"]:
            local_by_remote[row["selected_code"]].append(row["local_code"])
    identities = identity_groups(entries)
    for item in identities:
        decision = aliases.get(item["source_code"])
        item["review_id"] = decision["id"] if decision else ""
        if decision:
            item["decision"] = "documented_same_word_and_meaning"
            item["merged"] = item["source_code"] != decision["canonical_code"]
    identity_by_code = {r["source_code"]: r for r in identities}
    analysed, assignments = [], []
    for row in entries:
        outcome = classify(row["artha"], rules)
        decision = resolved.get(row["code"])
        pending = opened.get(row["code"])
        if decision:
            status = ("partial_enumeration" if decision.get("completeness") == "partial"
                      else "single_gloss" if len(decision["units"]) == 1 else "enumerated_glosses")
            outcome = {"status": status,
                       "units": decision["units"], "reason": decision["decision"]}
        elif pending:
            outcome = {"status": pending.get("disposition", "needs_interpretation"),
                       "units": [], "reason": pending["decision"]}
        note = decision or pending or {}
        alias = aliases.get(row["code"])
        item = {
            "source_code": row["code"], "gana": int(row["code"][:2]),
            "citation_slp1": row["dhatu"], "source_gloss_slp1": row["artha"],
            "source_gloss_devanagari": lipi.transliterate(
                row["artha"], lipi.Scheme.Slp1, lipi.Scheme.Devanagari),
            "source_line": row["source_line"], "status": outcome["status"],
            "assignment_count": len(outcome["units"]) if outcome["units"] else None,
            "units_slp1": outcome["units"], "reason": outcome["reason"],
            "remaining_meaning_gap": note.get("remaining", ""),
            "interpretation_review_id": note.get("id", "reviewed_but_open" if pending else ""),
            "eligibility_note": note.get("eligibility", ""),
            "review_evidence": [{**source_records[name]} for name in note.get("sources", [])],
            "provisional_word_id": alias["canonical_code"] if alias else row["code"],
            "identity_review": identity_by_code.get(row["code"], {}).get(
                "decision", "not_flagged_by_exact_citation_check"),
            "candidate_local_codes": local_by_remote[row["code"]],
            "source_url": source_meta["url"], "source_sha256": source_meta["sha256"],
        }
        analysed.append(item)
        for unit in outcome["units"]:
            # IDs follow the source entry and meaning, not the surface word spelling.
            sense_id = "meaning-" + hashlib.sha256(unit.encode()).hexdigest()[:12]
            witness = note.get("unit_evidence", {}).get(unit, {})
            cross_reference = note.get("cross_reference", {})
            if cross_reference.get("code") != row["code"]:
                cross_reference = {}
            assignments.append({"source_code": row["code"], "meaning_id": sense_id,
                "provisional_word_id": item["provisional_word_id"],
                "gana": item["gana"], "citation_slp1": row["dhatu"],
                "meaning_slp1": unit, "meaning_display": display(unit),
                "status": "source_assignment_pending_lexical_review",
                "source_gloss_slp1": row["artha"], "source_line": row["source_line"],
                "source_url": source_meta["url"],
                "meaning_evidence": json.dumps({**source_records[witness["source"]], **witness},
                                               ensure_ascii=False) if witness else "",
                "cross_reference_evidence": json.dumps(
                    {**source_records[cross_reference["source"]], **cross_reference},
                    ensure_ascii=False) if cross_reference else "",
                "entry_completeness": outcome["status"]})
    identity_batch = apply_review(analysed, assignments, identities, source_records)
    summary = []
    for gana in range(1, 11):
        group = [r for r in analysed if r["gana"] == gana]
        counts = Counter(r["status"] for r in group)
        summary.append({"gana": gana, "source_entries": len(group),
            "single_gloss_entries": counts["single_gloss"],
            "enumerated_entries": counts["enumerated_glosses"],
            "partial_entries": counts["partial_enumeration"],
            "unenumerated_entries": counts["unenumerated"],
            "unresolved_entries": counts["needs_interpretation"],
            "source_meaning_assignments": sum(r["assignment_count"] or 0 for r in group),
            "repeated_citation_entries": sum(r["source_code"] in identity_by_code for r in group)})

    by_remote_code = {r["source_code"]: r for r in analysed}
    comparisons = []
    for row in mapping:
        same_code = by_remote_code.get(row["local_code"])
        candidate = by_remote_code.get(row["selected_code"])
        comparisons.append({**row,
            "same_code_source_citation": same_code["citation_slp1"] if same_code else "",
            "same_code_source_gloss": same_code["source_gloss_slp1"] if same_code else "",
            "candidate_assignment_count": candidate["assignment_count"] if candidate else None,
            "candidate_meaning_status": candidate["status"] if candidate else "no_selected_candidate",
            "accepted_lexical_transfer": False})
    report = {
        "counting_unit": "Source-entry/explicit-gloss assignments before lexical identity review",
        "vocabulary_total": None, "local_inventory_meaning_total": None,
        "source_entries": len(entries), "placeholder_rows_excluded": len(placeholders),
        "local_entries": len(mapping), "unique_glosses": len({r["artha"] for r in entries}),
        "by_gana": summary,
        "source_meaning_assignments": len(assignments),
        "unresolved_entries": sum(r["status"] in ("needs_interpretation", "partial_enumeration", "unenumerated")
                                  for r in analysed),
        "partial_entries": sum(r["status"] == "partial_enumeration" for r in analysed),
        "unenumerated_entries": sum(r["status"] == "unenumerated" for r in analysed),
        "repeated_citation_groups": len({r["group_id"] for r in identities}),
        "repeated_citation_entries": len(identities),
        "documented_identity_groups": len(review["identity_decisions"]) + identity_batch["merge_groups"],
        "lexical_merges": len(assignments) - identity_batch["after"],
        "assignments_after_initial_merges": identity_batch["before"],
        "assignments_after_documented_merges": identity_batch["after"],
        "identity_batch": {k: v for k, v in identity_batch.items() if k != "groups"},
        "interpretations_resolved_this_pass": sum(r.get("completeness") != "partial" for r in resolved.values()),
        "interpretations_reviewed_but_open": len(opened) + sum(r.get("completeness") == "partial" for r in resolved.values()),
        "crosswalk_statuses": dict(Counter(r["status"] for r in mapping)),
        "shared_target_rows": sum(r["shared_selected_code"] for r in mapping),
        "inputs": {str(p.relative_to(ROOT)): sha(p) for p in (
            source_path, LOCAL_DATA, ANALYSIS, REVIEW, ARCHIVE / "manifest.json", Path(__file__),
            HERE / "read_dhatu_concordance.py", HERE / "run_pilot.py", IDENTITY_REVIEW,
            HERE / "review_base_identities.py")},
        "source": source_meta, "entries": analysed,
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "base_meanings.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    export = [{**r, "units_slp1": "; ".join(r["units_slp1"]),
               "review_evidence": json.dumps(r["review_evidence"], ensure_ascii=False),
               "candidate_local_codes": ";".join(r["candidate_local_codes"])} for r in analysed]
    write_csv(RESULTS / "base_meanings.csv", export, export[0].keys())
    write_csv(RESULTS / "base_meaning_assignments.csv", assignments, assignments[0].keys())
    write_csv(RESULTS / "base_meanings_by_gana.csv", summary, summary[0].keys())
    write_csv(RESULTS / "base_identity_review.csv", identities, identities[0].keys())
    write_csv(RESULTS / "base_local_reconciliation.csv", comparisons, comparisons[0].keys())
    write_csv(RESULTS / "base_placeholders.csv", placeholders, placeholders[0].keys())
    write_report(report, identities)
    write_review_report(review, report, source_records)
    write_identity_report({**identity_batch, "inputs": report["inputs"]})
    print(json.dumps({k: v for k, v in report.items() if k not in ("entries", "inputs", "source")}, indent=2))
    return report


def write_report(report, identities):
    lines = ["# Base Meaning Audit", "", "## First Result", "",
        f"The meaning-bearing source contains **{report['source_entries']:,} entries**. "
        f"This pass extracts **{report['source_meaning_assignments']:,} provisional source meaning assignments** "
        f"including **{report['partial_entries']} partially enumerated entries**. "
        f"Another **{report['unenumerated_entries']} entries** have no finite meaning list and remain outside the subtotal.", "",
        "These are assignments of meanings to source entries, not a finished vocabulary count. "
        "A list may use overlapping descriptions, and two entries may represent the same word and meaning. "
        "Both must be settled before these assignments become the base-word total. "
        "Unenumerated entries have a blank count, not zero. Partial entries contribute only their admitted meanings; "
        "their remaining gaps are recorded explicitly.", "",
        "The book's older file has 2,168 entries and no meaning column. "
        "Its counts remain separate: this pass does not silently substitute a different inventory. "
        "No prefixes, derived bases, conjugations, or declensions have been added.", "",
        f"The [commentary review](meaning_review.md) resolved {report['interpretations_resolved_this_pass']} "
        "of the initial 38 interpretation gaps. "
        f"After {report['lexical_merges']} documented duplicate reductions, "
        f"**{report['assignments_after_documented_merges']:,} provisional assignments** remain. "
        "The [identity reviews](identity_review.md) record the individual reductions and their sources. "
        "That subtotal still awaits the wider lexical-identity review.", "",
        "## By Gana", "",
        "| Gana | Source entries | One gloss | Enumerated | Partial | Unenumerated | Needs interpretation | Assignments |",
        "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in report["by_gana"]:
        lines.append(f"| {r['gana']}. {display(GANA_NAMES[r['gana']])} | {r['source_entries']} | "
                     f"{r['single_gloss_entries']} | {r['enumerated_entries']} | "
                     f"{r['partial_entries']} | {r['unenumerated_entries']} | "
                     f"{r['unresolved_entries']} | {r['source_meaning_assignments']} |")
    lines += ["", "The status columns count source entries; the last counts their extracted meanings. "
        "An entry listing three meanings contributes one to 'Enumerated meanings' and three to the last column.",
        "", "## What the Extraction Does", "",
        "1. Keeps each source entry's identifier, citation form, original gloss, source line, URL, and checksum.",
        "2. Keeps qualified phrases together. For example, vyaktayam vaci is one description, not two meanings.",
        "3. Separates visible lists and explicitly annotated compounds. It does not guess the segmentation of every compound.",
        "4. Counts sourced members of partial lists while retaining the uncounted remainder. Leaves unenumerated entries blank.",
        "5. Counts neither English synonyms nor spellings. The assignment key is the source entry plus its meaning identifier.",
        "", "The segmentations are analysis annotations. The commentary review settles the selected entries listed "
        "in its decision ledger; the rest have not received a complete independent Sanskrit review. "
        "A single listed gloss is provisionally one assignment; it may conceal finer senses that this source does not state. "
        "The complete CSV preserves the Sanskrit wording rather than introducing unverified English translations.",
        "", "## Examples", "",
        "| Source entry | Original meaning description | Extracted meanings |",
        "|---|---|---|"]
    by_code = {r["source_code"]: r for r in report["entries"]}
    for code in ("01.1074", "02.0051", "06.0022", "01.0978", "01.1165", "01.0951"):
        r = by_code[code]
        units = "; ".join(display(s) for s in r["units_slp1"]) or "Unresolved; no invented count"
        lines.append(f"| {code}: `{r['citation_slp1']}` | {display(r['source_gloss_slp1'])} | {units} |")
    lines += ["", "The two pa entries retain drinking and protecting separately. "
        "The rc entry retains praise and shining separately. "
        "The hula entry lists movement, harming, and covering. "
        "The van entry says multiple meanings without supplying an enumeration.",
        "", "## Identity Review", "",
        f"The exact-citation check flags **{report['repeated_citation_groups']} groups**, "
        f"covering **{report['repeated_citation_entries']} source entries**. "
        "The ledger distinguishes groups with repeated glosses from groups with different descriptions. "
        f"The commentary review establishes {report['documented_identity_groups']} same-identity groups; "
        "their repeated assignments are consolidated without deleting either source record. "
        "The remaining groups have not been automatically merged. A different citation form can also represent the same word; "
        "this exact-form check is a first diagnostic, not the complete identity review.", "",
        "In the old-to-new comparison, 1,773 entries match in code and citation, "
        "41 have a unique same-class citation candidate elsewhere, "
        "four have several candidates, and 350 have no exact candidate. "
        "Fifty local entries share a selected target with another local entry. "
        "The reconciliation table now shows both the proposed target and the newer source's entry at the old code. "
        "Candidate matches remain candidates; no ambiguous meanings have been copied into the old inventory.",
        "", "## Files", "",
        "- [Full source-entry ledger](base_meanings.csv)",
        "- [One row per extracted meaning](base_meaning_assignments.csv)",
        "- [Counts by gana](base_meanings_by_gana.csv)",
        "- [Repeated-citation review](base_identity_review.csv)",
        "- [Old-to-new reconciliation](base_local_reconciliation.csv)",
        "- [Excluded placeholder rows](base_placeholders.csv)",
        "- [Analysis rules and explicit segmentations](../meaning_analysis.json)",
        "- [Commentary decisions and source links](meaning_review.md)",
        "", "## Source", "",
        f"[Pinned Vidyut Dhatupatha]({report['source']['url']}), "
        "archived locally with its source manifest. This is a digital transcription, not a new collation of printed editions.",
        f"SHA-256: `{report['source']['sha256']}`.",
        "", "## Next Work", "",
        "Continue lexical-identity review, carrying the specific meaning gaps below alongside it. "
        "Reconcile the older inventory before assigning it a meaning total. "
        "After that, apply named derivational operations to admitted base meanings. "
        "Conjugation and declension remain a later, separate operation.",
        "", "## Interpretation Queue", "",
        "Repeated descriptions are grouped here; the CSV retains every affected source entry.", "",
        "| Source entries | Original gloss | What needs checking |", "|---|---|---|"]
    queue = defaultdict(list)
    for r in report["entries"]:
        if r["status"] in ("needs_interpretation", "partial_enumeration", "unenumerated"):
            queue[(r["source_gloss_slp1"], r["remaining_meaning_gap"] or r["reason"])].append(r["source_code"])
    for (gloss, reason), codes in queue.items():
        lines.append(f"| {', '.join(codes)} | {display(gloss)} | {reason} |")
    (RESULTS / "base_meanings.md").write_text("\n".join(lines) + "\n")


def write_review_report(review, report, sources):
    entries = {r["source_code"]: r for r in report["entries"]}

    def names(item):
        return "; ".join(f"{code}: {display(entries[code]['citation_slp1'])}" for code in item["codes"])

    def links(item):
        return ", ".join(f"[{name.removeprefix('dhatu-').removesuffix('.html')}]({sources[name]['url']})"
                         for name in item["sources"])

    lines = ["# Base Meaning Review: Commentary Decisions", "", f"Date: {review['date']}.", "",
        "## Result", "",
        f"Reviewed all {review['baseline']['unresolved_entries']} entries left open by the first extraction. "
        f"Resolved the source-gloss interpretation for {report['interpretations_resolved_this_pass']}; "
        f"{report['partial_entries']} have a sourced partial count and "
        f"{report['unenumerated_entries']} have no finite enumeration. "
        "This does not complete the separate review of all lexical identities.", "",
        f"Source assignments: **{review['baseline']['source_meaning_assignments']:,} → "
        f"{report['source_meaning_assignments']:,}**. The two initial repeated-entry groups reduce the latter "
        f"to **{report['assignments_after_initial_merges']:,} provisional assignments**. "
        f"The subsequent [identity batch](identity_review.md) reduces that to "
        f"**{report['assignments_after_documented_merges']:,}**. "
        "No prefixes or inflections have been multiplied into these numbers.", "",
        "## Latest Pass: Remaining Ten", "",
        review.get("variant_policy", ""), "",
        f"Before this pass: **{review['previous_pass']['source_meaning_assignments']:,} source assignments**, "
        f"**{review['previous_pass']['adjusted_assignments']:,} after documented repetitions**; ten entries had no count. "
        f"This pass adds **{report['source_meaning_assignments'] - review['previous_pass']['source_meaning_assignments']} "
        "documented assignments**. Five entries now have interpreted lists, three contribute partial lists, "
        "and two remain unenumerated. No additional identities were merged during that meaning pass; "
        "the subsequent identity review is reported separately.", "",
        "| Entry | Before | Now | Status / remaining work |", "|---|---|---:|---|"]
    for item in review["decisions"]:
        if "unit_evidence" in item:
            lines.append(f"| {names(item)} | No count | {len(item['units'])} per entry | "
                         f"{item.get('remaining', 'Listed readings interpreted; broader lexical review remains.')} |")
    for item in review["open_reviews"]:
        lines.append(f"| {names(item)} | No count | Not enumerated | {item['decision']} |")
    lines += ["", "## Meaning-Level Evidence", "",
        "Shared members count once within an entry. Each additional member retains the reading that supplies it. "
        "For vevi, the recorded cross-reference carries vi's meanings to a separate input; it does not merge their identities.", "",
        "| Entries | Admitted meaning | Reading | Source / locator |", "|---|---|---|---|"]
    for item in review["decisions"]:
        for unit, witness in item.get("unit_evidence", {}).items():
            lines.append(f"| {', '.join(item['codes'])} | {display(unit)} | {witness['reading']} | "
                         f"[{witness['source']}]({sources[witness['source']]['url']}): {witness['anchor']} |")
    lines += ["", "## Interpretation Decisions", "",
        "The first extraction left each of these entries without a count. The new count follows the "
        "source-specific interpretation described here, not a mechanical split of every compound.", "",
        "| Entry | Assignments per entry | Decision | Evidence |", "|---|---:|---|---|"]
    for item in review["decisions"]:
        lines.append(f"| {names(item)} | {len(item['units'])} | {item['decision']} | {links(item)} |")
    lines += ["", "## Documented Repetitions", "",
        "The source-entry ledger retains both records. Their provisional word identity is shared, "
        "so the same meaning contributes only once to the adjusted subtotal.", "",
        "| Entries | Decision | Evidence |", "|---|---|---|"]
    for item in review["identity_decisions"]:
        lines.append(f"| {names(item)} | {item['decision']} | {links(item)} |")
    lines += ["", "## Partial Lists", "", "| Entries | Uncounted remainder | Evidence |", "|---|---|---|"]
    for item in review["decisions"]:
        if item.get("completeness") == "partial":
            lines.append(f"| {names(item)} | {item['remaining']} | {links(item)} |")
    lines += ["", "## Unenumerated Entries", "", "| Entries | Finding | Evidence |", "|---|---|---|"]
    for item in review["open_reviews"]:
        lines.append(f"| {names(item)} | {item['decision']} | {links(item)} |")
    lines += ["", "## Conditions for the Next Stage", ""]
    for item in review["decisions"] + review["open_reviews"]:
        if item.get("eligibility"):
            lines.append(f"- **{', '.join(item['codes'])}:** {item['eligibility']} {links(item)}.")
    lines += ["", "## Evidence Record", "",
        "The University of Hyderabad concordance provides transcriptions of Madhaviya Dhatvritti, "
        "Kshiratarangini, and Dhatupradipa. Its "
        f"[edition statement]({sources['dhatu-concordance-about.html']['url']}) identifies the editions. "
        "The review uses the actual commentary passages, not just the concordance's summary cells. "
        "Downloaded passages retain their original wording, including apparent transcription errors.", "",
        "Every decision records source filenames and a locator phrase in "
        "[meaning_review.json](../meaning_review.json). The build validates the locator against the "
        "archived page and checks source hashes against the manifest. The full ledger links those "
        "sources to the affected entries. No manuscript or published endnote was changed.", "",
        "## Next", "",
        "Use the [identity review](identity_review.md) for the current batch results and remaining checks. "
        "Carry the three partial-list gaps and two unenumerated entries separately; do not invent a remainder. "
        "Review the recorded domain, prefix, and nominal-input "
        "conditions before expanding derivations."]
    (RESULTS / "meaning_review.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    build()

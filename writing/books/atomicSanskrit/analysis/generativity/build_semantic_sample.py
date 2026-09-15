#!/usr/bin/env python3
"""Build a reviewed-by-source, selected meaning inventory, not a vocabulary total."""

from collections import Counter
import csv
import importlib.metadata
import json
from pathlib import Path

from vidyut import lipi
from vidyut.prakriya import Data, Lakara, Pada, Prayoga, Purusha, Vacana, Vyakarana

from run_pilot import ARCHIVE, HERE, RESULTS, ROOT, build_argument, compare, crosswalk, sha, verify_sources

EVIDENCE = {
    "source_meaning": "Base meaning listed",
    "source_example": "Source example",
    "rule_application": "Rule applied to this base",
}


def semantic_counts(rows):
    identities = {}
    for row in rows:
        key = (row["word_id"], row["sense_id"])
        meaning = (row["stage"], row["meaning"])
        if key in identities and identities[key] != meaning:
            raise ValueError(f"Conflicting annotation for {key}")
        identities[key] = meaning
    return dict(Counter(stage for stage, meaning in identities.values()))


def display(text):
    dev = lipi.transliterate(text, lipi.Scheme.Slp1, lipi.Scheme.Devanagari)
    iast = lipi.transliterate(text, lipi.Scheme.Slp1, lipi.Scheme.Iast)
    return f"{dev} (*{iast}*)"


def operation_display(item):
    request = item["request"]
    if request.get("sanadi"):
        names = {"Ric": "Causative", "san": "Desire", "yaN": "Intensive"}
        return names[request["sanadi"]] + ": " + display(request["sanadi"])
    if request.get("nama_sanadi"):
        return "Verb from noun: " + display(request["nama_sanadi"])
    if item["word_id"] == "prakrtya":
        return display("pra") + "; " + display("ktvA") + " replaced by " + display("lyap")
    suffix = request.get("krt") or request.get("taddhita")
    if suffix:
        return item["operation"].split(":")[0] + ": " + display(suffix)
    if request.get("prefixes"):
        return "Prefix " + display("A")
    return item["operation"]


def build_records(sample, entries, grammar):
    records = []
    for item in sample["entries"]:
        argument = build_argument(item["request"], entries)
        paths = grammar.derive(argument)
        actual = sorted({path.text for path in paths})
        checked = compare(item["expected"], actual)
        if not checked["matches_expected"]:
            raise ValueError(f"Output mismatch for {item['word_id']}/{item['sense_id']}: {actual}")
        if item.get("illustration"):
            example = Pada.Tinanta(argument, Prayoga.Kartari, Lakara.Lat,
                                  Purusha.Prathama, Vacana.Eka)
            examples = sorted({p.text for p in grammar.derive(example)})
            if item["illustration"] not in examples:
                raise ValueError(f"Illustration mismatch: {item['illustration']} not in {examples}")
        code = item["request"].get("dhatu")
        source = entries[code] if code else None
        records.append({
            **item, "actual": actual, "display": display(item.get("illustration", actual[0])),
            "source_entry": ({"code": source.code, "citation": source.dhatu.aupadeshika,
                "meaning_slp1": source.artha} if source else None),
            "form_check_passed": True,
            "semantic_condition_selected_by_engine": False,
            "counting_status": "author_accepted_selected_annotation_not_full_lexical_verification",
            "paths": [{"text": p.text, "rules": [
                {"source": str(step.source), "code": step.code} for step in p.history
            ]} for p in paths],
        })
    return records


def resolve_evidence(item, sources):
    names = item.get("source_pages", [f"rule-{rule}.html" for rule in item["rules"]])
    if item["request"].get("dhatu"):
        names = ["dhatupatha.tsv", *names]
    result = []
    for name in names:
        if name not in sources:
            raise ValueError(f"Unarchived source {name}")
        result.append({"filename": name, "url": sources[name]["url"],
                       "sha256": sources[name]["sha256"]})
    return result


def main():
    if importlib.metadata.version("vidyut") != "0.4.0":
        raise ValueError("The semantic sample requires vidyut 0.4.0")
    manifest = verify_sources()
    source_path = HERE / "semantic_sample.json"
    sample = json.loads(source_path.read_text())
    sources = {r["filename"]: r for r in manifest["sources"]}
    entries = {e.code: e for e in Data(str(ARCHIVE)).load_dhatu_entries()}
    grammar = Vyakarana(is_chandasi=False, use_svaras=False, log_steps=True, nlp_mode=False)
    records = build_records(sample, entries, grammar)
    for record in records:
        record["evidence_sources"] = resolve_evidence(record, sources)
    unresolved = sample["unresolved"]
    mappings = {row["local_code"]: row for row in crosswalk()}
    for issue in unresolved:
        for code in issue.get("local_codes", []):
            if mappings[code]["selected_code"] != issue["candidate_code"]:
                raise ValueError(f"Crosswalk changed for reviewed example {code}")
        if "dhatu" in issue and entries[issue["dhatu"]].artha != issue["source_artha"]:
            raise ValueError(f"Source gloss changed for {issue['id']}")
    counts = semantic_counts(records)
    report = {
        "scope": sample["scope"], "unit": "word identity plus specified lexical meaning",
        "selected_entries_by_stage": counts, "sanskrit_vocabulary_total": None,
        "author_review_pending": False,
        "author_review_date": "2026-09-12",
        "inputs": {str(p.relative_to(ROOT)): sha(p) for p in (
            source_path, Path(__file__), HERE / "run_pilot.py", ARCHIVE / "manifest.json")},
        "entries": records, "unresolved": unresolved,
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "semantic_sample.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    with (RESULTS / "semantic_sample.csv").open("w", newline="") as handle:
        columns = ["word_id", "sense_id", "stage", "base", "operation", "result_slp1", "meaning", "evidence", "source_locator"]
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for record in records:
            writer.writerow({**{key: record[key] for key in columns if key != "result_slp1"},
                             "result_slp1": ";".join(record["actual"])})
    lines = ["# Words and Meanings: First Review Table", "",
        "This table counts a word with a specified meaning, not a unique spelling. It is a selected sample for review, not a new total for Sanskrit.", "",
        "For derived verbs, familiar present-tense forms illustrate the meaning. They do not add another entry or a person-number multiplier. Nominals are shown as bases, before case endings.", "",
        "**Evidence:** 'Base meaning listed' refers to the source inventory; 'Source example' identifies a traditional example, sometimes in an inflected form; 'Rule applied' means that the grammatical operation is documented and applied here to the selected base. Software checks the output form; the semantic annotation remains separate.", ""]
    for stage, title in (("verbal", "Verbal Entries"), ("nominal", "Nominal Entries"), ("indeclinable", "Indeclinable Entries")):
        lines += [f"## {title}", "", "| Base and operation | Result | Meaning | Evidence |", "|---|---|---|---|"]
        for r in records:
            if r["stage"] != stage:
                continue
            n = records.index(r) + 1
            lines.append(f"| {display(r['base'])}; {operation_display(r)} | {r['display']} | {r['meaning']} | [{EVIDENCE[r['evidence']]}](#source-{n}) |")
        lines.append("")
    lines += ["## What Stays Separate", "",
        f"- The two {display('pA')} entries distinguish drinking from protecting even before inflection.",
        f"- One {display('fc')} source entry explicitly lists praise and shine. These remain two readings of the same form.",
        f"- {display('karaRa')} as an action and as an instrument remain separate meanings. {display('Asana')} as sitting and as a seat are likewise listed separately, with their evidence levels shown.",
        f"- The {display('yaN')} rule distinguishes repetition and intensity. The exact {display('pac')} example illustrates repetition; the intensive reading is retained as a rule application for review.",
        f"- {display('putrIya')} and {display('putrakAmya')} are different formations with a similar meaning. {display('gotva')} and {display('gotA')} likewise remain separate formations. We are not counting abstract concepts alone.",
        "- Do/make and cook/chef are not automatically split into extra entries just because English supplies two glosses.", "",
        "## Items Left Open", ""]
    for issue in unresolved:
        lines += [f"### {issue['id']}", "", issue["issue"], "", issue["action"], ""]
    lines += ["## Sample Size", "", "These are selected annotations, not a minimum vocabulary estimate:", ""]
    lines += [f"- {stage}: {count}" for stage, count in counts.items()]
    lines += ["", "Inflection is not included in these subtotals. No Sanskrit-wide total is computed.", "", "## Source Details", ""]
    for n, r in enumerate(records, 1):
        lines += [f'<a id="source-{n}"></a>', f"### {n}. {r['word_id']} / {r['sense_id']}", "",
            f"{r['source_locator']}.", ""]
        if r["source_entry"]:
            source = r["source_entry"]
            lines += [f"Source {source['code']}, original SLP1 citation `{source['citation']}`; meaning: {display(source['meaning_slp1'])}.", ""]
        lines += [f"- [{s['filename']}]({s['url']})" for s in r["evidence_sources"]]
        lines.append("")
    (RESULTS / "words_and_meanings.md").write_text("\n".join(lines) + "\n")
    print(f"Checked {len(records)} annotated entries; {len(unresolved)} unresolved items retained.")
    print(json.dumps(counts))
    print(f"Review: {RESULTS.relative_to(ROOT) / 'words_and_meanings.md'}")


if __name__ == "__main__":
    main()

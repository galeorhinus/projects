#!/usr/bin/env python3
"""Run the bounded derivation pilot; never extrapolate it to a word total."""

from collections import Counter, defaultdict
import csv
import hashlib
import importlib.metadata
import inspect
import json
from pathlib import Path

from vidyut import lipi
from vidyut.prakriya import (
    Data, Dhatu, DhatuPada, Krt, Lakara, Linga, Pada, Pratipadika,
    Prayoga, Purusha, Sanadi, Taddhita, Vacana, Vibhakti, Vyakarana,
)

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
RESULTS = HERE / "results"
LOCAL_DATA = ROOT / "analysis/dhatupatha/data/dhatupatha.csv"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sources():
    manifest = json.loads((ARCHIVE / "manifest.json").read_text())
    for item in manifest["sources"]:
        if sha(ARCHIVE / item["filename"]) != item["sha256"]:
            raise ValueError(f"Source checksum mismatch: {item['filename']}")
    return manifest


def crosswalk():
    with (ARCHIVE / "dhatupatha.tsv").open() as handle:
        remote = list(csv.DictReader(handle, delimiter="\t"))
    by_code = {row["code"]: row for row in remote}
    by_form = defaultdict(list)
    for row in remote:
        by_form[(int(row["code"].split(".")[0]), row["dhatu"])].append(row)
    rows = []
    with LOCAL_DATA.open() as handle:
        for gana, position, form in csv.reader(handle):
            if gana.lstrip().startswith("#"):
                continue
            code = f"{int(gana):02}.{int(position):04}"
            same_code = by_code.get(code)
            candidates = by_form[(int(gana), form)]
            if same_code and same_code["dhatu"] == form:
                status, selected = "same_code_and_citation", same_code
            elif len(candidates) == 1:
                status, selected = "unique_same_gana_citation_candidate", candidates[0]
            elif candidates:
                status, selected = "ambiguous_same_gana_citation", None
            else:
                status, selected = "no_exact_same_gana_citation", None
            rows.append({
                "local_code": code, "local_citation": form, "status": status,
                "candidate_codes": ";".join(r["code"] for r in candidates),
                "selected_code": selected["code"] if selected else "",
                "selected_meaning_slp1": selected["artha"] if selected else "",
            })
    # Even a unique spelling candidate is not a verified semantic identity.
    uses = Counter(row["selected_code"] for row in rows if row["selected_code"])
    for row in rows:
        row["shared_selected_code"] = bool(row["selected_code"] and uses[row["selected_code"]] > 1)
    return rows


def build_argument(case, entries):
    if "dhatu" in case:
        dhatu = entries[case["dhatu"]].dhatu
    elif "nama_sanadi" in case:
        dhatu = Dhatu.nama(Pratipadika.basic(case["nominal"]),
                           nama_sanadi=getattr(Sanadi, case["nama_sanadi"]))
    else:
        dhatu = None
    if case.get("prefixes"):
        dhatu = dhatu.with_prefixes(case["prefixes"])
    if case.get("sanadi"):
        dhatu = dhatu.with_sanadi([getattr(Sanadi, case["sanadi"])])
    if case.get("tinanta"):
        options = {"dhatu_pada": getattr(DhatuPada, case["pada"])} if case.get("pada") else {}
        return Pada.Tinanta(dhatu, Prayoga.Kartari, Lakara.Lat,
                            Purusha.Prathama, Vacana.Eka, **options)
    if case.get("krt"):
        return Pratipadika.krdanta(dhatu, getattr(Krt, case["krt"]))
    if case.get("taddhita"):
        nominal = (Pratipadika.nyap(case["nominal"]) if case.get("nyap")
                   else Pratipadika.basic(case["nominal"]))
        return Pratipadika.taddhitanta(nominal,
                                      getattr(Taddhita, case["taddhita"]))
    return dhatu


def compare(expected, actual):
    return {
        "matches_expected": set(expected) == set(actual),
        "missing": sorted(set(expected) - set(actual)),
        "unexpected": sorted(set(actual) - set(expected)),
    }


def devanagari(text):
    return lipi.transliterate(text, lipi.Scheme.Slp1, lipi.Scheme.Devanagari)


def run_cases(cases, entries, grammar):
    results = []
    for case in cases:
        outputs = grammar.derive(build_argument(case, entries))
        actual = sorted({p.text for p in outputs})
        paths = [{"text": p.text, "steps": [
            {"source": str(s.source), "rule": s.code,
             "terms": list(s.result)} for s in p.history
        ]} for p in outputs]
        results.append({
            **case, "actual": actual, "actual_devanagari": [devanagari(s) for s in actual],
            **compare(case["expected"], actual), "derivation_paths": paths,
            "source_entry": ({"code": entries[case["dhatu"]].code,
                "aupadeshika": entries[case["dhatu"]].dhatu.aupadeshika,
                "gana": str(entries[case["dhatu"]].dhatu.gana),
                "artha_slp1": entries[case["dhatu"]].artha} if "dhatu" in case else None),
            "rule_references": [f"https://sanskritdocuments.org/learning_tools/"
                f"ashtadhyayi/vyakhya/{rule.split('.')[0]}/{rule}.htm" for rule in case["rules"]],
            "evidence_status": "pilot_expectation_check_not_full_semantic_validation",
        })
    return results


def inflection_sample(entries, grammar):
    groups = []
    pacaka = Pratipadika.krdanta(entries["01.1151"].dhatu, Krt.Rvul)
    for kind in ("bhu_present_parasmai", "pacaka_masculine"):
        cells = []
        features = Purusha.choices() if kind.startswith("bhu") else Vibhakti.choices()
        for feature in features:
            for number in Vacana.choices():
                if kind.startswith("bhu"):
                    arg = Pada.Tinanta(entries["01.0001"].dhatu, Prayoga.Kartari,
                        Lakara.Lat, feature, number, dhatu_pada=DhatuPada.Parasmaipada)
                else:
                    arg = Pada.Subanta(pacaka, Linga.Pum, feature, number)
                forms = sorted({p.text for p in grammar.derive(arg)})
                cells.append({"feature": str(feature), "number": str(number), "forms": forms})
        groups.append({"id": kind, "cells": cells, "requested_cells": len(cells),
            "filled_cells": sum(bool(c["forms"]) for c in cells),
            "distinct_spellings": len({s for c in cells for s in c["forms"]})})
    return groups


def main():
    version = importlib.metadata.version("vidyut")
    if version != "0.4.0":
        raise ValueError(f"Pilot requires vidyut 0.4.0, found {version}")
    manifest = verify_sources()
    with (ARCHIVE / "sutrapatha.tsv").open() as handle:
        rule_texts = {row["code"]: row["text"] for row in csv.DictReader(handle, delimiter="\t")}
    entries = {e.code: e for e in Data(str(ARCHIVE)).load_dhatu_entries()}
    grammar = Vyakarana(log_steps=True, is_chandasi=False, use_svaras=False, nlp_mode=False)
    cases = json.loads((HERE / "pilot_cases.json").read_text())
    if len({c["id"] for c in cases}) != len(cases):
        raise ValueError("Duplicate pilot case IDs")
    results = run_cases(cases, entries, grammar)
    for result in results:
        result["principal_rules_slp1"] = {code: rule_texts[code] for code in result["rules"]}
    inflections = inflection_sample(entries, grammar)
    mapping = crosswalk()
    RESULTS.mkdir(exist_ok=True)
    with (RESULTS / "source_crosswalk.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=mapping[0].keys())
        writer.writeheader()
        writer.writerows(mapping)
    report = {
        "engine_version": version, "generator_source_commit": manifest["generator_commit"],
        "inputs": {str(p.relative_to(ROOT)): sha(p) for p in (
            LOCAL_DATA, ARCHIVE / "dhatupatha.tsv", ARCHIVE / "sutrapatha.tsv",
            ARCHIVE / "manifest.json", HERE / "pilot_cases.json",
            HERE / "operations.csv", Path(__file__))},
        "engine_signature_taddhita": str(inspect.signature(Pratipadika.taddhitanta)),
        "engine_signature_krt": str(inspect.signature(Pratipadika.krdanta)),
        "engine_data_entries": len(entries), "local_entries": len(mapping),
        "crosswalk_statuses": dict(Counter(r["status"] for r in mapping)),
        "shared_target_rows": sum(r["shared_selected_code"] for r in mapping),
        "pilot_cases": len(results), "matches": sum(r["matches_expected"] for r in results),
        "cases": results, "inflection_samples": inflections,
        "counting_unit": "Meaning-bearing lexical entries first; grammatical cells separately.",
        "semantic_word_count": None,
        "spelling_counts_are_diagnostics_only": True,
        "limits": [
            "Coincident spellings do not collapse distinct lexical meanings or grammatical cells.",
            "Expected outputs check selected examples; no universal word count follows.",
            "Python 0.4.0 krt/taddhita entry points do not expose an artha argument.",
            "Zero output is not a proof of grammatical prohibition.",
            "Crosswalk candidates require identity review before meaning enrichment.",
        ],
    }
    (RESULTS / "pilot.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Generativity Pilot Results", "", "Generated by `analysis/generativity/run_pilot.py`.",
        "", "This is an example and software-coverage audit, not a Sanskrit word count.", "",
        f"Vidyut {version}: {report['matches']}/{len(results)} cases match the declared expectations.", "",
        "## Formations", "", "| Case | Stage | Output | Expectation matched |",
        "|---|---|---|---|"]
    for r in results:
        forms = "; ".join(r["actual_devanagari"]) or "No output"
        lines.append(f"| {r['id']} | {r['stage']} | {forms} | {r['matches_expected']} |")
    lines += ["", "## Inflection Separately", "",
              "Count all applicable grammatical cells. Repeated spellings do not merge their functions.",
              "Spelling totals below are diagnostics, not vocabulary counts; no semantic word total has been computed.", "",
              "| Sample | Requested cells | Filled cells | Spellings (diagnostic only) |",
              "|---|---:|---:|---:|"]
    for group in inflections:
        lines.append(f"| {group['id']} | {group['requested_cells']} | {group['filled_cells']} | {group['distinct_spellings']} |")
    lines += ["", "## Source Crosswalk", "", "Candidate matching preserves source IDs; it does not resolve semantic identity.", ""]
    lines += [f"- {key}: {value}" for key, value in report["crosswalk_statuses"].items()]
    lines += [f"- Rows sharing a selected target: {report['shared_target_rows']}", "", "## Limits", ""]
    lines += [f"- {limit}" for limit in report["limits"]]
    (RESULTS / "pilot.md").write_text("\n".join(lines) + "\n")
    print(f"Pilot: {report['matches']}/{len(results)} expectation checks matched")
    for r in results:
        if not r["matches_expected"]:
            print(r["id"], "expected", r["expected"], "actual", r["actual"])
    print(json.dumps(report["crosswalk_statuses"], indent=2))
    print(f"Report: {RESULTS.relative_to(ROOT) / 'pilot.md'}")


if __name__ == "__main__":
    main()

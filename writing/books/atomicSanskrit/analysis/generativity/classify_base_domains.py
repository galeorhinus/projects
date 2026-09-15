#!/usr/bin/env python3
"""Audit the domain evidence attached to every admitted base meaning."""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
import html
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
ASSIGNMENTS = RESULTS / "current_base_assignments.csv"
RESTRICTIONS = HERE / "vaidika_base_restrictions.json"
DOMAIN_MARKER = re.compile(r"छान्दस|छान्दसाः|छन्दसि|वेदे(?:षु)?|वैदिक")
FILE_REF = re.compile(r'"filename"\s*:\s*"([^"]+\.html)"')
CATALOGUE_FILES = {"dhatupatha-sanskritdocuments.html"}
RESOLVED_NON_DOMAIN_HITS = {
    "03.0001": "The cited hu commentary uses chandasi while discussing a case rule and a construction, not to restrict the base entry to the Vedic domain."
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plain_text(path: Path) -> str:
    text = re.sub(r"<[^>]+>", " ", path.read_text(errors="replace"))
    return re.sub(r"\s+", " ", html.unescape(text))


def main() -> None:
    known = {
        row["source_code"]: row
        for row in json.loads(RESTRICTIONS.read_text())["source_entries"]
    }
    source_text = {}
    source_rows = []
    with ASSIGNMENTS.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["record_kind"] != "lexical":
                continue
            source_rows.append(row)
    grouped = {}
    for row in source_rows:
        item = grouped.setdefault(row["normalized_count_key"], {
            "base_count_key": row["normalized_count_key"], "source_codes": set(),
            "citations": set(), "meanings": set(), "files": set(),
        })
        item["source_codes"].add(row["source_code"])
        item["citations"].add(row["normalized_citation_slp1"])
        item["meanings"].add(row["normalized_meaning_slp1"])
        item["files"].update(FILE_REF.findall(
            row.get("meaning_evidence", "") + " " + row.get("cross_reference_evidence", "")
        ))

    rows = []
    for key in sorted(grouped):
        item = grouped[key]
        files = sorted(item["files"])
        hits = []
        for filename in files:
            if filename in CATALOGUE_FILES:
                continue
            path = ARCHIVE / filename
            if not path.exists():
                continue
            text = source_text.setdefault(filename, plain_text(path))
            matches = list(DOMAIN_MARKER.finditer(text))
            if matches:
                excerpts = []
                for match in matches[:3]:
                    start = max(0, match.start() - 90)
                    end = min(len(text), match.end() + 150)
                    excerpts.append(text[start:end])
                hits.append({"filename": filename, "excerpts": excerpts})
        known_codes = item["source_codes"] & set(known)
        if known_codes and known_codes != item["source_codes"]:
            status = "mixed_domain_identity_review_required"
            basis = "One normalized identity contains both a documented Vedic-only source and another source code."
        elif known_codes:
            status = "documented_vedic_only"
            basis = "; ".join(known[code]["restriction"] for code in sorted(known_codes))
        elif item["source_codes"] <= set(RESOLVED_NON_DOMAIN_HITS):
            status = "no_domain_restriction_found_in_cited_evidence"
            basis = "; ".join(RESOLVED_NON_DOMAIN_HITS[code] for code in sorted(item["source_codes"]))
        elif hits:
            status = "domain_language_present_review_required"
            basis = "A cited commentary contains Vedic-domain language; its scope must be resolved manually."
        else:
            status = "no_domain_restriction_found_in_cited_evidence"
            basis = "The currently cited evidence contains no explicit domain restriction; this is not affirmative proof of unrestricted use."
        rows.append({
            "base_count_key": item["base_count_key"],
            "source_codes": ";".join(sorted(item["source_codes"])),
            "citations_slp1": ";".join(sorted(item["citations"])),
            "meanings_slp1": ";".join(sorted(item["meanings"])),
            "domain_status": status,
            "domain_basis": basis,
            "evidence_files": ";".join(files),
            "domain_marker_hits": json.dumps(hits, ensure_ascii=False),
        })
    rows.sort(key=lambda row: row["base_count_key"])
    with (RESULTS / "base_domain_audit.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    counts = Counter(row["domain_status"] for row in rows)
    review_codes = sorted({
        code for row in rows for code in row["source_codes"].split(";")
        if row["domain_status"] == "domain_language_present_review_required"
    })
    report = {
        "date": "2026-09-13",
        "base_word_meanings_audited": len(rows),
        "status_counts": dict(sorted(counts.items())),
        "source_codes_requiring_domain_review": review_codes,
        "method": "Each admitted base meaning was checked against its currently cited archived commentaries for explicit Vedic-domain language. Absence of such language was not converted into proof of unrestricted laukika use.",
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (ASSIGNMENTS, RESTRICTIONS, ARCHIVE / "manifest.json", Path(__file__))
        },
    }
    (RESULTS / "base_domain_audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Base-Domain Evidence Audit", "",
        f"This pass checks all **{len(rows):,} admitted base word-meanings** against the commentary evidence already attached to them. It distinguishes a documented restriction from a source that merely contains domain language, and it does not treat silence as proof of unrestricted use.", "",
        "| Status | Word-meanings |", "|---|---:|",
    ]
    for status, count in sorted(counts.items()):
        lines.append(f"| {status.replace('_', ' ')} | {count:,} |")
    if review_codes:
        lines.extend(["", f"**{len(review_codes):,} source codes** require a manual scope decision because one of their cited commentaries contains Vedic-domain language. They remain outside any newly asserted domain classification."])
    lines.extend([
        "",
        "The eleven meanings already supported as Vedic-only remain excluded from the known laukika subtotal. This audit adds no restriction merely because a root occurs in the Vedas, and it adds no laukika authorization merely because a reviewed excerpt is silent.", "",
    ])
    (RESULTS / "base_domain_audit.md").write_text("\n".join(lines))
    print(f"Audited {len(rows)} base meanings; {len(review_codes)} source codes require domain review.")


if __name__ == "__main__":
    main()

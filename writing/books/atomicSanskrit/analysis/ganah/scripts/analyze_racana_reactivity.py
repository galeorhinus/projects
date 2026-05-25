#!/usr/bin/env python3
"""
analyze_racana_reactivity.py — Cross-tabulate dhātu *racanā* (phonetic
template, Ch 10) against Path C *reactivity* (corpus-attested valency, Ch 11).

Reads: data/derived/dhatu_scaffold_path_c_join.csv (2,168-row join of
Dhātupāṭha entries with their racanā template + corpus-attested valency).

The join is row-level (one row per Dhātupāṭha entry); the same dhātu
recurs across multiple gaṇas. Path C valency is per-root, so summing
across gaṇa-repeated rows would inflate counts. This script deduplicates
by (dhatu_iast, racana_scaffold) before computing per-scaffold aggregates.

Outputs:
  data/derived/racana_reactivity.csv — one row per racanā with valency
    distribution, tier counts, and top-attested members
  data/derived/racana_reactivity.md  — readable narrative summary

Tier definitions (per Path C locked scheme):
  Polyvalent: valency ≥ 50
  Bivalent:   5 ≤ valency ≤ 49
  Monovalent: 0 ≤ valency ≤ 4
"""

from __future__ import annotations

import csv
import statistics
from collections import defaultdict
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent.parent
JOIN_FILE = BUNDLE / "data" / "derived" / "dhatu_scaffold_path_c_join.csv"
OUT_CSV = BUNDLE / "data" / "derived" / "racana_reactivity.csv"
OUT_MD = BUNDLE / "data" / "derived" / "racana_reactivity.md"


# Top-10 racanā class names (from Ch 10 §10.6)
RACANA_NAMES = {
    "CV1C":   "gamādi (गमादि)",
    "CCV1C":  "smarādi (स्मरादि)",
    "CV1CC":  "kalpādi (कल्पादि)",
    "CV2CV1": "bādhrādi (बाध्रादि)",
    "CV2C":   "vācādi (वाचादि)",
    "CV2":    "dhādi (धादि)",
    "V1C":    "iṣādi (इषादि)",
    "CV1":    "krādi (क्रादि)",
    "CV1CV2": "cityādi (चित्यादि)",
    "CCV2":   "sthādi (स्थादि)",
}
TOP_TEN = list(RACANA_NAMES.keys())


def tier(v: int) -> str:
    if v >= 50:
        return "Polyvalent"
    if v >= 5:
        return "Bivalent"
    return "Monovalent"


def main():
    # Deduplicate by (dhatu_iast, racana_scaffold) — keep one row per unique
    # (root, scaffold) pair so that gaṇa-recurring dhātus don't double-count.
    # If a dhātu legitimately sits under multiple scaffolds (rare), each
    # scaffold gets its own row, attributing the same Path C valency to each.
    seen = set()
    unique_rows = []
    with JOIN_FILE.open() as fh:
        for row in csv.DictReader(fh):
            key = (row["dhatu_iast"], row["racana_scaffold"])
            if key in seen:
                continue
            seen.add(key)
            unique_rows.append(row)

    # Bucket by racanā
    by_racana = defaultdict(list)
    for row in unique_rows:
        racana = row["racana_scaffold"]
        by_racana[racana].append({
            "iast": row["dhatu_iast"],
            "deva": row["dhatu_devanagari"],
            "valency": int(row["path_c_valency"] or 0),
            "tokens": int(row["path_c_token_count"] or 0),
            "attested": row["attested_in_dcs"] == "yes",
            "matra": float(row["matra_count"]) if row["matra_count"] else 0.0,
            "particles": int(row["particle_count"]) if row["particle_count"] else 0,
        })

    # Per-racanā aggregates
    rows_for_csv = []
    for racana, dhatus in by_racana.items():
        n_total = len(dhatus)
        attested = [d for d in dhatus if d["attested"]]
        n_attested = len(attested)
        valencies = [d["valency"] for d in dhatus]   # zeros for unattested
        valencies_att = [d["valency"] for d in attested]
        tokens_total = sum(d["tokens"] for d in dhatus)

        # Tier counts (treating unattested = monovalent, since valency = 0)
        poly = sum(1 for d in dhatus if d["valency"] >= 50)
        biv = sum(1 for d in dhatus if 5 <= d["valency"] < 50)
        mono = n_total - poly - biv

        # Top attested members
        top_5 = sorted(attested, key=lambda d: -d["valency"])[:5]
        top_names = "; ".join(
            f"{d['iast']} ({d['valency']})" for d in top_5
        )

        # Coverage = % of this scaffold that's corpus-attested
        coverage = (100 * n_attested / n_total) if n_total else 0

        rows_for_csv.append({
            "racana": racana,
            "name": RACANA_NAMES.get(racana, ""),
            "n_total": n_total,
            "n_attested": n_attested,
            "coverage_pct": round(coverage, 1),
            "mean_valency_attested": round(statistics.mean(valencies_att), 1)
                if valencies_att else 0,
            "median_valency_attested": int(statistics.median(valencies_att))
                if valencies_att else 0,
            "max_valency": max(valencies, default=0),
            "polyvalent_count": poly,
            "bivalent_count": biv,
            "monovalent_count": mono,
            "total_corpus_tokens": tokens_total,
            "top_5_attested": top_names,
        })

    # Sort by mean valency descending (most-reactive scaffolds first)
    rows_for_csv.sort(key=lambda r: -r["mean_valency_attested"])

    # --- CSV ---
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows_for_csv[0].keys()))
        w.writeheader()
        for r in rows_for_csv:
            w.writerow(r)

    # --- Markdown narrative ---
    total_dhatus = sum(r["n_total"] for r in rows_for_csv)
    total_attested = sum(r["n_attested"] for r in rows_for_csv)
    total_polyvalent = sum(r["polyvalent_count"] for r in rows_for_csv)
    total_bivalent = sum(r["bivalent_count"] for r in rows_for_csv)
    total_tokens = sum(r["total_corpus_tokens"] for r in rows_for_csv)

    with OUT_MD.open("w") as fh:
        fh.write("# Dhātu *racanā* × Path C reactivity\n\n")
        fh.write("> Cross-analysis joining Ch 10's phonetic-scaffold framework "
                 "with Ch 11's corpus-attested valency. "
                 "Generated by `scripts/analyze_racana_reactivity.py`.\n>\n")
        fh.write(f"> Dataset: {total_dhatus:,} unique (dhātu, racanā) pairs "
                 f"after deduplication; {total_attested:,} corpus-attested "
                 f"({100 * total_attested / total_dhatus:.1f}% coverage); "
                 f"{total_polyvalent:,} polyvalent + {total_bivalent:,} "
                 f"bivalent.\n\n")
        fh.write("---\n\n")

        # Top-10 racanāḥ — reactivity table
        fh.write("## Top-10 *racanāḥ* — reactivity profile\n\n")
        fh.write("Rows in the §10.6 Ch 10 order (descending corpus count). "
                 "Columns show how each scaffold distributes across reactivity tiers.\n\n")
        fh.write("| Racanā | Class | N | Attested | Mean val (att.) | Polyvalent | Bivalent | Mono | Max val | Top attested |\n")
        fh.write("|---|---|---:|---:|---:|---:|---:|---:|---:|---|\n")
        for tmpl in TOP_TEN:
            r = next((x for x in rows_for_csv if x["racana"] == tmpl), None)
            if r is None:
                continue
            top_brief = r["top_5_attested"].split(";")[0].strip() if r["top_5_attested"] else "—"
            fh.write(
                f"| **{r['racana']}** | *{RACANA_NAMES[tmpl].split(' (')[0]}* | "
                f"{r['n_total']} | {r['n_attested']} ({r['coverage_pct']:.0f}%) | "
                f"**{r['mean_valency_attested']}** | "
                f"{r['polyvalent_count']} | {r['bivalent_count']} | "
                f"{r['monovalent_count']} | {r['max_valency']} | "
                f"{top_brief} |\n"
            )
        fh.write("\n")

        # Reactivity-ranked view — all racanāḥ with ≥ 1 polyvalent
        fh.write("## All *racanāḥ* with ≥1 polyvalent member (mean valency descending)\n\n")
        fh.write("Highlights the scaffolds whose attested members are *reactive*, "
                 "not just *numerous*. Sorted by mean-valency-of-attested descending.\n\n")
        fh.write("| Racanā | Class | N | Attested | Mean val | Polyvalent | Top attested |\n")
        fh.write("|---|---|---:|---:|---:|---:|---|\n")
        reactive_rows = [r for r in rows_for_csv if r["polyvalent_count"] > 0]
        reactive_rows.sort(key=lambda r: -r["mean_valency_attested"])
        for r in reactive_rows[:25]:
            class_name = RACANA_NAMES.get(r["racana"], "—").split(" (")[0]
            top_brief = r["top_5_attested"].split(";")[0].strip() if r["top_5_attested"] else "—"
            fh.write(
                f"| **{r['racana']}** | *{class_name}* | {r['n_total']} | "
                f"{r['n_attested']} | **{r['mean_valency_attested']}** | "
                f"{r['polyvalent_count']} | {top_brief} |\n"
            )
        fh.write(f"\n*Showing top 25 of {len(reactive_rows)} reactive *racanāḥ*.*\n\n")

        # Token coverage by top-10 racanāḥ
        fh.write("## Corpus-token coverage by *racanā*\n\n")
        top10_tokens = sum(
            next((x["total_corpus_tokens"] for x in rows_for_csv if x["racana"] == t), 0)
            for t in TOP_TEN
        )
        fh.write(f"- Top-10 *racanāḥ* (Ch 10 §10.6 spine): "
                 f"**{top10_tokens:,} corpus tokens** "
                 f"= **{100 * top10_tokens / total_tokens:.1f}%** of all attestations.\n")
        # CV1C alone
        cv1c = next((x for x in rows_for_csv if x["racana"] == "CV1C"), None)
        if cv1c:
            fh.write(f"- **CV1C (*gamādi*) alone**: {cv1c['total_corpus_tokens']:,} tokens = "
                     f"**{100 * cv1c['total_corpus_tokens'] / total_tokens:.1f}%** "
                     f"of all attestations.\n")
        # Top 3
        top3 = ["CV1C", "CV1", "CV2"]
        top3_tok = sum(next((x["total_corpus_tokens"] for x in rows_for_csv if x["racana"] == t), 0) for t in top3)
        fh.write(f"- **Top-3 compact *racanāḥ* (CV1C + CV1 + CV2)**: {top3_tok:,} tokens = "
                 f"**{100 * top3_tok / total_tokens:.1f}%** of all attestations.\n\n")

        # Reactivity concentration headline
        fh.write("## Reactivity concentration\n\n")
        fh.write("Where do the polyvalent dhātus actually sit?\n\n")
        # Group polyvalent counts by racanā, descending
        poly_by_racana = sorted(
            ((r["racana"], r["polyvalent_count"], RACANA_NAMES.get(r["racana"], ""))
             for r in rows_for_csv if r["polyvalent_count"] > 0),
            key=lambda x: -x[1]
        )
        cum = 0
        for racana, n_poly, name in poly_by_racana:
            cum += n_poly
        fh.write(f"- Total polyvalent dhātus (valency ≥ 50): **{total_polyvalent}** "
                 f"(across {len(poly_by_racana)} distinct *racanāḥ*).\n")
        top_poly = poly_by_racana[:5]
        fh.write("- Top scaffolds by polyvalent count:\n")
        running = 0
        for racana, n_poly, name in top_poly:
            running += n_poly
            class_name = name.split(" (")[0] if name else "—"
            fh.write(f"  - **{racana}** (*{class_name}*): {n_poly} polyvalent dhātus "
                     f"(cum: {running}/{total_polyvalent}, "
                     f"{100 * running / total_polyvalent:.0f}%)\n")
        fh.write(f"\nThe top 5 *racanāḥ* by polyvalent count carry "
                 f"**{running}/{total_polyvalent} "
                 f"({100 * running / total_polyvalent:.0f}%)** of all reactive dhātus.\n")

    # Console summary
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Unique (dhātu, racanā) pairs: {total_dhatus}")
    print(f"Attested: {total_attested} ({100 * total_attested / total_dhatus:.1f}%)")
    print(f"Polyvalent: {total_polyvalent}; Bivalent: {total_bivalent}")
    print(f"\nTop-10 racanāḥ by mean valency:")
    for r in rows_for_csv[:10]:
        print(f"  {r['racana']:<8} mean v = {r['mean_valency_attested']:>6} "
              f"(n_att={r['n_attested']}, poly={r['polyvalent_count']}, "
              f"top={r['top_5_attested'].split(';')[0].strip() if r['top_5_attested'] else '—'})")


if __name__ == "__main__":
    main()

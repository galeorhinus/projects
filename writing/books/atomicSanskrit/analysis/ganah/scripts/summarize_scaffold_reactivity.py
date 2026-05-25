#!/usr/bin/env python3
"""Summarize Ch10 scaffold compression against DCS actual use.

Inputs:
  data/derived/dhatu_scaffold_path_c_join.csv
  data/derived/path_c_valency.csv

Outputs:
  data/derived/dhatu_scaffold_path_c_join_canonical.csv
  data/derived/scaffold_reactivity_summary.csv
  data/derived/scaffold_reactivity_summary.md
  data/derived/dhatu_scaffold_path_c_join_audit.txt

The input join is row-level: one row per Dhātupāṭha listing. The DCS usage
fields are dhātu-level, so this script keeps inventory counts row-level but
deduplicates actual-use metrics by canonical dhātuḥ before summing combinations
or occurrence counts by scaffold.
"""

from __future__ import annotations

import csv
import statistics
from collections import Counter, defaultdict
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent.parent
DERIVED = BUNDLE / "data" / "derived"

JOIN_FILE = DERIVED / "dhatu_scaffold_path_c_join.csv"
PATH_C_VALENCY = DERIVED / "path_c_valency.csv"

OUT_CANONICAL = DERIVED / "dhatu_scaffold_path_c_join_canonical.csv"
OUT_SUMMARY = DERIVED / "scaffold_reactivity_summary.csv"
OUT_MD = DERIVED / "scaffold_reactivity_summary.md"
OUT_AUDIT = DERIVED / "dhatu_scaffold_path_c_join_audit.txt"

RACANA_NAMES = {
    "CV1C": "gamādi (गमादि)",
    "CCV1C": "smarādi (स्मरादि)",
    "CV1CC": "kalpādi (कल्पादि)",
    "CV2CV1": "bādhrādi (बाध्रादि)",
    "CV2C": "vācādi (वाचादि)",
    "CV2": "dhādi (धादि)",
    "V1C": "iṣādi (इषादि)",
    "CV1": "krādi (क्रादि)",
    "CV1CV2": "cityādi (चित्यादि)",
    "CCV2": "sthādi (स्थादि)",
}

TOP_TEN = [
    "CV1C",
    "CCV1C",
    "CV1CC",
    "CV2CV1",
    "CV2C",
    "CV2",
    "V1C",
    "CV1",
    "CV1CV2",
    "CCV2",
]

# Targeted canonicalization for high-value DCS dhātavaḥ whose Dhātupāṭha
# citation form survives the first-pass stripping differently from the DCS
# dhātu key. These overrides are deliberately small and audited, not a hidden
# rewrite of the full Ch10 inventory analysis.
CANONICAL_OVERRIDES = {
    "gamḷ": {
        "canonical_dhatu": "gam",
        "canonical_devanagari": "गम्",
        "canonical_scaffold": "CV1C",
        "canonical_particle_count": "3",
        "canonical_matra_count": "2.0",
        "reason": "Dhātupāṭha citation retains final ḷ marker; DCS canonical dhātu is gam.",
    },
    "ṇī": {
        "canonical_dhatu": "nī",
        "canonical_devanagari": "नी",
        "canonical_scaffold": "CV2",
        "canonical_particle_count": "2",
        "canonical_matra_count": "2.5",
        "reason": "Dhātupāṭha citation uses ṇī; DCS canonical dhātu is nī.",
    },
    "ṣṭhā": {
        "canonical_dhatu": "sthā",
        "canonical_devanagari": "स्था",
        "canonical_scaffold": "CCV2",
        "canonical_particle_count": "3",
        "canonical_matra_count": "3.0",
        "reason": "Dhātupāṭha citation uses ṣṭhā; DCS canonical dhātu is sthā.",
    },
    "ruḥ": {
        "canonical_dhatu": "ruh",
        "canonical_devanagari": "रुह्",
        "canonical_scaffold": "CV1C",
        "canonical_particle_count": "3",
        "canonical_matra_count": "2.0",
        "reason": "Dhātupāṭha citation writes final visarga; DCS canonical dhātu is ruh.",
    },
}

ACCOUNTED_UNMATCHED_TOP_ROOTS = {
    "vartay": (
        "The DCS usage record carries vartay as a corpus-derived causative/derived lemma. "
        "It is not forced into the Dhātupāṭha scaffold inventory as a separate atom."
    ),
}


def load_path_c() -> dict[str, dict[str, str]]:
    with PATH_C_VALENCY.open(encoding="utf-8") as f:
        # The source file uses the field name "root". Keep the input contract
        # here, but expose the result as dhātuḥ terminology in generated output.
        return {row["root"]: row for row in csv.DictReader(f)}


def canonicalize(row: dict[str, str], path_c: dict[str, dict[str, str]]) -> dict[str, str]:
    out = dict(row)
    root = row["dhatu_iast"]
    override = CANONICAL_OVERRIDES.get(root)

    out["canonical_note"] = ""
    if override:
        out["canonical_dhatu_iast"] = override["canonical_dhatu"]
        out["canonical_dhatu_devanagari"] = override["canonical_devanagari"]
        out["canonical_racana_scaffold"] = override["canonical_scaffold"]
        out["canonical_particle_count"] = override["canonical_particle_count"]
        out["canonical_matra_count"] = override["canonical_matra_count"]
        out["canonical_note"] = override["reason"]
    else:
        out["canonical_dhatu_iast"] = row["dhatu_iast"]
        out["canonical_dhatu_devanagari"] = row["dhatu_devanagari"]
        out["canonical_racana_scaffold"] = row["racana_scaffold"]
        out["canonical_particle_count"] = row["particle_count"]
        out["canonical_matra_count"] = row["matra_count"]

    pc = path_c.get(out["canonical_dhatu_iast"])
    out["canonical_visible_in_dcs"] = "yes" if pc else "no"
    out["canonical_path_c_valency"] = pc["valency_path_c"] if pc else "0"
    out["canonical_path_c_token_count"] = pc["total_tokens"] if pc else "0"
    out["canonical_path_c_distinct_preverbs"] = pc["distinct_preverbs"] if pc else "0"
    out["canonical_path_c_distinct_pratyayas"] = pc["distinct_pratyayas"] if pc else "0"
    return out


def representative_rows(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    """Return one row per canonical dhātuḥ for DCS metric aggregation."""
    by_root: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_root[row["canonical_dhatu_iast"]].append(row)

    reps: dict[str, dict[str, str]] = {}
    for root, root_rows in by_root.items():
        # Prefer a row that appears in DCS after canonicalization, then
        # the shortest canonical scaffold, then the earliest Dhātupāṭha id.
        reps[root] = sorted(
            root_rows,
            key=lambda r: (
                0 if r["canonical_visible_in_dcs"] == "yes" else 1,
                float(r["canonical_matra_count"] or 99),
                int(r["particle_count"] or 99),
                tuple(int(p) for p in r["dhatu_id"].split(".") if p.isdigit()),
            ),
        )[0]
    return reps


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if not JOIN_FILE.exists():
        raise SystemExit(f"missing input: {JOIN_FILE}")
    if not PATH_C_VALENCY.exists():
        raise SystemExit(f"missing input: {PATH_C_VALENCY}")

    path_c = load_path_c()
    with JOIN_FILE.open(encoding="utf-8") as f:
        raw_rows = list(csv.DictReader(f))

    canonical_rows = [canonicalize(row, path_c) for row in raw_rows]
    reps = representative_rows(canonical_rows)
    visible_reps = [
        row for row in reps.values()
        if row["canonical_visible_in_dcs"] == "yes"
    ]

    canonical_fieldnames = list(raw_rows[0].keys()) + [
        "canonical_dhatu_iast",
        "canonical_dhatu_devanagari",
        "canonical_racana_scaffold",
        "canonical_particle_count",
        "canonical_matra_count",
        "canonical_visible_in_dcs",
        "canonical_path_c_valency",
        "canonical_path_c_token_count",
        "canonical_path_c_distinct_preverbs",
        "canonical_path_c_distinct_pratyayas",
        "canonical_note",
    ]
    write_csv(OUT_CANONICAL, canonical_rows, canonical_fieldnames)

    inventory_counts = Counter(r["canonical_racana_scaffold"] for r in canonical_rows)
    dhatus_by_scaffold: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in visible_reps:
        dhatus_by_scaffold[row["canonical_racana_scaffold"]].append(row)

    total_visible_dhatus = len(visible_reps)
    total_valency = sum(int(r["canonical_path_c_valency"]) for r in visible_reps)
    total_tokens = sum(int(r["canonical_path_c_token_count"]) for r in visible_reps)

    scaffolds = sorted(
        set(inventory_counts) | set(dhatus_by_scaffold),
        key=lambda s: (-inventory_counts[s], s),
    )
    summary_rows: list[dict[str, object]] = []
    for scaffold in scaffolds:
        dhatus = dhatus_by_scaffold.get(scaffold, [])
        valencies = [int(r["canonical_path_c_valency"]) for r in dhatus]
        tokens = [int(r["canonical_path_c_token_count"]) for r in dhatus]
        top_dhatus = sorted(
            dhatus,
            key=lambda r: -int(r["canonical_path_c_valency"]),
        )[:5]
        summary_rows.append({
            "racana_scaffold": scaffold,
            "racana_name": RACANA_NAMES.get(scaffold, ""),
            "inventory_count": inventory_counts[scaffold],
            "inventory_share_pct": round(100 * inventory_counts[scaffold] / len(canonical_rows), 2),
            "text_visible_dhatu_count": len(dhatus),
            "text_visible_dhatu_share_pct": round(100 * len(dhatus) / total_visible_dhatus, 2)
                if total_visible_dhatus else 0,
            "total_path_c_valency": sum(valencies),
            "valency_share_pct": round(100 * sum(valencies) / total_valency, 2)
                if total_valency else 0,
            "mean_valency": round(statistics.mean(valencies), 1) if valencies else 0,
            "median_valency": round(statistics.median(valencies), 1) if valencies else 0,
            "total_tokens": sum(tokens),
            "token_share_pct": round(100 * sum(tokens) / total_tokens, 2)
                if total_tokens else 0,
            "top_text_visible_dhatavah": "; ".join(
                f"{r['canonical_dhatu_iast']} ({r['canonical_path_c_valency']})"
                for r in top_dhatus
            ),
        })

    summary_fieldnames = [
        "racana_scaffold",
        "racana_name",
        "inventory_count",
        "inventory_share_pct",
        "text_visible_dhatu_count",
        "text_visible_dhatu_share_pct",
        "total_path_c_valency",
        "valency_share_pct",
        "mean_valency",
        "median_valency",
        "total_tokens",
        "token_share_pct",
        "top_text_visible_dhatavah",
    ]
    write_csv(OUT_SUMMARY, summary_rows, summary_fieldnames)

    top10_inventory = sum(r["inventory_count"] for r in summary_rows if r["racana_scaffold"] in TOP_TEN)
    top10_dhatus = sum(r["text_visible_dhatu_count"] for r in summary_rows if r["racana_scaffold"] in TOP_TEN)
    top10_valency = sum(r["total_path_c_valency"] for r in summary_rows if r["racana_scaffold"] in TOP_TEN)
    top10_tokens = sum(r["total_tokens"] for r in summary_rows if r["racana_scaffold"] in TOP_TEN)

    with OUT_MD.open("w", encoding="utf-8") as f:
        f.write("# Scaffold Actual-Use Summary\n\n")
        f.write("Generated by `analysis/ganah/scripts/summarize_scaffold_reactivity.py`.\n\n")
        f.write(f"- Inventory rows: **{len(canonical_rows):,}**\n")
        f.write(f"- Canonical distinct dhātavaḥ: **{len(reps):,}**\n")
        f.write(f"- DCS-visible canonical dhātavaḥ: **{total_visible_dhatus:,}**\n")
        f.write(f"- Total DCS-derived combinations after deduplication: **{total_valency:,}**\n")
        f.write(f"- Total DCS occurrences after deduplication: **{total_tokens:,}**\n\n")
        f.write("## Top-ten scaffold coverage\n\n")
        f.write(f"- Inventory: **{top10_inventory:,} / {len(canonical_rows):,}** "
                f"(**{100 * top10_inventory / len(canonical_rows):.1f}%**)\n")
        f.write(f"- Dhātavaḥ in texts: **{top10_dhatus:,} / {total_visible_dhatus:,}** "
                f"(**{100 * top10_dhatus / total_visible_dhatus:.1f}%**)\n")
        f.write(f"- Combinations: **{top10_valency:,} / {total_valency:,}** "
                f"(**{100 * top10_valency / total_valency:.1f}%**)\n")
        f.write(f"- Occurrences: **{top10_tokens:,} / {total_tokens:,}** "
                f"(**{100 * top10_tokens / total_tokens:.1f}%**)\n\n")
        f.write("## Top rows\n\n")
        f.write("| Scaffold | Inventory % | Dhātavaḥ in texts % | Combination % | Occurrence % | Top dhātavaḥ |\n")
        f.write("|---|---:|---:|---:|---:|---|\n")
        for row in [r for r in summary_rows if r["racana_scaffold"] in TOP_TEN]:
            f.write(
                f"| **{row['racana_scaffold']}** | "
                f"{row['inventory_share_pct']} | "
                f"{row['text_visible_dhatu_share_pct']} | "
                f"{row['valency_share_pct']} | "
                f"{row['token_share_pct']} | "
                f"{row['top_text_visible_dhatavah'] or '—'} |\n"
            )

    path_roots = list(path_c.values())
    top20 = path_roots[:20]
    canonical_roots = set(reps)
    override_notes = [
        (src, vals["canonical_dhatu"], vals["reason"])
        for src, vals in CANONICAL_OVERRIDES.items()
    ]
    row_count_by_root = Counter(r["canonical_dhatu_iast"] for r in canonical_rows)
    scaffold_by_root = {
        root: reps[root]["canonical_racana_scaffold"]
        for root in reps
    }

    with OUT_AUDIT.open("w", encoding="utf-8") as f:
        f.write("Dhātupāṭha scaffold × DCS usage canonicalization audit\n")
        f.write("=" * 62 + "\n\n")
        f.write("Targeted canonicalization overrides applied:\n")
        for src, dst, reason in override_notes:
            f.write(f"- {src} -> {dst}: {reason}\n")
        f.write("\nTop 20 DCS dhātavaḥ by measured combination count:\n")
        for i, row in enumerate(top20, start=1):
            root = row["root"]
            if root in canonical_roots:
                f.write(
                    f"{i:02d}. {root}: matched; scaffold={scaffold_by_root[root]}; "
                    f"inventory_rows={row_count_by_root[root]}; "
                    f"combinations={row['valency_path_c']}; occurrences={row['total_tokens']}\n"
                )
            elif root in ACCOUNTED_UNMATCHED_TOP_ROOTS:
                f.write(
                    f"{i:02d}. {root}: accounted but not matched; "
                    f"{ACCOUNTED_UNMATCHED_TOP_ROOTS[root]} "
                    f"combinations={row['valency_path_c']}; occurrences={row['total_tokens']}\n"
                )
            else:
                f.write(
                    f"{i:02d}. {root}: not matched to a Dhātupāṭha atom after targeted "
                    f"canonicalization; combinations={row['valency_path_c']}; "
                    f"occurrences={row['total_tokens']}. Account separately before using "
                    "for scaffold-level claims.\n"
                )
        f.write("\nDeduplication rule:\n")
        f.write("- Inventory counts remain row-level across the 2,168 Dhātupāṭha entries.\n")
        f.write("- Corpus usage metrics are deduplicated by canonical dhātu before summing.\n")
        f.write("- Repeated gaṇa rows therefore do not inflate combination or occurrence totals.\n")
        f.write("\nTop-ten coverage after canonicalization:\n")
        f.write(f"- Inventory: {top10_inventory:,}/{len(canonical_rows):,} "
                f"({100 * top10_inventory / len(canonical_rows):.1f}%)\n")
        f.write(f"- Dhātavaḥ in texts: {top10_dhatus:,}/{total_visible_dhatus:,} "
                f"({100 * top10_dhatus / total_visible_dhatus:.1f}%)\n")
        f.write(f"- Combinations: {top10_valency:,}/{total_valency:,} "
                f"({100 * top10_valency / total_valency:.1f}%)\n")
        f.write(f"- Occurrences: {top10_tokens:,}/{total_tokens:,} "
                f"({100 * top10_tokens / total_tokens:.1f}%)\n")

    print(f"Wrote {OUT_CANONICAL}")
    print(f"Wrote {OUT_SUMMARY}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_AUDIT}")
    print(f"Top-ten inventory share: {100 * top10_inventory / len(canonical_rows):.1f}%")
    print(f"Top-ten dhātavaḥ-in-texts share: {100 * top10_dhatus / total_visible_dhatus:.1f}%")
    print(f"Top-ten combination share: {100 * top10_valency / total_valency:.1f}%")
    print(f"Top-ten occurrence share: {100 * top10_tokens / total_tokens:.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

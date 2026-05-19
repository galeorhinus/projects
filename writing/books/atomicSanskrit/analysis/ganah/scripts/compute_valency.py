#!/usr/bin/env python3
"""Path C — Phase 4: Compute per-root corpus-attested combinatorial valency.

Reads data/derived/attestation_index.csv (rows: root, preverb, pratyaya_class,
count) and aggregates per root:

  v_C(root) = | { (preverb, pratyaya_class) : count > 0 for this root } |

Also reports:
  - total_tokens: total token-occurrences across all (preverb, pratyaya) cells
  - distinct_preverbs: count of distinct preverbs attested (incl. bare-stem)
  - distinct_pratyayas: count of distinct pratyaya_classes attested

Output: data/derived/path_c_valency.csv
  Columns: root, valency_path_c, total_tokens, distinct_preverbs, distinct_pratyayas
"""
from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent.parent
IN_ATTEST = BUNDLE / "data" / "derived" / "attestation_index.csv"
OUT = BUNDLE / "data" / "derived" / "path_c_valency.csv"


def main():
    # root → set of (preverb, pratyaya) ; total_count ; preverbs ; pratyayas
    pairs: dict[str, set[tuple[str, str]]] = defaultdict(set)
    totals: dict[str, int] = defaultdict(int)
    preverbs: dict[str, set[str]] = defaultdict(set)
    pratyayas: dict[str, set[str]] = defaultdict(set)

    with open(IN_ATTEST, encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            root = row["root"]
            preverb = row["preverb"]
            prat = row["pratyaya_class"]
            count = int(row["count"])
            pairs[root].add((preverb, prat))
            totals[root] += count
            preverbs[root].add(preverb)
            pratyayas[root].add(prat)

    rows = []
    for root in pairs:
        rows.append({
            "root": root,
            "valency_path_c": len(pairs[root]),
            "total_tokens": totals[root],
            "distinct_preverbs": len(preverbs[root]),
            "distinct_pratyayas": len(pratyayas[root]),
        })
    rows.sort(key=lambda r: (-r["valency_path_c"], -r["total_tokens"], r["root"]))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["root", "valency_path_c", "total_tokens",
                                          "distinct_preverbs", "distinct_pratyayas"])
        w.writeheader()
        for row in rows:
            w.writerow(row)

    # Summary stats
    valencies = [r["valency_path_c"] for r in rows]
    print(f"Roots: {len(rows):,}")
    print(f"Max valency: {max(valencies)}")
    print(f"Mean valency: {sum(valencies)/len(valencies):.2f}")
    print(f"Median valency: {sorted(valencies)[len(valencies)//2]}")
    print(f"\nTop 20 by Path C valency:")
    for r in rows[:20]:
        print(f"  {r['root']:20s}  v={r['valency_path_c']:4d}  "
              f"tokens={r['total_tokens']:8,}  "
              f"prev={r['distinct_preverbs']:3d}  "
              f"prat={r['distinct_pratyayas']:3d}")
    print(f"\nWrote {OUT.relative_to(BUNDLE)}")


if __name__ == "__main__":
    main()

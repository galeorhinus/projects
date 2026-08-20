#!/usr/bin/env python3
"""Print full sentence with per-token analysis for a citation."""
import csv, sys
from pathlib import Path
IDX = Path(__file__).parent / "rv_index.tsv"
rows = list(csv.DictReader(IDX.open(encoding="utf-8"), delimiter="\t"))
cit = "RV " + sys.argv[1]
hits = [r for r in rows if r["citation"] == cit]
if not hits:
    print(f"no tokens at {cit}"); sys.exit(1)
seen=set()
for r in hits:
    if r["sent_text"] not in seen:
        seen.add(r["sent_text"]); print(f"\nTEXT: {r['sent_text']}")
    print(f"   {r['form']:16s} uns={r['unsandhied']:16s} {r['lemma']:12s} {r['upos']:6s} {r['feats']}")

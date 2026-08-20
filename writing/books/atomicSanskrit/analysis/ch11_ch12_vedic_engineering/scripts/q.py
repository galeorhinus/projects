#!/usr/bin/env python3
"""Query the RV index. Usage:
   q.py form <form>        -- exact surface OR unsandhied match
   q.py lemma <lemma>      -- all forms of a lemma
   q.py at <book.hymn.st>  -- everything at a citation
"""
import csv, sys
from pathlib import Path
IDX = Path(__file__).parent / "rv_index.tsv"
rows = list(csv.DictReader(IDX.open(encoding="utf-8"), delimiter="\t"))

def show(rs, limit=40):
    for r in rs[:limit]:
        print(f"{r['citation']:16s} {r['form']:22s} unsandhied={r['unsandhied']:22s} "
              f"lemma={r['lemma']:14s} {r['upos']:6s} {r['feats']}")
    if len(rs) > limit:
        print(f"... and {len(rs)-limit} more (total {len(rs)})")
    else:
        print(f"(total {len(rs)})")

cmd, arg = sys.argv[1], sys.argv[2]
if cmd == "form":
    show([r for r in rows if r["form"] == arg or r["unsandhied"] == arg])
elif cmd == "lemma":
    show([r for r in rows if r["lemma"] == arg])
elif cmd == "at":
    show([r for r in rows if r["citation"] == f"RV {arg}"], limit=100)

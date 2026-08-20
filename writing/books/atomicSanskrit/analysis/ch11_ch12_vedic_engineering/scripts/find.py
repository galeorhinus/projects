#!/usr/bin/env python3
import csv, re, sys
from pathlib import Path
IDX = Path(__file__).parent / "rv_index.tsv"
rows = list(csv.DictReader(IDX.open(encoding="utf-8"), delimiter="\t"))
def feat(r,k):
    m = re.search(rf"{k}=([^|]*)", r["feats"]); return m.group(1) if m else ""
# find.py LEMMA MOOD TENSE PERSON NUMBER  (use '-' for any)
lemma, mood, tense, person, number = (sys.argv[1:6] + ['-']*5)[:5]
out=[]
for r in rows:
    if r["upos"]!="VERB": continue
    if lemma!='-' and r["lemma"]!=lemma: continue
    if mood!='-' and feat(r,"Mood")!=mood: continue
    if tense!='-' and feat(r,"Tense")!=tense: continue
    if person!='-' and feat(r,"Person")!=person: continue
    if number!='-' and feat(r,"Number")!=number: continue
    out.append(r)
for r in out[:12]:
    print(f"{r['citation']:14s} {r['form']:18s} uns={r['unsandhied']:16s} {r['lemma']:10s} {r['feats']}")
    print(f"    → {r['sent_text'][:95]}")
print(f"(total {len(out)})")

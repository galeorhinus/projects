#!/usr/bin/env python3
"""Survey the RV index for the grammatical breadth categories the research needs."""
import csv, re, collections
from pathlib import Path
IDX = Path("/private/tmp/claude-501/-Users-paragtope-projects-writing-books-atomicSanskrit/41f61db1-8c52-45f2-84e7-50ceb19a8206/scratchpad/vedic/rv_index.tsv")
rows = list(csv.DictReader(IDX.open(encoding="utf-8"), delimiter="\t"))
verbs = [r for r in rows if r["upos"] == "VERB"]

def feat(r, k):
    m = re.search(rf"{k}=([^|]*)", r["feats"])
    return m.group(1) if m else ""

print("=== VERB Mood values present in RV (DCS tagging) ===")
for v, n in collections.Counter(feat(r,"Mood") for r in verbs).most_common():
    print(f"  {v or '(none)':12s} {n}")
print()
print("=== VERB Tense values ===")
for v, n in collections.Counter(feat(r,"Tense") for r in verbs).most_common():
    print(f"  {v or '(none)':12s} {n}")
print()
print("=== Person x Number coverage (finite verbs) ===")
grid = collections.Counter()
for r in verbs:
    p, n = feat(r,"Person"), feat(r,"Number")
    if p and n:
        grid[(p,n)] += 1
print(f"  {'':10s}" + "".join(f"{n:>10s}" for n in ["Sing","Dual","Plur"]))
for p in ["1","2","3"]:
    print(f"  person {p}  " + "".join(f"{grid.get((p,n),0):>10d}" for n in ["Sing","Dual","Plur"]))
print()
print("=== VerbForm values (participles, gerundives, infinitives) ===")
for v, n in collections.Counter(feat(r,"VerbForm") for r in verbs).most_common():
    print(f"  {v or '(finite)':12s} {n}")
print()
print("=== NOUN Case coverage ===")
nouns = [r for r in rows if r["upos"] in ("NOUN","PRON","ADJ")]
for v, n in collections.Counter(feat(r,"Case") for r in nouns).most_common():
    print(f"  {v or '(none)':12s} {n}")

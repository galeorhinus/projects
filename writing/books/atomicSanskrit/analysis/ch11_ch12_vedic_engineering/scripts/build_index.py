#!/usr/bin/env python3
"""Build a searchable index of every word in the DCS Ṛgveda CoNLL-U dump.

One row per token: citation, surface form, unsandhied form, lemma, POS,
and the full morphological feature string. This is the verification
substrate -- "does this exact form occur at this exact citation" becomes
a lookup instead of a guess.
"""
import csv, re, sys
from pathlib import Path

RV_DIR = Path("/Users/paragtope/projects/writing/books/atomicSanskrit/analysis/ganah/data/raw/dcs/dcs/data/conllu/files/Ṛgveda")
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "rv_index.tsv")

# filename: "Ṛgveda-0295-ṚV, 3, 62-10221.conllu"  -> book 3, hymn 62
FNAME_RE = re.compile(r"ṚV, (\d+), (\d+)-")

rows = []
files = sorted(p for p in RV_DIR.iterdir() if p.name.endswith(".conllu"))
print(f"{len(files)} chapter files", file=sys.stderr)

for path in files:
    m = FNAME_RE.search(path.name)
    if not m:
        print(f"  skip (no citation in name): {path.name}", file=sys.stderr)
        continue
    book, hymn = m.group(1), m.group(2)
    stanza = ""
    sent_text = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.rstrip("\n")
        if line.startswith("# sent_counter = "):
            stanza = line.split("= ", 1)[1].strip()
            continue
        if line.startswith("# text = "):
            sent_text = line.split("= ", 1)[1].strip()
            continue
        if not line or line.startswith("#") or line.startswith("##"):
            continue
        parts = line.split("\t")
        if len(parts) < 10 or not parts[0][0].isdigit():
            continue
        idx, form, lemma, upos, xpos, feats, head, deprel, deps, misc = parts[:10]
        unsandhied = ""
        mm = re.search(r"Unsandhied=([^|]*)", misc)
        if mm:
            unsandhied = mm.group(1)
        rows.append({
            "book": book, "hymn": hymn, "stanza": stanza,
            "citation": f"RV {book}.{hymn}.{stanza}" if stanza else f"RV {book}.{hymn}",
            "form": form, "unsandhied": unsandhied, "lemma": lemma,
            "upos": upos, "feats": feats, "sent_text": sent_text,
            "file": path.name,
        })

with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
    w.writeheader()
    w.writerows(rows)
print(f"wrote {len(rows)} tokens -> {OUT}", file=sys.stderr)

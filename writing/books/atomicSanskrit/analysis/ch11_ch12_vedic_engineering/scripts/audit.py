#!/usr/bin/env python3
"""Audit every claim in working/10_active.md against the RV index."""
import csv
from pathlib import Path
IDX = Path("/private/tmp/claude-501/-Users-paragtope-projects-writing-books-atomicSanskrit/41f61db1-8c52-45f2-84e7-50ceb19a8206/scratchpad/vedic/rv_index.tsv")
rows = list(csv.DictReader(IDX.open(encoding="utf-8"), delimiter="\t"))

by_form = {}
for r in rows:
    for key in {r["form"], r["unsandhied"]}:
        if key:
            by_form.setdefault(key, []).append(r)

# (form, claimed_citation, claimed_person, claimed_number, gana_label)
CLAIMS = [
 ("bhavati","RV 10.85.34","3","Sing","1 bhvādi"),("bhavataḥ","RV 10.12.1","3","Dual","1 bhvādi"),
 ("bhavanti","RV 1.89.9","3","Plur","1 bhvādi"),("bhavasi","RV 5.81.5","2","Sing","1 bhvādi"),
 ("bhavathaḥ","RV 1.112.20","2","Dual","1 bhvādi"),("bhavatha","RV 5.55.8","2","Plur","1 bhvādi"),
 ("bhavāmi","TB (non-RV)","1","Sing","1 bhvādi"),("bhavāva","AV 14.2.71 (non-RV)","1","Dual","1 bhvādi"),
 ("bhavāma","RV 5.45.5","1","Plur","1 bhvādi"),
 ("atti","RV 1.164.20","3","Sing","2 adādi"),("attaḥ","RV 10.79.1","3","Dual","2 adādi"),
 ("adanti","RV 10.146.3","3","Plur","2 adādi"),("atsi","RV 10.28.3","2","Sing","2 adādi"),
 ("atthaḥ","NOT FOUND claim","2","Dual","2 adādi"),("attha","NOT FOUND claim","2","Plur","2 adādi"),
 ("admi","RV 10.86.14","1","Sing","2 adādi"),("advaḥ","NOT FOUND claim","1","Dual","2 adādi"),
 ("admaḥ","NOT FOUND claim","1","Plur","2 adādi"),
 ("dadāti","RV 10.117.3","3","Sing","3 juhotyādi"),("dattaḥ","NOT FOUND claim","3","Dual","3 juhotyādi"),
 ("dadati","RV 7.16.10","3","Plur","3 juhotyādi"),("dadāsi","RV 1.190.5","2","Sing","3 juhotyādi"),
 ("datthaḥ","NOT FOUND claim","2","Dual","3 juhotyādi"),("dattha","NOT FOUND claim","2","Plur","3 juhotyādi"),
 ("dadāmi","claimed non-Samhita","1","Sing","3 juhotyādi"),("dadvaḥ","NOT FOUND claim","1","Dual","3 juhotyādi"),
 ("dadmaḥ","ŚB/BĀU (non-RV)","1","Plur","3 juhotyādi"),
 ("dīvyati","RV 10.34 (root only)","3","Sing","4 divādi"),("dīvyataḥ","NOT FOUND claim","3","Dual","4 divādi"),
 ("dīvyanti","RV 10.34 (root only)","3","Plur","4 divādi"),("dīvyasi","NOT FOUND claim","2","Sing","4 divādi"),
 ("dīvyathaḥ","NOT FOUND claim","2","Dual","4 divādi"),("dīvyatha","NOT FOUND claim","2","Plur","4 divādi"),
 ("dīvyāmi","NOT FOUND claim","1","Sing","4 divādi"),("dīvyāvaḥ","NOT FOUND claim","1","Dual","4 divādi"),
 ("dīvyāmaḥ","NOT FOUND claim","1","Plur","4 divādi"),
 ("kṛṇoti","RV 1.92.6","3","Sing","5 svādi"),("kṛṇutaḥ","NOT FOUND claim","3","Dual","5 svādi"),
 ("kṛṇvanti","RV 1.47.2","3","Plur","5 svādi"),("kṛṇoṣi","RV 7.81.4","2","Sing","5 svādi"),
 ("kṛṇuthaḥ","NOT FOUND claim","2","Dual","5 svādi"),("kṛṇutha","NOT FOUND claim","2","Plur","5 svādi"),
 ("kṛṇomi","RV 10.125.5","1","Sing","5 svādi"),("kṛṇuvaḥ","NOT FOUND claim","1","Dual","5 svādi"),
 ("kṛṇumaḥ","NOT FOUND claim","1","Plur","5 svādi"),
 ("vindati","RV 9.67.21","3","Sing","6 tudādi"),("vindataḥ","NOT FOUND claim","3","Dual","6 tudādi"),
 ("vindanti","NOT FOUND claim","3","Plur","6 tudādi"),("vindasi","NOT FOUND claim","2","Sing","6 tudādi"),
 ("vindāmi","NOT FOUND claim","1","Sing","6 tudādi"),
 ("ruṇaddhi","RV 10.34.3","3","Sing","7 rudhādi"),("rundhanti","RV 9.70.5","3","Plur","7 rudhādi"),
 ("ruṇatsi","NOT FOUND claim","2","Sing","7 rudhādi"),
 ("tanute","RV 10.130.1","3","Sing","8 tanādi"),("tanvate","NOT FOUND claim","3","Plur","8 tanādi"),
 ("tanve","NOT FOUND claim","1","Sing","8 tanādi"),
 ("krīṇāti","RV 4.24.10","3","Sing","9 kryādi"),("krīṇanti","NOT FOUND claim","3","Plur","9 kryādi"),
 ("krīṇāmi","NOT FOUND claim","1","Sing","9 kryādi"),
 ("dhārayati","RV 7.85.3","3","Sing","10 curādi"),("dhārayanti","NOT FOUND claim","3","Plur","10 curādi"),
 ("dhārayāmi","NOT FOUND claim","1","Sing","10 curādi"),
]

print(f"{'FORM':14s} {'CLAIMED':22s} {'VERDICT':10s} DETAIL")
print("="*130)
for form, claimed, person, number, gana in CLAIMS:
    hits = by_form.get(form, [])
    if not hits:
        verdict = "ABSENT" if "NOT FOUND" in claimed else "**MISSING**"
        print(f"{form:14s} {claimed:22s} {verdict:10s} not in RV index (0 occurrences)")
        continue
    cits = sorted({h["citation"] for h in hits})
    # does the claimed citation appear among the hits?
    claim_cit = claimed.replace("RV ","RV ").strip()
    exact = [c for c in cits if c == claim_cit]
    feats = sorted({h["feats"] for h in hits})
    if exact:
        verdict = "CONFIRMED"
        detail = f"{len(hits)}x in RV; claimed citation present. feats={feats[0][:60]}"
    elif claimed.startswith("RV"):
        verdict = "**CIT-WRONG**"
        detail = f"{len(hits)}x in RV but NOT at {claim_cit}. Actual: {', '.join(cits[:6])}"
    else:
        verdict = "**FOUND-IN-RV**"
        detail = f"claimed absent/non-RV, but occurs {len(hits)}x: {', '.join(cits[:6])}"
    print(f"{form:14s} {claimed:22s} {verdict:10s} {detail}")

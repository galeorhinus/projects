#!/usr/bin/env python3
"""Archive the pinned generator inputs and primary grammar used in the pilot."""

from datetime import datetime, timezone
import csv
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
COMMIT = "f3ba4167d40eebc4b3023d24e66867aa6a8cdb32"
RAW = f"https://raw.githubusercontent.com/ambuda-org/vidyut/{COMMIT}/"
FILES = {
    "vidyut-readme.md": RAW + "vidyut-prakriya/README.md",
    "vidyut-architecture.md": RAW + "vidyut-prakriya/ARCHITECTURE.md",
    "vidyut-license.md": RAW + "bindings-python/LICENSE.md",
    "vidyut-args-dhatu.rs": RAW + "vidyut-prakriya/src/args/dhatu.rs",
    "vidyut-args-krt.rs": RAW + "vidyut-prakriya/src/args/krt.rs",
    "vidyut-krt-basic.rs": RAW + "vidyut-prakriya/src/krt/basic.rs",
    "vidyut-args-taddhita.rs": RAW + "vidyut-prakriya/src/args/taddhita.rs",
    "vidyut-sanadi.rs": RAW + "vidyut-prakriya/src/sanadi.rs",
    "dhatupatha.tsv": RAW + "vidyut-prakriya/data/dhatupatha.tsv",
    "sutrapatha.tsv": RAW + "vidyut-prakriya/data/sutrapatha.tsv",
    "prakriya.pyi": RAW + "bindings-python/vidyut/prakriya.pyi",
    "test_prakriya.py": RAW + "bindings-python/test/integration/test_prakriya.py",
    "kashika_3_1.rs": RAW + "vidyut-prakriya/tests/integration/kashika_3_1.rs",
    "kashika_4_1.rs": RAW + "vidyut-prakriya/tests/integration/kashika_4_1.rs",
    "dhatu-concordance-about.html": "https://sanskrit.uohyd.ac.in/scl/dhaatupaatha/About.html",
    "dhatu-concordance.html": "https://sanskrit.uohyd.ac.in/scl/dhaatupaatha/compare_with_svara_prasanna.html",
    "dhatu-concordance-gana.html": "https://sanskrit.uohyd.ac.in/scl/dhaatupaatha/gaNa.html",
    "dhatupatha-sanskritdocuments.html": "https://sanskritdocuments.org/doc_z_misc_major_works/dhatupatha.html",
}
HERE = Path(__file__).resolve().parent
COMMENTARIES = (
    "mA6 mA37 mA48 mA105 mA203 mA265 mA292 mA360 mA365 mA368 "
    "mA493 mA494 mA511 mA549 mA586 mA603 mA645 mA698 mA704 mA727 "
    "mA732 mA773 mA783 mA795 mA894 mA1313 kRi1355 mA1347 mA1397 "
    "mA1431 mA1438 kRi111 kRi795 mA52 mA232 mA509 mA512 mA634 "
    "mA487 mA653 kRi677 XA691 mA821 kRi840 kRi720 XA737 "
    "kRi749 XA766 kRi754 XA770 "
    "mA1 mA1316 mA1359 mA418 mA1299 mA189 mA480 mA526 mA846 "
    "mA987 kRi1213 kRi911 mA1088 mA1351 mA257 mA1321 kRi1340 "
    "mA610 mA1014 mA601 mA1003 kRi527 XA538 kRi298 "
    "mA1294 mA596 mA745 mA398 mA1296 kRi1316 XA1349 mA433 mA924 "
    "mA811 mA1050 kRi181 mA1174 mA876 mA1121 mA43 kRi43 "
    "mA192 mA481 mA1322 mA1343 kRi1361 kRi201 kRi504 XA509 "
    "mA215 mA1158 mA1265 mA531 mA1029 mA650 mA809 mA421 mA1334 "
    "mA490 mA1169 kRi1184 mA491 mA1144 mA1340 kRi1358 mA1112 XA1167 mA1353 "
    "mA269 mA937 mA216 mA1225 mA219 mA1226 mA59 mA1348 "
    "mA287 mA1292 mA107 mA1307 mA112 mA1326 mA448 mA1301 mA1346 "
    "mA125 mA1295 mA518 mA1211 mA1241 kRi465 kRi466 mA970 mA1191 "
    "mA80 mA1286 XA1337 mA859 mA442 mA1209 kRi530 mA967 mA1193 "
    "mA289 mA907 mA492 mA1357 mA259 XA1263 mA341 mA1314 "
    "mA629 XA868 kRi928 XA949 mA1356 mA855"
).split()
packet_sources = HERE / "identity_commentary_sources.json"
if packet_sources.exists():
    COMMENTARIES.extend(json.loads(packet_sources.read_text()))
for code in COMMENTARIES:
    FILES[f"dhatu-{code}.html"] = f"https://sanskrit.uohyd.ac.in/scl/dhaatupaatha/files/{code}.html"
with (HERE / "operations.csv").open() as handle:
    RULES = {rule for row in csv.DictReader(handle) for rule in row["rule_refs"].split(";")}
RULES.update(rule for case in json.loads((HERE / "pilot_cases.json").read_text())
             for rule in case["rules"])
semantic_path = HERE / "semantic_sample.json"
if semantic_path.exists():
    RULES.update(rule for entry in json.loads(semantic_path.read_text())["entries"]
                 for rule in entry["rules"])
RULES.add("3.1.32")
RULES.update({
    "1.1.39", "1.1.40",
    "3.1.23", "3.1.24", "3.1.25", "3.1.124", "3.3.10",
    "3.1.134", "3.1.150", "3.2.105", "3.2.106", "3.2.107", "3.2.108",
    "3.2.109", "3.2.129",
    "3.3.94", "3.3.118", "3.3.174", "3.4.8", "3.4.9", "3.4.10",
    "3.4.11", "3.4.12", "3.4.13", "3.4.14", "3.4.15", "3.4.16",
    "3.4.17", "3.4.21", "3.4.22",
    "3.4.67", "7.1.37",
})
for rule in sorted(RULES, key=lambda code: tuple(map(int, code.split(".")))):
    FILES[f"rule-{rule}.html"] = (
        f"https://sanskritdocuments.org/learning_tools/ashtadhyayi/vyakhya/"
        f"{rule.split('.')[0]}/{rule}.htm"
    )


reconciliation_sources = HERE / "reconciliation_sources.json"
if reconciliation_sources.exists():
    FILES.update(json.loads(reconciliation_sources.read_text()))

remaining_sources = HERE / "remaining_followup_sources.json"
if remaining_sources.exists():
    FILES.update(json.loads(remaining_sources.read_text()))


def main():
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    manifest_path = ARCHIVE / "manifest.json"
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    records = []
    prior = {r["filename"]: r for r in previous.get("sources", [])}
    for name, url in FILES.items():
        path = ARCHIVE / name
        old = prior.get(name)
        if old and path.exists() and old["url"] == url:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest == old["sha256"]:
                records.append(old)
                continue
            raise ValueError(f"Archived source changed: {path}")
        payload = subprocess.run(
            ["curl", "-fLsS", "--retry", "2", "--max-time", "45", url],
            check=True, capture_output=True,
        ).stdout
        path.write_bytes(payload)
        records.append({
            "filename": name, "url": url,
            "accessed_utc": datetime.now(timezone.utc).isoformat(),
            "sha256": hashlib.sha256(payload).hexdigest(), "bytes": len(payload),
        })
        # Keep earlier records too if a later request interrupts this run.
        progress = {**prior, **{record["filename"]: record for record in records}}
        manifest_path.write_text(json.dumps({"generator_commit": COMMIT,
            "sources": list(progress.values())}, indent=2) + "\n")
    manifest_path.write_text(json.dumps({"generator_commit": COMMIT,
        "sources": records}, indent=2) + "\n")
    print(f"Archived {len(records)} sources in {ARCHIVE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

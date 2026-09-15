#!/usr/bin/env python3
"""Archive the rule pages governing literal plain taddhita source examples."""

from __future__ import annotations

from datetime import datetime, timezone
import csv
import hashlib
import json
from pathlib import Path
import subprocess

from taddhita_conditioned_common import ARCHIVE, HERE, RESULTS


SOURCE = RESULTS / "plain_taddhita_source_assertions.csv"
CONFIG = HERE / "plain_taddhita_operations.json"
GENERALIZATION_CONFIG = HERE / "taddhita_generalization_operations.json"
MANIFEST = ARCHIVE / "plain_taddhita_rule_manifest.json"
BASE = "https://sanskritdocuments.org/learning_tools/ashtadhyayi/vyakhya"


def main() -> None:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        rows = [
            row for row in csv.DictReader(handle)
            if row["assertion_status"] == "positive"
        ]
    config = json.loads(CONFIG.read_text())
    config_rules = {
        rule
        for operation in config["rule_operations"]
        for rule in (*operation["rules"], operation.get("canonical_rule", ""))
        if rule
    }
    if GENERALIZATION_CONFIG.exists():
        generalization = json.loads(GENERALIZATION_CONFIG.read_text())
        config_rules.update(
            rule
            for operation in (*generalization["operations"], *generalization.get("deferred_operations", []))
            for rule in operation["rule_refs"]
        )
    rules = sorted(
        {row["governing_rule"] for row in rows} | config_rules,
        key=lambda code: tuple(map(int, code.split("."))),
    )
    previous = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    prior = {row["filename"]: row for row in previous.get("sources", [])}
    records = []
    for rule in rules:
        name = f"plain-taddhita-rule-{rule}.html"
        url = f"{BASE}/{rule.split('.')[0]}/{rule}.htm"
        path = ARCHIVE / name
        old = prior.get(name)
        if old and path.exists() and old["url"] == url:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != old["sha256"]:
                raise ValueError(f"Archived source changed: {path}")
            records.append(old)
            continue
        payload = subprocess.run(
            ["curl", "-fLsS", "--retry", "2", "--max-time", "45", url],
            check=True,
            capture_output=True,
        ).stdout
        path.write_bytes(payload)
        records.append({
            "filename": name,
            "rule": rule,
            "url": url,
            "accessed_utc": datetime.now(timezone.utc).isoformat(),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "bytes": len(payload),
        })
    MANIFEST.write_text(json.dumps({"sources": records}, indent=2) + "\n")
    print(f"Archived {len(records)} governing rule pages in {ARCHIVE.relative_to(HERE.parents[1])}")


if __name__ == "__main__":
    main()

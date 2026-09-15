#!/usr/bin/env python3
"""Archive the rule pages used by the namadhatu expansion."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "namadhatu_manifest.json"
RULES = tuple(f"3.1.{number}" for number in range(8, 22))


def main() -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    previous = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    prior = {row["filename"]: row for row in previous.get("sources", [])}
    records = []
    for rule in RULES:
        name = f"rule-{rule}.html"
        url = f"https://sanskritdocuments.org/learning_tools/ashtadhyayi/vyakhya/3/{rule}.htm"
        path = ARCHIVE / name
        old = prior.get(name)
        if old and path.exists() and old["url"] == url:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != old["sha256"]:
                raise ValueError(f"Archived source changed: {path}")
            records.append(old)
            continue
        if path.exists():
            payload = path.read_bytes()
        else:
            payload = subprocess.run(
                ["curl", "-fLsS", "--retry", "2", "--max-time", "45", url],
                check=True,
                capture_output=True,
            ).stdout
            path.write_bytes(payload)
        records.append({
            "filename": name,
            "url": url,
            "accessed_utc": datetime.now(timezone.utc).isoformat(),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "bytes": len(payload),
        })
    MANIFEST.write_text(json.dumps({"sources": records}, indent=2) + "\n")
    print(f"Archived {len(records)} namadhatu rule pages.")


if __name__ == "__main__":
    main()

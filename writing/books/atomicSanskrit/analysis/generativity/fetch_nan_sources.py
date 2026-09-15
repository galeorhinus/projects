#!/usr/bin/env python3
"""Archive the primary grammatical sources used by the bounded nan pass."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "nan_manifest.json"
BASE = "https://sanskritdocuments.org/learning_tools/ashtadhyayi/vyakhya"
COMMIT = "f3ba4167d40eebc4b3023d24e66867aa6a8cdb32"
RAW = f"https://raw.githubusercontent.com/ambuda-org/vidyut/{COMMIT}/"
FILES = {
    "rule-2.2.6.html": f"{BASE}/2/2.2.6.htm",
    "rule-6.3.73.html": f"{BASE}/6/6.3.73.htm",
    "rule-6.3.74.html": f"{BASE}/6/6.3.74.htm",
    "vidyut-samasa.rs": RAW + "vidyut-prakriya/src/samasa.rs",
    "kashika_2_2.rs": RAW + "vidyut-prakriya/tests/integration/kashika_2_2.rs",
    "kashika_6_3.rs": RAW + "vidyut-prakriya/tests/integration/kashika_6_3.rs",
}


def main() -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    previous = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    prior = {row["filename"]: row for row in previous.get("sources", [])}
    records = []
    for name, url in FILES.items():
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
            check=True, capture_output=True,
        ).stdout
        path.write_bytes(payload)
        records.append({
            "filename": name,
            "url": url,
            "accessed_utc": datetime.now(timezone.utc).isoformat(),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "bytes": len(payload),
        })
    MANIFEST.write_text(json.dumps({"generator_commit": COMMIT, "sources": records}, indent=2) + "\n")
    print(f"Archived {len(records)} nan sources in {ARCHIVE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Archive the pinned implementation and rule sources used by the samasa pass."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

from samasa_common import ARCHIVE, COMMIT, MANIFEST


RAW = f"https://raw.githubusercontent.com/ambuda-org/vidyut/{COMMIT}/"
FILES = {
    "kashika_2_1.rs": RAW + "vidyut-prakriya/tests/integration/kashika_2_1.rs",
    "kashika_2_2.rs": RAW + "vidyut-prakriya/tests/integration/kashika_2_2.rs",
    "vidyut-samasa.rs": RAW + "vidyut-prakriya/src/samasa.rs",
    "vidyut-args-samasa.rs": RAW + "vidyut-prakriya/src/args/samasa.rs",
    "vidyut-vyakarana.rs": RAW + "vidyut-prakriya/src/vyakarana.rs",
    "vidyut-test-utils.rs": RAW + "vidyut-prakriya/test_utils/src/lib.rs",
    "vidyut-sutrapatha.tsv": RAW + "vidyut-prakriya/data/sutrapatha.tsv",
}

RULES = (
    "2.1.1", "2.1.5", "2.1.7", "2.1.8", "2.1.9", "2.1.10", "2.1.13",
    "2.1.14", "2.1.15", "2.1.19", "2.1.24", "2.1.25", "2.1.26",
    "2.1.27", "2.1.30", "2.1.31", "2.1.32", "2.1.33", "2.1.34",
    "2.1.36", "2.1.37", "2.1.38", "2.1.40", "2.1.41", "2.1.42",
    "2.1.47", "2.1.58", "2.1.61", "2.1.62", "2.1.64", "2.1.67",
    "2.2.6", "2.2.8", "2.2.24", "2.2.29",
)
for rule in RULES:
    FILES[f"rule-{rule}.html"] = (
        f"https://sanskritdocuments.org/learning_tools/ashtadhyayi/vyakhya/2/{rule}.htm"
    )


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
    MANIFEST.write_text(json.dumps({"generator_commit": COMMIT, "sources": records}, indent=2) + "\n")
    print(f"Archived {len(records)} samasa sources.")


if __name__ == "__main__":
    main()

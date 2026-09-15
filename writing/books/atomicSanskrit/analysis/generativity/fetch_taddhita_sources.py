#!/usr/bin/env python3
"""Archive the pinned implementation and tests used by the taddhita expansion."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "taddhita_manifest.json"
COMMIT = "f3ba4167d40eebc4b3023d24e66867aa6a8cdb32"
RAW = f"https://raw.githubusercontent.com/ambuda-org/vidyut/{COMMIT}/"
FILES = {
    "vidyut-taddhita.rs": RAW + "vidyut-prakriya/src/taddhita.rs",
    "vidyut-taddhita-matvartha.rs": RAW + "vidyut-prakriya/src/taddhita/matvartha_prakarana.rs",
    "vidyut-taddhita-nan-snan.rs": RAW + "vidyut-prakriya/src/taddhita/nan_snan_adhikara_prakarana.rs",
    "vidyut-taddhita-panchami.rs": RAW + "vidyut-prakriya/src/taddhita/panchami_prakarana.rs",
    "vidyut-taddhita-pragdishiya.rs": RAW + "vidyut-prakriya/src/taddhita/pragdishiya.rs",
    "vidyut-taddhita-pragdivyatiya.rs": RAW + "vidyut-prakriya/src/taddhita/pragdivyatiya.rs",
    "vidyut-taddhita-pragghitiya.rs": RAW + "vidyut-prakriya/src/taddhita/pragghitiya.rs",
    "vidyut-taddhita-pragiviya.rs": RAW + "vidyut-prakriya/src/taddhita/pragiviya.rs",
    "vidyut-taddhita-pragvahatiya.rs": RAW + "vidyut-prakriya/src/taddhita/pragvahatiya.rs",
    "vidyut-taddhita-pragvatiya.rs": RAW + "vidyut-prakriya/src/taddhita/pragvatiya.rs",
    "vidyut-taddhita-prakkritiya.rs": RAW + "vidyut-prakriya/src/taddhita/prakkritiya.rs",
    "vidyut-taddhita-samasanta.rs": RAW + "vidyut-prakriya/src/taddhita/samasanta_prakarana.rs",
    "vidyut-taddhita-svarthika.rs": RAW + "vidyut-prakriya/src/taddhita/svarthika_prakarana.rs",
    "vidyut-taddhita-utils.rs": RAW + "vidyut-prakriya/src/taddhita/utils.rs",
    "kashika_4_2.rs": RAW + "vidyut-prakriya/tests/integration/kashika_4_2.rs",
    "kashika_4_3.rs": RAW + "vidyut-prakriya/tests/integration/kashika_4_3.rs",
    "kashika_4_4.rs": RAW + "vidyut-prakriya/tests/integration/kashika_4_4.rs",
    "kashika_5_1.rs": RAW + "vidyut-prakriya/tests/integration/kashika_5_1.rs",
    "kashika_5_2.rs": RAW + "vidyut-prakriya/tests/integration/kashika_5_2.rs",
    "kashika_5_3.rs": RAW + "vidyut-prakriya/tests/integration/kashika_5_3.rs",
    "kashika_5_4.rs": RAW + "vidyut-prakriya/tests/integration/kashika_5_4.rs",
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
    print(f"Archived {len(records)} taddhita sources in {ARCHIVE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

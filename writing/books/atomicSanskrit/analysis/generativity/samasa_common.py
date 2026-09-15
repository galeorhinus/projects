"""Shared paths and helpers for the bounded samasa source pass."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ANALYSIS = ROOT / "analysis/generativity"
RESULTS = ANALYSIS / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
MANIFEST = ARCHIVE / "samasa_manifest.json"
SOURCE_FILES = (ARCHIVE / "kashika_2_1.rs", ARCHIVE / "kashika_2_2.rs")
CURRENT_SUBTOTAL = 12_845_387
COMMIT = "f3ba4167d40eebc4b3023d24e66867aa6a8cdb32"


HELPERS = {
    "assert_has_avyayibhava": ("avyayibhava", "indeclinable relation of {a} to {b}"),
    "assert_has_avyaya_tatpurusha": ("avyaya_tatpurusha", "{b} qualified by the indeclinable {a}"),
    "assert_has_dvitiya_tatpurusha": ("dvitiya_tatpurusha", "{b} directed toward or involving {a}"),
    "assert_has_trtiya_tatpurusha": ("trtiya_tatpurusha", "{b} by, with, or through {a}"),
    "assert_has_caturthi_tatpurusha": ("caturthi_tatpurusha", "{b} for {a}"),
    "assert_has_panchami_tatpurusha": ("panchami_tatpurusha", "{b} from or because of {a}"),
    "assert_has_sasthi_tatpurusha": ("sasthi_tatpurusha", "{b} of {a}"),
    "assert_has_saptami_tatpurusha": ("saptami_tatpurusha", "{b} in or upon {a}"),
    "assert_has_karmadharaya": ("karmadharaya", "{b} qualified or identified by {a}"),
    "assert_has_bahuvrihi": ("bahuvrihi", "one characterized by {a} and {b}"),
    "assert_has_dvandva": ("dvandva", "{members} together"),
    "assert_has_samahara_dvandva": ("samahara_dvandva", "the collection of {members}"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(*parts: str) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def project_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


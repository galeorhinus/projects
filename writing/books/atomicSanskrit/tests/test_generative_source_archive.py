import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "generativity_fetch", ROOT / "analysis/generativity/fetch_pilot_sources.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SourceArchiveTests(unittest.TestCase):
    def test_interrupted_fetch_preserves_existing_manifest_records(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory)
            payload = b"existing source"
            old = {"filename": "old.html", "url": "https://example.test/old",
                   "sha256": hashlib.sha256(payload).hexdigest(),
                   "accessed_utc": "2026-09-12T00:00:00+00:00", "bytes": len(payload)}
            (archive / "old.html").write_bytes(payload)
            manifest = archive / "manifest.json"
            manifest.write_text(json.dumps({"sources": [old]}))
            files = {"new.html": "https://example.test/new",
                     "failed.html": "https://example.test/failed",
                     "old.html": old["url"]}
            responses = [subprocess.CompletedProcess([], 0, stdout=b"new source"),
                         subprocess.CalledProcessError(22, "curl")]
            with patch.object(MODULE, "ARCHIVE", archive), patch.object(MODULE, "FILES", files), \
                    patch.object(MODULE.subprocess, "run", side_effect=responses):
                with self.assertRaises(subprocess.CalledProcessError):
                    MODULE.main()
            records = {r["filename"]: r for r in json.loads(manifest.read_text())["sources"]}
            self.assertEqual(records["old.html"], old)
            self.assertEqual(records["new.html"]["sha256"], hashlib.sha256(b"new source").hexdigest())
            self.assertNotIn("failed.html", records)


if __name__ == "__main__":
    unittest.main()

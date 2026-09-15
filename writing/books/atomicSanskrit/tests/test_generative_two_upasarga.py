import csv
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/generativity/build_two_upasarga_ledger.py"
RESULTS = ROOT / "analysis/generativity/results"


class TwoUpasargaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
        cls.report = json.loads((RESULTS / "two_upasarga_summary.json").read_text())

    def test_candidate_arithmetic(self):
        self.assertEqual(self.report["base_word_meanings"], 2634)
        self.assertEqual(self.report["ordered_upasarga_sequences"], 400)
        self.assertEqual(self.report["structural_base_candidates"], 1053600)
        self.assertEqual(self.report["documented_base_meaning_conflicts"], 2680)
        self.assertEqual(self.report["source_attested_enrichment_meanings"], 420)

    def test_admitted_total(self):
        expected = 1053600 - 2680 + 420
        self.assertEqual(self.report["admitted_two_upasarga_word_meanings"], expected)
        self.assertEqual(self.report["unresolved_zero_output_meanings"], 0)

    def test_compressed_ledgers_match_report(self):
        with gzip.open(RESULTS / "two_upasarga_ledger.csv.gz", "rt", encoding="utf-8") as handle:
            admitted = sum(1 for _ in csv.DictReader(handle))
        with gzip.open(RESULTS / "two_upasarga_exclusions.csv.gz", "rt", encoding="utf-8") as handle:
            excluded = sum(1 for _ in csv.DictReader(handle))
        self.assertEqual(admitted, self.report["admitted_two_upasarga_word_meanings"])
        self.assertEqual(excluded, self.report["documented_base_meaning_conflicts"])

    def test_subtotal_reconciles(self):
        self.assertEqual(
            self.report["bounded_verbal_capacity_subtotal"],
            self.report["prior_bounded_verbal_capacity_subtotal"]
            + self.report["admitted_two_upasarga_word_meanings"],
        )

    def test_two_prefix_scope_is_explicitly_bounded(self):
        self.assertIn("declared computational bound", self.report["scope"])
        self.assertIn("1.4.80", self.report["sequence_policy"])
        self.assertIn("6.4.96", self.report["sequence_policy"])
        self.assertIn("outer upasarga, then inner upasarga, then dhatu", self.report["sequence_policy"])
        manifest = json.loads((ROOT / "working/40_reference/sources/archive/documents/generativity-pilot/upasarga_stacking_manifest.json").read_text())
        self.assertEqual(len(manifest["sources"]), 1)
        record = manifest["sources"][0]
        source = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot" / record["filename"]
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), record["sha256"])


if __name__ == "__main__":
    unittest.main()

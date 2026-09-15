import csv
import gzip
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/generativity/build_upasarga_sanadi_ledger.py"
RESULTS = ROOT / "analysis/generativity/results"


class UpasargaSanadiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
        cls.report = json.loads((RESULTS / "upasarga_sanadi_summary.json").read_text())
        with gzip.open(RESULTS / "upasarga_sanadi_ledger.csv.gz", "rt", encoding="utf-8") as handle:
            cls.ledger = list(csv.DictReader(handle))
        with gzip.open(RESULTS / "upasarga_sanadi_exclusions.csv.gz", "rt", encoding="utf-8") as handle:
            cls.excluded = list(csv.DictReader(handle))

    def test_scope_and_identity(self):
        self.assertEqual(self.report["normalized_upasarga_identities"], 20)
        self.assertEqual(self.report["admitted_one_sanadi_meanings"], 12522)
        ids = [row["stacked_word_meaning_id"] for row in self.ledger]
        self.assertEqual(len(ids), len(set(ids)))

    def test_count_reconciles(self):
        self.assertEqual(len(self.ledger), self.report["admitted_stacked_word_meanings"])
        self.assertEqual(
            self.report["bounded_verbal_capacity_subtotal"],
            self.report["prior_bounded_verbal_capacity_subtotal"] + len(self.ledger),
        )

    def test_only_documented_conflicts_or_zero_outputs_are_excluded(self):
        self.assertEqual(len(self.excluded), sum(self.report["not_admitted_by_status"].values()))
        self.assertTrue(all(row["count_status"] in {
            "not_counted_documented_base_meaning_conflict",
            "not_admitted_engine_zero_unresolved",
        } for row in self.excluded))

    def test_attestation_is_not_an_admission_gate(self):
        self.assertIn("Attestation is not required", self.report["admission_standard"])
        self.assertTrue(all(row["count_status"] == "admitted_generated_capacity" for row in self.ledger))


if __name__ == "__main__":
    unittest.main()

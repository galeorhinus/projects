import gzip
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis/generativity/results"


class SanadiKrdantaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(
            [sys.executable, str(ROOT / "analysis/generativity/build_sanadi_krdanta_ledger.py")],
            cwd=ROOT, check=True, capture_output=True,
        )
        cls.report = json.loads((RESULTS / "sanadi_krdanta_summary.json").read_text())

    def test_scope_and_ledger_reconcile(self):
        self.assertEqual(self.report["source_one_sanadi_word_meanings"], 12522)
        self.assertEqual(self.report["source_curadi_true_causative_word_meanings"], 522)
        self.assertEqual(self.report["source_sanadi_word_meanings"], 13044)
        self.assertEqual(self.report["selected_semantic_operations"], 14)
        self.assertEqual(self.report["structural_operation_candidates"], 13044 * 14)
        with gzip.open(RESULTS / "sanadi_krdanta_ledger.csv.gz", "rt") as handle:
            admitted = sum(1 for _ in handle) - 1
        with gzip.open(RESULTS / "sanadi_krdanta_exclusions.csv.gz", "rt") as handle:
            excluded = sum(1 for _ in handle) - 1
        self.assertEqual(admitted, self.report["admitted_sanadi_krdanta_word_meanings"])
        self.assertEqual(excluded, self.report["not_admitted_total"])
        self.assertEqual(admitted + excluded, self.report["structural_operation_candidates"])

    def test_subtotal_reconciles(self):
        self.assertEqual(
            self.report["bounded_word_meaning_subtotal"],
            self.report["prior_bounded_word_meaning_subtotal"]
            + self.report["admitted_sanadi_krdanta_word_meanings"],
        )


if __name__ == "__main__":
    unittest.main()

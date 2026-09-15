import csv
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis/generativity/results"


class ConditionedKrdantaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "analysis/generativity/build_conditioned_krdanta_ledger.py")], cwd=ROOT, check=True, capture_output=True)
        cls.report = json.loads((RESULTS / "conditioned_krdanta_summary.json").read_text())
        with (RESULTS / "conditioned_krdanta_ledger.csv").open() as handle:
            cls.rows = list(csv.DictReader(handle))
        with (RESULTS / "conditioned_krdanta_exclusions.csv").open() as handle:
            cls.excluded = list(csv.DictReader(handle))

    def test_ledger_reconciles(self):
        self.assertEqual(len(self.rows), self.report["admitted_conditioned_krdanta_word_meanings"])
        self.assertEqual(len(self.excluded), self.report["not_admitted_total"])
        self.assertEqual(len(self.rows) + len(self.excluded), self.report["structural_operation_candidates"])

    def test_semantic_operations_remain_separate(self):
        self.assertEqual(self.report["selected_identifiers"], 7)
        self.assertEqual(self.report["selected_semantic_operations"], 10)
        self.assertEqual(len({row["derived_word_meaning_id"] for row in self.rows}), len(self.rows))
        self.assertEqual(self.report["admitted_by_operation"]["habit_canas"], self.report["admitted_by_operation"]["capacity_canas"])

    def test_subtotal_reconciles(self):
        self.assertEqual(
            self.report["bounded_word_meaning_subtotal"],
            self.report["prior_bounded_word_meaning_subtotal"] + len(self.rows),
        )


if __name__ == "__main__":
    unittest.main()

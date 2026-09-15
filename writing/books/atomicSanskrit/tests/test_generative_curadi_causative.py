import csv
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/generativity/build_curadi_causative_ledger.py"
RESULTS = ROOT / "analysis/generativity/results"


class CuradiCausativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
        cls.report = json.loads((RESULTS / "curadi_causative_summary.json").read_text())
        with (RESULTS / "curadi_causative_ledger.csv").open() as handle:
            cls.ledger = list(csv.DictReader(handle))
        with (RESULTS / "curadi_causative_exclusions.csv").open() as handle:
            cls.excluded = list(csv.DictReader(handle))

    def test_all_curadi_candidates_are_resolved(self):
        self.assertEqual(self.report["candidate_curadigana_base_meanings"], 522)
        self.assertEqual(self.report["admitted_true_causative_word_meanings"], 522)
        self.assertEqual(self.report["unresolved_word_meanings"], 0)
        self.assertEqual(len(self.ledger), 522)
        self.assertEqual(len(self.excluded), 0)

    def test_stacked_nic_is_explicit(self):
        self.assertTrue(all(row["rule_refs"] == "3.1.25;3.1.26" for row in self.ledger))
        self.assertTrue(all(row["operation_id"] == "curadi_true_causative" for row in self.ledger))

    def test_subtotal_reconciles(self):
        self.assertEqual(
            self.report["bounded_verbal_capacity_subtotal"],
            self.report["prior_bounded_verbal_capacity_subtotal"] + len(self.ledger),
        )


if __name__ == "__main__":
    unittest.main()

import csv
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/generativity/build_krdanta_ledger.py"
RESULTS = ROOT / "analysis/generativity/results"


class KrdantaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
        cls.report = json.loads((RESULTS / "krdanta_summary.json").read_text())
        with (RESULTS / "krdanta_ledger.csv").open() as handle:
            cls.ledger = list(csv.DictReader(handle))
        with (RESULTS / "krdanta_exclusions.csv").open() as handle:
            cls.excluded = list(csv.DictReader(handle))

    def test_scope(self):
        self.assertEqual(self.report["base_word_meanings"], 2634)
        self.assertEqual(self.report["selected_krt_identifiers"], 12)
        self.assertEqual(self.report["selected_semantic_operations"], 14)
        self.assertEqual(self.report["structural_operation_candidates"], 36876)

    def test_ledger_reconciles(self):
        self.assertEqual(len(self.ledger), self.report["admitted_krdanta_word_meanings"])
        self.assertEqual(len(self.excluded), self.report["not_admitted_total"])
        self.assertEqual(len(self.ledger) + len(self.excluded), self.report["structural_operation_candidates"])

    def test_word_meaning_ids_are_unique(self):
        ids = [row["derived_word_meaning_id"] for row in self.ledger]
        self.assertEqual(len(ids), len(set(ids)))

    def test_general_operations_cover_all_bases(self):
        full = {"agent_nvul", "agent_trc", "action_lyut", "instrument_lyut", "location_lyut", "completed_kta", "completed_agent_ktavatu", "obligation_tavya", "obligation_aniyar"}
        for operation_id in full:
            self.assertEqual(self.report["admitted_by_operation"][operation_id], 2634)
            self.assertNotIn(operation_id, self.report["not_admitted_by_operation"])

    def test_no_attestation_gate(self):
        self.assertIn("does not exclude", self.report["admission_standard"])

    def test_combined_subtotal_reconciles(self):
        self.assertEqual(
            self.report["bounded_word_meaning_subtotal"],
            self.report["prior_bounded_verbal_capacity_subtotal"] + len(self.ledger),
        )


if __name__ == "__main__":
    unittest.main()

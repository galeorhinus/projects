import csv
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis/generativity/results"


class TaddhitaPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(
            [sys.executable, str(ROOT / "analysis/generativity/build_nominal_taddhita_pilot.py")],
            cwd=ROOT, check=True, capture_output=True,
        )
        cls.report = json.loads((RESULTS / "taddhita_pilot_summary.json").read_text())

    def test_declared_boundary_and_ledger_reconcile(self):
        self.assertEqual(self.report["nominal_input_count"], 5)
        self.assertEqual(self.report["selected_taddhita_semantic_operations"], 3)
        self.assertEqual(self.report["eligible_operation_candidates"], 7)
        with (RESULTS / "taddhita_pilot_ledger.csv").open() as handle:
            admitted = list(csv.DictReader(handle))
        with (RESULTS / "taddhita_pilot_exclusions.csv").open() as handle:
            excluded = list(csv.DictReader(handle))
        self.assertEqual(len(admitted), self.report["admitted_taddhita_word_meanings"])
        self.assertEqual(len(excluded), self.report["not_admitted_total"])
        self.assertEqual(len(admitted) + len(excluded), 7)

    def test_expected_pilot_outputs(self):
        with (RESULTS / "taddhita_pilot_ledger.csv").open() as handle:
            rows = list(csv.DictReader(handle))
        actual = {
            (row["nominal_id"], row["operation_id"]): row["output_forms_slp1"]
            for row in rows
        }
        self.assertEqual(actual[("kunti", "descendant_dhak")], "kOnteya")
        self.assertEqual(actual[("go", "state_tva")], "gotva")
        self.assertEqual(actual[("go", "state_tal")], "gotA")

    def test_pilot_subtotal_reconciles(self):
        self.assertEqual(
            self.report["bounded_word_meaning_subtotal_including_pilot"],
            self.report["prior_bounded_word_meaning_subtotal"]
            + self.report["admitted_taddhita_word_meanings"],
        )


if __name__ == "__main__":
    unittest.main()

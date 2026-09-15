import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis/generativity/results"


class TwelvePassSummaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(
            [sys.executable, str(ROOT / "analysis/generativity/build_twelve_pass_summary.py")],
            cwd=ROOT, check=True, capture_output=True,
        )
        cls.report = json.loads((RESULTS / "twelve_pass_expansion_summary.json").read_text())

    def test_passes_and_total(self):
        self.assertEqual(self.report["first_six_pass_subtotal"], 1399621)
        self.assertEqual(len(self.report["second_six_passes"]), 6)
        self.assertEqual(
            sum(row["word_meanings"] for row in self.report["second_six_passes"]),
            775100,
        )
        self.assertEqual(self.report["bounded_word_meaning_subtotal"], 2174721)

    def test_domain_boundary(self):
        self.assertEqual(
            self.report["domain"],
            "laukika_generation_mode_over_current_base_inventory",
        )
        self.assertIn("Nineteen Vedic-only", self.report["vedic_boundary"])
        self.assertTrue(self.report["not_a_complete_sanskrit_vocabulary_total"])


if __name__ == "__main__":
    unittest.main()

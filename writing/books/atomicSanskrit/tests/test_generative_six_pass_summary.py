import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/generativity/build_six_pass_summary.py"
RESULT = ROOT / "analysis/generativity/results/six_pass_expansion_summary.json"


class SixPassSummaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
        cls.report = json.loads(RESULT.read_text())

    def test_six_layers_reconcile(self):
        self.assertEqual(len(self.report["layers"]), 6)
        self.assertEqual(sum(row["word_meanings"] for row in self.report["layers"]), 1399621)
        self.assertEqual(self.report["bounded_word_meaning_subtotal"], 1399621)

    def test_scope_remains_explicit(self):
        self.assertTrue(self.report["not_a_complete_sanskrit_vocabulary_total"])
        self.assertIn("laukika avyayas", self.report["remaining_major_layers"])
        self.assertIn("tin and sup inflection, reported separately from word-meanings", self.report["remaining_major_layers"])


if __name__ == "__main__":
    unittest.main()

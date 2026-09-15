import csv
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis/generativity/results"


class ConditionedKrtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "analysis/generativity/classify_conditioned_krt.py")], cwd=ROOT, check=True, capture_output=True)
        cls.report = json.loads((RESULTS / "conditioned_krt_classification.json").read_text())
        with (RESULTS / "conditioned_krt_classification.csv").open() as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_every_deferred_identifier_is_classified(self):
        self.assertEqual(len(self.rows), 87)
        self.assertEqual(len({row["source_variant"] for row in self.rows}), 87)
        self.assertEqual(sum(self.report["engine_path_classification_counts"].values()), 87)

    def test_only_source_defined_operations_are_selected(self):
        self.assertEqual(self.report["selected_identifiers"], 7)
        self.assertEqual(self.report["selected_semantic_operations"], 10)
        selected = {row["source_variant"] for row in self.rows if row["count_status"] == "selected_for_bounded_semantic_generation"}
        self.assertEqual(selected, {"ac", "kelimar", "vun", "cAnaS", "ktin", "Ga", "ktic"})

    def test_zero_output_is_not_called_prohibition(self):
        self.assertIn("does not prove prohibition", self.report["classification_boundary"])


if __name__ == "__main__":
    unittest.main()

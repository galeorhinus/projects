import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/generativity/run_sanadi_eligibility.py"
RESULTS = ROOT / "analysis/generativity/results"
HAS_ENGINE = importlib.util.find_spec("vidyut") is not None


@unittest.skipUnless(HAS_ENGINE, "Use build/generativity-venv/bin/python for integration tests")
class SanadiEligibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
        cls.report = json.loads((RESULTS / "sanadi_eligibility.json").read_text())
        with (RESULTS / "sanadi_engine_results.csv").open() as handle:
            cls.engine_rows = list(csv.DictReader(handle))
        with (RESULTS / "sanadi_candidate_meanings.csv").open() as handle:
            cls.candidates = list(csv.DictReader(handle))

    def test_scope_and_current_base_count(self):
        self.assertEqual(self.report["engine"]["version"], "0.4.0")
        self.assertEqual(self.report["source_entries_tested"], 2229)
        self.assertEqual(self.report["current_base_word_meanings"], 2634)
        self.assertEqual(self.report["preserved_assignment_rows"], 2741)
        self.assertEqual(len(self.engine_rows), 2229 * 4)

    def test_operation_coverage_is_stable(self):
        rows = {row["operation_id"]: row for row in self.report["verbal_operations"]}
        expected = {
            "causative": (2229, 0, 2634, 2634),
            "desiderative": (2229, 0, 2634, 2634),
            "intensive": (1775, 454, 2099, 2099),
            "intensive_luk": (1775, 454, 2099, 2099),
        }
        for operation, values in expected.items():
            row = rows[operation]
            actual = (row["source_entries_with_output"], row["source_entries_with_zero_output"],
                      row["base_word_meanings_with_output"], row["candidate_derived_word_meanings"])
            self.assertEqual(actual, values, operation)

    def test_candidates_are_not_admitted(self):
        self.assertIsNone(self.report["vocabulary_total"])
        self.assertTrue(self.report["candidate_rows_are_not_a_count"])
        self.assertTrue(all(row["count_status"] == "not_admitted" for row in self.engine_rows))
        self.assertTrue(all(row["count_status"] == "not_admitted" for row in self.candidates))

    def test_missing_meaning_entries_are_explicit(self):
        self.assertEqual(self.report["source_entries_without_admitted_meaning"], ["01.0900", "01.0930", "01.0951"])

    def test_known_anabhidhana_control_remains_unadmitted(self):
        control = self.report["known_semantic_control"]
        self.assertEqual(control["rule"], "3.1.22")
        self.assertEqual(control["engine_outputs"]["01.0847 ruc"], ["rorucya", "roruc"])
        self.assertIn("do not admit", control["disposition"])

    def test_word_meaning_key_does_not_collapse_homographs(self):
        by_output = {}
        for row in self.candidates:
            for output in row["output_forms_slp1"].split(";"):
                by_output.setdefault((row["operation_id"], output), set()).add(row["base_count_key"])
        self.assertTrue(any(len(keys) > 1 for keys in by_output.values()))

    def test_alternative_forms_do_not_multiply_a_candidate(self):
        self.assertTrue(any(int(row["output_variant_count"]) > 1 for row in self.candidates))
        keys = [(row["operation_id"], row["base_count_key"]) for row in self.candidates]
        self.assertEqual(len(keys), len(set(keys)))


if __name__ == "__main__":
    unittest.main()

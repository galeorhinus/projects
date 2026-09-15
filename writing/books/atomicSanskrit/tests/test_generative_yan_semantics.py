import csv
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/generativity/review_yan_semantics.py"
RESULTS = ROOT / "analysis/generativity/results"


class YanSemanticReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
        cls.report = json.loads((RESULTS / "yan_semantic_review.json").read_text())
        with (RESULTS / "yan_movement_candidates.csv").open() as handle:
            cls.movement = list(csv.DictReader(handle))

    def test_engine_path_counts_are_stable(self):
        self.assertEqual(
            self.report["engine_coverage"]["source_entries"],
            {"3.1.22": 1754, "3.1.24": 12, "varttika_3.1.22.1": 9, "zero_output": 454},
        )
        self.assertEqual(
            self.report["engine_coverage"]["reconciled_base_meanings"],
            {"3.1.22": 2072, "3.1.24": 15, "varttika_3.1.22.1": 12, "zero_output": 559},
        )

    def test_rule_3123_gap_is_explicit(self):
        coverage = self.report["engine_coverage"]
        self.assertEqual(coverage["rule_3.1.23_engine_path_entries"], 0)
        self.assertIn("does not implement", coverage["rule_3.1.23_gap"])

    def test_movement_screen_cannot_change_the_count(self):
        self.assertGreater(len(self.movement), 0)
        self.assertTrue(all(row["semantic_status"] == "review_required_not_counted" for row in self.movement))
        self.assertEqual(
            len({row["base_count_key"] for row in self.movement}),
            self.report["engine_coverage"]["movement_screen_unique_base_meanings"],
        )

    def test_proposals_are_unapplied(self):
        self.assertEqual(self.report["status"], "semantic_proposals_only_not_applied")
        self.assertIsNone(self.report["vocabulary_total"])
        self.assertFalse(self.report["published_total_changed"])
        self.assertTrue(all(row["status"] == "pending_author_approval" for row in self.report["proposals"]))

    def test_yan_luk_inherits_semantics_without_a_new_multiplier(self):
        proposal = next(row for row in self.report["proposals"] if row["id"] == "YAN-P5")
        self.assertIn("separate derived verbal word", proposal["proposal"])
        self.assertIn("inherit", proposal["proposal"])
        self.assertIn("does not create another meaning multiplier", proposal["proposal"])

    def test_sources_and_hashes_are_retained(self):
        manifest = json.loads((ROOT / "working/40_reference/sources/archive/documents/generativity-pilot/manifest.json").read_text())
        self.assertEqual(self.report["manifest_source_count"], len(manifest["sources"]))
        self.assertEqual(len(self.report["sources"]), 6)
        self.assertTrue(all(row["url"] and len(row["sha256"]) == 64 for row in self.report["sources"]))
        self.assertIn("analysis/generativity/review_yan_semantics.py", self.report["inputs"])

    def test_anabhidhana_control_remains_outside_the_count(self):
        control = self.report["known_anabhidhana_control"]
        self.assertEqual(control["count_status"], "not_admitted")
        self.assertEqual(control["source_entries"], ["01.0847 ruc", "06.0046 shubh"])


if __name__ == "__main__":
    unittest.main()

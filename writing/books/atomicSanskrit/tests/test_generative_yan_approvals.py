import csv
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/generativity/apply_yan_semantic_approvals.py"
RESULTS = ROOT / "analysis/generativity/results"


class YanSemanticApprovalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
        cls.report = json.loads((RESULTS / "yan_semantic_approval.json").read_text())
        with (RESULTS / "yan_movement_classification.csv").open() as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_all_proposals_are_approved(self):
        self.assertEqual(cls_ids := self.report["approved_proposal_ids"], [
            "YAN-P1", "YAN-P2", "YAN-P3", "YAN-P4", "YAN-P5"
        ])
        self.assertEqual(len(cls_ids), len(set(cls_ids)))

    def test_every_unique_movement_candidate_is_reviewed_once(self):
        self.assertEqual(len(self.rows), 312)
        self.assertEqual(len({row["base_count_key"] for row in self.rows}), 312)
        self.assertEqual(self.report["movement_queue"]["unique_base_meanings_reviewed"], 312)

    def test_classification_counts_are_stable(self):
        self.assertEqual(
            self.report["movement_queue"]["classification_counts"],
            {"direct_movement": 289, "not_movement": 23},
        )

    def test_no_rule_3123_scope_questions_remain(self):
        deferred = [row for row in self.rows if row["classification"] == "deferred_scope"]
        self.assertEqual(deferred, [])

    def test_rule_classification_does_not_admit_vocabulary(self):
        status = self.report["count_status"]
        self.assertIsNone(status["vocabulary_total"])
        self.assertEqual(status["derived_word_meanings_admitted"], 0)
        self.assertFalse(status["published_total_changed"])

    def test_yan_luk_policy_preserves_inherited_meaning(self):
        policy = self.report["semantic_model"]["yaNluk"]
        self.assertIn("separate derived verbal word", policy)
        self.assertIn("inheriting", policy)
        self.assertIn("no additional meaning multiplier", policy)

    def test_inputs_have_hashes(self):
        self.assertEqual(len(self.report["inputs"]), 4)
        self.assertTrue(all(len(value) == 64 for value in self.report["inputs"].values()))


if __name__ == "__main__":
    unittest.main()

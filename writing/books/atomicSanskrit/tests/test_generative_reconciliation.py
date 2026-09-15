import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
HAS_ENGINE = importlib.util.find_spec("vidyut") is not None
if HAS_ENGINE:
    sys.path.insert(0, str(ROOT / "analysis/generativity"))
    try:
        import review_reconciliation as MODULE
    finally:
        sys.path.pop(0)


@unittest.skipUnless(HAS_ENGINE, "Use build/generativity-venv/bin/python")
class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.review = json.loads(MODULE.REVIEW.read_text())

    def test_ten_proposals_preserve_original_count_and_inputs(self):
        paths = [MODULE.HERE / "identity_review.json",
                 MODULE.RESULTS / "base_meaning_assignments.csv",
                 MODULE.RESULTS / "base_meanings.json", MODULE.ARCHIVE / "dhatupatha.tsv"]
        before = {p: MODULE.sha(p) for p in paths}
        original = copy.deepcopy(self.review)
        report = MODULE.build_report(self.review)
        self.assertEqual(self.review, original)
        self.assertEqual(before, {p: MODULE.sha(p) for p in paths})
        self.assertEqual(len(report["cases"]), 10)
        self.assertEqual((report["baseline"], report["proposed_subtotal"]), (2653, 2649))
        self.assertEqual(report["proposed_delta"], -4)
        self.assertIsNone(report["vocabulary_total"])
        self.assertEqual({c["id"] for c in report["cases"] if c["delta"]},
                         {"IR141", "IR170", "IR194", "IR211"})
        self.assertTrue(all(e["record"]["sha256"] and e["record"]["url"]
                            for c in report["cases"] for e in c["evidence"]))

    def test_saved_report_matches_validated_sources(self):
        report = MODULE.build_report()
        saved = json.loads((MODULE.RESULTS / "reconciliation_review_01.json").read_text())
        self.assertEqual(saved, report)
        self.assertEqual((MODULE.RESULTS / "reconciliation_review_01.md").read_text(), MODULE.render(report))

    def test_wrong_anchor_is_rejected(self):
        self.review["cases"][0]["evidence"][0]["anchor"] = "INVENTED EVIDENCE"
        with self.assertRaisesRegex(ValueError, "missing anchor"):
            MODULE.build_report(self.review)

    def test_changed_baseline_is_rejected(self):
        self.review["baseline"] = 2649
        with self.assertRaisesRegex(ValueError, "Baseline changed"):
            MODULE.build_report(self.review)

    def test_duplicate_cases_are_rejected(self):
        self.review["cases"].append(copy.deepcopy(self.review["cases"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            MODULE.build_report(self.review)

    def test_count_drift_is_rejected(self):
        self.review["cases"][0]["before_count"] = 1
        with self.assertRaisesRegex(ValueError, "current count"):
            MODULE.build_report(self.review)

    def test_reporter_cannot_apply_changes(self):
        self.review["status"] = "applied"
        with self.assertRaisesRegex(ValueError, "cannot apply"):
            MODULE.build_report(self.review)


if __name__ == "__main__":
    unittest.main()

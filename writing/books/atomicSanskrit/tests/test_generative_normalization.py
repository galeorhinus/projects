import copy
import csv
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
        import apply_reconciliation as APP
        import review_followups_02 as FOLLOWUP
    finally:
        sys.path.pop(0)


@unittest.skipUnless(HAS_ENGINE, "Use build/generativity-venv/bin/python")
class NormalizationTests(unittest.TestCase):
    def test_preserves_every_original_field_and_applies_four_reductions(self):
        with (APP.RESULTS / "base_meaning_assignments.csv").open() as handle:
            originals = list(csv.DictReader(handle))
        rows, report = APP.normalize()
        self.assertEqual(len(rows), 2741)
        self.assertEqual([{k: r[k] for k in originals[0]} for r in rows], originals)
        self.assertEqual(report["current_provisional_assignments"], 2649)
        self.assertEqual(report["grammatical_metadata_rows"], 1)
        self.assertIsNone(report["vocabulary_total"])
        by_key = {(r["source_code"], r["meaning_slp1"]): r for r in rows}
        self.assertEqual(by_key["04.0143", "hiMsAyAm"]["normalized_meaning_slp1"], "roze")
        self.assertEqual(by_key["04.0143", "hiMsAyAm"]["normalized_count_key"],
                         by_key["10.0187", "roze"]["normalized_count_key"])
        self.assertNotEqual(by_key["01.0789", "hiMsAyAm"]["normalized_count_key"],
                            by_key["04.0143", "hiMsAyAm"]["normalized_count_key"])
        ay = by_key["01.1031", "uparame"]
        self.assertEqual((ay["normalized_citation_slp1"], ay["normalized_meaning_slp1"]), ("aya~^", "gatO"))
        self.assertEqual(by_key["01.0930", "aparivezaRe"]["record_kind"], "grammatical_metadata")
        self.assertEqual(by_key["04.0121", "viBAge"]["record_kind"], "lexical")

    def test_overlay_is_repeatable_and_saved_outputs_match(self):
        first = APP.normalize()
        self.assertEqual(first, APP.normalize())
        with (APP.RESULTS / "normalized_base_assignments.csv").open() as handle:
            self.assertEqual(first[0], list(csv.DictReader(handle)))
        self.assertEqual(first[1], json.loads((APP.RESULTS / "normalized_base_meanings.json").read_text()))

    def test_scope_and_delta_guards(self):
        approval = json.loads(APP.APPROVAL.read_text())
        invalid = copy.deepcopy(approval)
        invalid["decisions"][0]["merges"][0]["members"][0] = ["01.0001", "sattAyAm"]
        with self.assertRaisesRegex(ValueError, "outside the reviewed"):
            APP.normalize(invalid)
        invalid = copy.deepcopy(approval)
        invalid["decisions"][0]["delta"] = -2
        with self.assertRaisesRegex(ValueError, "count effect"):
            APP.normalize(invalid)
        invalid = copy.deepcopy(approval)
        invalid["decisions"].append(copy.deepcopy(invalid["decisions"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            APP.normalize(invalid)

    def test_followup_uses_normalized_ay_not_original_yam(self):
        report = FOLLOWUP.build_report()
        self.assertEqual((report["baseline"], report["proposed_subtotal"]), (2649, 2645))
        self.assertEqual(len(report["cases"]), 10)
        ay = report["cases"][0]["original_rows"][1]
        self.assertEqual(ay["meaning_slp1"], "uparame")
        self.assertEqual(ay["normalized_meaning_slp1"], "gatO")
        self.assertEqual({c["prior_id"] for c in report["cases"] if c["delta"]},
                         {"IR04", "IR08", "IR10", "IR14"})
        self.assertEqual(report["followup_coverage"]["records_revisited"], 19)
        self.assertEqual(report["followup_coverage"]["not_revisited"], 65)

    def test_second_report_reproduces_and_does_not_apply_proposals(self):
        paths = [APP.RESULTS / "normalized_base_meanings.json", APP.RESULTS / "normalized_base_assignments.csv"]
        before = {p: APP.sha(p) for p in paths}
        report = FOLLOWUP.build_report()
        self.assertEqual(before, {p: APP.sha(p) for p in paths})
        self.assertEqual(report, json.loads((APP.RESULTS / "reconciliation_review_02.json").read_text()))
        self.assertEqual(FOLLOWUP.render(report), (APP.RESULTS / "reconciliation_review_02.md").read_text())

    def test_second_report_rejects_missing_evidence_or_count_drift(self):
        review = json.loads(FOLLOWUP.REVIEW.read_text())
        invalid = copy.deepcopy(review)
        invalid["cases"][0]["evidence"][0]["anchor"] = "INVENTED SOURCE CLAIM"
        with self.assertRaisesRegex(ValueError, "missing anchor"):
            FOLLOWUP.build_report(invalid)
        invalid = copy.deepcopy(review)
        invalid["cases"][0]["before_count"] = 1
        with self.assertRaisesRegex(ValueError, "count drift"):
            FOLLOWUP.build_report(invalid)


if __name__ == "__main__":
    unittest.main()

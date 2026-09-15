import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
HAS_ENGINE = importlib.util.find_spec("vidyut") is not None
if HAS_ENGINE:
    sys.path.insert(0, str(ROOT / "analysis/generativity"))
    try:
        import apply_reconciliation_02 as APPLIED
        import apply_eight_pass_approvals as CURRENT
        import review_remaining_followups as REVIEW
    finally:
        sys.path.pop(0)


@unittest.skipUnless(HAS_ENGINE, "Use build/generativity-venv/bin/python")
class EightPassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, cls.applied = APPLIED.normalize()
        cls.report = REVIEW.build_report()

    def test_second_approval_preserves_every_original_field(self):
        first, _ = APPLIED.first_normalize()
        self.assertEqual(len(first), 2741)
        self.assertEqual(len(self.rows), len(first))
        allowed = {"normalized_count_key", "reconciliation_id", "record_kind"}
        for before, after in zip(first, self.rows):
            for key in before.keys() - allowed:
                self.assertEqual(before[key], after[key], (before["source_code"], key))
        self.assertEqual(self.applied["current_provisional_assignments"], 2645)
        self.assertEqual(len(self.applied["decisions"]), 4)
        self.assertIsNone(self.applied["vocabulary_total"])

    def test_second_approval_is_repeatable_and_saved(self):
        self.assertEqual((self.rows, self.applied), APPLIED.normalize())
        saved = json.loads((APPLIED.RESULTS / "reconciliation_02_base_meanings.json").read_text())
        self.assertEqual(saved, self.applied)

    def test_second_approval_rejects_scope_drift(self):
        approval = json.loads(APPLIED.APPROVAL.read_text())
        approval["merges"][0]["members"][0] = ["01.0001", "sattAyAm"]
        with patch.object(Path, "read_text", autospec=True, side_effect=self.reader_override(APPLIED.APPROVAL, approval)):
            with self.assertRaisesRegex(ValueError, "scope"):
                APPLIED.normalize()

    @staticmethod
    def reader_override(target, payload):
        original = Path.read_text
        return lambda path, *args, **kwargs: json.dumps(payload) if path == target else original(path, *args, **kwargs)

    def test_seven_batches_and_proposal_total(self):
        self.assertEqual(self.report["reviewed_records"], 65)
        self.assertTrue(self.report["complete"])
        self.assertEqual([sum(c["batch"] == b for c in self.report["cases"]) for b in range(1, 8)], [10]*6 + [5])
        self.assertEqual(self.report["baseline"], 2645)
        self.assertEqual(self.report["proposed_delta"], -11)
        self.assertEqual(sum(bool(c["delta"]) for c in self.report["cases"]), 10)
        self.assertIsNone(self.report["vocabulary_total"])

    def test_proposal_runner_never_changes_inputs_or_applied_data(self):
        paths = [REVIEW.REVIEW, REVIEW.HERE / "identity_review.json",
                 REVIEW.RESULTS / "current_base_assignments.csv", REVIEW.RESULTS / "current_base_meanings.json",
                 REVIEW.RESULTS / "normalized_base_assignments.csv", REVIEW.RESULTS / "base_meanings.json"]
        before = {p: REVIEW.sha(p) for p in paths}
        data = json.loads(REVIEW.REVIEW.read_text())
        original = copy.deepcopy(data)
        REVIEW.build_report(data)
        self.assertEqual(data, original)
        self.assertEqual(before, {p: REVIEW.sha(p) for p in paths})

    def test_bad_evidence_is_rejected(self):
        data = json.loads(REVIEW.REVIEW.read_text())
        data["cases"][0]["evidence"][0]["anchor"] = "INVENTED EVIDENCE"
        with self.assertRaisesRegex(ValueError, "missing anchor"):
            REVIEW.build_report(data)

    def test_wrong_queue_order_and_duplicate_are_rejected(self):
        data = json.loads(REVIEW.REVIEW.read_text())
        data["cases"][0], data["cases"][1] = data["cases"][1], data["cases"][0]
        with self.assertRaisesRegex(ValueError, "queue"):
            REVIEW.build_report(data)
        data["cases"].append(copy.deepcopy(data["cases"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            REVIEW.build_report(data)

    def test_wrong_baseline_and_unscoped_merger_are_rejected(self):
        data = json.loads(REVIEW.REVIEW.read_text())
        data["baseline"] = 2649
        with self.assertRaisesRegex(ValueError, "Baseline"):
            REVIEW.build_report(data)
        data["baseline"] = 2645
        data["cases"][0]["proposed_merges"] = [[["01.0001", "sattAyAm"], ["10.0072", "KaRqane"]]]
        with self.assertRaisesRegex(ValueError, "scope"):
            REVIEW.build_report(data)

    def test_every_record_has_evidence_and_disposition(self):
        for case in self.report["cases"]:
            self.assertTrue(case["remaining"])
            self.assertTrue(case["evidence"])
            for evidence in case["evidence"]:
                self.assertIn(evidence["anchor"], REVIEW.source_text(evidence["source"]))
                self.assertTrue(evidence["record"]["url"])
                self.assertTrue(evidence["record"]["accessed_utc"])
                self.assertEqual(len(evidence["record"]["sha256"]), 64)

    def test_saved_reports_and_all_historical_followups(self):
        self.assertEqual(json.loads((REVIEW.RESULTS / "remaining_followup_review.json").read_text()), self.report)
        for batch in range(1, 8):
            self.assertEqual((REVIEW.RESULTS / f"remaining_followup_batch_{batch:02d}.md").read_text(),
                             REVIEW.render_batch(self.report, batch))
        summary = REVIEW.consolidate(self.report)
        self.assertEqual(len({c["id"] for c in summary["historical_coverage"]}), 84)
        self.assertEqual(summary["previously_revisited"] + summary["newly_reviewed"], 84)
        self.assertEqual(sum(summary["new_dispositions"].values()), 65)
        self.assertEqual(summary["applied_subtotal"], 2634)
        self.assertEqual(summary["approved_new_cases"],
                         ["IR116", "IR118", "IR131", "IR160", "IR166", "IR219", "IR43", "IR51", "IR68", "IR72"])
        self.assertEqual(summary["remaining_proposed_delta"], 0)
        self.assertEqual(summary["proposed_subtotal"], 2634)
        self.assertEqual(json.loads((REVIEW.RESULTS / "eight_pass_consolidation.json").read_text()), summary)
        self.assertEqual((REVIEW.RESULTS / "eight_pass_consolidation.md").read_text(), REVIEW.render_consolidation(summary, self.report))

    def test_consolidation_rejects_incomplete_sweep(self):
        incomplete = dict(self.report, complete=False, reviewed_records=64)
        with self.assertRaisesRegex(ValueError, "65"):
            REVIEW.consolidate(incomplete)

    def test_all_approved_proposals_are_applied_separately(self):
        rows, report = CURRENT.normalize()
        self.assertEqual(len(rows), 2741)
        self.assertEqual(report["baseline"], 2645)
        self.assertEqual(report["current_provisional_assignments"], 2634)
        self.assertEqual([d["case"] for d in report["decisions"]],
                         ["IR43", "IR51", "IR68", "IR72", "IR116", "IR118", "IR131", "IR160", "IR166", "IR219"])
        self.assertEqual(report["remaining_eight_pass_proposed_delta"], 0)
        self.assertEqual(json.loads((CURRENT.RESULTS / "current_base_meanings.json").read_text()), report)


if __name__ == "__main__":
    unittest.main()

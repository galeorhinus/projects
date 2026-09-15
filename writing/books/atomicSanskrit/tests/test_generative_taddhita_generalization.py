import gzip
import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis/generativity/results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


class TaddhitaGeneralizationTests(unittest.TestCase):
    def test_all_recovered_families_have_a_disposition(self):
        report = read_json(RESULTS / "taddhita_generalization_classification.json")
        self.assertEqual(report["semantic_families_reviewed"], 57)
        self.assertEqual(report["selected_families"], ["comparative", "superlative"])

    def test_eligibility_defers_rule_5358_quality_operations(self):
        report = read_json(RESULTS / "taddhita_generalization_eligibility.json")
        self.assertEqual(report["nominal_word_meanings"], 794_078)
        self.assertEqual(len(report["deferred_gunavacana_operations"]), 2)
        self.assertEqual(report["eligible_operation_relations"], 1_588_156)

    def test_rule_5358_is_archived_and_hashed(self):
        manifest = read_json(ARCHIVE / "plain_taddhita_rule_manifest.json")
        record = next(row for row in manifest["sources"] if row["rule"] == "5.3.58")
        data = (ARCHIVE / record["filename"]).read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), record["sha256"])

    def test_generation_and_verification_exhaust_eligibility(self):
        generated = read_json(RESULTS / "taddhita_generalization_generation.json")
        verified = read_json(RESULTS / "taddhita_generalization_verification.json")
        self.assertEqual(generated["engine_verified_candidate_relations"], 1_588_156)
        self.assertEqual(generated["engine_zero_or_error_relations"], 0)
        self.assertEqual(verified["candidate_relations_verified"], 1_588_156)
        self.assertEqual(verified["verification_status"], "passed")

    def test_reconciliation_adds_only_new_meanings(self):
        report = read_json(RESULTS / "taddhita_generalization_reconciliation.json")
        self.assertEqual(report["existing_word_meaning_overlaps_not_added"], 1)
        self.assertEqual(report["additional_generalized_word_meanings"], 1_588_155)
        self.assertEqual(report["combined_bounded_word_meaning_subtotal"], 12_704_821)

    def test_summary_and_graph_agree(self):
        summary = read_json(RESULTS / "taddhita_generalization_six_pass_summary.json")
        graph = read_json(RESULTS / "generation_stage_graph.json")
        node = next(node for node in graph["nodes"] if node["id"] == "generalized_comparison")
        self.assertEqual(summary["remaining_passes"], 30)
        self.assertEqual(node["added_count"], 1_588_155)
        self.assertEqual(node["cumulative_count"], 12_704_821)


if __name__ == "__main__":
    unittest.main()

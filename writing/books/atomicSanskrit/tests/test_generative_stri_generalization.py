import gzip
import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis/generativity/results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"


def read_json(name):
    return json.loads((RESULTS / name).read_text())


class StriGeneralizationTests(unittest.TestCase):
    def test_four_lexical_agent_operations_are_selected(self):
        report = read_json("stri_generalization_classification.json")
        self.assertEqual(report["selected_semantic_operations"], 4)
        self.assertEqual(set(report["selected_source_operations"]), {
            "agent_nvul", "agent_trc", "agent_ac", "blessed_agent_vun",
        })

    def test_rule_sources_are_archived(self):
        manifest = json.loads((ARCHIVE / "stri_manifest.json").read_text())
        names = {row["filename"] for row in manifest["sources"]}
        self.assertTrue({"rule-4.1.3.html", "rule-4.1.4.html", "rule-4.1.5.html"} <= names)
        for row in manifest["sources"]:
            self.assertEqual(hashlib.sha256((ARCHIVE / row["filename"]).read_bytes()).hexdigest(), row["sha256"])

    def test_eligibility_retains_constructor_provenance(self):
        report = read_json("stri_generalization_eligibility.json")
        self.assertEqual(report["eligible_lexical_agent_meanings"], 140_568)
        self.assertEqual(report["constructor_provenance_missing"], 0)

    def test_generation_and_verification_exhaust_eligibility(self):
        generation = read_json("stri_generalization_generation.json")
        verification = read_json("stri_generalization_verification.json")
        self.assertEqual(generation["engine_verified_relations"], 140_568)
        self.assertEqual(generation["engine_zero_or_no_stri_suffix_relations"], 0)
        self.assertEqual(verification["verified_relations"], 140_568)
        self.assertEqual(set(verification["suffixes_observed"]), {"wAp", "NIp"})

    def test_reconciliation_uses_meaning_not_spelling(self):
        report = read_json("stri_generalization_reconciliation.json")
        self.assertEqual(report["confirmed_existing_word_meaning_overlaps_not_added"], 2)
        self.assertEqual(report["same_spelling_cases_not_merged"], 4)
        self.assertEqual(report["additional_generalized_stri_word_meanings"], 140_566)

    def test_summary_and_graph_agree(self):
        summary = read_json("stri_generalization_six_pass_summary.json")
        graph = read_json("generation_stage_graph.json")
        node = next(node for node in graph["nodes"] if node["id"] == "generalized_stri")
        self.assertEqual(summary["combined_bounded_word_meaning_subtotal"], 12_845_387)
        self.assertEqual(summary["remaining_passes"], 24)
        self.assertEqual(node["added_count"], 140_566)
        self.assertEqual(node["cumulative_count"], 12_845_387)


if __name__ == "__main__":
    unittest.main()

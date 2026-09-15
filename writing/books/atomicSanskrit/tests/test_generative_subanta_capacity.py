import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis/generativity"
RESULTS = ANALYSIS / "results"
SCRIPTS = (
    "reconcile_subanta_word_classes.py",
    "build_subanta_nominal_inventory.py",
    "classify_subanta_coordinates.py",
    "build_subanta_citation_capacity.py",
    "build_subanta_citation_sample.py",
    "build_subanta_citation_six_pass_summary.py",
    "build_subanta_paradigm_capacity.py",
    "classify_subanta_gender_outputs.py",
    "build_subanta_paradigm_sample.py",
    "analyze_subanta_sample_collisions.py",
    "reconcile_subanta_capacity.py",
    "build_subanta_twelve_pass_summary.py",
)


class SubantaCapacityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for name in SCRIPTS:
            subprocess.run(
                [sys.executable, str(ANALYSIS / name)], cwd=ROOT,
                check=True, capture_output=True,
            )

    def test_word_classes_reconcile(self):
        report = json.loads((RESULTS / "subanta_word_class_reconciliation.json").read_text())
        self.assertEqual(report["combined_lexical_word_meanings"], 12_846_458)
        self.assertEqual(report["laukika_name_meanings"], 8_084_287)
        self.assertEqual(report["laukika_unchanging_meanings"], 7_925)
        self.assertEqual(report["difference_from_previous_compound_member_view"], 666)
        self.assertEqual(report["unresolved_reader_graph_residual_after_reconciliation"], 0)
        self.assertEqual(
            report["laukika_word_meanings"],
            report["laukika_action_meanings"]
            + report["laukika_name_meanings"]
            + report["laukika_unchanging_meanings"],
        )

    def test_virtual_inventory_and_samples(self):
        report = json.loads((RESULTS / "subanta_nominal_inventory.json").read_text())
        self.assertEqual(report["laukika_name_word_meanings"], 8_084_287)
        self.assertEqual(sum(report["counts_by_source_layer"].values()), 8_084_287)
        self.assertFalse(report["full_inventory_duplicated"])
        self.assertEqual(report["materialized_sample_records"], 8)
        self.assertEqual(report["sample_source_ledgers_verified"], 6)

    def test_coordinate_and_citation_capacity(self):
        coordinates = json.loads((RESULTS / "subanta_coordinate_classification.json").read_text())
        capacity = json.loads((RESULTS / "subanta_citation_capacity.json").read_text())
        sample = json.loads((RESULTS / "subanta_citation_sample.json").read_text())
        self.assertEqual(coordinates["engine_relation_coordinates"], 8)
        self.assertEqual(coordinates["engine_number_coordinates"], 3)
        self.assertEqual(coordinates["cells_per_name_meaning"], 24)
        self.assertEqual(capacity["citation_semantic_cells"], 8_084_287)
        self.assertEqual(sample["locally_regenerated_cells"], 8)
        self.assertEqual(sample["expected_citation_forms_recovered"], 8)

    def test_full_capacity_and_gender_policy(self):
        capacity = json.loads((RESULTS / "subanta_paradigm_capacity.json").read_text())
        gender = json.loads((RESULTS / "subanta_gender_classification.json").read_text())
        self.assertEqual(capacity["full_relation_number_semantic_cells"], 194_022_888)
        self.assertFalse(capacity["gender_multiplier_applied"])
        self.assertEqual(gender["automatic_gender_multiplier"], 1)
        self.assertFalse(gender["agreement_gender_expansion_included"])

    def test_full_sample_and_collision_policy(self):
        sample = json.loads((RESULTS / "subanta_paradigm_sample.json").read_text())
        collisions = json.loads((RESULTS / "subanta_sample_collisions.json").read_text())
        self.assertEqual(sample["semantic_cells_requested"], 192)
        self.assertEqual(sample["semantic_cells_locally_regenerated"], 192)
        self.assertEqual(collisions["spellings_shared_across_semantic_cells"], 46)
        self.assertEqual(collisions["semantic_cells_merged"], 0)

    def test_final_report_and_graphs(self):
        report = json.loads((RESULTS / "subanta_twelve_pass_summary.json").read_text())
        self.assertEqual(report["passes_completed"], 12)
        self.assertEqual(report["remaining_subanta_passes"], 0)
        self.assertFalse(report["inflectional_cells_added_to_lexical_subtotal"])
        graph = json.loads((RESULTS / "generation_stage_graph.json").read_text())
        nodes = {node["id"]: node for node in graph["nodes"]}
        self.assertNotIn("subanta_expansion_pending", nodes)
        for node_id in ("laukika_nominal_inventory", "subanta_citation_capacity", "subanta_paradigm_capacity"):
            self.assertFalse(nodes[node_id]["included_in_current_research_subtotal"])
        reader = json.loads((RESULTS / "wordspace_category_graph.json").read_text())
        reader_nodes = {node["id"]: node for node in reader["nodes"]}
        self.assertEqual(reader_nodes["name_meanings"]["count"], 8_084_287)
        self.assertEqual(reader_nodes["unchanging_meanings"]["count"], 7_925)
        self.assertEqual(reader_nodes["all_name_forms"]["count"], 194_022_888)


if __name__ == "__main__":
    unittest.main()

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis/generativity"
RESULTS = ANALYSIS / "results"
VERIFIER = ANALYSIS / "rust/samasa_verifier/target/release/samasa-verifier"
SCRIPTS = (
    "classify_samasa_capacity_rules.py",
    "build_samasa_member_inventory.py",
    "build_samasa_capacity_eligibility.py",
    "build_samasa_capacity_counts.py",
    "build_samasa_capacity_sample.py",
    "build_samasa_capacity_six_pass_summary.py",
    "classify_samasa_reuse_operations.py",
    "build_samasa_reuse_eligibility.py",
    "build_recursive_samasa_capacity.py",
    "build_recursive_samasa_sample.py",
    "reconcile_samasa_capacity.py",
    "build_samasa_capacity_twelve_pass_summary.py",
)


class SamasaCapacityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for name in SCRIPTS:
            if "sample" in name and not VERIFIER.exists():
                continue
            subprocess.run([sys.executable, str(ANALYSIS / name)], cwd=ROOT, check=True, capture_output=True)

    def test_member_inventory_and_depth_one_arithmetic(self):
        members = json.loads((RESULTS / "samasa_capacity_member_inventory.json").read_text())
        capacity = json.loads((RESULTS / "samasa_capacity_eligibility.json").read_text())
        self.assertEqual(members["compoundable_nominal_word_meanings"], 8_083_621)
        self.assertEqual(capacity["eligible_depth_one_relation_slots"], 196_034_769_247_681)
        self.assertFalse(capacity["materialized_all_relations"])

    def test_source_fixture_and_samples_are_locally_regenerated(self):
        fixture = json.loads((RESULTS / "samasa_verification.json").read_text())
        sample = json.loads((RESULTS / "samasa_capacity_sample.json").read_text())
        recursive = json.loads((RESULTS / "recursive_samasa_sample.json").read_text())
        if VERIFIER.exists():
            self.assertEqual(fixture["locally_regenerated_relations"], 113)
            self.assertEqual(sample["locally_regenerated_relations"], 16)
            self.assertEqual(recursive["locally_regenerated_relations"], 6)

    def test_reuse_and_depth_two_arithmetic(self):
        reuse = json.loads((RESULTS / "samasa_reuse_eligibility.json").read_text())
        recursive = json.loads((RESULTS / "recursive_samasa_capacity.json").read_text())
        self.assertEqual(reuse["post_compound_derivational_slots"], 1_960_347_692_476_810)
        self.assertEqual(recursive["depth_two_compound_relation_slots"], 9_508_024_664_524_249_997_406)
        self.assertFalse(recursive["two_depth_one_compounds_as_members"])

    def test_capacity_is_not_added_to_lexical_subtotal(self):
        report = json.loads((RESULTS / "samasa_capacity_twelve_pass_summary.json").read_text())
        self.assertEqual(report["passes_completed"], 12)
        self.assertEqual(report["materialized_lexical_word_meaning_subtotal"], 12_846_458)
        self.assertFalse(report["symbolic_counts_added_to_lexical_subtotal"])
        self.assertEqual(report["remaining_samasa_capacity_passes"], 0)

    def test_graph_marks_capacity_as_non_additive(self):
        graph = json.loads((RESULTS / "generation_stage_graph.json").read_text())
        nodes = {node["id"]: node for node in graph["nodes"]}
        self.assertFalse(nodes["samasa_member_inventory"]["included_in_current_research_subtotal"])
        self.assertEqual(
            nodes["samasa_member_inventory"]["count_role"],
            "virtual_input_inventory_not_lexical_subtotal",
        )
        for node_id in ("samasa_depth_one_capacity", "post_compound_capacity", "samasa_depth_two_capacity"):
            self.assertFalse(nodes[node_id]["included_in_current_research_subtotal"])
            self.assertEqual(nodes[node_id]["count_role"], "symbolic_capacity_not_lexical_subtotal")


if __name__ == "__main__":
    unittest.main()

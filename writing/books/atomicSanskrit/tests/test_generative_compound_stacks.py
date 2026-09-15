import csv
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis/generativity"
RESULTS = ANALYSIS / "results"
SCRIPTS = (
    "classify_compound_stack_inventory.py",
    "build_compound_stack_eligibility.py",
    "build_compound_stack_ledger.py",
    "verify_compound_stack_ledger.py",
    "reconcile_compound_stack_ledger.py",
    "build_compound_stack_six_pass_summary.py",
)


def rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class CompoundStackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for name in SCRIPTS:
            subprocess.run([sys.executable, str(ANALYSIS / name)], cwd=ROOT, check=True, capture_output=True)

    def test_input_classification(self):
        report = json.loads((RESULTS / "compound_stack_classification.json").read_text())
        self.assertEqual(report["source_compound_word_meanings"], 113)
        self.assertEqual(report["derived_nominal_bases"], 96)
        self.assertEqual(report["complete_avyayibhava_indeclinables"], 17)

    def test_eligibility_boundary(self):
        report = json.loads((RESULTS / "compound_stack_eligibility.json").read_text())
        self.assertEqual(report["eligible_relations"], 958)
        self.assertEqual(report["eligible_by_operation"]["nan_privative"], 94)
        self.assertFalse(report["recursive_nan_admitted"])
        self.assertFalse(report["recursive_compounding_admitted"])

    def test_generation_and_verification(self):
        generation = json.loads((RESULTS / "compound_stack_generation.json").read_text())
        verification = json.loads((RESULTS / "compound_stack_verification.json").read_text())
        self.assertEqual(generation["generated_candidate_relations"], 958)
        self.assertEqual(generation["engine_zero_or_error_relations"], 0)
        self.assertEqual(verification["verified_relations"], 958)
        self.assertEqual(verification["mismatches"], 0)

    def test_distinct_meanings_survive_same_spelling(self):
        ledger = rows(RESULTS / "compound_stack_ledger.csv")
        pair = [
            row for row in ledger
            if row["input_forms_slp1"] == "rAjapuruza"
            and row["operation_id"] in {"self_desire_kyac", "object_comparison_kyac"}
        ]
        self.assertEqual(len(pair), 2)
        self.assertEqual(len({row["output_forms_slp1"] for row in pair}), 1)
        self.assertEqual(len({row["semantic_branch_id"] for row in pair}), 2)

    def test_reconciliation_and_graph(self):
        report = json.loads((RESULTS / "compound_stack_six_pass_summary.json").read_text())
        self.assertEqual(report["additional_compound_stack_word_meanings"], 958)
        self.assertEqual(report["combined_bounded_word_meaning_subtotal"], 12_846_458)
        self.assertEqual(report["remaining_passes"], 12)
        graph = json.loads((RESULTS / "generation_stage_graph.json").read_text())
        node = next(node for node in graph["nodes"] if node["id"] == "compound_input_stacks")
        self.assertEqual(node["cumulative_count"], 12_846_458)
        self.assertNotIn("stacked_operations_pending", {node["id"] for node in graph["nodes"]})


if __name__ == "__main__":
    unittest.main()

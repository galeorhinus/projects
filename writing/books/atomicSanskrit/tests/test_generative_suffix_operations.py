import csv
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis/generativity/results"


class SuffixOperationTests(unittest.TestCase):
    def test_all_suffix_identifiers_are_classified(self):
        report = json.loads((RESULTS / "suffix_semantic_families.json").read_text())
        self.assertEqual(report["suffix_identifiers"], 175)

    def test_visible_endings_are_not_treated_as_operations(self):
        with (RESULTS / "suffix_semantic_families.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        ka_sources = {row["source_variant"] for row in rows if row["visible_suffix"] == "ka"}
        ya_sources = {row["source_variant"] for row in rows if row["visible_suffix"] == "ya"}
        self.assertGreater(len(ka_sources), 1)
        self.assertGreater(len(ya_sources), 1)

    def test_only_semantically_named_relations_enter_new_ledger(self):
        with (RESULTS / "suffix_conditioned_ledger.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 24)
        self.assertTrue(all(row["semantic_context"] and row["semantic_relation"] for row in rows))
        self.assertTrue(all(row["reconciliation_status"] == "admitted_additional_conditioned_relation" for row in rows))

    def test_optional_variants_do_not_multiply_meanings(self):
        with (RESULTS / "suffix_conditioned_ledger.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        tavat = [row for row in rows if row["input_form_slp1"] == "tAvat"]
        self.assertEqual(len(tavat), 1)
        self.assertEqual(tavat[0]["expected_output_variant_count"], "2")
        self.assertEqual(tavat[0]["verification_status"], "verified_relation_partial_variant_coverage")

    def test_reconciliation_total(self):
        report = json.loads((RESULTS / "suffix_conditioned_reconciliation.json").read_text())
        self.assertEqual(report["additional_suffix_word_meanings"], 24)
        self.assertEqual(report["combined_bounded_word_meaning_subtotal"], 11_116_430)

    def test_graph_contains_new_stage(self):
        graph = json.loads((RESULTS / "generation_stage_graph.json").read_text())
        node = next(node for node in graph["nodes"] if node["id"] == "additional_suffix_relations")
        self.assertEqual(node["cumulative_count"], 11_116_430)


if __name__ == "__main__":
    unittest.main()

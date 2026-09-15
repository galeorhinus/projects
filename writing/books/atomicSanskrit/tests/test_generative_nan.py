import csv
import gzip
import hashlib
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis/generativity"
RESULTS = ANALYSIS / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
sys.path.insert(0, str(ANALYSIS))

from nan_common import nan_surface  # noqa: E402


class NanExpansionTests(unittest.TestCase):
    def test_source_archive_is_pinned(self):
        manifest = json.loads((ARCHIVE / "nan_manifest.json").read_text())
        self.assertEqual(len(manifest["sources"]), 6)
        for row in manifest["sources"]:
            self.assertEqual(hashlib.sha256((ARCHIVE / row["filename"]).read_bytes()).hexdigest(), row["sha256"])

    def test_one_operation_has_two_surface_outcomes(self):
        report = json.loads((RESULTS / "nan_rule_classification.json").read_text())
        self.assertEqual(report["semantic_operations"], 1)
        self.assertEqual(report["surface_allomorphs"], 2)
        self.assertEqual(nan_surface("jYAna"), ("ajYAna", "a_before_consonant"))
        self.assertEqual(nan_surface("Agamana"), ("anAgamana", "an_before_vowel"))

    def test_pinned_examples_match(self):
        report = json.loads((RESULTS / "nan_source_examples.json").read_text())
        self.assertEqual(report["verified_examples"], 5)
        with (RESULTS / "nan_source_examples.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual({row["derived_output_slp1"] for row in rows}, {"abrAhmaRa", "avfzala", "asomapa", "anaja", "anaSva"})

    def test_current_nominal_inventory_reconciles(self):
        report = json.loads((RESULTS / "nan_eligibility.json").read_text())
        self.assertEqual(report["eligible_by_source_layer"], {
            "first_nominal_inventory": 794078,
            "broad_taddhita": 2382237,
            "conditioned_taddhita": 975,
            "stri": 50,
        })
        self.assertEqual(report["candidate_nan_word_meanings"], 3177340)

    def test_generation_and_reconciliation(self):
        generated = json.loads((RESULTS / "nan_summary.json").read_text())
        reconciled = json.loads((RESULTS / "nan_reconciliation.json").read_text())
        self.assertEqual(generated["admitted_nan_word_meanings"], 3177340)
        self.assertEqual(generated["not_admitted_total"], 0)
        self.assertEqual(reconciled["prior_combined_bounded_word_meanings"], 7939066)
        self.assertEqual(reconciled["combined_bounded_word_meaning_subtotal"], 11116406)
        self.assertEqual(reconciled["complete_inflected_words_counted"], 0)

    def test_familiar_and_less_familiar_examples_exist_in_ledger(self):
        wanted = {"ajYAna", "akartftva", "anAgamana"}
        found = set()
        with gzip.open(RESULTS / "nan_ledger.csv.gz", "rt", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                found.update(wanted.intersection(row["output_forms_slp1"].split(";")))
                if found == wanted:
                    break
        self.assertEqual(found, wanted)

    def test_stage_graph_records_reader_label_and_pending_layers(self):
        graph = json.loads((RESULTS / "generation_stage_graph.json").read_text())
        nodes = {row["id"]: row for row in graph["nodes"]}
        self.assertEqual(nodes["nan_privative"]["cumulative_count"], 11116406)
        self.assertEqual(nodes["nan_privative"]["reader_label"], "Nouns and descriptive meanings generate negative counterparts")
        self.assertFalse(nodes["nan_privative"]["complete_pada"])
        self.assertNotIn("subanta_expansion_pending", nodes)
        self.assertEqual(nodes["laukika_nominal_inventory"]["added_count"], 8084287)
        self.assertEqual(nodes["subanta_citation_capacity"]["added_count"], 8084287)
        self.assertEqual(nodes["subanta_paradigm_capacity"]["added_count"], 194022888)


if __name__ == "__main__":
    unittest.main()

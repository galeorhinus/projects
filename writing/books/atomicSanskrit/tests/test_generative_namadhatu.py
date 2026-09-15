import csv
import gzip
import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis/generativity/results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"


class NamadhatuExpansionTests(unittest.TestCase):
    def test_rule_sources_are_archived_and_unchanged(self):
        manifest = json.loads((ARCHIVE / "namadhatu_manifest.json").read_text())
        self.assertEqual(len(manifest["sources"]), 14)
        self.assertEqual(
            {row["filename"] for row in manifest["sources"]},
            {f"rule-3.1.{number}.html" for number in range(8, 22)},
        )
        for row in manifest["sources"]:
            source = ARCHIVE / row["filename"]
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), row["sha256"])

    def test_operation_and_source_classification(self):
        operations = json.loads((RESULTS / "namadhatu_operation_classification.json").read_text())
        examples = json.loads((RESULTS / "namadhatu_source_examples.json").read_text())
        self.assertEqual(operations["rules_classified"], 14)
        self.assertEqual(operations["productive_broad_relations"], 4)
        self.assertEqual(operations["conditioned_rule_groups"], 10)
        self.assertEqual(examples["unique_source_relations"], 67)
        self.assertEqual(examples["active_broad_examples"], 17)
        self.assertEqual(examples["active_conditioned_relations"], 40)
        self.assertEqual(examples["ignored_relations"], 10)

    def test_eligibility_arithmetic(self):
        report = json.loads((RESULTS / "namadhatu_eligibility.json").read_text())
        self.assertEqual(report["declared_laukika_nominal_word_meanings"], 794078)
        self.assertEqual(report["broad_candidate_relations"], 4 * 794078)
        self.assertEqual(report["total_candidate_relations"], 4 * 794078 + 40)

    def test_generation_and_reconciliation(self):
        generated = json.loads((RESULTS / "namadhatu_summary.json").read_text())
        reconciled = json.loads((RESULTS / "namadhatu_reconciliation.json").read_text())
        self.assertEqual(generated["admitted_namadhatu_word_meanings"], 3176352)
        self.assertEqual(generated["not_admitted_total"], 0)
        self.assertEqual(generated["source_present_form_verifications"], 40)
        self.assertEqual(reconciled["combined_bounded_word_meaning_subtotal"], 7939066)
        self.assertEqual(reconciled["complete_inflected_words_counted"], 0)

    def test_ledger_count_and_unique_ids(self):
        count = 0
        identifiers = set()
        with gzip.open(RESULTS / "namadhatu_ledger.csv.gz", "rt", newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                count += 1
                identifiers.add(row["derived_word_meaning_id"])
                self.assertEqual(row["form_status"], "derived_verbal_base_not_inflected_tinanta")
        self.assertEqual(count, 3176352)
        self.assertEqual(len(identifiers), count)

    def test_stage_graph_separates_form_classes(self):
        graph = json.loads((RESULTS / "generation_stage_graph.json").read_text())
        nodes = {row["id"]: row for row in graph["nodes"]}
        self.assertEqual(nodes["namadhatu"]["cumulative_count"], 7939066)
        self.assertEqual(nodes["namadhatu"]["complete_pada"], "mixed")
        self.assertTrue(nodes["avyaya_complete_component"]["complete_pada"])
        self.assertNotIn("tinanta_expansion_pending", nodes)
        self.assertFalse(nodes["laukika_verbal_inventory"]["complete_pada"])
        self.assertTrue(nodes["tinanta_citation_capacity"]["complete_pada"])
        self.assertTrue(nodes["tinanta_paradigm_capacity"]["complete_pada"])
        self.assertIsNone(nodes["tinanta_paradigm_capacity"]["cumulative_count"])


if __name__ == "__main__":
    unittest.main()

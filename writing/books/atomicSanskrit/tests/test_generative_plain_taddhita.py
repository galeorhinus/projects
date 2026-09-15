import csv
import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis/generativity/results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


class PlainTaddhitaTests(unittest.TestCase):
    def test_source_inventory_boundary(self):
        report = read_json(RESULTS / "plain_taddhita_source_assertions.json")
        self.assertEqual(report["literal_plain_assertions"], 301)
        self.assertEqual(report["positive_assertions"], 292)
        self.assertEqual(report["negative_assertions"], 9)
        self.assertEqual(report["active_positive_assertions"], 248)
        self.assertEqual(report["ignored_positive_assertions"], 44)

    def test_every_positive_assertion_is_classified_and_sources_are_intact(self):
        report = read_json(RESULTS / "plain_taddhita_semantic_classification.json")
        self.assertEqual(report["classified_positive_assertions"], 292)
        self.assertEqual(report["active_semantic_rows"], 249)
        manifest = read_json(ARCHIVE / "plain_taddhita_rule_manifest.json")
        self.assertEqual(len(manifest["sources"]), 110)
        for record in manifest["sources"]:
            data = (ARCHIVE / record["filename"]).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), record["sha256"])

    def test_eligibility_separates_nominal_bases_and_complete_avyayas(self):
        report = read_json(RESULTS / "plain_taddhita_eligibility.json")
        self.assertEqual(report["eligible_word_meaning_relations"], 245)
        self.assertEqual(report["duplicate_assertions_collapsed"], 4)
        self.assertEqual(report["by_output_class"]["nominal_base"], 206)
        self.assertEqual(report["by_output_class"]["complete_avyaya"], 39)

    def test_all_eligible_relations_are_verified(self):
        report = read_json(RESULTS / "plain_taddhita_verification.json")
        self.assertEqual(report["eligible_relations"], 245)
        self.assertEqual(report["verified_relations"], 245)
        self.assertEqual(report["engine_mismatches_not_admitted"], 0)

    def test_reconciliation_adds_only_new_word_meanings(self):
        report = read_json(RESULTS / "plain_taddhita_reconciliation.json")
        self.assertEqual(report["existing_word_meaning_overlaps_not_added"], 9)
        self.assertEqual(report["additional_plain_taddhita_word_meanings"], 236)
        self.assertEqual(report["additional_nominal_bases"], 197)
        self.assertEqual(report["additional_complete_avyayas"], 39)
        self.assertEqual(report["combined_bounded_word_meaning_subtotal"], 11_116_666)
        with (RESULTS / "plain_taddhita_ledger.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(
            sum(row["reconciliation_status"] == "admitted_additional_plain_relation" for row in rows),
            236,
        )

    def test_summary_and_graph_report_the_same_stage(self):
        summary = read_json(RESULTS / "plain_taddhita_six_pass_summary.json")
        graph = read_json(RESULTS / "generation_stage_graph.json")
        node = next(node for node in graph["nodes"] if node["id"] == "plain_source_taddhita")
        self.assertEqual(summary["additional_plain_taddhita_word_meanings"], 236)
        self.assertEqual(summary["combined_bounded_word_meaning_subtotal"], 11_116_666)
        self.assertEqual(node["added_count"], 236)
        self.assertEqual(node["cumulative_count"], 11_116_666)
        self.assertEqual(node["nominal_bases"], 197)
        self.assertEqual(node["complete_avyayas"], 39)


if __name__ == "__main__":
    unittest.main()

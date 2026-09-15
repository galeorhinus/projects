import csv
import gzip
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "analysis/generativity"
RESULTS = HERE / "results"


def csv_count(path: Path, compressed: bool = False) -> int:
    opener = gzip.open if compressed else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


class VaidikaGenerationTests(unittest.TestCase):
    def test_base_domain_audit_covers_normalized_inventory(self):
        report = json.loads((RESULTS / "base_domain_audit.json").read_text())
        self.assertEqual(report["base_word_meanings_audited"], 2634)
        self.assertEqual(report["status_counts"]["documented_vedic_only"], 11)
        self.assertFalse(report["source_codes_requiring_domain_review"])

    def test_nineteen_metadata_identifiers_plus_kvasu_map_to_seven_operations(self):
        report = json.loads((RESULTS / "vaidika_krt_classification.json").read_text())
        self.assertEqual(report["identifier_count"], 20)
        self.assertEqual(report["engine_metadata_deferred_identifiers"], 19)
        self.assertEqual(report["source_recovered_identifiers"], ["kvasu"])
        self.assertEqual(report["semantic_operation_count"], 7)
        identifiers = {item for operation in report["operations"] for item in operation["identifiers"]}
        self.assertEqual(len(identifiers), 20)

    def test_direct_and_conditioned_ledgers_match_summaries(self):
        direct = json.loads((RESULTS / "vaidika_direct_summary.json").read_text())
        conditioned = json.loads((RESULTS / "vaidika_conditioned_summary.json").read_text())
        self.assertEqual(csv_count(RESULTS / "vaidika_direct_ledger.csv"), direct["admitted_vaidika_direct_word_meanings"])
        self.assertEqual(csv_count(RESULTS / "vaidika_conditioned_ledger.csv"), conditioned["admitted_vaidika_conditioned_word_meanings"])
        self.assertEqual(conditioned["admitted_by_operation"]["vedic_bhavalaksana_kasun"], 3)
        self.assertTrue(all(row["status"].startswith("not_admitted_engine_coverage_gap") for row in conditioned["coverage_gaps"]))

    def test_stacked_ledger_is_materialized(self):
        report = json.loads((RESULTS / "vaidika_stacked_summary.json").read_text())
        self.assertEqual(csv_count(RESULTS / "vaidika_stacked_ledger.csv.gz", True), report["admitted_vaidika_stacked_word_meanings"])
        self.assertEqual(report["not_admitted_total"], 0)

    def test_reconciliation_partitions_without_double_counting(self):
        report = json.loads((RESULTS / "vaidika_laukika_reconciliation.json").read_text())
        self.assertEqual(
            report["current_bounded_laukika_subtotal_after_known_restrictions"]
            + report["bounded_vaidika_subtotal"],
            report["combined_bounded_word_meaning_subtotal"],
        )
        self.assertEqual(report["unsupported_vaidika_semantic_candidates_not_counted"], 5280)


if __name__ == "__main__":
    unittest.main()

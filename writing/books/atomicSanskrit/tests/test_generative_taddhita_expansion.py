import csv
import gzip
import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis/generativity/results"


def csv_count(path: Path, compressed: bool = False) -> int:
    opener = gzip.open if compressed else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


class TaddhitaExpansionTests(unittest.TestCase):
    def test_taddhita_source_archive_is_pinned(self):
        archive = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
        manifest = json.loads((archive / "taddhita_manifest.json").read_text())
        self.assertEqual(len(manifest["sources"]), 21)
        for row in manifest["sources"]:
            self.assertEqual(hashlib.sha256((archive / row["filename"]).read_bytes()).hexdigest(), row["sha256"])

    def test_nominal_input_boundary(self):
        report = json.loads((RESULTS / "nominal_input_inventory_summary.json").read_text())
        self.assertEqual(report["admitted_nominal_word_meanings"], 794078)
        self.assertEqual(report["known_vedic_restricted_rows_excluded"], 3114)
        self.assertEqual(csv_count(RESULTS / "nominal_input_inventory.csv.gz", True), 794078)

    def test_all_identifiers_have_a_disposition(self):
        report = json.loads((RESULTS / "taddhita_identifier_classification.json").read_text())
        self.assertEqual(report["identifier_count"], 175)
        with (RESULTS / "taddhita_identifier_classification.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 175)
        self.assertTrue(all(row["classification_disposition"] for row in rows))
        self.assertEqual(sum(row["count_status"] == "admitted_by_declared_operation" for row in rows), 4)

    def test_eligibility_is_semantic_not_an_identifier_multiplier(self):
        report = json.loads((RESULTS / "taddhita_eligibility.json").read_text())
        self.assertEqual(report["selected_semantic_operations"], 4)
        self.assertEqual(report["eligible_operation_candidates"], 2382237)
        self.assertEqual(
            {row["operation_id"] for row in report["operations"]},
            {"state_tva", "state_tal", "possession_matup", "descendant_dhak"},
        )

    def test_materialized_ledger_reconciles(self):
        report = json.loads((RESULTS / "taddhita_summary.json").read_text())
        self.assertEqual(report["admitted_taddhita_word_meanings"], 2382237)
        self.assertEqual(report["not_admitted_total"], 0)
        self.assertEqual(csv_count(RESULTS / "taddhita_ledger.csv.gz", True), 2382237)
        self.assertEqual(csv_count(RESULTS / "taddhita_exclusions.csv.gz", True), 0)

    def test_familiar_outputs_are_materialized(self):
        wanted = {"kOnteya", "mitratva", "mitratA", "mitravat", "jYAnatva", "jYAnavat", "kartftva"}
        found = set()
        with gzip.open(RESULTS / "taddhita_ledger.csv.gz", "rt", newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                found.update(wanted.intersection(row["output_forms_slp1"].split(";")))
                if found == wanted:
                    break
        self.assertEqual(found, wanted)

    def test_pilot_overlap_and_new_subtotal(self):
        report = json.loads((RESULTS / "taddhita_reconciliation.json").read_text())
        self.assertEqual(report["prior_taddhita_pilot_word_meanings_already_counted"], 7)
        self.assertEqual(report["additional_taddhita_word_meanings"], 2382230)
        self.assertEqual(report["combined_bounded_word_meaning_subtotal"], 4761689)
        self.assertEqual(
            report["bounded_laukika_subtotal_after_taddhita_expansion"]
            + report["bounded_vaidika_subtotal_unchanged"],
            report["combined_bounded_word_meaning_subtotal"],
        )


if __name__ == "__main__":
    unittest.main()

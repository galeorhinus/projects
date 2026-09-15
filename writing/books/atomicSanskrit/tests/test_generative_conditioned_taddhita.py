import csv
import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis/generativity/results"


def csv_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class ConditionedTaddhitaTests(unittest.TestCase):
    def test_pinned_test_files_cover_both_taddhita_chapters(self):
        archive = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
        records = {}
        for name in ("manifest.json", "taddhita_manifest.json"):
            manifest = json.loads((archive / name).read_text())
            records.update({row["filename"]: row for row in manifest["sources"]})
        expected = {f"kashika_{chapter}_{section}.rs" for chapter in (4, 5) for section in range(1, 5)}
        self.assertTrue(expected.issubset(records))
        for name in expected:
            self.assertEqual(hashlib.sha256((archive / name).read_bytes()).hexdigest(), records[name]["sha256"])

    def test_source_extraction_partitions_positive_and_negative_assertions(self):
        report = json.loads((RESULTS / "conditioned_taddhita_source_examples.json").read_text())
        self.assertEqual(report["literal_conditioned_assertions"], 1056)
        self.assertEqual(report["positive_source_examples"], 1047)
        self.assertEqual(report["negative_source_examples"], 9)

    def test_semantic_and_input_reconciliation(self):
        semantics = json.loads((RESULTS / "conditioned_taddhita_semantic_classification.json").read_text())
        inputs = json.loads((RESULTS / "conditioned_taddhita_inputs.json").read_text())
        self.assertEqual(semantics["conditioned_candidates"], 1047)
        self.assertEqual(inputs["unique_conditioned_relations"], 1010)
        self.assertEqual(inputs["duplicate_assertions_collapsed"], 37)

    def test_engine_verification_preserves_mismatches_as_exclusions(self):
        report = json.loads((RESULTS / "conditioned_taddhita_verification.json").read_text())
        self.assertEqual(report["verified_relations"], 975)
        self.assertEqual(report["engine_mismatches_not_admitted"], 35)
        self.assertEqual(len(csv_rows(RESULTS / "conditioned_taddhita_verification.csv")), 1010)

    def test_reconciliation_and_subtotal(self):
        report = json.loads((RESULTS / "conditioned_taddhita_reconciliation.json").read_text())
        self.assertEqual(report["additional_conditioned_taddhita_word_meanings"], 975)
        self.assertEqual(report["combined_bounded_word_meaning_subtotal"], 4762664)
        self.assertEqual(len(csv_rows(RESULTS / "conditioned_taddhita_ledger.csv")), 975)
        self.assertEqual(len(csv_rows(RESULTS / "conditioned_taddhita_reconciliation_exclusions.csv")), 35)

    def test_same_spelling_can_retain_two_meanings(self):
        rows = csv_rows(RESULTS / "conditioned_taddhita_ledger.csv")
        aditya = [
            row for row in rows
            if row["input_form_slp1"] == "aditi"
            and "Aditya" in row["expected_output_forms_slp1"].split(";")
        ]
        self.assertEqual({row["semantic_context"] for row in aditya}, {"TasyaApatyam", "SaAsyaDevata"})


if __name__ == "__main__":
    unittest.main()

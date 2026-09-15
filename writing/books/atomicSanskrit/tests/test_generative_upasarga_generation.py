import csv
import json
from collections import Counter
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/generativity/build_upasarga_generation_ledger.py"
RESULTS = ROOT / "analysis/generativity/results"


class UpasargaGenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
        cls.report = json.loads((RESULTS / "upasarga_generation_summary.json").read_text())
        with (RESULTS / "upasarga_generation_ledger.csv").open() as handle:
            cls.ledger = list(csv.DictReader(handle))
        with (RESULTS / "upasarga_generation_exclusions.csv").open() as handle:
            cls.excluded = list(csv.DictReader(handle))

    def test_full_matrix_count(self):
        self.assertEqual(self.report["original_base_word_meanings"], 2634)
        self.assertEqual(self.report["normalized_upasarga_identities"], 20)
        self.assertEqual(self.report["generated_upasarga_word_meanings"], 52567)
        self.assertEqual(len(self.ledger), 52567)

    def test_every_source_entry_operation_generates(self):
        self.assertEqual(self.report["source_entry_operations_tested"], 44580)
        self.assertEqual(self.report["source_entry_operations_with_output"], 44580)
        self.assertEqual(self.report["source_entry_zero_outputs"], 0)

    def test_each_prefix_covers_every_base_meaning(self):
        self.assertEqual(Counter(row["upasarga_id"] for row in self.ledger), Counter({
            "pra": 2628, "para": 2628, "apa": 2628, "sam": 2628, "anu": 2628,
            "ava": 2628, "nis": 2628, "dus": 2628, "vi": 2628, "ang": 2632,
            "ni": 2628, "adhi": 2630, "api": 2628, "ati": 2628, "su": 2628,
            "ut": 2629, "abhi": 2628, "prati": 2628, "pari": 2628, "upa": 2628,
        }))

    def test_generated_identities_are_unique(self):
        ids = [row["generated_word_meaning_id"] for row in self.ledger]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(row["count_status"] == "admitted_generated_capacity" for row in self.ledger))
        self.assertEqual(Counter(row["semantic_status"] for row in self.ledger), Counter({
            "generated_meaning_open": 52546,
            "source_attested_prefixed_meaning": 21,
        }))

    def test_attestation_is_not_an_admission_gate(self):
        self.assertEqual(self.report["meaning_status"]["generated_meaning_open"], 52546)
        self.assertEqual(self.report["meaning_status"]["source_attested_prefixed_meanings"], 21)
        self.assertEqual(self.report["meaning_status"]["known_glosses_attached"], 21)
        self.assertIn("not required", self.report["counting_standard"])

    def test_only_actual_conflicts_or_zero_outputs_are_excluded(self):
        self.assertEqual(self.report["documented_pair_conflicts"], 134)
        self.assertEqual(self.report["unresolved_zero_output_pairs"], 0)
        self.assertEqual(len(self.excluded), 134)
        self.assertTrue(all(
            row["count_status"] == "not_counted_documented_conflict"
            for row in self.excluded
        ))

    def test_subtotal_reconciles_without_stacking(self):
        self.assertEqual(self.report["prior_verbal_subtotal_including_bases"], 15156)
        self.assertEqual(self.report["bounded_verbal_capacity_subtotal"], 67723)
        self.assertIn("no sanadi operation", self.report["scope"])
        self.assertIsNone(self.report["vocabulary_total"])

    def test_sources_and_inputs_are_hashed(self):
        manifest = json.loads((ROOT / "working/40_reference/sources/archive/documents/generativity-pilot/manifest.json").read_text())
        self.assertEqual(self.report["manifest_source_count"], len(manifest["sources"]))
        self.assertEqual(len(self.report["sources"]), 7)
        self.assertTrue(all(len(row["sha256"]) == 64 for row in self.report["sources"]))
        self.assertTrue(all(len(value) == 64 for value in self.report["inputs"].values()))


if __name__ == "__main__":
    unittest.main()

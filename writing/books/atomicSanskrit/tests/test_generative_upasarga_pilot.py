import csv
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/generativity/run_upasarga_pilot.py"
HERE = ROOT / "analysis/generativity"
RESULTS = HERE / "results"


class UpasargaPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
        cls.report = json.loads((RESULTS / "upasarga_pilot.json").read_text())
        with (RESULTS / "upasarga_pilot.csv").open() as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_twenty_identities_preserve_twenty_two_listed_forms(self):
        self.assertEqual(self.report["inventory"]["normalized_upasarga_identities"], 20)
        self.assertEqual(self.report["inventory"]["listed_pradi_forms"], 22)
        self.assertEqual(len(self.rows), 20)

    def test_conditioned_forms_do_not_multiply_inventory(self):
        by_id = {row["upasarga_id"]: row for row in self.rows}
        self.assertEqual(by_id["nis"]["source_forms_slp1"], "nis;nir")
        self.assertEqual(by_id["dus"]["source_forms_slp1"], "dus;dur")

    def test_every_gam_generation_matches_the_pinned_expectation(self):
        self.assertEqual(self.report["pilot"]["operations_with_output"], 20)
        self.assertEqual(self.report["pilot"]["expectation_matches"], 20)
        self.assertTrue(all(row["matches_expected"] == "true" for row in self.rows))

    def test_alternative_outputs_do_not_multiply_a_relation(self):
        sam = next(row for row in self.rows if row["upasarga_id"] == "sam")
        self.assertEqual(sam["output_variant_count"], "2")
        self.assertEqual(set(sam["output_forms_slp1"].split(";")), {"saMgam", "saNgam"})
        self.assertEqual(self.report["pilot"]["distinct_output_spellings_diagnostic"], 21)

    def test_full_matrix_capacity_is_declared_without_pilot_double_count(self):
        matrix = self.report["planned_full_matrix"]
        self.assertEqual(matrix["original_base_word_meanings"], 2634)
        self.assertEqual(matrix["structural_operation_base_pairs"], 52680)
        self.assertEqual(matrix["pre_restriction_candidates"], 52680)
        self.assertEqual(self.report["pilot"]["generated_capacity_relations"], 20)
        self.assertEqual(self.report["pilot"]["separately_added_to_subtotal"], 0)
        self.assertIsNone(self.report["vocabulary_total"])

    def test_scope_excludes_stacking_and_inflection(self):
        self.assertIn("no sanadi operation", self.report["scope"])
        self.assertIn("stacking", self.report["scope"])
        self.assertIn("inflection", self.report["scope"])
        self.assertTrue(all(row["count_status"] == "pilot_subset_not_added_separately" for row in self.rows))
        self.assertTrue(all(row["semantic_status"] == "generated_meaning_open" for row in self.rows))

    def test_sources_and_inputs_are_hashed(self):
        manifest = json.loads((ROOT / "working/40_reference/sources/archive/documents/generativity-pilot/manifest.json").read_text())
        self.assertEqual(self.report["manifest_source_count"], len(manifest["sources"]))
        self.assertEqual(len(self.report["sources"]), 6)
        self.assertTrue(all(len(row["sha256"]) == 64 for row in self.report["sources"]))
        self.assertTrue(all(len(value) == 64 for value in self.report["inputs"].values()))


if __name__ == "__main__":
    unittest.main()

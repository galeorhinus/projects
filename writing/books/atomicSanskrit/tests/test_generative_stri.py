import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis/generativity"
RESULTS = ANALYSIS / "results"
ARCHIVE = ROOT / "working/40_reference/sources/archive/documents/generativity-pilot"
SCRIPTS = (
    "classify_stri_inventory.py",
    "extract_stri_source_examples.py",
    "build_stri_eligibility.py",
    "verify_stri_examples.py",
    "reconcile_stri_ledger.py",
    "build_stri_six_pass_summary.py",
)


def csv_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class StriExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for name in SCRIPTS:
            subprocess.run([sys.executable, str(ANALYSIS / name)], cwd=ROOT, check=True, capture_output=True)

    def test_pinned_source_integrity(self):
        manifest = json.loads((ARCHIVE / "stri_manifest.json").read_text())
        self.assertEqual(manifest["generator_commit"], "f3ba4167d40eebc4b3023d24e66867aa6a8cdb32")
        self.assertEqual(len(manifest["sources"]), 5)
        for row in manifest["sources"]:
            self.assertEqual(hashlib.sha256((ARCHIVE / row["filename"]).read_bytes()).hexdigest(), row["sha256"])

    def test_suffix_inventory_is_complete(self):
        report = json.loads((RESULTS / "stri_suffix_inventory.json").read_text())
        self.assertEqual(report["pinned_suffix_identifiers"], 7)
        self.assertEqual(set(report["identifiers"]), {"cAp", "wAp", "qAp", "NIn", "NIp", "NIz", "UN"})

    def test_source_assertions_and_eligibility_reconcile(self):
        source = json.loads((RESULTS / "stri_source_examples.json").read_text())
        eligibility = json.loads((RESULTS / "stri_eligibility.json").read_text())
        self.assertEqual((source["source_assertions"], source["active_assertions"], source["ignored_assertions"]), (77, 66, 11))
        self.assertEqual(eligibility["unique_source_demonstrated_inputs"], 65)
        self.assertEqual(eligibility["duplicate_assertions_collapsed"], 1)
        self.assertFalse(eligibility["broad_nominal_multiplier_applied"])

    def test_engine_requires_an_actual_stri_suffix(self):
        report = json.loads((RESULTS / "stri_verification.json").read_text())
        self.assertEqual(report["verified_stri_derivations"], 50)
        self.assertEqual(report["inflection_only_relations_not_admitted"], 5)
        self.assertEqual(report["engine_mismatches_not_admitted"], 10)
        self.assertEqual(set(report["suffixes_observed"]), {"wAp", "NIp", "NIz", "UN"})

    def test_inflection_only_bases_remain_outside_ledger(self):
        ledger_inputs = {row["input_form_slp1"] for row in csv_rows(RESULTS / "stri_ledger.csv")}
        exclusions = {row["input_form_slp1"]: row["verification_status"] for row in csv_rows(RESULTS / "stri_exclusions.csv")}
        for form in ("svasf", "duhitf", "nanAndf", "yAtf", "mAtf"):
            self.assertNotIn(form, ledger_inputs)
            self.assertEqual(exclusions[form], "inflection_only_no_stri_derivation")

    def test_subtotal_and_examples(self):
        report = json.loads((RESULTS / "stri_six_pass_summary.json").read_text())
        self.assertEqual(report["passes_completed"], 6)
        self.assertEqual(report["additional_stri_word_meanings"], 50)
        self.assertEqual(report["combined_bounded_word_meaning_subtotal"], 4762714)
        rows = {row["input_form_slp1"]: row for row in csv_rows(RESULTS / "stri_ledger.csv")}
        self.assertEqual(rows["aja"]["expected_nominative_forms_slp1"], "ajA")
        self.assertEqual(rows["kartf"]["expected_nominative_forms_slp1"], "kartrI")
        self.assertEqual(rows["indra"]["expected_nominative_forms_slp1"], "indrARI")


if __name__ == "__main__":
    unittest.main()

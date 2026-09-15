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
    "classify_samasa_inventory.py",
    "extract_samasa_source_examples.py",
    "build_samasa_eligibility.py",
    "verify_samasa_examples.py",
    "reconcile_samasa_ledger.py",
    "build_samasa_six_pass_summary.py",
)


def csv_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class SamasaExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for name in SCRIPTS:
            subprocess.run([sys.executable, str(ANALYSIS / name)], cwd=ROOT, check=True, capture_output=True)

    def test_pinned_sources(self):
        manifest = json.loads((ARCHIVE / "samasa_manifest.json").read_text())
        self.assertEqual(manifest["generator_commit"], "f3ba4167d40eebc4b3023d24e66867aa6a8cdb32")
        self.assertEqual(len(manifest["sources"]), 42)
        for row in manifest["sources"]:
            path = ARCHIVE / row["filename"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row["sha256"])

    def test_type_inventory(self):
        report = json.loads((RESULTS / "samasa_type_inventory.json").read_text())
        self.assertEqual(report["implemented_type_count"], 8)
        self.assertFalse(report["broad_multiplier_applied"])

    def test_source_and_eligibility_counts(self):
        source = json.loads((RESULTS / "samasa_source_examples.json").read_text())
        eligible = json.loads((RESULTS / "samasa_eligibility.json").read_text())
        self.assertEqual((source["source_assertions"], source["active_assertions"], source["ignored_assertions"]), (167, 132, 35))
        self.assertEqual(eligible["unique_eligible_relations"], 113)
        self.assertEqual(eligible["duplicate_assertions_collapsed"], 7)
        self.assertFalse(eligible["recursive_compounding_admitted"])

    def test_verification_claim_is_precise(self):
        report = json.loads((RESULTS / "samasa_verification.json").read_text())
        self.assertEqual(report["relations_asserted_by_pinned_active_tests"], 113)
        verifier = ROOT / "analysis/generativity/rust/samasa_verifier/target/release/samasa-verifier"
        expected = 113 if verifier.exists() else 0
        self.assertEqual(report["locally_regenerated_relations"], expected)
        self.assertEqual(report["local_execution_status"], "completed" if verifier.exists() else "not_run_rust_toolchain_unavailable")

    def test_subtotal_and_known_examples(self):
        report = json.loads((RESULTS / "samasa_six_pass_summary.json").read_text())
        self.assertEqual(report["additional_samasa_word_meanings"], 113)
        self.assertEqual(report["combined_bounded_word_meaning_subtotal"], 12_845_500)
        self.assertEqual(report["remaining_passes"], 18)
        graph = json.loads((RESULTS / "generation_stage_graph.json").read_text())
        stage = next(node for node in graph["nodes"] if node["id"] == "source_samasa")
        self.assertEqual(stage["cumulative_count"], 12_845_500)
        self.assertNotIn("compound_expansion_pending", {node["id"] for node in graph["nodes"]})
        forms = {form for row in csv_rows(RESULTS / "samasa_ledger.csv") for form in row["output_forms_slp1"].split(";")}
        for form in ("rAjapuruza", "mahApuruza", "plakzanyagroDa", "vAktvaca", "grAmagata"):
            self.assertIn(form, forms)


if __name__ == "__main__":
    unittest.main()

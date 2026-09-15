import csv
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/generativity/build_verbal_derivation_ledger.py"
RESULTS = ROOT / "analysis/generativity/results"


class VerbalDerivationLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
        cls.report = json.loads((RESULTS / "verbal_derivation_summary.json").read_text())
        with (RESULTS / "verbal_derivation_ledger.csv").open() as handle:
            cls.ledger = list(csv.DictReader(handle))
        with (RESULTS / "verbal_derivation_exclusions.csv").open() as handle:
            cls.excluded = list(csv.DictReader(handle))

    def test_operation_subtotals_are_stable(self):
        self.assertEqual(self.report["admitted_by_operation"], {
            "causative": 2112,
            "desiderative": 2634,
            "intensive": 3888,
            "intensive_luk": 3888,
        })
        self.assertEqual(self.report["admitted_derived_word_meanings"], 12522)
        self.assertEqual(self.report["verbal_word_meanings_including_bases"], 15156)

    def test_yan_semantic_branches_are_stable(self):
        branches = self.report["admitted_by_operation_and_branch"]
        expected = {
            "crooked_movement": 289,
            "disparaged_action": 15,
            "intensity": 1792,
            "repetition": 1792,
        }
        for operation in ("intensive", "intensive_luk"):
            self.assertEqual(
                {key.split(":", 1)[1]: value for key, value in branches.items() if key.startswith(operation + ":")},
                expected,
            )

    def test_curadi_first_nic_is_not_counted_as_causative(self):
        excluded = [row for row in self.excluded if row["count_status"] == "not_counted_class_forming_nic"]
        self.assertEqual(len(excluded), 522)
        admitted_keys = {row["base_count_key"] for row in self.ledger if row["operation_id"] == "causative"}
        self.assertTrue(all(row["base_count_key"] not in admitted_keys for row in excluded))

    def test_desiderative_covers_every_reconciled_base_meaning(self):
        rows = [row for row in self.ledger if row["operation_id"] == "desiderative"]
        self.assertEqual(len(rows), 2634)
        self.assertEqual(len({row["base_count_key"] for row in rows}), 2634)

    def test_anabhidhana_controls_are_excluded_from_yan_and_yan_luk(self):
        excluded = [row for row in self.excluded if row["count_status"] == "not_counted_anabhidhana"]
        self.assertEqual(len(excluded), 6)
        self.assertEqual({row["operation_id"] for row in excluded}, {"intensive", "intensive_luk"})
        self.assertTrue(all(set(row["base_source_codes"].split(";")) & {"01.0847", "06.0046"} for row in excluded))

    def test_zero_engine_outputs_remain_unresolved(self):
        rows = [row for row in self.excluded if row["count_status"] == "not_admitted_engine_zero_unresolved"]
        self.assertEqual(len(rows), 1070)
        self.assertEqual({row["operation_id"] for row in rows}, {"intensive", "intensive_luk"})

    def test_each_ledger_row_has_one_unique_semantic_identity(self):
        ids = [row["derived_word_meaning_id"] for row in self.ledger]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(row["count_status"] == "admitted_research_ledger" for row in self.ledger))
        self.assertTrue(all(row["output_forms_slp1"] for row in self.ledger))

    def test_report_is_research_only_and_source_backed(self):
        self.assertIsNone(self.report["vocabulary_total"])
        self.assertEqual(self.report["publication_status"], "research_subtotal_only_not_deployed")
        manifest = json.loads((ROOT / "working/40_reference/sources/archive/documents/generativity-pilot/manifest.json").read_text())
        self.assertEqual(self.report["manifest_source_count"], len(manifest["sources"]))
        self.assertEqual(len(self.report["sources"]), 8)
        self.assertTrue(all(len(row["sha256"]) == 64 for row in self.report["sources"]))


if __name__ == "__main__":
    unittest.main()

import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/generativity/build_operation_inventory.py"
RESULTS = ROOT / "analysis/generativity/results"


class OperationInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(["python3", str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
        cls.payload = json.loads((RESULTS / "operation_inventory.json").read_text())
        with (RESULTS / "operation_inventory.csv").open() as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_complete_pinned_engine_census(self):
        self.assertEqual(self.payload["counts"]["total_identifiers"], 304)
        self.assertEqual(self.payload["counts"]["by_family"], {"sanadi": 7, "krt": 122, "taddhita": 175})
        self.assertEqual(len(self.rows), 304)
        self.assertEqual(len({row["catalog_id"] for row in self.rows}), 304)

    def test_inventory_never_becomes_a_multiplier(self):
        self.assertEqual(self.payload["counts"]["admitted_to_count"], 0)
        self.assertTrue(all(row["count_status"] == "not_admitted" for row in self.rows))

    def test_every_row_has_archived_source_and_status(self):
        for row in self.rows:
            self.assertTrue(row["source_url"].startswith("https://"))
            self.assertEqual(len(row["source_sha256"]), 64)
            self.assertIn(row["semantic_status"], {"seeded", "pending"})
            self.assertIn(row["eligibility_status"], {"example_scope_only", "pending"})

    def test_all_curated_affixes_are_linked(self):
        spec = importlib.util.spec_from_file_location("operation_inventory", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        curated_affix_rows = [row for row in module.curated_rows() if row["affix_slp1"]]
        linked_ids = {item for row in self.rows for item in row["curated_operation_ids"].split(";") if item}
        self.assertEqual(linked_ids, {row["id"] for row in curated_affix_rows})

    def test_family_table_keeps_inflection_separate(self):
        with (ROOT / "analysis/generativity/operation_families.csv").open() as handle:
            families = {row["id"]: row for row in csv.DictReader(handle)}
        self.assertEqual(families["tin"]["lexical_role"], "inflection")
        self.assertEqual(families["sup"]["lexical_role"], "inflection")
        self.assertEqual(families["krt"]["lexical_role"], "derived_word")
        self.assertEqual(families["taddhita"]["lexical_role"], "derived_word")


if __name__ == "__main__":
    unittest.main()

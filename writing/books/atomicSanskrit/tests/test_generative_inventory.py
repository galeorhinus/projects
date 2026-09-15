import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "generative_inventory", ROOT / "analysis/generativity/audit_inventory.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class InventoryAuditTests(unittest.TestCase):
    def run_audit(self, content):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "inventory.csv"
            source.write_text(content, encoding="utf-8")
            return MODULE.audit(source)

    def test_entries_remain_distinct_when_spelling_matches(self):
        result = self.run_audit("1,1,BU\n1,2,BU\n# 1,3,gam\n\n")
        self.assertEqual(result["active_entries"], 2)
        self.assertEqual(result["distinct_citation_spellings"], 1)
        self.assertEqual(result["distinct_normalized_spellings"], 1)
        self.assertEqual(result["commented_rows_excluded"], 1)

    def test_duplicate_identifier_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate entry identifier"):
            self.run_audit("1,1,BU\n1,1,gam\n")

    def test_bad_rows_are_rejected(self):
        for row in ("1,1\n", "1,1,\n", "11,1,BU\n", "1,0,BU\n"):
            with self.subTest(row=row), self.assertRaises(ValueError):
                self.run_audit(row)

    def test_existing_inventory(self):
        result = MODULE.audit(MODULE.DEFAULT_SOURCE)
        self.assertEqual(result["active_entries"], 2168)
        self.assertEqual(result["commented_rows_excluded"], 67)
        self.assertEqual(result["distinct_citation_spellings"], 1910)
        self.assertEqual(result["distinct_normalized_spellings"], 1518)
        self.assertEqual(result["empty_normalized_entries"], 0)


if __name__ == "__main__":
    unittest.main()

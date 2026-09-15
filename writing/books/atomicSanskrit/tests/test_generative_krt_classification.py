import csv
import json
from collections import Counter
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/generativity/classify_krt_inventory.py"
RESULTS = ROOT / "analysis/generativity/results"


class KrtClassificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
        cls.report = json.loads((RESULTS / "krt_classification.json").read_text())
        with (RESULTS / "krt_classification.csv").open() as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_all_identifiers_are_classified_once(self):
        self.assertEqual(len(self.rows), 122)
        self.assertEqual(len({row["source_variant"] for row in self.rows}), 122)
        self.assertEqual(sum(self.report["classification_counts"].values()), 122)

    def test_source_properties_match_pinned_inventory(self):
        self.assertEqual(self.report["property_counts"], {
            "vedic_only": 19,
            "avyaya": 21,
            "near_duplicate": 7,
        })

    def test_source_rules_correct_engine_avyaya_metadata(self):
        by_variant = {row["source_variant"]: row for row in self.rows}
        for variant in ("kamul", "kase", "kasen"):
            self.assertEqual(by_variant[variant]["primary_classification"], "vedic_only_deferred")
        self.assertEqual(self.report["classification_counts"]["laukika_avyaya_deferred"], 3)

    def test_bounded_selection(self):
        self.assertEqual(self.report["bounded_laukika_identifiers"], 12)
        self.assertEqual(self.report["bounded_laukika_semantic_operations"], 14)
        selected = [row for row in self.rows if row["count_status"] == "eligible_for_bounded_generation"]
        self.assertEqual(len(selected), 12)
        self.assertEqual(sum(int(row["bounded_semantic_operation_count"]) for row in selected), 14)

    def test_primary_classes_are_exhaustive(self):
        self.assertEqual(Counter(row["primary_classification"] for row in self.rows), Counter(self.report["classification_counts"]))


if __name__ == "__main__":
    unittest.main()

import csv
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/generativity/build_avyaya_ledger.py"
RESULTS = ROOT / "analysis/generativity/results"


class AvyayaLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
        cls.report = json.loads((RESULTS / "avyaya_summary.json").read_text())
        with (RESULTS / "avyaya_ledger.csv").open() as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_three_source_corrected_laukika_operations(self):
        self.assertEqual(self.report["selected_laukika_avyaya_identifiers"], 3)
        self.assertEqual(self.report["selected_semantic_operations"], 3)
        self.assertEqual({row["krt_source_variant"] for row in self.rows}, {"tumun", "ktvA", "Ramul"})

    def test_every_operation_covers_every_base_meaning(self):
        self.assertEqual(self.report["admitted_by_operation"], {
            "prior_action_ktva": 2634,
            "purpose_tumun": 2634,
            "repeated_prior_action_namul": 2634,
        })
        self.assertEqual(self.report["admitted_avyaya_word_meanings"], 7902)
        self.assertEqual(self.report["not_admitted_total"], 0)

    def test_vedic_identifiers_remain_outside(self):
        self.assertEqual(
            {row["source_variant"] for row in self.report["deferred_or_excluded_identifiers"]},
            {"kamul", "kase", "kasen"},
        )

    def test_subtotal_reconciles(self):
        self.assertEqual(self.report["bounded_word_meaning_subtotal"], 1407523)
        self.assertEqual(len({row["derived_word_meaning_id"] for row in self.rows}), len(self.rows))


if __name__ == "__main__":
    unittest.main()

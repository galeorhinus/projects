import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/generativity/audit_upasarga_restrictions.py"
HERE = ROOT / "analysis/generativity"
RESULTS = HERE / "results"


class UpasargaRestrictionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True)
        cls.conflicts = json.loads((HERE / "upasarga_conflicts.json").read_text())
        cls.report = json.loads((RESULTS / "upasarga_restriction_audit.json").read_text())

    def test_every_source_quote_is_verified(self):
        self.assertEqual(self.report["restriction_groups"], 7)
        self.assertEqual(self.report["non_subtractive_annotations"], 3)
        self.assertEqual(self.report["prefixed_meaning_enrichments"], 2)
        self.assertEqual(self.report["enriched_word_meanings"], 21)
        self.assertEqual(len(self.report["source"]["sha256"]), 64)

    def test_exact_exclusion_count(self):
        self.assertEqual(self.report["pair_exclusions"], 134)
        self.assertEqual(len(self.conflicts["exclusions"]), 134)

    def test_named_prefix_restrictions(self):
        groups = {row["source_code"]: row for row in self.conflicts["restriction_groups"]}
        self.assertEqual(groups["01.0716"]["allowed_upasarga_ids"], ["ang"])
        self.assertEqual(groups["02.0041"]["allowed_upasarga_ids"], ["adhi"])
        self.assertEqual(groups["10.0401"]["allowed_upasarga_ids"], [])
        self.assertEqual(groups["10.0401"]["exclusion_count"], 20)

    def test_attestation_is_not_used_as_an_exclusion(self):
        self.assertIn("Missing attestation is never an exclusion", self.conflicts["status"])
        self.assertTrue(all(row["rule_refs"] for row in self.conflicts["exclusions"]))
        self.assertTrue(all(row["source_quote"] for row in self.conflicts["exclusions"]))


if __name__ == "__main__":
    unittest.main()

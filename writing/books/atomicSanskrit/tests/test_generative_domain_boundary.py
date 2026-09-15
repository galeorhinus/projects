import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis/generativity/results"


class DomainBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(
            [sys.executable, str(ROOT / "analysis/generativity/audit_domain_boundary.py")],
            cwd=ROOT, check=True, capture_output=True,
        )
        cls.report = json.loads((RESULTS / "domain_boundary_audit.json").read_text())

    def test_known_restricted_sources(self):
        self.assertEqual(
            self.report["known_vedic_restricted_source_codes"],
            ["02.0072", "03.0015", "05.0014"],
        )
        self.assertEqual(self.report["known_vedic_restricted_base_meanings"], 11)
        self.assertTrue(all(
            row["mixed_restricted_and_unrestricted_rows"] == 0
            for row in self.report["layers"]
        ))

    def test_domain_subtotal(self):
        self.assertEqual(self.report["gross_bounded_word_meaning_subtotal"], 2174721)
        self.assertEqual(self.report["known_vedic_restricted_base_and_descendant_rows"], 8660)
        self.assertEqual(
            self.report["bounded_laukika_subtotal_after_known_domain_restrictions"],
            2166061,
        )
        self.assertEqual(self.report["vedic_generation_status"], "completed")


if __name__ == "__main__":
    unittest.main()

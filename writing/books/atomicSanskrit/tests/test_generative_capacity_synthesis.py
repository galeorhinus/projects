import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis/generativity"
RESULTS = ANALYSIS / "results"
SCRIPTS = (
    "reconcile_integrated_grammatical_capacity.py",
    "reconcile_vaidika_capacity_boundary.py",
    "build_publication_capacity_cascade.py",
    "audit_manuscript_generativity_claims.py",
    "build_generativity_manuscript_proposal.py",
    "build_generativity_synthesis_report.py",
)


class CapacitySynthesisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for name in SCRIPTS:
            subprocess.run(
                [sys.executable, str(ANALYSIS / name)], cwd=ROOT,
                check=True, capture_output=True,
            )

    def test_integrated_laukika_capacity(self):
        report = json.loads((RESULTS / "integrated_grammatical_capacity.json").read_text())
        self.assertEqual(report["laukika_lexical_word_meanings"], 12_633_060)
        self.assertEqual(report["action_grammatical_cells"], 408_676_320)
        self.assertEqual(report["name_grammatical_cells"], 194_022_888)
        self.assertEqual(report["complete_unchanging_word_meanings"], 7_925)
        self.assertEqual(report["integrated_laukika_grammatical_cells"], 602_707_133)
        self.assertFalse(report["lexical_subtotal_added_to_capacity"])

    def test_vaidika_boundary_keeps_units_separate(self):
        report = json.loads((RESULTS / "vaidika_capacity_boundary.json").read_text())
        self.assertEqual(report["bounded_lexical_word_meanings"], 12_846_458)
        self.assertEqual(report["vaidika_lexical_word_meanings"], 213_398)
        self.assertFalse(report["vaidika_inflection_modeled"])
        self.assertFalse(report["mixed_unit_grand_total_published"])

    def test_publication_cascade(self):
        report = json.loads((RESULTS / "publication_capacity_cascade.json").read_text())
        counts = [stage["count"] for stage in report["stages"]]
        self.assertEqual(counts[0], 2_634)
        self.assertEqual(counts[-2], 12_846_458)
        self.assertEqual(counts[-1], 602_707_133)
        self.assertTrue(all(stage["examples"] for stage in report["stages"]))
        self.assertFalse(report["recursive_compound_capacity_enters_headline"])
        wordspace = json.loads((RESULTS / "wordspace_category_graph.json").read_text())
        labels = {node["id"]: node["label"] for node in wordspace["nodes"]}
        self.assertEqual(labels["action_meanings"], "क्रियार्थाः")
        self.assertEqual(labels["name_meanings"], "नामार्थाः")
        self.assertEqual(labels["unchanging_meanings"], "अव्ययानि")

    def test_audit_and_deployment_record_match_manuscript(self):
        audit = json.loads((RESULTS / "manuscript_generativity_claim_audit.json").read_text())
        proposal = json.loads((RESULTS / "generativity_manuscript_proposal.json").read_text())
        self.assertEqual(audit["body_deployments_verified"], 2)
        self.assertEqual(audit["endnote_deployments_verified"], 1)
        self.assertEqual(audit["obsolete_count_occurrences"], 0)
        self.assertFalse(audit["stale_deployment_found"])
        self.assertTrue(audit["manuscript_modified"])
        self.assertEqual(proposal["status"], "deployed")
        self.assertTrue(proposal["manuscript_modified"])
        self.assertEqual(len(proposal["proposals"]), 3)
        for item in proposal["proposals"]:
            self.assertIn("602,707,133", item["after"])
        chapter_12 = next(item for item in proposal["proposals"] if item["deployment"] == "Chapter 12 §12.7")
        self.assertIn("This gives Bṛhaspati's thousand divine years", chapter_12["after"])

    def test_final_synthesis(self):
        report = json.loads((RESULTS / "generativity_six_pass_synthesis.json").read_text())
        self.assertEqual(report["passes_completed"], 6)
        self.assertEqual(report["publication_endpoint_unit"], "semantic_grammatical_cell")
        self.assertEqual(report["manuscript_targets_audited"], 3)
        self.assertEqual(report["manuscript_proposals_prepared"], 3)
        self.assertTrue(report["manuscript_modified"])
        self.assertEqual(report["full_generative_test_suite"]["tests_run"], 276)
        self.assertEqual(report["full_generative_test_suite"]["status"], "passed")


if __name__ == "__main__":
    unittest.main()

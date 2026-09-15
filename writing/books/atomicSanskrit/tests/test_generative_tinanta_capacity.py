import csv
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis/generativity"
RESULTS = ANALYSIS / "results"
SCRIPTS = (
    "classify_tinanta_inventory.py",
    "build_tinanta_verbal_inventory.py",
    "classify_tinanta_reconstruction.py",
    "build_tinanta_citation_capacity.py",
    "build_tinanta_citation_sample.py",
    "build_tinanta_citation_six_pass_summary.py",
    "build_tinanta_paradigm_capacity.py",
    "classify_tinanta_pada_outputs.py",
    "build_tinanta_paradigm_sample.py",
    "analyze_tinanta_sample_collisions.py",
    "reconcile_tinanta_capacity.py",
    "build_tinanta_twelve_pass_summary.py",
)


class TinantaCapacityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for name in SCRIPTS:
            subprocess.run(
                [sys.executable, str(ANALYSIS / name)], cwd=ROOT,
                check=True, capture_output=True,
            )

    def test_lakara_boundary(self):
        report = json.loads((RESULTS / "tinanta_lakara_classification.json").read_text())
        self.assertEqual(report["engine_lakaras"], 11)
        self.assertEqual(report["counted_laukika_lakaras"], 10)
        self.assertEqual(report["withheld_vaidika_lakaras"], 1)
        with (RESULTS / "tinanta_lakara_classification.csv").open(newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual({row["id"] for row in rows if row["disposition"] == "withheld_vaidika_domain"}, {"let"})

    def test_virtual_verbal_inventory(self):
        report = json.loads((RESULTS / "tinanta_verbal_inventory.json").read_text())
        self.assertEqual(report["laukika_verbal_word_meanings"], 4_540_848)
        self.assertEqual(sum(report["counts_by_source_layer"].values()), 4_540_848)
        self.assertFalse(report["full_inventory_duplicated"])
        self.assertEqual(report["materialized_sample_records"], 9)

    def test_citation_capacity_and_sample(self):
        capacity = json.loads((RESULTS / "tinanta_citation_capacity.json").read_text())
        sample = json.loads((RESULTS / "tinanta_citation_sample.json").read_text())
        self.assertEqual(capacity["citation_semantic_cells"], 45_408_480)
        self.assertFalse(capacity["pada_series_multiplier_applied"])
        self.assertEqual(sample["sample_reconstruction_classes"], 8)
        self.assertEqual(sample["requested_citation_cells"], 90)
        self.assertEqual(sample["locally_regenerated_cells"], 90)

    def test_full_paradigm_capacity_and_sample(self):
        capacity = json.loads((RESULTS / "tinanta_paradigm_capacity.json").read_text())
        sample = json.loads((RESULTS / "tinanta_paradigm_sample.json").read_text())
        self.assertEqual(capacity["person_number_cells_per_lakara"], 9)
        self.assertEqual(capacity["full_kartari_tinanta_semantic_cells"], 408_676_320)
        self.assertEqual(sample["semantic_cells_requested"], 270)
        self.assertEqual(sample["semantic_cells_locally_regenerated"], 270)

    def test_pada_and_collision_policy(self):
        pada = json.loads((RESULTS / "tinanta_pada_classification.json").read_text())
        collisions = json.loads((RESULTS / "tinanta_sample_collisions.json").read_text())
        self.assertEqual(pada["automatic_pada_multiplier"], 1)
        self.assertGreater(pada["sample_profile"]["atmanepada_only"], 0)
        self.assertGreater(pada["sample_profile"]["both"], 0)
        self.assertEqual(collisions["spellings_shared_across_semantic_cells"], 13)

    def test_reconciliation_and_graph(self):
        report = json.loads((RESULTS / "tinanta_twelve_pass_summary.json").read_text())
        self.assertEqual(report["passes_completed"], 12)
        self.assertEqual(report["materialized_lexical_word_meaning_subtotal"], 12_846_458)
        self.assertFalse(report["inflectional_cells_added_to_lexical_subtotal"])
        self.assertEqual(report["remaining_tinanta_passes"], 0)
        graph = json.loads((RESULTS / "generation_stage_graph.json").read_text())
        nodes = {node["id"]: node for node in graph["nodes"]}
        self.assertNotIn("tinanta_expansion_pending", nodes)
        for node_id in ("laukika_verbal_inventory", "tinanta_citation_capacity", "tinanta_paradigm_capacity"):
            self.assertFalse(nodes[node_id]["included_in_current_research_subtotal"])


if __name__ == "__main__":
    unittest.main()

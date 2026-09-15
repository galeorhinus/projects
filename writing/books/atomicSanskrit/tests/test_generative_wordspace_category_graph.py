import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis/generativity"
RESULTS = ANALYSIS / "results"


class WordspaceCategoryGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(
            [sys.executable, str(ANALYSIS / "build_wordspace_category_graph.py")],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
        cls.report = json.loads((RESULTS / "wordspace_category_graph.json").read_text())
        cls.nodes = {node["id"]: node for node in cls.report["nodes"]}

    def test_domain_partition_reconciles(self):
        self.assertEqual(self.nodes["all_word_meanings"]["count"], 12_846_458)
        self.assertEqual(self.nodes["vedic_word_meanings"]["count"], 213_398)
        self.assertEqual(self.nodes["ordinary_word_meanings"]["count"], 12_633_060)
        self.assertEqual(
            self.nodes["all_word_meanings"]["count"],
            self.nodes["vedic_word_meanings"]["count"]
            + self.nodes["ordinary_word_meanings"]["count"],
        )

    def test_ordinary_partition_reconciles(self):
        self.assertEqual(self.nodes["action_meanings"]["count"], 4_540_848)
        self.assertEqual(self.nodes["name_meanings"]["count"], 8_084_287)
        self.assertEqual(self.nodes["unchanging_meanings"]["count"], 7_925)
        self.assertEqual(
            self.nodes["ordinary_word_meanings"]["count"],
            sum(
                self.nodes[node_id]["count"]
                for node_id in (
                    "action_meanings",
                    "name_meanings",
                    "unchanging_meanings",
                )
            ),
        )

    def test_grammatical_capacity_is_non_additive(self):
        self.assertEqual(self.nodes["ten_time_mood_forms"]["count"], 45_408_480)
        self.assertEqual(self.nodes["all_action_forms"]["count"], 408_676_320)
        self.assertEqual(self.nodes["name_citation_forms"]["count"], 8_084_287)
        self.assertEqual(self.nodes["all_name_forms"]["count"], 194_022_888)
        for node_id in ("ten_time_mood_forms", "all_action_forms", "name_citation_forms", "all_name_forms"):
            self.assertEqual(
                self.nodes[node_id]["count_role"],
                "non_additive_grammatical_capacity",
            )

    def test_reader_labels_avoid_paninian_category_names(self):
        labels = " ".join(node["label"] for node in self.report["nodes"])
        for term in ("प्रातिपदिक", "तिङन्त", "सुबन्त", "लकार", "पुरुष", "वचन"):
            self.assertNotIn(term, labels)


if __name__ == "__main__":
    unittest.main()

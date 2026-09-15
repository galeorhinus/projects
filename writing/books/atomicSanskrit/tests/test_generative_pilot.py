import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
HAS_ENGINE = importlib.util.find_spec("vidyut") is not None
if HAS_ENGINE:
    SPEC = importlib.util.spec_from_file_location(
        "generative_pilot", ROOT / "analysis/generativity/run_pilot.py"
    )
    MODULE = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(MODULE)


@unittest.skipUnless(HAS_ENGINE, "Use build/generativity-venv/bin/python for integration tests")
class GenerativePilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        MODULE.verify_sources()
        cls.entries = {e.code: e for e in MODULE.Data(str(MODULE.ARCHIVE)).load_dhatu_entries()}
        cls.grammar = MODULE.Vyakarana()
        cls.cases = json.loads((MODULE.HERE / "pilot_cases.json").read_text())

    def test_all_declared_cases(self):
        results = MODULE.run_cases(self.cases, self.entries, self.grammar)
        for result in results:
            with self.subTest(case=result["id"]):
                self.assertTrue(result["matches_expected"], result["actual"])

    def test_spelling_deduplication_does_not_hide_an_unexpected_form(self):
        self.assertTrue(MODULE.compare(["x"], ["x", "x"])["matches_expected"])
        result = MODULE.compare(["x"], ["x", "y"])
        self.assertFalse(result["matches_expected"])
        self.assertEqual(result["unexpected"], ["y"])

    def test_inflection_counts_are_separate(self):
        groups = MODULE.inflection_sample(self.entries, self.grammar)
        self.assertEqual(groups[0]["filled_cells"], 9)
        self.assertEqual(groups[0]["distinct_spellings"], 9)
        self.assertEqual(groups[1]["filled_cells"], 24)
        self.assertEqual(groups[1]["distinct_spellings"], 18)

    def test_homonyms_keep_different_meanings(self):
        drink = self.entries["01.1074"]
        protect = self.entries["02.0051"]
        self.assertEqual(drink.dhatu.aupadeshika, protect.dhatu.aupadeshika)
        self.assertNotEqual(drink.artha, protect.artha)

    def test_crosswalk_preserves_every_local_entry(self):
        rows = MODULE.crosswalk()
        self.assertEqual(len(rows), 2168)
        self.assertEqual(len({r["local_code"] for r in rows}), 2168)
        for row in rows:
            if row["status"] in ("ambiguous_same_gana_citation", "no_exact_same_gana_citation"):
                self.assertEqual(row["selected_code"], "")


if __name__ == "__main__":
    unittest.main()

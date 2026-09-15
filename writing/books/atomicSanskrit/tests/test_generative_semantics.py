import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
HAS_ENGINE = importlib.util.find_spec("vidyut") is not None
if HAS_ENGINE:
    sys.path.insert(0, str(ROOT / "analysis/generativity"))
    try:
        import build_semantic_sample as MODULE
    finally:
        sys.path.pop(0)


@unittest.skipUnless(HAS_ENGINE, "Use build/generativity-venv/bin/python")
class SemanticSampleTests(unittest.TestCase):
    def row(self, word, sense, meaning):
        return {"word_id": word, "sense_id": sense, "meaning": meaning,
                "stage": "nominal", "actual": ["same-form"]}

    def test_same_form_different_meanings_stay_separate(self):
        rows = [self.row("karana", "action", "doing"),
                self.row("karana", "instrument", "instrument")]
        self.assertEqual(MODULE.semantic_counts(rows), {"nominal": 2})

    def test_different_words_with_same_meaning_stay_separate(self):
        rows = [self.row("gotva", "quality", "being a cow"),
                self.row("gota", "quality", "being a cow")]
        self.assertEqual(MODULE.semantic_counts(rows), {"nominal": 2})

    def test_repeated_record_does_not_double_same_word_and_meaning(self):
        row = self.row("karana", "action", "doing")
        self.assertEqual(MODULE.semantic_counts([row, dict(row)]), {"nominal": 1})

    def test_conflicting_meanings_cannot_share_an_identity(self):
        rows = [self.row("karana", "action", "doing"),
                self.row("karana", "action", "instrument")]
        with self.assertRaises(ValueError):
            MODULE.semantic_counts(rows)

    def test_sample_forms_and_counts(self):
        MODULE.verify_sources()
        sample = json.loads((MODULE.HERE / "semantic_sample.json").read_text())
        entries = {e.code: e for e in MODULE.Data(str(MODULE.ARCHIVE)).load_dhatu_entries()}
        records = MODULE.build_records(sample, entries, MODULE.Vyakarana())
        self.assertEqual(len(records), 28)
        self.assertEqual(MODULE.semantic_counts(records),
                         {"verbal": 13, "nominal": 12, "indeclinable": 3})
        self.assertTrue(all(r["form_check_passed"] for r in records))
        self.assertTrue(all(not r["semantic_condition_selected_by_engine"] for r in records))

    def test_all_citations_have_archived_sources(self):
        manifest = MODULE.verify_sources()
        sources = {s["filename"]: s for s in manifest["sources"]}
        sample = json.loads((MODULE.HERE / "semantic_sample.json").read_text())
        for entry in sample["entries"]:
            with self.subTest(entry=entry["word_id"], sense=entry["sense_id"]):
                self.assertTrue(MODULE.resolve_evidence(entry, sources))


if __name__ == "__main__":
    unittest.main()

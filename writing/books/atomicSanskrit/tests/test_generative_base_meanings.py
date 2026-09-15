import csv
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HAS_ENGINE = importlib.util.find_spec("vidyut") is not None
if HAS_ENGINE:
    sys.path.insert(0, str(ROOT / "analysis/generativity"))
    try:
        import build_base_meanings as MODULE
    finally:
        sys.path.pop(0)


@unittest.skipUnless(HAS_ENGINE, "Use build/generativity-venv/bin/python")
class BaseMeaningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = json.loads(MODULE.ANALYSIS.read_text())

    def parse(self, text):
        return MODULE.classify(text, self.rules)

    def test_two_meanings_from_one_entry(self):
        self.assertEqual(self.parse("stutO dIptO ca")["units"], ["stutO", "dIptO"])

    def test_anusvara_in_list_is_not_a_research_gap(self):
        self.assertEqual(self.parse("gatO hiMsAyAM saMvaraRe ca")["units"],
                         ["gatO", "hiMsAyAM", "saMvaraRe"])

    def test_qualified_phrase_not_split_into_extra_meanings(self):
        self.assertEqual(self.parse("vyaktAyAM vAci")["units"], ["vyaktAyAM vAci"])
        self.assertEqual(self.parse("avyakte Sabde suKe ca")["units"],
                         ["avyakte Sabde", "suKe"])
        self.assertEqual(self.parse("Sabde rozakfte gatO ca")["units"],
                         ["Sabde rozakfte", "gatO"])

    def test_explicit_compound_analysis(self):
        self.assertEqual(self.parse("gativfdDyoH")["units"], ["gatO", "vfdDO"])

    def test_unknown_compound_and_unspecified_meanings_remain_open(self):
        for gloss in ("anekArTatve", "anekArTAH", "unknownayoH", "tatkriyAyAm",
                      "vfdDisidDidrohadEvaparyAlocanAdizu ca"):
            with self.subTest(gloss=gloss):
                result = self.parse(gloss)
                self.assertEqual(result["status"], "needs_interpretation")
                self.assertEqual(result["units"], [])

    def test_parenthesis_and_overlapping_glosses_not_extra_senses(self):
        for gloss in ("aBiBave (nyUnIBavane nyUnIkaraRe ca)", "CAdane AcCAdane ca"):
            self.assertEqual(self.parse(gloss)["status"], "needs_interpretation")

    def test_repeated_list_member_not_counted_twice(self):
        self.assertEqual(self.parse("gatO gatO ca")["status"], "needs_interpretation")

    def test_homonyms_preserved_and_repeated_glosses_flagged(self):
        entries = [
            {"code": "01.0001", "dhatu": "pA", "artha": "pAne"},
            {"code": "02.0001", "dhatu": "pA", "artha": "rakzaRe"},
            {"code": "01.0002", "dhatu": "gam", "artha": "gatO"},
            {"code": "01.0003", "dhatu": "gam", "artha": "gatO"},
        ]
        rows = MODULE.identity_groups(entries)
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(not r["merged"] for r in rows))
        self.assertEqual({r["decision"] for r in rows}, {
            "same_gloss_identity_unresolved", "different_glosses_preserve_pending_sense_review"})

    def test_source_rows_and_placeholder_exclusion(self):
        MODULE.verify_sources()
        entries, placeholders = MODULE.load_source(MODULE.ARCHIVE / "dhatupatha.tsv")
        self.assertEqual((len(entries), len(placeholders)), (2229, 30))
        self.assertTrue(all(r["dhatu"] != "-" for r in entries))

    def test_duplicate_ids_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.tsv"
            path.write_text("code\tdhatu\tartha\n01.0001\tBU\tsattAyAm\n01.0001\tBU\tsattAyAm\n")
            with self.assertRaises(ValueError):
                MODULE.load_source(path)

    def test_generated_totals_and_provenance(self):
        report = json.loads((MODULE.RESULTS / "base_meanings.json").read_text())
        rows = report["entries"]
        self.assertEqual(len(rows), 2229)
        self.assertIsNone(report["vocabulary_total"])
        self.assertIsNone(report["local_inventory_meaning_total"])
        for path, digest in report["inputs"].items():
            self.assertEqual(MODULE.sha(ROOT / path), digest, path)
        for group in report["by_gana"]:
            self.assertEqual(group["source_entries"], group["single_gloss_entries"] +
                             group["enumerated_entries"] + group["unresolved_entries"] +
                             group["partial_entries"] + group["unenumerated_entries"])
        self.assertEqual(report["source_meaning_assignments"],
                         sum(r["assignment_count"] or 0 for r in rows))
        self.assertTrue(all(r["assignment_count"] is None for r in rows
                            if r["status"] in ("needs_interpretation", "unenumerated")))
        with (MODULE.RESULTS / "base_meaning_assignments.csv").open() as handle:
            assignments = list(csv.DictReader(handle))
        self.assertEqual(len(assignments), report["source_meaning_assignments"])
        self.assertEqual(len({(r["source_code"], r["meaning_id"]) for r in assignments}), len(assignments))

    def test_review_covers_exactly_the_original_interpretation_queue(self):
        entries, _ = MODULE.load_source(MODULE.ARCHIVE / "dhatupatha.tsv")
        sources = {s["filename"]: s for s in MODULE.verify_sources()["sources"]}
        review = json.loads(MODULE.REVIEW.read_text())
        resolved, opened, aliases = MODULE.review_index(review, entries, sources)
        initial_queue = {r["code"] for r in entries if self.parse(r["artha"])["status"] == "needs_interpretation"}
        self.assertEqual(set(resolved) | set(opened), initial_queue)
        self.assertEqual((len(resolved), len(opened)), (36, 2))
        self.assertEqual(sum(r.get("completeness") == "partial" for r in resolved.values()), 3)

    def test_variant_pairs_count_shared_meaning_once(self):
        report = json.loads((MODULE.RESULTS / "base_meanings.json").read_text())
        rows = {r["source_code"]: r for r in report["entries"]}
        self.assertEqual(rows["05.0014"]["units_slp1"], ["prItO", "pAlane", "jIvane"])
        self.assertEqual(rows["10.0429"]["units_slp1"], ["prItO", "darSane", "sevane"])
        self.assertEqual(rows["03.0001"]["units_slp1"], ["dAne", "adane", "AdAne", "prIRane"])

    def test_partial_counts_do_not_claim_complete_enumeration(self):
        report = json.loads((MODULE.RESULTS / "base_meanings.json").read_text())
        rows = {r["source_code"]: r for r in report["entries"]}
        for code, count in (("01.0365", 1), ("01.1158", 3), ("04.0077", 3)):
            self.assertEqual(rows[code]["status"], "partial_enumeration")
            self.assertEqual(rows[code]["assignment_count"], count)
            self.assertTrue(rows[code]["remaining_meaning_gap"])
        self.assertNotIn("drohe", rows["04.0077"]["units_slp1"])
        for code in ("01.0900", "01.0951"):
            self.assertEqual(rows[code]["status"], "unenumerated")
            self.assertIsNone(rows[code]["assignment_count"])

    def test_cross_reference_preserves_identity_and_meaning_provenance(self):
        report = json.loads((MODULE.RESULTS / "base_meanings.json").read_text())
        rows = {r["source_code"]: r for r in report["entries"]}
        self.assertEqual(rows["02.0043"]["assignment_count"], 6)
        self.assertEqual(rows["02.0072"]["assignment_count"], 6)
        self.assertNotEqual(rows["02.0043"]["provisional_word_id"], rows["02.0072"]["provisional_word_id"])
        with (MODULE.RESULTS / "base_meaning_assignments.csv").open() as handle:
            assignments = list(csv.DictReader(handle))
        for row in assignments:
            if row["source_code"] in ("02.0043", "02.0072"):
                evidence = json.loads(row["meaning_evidence"])
                self.assertIn(evidence["anchor"], MODULE.source_text(evidence["filename"]))
                self.assertEqual(evidence["sha256"], MODULE.sha(MODULE.ARCHIVE / evidence["filename"]))
                self.assertEqual(bool(row["cross_reference_evidence"]), row["source_code"] == "02.0072")

    def test_missing_per_meaning_evidence_is_rejected(self):
        entries, _ = MODULE.load_source(MODULE.ARCHIVE / "dhatupatha.tsv")
        sources = {s["filename"]: s for s in MODULE.verify_sources()["sources"]}
        review = json.loads(MODULE.REVIEW.read_text())
        item = next(r for r in review["decisions"] if r["id"] == "MR29")
        item["unit_evidence"].pop("jIvane")
        with self.assertRaisesRegex(ValueError, "Incomplete per-meaning evidence"):
            MODULE.review_index(review, entries, sources)
        item["unit_evidence"]["jIvane"] = {
            "source": "dhatu-mA894.html", "anchor": "invented locator", "reading": "alternative"}
        with self.assertRaisesRegex(ValueError, "Meaning witness not found"):
            MODULE.review_index(review, entries, sources)

    def test_commentary_controls_compound_grouping(self):
        report = json.loads((MODULE.RESULTS / "base_meanings.json").read_text())
        rows = {r["source_code"]: r for r in report["entries"]}
        self.assertEqual(rows["01.1018"]["assignment_count"], 5)
        self.assertIn("vAditragrahaRe", rows["01.1018"]["units_slp1"])
        self.assertEqual(rows["04.0047"]["units_slp1"], ["gatitvaraRe", "hiMsane"])
        self.assertEqual(rows["01.0684"]["assignment_count"], 19)

    def test_shared_cross_reference_does_not_merge_opposite_meanings(self):
        report = json.loads((MODULE.RESULTS / "base_meanings.json").read_text())
        rows = {r["source_code"]: r for r in report["entries"]}
        self.assertNotEqual(rows["10.0475"]["units_slp1"], rows["10.0476"]["units_slp1"])
        self.assertNotEqual(rows["10.0475"]["provisional_word_id"], rows["10.0476"]["provisional_word_id"])
        self.assertTrue(rows["10.0368"]["eligibility_note"])

    def test_only_documented_repetitions_share_identity(self):
        report = json.loads((MODULE.RESULTS / "base_meanings.json").read_text())
        rows = {r["source_code"]: r for r in report["entries"]}
        self.assertEqual(rows["01.0916"]["provisional_word_id"], rows["01.0965"]["provisional_word_id"])
        self.assertNotEqual(rows["01.1074"]["provisional_word_id"], rows["02.0051"]["provisional_word_id"])
        self.assertEqual(report["source_meaning_assignments"] - report["assignments_after_documented_merges"], 88)
        self.assertEqual(report["assignments_after_initial_merges"] - report["assignments_after_documented_merges"], 86)

    def test_changed_evidence_and_meaning_block_identity_merge(self):
        entries, _ = MODULE.load_source(MODULE.ARCHIVE / "dhatupatha.tsv")
        sources = {s["filename"]: s for s in MODULE.verify_sources()["sources"]}
        review = json.loads(MODULE.REVIEW.read_text())
        bad = copy.deepcopy(review)
        bad["identity_decisions"][0]["meaning"] = "different meaning"
        with self.assertRaises(ValueError):
            MODULE.review_index(bad, entries, sources)
        bad = copy.deepcopy(review)
        bad["decisions"][0]["anchor"] = "not found in this source"
        with self.assertRaises(ValueError):
            MODULE.review_index(bad, entries, sources)


if __name__ == "__main__":
    unittest.main()

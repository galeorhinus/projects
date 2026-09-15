import copy
import csv
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
        import review_base_identities as MODULE
        from run_pilot import verify_sources
    finally:
        sys.path.pop(0)


@unittest.skipUnless(HAS_ENGINE, "Use build/generativity-venv/bin/python")
class IdentityReviewTests(unittest.TestCase):
    def setUp(self):
        self.review = json.loads(MODULE.IDENTITY_REVIEW.read_text())
        self.report = json.loads((MODULE.RESULTS / "base_meanings.json").read_text())
        self.entries = copy.deepcopy(self.report["entries"])
        with (MODULE.RESULTS / "base_meaning_assignments.csv").open() as handle:
            self.assignments = list(csv.DictReader(handle))
        with (MODULE.RESULTS / "base_identity_review.csv").open() as handle:
            self.identities = list(csv.DictReader(handle))
        for row in self.identities:
            if row["review_id"].startswith("IR"):
                row["review_id"] = ""
        self.sources = {r["filename"]: r for r in verify_sources()["sources"]}

    def run_review(self):
        return MODULE.apply_review(self.entries, self.assignments, self.identities, self.sources, self.review)

    def test_batch_counts_and_reproducible_provenance(self):
        result = self.run_review()
        self.assertEqual((result["reviewed_groups"], result["reviewed_entries"]), (221, 483))
        self.assertEqual((result["merge_groups"], result["retained_groups"], result["open_groups"]), (79, 105, 37))
        self.assertEqual((result["before"], result["after"], result["reduction"]), (2739, 2653, 86))
        self.assertEqual(result["unreviewed_groups"], 0)
        self.assertEqual(len(self.assignments), 2741)
        self.assertEqual(len({r["count_key"] for r in self.assignments}), 2653)
        recorded = json.loads((MODULE.RESULTS / "identity_review.json").read_text())
        self.assertEqual(recorded["inputs"], self.report["inputs"])
        self.assertEqual(recorded["groups"], result["groups"])

    def test_batch_history_and_individual_reports(self):
        result = self.run_review()
        one, two, three = result["batches"][:3]
        self.assertEqual((one["before"], one["after"], one["reduction"]), (2739, 2734, 5))
        self.assertEqual((two["before"], two["after"], two["reduction"]), (2734, 2731, 3))
        self.assertEqual((two["reviewed_groups"], two["reviewed_entries"]), (10, 20))
        self.assertEqual((two["merge_groups"], two["retained_groups"], two["open_groups"]), (3, 5, 2))
        self.assertEqual((three["before"], three["after"], three["reduction"]), (2731, 2720, 11))
        self.assertEqual((three["reviewed_groups"], three["reviewed_entries"]), (30, 66))
        self.assertEqual((three["merge_groups"], three["retained_groups"], three["open_groups"]), (11, 11, 8))
        for batch in result["batches"]:
            saved = json.loads((MODULE.RESULTS / f"identity_review_batch_{batch['number']:02d}.json").read_text())
            self.assertEqual(saved["group_ids"], [row["id"] for row in saved["groups"]])
            self.assertEqual(saved["after"], batch["after"])
            self.assertEqual(saved["inputs"], self.report["inputs"])

    def test_third_batch_uses_next_thirty_groups(self):
        ordered = list(dict.fromkeys(row["group_id"] for row in self.identities if not row["review_id"]))
        selected = [row["group_id"] for row in self.review["groups"] if row.get("batch") == 3]
        self.assertEqual(selected, ordered[20:50])

    def test_remaining_batches_cover_the_queue_in_order(self):
        ordered = list(dict.fromkeys(row["group_id"] for row in self.identities if not row["review_id"]))
        self.assertEqual([row["group_id"] for row in self.review["groups"]], ordered)
        result = self.run_review()
        expected = [(2720, 2708), (2708, 2701), (2701, 2691),
                    (2691, 2678), (2678, 2663), (2663, 2653)]
        self.assertEqual([(b["before"], b["after"]) for b in result["batches"][3:]], expected)
        self.assertEqual([b["reviewed_groups"] for b in result["batches"][3:]], [30, 30, 30, 30, 30, 21])

    def test_remaining_batches_keep_unshared_meanings(self):
        self.run_review()
        keys = {(r["source_code"], r["meaning_slp1"]): r["count_key"] for r in self.assignments}
        self.assertEqual(keys["03.0004", "pAlane"], keys["09.0022", "pAlane"])
        self.assertEqual(keys["03.0004", "pUraRe"], keys["10.0022", "pUraRe"])
        self.assertNotEqual(keys["03.0004", "pAlane"], keys["03.0004", "pUraRe"])
        self.assertEqual(keys["01.0797", "puzwO"], keys["09.0065", "puzwO"])
        self.assertNotEqual(keys["01.0797", "puzwO"], keys["04.0121", "viBAge"])
        self.assertEqual(keys["04.0009", "dAhe"], keys["04.0122", "dAhe"])
        self.assertNotEqual(keys["04.0009", "dAhe"], keys["09.0064", "snehane"])

    def test_same_meaning_different_words_and_open_readings_stay_separate(self):
        self.run_review()
        keys = {(r["source_code"], r["meaning_slp1"]): r["count_key"] for r in self.assignments}
        for first, second in [("01.0470", "06.0032"), ("01.0471", "06.0033"),
                              ("01.0474", "06.0034"), ("01.0475", "06.0035")]:
            self.assertEqual(keys[first, "hiMsAyAm"], keys[second, "hiMsAyAm"])
        self.assertEqual(len({keys[c, "hiMsAyAm"] for c in ["01.0470", "01.0471", "01.0474", "01.0475"]}), 4)
        self.assertNotEqual(keys["09.0060", "uYCe"], keys["10.0270", "uYCe"])
        self.assertNotEqual(keys["04.0151", "samucCrAye"], keys["04.0152", "samucCrAye"])

    def test_followups_survive_supported_partial_merges(self):
        result = self.run_review()
        followups = [g for g in result["groups"] if g.get("remaining")]
        self.assertTrue(all(g.get("remaining") for g in result["groups"] if g["outcome"] == "open"))
        self.assertTrue(any(g["outcome"] == "merge_shared_meanings" for g in followups))
        self.assertTrue(any(g["outcome"] == "retain_distinct_meanings" for g in followups))
        self.assertIsNone(self.report["vocabulary_total"])

    def test_followup_report_has_every_recorded_remainder(self):
        result = self.run_review()
        expected = {g["id"] for g in result["groups"] if g.get("remaining")}
        saved = json.loads((MODULE.RESULTS / "identity_followups.json").read_text())
        self.assertEqual({g["id"] for g in saved["groups"]}, expected)
        self.assertEqual(saved["inputs"], self.report["inputs"])
        self.assertEqual(saved["unreviewed_groups"], 0)
        self.assertTrue((MODULE.RESULTS / "identity_passes_complete.md").exists())

    def test_third_batch_partial_merges_preserve_unresolved_and_other_meanings(self):
        self.run_review()
        keys = {(r["source_code"], r["meaning_slp1"]): r["count_key"] for r in self.assignments}
        self.assertEqual(keys["01.0841", "pUjAyAm"], keys["10.0257", "pUjAyAm"])
        self.assertNotEqual(keys["01.0841", "pUjAyAm"], keys["10.0367", "pUjAyAm"])
        self.assertEqual(keys["01.0974", "prARane"], keys["10.0123", "prARane"])
        self.assertNotEqual(keys["01.0974", "DAnyAvaroDane"], keys["10.0123", "prARane"])
        self.assertEqual(keys["09.0048", "sandarBe"], keys["10.0374", "sandarBe"])
        self.assertNotEqual(keys["09.0046", "vimocane"], keys["10.0374", "sandarBe"])

    def test_third_batch_shared_gloss_does_not_override_different_word_evidence(self):
        self.run_review()
        keys = {(r["source_code"], r["meaning_slp1"]): r["count_key"] for r in self.assignments}
        self.assertNotEqual(keys["01.0907", "dAne"], keys["10.0063", "dAne"])
        self.assertNotEqual(keys["01.0126", "BazaRe"], keys["10.0238", "BazaRe"])
        self.assertEqual(keys["01.0399", "SozaRe"], keys["10.0147", "SozaRe"])

    def test_third_batch_different_gloss_can_share_documented_meaning(self):
        self.run_review()
        rows = {(r["source_code"], r["meaning_slp1"]): r for r in self.assignments}
        a, b = rows["01.0540", "adane"], rows["05.0031", "BakzaRe"]
        self.assertEqual(a["count_key"], b["count_key"])
        self.assertNotEqual(a["meaning_id"], b["meaning_id"])
        self.assertNotEqual(a["source_gloss_slp1"], b["source_gloss_slp1"])

    def test_second_batch_partial_merge_and_unresolved_matching_gloss(self):
        self.run_review()
        rows = {(r["source_code"], r["meaning_slp1"]): r for r in self.assignments}
        self.assertEqual(rows["01.0815", "pariBAzaRe"]["count_key"], rows["06.0020", "pariBAzaRe"]["count_key"])
        self.assertNotEqual(rows["01.0815", "tarjane"]["count_key"], rows["06.0020", "Bartsane"]["count_key"])
        self.assertNotEqual(rows["01.0347", "nfttO"]["count_key"], rows["01.0890", "nfttO"]["count_key"])
        self.assertEqual(rows["04.0066", "dEnye"]["count_key"], rows["07.0012", "dEnye"]["count_key"])

    def test_second_batch_baseline_must_follow_first_batch(self):
        self.review["batches"][1]["before"] = 2733
        with self.assertRaisesRegex(ValueError, "batch baseline or membership changed"):
            self.run_review()

    def test_partial_merge_retains_additional_meaning(self):
        self.run_review()
        rows = {(r["source_code"], r["meaning_slp1"]): r for r in self.assignments}
        self.assertEqual(rows["01.1093", "sTErye"]["count_key"], rows["06.0135", "sTErye"]["count_key"])
        self.assertNotEqual(rows["06.0135", "gatO"]["count_key"], rows["06.0135", "sTErye"]["count_key"])
        identity = next(r for r in self.identities if r["source_code"] == "06.0135")
        self.assertFalse(identity["merged"])
        self.assertEqual(identity["assignment_reductions"], 1)

    def test_documented_gloss_normalization_preserves_originals(self):
        self.run_review()
        rows = {(r["source_code"], r["meaning_slp1"]): r for r in self.assignments}
        a, b = rows["01.0777", "alaNkAre"], rows["10.0255", "alaNkaraRe"]
        self.assertNotEqual(a["meaning_id"], b["meaning_id"])
        self.assertEqual(a["count_key"], b["count_key"])
        self.assertNotEqual(a["source_gloss_slp1"], b["source_gloss_slp1"])

    def test_retained_and_open_groups_are_not_merged(self):
        result = self.run_review()
        for group in result["groups"]:
            if group["outcome"] != "merge_shared_meanings":
                self.assertEqual(group["before"], group["after"])
                self.assertEqual(group["reduction"], 0)

    def test_missing_evidence_is_rejected(self):
        self.review["groups"][1]["evidence"][0]["anchor"] = "not in this source"
        with self.assertRaisesRegex(ValueError, "Identity evidence not found"):
            self.run_review()

    def test_scope_changes_and_undocumented_merges_are_rejected(self):
        self.review["groups"][0]["entries"]["01.0001"] = ["inventedMeaning"]
        with self.assertRaisesRegex(ValueError, "citation or meanings changed"):
            self.run_review()
        self.review = json.loads(MODULE.IDENTITY_REVIEW.read_text())
        self.review["groups"][1]["merges"][0]["members"].append(["06.0135", "gatO"])
        with self.assertRaisesRegex(ValueError, "Overlapping or unknown meaning merge"):
            self.run_review()

    def test_baseline_and_overlapping_merges_are_rejected(self):
        self.review["baseline_adjusted_assignments"] = 2738
        with self.assertRaisesRegex(ValueError, "baseline changed"):
            self.run_review()
        self.review = json.loads(MODULE.IDENTITY_REVIEW.read_text())
        group = self.review["groups"][1]
        group["merges"].append(copy.deepcopy(group["merges"][0]))
        with self.assertRaisesRegex(ValueError, "Overlapping or unknown meaning merge"):
            self.run_review()


if __name__ == "__main__":
    unittest.main()

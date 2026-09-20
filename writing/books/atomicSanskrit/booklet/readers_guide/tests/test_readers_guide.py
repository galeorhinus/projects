from collections import Counter
import json
from pathlib import Path
import re
import sys
import unittest
import xml.etree.ElementTree as ET

import pymupdf as fitz
import yaml

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from build_readers_guide import INVITATION, expanded_markdown, load_guide, load_pages, word_count
import build_scaffold_icons as scaffold


class GuideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (HERE / "manuscript/readers_guide.md").read_text()
        cls.cfg = yaml.safe_load((HERE / "readers_guide.yaml").read_text())
        cls.pages, cls.invitations = load_guide(cls.cfg)
        cls.exploration = (HERE / cls.cfg["exploration"]).read_text()

    def test_page_map(self):
        self.assertEqual(len(self.pages), self.cfg["expected_pages"])
        self.assertEqual(self.pages[0]["slug"], "title")
        self.assertEqual(self.pages[8]["title"], "Sanskrit's Subcontinental Home")
        self.assertEqual(self.pages[24]["slug"], "explore")
        self.assertEqual(self.pages[-1]["slug"], "terms")
        self.assertEqual(len({p["slug"] for p in self.pages}), len(self.pages))

    def test_duplicate_page_ids_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            load_pages("<!-- page: first -->\n# One\n\n<!-- page: first -->\n# Two\n")

    def test_every_approved_invitation_appears_once(self):
        used = Counter(INVITATION.findall(self.source + self.exploration))
        self.assertEqual(len(used), 101)
        self.assertEqual(set(used), set(self.invitations))
        self.assertEqual(set(used.values()), {1})
        self.assertEqual(len(INVITATION.findall(self.source)), 16)
        self.assertEqual(len(INVITATION.findall(self.exploration)), 85)
        for chapter in range(21):
            keys = [key for key in used if key.startswith(f"C{chapter:02}-")]
            self.assertEqual(len(keys), 5 if chapter == 10 else 4)
        for appendix in range(1, 11):
            self.assertIn(f"A{appendix:02}-1", used)

    def test_invitation_destinations_exist(self):
        for key, entry in self.invitations.items():
            with self.subTest(invitation=key):
                source = ROOT / entry["source"]
                self.assertTrue(source.is_file())
                headings = "\n".join(line for line in source.read_text().splitlines()
                                     if line.startswith("#"))
                for section in re.findall(r"\b\d+\.\d+\b", entry["reference"]):
                    self.assertRegex(headings, rf"(?m)^#+ {re.escape(section)}(?:\s|$)")
                for heading in re.findall("“([^”]+)”", entry["reference"]):
                    self.assertIn(heading, headings)

    def test_published_copy_has_no_internal_markers(self):
        expanded = expanded_markdown(self.source + self.exploration, self.invitations)
        self.assertNotIn("{{invite:", expanded)
        self.assertNotRegex(expanded, r"\[NOTE:|\[VERIFY:|\[TODO:")
        for term in ("ॐ", "वर्ण", "धातुः", "प्रतिमानकम्", "वैदिक", "लौकिक", "विवेक"):
            self.assertIn(term, expanded)

    def test_source_markers_do_not_count_as_words(self):
        self.assertEqual(word_count("<!-- page: title -->\n# Two words\n\nOne more."), 4)

    def test_all_argument_pages_have_pointers(self):
        for page in self.pages[1:24]:
            with self.subTest(page=page["slug"]):
                self.assertTrue(INVITATION.search(page["body"]) or
                                page["reference"] or
                                re.search(r"Chapter(?:s)? \d", page["body"]))

    def test_ten_figure_sources_exist(self):
        refs = re.findall(r"!\[\]\(([^)]+)\)", self.source)
        self.assertEqual(len(refs), 10)
        for ref in refs:
            path = HERE / "manuscript" / ref
            self.assertTrue(path.is_file())
            svg = ET.parse(path).getroot()
            self.assertTrue(svg.attrib.get("aria-label"))
            sizes = [float(e.attrib["font-size"]) for e in svg.iter() if "font-size" in e.attrib]
            self.assertGreaterEqual(min(sizes)*118/25.4*72/720, 8.5)

    def test_shared_assets_and_hex_geometry(self):
        icons, tiles = 0, 0
        for path in (HERE / "figures").glob("*.svg"):
            for element in ET.parse(path).getroot().iter():
                if "data-source" in element.attrib:
                    self.assertTrue((ROOT / element.attrib["data-source"]).is_file())
                    self.assertEqual(element.attrib["preserveAspectRatio"], "xMidYMid meet")
                    icons += 1
                kind = element.attrib.get("data-geometry", "").removeprefix("shared-scaffold-")
                if kind:
                    points = [tuple(map(float, pair.split(","))) for pair in element.attrib["points"].split()]
                    expected = [tuple(map(float, pair.split(","))) for pair in
                                scaffold.hex_points(0, 0, scaffold.WIDTH_BY_CLASS[kind]).split()]
                    def ratio(points):
                        xs, ys = zip(*points)
                        return (max(xs)-min(xs))/(max(ys)-min(ys))
                    self.assertAlmostEqual(ratio(points), ratio(expected), delta=.001)
                    tiles += 1
        self.assertGreaterEqual(icons, 7)
        self.assertEqual(tiles, 28)

    def test_generativity_totals_match_manuscript(self):
        chapter = (ROOT / "manuscript/as_1_12_building_vakya.md").read_text()
        atoms = (ROOT / "manuscript/as_1_10_building_dhatuh.md").read_text()
        for number in ("2,168", "2,634", "12,846,458"):
            self.assertIn(number, self.source)
            self.assertIn(number, chapter + atoms)

    def test_outputs(self):
        out = (HERE / self.cfg["output_dir"]).resolve()
        n = self.cfg["expected_pages"]
        for suffix, total in (("a5.pdf", n), ("a5.print.pdf", n), ("cover.pdf", 4), ("a5.complete.pdf", n+4)):
            with self.subTest(file=suffix), fitz.open(out / f"atomic_sanskrit_readers_guide.{suffix}") as doc:
                self.assertEqual(len(doc), total)
                self.assertTrue(doc.metadata["title"])
                for page in doc:
                    self.assertAlmostEqual(page.rect.width, 148/25.4*72, delta=.1)
                    self.assertAlmostEqual(page.rect.height, 210/25.4*72, delta=.1)
                    self.assertNotRegex(page.get_text().lower(), r"\b(?:claude|codex|placeholder|tbd)\b")
                    self.assertNotIn("{{invite:", page.get_text())

    def test_bookmarks_match_pages(self):
        out = (HERE / self.cfg["output_dir"]).resolve()
        with fitz.open(out / "atomic_sanskrit_readers_guide.a5.pdf") as interior:
            toc = interior.get_toc()
            self.assertEqual([entry[2] for entry in toc], list(range(2, len(self.pages)+1)))
        with fitz.open(out / "atomic_sanskrit_readers_guide.a5.complete.pdf") as complete:
            self.assertEqual(complete.get_toc()[-2][2], len(self.pages)+3)
            self.assertEqual(complete.get_toc()[-1][2], len(self.pages)+4)

    def test_qa_report_matches_sources(self):
        report = json.loads((HERE / "build/qa_report.json").read_text())
        self.assertEqual(report["interior_pages"], len(self.pages))
        self.assertEqual(report["invitation_count"], 101)
        placements = {key: p["slug"] for p in self.pages for key in INVITATION.findall(p["body"])}
        self.assertEqual(report["invitation_placements"], placements)
        self.assertEqual(set(report["checks"].values()), {0})

    def test_outlined_figures(self):
        for svg in (HERE / "figures").glob("*.svg"):
            with self.subTest(figure=svg.name), fitz.open(HERE / "build" / (svg.stem+".pdf")) as doc:
                self.assertEqual(doc[0].get_text().strip(), "")
                self.assertTrue(doc[0].get_drawings())


if __name__ == "__main__":
    unittest.main()

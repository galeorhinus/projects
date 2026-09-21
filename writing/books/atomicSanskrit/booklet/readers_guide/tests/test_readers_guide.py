from collections import Counter
import json
import os
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
from build_readers_guide import (INVITATION, expanded_markdown, figure_metrics, layout_config,
                                load_guide, load_pages, preamble, title_page, word_count)
import build_scaffold_icons as scaffold
from make_figures import canonical_figures


class GuideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (HERE / "manuscript/readers_guide.md").read_text()
        cls.cfg = yaml.safe_load((HERE / "readers_guide.yaml").read_text())
        cls.pages, cls.invitations = load_guide(cls.cfg)
        cls.exploration = (HERE / cls.cfg["exploration"]).read_text()
        layout = os.environ.get("GUIDE_TEST_LAYOUT", "all")
        if layout not in ("all", *cls.cfg["layouts"]):
            raise ValueError(f"Unknown test layout: {layout}")
        cls.output_layouts = {key: settings for key, settings in cls.cfg["layouts"].items()
                              if layout in ("all", key)}

    def test_page_map(self):
        self.assertEqual(len(self.pages), self.cfg["expected_sections"])
        self.assertEqual(self.pages[0]["slug"], "title")
        by_slug = {p["slug"]: p for p in self.pages}
        self.assertEqual(by_slug["home-sound"]["title"], "Sanskrit's Subcontinental Home")
        slugs = [p["slug"] for p in self.pages]
        self.assertEqual(slugs.index("explore"), 27)
        self.assertLess(slugs.index("challenge"), slugs.index("mouth"))
        self.assertEqual(slugs.index("panini") + 1, slugs.index("domains"))
        self.assertEqual(slugs[slugs.index("progress"):slugs.index("pie")], ["progress", "custody"])
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

    def test_specialized_iast_has_devanagari(self):
        expanded = expanded_markdown(self.source + self.exploration, self.invitations)
        pairs = re.compile(r"\(\*([^*()]+)\*\)")
        diacritics = r"[āīūṛṝḷḹṅñṭḍṇśṣṃṁḥĀĪŪṚṜḶḸṄÑṬḌṆŚṢṂḤ]"
        for match in pairs.finditer(expanded):
            if re.search(diacritics, match[1]):
                preceding = expanded[:match.start()].rstrip(" *⟫")
                self.assertRegex(preceding[-1:], r"[\u0900-\u097f]")
        self.assertNotRegex(pairs.sub("", expanded), diacritics)
        self.assertIn("माण्डूक्य उपनिषद् (*Māṇḍūkya Upaniṣad*)", expanded)

    def test_guide_subtitle_adds_devanagari_without_changing_metadata(self):
        book = yaml.safe_load((ROOT / "as_book.yaml").read_text())
        original = book["subtitle"]
        for layout in ("a5", "a4"):
            tex = title_page(book, layout_config(self.cfg, layout))
            self.assertIn("सनातन", tex)
            self.assertIn("Sanātan", tex)
        self.assertEqual(book["subtitle"], original)

    def test_source_markers_do_not_count_as_words(self):
        self.assertEqual(word_count("<!-- page: title -->\n# Two words\n\nOne more."), 4)

    def test_all_argument_pages_have_pointers(self):
        for page in (p for p in self.pages if p["part"] == "argument" and p["slug"] != "title"):
            with self.subTest(page=page["slug"]):
                self.assertTrue(INVITATION.search(page["body"]) or
                                page["reference"] or
                                re.search(r"Chapter(?:s)? \d", page["body"]))

    def test_numbered_chapter_titles_match_manuscript(self):
        for number, title in re.findall(r"^## Chapter (\d+): (.+)$", self.exploration, re.M):
            source, = (ROOT / "manuscript").glob(f"as_1_{int(number):02}_*.md")
            self.assertIn(f"# Chapter {number} — {title}", source.read_text())
        for number, title in re.findall(r"^## Appendix Part (\d+): (.+)$", self.exploration, re.M):
            source, = (ROOT / "manuscript").glob(f"as_3_{int(number):02}_*.md")
            self.assertIn(f"# Appendix Part {number} — {title}", source.read_text())
        epilogue = re.search(r"^## Epilogue: (.+)$", self.exploration, re.M)[1]
        self.assertIn(f"# Epilogue — {epilogue}", (ROOT / "manuscript/as_2_01_epilogue.md").read_text())

    def test_content_revision_keeps_named_arguments(self):
        by_slug = {p["slug"]: p["body"] for p in self.pages}
        for slug, terms in {
            "challenge": ["does not pretend neutrality", "engineered within the Indian subcontinent"],
            "progress": ["fourth Abrahamic religion", "church of progress"],
            "custody": ["Boden", "1948", "Deccan College", "Sātavaḷekar"],
            "pie": ["philological fraud", "replacement civilizational memory"],
            "panini": ["heroic erasure", "decoder"],
            "return": ["containment", "second domain"],
        }.items():
            for term in terms:
                self.assertIn(term, by_slug[slug])

    def test_voice_names_actors_and_enforcement(self):
        expanded = expanded_markdown(self.source + self.exploration, self.invitations)
        for softened in ("The familiar account", "The familiar linguistic account",
                         "Formal Arabic illustrates another arrangement",
                         "The rival account places"):
            self.assertNotIn(softened, expanded)
        by_slug = {p["slug"]: p["body"] for p in self.pages}
        for term in ("The pyramid credits", "Caliph Uthman", "burned",
                     "Al-Azhar", "prison sentences and fines", "Teaching and memorization"):
            self.assertIn(term, by_slug["panini"])
        self.assertIn("Western philologists", by_slug["challenge"])
        self.assertIn("Western philologists recast", by_slug["domains"])
        self.assertIn("Dictionary editors", by_slug["categories"])

    def test_ten_figure_sources_exist(self):
        refs = re.findall(r"!\[\]\(([^)]+)\)", self.source)
        self.assertEqual(len(refs), 10)
        for ref in refs:
            path = HERE / "manuscript" / ref
            self.assertTrue(path.is_file())
            svg = ET.parse(path).getroot()
            self.assertTrue(svg.attrib.get("aria-label"))
            sizes = [float(e.attrib["font-size"]) for e in svg.iter() if "font-size" in e.attrib]
            width = float(svg.attrib["viewBox"].split()[2])
            self.assertGreaterEqual(min(sizes)*116/25.4*72/width, 8.5)

    def test_inside_out_uses_sonomer(self):
        svg = ET.parse(HERE / "figures/inside_out.svg").getroot()
        labels = [e.text for e in svg.iter("{http://www.w3.org/2000/svg}text")]
        self.assertEqual(labels[:12], ["वर्ण", "Sonomer", "varṇa", "धातुः", "Atom", "dhātuḥ",
                                      "पदम्", "Word", "padam", "वाक्यम्", "Sentence", "vākyam"])
        self.assertIn("sonomer", svg.attrib["aria-label"])
        route = next(page for page in self.pages if page["slug"] == "route")
        self.assertIn("**sonomer** for वर्ण (*varṇa*)", route["body"].split("![]")[0])
        self.assertIn("**Sonomer, वर्ण (*varṇa*):**", self.source)

    def test_imported_figure_is_not_exported_as_a_second_figure(self):
        names = {path.name for path in canonical_figures()}
        self.assertEqual(len(names), 10)
        self.assertIn("inside_out.svg", names)
        self.assertNotIn("two_chains_hex_nodes.from-cd.svg", names)
        svg = ET.parse(HERE / "figures/inside_out.svg").getroot()
        self.assertEqual(len(list(svg.iter("{http://www.w3.org/2000/svg}style"))), 0)

    def test_two_orders_uses_authority_and_architecture_icons(self):
        svg = ET.parse(HERE / "figures/two_orders.svg").getroot()
        sources = [e.attrib["data-source"] for e in svg.iter() if "data-source" in e.attrib]
        self.assertEqual(sources, ["figures/_shared/icons/ic-authority.svg",
                                   "figures/_shared/icons/ic-architecture.svg"])

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
        for layout, settings in self.output_layouts.items():
            report = json.loads((HERE / "build" / layout / "qa_report.json").read_text())
            n = report["interior_pages"]
            if settings["expected_pages"] is not None:
                self.assertEqual(n, settings["expected_pages"])
            for suffix, total in (("pdf", n), ("print.pdf", n), ("cover.pdf", 4), ("complete.pdf", n+4)):
                with self.subTest(layout=layout, file=suffix), fitz.open(out / f"atomic_sanskrit_readers_guide.{layout}.{suffix}") as doc:
                    self.assertEqual(len(doc), total)
                    self.assertTrue(doc.metadata["title"])
                    for page in doc:
                        self.assertAlmostEqual(page.rect.width, settings["trim_mm"][0]/25.4*72, delta=.1)
                        self.assertAlmostEqual(page.rect.height, settings["trim_mm"][1]/25.4*72, delta=.1)
                        self.assertNotRegex(page.get_text().lower(), r"\b(?:claude|codex|placeholder|tbd)\b")
                        self.assertNotIn("{{invite:", page.get_text())

    def test_title_page_subtitle_hierarchy(self):
        out = (HERE / self.cfg["output_dir"]).resolve()
        for layout, settings in self.output_layouts.items():
            for suffix in ("pdf", "cover.pdf"):
                with self.subTest(layout=layout, file=suffix), fitz.open(
                        out / f"atomic_sanskrit_readers_guide.{layout}.{suffix}") as doc:
                    page = doc[0]
                    text = page.get_text()
                    self.assertLess(text.index("Radiant"), text.index("Reader"))
                    self.assertIn("Parag Tope", text)
                    self.assertIn("Revised review draft", text)
                    spans = [span for block in page.get_text("dict")["blocks"]
                             for line in block.get("lines", []) for span in line["spans"]]
                    subtitle = next(s for s in spans if "Radiant" in s["text"])
                    label = next(s for s in spans if "Reader" in s["text"])
                    self.assertAlmostEqual(subtitle["size"], settings["subtitle_font_size"] * 72 / 72.27, delta=.02)
                    self.assertGreater(subtitle["size"], label["size"])

    def test_bookmarks_match_pages(self):
        out = (HERE / self.cfg["output_dir"]).resolve()
        for layout, settings in self.output_layouts.items():
            with self.subTest(layout=layout), fitz.open(out / f"atomic_sanskrit_readers_guide.{layout}.pdf") as interior:
                toc = interior.get_toc()
                self.assertEqual(len(toc), len(self.pages)-1 + sum(map(len, settings["splits"].values())))
                self.assertEqual([entry[2] for entry in toc], sorted(entry[2] for entry in toc))
                self.assertTrue(all(2 <= entry[2] <= len(interior) for entry in toc))
                with fitz.open(out / f"atomic_sanskrit_readers_guide.{layout}.complete.pdf") as complete:
                    self.assertEqual(complete.get_toc()[-2][2], len(interior)+3)
                    self.assertEqual(complete.get_toc()[-1][2], len(interior)+4)
                    self.assertEqual(complete.get_toc()[2:-2], [[n, t, p+2] for n, t, p in toc])

    def test_qa_report_matches_sources(self):
        placements = {key: p["slug"] for p in self.pages for key in INVITATION.findall(p["body"])}
        source = "\n\n".join("# " + p["title"] + "\n\n" + expanded_markdown(p["body"], self.invitations) for p in self.pages)
        for layout in self.output_layouts:
            report = json.loads((HERE / "build" / layout / "qa_report.json").read_text())
            with self.subTest(layout=layout):
                self.assertEqual(report["source_sections"], len(self.pages))
                self.assertEqual(report["invitation_count"], 101)
                self.assertEqual(report["invitation_placements"], placements)
                self.assertEqual(report["source_word_count"], word_count(source))
                self.assertEqual(set(report["checks"].values()), {0})
                self.assertEqual(report["body_font_pt"], self.cfg["layouts"][layout]["body_font_size"])

    def test_layout_fonts_and_binding_margins(self):
        book = yaml.safe_load((ROOT / "as_book.yaml").read_text())
        for layout, size in (("a5", 11), ("a4", 12)):
            cfg = layout_config(self.cfg, layout)
            with self.subTest(layout=layout):
                self.assertEqual(cfg["body_font_size"], size)
                self.assertGreaterEqual(cfg["margins_mm"]["inner"], 20)
                tex = preamble(book, cfg)
                self.assertIn("twoside", tex)
                self.assertIn(f"\\fontsize{{{size}}}{{{cfg['line_spacing_pt']}}}", tex)
                self.assertTrue(all(row["minimum_font_pt"] >= 8.5 for row in figure_metrics(cfg["text_width_mm"])))

    def test_layout_breaks_reference_source(self):
        by_slug = {p["slug"]: p for p in self.pages}
        for settings in self.cfg["layouts"].values():
            self.assertTrue(set(settings["join_before"]) <= set(by_slug))
            for slug, splits in settings["splits"].items():
                self.assertIn(slug, by_slug)
                self.assertEqual(splits, sorted(set(splits)))
                self.assertTrue(all(0 < i < len(by_slug[slug]["body"].split("\n\n")) for i in splits))

    def test_duplex_padding_and_print_copies(self):
        out = (HERE / self.cfg["output_dir"]).resolve()
        for layout in self.output_layouts:
            base = out / f"atomic_sanskrit_readers_guide.{layout}.pdf"
            with self.subTest(layout=layout), fitz.open(base) as doc:
                self.assertEqual(len(doc) % 2, 0)
                blank = [p.number + 1 for p in doc if not p.get_text().strip()]
                self.assertIn(blank, ([], [len(doc)]))
                self.assertEqual(base.read_bytes(), (out / f"atomic_sanskrit_readers_guide.{layout}.print.pdf").read_bytes())

    def test_no_unplanned_continuation_pages(self):
        out = (HERE / self.cfg["output_dir"]).resolve()
        for layout in self.output_layouts:
            with self.subTest(layout=layout), fitz.open(out / f"atomic_sanskrit_readers_guide.{layout}.pdf") as doc:
                titled_pages = {page for _, _, page in doc.get_toc()}
                for page in doc:
                    if page.number and page.get_text().strip():
                        self.assertIn(page.number + 1, titled_pages)

    def test_rendered_fonts_and_binding_clearance(self):
        out = (HERE / self.cfg["output_dir"]).resolve()
        for layout, settings in self.output_layouts.items():
            with self.subTest(layout=layout), fitz.open(out / f"atomic_sanskrit_readers_guide.{layout}.pdf") as doc:
                body_spans = 0
                expected_size = settings["body_font_size"] * 72 / 72.27
                for page in doc:
                    for block in page.get_text("dict")["blocks"]:
                        for line in block.get("lines", []):
                            for span in line["spans"]:
                                if not span["text"].strip():
                                    continue
                                if span["font"] == "STIXTwoText-Regular" and abs(span["size"] - expected_size) < .02:
                                    body_spans += 1
                                clearance = (span["bbox"][0] if page.number % 2 == 0 else
                                             page.rect.width - span["bbox"][2]) * 25.4 / 72
                                # Allow optical margin protrusion, not misplaced text frames.
                                self.assertGreaterEqual(clearance, settings["margins_mm"]["inner"] - .75)
                self.assertGreater(body_spans, 100)

    def test_outlined_figures(self):
        for svg in canonical_figures():
            with self.subTest(figure=svg.name), fitz.open(HERE / "build" / (svg.stem+".pdf")) as doc:
                self.assertEqual(doc[0].get_text().strip(), "")
                self.assertTrue(doc[0].get_drawings())


if __name__ == "__main__":
    unittest.main()

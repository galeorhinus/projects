"""Small, print-sized diagrams for the reader's guide, not book replacements."""

from copy import deepcopy
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

DIR = Path(__file__).resolve().parent / "figures"
ROOT = DIR.parents[2]
SHARED = ROOT / "figures/_shared"
sys.path.insert(0, str(SHARED))
sys.path.insert(0, str(SHARED / "icons"))
import matra_style as style
import build_scaffold_icons as scaffold
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
INK, TEAL, GOLD, RED = style.TEXT, "#24665e", style.GOLD, "#94483f"
PALE, LINE = "#f3efe6", style.GUIDE


class Figure:
    def __init__(self, height, title):
        self.root = ET.Element(f"{{{NS}}}svg", {
            "viewBox": f"0 0 720 {height}", "width": "720", "height": str(height),
            "role": "img", "aria-label": title,
        })
        ET.SubElement(self.root, f"{{{NS}}}title").text = title
        self.rect(0, 0, 720, height, "white")

    def add(self, tag, **attrs):
        return ET.SubElement(self.root, f"{{{NS}}}{tag}", {
            key.replace("_", "-"): str(value) for key, value in attrs.items()
        })

    def rect(self, x, y, w, h, fill=PALE, stroke="none"):
        self.add("rect", x=x, y=y, width=w, height=h, fill=fill, stroke=stroke)

    def text(self, x, y, value, size=24, color=INK, anchor="start", dev=False, bold=False):
        self.add("text", x=x, y=y, fill=color, font_size=size,
                 text_anchor=anchor, font_family="Tiro Devanagari Sanskrit" if dev else "STIX Two Text",
                 font_weight="bold" if bold else "normal").text = value

    def line(self, x1, y1, x2, y2, color=LINE, width=2):
        self.add("line", x1=x1, y1=y1, x2=x2, y2=y2, stroke=color, stroke_width=width)

    def arrow(self, x1, y1, x2, y2, color=TEAL):
        from math import atan2, cos, sin
        angle = atan2(y2-y1, x2-x1)
        self.line(x1, y1, x2, y2, color, 3)
        points = [(x2, y2)] + [(x2-11*cos(angle+d), y2-11*sin(angle+d)) for d in (-.48, .48)]
        self.add("polygon", points=" ".join(f"{x},{y}" for x, y in points), fill=color)

    def save(self, name):
        DIR.mkdir(parents=True, exist_ok=True)
        ET.indent(self.root)
        ET.ElementTree(self.root).write(DIR / f"{name}.svg", encoding="utf-8", xml_declaration=True)

    def icon(self, name, x, y, width, height=None, color=GOLD):
        node = deepcopy(ET.parse(SHARED / "icons" / f"{name}.svg").getroot())
        node.attrib.update(x=str(x), y=str(y), width=str(width), height=str(height or width),
                           style=f"color:{color}", preserveAspectRatio="xMidYMid meet")
        node.set("data-source", f"figures/_shared/icons/{name}.svg")
        self.root.append(node)

    def hex(self, cx, cy, kind="V1", scale=4, fill=style.LIGHT_FILL):
        points = scaffold.hex_points(0, 0, scaffold.WIDTH_BY_CLASS[kind])
        pts = []
        for pair in points.split():
            x, y = map(float, pair.split(","))
            pts.append(f"{cx+x*scale:.2f},{cy+y*scale:.2f}")
        self.add("polygon", points=" ".join(pts), fill=fill, stroke=style.STROKE,
                 stroke_width=1.7, data_geometry=f"shared-scaffold-{kind}")


def canonical_figures():
    return sorted(path for path in DIR.glob("*.svg") if ".from-" not in path.name)


def promote_inside_out():
    root = ET.parse(DIR / "two_chains_hex_nodes.from-cd.svg").getroot()
    title = "Inside-out construction: sonomer to language, memory to shared order"
    root.set("role", "img")
    root.set("aria-label", title)
    for node in list(root):
        if node.tag in (f"{{{NS}}}style", f"{{{NS}}}title"):
            root.remove(node)
    heading = ET.Element(f"{{{NS}}}title")
    heading.text = title
    root.insert(0, heading)
    # Use installed print fonts; the supplied design's web-font import cannot
    # be relied on by Inkscape. Keep its geometry and original source intact.
    for node in root.iter(f"{{{NS}}}text"):
        dev = any("\u0900" <= char <= "\u097f" for char in (node.text or ""))
        node.set("font-family", "Tiro Devanagari Sanskrit" if dev else "STIX Two Text")
        if node.get("font-weight") == "600":
            node.set("font-weight", "700")
        if node.get("font-style") == "italic":
            node.set("font-size", "30")
            node.set("fill", "#756344")
    ET.indent(root)
    ET.ElementTree(root).write(DIR / "inside_out.svg", encoding="utf-8", xml_declaration=True)


def make_all():
    promote_inside_out()

    f = Figure(260, "Authority and inside-out architecture: command and shared calibration")
    f.text(174, 28, "Command from above", 26, RED, "middle", bold=True)
    f.text(544, 28, "Order from within", 26, TEAL, "middle", bold=True)
    f.icon("ic-authority", 94, 42, 160, 145, RED)
    f.icon("ic-architecture", 464, 42, 160, 145, GOLD)
    f.line(355, 46, 355, 234)
    f.text(174, 208, "An apex directs people", 23, INK, "middle")
    f.text(544, 208, "People use a shared standard", 23, INK, "middle")
    f.text(544, 241, "प्रतिमानकम्", 27, TEAL, "middle", dev=True)
    f.text(174, 241, "Authority", 23, RED, "middle")
    f.save("two_orders")

    f = Figure(210, "Oṃ: open sound, changing mouth shape, closing lips and nasal resonance")
    f.icon("ic-om", 4, 28, 136, color=GOLD)
    for x, dev, roman, label in ((245, "अ", "a", "Open tone"), (431, "उ", "u", "Rounded lips"),
                                (618, "म्", "m", "Closing hum")):
        f.text(x, 64, dev, 48, INK, "middle", dev=True)
        f.text(x, 97, roman, 24, TEAL, "middle")
        f.text(x, 138, label, 24, INK, "middle")
    f.arrow(302, 76, 373, 76, GOLD)
    f.arrow(490, 76, 560, 76, GOLD)
    f.text(360, 198, "One utterance brings the speaking body into use", 23, TEAL, "middle")
    f.save("om_body")

    f = Figure(440, "Five mouth-places; repeated effort; equal one-mātrā-shaped grid cells")
    f.text(6, 36, "स्थान", 28, INK, dev=True)
    f.text(6, 66, "Mouth-place", 21, TEAL)
    heads = (("अल्पप्राण", "अघोष", "light", "unvoiced"), ("महाप्राण", "अघोष", "heavy", "unvoiced"),
             ("अल्पप्राण", "घोष", "light", "voiced"), ("महाप्राण", "घोष", "heavy", "voiced"),
             ("अनुनासिक", "", "through", "the nose"))
    for i, (a, b, c, d) in enumerate(heads):
        x = 239+101*i
        f.text(x, 24, a, 21, INK, "middle", dev=True)
        f.text(x, 47, b, 21, INK, "middle", dev=True)
        f.text(x, 70, c, 20, TEAL, "middle")
        f.text(x, 93, d, 20, TEAL, "middle")
    places = (("कण्ठ्य", "Back of mouth"), ("तालव्य", "Palate"), ("मूर्धन्य", "Curled tongue"),
              ("दन्त्य", "Teeth"), ("ओष्ठ्य", "Lips"))
    for row, ((dev, eng), letters) in enumerate(zip(places,
            ("क ख ग घ ङ", "च छ ज झ ञ", "ट ठ ड ढ ण", "त थ द ध न", "प फ ब भ म"))):
        y = 135+59*row
        f.text(6, y, dev, 27, INK, dev=True)
        f.text(6, y+24, eng, 21, TEAL)
        for col, char in enumerate(letters.split()):
            x = 239+101*col
            heavy = col in (1, 3)
            f.hex(x, y+3, scale=3.75, fill=style.DARK_FILL if heavy else style.LIGHT_FILL)
            f.text(x, y+15, char, 37, style.INK_LIGHT if heavy else INK, "middle", dev=True)
    f.text(6, 432, "Darker cells: the ten heavy-breath stops", 22, TEAL)
    f.save("sound_grid")

    f = Figure(295, "Coverage of 23 Sanskrit base consonantal positions in Chapter 8")
    data = (("Tamil · Toda · Kurukh", 22, TEAL), ("Korku · Mundari · Ho", 20, TEAL),
            ("English · French · Greek", 16, RED), ("Tajik · Kazakh · Kyrgyz", 15, RED))
    for row, (label, value, color) in enumerate(data):
        y = 26 + row*67
        f.text(8, y, label, 25)
        f.rect(8, y+10, 626, 15, PALE)
        f.rect(8, y+10, 626*value/23, 15, color)
        f.text(711, y+24, f"{value}/23", 25, color, "end", bold=True)
    f.text(8, 289, "Combined sets; ten heavy-breath stops excluded", 21, TEAL)
    f.save("home_coverage")

    f = Figure(244, "G plus a plus m: measured consonants and vowel on the book's two rails")
    positions, units, bounds = scaffold.layout(["C", "V1", "C"])
    scale = 7
    mid = (bounds[0]+bounds[2])/2
    for (x, y), unit, dev, roman in zip(positions, units, ("ग्", "अ", "म्"), ("g", "a", "m")):
        cx, cy = 360+(x-mid)*scale, 83+y*scale
        kind = unit["class"]
        ink = style.INK_LIGHT if kind == "C" else INK
        f.hex(cx, cy, kind, scale, style.DARK_FILL if kind == "C" else style.LIGHT_FILL)
        f.text(cx, cy+6, dev, 44, ink, "middle", dev=True)
        f.text(cx, cy+34, roman, 24, ink, "middle")
        f.text(cx, 185, "½" if kind == "C" else "1", 26, INK, "middle")
    f.text(310, 230, "मात्रा", 27, TEAL, "middle", dev=True)
    f.text(360, 230, "mātrā / duration", 22, TEAL)
    f.save("atom_assembly")

    f = Figure(230, "Selected words in the family of the atom kṛ, to do or make")
    f.text(360, 35, "कृ", 39, INK, "middle", dev=True)
    f.text(360, 63, "kṛ / to do or make", 23, TEAL, "middle")
    f.line(360, 74, 360, 88, GOLD)
    f.line(112, 88, 608, 88, GOLD)
    for x, word, roman, meaning in ((112, "कर्म", "karma", "action / deed"),
                                   (360, "कर्तृ", "kartṛ", "doer"),
                                   (608, "कार्य", "kārya", "what is to be done")):
        f.line(x, 88, x, 104, GOLD)
        f.text(x, 140, word, 37, INK, "middle", dev=True)
        f.text(x, 170, roman, 22, TEAL, "middle")
        f.text(x, 205, meaning, 23, INK, "middle")
    f.save("word_family")

    f = Figure(245, "One Sanskrit architecture: exact Vedic transmission and new expression")
    f.text(360, 29, "ONE SANSKRIT ARCHITECTURE", 24, TEAL, "middle", bold=True)
    f.line(12, 48, 708, 48, GOLD, 3)
    for x, dev, roman, action, verbs in ((174, "वैदिक", "vaidika", "Keep the examples exact", "Recite · compare · correct"),
                                        (546, "लौकिक", "laukika", "Make new expressions", "Explain · compose · name")):
        f.text(x, 91, dev, 34, INK, "middle", dev=True)
        f.text(x, 120, roman, 22, TEAL, "middle")
        f.text(x, 154, action, 24, INK, "middle")
        f.text(x, 189, verbs, 22, TEAL, "middle")
    f.arrow(323, 99, 395, 99, GOLD)
    f.text(360, 236, "A fixed reference supports continued creation", 22, TEAL, "middle")
    f.save("two_domains")

    f = Figure(280, "Teacher, student and other listeners check the same Vedic passage")
    for x, dev, label, icon in ((110, "गुरु", "Teacher", "ic-mouth"), (360, "शिष्य", "Student", "ic-memory"),
                               (610, "श्रोतारः", "Other listeners", "ic-ear")):
        f.icon(icon, x-28, 0, 56, color=GOLD)
        f.text(x, 86, dev, 29, INK, "middle", dev=True)
        f.text(x, 113, label, 23, TEAL, "middle")
        f.line(x, 123, x, 143, GOLD)
    f.line(110, 143, 610, 143, GOLD)
    f.line(360, 143, 360, 163, GOLD)
    f.rect(45, 165, 630, 47, PALE)
    f.text(360, 197, "The same passage, known by many", 26, INK, "middle")
    for x, label in ((115, "Word sequence"), (360, "Timing and pitch"), (605, "Recitation patterns")):
        f.text(x, 260, label, 22, TEAL, "middle")
    f.save("distributed_checks")

    f = Figure(240, "Sanskrit's connected architecture and the words and methods carried outward")
    f.icon("ic-sanskrit-sun", 5, 1, 88)
    f.text(110, 37, "संस्कृतम्", 34, INK, dev=True)
    f.text(110, 70, "Connected architecture", 23, TEAL)
    for i, label in enumerate(("Sound and word formation", "Grammatical analysis", "Vedic transmission")):
        f.text(10, 125+42*i, label, 23)
    for y, label in ((60, "Words"), (130, "Sound patterns"), (200, "Methods of analysis")):
        f.arrow(344, y-8, 431, y-8, GOLD)
        f.text(451, y, label, 25)
    f.save("radiance")


if __name__ == "__main__":
    make_all()

"""Generate front-cover studies without changing the canonical A5 wrap."""

from copy import deepcopy
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "as-book-a5.svg"
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
INKSCAPE = shutil.which("inkscape") or "/Applications/Inkscape.app/Contents/MacOS/inkscape"

VARIANTS = [
    # label, name, subtitle size, weight, style, rule width, tagline lines
    ("A", "balanced", 29, "400", "normal", 414,
     [("Distributed · Radiant · Calibrant · Fractal", 470, 20)]),
    ("B", "bold-subtitle", 28, "700", "normal", 414,
     [("Distributed · Radiant · Calibrant · Fractal", 470, 20)]),
    ("C", "italic-subtitle", 31, "400", "italic", 300,
     [("Distributed · Radiant · Calibrant · Fractal", 470, 20)]),
    ("D", "two-line-tagline", 29, "400", "normal", 414,
     [("Distributed · Radiant", 468, 24),
      ("Calibrant · Fractal", 498, 24)]),
]


def text_node(identifier, content, y, size, weight="400", style="normal"):
    node = ET.Element(f"{{{SVG}}}text", {
        "id": identifier, "x": "827.75", "y": str(y),
        "text-anchor": "middle", "font-family": "Charter",
        "font-size": str(size), "font-weight": weight,
        "font-style": style, "fill": "#4A3F30",
    })
    node.text = content
    return node


def main():
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    original = ET.parse(SOURCE, parser=parser)
    previews = []
    for label, name, size, weight, style, rule_width, tagline in VARIANTS:
        tree = deepcopy(original)
        root = tree.getroot()
        root.set("id", f"as-book-a5-variant-{label.lower()}")
        group = root.find(".//*[@id='text_and_icons_2_']")
        assert group is not None
        removed = []
        for node in list(group):
            if node.tag == f"{{{SVG}}}line" or node.text in (
                "The Architecture of Sanātan",
                "Distributed. Radiant. Calibrant. Fractal",
            ):
                removed.append(node)
                group.remove(node)
        assert len(removed) == 3, "Canonical cover layout has changed; inspect it first."
        group.append(text_node("variant-subtitle", "The Architecture of Sanātan",
                               409, size, weight, style))
        group.append(ET.Element(f"{{{SVG}}}line", {
            "id": "variant-rule", "x1": str(827.75 - rule_width / 2),
            "x2": str(827.75 + rule_width / 2), "y1": "435", "y2": "435",
            "stroke": "#8A7C64", "stroke-width": "1.3",
        }))
        for index, (words, y, font_size) in enumerate(tagline):
            group.append(text_node(f"variant-tagline-{index}", words, y, font_size))

        # Everything outside the three replaced front-cover elements stays intact.
        for identifier in ("back", "spine_2_", "icons_2_", "as-reference-a4"):
            assert ET.tostring(root.find(f".//*[@id='{identifier}']")) == ET.tostring(
                original.getroot().find(f".//*[@id='{identifier}']"))
        assert root.get("viewBox") == original.getroot().get("viewBox")
        stem = HERE / f"as-book-a5-{label.lower()}-{name}"
        tree.write(stem.with_suffix(".svg"), encoding="utf-8", xml_declaration=True)
        preview = stem.with_suffix(".png")
        subprocess.run([INKSCAPE, str(stem.with_suffix(".svg")),
                        "--export-id=front", "--export-id-only", "--export-width=1000",
                        f"--export-filename={preview}"], check=True)
        previews.append((label, name, preview))

    command = ["magick", "montage"]
    for label, name, preview in previews:
        command += ["-label", f"{label}  {name.replace('-', ' ').title()}", str(preview)]
    command += ["-font", "Helvetica", "-pointsize", "22", "-fill", "#242424",
                "-background", "#E7E7E7", "-geometry", "520x738+16+16", "-tile", "2x2",
                str(HERE / "a5-cover-comparison.png")]
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()

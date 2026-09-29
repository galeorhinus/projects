"""Build the A5 cover with the final four labelled architecture icons."""

from copy import deepcopy
import csv
import io
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
COVERS = HERE.parents[1]
ROOT = COVERS.parents[1]
SOURCE = HERE.parent / "a5-subtitle-20260927/as-book-a5-b-bold-subtitle.svg"
DESTINATION = COVERS / "as-book-a5-four-icons.svg"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
INKSCAPE = shutil.which("inkscape") or "/Applications/Inkscape.app/Contents/MacOS/inkscape"
FRONT_SCALE_X = 0.8409051
FRONT_SCALE_Y = 0.8399543
ICON_WIDTH_MM = 13
LABEL_PT = 12.5


def main():
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    original = ET.parse(SOURCE, parser=parser)
    tree = deepcopy(original)
    root = tree.getroot()
    root.set("id", "as-book-a5-four-icons")
    front = root.find(".//*[@id='front']")
    subtitle = front.find(".//*[@id='variant-subtitle']")
    subtitle.text = subtitle.text.upper()
    subtitle.set("font-size", "24")
    text_group = front.find(".//*[@id='text_and_icons_2_']")
    tagline = text_group.find(".//*[@id='variant-tagline-0']")
    assert tagline is not None
    text_group.remove(tagline)
    icons = front.find(".//*[@id='icons_2_']")
    standalone = icons.find(".//*[@id='calibrant_1_']")
    assert standalone is not None
    icons.remove(standalone)

    band = ET.SubElement(front, f"{{{NS}}}g", {"id": "architecture-icons"})
    icon_scale = ICON_WIDTH_MM * 72 / 25.4 / FRONT_SCALE_X / 80
    for index, name in enumerate(("Distributed", "Radiant", "Calibrant", "Fractal")):
        key = name.lower()
        centre = 620.75 + 414 / 4 * (index + 0.5)
        slot = ET.SubElement(band, f"{{{NS}}}g", {
            "id": f"cover-icon-{key}",
            "transform": f"translate({centre} 491) scale({icon_scale:.10f}) translate(-48 -48)",
        })
        icon = ET.parse(ROOT / f"figures/_shared/icons/ic-{key}.svg").getroot()
        artwork = deepcopy(icon.find(".//*[@id='artwork']"))
        assert artwork is not None
        for node in artwork.iter():
            if "id" in node.attrib:
                node.set("id", f"cover-{key}-{node.get('id')}")
        slot.append(artwork)
        label = ET.SubElement(band, f"{{{NS}}}text", {
            "id": f"cover-label-{key}", "x": str(centre), "y": "537",
            "text-anchor": "middle", "font-family": "Charter", "font-weight": "bold",
            "font-size": f"{LABEL_PT / FRONT_SCALE_Y:.8f}", "fill": "#4A3F30",
        })
        label.text = name.upper()

    for identifier in ("back", "spine_2_", "engineering_1_", "as-reference-a4",
                       "variant-rule"):
        assert ET.tostring(root.find(f".//*[@id='{identifier}']")) == ET.tostring(
            original.getroot().find(f".//*[@id='{identifier}']"))
    for key in ("width", "height", "viewBox"):
        assert root.get(key) == original.getroot().get(key)
    ids = [node.get("id") for node in root.iter() if node.get("id")]
    assert len(ids) == len(set(ids)), "Duplicate SVG IDs"
    tree.write(DESTINATION, encoding="utf-8", xml_declaration=True)

    result = subprocess.run([INKSCAPE, str(DESTINATION), "--query-all"],
                            check=True, text=True, capture_output=True)
    boxes = {row[0]: tuple(map(float, row[1:]))
             for row in csv.reader(io.StringIO(result.stdout))}
    rule = boxes["variant-rule"]
    sx, sy, sw, sh = boxes["variant-subtitle"]
    assert sx >= rule[0] and sx + sw <= rule[0] + rule[2], "Subtitle exceeds divider width"
    last_right = None
    for name in ("distributed", "radiant", "calibrant", "fractal"):
        x, y, width, height = boxes[f"cover-icon-{name}"]
        lx, ly, lw, lh = boxes[f"cover-label-{name}"]
        assert abs(width * 25.4 / 96 - ICON_WIDTH_MM) < 0.01
        assert y > rule[1] + rule[3] and ly > y + height
        assert abs(x + width / 2 - (lx + lw / 2)) < 2
        assert lx >= rule[0] and lx + lw <= rule[0] + rule[2]
        assert last_right is None or lx > last_right
        last_right = lx + lw
    subprocess.run([INKSCAPE, str(DESTINATION), "--export-id=front", "--export-id-only",
                    "--export-width=1200",
                    f"--export-filename={COVERS / 'as-book-a5-four-icons.front.png'}"], check=True)
    subprocess.run([INKSCAPE, str(DESTINATION), "--export-width=2400",
                    f"--export-filename={COVERS / 'as-book-a5-four-icons.wrap.png'}"], check=True)
    print(f"Verified: 13 mm icons, {LABEL_PT} pt bold labels, no collisions; back, spine and wrap geometry unchanged.")


if __name__ == "__main__":
    main()

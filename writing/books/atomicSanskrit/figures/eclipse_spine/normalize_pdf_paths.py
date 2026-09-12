"""Split disconnected strokes so rsvg's PDF output preserves their positions.

Run from figures/: ../.venv-figures/bin/python3 -m eclipse_spine.normalize_pdf_paths
The original .from-ai.svg designs remain the editable sources. This creates
.from-ai-cdx.svg production variants and promotes them through the usual
outlining and lineage helper.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.svgLib.path import parse_path

from _shared.lineage import promote

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


def split_strokes(tree: ET.ElementTree) -> int:
    changed = 0
    for parent in list(tree.iter()):
        for element in list(parent):
            if (
                element.tag != f"{{{SVG}}}path"
                or element.get("fill") != "none"
                or not element.get("stroke")
            ):
                continue
            recording = RecordingPen()
            parse_path(element.get("d", ""), recording)
            if sum(op == "moveTo" for op, _ in recording.value) < 2:
                continue
            contours = []
            pen = None
            for operation, arguments in recording.value:
                if operation == "moveTo":
                    if pen is not None:
                        contours.append(pen.getCommands())
                    pen = SVGPathPen(None)
                getattr(pen, operation)(*arguments)
            if pen is not None:
                contours.append(pen.getCommands())

            # Keep opacity, filters, transforms, and IDs on the original union
            # of strokes; the child paths inherit the stroke appearance.
            group = ET.Element(f"{{{SVG}}}g", {
                key: value for key, value in element.attrib.items() if key != "d"
            })
            group.tail = element.tail
            for contour in contours:
                ET.SubElement(group, f"{{{SVG}}}path", {"d": contour})
            index = list(parent).index(element)
            parent.remove(element)
            parent.insert(index, group)
            changed += 1
    return changed


def main() -> None:
    folder = Path(__file__).resolve().parent
    for source in sorted(folder.glob("*.from-ai.svg")):
        tree = ET.parse(source)
        changed = split_strokes(tree)
        if not changed:
            print(f"{source.name}: no disconnected strokes")
            continue
        tree.getroot().insert(0, ET.Comment(
            " PDF geometry normalization: disconnected strokes are separate "
            "paths; original coordinates and appearance are retained. "
        ))
        variant = source.with_name(source.name.replace(".from-ai.svg", ".from-ai-cdx.svg"))
        ET.indent(tree, space="  ")
        tree.write(variant, encoding="utf-8", xml_declaration=True)
        promote(variant)
        print(f"{variant.name}: separated {changed} compound stroke paths")


if __name__ == "__main__":
    main()

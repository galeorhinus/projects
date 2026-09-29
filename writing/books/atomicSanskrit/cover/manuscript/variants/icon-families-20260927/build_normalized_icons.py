"""Normalize the selected four icons by visible width, including strokes."""

from copy import deepcopy
import csv
import io
import subprocess
import tempfile
from pathlib import Path
import xml.etree.ElementTree as ET

from build_options import HERE, ICONS, INKSCAPE, NS, GOLD, PAPER, element, existing, icon, label, line, place, ring

OUTPUT = HERE / "normalized-icons"
TARGET_WIDTH = 80


def bounds(path):
    result = subprocess.run([INKSCAPE, str(path), "--query-all"],
                            check=True, capture_output=True, text=True)
    for row in csv.reader(io.StringIO(result.stdout)):
        if row[0] == "artwork":
            return tuple(float(value) for value in row[1:])
    raise ValueError(f"No artwork bounds in {path}")


def source_group(source):
    group = deepcopy(source)
    if group.tag == f"{{{NS}}}svg":
        group.tag = f"{{{NS}}}g"
        for key in ("viewBox", "width", "height"):
            group.attrib.pop(key, None)
    return group


def write(root, path):
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def export(path, output, width, background=False):
    command = [INKSCAPE, str(path), f"--export-width={width}", f"--export-filename={output}"]
    if background:
        command += [f"--export-background={PAPER}", "--export-background-opacity=1"]
    subprocess.run(command, check=True)


def final_distributed():
    root = icon()
    points = ring(48, 48, 30)
    for i, p in enumerate(points):
        q = points[(i + 1) % 6]
        dx, dy = (q[0] - p[0]) / 30, (q[1] - p[1]) / 30
        line(root, (p[0] + dx * 7.5, p[1] + dy * 7.5),
             (q[0] - dx * 7.5, q[1] - dy * 7.5), 2.3)
    for p in points:
        element("polygon", root,
                points=" ".join(f"{x:.3f},{y:.3f}" for x, y in ring(*p, 7)),
                stroke_width=2, fill=GOLD)
    return root


def main():
    OUTPUT.mkdir(exist_ok=True)
    sources = [
        ("Distributed", final_distributed()),
        ("Radiant", existing("ic-sanskrit-sun.svg")),
        ("Calibrant", existing("ic-calibration.svg")),
        ("Fractal", ET.parse(HERE / "fractal-fork-weight/option-4-fractal.svg").getroot()),
    ]
    normalized = []
    with tempfile.TemporaryDirectory(prefix="as-icon-bounds-") as directory:
        for name, source in sources:
            root = element("svg", viewBox="0 0 96 96", width=96, height=96,
                           id=f"ic-{name.lower()}", role="img",
                           aria_labelledby=f"{name.lower()}-title")
            title = element("title", root, id=f"{name.lower()}-title")
            title.text = name
            artwork = element("g", root, id="artwork")
            artwork.append(source_group(source))
            temporary = Path(directory) / f"{name}.svg"
            write(root, temporary)
            x, y, width, height = bounds(temporary)
            scale = TARGET_WIDTH / width
            artwork.set("transform", f"translate(48 48) scale({scale:.10f}) "
                        f"translate({-(x + width / 2):.10f} {-(y + height / 2):.10f})")
            destination = ICONS / f"ic-{name.lower()}.svg"
            write(root, destination)
            final_x, final_y, final_width, final_height = bounds(destination)
            assert abs(final_width - TARGET_WIDTH) < 0.002
            assert abs(final_x + final_width / 2 - 48) < 0.002
            assert abs(final_y + final_height / 2 - 48) < 0.002
            assert final_y >= 0 and final_y + final_height <= 96
            export(destination, OUTPUT / f"ic-{name.lower()}.png", 576, background=True)
            print(f"{name}: visible {final_width:.2f} x {final_height:.2f}; scale {scale:.4f}")
            normalized.append((name, root, final_width, final_height))

    sheet = element("svg", viewBox="0 0 1120 470", width=1120, height=470)
    element("rect", sheet, width=1120, height=470, fill=PAPER)
    label(sheet, "Atomic Sanskrit: Final Icons", 40, 42, 26, "700", "start")
    label(sheet, "80-unit visible width on 96-unit canvases; proportions preserved; artwork centred",
          40, 74, 18, anchor="start")
    for col, (name, source, width, height) in enumerate(normalized):
        centre = 140 + col * 280
        label(sheet, name, centre, 119, 22, "700")
        place(sheet, source, centre - 90, 150, 180)
        label(sheet, f"{width:.1f} x {height:.1f}", centre, 356, 17)
        place(sheet, source, centre - 22, 390, 44)
    sheet_path = OUTPUT / "four-icons-normalized.svg"
    write(sheet, sheet_path)
    export(sheet_path, OUTPUT / "four-icons-normalized.png", 2240)
    final_path = ICONS / "final-icons.svg"
    write(sheet, final_path)
    export(final_path, ICONS / "final-icons.png", 2240)


if __name__ == "__main__":
    main()

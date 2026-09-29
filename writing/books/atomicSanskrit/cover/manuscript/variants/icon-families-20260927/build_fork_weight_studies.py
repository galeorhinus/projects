"""Keep the selected compact 3-2-3 design and compare outer forks and weight."""

import subprocess
import xml.etree.ElementTree as ET

from build_options import HERE, INKSCAPE, PAPER, element, existing, hex_family, label, line, place
from build_fractal_variations import branching_icon

OUTPUT = HERE / "fractal-fork-weight"
STUDIES = [
    ("Selected row 4", 18.8 * 0.70 * 0.70, 2.3),
    ("Longer outer forks", 12, 2.3),
    ("Longer, lighter", 12, 1.8),
    ("Longer, heavier", 12, 2.8),
]


def render(root, name, width):
    path = OUTPUT / f"{name}.svg"
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    subprocess.run([INKSCAPE, str(path), f"--export-width={width}",
                    f"--export-filename={path.with_suffix('.png')}"], check=True)


def main():
    OUTPUT.mkdir(exist_ok=True)
    distributed = hex_family()[0]
    radiant = existing("ic-sanskrit-sun.svg")
    calibrant = existing("ic-calibration.svg")
    selected = ET.parse(HERE / "fractal-second-fork-four/option-4-fractal.svg").getroot()
    sheet = element("svg", viewBox="0 0 1280 1315", width=1280, height=1315)
    element("rect", sheet, width=1280, height=1315, fill=PAPER)
    label(sheet, "Compact Fractal: Fork Length and Stroke", 44, 48, 28, "700", "start")
    label(sheet, "All 3-2-3. Centre to first fork: 10 units; between forks: 7 units; angles: 35 degrees.",
          44, 78, 17, anchor="start")
    columns = ["Distributed", "Radiant", "Calibrant", "Fractal"]
    for col, name in enumerate(columns):
        label(sheet, name, 410 + col * 240, 128, 23, "700")
    for row, (name, outer_length, stroke) in enumerate(STUDIES):
        fractal = branching_icon(3, (2, 3), fork_degrees=35,
                                 uniform_width=stroke, segment_lengths=(10, 7, outer_length))
        if row == 0:
            assert ET.tostring(fractal) == ET.tostring(selected)
        ET.ElementTree(fractal).write(OUTPUT / f"option-{row + 1}-fractal.svg",
                                      encoding="utf-8", xml_declaration=True)
        top = 155 + row * 285
        line(sheet, (44, top), (1236, top), 1, "#DBCEB4")
        label(sheet, f"OPTION {row + 1}", 44, top + 78, 16, "700", "start", "#7C5E29")
        label(sheet, name, 44, top + 110, 20, anchor="start")
        label(sheet, f"Outer forks: {outer_length:g}", 44, top + 142, 17, anchor="start")
        label(sheet, f"Uniform stroke: {stroke:g}", 44, top + 169, 17, anchor="start")
        strip = element("svg", viewBox="0 0 1120 350", width=1120, height=350)
        element("rect", strip, width=1120, height=350, fill=PAPER)
        label(strip, f"Option {row + 1}: {name} | outer forks {outer_length:g} | stroke {stroke:g}",
              40, 42, 24, "700", "start")
        for col, item in enumerate([distributed, radiant, calibrant, fractal]):
            place(sheet, item, 330 + col * 240, top + 40, 160)
            place(sheet, item, 388 + col * 240, top + 218, 44)
            label(strip, columns[col], 140 + col * 280, 88, 20, "700")
            place(strip, item, 60 + col * 280, 115, 160)
            place(strip, item, 122 + col * 280, 300, 36)
        render(strip, f"option-{row + 1}", 1680)
    render(sheet, "four-fork-weight-variations", 1920)


if __name__ == "__main__":
    main()

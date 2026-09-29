"""Render four architecture-icon families beside the existing cover icons."""

from copy import deepcopy
import math
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ICONS = ROOT / "figures/_shared/icons"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
GOLD = "#CF8A2E"
PAPER = "#FFF6E1"
INK = "#4A3F30"
INKSCAPE = shutil.which("inkscape") or "/Applications/Inkscape.app/Contents/MacOS/inkscape"


def element(tag, parent=None, **attrs):
    node = ET.Element(f"{{{NS}}}{tag}", {k.replace("_", "-"): str(v) for k, v in attrs.items()})
    if parent is not None:
        parent.append(node)
    return node


def icon():
    return element("svg", viewBox="0 0 96 96", width=96, height=96,
                   fill="none", stroke=GOLD, stroke_width=3.2,
                   stroke_linecap="round", stroke_linejoin="round")


def line(parent, a, b, width=3.2, color=GOLD):
    element("line", parent, x1=a[0], y1=a[1], x2=b[0], y2=b[1],
            stroke=color, stroke_width=width)


def dot(parent, p, radius=4):
    element("circle", parent, cx=p[0], cy=p[1], r=radius, fill=GOLD, stroke="none")


def ring(cx, cy, radius, count=6, angle=0):
    return [(cx + radius * math.cos(angle + i * 2 * math.pi / count),
             cy + radius * math.sin(angle + i * 2 * math.pi / count)) for i in range(count)]


def hexagon(parent, p, radius, width=3):
    element("polygon", parent, points=" ".join(f"{x:.3f},{y:.3f}" for x, y in ring(*p, radius)),
            stroke_width=width)


def hex_family():
    distributed, fractal = icon(), icon()
    points = ring(48, 48, 30)
    for index, p in enumerate(points):
        q = points[(index + 1) % 6]
        vector = ((q[0] - p[0]) / 30, (q[1] - p[1]) / 30)
        line(distributed, (p[0] + vector[0] * 11, p[1] + vector[1] * 11),
             (q[0] - vector[0] * 11, q[1] - vector[1] * 11), 2.6)
        hexagon(distributed, p, 9)
        hexagon(fractal, p, 12, 2)
        for small in ring(*p, 6):
            hexagon(fractal, small, 2.3, 1.25)
    return distributed, fractal


def network_family():
    distributed, fractal = icon(), icon()
    points = [(17, 25), (45, 12), (79, 23), (32, 48), (70, 55), (16, 77), (53, 83)]
    for a, b in [(0, 1), (1, 2), (0, 3), (1, 3), (2, 4), (3, 4),
                 (3, 5), (3, 6), (4, 6), (5, 6)]:
        line(distributed, points[a], points[b], 2.7)
    for point in points:
        dot(distributed, point, 5)

    def branch(start, angle, length, depth):
        end = (start[0] + length * math.cos(angle), start[1] + length * math.sin(angle))
        line(fractal, start, end, 1.6 + depth * 0.7)
        if depth:
            for turn in (-math.pi / 4, math.pi / 4):
                branch(end, angle + turn, length * 0.57, depth - 1)

    for direction in range(4):
        branch((48, 48), direction * math.pi / 2, 22, 2)
    return distributed, fractal


def constellation_family():
    distributed, fractal = icon(), icon()
    points = [(17, 23), (44, 16), (77, 24), (28, 46), (64, 44),
              (14, 76), (47, 68), (79, 78), (74, 61)]
    for a, b in [(0, 1), (0, 3), (2, 4), (4, 8), (5, 6), (6, 7)]:
        line(distributed, points[a], points[b], 1.9)
    for p in points:
        dot(distributed, p, 4.2)
    # The three-dot arrangement repeats at the larger scale of three clusters.
    for centre in ring(48, 48, 27, 3, -math.pi / 2):
        for p in ring(*centre, 11, 3, -math.pi / 2):
            dot(fractal, p, 4.3)
    return distributed, fractal


def woven_grid(parent, positions, low, high, width):
    for p in positions:
        line(parent, (p, low), (p, high), width)
        line(parent, (low, p), (high, p), width)
    for row, y in enumerate(positions):
        for col, x in enumerate(positions):
            horizontal = (row + col) % 2 == 0
            a, b = ((x - width - 1, y), (x + width + 1, y)) if horizontal else (
                (x, y - width - 1), (x, y + width + 1))
            line(parent, a, b, width + 3, PAPER)
            line(parent, a, b, width)


def weave_family():
    distributed, fractal = icon(), icon()
    woven_grid(distributed, [24, 48, 72], 11, 85, 5)
    # Each broad strand is a bundle; intersections repeat the over/under weave.
    positions = [22, 28, 34, 62, 68, 74]
    woven_grid(fractal, positions, 10, 86, 2.3)
    return distributed, fractal


def existing(name):
    source = ET.parse(ICONS / name).getroot()
    group = element("g", color=GOLD)
    if source.get("viewBox") == "0 0 48 48":
        group.set("transform", "scale(2)")
    for child in source:
        group.append(deepcopy(child))
    return group


def label(parent, words, x, y, size=20, weight="400", anchor="middle", color=INK):
    node = element("text", parent, x=x, y=y, font_family="Charter", font_size=size,
                   font_weight=weight, text_anchor=anchor, fill=color, stroke="none")
    node.text = words


def place(parent, source, x, y, size):
    group = element("g", parent, transform=f"translate({x} {y}) scale({size / 96})")
    if source.tag == f"{{{NS}}}svg":
        nested = deepcopy(source)
        group.append(nested)
    else:
        group.append(deepcopy(source))


def render(root, filename, width):
    svg = HERE / f"{filename}.svg"
    ET.ElementTree(root).write(svg, encoding="utf-8", xml_declaration=True)
    subprocess.run([INKSCAPE, str(svg), f"--export-width={width}",
                    f"--export-filename={svg.with_suffix('.png')}"], check=True)


def main():
    families = [hex_family(), network_family(), constellation_family(), weave_family()]
    names = ["Hexagonal", "Network and branching", "Constellations", "Interweaving"]
    columns = ["Distributed", "Radiant", "Calibrant", "Fractal"]
    radiant, calibrant = existing("ic-sanskrit-sun.svg"), existing("ic-calibration.svg")
    sheet = element("svg", viewBox="0 0 1280 1315", width=1280, height=1315)
    element("rect", sheet, width=1280, height=1315, fill=PAPER)
    label(sheet, "Four Architecture Icon Families", 44, 48, 28, "700", "start")
    label(sheet, "Existing radiant and calibrant icons repeated for comparison", 44, 78, 17, anchor="start")
    for col, name in enumerate(columns):
        label(sheet, name, 410 + col * 240, 128, 23, "700")
    for row, ((distributed, fractal), name) in enumerate(zip(families, names)):
        top = 155 + row * 285
        line(sheet, (44, top), (1236, top), 1, "#DBCEB4")
        label(sheet, f"OPTION {row + 1}", 44, top + 92, 16, "700", "start", "#7C5E29")
        for index, word in enumerate(name.split(" and ")):
            label(sheet, word if index == 0 else "and " + word, 44, top + 124 + index * 26,
                  22, anchor="start")
        strip = element("svg", viewBox="0 0 1120 350", width=1120, height=350)
        element("rect", strip, width=1120, height=350, fill=PAPER)
        label(strip, f"Option {row + 1}: {name}", 40, 42, 24, "700", "start")
        for col, item in enumerate([distributed, radiant, calibrant, fractal]):
            place(sheet, item, 330 + col * 240, top + 40, 160)
            # A second, smaller rendering tests how the details survive reduction.
            place(sheet, item, 388 + col * 240, top + 218, 44)
            label(strip, columns[col], 140 + col * 280, 88, 20, "700")
            place(strip, item, 60 + col * 280, 115, 160)
            place(strip, item, 122 + col * 280, 300, 36)
        for kind, source in [("distributed", distributed), ("fractal", fractal)]:
            ET.ElementTree(source).write(HERE / f"option-{row + 1}-{kind}.svg",
                                         encoding="utf-8", xml_declaration=True)
        render(strip, f"option-{row + 1}", 1680)
    render(sheet, "four-icon-families", 1920)


if __name__ == "__main__":
    main()

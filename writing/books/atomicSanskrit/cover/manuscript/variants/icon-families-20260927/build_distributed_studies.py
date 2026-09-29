"""Compare filled hexagons with three progressively heavier connector weights."""

import xml.etree.ElementTree as ET

from build_options import HERE, ICONS, GOLD, PAPER, element, label, line, place, ring
from build_normalized_icons import bounds, export, write

OUTPUT = HERE / "distributed-fill-studies"
STUDIES = [
    ("Thin connectors", [1.4] * 6, True),
    ("Medium connectors", [2.3] * 6, True),
    ("Thick connectors", [3.2] * 6, True),
]


def distributed_icon(widths, path, filled):
    root = element("svg", viewBox="0 0 96 96", width=96, height=96)
    artwork = element("g", root, id="artwork", fill="none", stroke=GOLD,
                      stroke_linecap="round", stroke_linejoin="round")
    points = ring(48, 48, 30)
    for i, p in enumerate(points):
        q = points[(i + 1) % 6]
        dx, dy = (q[0] - p[0]) / 30, (q[1] - p[1]) / 30
        line(artwork, (p[0] + dx * 7.5, p[1] + dy * 7.5),
             (q[0] - dx * 7.5, q[1] - dy * 7.5), widths[i])
    for p in points:
        element("polygon", artwork,
                points=" ".join(f"{x:.3f},{y:.3f}" for x, y in ring(*p, 7)),
                stroke_width=2, fill=GOLD if filled else "none")
    write(root, path)
    x, y, width, height = bounds(path)
    artwork.set("transform", f"translate(48 48) scale({80 / width:.10f}) "
                f"translate({-(x + width / 2):.10f} {-(y + height / 2):.10f})")
    write(root, path)
    x, y, width, height = bounds(path)
    assert abs(width - 80) < 0.002
    assert abs(x + width / 2 - 48) < 0.002
    assert abs(y + height / 2 - 48) < 0.002
    return root


def main():
    OUTPUT.mkdir(exist_ok=True)
    reference = ET.parse(ICONS / "ic-distributed.svg").getroot()
    fixed = [ET.parse(ICONS / f"ic-{name}.svg").getroot()
             for name in ("radiant", "calibrant", "fractal")]
    rows = [("Current design", reference, ["All hexagons unfilled", "Original weights"])]
    for i, (name, widths, filled) in enumerate(STUDIES, start=1):
        root = distributed_icon(widths, OUTPUT / f"variation-{i}-distributed.svg", filled)
        details = ["All six hexagons filled" if filled else "All six hexagons hollow",
                   f"Connector stroke: {widths[0]:g}"]
        rows.append((name, root, details))

    sheet = element("svg", viewBox="0 0 1280 1315", width=1280, height=1315)
    element("rect", sheet, width=1280, height=1315, fill=PAPER)
    label(sheet, "Distributed: Filled Hexagons, Connector Weights", 44, 48, 28, "700", "start")
    label(sheet, "80-unit visible widths throughout; radiant, calibrant and fractal unchanged",
          44, 78, 17, anchor="start")
    names = ["Distributed", "Radiant", "Calibrant", "Fractal"]
    for col, name in enumerate(names):
        label(sheet, name, 410 + col * 240, 128, 23, "700")
    for row, (name, distributed, details) in enumerate(rows):
        top = 155 + row * 285
        line(sheet, (44, top), (1236, top), 1, "#DBCEB4")
        label(sheet, "REFERENCE" if row == 0 else f"VARIATION {row}",
              44, top + 78, 16, "700", "start", "#7C5E29")
        label(sheet, name, 44, top + 110, 20, anchor="start")
        for j, text in enumerate(details):
            label(sheet, text, 44, top + 144 + j * 25, 16, anchor="start")
        strip = element("svg", viewBox="0 0 1120 350", width=1120, height=350)
        element("rect", strip, width=1120, height=350, fill=PAPER)
        label(strip, name, 40, 42, 24, "700", "start")
        for col, item in enumerate([distributed] + fixed):
            place(sheet, item, 330 + col * 240, top + 40, 160)
            place(sheet, item, 388 + col * 240, top + 218, 44)
            label(strip, names[col], 140 + col * 280, 88, 20, "700")
            place(strip, item, 60 + col * 280, 115, 160)
            place(strip, item, 122 + col * 280, 300, 36)
        path = OUTPUT / f"row-{row + 1}.svg"
        write(strip, path)
        export(path, path.with_suffix(".png"), 1680)
    path = OUTPUT / "distributed-fill-comparison.svg"
    write(sheet, path)
    export(path, path.with_suffix(".png"), 1920)


if __name__ == "__main__":
    main()

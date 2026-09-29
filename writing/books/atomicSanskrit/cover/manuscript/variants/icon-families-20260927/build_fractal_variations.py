"""Compare spoke/fork counts while holding the other three icons fixed."""

import argparse
import math
import subprocess
import xml.etree.ElementTree as ET

from build_options import (
    HERE, INKSCAPE, NS, PAPER, element, existing, hex_family, icon,
    label, line, network_family, place,
)

OUTPUT = HERE / "fractal-spokes"
OPTIONS = [(4, 2), (3, 2), (3, 3), (6, 3)]


def branching_icon(spokes, forks, root_length=22, ratio=0.57, fork_degrees=45,
                   uniform_width=None, segment_lengths=None):
    result = icon()
    spread = math.radians(fork_degrees)
    fork_counts = (forks, forks) if isinstance(forks, int) else forks
    assert len(fork_counts) == 2 and all(count in (2, 3) for count in fork_counts)

    def branch(start, angle, length, depth):
        if segment_lengths is not None:
            length = segment_lengths[2 - depth]
        end = (start[0] + length * math.cos(angle), start[1] + length * math.sin(angle))
        line(result, start, end, uniform_width if uniform_width is not None else 1.6 + depth * 0.7)
        if depth:
            count = fork_counts[2 - depth]
            turns = (-spread, spread) if count == 2 else (-spread, 0, spread)
            for turn in turns:
                branch(end, angle + turn, length * ratio, depth - 1)

    rotation = -math.pi / 2 if spokes == 3 else 0
    for direction in range(spokes):
        branch((48, 48), rotation + direction * 2 * math.pi / spokes, root_length, 2)
    assert len(result.findall(f"{{{NS}}}line")) == spokes * (
        1 + fork_counts[0] + fork_counts[0] * fork_counts[1])
    return result


def render(root, name, width):
    path = OUTPUT / f"{name}.svg"
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    subprocess.run([INKSCAPE, str(path), f"--export-width={width}",
                    f"--export-filename={path.with_suffix('.png')}"], check=True)


def main():
    global OUTPUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--early-forks", action="store_true")
    parser.add_argument("--compare-strokes", action="store_true",
                        help="Append four uniform 2.3-unit stroke variants to the early-fork comparison.")
    parser.add_argument("--uniform-six", action="store_true",
                        help="Four fixed-stroke designs plus mixed 3-2-3 and 3-3-2 patterns.")
    parser.add_argument("--second-fork-four", action="store_true",
                        help="Retain 3-2-2 and 3-2-3, then move the second fork inward in two variants.")
    args = parser.parse_args()
    if args.compare_strokes and not args.early_forks:
        parser.error("--compare-strokes requires --early-forks")
    if args.uniform_six and (not args.early_forks or args.compare_strokes):
        parser.error("--uniform-six requires --early-forks and excludes --compare-strokes")
    if args.second_fork_four and (not args.early_forks or args.compare_strokes or args.uniform_six):
        parser.error("--second-fork-four requires --early-forks and excludes other comparison modes")
    options = OPTIONS
    geometry = {}
    if args.early_forks:
        OUTPUT = HERE / "fractal-spokes-early"
        options = [(3, 2), (3, 3), (6, 2), (6, 3)]
        # Earlier splits lengthen the outer branches; narrower forks keep adjacent
        # six-spoke sectors separate while retaining the original overall reach.
        geometry = dict(root_length=18.8, ratio=0.70, fork_degrees=35)
    if args.compare_strokes:
        OUTPUT = HERE / "fractal-stroke-comparison"
        options = options * 2
    if args.uniform_six:
        OUTPUT = HERE / "fractal-uniform-six"
        options += [(3, (2, 3)), (3, (3, 2))]
    if args.second_fork_four:
        OUTPUT = HERE / "fractal-second-fork-four"
        options = [(3, 2), (3, (2, 3)), (3, (2, 3)), (3, (2, 3))]
    OUTPUT.mkdir(exist_ok=True)
    distributed = hex_family()[0]
    radiant, calibrant = existing("ic-sanskrit-sun.svg"), existing("ic-calibration.svg")
    assert ET.tostring(branching_icon(4, 2)) == ET.tostring(network_family()[1])
    height = 175 + len(options) * 285
    sheet = element("svg", viewBox=f"0 0 1280 {height}", width=1280, height=height)
    element("rect", sheet, width=1280, height=height, fill=PAPER)
    title = "Earlier Forks: Three and Six Spokes" if args.early_forks else "Four Fractal Variations"
    description = ("First fork at 46% of the branch path; distributed, radiant and calibrant unchanged"
                   if args.early_forks else
                   "Distributed, radiant and calibrant fixed; two levels of branching in every fractal")
    if args.compare_strokes:
        title = "Fractal Strokes: Stepped and Uniform"
        description = "Rows 1-4 unchanged: 3 / 2.3 / 1.6 units. Rows 5-8: uniform 2.3-unit strokes."
    if args.uniform_six:
        title = "Fixed Strokes: Six Fractal Variations"
        description = "Fixed 2.3-unit strokes. First forks: rows 1-2 and 5-6 at 10; rows 3-4 at 18.8 units."
    if args.second_fork_four:
        title = "Fractal Variations: Earlier Second Forks"
        description = "Fixed 2.3-unit strokes; first fork at 10 units. Only the middle segment changes in rows 3-4."
    label(sheet, title, 44, 48, 28, "700", "start")
    label(sheet, description,
          44, 78, 17, anchor="start")
    columns = ["Distributed", "Radiant", "Calibrant", "Fractal"]
    for col, name in enumerate(columns):
        label(sheet, name, 410 + col * 240, 128, 23, "700")
    for row, (spokes, forks) in enumerate(options):
        fork_counts = (forks, forks) if isinstance(forks, int) else forks
        fork_label = f"{fork_counts[0]} then {fork_counts[1]} forks"
        uniform = args.uniform_six or args.second_fork_four or (args.compare_strokes and row >= 4)
        row_geometry = dict(geometry)
        if args.uniform_six and (row < 2 or row >= 4):
            row_geometry["segment_lengths"] = (10, 18.8 * 0.70, 18.8 * 0.70 * 0.70)
        if args.second_fork_four:
            middle_length = [18.8 * 0.70, 18.8 * 0.70, 10, 7][row]
            row_geometry["segment_lengths"] = (10, middle_length, 18.8 * 0.70 * 0.70)
        first_fork = row_geometry.get("segment_lengths", (geometry.get("root_length", 22),))[0]
        fractal = branching_icon(spokes, forks, **row_geometry,
                                 uniform_width=2.3 if uniform else None)
        ET.ElementTree(fractal).write(OUTPUT / f"option-{row + 1}-fractal.svg",
                                      encoding="utf-8", xml_declaration=True)
        top = 155 + row * 285
        line(sheet, (44, top), (1236, top), 1, "#DBCEB4")
        label(sheet, f"OPTION {row + 1}", 44, top + 92, 16, "700", "start", "#7C5E29")
        label(sheet, f"{spokes} spokes", 44, top + 124, 22, anchor="start")
        label(sheet, fork_label, 44, top + 152, 20, anchor="start")
        if args.compare_strokes:
            label(sheet, "Uniform 2.3 units" if uniform else "Stepped thickness",
                  44, top + 184, 16, anchor="start", color="#7C5E29")
        if args.uniform_six:
            label(sheet, f"First fork: {first_fork:g} units",
                  44, top + 184, 16, anchor="start", color="#7C5E29")
        if args.second_fork_four:
            label(sheet, f"Between forks: {middle_length:g}",
                  44, top + 184, 16, anchor="start", color="#7C5E29")
            if row < 2:
                label(sheet, f"Previous row {1 if row == 0 else 5}",
                      44, top + 208, 15, anchor="start", color="#7C5E29")
        strip = element("svg", viewBox="0 0 1120 350", width=1120, height=350)
        element("rect", strip, width=1120, height=350, fill=PAPER)
        stroke_label = " | uniform 2.3 units" if uniform else ""
        if args.uniform_six:
            stroke_label += f" | fork at {first_fork:g}"
        if args.second_fork_four:
            stroke_label += f" | between forks: {middle_length:g}"
        label(strip, f"Option {row + 1}: {spokes} spokes, {fork_label}{stroke_label}",
              40, 42, 24, "700", "start")
        for col, item in enumerate([distributed, radiant, calibrant, fractal]):
            place(sheet, item, 330 + col * 240, top + 40, 160)
            place(sheet, item, 388 + col * 240, top + 218, 44)
            label(strip, columns[col], 140 + col * 280, 88, 20, "700")
            place(strip, item, 60 + col * 280, 115, 160)
            place(strip, item, 122 + col * 280, 300, 36)
        render(strip, f"option-{row + 1}", 1680)
    filename = "six-fractal-variations" if args.uniform_six else (
        "eight-fractal-variations" if args.compare_strokes else "four-fractal-variations")
    if args.second_fork_four:
        filename = "four-second-fork-variations"
    render(sheet, filename, 1920)


if __name__ == "__main__":
    main()

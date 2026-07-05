#!/usr/bin/env python3
"""Generate the yuga combined-wave SVG.

Edit the parameter block below, then run:

    python3 figures/yuga/generate_yuga_wave.py
"""

from __future__ import annotations

import math
from pathlib import Path


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------

OUTPUT_SVG = "yuga_combined_wave.svg"

WIDTH = 1200
HEIGHT = 520
MARGIN_LEFT = 90
MARGIN_RIGHT = 60
MARGIN_TOP = 54
MARGIN_BOTTOM = 86

# The actual x-domain being plotted.
X_START = 13_100
X_END = 20_600

# Axis labels display x - X_AXIS_OFFSET.
X_AXIS_OFFSET = 17_900

# Combined wave components. Positive phase_degrees_left shifts the wave left.
WAVES = [
    {"name": "A", "period": 25_600, "amplitude": 256, "phase_degrees_left": 0},
    {"name": "B", "period": 2_560, "amplitude": 32, "phase_degrees_left": 0},
    {"name": "C", "period": 360, "amplitude": 8, "phase_degrees_left": 180},
]

# Plot sampling and local y-scaling.
PATH_SAMPLES = 2400
Y_RANGE_PROBE_SAMPLES = 20_000
Y_PADDING_FRACTION = 0.08
Y_TICK_COUNT = 5

# X-axis ticks are generated from the original x-domain, then relabeled.
X_TICK_STEP = 500
X_MAJOR_TICK_MOD = 1000

# Vertical marker lines. Values are in original x-domain coordinates.
# The label is optional. If omitted, the displayed x-axis value is used.
VERTICAL_MARKERS = [
    #{"x": X_AXIS_OFFSET, "label": f"0 = {X_AXIS_OFFSET:,}"},
    # Example:
     {"x": 19_900, "label": "today"},
     {"x": 14_850, "label": "kaliyuga"},
]

# Style
BACKGROUND = "#f7f3ea"
TITLE_COLOR = "#21190f"
TEXT_COLOR = "#4c453b"
TICK_COLOR = "#5c554a"
MAJOR_GRID_COLOR = "#d6ccba"
MINOR_GRID_COLOR = "#e9e1d4"
Y_GRID_COLOR = "#ded4c2"
MARKER_LINE_COLOR = "#7f7666"
WAVE_COLOR = "#1f1710"
FONT_FAMILY = "EB Garamond, Georgia, serif"
WAVE_STROKE_WIDTH = 4.2


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

PLOT_WIDTH = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
PLOT_HEIGHT = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
X_SPAN = X_END - X_START


def fmt(value: float) -> str:
    return f"{value:.2f}"


def label_int(value: float) -> str:
    return f"{round(value):,}"


def label_decimal(value: float) -> str:
    return f"{round(value, 1):,}"


def wave_value(x: float, period: float, amplitude: float, phase_degrees_left: float) -> float:
    phase_shift = period * (phase_degrees_left / 360.0)
    return math.sin(((x + phase_shift) / period) * 2.0 * math.pi) * amplitude


def combined_value(x: float) -> float:
    return sum(
        wave_value(
            x,
            wave["period"],
            wave["amplitude"],
            wave["phase_degrees_left"],
        )
        for wave in WAVES
    )


def x_pixel(x: float) -> float:
    return MARGIN_LEFT + ((x - X_START) / X_SPAN) * PLOT_WIDTH


def y_pixel(value: float, y_min: float, y_max: float) -> float:
    return MARGIN_TOP + ((y_max - value) / (y_max - y_min)) * PLOT_HEIGHT


def local_y_range() -> tuple[float, float, float, float]:
    values = [
        combined_value(X_START + (i / Y_RANGE_PROBE_SAMPLES) * X_SPAN)
        for i in range(Y_RANGE_PROBE_SAMPLES + 1)
    ]
    raw_min = min(values)
    raw_max = max(values)
    padding = (raw_max - raw_min) * Y_PADDING_FRACTION
    return raw_min, raw_max, raw_min - padding, raw_max + padding


def combined_path(y_min: float, y_max: float) -> str:
    parts = []
    for i in range(PATH_SAMPLES + 1):
        x = X_START + (i / PATH_SAMPLES) * X_SPAN
        command = "M" if i == 0 else "L"
        parts.append(f"{command}{fmt(x_pixel(x))} {fmt(y_pixel(combined_value(x), y_min, y_max))}")
    return " ".join(parts)


def wave_formula_label() -> str:
    chunks = []
    for wave in WAVES:
        phase = wave["phase_degrees_left"]
        phase_text = f", phase left {phase:g}°" if phase else ""
        chunks.append(
            f"{wave['name']}(P={wave['period']:,},A={wave['amplitude']:,}{phase_text})"
        )
    return "+".join(chunks)


def svg_line(x1: float, y1: float, x2: float, y2: float, **attrs: object) -> str:
    attr_text = " ".join(f'{key.replace("_", "-")}="{value}"' for key, value in attrs.items())
    return f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" {attr_text}/>'


def svg_text(x: float, y: float, text: str, **attrs: object) -> str:
    attr_text = " ".join(f'{key.replace("_", "-")}="{value}"' for key, value in attrs.items())
    return f'<text x="{fmt(x)}" y="{fmt(y)}" {attr_text}>{text}</text>'


def build_grid(y_min: float, y_max: float) -> list[str]:
    elements: list[str] = []

    tick = X_START
    while tick <= X_END:
        x = x_pixel(tick)
        rel = tick - X_AXIS_OFFSET
        major = tick % X_MAJOR_TICK_MOD == 0
        elements.append(
            svg_line(
                x,
                MARGIN_TOP,
                x,
                MARGIN_TOP + PLOT_HEIGHT,
                stroke=MAJOR_GRID_COLOR if major else MINOR_GRID_COLOR,
                stroke_width=1,
            )
        )
        elements.append(
            svg_line(
                x,
                MARGIN_TOP + PLOT_HEIGHT,
                x,
                MARGIN_TOP + PLOT_HEIGHT + 7,
                stroke=TICK_COLOR,
                stroke_width=1.2,
            )
        )
        elements.append(
            svg_text(
                x,
                HEIGHT - 54,
                label_int(rel),
                font_size=14 if major else 12,
                fill=TICK_COLOR,
                text_anchor="middle",
            )
        )
        tick += X_TICK_STEP

    for marker in VERTICAL_MARKERS:
        marker_x_value = marker["x"]
        if not (X_START <= marker_x_value <= X_END):
            continue

        marker_x = x_pixel(marker_x_value)
        label = marker.get("label", label_int(marker_x_value - X_AXIS_OFFSET))
        elements.append(
            svg_line(
                marker_x,
                MARGIN_TOP,
                marker_x,
                MARGIN_TOP + PLOT_HEIGHT,
                stroke=MARKER_LINE_COLOR,
                stroke_width=1.8,
            )
        )
        elements.append(
            svg_text(
                marker_x,
                HEIGHT - 34,
                label,
                font_size=13,
                fill=TEXT_COLOR,
                text_anchor="middle",
            )
        )

    for i in range(Y_TICK_COUNT + 1):
        value = y_min + (i / Y_TICK_COUNT) * (y_max - y_min)
        y = y_pixel(value, y_min, y_max)
        elements.append(
            svg_line(
                MARGIN_LEFT,
                y,
                WIDTH - MARGIN_RIGHT,
                y,
                stroke=Y_GRID_COLOR,
                stroke_width=1,
                stroke_dasharray="6 8",
            )
        )
        elements.append(
            svg_text(52, y + 5, label_decimal(value), font_size=14, fill=TICK_COLOR)
        )

    return elements


def build_svg() -> str:
    raw_min, raw_max, y_min, y_max = local_y_range()
    grid = "\n    ".join(build_grid(y_min, y_max))
    path = combined_path(y_min, y_max)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <rect width="{WIDTH}" height="{HEIGHT}" fill="{BACKGROUND}"/>
  <text x="{MARGIN_LEFT}" y="34" font-family="{FONT_FAMILY}" font-size="24" font-weight="700" fill="{TITLE_COLOR}">Combined Sine Wave: x = {X_START:,} to {X_END:,}</text>
  <g id="plot-area" font-family="{FONT_FAMILY}">
    {grid}
    <path id="combined-wave" d="{path}" fill="none" stroke="{WAVE_COLOR}" stroke-width="{WAVE_STROKE_WIDTH}" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="{fmt(MARGIN_LEFT + PLOT_WIDTH / 2)}" y="{HEIGHT - 20}" font-size="16" fill="{TEXT_COLOR}" text-anchor="middle">x - {X_AXIS_OFFSET:,}</text>
    <text x="{MARGIN_LEFT}" y="500" font-size="17" fill="{TEXT_COLOR}">Local y-range: {label_decimal(raw_min)} to {label_decimal(raw_max)}. Formula: {wave_formula_label()}</text>
  </g>
</svg>
'''


def main() -> None:
    output_path = Path(__file__).with_name(OUTPUT_SVG)
    output_path.write_text(build_svg(), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()

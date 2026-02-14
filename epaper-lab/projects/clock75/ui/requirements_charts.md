# Clock75 Bottom‑Half Charts Requirements

## Chart Area
- Bounds: x = 10..790, y = 240..470 (780×230)
- Use two stacked rectangles:
  - Top chart: moon elevation vs time (780×115)
  - Bottom chart: temperature vs time (780×115)
- Padding only for labels/ticks.

## Shared X‑Axis
- X‑axis always starts at **sunrise** (leftmost).
- Timeline spans the next 24 hours.
- Tick marks + labels every 2–3 hours.
- Time labels placed **between** the two charts.
- Night shading: since x starts at sunrise, the **rightmost** section (from sunset to next sunrise) is shaded/filled black.

## Temperature Chart (Bottom)
- Left y‑axis shows temperature.
- Range derived from past+forecast, rounded to nearest multiple of 5 (e.g., 37–78 → 35–80).
- Horizontal gridlines every 5° with labels.
- Two curves:
  - **Actuals** (previous hours)
  - **Forecast** (next hours)
- Actual/forecast line style should be distinguishable (solid vs dashed, thickness, or markers).

## Moon Elevation Chart (Top)
- Right y‑axis shows moon elevation.
- Curve shows moon altitude across the same 24‑hour window.
- A moon icon is drawn **on the curve at the current time**.
- Moon icon:
  - Exact phase and orientation derived from **lat/lon/time**.
  - Fill/outline rules depend on:
    - Below vs above horizon
    - Day vs night region (per shading)

## Top Half (Current Layout)
- Keep as‑is for now (date/time + lunar + temps + 7‑day + hourly).

## Readability
- Axis labels and tick labels must remain legible at distance.

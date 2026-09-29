# Final Architecture Icons

Selected 27 September 2026 for *Atomic Sanskrit*.

[View the final set](final-icons.png).

| Concept | Final SVG | Selected design |
| --- | --- | --- |
| Distributed | [ic-distributed.svg](ic-distributed.svg) | Six filled hexagons, medium connectors; row 3 / variation 2 from the distributed-fill comparison. |
| Radiant | [ic-radiant.svg](ic-radiant.svg) | Hexagonal sun with outward rays. |
| Calibrant | [ic-calibrant.svg](ic-calibrant.svg) | Outlined hexagon, centre dot, four alignment marks. |
| Fractal | [ic-fractal.svg](ic-fractal.svg) | Selected 3-2-3 branching design, longer outer forks and heavier uniform strokes; option 4 from the fork/weight comparison. |

Each has an 80-unit visible width, including strokes, centred on a 96 x 96-unit canvas. Proportions are preserved; heights differ slightly. Artwork is gold (`#CF8A2E`), with transparent backgrounds. The comparison PNG uses the cover's cream background.

Distributed source geometry: hexagon radius 7, ring radius 30, connector stroke 2.3, polygon stroke 2. Fractal source geometry: segment lengths 10/7/12, fork angles 35 degrees, uniform stroke 2.8. Uniform normalization scales the geometry and strokes together.

[Fractal Lotus](ic-fractal-lotus.svg) remains a separate saved icon, not the selected fractal in this four-icon set. Older sun and calibration assets remain available and unchanged.

Regenerate from the book root with:

```sh
python3 cover/manuscript/variants/icon-families-20260927/build_normalized_icons.py
```

This selection does not itself replace any cover or manuscript figure.

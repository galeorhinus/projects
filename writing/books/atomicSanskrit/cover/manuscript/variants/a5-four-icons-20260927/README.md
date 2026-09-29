# A5 Cover With Final Architecture Icons

New cover based on subtitle variant B, retaining the existing Atomic Sanskrit title and engineering hexagons.

- [Front preview](../../as-book-a5-four-icons.front.png)
- [Full wrap preview](../../as-book-a5-four-icons.wrap.png)
- [Editable full wrap SVG](../../as-book-a5-four-icons.svg)

The bold uppercase subtitle sits above the divider. Below it are four evenly spaced icons with uppercase labels: DISTRIBUTED, RADIANT, CALIBRANT, FRACTAL. The icons come from the final shared set, including the selected filled-hexagon distributed design. Each icon's visible width is 13 mm; labels are 12.5 pt bold. The subtitle uses 24 source units (approximately 20.2 pt at print size). These sizes accommodate the wider uppercase lettering without overlap. The old text-only tagline and duplicate standalone front calibrant are removed. The author and series line remain unchanged.

The earlier canonical cover `as-book-a5.svg` is untouched. The new wrap retains its back cover, spine, 148 x 210 mm panels, provisional 34.7 mm spine, and 3 mm outer bleed (336.7 x 216 mm overall). Spine suitability has not been recalculated for a new page count or printer stock. This is a layout preview, not a newly validated print package. No PDF was generated.

Run from the book root:

```sh
python3 cover/manuscript/variants/a5-four-icons-20260927/build_cover.py
```

The generator embeds the final SVG icon artwork, prefixes imported IDs, verifies unchanged back/spine geometry, and checks visible icon widths, centred labels, spacing, and collisions using Inkscape bounds. PNG previews were visually inspected.

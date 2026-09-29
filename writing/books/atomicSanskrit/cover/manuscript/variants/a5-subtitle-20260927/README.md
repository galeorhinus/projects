# A5 Cover Studies

Four front-cover alternatives for *Atomic Sanskrit*, 27 September 2026.

Subtitle: **The Architecture of Sanātan**

Tagline: **Distributed · Radiant · Calibrant · Fractal**

[Compare all four](a5-cover-comparison.png).

| Variant | Treatment | Preview | Editable full wrap |
| --- | --- | --- | --- |
| A | Regular subtitle, full-width divider | [PNG](as-book-a5-a-balanced.png) | [SVG](as-book-a5-a-balanced.svg) |
| B | Bold subtitle, full-width divider | [PNG](as-book-a5-b-bold-subtitle.png) | [SVG](as-book-a5-b-bold-subtitle.svg) |
| C | Italic subtitle, shorter divider | [PNG](as-book-a5-c-italic-subtitle.png) | [SVG](as-book-a5-c-italic-subtitle.svg) |
| D | Regular subtitle, larger two-line tagline | [PNG](as-book-a5-d-two-line-tagline.png) | [SVG](as-book-a5-d-two-line-tagline.svg) |

All variants retain the original title and icons. The subtitle spans the composition below them, followed by the divider and tagline. The author, series line, review-copy banner, back cover, and spine are unchanged.

The editable SVGs retain the source wrap's 336.7 x 216 mm dimensions: two 148 x 210 mm panels, a provisional 34.7 mm spine, and 3 mm outer bleed. These are design studies, not a new validation of the spine against the current page count or printer's stock.

The PNGs show only the front panel. No production PDF or canonical cover has been replaced.

To regenerate, run `python3 build_variants.py` in this directory. Requires Inkscape, ImageMagick, and Charter. The script checks that the back, spine, front icons, review banner, and wrap viewBox remain unchanged.

# Archived SVG Raster Fallbacks

Archived on 2026-09-12 after the PDF pipeline switched to canonical vector SVGs.

This directory preserves 146 color PNGs and their 146 grayscale derivatives. Every archived file has a canonical SVG with the same relative path under `figures/`. The raster copies previously overrode those SVGs during PDF assembly, which allowed an older PNG to conceal newer vector artwork.

The relative directory structure is preserved so an individual fallback can be recovered if a future renderer exposes a figure-specific problem.

The eclipse series subsequently required a print exception for unreliable PDF
transparency. Its print images are generated automatically from the current
canonical SVGs under `build/figure-rasters/`, not recovered from this archive.

The following raster-only working assets remain under `figures/` because they have no SVG equivalent:

- `figures/_shared/eng_compare.png`
- `figures/botanical/language2x2-categories.png`
- `figures/botanical/language2x2-list.png`
- `figures/botanical/language2x2-misclassification.png`
- `figures/botanical/language2x2.png`
- `figures/pie_in_sky/seed_icon_options.png`
- `figures/superset/superset_subcontinental_overlay.png`

Of these, the two Chapter 2 language-category figures are intentionally raster because their shadows come from the original design file.

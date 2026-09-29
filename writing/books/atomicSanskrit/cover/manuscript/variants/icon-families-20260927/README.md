# Architecture Icon Studies

[Four-column, four-row comparison](four-icon-families.png)

Columns: Distributed, Radiant, Calibrant, Fractal.

Rows:

1. [Hexagonal](option-1.png): equal connected hexagons; a hexagonal arrangement repeated at a smaller scale.
2. [Network and branching](option-2.png): a peer mesh; successive outward branching.
3. [Constellations](option-3.png): distributed dot clusters; the same three-dot arrangement at two scales.
4. [Interweaving](option-4.png): interdependent strands; bundled strands repeating the over-and-under pattern.

The smaller samples beneath the main icons are reduction checks, not additional options. All designs are exploratory and have not been deployed to the covers or shared icon library.

Radiant uses `figures/_shared/icons/ic-sanskrit-sun.svg`. Calibrant uses `figures/_shared/icons/ic-calibration.svg`, coloured to match the radiant icon. Their geometry is unchanged.

Each new distributed/fractal icon has its own editable SVG. The comparison sheet and four individual rows also have SVG sources and PNG previews. The weaving studies use the cover's cream background for crossing gaps; they would need masks for use on arbitrary backgrounds.

Regenerate with `python3 build_options.py`. Requires Inkscape and Charter.

## Fractal Spoke Variations

[New comparison](fractal-spokes/four-fractal-variations.png) holds the selected Option 1 distributed icon and the existing radiant/calibrant icons fixed in all four rows.

1. Four spokes, two branches followed by two branches: unchanged from the original branching study.
2. Three spokes, two branches followed by two branches.
3. Three spokes, three branches followed by three branches.
4. Six spokes, three branches followed by three branches.

The same branch lengths, shortening ratio, stroke weights, and 45-degree fork angle are used throughout. Three-way forks add a straight continuation between the two angled branches. The small samples test reduction. Individual row PNGs and editable fractal SVGs are in `fractal-spokes/`.

Regenerate this comparison with `python3 build_fractal_variations.py`. The earlier studies remain unchanged.

## Earlier Forks

[Three- and six-spoke comparison](fractal-spokes-early/four-fractal-variations.png): each spoke count has a two-way and a three-way fork variant, with the same fork count repeated at both branching levels. The other three icons are fixed.

The first segment is 18.8 units; subsequent segments are 70% of their parent's length (13.16 and 9.212 units). The first fork is therefore 45.66% along the complete branch path, previously 52.77%. Fork angles are narrowed from 45 to 35 degrees to prevent the longer outer branches from colliding between neighbouring spokes. Overall reach remains similar.

Regenerate with `python3 build_fractal_variations.py --early-forks`. Original comparisons are retained.

## Uniform Stroke Comparison

[Eight-row comparison](fractal-stroke-comparison/eight-fractal-variations.png) retains the four early-fork designs in rows 1-4, then repeats their geometry with uniform 2.3-unit strokes in rows 5-8. The distributed, radiant and calibrant icons remain fixed throughout. Original four-row previews are unchanged.

Regenerate with `python3 build_fractal_variations.py --early-forks --compare-strokes`.

## Six Fixed-Stroke Variants

[Six-row comparison](fractal-uniform-six/six-fractal-variations.png) uses fixed-stroke variants with first forks at 10 units (rows 1-2 and 5-6) and 18.8 units (rows 3-4). All strokes are 2.3 units; all fork angles remain 35 degrees. The other three icons remain fixed.

Rows 1-2 use segment lengths 10, 13.16, and 9.212 units: only the first segment was shortened, without enlarging the outer branches. Rows 3-4 retain 18.8, 13.16, and 9.212 units. Rows 5-6 now use the same geometry as rows 1-2, with mixed branching: 3-2-3 (three spokes, then two branches, then three branches) and 3-3-2 respectively. These replace the earlier 14-unit variants.

Regenerate with `python3 build_fractal_variations.py --early-forks --uniform-six`. Earlier comparisons are retained.

## Earlier Second Forks

[Four-row comparison](fractal-second-fork-four/four-second-fork-variations.png) keeps the preceding six-row sheet's rows 1 and 5 as the first two options: 3-2-2 and 3-2-3. Rows 3-4 are additional 3-2-3 variants with the middle segment shortened from 13.16 units to 10 and 7 units respectively.

All four keep the first segment at 10 units, final segments at 9.212 units, fork angles at 35 degrees, and strokes at 2.3 units. Shortening the middle segment makes the new variants more compact; there is no compensating rescaling. The other three icons are unchanged.

Regenerate with `python3 build_fractal_variations.py --early-forks --second-fork-four`.

## Selected Icons and Fork/Weight Studies

Fractal Lotus is saved in the shared library as `figures/_shared/icons/ic-fractal-lotus.svg`: six spokes, two then two forks, first segment 18.8 units, fixed 2.3-unit strokes. [Standalone PNG](fractal-lotus.png).

[Fork length and stroke comparison](fractal-fork-weight/four-fork-weight-variations.png) retains row 4 from the preceding four-row sheet as option 1, then adds three studies:

1. Selected 3-2-3: outer forks 9.212 units, fixed stroke 2.3 units.
2. Outer forks 12 units, fixed stroke 2.3 units.
3. Outer forks 12 units, fixed stroke 1.8 units.
4. Outer forks 12 units, fixed stroke 2.8 units.

All retain the first two segment lengths (10 and 7 units), 35-degree angles, and the other three icons. Regenerate with `python3 build_fork_weight_studies.py`. Prior sheets and canonical covers are unchanged.

## Final Matched Set

[Normalized comparison PNG](normalized-icons/four-icons-normalized.png).

All four selected icons have an 80-unit visible width, including strokes, centred on 96 x 96 canvases. Scaling is uniform, without stretching. Measured heights vary with the original proportions:

| Shared icon | Visible width | Visible height |
| --- | --- | --- |
| `figures/_shared/icons/ic-distributed.svg` | 80 | 69.56 |
| `figures/_shared/icons/ic-radiant.svg` | 80 | 69.92 |
| `figures/_shared/icons/ic-calibrant.svg` | 80 | 75.58 |
| `figures/_shared/icons/ic-fractal.svg` | 80 | 74.09 |

The distributed icon is the selected row 3 / variation 2 from the fill studies: six small filled hexagons with medium connectors. The fractal is the selected option 4 from the fork/weight studies (3-2-3, lengths 10/7/12, uniform source stroke 2.8). Its proportional enlargement also scales the stroke; it remains uniform. Other icons likewise retain their proportional stroke weights.

The final set is documented in `figures/_shared/icons/FINAL_ICONS.md`, with a stable comparison preview at `figures/_shared/icons/final-icons.png`. The generator now builds the final distributed geometry explicitly rather than restoring the earlier hollow design.

Existing `ic-sanskrit-sun.svg`, `ic-calibration.svg`, and `ic-fractal-lotus.svg` are untouched. No cover has been replaced. Individual PNG previews are in `normalized-icons/`.

Regenerate with `python3 build_normalized_icons.py`. The script measures actual artwork bounds using Inkscape and checks equal widths, centring, and canvas fit.

## Distributed Fill Studies

[Four-row comparison](distributed-fill-studies/distributed-fill-comparison.png) shows the current normalized set followed by three changes to the Distributed column only. The other three icons are reused unchanged.

The new designs reduce the hexagon radius from 9 to 7 source units and outline width from 3 to 2. Rows 2-4 now all use the same six filled hexagons. Only connector widths vary: 1.4 units (variation 1), 2.3 units (variation 2), and 3.2 units (variation 3), before uniform normalization to an 80-unit visible width. Row 3 / variation 2 was selected and promoted to the final shared set; the existing comparison PNG retains the earlier hollow reference row.

Regenerate with `python3 build_distributed_studies.py`.

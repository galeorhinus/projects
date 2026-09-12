# Eclipse SVG PDF Rendering Correction

Date: 2026-09-12

## Defect

After the move from PNG derivatives to SVGs, rsvg-convert's PDF output displaced
some disconnected strokes in the Sun's rays. Its direct PNG rendering retained
the correct geometry. Successful XML validation and conversion therefore missed
a visible production defect.

## Correction

`figures/eclipse_spine/normalize_pdf_paths.py` parses the path geometry and emits
each disconnected stroke as a separate path. A containing group retains the
original stroke properties, opacity, transforms, and filters. It produces
`.from-ai-cdx.svg` variants and promotes them to the canonical SVGs. The original
`.from-ai.svg` designs remain available for editing and comparison.

Eleven figures required this correction. The pyramid-only Chapter 1 figure has
no affected compound strokes. The epilogue's compound crack paths received the
same correction as the rays.

The book continues to use SVG artwork through its existing PDF conversion.
An attempted Inkscape PDF export was rejected during comparison because it
changed the globe's shadow masks in the later stages of the sequence.

## Verification

The following was the initial check, not sufficient cross-renderer verification.
The user subsequently reported an opaque band over the globe in E.7. The final
print correction is recorded below.

- Compared all twelve original SVG raster renders against the corrected vector
  PDFs, rasterized through Poppler on a white background.
- Inspected rays, block states, cracks, conch, globe outlines, and the progressive
  shadow-to-light transition. Filter rasterization still produces minor texture
  differences; the displaced geometry is corrected.
- Verified all eleven changed production variants through the existing lineage
  helper. The unchanged pyramid-only figure was checked visually.
- Rebuilt the A5 short-note book: 662 pages. Inspected all twelve deployed figures
  on physical PDF pages 38, 41, 44, 64, 78, 140, 165, 233, 289, 360, 430, and 450.

The comparison images and numerical results are under
`tmp/pdfs/eclipse-audit/`. The book PDF is
`build/atomic_sanskrit.a5.short.pdf`.

## Final Print Correction

The PDF output still depended on the reader's handling of gradient transparency
and soft masks. A successful Poppler render did not establish reliable output
in other readers. E.7's light band could become a solid rectangle hiding the map.

`build_book.py` now generates opaque RGB PNGs from current canonical eclipse
SVGs before PDF embedding. This exception covers all twelve figures in the
sequence. Each image is 4,200 pixels wide, providing 600 dpi at 7 inches and
more at A5 size. rsvg renders the lighting onto a white background, so the
embedded image needs no PDF transparency mask. Other SVG figures remain vector.

The generated images live under `build/figure-rasters/`. Their filenames include
a hash of the SVG content and rendering recipe. Updating the SVG triggers a new
image; no archived raster can silently override the source. Manuscript prose,
captions, figure sizes, and editable SVG artwork are unchanged in this follow-up.

Four automated tests cover source-change cache invalidation, preservation of
captions and attributes, restriction to the eclipse directory, and failure
handling. All twelve generated images were checked as opaque RGB at 4,200 px.

Final verification completed:

- Reproduced the old solid-band defect with Apple's PDF renderer (`sips`).
- Rebuilt the book: 662 pages; all twelve figures remain on the pages listed
  above. Each is embedded at approximately 904 dpi in the A5 layout.
- Extracted every eclipse image from the final PDF and confirmed exact RGB
  pixel equality with its flattened source and no PDF soft mask.
- Rendered all twelve deployed figure pages using both MuPDF and Apple's
  renderer. Checked E.7 at enlarged size and inspected the complete sequence.
- Four unit tests pass; `git diff --check` passes.

Evidence: `tmp/pdfs/eclipse-flat-audit/results.json`, `all-12-apple.png`, and
`E7-book.png`. A distinctly named copy is available at
`output/pdf/atomic_sanskrit.a5.short.eclipse-fixed.pdf` to avoid confusion with
an already-open earlier PDF. The standard build output is also updated.

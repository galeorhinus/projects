#!/bin/bash

# ==============================================================================
# Build Script for Atomic Sanskrit Paper
# ==============================================================================

# 1. Path setup (Adding the internal Inkscape binary path)
export PATH="/Library/TeX/texbin:/usr/local/bin:/opt/homebrew/bin:/Applications/Inkscape.app/Contents/MacOS:$PATH"

# 2. Configuration
INPUT="atomicSanskrit.md"
OUTPUT="atomicSanskrit.pdf"
SVG_DIR="./svg"

# 3. Pre-convert SVGs using Inkscape's internal CLI
echo "Converting SVGs in $SVG_DIR using Inkscape (Flattening Text to Paths)..."
for svg in "$SVG_DIR"/*.svg; do
    if [ -f "$svg" ]; then
        echo "Processing $svg..."
        # This is the "Nuclear Option" - it turns text into vector shapes
        inkscape "$svg" --export-type=pdf --export-text-to-path -o "${svg%.svg}.pdf"
    fi
done

# 4. Run Pandoc
# Setting Arial Unicode MS for Devanagari support
echo "Generating final 6x9 PDF with Arial Unicode MS..."

pandoc "$INPUT" \
  --pdf-engine=xelatex \
  --embed-resources \
  --standalone \
  -V geometry:"paperwidth=6in,paperheight=9in,top=0.75in,left=1in,right=0.75in,bottom=1in" \
  -V mainfont="Arial Unicode MS" \
  -V mainfontoptions="Renderer=HarfBuzz" \
  -o "$OUTPUT"

if [ $? -eq 0 ]; then
    echo "Success! Opening $OUTPUT..."
    open "$OUTPUT"
else
    echo "Build failed. Check for LaTeX errors above."
fi
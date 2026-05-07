#!/bin/bash

# ==============================================================================
# Build Script for Atomic Sanskrit Paper
# ==============================================================================

# 1. Path setup (Adding the internal Inkscape binary path)
export PATH="/Library/TeX/texbin:/usr/local/bin:/opt/homebrew/bin:/Applications/Inkscape.app/Contents/MacOS:$PATH"

# 2. Configuration
INPUT="AtomicSanskritTOC.md"
OUTPUT="AtomicSanskritTOC.pdf"

# 4. Run Pandoc
# Setting Arial Unicode MS for Devanagari support
echo "Generating final 6x9 PDF with Arial Unicode MS..."

pandoc "$INPUT" \
  --pdf-engine=xelatex \
  --embed-resources \
  --standalone \
  -V geometry:"paperwidth=3in,paperheight=6in,top=0.1in,left=0.1in,right=0.1in,bottom=0.1in" \
  -V mainfont="Arial Unicode MS" \
  -V mainfontoptions="Renderer=HarfBuzz" \
  -o "$OUTPUT"

if [ $? -eq 0 ]; then
    echo "Success! Opening $OUTPUT..."
    open "$OUTPUT"
else
    echo "Build failed. Check for LaTeX errors above."
fi
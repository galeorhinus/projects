#!/bin/bash

# ==============================================================================
# Build Script for Atomic Sanskrit Paper
# ==============================================================================

# 1. Path setup (Adding the internal Inkscape binary path)
export PATH="/Library/TeX/texbin:/usr/local/bin:/opt/homebrew/bin:/Applications/Inkscape.app/Contents/MacOS:$PATH"

# 2. Configuration
INPUT="as_toc_share.md"
OUTPUT="as_toc_share.pdf"

# 4. Run Pandoc
# Setting Arial Unicode MS for Devanagari support
echo "Generating final 3x6 PDF..."

pandoc "$INPUT" \
  --pdf-engine=xelatex \
  --embed-resources \
  --standalone \
  -V geometry:"paperwidth=3in,paperheight=6in,top=0.1in,left=0.1in,right=0.1in,bottom=0.1in" \
  -V mainfont="Shobhika" \
  -V mainfontoptions="Renderer=HarfBuzz,Script=Devanagari,Language=Sanskrit" \
  -o "$OUTPUT"

if [ $? -eq 0 ]; then
    echo "Success! Opening $OUTPUT..."
    open "$OUTPUT"
else
    echo "Build failed. Check for LaTeX errors above."
fi
#!/usr/bin/env bash
set -euo pipefail

LAYOUT_JSON=${1:-/Users/paragtope/projects/epaper-lab/projects/clock75/ui/layout.json}
FRAME_JSON=${2:-/Users/paragtope/projects/epaper-lab/projects/clock75/ui/frame.json}
SVG_PATH=/Users/paragtope/projects/epaper-lab/projects/clock75/ui/mockups/clock75_layout_generated.svg
OUT_PATH=${3:-/Users/paragtope/projects/epaper-lab/projects/clock75/ui/mockups/clock75_layout_1bit.png}
GRAY_PATH=${OUT_PATH%.png}_gray.png
NIGHT_SVG=${OUT_PATH%.png}_night.svg
NIGHT_MASK=${OUT_PATH%.png}_night_mask.png
NIGHT_WHITE=${OUT_PATH%.png}_night_white.png
SCALE=2
W=800
H=480

# Render SVG to exact 800x480, 1-bit, no AA
 /Users/paragtope/projects/epaper-lab/projects/clock75/ui/tools/render_layout_svg.py \
  "$LAYOUT_JSON" "$SVG_PATH" --frame "$FRAME_JSON"

/usr/local/bin/magick \
  -define svg:antialias=false \
  -define svg:width=$((W*SCALE)) -define svg:height=$((H*SCALE)) \
  "$SVG_PATH" \
  -background white -alpha remove -alpha off \
  -colorspace Gray -depth 8 \
  -resize ${W}x${H}! -filter point -interpolate nearest \
  "$GRAY_PATH"

/usr/local/bin/magick \
  "$GRAY_PATH" \
  -dither none -threshold 50% \
  -type bilevel -depth 1 \
  -define png:color-type=0 -define png:bit-depth=1 \
  "$OUT_PATH"

# Build a night-only SVG layer and composite white strokes after thresholding
/Users/paragtope/projects/epaper-lab/projects/clock75/ui/tools/extract_night_layer.py \
  "$SVG_PATH" "$NIGHT_SVG"

/usr/local/bin/magick \
  -define svg:antialias=false \
  -define svg:width=$((W*SCALE)) -define svg:height=$((H*SCALE)) \
  "$NIGHT_SVG" \
  -background white -alpha remove -alpha off \
  -colorspace Gray -depth 8 \
  -resize ${W}x${H}! -filter point -interpolate nearest \
  -dither none -threshold 50% \
  -type bilevel -depth 1 \
  "$NIGHT_MASK"

/usr/local/bin/magick \
  "$NIGHT_MASK" -negate \
  "$NIGHT_WHITE"

/usr/local/bin/magick \
  "$OUT_PATH" "$NIGHT_WHITE" -compose lighten -composite \
  "$OUT_PATH"

printf "Wrote %s\n" "$GRAY_PATH"
printf "Wrote %s\n" "$OUT_PATH"

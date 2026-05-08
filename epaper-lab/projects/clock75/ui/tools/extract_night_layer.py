#!/usr/bin/env python3
from pathlib import Path
import re
import sys

if len(sys.argv) < 3:
    raise SystemExit("usage: extract_night_layer.py <in.svg> <out.svg>")

in_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])
text = in_path.read_text()

# Keep header up to </defs> if present
header = ""
body = text
m = re.search(r'(.*?</defs>\s*)', text, flags=re.S)
if m:
    header = m.group(1)
    body = text[m.end():]
else:
    # keep opening <svg ...> tag if no defs
    m2 = re.search(r'(<svg[^>]*>\s*)', text, flags=re.S)
    if m2:
        header = m2.group(1)
        body = text[m2.end():]

# Extract elements that should be white in night region
lines = []
for line in body.splitlines():
    if '<line' in line:
        if 'stroke="#fff"' in line or 'class="divider-inv"' in line or 'class="xaxis-inv"' in line:
            lines.append(line)
    elif '<text' in line:
        if 'class="label-inv"' in line:
            lines.append(line)

# Close svg
footer = "\n</svg>\n"

out_path.write_text(header + "\n" + "\n".join(lines) + footer)

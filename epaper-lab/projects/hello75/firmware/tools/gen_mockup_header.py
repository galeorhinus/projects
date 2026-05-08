#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess


def read_pbm(raw: bytes):
    if not raw.startswith(b"P4"):
        raise ValueError("Not a binary PBM (P4)")
    idx = 2
    tokens = []
    while len(tokens) < 2:
        while idx < len(raw) and raw[idx] in b" \t\r\n":
            idx += 1
        if idx >= len(raw):
            break
        if raw[idx] == ord("#"):
            while idx < len(raw) and raw[idx] != ord("\n"):
                idx += 1
            continue
        start = idx
        while idx < len(raw) and raw[idx] not in b" \t\r\n":
            idx += 1
        tokens.append(raw[start:idx])
    if len(tokens) < 2:
        raise ValueError("PBM missing width/height")
    width = int(tokens[0])
    height = int(tokens[1])
    while idx < len(raw) and raw[idx] in b" \t\r\n":
        idx += 1
    data = raw[idx:]
    expected = ((width + 7) // 8) * height
    if len(data) < expected:
        raise ValueError(f"PBM data too short: {len(data)} < {expected}")
    return width, height, data[:expected]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_png")
    ap.add_argument("output_h")
    ap.add_argument("--magick", default="/usr/local/bin/magick")
    args = ap.parse_args()

    cmd = [
        args.magick,
        args.input_png,
        "-resize",
        "800x480!",
        "-threshold",
        "50%",
        "-type",
        "bilevel",
        "pbm:-",
    ]
    result = subprocess.run(cmd, check=True, capture_output=True)
    width, height, data = read_pbm(result.stdout)

    out = []
    out.append("#pragma once")
    out.append("")
    out.append(f"#define CLOCK75_MOCKUP_WIDTH {width}")
    out.append(f"#define CLOCK75_MOCKUP_HEIGHT {height}")
    out.append(f"#define CLOCK75_MOCKUP_LEN {len(data)}")
    out.append("")
    out.append("static const unsigned char CLOCK75_MOCKUP_DATA[CLOCK75_MOCKUP_LEN] = {")
    line = "    "
    for i, b in enumerate(data):
        chunk = f"0x{b:02x}, "
        if len(line) + len(chunk) > 100:
            out.append(line.rstrip())
            line = "    "
        line += chunk
    if line.strip():
        out.append(line.rstrip())
    out.append("};")
    out.append("")

    with open(args.output_h, "w", encoding="utf-8") as f:
        f.write("\n".join(out))


if __name__ == "__main__":
    main()

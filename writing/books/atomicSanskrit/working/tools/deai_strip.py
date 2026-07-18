#!/usr/bin/env python3
"""Strip AISWEEP-OLD redline blocks from a de-AI'd manuscript file.

During a de-AI pass, each changed paragraph keeps its original wrapped as:

    <!-- AISWEEP-OLD
    {verbatim original paragraph(s)}
    AISWEEP-END -->
    {new paragraph(s)}

The wrapper is an HTML comment, so it never renders in a build and shows
greyed-out in the editor — the original sits visibly above the rewrite for
review. Once the author has approved, run this to drop every OLD block,
leaving only the new text. Idempotent; safe to re-run.

Usage:
    python3 working/tools/deai_strip.py FILE [FILE ...]      # strip in place
    python3 working/tools/deai_strip.py --check FILE [...]   # count blocks, no write
"""
import sys

OPEN = "<!-- AISWEEP-OLD"
CLOSE = "AISWEEP-END -->"


def strip_lines(lines):
    out, removed, i, n = [], 0, 0, len(lines)
    while i < n:
        if lines[i].lstrip().startswith(OPEN):
            j = i
            while j < n and CLOSE not in lines[j]:
                j += 1
            removed += 1
            i = j + 1  # skip the closing marker line too
            continue
        out.append(lines[i])
        i += 1
    return out, removed


def count_blocks(lines):
    return sum(1 for ln in lines if ln.lstrip().startswith(OPEN))


def main(argv):
    check = "--check" in argv
    files = [a for a in argv if a != "--check"]
    if not files:
        print(__doc__)
        return 1
    for path in files:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        if check:
            print(f"{count_blocks(lines):4d} AISWEEP-OLD blocks  {path}")
            # integrity guards: a sweep that wraps a mid-paragraph substring leaves
            # the opener mid-line, where strip_lines can't see it. Flag it.
            malformed = [i + 1 for i, ln in enumerate(lines)
                         if OPEN in ln and not ln.lstrip().startswith(OPEN)]
            opens = sum(1 for ln in lines if OPEN in ln)
            closes = sum(1 for ln in lines if CLOSE in ln)
            if malformed:
                print(f"     !! {len(malformed)} MID-LINE opener(s) at line(s) {malformed} "
                      f"— rewrap the whole paragraph")
            if opens != closes:
                print(f"     !! marker imbalance: {opens} open vs {closes} close")
            continue
        new_lines, removed = strip_lines(lines)
        if removed:
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
        print(f"stripped {removed:4d} blocks  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Southern Survey — Sanskrit base vs Tamil + Toda + Kurukh.

Quad-overlay matrix.  Sanskrit (with the mahāprāṇa rows held aside)
sits as the tinted base shell with its Devanāgarī letters; Tamil,
Toda, and Kurukh overlay the other three corners.  The figure
self-titles "Southern Survey: 22 of 23 Sanskrit Base Cells" with
the remaining unfilled letter (श) named in the subtitle.

Shared renderer:  _shared/toolkits/vocal_tract/quad_overlay.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _shared.toolkits.vocal_tract.quad_overlay import (
    QuadOverlaySpec, build_and_write,
)


SPEC = QuadOverlaySpec(
    set_name="Southern Survey",
    languages=[
        ("sanskrit", "Sanskrit", "tl"),
        ("tamil",    "Tamil",    "tr"),
        ("toda",     "Toda",     "bl"),
        ("kurukh",   "Kurukh",   "br"),
    ],
    # Editorial trim: drop PA (col 5) — only Toda lights it, with a
    # single ʃ cell, not enough payload to justify a column.
    selected_places=[0, 3, 4, 6, 7, 8, 11],
)


def main() -> int:
    out = Path(__file__).resolve().parent / "sk_tamil_toda_kurukh.from-py.svg"
    return build_and_write(SPEC, out)


if __name__ == "__main__":
    sys.exit(main())

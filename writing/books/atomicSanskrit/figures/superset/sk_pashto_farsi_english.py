#!/usr/bin/env python3
"""External IE Control — Sanskrit base vs Pashto + Farsi + English.

Quad-overlay matrix.  One north-western / Central-Asian-corridor
Indo-Iranian language (Pashto), one West-Asian Iranian language
(Farsi), and one European language (English).  This is the clean
body-text external comparison: all three are orthodoxy-classified as
Indo-European, while Arabic is kept for the appendix-level sound /
script / standard comparison.

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
    set_name="External IE Control",
    languages=[
        ("sanskrit", "Sanskrit", "tl"),
        ("pashto",   "Pashto",   "tr"),
        ("farsi",    "Farsi",    "bl"),
        ("english",  "English",  "br"),
    ],
    selected_places=None,
)


def main() -> int:
    out = Path(__file__).resolve().parent / "sk_pashto_farsi_english.from-py.svg"
    return build_and_write(SPEC, out)


if __name__ == "__main__":
    sys.exit(main())

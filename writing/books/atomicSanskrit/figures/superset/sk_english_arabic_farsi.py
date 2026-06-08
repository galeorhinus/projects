#!/usr/bin/env python3
"""External Comparison — Sanskrit base vs English + Arabic + Farsi.

Quad-overlay matrix.  Replaces the three subcontinental partners with
three non-subcontinental contact-zone languages.  The polemic point is
the inverse of the southern / Munda / mixed surveys: subcontinental
language sets cover the Sanskrit base because Sanskrit's selection
came from the subcontinental field; external sets do not, because
they were selecting from different fields.

Note: the canvas runs wider than the other three surveys because
English, Arabic, and Farsi collectively light labio-dental and
pharyngeal columns that no subcontinental survey reaches.

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
    set_name="External Comparison",
    languages=[
        ("sanskrit", "Sanskrit", "tl"),
        ("english",  "English",  "tr"),
        ("arabic",   "Arabic",   "bl"),
        ("farsi",    "Farsi",    "br"),
    ],
    selected_places=None,
)


def main() -> int:
    out = Path(__file__).resolve().parent / "sk_english_arabic_farsi.from-py.svg"
    return build_and_write(SPEC, out)


if __name__ == "__main__":
    sys.exit(main())

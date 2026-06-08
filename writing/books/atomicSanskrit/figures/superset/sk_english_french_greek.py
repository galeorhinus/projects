#!/usr/bin/env python3
"""Western IE Survey — Sanskrit base vs English + French + Greek.

Quad-overlay matrix.  Three major Western European languages, all
orthodoxy-classified as "Indo-European": English (Germanic), French
(Romance / Italic), Greek (its own branch, the IE founder-text of
the Schleicher reconstruction).  The figure asks how much of
Sanskrit's base this Western IE set covers — the inverse polemic of
the southern subcontinental surveys.

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
    set_name="Western IE Survey",
    languages=[
        ("sanskrit", "Sanskrit", "tl"),
        ("english",  "English",  "tr"),
        ("french",   "French",   "bl"),
        ("greek",    "Greek",    "br"),
    ],
    selected_places=None,
)


def main() -> int:
    out = Path(__file__).resolve().parent / "sk_english_french_greek.from-py.svg"
    return build_and_write(SPEC, out)


if __name__ == "__main__":
    sys.exit(main())

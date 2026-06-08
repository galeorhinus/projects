#!/usr/bin/env python3
"""Iranian Survey — Sanskrit base vs Farsi + Kurdish + Balochi.

Quad-overlay matrix.  Three Iranian languages spanning the
Persianate sphere: Farsi (Iran), Kurdish (Kurmanji — northern Iraq /
Syria / Turkey), and Balochi (south-western Pakistan / south-eastern
Iran).  All three are orthodoxy-classified as Sanskrit's "Iranian
sister branch" cousins.  The figure asks how much of Sanskrit's base
this Iranian cluster covers.

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
    set_name="Iranian Survey",
    languages=[
        ("sanskrit", "Sanskrit", "tl"),
        ("farsi",    "Farsi",    "tr"),
        ("kurdish",  "Kurdish",  "bl"),
        ("balochi",  "Balochi",  "br"),
    ],
    selected_places=None,
)


def main() -> int:
    out = Path(__file__).resolve().parent / "sk_farsi_kurdish_balochi.from-py.svg"
    return build_and_write(SPEC, out)


if __name__ == "__main__":
    sys.exit(main())

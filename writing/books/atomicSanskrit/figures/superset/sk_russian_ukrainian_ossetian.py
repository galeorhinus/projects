#!/usr/bin/env python3
"""Slavic & Caucasus IE Survey — Sanskrit base vs Russian + Ukrainian + Ossetian.

Quad-overlay matrix.  Two East Slavic languages and one Caucasian
Iranian language — all classified by the orthodoxy as "Indo-
European" relatives of Sanskrit.  The figure asks how much of
Sanskrit's base coordinates this Eastern European / Caucasus
cluster covers.

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
    set_name="Slavic & Caucasus IE Survey",
    languages=[
        ("sanskrit",  "Sanskrit",  "tl"),
        ("russian",   "Russian",   "tr"),
        ("ukrainian", "Ukrainian", "bl"),
        ("ossetian",  "Ossetian",  "br"),
    ],
    selected_places=None,
)


def main() -> int:
    out = Path(__file__).resolve().parent / "sk_russian_ukrainian_ossetian.from-py.svg"
    return build_and_write(SPEC, out)


if __name__ == "__main__":
    sys.exit(main())

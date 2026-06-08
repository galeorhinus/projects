#!/usr/bin/env python3
"""Caucasus Survey — Sanskrit base vs Armenian + Georgian + Ossetian.

Quad-overlay matrix.  Three Caucasus-region languages from three
different orthodox classifications: Armenian (its own IE branch),
Georgian (Kartvelian / South Caucasian — NOT IE), Ossetian (Iranian).
The mixed taxonomic origins make this a useful test of whether the
Caucasus AREA predicts shared sound-field structure when the family-
tree label doesn't.

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
    set_name="Caucasus Survey",
    languages=[
        ("sanskrit", "Sanskrit", "tl"),
        ("armenian", "Armenian", "tr"),
        ("georgian", "Georgian", "bl"),
        ("ossetian", "Ossetian", "br"),
    ],
    selected_places=None,
)


def main() -> int:
    out = Path(__file__).resolve().parent / "sk_armenian_georgian_ossetian.from-py.svg"
    return build_and_write(SPEC, out)


if __name__ == "__main__":
    sys.exit(main())

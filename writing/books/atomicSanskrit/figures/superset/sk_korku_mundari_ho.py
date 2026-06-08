#!/usr/bin/env python3
"""Forest-Belt Survey — Sanskrit base vs Korku + Mundari + Ho.

Quad-overlay matrix.  Three central-forest-belt languages from the
North Munda cluster: Korku (west-central, Madhya Pradesh /
Maharashtra), Mundari (eastern, Chotanagpur plateau), Ho (eastern,
Chotanagpur plateau and Singhbhum).  Santali is held aside in this
figure — Santali carries the heaviest Indic absorption in the
Kherwarian sub-cluster, and excluding it sharpens the test of how
much of Sanskrit's base the unabsorbed forest-belt inventories cover.

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
    set_name="Forest-Belt Survey",
    languages=[
        ("sanskrit", "Sanskrit", "tl"),
        ("korku",    "Korku",    "tr"),
        ("mundari",  "Mundari",  "bl"),
        ("ho",       "Ho",       "br"),
    ],
    selected_places=None,
)


def main() -> int:
    out = Path(__file__).resolve().parent / "sk_korku_mundari_ho.from-py.svg"
    return build_and_write(SPEC, out)


if __name__ == "__main__":
    sys.exit(main())

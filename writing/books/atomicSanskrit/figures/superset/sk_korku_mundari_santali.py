#!/usr/bin/env python3
"""Munda Survey — Sanskrit base vs Korku + Mundari + Santali.

Quad-overlay matrix.  Sanskrit (with the mahāprāṇa rows held aside)
sits as the tinted base shell with its Devanāgarī letters; the three
Chotanagpur-and-surrounding-belt languages overlay the other three
corners.

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
    set_name="Munda Survey",
    languages=[
        ("sanskrit", "Sanskrit", "tl"),
        ("korku",    "Korku",    "tr"),
        ("mundari",  "Mundari",  "bl"),
        ("santali",  "Santali",  "br"),
    ],
    # Auto-detect columns from the data union.
    selected_places=None,
)


def main() -> int:
    out = Path(__file__).resolve().parent / "sk_korku_mundari_santali.from-py.svg"
    return build_and_write(SPEC, out)


if __name__ == "__main__":
    sys.exit(main())

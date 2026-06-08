#!/usr/bin/env python3
"""Mixed Control (Santali-free) — Sanskrit base vs Korku + Mundari + Burushaski.

Quad-overlay matrix.  Replaces Santali (whose orthodoxy-classification
is sometimes contested as a borrowing-heavy edge case) with the
Burushaski isolate from the north-western subcontinent — a control
that mixes two Munda-family languages with one non-Munda non-"Indo-
Aryan" subcontinental isolate.

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
    set_name="Mixed Control",
    languages=[
        ("sanskrit",   "Sanskrit",   "tl"),
        ("korku",      "Korku",      "tr"),
        ("mundari",    "Mundari",    "bl"),
        ("burushaski", "Burushaski", "br"),
    ],
    selected_places=None,
)


def main() -> int:
    out = Path(__file__).resolve().parent / "sk_korku_mundari_burushaski.from-py.svg"
    return build_and_write(SPEC, out)


if __name__ == "__main__":
    sys.exit(main())

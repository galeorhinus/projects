#!/usr/bin/env python3
"""Northwest Frontier Survey — Sanskrit base vs Pashto + Nuristani + Burushaski.

Quad-overlay matrix.  Three languages of the north-western frontier
of the subcontinent: Pashto (Iranian, with the full retroflex set),
Nuristani (its own IE branch, with partial retroflex), and Burushaski
(isolate, no genetic affiliation per the orthodoxy).  All three sit
adjacent to or inside the historical subcontinental retroflex zone.
The figure tests how much of Sanskrit's base the frontier-contact
inventories cover.

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
    set_name="Northwest Frontier Survey",
    languages=[
        ("sanskrit",   "Sanskrit",   "tl"),
        ("pashto",     "Pashto",     "tr"),
        ("nuristani",  "Nuristani",  "bl"),
        ("burushaski", "Burushaski", "br"),
    ],
    selected_places=None,
)


def main() -> int:
    out = Path(__file__).resolve().parent / "sk_pashto_nuristani_burushaski.from-py.svg"
    return build_and_write(SPEC, out)


if __name__ == "__main__":
    sys.exit(main())

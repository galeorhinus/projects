#!/usr/bin/env python3
"""Central Asian Survey — Sanskrit base vs Tajik + Kazakh + Kyrgyz.

Quad-overlay matrix.  One Iranian (Tajik) and two Turkic (Kazakh,
Kyrgyz) languages of Central Asia.  Tajik is the orthodoxy's "Indo-
European" relative; Kazakh and Kyrgyz are NOT — Turkic is a separate
family.  The figure asks whether geographic adjacency to the
subcontinent (across the Pamirs / Hindu Kush) predicts coverage when
language-family classification doesn't.

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
    set_name="Central Asian Survey",
    languages=[
        ("sanskrit", "Sanskrit", "tl"),
        ("tajik",    "Tajik",    "tr"),
        ("kazakh",   "Kazakh",   "bl"),
        ("kyrgyz",   "Kyrgyz",   "br"),
    ],
    selected_places=None,
)


def main() -> int:
    out = Path(__file__).resolve().parent / "sk_tajik_kazakh_kyrgyz.from-py.svg"
    return build_and_write(SPEC, out)


if __name__ == "__main__":
    sys.exit(main())

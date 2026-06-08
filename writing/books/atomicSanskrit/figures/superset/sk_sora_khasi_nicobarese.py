#!/usr/bin/env python3
"""Dispersed Survey — Sanskrit base vs Sora + Khasi + Nicobarese.

Quad-overlay matrix.  The three other languages here are all
orthodoxy-classified into the same 'Austro-Asiatic' family, but they
sit at three geographically and structurally remote poles of the
subcontinent:

  - Sora        — Eastern Ghats and Rushikulya basin (Odisha / AP)
  - Khasi       — Meghalaya highlands (northeastern hills)
  - Nicobarese  — Car Nicobar (southeastern Indian Ocean islands)

The figure tests whether the orthodoxy's single family label predicts
shared sound-field structure across that geographic spread.  Khasi's
voiceless-aspirated stop row, Sora's missing retroflex column, and
Nicobarese's lighter inventory together show three different
templates inside the same orthodox 'family'.

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
    set_name="Dispersed Survey",
    languages=[
        ("sanskrit",   "Sanskrit",   "tl"),
        ("sora",       "Sora",       "tr"),
        ("khasi",      "Khasi",      "bl"),
        ("nicobarese", "Nicobarese", "br"),
    ],
    selected_places=None,
)


def main() -> int:
    out = Path(__file__).resolve().parent / "sk_sora_khasi_nicobarese.from-py.svg"
    return build_and_write(SPEC, out)


if __name__ == "__main__":
    sys.exit(main())

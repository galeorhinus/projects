"""Vocal-tract figure toolkit — shared across Ch 7 / 8 / 9 / App 3.

Modules:
  schematics — shape primitives (point_at, build_ribbon_path_d, …)
  regions    — JSON-driven vocal-tract region atlas
  scatter    — JSON-driven scatter overlay on a vocal-tract ribbon
  overlay    — two-language consonant inventory overlay + similarity metrics

Data:
  CONFIGS_DIR — Path to configs/ directory holding the per-language
                scatter_<lang>.json input files.

Usage from a chapter script:

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from _shared.toolkits.vocal_tract.schematics import point_at
    from _shared.toolkits.vocal_tract import CONFIGS_DIR
"""

from pathlib import Path

CONFIGS_DIR = Path(__file__).resolve().parent / "configs"

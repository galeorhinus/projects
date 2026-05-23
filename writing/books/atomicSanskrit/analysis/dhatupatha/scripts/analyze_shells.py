#!/usr/bin/env python3
"""
analyze_shells.py — Shell-distribution analysis of the Pāṇinian Dhātupāṭha.

Extends the C / V skeleton with the V1 / V2 (short / long) vowel distinction
to produce the finer-grained classification — the dhātu-ākṛti shell catalog
documented in `working/dhatu_hexagons/SHELLS.md`.

For each of the ~2,168 dhātus in data/dhatupatha.csv:
  1. Strip Pāṇinian anubandhas per Aṣṭādhyāyī 1.3.2 / 1.3.3 / 1.3.5
  2. Classify each varṇa as C, V1 (hrasva), or V2 (dīrgha)
  3. Build the shell label by concatenating per-varṇa classifications
  4. Tally counts per shell, with exemplars and per-gaṇa breakdown

Outputs:
  data/derived/shell_distribution.csv — one row per shell, with count,
    cumulative percentage, and top exemplars
  data/derived/shell_distribution.md  — human-readable summary
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

# Reuse parsing logic from decompose_dhatupatha.py
sys.path.insert(0, str(Path(__file__).parent))
from decompose_dhatupatha import (  # noqa: E402
    strip_markers, strip_anubandhas, slp1_to_devanagari,
    VOWELS, CONSONANTS, GANA_NAMES,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = REPO_ROOT / "data" / "dhatupatha.csv"
CSV_OUT = REPO_ROOT / "data" / "derived" / "shell_distribution.csv"
MD_OUT = REPO_ROOT / "data" / "derived" / "shell_distribution.md"

# Short vowels: a i u f (ṛ) x (ḷ)
SHORT_VOWELS = set("aiufx")
# Long vowels and diphthongs: A I U F X e E o O — all dīrgha per Pāṇinian
# convention (the diphthongs e/ai/o/au are 2-mātrā in the duration framework).
LONG_VOWELS = set("AIUFXeEoO")


def classify_shell(s: str) -> str:
    """Return a V1/V2-aware shell pattern (string of C, V1, V2 tokens)."""
    parts = []
    for c in s:
        if c in SHORT_VOWELS:
            parts.append("V1")
        elif c in LONG_VOWELS:
            parts.append("V2")
        elif c in CONSONANTS:
            parts.append("C")
    return "".join(parts)


def count_particles(shell: str) -> int:
    """Count particles in a shell pattern (each C, V1, V2 is one particle)."""
    # V1 / V2 are 2-char tokens; C is 1-char
    return shell.replace("V1", "V").replace("V2", "V").count("V") + shell.count("C")


def main() -> int:
    if not DATA_FILE.exists():
        print(f"ERROR: data file not found at {DATA_FILE}", file=sys.stderr)
        return 1

    # tally: shell -> list of (dev_full, slp1_structural, gana)
    tally = defaultdict(list)
    # gana -> shell -> count
    by_gana = defaultdict(lambda: defaultdict(int))
    total = 0

    with DATA_FILE.open() as fh:
        for row in csv.reader(fh):
            if len(row) < 3 or not row[0].isdigit():
                continue
            gana = int(row[0])
            original = row[2].strip()

            stripped_markers = strip_markers(original)
            structural = strip_anubandhas(stripped_markers)
            if not structural:
                continue

            shell = classify_shell(structural)
            if not shell:
                continue
            dev_full = slp1_to_devanagari(structural)
            tally[shell].append((dev_full, structural, gana))
            by_gana[gana][shell] += 1
            total += 1

    # Sort shells by count descending
    sorted_shells = sorted(tally.items(), key=lambda x: -len(x[1]))

    # Compute cumulative percentages and assemble rows
    rows = []
    cumulative_count = 0
    for shell, entries in sorted_shells:
        count = len(entries)
        pct = 100 * count / total
        cumulative_count += count
        cum_pct = 100 * cumulative_count / total
        # Top exemplars — deduplicate (a few SLP1 forms collide on Devanagari)
        seen = set()
        unique_devs = []
        for dev, _slp1, _gana in entries:
            if dev not in seen:
                unique_devs.append(dev)
                seen.add(dev)
            if len(unique_devs) >= 5:
                break
        top_str = ", ".join(unique_devs)
        rows.append((shell, count, pct, cum_pct, top_str, count_particles(shell)))

    # Ensure output directory
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)

    # Write CSV
    with CSV_OUT.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["rank", "shell", "particles", "count", "percentage",
                    "cumulative_pct", "top_exemplars"])
        for i, (shell, count, pct, cum_pct, top, particles) in enumerate(rows, 1):
            w.writerow([i, shell, particles, count,
                        f"{pct:.2f}", f"{cum_pct:.2f}", top])

    # Cumulative thresholds
    thresholds = [50, 75, 80, 90, 95, 99]
    threshold_results = []
    for thr in thresholds:
        for i, (shell, count, pct, cum_pct, _, _) in enumerate(rows, 1):
            if cum_pct >= thr:
                threshold_results.append((thr, i, shell, cum_pct))
                break

    # Write markdown
    with MD_OUT.open("w") as fh:
        fh.write("# Dhātu-Ākṛti Shell Distribution\n\n")
        fh.write(f"> Source: `data/dhatupatha.csv` ({total} dhātus, anubandhas "
                 "stripped per *Aṣṭādhyāyī* 1.3.2 / 1.3.3 / 1.3.5).\n>\n")
        fh.write(f"> **Total entries:** {total}  |  "
                 f"**Distinct shells:** {len(rows)}\n>\n")
        fh.write("> Generated by `scripts/analyze_shells.py`. "
                 "See `working/dhatu_hexagons/SHELLS.md` for the shell concept.\n\n")
        fh.write("---\n\n")

        # Cumulative threshold report
        fh.write("## Cumulative thresholds\n\n")
        fh.write("How many of the most common shells does it take to cover X% of the corpus?\n\n")
        fh.write("| Coverage | # of shells | Last shell added | Reached at |\n")
        fh.write("|---:|---:|---|---:|\n")
        for thr, num_shells, last_shell, reached in threshold_results:
            fh.write(f"| {thr}% | {num_shells} | **{last_shell}** | "
                     f"{reached:.2f}% |\n")

        # Overall shell distribution
        fh.write("\n---\n\n## Full shell distribution\n\n")
        fh.write("| Rank | Shell | Particles | Count | % | Cum % | Top exemplars |\n")
        fh.write("|---:|---|---:|---:|---:|---:|---|\n")
        for i, (shell, count, pct, cum_pct, top, particles) in enumerate(rows, 1):
            fh.write(f"| {i} | **{shell}** | {particles} | {count} | "
                     f"{pct:.2f} | {cum_pct:.2f} | {top} |\n")

        # Per-gana breakdown — top 5 shells per gana
        fh.write("\n---\n\n## Top shells per *gaṇa*\n\n")
        for gana in sorted(by_gana):
            shells_in_gana = by_gana[gana]
            total_gana = sum(shells_in_gana.values())
            sorted_in_gana = sorted(shells_in_gana.items(),
                                    key=lambda x: -x[1])[:7]
            fh.write(f"### Gaṇa {gana} — *{GANA_NAMES.get(gana, '')}* "
                     f"({total_gana} dhātavaḥ)\n\n")
            fh.write("| Shell | Count | % of gaṇa |\n|---|---:|---:|\n")
            for shell, count in sorted_in_gana:
                fh.write(f"| **{shell}** | {count} | "
                         f"{100*count/total_gana:.1f} |\n")
            fh.write("\n")

    print(f"Wrote {CSV_OUT}")
    print(f"Wrote {MD_OUT}")
    print(f"Total dhātus: {total}")
    print(f"Distinct shells: {len(rows)}")
    print(f"Top 10 shells: {[(r[0], r[1]) for r in rows[:10]]}")
    print("\nCumulative thresholds:")
    for thr, num_shells, last_shell, reached in threshold_results:
        print(f"  {thr:>3}% reached at {num_shells:>3} shells "
              f"(last added: {last_shell})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
cluster_by_reactivity.py — cluster the 33 consonants by empirical reactivity.

For each consonant, build a reactivity-profile feature vector from its observed
combinatorial behavior across CV / VC / CVC atoms in the Dhātupāṭha:
  - Which vowels does it pair with, and how often?
  - Which other consonants does it pair with in CVC?
  - Initial / final position preference
  - Overall productivity

Then cluster consonants by similarity in their reactivity profiles, using
greedy agglomerative clustering with cosine similarity. The question:
do the emergent clusters align with the varṇamālā (place-of-articulation
groupings), or do they reveal a different organizational principle?

Run: python3 scripts/cluster_by_reactivity.py
"""

from __future__ import annotations

import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_dhatupatha import strip_anubandhas, strip_markers, classify_phonemes  # noqa
from analyze_internal_structure import (  # noqa
    DEV, VARGAS, VARGA_DEV, ALL_CONS, VOWELS, PLACE_OF, PLACE_DEV
)

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "dhatupatha.csv"


def load_dhatus_by_pattern():
    by_pattern = defaultdict(list)
    with open(DATA_FILE) as fh:
        for line in fh:
            parts = line.strip().split(",")
            if len(parts) < 3:
                continue
            stripped = strip_anubandhas(strip_markers(parts[2]))
            pat = classify_phonemes(stripped)
            by_pattern[pat].append(stripped)
    return by_pattern


def compute_features(cv_atoms, vc_atoms, cvc_atoms):
    """Build a feature dict per consonant."""
    features = defaultdict(lambda: defaultdict(float))

    for atom in cv_atoms:
        if len(atom) != 2: continue
        c, v = atom[0], atom[1]
        features[c][f"V_{v}"] += 1
        features[c]["initial"] += 1
        features[c]["total"] += 1

    for atom in vc_atoms:
        if len(atom) != 2: continue
        v, c = atom[0], atom[1]
        features[c][f"V_{v}"] += 1
        features[c]["final"] += 1
        features[c]["total"] += 1

    for atom in cvc_atoms:
        if len(atom) != 3: continue
        c1, v, c2 = atom[0], atom[1], atom[2]
        features[c1][f"V_{v}"] += 1
        features[c1]["initial"] += 1
        features[c1]["total"] += 1
        features[c1][f"pairs_{c2}"] += 1

        features[c2][f"V_{v}"] += 1
        features[c2]["final"] += 1
        features[c2]["total"] += 1
        features[c2][f"pairs_{c1}"] += 1

    return features


def cosine(v1, v2):
    keys = set(v1) | set(v2)
    dot = sum(v1.get(k, 0) * v2.get(k, 0) for k in keys)
    n1 = math.sqrt(sum(v1.get(k, 0) ** 2 for k in keys))
    n2 = math.sqrt(sum(v2.get(k, 0) ** 2 for k in keys))
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot / (n1 * n2)


def agglomerative_cluster(consonants, features, k_target=5):
    """Greedy agglomerative clustering with average-link cosine similarity."""
    clusters = [[c] for c in consonants if features[c]["total"] > 0]

    # Precompute pairwise consonant similarities
    sim_cache = {}
    for c1 in consonants:
        for c2 in consonants:
            if c1 < c2 and features[c1]["total"] > 0 and features[c2]["total"] > 0:
                sim_cache[(c1, c2)] = cosine(features[c1], features[c2])

    def pair_sim(c1, c2):
        if c1 == c2:
            return 1.0
        key = (c1, c2) if c1 < c2 else (c2, c1)
        return sim_cache.get(key, 0.0)

    def cluster_sim(cl1, cl2):
        sims = [pair_sim(a, b) for a in cl1 for b in cl2]
        return sum(sims) / len(sims) if sims else 0.0

    while len(clusters) > k_target:
        best = (-1, None, None)
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                s = cluster_sim(clusters[i], clusters[j])
                if s > best[0]:
                    best = (s, i, j)
        _, i, j = best
        clusters[i].extend(clusters[j])
        clusters.pop(j)

    return clusters, sim_cache


def print_reactivity_profile(consonants, features):
    print(f"\n{'=' * 78}")
    print(f"REACTIVITY PROFILE PER CONSONANT")
    print(f"{'=' * 78}")
    print(f"  {'cons':4s} {'tot':>5s} {'init':>5s} {'fin':>5s} {'i/f':>6s}  top vowels (count)")
    print("  " + "-" * 76)

    rows = []
    for c in consonants:
        f = features[c]
        if f["total"] == 0:
            continue
        init = f["initial"]
        fin = f["final"]
        ratio = init / fin if fin > 0 else float("inf")
        vowel_counts = [(v, int(f[f"V_{v}"])) for v in VOWELS if f[f"V_{v}"] > 0]
        vowel_counts.sort(key=lambda x: -x[1])
        top_vs = ", ".join(f"{DEV[v]}({n})" for v, n in vowel_counts[:5])
        rows.append((c, f["total"], init, fin, ratio, top_vs))

    rows.sort(key=lambda r: -r[1])  # most productive first
    for c, tot, init, fin, ratio, top_vs in rows:
        ratio_str = f"{ratio:>5.2f}x" if ratio != float("inf") else "  inf"
        print(f"  {DEV[c]:3s}  {int(tot):>5d} {int(init):>5d} {int(fin):>5d} {ratio_str}  {top_vs}")


def print_clusters(clusters, features, label):
    print(f"\n{'=' * 78}")
    print(f"REACTIVITY CLUSTERS  ({label})")
    print(f"{'=' * 78}")
    print(f"\nGreedy agglomerative clustering with cosine similarity on")
    print(f"feature vectors (vowel preferences + position + consonant co-occurrence).")
    print()

    for idx, cluster in enumerate(clusters, 1):
        # Sort members by productivity
        members = sorted(cluster, key=lambda c: -features[c]["total"])

        # Compute the dominant varṇamālā place for the cluster
        places = Counter()
        for c in members:
            if c in PLACE_OF:
                places[PLACE_OF[c]] += 1
        dominant_place = places.most_common(1)[0] if places else ("mixed", 0)

        # Compute the dominant varga column (manner) — only for varga members
        VARGA_COL = {}  # consonant -> column index in its varga (C1..C5)
        for varga_name, varga_row in VARGAS:
            for col_idx, c in enumerate(varga_row):
                VARGA_COL[c] = col_idx
        cols = Counter()
        for c in members:
            if c in VARGA_COL:
                cols[VARGA_COL[c]] += 1
        col_names = ["C1 अल्प-अघोष", "C2 महा-अघोष", "C3 अल्प-घोष", "C4 महा-घोष", "C5 अनुनासिक"]
        dominant_col = cols.most_common(1)[0] if cols else (None, 0)

        # Membership annotation
        member_display = []
        for c in members:
            place = PLACE_DEV.get(PLACE_OF.get(c, "?"), "?")
            col_idx = VARGA_COL.get(c)
            col_label = f"C{col_idx + 1}" if col_idx is not None else "—"
            member_display.append(f"{DEV[c]}({place[:3]}/{col_label})")

        print(f"  Cluster {idx} ({len(members)} consonants):")
        print(f"    Members: {' '.join(member_display)}")
        print(f"    Dominant place: {PLACE_DEV.get(dominant_place[0], dominant_place[0])} ({dominant_place[1]}/{len(members)})")
        if dominant_col[0] is not None:
            print(f"    Dominant column: {col_names[dominant_col[0]]} ({dominant_col[1]}/{len(members)})")
        print()


def main():
    by_pattern = load_dhatus_by_pattern()
    cv = by_pattern.get("CV", [])
    vc = by_pattern.get("VC", [])
    cvc = by_pattern.get("CVC", [])

    features = compute_features(cv, vc, cvc)

    print(f"DHĀTUPĀṬHA — CONSONANTS CLUSTERED BY EMPIRICAL REACTIVITY")
    print(f"Data: {len(cv)} CV atoms, {len(vc)} VC atoms, {len(cvc)} CVC atoms")

    print_reactivity_profile(ALL_CONS, features)

    for k in (3, 5, 7):
        clusters, _ = agglomerative_cluster(ALL_CONS, features, k_target=k)
        print_clusters(clusters, features, label=f"k = {k} clusters")


if __name__ == "__main__":
    main()

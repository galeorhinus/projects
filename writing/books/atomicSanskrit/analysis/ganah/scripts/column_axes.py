#!/usr/bin/env python3
"""Path C — Phase 9: Column-axis testing.

The varṇamālā organizes consonants in a 5×5 grid (5 vargas × 5 columns)
plus the vowel array. Ch 11 of the book posits that dhātus inherit some
*column property* from the varṇamālā that conditions their valency
behavior — but the brief defers the question of *which* column-axis is
the right one. Phase 9 reports numbers under four candidate
interpretations of "column" and STOPS THERE (per the autonomous-night
brief — the user picks the winner; this script does not).

Four candidate column-axes:

  A. Inherent vowel — the root's vowel (a, ā, i, ī, u, ū, ṛ, ṝ, e, ai, o, au).
     Roots are classed by their nucleus vowel.

  B. Initial articulation place — the varga of the root's first consonant
     (kavarga, cavarga, ṭavarga, tavarga, pavarga, semivowel, sibilant,
     glottal, or "vowel-initial").

  C. Initial varga-column — the column position (C1=unvoiced unaspirate,
     C2=unvoiced aspirate, C3=voiced unaspirate, C4=voiced aspirate,
     C5=nasal) of the root's first consonant; non-varga initials grouped
     separately.

  D. Empirical bonding clusters — data-driven Jaccard-similarity clustering
     of roots on their attested preverb-sets. Reports the top-N (N=100 by
     tokens) roots' cluster structure under greedy agglomerative grouping
     at a Jaccard threshold of 0.5. The "column" here is whatever the
     valency-similarity geometry produces, with no prior phonological
     interpretation.

For each axis, report:
  - Per-bucket: count of roots, mean valency, median valency, total tokens,
    top-3 exemplars by valency.
  - A chi-square-style heterogeneity index (Σ (observed - expected)² / expected)
    to indicate how much per-column means deviate from the grand mean. Higher
    deviation = the axis splits the distribution more sharply.

Output: data/derived/column_axes.txt (the report)
        data/derived/column_axes_per_root.csv (per-root axis assignments)
"""
from __future__ import annotations
import csv
import re
from collections import defaultdict
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent.parent
ATTEST = BUNDLE / "data" / "derived" / "attestation_index.csv"
PATH_C = BUNDLE / "data" / "derived" / "path_c_valency.csv"
OUT_REPORT = BUNDLE / "data" / "derived" / "column_axes.txt"
OUT_PER_ROOT = BUNDLE / "data" / "derived" / "column_axes_per_root.csv"


# ---------- Phonological lookup tables ----------

# Vowels in the varṇamālā order; "compound" vowels (e, ai, o, au) included.
VOWELS = ["a", "ā", "i", "ī", "u", "ū", "ṛ", "ṝ", "ḷ", "ḹ", "e", "ai", "o", "au"]

# Vargas (rows). Each entry: varga_name → list of consonants in column order
# C1, C2, C3, C4, C5.
VARGAS = {
    "kavarga":   ["k", "kh", "g", "gh", "ṅ"],
    "cavarga":   ["c", "ch", "j", "jh", "ñ"],
    "ṭavarga":   ["ṭ", "ṭh", "ḍ", "ḍh", "ṇ"],
    "tavarga":   ["t", "th", "d", "dh", "n"],
    "pavarga":   ["p", "ph", "b", "bh", "m"],
}
SEMIVOWELS = ["y", "r", "l", "v"]
SIBILANTS = ["ś", "ṣ", "s"]
GLOTTAL = ["h"]

COLUMN_NAMES = ["C1 (unvoiced unaspirate)", "C2 (unvoiced aspirate)",
                "C3 (voiced unaspirate)", "C4 (voiced aspirate)",
                "C5 (nasal)"]


def first_consonant(root: str) -> str | None:
    """Return the first consonant of the root (longest-match, multi-char
    consonants like 'kh', 'bh' captured). Returns None if vowel-initial."""
    # Order candidates by length-desc to ensure longest-match wins.
    candidates = []
    for varga in VARGAS.values():
        candidates.extend(varga)
    candidates.extend(SEMIVOWELS + SIBILANTS + GLOTTAL)
    candidates.sort(key=len, reverse=True)
    for c in candidates:
        if root.startswith(c):
            return c
    return None  # vowel-initial


def root_vowel(root: str) -> str:
    """Return the first vowel of the root. Longest-match (ai/au before a/u)."""
    # Strip a leading consonant if present.
    fc = first_consonant(root)
    rest = root[len(fc):] if fc else root
    # Try longest match for compound vowels first.
    for v in sorted(VOWELS, key=len, reverse=True):
        if rest.startswith(v):
            return v
    # Fallback: scan for any vowel character.
    for i, ch in enumerate(rest):
        for v in VOWELS:
            if v.startswith(ch):
                return v
    return "?"


def articulation_place(root: str) -> str:
    fc = first_consonant(root)
    if fc is None:
        return "vowel-initial"
    for varga_name, varga_chars in VARGAS.items():
        if fc in varga_chars:
            return varga_name
    if fc in SEMIVOWELS:
        return "semivowel"
    if fc in SIBILANTS:
        return "sibilant"
    if fc in GLOTTAL:
        return "glottal"
    return "other"


def varga_column(root: str) -> str:
    fc = first_consonant(root)
    if fc is None:
        return "non-varga (vowel-initial)"
    for varga_chars in VARGAS.values():
        if fc in varga_chars:
            return COLUMN_NAMES[varga_chars.index(fc)]
    if fc in SEMIVOWELS:
        return "non-varga (semivowel)"
    if fc in SIBILANTS:
        return "non-varga (sibilant)"
    if fc in GLOTTAL:
        return "non-varga (glottal)"
    return "non-varga (other)"


# ---------- Bonding clustering ----------

def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    u = a | b
    return len(a & b) / len(u) if u else 0.0


def bonding_clusters(top_roots: list[str],
                     preverb_sets: dict[str, set[str]],
                     threshold: float = 0.5) -> dict[str, int]:
    """Greedy agglomerative clustering by Jaccard similarity of preverb-sets.
    Returns root → cluster_id."""
    clusters: list[list[str]] = []
    cluster_signature: list[set[str]] = []
    for root in top_roots:
        sig = preverb_sets.get(root, set())
        placed = False
        best_idx = -1
        best_sim = threshold
        for i, csig in enumerate(cluster_signature):
            sim = jaccard(sig, csig)
            if sim >= best_sim:
                best_sim = sim
                best_idx = i
        if best_idx >= 0:
            clusters[best_idx].append(root)
            cluster_signature[best_idx] = cluster_signature[best_idx] & sig \
                if cluster_signature[best_idx] else sig
            placed = True
        if not placed:
            clusters.append([root])
            cluster_signature.append(sig)
    return {r: i for i, members in enumerate(clusters) for r in members}, clusters


# ---------- Report machinery ----------

def heterogeneity_index(per_bucket_means: list[float],
                        grand_mean: float,
                        per_bucket_n: list[int]) -> float:
    """Weighted sum-of-squared-deviations of bucket means from grand mean,
    normalized by grand mean. Higher = axis splits valency more sharply."""
    if grand_mean == 0:
        return 0.0
    s = sum(n * (m - grand_mean) ** 2 for m, n in zip(per_bucket_means, per_bucket_n))
    total_n = sum(per_bucket_n)
    return s / (total_n * grand_mean) if total_n else 0.0


def bucket_report(rows: list[dict], bucket_key, axis_name: str) -> list[str]:
    """Generate per-bucket report lines for one axis. `bucket_key` is a
    function root → bucket name."""
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        buckets[bucket_key(r["root"])].append(r)

    grand_n = sum(len(v) for v in buckets.values())
    grand_total_valency = sum(r["valency"] for v in buckets.values() for r in v)
    grand_total_tokens = sum(r["tokens"] for v in buckets.values() for r in v)
    grand_mean = grand_total_valency / grand_n if grand_n else 0

    sorted_buckets = sorted(buckets.items(), key=lambda kv: -len(kv[1]))

    out = [
        f"Axis: {axis_name}",
        "-" * 64,
        f"{'Bucket':<32} {'N':>5} {'%N':>6} {'MeanV':>7} {'MedV':>5} "
        f"{'Tokens':>9} {'%Tok':>6}",
    ]
    means, ns = [], []
    for name, members in sorted_buckets:
        n = len(members)
        vals = [m["valency"] for m in members]
        mean_v = sum(vals) / n
        med_v = sorted(vals)[n // 2]
        toks = sum(m["tokens"] for m in members)
        pct_n = n / grand_n * 100
        pct_t = toks / grand_total_tokens * 100 if grand_total_tokens else 0
        out.append(
            f"{name:<32} {n:>5} {pct_n:>5.1f}% {mean_v:>7.2f} {med_v:>5} "
            f"{toks:>9,} {pct_t:>5.1f}%"
        )
        means.append(mean_v)
        ns.append(n)

    h_idx = heterogeneity_index(means, grand_mean, ns)
    out.append("")
    out.append(f"Grand mean valency: {grand_mean:.2f}")
    out.append(f"Heterogeneity index (weighted Σ (μ_bucket − μ_grand)² / μ_grand): "
               f"{h_idx:.4f}")
    out.append("")
    out.append("Top-3 exemplars per bucket (by valency):")
    for name, members in sorted_buckets:
        top3 = sorted(members, key=lambda m: -m["valency"])[:3]
        s = ", ".join(f"{m['root']} (v={m['valency']})" for m in top3)
        out.append(f"  {name:<32} {s}")
    out.append("")
    return out


def main():
    # Load Path C valency
    rows = []
    with open(PATH_C, encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append({
                "root": row["root"],
                "valency": int(row["valency_path_c"]),
                "tokens": int(row["total_tokens"]),
            })

    # Load preverb-sets per root (for the bonding-clustering axis)
    preverb_sets: dict[str, set[str]] = defaultdict(set)
    with open(ATTEST, encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            preverb_sets[row["root"]].add(row["preverb"])

    report = [
        "Path C Phase 9 — Column-axis testing",
        "=" * 64,
        "",
        "Four candidate column-axis interpretations are tested against the",
        "Path C valency distribution. The brief is explicit: REPORT NUMBERS",
        "DO NOT PICK A WINNER. The user decides which axis the book commits",
        "to. The four candidates are run in parallel; the heterogeneity index",
        "indicates how sharply each axis splits the valency distribution,",
        "but the index alone is not a winner-selection criterion — domain",
        "interpretation matters and the brief defers that interpretation.",
        "",
        "Distribution stats:",
        f"  Total roots: {len(rows):,}",
        f"  Grand-mean valency: {sum(r['valency'] for r in rows)/len(rows):.2f}",
        "",
    ]

    # AXIS A: Inherent vowel
    report.extend(bucket_report(rows, root_vowel, "A. Inherent vowel"))

    # AXIS B: Articulation place
    report.extend(bucket_report(rows, articulation_place,
                                "B. Initial articulation place (varga row)"))

    # AXIS C: Varga column
    report.extend(bucket_report(rows, varga_column,
                                "C. Initial varga column (C1–C5)"))

    # AXIS D: Empirical bonding clusters
    # Take top-100 roots by tokens; cluster by preverb-set Jaccard at threshold 0.5
    top_by_tokens = sorted(rows, key=lambda r: -r["tokens"])[:100]
    top_root_names = [r["root"] for r in top_by_tokens]
    cluster_map, clusters = bonding_clusters(
        top_root_names, preverb_sets, threshold=0.5)

    report.extend([
        "Axis: D. Empirical bonding clusters (top-100 by tokens, Jaccard ≥ 0.5)",
        "-" * 64,
    ])
    # Sort clusters by valency-sum descending
    cluster_summaries = []
    rows_by_root = {r["root"]: r for r in rows}
    for i, members in enumerate(clusters):
        m_rows = [rows_by_root[r] for r in members]
        sum_v = sum(m["valency"] for m in m_rows)
        sum_t = sum(m["tokens"] for m in m_rows)
        mean_v = sum_v / len(m_rows)
        # Get common preverbs across the cluster (intersection)
        sets = [preverb_sets[r] for r in members]
        common = set.intersection(*sets) if sets else set()
        union_set = set.union(*sets) if sets else set()
        cluster_summaries.append({
            "id": i,
            "n": len(members),
            "members": members,
            "mean_v": mean_v,
            "tokens": sum_t,
            "common_preverbs": common,
            "union_preverbs": union_set,
        })
    cluster_summaries.sort(key=lambda c: -c["tokens"])
    report.append(
        f"{'Cluster':<8} {'N':>4} {'MeanV':>7} {'Tokens':>9} "
        f"{'Common preverbs':<30} {'Representative roots':<40}"
    )
    for c in cluster_summaries:
        common_str = ",".join(sorted(c["common_preverbs"]))[:28] or "—"
        reps = ", ".join(c["members"][:3])
        if len(c["members"]) > 3:
            reps += "…"
        report.append(
            f"C{c['id']:<7} {c['n']:>4} {c['mean_v']:>7.2f} {c['tokens']:>9,} "
            f"{common_str:<30} {reps:<40}"
        )
    report.extend([
        "",
        f"Number of emergent clusters at threshold 0.5: {len(clusters)}",
        f"Largest cluster size: {max(len(c) for c in clusters)}",
        f"Singletons (n=1): {sum(1 for c in clusters if len(c) == 1)}",
        "",
        "Cluster detail (top-5 by tokens):",
    ])
    for c in cluster_summaries[:5]:
        report.append(
            f"  C{c['id']}: {c['n']} members, {c['tokens']:,} tokens, "
            f"mean valency {c['mean_v']:.1f}"
        )
        report.append(f"    members: {', '.join(c['members'])}")
        report.append(
            f"    common preverbs ({len(c['common_preverbs'])}): "
            f"{sorted(c['common_preverbs'])}"
        )
        report.append("")

    # Final framing note
    report.extend([
        "",
        "=" * 64,
        "Decision-deferral note (per autonomous-night brief):",
        "",
        "  This script reports numbers under four candidate column-axis",
        "  interpretations. It does NOT recommend or select a winner. The",
        "  heterogeneity index is a heterogeneity-of-means measure only;",
        "  it does not encode the structural fit between an axis and the",
        "  Ch 11 / Ch 10 polemic move (which is about *whether* and *how*",
        "  the varṇamālā column maps to dhātu reactivity).",
        "",
        "  The four axes are compatible — multiple axes can be load-bearing",
        "  simultaneously, and the book may commit to a primary axis with",
        "  the others as orthogonal secondary dimensions. Selection waits",
        "  for the user.",
        "",
    ])

    text = "\n".join(report) + "\n"
    OUT_REPORT.write_text(text)
    print(text)

    # Per-root assignments CSV
    with open(OUT_PER_ROOT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["root", "valency", "tokens", "first_consonant",
                    "vowel", "articulation_place", "varga_column",
                    "bonding_cluster"])
        for r in rows:
            root = r["root"]
            fc = first_consonant(root) or "—"
            v = root_vowel(root)
            ap = articulation_place(root)
            vc = varga_column(root)
            bc = cluster_map.get(root, "")  # only top-100 have cluster assignments
            w.writerow([root, r["valency"], r["tokens"], fc, v, ap, vc, bc])

    print(f"\nWrote {OUT_REPORT.relative_to(BUNDLE)}")
    print(f"Wrote {OUT_PER_ROOT.relative_to(BUNDLE)}")


if __name__ == "__main__":
    main()

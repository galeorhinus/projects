#!/usr/bin/env python3
"""Path C — Phase 3: Build attestation index.

Iterates all DCS CoNLL-U files, extracts VERB tokens, normalizes each
to its bare root (via DCS dictionary's preverbs column), records the
(preverb, pratyaya-class) pair from morphology features. Output is a
per-root attestation table the Phase 4 valency computation aggregates.

Pratyaya-class normalization is intentionally a coarse approximation
of the Pāṇinian pratyaya space:
  - Finite verbs: tuple of (Tense, Mood, Voice) → 'fin:Pres+Ind+Act' etc.
  - Non-finite: VerbForm value → 'nfin:Gdv', 'nfin:Part', 'nfin:Inf', etc.
  - Unknown morphology: 'fin:unknown' or 'nfin:unknown'

The approximation captures combinatorial reach without requiring the
full Pāṇinian pratyaya-derivation apparatus (which would need Path B).

Output (data/derived/attestation_index.csv):
  root, preverb, pratyaya_class, count
  (one row per unique triple; count = corpus-attested occurrences)
"""
from __future__ import annotations
import csv
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent.parent
DCS_ROOT = BUNDLE / "data" / "raw" / "dcs" / "dcs" / "data" / "conllu"
DICT_FILE = DCS_ROOT / "lookup" / "dictionary.csv"
CONLLU_DIR = DCS_ROOT / "files"
DHATUPATHA = BUNDLE.parent / "dhatupatha" / "data" / "dhatupatha.csv"
OUT = BUNDLE / "data" / "derived" / "attestation_index.csv"
META = BUNDLE / "data" / "derived" / "attestation_meta.txt"


def load_dictionary() -> dict[int, dict]:
    """LemmaId → {word, grammar, preverbs}. Reads ~180K rows; in-memory dict."""
    d = {}
    with open(DICT_FILE, encoding="utf-8") as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            try:
                lemma_id = int(row["id"])
            except (ValueError, KeyError, TypeError):
                continue
            d[lemma_id] = {
                "word": (row.get("word") or "").strip(),
                "grammar": (row.get("grammar") or "").strip(),
                "preverbs": (row.get("preverbs") or "").strip(),
            }
    return d


def parse_misc(misc: str) -> dict[str, str]:
    """Parse CoNLL-U MISC column (key=value|key=value) → dict."""
    out = {}
    if not misc or misc == "_":
        return out
    for part in misc.split("|"):
        if "=" in part:
            k, _, v = part.partition("=")
            out[k] = v
    return out


def parse_features(feats: str) -> dict[str, str]:
    """Parse CoNLL-U FEATS column. Same format as MISC."""
    return parse_misc(feats)


def normalize_pratyaya_class(feats: dict[str, str]) -> str:
    """Coarse normalization of pratyaya-class from morphology features."""
    vf = feats.get("VerbForm", "")
    if vf and vf != "Fin":
        # Non-finite: gerundive, participle, infinitive, absolutive, etc.
        return f"nfin:{vf}"
    # Finite verb
    tense = feats.get("Tense", "?")
    mood = feats.get("Mood", "?")
    voice = feats.get("Voice", "Act")  # default to Act if unspecified
    return f"fin:{tense}+{mood}+{voice}"


def extract_root_and_preverb(lemma: str, preverbs: str) -> tuple[str, str]:
    """Given the corpus lemma and its declared preverbs field from the
    dictionary, return (bare_root, preverb).

    The preverbs field looks like 'niḥ' for nirvap, 'pra' for pravac,
    'sam' for sambhū, etc. Multiple preverbs are space-separated.
    Bare-root lemmas have empty preverbs.
    """
    if not preverbs:
        return (lemma, "")
    # Strip preverbs from front of lemma, in order they appear in `preverbs`.
    # Note: the preverbs in `preverbs` are written in their sandhi-adjusted
    # surface form (e.g., 'niḥ' for nir-), but the lemma usually carries them
    # as a contracted form (e.g., 'nirvap'). We strip what we can; if the
    # surface preverb doesn't prefix the lemma exactly, we fall back to
    # joining the preverbs with the lemma as the "lemma+preverb" key.
    preverb_list = preverbs.split()
    # Common upasarga set with multiple sandhi forms.
    preverb_aliases = {
        "niḥ": ["niḥ", "nir", "ni"],
        "duḥ": ["duḥ", "dur", "duṣ"],
        "sam": ["sam", "saṃ"],
        "pra": ["pra"],
        "parā": ["parā", "para"],
        "apa": ["apa"],
        "anu": ["anu"],
        "ava": ["ava", "ā"],
        "vi": ["vi", "vy"],
        "ā": ["ā", "ā"],
        "ni": ["ni"],
        "adhi": ["adhi"],
        "api": ["api", "pi"],
        "ati": ["ati"],
        "su": ["su"],
        "ud": ["ud", "ut", "ucc", "ujj", "ucch"],
        "abhi": ["abhi", "abhy"],
        "prati": ["prati", "praty"],
        "pari": ["pari"],
        "upa": ["upa"],
    }
    root = lemma
    primary_preverb = preverb_list[0] if preverb_list else ""
    # Try to strip the first preverb from the lemma's start.
    candidates = preverb_aliases.get(primary_preverb, [primary_preverb])
    for cand in sorted(candidates, key=len, reverse=True):
        if root.startswith(cand) and len(root) > len(cand):
            root = root[len(cand):]
            break
    # If multiple preverbs, the secondary ones often stay attached to the root.
    # For the valency analysis, we report the primary preverb only — multiple-
    # preverb compounds are rare enough that this simplification is acceptable.
    return (root, primary_preverb)


def main():
    print(f"Loading dictionary from {DICT_FILE.relative_to(BUNDLE)}...", flush=True)
    dictionary = load_dictionary()
    print(f"  Loaded {len(dictionary):,} dictionary entries.", flush=True)

    # Find all .conllu files
    print(f"Scanning {CONLLU_DIR.relative_to(BUNDLE)} for .conllu files...", flush=True)
    conllu_files = sorted(CONLLU_DIR.rglob("*.conllu"))
    print(f"  Found {len(conllu_files):,} .conllu files.", flush=True)

    # Aggregate: (root, preverb, pratyaya_class) → count
    attestations: dict[tuple[str, str, str], int] = defaultdict(int)
    verb_tokens = 0
    files_done = 0
    errors = 0

    for fp in conllu_files:
        files_done += 1
        if files_done % 1000 == 0:
            print(f"  ...{files_done:,}/{len(conllu_files):,} files, "
                  f"{verb_tokens:,} verb tokens so far", flush=True)
        try:
            with open(fp, encoding="utf-8") as f:
                for line in f:
                    line = line.rstrip("\n")
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split("\t")
                    if len(parts) < 10:
                        continue
                    # Skip multi-word tokens (e.g., "1-2")
                    if "-" in parts[0] or "." in parts[0]:
                        continue
                    upos = parts[3]
                    if upos != "VERB":
                        continue
                    lemma = parts[2]
                    feats = parse_features(parts[5])
                    misc = parse_misc(parts[9])
                    try:
                        lemma_id = int(misc.get("LemmaId", "0"))
                    except ValueError:
                        lemma_id = 0
                    dict_entry = dictionary.get(lemma_id, {})
                    preverbs = dict_entry.get("preverbs", "")
                    root, preverb = extract_root_and_preverb(lemma, preverbs)
                    prat = normalize_pratyaya_class(feats)
                    key = (root, preverb, prat)
                    attestations[key] += 1
                    verb_tokens += 1
        except Exception as e:
            errors += 1
            if errors < 5:
                print(f"  ERROR in {fp.name}: {e}", file=sys.stderr)

    print(f"\nProcessed {files_done:,} files, {verb_tokens:,} verb tokens, "
          f"{len(attestations):,} unique (root, preverb, pratyaya) triples. "
          f"{errors} file errors.", flush=True)

    # Write output
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["root", "preverb", "pratyaya_class", "count"])
        for (root, preverb, prat), count in sorted(attestations.items(),
                                                    key=lambda kv: (-kv[1], kv[0])):
            w.writerow([root, preverb, prat, count])

    with open(META, "w", encoding="utf-8") as f:
        f.write(f"DCS conllu files processed: {files_done}\n")
        f.write(f"Total verb tokens: {verb_tokens}\n")
        f.write(f"Unique (root, preverb, pratyaya) triples: {len(attestations)}\n")
        f.write(f"File errors: {errors}\n")
        f.write(f"Dictionary entries loaded: {len(dictionary)}\n")

    print(f"Wrote {OUT.relative_to(BUNDLE)}", flush=True)
    print(f"Wrote {META.relative_to(BUNDLE)}", flush=True)


if __name__ == "__main__":
    main()

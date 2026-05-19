# Path C Night Session — STATUS.md

*Live status log for the autonomous Path C empirical kickoff. Started 2026-05-18.*

This file is the morning handoff: the user reads this first to understand what completed, what blocked, and where the run ended. Phases are logged with timestamps (relative — "Phase N start" / "Phase N done") and per-phase outcome (✓ completed / ⚠ partial / ✗ blocked).

---

## Run plan

Eleven phases per `working/as_todo.md` CURRENT FOCUS — Path C autonomous-night-session brief:

1. Bundle scaffolding (`analysis/ganah/` mirroring `analysis/dhatupatha/`).
2. Corpus acquisition (DCS GitHub → GRETIL → Whitney 1885 fallback).
3. Parser: build (*dhātu*, *upasarga*, *pratyaya*) attestation index.
4. Path C valency computation per *dhātu*.
5. Spearman baseline: Path A (MW-derivative count) vs Path C (corpus-attested count) on the 144-row MW sample.
6. Tier cutoffs (Polyvalent / Bivalent / Monovalent) with ±10% sensitivity testing.
7. Tier-distribution across the full *Dhātupāṭha*.
8. Cross-corpus: BhG vs *Ṛgveda saṃhitā*.
9. Column-axis testing: 4 candidates (inherent vowel, articulation place, *varga* column, empirical bonding clusters) — report numbers, **do not pick a winner** (hard stop per brief).
10. Cross-*gaṇa* column-distribution extension (recompute Ch 10's *juhotyādi* C4-enrichment at 31.8% etc. under Path C).
11. `FINDINGS.md` synthesis + final report + push.

## Hard stops (per brief — DO NOT do without user sign-off)

- Pick the column axis (Phase 9 reports per-axis numbers; user decides).
- Rewrite Claim 12 / Claim 8 in TOC files.
- Draft Ch 11 prose beyond the stub.
- Touch the Saunaga / Śākaṭāyana flag.
- Modify other chapter files unless empirical work directly invalidates a cited number.

## Commit / push cadence

- Commit at the end of each coherent phase.
- Push to `origin/main` at end if working tree is clean of unrelated changes.
- Working tree at start: only `atomicSanskrit/build/` artifacts (derived; not committed). Plus `bed-controller-idf/`, `aiWritingStyle/` (untouched). Safe to push manuscript commits.

---

## Phase log

### Phase 1 — Bundle scaffolding

**Start.** Created `analysis/ganah/` with subdirectories: `data/raw/`, `data/derived/`, `scripts/`, `figures/`. Mirroring `analysis/dhatupatha/` structure.


# Author Tasks

Quick task list for tactical items tracked separately from the project-level `as_todo.md`. Mark off as work lands.

**Conventions.** `[ ]` open · `[~]` in progress · `[x]` done.

---

## Open

### [ ] Sanskrit word for *calibrant*

The book deploys ***calibrant*** as the English term for Sanskrit's role across the architecture (*the calibrant*, *calibrant-anchored languages* — Ch 5 §5.6, Ch 13 §13.5, Ch 14 forward). The term is precise but unanchored to Sanskrit's own vocabulary. Decide on the canonical Sanskrit anchor, deploy at first-use, and add to CLAUDE.md's calibration vocabulary cluster.

**Candidate terms to evaluate:**

- **मानक (*mānaka*)** — that which measures, the standard. Modern-Sanskrit register; clean fit for "calibrant."
- **प्रमाण (*pramāṇa*)** — means of valid measure; already canonical in Nyāya / Mīmāṃsā as the means of valid knowledge. Carries the epistemological weight already.
- **मान (*māna*)** — measure / criterion / standard. Shorter; less load.
- **आधार (*ādhāra*)** — substrate / foundation. Different angle; might fit when emphasizing the bearing function rather than the measuring function.

Pair the chosen term on first-use following the standard Indic-anchor convention (English + Devanagari + IAST).

### [~] Samskrita Bharati acknowledgment — separate Acknowledgments chapter

**Status (2026-05-22).** Initial Samskrita Bharati paragraph drafted and placed in new front-matter chapter `as_0_02_acknowledgements.md`, inserted between Preface and Prologue. Three-paragraph entry covers: (1) the architectural framing of their decades of work, (2) the volunteer-teachers as Wave-3 *ṛṣis* in action, (3) the explicit disclaimer that the book's argument is the author's alone and Samskrita Bharati bears no responsibility for it. The Preface's existing `[ACKNOWLEDGMENTS — TO BE EXPANDED BY AUTHOR]` placeholder (line 94) is left in place pending author decision on whether to migrate or keep separate.

**Open extensions** (author adding more later): family, contributors, scholarly debts, archives, translators, readers of early drafts. Decide whether Preface placeholder should be merged into the new chapter or retained for in-Preface acknowledgments.

---

### [ ] Template-distribution analysis — Bhagavad Gītā + Vedic *dhātu* subsets

Run the template-classification (*racanā*) analysis (per [`dhatu_hexagons/TEMPLATES.md`](../50_projects/dhatu_hexagons/TEMPLATES.md) §6) on the ~500 *dhātus* traditionally listed for the *Bhagavad Gītā* and the *Vedas*, and compare the template distributions against the full *Dhātupāṭha* (~2,168 entries).

**Why.** Different corpora may favor different templates. If the *Vedic* / *Gītā* *dhātus* show the same template distribution as the full *Dhātupāṭha*, the architecture's *racanā* preferences are invariant across text-types — a strong engineering signal. If they diverge, the divergence pattern is itself analytically interesting (register difference? chronological signature? semantic-domain skew?).

**Inputs needed.**

- The traditional list of *Bhagavad Gītā* *dhātus* — a published index or a scholarly compilation. Likely sources: a *Gītā* concordance, a *Gītā*-specific dhātu list in commentarial literature, or a Sanskrit corpus tool (GRETIL / SARIT). Need to locate and verify the count (~500 is a working estimate).
- The traditional list of Vedic *dhātus* — typically derived from the *padapāṭha* / Yāska / W. S. Allen's appendix or similar scholarly compilations.
- The *Dhātupāṭha* baseline already lives in [`analysis/dhatupatha/data/dhatupatha.csv`](../../analysis/dhatupatha/) (2,168 entries).

**Analysis steps.**

1. Acquire / curate the Gītā and Vedic *dhātu* lists. Store under `analysis/dhatupatha/data/` (e.g., `gita_dhatus.csv`, `vedic_dhatus.csv`).
2. For each list, run the template-classifier (the existing `analyze_shells.py` script with the V1/V2-aware parser; or a thin wrapper that accepts a different input corpus).
3. Tally templates per corpus. Compute cumulative percentages.
4. Compare distributions side-by-side: which templates dominate each corpus?
5. Identify the most divergent templates (largest difference in rank or share).
6. Test whether the *Dhātupāṭha* template distribution is the union of the corpus-specific distributions, or whether the full *Dhātupāṭha* contains *dhātus* that no actual corpus uses.

**Outputs.**

- `analysis/dhatupatha/derived/template_distribution_comparison.csv` — one row per template, columns: count + percentage for Dhātupāṭha / Gītā / Vedic.
- `analysis/dhatupatha/figures/template_distribution_comparison.svg` — side-by-side Zipfian / histogram comparison.
- Brief writeup of which templates dominate each corpus and what the divergences (if any) suggest. Lands eventually in App 5 or a new sub-section.

**Why this is high-value.** A *Dhātupāṭha* listing is a *compiled inventory* — the grammarians' catalogue. A *Gītā* / Vedic list is the *actual usage* — what speakers / reciters actually deployed. The two should converge if the inventory was built to reflect usage. If they diverge significantly, either the inventory is over-comprehensive (lists *dhātus* nobody used) or the corpora are register-specific (use only a slice of the inventory).

Either result is empirically meaningful for the engineering thesis.

---

## Done

(none yet)

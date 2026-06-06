# Vocal-tract inventory atlas — roadmap for future work

> Outstanding analytical work, polemic extensions, and open questions arising from the 34-language atlas + overlay-and-metric system. Companion documents: `inventory_atlas_analysis.md` (findings), `inventory_atlas_critique.md` (anticipated critique + methodology response).

The frame everything operates under: **Sanskrit's phoneme inventory is the curated superset of the human articulator space.** Each work item below tests, refines, or extends that claim.

---

## 1. Immediate next steps (highest polemic ROI)

### 1.1 The mahāprāṇa-stripped pairwise

**Status, 2026-06-06: completed.** `vocal_tract_overlay.py` now supports `--strip`, `--strip-a`, and `--strip-b`. The full Sanskrit-stripped comparison is recorded in `inventory_atlas_mahaprana_strip_results.md`.

**The move.** Strip the engineered features from Sanskrit (the mahāprāṇa rows — voiceless aspirated and voiced aspirated stops) and re-run the Sanskrit-pairwise. The book's prediction: removing the engineering layer SHIFTS the rankings in a specific, polemic-relevant way.

**Observed outcomes:**

| Language | Current Jaccard | Sanskrit-stripped Jaccard | Direction |
|---|---:|---:|---|
| Tamil | 0.31 | 0.41 | UP — Tamil's "no mahāprāṇa" stops being a non-shared feature |
| Korku | 0.47 | 0.65 | UP — base inventories align |
| Gondi / Kurukh | 0.49 | 0.67 | UP — same reason |
| Telugu / Kannada | 0.76 | 0.50 | DOWN — removing the absorbed engineering layer lowers the match |
| Malayalam | 0.74 | 0.49 | DOWN — same reason |
| Santali | 0.78 | 0.50 | DOWN sharply — the high score is largely the absorbed mahāprāṇa rows |
| English / French | 0.30 / 0.32 | 0.38 / 0.42 | UP — removing Sanskrit-only aspirates reduces non-shared cells |
| Farsi | 0.26 | 0.33 | UP |

**Polemic deliverable:** Removing the engineered mahāprāṇa layer shows that the southern subcontinental + central forest belt languages cluster more closely to Sanskrit's base, while the Sanskritic-absorbed languages (Telugu, Kannada, Malayalam, Santali) drop. That split confirms that the high scores in the absorbed group are carried by the aspirated engineering layer, not by base inventory similarity alone.

**Implementation.** The implemented presets are `mahaprana`, `voiceless_asp`, `voiced_asp`, and `sibilants`. `--strip-a` strips the first language, `--strip-b` strips the second language, and `--strip` strips both before computing metrics.

### 1.2 The Sanskrit ह placement fix

**Status, 2026-06-06: completed.** Sanskrit ह now sits in column 12, the modern glottal / laryngeal column, while the README preserves the traditional *kaṇṭhya* note.

**The issue.** Sanskrit's ह had been placed at column 9 (velar) in the chart, reflecting the Pāṇinian *kaṇṭhya* (throat/velar) classification. In standardised IPA terms, ह is /ɦ/ glottal — column 12.

**Polemic value.** Fixing it would slightly bump Sanskrit's coverage / Jaccard / etc. with every language that has /h/ at column 12 (most of the atlas). The current placement underestimates Sanskrit's similarity with the rest of the atlas by one cell systematically.

**Implementation.** `scatter_sanskrit.json` now places "ह" in the final glottal / laryngeal slot. `scatter_sanskrit.svg` and the active Sanskrit overlays have been regenerated.

**Note.** This is a defensible reading-of-the-source choice rather than a bug. The Pāṇinian classification is internally valid; the IPA classification is the cross-language standard the atlas otherwise uses. Document the choice either way.

### 1.3 README integration

**Status, 2026-06-06: completed in compact form.** `figures/vocal_tract/README.md` §10.4 now carries the updated Sanskrit-pairwise ranking with Jaccard and asymmetric Sanskrit-coverage values, plus a mahāprāṇa-strip sensitivity note. The full eight-metric table remains in the working analysis files.

---

## 2. The PIE time-series

**The move.** Construct 4–5 PIE chart configs corresponding to the major milestones of the reconstruction:

| # | Year | Theorist | Distinguishing feature |
|---:|---:|---|---|
| 1 | 1862 | Schleicher | 3 stop series × 3 places (labial, dental, velar); essentially Sanskrit with Greek/Latin overlay |
| 2 | ~1897 | Brugmann + Neogrammarians | Same 3 series, 3 dorsal places (palatovelar, velar, labiovelar); expanded vowel system |
| 3 | 1879/1927 | Saussure → confirmed-via-Kuryłowicz | Adds 3 "laryngeals" *h₁ *h₂ *h₃ |
| 4 | 1973 | Gamkrelidze-Ivanov + Hopper | Glottalic Theory: same correspondences re-read as ejective / voiceless / voiced |
| 5 | ~2020 | Modern eclectic | Various positions; no consensus |

**The polemic deliverable.** Sanskrit-vs-PIE overlay charts showing similarity DECLINING over 150 years of revision. Schleicher 1862 should have very high Jaccard with Sanskrit (because Schleicher walked backward from Sanskrit). The Glottalic-theory PIE should have much lower Jaccard because the voicing series is re-interpreted. The modern eclectic PIE should be different again.

**The chart message:** *Actual languages have stable phoneme inventories; PIE's inventory has been revised five times in 150 years. The orthodox claim of inheritance from PIE through Sanskrit is methodologically a moving target.*

**Implementation.** Five JSON configs (one per milestone) with phoneme matrices reflecting that milestone's reconstruction. Each chart marked clearly as RECONSTRUCTED — asterisks on every cell, distinct visual marker (outline-only dots? grey-stippled?), prominent caption.

**Sources.**
- Schleicher 1862: *Compendium der vergleichenden Grammatik der indogermanischen Sprachen*; the *Avis akvāsas ka* fable as the canonical specimen
- Brugmann 1886–1893: *Grundriss der vergleichenden Grammatik der indogermanischen Sprachen*
- Saussure 1879: *Mémoire sur le système primitif des voyelles dans les langues indo-européennes*
- Kuryłowicz 1927: laryngeal-confirmation work
- Gamkrelidze-Ivanov 1984/1995: *Indo-European and the Indo-Europeans* (the English translation)
- Modern eclectic: Mallory and Adams 2006 *The Oxford Introduction to Proto-Indo-European*; Fortson 2010 *Indo-European Language and Culture*

---

## 3. Central Asian and Iranian additions

**The polemic test.** Does any orthodoxy-Indo-Iranian language land in the high-Sanskrit-similarity band, or are they all down with English/French/Farsi at 0.25–0.35 Jaccard?

**Candidate languages:**

| Language | Status | Why it matters |
|---|---|---|
| Pashto | Modern; Iran/Pakistan/Afghanistan | Orthodox Iranian; spoken near Indic; tests the "Indo-Iranian closeness" claim |
| Old Persian | Extinct; attested | Achaemenid royal language; close in date to Vedic Sanskrit |
| Avestan | Extinct; attested | Zoroastrian sacred language; orthodoxy's "closest Iranian cousin of Sanskrit" |
| Tocharian A / B | Extinct; attested in Tarim Basin | "Most distant" Indo-European branch per orthodoxy; tests the family-tree edge |
| Sogdian | Extinct; attested in Central Asia | Iranian language with heavy Indic contact through Buddhism |
| Khotanese | Extinct; attested | Iranian with extensive Indic loans in Buddhist texts |
| Bactrian | Extinct; Greek-script Iranian | Cultural-zone outlier |
| Ossetian | Modern; Caucasus | Modern Iranian in non-Iranian linguistic environment |
| Pamir languages | Modern; Tajikistan / Afghanistan / Pakistan | Mountain-isolated Iranian varieties |

**Prediction.** Avestan should score moderate-to-high against Sanskrit (the orthodoxy expects this; the inventory data may or may not corroborate). Tocharian should score low (modern reconstructions place Tocharian as the most-divergent IE branch). Pashto/Pamir/Ossetian should score moderate. Old Persian should score moderate-to-high.

**The interesting test:** is Sanskrit-Avestan higher than Sanskrit-Tamil? The orthodoxy SAYS yes (sibling languages should be close). The data might say no. If the data show Sanskrit-Tamil > Sanskrit-Avestan on multiple metrics, the Indo-Iranian closeness claim is undermined even at the metric the orthodoxy would expect to confirm it.

**Sources.** Standard descriptive grammars and inventory tables:
- Pashto: Heston 1992; Septfonds 2009
- Old Persian: Kent 1953 (*Old Persian: Grammar, Texts, Lexicon*)
- Avestan: Hoffmann and Forssman 1996; Beekes 1988
- Tocharian: Krause-Thomas 1960; Adams 1988
- Sogdian: Sims-Williams (multiple)
- Khotanese: Emmerick 1968, 1992
- Bactrian: Sims-Williams 2007
- Ossetian: Thordarson 2009
- Pamir: Edelman / Dodykhudoeva (multiple)

---

## 4. Visualization extensions

### 4.1 Multi-language overlays (3-4 languages)

The current overlay supports 2 languages. The polemic gains from 3-up or 4-up overlays:

- Sanskrit + Tamil + Telugu + Malayalam — the southern bulk
- Sanskrit + Mundari + Santali + Korku — the Munda spectrum
- Sanskrit + Gondi + Kui + Kurukh — the central forest belt
- Sanskrit + English + French + German — the orthodox IE comparison
- Sanskrit + Avestan + Pashto + Farsi — the orthodox Iranian comparison

**Visual codes (grayscale).** Add markers beyond filled/outlined:
- Language A: filled gray circle, radius 0.05"
- Language B: outlined circle, radius 0.075"
- Language C: small inner dot (radius 0.025") — only visible when A or B is at the same cell
- Language D: dashed outline ring (radius 0.09")

Overlapping cells become readable as "all four have this phoneme" or "A and B but not C" etc.

### 4.2 Comparison strip layouts

For book deployment, side-by-side layouts of 2/4/6 charts in a single figure:

- Strip layout for 4 languages: 2×2 grid, shared legend across the bottom
- Highlighted-overlap layout: 4 mini-charts in a row, with the SHARED cells highlighted across all 4 (showing the common-to-all skeleton)

### 4.3 Pairwise similarity heatmap

Visualise the 34×34 Sanskrit-pairwise + cross-pairwise Jaccard matrix as a grayscale heatmap. Darker cells = more similar. Reordering the rows/columns by clustering (e.g., complete-linkage hierarchical clustering) would expose latent groupings — the "Sanskrit-centric cluster" emerging naturally without imposing the orthodox family-tree labels.

### 4.4 Sanskrit-as-anchor radial diagram

A single radial chart with Sanskrit at the centre and 33 other languages arrayed around it at distance proportional to (1 − cosine similarity). The southern/Munda/central forest belt languages would cluster close; the orthodox-IE languages would cluster far. Visually striking; one-glance polemic deliverable.

---

## 5. Methodology extensions

### 5.1 Frequency-weighted metrics

The current metric treats each phoneme as equal weight. A frequency-weighted version would assign weight proportional to the phoneme's actual usage in attested text. Sanskrit's /a/ would carry more weight than /ɭ/.

Frequency data sources: large corpora exist for major languages (English, Hindi, Tamil corpora are accessible). For Sanskrit, frequency data from the Vedic corpus or the *Aṣṭādhyāyī* would be appropriate.

**Polemic value.** Sanskrit's mahāprāṇa series is LOW frequency in practice (aspirates appear in fewer roots than unaspirated stops). A frequency-weighted comparison would diminish the "Sanskrit has 4 stop rows" depth advantage and likely SHIFT the metrics toward the place-overlap pattern — strengthening the curated-superset claim by showing Sanskrit's "extra" cells are used sparingly.

### 5.2 Phonotactic / syllable-structure comparison

Two languages may share inventory but combine phonemes very differently. Sanskrit allows complex onset clusters (कृ kr-, स्थ sth-, ह्र hr-), Tamil does not. A phonotactic comparison would test whether the shared inventory cells are also combined similarly.

**Polemic angle.** The book's engineering thesis covers not just inventory but ALSO the rules for combination (sandhi, syllable structure, the *Aṣṭādhyāyī* phonotactics). A second-dimension comparison would extend the inventory analysis to combinatorial engineering.

### 5.3 Articulator-load distribution

For each language, what fraction of its inventory uses tongue tip vs blade vs body vs root vs lips? Comparison of articulator-engagement profiles. Sanskrit's broad articulator engagement vs (say) Bodo's narrow engagement should be visible.

### 5.4 Manner-repertoire complexity

How many of the 13 standard manners does each language use? Single-number summary of inventory shape complexity. Sanskrit uses 9, Tamil 5, Arabic 11, Bodo 5. Quick descriptor for chart captions.

### 5.5 Engineering-density score

A composite score: weighted combination of (place breadth, manner depth, retroflex presence, mahāprāṇa presence, sibilant series, aspirated-voiced series). Sanskrit would score highest by design. Tamil would score lower. The orthodox IE languages would score in between. This would be a numerical "engineering signature" — defensible if the weights are pre-registered and the metric isn't tuned to produce the desired ranking.

**Methodological caution.** The book should NOT introduce this metric tuned to confirm a polemic claim. It should be defined before being computed, transparent about weights, and published with the raw cell counts so independent readers can audit.

---

## 6. Open analytical questions

### 6.1 Sanskrit ह — Pāṇinian kaṇṭhya vs IPA glottal

Already noted in §1.2. The Pāṇinian classification places ह as kaṇṭhya (throat / velar zone). IPA places ह as glottal. Both are internally defensible. The book should document which placement is used and why, and ideally run the analysis BOTH ways to show that the central findings are robust to this choice.

### 6.2 The classification table

`SYMBOL_TO_MANNER` in `vocal_tract_overlay.py` hand-codes ~280 symbol-to-manner mappings. A few are debatable:
- Sanskrit च /c/ ~ /tʃ/: classified as voiceless unaspirated stop, but some analyses treat as voiceless affricate
- Tamil ழ /ɻ/: classified as approximant, sometimes called retroflex approximant or retroflex flap
- Mundari ʔ glottal stop: classified as voiceless unaspirated stop
- Korean tensed stops ㅃ ㄸ ㄲ: classified as voiceless unaspirated stops, but the "tensed" feature is sometimes treated as a separate phonemic dimension

Each ambiguity is a methodological choice with downstream effects on the metrics. The book should document these choices in an endnote or appendix.

### 6.3 The 12-place axis

Other phonetic taxonomies could be used:
- 8-place (coarser): bilabial, labio-dental, dental-alveolar, post-alv, retroflex, palatal, velar+uvular+pharyngeal+glottal
- 16-place (finer): split alveolar into alveolo-palatal and alveolar; split velar into velar and labio-velar; etc.

Robustness check: do the rank orderings survive these variants?

### 6.4 The Pāṇinian-centric option

What if the place axis were the Pāṇinian *sthāna* scheme (kaṇṭhya, tālavya, mūrdhanya, dantya, oṣṭhya — 5 places) instead of the 12-place IPA? Each language would be cast onto the Pāṇinian grid. This would be a different polemic argument: not "comparing on the IPA standard" but "comparing on the Sanskrit native classification." Some languages would map cleanly; others (those with sounds Sanskrit doesn't have a place for) would need extension.

Implementation: alternate config with a 5-place or 6-place Pāṇinian axis. Probably worth doing once for the Indic languages.

### 6.5 Engineered vs absorbed identification

For each language, identify (using independent linguistic-history sources) which inventory cells are "native" and which are "absorbed from contact." Then re-run the metric on the NATIVE inventories only.

This would test the engineering thesis more sharply: do Telugu/Kannada/Malayalam's high scores against Sanskrit DROP when we restrict to native phonemes only? The book's thesis predicts yes.

Tools needed: linguistic-history annotations per language, sourced from Krishnamurti and the regional grammar tradition. Non-trivial to build but worth it.

---

## 7. Polemic moves to develop in the book

### 7.1 The "engineered game" framing

The orthodoxy plays the genetic-vs-areal game. The book can introduce a third frame: **the engineered-vs-organic game.** Languages are either deliberately engineered (Sanskrit, possibly Classical Arabic under Sibawayh, possibly Greek under Alexandrian grammarians) or organic (everything else). Inventory comparisons should be cast accordingly:

- Comparing two organic languages: areal effects dominate; family-tree may also show
- Comparing an engineered language to an organic one: the engineered language is the curated superset; the organic language nests inside or stands apart
- Comparing two engineered languages: their architectures can be compared structurally (e.g., does Sanskrit's varga organisation share structural features with Arabic's *ḥurūf al-halq* etc.)

The atlas data fits this frame naturally: Sanskrit (engineered) is the curated superset; everything else nests in or stands apart based on areal effects.

### 7.2 The "Schleicher's bake" closing argument

A specific chapter section devoted to Schleicher 1862 and the PIE time-series. The argument:

1. Schleicher walked backward from Sanskrit to construct PIE
2. The resulting PIE was Sanskrit-shaped because the bake was Sanskrit
3. The orthodoxy later revised PIE away from Sanskrit (Glottalic Theory, laryngeals) — but only because the bake had become embarrassing
4. The methodology that produced the original bake was never re-examined
5. The current PIE has been revised five times in 150 years; this is not the behaviour of a discovered fact, this is the behaviour of a theoretical construct under constant adjustment

The atlas data provides the visual companion: the PIE time-series Sanskrit-similarity chart, declining over the revision history.

### 7.3 The Tamil-as-Sanskrit-base argument

Restate Finding 2 from `inventory_atlas_analysis.md` polemically: Tamil is the closest visible approximation in the atlas to what Sanskrit's pre-engineering anatomical base would look like. Tamil + Sanskrit's 21-cell engineering = Sanskrit. Tamil + 6 cells of Tamil-specific elaboration = Tamil.

The orthodox response (Sanskrit and Tamil are different families) requires explaining the asymmetric containment. The engineering thesis explains it cleanly: same anatomical base, different curation history.

### 7.4 The "areal-effects-are-detectable-when-real" closing

Brahui is the structural witness: areal effects DO show in this data, when they're real. The orthodox dismissal of Sanskrit-Tamil similarity as "areal" is a framework-protective gesture, not an empirical observation about the data. The book can name and dispatch this gesture once, in a single chapter, with the Brahui control case as the structural pivot.

---

## 8. Things to NOT do (avoid overreach)

- Don't claim the atlas refutes PIE reconstruction. It doesn't. It's one dimension of evidence against the framework's predictive power, not a complete refutation.
- Don't claim Sanskrit was engineered FROM the data of other inventories. The engineering thesis is about Sanskrit's own architecture; the data show consistency but not causation.
- Don't claim a "natural" or "neutral" position on family classification. The atlas is itself a framework, with methodological choices. Be transparent about them.
- Don't oversell the metrics. Cosine, Jaccard, Dice, JSD-sim all carry roughly the same information for binary inventories. The asymmetric coverage and place-overlap metrics carry distinctive information. Lead with those.
- Don't conflate inventory similarity with phonological identity. Two languages may have the same phoneme cells but very different phonological behaviour (sandhi rules, syllable structure, prosody). The atlas captures only one dimension.

---

## 9. Sequence of work

If asked "what should we build next, in what order":

1. **Sanskrit ह placement fix** (1 line change, 1 commit; cleans up the central data anomaly)
2. **Mahāprāṇa-stripped pairwise** (implement `--strip`, run analysis, see if predictions hold)
3. **README integration** of the 6-metric pairwise table (replaces the partial Jaccard-only table)
4. **Avestan + Pashto + Old Persian charts** (tests the Indo-Iranian closeness claim directly)
5. **PIE time-series** (5 milestone configs, runs the Schleicher's-bake argument visually)
6. **Multi-language overlay extension** (3-4 language overlays for grouped comparisons)
7. **Pairwise similarity heatmap** (34×34 matrix, latent-cluster visualisation)
8. **Frequency-weighted metric** (only if frequency data is available; otherwise stop here)

Steps 1–3 are routine, can be completed in one session. Steps 4–5 require new linguistic data per language. Steps 6–7 are visualisation work. Step 8 requires corpus data.

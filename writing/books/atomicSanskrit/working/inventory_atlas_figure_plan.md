# Vocal-tract inventory atlas — figure deployment plan (Ch 7 / Ch 8 / Ch 9 / AP3)

> Placement plan for all the figures generated from the 34-language inventory atlas + the PIE time-series + the polished overlay infrastructure.  Companion documents: `inventory_atlas_analysis.md`, `inventory_atlas_critique.md`, `inventory_atlas_roadmap.md`, `inventory_atlas_ch9_memo.md`.  Tooling and per-figure technical reference live in `../figures/vocal_tract/README.md`.

---

## 0. Chapter framings (from the TOC)

| Where | Title | The move the chapter makes |
|---|---|---|
| **Ch 7** | *ॐ (Oṃ): The Anatomy of Sound* | Descriptive — voice as *ādivādya*, the mouth as the original instrument; standard phonetic vocabulary + Sanskrit naming |
| **Ch 8** | *Mapping the Mouth: The Sonomeric Grid* | Polemic — the *varṇamālā* as engineered selection of well-separated *sthāna* positions from the superset of mouth-producible sounds |
| **Ch 9** | *The Subcontinental Superset* | Evidence — surveys non-IE Indic inventories to demonstrate the Indic Superset thesis |
| **AP3** | *The Sonomer and the Audiograph* | Prosecution + reference — Sanskrit is sonomeric before audiographic; Brāhmī ≠ Aramaic; complete dossier for the serious reader |

---

## 1. Ch 7 — The Anatomy of Sound  *(2–3 figures)*

**Register.** Descriptive — the anatomy is the foundation.  Avoid data overlays here; quantitative comparison would break the descriptive register.

| Fig | What | Source | Status |
|---|---|---|---|
| 7.1 | **Vocal-tract anatomy diagram** — clean cross-section showing the 12 places of articulation labeled with both English (BIL, DEN, ALV, …) and Sanskrit (*oṣṭhya*, *dantya*, …).  The "mouth as instrument" anchor. | New — strip `overlay_sanskrit_vs_*_polished.svg` to just the ribbon + place labels (no dots / no metrics) | Build |
| 7.2 | **The *Oṃ* sweep** — vowel trajectory through the vocal tract for ओम् (a → u → m), with arrow showing the resonance shifting from open → rounded → bilabial. | New — small bespoke figure | Build |
| 7.3 *(optional)* | **A single consonant** placed on the grid — क at velar — as a teaser for Ch 8. | Cropped from `scatter_sanskrit.svg` | Build if space |

---

## 2. Ch 8 — Mapping the Mouth: The Sonomeric Grid  *(3–4 figures)*

**Register.** Polemic — the *varṇamālā* presented as engineered architecture.  Lean Sanskrit-only; the comparative move belongs in Ch 9.

| Fig | What | Source | Status |
|---|---|---|---|
| 8.1 | **The Sanskrit *varga* matrix as a phonetic grid** — labeled atlas chart showing the 5 × 5 *sparśa* matrix + semivowels + sibilants, with the *varga* names along the right edge (*kavarga*, *cavarga*, *ṭavarga*, *tavarga*, *pavarga*).  *This is the central reveal of Chapter 8.* | `scatter_sanskrit.svg` annotated | Build (annotation layer) |
| 8.2 | **Snap-to-grid demonstration** — show "candidate places" the *varṇamālā* could have used but doesn't (the columns Sanskrit leaves dark) with caption explaining range-boundary-exclusion and acoustic adjacent-exclusion. | New — sparse / annotated version of `scatter_sanskrit.svg` | Build |
| 8.3 | **The engineered ribbon** — the *varṇamālā* organisation as a deliberate structure, with the 5 *varga* columns highlighted and the spaces-between annotated as "deliberately empty." | New — annotated version of `scatter_sanskrit.svg` | Build |
| 8.4 *(optional)* | **A teaser one-pair overlay**: Sanskrit + Tamil, showing where Tamil's 6th column (alveolar) sits and signaling *more on this in Ch 9*. | `overlay_sanskrit_vs_tamil_polished.svg` | Use as-is |

---

## 3. Ch 9 — The Subcontinental Superset  *(6–8 figures, the heaviest chapter)*

**Register.** Evidence — lead with the cluster claim, then the per-pair details, then the PIE trajectory.  This is the empirically-anchored chapter; figures carry the polemic weight directly.

| Fig | What | Source | Status |
|---|---|---|---|
| 9.1 | **The Sanskrit-shell cluster rosette** — 3-language version (Tamil + Telugu + Santali overlaid on the Sanskrit shell).  Opens the chapter; thesis-statement figure. | New — build in our pipeline (rosette mode for the overlay script) | Build |
| 9.2 | **Sanskrit vs Tamil polished overlay** — the curated-superset structure; metric panel shows Sk⊇Tamil = 0.67, Tamil ⊇ Sanskrit = 0.36.  Asymmetric containment witnessed directly. | `overlay_sanskrit_vs_tamil_polished.svg` | Use as-is |
| 9.3 | **Sanskrit vs Santali polished overlay** — the absorbed-Sanskritic Munda case (Jaccard = 0.73, the highest in the atlas; same matrix shape as Sanskrit, built from absorption). | `overlay_sanskrit_vs_santali_polished.svg` | Use as-is |
| 9.4 | **Sanskrit vs Brahui polished overlay** — the areal-control case; place-overlap drops to 0.45 because Persian / Arabic reshaping; the metric correctly captures areal pressure when it exists. | `overlay_sanskrit_vs_brahui_polished.svg` | Use as-is |
| 9.5 | **Sanskrit vs Korean polished overlay** — the geography-independent containment case (Sk⊇Korean = 0.87 from another continent — the curated-superset signature in pure form). | `overlay_sanskrit_vs_korean_polished.svg` | Use as-is |
| 9.6 | **Sanskrit vs English polished overlay** — the orthodox-IE "sibling" that ISN'T (Sk⊇English = 0.50; place-overlap = 0.40). | `overlay_sanskrit_vs_english_polished.svg` | Use as-is |
| 9.7 | **Sanskrit vs Farsi polished overlay** — the orthodox-Indo-Iranian "closest sister" — invisible at inventory level (Sk⊇Farsi = 0.44, lower than Tamil's 0.67). | `overlay_sanskrit_vs_farsi_polished.svg` | Use as-is |
| 9.8 | **PIE trajectory bar chart** — Sk⊇PIE declining over 150 years (0.81 Schleicher → 0.48 Glottalic → 0.64 Modern), with Tamil ⊇ PIE for reference. | `pie_trajectory_bar_chart.svg` | Use as-is |

**Closing.** The chapter closes on figure 9.8 (the PIE-trajectory bar chart), transitioning into the methodology critique in the appendix.

---

## 4. AP3 — The Sonomer and the Audiograph  *(reference-heavy; 10–20+ figures)*

**Register.** Reference + prosecution.  This is where everything else lives.  The reader who wants depth comes here; chapter readers don't have to.  AP3 holds the entire atlas as a reference document, plus the methodology critique.

| Section | Figures | Source |
|---|---|---|
| AP3.1 **Methodology** | The 12-place anatomical axis with distances; the 13-row manner taxonomy; the symbol-to-manner classification table | Reproduce from `figures/vocal_tract/README.md` |
| AP3.2 **The original three** (Sanskrit, Arabic, Korean) — the seed set that motivated the whole atlas | `scatter_sanskrit.svg`, `scatter_arabic.svg`, `scatter_korean.svg` |
| AP3.3 **The full 34-language atlas** — every standalone language chart, ordered by region | All `scatter_<lang>.svg` files |
| AP3.4 **The 5-panel PIE strip layout** — Sanskrit-vs-PIE overlays side-by-side as a single appendix figure | `pie_strip_layout.svg` |
| AP3.5 **The 5 PIE standalone atlases** — each reconstruction as its own chart | `scatter_pie_1862.svg` through `scatter_pie_2020.svg` |
| AP3.6 **The 5 Tamil-vs-PIE overlays** — for completeness, the parallel trajectory | `overlay_tamil_vs_pie_<year>_polished.svg` × 5 |
| AP3.7 **The complete Sanskrit-pairwise table** — all 8 metrics across all 33 atlas languages | Table from `inventory_atlas_analysis.md` |
| AP3.8 **Critique notes** — anticipated orthodox responses, methodology critique, the genetic-vs-areal deflection, Schleicher's bake | Lifted from `inventory_atlas_critique.md` |

---

## 5. The polemic trajectory the figure plan enables

Reading order matters.  Each chapter advances one stage of the argument; the figures land each stage.

**Ch 7** — *here is the mouth (anatomy).*  Foundation; no contestation yet.  The vocal-tract diagram is the descriptive anchor.

**Ch 8** — *here is the engineered varṇamālā mapping the mouth (curation).*  Sanskrit's engineering shown as engineering; comparison hinted but not deployed.  The annotated Sanskrit chart is the polemic centrepiece.

**Ch 9** — *here is the data showing other languages' inventories nesting inside the curation (containment evidence).*  Three movements:

- **Movement 1 (9.1–9.4)** — the cluster claim.  Southern subcontinental + Munda languages all nest inside Sanskrit; Brahui's areal exception confirms the rule.
- **Movement 2 (9.5–9.7)** — geography-independence + the orthodox-IE failure.  Korean nests at 87%; English at 50%; Farsi at 44%.  The orthodoxy's "Indo-Iranian closeness" claim has no inventory-level corroboration.
- **Movement 3 (9.8)** — the PIE trajectory.  Even the orthodoxy's own ancestor reconstruction has DRIFTED from Sanskrit over 150 years.  The reconstruction project's instability is itself evidence against treating it as an empirical anchor.

**AP3** — *here is the entire dataset, methodology, and critique catalogue for the serious reader.*  The dossier behind the chapter claims.  Holds the full atlas, the 8-metric pairwise tables, the methodology critique, the named-source citations.

---

## 6. Build queue

What's already built (just deploy):

- All 34 standalone atlas charts (`scatter_<lang>.svg`)
- All 5 PIE standalone charts (`scatter_pie_<year>.svg`)
- 7 Sanskrit-vs-X polished overlays (Tamil, Santali, Brahui, Korean, English, Farsi, Arabic)
- 5 Sanskrit-vs-PIE polished overlays
- 5 Tamil-vs-PIE polished overlays
- The PIE trajectory bar chart (`pie_trajectory_bar_chart.svg`)
- The 5-panel PIE strip layout (`pie_strip_layout.svg`)

What still needs to be built:

1. **The cluster rosette (Fig 9.1)** — 3-language version (Tamil + Telugu + Santali) on the Sanskrit shell.  Build as a `--style rosette` mode on the overlay script.
2. **The Ch 7 anatomy diagram (Fig 7.1)** — strip an existing polished overlay down to the ribbon + place labels (BIL/LD/…/GLO) with no data.
3. **The Ch 7 *Oṃ* sweep (Fig 7.2)** — small bespoke figure.
4. **The Ch 8 annotated Sanskrit chart (Fig 8.1)** — add *varga* labels along the right edge of `scatter_sanskrit.svg`.
5. **The Ch 8 snap-to-grid demonstration (Fig 8.2)** — show "places not used" as annotation.
6. **The Ch 8 engineered ribbon (Fig 8.3)** — highlight the 5 *varga* columns + annotate the empty columns.

The rosette and the Ch 8 annotation layer are the two biggest unbuilt items.  Anatomy diagrams (Ch 7) are small bespoke figures that can be built when the chapter draft is closer to lock.

---

## 7. Figure budgets

Trade nonfiction typically carries 2–4 figures per body chapter, with appendices holding much more.  This plan respects that:

| Chapter / Appendix | Figure count |
|---|---:|
| Ch 7 | 2–3 |
| Ch 8 | 3–4 |
| Ch 9 | 6–8 |
| AP3 | 20+ |

Ch 9's higher count is justified by its evidence role.  AP3 holds the rest of the atlas as reference.

---

## 8. Source files cross-reference

For build / regeneration:

- All language configs: `figures/vocal_tract/configs/scatter_*.json`
- All PIE configs: `figures/vocal_tract/configs/scatter_pie_*.json`
- Build pipeline:
  - `figures/vocal_tract/vocal_tract_scatter.py` — single-language standalone atlas
  - `figures/vocal_tract/vocal_tract_overlay.py` — two-language polished overlay
  - `figures/vocal_tract/pie_trajectory_chart.py` — PIE trajectory bar chart
  - `figures/vocal_tract/pie_strip_layout.py` — 5-panel PIE strip
- Build outputs: `figures/build/vocal_tract/*.svg`
- Working notes: `working/inventory_atlas_*.md`
- Technical reference: `figures/vocal_tract/README.md`

All artifacts are version-controlled and deterministically reproducible from the JSON configs + scripts.

---

*Plan authored alongside the inventory atlas work, summarising commits through f74357a (PIE trajectory deliverables).  Update as figures land and chapter drafts lock.*

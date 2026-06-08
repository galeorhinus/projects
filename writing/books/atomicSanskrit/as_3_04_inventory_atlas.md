# Appendix Part 4 — The Subcontinental Sound-Field: Inventory Atlas and Control Surveys

---

*Draft scaffold (2026-06-08). This appendix carries the field-level
material Chapter 8 promises but does not develop in full: the
inventory-atlas methodology, the Santali-inclusive Munda control, the
Northwest Frontier survey, the Iranian / Caucasus / Slavic external
controls, and the coverage cascade summary. Body sections are
placeholders pending the prose pass.*

## 4.1 The Atlas Method in Depth

The atlas asks one physical question: when a language treats a consonant as a contrastive coordinate, where does that consonant sit on a shared mouth-map?

Everything else follows from that question. The atlas does not measure vocabulary, descent, prestige, script, age, or any of the classificatory buckets the orthodoxy has constructed. It records the single fact a place × manner matrix can record: which body-anchored coordinates each language carries as independent contrastive slots.

**The horizontal axis carries twelve places.** Each language's consonants land on a 12-column axis that runs from lips to glottis along the human vocal tract:

| Col | Sanskrit anchor | Standard label | Body location |
|---:|---|---|---|
| 0 | **ओष्ठ्य** (*oṣṭhya*) | bilabial | both lips meeting |
| 1 | — | labio-dental | lower lip to upper teeth |
| 2 | — | interdental | tongue tip between teeth |
| 3 | **दन्त्य** (*dantya*) | dental | tongue against upper teeth |
| 4 | — | alveolar | tongue against alveolar ridge |
| 5 | — | post-alveolar | tongue blade behind alveolar ridge |
| 6 | **मूर्धन्य** (*mūrdhanya*) | retroflex | tongue tip curled toward palate ridge |
| 7 | **तालव्य** (*tālavya*) | palatal | tongue body toward hard palate |
| 8 | **कण्ठ्य** (*kaṇṭhya*) | velar | tongue back toward soft palate |
| 9 | — | uvular | tongue back against uvula |
| 10 | — | pharyngeal | tongue root toward pharynx wall |
| 11 | — | glottal | vocal folds |

The five Sanskrit-named places (BIL, DEN, RET, PAL, VEL) appear with their *sthāna* names. The seven other columns carry standard labels alone because Sanskrit's selected grid does not stop at those coordinates — the five *sthāna* names mark Sanskrit's selection from a broader anatomical possibility space the human voice can reach.

**The vertical axis carries thirteen manners.** Thirteen manner rows describe how the consonant is shaped at its place: five stop rows (voiceless unaspirated, voiceless aspirated, voiced unaspirated, voiced aspirated, ejective), two affricate rows (voiceless, voiced), two fricative rows (voiceless, voiced), and one each for nasal, lateral, tap-or-trill, and approximant / glide. The two aspirated stop rows are Sanskrit's *mahāprāṇa* row pair, set apart by the strip preset described below. The ejective row appears for languages carrying the Caucasian or Native American glottal-pressure system; Sanskrit does not light it.

**The mahāprāṇa-strip preset isolates the base field.** Chapter 8 §8.3 defines a 23-cell Sanskrit base by holding aside the ten *mahāprāṇa* stop cells: **ख छ ठ थ फ** and **घ झ ढ ध भ**. This is a sensitivity check, not a demotion of breath-pressure engineering. Sanskrit's vertical breath axis remains structural; what Chapter 8 needs is the base field isolated from the breath layer Sanskrit stacks on top. Mathematically, the preset removes manner rows 1 (voiceless aspirated) and 3 (voiced aspirated) from every language's harmonized cell set before the comparison runs. If a comparison language carries aspirated stops, those cells are removed too. The atlas is therefore measuring not "what coverage exists across all manner rows" but "what coverage exists across the rows Sanskrit's base lights."

**The field-versus-coordinate distinction is what keeps the comparison honest.** Chapter 8 §8.2 introduces it. The full depth matters here.

A *spoken sound-field* is the set of acoustic realizations a language's speakers can and do produce. It includes allophonic variation, contextual realization, dialect-level variation, and the long tail of phonetic detail a careful field-phonetician would record.

A *sonomeric coordinate* is a contrastive unit the language promotes into its inventory as an independent slot. Two sounds occupy two coordinates only if the language treats them as distinct word-making units.

Tamil speakers produce voiced stop sounds in real speech. Tamil's contrastive inventory does not promote those voiced realizations to independent voiced-stop coordinates the way Sanskrit does. The atlas records the latter, not the former. The same caution governs aspirated stops, palatal-versus-post-alveolar distinctions, and any other case where a language's spoken field contains material its inventory does not formally credit. The atlas operates at the inventory layer because Sanskrit's engineering operates at the inventory layer.

**The coverage criterion is union, not ranking.** For each three-language comparison set, the atlas counts a Sanskrit cell as *covered* if at least one of the three languages lights that cell. The union-coverage criterion is the right metric for the question Chapter 8 asks: does the subcontinental field — or some other region — supply enough material to make Sanskrit's base recoverable?

The coverage number is therefore not a per-language ranking. Three languages collectively covering 20 of 23 cells does not mean each language carries 20 of those cells; it means the union of their three inventories intersects Sanskrit's base in 20 places. A language that contributes only three or four cells to the union can still be load-bearing for the count if those cells are otherwise unfilled.

**Inventory provenance is open.** The eleven surveys are computed against a harmonized set of phonemic inventories drawn from standard linguistic descriptions per language. The Python generator `figures/_shared/toolkits/vocal_tract/configs/_generate_new_configs.py` carries every inventory in one place alongside its reference work — Padgett (2003) and Yanushevskaya & Bunčić (2015) for Russian; Tegey & Robson (1996) and Bečka (1969) for Pashto; Schulze (2000), Stilo (2008), and Pirejko (1976) for Talysh; and so on for each comparison language. Anyone who wants to test an alternative inventory choice can edit the file, regenerate the JSON, and rebuild the figure. The reproducibility bundle accompanies the figure pipeline rather than living as an opaque dataset behind the figures.

The inventory choices are conservative and editorial. The verification flags are tracked at the working-doc level in `working/inventory_atlas_coverage_surveys.md` §5: Pashto's full retroflex set, Greek's lack of phonemic /h/, the aspirated/ejective affricate collapse Armenian and Georgian carry, and the single Burushaski symbol (ʈʂ) the harmonizer's manner taxonomy does not have a row for. These are visible to any reader who wants the data trail.

The method is therefore narrow, reproducible, and editorial-trail-friendly. It does not prove a thesis by itself. What it does is make the question Chapter 8 asks answerable in numbers the reader can audit.

## 4.2 Santali-Inclusive Munda Control: 18 of 23

**[CONTROL FIGURE PROSE — Pass 4.]**

![Figure A.4.1 — Munda Survey: 18 of 23 Sanskrit base coordinates. Korku, Mundari, and Santali cover 18 of the 23 cells the body's Forest-Belt Survey also covers — the same unfilled set (ण · स · ष · श · ल). Santali's heavier Indic absorption does not move the count.](figures/superset/sk_korku_mundari_santali.svg){#fig:app4-munda-survey width=90%}

## 4.3 Santali-Free Mixed Control: 18 of 23

**[CONTROL FIGURE PROSE — Pass 4.]**

![Figure A.4.2 — Mixed Control: 18 of 23 Sanskrit base coordinates. Korku, Mundari, and Burushaski (a north-western isolate) reach the same 18-cell coverage as the all-Munda control — geographic adjacency to the subcontinent matters more than family-tree classification.](figures/superset/sk_korku_mundari_burushaski.svg){#fig:app4-mixed-control width=90%}

## 4.4 Dispersed *"Austro-Asiatic"* Survey: 15 of 23

**[CONTROL FIGURE PROSE — Pass 4.]**

![Figure A.4.3 — Dispersed Survey: 15 of 23 Sanskrit base coordinates. Sora (Eastern Ghats), Khasi (Meghalaya hills), and Nicobarese (Nicobar Islands) — three orthodoxy-*"Austro-Asiatic"*-classified languages across three geographically remote subcontinental poles — cover only 15 cells. The single family label does not predict shared sound-field structure.](figures/superset/sk_sora_khasi_nicobarese.svg){#fig:app4-dispersed-survey width=90%}

## 4.5 Northwest Frontier Survey: 20 of 23

**[CONTROL FIGURE PROSE — Pass 4.]**

![Figure A.4.4 — Northwest Frontier Survey: 20 of 23 Sanskrit base coordinates. Pashto, Nuristani, and Burushaski together cover the same 20 cells the southern Tamil + Toda + Kurukh set covers — same unfilled letters (ल · स · श). The retroflex contact zone is what allows the north-western frontier to match the deep south.](figures/superset/sk_pashto_nuristani_burushaski.svg){#fig:app4-nw-frontier-survey width=90%}

## 4.6 Iranian Survey: 13 of 23 (Non-Contact Zone)

**[CONTROL FIGURE PROSE — Pass 4.]**

![Figure A.4.5 — Iranian Survey: 13 of 23 Sanskrit base coordinates. Farsi, Kurdish, and Talysh — three orthodoxy-classified Iranian languages outside the north-western subcontinental contact zone — cover only 13 cells, the same coverage the random external English + Arabic + Farsi mix delivers. Replacing Talysh with Balochi (a NW-frontier Iranian language that did acquire retroflex) raises the count to 16/23. Iranian *classification* predicts nothing; subcontinental *contact* does.](figures/superset/sk_farsi_kurdish_talysh.svg){#fig:app4-iranian-survey width=90%}

## 4.7 Caucasus Survey: 10 of 23

**[CONTROL FIGURE PROSE — Pass 4.]**

![Figure A.4.6 — Caucasus Survey: 10 of 23 Sanskrit base coordinates. Armenian (orthodoxy-IE), Georgian (Kartvelian — outside the IE classification), and Ossetian (Iranian) cover only 10 of Sanskrit's base — the lowest of all eleven surveys. Three orthodox family labels collide in one geographic region, and the coverage falls because geography is what matters.](figures/superset/sk_armenian_georgian_ossetian.svg){#fig:app4-caucasus-survey width=90%}

## 4.8 Slavic & Caucasus IE Survey: 11 of 23

**[CONTROL FIGURE PROSE — Pass 4.]**

![Figure A.4.7 — Slavic & Caucasus IE Survey: 11 of 23 Sanskrit base coordinates. Russian, Ukrainian, and Ossetian — three orthodoxy-IE languages spanning the steppe corridor — cover 11 cells. The "IE inheritance" framing predicts nothing about coverage of Sanskrit's base; geographic distance from the subcontinent does.](figures/superset/sk_russian_ukrainian_ossetian.svg){#fig:app4-slavic-caucasus-survey width=90%}

## 4.9 The Coverage Cascade

**[SUMMARY SECTION — Pass 5.]**

To carry: the full eleven-survey summary table (body figures + appendix
controls, coverage numbers, unfilled cells), the contact-vs-classification
finding (geography moves the count, family-tree classification does not),
and the editorial split — why these seven figures live in the appendix
rather than the body.

---

## Draft notes (Appendix Part 4 v1)

**Purpose:** field-level supplement to Chapter 8. The body chapter
runs four surveys (Southern, Forest-Belt, Western IE, Central Asian)
as a four-step polemic ladder. This appendix carries the seven
controls and the deep methodology so the body chapter can stay
compact without losing the empirical backbone.

**Section spine:**

- §4.1 atlas method in depth (axis, strip preset, field-vs-coordinate,
  union-coverage, inventory provenance)
- §§4.2–4.8 seven control surveys with one figure each
- §4.9 coverage cascade summary

**Cross-references:**
- Chapter 8 §8.7 promises this appendix and points readers here
- Chapter 16 will reach back here for the retroflex-band figure
  context
- Body figures live at `figures/superset/sk_tamil_toda_kurukh.svg`,
  `sk_korku_mundari_ho.svg`, `sk_english_french_greek.svg`,
  `sk_tajik_kazakh_kyrgyz.svg`
- Appendix figures live at `figures/superset/sk_korku_mundari_santali.svg`
  and the six wider-canvas variants
- Working analysis at `working/inventory_atlas_coverage_surveys.md`
  carries the full coverage table and per-figure notes

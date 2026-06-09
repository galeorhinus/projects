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

The body's Forest-Belt Survey held Santali aside because the orthodoxy treats Santali as Indic-influenced. The Santali-inclusive control runs the same comparison with Santali in place of Ho and demonstrates that the editorial protection costs no coverage.

The figure replaces Ho with Santali: Korku, Mundari, and Santali. The count holds at 18 of 23 — identical to the body's Forest-Belt set. The unfilled letters are also identical: **ण · स · ष · श · ल**. The *dantya* / *tālavya* line where Sanskrit's place-coding decisions diverge from the broader subcontinental alveolar / post-alveolar placement remains the same set of cells.

![Figure A.4.1 — Munda Survey: 18 of 23 Sanskrit base coordinates. Korku, Mundari, and Santali cover the same 18 cells the body's Forest-Belt Survey covers, with the same unfilled set (ण · स · ष · श · ल).](figures/superset/sk_korku_mundari_santali.svg){#fig:app4-munda-survey width=90%}

Santali's heavier Indic absorption does not move the count. The unfilled cells are not what Santali borrowed from Sanskrit; they are what Sanskrit chose to place differently from the broader subcontinental field. Switching Ho for Santali leaves the geographic verdict intact. The forest belt carries 18 of Sanskrit's 23 base coordinates regardless of which three forest-belt languages are sampled.

## 4.3 Santali-Free Mixed Control: 18 of 23

The Mixed Control combines two Munda-classified languages — Korku and Mundari — with Burushaski, the Hunza Valley language-isolate sitting outside every family tree the subcontinent carries.

![Figure A.4.2 — Mixed Control: 18 of 23 Sanskrit base coordinates. Korku, Mundari, and Burushaski reach the same 18-cell coverage as the all-Munda control; Burushaski's retroflex inventory exchanges one unfilled cell for another but does not move the count.](figures/superset/sk_korku_mundari_burushaski.svg){#fig:app4-mixed-control width=90%}

The figure substitutes Burushaski for Santali and reaches the same 18 of 23 coverage. The unfilled set differs slightly from the Munda-pure surveys: **ण · स · श · ल · र**. Burushaski's retroflex inventory covers cells the all-Munda set leaves open, but trades the gain against the alveolar tap / trill र, which Burushaski places at a different coordinate.

The substitution forecloses two orthodox deflections at once. Santali is excluded — Indic absorption cannot explain the coverage. The all-Munda framing is broken — the family-resemblance argument cannot explain it either. What survives is the geographic explanation. Three languages drawn from three different orthodoxy classifications, all sitting in or adjacent to the central forest belt and the north-western frontier, cover the same 18 cells the Forest-Belt and Munda Surveys cover.

## 4.4 Dispersed *"Austro-Asiatic"* Survey: 15 of 23

The orthodoxy classifies Munda alongside two other branches under the umbrella *"Austro-Asiatic"*: a Khasian branch in the Meghalaya highlands and a Nicobaric branch on the Nicobar Islands. The three branches sit at geographically remote subcontinental poles.

The Dispersed Survey picks one representative from each branch: Sora (South Munda, Eastern Ghats and Rushikulya basin), Khasi (Meghalaya highlands), and Nicobarese (Car Nicobar). Coverage falls to 15 of 23. The unfilled set expands to **ट · ड · ण · स · ष · श · ल · र** — eight cells, three more than the Munda-pure Forest-Belt set the body uses.

![Figure A.4.3 — Dispersed Survey: 15 of 23 Sanskrit base coordinates. Sora, Khasi, and Nicobarese — three languages the orthodoxy classifies under one *"Austro-Asiatic"* umbrella across three remote subcontinental poles — cover three fewer cells than the all-Munda Forest-Belt Survey.](figures/superset/sk_sora_khasi_nicobarese.svg){#fig:app4-dispersed-survey width=90%}

The collapse is informative. The single orthodoxy label *"Austro-Asiatic"* predicts that these three languages should share structural sound-field properties. They do not. Sora's South Munda inventory lacks the retroflex stops that North Munda carries; Khasi runs voiceless-aspirated stops as the Mon-Khmer signature; Nicobarese carries neither retroflex nor aspirated stops. Three languages under one orthodox umbrella deliver three different inventory shapes, and their union covers less of Sanskrit's base than any all-subcontinental control.

The family label is not structural. Geography is structural — and inside the *"Austro-Asiatic"* umbrella the geography is dispersed across three remote regions of the subcontinent.

## 4.5 Northwest Frontier Survey: 20 of 23

This is the deepest result in the appendix.

Three north-western contact-zone languages — Pashto (orthodoxy-Iranian, Afghanistan and Pakistan tribal belt), Nuristani (a separate IE branch isolated in the Hindu Kush valleys), and Burushaski (the Hunza Valley isolate) — cover 20 of 23. The unfilled cells are exactly the three the body's Southern Survey (Tamil + Toda + Kurukh) leaves unfilled: **ल · स · श**.

![Figure A.4.4 — Northwest Frontier Survey: 20 of 23 Sanskrit base coordinates. Pashto, Nuristani, and Burushaski cover the same 20 cells the deep-south Tamil + Toda + Kurukh set covers, with the same unfilled triple (ल · स · श). Two geographically opposite ends of the subcontinent deliver the same count.](figures/superset/sk_pashto_nuristani_burushaski.svg){#fig:app4-nw-frontier-survey width=90%}

Two geographically opposite sets — deep south and north-western frontier — deliver the same count with the same unfilled list. The pattern is geographic, not classificatory. Both regions sit inside the subcontinental retroflex contact zone, and both consequently carry the cells Sanskrit's base lights.

The set is also taxonomically mixed. Pashto is orthodoxy-Iranian; Nuristani is a separate IE branch the orthodoxy classifies neither as Indic nor as Iranian; Burushaski is classified as a language-isolate. Three orthodox classifications do not predict why the survey ties the southern set. The geography does.

This is Chapter 8's claim verified at the opposite geographic pole. The frontier-zone Iranian and isolate inventories acquired the retroflex column from the same subcontinental contact zone the deep-south languages preserve. The Iranian and isolate classifications predict nothing once geographic position is held constant.

## 4.6 Iranian Survey: 13 of 23 (Non-Contact Zone)

The Iranian Survey is the Northwest Frontier Survey's geographic mirror image.

Three Iranian languages outside the north-western contact zone — Farsi (Iran), Kurdish Kurmanji (northern Iraq, Syria, eastern Turkey), and Talysh (Caspian littoral, Azerbaijan and northern Iran) — cover only 13 of 23. The unfilled set runs **ट · च · ड · ज · ण · ञ · स · ष · श · र**: ten cells, including the entire retroflex column.

![Figure A.4.5 — Iranian Survey: 13 of 23 Sanskrit base coordinates. Three Iranian languages outside the north-western subcontinental contact zone cover the same number of Sanskrit's base cells as three random external languages. The retroflex column the Northwest Frontier Survey lit is here entirely unfilled.](figures/superset/sk_farsi_kurdish_talysh.svg){#fig:app4-iranian-survey width=90%}

The 13/23 number is the same coverage a random external English + Arabic + Farsi mix delivers. Three languages the orthodoxy classifies as Sanskrit's "Iranian sister branch" cousins cover no more of Sanskrit's base than three external languages do.

The contact / non-contact contrast is the key axis. Swapping Talysh for Balochi — a north-western frontier Iranian language that did acquire retroflex from the subcontinental contact zone — moves coverage from 13 to 16. The exact 3-cell jump is the retroflex column **ट · ड · र** that Balochi carries and Caspian-littoral Iranian does not. The "Iranian" classification predicts nothing once contact is held constant. What predicts the coverage is whether the Iranian language sat inside the subcontinental contact zone.

The body's framing flag for this finding: not "Iranian languages cover Sanskrit modestly" but "Iranian languages without subcontinental contact cover Sanskrit's base no better than three random external languages do."

## 4.7 Caucasus Survey: 10 of 23

The Caucasus Survey is the floor of the eleven-survey set.

Three languages from three different orthodox classifications, all from the Caucasus region: Armenian (a separate IE branch), Georgian (Kartvelian / South Caucasian, outside the IE classification altogether), and Ossetian (Iranian, north Caucasus). Coverage falls to 10 of 23 — lower than any other survey in the set. The unfilled list runs **ट · च · ड · ज · ण · ञ · ङ · स · ष · श · ल · र · व**: thirteen cells, the largest unfilled list of any survey.

![Figure A.4.6 — Caucasus Survey: 10 of 23 Sanskrit base coordinates. Three orthodox classifications collide in one geographic region — and the floor coverage of all eleven surveys appears at exactly that point. Geographic distance from the subcontinent is what moves the number.](figures/superset/sk_armenian_georgian_ossetian.svg){#fig:app4-caucasus-survey width=90%}

The result is methodologically clean. Three orthodox classifications collide inside one geographic region; no classification rescues the coverage. The Caucasus is far enough from the subcontinent that geographic distance dominates every other variable, and the Caucasus sits at the floor.

## 4.8 Slavic & Caucasus IE Survey: 11 of 23

The Slavic & Caucasus IE Survey runs three IE-classified languages along the steppe corridor: Russian and Ukrainian from East Slavic, Ossetian from Caucasian Iranian. Coverage reaches 11 of 23, one cell above the Caucasus floor.

![Figure A.4.7 — Slavic & Caucasus IE Survey: 11 of 23 Sanskrit base coordinates. Three IE-classified languages along the steppe corridor cover only one cell more than the Caucasus floor — and considerably less than the body's Western IE and Central Asian sets.](figures/superset/sk_russian_ukrainian_ossetian.svg){#fig:app4-slavic-caucasus-survey width=90%}

What's revealing is the classification. All three languages share the orthodoxy's "Indo-European" label that supposedly makes them Sanskrit's relatives. The shared classification predicts nothing about coverage. East Slavic and Caucasian Iranian together cover less of Sanskrit's base than the body's Western IE Survey at 14/23, and considerably less than the Central Asian Tajik + Kazakh + Kyrgyz at 12/23 — itself classified as a mix of orthodoxy-Iranian and orthodoxy-Turkic.

Two facts emerge. The "Indo-European" classification does not predict coverage at all — the IE-classified sets span 11/23 to 20/23 depending only on which IE languages sat geographically close to the subcontinental contact zone. And the steppe corridor — frequently named as the source field in the orthodox Aryan-migration story — supplies less of Sanskrit's base material than the deep south, the central forest belt, or the north-western frontier.

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

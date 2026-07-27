# Designed Variations: Figure Source Data

**Status:** production overlay for the 83-row declensional inventory  
**Content source:** `working/40_reference/source_material/vaidika_laukika_declensional_variations_complete.md`  
**Evidence source:** `working/10_active/as_vaidika_laukika_83_row_evidence_ledger.md`  
**Passage source:** `working/10_active/as_vaidika_laukika_high_value_passage_concordance.md`  
**Prevalence source:** `working/10_active/as_vaidika_laukika_prevalence_ledger.md`  
**Figure-ready numerical data:** `working/10_active/as_vaidika_laukika_prevalence_figure_data.csv`

## How the Figure Builder Should Use This File

The complete inventory supplies each row's ending class, *vibhakti*, Vedic
form, and laukika comparison. This file supplies the evidence overlay.
The files must be joined by ID. The prevalence CSV may contain several subrows
for one inventory ID because one grammatical row can preserve more than one
numerical claim. Those subrows must remain separate during illustration.

No row may disappear merely because its function remains open. The figure
should distinguish:

- **FORM** — the grammatical category is documented;
- **PASSAGE** — an exact passage has been checked;
- **FUNCTION** — a local contribution has been demonstrated;
- **OPEN** — the next evidentiary step remains unfinished.

The figure must also preserve the numerical unit. A token count cannot be drawn
as if it measured lexemes, and a ratio reported for an ending class cannot be
replaced by a raw count from one word. Every percentage must retain its
numerator, denominator, scope, and evidence grade in the source data, even when
the designed figure prints only a shortened form.

The qualification column uses **RARE, ISOLATED, DOUBTFUL,** and **ABSENCE**.
A blank confirmed-DV cell means that the research plan may contain candidate
codes, but the publication figure must not print them yet.

## *Ekavacanam*

| ID | Evidence | Qualification | Confirmed DV | Figure instruction |
|---|---|---|---|---|
| SG-01 | FORM · PASSAGE · FUNCTION | — | MAT · ARR | Use ***महित्वा (*mahitvā*)*** at RV 2.15.6a; keep ***यज्ञा*** as an unlocated grammar example. |
| SG-02 | FORM · PASSAGE · FUNCTION | — | MAT · ARR | Use ***मनीषा (*manīṣā*)*** at RV 10.129.4d. |
| SG-03 | FORM · PASSAGE · OPEN | — | — | Use ***पश्वा (*paśvā*)*** only as passage verification; do not claim meter until its resolved form is scanned. |
| SG-04 | FORM · OPEN | RARE | — | Attach RARE only to occasional **-i** and **-inā**, not to the common contraction. |
| SG-05 | FORM · OPEN | RARE | — | Identify the small adverbial **-uyā** class. |
| SG-06 | FORM · PASSAGE · FUNCTION | — | MAT · ARR | Use ***शिश्वे (*śiśve*)*** at RV 2.34.8c. |
| SG-07 | FORM · OPEN | RECURRING | — | Morphological review finds inserted **n** in 1/18 checked tokens. |
| SG-08 | FORM · OPEN | — | — | Retain without a DV code. |
| SG-09 | FORM · OPEN | RARE | — | Split common **-yaḥ / -vaḥ** from very rare masculine **-unaḥ**. |
| SG-10 | FORM · PASSAGE · OPEN | — | — | Use ***अग्ना (*agnā*)*** at RV 8.27.3b; function remains open. |
| SG-11 | FORM · PASSAGE · FUNCTION | RARE | REL · REC | Use ***वेदी अस्याम् (*vedī asyām*)*** at RV 2.3.4b and mark *pragṛhya*. |
| SG-12 | FORM · PASSAGE · FUNCTION | DOUBTFUL in part | MAT · ARR for **-avi** | Split verified **-avi** from doubtful **-ayi**. |
| SG-13 | FORM | ABSENCE | — | Draw as a distribution note, not as an alternate Vedic ending. |
| SG-14 | FORM · OPEN | ABSENCE · one doubtful exception | — | Use an absence treatment with doubtful *bhiyāi* once. |
| SG-15 | FORM · PASSAGE · FUNCTION | — | MAT · ARR | Cross-reference SG-02; both use the ***मनीषा*** passage. |
| SG-16 | FORM · OPEN | DOMINANT in checked lexeme | — | Show *śamī/śami : śamyā* as 8:2. |
| SG-17 | FORM · OPEN | ISOLATED | — | Use the single checked *gaurī* locative. |
| SG-18 | FORM · OPEN | UNKNOWN | — | Whitney's *kartarī* and VedaWeb's *kartari* require reconciliation. |
| SG-19 | FORM · PASSAGE · FUNCTION · OPEN | — | MAT · ARR for endingless locative | Use ***मूर्धन् (*mūrdhan*)*** at RV 9.17.6b; keep fuller and reduced subcategories open. |
| SG-20 | FORM · PASSAGE · OPEN | RARE | — | Use ***महिना (*mahinā*)*** at RV 10.28.7d; print no DV code. |
| SG-21 | FORM · PASSAGE · OPEN | — | — | Use ***भूमना (*bhūmanā*)*** at RV 10.31.6b; print no DV code. |
| SG-22 | FORM · PASSAGE · OPEN | — | — | Use ***हरिवः (*harivaḥ*)*** at RV 8.2.13c; direct address is verified, alternate-ending purpose is open. |
| SG-23 | FORM · PASSAGE · OPEN | — | — | Use ***चिकित्वः (*cikitvaḥ*)*** at RV 3.25.1c; direct address is verified, alternate-ending purpose is open. |
| SG-24 | FORM · PASSAGE · OPEN | RARE | — | Use ***ओजीयः (*ojīyaḥ*)*** at RV 10.120.4c; print no DV code. |
| SG-25 | FORM · OPEN | RARE / DOUBTFUL in part | — | Omit the doubtful member from any displayed example. |
| SG-26 | FORM · OPEN | RECURRING | — | Morphological review gives instrumental *tvā : tvayā* as 5:45. |
| SG-27 | FORM · PASSAGE · FUNCTION | N/A · absolute counts | REL · REC | Use ***युष्मे इत् (*yuṣme id*)*** and ***त्वे इत् (*tve id*)*** as *pragṛhya* examples. |
| SG-28 | FORM · OPEN | RECURRING · absolute counts | — | Preserve *enā* 38 and *ayā* 25 as separate dots. |
| SG-29 | FORM · OPEN | ISOLATED | — | One instrumental token survives morphological review. |

## *Dvivacanam*

| ID | Evidence | Qualification | Confirmed DV | Figure instruction |
|---|---|---|---|---|
| DU-01 | FORM · PASSAGE · OPEN | — | — | Use ***अश्विना (*aśvinā*)*** at RV 1.34.1b; function remains open. |
| DU-02 | FORM · OPEN | — | — | Retain without a DV code. |
| DU-03 | FORM · OPEN | — | — | Retain as a class summary; selected classes still need passages. |
| DU-04 | FORM · PASSAGE · OPEN | — | — | Use ***देवी (*devī*)*** at RV 10.70.6a; do not repeat the rejected metrical claim. |
| DU-05 | FORM · OPEN | ISOLATED · uncertain in part | — | Show one short token and one later-form candidate; keep *mahi* open. |
| DU-06 | FORM · OPEN | ISOLATED | — | Display only after locating the single example. |
| DU-07 | FORM · OPEN | DOMINANT provisionally · 12 tokens | — | Preserve the fuller-form count without inventing a class denominator. |
| DU-08 | FORM | DOUBTFUL | — | Retain with the doubtful marker and an open prevalence cell; do not present the form as verified. |
| DU-09 | FORM · PASSAGE · FUNCTION | — | SEM · REL | Use the five exact second-person dual passages in the concordance. |
| DU-10 | FORM · PASSAGE · OPEN | — | — | Display both ***युवभ्याम् / युवाभ्याम्***; no DV code yet. |
| DU-11 | FORM · PASSAGE · FUNCTION | — | SEM · REL | Use ***एनोः (*enoḥ*)*** at RV 7.103.4a. |
| DU-12 | FORM · OPEN | ISOLATED | — | Locate the single passage before display. |

## *Bahuvacanam*

| ID | Evidence | Qualification | Confirmed DV | Figure instruction |
|---|---|---|---|---|
| PL-01 | FORM · PASSAGE · FUNCTION | — | MAT · ARR | Use ***देवासः (*devāsaḥ*)*** at RV 1.3.7b. |
| PL-02 | FORM · PASSAGE · FUNCTION | RARE | MAT · ARR | Use ***वशासः (*vaśāsaḥ*)*** at RV 6.63.9d. |
| PL-03 | FORM · PASSAGE · OPEN | — | — | Use ***देवीः (*devīḥ*)*** at RV 9.5.8d; function remains open. |
| PL-04 | FORM · OPEN | N/A · absolute counts | — | Use *devīḥ* as 37 nominative and 5 accusative tokens. |
| PL-05 | FORM · OPEN | RARE | — | Split unstrengthened **-ias / -uas** from feminine **-īs**. |
| PL-06 | FORM · OPEN | UNKNOWN | — | Flag the source-annotation disagreement for the listed accusative forms. |
| PL-07 | FORM · PASSAGE · FUNCTION | — | MAT · ARR | Use ***विश्वा (*viśvā*)*** at RV 8.70.6b. |
| PL-08 | FORM · OPEN | — | — | Retain without a DV code. |
| PL-09 | FORM · OPEN | — | — | Retain without a DV code. |
| PL-10 | FORM · OPEN | — | — | Retain without a DV code. |
| PL-11 | FORM · OPEN | ISOLATED in RV | — | Display the source-reported **2 RV passages** and state that the exact passages remain open. |
| PL-12 | FORM · PASSAGE · FUNCTION | — | MAT · ARR | Use ***देवेभिः (*devebhiḥ*)*** at RV 1.1.5c and the RV 10.125.1 comparison. |
| PL-13 | FORM · PASSAGE · FUNCTION | — | MAT · ARR · REL | Use ***येभिः (*yebhiḥ*)*** at RV 7.1.7b. |
| PL-14 | FORM · OPEN | N/A | — | Identify this as recitational resolution, not a second written ending. |
| PL-15 | FORM · OPEN | RARE in part | — | Split rare simple **-ām** from recitational resolution of **-ānām**. |
| PL-16 | FORM · PASSAGE · FUNCTION · OPEN | N/A / UNKNOWN | REL · REC for e-form | Use ***युष्मे (*yuṣme*)*** for the e-form; keep **-bhya** open. |
| PL-17 | FORM · OPEN | RARE | — | Mark loss of the final nasal as rare. |
| PL-18 | FORM · OPEN | ISOLATED | — | Identify as two Vājasaneyi Saṃhitā forms; exact passages remain open. |
| PL-19 | FORM · OPEN | DOMINANT | — | Morphological review gives *imā : imāni* as 63:8. |
| PL-20 | FORM · OPEN | COMMON | — | Morphological review gives *yā : yāni* as 50:26. |
| PL-21 | FORM · PASSAGE · FUNCTION | — | MAT · ARR · REL | Use ***येभिः (*yebhiḥ*)*** at RV 7.1.7b. |

## Word Classes

| ID | Evidence | Qualification | Confirmed DV | Figure instruction |
|---|---|---|---|---|
| CL-01 | FORM · OPEN | — | — | Retain as a paradigm-distribution summary. |
| CL-02 | FORM · OPEN | RARE · 3 secure + 2-3 doubtful | — | Retain as a class-redistribution summary. |
| CL-03 | FORM · OPEN | RECURRING · 4 source examples | — | Show examples rather than a percentage. |
| CL-04 | FORM · OPEN | ISOLATED | — | Use *janūs* once and label the broader family summary separately. |
| CL-05 | FORM · OPEN | — | — | Retain the ***अहन् / अहर् / अहस्*** paradigm. |
| CL-06 | FORM · OPEN | — | — | Retain the ***ऊधन् / ऊधर् / ऊधस्*** paradigm. |
| CL-07 | FORM · OPEN | — | — | Retain the four-word class summary. |
| CL-08 | FORM · OPEN | — | — | Retain the ***पन्था / पथि / पथ्*** paradigm. |
| CL-09 | FORM · OPEN | — | — | Retain without a DV code. |
| CL-10 | FORM · OPEN | DOMINANT dual / ISOLATED RV plural | — | Split the reported **6/7** participial-dual share from the **2** RV neuter-plural **-ānti** passages. |

## Numerals

| ID | Evidence | Qualification | Confirmed DV | Figure instruction |
|---|---|---|---|---|
| NU-01 | FORM · OPEN | — | — | Retain without a DV code. |
| NU-02 | FORM · OPEN | COMMON | — | Morphological review gives *trī : trīṇi* as 22:32. |
| NU-03 | FORM · OPEN | ISOLATED | — | Locate the single ***त्रीणाम् (*trīṇām*)*** passage before display. |
| NU-04 | FORM · OPEN | 1:2:3 across six tokens | — | Retain the three-form range and print each count. |
| NU-05 | FORM · PASSAGE · FUNCTION · OPEN | N/A · checked example | SEM · REL | Use ***पञ्च कृष्टिषु (*pañca kṛṣṭiṣu*)***; the second grammar example remains open. |
| NU-06 | FORM · PASSAGE · FUNCTION | N/A · two checked examples | SEM · REL | Use ***सहस्रम् ऋषिभिः*** and ***शतम् पूर्भिः***. |
| NU-07 | FORM · FUNCTION · PASSAGE OPEN | N/A | SVR · REL | The governed accent operation is documented; add an exact audible example later. |

## Accent and Recitation

| ID | Evidence | Qualification | Confirmed DV | Figure instruction |
|---|---|---|---|---|
| AC-01 | FORM · OPEN | N/A | — | Add a paired vocative-accent passage before assigning a code. |
| AC-02 | FORM · OPEN | N/A | — | Select two accent-movement classes before assigning a code. |
| AC-03 | FORM · FUNCTION · PASSAGE OPEN | — | MAT · REC | Present as audible resolution, not as another written ending. |
| AC-04 | FORM · PASSAGE · FUNCTION | — | REC · REL | Use ***वेदी अस्याम्, युष्मे इत्,*** and ***त्वे इत्***. |

## Evidence Progress

| Measure | Count |
|---|---:|
| Inventory rows | 83 |
| Rows with an exact passage | 31 |
| Rows with at least one demonstrated function | 22 |
| Rows requiring a qualification | 26 |
| Rows with a confirmed publication DV code | 22 |
| Rows whose function remains wholly or partly open | 61 |
| Rows carrying at least one retained prevalence number, including a defined zero | 76 |
| Rows with a graphable percentage, bounded percentage, or defined zero | 39 |
| Rows with absolute counts but no complete denominator | 37 |
| Rows still lacking a reliable numerical measurement | 7 |

These measures describe different kinds of progress. A row can have an exact
passage but no complete prevalence denominator, or a source-reported prevalence
ratio while its architectural contribution remains open. The complete figure
series maps the full grammatical range without disguising unfinished analysis
as a finished result.

## Recommended Page Deployment

1. **Codebook and evidence key:** one compact half-page before the first data
   figure.
2. **Ekavacanam:** two facing pages, SG-01–SG-15 and SG-16–SG-29.
3. **Dvivacanam:** one page, DU-01–DU-12, with DU-09 given extra vertical
   space for its five-way paradigm.
4. **Bahuvacanam:** two facing pages, PL-01–PL-11 and PL-12–PL-21.
5. **Word classes and numerals:** two pages; do not force the paradigm-summary
   rows into the narrower ending-row design.
6. **Accent and recitation:** one explanatory page joined to three worked
   examples rather than a four-line standalone table.

At trade size, each data page should show no more than 12–15 ordinary rows.
Rare, isolated, doubtful, and absence markers should remain visible in
grayscale through shape or line style, not color alone.

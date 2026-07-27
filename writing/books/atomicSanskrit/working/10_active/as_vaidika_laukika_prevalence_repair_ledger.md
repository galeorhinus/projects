# Vaidika-Laukika Prevalence Repair Ledger

**Status:** three-pass repair completed for the unresolved and raw-count rows  
**Manuscript impact:** none  
**Figure impact:** numerical and visual-measure guidance only  

## Corpus and Reproduction

The first prevalence pass searched visible spellings in the ten-maṇḍala
Ṛgveda *padapāṭha*. That search found candidates, but a visible form such as
*tvā*, *imā*, or *yā* can perform several grammatical jobs. The repair uses
the morphologically annotated VedaWeb Ṛgveda TEI corpus to separate those
jobs.

- Corpus repository: `c-salt_vedaweb_tei`
- Corpus commit used: `6d94702e078b2d8fc04af1241aba63132c4601a3`
- Local extraction script:
  `analysis/vaidika_laukika/adjudicate_rv_prevalence.py`
- Retained accepted and review records:
  `working/10_active/as_vaidika_laukika_morphological_adjudication.csv`

The VedaWeb repository describes itself as a legacy form of the dataset.
Every extracted row therefore preserves the visible form, lemma,
morphological annotation, passage reference, and decision. A disagreement
between VedaWeb and a grammar remains visible rather than being silently
resolved in favor of either source.

## The Four Figure Measures

The figure should use four distinct measures:

1. **Percentage bars** when the compared forms perform the same grammatical
   job and both numerator and denominator are defined.
2. **Numbered dots** when an exact token, passage, lexeme, form, or paradigm
   count is useful but no honest selection denominator exists.
3. **Range marks** for approximate counts, inequalities, and source-defined
   uncertainty.
4. **Open cells** when the operation is non-quantitative or the evidence
   remains unresolved.

An open cell is not zero. A measured zero requires a declared corpus and a
fully defined search field.

## Pass One: Denominator Decisions

| ID | Denominator decision | Figure measure | Result |
|---|---|---|---|
| SG-07 | Valid within reviewed Ṛgvedic neuter *ikārānta/ukārānta* dative-singular tokens | Bar | Inserted **n** occurs in **1/18 = 5.6%** of the reviewed tokens and in one of five lexemes. |
| SG-14 | No complete class denominator | Dot plus range note | The Veda normally lacks the later expanded endings; Whitney reports one possible exception, *bhiyāi*, and marks it doubtful. |
| SG-16 | Valid within the checked *śamī* instrumental-singular paradigm | Bar | Contracted *śamī/śami* occurs in **8/10 = 80.0%**; *śamyā* occurs twice. |
| SG-17 | One checked lexical occurrence; a percentage would exaggerate the field | Dot | *Gaurī* occurs once as a locative singular. |
| SG-18 | Source and corpus transcription disagree | Open cell | Whitney prints *kartarī*; VedaWeb annotates the sole token as *kartari* at RV 1.139.7f. |
| SG-26 | Valid comparison of instrumental *tvā* and *tvayā* | Bar | *Tvā* is **5/50 = 10.0%**. Another **590** visible *tvā* forms perform other jobs and were excluded. |
| SG-27 | The e-forms cover a wider case range than the later comparison forms | Dots | *Asme* has **212** pronoun tokens and *yuṣme* **6**. No combined percentage is warranted. |
| SG-28 | The two forms are both members of a larger demonstrative field, not a complete pair | Dots | *Enā* has **38** instrumental tokens; *ayā* has **25** after one verbal homograph is removed. |
| SG-29 | The row isolates one grammatical use from twenty homographs | Dot | Only **1** of **21** visible *tyā* tokens is instrumental singular feminine. No *tyayā* token occurs. |
| DU-05 | Source uncertainty and annotation disagreement prevent a class denominator | Dots plus open note | VedaWeb confirms one short *śucī* and one later-form candidate *hariṇī*; Whitney treats the RV later form as uncertain. The source-listed *mahi* still needs passage-level review. |
| DU-07 | Twelve fuller forms are countable, but the complete *an/man/van* dual field is not yet enumerated | Dot | **12** reviewed fuller **-anī/-aṇī** tokens; retain Whitney's qualitative “strongly preferred” statement. |
| PL-04 | The row demonstrates one form serving two relations rather than choosing between alternatives | Dots | For the checked lexeme *devīḥ*, VedaWeb gives **37** nominative-plural and **5** accusative-plural tokens. |
| PL-06 | The source-listed spellings and VedaWeb analyses disagree | Open cell | Whitney calls **-ias/-uas** accusatives sparse; VedaWeb assigns the visible source examples to other relations. |
| PL-14 | Audible resolution is an operation, not a choice between written endings | Open cell marked N/A | Preserve the qualitative source statement and a worked recitational example rather than inventing prevalence. |
| PL-16 | Split the row | Dots plus open cell | Use the SG-27 *asme/yuṣme* dots for the pronoun forms. Keep loss of final nasal in **-bhya** open until an audible corpus can measure it. |
| PL-19 | Valid after removing the masculine-dual homograph | Bar | Neuter-plural *imā : imāni* is **63:8**, so the shorter form is **88.7%**. |
| PL-20 | Valid after removing feminine-singular and masculine-dual homographs | Bar | Neuter-plural *yā : yāni* is **50:26**, so the shorter form is **65.8%**. |
| CL-02 | The grammar gives a closed secure example list but no class denominator | Dot plus range | Three secure RV forms: *dūtiām, śvaśruām,* and *dravitnuā*; two or three further cases are doubtful. |
| CL-03 | The grammar gives examples but no complete occurrence count | Dot | Four illustrated contractions: *āśām, vedhām, surādhās,* and *anāgās*. |
| CL-04 | One exact transition is reported | Dot | *Janūs* occurs once. |
| NU-02 | Valid after morphological filtering | Bar | Neuter-plural *trī : trīṇi* is **22:32**, so *trī* is **40.7%**. |
| NU-04 | Valid six-token numeral field after verbal homographs are removed | Three bars with counts | *Aṣṭa* **1/6**, *aṣṭā* **2/6**, *aṣṭau* **3/6**. |
| NU-05 | A visible count of *pañca* does not measure the uninflected construction | Dot for checked construction | Use the verified *pañca kṛṣṭiṣu* passage; keep the forty visible tokens out of a prevalence bar. |
| NU-06 | Visible counts of *śatam/sahasram* do not measure the construction | Two checked-example dots | Use *sahasram ṛṣibhiḥ* and *śatam pūrbhiḥ*. |
| NU-07 | Accent pattern, not visible-form prevalence | Open cell marked N/A | Demonstrate the operation through an accented paradigm or passage. |
| AC-01 | Sentence-level vocative accent operation | Open cell marked N/A | Select a paired example; do not convert it to a percentage. |
| AC-02 | Family of accent movements | Open cell marked N/A | Select representative ending classes; do not combine them into one rate. |

## Pass Two: Source Forms and Lexical Lists

The following lists replace vague statements such as “a few forms” wherever
the checked grammar supplies the actual members.

| ID | Source forms or lexical members recovered | Source |
|---|---|---|
| SG-07 | Vedic neuter dative **-aye, -ve, -ave**; inserted-**n** forms described as sporadic | Whitney §336d |
| SG-14 | Shorter long-vowel pattern represented by *rathī, nadī,* and *tanū*; the later expanded singular endings are absent in the Veda except doubtful *bhiyāi* once | Whitney §§355-358 |
| SG-16 | *Śamī, śami* beside *śamyā* | Whitney §365b; VedaWeb passages retained in the CSV |
| SG-17 | *Gaurī* | Whitney §365b; RV 9.12.3c |
| SG-18 | *Kartarī* in Whitney; *kartari* in VedaWeb | Whitney §371g; RV 1.139.7f |
| DU-05 | Short *śucī, mahi*; later-form *hariṇī* marked uncertain | Whitney §340h |
| DU-07 | *Ahanī, janmanī, sadmanī, dhāmanī,* and *carmaṇī* occur in the annotated fuller-form set | VedaWeb extraction |
| PL-04 | *Devīḥ* supplies the checked same-form nominative/accusative demonstration | Whitney §§340k-l, 365b; VedaWeb extraction |
| PL-06 | Source examples include *paśvas, madhvas,* and doubtful *śucayas* | Whitney §§340l, 342l |
| CL-02 | *Dūtiām, śvaśruām, dravitnuā*; two or three further cases doubtful | Whitney §358 |
| CL-03 | *Āśām, vedhām, surādhās, anāgās*; resulting parallel forms *āśā, jarā, medhā* | Whitney §415a |
| CL-04 | *Janūs* once | Whitney §415c |
| NU-05 | *Pañca kṛṣṭiṣu; sapta ṛṣīṇām* | Whitney §486c |
| NU-06 | *Sahasram ṛṣibhiḥ; śatam pūrbhiḥ* | Whitney §486c |

This extraction is complete for the source-named examples above. It is not a
claim that every member of each broad declensional class has been enumerated.
Where the grammar itself supplies examples rather than a closed class list,
the figure must label them as examples.

## Pass Three: Morphological Adjudication

The adjudication changed several raw counts materially:

- *Tvā* fell from hundreds of visible matches to **five** instrumental uses.
- *Tyā* fell from twenty-one visible matches to **one** instrumental use.
- *Yā* fell from 159 visible matches in the annotated edition to **fifty**
  neuter-plural uses.
- *Imā* retained **sixty-three** neuter-plural uses after one masculine-dual
  homograph was removed.
- *Aṣṭa* fell from five annotated visible matches to **one** numeral token
  after four forms of another lemma were removed.
- The apparent *PL-06* examples did not survive VedaWeb's case analysis and
  therefore remain open rather than being counted as zero.

The retained CSV contains every accepted or review token with its reference.
Rejected homographs are reproducible by rerunning the script with
`--include-rejected`.

## Remaining Gaps

The repair closes the numerical presentation problem, but it does not erase
the following research gaps:

1. **SG-18:** inspect the scanned grammar and the accented RV editions to
   determine why Whitney reads *kartarī* where VedaWeb gives *kartari*.
2. **DU-05:** review *mahi* passage by passage and reconcile Whitney's
   “perhaps once” later-form statement with the corpus annotation.
3. **DU-07:** enumerate the complete RV neuter dual field for
   *an/man/van*-ending words before assigning a percentage.
4. **PL-04:** a full class percentage requires a defensible division between
   inherited long-vowel words and derivative *īkārānta* words. The *devīḥ*
  lexical demonstration is secure without that ending-class division.
5. **PL-06:** reconcile Whitney's analysis with modern morphological
   annotation and inspect the original passages.
6. **PL-14 / PL-16 / NU-07 / AC-01 / AC-02:** these need an accented or
   audible corpus and worked passages, not additional spelling counts.
7. **NU-05 / NU-06:** a full prevalence rate would require syntactic
   annotation of every numeral construction. The existing checked examples
   are sufficient for a numbered-dot figure measure.

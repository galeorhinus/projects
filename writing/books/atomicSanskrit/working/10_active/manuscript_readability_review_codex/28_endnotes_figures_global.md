# Endnotes, Figures, and Global Review

The manuscript remains unchanged until a decision is selected here. These decisions control later mechanical or cross-file work and should be approved before application.

## GLOBAL-001 - Replace the production introduction to the expanded endnotes

**Source:** [Expanded endnotes opening](/Users/paragtope/projects/writing/books/atomicSanskrit/as_endnotes.md:1)  
**Action:** REPLACE  
**Status:** OPEN  
### Original

> # Atomic Sanskrit — Endnotes (Expanded Prose)
>
> > **Status:** Reference file for expanded endnote prose. Endnote stubs throughout the chapter drafts are marked inline as `[NOTE: stub-name]`. As stubs are expanded into full endnote prose, the expanded version lives here, keyed by stub name. Each entry includes the deployment locations (which chapters/sections cite the endnote) so the prose can be revised once and the revision propagates to all citations.
> >
> > Convention: each endnote begins with its stub name as a level-3 heading. The prose follows. Length varies — most endnotes are 50–200 words (standard citation-plus-context); a few central endnotes are longer (400–800 words) where the supporting analysis is substantive.
> >
> > Endnote production sessions accumulate expansions in this file. Stubs not yet expanded remain as bare references in the chapter drafts.

### Proposed

> # Atomic Sanskrit — Source and Reference Companion
>
> This companion expands the short notes printed in *Atomic Sanskrit*. Each entry provides the source and the textual or historical detail that connects it to the corresponding passage in the book. When the book goes beyond what the source states directly, the entry explains that step in plain language.
>
> Some entries are brief bibliographic anchors. Others examine a Vedic passage, grammatical rule, dataset, or disputed history in greater depth. Readers may use the printed note identifier to locate the matching entry here.
>
> Editorial workflow, deployment locations, verification status, and uncited research remain in the project's working files rather than in the published companion.

### Decision

- [x] ACCEPT PROPOSED
- [ ] KEEP ORIGINAL
- [ ] USE AUTHOR REVISION
- [ ] REVISE AGAIN
- [ ] DEFER

### Author Revision

```text

```

### Comments


## GLOBAL-002 - Standardize substantial companion notes

**Source:** [First expanded note](/Users/paragtope/projects/writing/books/atomicSanskrit/as_endnotes.md:11)  
**Action:** GLOBAL STRUCTURE  
**Status:** OPEN  
### Original

> ### `rigveda-5-40-5-svarbhanu-eclipse`
>
> **Short:** Ṛgveda 5.40.5 supplies the eclipse diagnostic: Svarbhānu pierces Sūrya with darkness, and the worlds become bewildered like one who does not know the field. The keystone phrase is **अक्षेत्रवित् (*akṣetravit*)**, rendered in the Preface as **field-loss**.
>
> **Deployment:** Preface opening epigraph and first prose activation.
>
> The quoted mantra is Ṛgveda 5.40.5:
>
> यत्त्वा सूर्य स्वर्भानुस्तमसाविध्यदासुरः ।\
> अक्षेत्रविद्यथा मुग्धो भुवनान्यदीधयुः ॥
>
> *yat tvā sūrya svarbhānus tamasāvidhyad āsuraḥ |*\
> *akṣetravid yathā mugdho bhuvanāny adīdhayuḥ ||*
>
> Working translation: *When Svarbhānu the asura pierced you, O Sun, with darkness, the worlds looked about bewildered, like one who does not know the field.*
>
> The key expression is **अक्षेत्रवित् (*akṣetravit*)**: *a-* (not) + *kṣetra* (field) + *vit* (knowing). The verse does not only describe darkness. It describes the loss of the field by which light is oriented. The phrase **field-loss** preserves that diagnostic force: Sūrya remains Sūrya, but the worlds no longer know how to locate themselves by his light.
>
> The verse belongs to the Svarbhānu sequence in Ṛgveda 5.40. The opening stops at the eclipse; the closing returns to the same sequence through **5.40.9**, *yaṃ vai sūryaṃ svarbhānus tamasāvidhyad āsuraḥ | atrayas tam anv avindan nahy anye aśaknuvan* — "the Sun whom Svarbhānu pierced with darkness, the Atris found; no others were able." The two verses mirror each other: both hold the same wound-line *svarbhānus tamasāvidhyad āsuraḥ*, and the second hemistich flips from *the worlds went field-blind* (5.40.5) to *the Atris alone found him* (5.40.9). The intervening **5.40.6** is the verse in which Indra strikes down Svarbhānu's *māyā* and Atri discovers the hidden Sun by the fourth *brahman*. Verse text and numbering verified against the Wilson/Sāyaṇa edition; confirm accenting against the selected printed Ṛgveda before final.

### Proposed

Use a common internal shape for substantial notes so that readers can find the source first and then follow the book's use of it. The fourth component belongs only in notes where a load-bearing inference extends beyond the source:

1. **Short note** — the sentence suitable for the printed book
2. **Source** — text, edition, verse, page, or bibliographic anchor
3. **Explanation** — what the source says and how the book uses it
4. **Source and inference** — include only when the book makes an additional inference that readers need help distinguishing from the source
5. **Related entry** — only when another note provides genuinely different evidence

Convert `Deployment` into reader-facing cross-references such as `Used in the Preface and Epilogue`, or remove it when the body already supplies the connection. Resolve verification reminders before publication. Move parked, uncited, and workflow-only entries to a working archive.

Split the longest notes when they combine several independent subjects. Priority candidates are `sound-volume-two-open-coordinates`, `apauruseya-mimamsa-sutra-1-1-5`, `rigveda-1-164-39-akshara-assembly`, `rigveda-10-125-vak-ambhrini`, `assalayana-sutta`, `dhatupatha-empirical-distribution`, `samskrtam-morphology`, `rigveda-10-71-4-vach`, `paspashahnika-apabhramsa-passage`, `buddhist-asia-radiance`, `pre-pie-dictionary-shift`, and `pie-cementing-recent-decades`.

### Decision

- [x] ACCEPT PROPOSED
- [ ] KEEP ORIGINAL
- [ ] USE AUTHOR REVISION
- [ ] REVISE AGAIN
- [ ] DEFER

### Author Revision

```text

```

### Comments


## GLOBAL-003 - Let the build own figure numbering

**Source:** [Example manual caption](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_00_seekers.md:107)  
**Action:** GLOBAL REPLACE  
**Status:** OPEN  
### Original

> ![Figure 0.1 — The three fields. *Saṃskṛta*, the wholly created language, runs in two domains. The *vaidika* holds language and content invariant. The *laukika* holds the language invariant while generative usage adapts and its curated corpus remains selected, accretive, and lossy. Beside them, *prākṛtika* flows as the changing natural speech of daily life. All three run the full span from *anādi* to *ananta*.](figures/seekers/sanatana_triad.svg){#fig:sanatana-triad width=100%}

### Proposed

> ![The three fields. *Saṃskṛta*, the wholly created language, runs in two domains. The *vaidika* domain keeps both language and content unchanged. The *laukika* domain keeps Sanskrit calibrated while speakers adapt its usage and curate a corpus that is selective, accretive, and lossy. Beside them, *prākṛtika* speech changes through daily use.](figures/seekers/sanatana_triad.svg){#fig:sanatana-triad width=100%}

Apply the same rule to every ordinary figure:

- keep the Pandoc identifier `{#fig:...}`;
- remove literal `Figure X.Y —` from the Markdown caption;
- let the build assign the number and `Figure` label;
- start the caption with its title or direct description;
- move argumentative conclusions into the paragraph after the image.

The E.1–E.12 eclipse sequence needs one explicit build rule if those labels must remain. Do not mix manual and automatic numbering again.

### Decision

- [x] ACCEPT PROPOSED
- [ ] KEEP ORIGINAL
- [ ] USE AUTHOR REVISION
- [ ] REVISE AGAIN
- [ ] DEFER

### Author Revision

```text

```

### Comments


## GLOBAL-004 - Resolve every visible figure specification

**Sources:** [Chapter 14](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_14_calibration.md:74), [Chapter 17](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_17_wrong_question.md:38), [Chapter 18](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_18_pie_in_sky.md:266), [Chapter 19](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_19_life_after_pie.md:27), and [Appendix 3](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_03_audiography.md:174)  
**Action:** PRODUCTION DECISION  
**Status:** OPEN  
### Original

> [FIGURE 14.2: The six-layer calibration matrix — Vedas, Prātiśākhya, Vyākaraṇam, Dhātupāṭha, Varṇamālā, Chandas — with Śikṣā operating as pedagogy across the layers.]
>
> [FIGURE 17.1: The Architectural Test — six rows: phonetic grid, dhātu architecture, generative rules, retroflex core, preservation mechanisms, formal grammar. For each row, one column states what a valid model must explain; a second column states what genealogical reconstruction can and cannot provide.]
>
> [FIGURE 18.7: The pyramid's PIE reconstructions and the vivimorphosis chains shown side by side for *deva* and *asura*. The pyramid's etymology, Sanskrit *dhātu* / *śabda*, receiving-language *bīja*, and contact-language *apaśabda* across the rows.]
>
> [FIGURE 18.8: One Sanskrit *dhātu*, multiple PIE ancestor-forms — *dṛś* as unified Sanskrit family versus the pyramid's split into **\*derḱ-**, **\*spek-**, and dropped or displaced visual cognates.]
>
> [FIGURE 19.1: The Mitanni Sanskritic Layer — treaty deities (Mitra / Varuṇa / Indra / Nāsatya), Kikkuli numerical terms (*aika* / *tera* / *panza* / *satta* / *na* / *vartana*), Mitanni throne names (Tushratta / Shattiwaza / Indaruda / Artashumara), and the *marya* warrior term, with the Sanskrit form and its receiving-language rendering alongside each.]
>
> [FIGURE 19.2: The Wave 2 Catalog of Methodological Metatypy — six rows (Greek / Latin / Tibetan / Arabic / Hebrew / Chinese-selective-reception); four columns (case type: direct / transitive / selective; approximate date; receiving-lineage text(s); transmission character).]
>
> [FIGURE 19.3: The Calibrant Waves and the Diasporic Wave — Wave 1 as pre-Pāṇinian corpus-form transmission (Saptaṛṣi roster + Mitanni anchor); Wave 2 as post-Pāṇinian methodological transmission (Greek / Latin / Tibetan / Arabic / Hebrew / Chinese-selective-reception, alongside Buddhist lexical and phonological transmission across Asia); Wave 3 as contemporary restatement (the engineered Sanskrit thesis); Diasporic Wave as demographic carrier of lived Indic substrate (Romani + four arcs of modern diaspora); Wave 3 conditional on diasporic relearning.]
>
> [FIGURE A.4: *Photography and Audiography.* — the two engineered captures laid in parallel, with the Indic achievement preceding the Western one by many thousands of years and operating at higher resolution along more channels.]
>
> [FIGURE A.9: *The audiographic family and its pyramid classification.* — the table below; a visual treatment may consolidate by region with the pyramid's labels as a column.]

### Proposed

Resolve each item before final sentence editing because surrounding prose may depend on the visual:

- Chapter 14 Figure 14.2 — create the calibration matrix or convert it into a body table.
- Chapter 17 Figure 17.1 — create the Architectural Test or retain the six-part prose and remove the placeholder.
- Chapter 18 Figures 18.7 and 18.8 — the adjacent tables may already show the same comparison; choose either the figure or the table unless each reveals something different.
- Chapter 19 Figures 19.1, 19.2, and 19.3 — use the decisions in `24_ch19.md` to define evidence status and wave structure before design.
- Appendix 3 Figures A.4 and A.9 — create, replace with the existing tables, or remove.

No bracketed figure specification should reach a public build.

### Decision

- [ ] ACCEPT PROPOSED
- [ ] KEEP ORIGINAL
- [ ] USE AUTHOR REVISION
- [ ] REVISE AGAIN
- [x] DEFER

### Author Revision

```text

```

### Comments


## GLOBAL-005 - Use captions for reading instructions, not conclusions

**Source:** [Appendix 4 caption example](/Users/paragtope/projects/writing/books/atomicSanskrit/as_3_04_inventory_atlas.md:112)  
**Action:** GLOBAL REVISE  
**Status:** OPEN  
### Original

> ![Figure A.4.6 — Caucasus Survey: 10 of 23 Sanskrit base coordinates. Three pyramid classifications collide in one geographic region — and the floor coverage of all eleven surveys appears at exactly that point. Geographic distance from the subcontinent is what moves the number.](figures/superset/sk_armenian_georgian_ossetian.svg){#fig:app4-caucasus-survey width=100%}

### Proposed

> ![Caucasus survey. Armenian, Georgian, and Ossetian together cover 10 of the 23 Sanskrit base coordinates. Filled cells mark shared independent consonant contrasts; empty cells mark Sanskrit coordinates absent from the selected union.](figures/superset/sk_armenian_georgian_ossetian.svg){#fig:app4-caucasus-survey width=100%}

Move `Geographic distance from the subcontinent is what moves the number` into the following prose, where it can be identified as the book's inference and qualified by the selected-language method.

Before every figure, tell the reader what to look for and why the image appears at that point in the argument. Let the caption identify what is shown and explain the visual encoding. Use the paragraph after the image to describe the visible result and explain what the book draws from it. Where the build supports separate alt text, describe shapes, axes, line styles, and states without relying on color alone.

### Decision

- [x] ACCEPT PROPOSED
- [ ] KEEP ORIGINAL
- [ ] USE AUTHOR REVISION
- [ ] REVISE AGAIN
- [ ] DEFER

### Author Revision

```text

```

### Comments


## GLOBAL-006 - Assign repeated theses a specific job

**Source:** [Representative refrain in Chapter 19](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_19_life_after_pie.md:43)  
**Action:** GLOBAL STRUCTURE  
**Status:** OPEN  
### Original

> The machinery made Pāṇini heroic under a false label — the *codifier* who froze a drifting language into order. Life after PIE restores the right one: Pāṇini is heroic as *decoder*, compressor, and transmitter. He took an operating architecture already preserved by the *Vedas*, the *Prātiśākhya* discipline, recitation lineages, and pre-Pāṇinian *vaiyākaraṇāḥ*, and made it explicit enough to travel. Sanskrit does not begin with him. Sanskrit's method becomes more portable through him.

### Proposed

Preserve repeated ideas only when the new location gives them a new function:

- **Pāṇini and codification:** Preface states the refrain; Chapter 2 explains category theft; Chapter 5 establishes the decoding lineage; Chapter 11 shows documentation operating on forms; Chapter 19 explains portability; appendices supply evidence.
- **Drift, petrification, calibration:** Chapter 1 introduces the conflict; Chapter 2 defines the classifications; Chapter 3 explains incentive; Chapter 13 contrasts custody; Chapter 14 demonstrates calibration.
- **Imaginary people, language, and words:** Chapter 17 states the triad; Chapter 18 applies it; the epilogue recalls it briefly.
- **Vaidika and laukika:** Chapter 0 defines the domains; Chapter 2 explains changing use with invariant language; later chapters apply rather than redefine them.
- **Distributed calibration:** Chapters 0, 13, 14, and 15 respectively introduce caretakers, contrast custody, explain layers, and let the reader hear the mechanism.

During application, remove later catalogue paragraphs that merely restate an established thesis without adding a mechanism, example, consequence, or transition. Preserve deliberate refrains and hammers even when they repeat a thesis; their function is cadence and judgment, not additional exposition.

### Decision

- [ ] ACCEPT PROPOSED
- [ ] KEEP ORIGINAL
- [ ] USE AUTHOR REVISION
- [x] REVISE AGAIN
- [ ] DEFER

### Author Revision

```text

```

### Comments
revise this and include specific examples of what will get dropped and why


## GLOBAL-007 - Apply the contextual vocabulary and actor audit

**Source:** [Representative concrete actor sentence](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_04_fourth_abrahamic.md:116)  
**Action:** GLOBAL CONTEXTUAL REVIEW  
**Status:** OPEN  
### Original

> Academic institutions continued the colonial operation after formal empire ended. The asuric pyramid has now opened another front in its war against Sanskrit: readers are taught to hate the language as an instrument of elite power, although Sanskrit’s calibrant architecture does the exact opposite by distributing authority.[NOTE: pollock-sanskrit-cosmopolis-position-3] A multimillion-dollar gift from an Indian family funded a major academic translation project that circulated this hate-driven narrative.[NOTE: murty-library-gift-gate]

### Proposed

Keep `the pyramid` when the sentence describes the recurring hierarchy. Name the concrete actor when the sentence concerns a specific curriculum, gift, dictionary, university, government, publisher, or classification decision. Then explain how the act fits the pyramid.

Review the remaining vocabulary by context rather than blind replacement:

- stale `prosecution`, `verdict`, and `courtroom` from the abandoned spine;
- `polemic` where diagnostic, argument, critique, or exposition is more exact;
- `ritual` where yajña, mantra use, recitation, ceremonial action, or inherited practice is intended;
- `canonical` in Hindu contexts where listed, inherited, received, or widely used is more accurate;
- `formalize` where document, state explicitly, arrange, or encode describes the action;
- `gloss` only for an actual short translation.

Apply the naming rule at the same time: a person named in body prose must be praised or criticized for a stated and supported action. Neutral bibliographic names belong in notes.

### Decision

- [ ] ACCEPT PROPOSED
- [ ] KEEP ORIGINAL
- [ ] USE AUTHOR REVISION
- [x] REVISE AGAIN
- [ ] DEFER

### Author Revision

```text

```

### Comments
Needs specifics


## GLOBAL-008 - Apply section granularity after structural decisions

**Source:** [Chapter 2 §2.1](/Users/paragtope/projects/writing/books/atomicSanskrit/as_1_02_botanical.md:21)  
**Action:** GLOBAL STRUCTURE  
**Status:** OPEN  
### Original

> ## 2.1 The Category Move
>
> ### Three Categories Hide the Fourth
>
> ### Origin and Generativity
>
> ### How the Pyramid Reclassifies Sanskrit
>
> ### The Seven Moves

### Proposed

Chapter 2 already applies the desired structure and needs no further granularity change. Use it as the model: add descriptive H3 headings when one numbered section performs several distinct tasks, and replace a very short numbered section with an H3 when it only divides one continuous movement. Avoid forcing every chapter into the same number of subsections.

Highest-priority decisions already represented in the chapter files are:

- merge Chapter 10's repeated design-test setup;
- add descriptive subheadings inside Chapter 13 §13.3;
- divide Chapter 17 §17.6;
- divide the epilogue's `Where the Nectar Rises`;
- decide whether to merge the epilogue's chronology section;
- add conceptual subheadings to Appendix 3;
- reorganize Appendix 8;
- simplify Appendix 9.

Use headings that identify a concrete operation or inquiry. Avoid generic labels such as `The Problem`, `Why It Matters`, `The Framework`, and `The Next Step`.

Do not use section restructuring as a reason to rewrite forceful prose into neutral summaries. Move the original paragraph intact when its claim is sound; revise it only when the new location creates a factual contradiction or an unclear reference.

### Decision

- [ ] ACCEPT PROPOSED
- [ ] KEEP ORIGINAL
- [ ] USE AUTHOR REVISION
- [x] REVISE AGAIN
- [ ] DEFER

### Author Revision

```text

```

### Comments
idea is good - need specifics
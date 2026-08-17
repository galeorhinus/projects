# Proposal - Endnotes, Captions, and Global Findings

Proposal only. No manuscript changes have been made.

## Endnotes

### What the Audit Found

The manuscript uses 242 distinct note stubs. Every one has a matching entry in `as_endnotes.md`; there are no missing expanded notes. The expanded file contains 272 entries, leaving 30 entries that no current body stub cites.

The file is now a substantial companion volume rather than a conventional endnote section:

- approximately 114,860 words;
- 272 entries;
- 222 entries longer than 200 words;
- 143 entries longer than 400 words;
- 16 entries longer than 800 words;
- 2 entries longer than 1,200 words.

That scale can work for the Source and Reference Companion, but the opening still describes most notes as 50-200 words. The public structure and the actual structure should agree.

### Separate Publication Text from Production Metadata

The first block of `as_endnotes.md` is written for the editing workflow. It explains stubs, deployments, propagation, production sessions, and unexpanded notes. Replace it in the published companion with a reader-facing introduction. Keep the workflow instructions in `working/40_reference/workflows/as_endnote_workflow.md`.

Most entries contain `Deployment` or `Deployments` labels. These are useful while writing but should not appear in the reader's companion unless the build system deliberately converts them into a simple cross-reference such as `Used in Chapters 5 and 14`.

The audit found:

- 93 uses of verification or completion language;
- 5 internal `working/...` paths;
- about 25 references to duplicate citations, future consolidation, or the same passage being treated in another note;
- one explicitly parked entry;
- 30 entries no longer cited by the body.

Resolve each verification reminder before publication. If the source cannot be verified, either narrow the claim or remove the note and its body citation. Move parked and uncited research into a working archive rather than publishing it as an endnote.

### Give Every Expanded Note One Shape

Use the following internal structure for substantial notes:

1. **Short note** - the sentence used in the printed book.
2. **Source** - edition, verse, page, or bibliographic anchor.
3. **Explanation** - what the source shows and why it supports the body.
4. **Limit** - one short qualification when the evidence does not establish the whole interpretation.
5. **Related note** - only when another entry genuinely adds different evidence.

Do not force tiny citation notes to display all five headings. The structure is for notes that have become essays.

### Divide Notes That Now Contain Several Essays

The longest entries should not simply be shortened. Several combine text, translation, grammatical analysis, interpretive argument, source history, and deployment decisions. Divide them where a reader may reasonably seek one part without the others.

Priority entries include:

- `sound-volume-two-open-coordinates` - 1,577 words;
- `apauruseya-mimamsa-sutra-1-1-5` - 1,544 words;
- `rigveda-1-164-39-akshara-assembly` - 1,193 words;
- `rigveda-10-125-vak-ambhrini` - 1,129 words;
- `assalayana-sutta` - 1,115 words;
- `dhatupatha-empirical-distribution` - 1,096 words;
- `samskrtam-morphology` - 1,045 words;
- `rigveda-10-71-4-vach` - 1,013 words;
- `paspashahnika-apabhramsa-passage` - 978 words;
- `buddhist-asia-radiance` - 972 words;
- `pre-pie-dictionary-shift` - 939 words;
- `pie-cementing-recent-decades` - 884 words.

For example, `sound-volume-two-open-coordinates` can contain a short explanation in the companion while its inventory survey and full phonetic discussion become a referenced technical excursus. The `vāc` and Vedic verse entries can separate text and padavaccheda from the larger architectural interpretation.

### Remove Duplicated Argument

An endnote should supply evidence, explain a difficult source, or state a necessary limit. It should not reproduce the chapter's full rhetoric. Several notes restate the pyramid diagnosis, describe the chapter's intended move, and then repeat the source analysis. Retain the source and the bridge to the claim; remove editorial descriptions such as `the polemic move`, `the chapter's deployment`, or `at chapter-lock time`.

Where two entries treat the same passage for different chapters, prefer one stable source note with short chapter-specific sentences in the body. The Patañjali `siddhe śabdārthasambandhe` notes are a visible consolidation candidate.

### Use Technical Language More Patiently

The companion may use terms such as `saṃhitā`, `padapāṭha`, `sandhi`, `allophone`, `phoneme`, `morphology`, and `substrate`, but each note should explain the term the first time it becomes necessary. Do not assume that a reader who follows a Sanskrit argument also knows the terminology of modern linguistics.

Tables are appropriate for padavaccheda, word-by-word translation, inventories, and comparisons. The prose after a table should explain the pattern rather than repeat every row.

### Sources and Quotations

Use one citation style throughout. Separate primary text, edition, translation, and modern commentary instead of placing all four in one long source paragraph. Avoid vague phrases such as `standard editions`, `standard reference literature`, or `any history-of-linguistics reference` when a specific source can be supplied.

Long quotations should be reserved for primary texts whose exact wording is under analysis. Modern scholarly prose can normally be paraphrased with a page reference.

## Captions and Figure Introductions

### One Numbering Authority

The body contains 90 image captions. Sixty-six begin with a manually written `Figure ...` number, while 24 do not. This mixed practice is the likely source of duplicated output such as `Figure 4: Figure 0.1`.

Choose one numbering authority. The preferred approach is:

- keep the Pandoc identifier, such as `{#fig:sanatana-triad}`;
- let the build assign `Figure`, chapter number, and sequence number;
- begin the Markdown caption with the title rather than a literal figure number;
- use cross-reference identifiers in prose so renumbering remains automatic.

If the eclipse series must retain `E.1-E.12`, configure that series explicitly in the build rather than typing numbers into some captions while the build numbers them again.

### Caption Length and Function

Fourteen captions exceed 40 words. The longest occur in Chapter 0, Chapter 8, Chapter 18, Appendix 4, and the Part openers. A caption should do two things:

1. identify what the reader is looking at;
2. explain how to read the visual encoding.

Move argumentative conclusions into the paragraph after the figure. A caption such as the Caucasus survey should state the languages, coverage count, and unfilled cells. The claim that geographic distance alone moves the number belongs in the analysis, where it can be qualified and defended.

### Introduce Every Figure Before It Appears

The paragraph before a figure should tell the reader what question the image will help answer. The paragraph after it should state the visible result. This prevents the image from looking dropped in and prevents the caption from carrying the entire argument.

Use this pattern without turning it into a repeated formula:

- before: `The next comparison asks whether...`
- caption: what the visual contains and how marks/colors/axes work;
- after: `The southern set covers... This gives the migration account a physical problem because...`

### Repair Caption-Specific Problems

- Part III: correct `plates:Botanical` and rewrite the sentence.
- Parts V and VI: replace `Three plates...Two plates...` and `Five plates; Two plates...` with complete prose.
- Chapter 12: replace `Ch12 visual key` with a reader-facing title.
- Chapter 16: `The mūrdhanya flex` is too slight for a detailed anatomical figure; name the tongue movement and contact point.
- Chapter 18: captions such as `No Sanskrit in the tree` and `the tree is never the source` make conclusions inside the caption. Let the following prose argue those conclusions.
- Appendix 4: shorten all survey captions and move comparative interpretation below each figure.

### Resolve Figure Placeholders

The public manuscript still contains unresolved bracketed figure specifications:

- Chapter 14: Figure 14.2;
- Chapter 17: Figure 17.1;
- Chapter 18: Figures 18.7 and 18.8;
- Chapter 19: Figures 19.1, 19.2, and 19.3;
- Appendix 3: Figures A.4 and A.9.

Create the figure, convert the specification into prose/table form, or remove the placeholder before line editing. These are structural decisions because the surrounding text may depend on the promised visual.

### Accessibility

The Markdown caption currently doubles as alt text. Several captions are too argumentative to describe the image accessibly. If the build supports separate alt text and captions, use concise visual alt text and retain the interpretive caption. At minimum, describe encoded color, line style, plate state, and axis meaning without relying on color alone.

## Cross-Chapter Repetition

### Pāṇini and Codification

The refrain `Sanskrit was engineered. Encoded in the Vedas. Decoded by many. Pāṇini's decoding is the finest.` is worth preserving. Give each later recurrence a different job:

- Preface: state the refrain.
- Chapter 2: show how `codification` steals the category.
- Chapter 5: establish the pre-Pāṇinian analytical lineage and Pāṇini's role.
- Chapter 11: show the documentation operating on actual forms.
- Chapter 19: show how the documented method became portable.
- Appendices: supply detailed evidence without restating the whole refrain.

Remove recurrences that perform none of those jobs.

### Drift, Petrification, and Calibration

The book repeatedly says that the pyramid can survey natural drift, capture codification, and cannot own calibration. Preserve the argument but assign it a progression:

- Chapter 1 introduces the conflict.
- Chapter 2 defines the language classifications.
- Chapter 3 explains the strategic incentive.
- Chapter 4 shows the institutional pyramid.
- Chapter 13 contrasts custody systems.
- Chapter 14 demonstrates distributed calibration.

Later chapters should refer to the established distinction through a concrete action rather than restating all three categories.

### Imaginary People, Language, and Words

The triad of the racial Arya thesis, PIE, and starred reconstructions is memorable and should remain a refrain. State the full triad in Chapter 17, apply it to the word histories in Chapter 18, and recall it briefly in the Epilogue's nectar passage. Avoid rebuilding its complete logic in every Part opener and appendix.

### Vaidika and Laukika

Chapter 0 should own the first definition: two Sanskrit domains with different work. Chapter 2 should explain how the two-domain architecture resolves invariant language and changing use. Chapters 9 and 17 can then apply the distinction to selection and chronology. Appendices should provide evidence rather than redefine the pair.

### Distributed Calibration

Chapter 0 introduces the caretaker architecture. Chapter 13 contrasts it with centralized custody. Chapter 14 explains its layers. Chapter 15 lets the reader hear it in recitation. Those four roles are distinct. Remove catalogue paragraphs elsewhere that list sound, meter, grammar, lineage, and correction without adding a new mechanism or example.

### Sound-Field Surveys

Chapter 7 introduces the mouth and survey method. Chapter 8 presents the comparative field. Chapter 9 explains how the selected grid works. Chapter 16 uses the evidence against portability. Appendix 4 should hold method, inventories, limitations, and replication detail. Keep that division so each chapter moves the argument forward.

### Eclipse and Radiance

The eclipse figures already supply visual repetition. The prose does not need to close every chapter by repeating Sun, shadow, plate, and radiance. Use the metaphor at Part boundaries and at genuine moments of recovery. Within technical chapters, prefer the concrete object being examined.

## Terminology and Reader Orientation

### New Terms

At first use, every coined or repurposed term should receive:

1. the ordinary phenomenon;
2. the reason the existing label fails;
3. the new term;
4. one example.

This is especially important for `sonomer`, `audiography`, `Auditure`, `vivimorphosis`, `petrification`, `revivification`, `calibrant contact`, `Radiance Thesis`, and `apex language`.

After that introduction, use the term consistently. Do not redefine it each time or alternate it casually with a near-synonym.

### Abstract Agents

The relaxed book-as-agent rule is sensible. `This book argues` and `Chapter 14 shows` are clear when they describe the work a text actually performs. Avoid constructions in which a chapter, category, chronology, or distinction appears to act on people by itself. Name the scholar, institution, curriculum, ruler, teacher, or classification that performs the action when the actor is known.

The same rule applies to `the pyramid`. It is useful for a repeated structure. When the sentence describes a specific gift, curriculum, dictionary, government, university, or classification decision, identify that concrete actor first and then show how the act fits the pyramid.

### Residual Vocabulary Audit

A contextual scan still finds the following in manuscript files outside the endnotes:

- `prosecution`: 16 uses;
- `verdict`: 43 uses;
- `courtroom`: 3 uses;
- `polemic`: 62 uses;
- `ritual`: 29 uses;
- `canonical`: 16 uses;
- `formalize/formalization`: 13 uses;
- `gloss`: 10 uses.

Do not replace these blindly. Some are quotations, historical terms, or exact descriptions. Review them by context:

- replace stale courtroom-spine language;
- retain `verdict` only for an actual judgment or deliberate metaphor;
- replace `polemic` with diagnostic, argumentative, expository, critique, or claim according to function;
- replace `ritual` with yajña, recitation, ceremonial action, liturgical use, or inherited practice when one is more exact;
- retain `canonical` for traditions that actually define a canon, but avoid it for the Hindu continuum when listed, inherited, received, or widely used is more accurate;
- replace `formalize` with document, state explicitly, arrange, or encode according to the action;
- use `gloss` only for an actual short translation, not as a generic verb for explanation.

### Sanskrit and Linguistic Terms

Retain the agreed first-use pattern: Devanagari, then IAST, then an ordinary English explanation. Do not bold every later Devanagari form. Use `⟪ ⟫` only for a *dhātuḥ* treated as an atom, and apply it consistently within a section.

Terms likely to need a plain first-use explanation include phoneme, allophone, substrate, retroflex, aspiration, phonotactics, morphophonemics, paradigm, metatypy, mora or *mātrā*, and rime table.

### Naming People

Apply the established rule consistently: people named in the body should be praised or criticized for a stated action. Neutral bibliographic names belong in endnotes. In the appendices, where historical actors are evidence, the prose should still say what the person did and why that action matters.

## Section Granularity

The audit does not recommend making every chapter symmetrical. It recommends adding structure where a section contains several different tasks and removing structure where a heading interrupts one continuous movement.

Highest-priority body changes already documented in the chapter files are:

- reduce the Part I opener from roughly 950 words;
- divide Chapter 2 §2.1 internally;
- merge Chapter 10 §10.6 into §10.7;
- add descriptive subheadings inside Chapter 13 §13.3;
- divide Chapter 17 §17.6;
- divide the Epilogue's `Where the Nectar Rises`;
- consider merging the Epilogue's short chronology section after explicit approval.

Highest-priority appendix changes are:

- add subheadings to Appendix 3's long conceptual sections;
- reduce and reorganize Appendix 8;
- turn Appendix 9 from a set of mini-essays into a working glossary.

Subheadings should be noun phrases or concrete questions. Avoid generic headings such as `The Problem`, `The Argument`, `Why It Matters`, `The Next Step`, or `The Framework` when a specific heading is available.

## Production Artifacts

Several files still expose draft or production material to the reader. Remove it before final prose editing so it does not distort section openings:

- draft labels in the Preface, Chapters 0 and 1, Acknowledgments, Appendices 1, 2, 5, 7, and 8, and the full reference Appendix 6;
- `[ACKNOWLEDGMENTS - TO BE EXPANDED]`;
- internal paths in Appendix 4 and the endnotes;
- `CLAUDE.md` in Appendix 9;
- figure specifications listed above;
- chapter-lock, final-publication, and verification-task language in the endnotes.

## Priority and Implementation Order

### Stage 1 - Publication Blockers

1. Remove production artifacts.
2. Resolve figure placeholders.
3. Correct numerical and factual inconsistencies identified in Appendices 4-8.
4. Resolve all endnote verification reminders tied to claims that remain in the body.
5. Choose one figure-numbering system.

### Stage 2 - Structural Work

1. Reduce the Part I opener.
2. Divide the long body sections identified above.
3. Reorganize Appendix 8.
4. Simplify Appendix 9.
5. Separate unused and parked endnotes from the published companion.

### Stage 3 - Plain-Language Revision

Work chapter by chapter. Preserve examples and argument while replacing compression, academic shorthand, legal phrasing, passive constructions, and abstract agents. Add the missing explanatory sentence whenever a reader would otherwise have to infer the mechanism.

### Stage 4 - Repetition and Transitions

After the structural work, assign every repeated thesis its chapter-specific role. Remove recurrences that merely announce the conclusion again. Repair transitions exposed by deleted repetition.

### Stage 5 - Captions, Notes, and Final Continuity

Shorten captions, add figure introductions, standardize expanded notes, verify cross-references, and read every Part boundary in sequence. Finish with an uninterrupted cover-to-cover read aimed at the intelligent non-specialist rather than another search-and-replace pass.

# Reader's Guide: Production Record

## Approved PDF Rebuild: 21 September 2026

The author requested commit, push, `as-deploy`, and PDF generation. The pending manuscript/thesis, guide, and Deccan College research changes were committed separately and pushed through `6a3e5e37`. `as-deploy` successfully refreshed the site on amrut; the public landing page returned HTTP 200. The source-only entries below describe the stages before this rebuild.

- Both guide editions now include the Devanagari, voice, and three-characteristic updates. Edition date: 21 September 2026.
- A5: 70 interior / 74 complete pages; A4: 44 interior / 48 complete pages. Each interior has one final blank duplex-padding page. Each separate cover has four faces.
- All eight size-qualified files regenerated: interior, print, cover, and complete for each size. The legacy cover alias also refreshed.
- 12,095 source words; 47 sections; all 101 invitations and ten figures retained. Fonts and margins unchanged.
- Three A5 sections received explicit continuation breaks: the challenge, the two domains, and the Chapter 15/16 exploration. A4 splits the PIE discussion. These replace accidental overflow pages without editing prose or shrinking type.
- All 28 tests pass. No missing glyphs, overfull boxes, off-page text, or unplanned continuation pages. All page sheets and both covers inspected, with a full-size check of the dense multilingual Arabic/Panini continuation.
- Physical print proof remains pending. These counts concern the Reader's Guide, not the full book or Reference Companion.

## Three Characteristics: 21 September 2026

Following the approved addition in manuscript §1.5, the guide now introduces containment, concealment, and control through the Vedic encounters in "Two Directions of Order." "What a Label Can Conceal" applies the three characteristics to Sanskrit's classification and interpretation. Both guide paragraphs are additions; no existing guide prose was removed.

The approved manuscript reminders accompany this update: Chapter 18 replaces "possession, concealment, and control" with "containment, concealment, and control"; the Epilogue expands "The pyramid repeats containment beneath an apex" to name all three and connect them to access to knowledge, Sanskrit's architecture, and its interpretation. These are reminders of the book's abstraction from the encounters, not a claim that a mantra enumerates the English triad.

PDFs remain unchanged. The next authorized render must recheck the paragraph-based breaks and page flow after these additions, along with the preceding voice and accessibility edits.

## Source-Only Voice Sweep: 21 September 2026

The author requested the book's argumentative voice in accessible English, not a neutral survey. Completed the sweep across the narrative, chapter introductions, all invitations, and cover prose. Named the pyramid, Western philologists, editors, and institutions where abstractions had concealed their actions. Expanded the Arabic comparison to identify the burning order, al-Azhar's approval, and Egyptian publication penalties, while retaining teaching and memorization as parts of preservation.

There are 36 replacement groups in the [exact before-and-after record](voice_sweep_20260921.md), with originals in `archive/pre_voice_sweep_20260921/`. Four invitation texts changed; all 101 IDs, placements, and destinations remain intact. The ten figures, technical examples, numerical scope, and personal-speculation markers are unchanged. README and the revision plan now explicitly distinguish simple vocabulary from a softened stance.

Twenty source-level tests pass. PDF-dependent tests were excluded because no render was authorized. The A4 and A5 PDFs still reflect 20 September; the next approved build must recheck pagination after both the accessibility and voice changes. No full-book manuscript edits or commits were made in this sweep.

## Source-Only Accessibility Sweep: 21 September 2026

The author requested Devanagari alongside terms whose specialized IAST letters may be difficult for this guide's readers. The main narrative, chapter introductions, invitation wording, and cover prose now pair those terms. Examples include माण्डूक्य उपनिषद् (*Māṇḍūkya Upaniṣad*), ऋग्वेद (*Ṛgveda*), पाणिनि (*Pāṇini*), पतञ्जलि (*Patañjali*), बृहस्पति (*Bṛhaspati*), स्वर्भानु (*Svarbhānu*), and ब्राह्मी (*Brāhmī*). तोल्काप्पियम् is a Devanagari reading aid for the Tamil title, not a claim that the work is Sanskrit. The existing figure labels already pair scripts.

English possessives were rephrased around the paired names. The adjective "Upaniṣadic" became "that description" after its source had been named; no argument was removed. The guide-only subtitle presentation pairs सनातन (*Sanātan*), leaving root book metadata unchanged. Historical archives and comparison records remain unchanged.

Eleven source-level checks pass, including all 101 invitations appearing once, destination and chapter-title checks, and new tests rejecting specialized IAST outside Devanagari pairs. No PDFs were generated; the 20 September files and their page counts remain the last rendered version. The two earlier wording changes made on 21 September are also pending that build.

## Current Revision: Content and Both Editions

**20 September 2026:** The author approved the content audit and section plan, then authorized all remaining passes and A4/A5 PDF production without further prompts. All four content passes are complete. The earlier revision records below remain historical; the counts in this section describe the current outputs.

- [Content change log](content_revision_change_log.md) and [exact before-and-after record](content_revision_before_after.md).
- Three new narrative sections: the explicit challenge, the fourth-Abrahamic-religion thesis, and institutional custody. Pāṇini now precedes the two-domain explanation. The institutional, PIE, radiance, and closing arguments are fuller; chapter-numbered headings match the manuscript.
- Source words: **11,708**, up from **9,488**; **47 sections**, **101 invitations**, and **10 diagrams**. Every invitation remains at its existing source-section placement and appears once.
- A5: **66 interior / 70 complete pages**, 148 × 210 mm, 11 pt body and 14.4 pt leading. A4: **42 interior / 46 complete pages**, 210 × 297 mm, 12 pt body and 16 pt leading. Four cover faces per edition; neither interior requires blank padding.
- STIX Two Text and Tiro Devanagari Sanskrit retained. Mirrored inner margins remain 20 mm in A5 and 25 mm in A4. Figure geometry and outlined exports are unchanged; minimum labels remain above 8.5 pt at final width.
- **25 tests pass.** No missing glyphs, overfull boxes, text outside page bounds, duplicate/missing invitations, or unplanned continuation pages. Trim, fonts, binding clearance, bookmarks, and print/complete copies checked. Both editions' page sheets and covers were inspected; revised multilingual headings were also checked at full-page scale.
- Final layout repair: explicit continuation breaks replace short accidental overflow pages; chapter headings wrap at word boundaries without smaller type.
- Main manuscript, thesis summary, unrelated figures, and outreach documents were not edited. Existing source/planning discrepancies are recorded in the audit, not silently reconciled.

The complete originals were archived before editing under `archive/pre_content_revision_20260920/`. These remain review copies; physical proof, author acceptance, website deployment, and printer submission were not performed.

## Scope and Approval

The author waived the interim review gates on 18 September 2026. Complete the booklet autonomously, retaining internal checks. No changes to the full manuscript are authorized by this task. This is a review draft, not an author-approved publication or an independently verified replacement for the full book.

The guide explains the book's argument in familiar English. It is distinct from both the long-form Reference Companion and the planned 20,000-word concise book. It does not reproduce the institutional case files, the complete grammatical inventory, or the full endnotes.

## First-Draft Pass Status

| Pass | Status | Record |
|---|---|---|
| 1. Product reconciliation | Complete | Separate orientation booklet, chapter-led reading pointers; main manuscript untouched. |
| 2. Thesis-to-page map | Complete | Map below, including a dedicated two-page subcontinental-home section. |
| 3. Source and example packet | Complete | Existing manuscript and notes are the source packet; source anchors below. |
| 4. Voice sample | Complete internally | Opening, atom, and calibrant sections checked against the familiar-vocabulary / varied-sentence brief. Author gate waived. |
| 5. Complete draft | Complete | Canonical prose in `manuscript/readers_guide.md`. |
| 6. Argument and continuity | Complete | Order introduced early; body and Indian-home evidence precede the historical dispute; ending returns to the three shantis. |
| 7. Selection and page fit | Complete | 5,285 source-prose words; 24 interior pages. Reduced a diagram's vertical spacing rather than compressing the prose or shrinking type. |
| 8. Figures | Complete | Eight SVG diagrams, vector PDF exports with all text outlined. Minimum label size 9.29 pt at 118 mm width. |
| 9. Vocabulary and rhythm | Complete internally | Unexplained “semantic” and similar shorthand avoided; Sanskrit examples introduced in prose; no run of one-line hammers. |
| 10. Evidence and pointers | Complete against manuscript | Source anchors below; counts and destinations checked. This is source alignment, not independent verification of every disputed thesis. |
| 11. Build and layout | Complete | A5; STIX Two Text 11 pt / 14.4 pt leading; Tiro Devanagari Sanskrit; separate four-face cover and combined reading copy. |
| 12. Final production checks | Digital checks complete | Page images inspected; seven tests pass; no missing-glyph or overfull-box warnings. Physical proof and author review remain outstanding. |

## First-Draft Page and Thesis Map

| Page | Subject | Core theses | Source |
|---|---|---|---|
| 1 | Title | All | `as_book.yaml` |
| 2 | Why this book | 8 | Preface |
| 3 | Sound to order | 1, 2, 8 | Chapters 10–12; inside-out plan |
| 4 | Two directions of order | 6, 8 | Preface; Chapters 1, 3–4 |
| 5 | Three shantis | 8 | Preface; Epilogue; inside-out plan |
| 6 | The speaking body | 1 | Chapters 7, 9–10 |
| 7 | The sound grid | 1 | Chapter 9 |
| 8 | Subcontinental home: sound | 7 | Chapter 8; Appendix 4 |
| 9 | Subcontinental home: order | 7, 8 | Chapters 2, 17–18 |
| 10 | Atoms and word families | 1, 2 | Chapter 10 |
| 11 | Generative scale | 1 | Chapters 2, 12; Appendix 6 |
| 12 | A completed verb | 1, 2 | Chapter 11 |
| 13 | Sentence and repeated design | 1, 2 | Chapters 10, 12 |
| 14 | Two domains | 4 | Chapters 14, 16; Appendix 8 |
| 15 | What a calibrant does | 3 | Chapters 14–16 |
| 16 | Many people, many checks | 3, 4 | Chapters 13, 15 |
| 17 | Memory, attack, writing | 4 | Chapters 6, 13, 18 |
| 18 | Grammar and Panini | 5 | Chapters 2, 5 |
| 19 | Categories and eclipse | 6 | Prologue; Chapters 2, 9–10, 19 |
| 20 | PIE and migration | 7 | Preface; Chapters 17–19 |
| 21 | Radiance | 7 | Chapters 19–20 |
| 22 | Inside-out conclusion | 2, 3, 4, 8 | Preface; Epilogue; revised thesis summary |
| 23 | Chapter routes | All | Current manuscript headings and YAML |
| 24 | Essential terms and sources | All | Guide and source packet |

## Source Anchors and Boundaries

- Regional counts: `manuscript/as_1_08_superset.md`, §§8.3–8.4; `inventory-atlas-coverage-surveys` in `manuscript/as_endnotes.md`; Appendix 4. Each total combines three languages against 23 base consonantal positions, with the ten heavy-breath stops excluded. Present-day datasets support the book's architectural comparison; they do not independently date the engineering or prove a historical borrowing event.
- Atoms and word families: Chapter 10 §§10.2, 10.10; Chapter 12 §12.2. The ⟪कृ⟫ family shows related forms, not immediate one-step concatenations.
- Count: Chapter 12 §12.7; the bounded reconstruction records 12,846,458 word-meaning entries before the separate expansion of person, number, and case. Generated entries are not a count of historically attested dictionary headwords. Use the current analysis total, not earlier 20-million or 3-million versions.
- Word-list story: Chapter 2 §2.3 and endnote `paspashahnika-brihaspati-indra-word-list`. Retell as Patañjali's story, not an event independently dated by this guide.
- Verbs: Chapter 11 §§11.1–11.3, especially ⟪इ⟫ → एति and ⟪भू⟫ → भवति. Glosses describe the illustrated form; a verb does not reveal an unnamed person's individual identity.
- Meter: Chapter 16 and endnote `vedic-akaranta-instrumental-plural-range`, RV 3.32.2d and 3.32.3d. The two endings occupy different places in their respective eleven-syllable lines. Do not imply that merely counting eleven syllables tests all of Triṣṭubh, or claim a pitch change without a demonstrated comparison.
- Documentation: Chapter 2 §2.2; `tolkappiyam-grammar-and-tamil-change`, `tamil-sanskrit-distributed-grammar`, `arabic-religio-political-authority`. Arabic's formal tradition is institutionally maintained; do not add a claim that its entire language is literally unchanged.
- Panini: Chapter 5. Keep analyst, decoder, and documenter. Do not redefine the ordinary word codification as necessarily state coercion.
- Three shantis: the three-domain inside-out arrangement is explicitly the author's interpretation. As clarified by the author on 20 September 2026, every volume of *Second Shanti* focuses on the second domain. The first and third domains provide context; they are not subjects assigned to later volumes. No new direct traditional quotation is introduced.
- Fractal: repeated design discipline at several scales, not a demonstrated mathematical self-similarity or a claim that every sound carries an independently fixed meaning.
- Sentence illustration: the two रामः / सीतां sentences are newly composed teaching examples applying the case-ending explanation in Chapter 12 §12.5; they are not quotations from a Vedic passage.
- Indian origin, PIE, and radiance: explain the book's contested thesis as its thesis. Distinguish shared sounds, structural comparison, and proof of historical descent. Migration evidence does not by itself identify a language's designers. Do not imply the guide independently verifies the book's full historical conclusions.

## Later Review

Author review remains necessary before public release. Check the overall emphasis, the two-page Indian-home treatment, and the balance between the language demonstration and the three-shanti frame. A physical A5 print proof remains necessary before a print run. No website publication or imposed printer signature is part of this task.

## Second Revision: 19 September 2026

### Six-Pass Execution

The author approved using all 101 invitations and an expanded two-part guide. Each invitation will appear once, either beside the introductory narrative or in the chapter-by-chapter exploration. The main manuscript remains untouched.

| Pass | Status | Scope |
|---|---|---|
| 1. Restructure | Complete | Two parts; separate Oṃ and sound-to-atom demonstrations; all invitation IDs retained in `invitations.json`. |
| 2. Introductory narrative | Complete internally | Added separate Oṃ and measured atom-construction pages; strengthened the memory and inside-out connections. Kept the two-page subcontinental-home treatment. |
| 3. Exploration guide | Complete | Seventeen exploration pages; 19 invitations beside the narrative and 82 in the exploration, all 101 used once. |
| 4. Figures and Sanskrit | Complete | Ten diagrams use the shared palette, icons, and scaffold geometry, with additional Devanagari. All diagram text outlined for PDF; minimum label size 9.29 pt at printed width. |
| 5. Editorial and coverage check | Complete against manuscript | Varied sentence lengths and familiar vocabulary; named and numbered destinations checked; 101 invitations exactly once; civilizational argument retained. |
| 6. Build and visual QA | Complete digitally | 42-page A5 interior, four cover faces, 46-page combined copy. All page images inspected; grayscale grid inspected separately; fourteen tests pass. Author review and physical proof remain open. |

The author requested stronger visual continuity with the book, more Devanagari, and concrete curiosity prompts drawn from every chapter. The first draft's 24-page count is no longer a ceiling. The original pass table above records the delivered first draft, not completion of these additions.

| Task | Status | Record |
|---|---|---|
| Inspect shared icons and established figure geometry | Complete | Identified the shared pyramid, swastika, Sanskrit sun, calibration, mouth, ear, memory, and Oṃ icons, plus the established mātrā hex geometry. |
| Build a chapter-by-chapter curiosity bank | Complete against current manuscript | [curiosity_map.md](curiosity_map.md): at least four candidates for every Chapter 0–20, additional front-matter/Epilogue/appendix pointers, and a proposed topic-based placement map. |
| Revise booklet copy and place printed pointers | Complete | Two-part guide with every invitation printed once. The Oṃ and sound-to-atom demonstrations have their own pages. |
| Revise figures and Devanagari labels | Complete | Reused shared icons and measured hex shapes; labels inspected in outlined exports. |
| Reflow and verify the expanded A5 guide | Complete digitally | Page count increased to 42, without shrinking body type. Four crowded-page invitations moved to the chapter guide; Chapter 0/1 and Chapter 19/20 entries given separate pages. |

The earlier curiosity-bank pass changed no prose and did not rebuild the PDF. It corrected one production locator: Chapter 8's main survey method and comparisons are in §§8.3–8.4, not §§8.2–8.3. The subsequent six passes produced the expanded booklet described above.

## First-Draft Delivery Record: 19 September 2026

- Source edition label retains 18 September, the date drafting began.
- `output/pdf/readers_guide/atomic_sanskrit_readers_guide.a5.pdf`: 24-page interior.
- `output/pdf/readers_guide/atomic_sanskrit_readers_guide.a5.print.pdf`: identical interior in ordinary reading order, not imposed or PDF/X-certified.
- `output/pdf/readers_guide/atomic_sanskrit_readers_guide.cover.pdf`: four cover faces with existing author biography, contact details, and QR code to `https://secondshanti.org/as/`.
- `output/pdf/readers_guide/atomic_sanskrit_readers_guide.a5.complete.pdf`: 28-page combined reading copy with bookmarks.
- Word count uses Pandoc plain-text output, including headings and reading pointers but excluding HTML page markers, image paths, SVG labels, and the separate cover.
- Source/figure/PDF tests cover page IDs, pointers, counts, figure existence and font sizes, outlined exports, trim dimensions, PDF metadata, and absence of accidental tool names or placeholders.
- Main manuscript files and the main PDF build were not edited. Earlier thesis-summary changes remain in the worktree; this task neither reverts nor commits them.

## Revised Delivery: 19 September 2026

This revision supersedes the first-draft PDFs at the same output paths.

| Interior pages | Contents |
|---|---|
| 1 | Title |
| 2–5 | Purpose, sound-to-order connection, two directions of order, three shantis |
| 6–8 | Speaking body, Oṃ, sound grid |
| 9–10 | Sanskrit's subcontinental home: sounds and architecture of order |
| 11–15 | Measured atom, word family, generative count, verb, sentence |
| 16–20 | Two domains, calibrant, distributed checks, threats to memory, Pāṇini |
| 21–24 | Categories, PIE, radiance, return to inside-out civilizational order |
| 25–41 | Explore the Book: front matter, every chapter, Epilogue, all ten appendices |
| 42 | Essential terms and source guidance |

- Interior: 42 pages, 8,367 words including titles, invitations, and destinations; excludes figure labels and cover copy.
- Complete reading copy: 46 pages, including four cover faces. The `.print.pdf` is the same 42-page interior in reading order, without imposed signatures or PDF/X certification.
- Ten outlined vector diagrams; seven shared icon instances and 28 tiles built from the established scaffold geometry. Devanagari labels are supported by IAST or plain English according to available space.
- All 101 invitations appear once: 19 in Part I and 82 in Part II. The bank retains all Chapter 0–20, front-matter, Epilogue, and appendix invitations.
- Pages increased instead of shrinking body type: STIX Two Text 11/14.4 pt with Tiro Devanagari Sanskrit. Four invitation moves resolved crowding on the grid, categories, PIE, and radiance pages; no introductory paragraph was deleted to make those pages fit.
- Every numbered and named invitation destination was checked against current manuscript headings. The calculations and comparative counts remain aligned with the full book, not independently reverified here.
- Fourteen tests pass. PDF fonts are embedded; no missing-glyph warnings, overfull boxes, or out-of-page text. All page contact sheets and diagram exports inspected; grayscale sound-grid rendering checked with Poppler.
- Canonical files are `manuscript/readers_guide.md`, `manuscript/explore_book.md`, and `invitations.json`. The build's `qa_report.json` records every invitation's actual page topic and the current per-page word count.
- No main-manuscript, main-build, or website changes. No commit or push performed. Author review and a physical print proof are still required before public distribution.

## Language Review: 20 September 2026

The author identified an unclear shift into instructions at line 26 and requested a review of the remaining guide. Both prose files and all 101 invitations were read. The edits address voice, awkward constructions, abstract transitions, and unnecessarily technical vocabulary. They do not remove an argument, example, figure, or invitation, or change the generated totals or evidence boundaries.

The default voice explains directly. Instructions remain where readers can perform an actual demonstration, such as comparing क and ख, or choose a chapter to read. Questions remain invitations into the book rather than exercises that the booklet leaves unexplained.

### Selected Before and After Wording

These excerpts identify the main kinds of correction; the source files contain the complete revised paragraphs.

| Location | Before | After |
|---|---|---|
| From Sound to Order | "Begin with a sound ... Combine selected sounds ... Use that unit ..." | "Sanskrit builds larger expressions from smaller parts," followed by गम् (*gam*) and an explanation of how a learner can examine a completed word. |
| From Sound to Order | "The next step connects language with civilization." | "Words and sentences also allow people to pass on stories about how to live." |
| From Sound to Order | "larger forms of meaning and responsibility" | "how sounds form words, how words express ideas, and how shared ideas guide people's conduct" |
| Two Directions of Order | "The difference concerns its place." | A king or government "serves the order and is judged by the same standard as everyone else." |
| Begin with the Mouth | "The written form क ... also contains an important distinction." | Directly explains that क represents क् joined to अ. |
| An Ordered Field of Sound | "The final position directs sound through the nose." | "The last sound in each row passes through the nose." |
| Sanskrit's Subcontinental Home | "join that regional pattern to the grammar and the communities" | "examine how the sound evidence relates to Sanskrit's grammar and to the communities" |
| A Shared Home for Knowledge | "examine a wider combination"; "Tamil helps explain the third part" | Names language analysis and teaching communities directly; Tamil explains how knowledge circulates without central control. |
| How Sounds Form an Atom | "The process begins inside sound and continues outward into expression." | "sounds form an atom, and the atom becomes the basis for words with related meanings" |
| Small Forms, Large Families | "add material before or after the atom" | "adds sounds or endings before or after the atom" |
| More Than a List of Words | "Combining completed bases opens further possibilities." | "Words already formed can then combine to create further expressions." |
| Completing an Action Word | "The verb carries information about the action and its participants." | "The verb tells us about the action and those involved in it." |
| Words Keep Their Roles | "understanding can proceed back through those parts" | "a learner can understand the expression by examining how those parts combine" |
| One Language, Two Domains | "different permissions for preservation and creation" | Explains that Vedic examples allow people to check their new expressions. |
| What the Vedas Calibrate | "The reference does not play the musician's next composition." | Explains tuning an instrument against a known note and using the tuned instrument for different compositions. |
| What the Vedas Calibrate | "complete instances of Sanskrit available in sound" | "complete spoken examples of Sanskrit" |
| Many People Can Check | "The standard exists in many people's knowledge rather than in one person's permission to approve it." | "Because many people know the standard, they can check the recitation without waiting for one person or institution to approve it." |
| Two Threats to Memory | "it introduces a material dependency"; "a destroyed copy cannot correct its reader" | Names records that can be damaged or withheld, and readers who can no longer consult a destroyed copy. |
| What Pāṇini Contributed | "Sanskrit analysis had teachers and debates before him." | "Earlier teachers had also studied Sanskrit and debated its construction." |
| What a Label Can Conceal | "The metaphor describes the argument's progression, not a substitute for its evidence." | Explains what removing a block represents and identifies the language as the evidence. |
| The Ancestor Above Sanskrit | "No surviving speaker's recording or written account gives us PIE in use." | "No recording or written passage gives us PIE in use." The next sentence explains the patterns on which the reconstruction argument depends. |
| Knowledge Traveling Outward | "The external comparisons retain selected resemblances without the complete connection." | "Other languages share particular features of Sanskrit without retaining that complete system," within the paragraph stating the book's argument. |
| Knowledge Traveling Outward | "routes with records of teaching or translation" | Names teachers and translators passing knowledge from one language to another, distinguished from proposed routes inferred through comparison and contact. |
| The Order Begins Within | "a familiar way to return from language to life" | "a familiar example of calibration beyond language" |
| Exploration: opening | "each offers somewhere further to go" | Explains the chapter arrangement and how to return to Part I for the larger argument. |
| Exploration: Chapter 0 | "follows the thought carried within them into the book's larger argument" | Explains what familiar examples reveal about Sanskrit and why they matter. |
| Exploration: Chapter 1 | "follows that distinction into institutions" | Explains how institutions and teaching can hide achievements through misleading categories. |
| Exploration: Chapter 2 | "Arabic and Tamil allow Chapter 2 to compare" | Makes the chapter the subject of the comparison and names the role of the Vedas. |
| Exploration: Chapter 7 | "The reader already possesses the instrument examined in Chapter 7." | "Chapter 7 examines the instrument you use whenever you speak." |
| Exploration: Chapter 19 | "occupy the source position in dictionary entries" | "dictionaries came to present its hypothetical words as the ancestors of recorded words" |
| Exploration: Epilogue | "The invitation extends beyond birth or ancestry. Its measure is conduct." | "The invitation to become आर्य (*ārya*) is based on conduct rather than birth or ancestry." |
| Invitation C03-2 | "reviewed thirty-five scholars on the word" | "reviewed the arguments of thirty-five scholars about" |
| Invitation C06-1 | "puts गौः ... beside four departures from it" | "compares गौः ... with four altered forms" |
| Invitation C08-3 | "Where do the Central Asian comparison languages lack the tongue positions ...?" | "Which sounds familiar in Indian speech are missing from the Central Asian languages in the comparison?" |
| Invitation C17-3 | "carry an earlier action into the next" | "show that the eating happened first" |
| Invitation C19-4 | "the language it came from stays in place" | "without the speakers of the source language moving there" |
| Invitation A06-1 | "which prefer its end" | "which occur most often at its end" |

### Layout and Verification

- The first render revealed five spillovers. To retain comfortable type and complete explanations, invitations C10-5, C08-4, and C06-3 moved to their respective chapter entries. The sound-to-order page retains a short Chapters 10-12 pointer.
- Chapters 2 and 3 now have separate exploration pages, as do Chapters 8 and 9. The guide has 44 interior pages and a 48-page complete reading copy, including the four cover faces. No figure was shrunk.
- All 101 invitations remain, each appearing once: 16 in Part I and 85 in Part II. Destinations are unchanged.
- The new interior count is 8,427 words, compared with 8,367: an increase of 60 words. The count includes headings, invitations, and destinations, but excludes figure labels and cover copy.
- Edition label updated to 20 September 2026. All four PDF outputs rebuilt at their existing paths.
- Fourteen tests pass; no missing glyphs, overfull boxes, or out-of-page text. All 44 interior pages and four cover faces inspected on contact sheets, with additional full-size Poppler checks for pages 3 and 31.
- Main manuscript, figures, website, and shared build script unchanged. No commit or push. Author review and physical proof remain open.

## Further Uncompression: 20 September 2026 (Source Only)

The author flagged "People make the connection between language and order. They must understand what they remember..." as outline-like prose and approved expanding it and similar passages. This pass explains what people learn, check, judge, and correct instead of merely naming a relationship between language and order. Sentence lengths vary with the explanation; the pass does not aim for a fixed word or page budget.

### Selected Before and After

| Location | Before | After |
|---|---|---|
| From Sound to Order | "People make the connection between language and order." | "A person who remembers a story must still decide what it means for his own actions." The paragraph explains how the person considers the consequences in the story and applies its lesson to a present choice. |
| Two Directions of Order | The account of an inside-out order named shared examples and correction without explaining how people use them. | Teachers discuss why choices helped or harmed others. A learner recognizes his own mistakes, and others familiar with the examples can point out what he has missed. |
| The Three Shantis | The connection relied on an "architectural interpretation" and the "integrity of smaller parts." | The explanation follows a person's thoughts and actions into relationships and then the wider world, before relating that construction to Sanskrit's smaller units and shared standards. |
| Small Forms, Large Families | "The family connects language to thought..." | Names what कर्म (*karma*), कर्तृ (*kartṛ*), and कार्य (*kārya*) each express, and how all three relate to doing. |
| More Than a List of Words | The distinction between new meanings and grammatical forms was compressed. | Compares "a doer" with "what ought to be done," then explains why making "doer" plural belongs to the separate grammatical expansion. |
| Completing an Action Word | "More happens inside this formation than adding an ending." | "The learner needs to understand how भू became भव् before अ and the ending ति joined it." The chapter pointer explains where readers can follow those sound changes. |
| Words Keep Their Roles | The comparison between the atom and a rule named their shared discipline. | Explains that a rule must retain necessary information, avoid unnecessary words, and remain clear enough to apply again; then identifies what Chapter 10 tests at the smaller scale. |
| Many People Can Check | The systems-engineering claim distinguished language design from preservation without fully developing the difference. | Separates sounds, word formation, and grammar from the teaching, error detection, and correction needed to maintain them across generations. |
| What Pāṇini Contributed | "Documentation belongs..." summarized the relationship. | Names the different contributions of grammar, Vedic examples, and teachers, then explains why crediting grammar alone leaves the Tamil comparison unresolved. |
| The Order Begins Within | Three compact clauses summarized fractal, calibrant, and radiant. | Each now has its own paragraph explaining what readers can examine, compare, or learn from others. |

### Other Changes

- Expanded the links between the subcontinental sound field and its teaching communities, between the two domains, and between language analysis and judgments about conduct.
- Replaced abstract transitions in the accounts of categories, PIE, radiance, and temple practice with the specific comparisons or decisions involved.
- Expanded chapter introductions in Part II where they named an argument without explaining what a reader would examine. These remain introductions, not replacements for the chapters.
- Clarified invitations C05-3, C12-3, C15-2, C15-4, and C19-2. All 101 invitations remain, with the same IDs, placements, and destinations.
- Retained every figure, the book's arguments and examples, and the generated totals. The verb example follows Chapter 11; the separation of word-meanings from grammatical forms follows Chapter 12 and the generative-wordspace note. No main-manuscript edits.

### Source Verification and Pending Layout

- Current source: 9,282 words, up 855 from the last-rendered 8,427. Counts include headings, invitations, and destinations, excluding figure labels and cover copy.
- Ten source-only tests pass. They check invitation coverage, destinations, page markers, source paths, numerical totals, figure sources and geometry, and word counting. The four output-dependent tests are deferred until an approved render.
- No PDF was generated or modified during this pass. The previous 44-page interior and 48-page complete PDF do not contain these changes. Their QA report describes that earlier render.
- The source still has 44 page markers, but fit has not been checked. At the next approved render, add or rearrange pages as needed without shrinking body type or compressing explanations to preserve the previous count.
- Main manuscript, figures, website, and build scripts remain unchanged. No commit or push.

### Author Follow-up: Government and the Three Domains

The government paragraph now begins "In an inside-out order, a government..." and states its responsibility directly. The second domain explicitly includes how people treat other living beings. The third names natural and cosmic forces beyond direct human control, with the Sun's light and heat as a familiar example of their effect on life. These three requested changes bring the source count to 9,291 words, 864 above the last render. PDFs remain unchanged.

### Series Scope Correction

The author clarified that all volumes focus on the second domain. Removed the promise to develop the third domain in later volumes and corrected both introductions to the three shantis. The first and third domains establish context; future volumes examine government, economic life, and other aspects of order within the second domain. The source-boundary rule above now records this scope for future edits. Current source count: 9,361 words. No PDF generated.

### Why the Second Domain Needs Reconstruction

Added the approved contrast to "Why I Wrote This Book": Hindu society continues to practise ways of seeking inner shanti, while much of its knowledge of shared order was lost under Abrahamic pyramids. Language, stories, teaching, and practices retain parts from which the architecture can be reconstructed. The author's approved yoga-and-meditation paragraph appears verbatim. The introduction now explains reconstruction from first principles before introducing Sanskrit as a living example. Current guide source count: 9,481 words. Layout remains unverified pending an approved PDF build.

The author separately requested "from first principles" in the main manuscript. The Preface's existing reconstruction paragraph now names that method and explains it through learning a shared standard, recognizing mistakes, and correcting oneself and others without apex ownership. This is the only main-manuscript change in this follow-up.

#### Manuscript Review: Preface Expansion Applied

- **Preface, "Why Sanskrit Comes First":** the author approved the expansion below, excluding the sentence "The first and third explain the wider setting within which living beings must create order together." Applied the approved contrast after the opening explanation of the three recitations. Retained the next paragraph on language, memory, economic life, and why Sanskrit comes first.
- **Epilogue:** the "Order Through Calibration" conclusion already points future volumes toward economic life, political authority, and society's relationships. The later custodianship paragraph explicitly names the second domain. Neither needs another explanation of the series's scope.
- **Other forward references:** Chapters 5, 6, 14, 16, and the glossary describe further social and civilizational applications; none promises a volume devoted to the first or third shanti. Chapter 19's Iranian comparison also does not assign a volume to another shanti domain.
- **Series planning document, `reference/as_second_shanti.md` section 3.3:** this internal document remains stale. It limits the second shanti to the political volume, describes the loss as a lapse in practice, and leaves the third domain undefined. It should adopt the author's current account and the all-volumes scope; not edited in this pass.

Approved Preface insertion, now applied after the opening explanation of the three recitations:

> Hindu society has kept alive the knowledge through which a person can seek शान्ति (*śānti*) within himself. Yoga, meditation, and several other practices continue to thrive, giving people ways to understand their own minds and respond to anger, fear, or desire without being ruled by them. This is the first domain.
>
> The second concerns how people live with one another and other living beings. Over the last millennium, under the rule of Abrahamic pyramids, much of the knowledge through which society maintained order in this domain has been lost. Institutions were destroyed or displaced, and later generations learned to organize public life around commands from above. Yet parts of the earlier architecture remained alive in language, stories, teaching, and everyday practice.
>
> The third concerns natural and cosmic forces beyond direct human control that affect human beings and other life. All volumes of *Second Shanti* focus on the second domain.

This expansion replaces the existing sentences that briefly name the second domain; it does not repeat them. Reconstruction from first principles remains explicit in the preceding paragraph. No PDF generated and no commit or push. The internal series-planning correction above remains pending.

## Approved A5 and A4 Editions: 20 September 2026

The author authorized both renders: A5 at 11 pt and A4 at 12 pt. Both use the same 9,481-word source and retain all 101 invitations. No prose was cut or rewritten during this layout pass, and the main manuscript was not changed.

| Setting | A5 | A4 |
|---|---|---|
| Page size | 148 x 210 mm | 210 x 297 mm |
| Body type and leading | 11 / 14.4 pt | 12 / 16 pt |
| Mirrored inner margin | 20 mm | 25 mm |
| Interior pages | 50 | 40 |
| Complete PDF, including four cover faces | 54 | 44 |
| Smallest figure label at printed width | 9.13 pt | 12.6 pt |

- STIX Two Text and Tiro Devanagari Sanskrit remain the body fonts. Figures remain outlined vectors. Font embedding was checked in both interiors.
- The 44 source sections are no longer treated as fixed physical pages. Five A5 sections have planned paragraph-boundary continuations; five A4 invitation sections share pages with the preceding section. Body type and leading remain at the approved sizes.
- Each interior includes one intentional final blank page for duplex printing. Each size has an interior PDF, an identical `.print.pdf`, a four-face `.cover.pdf`, and a `.complete.pdf`. The unsuffixed cover filename remains an A5 compatibility alias.
- The builder accepts `--layout a5`, `--layout a4`, or `--layout all`. Reports and visual checks now live under `build/a5/` and `build/a4/`; older root-level reports describe earlier editions.
- All pages and cover faces were inspected in contact sheets. Selected pages were also inspected at larger size with Poppler, including the A5 continuation heading, the sound grid in grayscale, and grouped A4 chapter invitations. No missing glyphs, overfull boxes, or text outside the page were detected. All 19 tests pass, including printed font sizes, binding clearance, destinations, figure outlines, and duplex padding.
- Print at actual size, double-sided with long-edge flipping. Use the interior and cover files separately when printing covers on different stock. Confirm the printer's punch requirements with a physical proof before ordering copies. These are not imposed or PDF/X files and have no bleed or crop marks.
- No website deployment, print order, commit, or push was performed.

### Sonomer Label Follow-up (Source Only)

Replaced **Sound** with **Sonomer** beneath वर्ण in `inside_out.svg`, its accessible description, and the figure generator. The same asset appears in the introductory narrative and inside front cover of both editions. Introduced the term before the narrative diagram and paired it with वर्ण (*varṇa*) in the final terms list. General references to sound remain unchanged.

The source now contains 9,497 words, 16 more than the last render. All 13 source-only tests pass, including a new check for the figure labels and nearby explanation. PDF-dependent checks are deferred: neither edition nor its covers has been rebuilt, so the current PDFs and their QA reports still describe the previous source. Rebuild without `--skip-figures` at the next approved render.

### Authority and Architecture Icons (Source Only)

Replaced the two icons in `two_orders.svg` and its generator: `ic-pyramid` becomes `ic-authority`, and `ic-swastika` becomes `ic-architecture`. Both sit in centered 160 x 145 viewports below their headings and above their captions. Updated the accessible description and added a test for the selected shared assets. No prose changes or PDF rebuild.

### Hex-Node Diagram and Approved A4 Rebuild

The author supplied `figures/two_chains_hex_nodes.from-cd.svg` and approved an A4 rebuild. It replaces the plain two-chain `inside_out.svg`, not the separate `two_orders.svg` comparison. The original remains untouched; the figure generator promotes it to the canonical `inside_out.svg` with local STIX/Tiro fonts, an accessible description, and slightly larger, darker IAST labels. The original hex geometry, arrows, wording, and layout remain. Imported design sources are excluded from canonical figure exports and size checks.

The new figure appears on the front cover, interior title page, and "From Sound to Order" page. Earlier follow-up entries incorrectly called the cover placement "inside front cover"; it is on the front cover itself. The A4 rebuild also includes the preceding sonomer prose changes and authority/architecture icons. No further prose changes were made in this pass.

A4 remains 40 interior pages, including the final blank, plus four cover faces (44 pages in the complete copy), at 12 pt body type. All 101 invitations remain. The smallest diagram label prints at 12.15 pt. Figures were outlined, the affected pages and cover faces were inspected, and the main diagram page was checked with Poppler at larger size. All 22 tests pass with `GUIDE_TEST_LAYOUT=a4`; no missing glyphs, overfull boxes, unplanned continuation pages, or out-of-page text were detected.

A5 PDFs remain unchanged, with the previous figure and 9,481-word source. Current source and A4 contain 9,497 words. Recheck A5 page flow for the taller diagram when its next render is approved. No commit, push, website deployment, or print order.

### Both Editions Updated: Cover Hierarchy and Neutral Pronouns

The author approved the A5 rebuild, then requested a larger subtitle above "A Reader's Guide" and easy neutral substitutions for generic masculine pronouns. Both editions now contain those changes and the latest figures.

- On front covers and interior title pages, the order is *Atomic Sanskrit*, its full subtitle, then *A Reader's Guide*. Subtitle type is 17/21 pt in A5 and 18/22 pt in A4, with the guide label at 14/18 pt. Subtitle words do not hyphenate. A5 title-page blank space was reduced without shrinking its typography or figure.
- A5's "From Sound to Order" now breaks after the diagram and resumes under a repeated heading marked "Continued." This adds a content page and removes the need for the former final blank. A5 remains 50 interior pages and 54 with covers. A4 remains 40 interior pages, including its final blank, and 44 with covers. Body type and leading are unchanged.
- Eleven guide paragraphs were adjusted for neutral references to generic people, learners, and seekers. The opening now says "one can seek ... within oneself." Other passages use plural subjects or straightforward singular *they*. References to named people and grammatical examples remain unchanged. The main book manuscript was not edited.
- Shared source count is now 9,488 words, nine fewer than the preceding 9,497-word version. All 101 invitations remain. Both interiors, print copies, cover files, complete copies, and the A5 legacy cover alias were refreshed.
- Inspected the cover hierarchy, A5 diagram page and continuation, and affected page flow. All 23 tests pass across both sizes, including subtitle order and font sizes, page counts, bookmarks, source consistency, figure outlines, and binding clearance. No missing glyphs, overfull boxes, or out-of-page text were reported.
- Physical proofs remain pending. No commit, push, deployment, or print order.

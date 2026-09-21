# Architecture-First Introductions: Revision Record

Date: 21 September 2026
Status: source edits committed and deployed; both Reader's Guide PDF editions rebuilt after author approval. Other rendered copies remain unchanged.

## Publication Follow-up

Committed and pushed as `54a2109f`, then deployed with `as-deploy`. Rebuilt the A5 and A4 Reader's Guide PDFs: 70 and 44 interior pages respectively, plus four cover faces each. All 28 guide tests pass, and the revised opening pages were visually inspected. The source-only verification record below describes the earlier editorial pass; the current production details are in `booklet/readers_guide/production_record.md`.

## Approved Sequence

1. What does a language have to do with the architecture of सनातन (*Sanātan*)?
2. How has Sanskrit remained unchanged for thousands of years without a central authority enforcing it?
3. Explain the connection: learners use a shared standard to recognize and correct mistakes; the book follows the same inside-out design into civilizational life through shared stories, discernment, and responsibility.
4. Develop the linguistic evidence and the indictment of the pyramid from that purpose.

The architecture of order is the reason for studying Sanskrit, not a surprise extension added after a linguistic argument. Invariance makes its durability available for examination. This pass changes the order of exposition, not the book's evidence or the scope of its claims.

## Deployment

- Reader's Guide: inside-front introduction and opening narrative.
- Overviews: proposal overview and the reusable overview in Manjeet Kripalani's folder. Historical correspondence is unchanged.
- Spoken descriptions: 25-, 75-, and 200-word versions.
- Essays: order without an apex; Vedic distributed calibration; Oṃ; both sonomer versions; the public engineered-Sanskrit introduction.
- Cover copy: the challenge-led source used by the live landing-page build, all four reviewer alternates, and pre-publication back-cover Markdown.

The Oṃ, sonomer, and Vedic-recitation essays retain their distinctive openings. Their transitions now explain why the example matters to inside-out order. The polity essay still begins with government. No identical opening was imposed on every essay.

The public engineering introduction also lost its stale claim that the book has eighteen chapters. Its existing source statistics were not reverified or changed in this editorial pass.

## Reviewed Without Rewriting

The retroflex, migration, and Brāhmī essays pursue narrower arguments about sound, origin, and writing. Their openings do not need a general introduction to the whole book, so they were left alone. Historical drafts, sent messages, thesis inventories, the main manuscript, and endnotes were not rewritten.

The old `web/public/as/landing-copy.md` is not the landing-page source configured in `build_html.py`. This pass updates the configured `cover/manuscript/jacket_copy_challenge_led.md` instead of treating the older document as a second canonical source.

## Verification and Publication State

- Twenty Reader's Guide source tests pass; all 101 invitation IDs and destinations remain intact.
- `git diff --check` passes.
- No PDF build, deployment, commit, or push in this pass.
- Existing guide, essay, and overview PDFs do not yet include these changes.
- Print-cover SVGs and PDFs remain unchanged. The Markdown back-cover revision needs a separate artwork/layout pass before printing.
- On the next approved guide render, recheck both inside front covers and the opening narrative's paragraph-based continuation breaks.

## Exact Before and After

The diff below retains the replaced wording for comparison. Minus lines are the former wording; plus lines are the revised wording. Context lines are unchanged. No removed claim requires a new home in the manuscript; the short pitches deliberately omit technical detail that remains in the longer overviews.

```diff
diff --git a/writing/books/atomicSanskrit/booklet/readers_guide/build_readers_guide.py b/writing/books/atomicSanskrit/booklet/readers_guide/build_readers_guide.py
index 245a6665..dcb94c2c 100644
--- a/writing/books/atomicSanskrit/booklet/readers_guide/build_readers_guide.py
+++ b/writing/books/atomicSanskrit/booklet/readers_guide/build_readers_guide.py
@@ -260,9 +260,11 @@ def make_interior(book, cfg, pages, invitations):
 def make_cover(book, cfg):
     text = [preamble(book, cfg), r"\pagestyle{empty}", title_page(book, cfg, cover=True), r"\clearpage"]
     text.append(r"\pagetitle{An Introduction to the Argument}{inside-front}")
-    text.append(latex("""How can a language remain unchanged while people continue creating new expressions? What does its preservation reveal about the order of the civilization that cares for it?
+    text.append(latex("""What does a language have to do with the architecture of सनातन (*Sanātan*)?
 
-This guide follows the argument of *Atomic Sanskrit* from the speaking body through sounds, words, sentences, and Vedic transmission. It explains the book's case for an engineered language within an inside-out architecture of सनातन (*Sanātan*), then examines how Western philologists and their institutional successors conceal that architecture through the history they teach.
+How has Sanskrit remained unchanged for thousands of years without a central authority enforcing it?
+
+*Atomic Sanskrit* begins with language because Sanskrit demonstrates how people can maintain order through a shared standard that no ruler owns. This guide follows that argument from the speaking body through sounds, words, sentences, and Vedic transmission. It explains how the same inside-out design extends into the way people learn, judge their actions, and correct one another. It then examines how Western philologists and their institutional successors conceal that architecture through the history they teach.
 
 You can follow the examples without knowing Sanskrit. The first part explains the argument in familiar English, supported by Devanagari and diagrams. The second part offers a chapter-by-chapter route into the full book.
 
diff --git a/writing/books/atomicSanskrit/booklet/readers_guide/manuscript/readers_guide.md b/writing/books/atomicSanskrit/booklet/readers_guide/manuscript/readers_guide.md
index 706c39bf..74da2317 100644
--- a/writing/books/atomicSanskrit/booklet/readers_guide/manuscript/readers_guide.md
+++ b/writing/books/atomicSanskrit/booklet/readers_guide/manuscript/readers_guide.md
@@ -14,7 +14,11 @@ Hindu society has kept alive the knowledge through which one can seek शान
 
 The second concerns how people live with one another and other living beings. Over the last millennium, Abrahamic rulers destroyed or displaced institutions through which Hindu society maintained order in this domain. They imposed commands from above, disrupting the transmission of knowledge that had guided public life. Much of that knowledge was lost, but parts of the earlier architecture remained alive in language, stories, teaching, and everyday practice.
 
-*Second Shanti* is my attempt to reconstruct that architecture from first principles. I begin with what we can still examine: how people learn a shared standard, recognize mistakes, exercise restraint, and correct one another without giving an apex ownership of the standard. Sanskrit is a living example through which we can study those principles in detail.
+*Second Shanti* is my attempt to reconstruct that architecture from first principles. I begin with what we can still examine: how people learn a shared standard, recognize mistakes, exercise restraint, and correct one another without giving an apex ownership of the standard.
+
+What does a language have to do with the architecture of सनातन (*Sanātan*)? Sanskrit demonstrates these principles in daily teaching and practice. Learners develop the ability to check their pronunciation and word formation against examples that many others also know. A ruler need not authorize each correction.
+
+How has Sanskrit remained unchanged for thousands of years without a central authority enforcing it?
 
 Generations of teachers and students had maintained Sanskrit's sounds and word-forming methods through teaching and practice. They could compare what they said with examples that others also knew, recognize mistakes, and correct them. The Vedas kept those examples available for later generations to hear and learn.
 
diff --git a/writing/books/atomicSanskrit/cover/manuscript/back_cover_prepublication.md b/writing/books/atomicSanskrit/cover/manuscript/back_cover_prepublication.md
index 89d7f29b..4514ccd5 100644
--- a/writing/books/atomicSanskrit/cover/manuscript/back_cover_prepublication.md
+++ b/writing/books/atomicSanskrit/cover/manuscript/back_cover_prepublication.md
@@ -2,7 +2,9 @@
 
 **PRE-PUBLICATION REVIEW COPY · SEPTEMBER 2026 · NOT FOR SALE**
 
-Did Sanskrit "evolve" over time until Pāṇini "codified" it? Or was Sanskrit engineered?
+What does a language have to do with the architecture of सनातन (*Sanātan*)?
+
+How has Sanskrit remained unchanged for thousands of years without a central authority enforcing it?
 
 Are the Vedas merely "religious chants," or do they preserve the architecture of a language and the civilization bonded to it?
 
@@ -18,7 +20,7 @@ If Sanskrit's engineered architecture was already operating within the Vedas lon
 
 For starters, he did *not* codify Sanskrit. Pāṇini's contribution is extraordinary, but the codification myth obscures the nature of his achievement. *Atomic Sanskrit* uncovers his actual role and explains why his documentation remains unmatched.
 
-In a world dominated by top-down pyramidal polities, Sanskrit provides living evidence that durable order does not require an apex. Its calibrant is distributed, and alignment remains voluntary. *Atomic Sanskrit*, the first volume of the *Second Shanti* series, begins reconstructing this alternative architecture at the scale of language.
+In a world dominated by top-down pyramidal polities, Sanskrit demonstrates an inside-out order. People learn a shared standard, recognize mistakes, and correct themselves and one another without an apex owning the standard. The same design extends into civilizational life through stories and examples that help people judge their conduct. *Atomic Sanskrit*, the first volume of the *Second Shanti* series, begins reconstructing this alternative architecture at the scale of language.
 
 ## About the Author
 
diff --git a/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_challenge_led.md b/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_challenge_led.md
index cf7d4e4b..eb51ae94 100644
--- a/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_challenge_led.md
+++ b/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_challenge_led.md
@@ -1,6 +1,8 @@
 # *Atomic Sanskrit* Jacket Copy — Challenge-Led
 
-Did Sanskrit "evolve" over time until Pāṇini "codified" it? Or was Sanskrit engineered?
+What does a language have to do with the architecture of सनातन (*Sanātan*)?
+
+How has Sanskrit remained unchanged for thousands of years without a central authority enforcing it?
 
 Are the Vedas merely "religious chants," or do they preserve the architecture of a language and the civilization bonded to it?
 
@@ -16,4 +18,4 @@ If Sanskrit's engineered architecture was already operating within the Vedas lon
 
 For starters, he did *not* codify Sanskrit. Pāṇini's contribution is extraordinary, but the codification myth obscures the nature of his achievement. *Atomic Sanskrit* uncovers his actual role and explains why his documentation remains unmatched.
 
-In a world dominated by top-down pyramidal polities, Sanskrit provides living evidence that durable order does not require an apex. Its calibrant is distributed, and alignment remains voluntary. *Atomic Sanskrit*, the first volume of the *Second Shanti* series, begins reconstructing this alternative architecture at the scale of language.
+In a world dominated by top-down pyramidal polities, Sanskrit demonstrates an inside-out order. People learn a shared standard, recognize mistakes, and correct themselves and one another without an apex owning the standard. The same design extends into civilizational life through stories and examples that help people judge their conduct. *Atomic Sanskrit*, the first volume of the *Second Shanti* series, begins reconstructing this alternative architecture at the scale of language.
diff --git a/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_question_led.md b/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_question_led.md
index 315735f4..e48def9e 100644
--- a/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_question_led.md
+++ b/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_question_led.md
@@ -1,8 +1,12 @@
 # *Atomic Sanskrit* Jacket Copy — Question-Led
 
-All natural languages change over time. Sanskrit, and Sanskrit alone, has thrived for thousands of years without changing. Yet its speakers have continued to create new words, compose poetry, record mathematics, explain astronomy, conduct trade, and describe a changing world.
+What does a language have to do with the architecture of सनातन (*Sanātan*)?
 
-How did Sanskrit remain invariant while continuing to generate new expression? Why do its smallest units of meaning behave like atoms rather than botanical roots? What do the Vedas preserve beyond their own words and meanings? Why does Sanskrit operate through one domain that preserves received content exactly and another that remains open to new composition?
+How has Sanskrit remained unchanged for thousands of years without a central authority enforcing it?
+
+Sanskrit demonstrates an inside-out order: learners develop the ability to recognize mistakes and correct them against a shared standard that no ruler owns. Its speakers continue to create new words, compose poetry, record mathematics, explain astronomy, conduct trade, and describe a changing world without rewriting that standard.
+
+Why do Sanskrit's smallest units of meaning behave like atoms rather than botanical roots? What do the Vedas preserve beyond their own words and meanings? Why does Sanskrit operate through one domain that preserves received content exactly and another that remains open to new composition?
 
 *Atomic Sanskrit* follows these questions into the engineering of the language. Sanskrit begins with the anatomy of speech. Sounds occupy precise positions in the human mouth. Those sounds combine into compact units of meaning, and those units generate words and sentences. This internal architecture is one feat of engineering.
 
@@ -14,4 +18,4 @@ For starters, he did *not* codify Sanskrit. Pāṇini’s contribution to the la
 
 The same evidence opens a larger challenge. Why did Esperanto begin to drift despite having an explicitly designed grammar, while Sanskrit did not? Why was the imaginary language called Proto-Indo-European placed above Sanskrit, a real language with a complete architecture? What if the similarities among Sanskrit, Greek, Latin, and other Eurasian languages came from Sanskrit moving outward rather than from an imaginary ancestor moving into India?
 
-These are not merely questions about language. *Atomic Sanskrit* asks what Sanskrit can reveal about two ways of creating order: shared alignment or control from above. It demonstrates that Sanskrit is *Saṃskṛti*, and that the same radiant, calibrant, and fractal architecture extends from sound and grammar into civilizational order.
+*Atomic Sanskrit* follows the same inside-out design into civilizational life. Shared stories help people examine their choices and correct their conduct, just as shared examples let a learner check a sound or a word. The book demonstrates that Sanskrit is *Saṃskṛti*: the language and the civilization share a radiant, calibrant, and fractal architecture in which the standard remains available and no apex can own it.
diff --git a/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_revelations.md b/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_revelations.md
index 64db3bc5..203fb1c3 100644
--- a/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_revelations.md
+++ b/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_revelations.md
@@ -1,8 +1,10 @@
 # *Atomic Sanskrit* Jacket Copy — Questions and Revelations
 
-How can a language remain unchanged for thousands of years and yet possess an unmatched capacity for new expression?
+What does a language have to do with the architecture of सनातन (*Sanātan*)?
 
-Sanskrit did exactly that. Its architecture has remained invariant across thousands of years. Throughout that time, speakers have used it, and continue to use it today, to compose epics and romantic poetry, preserve mathematical formulae, calculate planetary movements, conduct trade, and create words for circumstances that earlier generations had never encountered.
+How has Sanskrit remained unchanged for thousands of years without a central authority enforcing it?
+
+Sanskrit's architecture has remained invariant across thousands of years while speakers continue to compose epics and romantic poetry, record mathematical formulae, calculate planetary movements, conduct trade, and create words for circumstances that earlier generations had never encountered. Its caretakers keep the same standard available without giving any one institution ownership of it.
 
 *Atomic Sanskrit* reveals how. Sanskrit's internal architecture begins in the human mouth. Its sounds occupy anatomical coordinates. Those sounds form stable units of meaning that behave like *atoms*, not roots of a language family tree. The atoms combine and recombine, demonstrating that the language was engineered for new expression without rebuilding its foundation.
 
@@ -18,4 +20,4 @@ The book exposes how Western philologists constructed an imaginary language call
 
 *Atomic Sanskrit* demonstrates that Greek, Latin, and other Eurasian languages preserve partial reflections of Sanskrit’s radiance as it traveled outward. Their similarities record contact with a complete architecture, not descent from an imaginary parent.
 
-The final revelation extends beyond language. Sanskrit and *Saṃskṛti* share the same architecture. It is radiant because it gives without diminishing its source, calibrant because it preserves alignment without an apex, and fractal because the same pattern repeats at every scale. The first *Second Shanti* volume begins with language and uncovers an ancient alternative to order imposed from above.
+Sanskrit and *Saṃskṛti* share the same inside-out architecture. People learn a shared standard and develop the ability to judge and correct their own actions. The design is radiant because it gives without diminishing its source, calibrant because it maintains alignment without an apex, and fractal because the same pattern repeats at different scales. The first *Second Shanti* volume begins with language to demonstrate an ancient alternative to order imposed from above.
diff --git a/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_statement_led.md b/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_statement_led.md
index 2a86e920..7af6aac0 100644
--- a/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_statement_led.md
+++ b/writing/books/atomicSanskrit/cover/manuscript/jacket_copy_statement_led.md
@@ -1,8 +1,8 @@
 # *Atomic Sanskrit* Jacket Copy
 
-All natural languages change over time. Sanskrit, and Sanskrit alone, has thrived for thousands of years without changing. Yet it has allowed speakers to create new words, compose poetry, record mathematics, explain astronomy, conduct trade, and describe a changing world.
+*Atomic Sanskrit* examines the inside-out architecture of सनातन (*Sanātan*) through language. Sanskrit demonstrates how people can learn a shared standard, recognize mistakes, and correct one another without an apex owning that standard. It has thrived for thousands of years without changing, while speakers continue to create new words, compose poetry, record mathematics, explain astronomy, conduct trade, and describe a changing world.
 
-How has Sanskrit remained invariant for thousands of years while continuing to generate new expression? Why did that invariance matter? What role did the Vedas play? What did Pāṇini actually document? Why do languages across Eurasia reflect Sanskrit? And what can Sanskrit teach us about creating durable order without an apex?
+How has Sanskrit remained unchanged for thousands of years without a central authority enforcing it? Why did that invariance matter? What role did the Vedas play? What did Pāṇini actually document? Why do languages across Eurasia reflect Sanskrit?
 
 *Atomic Sanskrit* examines Sanskrit as an engineered system. Its internal architecture begins in the human mouth, where sounds occupy anatomical coordinates. Those sounds combine into compact units of meaning that generate words and sentences.
 
diff --git a/writing/books/atomicSanskrit/cover/manuscript/website_copy_questions_answers.md b/writing/books/atomicSanskrit/cover/manuscript/website_copy_questions_answers.md
index 13ef35ad..b6697001 100644
--- a/writing/books/atomicSanskrit/cover/manuscript/website_copy_questions_answers.md
+++ b/writing/books/atomicSanskrit/cover/manuscript/website_copy_questions_answers.md
@@ -1,6 +1,12 @@
 # *Atomic Sanskrit* Website Copy — What the Book Reveals
 
-## A Language That Should Not Exist
+## What Does Language Have to Do with सनातन (*Sanātan*)?
+
+What does a language have to do with the architecture of सनातन (*Sanātan*)? *Atomic Sanskrit* begins with language because Sanskrit demonstrates how people can maintain order through a shared standard that no ruler owns. Learners develop the ability to recognize mistakes and correct themselves and one another. The book follows this inside-out design into civilizational life, where shared stories and examples help people judge how to act.
+
+## How Has Sanskrit Remained Unchanged?
+
+How has Sanskrit remained unchanged for thousands of years without a central authority enforcing it?
 
 All natural languages change over time. Sounds shift, words acquire new meanings, grammar changes, and later generations struggle to understand older compositions. Esperanto shows that an explicitly designed grammar does not solve this problem. Once people adopt a language, ordinary use begins to reshape it.
 
@@ -34,7 +40,7 @@ But Proto-Indo-European has no surviving text, inscription, recitation lineage,
 
 ## Two Architectures of Order
 
-The inquiry eventually reaches beyond language. What can Sanskrit reveal about two ways of creating order: shared alignment or control from above?
+The language makes the contrast between two architectures of order available for examination. A learner can hear a shared example and correct a mistake without waiting for a central authority to rule on it. People throughout society can acquire that ability.
 
 Sanskrit preserves order through a distributed calibrant. Every participant can align with the same invariant architecture, but no ruler, academy, or central institution can own it. The opposing architecture places authority at an apex, controls access, and turns correction into obedience.
 
diff --git a/writing/books/atomicSanskrit/outreach/articles/order_without_an_apex.md b/writing/books/atomicSanskrit/outreach/articles/order_without_an_apex.md
index 30c28427..10416c99 100644
--- a/writing/books/atomicSanskrit/outreach/articles/order_without_an_apex.md
+++ b/writing/books/atomicSanskrit/outreach/articles/order_without_an_apex.md
@@ -56,7 +56,7 @@ Calibrant order therefore accommodates disagreement. Discussion is one of the wa
 
 The distinction would collapse if one ruler, priesthood, or institution could alter the calibrant. Whoever owns the standard can eventually command everyone who depends upon it. Calibrant order therefore requires more than wise teaching. The standard must remain stable, widely available, and beyond capture.
 
-The Vedas demonstrate that such an architecture can exist.
+This is where language enters the inquiry into order. If people can keep Sanskrit unchanged for thousands of years without giving one institution ownership of its standard, they have already demonstrated a durable alternative to command from above. The Vedas allow us to examine how they did it.
 
 Hindu society preserved the Vedas as exact sound through many recitation lineages spread across the Indian subcontinent. Teachers trained students to reproduce the received pronunciation, vowel duration, pitch, sequence, and meter. Several recitation patterns passed the same words through different arrangements, allowing a departure hidden in one form to be exposed in another.
 
@@ -68,7 +68,7 @@ Sanskrit divides this work between two domains. The **वैदिक (*vaidika*
 
 One domain protected continuity. The other protected freedom to create.
 
-This is why the Vedas and Sanskrit belong inside an inquiry about political order. Together they demonstrate that exact and durable order can continue without placing the standard beneath one owner. *Atomic Sanskrit* follows that demonstration from the anatomy of sound through grammar and sentence to the systems of Vedic preservation.
+*Atomic Sanskrit* follows this inside-out architecture of सनातन (*Sanātan*) from sound through words and sentences to the people who learn and transmit them. Learners develop the ability to hear mistakes and make corrections against examples others also know. The same principle extends into civilizational life when people use shared stories to judge conduct and remain responsible for their own decisions. Later volumes examine how institutions can protect that responsibility without claiming ownership of the standard.
 
 **The pyramid protects a standard by owning it. The Vedic architecture protects the calibrant by making ownership impossible.**
 
diff --git a/writing/books/atomicSanskrit/outreach/articles/vedas_distributed_calibrant.md b/writing/books/atomicSanskrit/outreach/articles/vedas_distributed_calibrant.md
index b803398d..f1954c0a 100644
--- a/writing/books/atomicSanskrit/outreach/articles/vedas_distributed_calibrant.md
+++ b/writing/books/atomicSanskrit/outreach/articles/vedas_distributed_calibrant.md
@@ -7,6 +7,8 @@ Calling this “religious chanting” describes the occasion while missing the a
 
 The Vedas preserve words, but they also preserve the physical form of their utterance. Pronunciation belongs to the received content. So do vowel duration, pitch, sequence, pause, and meter. Hindu society therefore had to transmit more than a text. It had to transmit a trained mouth and a trained ear, and the system it built still functions.
 
+What does this achievement tell us about the architecture of सनातन (*Sanātan*)? Every trained reciter can recognize and correct a departure from a shared standard. No central office owns that standard. The ability to maintain order develops within the people who participate in it. Sanskrit's invariance across thousands of years lets us examine how such an inside-out order endures.
+
 ## One Passage, Several Recitations
 
 Suppose a passage contains three words: A, B, and C.
diff --git a/writing/books/atomicSanskrit/outreach/atomic_sanskrit_proposal_overview.md b/writing/books/atomicSanskrit/outreach/atomic_sanskrit_proposal_overview.md
index 29be0e30..977bba8a 100644
--- a/writing/books/atomicSanskrit/outreach/atomic_sanskrit_proposal_overview.md
+++ b/writing/books/atomicSanskrit/outreach/atomic_sanskrit_proposal_overview.md
@@ -1,6 +1,8 @@
 # *Atomic Sanskrit* Proposal Overview
 
-*Atomic Sanskrit: The Radiant, Calibrant, and Fractal Architecture of Sanātan* is the first volume of the *Second Shanti* series. It argues that Sanskrit is not a naturally evolving language later stabilized by Pāṇini. Sanskrit is an engineered, internally generative, and anti-entropic architecture whose design begins in the human mouth and extends into the civilization that preserved it.
+*Atomic Sanskrit: The Radiant, Calibrant, and Fractal Architecture of Sanātan* is the first volume of the *Second Shanti* series. What does a language have to do with the architecture of सनातन (*Sanātan*)? The book argues that Sanskrit demonstrates an inside-out order: people learn a shared standard, develop the ability to recognize mistakes, and correct themselves and one another without making an apex the owner of that standard.
+
+How has Sanskrit remained unchanged for thousands of years without a central authority enforcing it? The book examines the language's engineering together with the Vedic system that keeps it calibrated. Its design begins in the human mouth, extends through words and sentences, and remains available across generations through distributed teaching and transmission. This is the first demonstration in the series' reconstruction of civilizational order from first principles.
 
 The book combines architectural reconstruction with a sustained indictment. It contrasts calibrant order, which distributes an invariant standard without giving an apex ownership, with pyramidal order, which encloses knowledge and controls access. Sanskrit and the Vedas provide a living demonstration of calibrant order. The book argues that the institutions of the asuric pyramid deliberately concealed that demonstration through false categorization.
 
diff --git a/writing/books/atomicSanskrit/outreach/atomic_sanskrit_spoken_descriptions.md b/writing/books/atomicSanskrit/outreach/atomic_sanskrit_spoken_descriptions.md
index bd1b5b18..4a536386 100644
--- a/writing/books/atomicSanskrit/outreach/atomic_sanskrit_spoken_descriptions.md
+++ b/writing/books/atomicSanskrit/outreach/atomic_sanskrit_spoken_descriptions.md
@@ -2,20 +2,18 @@
 
 ## 25 Words
 
-*Atomic Sanskrit* reconstructs Sanskrit as an engineered language. The Vedas preserve its architecture as an invariant calibrant while the worldly domain meets a changing world.
+*Atomic Sanskrit* examines Sanātan's inside-out order through language: how people keep Sanskrit unchanged across thousands of years through a shared standard that no apex owns.
 
 ## 75 Words
 
-*Atomic Sanskrit* reconstructs Sanskrit as a living example of calibrant order and indicts the asuric pyramid that concealed its architecture through false categorization. Sanskrit’s sonomers occupy anatomical coordinates, its *dhātavaḥ* function as semantic atoms, and its two domains unite exact preservation with new composition. The Vedas serve as its invariant calibrant. Pāṇini inherited and documented the architecture. The book follows Sanskrit’s radiance beyond India and shows how PIE turned partial reflections into an imaginary ancestor.
+What does a language have to do with Sanātan's architecture? *Atomic Sanskrit* examines how Sanskrit has remained unchanged for thousands of years without central enforcement. The Vedas keep a shared standard available, and people learn to recognize mistakes and correct themselves. This inside-out design extends into civilizational life through stories and examples that guide conduct. The book challenges Western philologists who concealed that architecture by placing an imaginary ancestor, Proto-Indo-European, above the language they studied.
 
 ## 200 Words
 
-*Atomic Sanskrit* reconstructs Sanskrit as an engineered language whose architecture extends from sound into systems of exact transmission. Its sonomers occupy anatomical coordinates. Its *dhātavaḥ* function as semantic atoms. Its grammar remains stable while people create new expression.
+What does a language have to do with the architecture of Sanātan? *Atomic Sanskrit* examines an inside-out order in which people learn a shared standard and develop the ability to judge and correct their own actions. Sanskrit makes that design available for examination, from sound to word to sentence and through generations of teaching.
 
-The conflict in this book is between two architectures of order. Calibrant order keeps an invariant standard available to everyone, and no apex can own it. The asuric pyramid encloses knowledge and controls access. It concealed Sanskrit's architecture through false categorization: sonomers became letters, *dhātavaḥ* became roots, the two domains became historical periods, Pāṇini became a codifier, and Sanskrit became a daughter of Proto-Indo-European.
+How has Sanskrit remained unchanged for thousands of years without a central authority enforcing it? The Vedas keep its sounds and grammar available in examples. Distributed recitation lineages protect those examples while speakers use the same language to create new expressions. The greater engineering achievement is this system of protection against unintended change and deliberate attack.
 
-The *vaidika* domain preserves received content exactly. The *laukika* domain applies the same language to a changing world. The Vedas encode several architectures of *Sanātan*, including Sanskrit. They preserve its full range as an invariant calibrant through recitation and distributed lineages.
+Western philologists concealed the architecture through false categories. They made Sanskrit's two domains into historical stages, Pāṇini into the codifier who stopped drift, and Sanskrit into a daughter of an imaginary Proto-Indo-European. The book challenges that ancestry and follows Sanskrit's radiance beyond India.
 
-Pāṇini inherited and documented this architecture. The book follows Sanskrit's radiance beyond India. Influential carriers took Sanskritic words and methods into other civilizations. Those languages preserve partial reflections; Sanskrit retains the complete architecture. European philology turned the fragments into Proto-Indo-European and placed that imaginary construction above Sanskrit.
-
-As the first *Second Shanti* volume, the book follows this conflict from language into the order through which living beings share a world.
+The same inside-out design extends into civilizational life through shared stories that help people judge conduct without surrendering judgment to an apex. As the first *Second Shanti* volume, *Atomic Sanskrit* begins the reconstruction of order from first principles. Later volumes examine institutions and relationships among living beings.
diff --git a/writing/books/atomicSanskrit/outreach/contacts/people/manjeet_kripalani/as_overview.md b/writing/books/atomicSanskrit/outreach/contacts/people/manjeet_kripalani/as_overview.md
index 664e1bf0..70feee0d 100644
--- a/writing/books/atomicSanskrit/outreach/contacts/people/manjeet_kripalani/as_overview.md
+++ b/writing/books/atomicSanskrit/outreach/contacts/people/manjeet_kripalani/as_overview.md
@@ -16,7 +16,9 @@ I eventually realized that the answer was already present in the civilization I
 
 The *Second Shanti* series examines an architecture of order that works through calibration rather than command. A calibrant is an invariant reference that remains available for comparison. It does not issue orders. People approach it, recognize a deviation, and correct themselves.
 
-*Atomic Sanskrit* begins with language because Sanskrit and the Vedas preserve a complete example of that architecture which can still be heard and examined.
+What does a language have to do with the architecture of सनातन (*Sanātan*)? In Sanskrit, a learner checks a sound or a newly formed word against examples that other learners and teachers can also examine. The standard remains shared, while the ability to recognize and correct mistakes develops within each participant. This is inside-out order at the scale of language.
+
+How has Sanskrit remained unchanged for thousands of years without a central authority enforcing it? *Atomic Sanskrit* follows that achievement through the language's construction and the Vedic disciplines that keep it calibrated. The answer explains why this inquiry into civilizational order begins with Sanskrit.
 
 Sanskrit starts from the human body. Its sound architecture places consonants according to where the mouth makes contact and how the breath, voice, and nasal passage behave. It gives vowels precise durations. These sounds combine into stable units, then into more than two thousand semantic atoms called **धातवः (*dhātavaḥ*)**. Sanskrit extends those atoms through consistent procedures to form words, verbs, and sentences.
 
diff --git a/writing/books/atomicSanskrit/web/private/om_garland_newspaper.md b/writing/books/atomicSanskrit/web/private/om_garland_newspaper.md
index dadb7fa1..eebd3c34 100644
--- a/writing/books/atomicSanskrit/web/private/om_garland_newspaper.md
+++ b/writing/books/atomicSanskrit/web/private/om_garland_newspaper.md
@@ -72,7 +72,9 @@ The relation between Oṃ and the *varṇamālā* introduces a pattern that cont
 
 The same discipline repeats at different scales: precise constituent, compact form, stable identity, and wide expressive range. A fractal repeats a recognizable architecture as its scale changes. Sanskrit begins displaying that fractal in the body, before anyone writes a grammatical rule on a page.
 
-Oṃ carries the signature of a civilizational order because the same fractal extends from Sanskrit into Sanskriti. *Atomic Sanskrit* compares this order with its opposite. One creates order through a shared and distributed standard that no ruler can own; Sanskrit demonstrates this architecture at the scale of language. The other imposes order from an apex. The Vedas preserve the first architecture and carry it through exact sound. Across generations, the Hindu continuum has protected Sanskrit; Sanskrit, in turn, has preserved the architecture that protects the continuum.
+Oṃ carries the signature of a civilizational order because the same fractal extends from Sanskrit into Sanskriti. A learner can hear a shared example, recognize a departure in their own pronunciation, and correct it. In civilizational life, people can remember shared stories, examine their own choices, and change how they act. Both begin with understanding developed within the participant and a standard available beyond any one person's judgment. This is the inside-out architecture of सनातन (*Sanātan*) that *Atomic Sanskrit* examines.
+
+Sanskrit's invariance across thousands of years demonstrates how such a standard can endure without an apex owning it. The Vedas keep the language's calibrant available through exact sound and distributed transmission. The pyramid imposes the opposite relationship: an apex determines what others must accept. Across generations, the Hindu continuum has protected Sanskrit; Sanskrit, in turn, has preserved the architecture that protects the continuum.
 
 **Oṃ is the *akṣara* in which Sanskrit and Sanskriti are compressed into a radiant fractal that can be heard. The sign ॐ is the visible symbol of Sanātan's fractal architecture.**
 
diff --git a/writing/books/atomicSanskrit/web/private/sonomer_longform.md b/writing/books/atomicSanskrit/web/private/sonomer_longform.md
index 91480c76..a843a048 100644
--- a/writing/books/atomicSanskrit/web/private/sonomer_longform.md
+++ b/writing/books/atomicSanskrit/web/private/sonomer_longform.md
@@ -83,7 +83,7 @@ That recurrence is the beginning of Sanskrit's fractal architecture. The speakin
 
 The Vedas stand at the center of that architecture. Their exact transmission keeps Sanskrit's sounds present in the ear and mouth across generations, while the worldly domain uses the same reusable sound-particles to create new expression. The received mantras remain invariant, and the language remains capable of describing circumstances no earlier speaker encountered.
 
-*Atomic Sanskrit* follows this architecture from mouth to language and then asks what kind of civilizational order could preserve it without surrendering control to an apex. The inquiry begins with something millions of children already carry in memory.
+This is why *Atomic Sanskrit* begins its examination of सनातन (*Sanātan*) with language. Learners develop the ability to recognize and correct a sound against a standard that others also know. They need no central office to approve each correction. The book follows this inside-out design into civilizational life, where shared stories and examples help people judge their own conduct. Sanskrit's invariance allows us to study how a shared standard can remain available across thousands of years without an apex owning it.
 
 **क ख ग घ ङ** is not merely the beginning of an alphabet. It is the opening sequence of an engineered map of human speech.
 
diff --git a/writing/books/atomicSanskrit/web/private/sonomer_newspaper.md b/writing/books/atomicSanskrit/web/private/sonomer_newspaper.md
index 364be1cd..520403a4 100644
--- a/writing/books/atomicSanskrit/web/private/sonomer_newspaper.md
+++ b/writing/books/atomicSanskrit/web/private/sonomer_newspaper.md
@@ -69,7 +69,7 @@ Sanskrit carries this architecture beyond pronunciation. Sonomers combine into *
 
 This is the fractal architecture that *Atomic Sanskrit* follows from mouth to language. The Vedas preserve its sounds through exact recitation, while Sanskrit's worldly domain uses the same architecture to create new expression. One domain protects what must remain invariant. The other allows every generation to speak about its own world.
 
-The inquiry begins before Pāṇini and before writing, in a sequence millions of Indians already know by heart.
+What does this have to do with the architecture of सनातन (*Sanātan*)? A learner develops the ability to recognize a mistake and correct it against a standard that others also know. Order continues through the understanding of those who participate, without an apex owning the standard. *Atomic Sanskrit* follows this inside-out design from language into the way people judge and correct conduct. It begins before Pāṇini and before writing, in a sequence millions of Indians already know by heart.
 
 **The letter came later. The sonomer came first.**
 
diff --git a/writing/books/atomicSanskrit/web/public/engineered_not_codified_landing.md b/writing/books/atomicSanskrit/web/public/engineered_not_codified_landing.md
index 5daebf01..fe29e17d 100644
--- a/writing/books/atomicSanskrit/web/public/engineered_not_codified_landing.md
+++ b/writing/books/atomicSanskrit/web/public/engineered_not_codified_landing.md
@@ -6,17 +6,21 @@ slug: sanskrit-was-engineered
 
 # Sanskrit Was Engineered
 
-Most accounts of Sanskrit treat it as a language that grew. Roots branched into stems, stems branched into words, words branched into the daughter languages of an imagined ancestor. The botanical metaphor is so old that we read it without noticing.
+What does a language have to do with the architecture of सनातन (*Sanātan*)? *Atomic Sanskrit* examines an inside-out order through which people learn a shared standard and develop the ability to recognize mistakes and correct them. Sanskrit allows us to examine that order in the sounds people make, the words they form, and the teaching that keeps both available across generations.
+
+How has Sanskrit remained unchanged for thousands of years without a central authority enforcing it? The book examines the language's engineering together with the Vedas, which keep its calibrant distributed across society. Speakers continue to create new expressions without rewriting that shared standard.
+
+Western philologists instead teach Sanskrit as a language that grew. Roots branched into stems, stems branched into words, words branched into the daughter languages of an imagined ancestor. The botanical metaphor is so old that we read it without noticing.
 
 The metaphor is wrong.
 
 Sanskrit's architecture is not biological. It is engineered. The sounds are measured. The atoms are timed. The grammar operates on particles below the word, governed by rules that read like specifications rather than descriptions of organic drift. Pāṇini did not freeze a language. He decoded an architecture that had been operating for thousands of years before him.
 
-This is the central claim of *Atomic Sanskrit*. Across eighteen chapters, the book develops the engineering thesis from the level of the sound-particle — what I call the **sonomer** — through the level of the semantic atom — the ***dhātuḥ*** — into the bonding chemistry that combines those atoms into the words and sentences Sanskrit deploys. The argument is procedural, not just polemical. It rests on empirical evidence drawn from the 2,168-entry ***Dhātupāṭha*** and the Digital Corpus of Sanskrit's 15,900 parsed Sanskrit files: the inventory shows compression, distinguishability, semantic-acoustic alignment, and engineered range — exactly the four signatures an engineered system leaves, and exactly the four signatures the philological orthodoxy's botanical-evolutionary account cannot explain.
+The book develops the language's engineering from the level of the sound-particle — what I call the **sonomer** — through the level of the semantic atom — the ***dhātuḥ*** — into the bonding chemistry that combines those atoms into the words and sentences Sanskrit deploys. The argument is procedural, not just polemical. It rests on empirical evidence drawn from the 2,168-entry ***Dhātupāṭha*** and the Digital Corpus of Sanskrit's 15,900 parsed Sanskrit files: the inventory shows compression, distinguishability, semantic-acoustic alignment, and engineered range — exactly the four signatures an engineered system leaves, and exactly the four signatures the philological orthodoxy's botanical-evolutionary account cannot explain.
 
 The book also dismantles the framework that has obscured the architecture for two centuries: the Indo-European family tree, the Proto-Indo-European ancestor that no one ever spoke, the botanical mistranslation of ***dhātuḥ*** as *"root,"* and the institutional inheritance that taught India to read its own language through categories built somewhere else.
 
-*Atomic Sanskrit* is the first volume of a larger project called *Second Shanti* and continues the same civilizational-recovery project — now at the level of language.
+*Atomic Sanskrit* is the first volume of *Second Shanti*, a reconstruction of civilizational order from first principles. The same inside-out design extends beyond language when people use shared stories and examples to judge their conduct without surrendering that judgment to an apex. Later volumes examine how institutions and relationships among living beings can follow that design.
 
 The full book is forthcoming.
```

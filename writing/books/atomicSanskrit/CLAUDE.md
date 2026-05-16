# Atomic Sanskrit — Project Context

> This file is the always-on context for the *Atomic Sanskrit* book project. It works in three places: auto-loaded by Claude Code at session start; uploaded to a claude.ai project as project knowledge; or pasted into a fresh chat when neither is available. Read this before touching any file in the repo.

---

## What this project is

A trade-nonfiction polemic on the engineered architecture of *saṃskṛtam* — *perfectly synthesized* or *wholly created* — and the dismantling of the Western philological framework that has held the orthodoxy for thousands of years of *guru-shishya paramparā* worth of evidence. The book argues that Sanskrit was engineered, that the engineered Sanskrit thesis explains what migration-and-decay accounts cannot, and that the AIT framework, the PIE reconstruction project, and the family-tree taxonomy of Indian languages are all unvalidated inferences the book unbuilds.

Target: ~85,000 prose words + ~5,000 endnotes ≈ ~90,000 manuscript. 18 chapters across six parts plus Preface and Epilogue. Voice = Parag Tope: analytical, argumentative non-fiction, engineer's mind, Indic civilizational frame.

---

## File map

### Reference (read at session start)

| File | What it is |
|---|---|
| `CLAUDE.md` | This file. Bootstrap context. |
| `.claude/skills/atomic-sanskrit/SKILL.md` | Full voice/style manual. Loaded automatically in the IDE; uploadable to web. |
| `as_session*_handoff.md` | Session-by-session state. Most recent is canonical. |
| `as_todo.md` | Queued work, P0 / P1 / P2 / P3 priorities. |
| `as_toc.md` | Bare TOC, shareable. |
| `as_toc_annotated.md` | TOC with summaries + the canonical Claims list (currently *The Twenty Claims* — count grows as new claims are surfaced). |
| `as_toc_notes.md` | Working TOC document. |
| `as_endnotes.md` | Expanded endnote prose. Stub names key the entries. |
| `as_orl_voice_reference.md` | Distilled voice patterns from the *Operation Red Lotus* Appendix (Chapter Zero: The Rear-View Mirror, pp. 317–324). Reference document for polemic-chapter drafting. The source PDF (`orlAppendix.pdf`) does not need to be re-read once this distillation is in place. |
| `as_92_appendix.md` | Appendix — Chapter Zero: The Encyclopaedic Confirmation. Institutional polemic against the *Encyclopaedic Dictionary of Sanskrit on Historical Principles* (Deccan College, 1948–present). Structurally analogous to ORL's *Chapter Zero: The Rear-View Mirror*. ~3,650 words, seven sections, two tables. |
| `as_verification_todo.md` | The verification queue. Every unverified claim across drafted chapters, organized by chapter, with verification path. Inline `[VERIFY:]` markers in chapter drafts log here. |
| `as_verification_process.md` | The verification workflow. Tier system (A–F), working modes (background / targeted / deep-dive), tool usage, division of labor. **When the user asks "how does verification work?" or "what needs verification?" — start here.** |
| `as_book.yaml` | Canonical book metadata (title, subtitle, author, fonts, document structure). Single source of truth; never duplicate inline in scripts or templates. |
| `build_book.py` | Pipeline: assemble chapters → render PDF via pandoc + xelatex. Three phases (`stubs`, `assemble`, `pdf`, `all`). Three layouts (`letter`, `book-on-letter`, `trade`). |

### Drafts (open as needed)

`as_00_preface_draft.md`, `as_01_chapter_draft.md` ... `as_18_chapter_draft.md`. Chapter notes are `as_NN_chapter_notes.md`. End matter: `as_90_epilogue_draft.md`, `as_91_appendix.md` (*Baking the Mother Tongue*), `as_92_appendix.md` (*The Encyclopaedic Confirmation*).

**Filename convention.** Manuscript files carry a two-digit numeric prefix encoding reading order (`00`=preface; `01`–`18`=chapters; `90`=epilogue; `91`–`92`=appendix parts). Reference and working files (TOC, endnotes, sidebars, todo, verification, etc.) keep non-numeric prefixes — they sort after manuscript files in alphabetical directory listings, giving a clean two-zone organization.

### Standing artifacts

`as_sidebars.md`, `as_session_review.md`, `as_atomic_draft_disposition.md`, `as_diversions_ss.md`, `as_companion_paper_subcontinental_calibrant.md`, `as_03_chapter_notes.md`, `as_90_epilogue_notes.md`.

### Archives (historical reference only)

`as_ch07_draft_pre_split.md`, `as_ch07_notes_pre_split.md` — pre-Session-9 Ch7 before the descriptive/polemic split.

---

## Session bootstrap

When opening a new session:

1. Read this file.
2. Read the latest `as_session*_handoff.md` for current state.
3. Read `as_todo.md` for queued work and priorities.
4. Confirm what we're working on before editing anything.

When closing a session:

1. Update `as_todo.md` if priorities shifted.
2. Write a new `as_sessionN_handoff.md` capturing: accomplishments, files modified, locked decisions, outstanding work, next-session opener recommendation.
3. Commit.

---

## Non-negotiable rules

These apply to every draft, every edit, every session. The full versions live in the skill; what follows is the always-on safety net.

### Chronology — strategic refusal for Indic, dates fine for non-Indic

Never use chronological dating for anything Indian: no centuries, no "two thousand years ago," no "by the time of [Pāṇini / the Vedas]." Use *thousands of years*, *across the ages*, *long before [external reference point]*, *guru-shishya transmission across many generations*. Internal-frame ordering is fine: *before Pāṇini*, *after Patañjali*, *the Prātiśākhya tradition that preceded him*.

Dating Greek, Roman, Arabic, Tibetan, Chinese, European, and other non-Indic figures, texts, and events is fine and often required. Schleicher's family-tree theory in the 1860s; *Proto-Indo-European* stabilizing as a term by 1905; the *PIE* abbreviation entering routine usage mid-twentieth-century. These are external, datable, and the dates are part of the argument.

The asymmetry is intentional. India is the *Forever Nation* — integral, continuous. External traditions are discrete, locatable enterprises with histories.

**Beyond the methodological asymmetry, the position is strategic.** The chronology the church of progress has established for Indic figures and texts may or may not be accurate — partly factual, partly agenda-driven, and currently inseparable from the asuric pyramid that built it (Ch 3 §3.6). The book's position on the chronology fight is *refusal*, not counter-construction. India is not yet equipped to fight the chronology battle — not because the technology is missing, but because the *mindset* of the contemporary Indian academic apparatus is not aligned with a dharmic world order. Eighty years after independence, the same institutions that operated for the colonial framework still operate it — Deccan College Pune the named exemplar (Appendix Part 2). Until every Indian academic operates aligned with the vision of *Sanātan*, the book refuses to accept the asuric chronology *and* refuses to provide an alternative. The refusal is the position. The next generation — those who will fight the chronology battle from inside the dharmic civilizational frame — will provide what the present generation cannot.

The Epilogue lands this strategic position; Appendix Part 2 develops the institutional case for why India is not yet equipped.

### "Indo-Aryan" — quoted always, adopted never

The compound *Indo-Aryan* never appears unquoted in the book's own prose. The second element rides on the racial-genealogical reading of *ārya* the book dismantles. Substitutes: *Indic* (default), *Sanskritic* (when register-derived), *pre-Vedic-Sanskritic* (Mitanni-style cases), *subcontinental Prākrit-Apabhraṃśa lineage* (long form). *"Indo-Aryan"* in scare quotes is acceptable when naming the orthodoxy's classification system for reader convenience. Geographic compounds (*Indo-Iranian*, *Indo-European*, *Austro-asiatic*) are fine unquoted.

### Indian-language classification — geography + named languages

Reject the establishment family-tree taxonomy (*Indo-Aryan / Dravidian / Tibeto-Burman*) as unvalidated inferences. Default: geography + named languages — northern, southern, eastern, western, central, with constituent languages named explicitly (Marathi, Tamil, Bengali, Punjabi, Korku, Mundari, Santali, Ho, Sora, Gondi). *Munda* accepted as observed-continuum sub-group; *Austro-asiatic* accepted as geographic compound. Family-tree labels in scare quotes only when attributing to the orthodoxy.

### "Tribal" — rejected in the Indian context

Never use *tribal* for the forest-dwelling communities of the subcontinent — colonial-anthropological baggage. Substitutes: *forest dwellers* (default), *forest belt* / *central forest belt* (for *tribal belt*), *vanavāsī* वनवासी (Sanskrit anchor), or name the communities and languages directly (Korku, Mundari, Santal, Ho, Sora, Gond). *"Tribal"* in scare quotes when attributing to the orthodoxy. The rejected-list pattern: *"not race, lineage, or skull shape"*, not *"not race, tribe, or skull shape."*

### *"Enlightenment"* — scare-quoted always

*Enlightenment* is a self-flattering self-naming of one specific period in European intellectual history. The term embeds the claim that this period achieved a cognitive elevation other civilizations and periods did not — a claim the engineered Sanskrit thesis directly contests. Scare-quote on every appearance: *"Enlightenment"*, *post-"Enlightenment"*, *"Enlightenment"-era*. Already deployed this way in Ch2 §2.1; Ch3 brought into consistency. Italic + double-quote scare-quote form, matching the book's existing treatment for *"Indo-Aryan"*, *"tribal"*, and similar contested self-namings.

### "Vernacular" — rejected for Indic languages

Never use *vernacular* for Marathi, Hindi, Bengali, Tamil, or any Indic language. From Latin *verna* (a slave born in the master's household), it historically subordinated "low" speech to learned/literary language — the same colonial-orientalist logic that produced *tribal* for forest-dwelling communities. Substitutes: *languages* (default — context names which), *calibrant-anchored languages* (within the engineering framework, Ch5 §5.6 forward), *Indic languages* (default civilizational frame), *Sanskritic languages* (when register-derivation is the point), *natural languages* (when the natural-vs-engineered contrast is the point), or name the languages directly. *"Vernacular"* in scare quotes when attributing to the orthodoxy. Full rationale in skill §7.3.

### *Mode*, not *register*, for Sanskrit-variety distinctions

Use *mode* for the Vedic vs. Pāṇinian-codified Sanskrit-variety distinction. **Vedic mode** = recitational-preservational (preserves ळ, accent, meter). **Generative-analytical mode** = Pāṇinian *bhāṣāyām*. Synchronic-parallel, not evolutionary-sequential. Three-term system: *mode* (Sanskrit-variety); *style* (*shruti* / *smriti* text-class); *register* (polemic / engineering discourse-style in the book's own voice and across the discipline's voices).

### Plain English primary; Sanskrit anchor when useful

No academic Greek/Latin abstract adjectives in the book's own prose — no *liturgical*, *pedagogical*, *exegetical*, *homiletic*, *hermeneutic*, *soteriological*, *eschatological*. Plain English naming the activity: *teaching*, *training*, *worship*, *recitation*, *commentary*, *interpretation*. Pair with Sanskrit anchor on first use where useful for non-Indian readers: *upadesha* उपदेश, *bhāṣya* भाष्य, *paṭha* पाठ, *japa* जप, *pravachana* प्रवचन, *śikṣā* शिक्षा. Example: *liturgical mode* → *recitational mode* (or *paṭha-mode*). The general rule extends: *list* not *catalog*, *start* not *commence*, *use* not *utilize*, *show* not *demonstrate*, *make up* not *constitute*, *help* not *facilitate*.

### Establishment-naming — concrete, no weasel phrases

Never weasel-phrase the establishment. Reject *"the standard discipline reading,"* *"the conventional academic view,"* *"the consensus interpretation,"* *"received scholarship,"* *"the mainstream view,"* *"the accepted account."* Name concretely: *Western philology*, *the Western philological orthodoxy* (polemic-register stack), *AIT-aligned Indology*, *the Müllerian framework*, *the philological orthodoxy*, *nineteenth-century Indo-Europeanism*. Name the figure where the source is specific, especially as strawman for the system: *Max Müller's account*, *Whitney's grammar*, *Brugmann's reconstruction*. Or scare-quote the self-claim: *the "standard" reading*, *the "established" view*. The book attacks named frameworks.

**Polemic-register stack for the philological framework.** When the polemical register is wanted (prosecutorial chapters Ch16, Ch17, Ch18, the Appendix), prefer the full stack ***the Western philological orthodoxy*** at first deployment in a section — three notes loaded: *Western* (geographic/civilizational), *philological* (disciplinary), *orthodoxy* (the doctrinal bite). Shorter forms (*the philological orthodoxy*, *this orthodoxy*) work on subsequent in-section deployments once the full form has been established. *Western philology* alone is descriptive — fine for neutral context, too thin for prosecutorial register.

### Voice — authoritative across the book

The book uses a single voice register universally: **expository / authoritative**. Direct subject-of-the-sentence is the *content* (Sanskrit, the architecture, the *varṇamālā*, the orthodoxy) rather than the book or its act of reading. Impersonal third-person; simple-present indicative; chapters *describe*, *establish*, *lay out*, *name*, *show*, *dismantle*, *prosecute* — they do not *walk*, *read*, *recover*, or *reclaim*. The book is the venue in which the description appears; the content is the agent.

**Reject the recoverist register everywhere.** The earlier convention had polemic chapters deploy a *hermeneutic / recoverist* voice — first-person plural ("we have walked"), present perfect continuous ("has been reading"), self-referential apparatus ("this book has been recovering"), book-as-humble-reader hand. That convention is retired. The polemic does not need the recoverist scaffolding; the polemic works through *named-agent active voice* (the orthodoxy does X; Sanskrit's apparatus does Y; the architecture stands) and through the named-cluster vocabulary (asuric / asuratva / pyramid / lokakṣema / Sanātan). The recoverist hand was load-bearing for an earlier draft frame; the named-categorical naming work now does the same job without the hedging that hermeneutic register accumulates.

**The conversion rule (apply universally):**

| Recoverist (retired) | Authoritative (canonical) |
|---|---|
| *"the architecture this book has been reading was built to last"* | *"Sanskrit's architecture was built to last"* |
| *"across the preceding chapters we have walked the varṇamālā..."* | *"the preceding chapters establish the varṇamālā..."* |
| *"the Sanskrit name for the system is what this chapter recovers"* | *"the Sanskrit name for the system is..."* (direct introduction) |
| *"the empirical fact this book is recovering"* | *"the empirical fact at the center of this book"* |
| *"this book has been describing"* | *"the preceding chapters describe"* / *"the book describes"* |
| *"we have named"* | *"Chapter N names"* / *"§N.M names"* |

**Polemic register is preserved through *active verbs with named agents*, not through recoverist hand.** Where the polemic critiques the orthodoxy, the orthodoxy is the named subject of the active verb: *the orthodoxy claims*, *the orthodoxy elevates*, *the orthodoxy treats*, *the orthodoxy refuses*. Where the polemic affirms the architecture, the architecture or its features are the named subject: *Sanskrit's apparatus generates*, *the varṇamālā maps*, *Sanātan operates*. Passive constructions that hide the orthodoxy as agent — *"is treated as"*, *"is credited"*, *"is foreclosed"* — are the failure mode the named-agent rule exists to catch.

**Diagnostic.** If the draft uses *this book*, *we*, *the book has been*, *recovering*, *walking*, *reading*, or other first-person-plural / book-as-agent constructions, the prose is in recoverist register and needs conversion. The only exceptions are the *book's own self-description* in the Preface and end-matter (e.g., naming the book itself as the venue), and the verb *names* / *introduces* / *develops* when used to point the reader at where the book treats a specific concept (e.g., "Chapter 8 §8.6 names heroic erasure").

### *Heroic erasure* — naming the orthodoxy's move against the engineering thesis

***Heroic erasure*** is the book's standing term for the move by which the *Western philological orthodoxy* praises a named tradition-internal figure or tradition for some downstream contribution — codification, documentation, transmission, adaptation — while structurally denying the **engineering thesis** the praise is positioned to obscure. The engineering thesis is the book's central claim, named in the subtitle (*The Architecture of Sanātan*): Sanskrit was engineered, the *varṇamālā* / *dhātupāṭha* / calibration-matrix / multi-axis architecture is engineered, and engineering implies *engineers* — the unknown architects of the system the named figures operate within, document, transmit, or render. The praise is not generosity; it is the mechanism of the erasure. Naming a brilliant Indian *operator* is how the orthodoxy denies that there were Indian *architects*.

The move has multiple deployments. **Pāṇini-as-brilliant-grammarian** (Ch8 §8.6, Ch15 §15.5) — celebration as the founder of generative linguistics, erasure of the engineered architecture Pāṇini was operating within and codifying rather than inventing. **The Prātiśākhya tradition as careful phoneticians** — praise for documentation, erasure of the engineered phonology being documented. **The Śikṣā tradition as devoted teachers** — praise for transmission, erasure of the engineered specification being transmitted. **The brilliant adapter of Aramaic** (Ch14 §14.3) — praise for the script's surface organization, erasure of the *varṇamālā* the script renders. The shape is invariant: praise the surface or the documentation, deny that the depth was engineered, deny that engineers existed.

Established as a standing term in Ch8 §8.6 — *"The orthodoxy's celebration of Pāṇini is the same operation as its* centuries of analysis *fabrication, run through a different mechanism — both substitute a manufactured story for what the texts actually present."* Generalized in Ch14 §14.3 as the orthodoxy's standing move against the engineering thesis at every level.

Structurally adjacent to the *outward-absorption* move Ch3 §3.4 names (the church of progress absorbing contemporary tradition-internal scholars by elevating them into the priesthood). Heroic erasure is the same mechanism applied to a historical figure rather than a contemporary one. Deploy where the polemic critiques a founder-myth narrative *or* any praise-of-the-operator framing the orthodoxy uses to avoid acknowledging the architects.

The standing test: any orthodoxy celebration of an Indic figure that stops short of acknowledging the engineered architecture as engineered is heroic erasure, regardless of how generous the celebration is. The deeper layer that gets erased is always the same — *engineering by engineers*. The named figure being praised is always downstream of that.

### Internal-frame anchors over external classifications

*Post-Pāṇinian Sanskrit* over *Post-Pāṇinian Classical Sanskrit*. *Vedic mode* over *Old Indic*. *Prakritic continuum* over *Middle Indo-Aryan*. *Munda lineage* over *Austroasiatic family*. *What Pāṇini describes as bhāṣāyām* over *the bhāṣāyām corpus*. *Mūrdhanya* over *retroflex* when the technical argument runs from inside the Sanskrit frame. The book operates in the internal frame primarily; the external term is the translation, not the anchor.

### Indic-tradition figures are not finger-pointed

*Sabhyata* says preserve the lesson, abstract the name. Antagonists from outside the tradition can be assailed; betrayers within the tradition are unnamed by design. The lesson survives; the name does not.

### Vocabulary register — name the side with the noun

The two sides of the book's central opposition (Sanskrit's engineering vs. the Western philological orthodoxy's apparatus) carry their structural opposition into the noun-choice itself. Replace generic *apparatus*-cluster vocabulary with side-specific words wherever the polemic register can carry it.

**For the European / orthodox side (the bake — organic, decays, dies):**

- ***ecosystem*** — biological-metaphor (connects directly to the cooking/baking-organic-decays cluster); the *philological ecosystem*, the *PIE-reconstruction ecosystem*. Default register-marker for the orthodoxy side.
- ***nexus*** — connecting-point with slight conspiracy connotation; the *philological nexus connecting Pune, Calcutta, Oxford, and Göttingen*; the *colonial-knowledge nexus*. Use where the *coordination* aspect is the point.
- ***cartel*** — the heaviest hammer (coordinated commercial collusion). **Ration deliberately** — reserve for one or two heavy hits per prosecutorial chapter (Ch3 §3.5, Ch17 §17.4, Appendix §3). Overuse cheapens it.
- ***machinery*** — industrial grinding, factory operation; the *machinery of peer review*, the *philological machinery*.
- ***regime*** — authoritarian register without going as heavy as *cartel*; the *reconstruction regime*, the *philological regime*.
- ***industry***, ***enterprise***, ***operation*** — neutral-orthodox-leaning; *enterprise* fits the colonial-Sanskrit enterprise where the colonial-administrative aspect is part of the point.

**For the Indian / Sanskrit side (the engineering — manufactured, inorganic, *sanātan*):**

- ***architecture*** — canonical and load-bearing; *the architecture of Sanātan*, *the architecture is on the ground*. Default register-marker for the Sanskrit side.
- ***framework*** — engineered, built, structured; *the vyākaraṇa framework*, *the Pāṇinian framework*.
- ***infrastructure*** — engineered, foundational; *the Vedāṅga infrastructure*, *the calibration infrastructure*.
- ***constellation*** — pattern of fixed/eternal points (connects to *sanātan*); *the constellation of dhātus*, *the engineered constellation*.
- ***grid*** — already in use for the *periodic table of gaṇāḥ*; engineering register.
- ***fabric*** — woven, integrated, holistic; *the fabric of the paramparā*.
- ***engine*** — generative, productive; *Pāṇini's generative engine*, *the affixation engine*.
- ***system*** — slightly engineering-leaning; safe Sanskrit-side use.

**Polyvalent (either side, register-neutral):**

- ***apparatus*** — still useful when neither register-pull is wanted; **ration** rather than eliminate.
- ***paradigm***, ***construct***, ***project*** — neutral.
- ***schematic*** — leans slightly Sanskrit-side (engineering-drawing register).

**Deployment pattern.** Where a sentence is doing prosecutorial work on the orthodoxy, prefer a *cartel* / *ecosystem* / *machinery* / *regime* word. Where a sentence is naming Sanskrit's design, prefer an *architecture* / *constellation* / *framework* / *engine* word. The noun choice carries the structural opposition without requiring the polemic move to be made explicitly in the surrounding prose. Don't sweep-and-replace blindly — *apparatus* remains the right choice in some contexts; the convention is to deploy the side-specific word *where the polemic register can carry it*.

### Cooking and baking for the fraud — *manufactured* reserved for Sanskrit's engineering

The cooking / baking vocabulary cluster (*bake*, *the bake*, *the bakers*, *the recipe*, *cooking up*, *the slip*) names the PIE-manufacture operation in fraud-register headings and prose. ***Manufacture*** / ***manufactured*** / ***engineered*** is reserved for Sanskrit's own architecture and is *not* deployed for the orthodoxy's reconstruction work.

The rationale carries the polemic. **Food is organic. Food decays. Food dies.** Calling PIE *baked* attaches it to the organic, decay-and-die end of the metaphor — PIE will rot, the way every reconstructed apparatus eventually rots. **Sanskrit is *manufactured* — engineered, inorganic, *sanātan*.** It will not decay. Using *manufacture* for the fraud would smear the word; reserving it for Sanskrit's engineering preserves the opposition the book is making: organic-decaying vs. manufactured-eternal, baked vs. engineered, fraud vs. *sanātan*.

**Deployment pattern.** In fraud-register headings, prefer the cooking / baking cluster: *Baking the Mother Tongue*, *The Recipe Slips*, *the bakers*. In Sanskrit-register prose, use *engineered* / *manufactured* / *architecture*. Body prose can mix — naming *bake* / *recipe* / *slip* at the moment the fraud is named, and *engineered* / *manufactured* at the moment the Sanskrit calibrant is named. The two registers are not interchangeable; the assignment to the two sides is load-bearing.

**Established deployments.** Ch1 §1.1 (*The Baker's Botanical Model*; Schleicher's "baking skills"); Ch17 §17.1 (*Did August Schleicher bake the first PIE?*), §17.8 (*The Recipe Slips*; *the bakers took the dhātu...the starred ancestors were the bake*); Appendix — Chapter Zero (Part 1): *Baking the Mother Tongue*. Convention applies forward across the book.

---

## Canonical glosses (deploy as-is)

These appear identically across the manuscript. Don't paraphrase.

**Saṃskṛtam canonical gloss (first use, deployed in Preface and Ch1, may be compressed but not broken in later chapters):**

> *saṃskṛtam* — *perfectly synthesized* or *wholly created*.

The dual translation is load-bearing. The endnote `samskrtam-morphology` (in `as_endnotes.md`) captures the rationale.

**Architects of Sanskrit framing:** unknown engineers; documenters came later; documenters inherited the architecture and did not invent it. Future chapters must not credit the *grammarians* with what the *architects* did.

***Asuratva* (असुरत्व) — the asuric operating mode.** The quality of being an asura, the operating-mode of an actor or institution that consolidates power through hierarchy, deceives to maintain authority, and operates by withholding light. Established in Ch 3 §3.6, parallel to ***āryatva*** (Ch 9 — the engineered phonetic-pedagogical achievement of mastery in service of *lokakṣema*). The morphological grounding: *sur* (*to shine*) → *suraḥ* (*the shining one*) → *asuraḥ* (privative *a-* + *suraḥ* = *not-light*); the operating-mode noun is *asuratva*. *Asuratva* has a characteristic geometry — the pyramid — and a characteristic substrate — *tamas* (the *guṇa* of inertia / darkness / obscurity). Ch 3 §3.6 names the *Western philological orthodoxy* and its institutional carrier (the *church of progress*) as a contemporary asuric formation operating in *asuratva*. Deploy where naming an actor / institution / framework as asuric in the Indic-categorical register is what's wanted; reference Ch 3 §3.6 rather than redeveloping the diagnostic. Schleicher is the canonical named individual operator (Ch 3 §3.6 close, Ch 18 §18.1, Appendix Part 4 §7).

**The fourth Abrahamic religion cluster (deploy where the structural level is the actual referent):**

- *progressive orthodoxy* (doctrinal — linear-progress axis)
- *foundational orthodoxy* (doctrinal — corridor-of-origin axis)
- *church of progress* (institutional)
- *priests of progress* (sanctifying class)
- *missionaries of progress* (extending class)
- *jihadis of progress* (defending class)

Calibration (revised):

- *Progressive orthodoxy* and *foundational orthodoxy* are the two canonical doctrinal strata (Ch 3 §3.2 introduces both as sibling strata). *Progressive orthodoxy* defends the linear-progress teleology — recent is more advanced, ancient is less. *Foundational orthodoxy* defends the corridor-of-origin claim — engineered writing (and by extension other foundational achievements) began in the Sumerian-Egyptian-Phoenician-Greek-Latin corridor. The two strata operate in coordination, defending the same asuric pyramid (§3.6) along distinct axes. Deploy *progressive orthodoxy* where the linear-time assumption is the polemic target (main chapters, especially Ch 2, Ch 14–15, Ch 17–18). Deploy *foundational orthodoxy* where the corridor-of-origin assumption is the polemic target (Appendix Part 3 — the *Brāhmī-from-Aramaic* claim and audiography prosecution; future chapters that prosecute *invention-of-writing-as-Western-achievement* claims).
- *Church of progress* (institutional) is the canonical name for the institutional level — the carrier-formation that holds both doctrinal strata across generations. Deploy wherever the institutional level IS the actual referent — not as polemic flourish, but because this is the book's named structural category. Generic uses of *Western establishment* / *the establishment* / *institutional Indology* should sharpen to the cluster term whenever the structural level is what is being named.
- *Priests of progress* / *missionaries of progress* / *jihadis of progress* are reserved for the **specific function-class action** being named (sanctifying / extending / defending). Don't deploy these for generic establishment-naming; deploy when the sub-class action is the referent.
- *Fourth Abrahamic religion* itself remains sparing — **3 deployments across the book**.
- Per-chapter pattern lands naturally: 0 in chapters that don't engage the establishment generically; 1–2 in chapters that do; 3+ in heavily prosecutorial chapters (Ch2, Ch3, Ch17, the Appendix). Total across the book likely 20–35.
- Italicize on first use in a chapter, then plain. No glossary entry, no scare quotes — self-glossing English compounds.
- Specific establishment-naming vocabulary (*Western philology*, *AIT framework*, *Müllerian Indology*, named figures) stays as is — those name specific fields / frameworks / figures, not the structural class.

---

## Voice in one paragraph

Argue, don't survey. Commit to positions. Combative on substance, civil on persons. Dichotomy → reframe is the signature move — set up the Western binary, show the binary is the wrong frame, offer the orthogonal third frame rooted in Indic thought. Layered multi-clause sentences build the case; short hammers close. Every section closes with an unqualified verdict. Open chapters with wordplay (running it as structural spine across the chapter) or scene (then pivot). Engineering vocabulary is natural — *orthogonal*, *integration vs. discreteness*, *dispersive*, *rotational symmetry*, *triad*, *two-pronged attack*. Trust the metaphor when it lands; send the technical proof to the chapter whose territory it belongs to or to an endnote. Plain-English hammer-closes even after technical interiors. Familiar examples from the reader's daily speech anchor the abstract argument.

The full voice manual is `.claude/skills/atomic-sanskrit/SKILL.md`. Load it when working on drafts.

---

## Endnote convention

Drafting: `[NOTE: stub-name]` inline at the point the note attaches. Expanded prose lives in `as_endnotes.md`, keyed by stub name, with deployment locations listed under each entry. Numerical conversion happens at chapter-lock time, not during drafting.

---

## Figure convention

Placeholder format inline at draft time:

```
[FIGURE X.Y: *Title.* — what it shows / what it compresses]
```

Production happens later in one unified pass. Two-to-three figures per chapter is typical; visual-heavy chapters (Part III sound-field, Part IV atomic architecture) may warrant more. No sub-§-level headings — five-or-so §-level sections per chapter at major argumentative pivots, with bold-leading phrases or contrastive lines doing the work that sub-headings would impose.

---

## TOC three-file family

Keep these in lockstep:

- `as_toc.md` — bare titles only.
- `as_toc_annotated.md` — TOC with 1–2 sentence summaries + the canonical Claims list (currently *The Twenty Claims*; titled "The Eighteen Provocations" in earlier sessions, renamed to "Claims" once the cold-reader rewrite landed and the count grew).
- `as_toc_notes.md` — working document.

When a chapter or sub-section structure changes, update all three. The Claims (currently twenty) are the canonical statement of the book's argument — when a Claim's chapter reference or content changes, `as_toc_annotated.md` (canonical, shareable) is the source of truth, and `as_toc_notes.md` (working) should be synced to match. Earlier sessions called these "Provocations"; the term was retired for "Claims" once the cold-reader rewrite shifted the register from polemic to descriptive.

---

*End of bootstrap. For full voice/style rules, load the atomic-sanskrit skill or read `.claude/skills/atomic-sanskrit/SKILL.md` directly.*

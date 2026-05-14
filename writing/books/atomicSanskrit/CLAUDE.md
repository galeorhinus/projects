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
| `as_toc_annotated.md` | TOC with summaries + 14 Provocations. |
| `as_toc_notes.md` | Working TOC document. |
| `as_endnotes.md` | Expanded endnote prose. Stub names key the entries. |
| `as_orl_voice_reference.md` | Distilled voice patterns from the *Operation Red Lotus* Appendix (Chapter Zero: The Rear-View Mirror, pp. 317–324). Reference document for polemic-chapter drafting. The source PDF (`orlAppendix.pdf`) does not need to be re-read once this distillation is in place. |
| `as_deccan_college_polemic.md` | Appendix — Chapter Zero: The Encyclopaedic Confirmation. Institutional polemic against the *Encyclopaedic Dictionary of Sanskrit on Historical Principles* (Deccan College, 1948–present). Structurally analogous to ORL's *Chapter Zero: The Rear-View Mirror*. ~3,650 words, seven sections, two tables. |
| `as_verification_todo.md` | The verification queue. Every unverified claim across drafted chapters, organized by chapter, with verification path. Inline `[VERIFY:]` markers in chapter drafts log here. |
| `as_verification_process.md` | The verification workflow. Tier system (A–F), working modes (background / targeted / deep-dive), tool usage, division of labor. **When the user asks "how does verification work?" or "what needs verification?" — start here.** |
| `as_book.yaml` | Canonical book metadata (title, subtitle, author, fonts, document structure). Single source of truth; never duplicate inline in scripts or templates. |
| `build_book.py` | Pipeline: assemble chapters → render PDF via pandoc + xelatex. Three phases (`stubs`, `assemble`, `pdf`, `all`). Three layouts (`letter`, `book-on-letter`, `trade`). |

### Drafts (open as needed)

`as_preface_draft.md`, `as_ch01_draft.md` ... `as_ch18_draft.md`. Chapter notes are `as_chNN_notes.md`.

### Standing artifacts

`as_sidebars.md`, `as_session_review.md`, `as_atomic_draft_disposition.md`, `as_diversions_ss.md`, `as_companion_paper_subcontinental_calibrant.md`, `as_ch_fourth_abrahamic_notes.md`, `as_epilogue_notes.md`.

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

### Chronology — qualitative for Indic, dates fine for non-Indic

Never use chronological dating for anything Indian: no centuries, no "two thousand years ago," no "by the time of [Pāṇini / the Vedas]." Use *thousands of years*, *across the ages*, *long before [external reference point]*, *guru-shishya transmission across many generations*. Internal-frame ordering is fine: *before Pāṇini*, *after Patañjali*, *the Prātiśākhya tradition that preceded him*.

Dating Greek, Roman, Arabic, Tibetan, Chinese, European, and other non-Indic figures, texts, and events is fine and often required. Schleicher's family-tree theory in the 1860s; *Proto-Indo-European* stabilizing as a term by 1905; the *PIE* abbreviation entering routine usage mid-twentieth-century. These are external, datable, and the dates are part of the argument.

The asymmetry is intentional. India is the *Forever Nation* — integral, continuous. External traditions are discrete, locatable enterprises with histories.

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

### Internal-frame anchors over external classifications

*Post-Pāṇinian Sanskrit* over *Post-Pāṇinian Classical Sanskrit*. *Vedic mode* over *Old Indic*. *Prakritic continuum* over *Middle Indo-Aryan*. *Munda lineage* over *Austroasiatic family*. *What Pāṇini describes as bhāṣāyām* over *the bhāṣāyām corpus*. *Mūrdhanya* over *retroflex* when the technical argument runs from inside the Sanskrit frame. The book operates in the internal frame primarily; the external term is the translation, not the anchor.

### Indic-tradition figures are not finger-pointed

*Sabhyata* says preserve the lesson, abstract the name. Antagonists from outside the tradition can be assailed; betrayers within the tradition are unnamed by design. The lesson survives; the name does not.

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

**The fourth Abrahamic religion cluster (deploy where the structural level is the actual referent):**

- *progressive orthodoxy* (doctrinal)
- *church of progress* (institutional)
- *priests of progress* (sanctifying class)
- *missionaries of progress* (extending class)
- *jihadis of progress* (defending class)

Calibration (revised):

- *Progressive orthodoxy* (doctrinal) and *church of progress* (institutional) are the canonical names for those two structural levels. Deploy wherever the doctrinal or institutional level IS the actual referent — not as polemic flourish, but because these are the book's named structural categories. Generic uses of *orthodoxy* (doctrinal) and *Western establishment* / *the establishment* / *institutional Indology* (institutional) should sharpen to the cluster term whenever the structural level is what is being named.
- *Priests of progress* / *missionaries of progress* / *jihadis of progress* are reserved for the **specific function-class action** being named (sanctifying / extending / defending). Don't deploy these for generic establishment-naming; deploy when the sub-class action is the referent.
- *Fourth Abrahamic religion* itself remains sparing — **3 deployments across the book**.
- Per-chapter pattern lands naturally: 0 in chapters that don't engage the establishment generically; 1–2 in chapters that do; 3+ in heavily prosecutorial chapters (Ch2, Ch3, Ch17, the Appendix). Total across the book likely 20–35.
- Italicize on first use, then plain. No glossary entry, no scare quotes — self-glossing English compounds.
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
- `as_toc_annotated.md` — TOC with 1–2 sentence summaries + the 14 Provocations.
- `as_toc_notes.md` — working document.

When a chapter or sub-section structure changes, update all three. The 14 Provocations are the canonical statement of the book's argument — when a Provocation's chapter reference changes, `as_toc_notes.md` (source) and `as_toc_annotated.md` (shareable) both update.

---

*End of bootstrap. For full voice/style rules, load the atomic-sanskrit skill or read `.claude/skills/atomic-sanskrit/SKILL.md` directly.*

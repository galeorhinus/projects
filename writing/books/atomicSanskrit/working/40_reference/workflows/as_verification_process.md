# Atomic Sanskrit — Verification Process

> **Purpose.** Process companion to [as_verification_todo.md](../../10_active/as_verification_todo.md). This file is the *how*; the todo file is the *what*. Together they constitute the verification apparatus.
>
> **When the user asks "what needs verification?" or "how do I work the verification queue?"** — this file is the answer.
>
> **When the user asks "what's still pending?"** — the todo file is the answer.

---

## The two paired files

| File | Purpose | Update rhythm |
|------|---------|---------------|
| [as_verification_todo.md](../../10_active/as_verification_todo.md) | The queue — every unverified claim, organized by chapter, with verification path | Add items when drafting new claims (via `[VERIFY:]` markers); check items off as discharged |
| [as_verification_process.md](as_verification_process.md) *(this file)* | The workflow — tier system, working modes, tool usage | Update only when the process itself changes |

---

## Tier system

Verification items are not uniform. They span from "look up a date in 30 seconds" to "verify a Sanskrit passage against a primary edition over an afternoon." Tier each item before working it.

| Tier | Item type | Effort/item | Primary tools | Claude-autonomous? |
|------|-----------|-------------|---------------|---------------------|
| **A** | Non-Indic dates (Schleicher, Bopp, IPA, Goddard, Pinker, Whitney, Müller, etc.) | 1–2 min | Web search, Wikipedia bio dates | Yes |
| **B** | Bibliographic facts — titles, publishers, editions (Thomason-Kaufman, Ross, Becker, Voegelin, Fukuyama, Rostow, Gray) | 2–5 min | WorldCat, Google Books, publisher pages | Yes |
| **C** | Etymology chains — OED entries, IE cognates (*hlāfweard*, *Sindhu*/*Hinduš*/*Indós*, *moron* treadmill) | 5–10 min | OED Online, etymonline.com, Mayrhofer KEWA/EWAia, Kent's *Old Persian* | Partial — OED-tier yes; IE-specialist references need library |
| **D** | Sanskrit/Pali primary passages — Mahābhāṣya, Aṣṭādhyāyī sūtras, Rigveda verses, Assalāyana Sutta, Prātiśākhya texts | 15–60 min | GRETIL (gretil.sub.uni-goettingen.de), SARIT, Tipitaka.org, accesstoinsight.org, sanskritdocuments.org, critical editions | Partial — GRETIL/SARIT/Tipitaka are public; critical-edition consultation may need physical access |
| **E** | Numerical / institutional facts — Kailasa tonnage, Deccan College stats, Mitanni evidence | Variable | Deccan College official records (koshashri-dc.ac.in), ASI publications, Bogazköy archive scholarship | Partial — public data yes; unpublished records no |
| **F** | Load-bearing P0 — claims whose failure would damage the book's argument | Highest care | Multi-source cross-check + author's judgment on hedging | Claude does legwork; user has final approval |

**Current P0 items** (Tier F, deserve dedicated sessions): **ALL CLEARED 2026-05-16.**

1. ~~Assalāyana Sutta (Majjhima Nikāya 93)~~ — **Cleared 2026-05-16 (Tier F deep-dive).** Endnote `assalayana-sutta` refined with PTS *M* ii 147 ff. citation, Bodhi page-range refinement (763 ff., end-page provisional), Pali compound *Yonakambojesu* added, *ariya/dāsa*-preservation flagged as chapter's rendering, mule-analogy / Wave 8 secondary anchor added.
2. ~~Paspaśāhnika passage form and unity~~ — **Cleared 2026-05-16 (Tier F triple deep-dive).** Endnote `paspashahnika-apabhramsa-passage` corrected: Kielhorn's standard text uses *'paśabdāḥ* in clauses 1–2 (not *'pabhraṃśāḥ*); Patañjali switches to *'pabhraṃśāḥ* only at the *tadyathā* example. Ch 5 §5.2 ¶1 quoted Sanskrit also corrected. Term-switch note added (*apaśabda*/*apabhraṃśa* near-synonymy is itself evidence of textual unity).
3. ~~Mitanni Sanskritic evidence~~ — **Cleared 2026-05-16 (Tier F triple deep-dive).** Endnote `mitanni-sanskritic-evidence` refined: CTH numbering added (CTH 51 = KBo I 1 + CTH 52 for treaty; CTH 284–286 for Kikkuli tablets); Artashumara form-vs-cognate clarified; expanded references list. All four substantive claim-blocks (treaty deities, Kikkuli + *aika* phonology, throne names, *marya/maryannu*) hold.
4. ~~Rigvedic *kṛṇvanto viśvam āryam*~~ — **Cleared 2026-05-16 (Tier F triple deep-dive).** RV 9.63.5 confirmed. Ch 3 §3.4 line 104 refined: *viśvam āryam* wholly omitted by Wilson and Griffith; *arāvṇaḥ* substituted-away (Wilson: "withholders of oblations" per Sāyaṇa; Griffith: "the godless ones"). Jamison-Brereton 2014 modern academic translation restores both phrases ("making it all Ārya"; "Ārya-ization") — vindication of the suppressed reading.

---

## Workflow per item

Four possible outcomes when verifying an item:

| Outcome | Action |
|---------|--------|
| **Verified** | Mark `[x]` in todo; remove inline `[VERIFY:]` marker from chapter draft (if present); minor wording adjustment to the prose if exact citation differs from current text |
| **Wrong** | Fix the prose in the chapter; update the todo entry to reflect the correction; mark `[x]` |
| **Uncertain after lookup** | Hedge the prose ("widely cited as," "by accepted accounts," "approximately"); mark `[x]` with note "cleared by hedging" |
| **Not economical to verify** | Cut the specific claim from the prose, or move to a "weak references" register; mark `[x]` with note "cleared by cut/softening" |

All four outcomes move the item to the **Cleared** section of [as_verification_todo.md](../../10_active/as_verification_todo.md) — there is no "left in limbo" state.

---

## Working modes

Three modes, paired to context:

### Background mode (between drafting sessions)

Claude clears a batch of 10–15 Tier A/B items autonomously using WebFetch/WebSearch. Returns a structured report: confirmed / refined / wrong / uncertain. User signs off in bulk.

**Trigger:** "Run a Tier A+B sweep on the verification queue."

### Targeted mode (during chapter work)

When working on a specific chapter, sweep that chapter's verification items first. Couples verification with active editing so corrections land in the same pass.

**Trigger:** "I'm working on Ch X — verify the open items for it first."

### Deep-dive mode (for Tier F load-bearing items)

Dedicated session for one P0 item. The Assalāyana Sutta deserves an hour with the PTS edition (or Bhikkhu Bodhi translation) in hand, not a 5-minute web check.

**Trigger:** "Let's verify the Assalāyana Sutta passage — focus session."

---

## Division of labor

| Tier | Claude alone | Claude + user | User alone |
|------|--------------|---------------|------------|
| A | ✓ | — | — |
| B | ✓ | — | — |
| C (OED-tier) | ✓ | — | — |
| C (IE-specialist) | — | ✓ | — |
| D (public digital editions) | ✓ partial | ✓ | — |
| D (critical editions) | — | ✓ | ✓ |
| E (public data) | ✓ | — | — |
| E (unpublished records) | — | — | ✓ |
| F (legwork) | ✓ | — | — |
| F (hedging decisions) | — | ✓ | ✓ |

---

## Quick-reference: what to say

When the user wants progress:

| User says... | Claude does... |
|--------------|----------------|
| "What's pending on verification?" | Read [as_verification_todo.md](../../10_active/as_verification_todo.md); summarize by chapter |
| "How does verification work?" | This file |
| "Run a Tier A+B sweep" | Spawn an agent to batch-verify Tier A+B items; report back |
| "Verify Ch X items" | Sweep just that chapter's open items |
| "Let's tackle the P0 items" | Open a focused session on Tier F load-bearing items |
| "Mark X as cleared" | Move from Pending to Cleared in todo; remove inline `[VERIFY:]` marker if any |

---

## Status tracking

Item counts as of last update — check current state in [as_verification_todo.md](../../10_active/as_verification_todo.md):

- **Total flagged:** 97 (initial 84 + items split off during sweeps + new claims surfaced during drafting)
- **Cleared:** 90 (Tier A+B sweep 2026-05-13; Sanskrit-at-terminus / MW10 verification 2026-05-13; P1 batch + Tier C sweep 2026-05-14/16; Tier A+B sweep 2026-05-16; Assalāyana deep-dive 2026-05-16; Tier F triple deep-dive 2026-05-16; Tier A+B+D web sweep 2026-05-17 morning; second web sweep 2026-05-17 afternoon)
- **Partial:** 5 (Ambedkar quote; Savarkar *mleccha* anecdote sub-item; Pāṇini-cited grammarian roster pending Saunaga→Śākaṭāyana author decision; *chandasi*/*bhāṣāyām* specific Aṣṭādhyāyī sūtras pending Tier D primary-text session; Behistun readability claim pending Old Persian textual analysis)
- **Pending P0 (Tier F):** 0 (all four cleared 2026-05-16 via Assalāyana deep-dive + Tier F triple deep-dive)
- **Pending Tier A+B (web-verifiable):** 0 (all cleared or hedged 2026-05-17)
- **Pending Tier C (etymology + historical philology):** 0 (AIT-framework colonial-mechanism + √दृश् three-PIE-roots both cleared)
- **Pending Tier D (primary texts):** 2 (*varṇamālā* grid geometry cm positions; formants and acoustic engineering — both Tier D acoustic-phonetics items requiring Stevens 1998 / specialist literature beyond web budget)
- **Pending Tier E (institutional):** 0

**Author decisions flagged:**
- **Saunaga → Śākaṭāyana swap** in the pre-Pāṇinian grammarian roster (Ch 1 §1.1, Ch 4 §4.1, several endnotes) — standard scholarly enumeration has Śākaṭāyana, not Saunaga. Recommend swap unless author has specific source for Saunaga.

After each verification session, update the counts.

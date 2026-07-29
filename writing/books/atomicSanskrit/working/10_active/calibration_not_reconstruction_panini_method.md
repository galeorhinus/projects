# Calibration, Not Reconstruction — Pāṇini's Calibrant Method

*Working note, 2026-07-23. A model of how Pāṇini produced the Aṣṭādhyāyī, with the दृश्/पश् suppletion as the worked case and a Vedic-corpus check as the evidence. **Thinking / research — not yet manuscript.** The manuscript should stay light; deployment notes and verification flags are at the end.*

**Proposed name.** *Calibration, Not Reconstruction* is the headline (the book's dichotomy→reframe, and it opposes the pyramid's "reconstruction regime" directly). *The Calibrant Method* names the mechanism inside it.

---

## 1. The model (author, thinking aloud)

Two civilizational domains handle entropy differently:

- **Vaidika / chandas — the calibrant.** Redundancy-protected (meter, accent, the eleven *pāṭhas* = an error-correcting code), so it resists *apabhraṃśa*. The Vedic forms are the **uncorrupted reference**.
- **Laukika / bhāṣā — the entropy battle.** No such armor; it drifts continuously and accumulates *apabhraṃśas*. This is *why* the Aṣṭādhyāyī helped: it holds the worldly domain against drift.

**Pāṇini's method then has two branches:**

1. **Decode from the calibrant.** Where the *laukika* gives conflicting answers, measure them against the Vedic reference and record what the calibrant attests.
2. **Construct where the calibrant is silent.** Where the Veda has too few samples to reverse-engineer, impose a rule consistent with *what is engineerable*.

**The contrast that names it.** Both Pāṇini and the pyramid operate on drifted forms — but:

- **Reconstruction (the pyramid):** infer a *lost, unattested ancestor* from drifted descendants. Forward from an imaginary source (PIE, \*derḱ-, \*speḱ-).
- **Calibration (Pāṇini):** check drifted forms against a *preserved, attested reference* (the Vedic calibrant). No invented ancestor.

This is the "encoded in the Vedas, decoded by Pāṇini" thesis turned into a *mechanism*: the Vedas are not only where the architecture is encoded — they are the fixed instrument against which *laukika* drift is measured.

---

## 2. The worked case — the दृश्/पश् suppletion

**The facts.** दृश् (*dṛś*, "see") uses a genuinely different root, पश् (*paś*), in the present:

- Present system → **पश्य**: पश्यति (sees), imperfect अपश्यत्, imperative पश्य, optative पश्येत्.
- Everything else → **दृश्**: perfect ददर्श, aorist अदर्शि, passive दृश्यते, participle दृष्ट, absolutive दृष्ट्वा, nominals दर्शन / दृष्टि / दृश्य.

**Pāṇini documents it — Aṣṭādhyāyī 7.3.78** (⚠ verify sūtra number), one rule enumerating *all* roots that take a special present stem, each with its substitute:

| *dhātu* | present substitute | present | gloss | same root or suppletion? |
|---|---|---|---|---|
| पा | पिब | पिबति | drinks | same root (reduplicated present) |
| घ्रा | जिघ्र | जिघ्रति | smells | same root |
| स्था | तिष्ठ | तिष्ठति | stands | **same root** (तिष्ठ = reduplicated present of स्था) |
| सद् | सीद | सीदति | sits | same root |
| **दृश्** | **पश्य** | **पश्यति** | **sees** | **true suppletion** (पश् ≠ दृश्) |
| दाण् (दा) | यच्छ | यच्छति | gives | suppletion-ish (यच्छ ← *yam*; ⚠ source) |

So **being in 7.3.78 does not make स्था "like दृश्."** स्था→तिष्ठ is one root's own reduplicated present; दृश्→पश्य is two roots. Pāṇini treats them *uniformly* as substitutions in the present environment, **origin-agnostic** — a closed lookup table of special-present roots. The pyramid comes later, picks the genuinely two-root entries, and reads *imaginary ancestry* back into the table.

**Retracted hypothesis (kept as a warning).** "\**darśati* would collide with the causative दर्शयति, so पश्यति" — **fails.** Sanskrit tolerates exactly that pair elsewhere: बुध् → present बोधति *and* causative बोधयति, differing only by -य-, no suppletion. Collision-avoidance cannot be the driver. Leave the दृश्/पश् "why" **open**, not papered over.

**Note दर्श् is not a separate *dhātu*** — it is the *guṇa* grade of दृश् (ऋ → अर्), used by the perfect and causative. One atom, two grades, plus one prescribed present-substitute (पश्य).

---

## 3. अस्/भू — the case that *does* have a "why"

Different from दृश्/पश्, and the stronger example if a functional reason is wanted:

- **अस् and भू are two genuinely separate *dhātus*** — both in the *Dhātupāṭha*; **भू is entry #1** (भू सत्तायाम्); अस् is *adādi* class 2.
- **अस्** = stative "be, exist," present-system only, **defective** (no natural aorist/perfect): अस्ति, सन्ति, आसीत्.
- **भू** = "become, come into being, grow," eventive, **full** paradigm: भवति, बभूव, भविष्यति, भूत.
- **The functional analysis (standard historical morphology; ⚠ source before body):** the stative root supplies the present (a state); the eventive "become" root supplies the perfective/future/participle (events of coming-to-be). A pure stative can't form an aorist, so भू fills the eventive slots. English shows it triply: *is/am/are* (अस्), *be/been/being* (भू), *was/were* (\*h₂wes-).

**The reframe for अस्/भू is descent vs design:** the pyramid says *two ancestral roots merged by accident*; the *Dhātupāṭha* says *two atoms, each placed where its aspect fits*. (No "manufactured split" to prosecute here — everyone agrees there are two roots — so this is a *different* argument from दृश्/पश्; don't conflate them.)

---

## 4. The evidence — Vedic-corpus check (run 2026-07-23)

**Question:** is the दृश्/पश् suppletion already in the calibrant (branch 1, decode), or a *laukika* reconstruction (branch 2, construct)?

**Method.** DCS (Digital Corpus of Sanskrit), CoNLL-U morphological tags, restricted to the Vedic Saṃhitās (Ṛgveda, both Atharvavedas, Kāṭhaka, Maitrāyaṇī, Taittirīya, Vājasaneyi). Token-level tally by lemma × tense/mood. Path: `analysis/ganah/data/raw/dcs/dcs/data/conllu/files/`.

**Result — the suppletion is fully Vedic:**

- **पश् (present system):** 244 present + 129 imperfect forms — पश्यति (30), पश्यन्ति (29), अपश्यत् (53), पश्येम (19), पश्यामि (15)…
- **दृश् (everything else):** 118 past (perfect ददर्श, दददृशे; aorist अदर्शि, अदृश्रन्), ~105 non-finite (infinitive दृशे 51, दृशये 13; absolutive दृष्ट्वा; participles), passive present दृश्यते (8), नोun दृश् (17).
- **The present *indicative* of "see" is *always* पश्यति. There is no indicative \**darśati*.**
- The only दर्श- **finite** forms in the Saṃhitās — दर्शति (1), दर्शत्/दर्शन्/दर्शथः/दर्शम् — are all **Mood=Sub (subjunctive) or Mood=Jus (jussive)**, the archaic Vedic modal system Classical Sanskrit dropped. Not the present indicative.

**Showcase, already in the book:** Ṛgveda 10.71.4 — **उत त्वः पश्यन् न ददर्श वाचम्** — one *seeing* (पश्यन्, from पश्) has not *seen* (ददर्श, perfect of दृश्) Speech. The two roots supplete *in one line of the Ṛgveda.* (Ch13 epigraph; endnote `rigveda-10-71-4-vach`.)

**Conclusion.** For दृश्/पश् it is **branch 1 (decode), not branch 2 (construct).** Pāṇini did not reconstruct the suppletion from drifted *laukika* forms and did not construct it in a data-gap — he **documented what the calibrant already attests.** The "why two roots" recedes past Pāṇini into the Vedic language itself, and the book does not need to answer it.

**A telling detail:** the DCS itself lemmatizes दृश् and पश् as **two separate lemmas** — the "two roots" instinct at the corpus level — while Pāṇini's 7.3.78 unifies them under one *Dhātupāṭha* entry (दृश्) + a stated substitution. Calibration unifies; the reconstruction instinct splits.

---

## 5. Book implications & deployment

- **Preserved outside the Chapter 19 body.** The clean framing remains available for a later Companion case: *Sanskrit places दृश्→पश्य in the same rule as स्था→तिष्ठ — one enumerated class of present-stem substitutions, and the calibrant records the distribution directly. The machinery treats one documented substitution as descent from two ancestors while leaving the similar स्था→तिष्ठ relation alone, because that one offers no second atom to reconstruct.*
- **The reframe is *calibration vs reconstruction*.** Both examine changed forms; reconstruction invents an unrecorded ancestor, while calibration checks a form against a recorded measure. This may support Chapter 1, Chapters 18–18, or a later *Second Shanti* treatment at civilizational scale.
- **A testable research program.** Where the Vedic record of a form is thin, branch 2 predicts that Pāṇini's treatment may reveal construction rather than documentation. The same corpus can identify sparsely recorded *dhātavaḥ* and test whether each rule was derived from existing use or completed by design.
- **Keep the manuscript light.** One line + endnote at most for the suppletion (the discussion is not the deliverable). Use **अस्/भू** if a *functional* suppletion example is wanted; keep the दृश्/पश् "why" open. The collision hypothesis is retracted — do not deploy it.

## 6. Verification flags

- **DCS is secondary, auto-tagged.** The tense/mood tallies are good for the pattern; a hand-check of the Ṛgveda present-forms of "see" would firm the headline before body use.
- **7.3.78** sūtra number and the substitute list (esp. सृ→धौ) — verify against the Aṣṭādhyāyī.
- **यच्छ ← *yam*** historical note — source it.
- **अस्/भू aspect account** — standard, but state as *the functional analysis* and cite.
- **The construct-where-silent branch** is a hypothesis about method; it needs its own grounding before it is more than a frame.

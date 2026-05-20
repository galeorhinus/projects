# Session 11 Handoff — Night Sweep Complete

**Date:** 2026-05-18
**Branch:** main (28+ commits ahead of pre-night-sweep state)
**Status:** Night sweep complete across all 29 manuscript files + Endnotes + Appendices 1–6.

---

## What this session did

### The night sweep

Comprehensive voice-correction pass across the entire manuscript to align with the Voice Prime Directive added to CLAUDE.md (836c8e1). Three failure modes targeted:

1. **Recoverist register** — *the book / we / this chapter* as agent of polemic verbs (*reads, walks, recovers, sides, has been describing*).
2. **Procedural-polemic register** — abstract nouns (*the argument, the position, the reading, the framework*) as grammatical subject of polemic claims.
3. **Sanskrit-frame codification violations** — the orthodoxy's *codified* misnaming applied uncontested to Pāṇini's decoding, the Prātiśākhya tradition's documentation, the varṇamālā's architecture.

The conversion rule used throughout: replace recoverist / procedural-polemic constructions with named-concrete agents (Sanskrit, the orthodoxy, the engineering, Pāṇini, the varṇamālā, the engineering thesis, codification, vyākaraṇam) or with chapter/section-as-venue + licit verbs (*describe, establish, lay out, name, show, dismantle, prosecute, develop, introduce*).

### Files touched (28 commits)

**Voice rules:** CLAUDE.md + .claude/skills/atomic-sanskrit/SKILL.md (836c8e1) — Voice Prime Directive + four-term polemic stack (engineered / encoded / decoded / codified).

**Main manuscript (front matter through end-matter):**
- as_0_01_preface.md — chronology refusal canonical form
- as_1_00_seekers.md (Ch 0) — 8 edits + final "The book reads" fix
- as_1_01_botanical.md (Ch 1) — book contests + Chapter 14 walks
- as_1_02_strategic.md (Ch 2) — chapter-as-agent + perimeter close
- as_1_03_fourth_abrahamic.md (Ch 3) — 8 edits
- as_1_04_siddha.md (Ch 4) — 4 edits
- as_1_05_apabhramsa.md (Ch 5) — 7 edits
- as_1_06_dhatuh.md (Ch 6) — title + §6.4
- as_1_07_adivadya.md (Ch 7) — walks → develops
- as_1_08_mapping_mouth.md (Ch 8) — chapter-as-agent
- as_1_09_retroflex.md (Ch 16) — §16.3 codification-perimeter rewrite
- as_1_09_superset.md (Ch 9) — §9.1 methodology cluster rewrite
- as_1_10_building_dhatuh.md (Ch 10) — corrections + figures
- as_1_11_ganah.md (Ch 11) — drafting scaffold + walks → develops
- as_1_12_affixation.md (Ch 12) — book-as-agent
- as_1_13_preservation.md (Ch 13) — italic abstract walks → develops (×2)
- as_1_14_calibration.md (Ch 14) — register vs mode terminology
- as_1_15_aural.md (Ch 15) — codifies → documents; this chapter walks → develops
- as_1_17_wrong_question.md (Ch 17) — 4 edits
- as_1_18_pie_in_sky.md (Ch 18) — 8 edits
- as_1_19_life_after_pie.md (Ch 19) — 5 edits
- as_2_01_epilogue.md — 8 edits
- **Appendices:** as_3_01 (App 1), as_3_02 (App 2) — voice fixes + strawman-engagement prose with contemporary softened orthodoxy; as_3_03 (App 3) — 8 edits including §7 first-person preservation; as_3_04 (App 4) — 5 edits; as_3_05 (App 5) — 4 edits; as_3_06 (App 6) — 6 edits.
- **Endnotes** (as_endnotes.md) — 83 line edits: 49× *the chapter anchors* → *the chapter establishes*; *the Appendix anchors* → *establishes*; *Chapter 2 anchors* → *establishes*; *the chapter argues for* → *develops*; book-deploys conversion; codification → decoding/documenting for Sanskrit-frame instances (Pāṇini's codification → decoding; Prātiśākhya codified → documented; Sanskrit codification perimeter → calibration perimeter; codified language → decoded language); non-Sanskrit codification uses (Masoretic, Quranic, Greek, Latin, Hebrew, Chinese, IPA, Nāṭyaśāstra) and deliberate polemic-target uses (endnotes that name *codification* as the orthodoxy's misnaming) preserved as-is.

### Phase 3 verification grep results

Final sweep across all `as_*.md` files confirms zero remaining hits for:
- chapter walks / chapter reads / chapter recovers
- book walks / book reads / book recovers
- this appendix walks / reads / recovers / sides / has been
- the contesting position / the position the book advances / the argument refuses / the framework refuses (as polemic subject)
- refuses outright / refuses categorically / refuses on principle

The remaining `the framework refuses to read` hit at as_3_02_encyclopaedic.md:196 is the polemic orthodoxy-frame ("the very Sanskrit the framework refuses to read as engineered") — the *philological framework* as named subject of its own refusal, which is canonical polemic register, not the banned procedural-polemic pattern.

### Empirical work that landed alongside

Ch 10 / App 5 Dhātupāṭha empirical-analysis bundle (af297ae): FINDINGS.md (~12K words, 23 sections); three new analysis scripts (analyze_internal_structure.py, analyze_position_roles.py, cluster_by_reactivity.py); particle-count one-particle row added to PROSE-READY SUMMARY. Ch 10 §10.10 figure planting + Engineering Was Common Knowledge close (11ffe97). Ch 11 drafting scaffold landed (fd79d5c).

---

## Locked decisions

**Voice Prime Directive is canonical** — recoverist and procedural-polemic registers are banned across the manuscript. The two failure modes share one grammatical seam (wrong subject for polemic sentence); CLAUDE.md and SKILL.md document conversion tables for both.

**Four-term polemic stack is canonical** — *Engineered / Encoded / Decoded / Codified*. The standing polemic phrase: *Sanskrit was engineered. Encoded in the Vedas. Decoded by many. Pāṇini's decoding is the finest.* Sanskrit-frame *codified* is the orthodoxy's misnaming, scare-quoted only.

**Saunaga decision was deferred by the user** during the night sweep — proceed with the rest of the sweep work; revisit Saunaga separately.

**App 1–2 carry strawman-engagement prose** — the contemporary softened orthodoxy (post-Cardona, post-Houben, post-Pollock) concedes Pāṇini-level structural sophistication via *codified* but still denies engineering-before-Pāṇini. App 1 §3 close and App 2 opening engage this directly.

---

## Outstanding work

**P0 (next session opener):**

1. **Saunaga decision** — user deferred during night sweep. The question: how to handle the *Saunaga* / *Śaunaka* attribution in the chapter that names the *Prātiśākhya* compilers and the pre-Pāṇinian grammarian roster.

2. **Title-page series-line** — carry-forward item from the pre-night-sweep todo list. The series-line text and placement on the title page have not yet been finalized.

**P1:**

3. **Figure production pass** — chapters 11, 12, 13 carry inline `[FIGURE X.Y]` placeholders that need to be materialized as actual figure scripts and built outputs. Ch 10 has its figure scripts already (figures/ch11/); Ch 11 and Ch 12 do not.

4. **Verification queue** — `working/as_verification_todo.md` carries the inline `[VERIFY:]` markers logged across chapter drafts. The queue has not been worked since pre-night-sweep.

5. **Endnote numerical conversion** — endnote stubs throughout the chapter drafts are still keyed by stub name (`[NOTE: stub-name]`). Numerical conversion happens at chapter-lock time. Not all chapters are chapter-locked yet.

**P2:**

6. **Ch 11 polemic-landing pass** — the Ch 11 drafting scaffold landed in fd79d5c carries the structural framework; the polemic-landing pass that converts the scaffold into final prose has not yet been done.

7. **Companion paper integration** — `reference/as_companion_paper_subcontinental_calibrant.md` exists as draft companion paper; the cross-references from main chapters to the companion have not yet been wired.

---

## Next-session opener recommendation

Open with the **Saunaga decision** (P0 #1) — it was the one item the user explicitly deferred during the night sweep, and it blocks finalization of the chapters that name the pre-Pāṇinian grammarian roster. Once decided, sweep the affected chapters (Ch 7, Ch 10, Endnotes §`pre-paninian-grammarians`) and update the canonical roster in one pass.

After that, **title-page series-line** (P0 #2) is the smallest remaining item.

Then move to **figure production** (P1 #3) for Ch 11 and Ch 12, which is the highest-leverage P1 item — figures are blocking on chapter-lock for those chapters.

---

*End of Session 11 handoff. The night sweep is complete; the manuscript is in canonical Voice Prime Directive register across all 29 files plus endnotes plus all six appendix parts.*

# *Atomic Sanskrit* — Finishing Plan

*Living checklist for the post-draft-1 work: tightening, verification, external input, and submission. Created 2026-05-31 when draft-1 of writing was declared complete. Updated as items complete.*

## Where we stand

- **Manuscript:** ~139k words (target: ~115k prose + ~5k endnotes ≈ ~120k, **raised 2026-05-31 from the earlier 90k target**). Currently **~1.16× target**. Gap is now ~19k, not ~49k — much more achievable; A.2 alone can essentially close it.
- **Endnotes:** ~89k words in `as_endnotes.md` — substantial reference-grade material; some movable to the companion companion.
- **Structural / framing work:** complete (recent passes: chapter renames, three-frame standardization, mouth-to-language scale-chain, six-characteristic test at three scales, App 5 reorg, Ch 12 §§12.1–12.10 drafted, Vedic-corpus research, public-facing essay framework).
- **Open audits:** contrastive framing (215 findings, 35 reds with APPLY decisions ready), repetition audit (scaffold only), verification queue (active backlog), endnote conversion (deferred to chapter-lock), epigraph deployment (candidates chosen per chapter, many not yet inserted), Vedic-corpus research deployment (findings catalogued, insertions pending).

## Status conventions

- `[ ]` — not started
- `[~]` — in progress
- `[x]` — done
- `[-]` — skipped / abandoned (with note)

When a phase or sub-item completes, mark the box and add a one-line note with the commit hash if relevant.

---

## Phase A — Tightening (prose work)

*Goal: bring word count toward target while sharpening the polemic. Highest leverage on getting to ship-ready.*

### A.1 — Apply contrastive-framing red fixes [x]

- [x] Apply the 34 🔴 findings marked `[APPLY REWRITE]` in `working/80_completed/audits/contrastive_framing_audit_2026-05-30.md`.
- [x] Leave the 5 🔴 findings marked `[KEEP ORIGINAL]` alone (Findings 2, 16, 17, 25, 33 — Findings 17 and 25 were re-marked from APPLY to KEEP after body text reread).
- [x] Per finding: open the named file, locate the prose, apply the suggested replacement.
- [ ] Commit (this batch — see status log entry 2026-05-31).

**Why first:** decisions already made; replacements drafted; will tighten polemic register across multiple chapters uniformly; surfaces any remaining defensive register; modestly reduces word count; sets up the repetition audit (some defensive prose IS repetition).

**Estimated:** one focused session.

### A.2 — Run the repetition audit [~]

- [x] Generate findings: 125 findings catalogued in `working/80_completed/audits/repetition_audit_findings_2026-05-31.md` (2026-05-31 agent pass). Categorized using the seven-label scheme: 22 KEEP, 39 COMPRESS, 7 MERGE, 16 CUT, 28 POINTER, 9 ENDNOTE, 4 PROMOTE.
- [ ] Decision pass: user reviews each finding, marks the recommendations to apply / override / KEEP. Same pattern as the contrastive-framing audit's decision pass (mark per-finding APPLY / KEEP / different-action).
- [ ] Apply the cuts, compressions, merges, and pointer-replacements.
- [ ] Track word count delta to confirm trim is happening.

**Estimated trim if all non-KEEP findings applied:** ~18,900 body words (~16,400 pure cut + ~2,100 body-to-endnote relocation). With target raised to ~120k (2026-05-31), A.2 essentially closes the trim gap by itself — Phase A.3 (endnotes) and A.4 (scope cuts) become optional polish rather than required cuts.

**Why second:** biggest single trim lever. Repetition cuts directly attack the word-count overrun. Decisions are non-trivial (must distinguish intentional refrains from accidental repetition) but the label system is ready.

**Estimated:** multiple sessions; could be split chapter-by-chapter.

### A.3 — Move expandable content to endnotes [ ]

- [ ] Identify body passages that serve verification-readers rather than narrative-readers (extended definitions, secondary examples, citation discussions, source-history mini-essays).
- [ ] Per CLAUDE.md two-form endnote architecture: short form in printed book, long form in companion.
- [ ] Move long-form to `as_endnotes.md` under appropriate stub names; insert `[NOTE: stub-name]` markers in body.
- [ ] Verify that the body still reads cleanly after extraction.

**Estimated:** chapter-by-chapter; 1–2 chapters per session.

### A.4 — Structural review for non-load-bearing sections [ ]

- [ ] With the framing now sharper, review each chapter for sections that may have been superseded by stronger material elsewhere.
- [ ] Candidates: any section that explains what another chapter explains better; any section that was a placeholder before the framing solidified; any section whose work is now done by a hammer-phrase or endnote.
- [ ] Cut or merge as warranted.

**Estimated:** structural pass across full manuscript; one session.

---

## Phase B — Verification (fact-check work)

*Goal: every empirical claim, every Sanskrit citation, every name-and-source is verified. Catches errors before external readers do.*

### B.1 — Run the verification queue [ ]

- [ ] Work through `working/10_active/as_verification_todo.md`. Each `[VERIFY:]` marker becomes a concrete check.
- [ ] Per verification: identify the canonical source, confirm the claim, log the resolution.
- [ ] Where chronology-claims appear, apply the book's chronology-refusal discipline (internal-frame ordering > orthodoxy chronology).

### B.2 — Deploy Vedic-corpus research findings [ ]

- [ ] Insert *helayo helayaḥ* / *āttavacaso parābabhūvuḥ* (Śatapatha Brāhmaṇa 3.2.1) into Ch 5 §5.1 or §5.2 (load-bearing for *apabhraṃśa* etiology).
- [ ] Insert *kā prakṛtiḥ* (Gopatha Brāhmaṇa 1.1.24) into Ch 0 §0.4 or Ch 1 §1.4 (categorial question in *śruti*).
- [ ] Insert *vikṛti*-altar-variants (Śatapatha Brāhmaṇa 6.7.2) into Ch 0 §0.4 (Vedic technical *prakṛti / vikṛti* opposition).
- [ ] Insert *siktiḥ / vikṛtiḥ* pairing (Aitareya Brāhmaṇa 2.39) where useful.
- [ ] Add endnote stubs for each; ensure proper Devanāgarī + IAST + translation per book convention.
- [ ] Source: `working/40_reference/research/sanskriti_prakriti_vikriti_vedic_corpus_research_2026-05-30.md`.

### B.3 — Deploy chosen epigraphs [ ]

- [ ] Per-chapter pass: insert the epigraphs chosen in `working/10_active/as_epigraph_plan.md`.
- [ ] Follow first-use convention: Devanāgarī + IAST + endnote-stub for translation (per chapter's translation-timing decision in the plan).
- [ ] Ensure no double-deployment (e.g., RV 1.164.39 chosen for Ch 12 is not duplicated elsewhere).
- [ ] Update the epigraph plan as deployments land.

### B.4 — Sanskrit-text verification pass [ ]

- [ ] Every Sanskrit word / phrase / verse / sūtra in the body needs verification: spelling, sandhi, source.
- [ ] Spot-check Devanāgarī rendering for typographical errors.
- [ ] Confirm IAST diacritics across the book are consistent.

---

## Phase C — External input

*Goal: trusted external readers surface what insiders cannot see. Most valuable after Phase A + B are substantially complete.*

### C.1 — Beta reader set [ ]

- [ ] Identify 3–5 beta readers covering:
  - One Sanskrit-knowing scholar (engagement with the *vyākaraṇa* / *śruti* claims)
  - One polemic-friendly Indic-thought reader (engagement with the *sanātan* / asuric-pyramid framing)
  - One non-specialist intelligent general reader (does the argument land?)
  - One academic comparativist (if a good-faith one is available) (engagement with the PIE / orthodoxy critique)
- [ ] Confirm willingness, time horizon, NDA / use-of-feedback expectations.

### C.2 — Send + collect feedback [ ]

- [ ] Send the manuscript with a structured feedback request:
  - Which arguments landed?
  - Which didn't?
  - Where did you get lost?
  - What did you want more / less of?
  - Specific factual corrections?
- [ ] Collect responses; categorize feedback.

### C.3 — Integrate beta feedback [ ]

- [ ] Second substantive editing pass based on beta findings.
- [ ] Distinguish feedback that requires structural change vs prose change vs no change.
- [ ] Log decisions in a beta-feedback-integration file.

---

## Phase D — Submission / production

*Goal: ready-to-ship manuscript and publisher submission.*

### D.1 — Carryover items from Session 11 P0 [ ]

- [x] **Saunaga decision** — corrected the pre-Pāṇinian grammarian roster to Śākaṭāyana in Chapter 5, Figure 5.1, and the governing endnotes on 2026-08-30.
- [ ] **Title-page series-line** — finalize series-line text and placement.

### D.2 — Endnote finalization [ ]

- [ ] Convert `[NOTE: stub-name]` markers to numbered references at chapter-lock time.
- [ ] Confirm every stub in body has a corresponding entry in `as_endnotes.md`.
- [ ] Run `--endnotes=short` build for the printed-book endnote section once the editorial short-form pass has completed across all stubs.
- [ ] Confirm `--endnotes=full` produces the reference-grade companion.
- [ ] Replace the ORL companion-work source anchor with final publication chapter/page citations before production lock.

### D.3 — Figure production finalization [ ]

- [ ] Work from `working/10_active/as_figure_production_queue.md` as the canonical placeholder queue.
- [ ] Confirm every `[FIGURE X.Y]` placeholder is resolved (drafted figure script, rendered SVG, captioned).
- [ ] Audit figure quality across all chapters.
- [ ] Confirm the Ch 12 9 SVG figures (commit `3b7075b`) render cleanly in the build.

### D.4 — Cover design [ ]

- [ ] Brief for the cover artist / designer.
- [ ] Title + subtitle locked: ***Atomic Sanskrit: The Radiant, Calibrant, and Fractal Architecture of Sanātan*** (per current `as_book.yaml`).

### D.5 — Final copy edit [ ]

- [ ] Professional copy edit pass after Phase A/B/C are complete.
- [ ] Spelling, punctuation, consistency, citation format.

### D.6 — Publisher / agent submission package [ ]

- [ ] Query letter
- [ ] Synopsis (short + long)
- [ ] Sample chapters
- [ ] Author bio
- [ ] Comparative titles
- [ ] Submission list (publishers / agents)

### D.7 — Pre-launch essay sequence [ ]

- [ ] Per `outreach/articles/article_release_table.md`, draft and place the priority essays.
- [ ] Recommended starter sequence:
  1. **Pāṇini Is a Hero — But Not Because He Codified Sanskrit** (Swarajya; publisher-attention piece)
  2. **The Third Category of Language** (Swarajya or Indian Express; introduces *saṃskṛti* publicly)
  3. **The Indian Accent That Breaks the Aryan Migration Story** (Firstpost; retroflex hook — drafts already exist)
  4. **Calibration, Not Codification** (Hindustan Times; authority-vs-architecture)
- [ ] Six-month rollout coordinated with submission / publication timeline.

---

## Sequencing recommendation

Run the phases roughly in order: **A → B → C → D**. Within each phase, items can sometimes be parallelized, but the macro sequence matters:

- Phase A first because trimming sharpens what beta readers will see
- Phase B second because verification catches errors before external eyes
- Phase C third because beta feedback is most valuable once polish is in
- Phase D last, but the remaining part of **D.1** (title-page) and **D.7** (essays) can run in parallel with earlier phases.

## Status log

*Append one line per major event. Use commit hashes where relevant.*

- **2026-05-31** — Finishing plan created. Draft 1 declared complete at commit `d277406`. Manuscript at ~139k words; target ~90k; trim is the biggest single gap.
- **2026-05-31** — Phase A.1 executed: 34 of 36 🔴 findings applied; Findings 17 and 25 re-marked KEEP ORIGINAL (body text disagreed with header); total reds now 5 KEEP + 34 APPLIED. See updated audit.
- **2026-05-31** — Word-count target raised from ~90k to ~120k (~115k prose + ~5k endnotes). Reflects that the architectural chapters and the prosecutorial arc need the depth they carry. Trim gap drops from ~49k to ~19k; Phase A.2 alone can essentially close it, making A.3 and A.4 optional polish rather than required cuts. Propagated to `CLAUDE.md`, `working/10_active/as_todo.md`, and `reference/as_toc_notes.md`.

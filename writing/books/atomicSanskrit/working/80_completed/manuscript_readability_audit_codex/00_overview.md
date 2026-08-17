# Manuscript Readability Audit - Approval Overview

**Status:** Twelve-pass audit complete. Proposal only. No manuscript changes have been made.

**Audience test:** An intelligent non-specialist should be able to follow the argument without training in linguistics, philology, law, or academic debate.

## Scope

The audit follows the configured reading order in `as_book.yaml`:

- About the series, Preface, Overture, Chapters 0-19, and Epilogue
- all seven Part openers
- Appendices 1-9
- Acknowledgments and Note on the Notes
- endnotes, at the more technical level appropriate to the Source and Reference Companion

Archives, build artifacts, superseded drafts, and reference-only planning documents are outside scope.

## Governing Rules

1. Prefer ordinary words and concrete actions.
2. Identify who acts, what they act upon, and what changes as a result.
3. Use a short qualifier when it preserves accuracy without interrupting the explanation.
4. Add an explanatory sentence when the reader genuinely needs the missing step.
5. Do not compress uncertainty into academic or legal labels.
6. Preserve earned refrains, deliberate hammers, mantra cadence, lists, and examples.
7. Add subheadings only when they help the reader see a real internal movement.
8. Merge a short numbered section only when it performs no independent argumentative work.
9. Preserve the author's thesis, level of certainty, and diagnostic force.
10. Make no manuscript edit until the author approves the proposal.

## Twelve Audit Passes

1. Lock scope and document format.
2. Measure section length, paragraph density, figures, and heading structure.
3. Scan for compressed, academic, legal, passive, and abstract prose.
4. Close-read front matter and Chapters 0-4.
5. Close-read Chapters 5-9.
6. Close-read Chapters 10-14.
7. Close-read Chapters 15-19 and Epilogue.
8. Close-read Part openers and Appendices 1-9.
9. Audit captions, tables, figure introductions, and section transitions.
10. Audit endnotes at the appropriate technical level.
11. Reconcile repetition, terminology, pacing, and priorities across chapters.
12. Verify completeness, links, and zero manuscript edits.

## Main Findings

The manuscript's strongest writing explains a visible mechanism through an example and then states the consequence. The weakest writing either compresses several steps into an abstract sentence or repeats a conclusion after the example has already established it.

The problems are concentrated rather than uniform:

1. A small number of long sections perform several different jobs without enough internal structure.
2. Several transitions rely on labels such as `framework`, `hinge`, `field`, `operation`, or `architecture` where the reader needs the concrete action.
3. Part I is much longer than the other Part openers and repeats material that belongs to its chapters.
4. The appendices contain valuable evidence but still include internal drafting language, unresolved figure instructions, duplicated body argument, and claims broader than the displayed evidence.
5. The expanded endnotes are a 114,000-word companion in their own right. They need publication triage, not merely copyediting.
6. Figure numbering is split between manually written numbers and build-generated numbers, which can produce duplicated labels.
7. The central refrains are strong. They will land harder when each recurrence performs a new job instead of restating the whole thesis.

## Proposed Execution After Approval

For implementation at the same level of care, use twelve passes:

1. Remove approved production artifacts and resolve publication blockers.
2. Apply approved section splits, merges, headings, and subheadings.
3. Revise the front matter and Chapters 0-4.
4. Revise Chapters 5-9.
5. Revise Chapters 10-14.
6. Revise Chapters 15-19 and the Epilogue.
7. Revise all Part openers and read the Part transitions in sequence.
8. Revise Appendices 1-4.
9. Revise Appendices 5-9.
10. Triage and revise the expanded endnotes.
11. Standardize figures, captions, introductions, and cross-references.
12. Read the complete book without interruption and repair pacing, repetition, terminology, and transitions.

The structural decisions should come first. Sentence-level revision before approved cuts and moves would polish material that may later disappear or change location.

## Inline Review Workflow

Chapter 17 is the pilot for keeping the comparison inside the manuscript file. The current prose remains live. A proposed change appears immediately beside it in a hidden block with this form:

```markdown
<!-- CODEX-REVIEW C17-001
ACTION: REPLACE
SCOPE: The paragraph or section under review.
REASON: Why a change is proposed.
PROPOSED:
Replacement prose or a structural instruction.
END-CODEX-REVIEW -->
```

These comments do not appear in Pandoc's rendered output. The stable ID makes every open item searchable.

Decision handling:

- **Keep current:** remove the `CODEX-REVIEW` block.
- **Accept proposal:** place the current prose in a `CODEX-OLD` block and make the proposed prose live.
- **Revise proposal:** edit the proposed text inside the review block until it is ready, then accept it.
- **Finish chapter:** move any important rejected or removed material to Lost and Found, then remove the resolved review comments.

The external proposal documents remain the audit record. Once a chapter is migrated inline, its manuscript file becomes the only active decision list.

## Proposal Documents

- `01_front_ch0_4.md`
- `02_ch5_9.md`
- `03_ch10_14.md`
- `04_ch15_19_epilogue.md`
- `05_parts_appendices.md`
- `06_endnotes_captions_global.md`

## Approval Key

The chapter-by-chapter proposal documents primarily use these labels:

- **KEEP** - current form works.
- **REPHRASE** - preserve content and location; rewrite for clarity.
- **EXPLAIN** - add the missing causal or conceptual step.
- **JOIN** - connect fragments that currently make the reader reconstruct the relation.
- **SPLIT** - divide a long section at a real internal turn.
- **MERGE** - fold a short subordinate section into a neighboring section.
- **RENAME** - change a heading that does not describe its material.
- **MOVE** - relocate material only when the current sequence obscures its function.

No **MOVE**, **MERGE**, or numbered-section renumbering should be implemented without explicit approval because each can affect cross-references.

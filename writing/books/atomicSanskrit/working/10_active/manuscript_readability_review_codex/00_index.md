# Atomic Sanskrit Readability Review

This directory is the active decision workspace for the Codex readability audit.

The manuscript contains no Codex review comments. The completed audit under `working/10_active/manuscript_readability_audit_codex/` remains an unchanged historical record. All decisions are made here before any manuscript prose is changed.

## Application Status

The selected decisions in review files 01–27 were processed on 2026-07-23. One hundred nine revisions were applied; two original passages were explicitly retained, and one Part I proposal was superseded without being applied. The accepted second-pass refinements in file 30 and the contradiction-audit repairs were incorporated during the same application cycle.

The complete decision-to-manuscript map is in [31_application_manifest.md](./31_application_manifest.md).

All substantive material removed by an audit revision must also appear in the central [Manuscript Readability Audit — Lost and Found](../../40_reference/source_material/manuscript_readability_audit_lost_and_found.md). The 109 applied revisions have been reconciled there, with 71 applied recovery records. The ledger remains an application gate for every later batch.

## Decision Workflow

Each review block contains the exact current manuscript text and a proposed replacement or structural treatment.

Each block must also classify its effect as `REPHRASE — NO SUBSTANTIVE CUT`, `CUT`, `CONDENSE`, or `MOVE`. A block classified as `CUT`, `CONDENSE`, or `MOVE` requires a Lost and Found ID before application.

Mark one decision:

- `ACCEPT PROPOSED` - apply the proposed text exactly.
- `KEEP ORIGINAL` - close the item without changing the manuscript.
- `USE AUTHOR REVISION` - apply the text written in the Author Revision field.
- `REVISE AGAIN` - Codex prepares another proposal from the comments.
- `DEFER` - leave the item open for a later pass.

When reviewed blocks are processed, Codex applies only accepted or author-revised text. The block status then becomes `APPLIED` or `CLOSED`, with the application date and resulting manuscript location recorded in the same review file.

## Status Summary

| Review file | Unit | Status |
|---|---|---|
| `01_about_series.md` | About the Series | APPLIED |
| `02_preface.md` | Preface | APPLIED |
| `03_overture.md` | Overture | APPLIED |
| `04_ch00.md` | Chapter 0 | APPLIED |
| `05_ch01.md` | Chapter 1 | APPLIED |
| `06_part01.md` | Part I opener | CLOSED / SUPERSEDED |
| `07_ch02.md` | Chapter 2 | APPLIED |
| `08_ch03.md` | Chapter 3 | APPLIED |
| `09_ch04.md` | Chapter 4 | APPLIED |
| `10_ch05.md` | Chapter 5 | APPLIED |
| `11_ch06.md` | Chapter 6 | APPLIED |
| `12_ch07.md` | Chapter 7 | APPLIED |
| `13_ch08.md` | Chapter 8 | APPLIED |
| `14_ch09.md` | Chapter 9 | APPLIED |
| `15_ch10.md` | Chapter 10 | APPLIED |
| `16_ch11.md` | Chapter 11 | APPLIED |
| `17_ch12.md` | Chapter 12 | APPLIED |
| `18_ch13.md` | Chapter 13 | APPLIED |
| `19_ch14.md` | Chapter 14 | APPLIED |
| `20_ch15.md` | Chapter 15 | APPLIED |
| `21_ch16.md` | Chapter 16 | APPLIED |
| `22_ch17.md` | Chapter 17 | APPLIED |
| `23_ch18.md` | Chapter 18 | PARTIAL — C18-007 AWAITS DECISION |
| `24_ch19.md` | Chapter 19 | APPLIED |
| `25_epilogue.md` | Epilogue | APPLIED |
| `26_parts_front_back.md` | Remaining Part openers, Acknowledgments, Note on Notes | APPLIED |
| `27_appendices.md` | Appendices 1-9 | PARTIAL — APP-003 AND APP-009 AWAIT DECISION |
| `28_endnotes_figures_global.md` | Endnotes, captions, and global decisions | REVIEWED / NOT APPLIED |
| `29_work_hold_lexical_sweep.md` | Contextual sweep for `question`, `answer`, `work`, and `hold` | PLANNED |

## Block Format

````markdown
## EXAMPLE-001 - Short description

**Source:** clickable manuscript location  
**Action:** REPLACE / INSERT / DELETE / MOVE / STRUCTURE  
**Cut impact:** REPHRASE — NO SUBSTANTIVE CUT / CUT / CONDENSE / MOVE  
**Lost and Found:** NONE / LAF-R-###  
**Status:** OPEN  
### Original

> Exact current manuscript text.

### Proposed

Proposed replacement text or structural treatment.

### Decision

- [ ] ACCEPT PROPOSED
- [ ] KEEP ORIGINAL
- [ ] USE AUTHOR REVISION
- [ ] REVISE AGAIN
- [ ] DEFER

### Author Revision

```text
Write replacement prose here when selecting USE AUTHOR REVISION.
````

### Comments

Write comments or revision instructions here.
```

## Processing Rules

1. The exact original is refreshed if the manuscript changes before a decision is applied.
2. A block with more than one affected paragraph contains the complete original and complete proposed replacement.
3. Structural blocks show the existing heading sequence and the proposed sequence. They are never applied automatically.
4. Codex does not infer acceptance from casual edits. Select a decision explicitly.
5. Every substantive sentence, clause, claim, example, qualification, citation, heading, figure, caption, or argumentative beat that disappears is copied into Lost and Found before the manuscript changes. The rule is not limited to material Codex considers important.
6. An accepted block marked `CUT`, `CONDENSE`, or `MOVE` cannot be applied without a Lost and Found ID. A move must also record its destination.
7. Pure rephrasing must be marked `REPHRASE — NO SUBSTANTIVE CUT`; when the classification is uncertain, log the material.
8. The historical audit documents are not modified as decisions are made.

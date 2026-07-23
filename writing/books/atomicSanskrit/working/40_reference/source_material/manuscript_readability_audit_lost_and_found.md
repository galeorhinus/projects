# Manuscript Readability Audit — Lost and Found

*Active recovery ledger for material removed through the Codex readability review. Nothing substantive leaves the manuscript silently.*

## Purpose

The chapter review files preserve each original passage beside a proposed revision, but the number and distribution of those files make it difficult to review everything that disappears. This ledger gathers removed material in one place so the author can decide whether it should:

- return to its original location;
- move to another chapter;
- become an endnote, figure caption, appendix passage, or later-volume seed;
- remain cut;
- receive another revision.

The ledger records removal; it does not presume that removal was correct.

## What Must Be Logged

Create an entry before applying an audit revision whenever the revision removes or materially narrows any:

- complete sentence or clause;
- claim, inference, qualification, or limitation;
- example, analogy, comparison, or counterexample;
- quotation, mantra, citation, note anchor, or source reference;
- definition, term installation, refrain, or rhetorical beat;
- heading, figure, caption, table row, list item, or cross-reference;
- historical detail, personal memory, or civilizational argument.

Ordinary copyediting does not require an entry when the new sentence preserves the complete meaning and changes only grammar, spelling, rhythm, or word choice. The audit block must mark that case **REPHRASE — NO SUBSTANTIVE CUT**. When reasonable readers could disagree about whether meaning survived, log the material.

Material moved intact is not a cut, but the ledger must still record the move and its destination so it cannot become lost during structural editing.

## Application Gate

The sequence is mandatory:

1. identify what will disappear;
2. copy the exact material into this ledger;
3. assign a Lost and Found ID;
4. link that ID from the audit block and application manifest;
5. apply the manuscript revision;
6. record the new manuscript location and disposition.

An accepted audit block with **CUT**, **CONDENSE**, or **MOVE** impact cannot be applied without a Lost and Found ID. Nothing gets cut first and reconstructed later from Git history.

## Author Decisions

Use one disposition for each entry:

- `[ ] RESTORE IN PLACE`
- `[ ] RELOCATE`
- `[ ] INCORPORATE PART`
- `[ ] DEVELOP LATER`
- `[ ] KEEP CUT`
- `[ ] REVISE AGAIN`
- `[ ] UNDECIDED`

Author comments control the next action. Codex does not infer a disposition from edits made elsewhere.

## Backfill Queue

### Application batch of 2026-07-23

**Status:** PENDING

The application manifest records 74 applied revisions from review files 01–22, including structural consolidations and contradiction repairs. Before another audit batch is applied, compare every applied original with the resulting manuscript text and create entries here for all substantive omissions. Blocks that only rephrased without loss should be marked **REPHRASE — NO SUBSTANTIVE CUT** in the backfill record.

Source: [`31_application_manifest.md`](../../10_active/manuscript_readability_review_codex/31_application_manifest.md)

### Open review files 23–28

**Status:** GATED

No accepted revision from Chapters 18–19, the Epilogue, remaining front/back matter, appendices, endnotes, captions, or global decisions may be applied until every proposed cut has an entry here.

## Backfill Record

| Audit block | Source unit | Cut impact | Lost and Found entry | Status |
|---|---|---|---|---|
| Review files 01–22 | Applied batch of 2026-07-23 | Audit pending | — | BACKFILL REQUIRED |
| Review files 23–28 | Remaining review | Pre-application audit required | — | APPLICATION BLOCKED |

## Entries

Add entries in source order using the next available ID.

---

## LAF-R-001 — Template

**Source:** `[manuscript file and line]`  
**Audit block:** `[block ID and link]`  
**Change type:** CUT / CONDENSE / MOVE  
**Status:** UNDECIDED  
**Applied:** NO  
**Destination if moved:** —

### Material Removed

> Copy the exact removed manuscript text here. Preserve formatting, note anchors, headings, and figure references.

### Replacement or Result

> Copy the replacement text, identify the new location, or describe the resulting structure.

### Reason Proposed

State why the audit proposed removing, condensing, or moving the material.

### What May Have Been Lost

Identify claims, examples, qualifications, voice, rhythm, civilizational framing, or cross-chapter support that may no longer survive.

### Author Decision

- [ ] RESTORE IN PLACE
- [ ] RELOCATE
- [ ] INCORPORATE PART
- [ ] DEVELOP LATER
- [ ] KEEP CUT
- [ ] REVISE AGAIN
- [x] UNDECIDED

### Author Comments

```text

```


# Atomic Sanskrit Working Directory

This directory holds material that is still useful to the development of *Atomic Sanskrit* but is not part of the compiled manuscript. Its numbered folders separate work by status; durable research and production projects are classified by function.

## Directory Map

| Directory | Purpose | Entry rule | Exit rule |
|---|---|---|---|
| `00_inbox/` | Newly captured material awaiting classification | The idea has value but no status decision yet | Classify during the next working-folder review |
| `10_active/` | Work being executed now or in the next few passes | A next action is defined and currently relevant | Move to queued, paused, completed, or superseded |
| `20_queued/` | Accepted work that has not started | The work belongs in the book and has a concrete next action | Promote when execution begins |
| `30_paused/` | Valid work intentionally deferred | A later volume, milestone, source, or author decision must arrive first | Record the trigger before moving it back to queued |
| `40_reference/` | Durable evidence, decisions, source material, and workflows | The document informs work but is not itself a task | Revise in place while it remains authoritative |
| `50_projects/` | Multi-file production workstreams | The work has its own files, assets, or internal structure | Archive the project only when the whole workstream closes |
| `80_completed/` | Executed plans, audits, and handoffs retained as records | The intended work landed or the audit closed | Keep for provenance; do not use as current guidance |
| `90_superseded/` | Replaced drafts and obsolete plans | A newer document or manuscript passage has taken its place | Preserve only for recovery and comparison |
| `tools/` | Scripts that support manuscript work | Executable or reproducible tooling | Move to a permanent project tool directory if it becomes production infrastructure |

`Completed` and `superseded` are deliberately different. A completed plan records work that was carried out. A superseded document contains an approach that was replaced and must not be treated as authoritative.

## Current Workstreams

| Workstream | Canonical document |
|---|---|
| Current manuscript priorities | [`10_active/as_todo.md`](10_active/as_todo.md) |
| Finishing sequence | [`10_active/as_finishing_plan.md`](10_active/as_finishing_plan.md) |
| Author decisions and tasks | [`10_active/as_author_tasks.md`](10_active/as_author_tasks.md) |
| Verification queue | [`10_active/as_verification_todo.md`](10_active/as_verification_todo.md) |
| Figure production | [`10_active/as_figure_production_queue.md`](10_active/as_figure_production_queue.md) |
| Asura synthesis and deployment | [`10_active/as_asura_synthesis_and_plan.md`](10_active/as_asura_synthesis_and_plan.md) |
| Four language behaviors | [`10_active/four_language_behaviors_claude_plan.md`](10_active/four_language_behaviors_claude_plan.md) and [`10_active/four_language_behaviors_codex_plan.md`](10_active/four_language_behaviors_codex_plan.md), pending consolidation |

## Document Header

New actionable documents should begin with a short status block:

```md
**Status:** Active
**Canonical:** Yes
**Owner:** Shared
**Next action:** Describe the next concrete step
**Last reviewed:** YYYY-MM-DD
```

Paused documents must state the condition that will reactivate them. Superseded documents must identify the replacement. Parallel Claude, Codex, or Gemini drafts remain together only while comparison is active; after reconciliation, the accepted plan moves forward and the alternatives move to `90_superseded/`.

## Maintenance

1. Put new uncategorized notes in `00_inbox/`.
2. Keep `10_active/` small enough to scan in one editor pane.
3. Keep completed history out of `as_todo.md`; move closed task history into a dated record under `80_completed/`.
4. Use `git mv` when status changes so file history remains intact.
5. Repair repository references after every move. A successful move has no stale `working/<old-path>` references.
6. Do not delete removed manuscript material silently. Recovery ledgers belong under `40_reference/source_material/`.

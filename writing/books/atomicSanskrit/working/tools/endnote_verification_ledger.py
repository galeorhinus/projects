#!/usr/bin/env python3
"""Build and validate the complete Atomic Sanskrit endnote-audit ledger.

Batch reports are the verification record. This script combines those reports
with the current manuscript markers and endnote definitions to produce the
master Markdown ledger.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import re
from pathlib import Path


BOOK_DIR = Path(__file__).resolve().parents[2]
MANUSCRIPT_DIR = BOOK_DIR / "manuscript"
ENDNOTES_PATH = MANUSCRIPT_DIR / "as_endnotes.md"
BATCH_DIR = BOOK_DIR / "working" / "10_active" / "endnote_verification_batches"
LEDGER_PATH = BOOK_DIR / "working" / "10_active" / "as_endnote_verification_master.md"

ENTRY_RE = re.compile(
    r"^### `([a-z0-9_-]+)`\s*\n(.*?)(?=^### `|^---|\Z)",
    re.MULTILINE | re.DOTALL,
)
MARKER_RE = re.compile(r"\[NOTE:\s*([a-z0-9_-]+)\s*\]")
SHORT_RE = re.compile(r"^\*\*Short:\*\*\s*(.+)$", re.MULTILINE)
DEPLOYMENTS_RE = re.compile(r"^\*\*Deployments:\*\*\s*(.+)$", re.MULTILINE)
STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+)$", re.MULTILINE)
DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")


def clean_cell(value: str) -> str:
    return value.strip().strip("`").replace("|", "\\|")


def parse_assembly_titles() -> dict[str, str]:
    titles: dict[str, str] = {}
    current_file: str | None = None
    for raw_line in (BOOK_DIR / "as_book.yaml").read_text().splitlines():
        line = raw_line.strip()
        if line.startswith("file: manuscript/"):
            current_file = line.removeprefix("file: manuscript/").strip()
        elif current_file and line.startswith("title:"):
            title = line.removeprefix("title:").strip().strip('"')
            titles[current_file] = title
            current_file = None
    return titles


def parse_entries() -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for match in ENTRY_RE.finditer(ENDNOTES_PATH.read_text()):
        body = match.group(2).strip()
        short = SHORT_RE.search(body)
        deployments = DEPLOYMENTS_RE.search(body)
        status = STATUS_RE.search(body)
        entries.append(
            {
                "id": match.group(1),
                "body": body,
                "short": short.group(1).strip() if short else "",
                "deployments": deployments.group(1).strip() if deployments else "",
                "declared_status": status.group(1).strip() if status else "",
            }
        )
    return entries


def parse_live_markers() -> tuple[dict[str, list[tuple[str, int]]], int]:
    markers: dict[str, list[tuple[str, int]]] = collections.defaultdict(list)
    occurrence_count = 0
    for path in sorted(MANUSCRIPT_DIR.glob("*.md")):
        if path == ENDNOTES_PATH:
            continue
        for line_number, line in enumerate(path.read_text().splitlines(), start=1):
            for match in MARKER_RE.finditer(line):
                markers[match.group(1)].append((path.name, line_number))
                occurrence_count += 1
    return markers, occurrence_count


def parse_markdown_table(lines: list[str], start: int) -> tuple[list[dict[str, str]], int]:
    headers = [clean_cell(cell) for cell in lines[start].strip().strip("|").split("|")]
    if start + 1 >= len(lines) or not re.match(r"^\s*\|?\s*:?-+", lines[start + 1]):
        return [], start + 1
    rows: list[dict[str, str]] = []
    index = start + 2
    while index < len(lines) and lines[index].lstrip().startswith("|"):
        cells = [clean_cell(cell) for cell in lines[index].strip().strip("|").split("|")]
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
        index += 1
    return rows, index


def parse_batch_reports() -> dict[str, dict[str, str]]:
    audited: dict[str, dict[str, str]] = {}
    if not BATCH_DIR.exists():
        return audited
    for path in sorted(BATCH_DIR.glob("batch_*.md")):
        text = path.read_text()
        date_match = DATE_RE.search(text)
        checked = date_match.group(1) if date_match else ""
        batch_match = re.search(r"batch_(\d+)", path.name)
        batch = f"B{int(batch_match.group(1)):03d}" if batch_match else path.stem
        lines = text.splitlines()
        index = 0
        while index < len(lines):
            if lines[index].lstrip().startswith("|"):
                rows, next_index = parse_markdown_table(lines, index)
                if rows and "Endnote" in rows[0] and "Result" in rows[0]:
                    for row in rows:
                        note_id = clean_cell(row["Endnote"])
                        result = row["Result"]
                        audited[note_id] = {
                            "status": result,
                            "risk": row.get("Risk", "P?"),
                            "batch": batch,
                            "checked": "—" if result == "Queued" else checked,
                            "report": path.name,
                        }
                index = next_index
            else:
                index += 1
    return audited


def unused_status(declared_status: str) -> str:
    lowered = declared_status.lower()
    if "retired" in lowered:
        return "Retired"
    if "parked" in lowered:
        return "Parked"
    if "supporting source" in lowered:
        return "Supporting"
    return "Disposition needed"


def deployment_label(
    locations: list[tuple[str, int]], titles: dict[str, str]
) -> str:
    grouped: dict[str, list[int]] = collections.OrderedDict()
    for filename, line_number in locations:
        grouped.setdefault(filename, []).append(line_number)
    labels: list[str] = []
    for filename, line_numbers in grouped.items():
        title = titles.get(filename, filename)
        if title.startswith("Chapter "):
            title = title.split(" — ", 1)[0]
        elif title.startswith("Part "):
            title = title.split(" — ", 1)[0]
        line = line_numbers[0]
        label = f"{title} L{line}"
        if len(line_numbers) > 1:
            label += f" ({len(line_numbers)} uses)"
        labels.append(label)
    return "; ".join(labels) if labels else "No direct manuscript marker"


def structure_status(entry: dict[str, str]) -> str:
    failures: list[str] = []
    if not entry["short"]:
        failures.append("missing Short")
    elif entry["short"].startswith("[TBD:"):
        failures.append("Short TBD")
    if not entry["deployments"]:
        failures.append("missing Deployments")
    if "[VERIFY" in entry["body"]:
        failures.append("VERIFY marker")
    return ", ".join(failures) if failures else "OK"


def build_ledger() -> tuple[str, dict[str, int]]:
    entries = parse_entries()
    markers, marker_occurrences = parse_live_markers()
    audited = parse_batch_reports()
    titles = parse_assembly_titles()
    definitions = [entry["id"] for entry in entries]
    definition_set = set(definitions)
    live_set = set(markers)
    missing_definitions = live_set - definition_set
    duplicate_definitions = len(definitions) - len(definition_set)
    unused = definition_set - live_set
    structure_counter: collections.Counter[str] = collections.Counter()
    for entry in entries:
        status = structure_status(entry)
        if status != "OK":
            structure_counter.update(status.split(", "))
    structure_failures = sum(structure_status(entry) != "OK" for entry in entries)

    status_counts: collections.Counter[str] = collections.Counter()
    rows: list[str] = []
    for entry in entries:
        note_id = entry["id"]
        audit = audited.get(note_id)
        if audit:
            status = audit["status"]
            risk = audit["risk"]
            batch = audit["batch"]
            checked = audit["checked"]
            report = (
                f"[{batch}](endnote_verification_batches/{audit['report']})"
            )
        elif note_id in live_set:
            status = "Unreviewed"
            risk = "P?"
            batch = "—"
            checked = "—"
            report = batch
        else:
            status = unused_status(entry["declared_status"])
            risk = "—"
            batch = "—"
            checked = "—"
            report = batch
        status_counts[status] += 1
        deployment = deployment_label(markers.get(note_id, []), titles)
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{note_id}`",
                    deployment.replace("|", "\\|"),
                    str(len(markers.get(note_id, []))),
                    risk,
                    status,
                    report,
                    checked,
                    structure_status(entry),
                ]
            )
            + " |"
        )

    today = dt.date.today().isoformat()
    summary_rows = "\n".join(
        f"| {status} | {count} |" for status, count in sorted(status_counts.items())
    )
    text = f"""# Atomic Sanskrit — Endnote Verification Master

**Generated:** {today}
**Source of truth for audit results:** `working/10_active/endnote_verification_batches/`
**Generator and integrity check:** `working/tools/endnote_verification_ledger.py`

## Purpose

Track the source verification of every endnote without confusing factual verification with mechanical completeness. Batch reports preserve what was checked, which sources were used, what changed, and why. This ledger projects those results across the complete current inventory.

Do not record an endnote as **Pass** merely because it contains a plausible citation. A completed audit must compare the body claim, Short form, full note, source, locator, and every live deployment.

## Inventory

| Category | Count |
|---|---:|
| Endnote definitions | {len(definitions)} |
| Unique definitions | {len(definition_set)} |
| Unique directly deployed notes | {len(live_set)} |
| Live marker occurrences | {marker_occurrences} |
| Definitions without a direct manuscript marker | {len(unused)} |
| Live markers without a definition | {len(missing_definitions)} |
| Duplicate definitions | {duplicate_definitions} |
| Entries with a structural problem | {structure_failures} |
| Missing `Deployments` field | {structure_counter['missing Deployments']} |
| Surviving verification marker | {structure_counter['VERIFY marker']} |
| Unfinished Short form | {structure_counter['Short TBD']} |

The directly deployed notes receive full source verification. Definitions without a direct manuscript marker receive a disposition review. Supporting entries should be audited with the deployed note that depends on them; parked entries need full source verification only before redeployment.

## Status Summary

| Status | Count |
|---|---:|
{summary_rows}

## Status Rules

- **Pass:** the source, locator, note, and every body deployment agree.
- **Strengthened:** the claim held, but its source, locator, wording, or boundary was improved.
- **Corrected:** a factual, attribution, translation, locator, or claim-scope error was repaired.
- **Narrowed:** the available evidence required a smaller claim.
- **Blocked:** verification reached a source-access or evidence gap that remains unresolved.
- **Supporting:** no direct body marker; another deployed endnote depends on this entry.
- **Parked:** intentionally unused source material.
- **Retired:** removed from the active argument with its disposition recorded.
- **Disposition needed:** unused definition whose future status still needs a decision.
- **Queued:** assigned to the next factual audit batch but not yet verified.
- **Unreviewed:** mechanically present but not yet source-verified under this audit.

Risk is assigned during factual triage: **P0** for load-bearing or potentially damaging claims, **P1** for substantive supporting claims, and **P2** for illustrative or low-risk facts. **P?** means that triage has not yet occurred.

## Audit Protocol

Each factual batch checks:

1. source identity and bibliographic metadata;
2. an exact page, verse, rule, inscription, table, or stable section locator;
3. quotations, Sanskrit text, translations, names, dates, and numbers;
4. agreement among the manuscript claim, Short form, and full note;
5. the boundary between evidence and the book's inference;
6. every live deployment and every dependent endnote;
7. successful full and short manuscript assembly.

## Complete Ledger

| Endnote | Direct deployments | Uses | Risk | Status | Batch | Checked | Structure |
|---|---|---:|:---:|---|---|---|---|
{"\n".join(rows)}
"""
    metrics = {
        "definitions": len(definitions),
        "live": len(live_set),
        "unused": len(unused),
        "missing": len(missing_definitions),
        "duplicates": duplicate_definitions,
        "structure_failures": structure_failures,
    }
    return text, metrics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode", choices=("write", "check"), help="write the ledger or validate it"
    )
    args = parser.parse_args()
    text, metrics = build_ledger()
    if args.mode == "write":
        LEDGER_PATH.write_text(text)
        print(f"Wrote {LEDGER_PATH.relative_to(BOOK_DIR)}")
    else:
        if not LEDGER_PATH.exists():
            print(f"MISSING: {LEDGER_PATH.relative_to(BOOK_DIR)}")
            return 1
        if LEDGER_PATH.read_text() != text:
            print("STALE: regenerate with endnote_verification_ledger.py write")
            return 1
        print("Ledger is current.")
    print(
        "Definitions={definitions} live={live} unused={unused} "
        "missing={missing} duplicates={duplicates} structure_failures={structure_failures}".format(
            **metrics
        )
    )
    return 1 if metrics["missing"] or metrics["duplicates"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

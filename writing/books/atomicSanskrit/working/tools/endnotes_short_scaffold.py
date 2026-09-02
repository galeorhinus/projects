#!/usr/bin/env python3
"""Insert `**Short:** [TBD: <type>]` placeholder after each endnote heading.

Idempotent: skips entries that already have a `**Short:**` field.

Categorization heuristics (rough — these guide the editorial pass, not gate it):
  Citation        — body ≤ 80 words; the citation IS the short form
  Citation+Context — 80 < body ≤ 300 words; pull one load-bearing sentence
  Mini-essay      — body > 300 words; editorial compression needed
  Verification    — body contains [VERIFY] markers or "to be verified";
                    short form is a pointer to the companion
"""
from pathlib import Path
import re

BOOK_DIR = Path(__file__).resolve().parents[2]
ENDNOTES = BOOK_DIR / "manuscript" / "as_endnotes.md"
DRY_RUN = False  # set True to preview only

text = ENDNOTES.read_text()
lines = text.split("\n")

# Each entry starts with `### `<stub>`` and ends at the next such heading or
# the section divider (---) preceding the next heading or end of file.
ENTRY_HEAD = re.compile(r"^### `([^`]+)`\s*$")

# Build list of (start_line_idx, end_line_idx_exclusive, stub_name) for each entry.
entries = []
i = 0
while i < len(lines):
    m = ENTRY_HEAD.match(lines[i])
    if m:
        stub = m.group(1)
        # Find end: next ### heading OR the `---` divider that precedes the next heading
        j = i + 1
        while j < len(lines) and not ENTRY_HEAD.match(lines[j]):
            j += 1
        # Body extent: lines[i+1 : j], strip trailing `---` and blank lines
        body_end = j
        while body_end > i + 1 and lines[body_end - 1].strip() in ("", "---"):
            body_end -= 1
        entries.append((i, j, body_end, stub))
    i += 1

print(f"Found {len(entries)} entries.")

# Categorize each entry
def categorize(body_text: str) -> tuple[str, int]:
    # Strip the Deployments line + any obvious boilerplate
    cleaned = re.sub(r"\*\*Deployments:\*\*[^\n]*\n", "", body_text)
    cleaned = re.sub(r"^\s*-\s+", "", cleaned, flags=re.MULTILINE)  # bullet markers
    cleaned = re.sub(r"^\s*\d+\.\s+", "", cleaned, flags=re.MULTILINE)  # numbered list markers
    # Strip markdown-decoration that inflates wc
    cleaned = re.sub(r"\*\*\*?|\*+|_+|`+", "", cleaned)
    words = cleaned.split()
    wc = len(words)
    # Verification heuristic: body has VERIFY markers or "to be verified" / "verify the citation"
    # Verification: pending-verification markers anywhere in body
    if re.search(r"\[VERIFY\]|\bto be verified\b|verification queue|verification pending|\bDocument\b.*\bcitation\b", body_text, re.IGNORECASE):
        return ("Verification", wc)
    if wc <= 60:
        return ("Citation", wc)
    if wc <= 250:
        return ("Citation+Context", wc)
    return ("Mini-essay", wc)

# Build new content; insert Short field right after the heading.
new_lines = []
inserted = 0
skipped_existing = 0
skipped_categories = {}
last_processed = -1

for (head_idx, end_idx, body_end, stub) in entries:
    # Copy any lines between last processed and this entry's head verbatim
    new_lines.extend(lines[last_processed + 1 : head_idx])

    body_text = "\n".join(lines[head_idx + 1 : body_end])

    # Check if **Short:** already present in this entry's body
    if re.search(r"^\*\*Short:\*\*", body_text, re.MULTILINE):
        new_lines.extend(lines[head_idx:end_idx])
        skipped_existing += 1
        last_processed = end_idx - 1
        continue

    category, wc = categorize(body_text)
    skipped_categories[category] = skipped_categories.get(category, 0) + 1

    # Insert: heading, blank line, **Short:** [TBD: <category>], then existing body
    new_lines.append(lines[head_idx])  # the ### heading
    # Find first non-blank line of body to decide spacing
    body_start_in_orig = head_idx + 1
    while body_start_in_orig < body_end and lines[body_start_in_orig].strip() == "":
        body_start_in_orig += 1
    # Emit blank + Short line + blank, then the rest of the entry from first non-blank body line
    new_lines.append("")
    new_lines.append(f"**Short:** [TBD: {category}]")
    new_lines.append("")
    new_lines.extend(lines[body_start_in_orig:end_idx])
    inserted += 1
    last_processed = end_idx - 1

# Append anything after the last entry
new_lines.extend(lines[last_processed + 1 :])

new_text = "\n".join(new_lines)

# Summary
print(f"\nCategorization summary:")
for cat in ("Citation", "Citation+Context", "Mini-essay", "Verification"):
    n = skipped_categories.get(cat, 0)
    print(f"  {cat:18s}  {n:4d}")
print(f"\nInserted: {inserted}")
print(f"Skipped (already has Short field): {skipped_existing}")
print(f"\nNet line delta: {len(new_lines) - len(lines):+d}")

if DRY_RUN:
    print("\n[DRY RUN — no write]")
    # Preview first 3 entries' new state
    for k in range(min(3, len(entries))):
        head_idx, end_idx, body_end, stub = entries[k]
        # Find the entry in new_lines (search by stub heading)
        for ni, line in enumerate(new_lines):
            if line == f"### `{stub}`":
                print(f"\n--- Preview {k+1}: {stub} ---")
                print("\n".join(new_lines[ni : ni + 8]))
                break
else:
    ENDNOTES.write_text(new_text)
    print(f"\nWrote: {ENDNOTES}")

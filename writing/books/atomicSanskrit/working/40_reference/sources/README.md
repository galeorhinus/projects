# Atomic Sanskrit Source Records

This directory preserves the reproducible digital evidence behind manuscript
endnotes. It is working material and is never included in the book or the
Source and Reference Companion.

## Architecture

- `as_source_registry.md` is the tracked catalogue of every digital source.
- `archive/` holds source files when retaining a copy is appropriate.
- Each endnote may contain a hidden `SOURCE-RECORDS` block that points to one
  or more registry IDs and records the exact page, mantra, sutra, table, query,
  or image used for that endnote.

The registry describes a source once. The hidden endnote block records how a
particular note used that source. Reader-facing citations remain in the normal
endnote prose.

## Hidden Endnote Block

Place the block immediately after the endnote heading, after `**Deployments:**`,
or at the end of the relevant endnote. Keeping it near the heading makes a
large backfilled apparatus easier to scan; all three positions build the same:

```markdown
<!-- SOURCE-RECORDS
- vedaweb-zurich-v3 | lemma query: adabdha-; 48 rows; dabdha-: 0 rows
- hale-asura-1986 | p. 24
-->
```

The IDs must match headings in `as_source_registry.md`. The text after `|` is
note-specific verification detail. `build_book.py` removes the entire block
before producing full or short endnotes. The explicit removal is the guarantee;
the system does not depend only on Pandoc's treatment of HTML comments.

## Archive Layout

Create source-specific folders only as needed:

```text
archive/
  documents/<source-id>/
  images/<source-id>/
  datasets/<source-id>/
  web/<source-id>/
```

Use the source ID in every path. Preserve the downloaded original unchanged.
Derived crops, page renders, or annotations should have separate filenames.

Examples:

```text
archive/documents/suryakanta-rktantram-1933/original.pdf
archive/images/suryakanta-rktantram-1933/page-0054-asurasya.png
archive/datasets/vedaweb-zurich-v3/vedaweb_zurich.xlsx
archive/web/ashtadhyayi-1-1-9/page.html
```

## What to Retain

- **Public-domain or openly licensed documents:** archive the original file.
- **Datasets:** archive the exact version used and record its checksum.
- **Web pages:** retain the exact URL and access date; save HTML, PDF, or a
  full-page image when the page is unstable or central to the claim.
- **Images and screenshots:** keep a full page or full screen as the evidence
  record. A crop may accompany it for convenience but must not replace it.
- **Modern copyrighted books:** record the edition, page, URL or library
  record, and the verification finding. Do not add an unauthorized complete
  copy to the repository. A narrowly necessary page image may be retained as
  private research evidence when lawfully obtained.
- **Physical books:** record the edition and page. A URL is not required when
  no digital source was consulted.

## File Integrity

For downloaded documents and datasets, record SHA-256 in the registry. Retain
an MD5 supplied by the publisher or repository as additional metadata, not as
the sole local integrity check.

Do not overwrite an archived source with a newer version. Give the newer
version a distinct source ID or versioned filename.

## Existing Material

`working/40_reference/source_material/source_cache/` predates this system.
Leave it in place for now. Move or register its contents when an associated
endnote is audited rather than performing an unverified bulk migration.

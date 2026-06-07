"""Lineage helper for the figures/ convention.

Promote a `from-*.svg` stage variant to its canonical `<base>.svg`,
inject the lineage XML comment, and verify or list lineages in a
chapter folder.  See `figures/_shared/README.md` for the convention.

Usage:
    python3 -m _shared.lineage promote <source-from-*.svg> [--date YYYY-MM-DD]
    python3 -m _shared.lineage list   [<dir>]
    python3 -m _shared.lineage verify <canonical-svg>

Examples:
    # After Claude Design returns the refined version, save it as
    # figures/adivadya/hotzones_panels.from-py-cd.svg, then:
    python3 -m _shared.lineage promote \\
        figures/adivadya/hotzones_panels.from-py-cd.svg

    # See lineage status of every figure in a chapter folder:
    python3 -m _shared.lineage list figures/adivadya/

    # Confirm hotzones_panels.svg still matches the source it claims:
    python3 -m _shared.lineage verify figures/adivadya/hotzones_panels.svg
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

# <base>.from-<chain>.svg ; chain is one or more tokens joined by hyphens.
FROM_RE = re.compile(r"^(?P<base>.+)\.from-(?P<chain>[a-zA-Z0-9-]+)\.svg$")

# Match the lineage XML comment we inject into canonicals.
LINEAGE_COMMENT_RE = re.compile(
    r"<!--\s*lineage:\s*(?P<chain>[^\n]+)\n"
    r"\s*canonical-source:\s*(?P<source>[^\n]+)\n"
    r"\s*updated:\s*(?P<date>[\d-]+)\s*-->\n?",
    re.MULTILINE,
)


def parse_from_filename(path: Path) -> tuple[str, str]:
    """Return (<base>, <chain-arrowed>) for a `<base>.from-<chain>.svg` path."""
    m = FROM_RE.match(path.name)
    if not m:
        raise ValueError(
            f"Not a from-*.svg filename: {path.name!r} "
            f"(expected pattern '<base>.from-<chain>.svg')"
        )
    base = m.group("base")
    chain_arrowed = m.group("chain").replace("-", " → ")
    return base, chain_arrowed


def inject_lineage_comment(content: str, lineage_chain: str,
                           source_filename: str, date: str) -> str:
    """Return `content` with the lineage comment inserted after the XML
    declaration (or at the very top, if no declaration is present).
    Replaces any existing lineage comment in the same position."""
    comment = (
        f"<!-- lineage: {lineage_chain}\n"
        f"     canonical-source: {source_filename}\n"
        f"     updated: {date} -->\n"
    )
    if content.startswith("<?xml"):
        nl = content.index("\n") + 1
        rest = content[nl:]
        existing = LINEAGE_COMMENT_RE.match(rest)
        if existing:
            rest = rest[existing.end():]
        return content[:nl] + comment + rest
    existing = LINEAGE_COMMENT_RE.match(content)
    if existing:
        content = content[existing.end():]
    return comment + content


def promote(source: Path, date: str | None = None) -> Path:
    """Copy `source` (a from-*.svg) to its sibling <base>.svg, injecting
    the lineage XML comment.  Returns the canonical path written."""
    if not source.exists():
        raise FileNotFoundError(f"Source not found: {source}")
    base, chain = parse_from_filename(source)
    if date is None:
        date = datetime.date.today().isoformat()
    canonical = source.parent / f"{base}.svg"
    content = source.read_text(encoding="utf-8")
    new_content = inject_lineage_comment(content, chain, source.name, date)
    canonical.write_text(new_content, encoding="utf-8")
    return canonical


def list_canonicals(directory: Path) -> None:
    """Print a table of every <base>.svg in `directory` with its lineage."""
    rows: list[tuple[str, str, str, str]] = []
    for svg in sorted(directory.glob("*.svg")):
        if FROM_RE.match(svg.name):
            continue  # skip from-* stage variants
        content = svg.read_text(encoding="utf-8")
        m = LINEAGE_COMMENT_RE.search(content)
        if m:
            rows.append((svg.name, m.group("chain").strip(),
                         m.group("source").strip(), m.group("date").strip()))
        else:
            rows.append((svg.name, "(no lineage comment)", "?", "?"))
    if not rows:
        print(f"  (no canonical SVGs found in {directory})")
        return
    name_w = max(len(r[0]) for r in rows)
    chain_w = max(len(r[1]) for r in rows)
    print(f"  {'canonical'.ljust(name_w)}  {'lineage'.ljust(chain_w)}  source  (updated)")
    print(f"  {'-' * name_w}  {'-' * chain_w}  ------  ---------")
    for name, chain, source, date in rows:
        print(f"  {name.ljust(name_w)}  {chain.ljust(chain_w)}  {source}  ({date})")


def verify(canonical: Path) -> bool:
    """Check that `canonical`'s recorded canonical-source exists and that
    stripping the lineage comment from the canonical yields content
    bit-identical to that source.  Returns True iff both hold."""
    content = canonical.read_text(encoding="utf-8")
    m = LINEAGE_COMMENT_RE.search(content)
    if not m:
        print(f"  ✗ {canonical.name}: no lineage comment present")
        return False
    source_name = m.group("source").strip()
    source_path = canonical.parent / source_name
    if not source_path.exists():
        print(f"  ✗ {canonical.name}: recorded source {source_name!r} not found in {canonical.parent}")
        return False
    src_content = source_path.read_text(encoding="utf-8")
    stripped = LINEAGE_COMMENT_RE.sub("", content, count=1)
    if stripped == src_content:
        print(f"  ✓ {canonical.name}: matches {source_name}")
        return True
    print(f"  ⚠ {canonical.name}: content differs from {source_name}")
    return False


def _cli() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_promote = sub.add_parser("promote",
                               help="Inject lineage + write canonical")
    p_promote.add_argument("source", type=Path,
                           help="path to a <base>.from-<chain>.svg file")
    p_promote.add_argument("--date", default=None,
                           help="override the updated date (YYYY-MM-DD); "
                                "defaults to today")

    p_list = sub.add_parser("list",
                            help="Show lineage of every canonical in a folder")
    p_list.add_argument("directory", type=Path, nargs="?", default=Path("."),
                        help="chapter folder (default: cwd)")

    p_verify = sub.add_parser("verify",
                              help="Check a canonical against its recorded source")
    p_verify.add_argument("canonical", type=Path,
                          help="path to a canonical <base>.svg")

    args = parser.parse_args()
    if args.cmd == "promote":
        result = promote(args.source, args.date)
        print(f"  → wrote {result}")
        return 0
    if args.cmd == "list":
        list_canonicals(args.directory)
        return 0
    if args.cmd == "verify":
        return 0 if verify(args.canonical) else 1
    return 2  # unreachable


if __name__ == "__main__":
    sys.exit(_cli())

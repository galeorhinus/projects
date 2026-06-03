#!/usr/bin/env python3
"""Audit effective print font sizes for referenced SVG figures.

This script is intentionally read-only for manuscript and figure sources. It
reads markdown image references, maps current percentage widths to an assumed
print text width, inspects live SVG font-size declarations, and writes a
markdown audit report.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


BOOK_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = BOOK_DIR / "working" / "figure_font_size_audit.md"

IMAGE_RE = re.compile(
    r"!\[(?P<caption>[^\]]*)\]"
    r"\((?P<path>figures/build/[^)\s]+\.svg)\)"
    r"\{(?P<attrs>[^}]*)\}"
)
WIDTH_RE = re.compile(r"\bwidth=(?P<width>[^\s}]+)")
ID_RE = re.compile(r"#(?P<id>[-A-Za-z0-9_:]+)")
VIEWBOX_RE = re.compile(
    r"""viewBox\s*=\s*["']\s*
    (?P<x>-?\d+(?:\.\d+)?)\s+
    (?P<y>-?\d+(?:\.\d+)?)\s+
    (?P<w>\d+(?:\.\d+)?)\s+
    (?P<h>\d+(?:\.\d+)?)\s*["']""",
    re.VERBOSE,
)
SVG_WIDTH_RE = re.compile(r"""<svg[^>]*\bwidth=["'](?P<width>[^"']+)["']""")
FONT_SIZE_RE = re.compile(
    r"""(?:font-size\s*[:=]\s*["']?)(?P<size>\d+(?:\.\d+)?)(?P<unit>px|pt|em|rem)?""",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class FigureRef:
    source: Path
    line: int
    caption: str
    path: Path
    fig_id: str
    width_raw: str


@dataclass(frozen=True)
class SvgInfo:
    exists: bool
    viewbox_width: float | None
    viewbox_height: float | None
    font_sizes: tuple[float, ...]
    outlined_text: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--textwidth",
        type=float,
        default=4.5,
        help="Assumed 100%% text width in inches. Default: 4.5 (trade layout).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Markdown report path. Default: {DEFAULT_OUTPUT.relative_to(BOOK_DIR)}",
    )
    parser.add_argument(
        "--target-min",
        type=float,
        default=6.0,
        help="Minimum acceptable effective print font size in points. Default: 6.0.",
    )
    parser.add_argument(
        "--target-comfort",
        type=float,
        default=7.0,
        help="Comfortable effective print font size in points. Default: 7.0.",
    )
    return parser.parse_args()


def manuscript_files() -> list[Path]:
    files = sorted(BOOK_DIR.glob("as_*.md"))
    if (BOOK_DIR / "as_endnotes.md").exists():
        files.append(BOOK_DIR / "as_endnotes.md")
    return files


def find_refs() -> list[FigureRef]:
    refs: list[FigureRef] = []
    for source in manuscript_files():
        text = source.read_text(encoding="utf-8")
        line_starts = [0]
        for match in re.finditer(r"\n", text):
            line_starts.append(match.end())
        for match in IMAGE_RE.finditer(text):
            attrs = match.group("attrs")
            width_match = WIDTH_RE.search(attrs)
            id_match = ID_RE.search(attrs)
            line = 1 + sum(1 for start in line_starts if start <= match.start()) - 1
            refs.append(
                FigureRef(
                    source=source,
                    line=line,
                    caption=" ".join(match.group("caption").split()),
                    path=BOOK_DIR / match.group("path"),
                    fig_id=id_match.group("id") if id_match else "",
                    width_raw=width_match.group("width") if width_match else "",
                )
            )
    return refs


def parse_svg_dimension(raw: str) -> float | None:
    value = raw.strip()
    match = re.match(r"(?P<num>\d+(?:\.\d+)?)(?P<unit>px|pt|in|cm|mm)?", value)
    if not match:
        return None
    num = float(match.group("num"))
    unit = match.group("unit") or "px"
    if unit == "px":
        return num
    if unit == "pt":
        return num * 96.0 / 72.0
    if unit == "in":
        return num * 96.0
    if unit == "cm":
        return num * 96.0 / 2.54
    if unit == "mm":
        return num * 96.0 / 25.4
    return None


def parse_font_size(match: re.Match[str]) -> float | None:
    size = float(match.group("size"))
    unit = match.group("unit") or "px"
    if unit == "px":
        return size
    if unit == "pt":
        return size * 96.0 / 72.0
    if unit in {"em", "rem"}:
        return size * 16.0
    return None


def inspect_svg(path: Path) -> SvgInfo:
    if not path.exists():
        return SvgInfo(False, None, None, (), False)
    text = path.read_text(encoding="utf-8", errors="replace")
    viewbox = VIEWBOX_RE.search(text)
    if viewbox:
        width = float(viewbox.group("w"))
        height = float(viewbox.group("h"))
    else:
        width_match = SVG_WIDTH_RE.search(text)
        width = parse_svg_dimension(width_match.group("width")) if width_match else None
        height = None

    sizes = []
    for match in FONT_SIZE_RE.finditer(text):
        parsed = parse_font_size(match)
        if parsed is not None and parsed > 0:
            sizes.append(parsed)
    font_sizes = tuple(sorted(set(round(size, 3) for size in sizes)))
    outlined_text = not font_sizes and (
        "Charter-" in text
        or "DejaVuSans-" in text
        or "NotoSans" in text
        or "<glyph" in text
        or "<use " in text
    )
    return SvgInfo(True, width, height, font_sizes, outlined_text)


def proposed_width_inches(width_raw: str, textwidth: float) -> float | None:
    width = width_raw.strip()
    if not width:
        return None
    if width.endswith("%"):
        try:
            return textwidth * float(width[:-1]) / 100.0
        except ValueError:
            return None
    if width.endswith("in"):
        try:
            return float(width[:-2])
        except ValueError:
            return None
    if width.endswith("pt"):
        try:
            return float(width[:-2]) / 72.0
        except ValueError:
            return None
    return None


def effective_sizes_pt(info: SvgInfo, width_in: float | None) -> list[float]:
    if width_in is None or not info.viewbox_width or not info.font_sizes:
        return []
    scale = width_in * 72.0 / info.viewbox_width
    return [round(size * scale, 2) for size in info.font_sizes]


def required_width_inches(info: SvgInfo, target_pt: float) -> float | None:
    if not info.viewbox_width or not info.font_sizes:
        return None
    smallest_svg_size = min(info.font_sizes)
    if smallest_svg_size <= 0:
        return None
    return target_pt * info.viewbox_width / (smallest_svg_size * 72.0)


def fmt_range(values: list[float]) -> str:
    if not values:
        return "—"
    unique = sorted(set(values))
    if len(unique) == 1:
        return f"{unique[0]:.2f}"
    return f"{unique[0]:.2f}–{unique[-1]:.2f}"


def flag_for(values: list[float], info: SvgInfo) -> str:
    if not info.exists:
        return "missing SVG"
    if not info.font_sizes:
        return "outlined/path text" if info.outlined_text else "no live SVG text"
    if not values:
        return "cannot scale"
    smallest = min(values)
    if smallest < 6:
        return "contains <6pt text"
    if smallest < 7:
        return "contains 6-7pt text"
    return ""


def fmt_inches(value: float | None) -> str:
    return f"{value:.2f} in" if value is not None else "—"


def width_verdict(
    info: SvgInfo,
    width_in: float | None,
    effective: list[float],
    textwidth: float,
    target_min: float,
) -> str:
    if not info.exists:
        return "missing SVG"
    if not info.font_sizes:
        return "manual visual check"
    if width_in is None or not effective:
        return "cannot scale"
    if min(effective) >= target_min:
        return "current width clears target"
    required = required_width_inches(info, target_min)
    if required is not None and required <= textwidth:
        return "width-only fix possible"
    return "needs redraw or font-size bump"


def short_caption(caption: str, max_len: int = 72) -> str:
    if len(caption) <= max_len:
        return caption
    return caption[: max_len - 1].rstrip() + "…"


def render_report(
    refs: list[FigureRef],
    textwidth: float,
    target_min: float,
    target_comfort: float,
) -> str:
    svg_cache = {ref.path: inspect_svg(ref.path) for ref in {r for r in refs}}
    refs_by_path: dict[Path, list[FigureRef]] = defaultdict(list)
    for ref in refs:
        refs_by_path[ref.path].append(ref)

    rows = []
    flags = Counter()
    verdicts = Counter()
    measurable = 0
    for ref in refs:
        info = svg_cache[ref.path]
        width_in = proposed_width_inches(ref.width_raw, textwidth)
        eff = effective_sizes_pt(info, width_in)
        flag = flag_for(eff, info)
        verdict = width_verdict(info, width_in, eff, textwidth, target_min)
        if flag:
            flags[flag] += 1
        verdicts[verdict] += 1
        if eff:
            measurable += 1
        rows.append((ref, info, width_in, eff, flag, verdict))

    unique_paths = sorted(refs_by_path)
    missing = sum(1 for path in unique_paths if not svg_cache[path].exists)
    outlined_unique = sum(
        1
        for path in unique_paths
        if svg_cache[path].exists and not svg_cache[path].font_sizes and svg_cache[path].outlined_text
    )
    live_unique = sum(1 for path in unique_paths if svg_cache[path].font_sizes)

    out: list[str] = []
    out.append("# Figure Font-Size Audit")
    out.append("")
    out.append("Audit and width-feasibility pass only. No manuscript files or figure files were changed.")
    out.append("")
    out.append("## Assumptions")
    out.append("")
    out.append(f"- Layout basis: `trade` text width assumed as **{textwidth:.2f} in**.")
    out.append(f"- Minimum target for print labels: **{target_min:.1f} pt**.")
    out.append(f"- Comfortable target for print labels: **{target_comfort:.1f} pt**.")
    out.append("- Current markdown percentage widths are converted against that text width.")
    out.append("- Effective font size is calculated as `svg_font_size * proposed_width_in * 72 / viewBox_width`.")
    out.append("- The audit measures only live SVG text with `font-size` declarations.")
    out.append("- Figures whose text has been converted to paths are marked as outlined/path text.")
    out.append("")
    out.append("## Summary")
    out.append("")
    out.append(f"- SVG figure references scanned: **{len(refs)}**")
    out.append(f"- Unique SVG files referenced: **{len(unique_paths)}**")
    out.append(f"- Unique SVGs with live measurable text: **{live_unique}**")
    out.append(f"- Unique SVGs with outlined/path text: **{outlined_unique}**")
    out.append(f"- Missing SVG files: **{missing}**")
    out.append(f"- References with measurable effective font sizes: **{measurable}**")
    if flags:
        out.append("")
        out.append("Flags:")
        for key, count in sorted(flags.items()):
            out.append(f"- {key}: {count}")
    if verdicts:
        out.append("")
        out.append("Width-only feasibility:")
        for key, count in sorted(verdicts.items()):
            out.append(f"- {key}: {count}")
    out.append("")
    out.append("## Audit Table")
    out.append("")
    out.append(
        "| Figure | Source | Current width | Proposed width | SVG viewBox | SVG font sizes | Effective print sizes | Flag |"
    )
    out.append("|---|---:|---:|---:|---:|---:|---:|---|")
    for ref, info, width_in, eff, flag, _verdict in rows:
        source = f"`{ref.source.relative_to(BOOK_DIR)}:{ref.line}`"
        fig = f"`{ref.fig_id or ref.path.stem}`"
        if not ref.fig_id:
            fig += f"<br>{short_caption(ref.caption)}"
        proposed = f"{width_in:.2f} in" if width_in is not None else "—"
        viewbox = (
            f"{info.viewbox_width:.0f}×{info.viewbox_height:.0f}"
            if info.viewbox_width and info.viewbox_height
            else "—"
        )
        svg_sizes = fmt_range(list(info.font_sizes))
        effective = fmt_range(eff)
        out.append(
            f"| {fig} | {source} | `{ref.width_raw or '—'}` | {proposed} | {viewbox} | {svg_sizes} | {effective} pt | {flag} |"
        )

    out.append("")
    out.append("## Width-Only Feasibility")
    out.append("")
    out.append(
        "| Figure | Current proposed width | Smallest current print text | Width for target | Width for comfort | Verdict |"
    )
    out.append("|---|---:|---:|---:|---:|---|")
    for ref, info, width_in, eff, _flag, verdict in rows:
        fig = f"`{ref.fig_id or ref.path.stem}`"
        smallest = f"{min(eff):.2f} pt" if eff else "—"
        req_min = required_width_inches(info, target_min)
        req_comfort = required_width_inches(info, target_comfort)
        out.append(
            f"| {fig} | {fmt_inches(width_in)} | {smallest} | {fmt_inches(req_min)} | {fmt_inches(req_comfort)} | {verdict} |"
        )

    out.append("")
    out.append("## Duplicate Figure References")
    out.append("")
    duplicate_paths = {path: refs for path, refs in refs_by_path.items() if len(refs) > 1}
    if not duplicate_paths:
        out.append("No referenced SVG appears more than once.")
    else:
        for path, path_refs in sorted(duplicate_paths.items()):
            rel = path.relative_to(BOOK_DIR)
            refs_text = ", ".join(
                f"`{ref.source.name}:{ref.line}` (`{ref.width_raw}`)" for ref in path_refs
            )
            out.append(f"- `{rel}`: {refs_text}")

    out.append("")
    out.append("## Next Pass")
    out.append("")
    out.append("1. Review figures marked `needs redraw or font-size bump`.")
    out.append("2. For figures marked `width-only fix possible`, decide whether the wider figure fits the page.")
    out.append("3. Convert selected markdown width attributes from percentages to inches.")
    out.append("4. Re-render figures where the required width exceeds the text block.")
    out.append("")
    return "\n".join(out)


def main() -> int:
    args = parse_args()
    refs = find_refs()
    report = render_report(refs, args.textwidth, args.target_min, args.target_comfort)
    output = args.output if args.output.is_absolute() else BOOK_DIR / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(output.relative_to(BOOK_DIR))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

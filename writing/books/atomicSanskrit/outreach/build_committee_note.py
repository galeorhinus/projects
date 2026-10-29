"""Build the October 7 committee note as an A4 PDF."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build_book import (  # noqa: E402
    mainfont_cli_args,
    render_devanagari_preamble,
    wrap_scripts_for_latex,
)

STEM = "sanskrit_language_system_committee_note_oct7"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--short", action="store_true", help="Build the three-page committee note")
    args = parser.parse_args()
    stem = STEM + ("_short" if args.short else "")
    source = ROOT / "outreach/strategy" / f"{stem}.md"
    work = ROOT / "tmp/pdfs" / stem
    output = ROOT / "output/pdf" / f"{stem}.a4.pdf"
    work.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text()
    parsed = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "json"],
        input=wrap_scripts_for_latex(text), text=True,
        capture_output=True, check=True,
    )
    doc = json.loads(parsed.stdout)
    blocks = []
    for i, block in enumerate(doc["blocks"]):
        if i == 1 and block["t"] == "Header":
            block = {"t": "Para", "c": [{"t": "Emph", "c": block["c"][2]}]}
        if block["t"] == "Header":
            page_starts = {"four-possible-projects", "needs"} if args.short else {"explanatory-examples"}
            if block["c"][1][0] in page_starts:
                blocks.append({"t": "RawBlock", "c": ["latex", r"\clearpage"]})
        if block["t"] == "Table":
            specs = block["c"][2]
            widths = {2: (0.24, 0.76), 3: (0.18, 0.37, 0.45)}[len(specs)]
            for spec, width in zip(specs, widths):
                spec[1] = {"t": "ColWidth", "c": width}
        blocks.append(block)
    doc["blocks"] = blocks
    ast = work / "note.json"
    ast.write_text(json.dumps(doc, ensure_ascii=False))
    layout = work / "layout.tex"
    layout_text = r"""
\usepackage{fancyhdr}
\usepackage{ragged2e}
\makeatletter
\renewcommand{\section}{\@startsection{section}{1}{0pt}{-1pt}{8pt}{\fontsize{25}{29}\selectfont\bfseries\raggedright}}
\renewcommand{\subsection}{\@startsection{subsection}{2}{0pt}{-15pt}{7pt}{\fontsize{16}{20}\selectfont\bfseries\raggedright}}
\renewcommand{\subsubsection}{\@startsection{subsubsection}{3}{0pt}{-12pt}{6pt}{\fontsize{13}{17}\selectfont\bfseries\raggedright}}
\makeatother
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt plus 1pt}
\setlength{\emergencystretch}{3em}
\setlength{\tabcolsep}{5pt}
\renewcommand{\arraystretch}{1.12}
\widowpenalty=10000
\clubpenalty=10000
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[L]{\fontsize{8}{10}\selectfont Sanskrit as a Language System | Discussion draft}
\fancyfoot[R]{\fontsize{9}{11}\selectfont\thepage}
\setlength{\footskip}{11mm}
\raggedbottom
\AtBeginDocument{\RaggedRight\hypersetup{pdfauthor={Parag Tope},pdftitle={Sanskrit as a Language System - Committee Note, 7 October 2026}}}
"""
    layout.write_text(layout_text)
    metadata = ROOT / "as_book.yaml"
    tex = work / "note.tex"
    subprocess.run([
        "pandoc", str(ast), "-f", "json", "-t", "latex", "--standalone",
        "-V", "documentclass=article", "-V", "fontsize=12pt",
        "-V", "geometry=a4paper,left=23mm,right=23mm,top=21mm,bottom=23mm",
        "-V", f"linestretch={1.0 if args.short else 1.10}", "-V", "colorlinks=true",
        "-V", "urlcolor=teal", "-V", "linkcolor=black",
        "-H", str(render_devanagari_preamble(metadata)), "-H", str(layout),
        *mainfont_cli_args(metadata), "-o", str(tex),
    ], cwd=ROOT, check=True)
    for _ in range(2):
        run = subprocess.run([
            "xelatex", "-interaction=nonstopmode", "-halt-on-error",
            f"-output-directory={work}", str(tex),
        ], cwd=ROOT, text=True, capture_output=True)
        if run.returncode:
            raise RuntimeError(run.stdout[-7000:])
    log = (work / "note.log").read_text()
    problems = [line for line in log.splitlines()
                if "Missing character:" in line or "Overfull" in line]
    if problems:
        raise RuntimeError("Layout or font warnings:\n" + "\n".join(problems))
    output.write_bytes((work / "note.pdf").read_bytes())
    print(output)


if __name__ == "__main__":
    main()

"""Build the shorter Penguin proposal for A4 submission or phone reading."""

import argparse
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layout", choices=("a4", "phone"), default="a4")
    args = parser.parse_args()
    source = ROOT / "outreach/atomic_sanskrit_penguin_proposal.md"
    work = ROOT / "tmp/pdfs/penguin_proposal" / args.layout
    output = ROOT / f"output/pdf/atomic_sanskrit_penguin_proposal.{args.layout}.pdf"
    work.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    wrapped = work / "proposal.md"
    wrapped.write_text(wrap_scripts_for_latex(source.read_text()))
    layout = work / "layout.tex"
    preamble = r"""
\usepackage{fancyhdr}
\makeatletter
\renewcommand{\section}{\@startsection{section}{1}{0pt}{-1pt}{6pt}{\fontsize{24}{28}\selectfont\bfseries}}
\renewcommand{\subsection}{\@startsection{subsection}{2}{0pt}{-16pt}{7pt}{\fontsize{15}{18}\selectfont\bfseries\raggedright}}
\renewcommand{\subsubsection}{\@startsection{subsubsection}{3}{0pt}{-14pt}{6pt}{\fontsize{13}{16}\selectfont\bfseries\raggedright}}
\makeatother
\setlength{\parindent}{0pt}
\setlength{\parskip}{7pt plus 1pt}
\setlength{\emergencystretch}{2em}
\widowpenalty=10000
\clubpenalty=10000
\brokenpenalty=10000
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\fancyfoot[L]{\footnotesize Atomic Sanskrit | Book Proposal}
\fancyfoot[R]{\footnotesize\thepage}
\setlength{\footskip}{12mm}
\raggedbottom
\AtBeginDocument{\hypersetup{pdftitle={Atomic Sanskrit: The Architecture of Sanatan - Book Proposal},pdfauthor={Parag Tope}}}
"""
    geometry = "a4paper,margin=25mm"
    if args.layout == "phone":
        geometry = "paperwidth=108mm,paperheight=192mm,left=9mm,right=9mm,top=10mm,bottom=13mm"
        preamble += r"""
\usepackage{ragged2e}
\makeatletter
\renewcommand{\section}{\@startsection{section}{1}{0pt}{-1pt}{6pt}{\fontsize{22}{26}\selectfont\bfseries\raggedright}}
\renewcommand{\subsection}{\@startsection{subsection}{2}{0pt}{-14pt}{7pt}{\fontsize{17}{20}\selectfont\bfseries\raggedright}}
\renewcommand{\subsubsection}{\@startsection{subsubsection}{3}{0pt}{-12pt}{6pt}{\fontsize{15}{18}\selectfont\bfseries\raggedright}}
\makeatother
\setlength{\footskip}{8mm}
\setlength{\parskip}{6pt plus 1pt}
\fancyfoot[L]{\fontsize{8}{10}\selectfont Atomic Sanskrit | Proposal}
\fancyfoot[R]{\fontsize{9}{11}\selectfont\thepage}
\AtBeginDocument{\fontsize{13}{16}\selectfont\RaggedRight}
"""
    layout.write_text(preamble)
    metadata = ROOT / "as_book.yaml"
    command = [
        "pandoc", str(wrapped), "--standalone", "--pdf-engine=xelatex",
        "-V", "documentclass=article", "-V", "fontsize=12pt",
        "-V", f"geometry={geometry}", "-V", "linestretch=1.15",
        "-H", str(render_devanagari_preamble(metadata)), "-H", str(layout),
        *mainfont_cli_args(metadata), "-o", str(output),
    ]
    subprocess.run(command, cwd=ROOT, check=True)
    print(output)


if __name__ == "__main__":
    main()

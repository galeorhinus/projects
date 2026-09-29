"""Build the shorter Penguin proposal for A4 submission or phone reading."""

import argparse
from copy import deepcopy
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build_book import (  # noqa: E402
    mainfont_cli_args,
    render_devanagari_preamble,
    wrap_scripts_for_latex,
)


def proposal_branding(source, work, phone):
    """Use the cover artwork without changing the proposal's Markdown source."""
    inkscape = shutil.which("inkscape") or "/Applications/Inkscape.app/Contents/MacOS/inkscape"
    ns = "http://www.w3.org/2000/svg"
    cover = ET.parse(ROOT / "cover/manuscript/as-book-a5.svg").getroot()
    mark = ET.Element(f"{{{ns}}}svg", {"viewBox": "526 108 131 128"})
    for style in cover.iter(f"{{{ns}}}style"):
        mark.append(deepcopy(style))
    artwork = deepcopy(cover.find(".//*[@id='engineering_1_']"))
    artwork.attrib.pop("transform", None)
    mark.append(artwork)
    mark_source = work / "engineering.svg"
    ET.ElementTree(mark).write(mark_source, encoding="utf-8", xml_declaration=True)
    names = ("Distributed", "Radiant", "Calibrant", "Fractal")
    assets = {"engineering": mark_source}
    assets.update({name: ROOT / f"figures/_shared/icons/ic-{name.lower()}.svg" for name in names})
    pdfs = {}
    for name, path in assets.items():
        destination = work / f"{name.lower()}.pdf"
        subprocess.run([inkscape, str(path), "--export-text-to-path",
                        f"--export-filename={destination}"], check=True, capture_output=True)
        pdfs[name] = destination.as_posix()

    title_block, separator, remainder = source.partition("**Book proposal")
    assert separator, "Missing proposal submission heading"
    headings = [line for line in title_block.splitlines() if line.startswith("#")]
    assert len(headings) == 2, "Expected title and subtitle before submission details"
    title, subtitle = (line.lstrip("# ").rstrip(":") for line in headings)
    title_size, subtitle_size = (23, 14) if phone else (30, 17)
    mark_mm, icon_mm, label_pt = (11, 9, 8.5) if phone else (14, 14, 10)
    band_mm = 90 if phone else 118
    cells = []
    for name in names:
        cells.append(r"\makebox[0.25\linewidth][c]{\shortstack[c]{"
                     + f"\\includegraphics[width={icon_mm}mm]{{{pdfs[name]}}}"
                     + rf"\\[1pt]{{\fontsize{{{label_pt}}}{{12}}\selectfont\bfseries {name.upper()}}}"
                     + "}}")
    header = rf"""```{{=latex}}
\begingroup
\setlength{{\parskip}}{{0pt}}
\centering
\newsavebox{{\proposalTitle}}
\sbox{{\proposalTitle}}{{\fontsize{{{title_size}}}{{{title_size + 4}}}\selectfont\bfseries {title}}}
\noindent\begin{{minipage}}[c]{{{mark_mm}mm}}
\includegraphics[width=\linewidth]{{{pdfs['engineering']}}}
\end{{minipage}}\hspace{{3mm}}%
\begin{{minipage}}[c]{{\wd\proposalTitle}}
\usebox{{\proposalTitle}}
\end{{minipage}}
\par\vspace{{8pt}}
{{\fontsize{{{subtitle_size}}}{{{subtitle_size + 4}}}\selectfont\bfseries {subtitle}\par}}
\vspace{{9pt}}
\begin{{minipage}}{{{band_mm}mm}}
{{\color[HTML]{{8A7C64}}\hrule height 0.4pt}}
\vspace{{8pt}}
\noindent {''.join(cells)}
\end{{minipage}}
\par\vspace{{10pt}}
\endgroup
```

"""
    return header + separator + remainder


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
    branded = proposal_branding(source.read_text(), work, args.layout == "phone")
    wrapped.write_text(wrap_scripts_for_latex(branded))
    layout = work / "layout.tex"
    preamble = r"""
\usepackage{fancyhdr}
\usepackage{graphicx}
\usepackage{xcolor}
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

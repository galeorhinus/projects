"""Render the internal-discussion article in A4 and phone layouts."""

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

STEM = "muller_macdonell_dalrymple_heroic_erasure"


def article_document(source):
    """Collect repeated citations into endnotes and remove local-file links."""
    parsed = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "json"],
        input=wrap_scripts_for_latex(source), text=True,
        capture_output=True, check=True,
    )
    document = json.loads(parsed.stdout)
    notes = []
    numbers = {}

    def walk(node):
        if isinstance(node, list):
            return [walk(item) for item in node]
        if not isinstance(node, dict):
            return node
        if node.get("t") == "Note":
            key = json.dumps(node["c"], sort_keys=True)
            if key not in numbers:
                numbers[key] = len(notes) + 1
                notes.append(walk(node["c"]))
            number = numbers[key]
            return {"t": "Link", "c": [
                ["", [], []],
                [{"t": "Superscript", "c": [{"t": "Str", "c": str(number)}]}],
                [f"#reference-{number}", ""],
            ]}
        if node.get("t") == "Link" and node["c"][2][0].split("#")[0].endswith(".md"):
            return {"t": "Span", "c": [["", [], []], walk(node["c"][1])]}
        return {key: walk(value) for key, value in node.items()}

    document = walk(document)
    blocks = []
    inserted = False
    for block in document["blocks"]:
        if block.get("t") == "Header" and block["c"][1][0] == "references":
            blocks.append({"t": "RawBlock", "c": ["latex", "\\clearpage"]})
            blocks.append(block)
            blocks.append({"t": "RawBlock", "c": ["latex", "\\begingroup\\referencefont"]})
            items = [[{"t": "Div", "c": [[f"reference-{n}", [], []], note]}]
                     for n, note in enumerate(notes, 1)]
            blocks.append({"t": "OrderedList", "c": [
                [1, {"t": "Decimal"}, {"t": "Period"}], items,
            ]})
            blocks.append({"t": "RawBlock", "c": ["latex", "\\endgroup"]})
            inserted = True
        else:
            blocks.append(block)
    if not inserted:
        raise ValueError("Article needs a References heading")
    document["blocks"] = blocks
    return document


def build(document, layout):
    phone = layout == "phone"
    work = ROOT / "tmp/pdfs" / STEM / layout
    work.mkdir(parents=True, exist_ok=True)
    output = ROOT / "output/pdf" / f"{STEM}.{layout}.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    ast = work / "article.json"
    ast.write_text(json.dumps(document, ensure_ascii=False))
    preamble = work / "layout.tex"
    preamble.write_text(r"""
\usepackage{fancyhdr}
\usepackage{ragged2e}
\makeatletter
\renewcommand{\section}{\@startsection{section}{1}{0pt}{-1pt}{12pt}{\fontsize{22}{26}\selectfont\bfseries\raggedright}}
\renewcommand{\subsection}{\@startsection{subsection}{2}{0pt}{-14pt}{9pt}{\fontsize{16}{20}\selectfont\bfseries\raggedright}}
\makeatother
\setlength{\parindent}{0pt}
\setlength{\parskip}{7pt plus 1pt}
\setlength{\emergencystretch}{3em}
\widowpenalty=10000
\clubpenalty=10000
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[L]{\fontsize{8}{10}\selectfont Discussion draft | Not for publication}
\fancyfoot[R]{\fontsize{9}{11}\selectfont\thepage}
\setlength{\footskip}{10mm}
\raggedbottom
\newcommand{\referencefont}{\fontsize{10.5}{13}\selectfont\RaggedRight}
\AtBeginDocument{\hypersetup{pdfauthor={Parag Tope},pdftitle={What Do Max Muller, Arthur Macdonell, and William Dalrymple Have in Common?}}}
""" + (r"""
\makeatletter
\renewcommand{\section}{\@startsection{section}{1}{0pt}{-1pt}{10pt}{\fontsize{20}{24}\selectfont\bfseries\raggedright}}
\makeatother
\setlength{\footskip}{8mm}
\setlength{\parskip}{6pt plus 1pt}
\renewcommand{\referencefont}{\fontsize{11}{14}\selectfont\RaggedRight}
\AtBeginDocument{\fontsize{13}{16}\selectfont\RaggedRight}
""" if phone else ""))
    geometry = ("paperwidth=108mm,paperheight=192mm,left=9mm,right=9mm,top=10mm,bottom=13mm"
                if phone else "a4paper,margin=25mm")
    metadata = ROOT / "as_book.yaml"
    tex = work / "article.tex"
    subprocess.run([
        "pandoc", str(ast), "-f", "json", "-t", "latex", "--standalone",
        "-V", "documentclass=article", "-V", "fontsize=12pt",
        "-V", f"geometry={geometry}", "-V", "linestretch=1.15",
        "-H", str(render_devanagari_preamble(metadata)), "-H", str(preamble),
        *mainfont_cli_args(metadata), "-o", str(tex),
    ], cwd=ROOT, check=True)
    for _ in range(2):
        result = subprocess.run([
            "xelatex", "-interaction=nonstopmode", "-halt-on-error",
            f"-output-directory={work}", str(tex),
        ], cwd=ROOT, text=True, capture_output=True)
        if result.returncode:
            raise RuntimeError(result.stdout[-6000:])
    output.write_bytes((work / "article.pdf").read_bytes())
    print(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layout", choices=("a4", "phone", "both"), default="both")
    args = parser.parse_args()
    source = ROOT / "outreach/articles" / f"{STEM}.md"
    document = article_document(source.read_text())
    for layout in (("a4", "phone") if args.layout == "both" else (args.layout,)):
        build(document, layout)


if __name__ == "__main__":
    main()

"""Build an A4 overview followed by the review manuscript's complete contents."""

import argparse
from pathlib import Path
import subprocess
import sys

from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build_book import (  # noqa: E402
    mainfont_cli_args,
    render_devanagari_preamble,
    wrap_scripts_for_latex,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manuscript", type=Path,
        default=ROOT / "build/atomic_sanskrit.review-a4.short.pdf",
    )
    args = parser.parse_args()
    reader = PdfReader(args.manuscript)
    texts = []
    for page in reader.pages:
        texts.append((page.extract_text() or "").strip())
        if texts[-1].startswith("List of Figures\n"):
            break
    start = next(i for i, text in enumerate(texts) if text.startswith("Contents\n"))
    stop = next(i for i in range(start + 1, len(texts))
                if texts[i].startswith("List of Figures\n"))
    # Omit the book's blank verso after the contents, but keep all entries.
    while stop > start and not texts[stop - 1]:
        stop -= 1
    assert "About the Author" in texts[stop - 1], "Contents endpoint changed"

    work = ROOT / "tmp/pdfs/toc_packet"
    work.mkdir(parents=True, exist_ok=True)
    output = ROOT / "output/pdf/atomic_sanskrit_overview_and_contents.a4.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    source = (ROOT / "outreach/atomic_sanskrit_toc_overview.md").read_text()
    source = source.replace("# How the Book Is Organized\n", "", 1).strip()
    heading = """# Atomic Sanskrit
### The Architecture of Sanātan

Parag Tope | Overview and Detailed Contents

## How the Book Is Organized

"""
    markdown = work / "overview.md"
    markdown.write_text(wrap_scripts_for_latex(heading + source))
    layout = work / "layout.tex"
    layout.write_text(r"""
\usepackage{fancyhdr}
\makeatletter
\renewcommand{\section}{\@startsection{section}{1}{0pt}{-1pt}{3pt}{\fontsize{22}{25}\selectfont\bfseries}}
\renewcommand{\subsection}{\@startsection{subsection}{2}{0pt}{-7pt}{5pt}{\fontsize{13}{16}\selectfont\bfseries}}
\renewcommand{\subsubsection}{\@startsection{subsubsection}{3}{0pt}{-2pt}{4pt}{\fontsize{14}{17}\selectfont}}
\makeatother
\setlength{\parindent}{0pt}
\setlength{\parskip}{3pt}
\AtBeginDocument{\fontsize{11}{12.5}\selectfont}
\setlength{\emergencystretch}{2em}
\widowpenalty=10000
\clubpenalty=10000
\raggedbottom
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0.3pt}
\fancyfoot[L]{\footnotesize Atomic Sanskrit | Overview and Contents}
\fancyfoot[R]{\footnotesize\thepage}
\setlength{\footskip}{9mm}
""")
    intro_pdf = work / "overview.pdf"
    metadata = ROOT / "as_book.yaml"
    subprocess.run([
        "pandoc", str(markdown), "--standalone", "--pdf-engine=xelatex",
        "-V", "documentclass=article", "-V", "fontsize=11pt",
        "-V", "geometry=a4paper,left=18mm,right=18mm,top=16mm,bottom=17mm",
        "-V", "linestretch=1.0",
        "-H", str(render_devanagari_preamble(metadata)), "-H", str(layout),
        *mainfont_cli_args(metadata), "-o", str(intro_pdf),
    ], cwd=ROOT, check=True)

    writer = PdfWriter()
    intro = PdfReader(intro_pdf)
    for page in intro.pages:
        page.pop("/Annots", None)
        writer.add_page(page, excluded_keys=["/Annots"])
    offset = len(intro.pages)
    for page in reader.pages[start:stop]:
        # Chapter destinations are deliberately absent from this extract.
        # Do not copy links that would import or point to omitted book pages.
        page.pop("/Annots", None)
        writer.add_page(page, excluded_keys=["/Annots"])
    writer.add_outline_item("How the Book Is Organized", 0)
    contents = writer.add_outline_item("Detailed Contents", offset)
    for i in range(start, stop):
        writer.add_outline_item(
            f"Contents: manuscript page {reader.page_labels[i]}",
            offset + i - start, parent=contents,
        )
    writer.set_page_label(0, offset - 1, style="/D", start=1)
    writer.set_page_label(offset, len(writer.pages) - 1, style="/r", start=start + 1)
    writer.add_metadata({
        "/Title": "Atomic Sanskrit: The Architecture of Sanatan - Overview and Contents",
        "/Author": "Parag Tope",
        "/Subject": "Book organization and complete contents for publisher review",
    })
    writer.write(output)
    check = PdfReader(output)
    assert len(check.pages) == offset + stop - start
    assert all(abs(float(p.mediabox.width) - 595.28) < 1
               and abs(float(p.mediabox.height) - 841.89) < 1 for p in check.pages)
    print(f"Overview: {offset} pages; contents: {stop - start} pages")
    print(f"Total: {len(check.pages)} pages; {output.stat().st_size:,} bytes")
    print(output)


if __name__ == "__main__":
    main()

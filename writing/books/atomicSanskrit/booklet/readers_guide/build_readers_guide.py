#!/usr/bin/env python3
"""Build the separate, page-directed A5 guide without rebuilding the main book."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

import pymupdf as fitz
from PIL import Image, ImageDraw
import qrcode
import qrcode.image.svg
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BUILD = HERE / "build"
sys.path.insert(0, str(ROOT))
from build_book import manuscript_word_count, wrap_scripts_for_latex
from make_figures import make_all

INVITATION = re.compile(r"\{\{invite:([A-Z0-9-]+)\}\}")


def run(args, **kwargs):
    result = subprocess.run([str(arg) for arg in args], capture_output=True, text=True, **kwargs)
    if result.returncode:
        raise RuntimeError(f"{' '.join(map(str, args))}\n{result.stdout[-4500:]}\n{result.stderr[-1500:]}")
    return result.stdout


def latex(md):
    return run(["pandoc", "--from=markdown", "--to=latex", "--wrap=none"],
               input=wrap_scripts_for_latex(md)).strip()


def word_count(md):
    plain = run(["pandoc", "--from=markdown", "--to=plain", "--wrap=none"], input=md)
    return manuscript_word_count(plain.replace("[image]", ""))


def load_pages(text):
    chunks = re.split(r"^<!-- page: ([a-z-]+) -->\s*$", text, flags=re.M)
    pages = []
    for slug, body in zip(chunks[1::2], chunks[2::2]):
        match = re.match(r"\s*# ([^\n]+)\n+", body)
        if not match:
            raise ValueError(f"Page {slug} needs a title")
        title, body = match.group(1), body[match.end():].strip()
        pointer = re.search(r"^Continue in the book: (.+)$", body, re.M)
        reference = pointer.group(1) if pointer else ""
        if pointer:
            body = body[:pointer.start()].rstrip()
        pages.append({"slug": slug, "title": title, "body": body, "reference": reference})
    if len({p["slug"] for p in pages}) != len(pages):
        raise ValueError("Duplicate page IDs")
    return pages


def load_guide(cfg):
    main = (HERE / cfg["manuscript"]).read_text()
    exploration = (HERE / cfg["exploration"]).read_text()
    pages = load_pages(main)
    terms = pages.pop()
    if terms["slug"] != "terms":
        raise ValueError("The source must close with the terms page")
    for page in pages:
        page["part"] = "argument"
    more = load_pages(exploration)
    for page in more:
        page["part"] = "exploration"
    terms["part"] = "terms"
    pages.extend(more + [terms])
    if len({page["slug"] for page in pages}) != len(pages):
        raise ValueError("Duplicate page IDs across the two manuscripts")
    invitations = json.loads((HERE / cfg["invitations"]).read_text())
    used = INVITATION.findall(main + exploration)
    if len(used) != len(set(used)):
        raise ValueError("An invitation appears more than once")
    if set(used) != set(invitations):
        raise ValueError(f"Invitation coverage differs: {set(used) ^ set(invitations)}")
    if len(used) != 101:
        raise ValueError(f"Expected the approved 101 invitations, found {len(used)}")
    for entry in invitations.values():
        if not (ROOT / entry["source"]).is_file():
            raise ValueError(f"Missing invitation source: {entry['source']}")
    return pages, invitations


def expanded_markdown(body, invitations):
    return INVITATION.sub(lambda m: invitations[m[1]]["text"] + "\n\n" +
                         invitations[m[1]]["reference"], body)


def export_figures(inkscape, website):
    make_all()
    qr = qrcode.make(website, image_factory=qrcode.image.svg.SvgPathImage, border=4)
    qr.save(BUILD / "website_qr.svg")
    manifest = []
    for svg in sorted((HERE / "figures").glob("*.svg")) + [BUILD / "website_qr.svg"]:
        pdf = BUILD / f"{svg.stem}.pdf"
        run([inkscape, svg, "--export-text-to-path", "--export-type=pdf",
             f"--export-filename={pdf}"])
        with fitz.open(pdf) as doc:
            if len(doc) != 1:
                raise ValueError(f"Figure export should be one page: {pdf}")
            if doc[0].get_text().strip():
                raise ValueError(f"Figure still has live text: {pdf}")
        if svg.name != "website_qr.svg":
            root = ET.parse(svg).getroot()
            min_px = min(float(e.attrib["font-size"]) for e in root.iter() if "font-size" in e.attrib)
            effective = min_px * (118 / 25.4 * 72) / 720
            if effective < 8.5:
                raise ValueError(f"Too-small figure type in {svg}: {effective:.2f} pt")
            manifest.append({"file": svg.name, "minimum_font_pt_at_118mm": round(effective, 2)})
    return manifest


def preamble(book, cfg):
    fonts = (ROOT / book["mainfontdir"]).as_posix() + "/"
    return r"""\documentclass[11pt,a5paper]{article}
\usepackage[a5paper,top=14mm,bottom=17mm,left=15mm,right=15mm,footskip=8mm]{geometry}
\usepackage{fontspec,graphicx,xcolor,ragged2e,fancyhdr,hyperref,bookmark}
\usepackage{microtype}
\setmainfont[Path={FONTS},FONTOPTIONS]{MAINFONT}
\newfontfamily\devanagarifont[Script=Devanagari,AutoFakeBold=1.8]{DEVFONT}
\newfontfamily\symbolfont{DejaVu Sans}
\newcommand{\latinfont}{\rmfamily}
\definecolor{ink}{HTML}{202C2A}
\definecolor{teal}{HTML}{24665E}
\definecolor{gold}{HTML}{A47E28}
\hypersetup{colorlinks=true,urlcolor=teal,linkcolor=teal,pdftitle={PDFTITLE},pdfauthor={AUTHOR}}
\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[L]{\fontsize{8.5}{10}\selectfont\color{teal}Atomic Sanskrit / A Reader's Guide}
\fancyfoot[R]{\fontsize{9}{10}\selectfont\thepage}
\setlength{\parindent}{0pt}\setlength{\parskip}{5.5pt}
\setlength{\emergencystretch}{1.5em}
\widowpenalty=10000\clubpenalty=10000
\newcommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\newcommand{\pandocbounded}[1]{#1}
\renewenvironment{quote}{\list{}{\leftmargin=10pt\rightmargin=10pt}\item\relax\color{teal}}{\endlist}
\newcommand{\pagetitle}[2]{\pdfbookmark[0]{#1}{#2}{\fontsize{18}{21}\selectfont\color{teal}\bfseries #1\par}\vspace{6pt}}
\renewcommand{\subsection}[1]{\par\vspace{7pt}{\fontsize{12.5}{16}\selectfont\bfseries\color{teal}#1\par}\vspace{2pt}}
\newcommand{\partlabel}[1]{{\fontsize{9}{12}\selectfont\color{teal}#1\par}\vspace{5pt}}
\newcommand{\invitation}[2]{\par\vfill\vspace{5pt}\begin{minipage}{\linewidth}\setlength{\parskip}{0pt}\fontsize{10.5}{13.5}\selectfont
{\color{gold}\hrule height .4pt}\vspace{4pt}\textbf{Explore:} #1\par
{\fontsize{9.5}{12}\selectfont\color{teal}#2\par}\end{minipage}}
\newcommand{\discovery}[2]{\par\vspace{5pt}\begin{minipage}{\linewidth}\fontsize{11}{14.4}\selectfont
#1\par{\fontsize{9.5}{12}\selectfont\color{teal}#2\par}\end{minipage}\par}
\newcommand{\reading}[1]{\vfill\vspace{5pt}{\fontsize{9}{11.5}\selectfont\color{teal}\textbf{Continue in the book:} #1\par}}
\newcommand{\guidefigure}[1]{\par\vspace{3pt}\includegraphics[width=\linewidth]{#1}\par\vspace{3pt}}
\begin{document}
\color{ink}\fontsize{BODY}{LEADING}\selectfont\RaggedRight
""".replace("FONTS", fonts).replace("FONTOPTIONS", book["mainfontoptionsraw"]).replace(
        "MAINFONT", book["mainfont"]).replace("DEVFONT", book["devanagarifont"]).replace(
        "PDFTITLE", f'{book["title"]}: {cfg["publication"]}').replace("AUTHOR", book["author"]).replace(
        "BODY", str(cfg["body_font_size"])).replace("LEADING", str(cfg["line_spacing_pt"]))


def title_page(book, cfg, cover=False):
    # Metadata stays in as_book.yaml; the guide adds only its publication label.
    return "\n".join([
        r"\thispagestyle{empty}",
        r"\vspace*{9mm}",
        r"{\color{teal}\fontsize{11}{14}\selectfont SECOND SHANTI\par}",
        r"\vspace{12mm}",
        r"{\fontsize{35}{38}\selectfont\bfseries " + latex(book["title"]).replace(" ", "\\par ", 1) + r"\par}",
        r"\vspace{4mm}",
        r"{\color{teal}\fontsize{18}{22}\selectfont " + latex(cfg["publication"]) + r"\par}",
        r"\vspace{9mm}",
        r"{\fontsize{13}{17}\selectfont " + latex(book["subtitle"]) + r"\par}",
        r"\vspace{8mm}",
        r"\includegraphics[width=\linewidth]{" + (BUILD / "inside_out.pdf").as_posix() + "}",
        r"\vfill",
        r"{\fontsize{16}{19}\selectfont " + latex(book["author"]) + r"\par}",
        r"\vspace{3mm}",
        r"{\fontsize{9}{12}\selectfont\color{teal}" + latex(cfg["edition"]) + r"\par}",
    ])


def make_interior(book, cfg, pages, invitations):
    output = [preamble(book, cfg)]
    for idx, page in enumerate(pages):
        if idx:
            output.append(r"\clearpage")
        if page["slug"] == "title":
            output.append(title_page(book, cfg))
            continue
        if page["slug"] == "why":
            output.append(r"\partlabel{PART I / UNDERSTAND THE ARGUMENT}")
        elif page["slug"] == "explore":
            output.append(r"\partlabel{PART II / EXPLORE THE BOOK}")
        output.append(r"\pagetitle{" + latex(page["title"]) + "}{" + page["slug"] + "}")
        body = page["body"]
        def figure(match):
            path = (BUILD / (Path(match.group(1)).stem + ".pdf")).as_posix()
            if not Path(path).is_file():
                raise ValueError(f"Missing figure: {path}")
            return "\n```{=latex}\n\\guidefigure{" + path + "}\n```\n"
        body = re.sub(r"!\[\]\(([^)]+\.svg)\)", figure, body)
        def invitation(match):
            entry = invitations[match[1]]
            macro = "invitation" if page["part"] == "argument" else "discovery"
            return "\n```{=latex}\n\\" + macro + "{" + latex(entry["text"]) + "}{" + latex(entry["reference"]) + "}\n```\n"
        body = INVITATION.sub(invitation, body)
        body_tex = latex(body)
        output.append(body_tex)
        if page["reference"]:
            output.append(r"\reading{" + latex(page["reference"]) + "}")
    return "\n".join(output) + "\n\\end{document}\n"


def make_cover(book, cfg):
    text = [preamble(book, cfg), r"\pagestyle{empty}", title_page(book, cfg, cover=True), r"\clearpage"]
    text.append(r"\pagetitle{An Introduction to the Argument}{inside-front}")
    text.append(latex("""How can a language remain dependable while people continue creating new expressions? What does its preservation reveal about the order of the civilization that cares for it?

This guide follows the argument of *Atomic Sanskrit* from the speaking body through sounds, words, sentences, and Vedic transmission. It explains why the book places Sanskrit within an inside-out architecture of Sanātan and why it challenges the inherited account of Sanskrit's origin.

You can follow the examples without knowing Sanskrit. The first part explains the argument in familiar English, supported by Devanagari and diagrams. The second part offers a chapter-by-chapter route into the full book.

Across both parts, 101 invitations point to particular examples, stories, comparisons, and arguments. Follow one that interests you; the chapter and section beside it show where to continue."""))
    text.extend([r"\vfill", latex("*Atomic Sanskrit* is the first volume of *Second Shanti*."), r"\clearpage"])
    text.append(r"\pagetitle{About This Edition}{inside-back}")
    text.append(latex(f"""{cfg['edition']}

© 2026 {book['author']}. All rights reserved.

Prepared for private review and discussion. Please do not redistribute or publish this draft without the author's permission.

This booklet summarizes the argument of *{book['title']}*. The full book and its Source and Reference Companion contain the detailed evidence, research methods, and references.

Contact: [{cfg['email']}](mailto:{cfg['email']})

Website: [secondshanti.org/as]({cfg['website']})"""))
    text.append(r"\par\vspace{10mm}{\fontsize{14}{17}\selectfont\bfseries\color{teal} About the Author\par}")
    text.append(latex((ROOT / "cover/_shared/parag_bio.md").read_text()))
    text.extend([r"\clearpage", r"\vspace*{12mm}", r"\pagetitle{From Sound to Civilization}{back}"])
    text.append(latex("""Sanskrit's familiar sound sequence maps the speaking body. Small forms carrying basic meanings combine into words, and words form expressions that can carry knowledge across generations. The Vedas keep complete examples available for checking and correction.

*Atomic Sanskrit* connects this linguistic architecture to a larger idea: order can grow through shared standards and distributed responsibility rather than commands from an apex. This reader's guide introduces that argument in familiar English, with examples, diagrams, and pointers to the book's chapters. It also explains the book's challenge to the accepted account of Sanskrit's origin and its alternative account of knowledge traveling outward from India."""))
    text.extend([r"\vfill", r"\includegraphics[width=29mm]{"+(BUILD / "website_qr.pdf").as_posix()+r"}\par",
                 latex(f"[secondshanti.org/as]({cfg['website']})")+r"\par",
                 r"\vspace{3mm}{\fontsize{14}{17}\selectfont "+latex(book["author"])+r"\par}", r"\end{document}"])
    return "\n".join(text)


def compile_pdf(name, tex, expected):
    path = BUILD / f"{name}.tex"
    path.write_text(tex, encoding="utf-8")
    for _ in range(2):
        run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", path.name], cwd=BUILD)
    log = path.with_suffix(".log").read_text(encoding="utf-8", errors="replace")
    bad = [line for line in log.splitlines() if "Missing character:" in line or "Overfull \\" in line]
    if bad:
        raise ValueError("Typesetting errors:\n" + "\n".join(bad))
    pdf = path.with_suffix(".pdf")
    with fitz.open(pdf) as doc:
        if len(doc) != expected:
            starts = [page.get_text().splitlines()[:2] for page in doc]
            raise ValueError(f"{name}: expected {expected} pages, got {len(doc)}.\n{starts}")
        for page in doc:
            if abs(page.rect.width-148/25.4*72) > .1 or abs(page.rect.height-210/25.4*72) > .1:
                raise ValueError("Wrong trim size")
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        rect = fitz.Rect(span["bbox"])
                        if not page.rect.contains(rect):
                            raise ValueError(f"Text outside page {page.number+1}: {span['text']}")
    return pdf


def render_qa(pdf, prefix):
    dest = BUILD / "qa"
    dest.mkdir(exist_ok=True)
    for old in dest.glob(f"{prefix}-*.png"):
        old.unlink()
    with fitz.open(pdf) as doc:
        thumbs = []
        for i, page in enumerate(doc):
            pix = page.get_pixmap(matrix=fitz.Matrix(1.7, 1.7), alpha=False)
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            image.save(dest / f"{prefix}-{i+1:02}.png")
            image.thumbnail((300, 426))
            thumb = Image.new("RGB", (320, 457), "#e1e5e2")
            thumb.paste(image, ((320-image.width)//2, 8))
            ImageDraw.Draw(thumb).text((12, 440), f"{prefix} / {i+1}", fill="black")
            thumbs.append(thumb)
        for start in range(0, len(thumbs), 6):
            sheet = Image.new("RGB", (960, 914), "white")
            for j, thumb in enumerate(thumbs[start:start+6]):
                sheet.paste(thumb, ((j%3)*320, (j//3)*457))
            sheet.save(dest / f"{prefix}-sheet-{start//6+1}.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-figures", action="store_true", help="Reuse existing outlined exports")
    args = parser.parse_args()
    cfg = yaml.safe_load((HERE / "readers_guide.yaml").read_text())
    book = yaml.safe_load((HERE / cfg["book_metadata"]).read_text())
    pages, invitations = load_guide(cfg)
    source = "\n\n".join("# " + p["title"] + "\n\n" + expanded_markdown(p["body"], invitations) for p in pages)
    if len(pages) != cfg["expected_pages"]:
        raise ValueError("Storyboard and page count differ")
    BUILD.mkdir(parents=True, exist_ok=True)
    ink = shutil.which("inkscape") or "/Applications/Inkscape.app/Contents/MacOS/inkscape"
    manifest_path = BUILD / "figure_manifest.json"
    if args.skip_figures:
        figures = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    else:
        figures = export_figures(ink, cfg["website"])
        manifest_path.write_text(json.dumps(figures, indent=2)+"\n")
    (BUILD / "reading_text.md").write_text(source, encoding="utf-8")
    print(f"Building {len(pages)}-page A5 interior...", flush=True)
    interior = compile_pdf("interior", make_interior(book, cfg, pages, invitations), cfg["expected_pages"])
    print("Building four cover faces...", flush=True)
    cover = compile_pdf("cover", make_cover(book, cfg), 4)
    out = (HERE / cfg["output_dir"]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    stem = "atomic_sanskrit_readers_guide"
    shutil.copy2(interior, out / f"{stem}.a5.pdf")
    shutil.copy2(interior, out / f"{stem}.a5.print.pdf")
    shutil.copy2(cover, out / f"{stem}.cover.pdf")
    with fitz.open() as combined, fitz.open(cover) as covers, fitz.open(interior) as inside:
        combined.insert_pdf(covers, from_page=0, to_page=1)
        combined.insert_pdf(inside)
        combined.insert_pdf(covers, from_page=2, to_page=3)
        combined.set_metadata({"title": f"{book['title']}: {cfg['publication']}", "author": book["author"]})
        toc = [[1, "Cover", 1], [1, "About this guide", 2]]
        toc += [[level, title, number+2] for level, title, number in inside.get_toc()]
        toc += [[1, "Edition information", len(inside)+3], [1, "Back cover", len(inside)+4]]
        combined.set_toc(toc)
        combined.save(out / f"{stem}.a5.complete.pdf")
    render_qa(interior, "interior")
    render_qa(cover, "cover")
    report = {"interior_pages": len(pages), "cover_pages": 4, "trim_mm": [148, 210],
              "body_font_pt": cfg["body_font_size"], "line_spacing_pt": cfg["line_spacing_pt"],
              "source_word_count": word_count(source), "figures": figures,
              "invitation_count": len(invitations),
              "invitation_placements": {m: p["slug"] for p in pages for m in INVITATION.findall(p["body"])},
              "word_count_scope": "Pandoc plain text; includes titles, invitations, and reading pointers; excludes HTML markers, image paths, SVG labels, and cover prose",
              "pages": [{"page": i+1, "title": p["title"], "words": word_count(expanded_markdown(p["body"], invitations))} for i,p in enumerate(pages)],
              "checks": {"missing_glyphs": 0, "overfull_boxes": 0, "out_of_page_text": 0},
              "physical_print_test": "not performed", "author_approval": "pending"}
    (BUILD / "qa_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n")
    print(json.dumps({k: report[k] for k in ("interior_pages", "cover_pages", "source_word_count", "checks")}, indent=2))
    print(f"Output: {out}")


if __name__ == "__main__":
    main()

"""Read the archived concordance as table cells, retaining commentary links."""

from html.parser import HTMLParser
import json
import sys

from run_pilot import ARCHIVE


class TextReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def source_text(filename):
    parser = TextReader()
    parser.feed((ARCHIVE / filename).read_text())
    return " ".join(" ".join(parser.parts).split())


class TableReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "tr":
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = {"text": "", "links": []}
        elif tag == "a" and self.cell is not None and attrs.get("href", "").startswith("files/"):
            self.cell["links"].append(attrs["href"])

    def handle_data(self, data):
        if self.cell is not None:
            self.cell["text"] += data

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.cell["text"] = " ".join(self.cell["text"].split())
            self.row.append(self.cell)
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if len(self.row) == 9 and self.row[0]["text"].isdigit():
                self.rows.append(self.row)
            self.row = None


def read_rows():
    parser = TableReader()
    parser.feed((ARCHIVE / "dhatu-concordance-gana.html").read_text())
    return [{"row": r[0]["text"], "gana": r[1]["text"], "citation": r[2]["text"],
             "gloss": r[3]["text"], "it": r[4]["text"], "pada": r[5]["text"],
             "commentaries": [link for c in r[6:] for link in c["links"]]}
            for r in parser.rows]


if __name__ == "__main__":
    terms = sys.argv[1:]
    for row in read_rows():
        if not terms or any(term in row["citation"] or term in row["gloss"] for term in terms):
            print(json.dumps(row, ensure_ascii=False))

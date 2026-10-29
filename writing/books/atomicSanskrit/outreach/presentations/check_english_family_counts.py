"""Reproduce the presentation's English headword count, not ancestry direction."""

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


class RootLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.root = None
        self.href = None
        self.entries = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.stack.append((tag, attrs))
        if tag == "a":
            self.href = attrs.get("href", "")

    def handle_endtag(self, tag):
        if tag == "a":
            if self.root and self.href and "/word/search.html" in self.href:
                query = parse_qs(urlsplit(self.href).query).get("q", [""])[0]
                # The overview repeats a few headwords with trailing punctuation.
                word = query.strip().rstrip(".,;:")
                if (word and word[0].islower()
                        and not word.startswith("-") and not word.endswith("-")):
                    self.entries.setdefault(self.root, set()).add(word)
            self.href = None
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                self.stack = self.stack[:index]
                break

    def handle_data(self, data):
        if (self.stack and self.stack[-1][0] == "font"
                and self.stack[-1][1].get("color") == "#006595"):
            label = data.strip()
            self.root = label if label in ("gen\u0259-", "st\u0101-") else None


if __name__ == "__main__":
    parser = RootLinks()
    parser.feed(Path(sys.argv[1]).read_text(encoding="utf-8"))
    assert set(parser.entries) == {"gen\u0259-", "st\u0101-"}, "Source format changed"
    combined = set().union(*parser.entries.values())
    print(json.dumps({
        "source": "https://www.ahdictionary.com/word/indoeurop.html",
        "counts": {key: len(value) for key, value in parser.entries.items()},
        "union": len(combined),
        "scope": "Distinct lower-case linked headwords; no combining forms or inflections added",
    }, indent=2))

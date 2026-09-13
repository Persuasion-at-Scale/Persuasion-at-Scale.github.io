#!/usr/bin/env python3.11
"""Assemble math.html from index.html's <head> (so the CSS matches) plus math-body.html.

Run from the site root:
    python3.11 src/build-math-page.py

Deterministic: the head is copied from index.html at build time, with the
<title> and description swapped, so a CSS change on the main page carries
over on the next build. The body lives in src/math-body.html and is the only
thing to edit by hand.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
index = (ROOT / "index.html").read_text(encoding="utf-8")
body = (ROOT / "src" / "math-body.html").read_text(encoding="utf-8")

head_end = index.index("</head>") + len("</head>")
head = index[:head_end]
head = re.sub(
    r"<title>.*?</title>",
    "<title>The math you will use | Persuasion at Scale | Columbia University</title>",
    head,
    flags=re.S,
)
head = re.sub(
    r'<meta name="description" content="[^"]*"',
    '<meta name="description" content="What mathematics and programming Persuasion at Scale (PSAM UN3707) actually uses, and how to get ready before the first class."',
    head,
)
head = head.replace(
    'content="https://persuasion-at-scale.github.io/index.html"',
    'content="https://persuasion-at-scale.github.io/math.html"',
)

out = head + "\n<body>\n" + body + "\n</body>\n</html>\n"
(ROOT / "math.html").write_text(out, encoding="utf-8")
print("wrote", ROOT / "math.html", len(out), "bytes")

#!/usr/bin/env python3
"""Small pre-flight check: internal links, required files, and head tags.

    python3 scripts/check.py
"""
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
HTML = sorted(p for p in ROOT.rglob("*.html") if "scripts" not in p.parts)
REQUIRED = [
    "index.html", "resume/index.html", "404.html",
    "robots.txt", "sitemap.xml", "favicon.svg", "favicon.ico",
    "site.webmanifest", "assets/img/og.png", "Priyansh-Verma-Resume.pdf",
    "_headers", "vercel.json", "README.md",
    "work/interviewer-coach/index.html", "work/email-spam/index.html", "work/churn/index.html",
]

errors, warnings = [], []

for rel in REQUIRED:
    if not (ROOT / rel).exists():
        errors.append(f"missing required file: {rel}")

href_re = re.compile(r'(?:href|src)="([^"]+)"')
for page in HTML:
    text = page.read_text(encoding="utf-8")
    rel_page = page.relative_to(ROOT)
    for url in href_re.findall(text):
        if url.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
            continue
        path = url.split("#")[0].split("?")[0]
        if not path:
            continue
        target = (ROOT / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            errors.append(f"{rel_page}: broken internal link -> {url}")

    noindex = "noindex" in text
    checks = {
        "<title>": "<title>" in text,
        "meta description": 'name="description"' in text,
        "canonical": 'rel="canonical"' in text or noindex,
        "og:image": 'property="og:image"' in text or noindex,
        "one h1": text.count("<h1") == 1,
        "lang": 'lang="en"' in text,
    }
    for label, ok in checks.items():
        if not ok:
            warnings.append(f"{rel_page}: missing/invalid {label}")

# sitemap <-> pages
sm = (ROOT / "sitemap.xml").read_text()
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
for loc in locs:
    path = urlparse(loc).path.strip("/")
    target = ROOT / path / "index.html" if path else ROOT / "index.html"
    if not target.exists():
        errors.append(f"sitemap: {loc} has no matching page")

print(f"checked {len(HTML)} HTML pages, {len(locs)} sitemap URLs")
for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
if errors:
    sys.exit(1)
print("OK — no broken internal links, required files present.")

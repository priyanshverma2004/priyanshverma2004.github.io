# The Index — priyanshverma2004.github.io

A card-catalogue portfolio for Priyansh Verma: four project records, three full case
studies, a printable résumé, and an author card that turns over to reveal contact
details.

Static HTML, hand-written CSS, one small vanilla JS file. No build step, no framework,
no npm, no analytics, no cookies. Every word of content is in the HTML, so the site is
fully readable and navigable with JavaScript switched off.

---

## Run it locally

```bash
cd portfolio
python3 -m http.server 8123
# open http://localhost:8123/
```

Any static server works. Opening `index.html` directly from the filesystem will not:
the pages use root-relative paths (`/assets/...`) so they can be deployed at a domain
root without rewriting.

---

## What is in here

```
.
├── index.html                     Home: hero, abstract, 4 records, also-filed list,
│                                  toolkit, log, contact
├── work/
│   ├── interviewer-coach/         R-001 case study
│   ├── email-spam/                R-002 case study
│   └── churn/                     R-003 case study
├── resume/index.html              Web résumé (print stylesheet included)
├── Priyansh-Verma-Resume.pdf      One-page A4 PDF, real links, 1 page
├── 404.html
├── robots.txt · sitemap.xml · site.webmanifest · favicon.svg · favicon.ico
├── _headers                       Security + cache headers (Netlify / Cloudflare)
├── vercel.json                    The same headers for Vercel
├── assets/
│   ├── css/archive.css            Design system, responsive rules, print styles
│   ├── js/archive.js              Progressive enhancement only
│   ├── fonts/                     Self-hosted WOFF2 + OFL licences
│   └── img/                       og.png, icons
└── scripts/
    ├── check.py                   Link + head-tag pre-flight
    ├── make-assets.py             Regenerates og.png and icons (Pillow)
    ├── make-resume-pdf.py         Regenerates the PDF (reportlab)
    └── set-site-url.sh            Rewrites the canonical domain everywhere
```

---

## Editing content

Everything is plain HTML; there is no CMS and no templating language. The three places
you are most likely to touch:

| Want to change | File | Look for |
| --- | --- | --- |
| Name, role, lede, hero facts | `index.html` | `<section class="hero"` |
| Contact links on the card back | `index.html` | `<div class="card__face--back"` |
| A project summary or metric | `index.html` | `<details class="record" id="r-00…">` |
| A full case study | `work/*/index.html` | the `<section id="…">` blocks |
| Contact details, status line | `index.html`, `resume/index.html` | `<section … id="contact"`, `.resume__contact` |
| Résumé PDF text | `scripts/make-resume-pdf.py` | `projects`, `skills` lists |

The search index is generated at runtime from the text of each record, so a new record
is searchable as soon as it is added — no index file to update.

### Adding a record

1. Copy an existing `<details class="record">` block in `index.html`.
2. Give it a unique `id` (`r-005`) and update `data-tags` (space-separated keywords used
   by the filter chips: `genai`, `nlp`, `ml`).
3. Update the `record__no`, title, role, metric and year in the `<summary>`.
4. If it deserves a case study, add `work/<slug>/index.html`, then add the URL to
   `sitemap.xml` and to `scripts/check.py`'s `REQUIRED` list.

---

## Change the domain

The site ships pointed at `https://priyanshverma2004.github.io`. To move it:

```bash
./scripts/set-site-url.sh https://your-domain.com
```

That rewrites canonical links, Open Graph and Twitter URLs, JSON-LD `@id`s and `url`s,
`robots.txt` and `sitemap.xml`. Then regenerate the PDF, because it prints the résumé URL:

```bash
scripts/.venv/bin/python scripts/make-resume-pdf.py
```

Verify with:

```bash
python3 scripts/check.py
grep -rn "priyanshverma2004.github.io" --include="*.html" --include="*.xml" --include="*.txt" .
```

---

## Deploy

The site **must be served from a domain root**, because every internal link starts with
`/`. All four options below do that.

### GitHub Pages (free, current default)

The repository must be named **`priyanshverma2004.github.io`** — a user/organisation
Pages site, which serves at the domain root. A normal project repo would serve at
`/repo-name/` and every root-relative link would break.

```bash
cd portfolio
git init
git add .
git commit -m "The Index — portfolio"
git branch -M main
git remote add origin git@github.com:priyanshverma2004/priyanshverma2004.github.io.git
git push -u origin main
```

Then: **Settings → Pages → Source: Deploy from a branch → main / (root)**.
Live at `https://priyanshverma2004.github.io` in about a minute.
`404.html` is picked up automatically.

### Netlify (free)

Drag the `portfolio` folder onto <https://app.netlify.com/drop>, or connect the repo
with build command empty and publish directory `.`. `_headers` is applied automatically.

### Vercel (free)

```bash
npx vercel --prod
```

Framework preset: **Other**. Build command: none. Output directory: `.`.
`vercel.json` supplies headers and clean URLs.

### Cloudflare Pages (free)

Connect the repo; build command empty, output directory `/`. `_headers` is honoured.

---

## Checks before you publish

```bash
python3 scripts/check.py            # broken internal links, required files, head tags
```

It verifies every `href`/`src`, that `sitemap.xml` only lists pages that exist, and that
each page has a title, description, canonical, OG image, one `<h1>` and `lang="en"`.

Regenerate the raster assets after changing the tagline or metrics:

```bash
python3 scripts/make-assets.py                              # needs Pillow
scripts/.venv/bin/python scripts/make-resume-pdf.py          # needs reportlab
```

---

## Accessibility and behaviour notes

- Semantic landmarks (`header`, `nav`, `main`, `footer`), one `<h1>` per page, skip link.
- Keyboard: search with `/`, close with `Esc`; the mobile menu traps Tab and restores
  focus; every control has a visible focus ring.
- `prefers-reduced-motion` disables the card and drawer transitions.
- `prefers-color-scheme: dark` is respected on first visit; the lamp button overrides it.
- **Plain view** (`localStorage: pv-plain`) hides decoration and expands every record —
  useful for a recruiter skimming on a phone, and it survives navigation.
- The author card is a real disclosure: the button flips it to the reverse side with
  email, GitHub, LinkedIn and résumé links. The back is `inert` while hidden, and
  keyboard order runs button → card links → rest of the page.
- Theme choice persists in `localStorage: pv-theme`. Nothing else is stored, ever.
- Print stylesheet: the résumé prints on one page; records print expanded.

---

## Privacy

No analytics, no cookies, no third-party requests, no tracking pixels. Fonts are
self-hosted, so no request reaches Google. The only network calls the page makes are
for files on its own domain; outbound links to GitHub and LinkedIn are ordinary links.

The phone number appears on the résumé page and in the PDF only — not on the home page.
Remove it from both if you would rather keep applications email-only.

---

## Licences

Site content and code: © 2026 Priyansh Verma.

Typefaces are self-hosted under the SIL Open Font License 1.1; the licence texts are in
`assets/fonts/licenses/`.

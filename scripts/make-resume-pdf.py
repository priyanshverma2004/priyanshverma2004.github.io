#!/usr/bin/env python3
"""Build the one-page A4 resume PDF.

    python3 -m venv scripts/.venv
    scripts/.venv/bin/pip install reportlab
    scripts/.venv/bin/python scripts/make-resume-pdf.py
"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, HRFlowable, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Priyansh-Verma-Resume.pdf"

INK = HexColor("#1a1714")
INK2 = HexColor("#4e483f")
INK3 = HexColor("#6d6558")
RULE = HexColor("#c9bda6")
STAMP = HexColor("#a3321f")
PAPER = HexColor("#ffffff")

FONTS = {
    "Georgia": "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "Georgia-Bold": "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    "Georgia-Italic": "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
}
for name, path in FONTS.items():
    pdfmetrics.registerFont(TTFont(name, path))

W, H = A4
M = 15 * mm

styles = {
    "name": ParagraphStyle("name", fontName="Georgia", fontSize=29, leading=31, textColor=INK, spaceAfter=2),
    "role": ParagraphStyle("role", fontName="Georgia-Italic", fontSize=11, leading=13.5, textColor=INK2, spaceAfter=5),
    "contact": ParagraphStyle("contact", fontName="Georgia", fontSize=8.3, leading=11.5, textColor=INK2),
    "h2": ParagraphStyle("h2", fontName="Georgia-Bold", fontSize=8.4, leading=10, textColor=STAMP, spaceBefore=8, spaceAfter=2),
    "body": ParagraphStyle("body", fontName="Georgia", fontSize=9.1, leading=12.2, textColor=INK2, alignment=TA_LEFT, spaceAfter=2),
    "entry": ParagraphStyle("entry", fontName="Georgia", fontSize=10.1, leading=12, textColor=INK, spaceBefore=2.5),
    "meta": ParagraphStyle("meta", fontName="Georgia-Italic", fontSize=8.4, leading=10.4, textColor=INK3, spaceAfter=1),
    "small": ParagraphStyle("small", fontName="Georgia", fontSize=8.35, leading=10.9, textColor=INK2),
    "link": ParagraphStyle("link", fontName="Georgia", fontSize=7.5, leading=9.8, textColor=INK3),
    "skill": ParagraphStyle("skill", fontName="Georgia", fontSize=8.5, leading=10.8, textColor=INK2),
}


def link(url, label=None):
    label = label or url
    return f'<link href="{url}" color="#4e483f">{label}</link>'


def rule(space_before=1, space_after=3):
    return HRFlowable(width="100%", thickness=0.6, color=RULE,
                      spaceBefore=space_before, spaceAfter=space_after)


def section(title):
    return [Paragraph(title.upper(), styles["h2"]), rule(0, 4)]


def make():
    doc = BaseDocTemplate(str(OUT), pagesize=A4,
                          leftMargin=M, rightMargin=M, topMargin=13 * mm, bottomMargin=11 * mm,
                          title="Priyansh Verma — Résumé",
                          author="Priyansh Verma",
                          subject="Machine learning, generative AI and software engineering",
                          creator="Priyansh Verma")
    frame = Frame(M, 11 * mm, W - 2 * M, H - 24 * mm, id="main",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="one", frames=[frame])])

    s = []
    s.append(Paragraph("Priyansh Verma", styles["name"]))
    s.append(Paragraph("Machine learning · Generative AI · Software engineering", styles["role"]))
    contact = (
        "Bengaluru, Karnataka, India &nbsp;·&nbsp; "
        f'{link("mailto:priyanshverma2004@gmail.com", "priyanshverma2004@gmail.com")} &nbsp;·&nbsp; '
        f'{link("tel:+919343603050", "+91 93436 03050")}<br/>'
        f'{link("https://github.com/priyanshverma2004", "github.com/priyanshverma2004")} &nbsp;·&nbsp; '
        f'{link("https://www.linkedin.com/in/priyansh-verma-7173572aa/", "linkedin.com/in/priyansh-verma")}'
    )
    s.append(Paragraph(contact, styles["contact"]))
    s.append(Spacer(1, 5))
    s.append(HRFlowable(width="100%", thickness=1.2, color=INK, spaceBefore=0, spaceAfter=2))

    s += section("Profile")
    s.append(Paragraph(
        "MCA (Generative AI) student at Alliance University with a foundation in software development, "
        "machine learning and NLP. I build complete, documented ML systems — from data cleaning and "
        "baselines to a Flask or Streamlit interface. Looking for an internship or entry-level role in "
        "machine learning, AI engineering or software engineering.", styles["body"]))

    s += section("Education")
    for title, meta, body in [
        ("MCA, Generative AI — Alliance University",
         "Bengaluru, India · Aug 2025 — present",
         "Coursework: machine learning, deep learning, natural language processing, generative AI, data structures and algorithms."),
        ("BCA, Computer Applications — Kalinga University",
         "Raipur, India · Aug 2022 — May 2025 · 74.28%",
         "Foundations in programming, databases, operating systems, networking and web development."),
    ]:
        s.append(Paragraph(title, styles["entry"]))
        s.append(Paragraph(meta, styles["meta"]))
        s.append(Paragraph(body, styles["small"]))

    s += section("Selected projects")
    projects = [
        ("AI Interview Coach — Flask · Gemini 2.5 Flash",
         "A mock-interview web app that generates role-specific questions from a job description and résumé, "
         "evaluates each answer and saves a performance report. Eight routes, six templates, four service modules. "
         "Includes a mock mode so the app can be reviewed without an API key.",
         "github.com/priyanshverma2004/interviewer-coach · priyanshverma2004.github.io/work/interviewer-coach/",
         "https://github.com/priyanshverma2004/interviewer-coach"),
        ("Email Spam Classifier — CountVectorizer · Multinomial Naive Bayes",
         "Classified 5,171 emails with an 80/20 split. 97.1% accuracy on 1,035 held-out emails against a 71.7% "
         "majority-class baseline; spam F1 0.95, ham F1 0.98. Reported per-class metrics, not accuracy alone.",
         "github.com/priyanshverma2004/email_spam · priyanshverma2004.github.io/work/email-spam/",
         "https://github.com/priyanshverma2004/email_spam"),
        ("Customer Churn Prediction — scikit-learn · Streamlit",
         "Built a churn pipeline on 1,000 customer records with one-hot encoding, scaling and a random forest "
         "(200 trees, depth 10). 0.868 ROC-AUC on 200 held-out rows against a 0.859 logistic baseline; served "
         "the saved pipeline through a Streamlit form.",
         "github.com/priyanshverma2004/Custo_churn_pred_prj · priyanshverma2004.github.io/work/churn/",
         "https://github.com/priyanshverma2004/Custo_churn_pred_prj"),
        ("Airport X-ray Screening — YOLO26n · Ultralytics · Streamlit",
         "Trained a YOLO26n detector on 13,728 X-ray images across 12 prohibited-item classes. "
         "Baseline (no augmentation) reached 0.796 mAP@50 and 0.734 recall; with augmentation, "
         "0.887 mAP@50 and 0.813 recall. Reported per-class results (HandCuffs 0.981, Knife 0.757) "
         "and the run's confounds honestly. Ships a Streamlit screening app with a live threshold.",
         "github.com/priyanshverma2004/airport-baggage-screening · priyanshverma2004.github.io/work/airport-baggage-screening/",
         "https://github.com/priyanshverma2004/airport-baggage-screening"),
        ("FridgeAI — FastAPI · React · FAISS RAG",
         "A full-stack kitchen assistant: photograph a fridge to build an inventory, then plan meals, "
         "generate a shopping list and chat with a recipe-grounded assistant. FastAPI + PostgreSQL + "
         "JWT auth backend, React/TanStack frontend, Gemini/Groq vision for scanning, FAISS over a "
         "recipe book. Documented the Lovable-scaffolded UI honestly.",
         "github.com/priyanshverma2004/fridgeai · priyanshverma2004.github.io/work/fridgeai/",
         "https://github.com/priyanshverma2004/fridgeai"),
    ]
    for title, body, label, url in projects:
        s.append(KeepTogether([
            Paragraph(title, styles["entry"]),
            Paragraph(body, styles["small"]),
            Paragraph(link(url, label), styles["link"]),
        ]))

    s += section("Technical skills")
    skills = [
        ("Languages", "Python (primary), C, C++, JavaScript, SQL"),
        ("ML", "scikit-learn, pandas, NumPy; classification, pipelines, class imbalance (SMOTE), evaluation"),
        ("Deep learning", "TensorFlow / Keras; CNNs, LSTMs, convolutional autoencoders; YOLO (Ultralytics) for object detection"),
        ("NLP", "Preprocessing, tokenisation, CountVectorizer / TF-IDF, text classification, RAG, FAISS, sentence-transformers"),
        ("Generative AI", "Gemini API, prompt design, structured JSON output, Flask / FastAPI integration"),
        ("Backend", "FastAPI, SQLAlchemy, PostgreSQL, JWT auth (passlib/bcrypt)"),
        ("Web", "Flask, Jinja, Streamlit, HTML/CSS/JS; React, TanStack Router, Vite, Tailwind (coursework)"),
        ("Tools", "Git, GitHub, Jupyter, VS Code, IntelliJ IDEA"),
    ]
    rows = [[Paragraph(k, styles["skill"]), Paragraph(v, styles["skill"])] for k, v in skills]
    t = Table(rows, colWidths=[29 * mm, W - 2 * M - 29 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6),
        ("TEXTCOLOR", (0, 0), (0, -1), INK3),
    ]))
    s.append(t)

    s += section("Certifications")
    s.append(Paragraph(
        "Python — SoloLearn &nbsp;·&nbsp; DBMS — Coursera &nbsp;·&nbsp; Advanced Data Structures &amp; Algorithms — Coursera "
        "&nbsp;·&nbsp; Machine Learning — Coursera &nbsp;·&nbsp; SQL &nbsp;·&nbsp; MongoDB Basics", styles["small"]))

    s += section("Also")
    s.append(Paragraph(
        "Public work: ten NLP experiment notebooks, deep-learning experiments with CNNs, LSTMs and autoencoders, "
        f'and a CRISP-DM case study on Netflix recommendations — {link("https://github.com/priyanshverma2004", "github.com/priyanshverma2004")}.',
        styles["small"]))
    s.append(Spacer(1, 5))
    s.append(Paragraph(
        f'This résumé is also a web page: {link("https://priyanshverma2004.github.io/resume/", "priyanshverma2004.github.io/resume")}. '
        "Last updated 14 November 2026.", styles["link"]))

    doc.build(s)
    print("wrote", OUT)


if __name__ == "__main__":
    make()

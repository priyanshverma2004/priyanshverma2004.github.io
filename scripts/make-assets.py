#!/usr/bin/env python3
"""Generate the static social preview, touch icon and favicon.

Run from the repository root:  python3 scripts/make-assets.py
Requires Pillow. Uses macOS system fonts (Georgia + Menlo) so no downloads.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
IMG.mkdir(parents=True, exist_ok=True)

PAPER = "#f2ecdf"
PAPER_2 = "#e9e0cf"
CARD = "#faf5e9"
INK = "#1a1714"
INK_2 = "#4e483f"
INK_3 = "#6d6558"
RULE = "#cec2ab"
STAMP = "#a3321f"

GEORGIA = "/System/Library/Fonts/Supplemental/Georgia.ttf"
GEORGIA_I = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
MENLO = "/System/Library/Fonts/Menlo.ttc"


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def tracked(draw, xy, text, f, fill, tracking=0):
    """Draw text with letter-spacing. Returns the end x."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking
    return x


def stamp_layer(text_lines, f, color, pad=18):
    tmp = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    widths = [d.textlength(t, font=f) for t in text_lines]
    w = int(max(widths)) + pad * 2
    h = int(f.size * 1.15 * len(text_lines)) + pad * 2
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([1, 1, w - 2, h - 2], outline=color, width=4)
    d.rectangle([8, 8, w - 9, h - 9], outline=color, width=1)
    y = pad - 4
    for t in text_lines:
        tw = d.textlength(t, font=f)
        d.text(((w - tw) / 2, y), t, font=f, fill=color)
        y += int(f.size * 1.15)
    return layer.rotate(-7, expand=True, resample=Image.BICUBIC)


def make_og():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # faint horizontal rules, like a ledger
    for y in range(0, H, 22):
        d.line([(0, y), (W, y)], fill="#ece3d2", width=1)

    # card
    x0, y0, x1, y1 = 58, 54, W - 58, H - 54
    d.rectangle([x0 + 7, y0 + 8, x1 + 7, y1 + 8], fill="#d9cbb2")
    d.rectangle([x0, y0, x1, y1], fill=CARD, outline=INK_3, width=2)
    d.rectangle([x0 + 9, y0 + 9, x1 - 9, y1 - 9], outline=RULE, width=1)

    mono = font(MENLO, 19)
    mono_s = font(MENLO, 16)
    name_f = font(GEORGIA, 112)
    role_f = font(GEORGIA_I, 44)
    meta_f = font(GEORGIA, 24)

    # header
    tracked(d, (x0 + 42, y0 + 40), "AUTHOR FILE", mono, INK_3, 2.2)
    d.text((x0 + 42 + 178, y0 + 40), "NO. 001", font=mono, fill=INK)
    right = "BENGALURU · INDIA"
    d.text((x1 - 42 - d.textlength(right, font=mono_s), y0 + 42), right, font=mono_s, fill=INK_3)
    d.line([(x0 + 42, y0 + 82), (x1 - 42, y0 + 82)], fill=RULE, width=1)

    # name
    d.text((x0 + 40, y0 + 98), "Priyansh Verma", font=name_f, fill=INK)
    d.text((x0 + 44, y0 + 232), "Machine learning & generative AI", font=role_f, fill=INK_2)
    d.line([(x0 + 44, y0 + 306), (x0 + 44 + 104, y0 + 306)], fill=STAMP, width=3)

    # footer facts
    d.text((x0 + 44, y0 + 326), "MCA (Generative AI) · Alliance University", font=meta_f, fill=INK_2)
    d.text((x0 + 44, y0 + 362), "Bengaluru, India", font=meta_f, fill=INK_3)
    d.text((x0 + 44, y0 + 408), "97.1% spam accuracy  ·  0.868 churn AUC  ·  8-route Flask app", font=mono_s, fill=INK_3)

    # stamp
    stamp = stamp_layer(["OPEN", "TO WORK"], font(MENLO, 30), STAMP, pad=20)
    img.paste(stamp, (x1 - stamp.width - 50, y1 - stamp.height - 54), stamp)

    img.save(IMG / "og.png", optimize=True)
    print("wrote", IMG / "og.png", img.size)


def make_icon(size):
    S = 4
    img = Image.new("RGBA", (size * S, size * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    n = size * S
    pad = int(n * 0.08)
    d.rounded_rectangle([pad, pad + int(n * 0.08), n - pad, n - pad], radius=int(n * 0.05), fill=CARD, outline=INK, width=max(2, int(n * 0.022)))
    # red file tab
    d.rectangle([int(n * 0.20), pad + int(n * 0.08), int(n * 0.52), pad + int(n * 0.22)], fill=STAMP)
    f = font(GEORGIA, int(n * 0.36))
    text = "PV"
    tw = d.textlength(text, font=f)
    d.text(((n - tw) / 2, n * 0.40), text, font=f, fill=INK)
    d.line([(int(n * 0.26), int(n * 0.76)), (int(n * 0.74), int(n * 0.76))], fill=RULE, width=max(1, int(n * 0.015)))
    return img.resize((size, size), Image.LANCZOS)


def make_icons():
    icon = make_icon(180)
    icon.save(IMG / "apple-touch-icon.png", optimize=True)
    make_icon(512).save(IMG / "icon-512.png", optimize=True)
    make_icon(192).save(IMG / "icon-192.png", optimize=True)
    ico = make_icon(48)
    ico.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("wrote icons")


if __name__ == "__main__":
    make_og()
    make_icons()

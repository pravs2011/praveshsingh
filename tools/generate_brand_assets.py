#!/usr/bin/env python3
"""One-time generator for site brand assets (SEO Sprint 3).

Creates:
  images/logo.png             512x512 square logo for schema.org Organization.logo
  images/favicon.ico          multi-size favicon (16/32/48)
  images/apple-touch-icon.png 180x180
  images/og-default.png       1200x630 social/OG card

Run from repo root:  python3 tools/generate_brand_assets.py
Requires: pillow  (pip3 install pillow)
"""
import os

from PIL import Image, ImageDraw, ImageFont

BG = (9, 11, 16)        # --bg #090b10
SURFACE = (16, 20, 29)  # --bg-surface #10141d
ACCENT = (99, 102, 241)  # --primary #6366f1
ACCENT_SOFT = (165, 180, 252)  # --indigo-300 #a5b4fc
TEXT = (240, 243, 248)  # --text #f0f3f8
MUTED = (154, 163, 181)  # --text-muted #9aa3b5

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "images")


def _font(size, bold=True):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/TTF/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def make_logo(size=512):
    """Square 'PS' monogram tile matching the inline SVG favicon."""
    img = Image.new("RGB", (size, size), BG)
    draw = ImageDraw.Draw(img)
    r = int(size * 0.22)
    rounded_rect(draw, (0, 0, size - 1, size - 1), r, BG)

    # subtle indigo ring
    pad = int(size * 0.045)
    rounded_rect(
        draw,
        (pad, pad, size - pad, size - pad),
        radius=int(r * 0.82),
        outline=ACCENT,
        width=max(2, size // 128),
    )

    font = _font(int(size * 0.44))
    text = "PS"
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - w) / 2 - bbox[0], (size - h) / 2 - bbox[1]), text, font=font, fill=ACCENT_SOFT)
    return img


def make_og_card(width=1200, height=630):
    """Social card: monogram tile + name, role and tagline."""
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    # dotted top-right accent glow imitation: layered rounded rects
    for i, alpha in enumerate(range(9, 2, -2)):
        pad = 48 + i * 26
        color = (
            ACCENT[0] + (TEXT[0] - ACCENT[0]) * alpha // 10,
            ACCENT[1] + (TEXT[1] - ACCENT[1]) * alpha // 10,
            ACCENT[2] + (TEXT[2] - ACCENT[2]) * alpha // 10,
        )
        rounded_rect(
            draw,
            (width - pad - 300, -160, width + 60, 460),
            radius=160,
            outline=color,
            width=2,
        )

    # left accent bar
    draw.rectangle((0, 0, 14, height), fill=ACCENT)

    # monogram tile
    tile = make_logo(220)
    img.paste(tile, (96, 118))

    x = 380
    name_font = _font(76)
    role_font = _font(40)
    tag_font = _font(30, bold=False)
    sub_font = _font(26, bold=False)

    draw.text((x, 150), "Pravesh Singh", font=name_font, fill=TEXT)
    draw.text((x, 258), "Founder & CTO, SoftEdge Technology Solutions", font=role_font, fill=ACCENT_SOFT)
    draw.text(
        (x, 356),
        "Healthcare platforms · Multi-tenant SaaS · Applied AI",
        font=tag_font,
        fill=MUTED,
    )

    # divider
    draw.line((x, 436, width - 96, 436), fill=(52, 58, 74), width=2)

    draw.text((x, 470), "praveshsingh.com", font=sub_font, fill=TEXT)
    draw.text((x, 516), "iCare · TaskEdge · ABDM & FHIR R4 engineering guides", font=sub_font, fill=MUTED)
    return img


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    logo = make_logo(512)
    logo.save(os.path.join(OUT_DIR, "logo.png"), optimize=True)

    # favicon.ico with 16/32/48 sizes
    icon_sizes = [(16, 16), (32, 32), (48, 48)]
    logo.save(
        os.path.join(OUT_DIR, "favicon.ico"),
        format="ICO",
        sizes=icon_sizes,
    )

    apple = make_logo(180)
    apple.save(os.path.join(OUT_DIR, "apple-touch-icon.png"), optimize=True)

    og = make_og_card()
    og.save(os.path.join(OUT_DIR, "og-default.png"), optimize=True)

    print("Generated in", os.path.abspath(OUT_DIR))
    for f in ("logo.png", "favicon.ico", "apple-touch-icon.png", "og-default.png"):
        p = os.path.join(OUT_DIR, f)
        print(f"  {f}: {os.path.getsize(p):,} bytes")


if __name__ == "__main__":
    main()

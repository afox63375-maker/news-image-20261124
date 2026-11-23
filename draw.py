#!/usr/bin/env python3
"""Render the Tuesday 24 November 2026 front page (entry.png).

Draws the whole broadsheet in code with Pillow primitives: the masthead,
stat strip, regional bar, weather strip, three illustrated leads, ten
illustrated cards, a dotted world map with numbered pins, the brief list
and the date-check box. No photographs, no downloaded assets, no network.
Run:  python3 draw.py   (writes entry.png next to this file)
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
CREAM = (246, 241, 227)
PAPER = (250, 246, 236)
INK = (24, 24, 28)
NAVY = (16, 32, 66)
RED = (178, 34, 34)
DARKRED = (140, 22, 22)
GOLD = (198, 148, 44)
GREY = (90, 86, 76)
LINE = (120, 110, 92)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)          # noqa: E731
SERIF_IT = lambda s: font("DejaVuSerif.ttf", s)            # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)                 # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)          # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, fill, max_w, leading=None):
    """Draw wrapped text; return the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, w, text, fill=RED):
    """Small red tag bar with white bold text, e.g. 'GURU NANAK JAYANTI'."""
    fnt = SANS_B(10)
    tw = draw.textlength(text, font=fnt)
    draw.rectangle([x, y, x + tw + 12, y + 16], fill=fill)
    draw.text((x + 6, y + 3), text, font=fnt, fill=(255, 255, 255))
    return tw + 12


def chip(draw, x, y, w, h, text, fill):
    """Small white-on-colour number chip used at a panel corner."""
    fnt = SANS_B(10)
    tw = draw.textlength(text, font=fnt)
    draw.rectangle([x, y, x + tw + 10, y + 16], fill=fill)
    draw.text((x + 5, y + 3), text, font=fnt, fill=(255, 255, 255))


def sun(draw, cx, cy, r, fill=(240, 180, 40)):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    for k in range(8):
        a = math.pi * k / 4
        x1, y1 = cx + int((r + 2) * math.cos(a)), cy + int((r + 2) * math.sin(a))
        x2, y2 = cx + int((r + 7) * math.cos(a)), cy + int((r + 7) * math.sin(a))
        draw.line([x1, y1, x2, y2], fill=fill, width=2)


def cloud(draw, x, y, s, fill=(255, 255, 255)):
    draw.ellipse([x, y, x + 16 * s, y + 10 * s], fill=fill)
    draw.ellipse([x + 8 * s, y - 5 * s, x + 24 * s, y + 8 * s], fill=fill)
    draw.ellipse([x + 16 * s, y, x + 32 * s, y + 10 * s], fill=fill)


def rain(draw, x, y, fill=(70, 120, 190)):
    for dx in (2, 9, 16):
        draw.line([x + dx, y + 12, x + dx - 2, y + 18], fill=fill, width=2)


def flame(draw, cx, base, h, fill=(255, 140, 0)):
    draw.polygon(
        [(cx, base - h), (cx + h * 0.38, base - h * 0.45),
         (cx + h * 0.16, base), (cx - h * 0.16, base),
         (cx - h * 0.38, base - h * 0.45)],
        fill=fill,
    )
    draw.polygon(
        [(cx, base - h * 0.55), (cx + h * 0.16, base - h * 0.2),
         (cx, base), (cx - h * 0.16, base - h * 0.2)],
        fill=(255, 210, 60),
    )


# ---------------------------------------------------------------- scenes
# Each painter fills the rectangle (x, y, x+w, y+h) with a literal scene
# for its story. All coordinates are relative to the rectangle.

def scene_temple(d, x, y, w, h):
    """Golden Temple at dusk: gold dome, lamps, still water."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 48, 96))
    for sx, sy in [(18, 14), (60, 8), (120, 18), (180, 10), (250, 16), (300, 8)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(24, 52, 84))
    d.rectangle([x, y + h * 0.62, x + w, y + h * 0.64], fill=(120, 140, 170))
    cx = x + w // 2
    d.rectangle([cx - 52, y + h * 0.30, cx + 52, y + h * 0.62], fill=(196, 148, 44))
    d.rectangle([cx - 62, y + h * 0.58, cx + 62, y + h * 0.64], fill=(150, 108, 30))
    d.polygon([(cx - 26, y + h * 0.30), (cx, y + h * 0.08),
               (cx + 26, y + h * 0.30)], fill=(226, 178, 66))
    d.ellipse([cx - 4, y + h * 0.02, cx + 4, y + h * 0.10], fill=(255, 214, 90))
    for dx in (-38, -14, 14, 38):
        d.rectangle([cx + dx - 3, y + h * 0.38, cx + dx + 3, y + h * 0.58],
                    fill=(30, 30, 40))
    for lx in range(x + 8, x + w - 8, 26):
        flame(d, lx + 6, y + h * 0.97, 9)
        d.ellipse([lx, y + h * 0.96, lx + 12, y + h * 0.99], fill=(120, 70, 20))
    d.polygon([(cx - 52, y + h * 0.64), (cx - 30, y + h * 0.80),
               (cx + 30, y + h * 0.80), (cx + 52, y + h * 0.64)],
              fill=(226, 178, 66))
    d.rectangle([cx - 40, y + h * 0.80, cx + 40, y + h * 0.86],
                fill=(150, 108, 30))


def scene_chip(d, x, y, w, h):
    """Nvidia: a glowing chip under a soaring green chart line."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 18, 34))
    for sx, sy in [(20, 12), (90, 20), (160, 8), (240, 16), (300, 10)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(140, 160, 200))
    pts = [(x + 6, y + h - 18), (x + 60, y + h - 30), (x + 110, y + h - 22),
           (x + 170, y + h - 44), (x + 230, y + h - 58), (x + 290, y + h - 84),
           (x + w - 6, y + 12)]
    d.line(pts, fill=(60, 220, 110), width=3)
    cx, cy = x + w // 2 + 30, y + h - 52
    d.rectangle([cx - 46, cy - 26, cx + 46, cy + 26], fill=(20, 40, 70),
                outline=(90, 140, 90), width=2)
    d.rectangle([cx - 26, cy - 14, cx + 26, cy + 14], fill=(40, 90, 50))
    d.text((cx - 20, cy - 9), "NVDA", font=SANS_B(12), fill=(180, 255, 190))
    for px in range(cx - 40, cx + 41, 13):
        d.line([px, cy - 34, px, cy - 26], fill=(150, 170, 190), width=2)
        d.line([px, cy + 26, px, cy + 34], fill=(150, 170, 190), width=2)
    for py in range(cy - 20, cy + 21, 13):
        d.line([cx - 54, py, cx - 46, py], fill=(150, 170, 190), width=2)
        d.line([cx + 46, py, cx + 54, py], fill=(150, 170, 190), width=2)


def scene_ballot(d, x, y, w, h):
    """Jakarta: ballot box, red-white flag, city towers."""
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 220))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(90, 110, 130))
    for bx, bw, bh in [(8, 26, 60), (44, 20, 84), (250, 30, 52), (288, 18, 70)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(70, 88, 108))
        for wy in range(y + h - bh + 8, y + h - 6, 14):
            d.rectangle([x + bx + 4, wy, x + bx + bw - 4, wy + 7],
                        fill=(240, 220, 120))
    d.rectangle([x + 108, y + h * 0.42, x + 222, y + h * 0.86],
                fill=(196, 40, 40))
    d.rectangle([x + 108, y + h * 0.42, x + 222, y + h * 0.60],
                fill=(255, 255, 255))
    d.rectangle([x + 128, y + h * 0.30, x + 202, y + h * 0.44],
                fill=(60, 40, 30))
    d.rectangle([x + 150, y + h * 0.34, x + 180, y + h * 0.40],
                fill=(20, 20, 26))
    d.line([x + 96, y + h * 0.44, x + 108, y + h * 0.30], fill=INK, width=2)
    d.line([x + 234, y + h * 0.44, x + 222, y + h * 0.30], fill=INK, width=2)
    d.ellipse([x + 232, y + h * 0.20, x + 258, y + h * 0.36], fill=(255, 255, 255))
    d.rectangle([x + 240, y + h * 0.28, x + 250, y + h * 0.52], fill=(200, 40, 40))
    d.rectangle([x + 240, y + h * 0.28, x + 250, y + h * 0.40], fill=(220, 40, 40))
    d.rectangle([x + 240, y + h * 0.40, x + 250, y + h * 0.52], fill=(255, 255, 255))


def scene_hill(d, x, y, w, h):
    """Karthigai Deepam: a hill at dusk, one great flame on top."""
    d.rectangle([x, y, x + w, y + h], fill=(52, 44, 84))
    d.ellipse([x + w - 42, y + 10, x + w - 14, y + 38], fill=(240, 220, 160))
    for sx, sy in [(14, 12), (70, 20), (140, 10), (200, 18)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    d.polygon([(x, y + h), (x + w * 0.42, y + h * 0.30), (x + w, y + h)],
              fill=(28, 34, 52))
    d.polygon([(x, y + h), (x + w * 0.62, y + h * 0.52), (x + w, y + h)],
              fill=(38, 46, 66))
    flame(d, x + int(w * 0.42), y + int(h * 0.32), 26)
    for lx in range(x + 10, x + w - 10, 24):
        flame(d, lx + 5, y + h - 4, 8)
        d.ellipse([lx, y + h - 5, lx + 10, y + h - 2], fill=(120, 70, 20))
    d.rectangle([x + 14, y + h * 0.78, x + 34, y + h * 0.86], fill=(200, 170, 90))
    d.rectangle([x + 16, y + h * 0.80, x + 32, y + h * 0.84], fill=(40, 40, 60))


def scene_court(d, x, y, w, h):
    """Warrant: courthouse columns, a gavel, a phone screen."""
    d.rectangle([x, y, x + w, y + h], fill=(210, 196, 168))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(120, 100, 80))
    for cx in (30, 70, 110, 150):
        d.rectangle([x + cx - 6, y + 18, x + cx + 6, y + h * 0.72],
                    fill=(240, 234, 214))
        d.rectangle([x + cx - 9, y + 14, x + cx + 9, y + 18], fill=(200, 190, 164))
    d.polygon([(x + 6, y + 14), (x + w // 2, y - 2), (x + w - 6, y + 14)],
              fill=(178, 34, 34))
    d.rectangle([x + 118, y + h * 0.34, x + 172, y + h * 0.78], fill=(24, 24, 30))
    d.rectangle([x + 122, y + h * 0.38, x + 168, y + h * 0.74],
                fill=(120, 180, 230))
    d.polygon([(x + 140, y + h * 0.44), (x + 140, y + h * 0.68),
               (x + 162, y + h * 0.56)], fill=(255, 255, 255))
    d.rectangle([x + 20, y + h * 0.60, x + 62, y + h * 0.68], fill=(120, 80, 40))
    d.line([x + 30, y + h * 0.60, x + 52, y + h * 0.42], fill=(90, 60, 30),
           width=5)
    d.rectangle([x + 44, y + h * 0.36, x + 60, y + h * 0.46], fill=(120, 80, 40))


def scene_startup(d, x, y, w, h):
    """Startups: rising bars, a rocket, a city skyline."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 60, 90))
    base = y + h - 14
    for i, bh in enumerate((18, 30, 26, 44, 58, 74)):
        bx = x + 12 + i * 26
        d.rectangle([bx, base - bh, bx + 18, base], fill=(60, 180, 120)
                    if i == 5 else (240, 180, 60))
    d.line([x + 8, base - 80, x + w - 10, base - 88], fill=(255, 255, 255),
           width=2)
    d.polygon([(x + w - 34, y + 8), (x + w - 22, y + 30), (x + w - 46, y + 30)],
              fill=(255, 255, 255))
    d.rectangle([x + w - 42, y + 30, x + w - 26, y + 52], fill=(220, 60, 60))
    d.polygon([(x + w - 42, y + 52), (x + w - 50, y + 62), (x + w - 42, y + 56)],
              fill=(255, 140, 0))
    d.polygon([(x + w - 26, y + 52), (x + w - 18, y + 62), (x + w - 26, y + 56)],
              fill=(255, 140, 0))
    d.ellipse([x + w - 38, y + 34, x + w - 30, y + 42], fill=(120, 200, 240))
    for bx, bw, bh in [(x + 8, 14, 26), (x + 168, 12, 34)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=(30, 40, 60))


def scene_flags(d, x, y, w, h):
    """India-Egypt: two flags, a handshake, a pyramid and a dome."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 180))
    d.polygon([(x + 8, y + h - 14), (x + 78, y + h * 0.30),
               (x + 148, y + h - 14)], fill=(210, 170, 90))
    d.ellipse([x + w - 40, y + h - 44, x + w - 8, y + h - 12],
              fill=(226, 178, 66))
    d.rectangle([x + w - 38, y + h - 46, x + w - 10, y + h - 40],
                fill=(150, 108, 30))
    for fx, cols in [(14, [(255, 153, 51), (255, 255, 255), (19, 136, 8)]),
                     (118, [(206, 17, 38), (255, 255, 255), (0, 0, 0)])]:
        for i, c in enumerate(cols):
            d.rectangle([x + fx, y + 10 + i * 12, x + fx + 62, y + 22 + i * 12],
                        fill=c)
        d.line([x + fx, y + 10, x + fx, y + 46], fill=(90, 70, 50), width=2)
    d.ellipse([x + 88, y + 52, x + 108, y + 72], fill=(240, 200, 150))
    d.ellipse([x + 108, y + 52, x + 128, y + 72], fill=(220, 170, 120))
    d.arc([x + 82, y + 44, x + 134, y + 84], 200, 340, fill=INK, width=3)


def scene_assembly(d, x, y, w, h):
    """Karnataka: assembly hall, an elephant, a ballot paper."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 190))
    d.rectangle([x, y + h * 0.66, x + w, y + h], fill=(110, 140, 90))
    d.rectangle([x + 14, y + 16, x + 96, y + h * 0.66], fill=(240, 234, 214))
    d.polygon([(x + 10, y + 16), (x + 55, y - 2), (x + 100, y + 16)],
              fill=(178, 34, 34))
    for cx in (28, 55, 82):
        d.rectangle([x + cx - 4, y + 26, x + cx + 4, y + h * 0.66],
                    fill=(200, 190, 164))
    d.ellipse([x + 118, y + h * 0.52, x + 178, y + h * 0.82], fill=(110, 110, 120))
    d.ellipse([x + 170, y + h * 0.56, x + 186, y + h * 0.72], fill=(110, 110, 120))
    d.rectangle([x + 178, y + h * 0.60, x + 190, y + h * 0.86], fill=(110, 110, 120))
    d.rectangle([x + 122, y + h * 0.80, x + 128, y + h * 0.96], fill=(90, 90, 100))
    d.rectangle([x + 160, y + h * 0.80, x + 166, y + h * 0.96], fill=(90, 90, 100))
    d.ellipse([x + 150, y + h * 0.56, x + 158, y + h * 0.62], fill=(255, 255, 255))
    d.rectangle([x + 112, y + 12, x + 158, y + 44], fill=(255, 255, 255),
                outline=(120, 120, 120))
    d.line([x + 118, y + 22, x + 152, y + 22], fill=(60, 60, 60), width=2)
    d.line([x + 118, y + 30, x + 146, y + 30], fill=(150, 150, 150), width=2)
    d.line([x + 118, y + 38, x + 152, y + 38], fill=(150, 150, 150), width=2)


def scene_hockey(d, x, y, w, h):
    """Hockey: green pitch, a stick, a ball, a 7-0 board."""
    d.rectangle([x, y, x + w, y + h], fill=(34, 130, 70))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(24, 100, 52))
    d.line([x, y + h * 0.55, x + w, y + h * 0.55], fill=(255, 255, 255),
           width=2)
    d.ellipse([x + w // 2 - 16, y + h // 2 - 8, x + w // 2 + 16,
               y + h // 2 + 8], fill=None, outline=(255, 255, 255), width=2)
    d.rectangle([x + 8, y + h - 34, x + w - 118, y + h - 12], fill=(16, 32, 66))
    d.text((x + 12, y + h - 31), "IND 7-0 THA", font=SANS_B(12),
           fill=(255, 255, 255))
    d.line([x + 120, y + h - 30, x + 150, y + h - 52], fill=(200, 160, 90),
           width=6)
    d.line([x + 150, y + h - 52, x + 168, y + h - 52], fill=(200, 160, 90),
           width=6)
    d.ellipse([x + 168, y + h - 58, x + 180, y + h - 46], fill=(255, 255, 255))
    d.ellipse([x + 96, y + h - 26, x + 106, y + h - 16], fill=(255, 255, 255))


def scene_squash(d, x, y, w, h):
    """Squash: court lines, a racket, a bouncing ball."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 120, 60))
    d.rectangle([x + 10, y + 8, x + w - 10, y + h - 8], fill=(240, 220, 190))
    d.line([x + 10, y + h * 0.42, x + w - 10, y + h * 0.42],
           fill=(178, 34, 34), width=2)
    d.line([x + w // 2, y + h * 0.42, x + w // 2, y + h - 8],
           fill=(178, 34, 34), width=2)
    d.line([x + 10, y + h * 0.62, x + w - 10, y + h * 0.62],
           fill=(120, 120, 120), width=1)
    d.ellipse([x + w - 66, y + h - 62, x + w - 26, y + h - 22],
              outline=(40, 40, 40), width=3)
    for xx in range(x + w - 62, x + w - 28, 8):
        d.line([xx, y + h - 58, xx, y + h - 26], fill=(40, 40, 40), width=1)
    for yy in range(y + h - 58, y + h - 24, 8):
        d.line([x + w - 62, yy, x + w - 30, yy], fill=(40, 40, 40), width=1)
    d.line([x + w - 46, y + h - 22, x + w - 30, y + 14], fill=(120, 70, 30),
           width=4)
    d.ellipse([x + 26, y + 16, x + 38, y + 28], fill=(20, 20, 20))
    d.ellipse([x + 44, y + 34, x + 52, y + 42], fill=(20, 20, 20))
    d.ellipse([x + 62, y + 52, x + 68, y + 58], fill=(20, 20, 20))


def scene_cinema(d, x, y, w, h):
    """IFFI: a cinema screen, a film reel, a clapperboard."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 40))
    d.rectangle([x + 16, y + 10, x + w - 16, y + h * 0.62], fill=(240, 230, 200))
    d.polygon([(x + w // 2 - 40, y + 16), (x + w // 2 + 40, y + 16),
               (x + w // 2 + 26, y + h * 0.56), (x + w // 2 - 26, y + h * 0.56)],
              fill=(178, 34, 34))
    d.ellipse([x + w // 2 - 10, y + h * 0.24, x + w // 2 + 10,
               y + h * 0.44], fill=(240, 230, 200))
    d.rectangle([x + 14, y + h * 0.70, x + 74, y + h * 0.94], fill=(40, 40, 52),
                outline=(200, 200, 200))
    d.rectangle([x + 14, y + h * 0.70, x + 74, y + h * 0.80], fill=(240, 240, 240))
    for i in range(4):
        d.rectangle([x + 18 + i * 15, y + h * 0.70, x + 28 + i * 15,
                     y + h * 0.80], fill=(30, 30, 40))
    d.line([x + 18, y + h * 0.86, x + 70, y + h * 0.86], fill=(255, 255, 255),
           width=2)
    d.ellipse([x + w - 52, y + h * 0.68, x + w - 12, y + h * 0.98],
              outline=(200, 200, 200), width=3)
    d.ellipse([x + w - 38, y + h * 0.80, x + w - 26, y + h * 0.88],
              outline=(200, 200, 200), width=2)
    for a in range(0, 360, 60):
        r = math.radians(a)
        d.ellipse([x + w - 32 + int(12 * math.cos(r)) - 2,
                   y + int(h * 0.83) + int(12 * math.sin(r)) - 2,
                   x + w - 32 + int(12 * math.cos(r)) + 2,
                   y + int(h * 0.83) + int(12 * math.sin(r)) + 2],
                  fill=(200, 200, 200))


def scene_satellite(d, x, y, w, h):
    """TRISHNA: a satellite over a blue Earth arc, stars above."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 16, 40))
    for sx, sy in [(16, 12), (60, 26), (120, 10), (170, 22), (30, 44),
                   (150, 44)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    d.ellipse([x - 30, y + h * 0.52, x + w + 30, y + h * 1.35],
              fill=(30, 90, 160))
    d.ellipse([x + 30, y + h * 0.62, x + 90, y + h * 0.86], fill=(60, 140, 80))
    d.ellipse([x + 120, y + h * 0.72, x + 170, y + h * 0.92],
              fill=(60, 140, 80))
    d.arc([x - 30, y + h * 0.52, x + w + 30, y + h * 1.35], 180, 360,
          fill=(140, 200, 240), width=2)
    d.rectangle([x + w // 2 - 26, y + 26, x + w // 2 + 26, y + 52],
                fill=(200, 200, 210), outline=(255, 255, 255))
    d.rectangle([x + w // 2 - 52, y + 32, x + w // 2 - 26, y + 46],
                fill=(40, 80, 180))
    d.rectangle([x + w // 2 + 26, y + 32, x + w // 2 + 52, y + 46],
                fill=(40, 80, 180))
    d.polygon([(x + w // 2, y + 14), (x + w // 2 + 8, y + 26),
               (x + w // 2 - 8, y + 26)], fill=(240, 200, 60))
    d.line([x + w // 2, y + 52, x + w // 2 + 10, y + 66], fill=(255, 255, 255),
           width=2)


def scene_fog(d, x, y, w, h):
    """IMD weather: fog banks, a rain cloud, an umbrella."""
    d.rectangle([x, y, x + w, y + h], fill=(120, 140, 160))
    cloud(d, x + 12, y + 12, 1, fill=(70, 80, 100))
    rain(d, x + 16, y + 12, fill=(40, 80, 160))
    for i, yy in enumerate((34, 52, 70)):
        d.rectangle([x + 6, y + yy, x + w - 6 - i * 14, y + yy + 10],
                    fill=(220, 224, 228))
    d.rectangle([x + w - 62, y + 34, x + w - 14, y + 52], fill=(240, 80, 80))
    d.polygon([(x + w - 62, y + 52), (x + w - 14, y + 52),
               (x + w - 38, y + 34)], fill=(240, 80, 80))
    d.line([x + w - 38, y + 52, x + w - 38, y + 82], fill=(60, 40, 30),
           width=3)
    d.line([x + w - 38, y + 82, x + w - 28, y + 82], fill=(60, 40, 30),
           width=3)
    d.rectangle([x + 12, y + h - 22, x + 60, y + h - 8], fill=(30, 40, 60))
    d.rectangle([x + 66, y + h - 22, x + 92, y + h - 8], fill=(200, 180, 60))


# ------------------------------------------------------------------- map
# Land is approximated by a set of ellipses in lon/lat space; dots are
# stamped on a grid wherever they fall inside one. Rough but readable.

LAND = [
    # (lon centre, lat centre, lon radius, lat radius)
    (-100, 50, 26, 16), (-96, 32, 18, 12), (-102, 18, 8, 8),   # N America
    (-60, -12, 12, 20), (-70, -30, 7, 10),                     # S America
    (10, 52, 14, 10), (24, 62, 10, 8), (2, 44, 8, 6),          # Europe
    (18, 6, 14, 16), (30, -8, 12, 16), (44, -22, 8, 8),        # Africa
    (45, 28, 10, 10), (78, 24, 16, 12), (100, 46, 30, 14),     # Asia
    (108, 14, 10, 10), (122, 30, 8, 10), (140, 38, 6, 8),      # E Asia
    (134, -24, 14, 8), (150, -36, 8, 6), (172, -40, 4, 4),     # Oceania
    (140, -70, 40, 8),                                          # Antarctica
]

REGION_COLOURS = {
    "APAC": (58, 110, 60),
    "EUROPE": (52, 96, 158),
    "MIDDLE EAST": (178, 34, 34),
    "AMERICAS": (118, 84, 150),
    "WORLD": (70, 70, 70),
}

# (story number, lon, lat, region, dx, dy) — dx/dy are pixel nudges so
# pins that share a city do not sit on top of each other.
PINS = [
    (1, 74.9, 31.6, "APAC", 0, 0), (2, -122.0, 37.4, "AMERICAS", 0, 0),
    (3, 106.8, -6.2, "APAC", 0, 0), (4, 78.1, 9.9, "APAC", 0, 0),
    (5, 77.2, 28.6, "APAC", 0, 0), (6, 77.6, 28.4, "APAC", 18, -14),
    (7, 31.2, 30.0, "MIDDLE EAST", 0, 0), (8, 77.6, 13.0, "APAC", 0, 0),
    (9, 77.0, 28.8, "APAC", -18, -10), (10, 77.4, 28.2, "APAC", 16, 12),
    (11, 74.0, 15.3, "APAC", 0, 0), (12, 2.3, 48.9, "EUROPE", 12, 8),
    (13, 76.8, 28.9, "APAC", -16, 12), (29, 21.0, 52.2, "EUROPE", 10, -8),
    (30, 13.4, 52.5, "EUROPE", -10, 8), (31, 23.7, 38.0, "EUROPE", 0, 10),
    (32, -77.0, 38.9, "WORLD", 0, 0), (33, -0.1, 51.5, "MIDDLE EAST", -12, -8),
    (34, 43.0, 12.6, "MIDDLE EAST", 0, 0), (35, -58.4, -34.6, "AMERICAS", 0, 0),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 224, 200))
    lon0, lon1, lat0, lat1 = -168, 192, 84, -58
    step = 7
    gx = x + 4
    while gx < x + w - 4:
        gy = y + 4
        while gy < y + h - 4:
            lon = lon0 + (gx - x) / w * (lon1 - lon0)
            lat = lat0 - (gy - y) / h * (lat0 - lat1)
            on_land = any(
                ((lon - cl) / rl) ** 2 + ((lat - ca) / ra) ** 2 <= 1
                for cl, ca, rl, ra in LAND)
            if on_land:
                d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1],
                          fill=(178, 158, 110))
            gy += step
        gx += step
    for num, lon, lat, region, dx, dy in PINS:
        px = x + (lon - lon0) / (lon1 - lon0) * w + dx
        py = y + (lat0 - lat) / (lat0 - lat1) * h + dy
        col = REGION_COLOURS[region]
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col,
                  outline=(255, 255, 255), width=1)
        fnt = SANS_B(8)
        tw = d.textlength(str(num), font=fnt)
        d.text((px - tw / 2, py - 5), str(num), font=fnt,
               fill=(255, 255, 255))


# ------------------------------------------------------------------ page

LEADS = [
    dict(num=1, tag="GURU NANAK JAYANTI", tag2="557th PRAKASH UTSAV",
         place="AMRITSAR, INDIA · FAITH", scene=scene_temple,
         head="Sikhs mark Guru Nanak's 557th birth anniversary",
         deck="Golden Temple glows as devotees gather; Punjab asks PM to "
              "reopen Kartarpur for the day. (ObserverVoice)"),
    dict(num=2, tag="NVIDIA: HUANG BACK", tag2="+13% CHIP STOCKS",
         place="SANTA CLARA, US · MARKETS", scene=scene_chip,
         head="Nvidia reinstates Jensen Huang as chief executive",
         deck="Board votes unanimously after US officials see no security "
              "risk; chip stocks jump 13%. (Causa Markets, Newsreel)"),
    dict(num=3, tag="INDONESIA: VP PICKS", tag2="EX-FM + AGRI MINISTER",
         place="JAKARTA, INDONESIA · POLITICS", scene=scene_ballot,
         head="Indonesia names its vice-presidential candidates",
         deck="Ex-foreign minister and agriculture minister put forward as "
              "the race takes shape. (Nikkei Asia)"),
]

CARDS = [
    dict(num=4, tag="KARTHIGAI DEEPAM", place="MADURAI, INDIA",
         scene=scene_hill,
         head="Hilltop lamp lit for Karthigai Deepam"),
    dict(num=5, tag="WARRANT ISSUED", place="NEW DELHI, INDIA",
         scene=scene_court,
         head="Court issues warrant for Dhruv Rathee"),
    dict(num=6, tag="STARTUP BOOM", place="NEW DELHI, INDIA",
         scene=scene_startup,
         head="Startups grow 52%; 2.23 lakh recognised"),
    dict(num=7, tag="INDIA–EGYPT PACT", place="NEW DELHI / CAIRO",
         scene=scene_flags,
         head="India, Egypt ease startup entry"),
    dict(num=8, tag="MLA RESIGNS", place="BENGALURU, INDIA",
         scene=scene_assembly,
         head="Karnataka MLA quits over elephant row"),
    dict(num=9, tag="HOCKEY 7–0", place="INDIA · SPORT",
         scene=scene_hockey,
         head="India women rout Thailand 7–0"),
    dict(num=10, tag="SQUASH TITLES", place="INDIA · SPORT",
         scene=scene_squash,
         head="Abhay, Akanksha win squash crowns"),
    dict(num=11, tag="IFFI GOA", place="GOA, INDIA",
         scene=scene_cinema,
         head="Ten films vie for Gandhi Medal"),
    dict(num=12, tag="TRISHNA SATELLITE", place="INDIA–FRANCE",
         scene=scene_satellite,
         head="India, France deepen space ties"),
    dict(num=13, tag="FOG + RAIN", place="NEW DELHI, INDIA",
         scene=scene_fog,
         head="IMD warns of fog, heavy rain"),
]

BRIEFS = [
    (14, "SC: Centre must answer on anti-defection law PIL"),
    (15, "SC sends Saharanpur mosque plea to Allahabad HC"),
    (16, "SC hears Delhi air, Bengal voter-roll cases today"),
    (17, "Punjab CM urges PM: reopen Kartarpur Corridor"),
    (18, "Hyderabad Sikhs celebrate Gurpurab with kirtans"),
    (19, "UGC NET Dec city slip expected today"),
    (20, "Delhi nursery admissions open for 2027–28"),
    (21, "Punjab Board sets 2027 exam dates"),
    (22, "Maharashtra NEET PG Round 2 choice filling opens"),
    (23, "BHEL opens 415 trainee posts; apply by Dec 28"),
    (24, "PM announces Rs 2 lakh aid for Kutch victims"),
    (25, "CJI: law students must do legal aid; AI rules due"),
    (26, "Odisha clears Rs 249-crore Cyber Command Centre"),
    (27, "Indian team demos drone link over 1,000 km"),
    (28, "AI-assisted work claims Riemann breakthrough"),
    (29, "NATO sends early-warning jets to Poland"),
    (30, "Germany pledges $300m military aid for Ukraine"),
    (31, "Athens reopens Acropolis Museum after 20 years"),
    (32, "US imposes new Iran-related sanctions"),
    (33, "Gaza children arrive in UK for treatment"),
    (34, "Houthis seize control of Bab el-Mandeb strait"),
    (35, "Pope Leo XIV meets Milei on South America tour"),
]

STATS = [
    ("557", "Guru Nanak Prakash Utsav"),
    ("+13%", "chip stocks jump on Huang"),
    ("52%", "growth in Indian startups"),
    ("7–0", "India women beat Thailand"),
    ("2.23 LAKH", "recognised startups"),
    ("415", "BHEL trainee posts open"),
]

REGIONS = [
    ("ASIA-PACIFIC 26", 26, (58, 110, 60)),
    ("EUROPE 3", 3, (52, 96, 158)),
    ("MIDDLE EAST 2", 2, (178, 34, 34)),
    ("AMERICAS 2", 2, (118, 84, 150)),
    ("WORLD 2", 2, (70, 70, 70)),
]

WEATHER = [
    ("AMRITSAR", "27/9 C", "sun"),
    ("NEW DELHI", "25/11 C", "sun"),
    ("MADURAI", "33/24 C", "storm"),
    ("JAKARTA", "33/26 C", "storm"),
    ("SYDNEY", "22/17 C", "rain"),
    ("LONDON", "9/3 C", "cloud"),
]


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=4)

    # masthead banner
    d.rectangle([4, 4, W - 5, 28], fill=NAVY)
    d.text((12, 9), "THE WORLD IN ONE DAY", font=SANS_B(13),
           fill=(255, 255, 255))
    right = "35 STORIES · 5 REGIONS · EVERY ONE DATED TUESDAY 24 NOVEMBER 2026"
    d.text((W - 12 - d.textlength(right, font=SANS_B(11)), 10), right,
           font=SANS_B(11), fill=(240, 200, 90))

    # giant date headline
    d.text((10, 34), "Tuesday 24 November 2026", font=SERIF(56), fill=INK)
    d.text((12, 100),
           "Huang back at Nvidia as chips soar 13% · Sikhs mark Guru Nanak's "
           "557th · Jakarta names its vice-presidential picks",
           font=SERIF_IT(14), fill=RED)

    # stat strip
    sx, sy, sw, sh = 10, 122, 167, 48
    for i, (num, label) in enumerate(STATS):
        x0 = sx + i * sw
        d.rectangle([x0, sy, x0 + sw - 6, sy + sh], fill=PAPER,
                    outline=LINE)
        d.text((x0 + 8, sy + 4), num, font=SANS_B(22), fill=RED)
        para(d, x0 + 8, sy + 30, label, SANS(9), GREY, sw - 16, leading=11)

    # regional count bar: legend line above, plain segments below
    rx, ry, rw, rh = 10, 188, 1004, 14
    lx = 10
    for label, n, col in REGIONS:
        d.rectangle([lx, 174, lx + 10, 184], fill=col)
        d.text((lx + 14, 174), label, font=SANS_B(10), fill=INK)
        lx += 14 + d.textlength(label, font=SANS_B(10)) + 22
    total = sum(n for _, n, _ in REGIONS)
    cx = rx
    for label, n, col in REGIONS:
        seg = int(rw * n / total)
        d.rectangle([cx, ry, cx + seg - 1, ry + rh], fill=col)
        cx += seg

    # weather strip
    wx, wy = 10, 208
    d.text((wx, wy + 2), "TUESDAY WEATHER", font=SANS_B(11), fill=RED)
    d.text((wx + 128, wy + 2), "Forecast, high/low", font=SANS(10), fill=GREY)
    cell = 144
    for i, (city, temp, kind) in enumerate(WEATHER):
        x0 = wx + 128 + 8 + i * cell
        d.rectangle([x0, wy, x0 + cell - 6, wy + 20], fill=PAPER,
                    outline=LINE)
        ix = x0 + 5
        if kind == "sun":
            sun(d, ix + 7, wy + 10, 5)
        elif kind == "storm":
            cloud(d, ix, wy + 4, 1, fill=(120, 120, 130))
            rain(d, ix, wy + 2, fill=(70, 120, 190))
        elif kind == "rain":
            cloud(d, ix, wy + 4, 1, fill=(150, 150, 160))
            rain(d, ix, wy + 2)
        else:
            cloud(d, ix, wy + 4, 1, fill=(150, 150, 160))
        d.text((x0 + 26, wy + 4), city, font=SANS_B(10), fill=INK)
        tw = d.textlength(temp, font=SANS_B(10))
        d.text((x0 + cell - 6 - tw - 4, wy + 4), temp, font=SANS_B(10),
               fill=INK)

    # ---- three illustrated leads
    lx, ly = 10, 234
    lw, gap = 330, 7
    for i, lead in enumerate(LEADS):
        x0 = lx + i * (lw + gap)
        panel = Image.new("RGB", (lw, 104))
        pd = ImageDraw.Draw(panel)
        lead["scene"](pd, 0, 0, lw, 104)
        img.paste(panel, (x0, ly))
        d.rectangle([x0, ly, x0 + lw, ly + 104], outline=INK, width=1)
        kicker(d, x0, ly, lw, lead["tag"])
        tw = d.textlength(lead["tag2"], font=SANS_B(10))
        chip(d, x0 + lw - tw - 16, ly, 40, 16, lead["tag2"], NAVY)
        d.text((x0, ly + 108), lead["place"], font=SANS_B(10), fill=RED)
        y = para(d, x0, ly + 122, lead["head"], SERIF(17), INK, lw,
                 leading=20)
        para(d, x0, y + 2, lead["deck"], SANS(10), GREY, lw, leading=13)

    # ---- ten illustrated cards, two rows of five
    cx0, cy0 = 10, 430
    cw, ch, cgap = 195, 78, 7
    for row in range(2):
        for col in range(5):
            card = CARDS[row * 5 + col]
            x0 = cx0 + col * (cw + cgap)
            y0 = cy0 + row * 122
            panel = Image.new("RGB", (cw, ch))
            pd = ImageDraw.Draw(panel)
            card["scene"](pd, 0, 0, cw, ch)
            img.paste(panel, (x0, y0))
            d.rectangle([x0, y0, x0 + cw, y0 + ch], outline=INK, width=1)
            kicker(d, x0, y0, cw, card["tag"])
            chip(d, x0 + cw - 20, y0, 16, 16, str(card["num"]), NAVY)
            d.text((x0, y0 + ch + 4), card["place"], font=SANS_B(9),
                   fill=RED)
            para(d, x0, y0 + ch + 16, card["head"], SANS_B(11), INK, cw,
                 leading=13)

    # ---- map + brief list
    my = 680
    d.text((10, my), "WHERE IT HAPPENED", font=SANS_B(12), fill=INK)
    d.text((168, my + 2), "pins match story numbers", font=SERIF_IT(10),
           fill=GREY)
    d.text((316, my), "ALSO ON TUESDAY 24 NOVEMBER — 22 MORE STORIES",
           font=SANS_B(12), fill=INK)
    d.line([10, my + 16, 1014, my + 16], fill=LINE, width=1)
    draw_map(d, 10, my + 22, 292, 238)
    d.rectangle([10, my + 22, 302, my + 260], outline=INK, width=1)

    bx, by = 316, my + 22
    col_w = 348
    for i, (num, text) in enumerate(BRIEFS):
        col = i // 11
        row = i % 11
        x0 = bx + col * (col_w + 4)
        y0 = by + row * 21
        d.text((x0, y0), str(num), font=SANS_B(10), fill=RED)
        para(d, x0 + 24, y0, text, SANS(10), INK, col_w - 24, leading=12)

    # ---- date check box
    dy = 946
    d.rectangle([10, dy, 1014, 990], outline=RED, width=2)
    d.text((18, dy + 5), "DATE CHECK", font=SANS_B(11), fill=RED)
    para(d, 18, dy + 21,
         "Wires read to 21:00 UTC, Mon 23 Nov 2026; every story was "
         "reported or still developing on Tue 24 Nov in at least one "
         "time zone. Left out as other days' news: COP31 collapse, "
         "Tajikistan ICC exit, Puigdemont charges dropped, Alcaraz ATP "
         "win, Ukraine warship claim (23 Nov); Modi–Shah talks, "
         "Saryu-Kamala flag-off, Bisleri case, BepiColombo orbit (21–23 Nov).",
         SANS(10), INK, 980, leading=13)

    # footer
    d.text((10, 996),
           "Sources: Reuters, BBC, Guardian, Al Jazeera, Nikkei Asia, "
           "Newsreel, Jagran Josh, ObserverVoice, IMD, weather.com. "
           "Pictures and map drawn in code.",
           font=SANS(9), fill=GREY)
    d.text((W - 12 - d.textlength("TUESDAY 24 NOVEMBER 2026 · ONE PAGE",
                                  font=SANS_B(9)), 996),
           "TUESDAY 24 NOVEMBER 2026 · ONE PAGE", font=SANS_B(9), fill=GREY)

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()

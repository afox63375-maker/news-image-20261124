#!/usr/bin/env python3
"""Render the one-page world-news front page for Tuesday 24 November 2026.

Build-time renderer (Pillow is fine here): draws every picture, the
dotted world map and every icon in code, then writes entry.png next to
this script. The output is deterministic: same input, same bytes.
Run:  python3 draw.py [output-path]
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas
W, H = 1024, 1024
CREAM = (247, 241, 222)
CREAM_DARK = (238, 230, 203)
INK = (26, 26, 26)
NAVY = (18, 32, 66)
NAVY_LIGHT = (38, 58, 104)
RED = (178, 34, 34)
RED_DARK = (139, 22, 22)
GOLD = (201, 162, 39)
GREY = (90, 86, 76)
LINE = (60, 52, 40)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"

# ---------------------------------------------------------------- content
STATS = [
    ("557", "Guru Nanak Prakash Utsav"),
    ("+31%", "Nvidia shares on return"),
    ("52%", "growth in Indian startups"),
    ("48 TEAMS", "first 48-team Women's WC"),
    ("24 DEAD", "Indonesia factory fire"),
    ("415", "BHEL trainee posts open"),
]

REGIONS = [
    ("ASIA-PACIFIC", 25, (31, 122, 61)),
    ("EUROPE", 3, (38, 58, 104)),
    ("M.EAST", 2, (178, 34, 34)),
    ("AMER.", 2, (122, 82, 160)),
    ("WORLD", 3, (90, 90, 90)),
]

WEATHER = [
    ("AMRITSAR", "27/9", "sun"),
    ("NEW DELHI", "25/11", "sun"),
    ("MADURAI", "33/24", "storm"),
    ("JAKARTA", "33/26", "storm"),
    ("SYDNEY", "22/17", "cloud"),
    ("LONDON", "9/3", "cloud"),
]

LEADS = [
    {
        "kicker": "GURU NANAK JAYANTI",
        "chip": "557th PRAKASH UTSAV",
        "place": "AMRITSAR, INDIA · FAITH",
        "headline": "Sikhs mark Guru Nanak's 557th birth anniversary",
        "deck": "Golden Temple glows as devotees gather; Punjab asks PM to "
                "reopen Kartarpur. (ObserverVoice)",
        "scene": "temple",
    },
    {
        "kicker": "NVIDIA: HUANG BACK",
        "chip": "+31% SHARES",
        "place": "SANTA CLARA, US · MARKETS",
        "headline": "Nvidia reinstates Jensen Huang as chief executive",
        "deck": "Board votes unanimously after US officials see no security "
                "risk; shares surge 31%. (Morningstar)",
        "scene": "chip",
    },
    {
        "kicker": "INDONESIA: VP PICKS",
        "chip": "EX-FM + AGRI MINISTER",
        "place": "JAKARTA, INDONESIA · POLITICS",
        "headline": "Indonesia names its vice-presidential picks",
        "deck": "Ex-foreign minister Sugiono and agriculture minister Amran "
                "put forward; MPR votes Dec 11. (Reuters)",
        "scene": "jakarta",
    },
]

CARDS = [
    {
        "kicker": "KARTHIGAI DEEPAM", "num": 4,
        "place": "MADURAI, INDIA",
        "headline": "Hilltop lamp lit for Karthigai Deepam",
        "scene": "lamp",
    },
    {
        "kicker": "BAIL GRANTED", "num": 5,
        "place": "NEW DELHI, INDIA",
        "headline": "SC grants bail to Godhra convict on medical grounds",
        "scene": "court",
    },
    {
        "kicker": "STARTUP BOOM", "num": 6,
        "place": "NEW DELHI, INDIA",
        "headline": "Startups grow 52%; 2.23 lakh recognised",
        "scene": "startup",
    },
    {
        "kicker": "INDIA–EGYPT PACT", "num": 7,
        "place": "NEW DELHI / CAIRO",
        "headline": "India, Egypt ease startup entry",
        "scene": "flags",
    },
    {
        "kicker": "MLA RESIGNS", "num": 8,
        "place": "BENGALURU, INDIA",
        "headline": "Karnataka MLA quits over elephant row",
        "scene": "podium",
    },
    {
        "kicker": "WOMEN'S WORLD CUP", "num": 9,
        "place": "ZURICH, SWITZERLAND",
        "headline": "FIFA names 2031 and 2035 hosts",
        "scene": "fifa",
    },
    {
        "kicker": "HOCKEY TODAY", "num": 10,
        "place": "BHOPAL, INDIA",
        "headline": "India women face China in ACT clash",
        "scene": "hockey",
    },
    {
        "kicker": "IFFI GOA", "num": 11,
        "place": "GOA, INDIA",
        "headline": "Ten films vie for Gandhi Medal",
        "scene": "film",
    },
    {
        "kicker": "TRISHNA SATELLITE", "num": 12,
        "place": "INDIA–FRANCE",
        "headline": "India, France deepen space ties",
        "scene": "satellite",
    },
    {
        "kicker": "FOG & RAIN", "num": 13,
        "place": "NEW DELHI, INDIA",
        "headline": "IMD warns of fog, heavy rain",
        "scene": "fog",
    },
]

BRIEFS = [
    "SC: Centre must answer on anti-defection PIL",
    "SC sends Saharanpur mosque plea to Allahabad HC",
    "SC hears Delhi air and Bengal voter-roll cases",
    "Punjab CM urges PM to reopen Kartarpur Corridor",
    "Hyderabad Sikhs celebrate Gurpurab with kirtans",
    "Indonesia confirms 24 dead in factory fire",
    "Delhi nursery admissions open for 2027–28",
    "Punjab Board sets 2027 exam dates",
    "Maharashtra NEET PG Round 2 choice filling opens",
    "BHEL opens 415 trainee posts; apply by Dec 28",
    "PM announces Rs 2 lakh aid for Kutch victims",
    "CJI: law students must do legal aid; AI rules due",
    "Odisha clears Rs 249-crore Cyber Command Centre",
    "Indian team demos drone link over 1,000 km",
    "AI-assisted work claims Riemann breakthrough",
    "NATO sends early-warning jets to Poland",
    "Germany pledges $300m military aid for Ukraine",
    "Athens reopens Acropolis Museum after 20 years",
    "US imposes new Iran-related sanctions",
    "Gaza children arrive in UK for treatment",
    "Houthis seize control of Bab el-Mandeb strait",
    "Pope Leo XIV meets Milei on South America tour",
]

# story number -> (lon, lat, display offset dx, dy) for the map pins
PINS = {
    1: (74.9, 31.6, -18, -14),
    2: (-122.0, 37.4, 0, 0),
    3: (106.8, -6.2, 0, 0),
    4: (78.1, 9.9, -16, 14),
    5: (77.2, 28.6, -20, -4),
    6: (77.2, 28.6, 16, -12),
    7: (31.2, 30.0, 0, 0),
    8: (77.6, 13.0, -22, 4),
    9: (8.5, 47.4, 0, 0),
    10: (77.4, 23.3, 14, 0),
    11: (74.1, 15.3, -8, 18),
    12: (2.4, 48.9, 0, 0),
    13: (77.2, 28.6, 18, 10),
}

# ---------------------------------------------------------------- helpers
class Page:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), CREAM)
        self.d = ImageDraw.Draw(self.img)

    def wrap(self, text, fname, size, max_w):
        f = font(fname, size)
        words, lines, cur = text.split(), [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if self.d.textlength(trial, font=f) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines, f

    def para(self, x, y, text, fname, size, max_w, fill, leading=None):
        lines, f = self.wrap(text, fname, size, max_w)
        lh = leading or int(size * 1.22)
        for ln in lines:
            self.d.text((x, y), ln, font=f, fill=fill)
            y += lh
        return y

    def badge(self, x, y, text, size=11, bg=RED, fg=(255, 255, 255)):
        f = font(SANS_B, size)
        tw = self.d.textlength(text, font=f)
        pad = 6
        self.d.rectangle([x, y, x + tw + pad * 2, y + size + 8], fill=bg)
        self.d.text((x + pad, y + 3), text, font=f, fill=fg)
        return tw + pad * 2

    def num_chip(self, x, y, num, r=9):
        self.d.ellipse([x - r, y - r, x + r, y + r], fill=NAVY,
                       outline=(255, 255, 255), width=1)
        f = font(SANS_B, 11)
        t = str(num)
        tw = self.d.textlength(t, font=f)
        self.d.text((x - tw / 2, y - 6), t, font=f, fill=(255, 255, 255))


def weather_icon(d, x, y, kind, s=16):
    """Tiny sun / cloud / storm glyph, drawn with primitives."""
    if kind == "sun":
        d.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], fill=GOLD,
                  outline=(180, 130, 20), width=1)
        for k in range(8):
            import math
            a = k * math.pi / 4
            x1 = x + s / 2 + math.cos(a) * (s / 2 + 1)
            y1 = y + s / 2 + math.sin(a) * (s / 2 + 1)
            x2 = x + s / 2 + math.cos(a) * (s / 2 + 4)
            y2 = y + s / 2 + math.sin(a) * (s / 2 + 4)
            d.line([x1, y1, x2, y2], fill=GOLD, width=2)
    elif kind == "cloud":
        d.ellipse([x + 1, y + 5, x + 9, y + 12], fill=(120, 125, 135))
        d.ellipse([x + 6, y + 2, x + 14, y + 12], fill=(120, 125, 135))
        d.ellipse([x + 10, y + 6, x + s, y + 12], fill=(120, 125, 135))
        d.rectangle([x + 2, y + 9, x + s - 1, y + 13], fill=(120, 125, 135))
    else:  # storm
        d.ellipse([x + 1, y + 2, x + 9, y + 9], fill=(90, 95, 110))
        d.ellipse([x + 6, y + 0, x + 14, y + 9], fill=(90, 95, 110))
        d.rectangle([x + 2, y + 6, x + s - 1, y + 10], fill=(90, 95, 110))
        d.line([x + 7, y + 10, x + 4, y + 15], fill=GOLD, width=2)
        d.line([x + 12, y + 10, x + 9, y + 15], fill=GOLD, width=2)


# ---------------------------------------------------------------- scenes
def scene_temple(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(16, 22, 54))
    for sx, sy in [(0.12, 0.2), (0.3, 0.1), (0.55, 0.18), (0.78, 0.08),
                   (0.9, 0.22), (0.42, 0.3), (0.66, 0.28)]:
        d.ellipse([x0 + (x1 - x0) * sx - 1, y0 + (y1 - y0) * sy - 1,
                   x0 + (x1 - x0) * sx + 1, y0 + (y1 - y0) * sy + 1],
                  fill=(255, 240, 180))
    w, h = x1 - x0, y1 - y0
    cx = x0 + w / 2
    wy = y0 + h * 0.62  # waterline
    d.rectangle([x0, wy, x1, y1], fill=(10, 28, 66))
    d.rectangle([cx - w * 0.16, wy - h * 0.30, cx + w * 0.16, wy],
                fill=(212, 175, 55))
    d.rectangle([cx - w * 0.20, wy - h * 0.34, cx + w * 0.20, wy - h * 0.30],
                fill=(212, 175, 55))
    d.ellipse([cx - w * 0.09, wy - h * 0.52, cx + w * 0.09, wy - h * 0.30],
              fill=(232, 196, 82))
    d.rectangle([cx - 2, wy - h * 0.62, cx + 2, wy - h * 0.52],
                fill=(232, 196, 82))
    d.rectangle([cx - w * 0.24, wy, cx + w * 0.24, wy + 3],
                fill=(170, 135, 40))
    for i in range(7):
        fx = x0 + w * (0.08 + i * 0.14)
        d.ellipse([fx - 3, y1 - 12, fx + 3, y1 - 6], fill=(255, 150, 40))
        d.ellipse([fx - 1.5, y1 - 16, fx + 1.5, y1 - 11],
                  fill=(255, 220, 120))
    d.rectangle([cx - w * 0.10, wy + 6, cx + w * 0.10, wy + 9],
                fill=(232, 196, 82))


def scene_chip(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(10, 16, 34))
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + w * 0.42, y0 + h * 0.58
    for i in range(5):
        px = x0 + w * (0.18 + i * 0.11)
        d.line([px, cy - 26, px, cy - 36], fill=(90, 160, 120), width=3)
        d.line([px, cy + 26, px, cy + 36], fill=(90, 160, 120), width=3)
    d.rectangle([cx - 52, cy - 26, cx + 52, cy + 26], fill=(16, 68, 48),
                outline=(70, 200, 130), width=2)
    d.rectangle([cx - 40, cy - 16, cx + 40, cy + 16], fill=(24, 96, 66))
    f = font(SANS_B, 20)
    t = "NVDA"
    d.text((cx - d.textlength(t, font=f) / 2, cy - 11), t, font=f,
           fill=(255, 255, 255))
    pts = [(x0 + w * 0.62, y0 + h * 0.62), (x0 + w * 0.70, y0 + h * 0.42),
           (x0 + w * 0.78, y0 + h * 0.48), (x0 + w * 0.86, y0 + h * 0.26),
           (x0 + w * 0.95, y0 + h * 0.14)]
    d.line(pts, fill=(80, 220, 130), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(140, 255, 170))


def scene_jakarta(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(146, 196, 226))
    d.ellipse([x0 + (x1 - x0) * 0.78, y0 + 8, x0 + (x1 - x0) * 0.78 + 34,
               y0 + 42], fill=(255, 244, 190))
    w, h = x1 - x0, y1 - y0
    base = y0 + h * 0.78
    builds = [(0.04, 0.42, 0.10), (0.13, 0.55, 0.10), (0.25, 0.34, 0.09),
              (0.36, 0.48, 0.10), (0.62, 0.40, 0.10), (0.74, 0.58, 0.10),
              (0.86, 0.44, 0.10)]
    for bx, bh, bw in builds:
        d.rectangle([x0 + w * bx, base - h * bh, x0 + w * (bx + bw), base],
                    fill=(70, 90, 120))
        for wy in range(3):
            for wx in range(2):
                d.rectangle([x0 + w * (bx + 0.015 + wx * 0.045),
                             base - h * bh + 6 + wy * 12,
                             x0 + w * (bx + 0.035 + wx * 0.045),
                             base - h * bh + 13 + wy * 12],
                            fill=(255, 230, 140))
    d.rectangle([x0, base, x1, y1], fill=(52, 72, 96))
    cx = x0 + w * 0.52
    d.rectangle([cx - 26, base - 34, cx + 26, base + 4], fill=(245, 245, 240),
                outline=(120, 40, 40), width=2)
    d.rectangle([cx - 14, base - 40, cx + 14, base - 34], fill=(178, 34, 34))
    d.rectangle([cx - 2, base - 46, cx + 2, base - 40], fill=(178, 34, 34))
    f = font(SANS_B, 10)
    for lbl, ly in [("SUGIONO", base - 28), ("AMRAN", base - 14)]:
        d.text((cx - d.textlength(lbl, font=f) / 2, ly), lbl, font=f,
               fill=(26, 26, 26))


def scene_lamp(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(38, 22, 62))
    d.ellipse([x0 + (x1 - x0) * 0.74, y0 + 6, x0 + (x1 - x0) * 0.74 + 26,
               y0 + 32], fill=(245, 235, 200))
    w, h = x1 - x0, y1 - y0
    base = y0 + h * 0.92
    d.polygon([(x0, base), (x0 + w * 0.30, y0 + h * 0.45),
               (x0 + w * 0.62, y0 + h * 0.55), (x0 + w * 0.85, y0 + h * 0.40),
               (x1, base)], fill=(18, 12, 36))
    cx = x0 + w * 0.45
    d.rectangle([cx - 3, y0 + h * 0.30, cx + 3, y0 + h * 0.52],
                fill=(120, 90, 50))
    d.polygon([(cx - 16, y0 + h * 0.52), (cx + 16, y0 + h * 0.52),
               (cx + 10, y0 + h * 0.60), (cx - 10, y0 + h * 0.60)],
              fill=(200, 150, 60))
    d.polygon([(cx - 6, y0 + h * 0.50), (cx, y0 + h * 0.18),
               (cx + 6, y0 + h * 0.50)], fill=(255, 170, 40))
    d.polygon([(cx - 3, y0 + h * 0.48), (cx, y0 + h * 0.28),
               (cx + 3, y0 + h * 0.48)], fill=(255, 230, 130))
    for i in range(6):
        fx = x0 + w * (0.1 + i * 0.15)
        d.ellipse([fx - 2, base - 8, fx + 2, base - 4], fill=(255, 170, 60))


def scene_court(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 222, 196))
    w, h = x1 - x0, y1 - y0
    cx = x0 + w / 2
    top = y0 + h * 0.12
    d.polygon([(cx - w * 0.34, top + h * 0.22), (cx + w * 0.34, top + h * 0.22),
               (cx, top)], fill=(178, 34, 34))
    d.rectangle([cx - w * 0.34, top + h * 0.22, cx + w * 0.34,
                 top + h * 0.28], fill=(120, 110, 96))
    for i, fx in enumerate([-0.24, -0.08, 0.08, 0.24]):
        d.rectangle([cx + w * fx - 5, top + h * 0.28, cx + w * fx + 5,
                     y0 + h * 0.82], fill=(250, 248, 240),
                    outline=(150, 140, 120), width=1)
    d.rectangle([x0 + w * 0.08, y0 + h * 0.82, x1 - w * 0.08, y0 + h * 0.88],
                fill=(150, 140, 120))
    d.rectangle([x0 + w * 0.04, y0 + h * 0.88, x1 - w * 0.04, y0 + h * 0.94],
                fill=(120, 110, 96))
    # scales of justice, small, bottom right
    sx, sy = x0 + w * 0.78, y0 + h * 0.62
    d.line([sx, sy - 12, sx, sy + 10], fill=(90, 70, 30), width=2)
    d.line([sx - 12, sy - 10, sx + 12, sy - 10], fill=(90, 70, 30), width=2)
    d.pieslice([sx - 18, sy + 2, sx - 6, sy + 14], 0, 180, fill=(180, 140, 60))
    d.pieslice([sx + 6, sy + 2, sx + 18, sy + 14], 0, 180, fill=(180, 140, 60))
    d.ellipse([sx - 2, sy - 16, sx + 2, sy - 12], fill=(180, 140, 60))


def scene_startup(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(12, 54, 58))
    w, h = x1 - x0, y1 - y0
    base = y0 + h * 0.88
    heights = [0.22, 0.34, 0.30, 0.48, 0.62]
    for i, bh in enumerate(heights):
        bx = x0 + w * (0.08 + i * 0.16)
        d.rectangle([bx, base - h * bh, bx + w * 0.11, base],
                    fill=(232, 176, 60))
    d.line([(x0 + w * 0.08, base - h * 0.18), (x0 + w * 0.88, base - h * 0.66)],
           fill=(120, 220, 160), width=3)
    d.polygon([(x0 + w * 0.88, base - h * 0.66), (x0 + w * 0.82, base - h * 0.62),
               (x0 + w * 0.86, base - h * 0.56)], fill=(120, 220, 160))
    rx, ry = x0 + w * 0.80, y0 + h * 0.20
    d.polygon([(rx, ry - 12), (rx + 8, ry + 6), (rx - 8, ry + 6)],
              fill=(220, 60, 50))
    d.rectangle([rx - 8, ry + 6, rx + 8, ry + 16], fill=(240, 240, 240))
    d.polygon([(rx - 8, ry + 16), (rx - 12, ry + 24), (rx - 4, ry + 16)],
              fill=(220, 60, 50))
    d.polygon([(rx + 8, ry + 16), (rx + 12, ry + 24), (rx + 4, ry + 16)],
              fill=(220, 60, 50))
    d.ellipse([rx - 3, ry + 8, rx + 3, ry + 14], fill=(120, 200, 240))


def scene_flags(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(238, 230, 203))
    w, h = x1 - x0, y1 - y0
    # India flag, left
    fx, fy, fw, fh = x0 + w * 0.06, y0 + h * 0.18, w * 0.36, h * 0.42
    for i, col in enumerate([(255, 153, 51), (255, 255, 255), (19, 136, 8)]):
        d.rectangle([fx, fy + fh * i / 3, fx + fw, fy + fh * (i + 1) / 3],
                    fill=col)
    d.ellipse([fx + fw / 2 - 5, fy + fh / 2 - 5, fx + fw / 2 + 5,
               fy + fh / 2 + 5], outline=(0, 0, 128), width=1)
    # Egypt flag, right
    ex = x0 + w * 0.58
    for i, col in enumerate([(206, 17, 38), (255, 255, 255), (0, 0, 0)]):
        d.rectangle([ex, fy + fh * i / 3, ex + fw, fy + fh * (i + 1) / 3],
                    fill=col)
    d.ellipse([ex + fw / 2 - 4, fy + fh / 2 - 4, ex + fw / 2 + 4,
               fy + fh / 2 + 4], fill=(201, 162, 39))
    # gold coin between, below
    cx, cy = x0 + w / 2, y0 + h * 0.74
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(232, 196, 82),
              outline=(150, 110, 30), width=2)
    f = font(SANS_B, 13)
    d.text((cx - d.textlength("₹$", font=f) / 2, cy - 8), "₹$",
           font=f, fill=(120, 80, 10))


def scene_podium(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(222, 214, 190))
    w, h = x1 - x0, y1 - y0
    cx = x0 + w / 2
    d.rectangle([cx - w * 0.30, y0 + h * 0.55, cx + w * 0.30, y0 + h * 0.92],
                fill=(122, 82, 52))
    d.rectangle([cx - w * 0.34, y0 + h * 0.50, cx + w * 0.34, y0 + h * 0.57],
                fill=(96, 62, 38))
    d.line([cx + w * 0.10, y0 + h * 0.50, cx + w * 0.20, y0 + h * 0.28],
           fill=(40, 40, 40), width=2)
    d.ellipse([cx + w * 0.20 - 4, y0 + h * 0.26, cx + w * 0.20 + 4,
               y0 + h * 0.32], fill=(40, 40, 40))
    # resignation letter, held up left
    d.rectangle([x0 + w * 0.08, y0 + h * 0.16, x0 + w * 0.34, y0 + h * 0.52],
                fill=(255, 255, 255), outline=(120, 120, 120), width=1)
    for i in range(4):
        d.line([x0 + w * 0.12, y0 + h * (0.24 + i * 0.07),
                x0 + w * 0.30, y0 + h * (0.24 + i * 0.07)],
               fill=(150, 150, 150), width=1)
    f = font(SANS_B, 9)
    d.text((x0 + w * 0.12, y0 + h * 0.42), "SIGNED", font=f, fill=RED)


def scene_fifa(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(34, 122, 66))
    w, h = x1 - x0, y1 - y0
    d.ellipse([x0 + w * 0.30, y0 - h * 0.55, x0 + w * 0.72, y0 + h * 0.45],
              outline=(255, 255, 255), width=2)
    d.line([x0, y0 + h * 0.55, x1, y0 + h * 0.55], fill=(255, 255, 255),
           width=2)
    # ball, left
    bx, by = x0 + w * 0.24, y0 + h * 0.42
    d.ellipse([bx - 20, by - 20, bx + 20, by + 20], fill=(255, 255, 255),
              outline=(40, 40, 40), width=1)
    d.polygon([(bx, by - 8), (bx + 8, by - 2), (bx + 5, by + 8),
               (bx - 5, by + 8), (bx - 8, by - 2)], fill=(30, 30, 30))
    for ang in range(5):
        import math
        a = ang * 2 * math.pi / 5 - math.pi / 2
        d.ellipse([bx + math.cos(a) * 15 - 3, by + math.sin(a) * 15 - 3,
                   bx + math.cos(a) * 15 + 3, by + math.sin(a) * 15 + 3],
                  fill=(30, 30, 30))
    # trophy, right
    tx, ty = x0 + w * 0.72, y0 + h * 0.40
    d.polygon([(tx - 12, ty - 16), (tx + 12, ty - 16), (tx + 8, ty + 2),
               (tx - 8, ty + 2)], fill=(232, 196, 82))
    d.arc([tx - 20, ty - 18, tx - 8, ty - 2], 90, 270, fill=(232, 196, 82),
          width=3)
    d.arc([tx + 8, ty - 18, tx + 20, ty - 2], -90, 90, fill=(232, 196, 82),
          width=3)
    d.rectangle([tx - 3, ty + 2, tx + 3, ty + 12], fill=(200, 160, 50))
    d.rectangle([tx - 10, ty + 12, tx + 10, ty + 17], fill=(200, 160, 50))
    d.rectangle([tx - 13, ty + 17, tx + 13, ty + 21], fill=(180, 140, 40))
    # host flags strip at the bottom
    cols = [(178, 34, 34), (255, 255, 255), (0, 90, 160), (0, 120, 60)]
    for i, col in enumerate(cols):
        d.rectangle([x0 + w * (0.10 + i * 0.20), y0 + h * 0.82,
                     x0 + w * (0.28 + i * 0.20), y0 + h * 0.94], fill=col,
                    outline=(255, 255, 255), width=1)


def scene_hockey(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(46, 130, 66))
    w, h = x1 - x0, y1 - y0
    d.line([x0, y0 + h * 0.30, x1, y0 + h * 0.30], fill=(255, 255, 255),
           width=2)
    d.ellipse([x0 + w * 0.38, y0 + h * 0.18, x0 + w * 0.62, y0 + h * 0.42],
              outline=(255, 255, 255), width=2)
    # crossed sticks
    d.line([x0 + w * 0.22, y0 + h * 0.80, x0 + w * 0.52, y0 + h * 0.30],
           fill=(210, 180, 120), width=5)
    d.line([x0 + w * 0.78, y0 + h * 0.80, x0 + w * 0.48, y0 + h * 0.30],
           fill=(150, 110, 60), width=5)
    d.line([x0 + w * 0.52, y0 + h * 0.30, x0 + w * 0.60, y0 + h * 0.38],
           fill=(210, 180, 120), width=5)
    d.line([x0 + w * 0.48, y0 + h * 0.30, x0 + w * 0.40, y0 + h * 0.38],
           fill=(150, 110, 60), width=5)
    bx, by = x0 + w * 0.50, y0 + h * 0.62
    d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(255, 255, 255),
              outline=(30, 30, 30), width=1)
    f = font(SANS_B, 11)
    for lbl, lx in [("IND", 0.10), ("CHN", 0.60)]:
        d.text((x0 + w * lx, y0 + h * 0.06), lbl, font=f, fill=(255, 255, 255))


def scene_film(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(96, 24, 40))
    w, h = x1 - x0, y1 - y0
    for i in range(5):
        d.polygon([(x0 + w * i / 5, y0), (x0 + w * (i + 0.5) / 5, y0 + h * 0.22),
                   (x0 + w * (i + 1) / 5, y0),
                   (x0 + w * (i + 1) / 5, y0 + h * 0.22),
                   (x0 + w * i / 5, y0 + h * 0.22)], fill=(70, 16, 30))
    d.rectangle([x0 + w * 0.10, y0 + h * 0.28, x0 + w * 0.62, y0 + h * 0.78],
                fill=(245, 245, 240), outline=(40, 40, 40), width=2)
    d.rectangle([x0 + w * 0.16, y0 + h * 0.36, x0 + w * 0.56, y0 + h * 0.70],
                fill=(18, 32, 66))
    d.polygon([(x0 + w * 0.30, y0 + h * 0.42), (x0 + w * 0.30, y0 + h * 0.64),
               (x0 + w * 0.50, y0 + h * 0.53)], fill=(255, 220, 120))
    # medal, right
    mx, my = x0 + w * 0.78, y0 + h * 0.55
    d.polygon([(mx - 8, y0 + h * 0.24), (mx + 8, y0 + h * 0.24),
               (mx + 4, my - 8), (mx - 4, my - 8)], fill=(178, 34, 34))
    d.ellipse([mx - 14, my - 12, mx + 14, my + 16], fill=(232, 196, 82),
              outline=(150, 110, 30), width=2)
    f = font(SANS_B, 11)
    d.text((mx - d.textlength("10", font=f) / 2, my - 6), "10", font=f,
           fill=(120, 80, 10))


def scene_satellite(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(10, 14, 40))
    w, h = x1 - x0, y1 - y0
    for sx, sy in [(0.1, 0.15), (0.25, 0.08), (0.5, 0.2), (0.7, 0.1),
                   (0.85, 0.25), (0.6, 0.32), (0.35, 0.3)]:
        d.ellipse([x0 + w * sx - 1, y0 + h * sy - 1, x0 + w * sx + 1,
                   y0 + h * sy + 1], fill=(255, 255, 255))
    d.ellipse([x0 - w * 0.25, y0 + h * 0.55, x0 + w * 1.25, y0 + h * 1.00],
              fill=(28, 92, 170))
    d.ellipse([x0 + w * 0.12, y0 + h * 0.66, x0 + w * 0.30, y0 + h * 0.80],
              fill=(52, 140, 90))
    d.ellipse([x0 + w * 0.58, y0 + h * 0.72, x0 + w * 0.72, y0 + h * 0.82],
              fill=(52, 140, 90))
    cx, cy = x0 + w * 0.52, y0 + h * 0.30
    d.rectangle([cx - 26, cy - 8, cx - 8, cy + 8], fill=(40, 90, 180),
                outline=(140, 180, 240), width=1)
    d.rectangle([cx + 8, cy - 8, cx + 26, cy + 8], fill=(40, 90, 180),
                outline=(140, 180, 240), width=1)
    d.rectangle([cx - 8, cy - 10, cx + 8, cy + 10], fill=(200, 200, 205),
                outline=(120, 120, 130), width=1)
    d.line([cx, cy + 10, cx + 10, cy + 20], fill=(200, 200, 205), width=2)
    d.ellipse([cx + 8, cy + 18, cx + 16, cy + 26], outline=(200, 200, 205),
              width=2)


def scene_fog(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(150, 158, 172))
    w, h = x1 - x0, y1 - y0
    for i, (fy, fh) in enumerate([(0.12, 0.16), (0.34, 0.14), (0.56, 0.16),
                                  (0.76, 0.14)]):
        d.rounded_rectangle([x0 + w * (0.05 + (i % 2) * 0.08), y0 + h * fy,
                             x1 - w * (0.05 + ((i + 1) % 2) * 0.08),
                             y0 + h * (fy + fh)], radius=8,
                            fill=(205, 210, 220))
    for i in range(8):
        rx = x0 + w * (0.08 + i * 0.11)
        d.line([rx, y0 + h * 0.10, rx - 6, y0 + h * 0.30], fill=(120, 140, 180),
               width=2)
    # umbrella
    ux, uy = x0 + w * 0.62, y0 + h * 0.55
    d.pieslice([ux - 22, uy - 20, ux + 22, uy + 6], 180, 360, fill=(178, 34, 34))
    d.line([ux, uy - 20, ux, uy + 22], fill=(60, 40, 30), width=2)
    d.arc([ux, uy + 16, ux + 10, uy + 26], 0, 180, fill=(60, 40, 30), width=2)


SCENES = {
    "temple": scene_temple, "chip": scene_chip, "jakarta": scene_jakarta,
    "lamp": scene_lamp, "court": scene_court, "startup": scene_startup,
    "flags": scene_flags, "podium": scene_podium, "fifa": scene_fifa,
    "hockey": scene_hockey, "film": scene_film, "satellite": scene_satellite,
    "fog": scene_fog,
}

# ---------------------------------------------------------------- map
# Land mask as row -> list of (col_start, col_end) spans on a 64 x 32 grid.
# Columns cover lon -180..180 (5.625 deg each); rows cover lat 84..-56.
LAND = {
    0: [(8, 13), (24, 27)],
    1: [(2, 6), (9, 15), (24, 28), (40, 58)],
    2: [(1, 7), (8, 17), (23, 28), (32, 34), (36, 62)],
    3: [(2, 7), (9, 19), (24, 27), (32, 35), (36, 62)],
    4: [(2, 8), (10, 20), (29, 29), (32, 36), (37, 62)],
    5: [(3, 8), (11, 21), (29, 30), (33, 36), (37, 61)],
    6: [(12, 22), (29, 30), (31, 38), (39, 60)],
    7: [(13, 23), (30, 40), (41, 59)],
    8: [(14, 24), (30, 39), (41, 57), (60, 61)],
    9: [(15, 25), (30, 38), (42, 56), (60, 60)],
    10: [(15, 26), (31, 37), (38, 42), (47, 55), (59, 60)],
    11: [(16, 26), (31, 37), (39, 43), (45, 47), (48, 55)],
    12: [(16, 20), (21, 26), (31, 38), (40, 43), (45, 48), (50, 54)],
    13: [(17, 21), (25, 26), (32, 39), (40, 43), (46, 48), (50, 53)],
    14: [(17, 21), (23, 25), (32, 40), (46, 48), (50, 54)],
    15: [(18, 21), (33, 41), (46, 48), (51, 54)],
    16: [(19, 22), (34, 42), (52, 55)],
    17: [(22, 26), (35, 42), (53, 56)],
    18: [(23, 28), (36, 42), (52, 58)],
    19: [(24, 29), (37, 41), (53, 59)],
    20: [(24, 29), (37, 41), (54, 61)],
    21: [(25, 29), (37, 41), (55, 61)],
    22: [(25, 29), (37, 40), (42, 42), (54, 61)],
    23: [(25, 29), (37, 40), (42, 42), (54, 60)],
    24: [(25, 28), (37, 40), (55, 60)],
    25: [(25, 28), (37, 39), (55, 59)],
    26: [(25, 27), (37, 39), (55, 59), (61, 62)],
    27: [(25, 27), (61, 61)],
    28: [(25, 26), (61, 61)],
    29: [(25, 26)],
    30: [(25, 25)],
    31: [(25, 25)],
}


def lonlat_to_grid(lon, lat):
    col = (lon + 180.0) / 5.625
    row = (84.0 - lat) / 4.375
    return col, row


def draw_map(p, x0, y0, x1, y1):
    d = p.d
    d.rectangle([x0, y0, x1, y1], fill=(250, 246, 232),
                outline=LINE, width=1)
    cw, ch = (x1 - x0) / 64.0, (y1 - y0) / 32.0
    for row, spans in LAND.items():
        for a, b in spans:
            for col in range(a, b + 1):
                cx = x0 + (col + 0.5) * cw
                cy = y0 + (row + 0.5) * ch
                d.ellipse([cx - 1.4, cy - 1.4, cx + 1.4, cy + 1.4],
                          fill=(178, 164, 120))
    for num, (lon, lat, dx, dy) in sorted(PINS.items()):
        col, row = lonlat_to_grid(lon, lat)
        tx = x0 + (col + 0.5) * cw
        ty = y0 + (row + 0.5) * ch
        px, py = tx + dx, ty + dy
        if dx or dy:
            d.line([tx, ty, px, py], fill=(120, 120, 120), width=1)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = font(SANS_B, 10)
        t = str(num)
        tw = d.textlength(t, font=f)
        d.text((px - tw / 2, py - 6), t, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- build
def build(out_path):
    p = Page()
    d = p.d
    d.rectangle([6, 6, W - 7, H - 7], outline=NAVY, width=3)

    # top bar
    d.rectangle([12, 12, 1012, 38], fill=NAVY)
    f = font(SANS_B, 15)
    d.text((20, 18), "THE WORLD IN ONE DAY", font=f, fill=(255, 255, 255))
    f2 = font(SANS_B, 11)
    right = "35 STORIES · 5 REGIONS · EVERY ONE DATED TUESDAY 24 NOVEMBER 2026"
    d.text((1012 - 8 - d.textlength(right, font=f2), 20), right, font=f2,
           fill=(255, 220, 120))

    # masthead
    f = font(SERIF_B, 57)
    d.text((14, 44), "Tuesday 24 November 2026", font=f, fill=INK)
    f = font(SERIF, 15)
    d.text((16, 106),
           "Huang back at Nvidia as shares soar 31%  ·  Sikhs mark Guru "
           "Nanak's 557th  ·  Jakarta names its VP picks",
           font=f, fill=RED_DARK)

    # stat strip
    y = 132
    bw, gap = 162, 5
    for i, (big, small) in enumerate(STATS):
        x = 12 + i * (bw + gap)
        d.rectangle([x, y, x + bw, y + 40], outline=LINE, width=1,
                    fill=(255, 255, 255))
        fb = font(SERIF_B, 24)
        d.text((x + 8, y + 3), big, font=fb, fill=RED)
        fs = font(SANS, 10)
        d.text((x + 8, y + 28), small, font=fs, fill=GREY)

    # region bar
    y = 178
    total = sum(c for _, c, _ in REGIONS)
    x = 12
    for name, count, col in REGIONS:
        seg = int(1000 * count / total)
        d.rectangle([x, y, x + seg - 1, y + 18], fill=col)
        fsize = 10 if seg >= 70 else 9
        f = font(SANS_B, fsize)
        label = "%s %d" % (name, count)
        if d.textlength(label, font=f) <= seg - 6:
            d.text((x + 4, y + 4), label, font=f, fill=(255, 255, 255))
        x += seg

    # weather strip
    y = 202
    f = font(SANS_B, 12)
    d.text((14, y + 2), "TUESDAY WEATHER", font=f, fill=RED)
    x = 150
    for city, temp, kind in WEATHER:
        weather_icon(d, x, y, kind)
        f = font(SANS_B, 11)
        d.text((x + 20, y + 2), "%s  %s°" % (city, temp), font=f, fill=INK)
        x += 145

    # leads
    lead_y, lead_h = 228, 132
    lead_text_y = 364
    for i, lead in enumerate(LEADS):
        x = 12 + i * 336
        w = 328
        SCENES[lead["scene"]](d, x, lead_y, x + w, lead_y + lead_h)
        d.rectangle([x, lead_y, x + w, lead_y + lead_h], outline=LINE,
                    width=1)
        p.badge(x + 4, lead_y + 4, lead["kicker"], size=11)
        f = font(SANS_B, 10)
        chip = lead["chip"]
        tw = d.textlength(chip, font=f)
        d.rectangle([x + w - tw - 14, lead_y + 4, x + w - 4, lead_y + 21],
                    fill=NAVY)
        d.text((x + w - tw - 8, lead_y + 7), chip, font=f,
               fill=(255, 255, 255))
        f = font(SANS_B, 11)
        d.text((x, lead_text_y), lead["place"], font=f, fill=RED)
        y2 = p.para(x, lead_text_y + 16, lead["headline"], SERIF_B, 21, w,
                    INK, leading=24)
        p.para(x, y2 + 3, lead["deck"], SANS, 11, w, (70, 66, 56),
               leading=14)

    # mini cards, two rows of five
    card_w, card_gap = 192, 10
    for row in range(2):
        art_y = 456 + row * 154
        text_y = art_y + 80
        for col in range(5):
            card = CARDS[row * 5 + col]
            x = 12 + col * (card_w + card_gap)
            SCENES[card["scene"]](d, x, art_y, x + card_w, art_y + 76)
            d.rectangle([x, art_y, x + card_w, art_y + 76], outline=LINE,
                        width=1)
            p.badge(x + 3, art_y + 3, card["kicker"], size=9)
            p.num_chip(x + card_w - 12, art_y + 12, card["num"], r=9)
            f = font(SANS_B, 10)
            d.text((x, text_y), card["place"], font=f, fill=RED)
            p.para(x, text_y + 14, card["headline"], SERIF_B, 13,
                   card_w, INK, leading=16)

    # bottom: map + the other 22 stories
    y = 768
    f = font(SANS_B, 12)
    d.text((14, y), "WHERE IT HAPPENED", font=f, fill=INK)
    d.text((182, y + 2), "pins match story numbers", font=font(SANS, 10),
           fill=GREY)
    d.text((318, y), "ALSO ON TUESDAY 24 NOVEMBER — 22 MORE STORIES",
           font=f, fill=INK)
    draw_map(p, 12, 788, 306, 910)
    # brief list, two columns
    f = font(SANS, 11)
    fb = font(SANS_B, 11)
    for i, item in enumerate(BRIEFS):
        col = i // 11
        r = i % 11
        bx = 318 + col * 352
        by = 790 + r * 11
        num = str(14 + i)
        d.text((bx, by), num, font=fb, fill=RED)
        d.text((bx + 22, by), item, font=f, fill=INK)

    # date check
    y = 918
    d.rectangle([12, y, 1012, y + 44], outline=RED, width=2)
    f = font(SANS_B, 12)
    d.text((20, y + 4), "DATE CHECK", font=f, fill=RED)
    f = font(SANS, 10)
    d.text((20, y + 22),
           "Wires read to 01:30 UTC, Tue 24 Nov 2026; every story was "
           "reported or still developing on Tue 24 Nov in at least one time "
           "zone.", font=f, fill=INK)
    d.text((20, y + 34),
           "Left out as other days' news: hockey 7–0 Thailand and squash "
           "titles (Sun 22 Nov); Rathee warrant (Mon 23 Nov); COP31 "
           "collapse, Tajikistan ICC exit, Alcaraz ATP win.",
           font=f, fill=INK)

    # footer
    f = font(SANS, 9)
    d.text((14, 972),
           "Sources: Reuters, BBC, Morningstar, TechCrunch, Nikkei Asia, "
           "FIFA, Hockey India, LiveLaw, Jagran Josh, ObserverVoice, IMD, "
           "weather.com. Pictures and map drawn in code.",
           font=f, fill=GREY)
    f = font(SANS_B, 9)
    tail = "TUESDAY 24 NOVEMBER 2026 · ONE PAGE"
    d.text((1012 - d.textlength(tail, font=f), 972), tail, font=f, fill=INK)

    p.img.save(out_path, "PNG")
    print("wrote", out_path)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build(out)

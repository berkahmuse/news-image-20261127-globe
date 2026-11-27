#!/usr/bin/env python3
"""Draw the 27 November 2026 world-news globe infographic (1024x1024 PNG).

Pure Pillow drawing: dark news-atlas background, a stylised globe drawn from
hand-plotted continent outlines (orthographic projection, Atlantic centred),
and six numbered callout cards for the six verified stories of the day.
Deterministic: fixed coordinates, fixed LCG seed for the star field, no
timestamps anywhere. Run: python3 draw.py  ->  writes entry.png beside it.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette ----------------------------------------------------------------
NAVY_TOP = (10, 26, 51)
NAVY_BOT = (14, 42, 78)
GOLD = (232, 184, 75)
CREAM = (245, 239, 224)
MUTED = (159, 179, 204)
CARD_BG = (16, 35, 63, 238)
CARD_EDGE = (232, 184, 75)
OCEAN_EDGE = (18, 63, 99)
OCEAN_MID = (32, 110, 150)
OCEAN_CTR = (46, 134, 171)
LAND = (87, 167, 115)
LAND_EDGE = (46, 125, 91)
INK = (8, 20, 38)

FONT_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


F_TITLE = font(FONT_B, 30)
F_DATE = font(FONT_B, 46)
F_TAG = font(FONT_B, 16)
F_HEAD = font(FONT_B, 20)
F_BODY = font(FONT_R, 15)
F_FOOT = font(FONT_R, 16)
F_SRC = font(FONT_R, 14)
F_NUM = font(FONT_B, 15)

# --- stories (verified 27 Nov 2026; see README for timestamps) --------------
# Every story below was first reported, or happened, on 27 November 2026
# in at least one Asia-Pacific time zone (UTC+7 to +13). Per-story
# timestamps and time-zone conversions are documented in README.md.
STORIES = [
    dict(n=1, tag="USA · TEXAS",
         head="Exchanges file for 23-hour trading",
         body="24X and Texas exchanges seek round-the-clock trading",
         lon=-96.8, lat=32.8, card=(24, 146)),
    dict(n=2, tag="PAKISTAN",
         head="Mecca alliance meets in Islamabad",
         body="Pakistan, Saudi, Turkey open defence talks Nov 27\u201328",
         lon=73.06, lat=33.68, card=(748, 146)),
    dict(n=3, tag="USA · MICHIGAN",
         head="Bears stun Lions in Thanksgiving thriller",
         body="Williams to Odunze, 3 seconds left; 39\u201335, Bears lead North",
         lon=-83.05, lat=42.33, card=(24, 416)),
    dict(n=4, tag="KUWAIT",
         head="Iran blames Kyiv for deadly strike",
         body="Tehran denies drone attack that killed 2 Italians",
         lon=47.98, lat=29.3, card=(748, 416)),
    dict(n=5, tag="GUINEA-BISSAU",
         head="Elections delayed to 2028",
         body="Military rulers extend transition by two years",
         lon=-15.6, lat=11.9, card=(24, 656)),
    dict(n=6, tag="SAUDI ARABIA",
         head="Houthis hit Aramco refinery",
         body="1 worker killed, several hurt; some operations halted",
         lon=42.5, lat=16.9, card=(748, 656)),
]

# --- continent outlines (lon, lat), simplified -------------------------------
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-85, 66), (-80, 73),
     (-65, 60), (-55, 52), (-60, 46), (-70, 42), (-75, 35), (-80, 26),
     (-84, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40),
     (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-55, 60), (-45, 60), (-40, 65), (-32, 68), (-22, 70), (-30, 76),
     (-55, 76), (-58, 70)],
    [(-80, 10), (-75, 5), (-70, 12), (-60, 8), (-52, 5), (-50, 0),
     (-40, -5), (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -40),
     (-70, -52), (-73, -40), (-72, -20), (-80, -5), (-81, 0)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
     (35, 28), (43, 12), (51, 11), (48, 2), (40, -10), (35, -18),
     (30, -30), (20, -35), (15, -27), (12, -18), (9, 4), (4, 6),
     (-8, 5), (-13, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 68),
     (15, 70), (12, 70), (5, 60), (5, 58), (-2, 57), (-5, 50), (-10, 43)],
    [(30, 62), (40, 68), (60, 69), (90, 72), (120, 73), (150, 70),
     (170, 66), (178, 65), (170, 60), (162, 55), (158, 50), (142, 45),
     (140, 40), (130, 35), (127, 33), (122, 30), (120, 25), (110, 20),
     (105, 10), (100, 8), (95, 15), (90, 22), (80, 13), (77, 8),
     (72, 20), (66, 25), (60, 25), (55, 26), (50, 29), (48, 30),
     (43, 35), (36, 36), (30, 36), (28, 41), (30, 46)],
    [(114, -22), (113, -26), (115, -33), (120, -34), (129, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -27), (146, -19), (142, -11),
     (136, -12), (132, -12), (126, -14), (122, -17)],
]

# --- orthographic projection, Atlantic centred (rotated east so that
# Islamabad, at the edge of the visible hemisphere, sits on the globe) ----
CX, CY, R = 512, 486, 222
LON0, LAT0 = math.radians(-16), math.radians(22)
SIN0, COS0 = math.sin(LAT0), math.cos(LAT0)


def project(lon_deg, lat_deg):
    lon, lat = math.radians(lon_deg), math.radians(lat_deg)
    cosc = SIN0 * math.sin(lat) + COS0 * math.cos(lat) * math.cos(lon - LON0)
    if cosc <= 0.03:
        return None
    x = R * math.cos(lat) * math.sin(lon - LON0)
    y = -R * (COS0 * math.sin(lat) - SIN0 * math.cos(lat) * math.cos(lon - LON0))
    return (CX + x, CY + y)


def densify(poly, step=2.0):
    out = []
    for (lon1, lat1), (lon2, lat2) in zip(poly, poly[1:] + poly[:1]):
        n = max(1, int(math.hypot(lon2 - lon1, lat2 - lat1) / step))
        for i in range(n):
            t = i / n
            out.append((lon1 + (lon2 - lon1) * t, lat1 + (lat2 - lat1) * t))
    return out


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def wrap(text, fnt, width):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def track(draw, cx, y, text, fnt, fill, spacing=3):
    widths = [fnt.getlength(c) for c in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + spacing


def main():
    img = Image.new("RGB", (W, H), NAVY_TOP)
    d = ImageDraw.Draw(img, "RGBA")
    # vertical gradient background
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(NAVY_TOP, NAVY_BOT, y / H))
    # deterministic star field (fixed-seed LCG)
    s = 1234567
    for _ in range(110):
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        x, y = s % W, (s >> 9) % H
        if (x - CX) ** 2 + (y - CY) ** 2 > (R + 40) ** 2:
            a = 40 + (s >> 17) % 90
            d.ellipse([x, y, x + 2, y + 2], fill=(255, 255, 255, a))

    # ---- header ----
    track(d, CX, 30, "THE WORLD IN ONE DAY", F_TITLE, GOLD, spacing=6)
    d.text((CX, 68), "FRIDAY \u00b7 27 NOVEMBER \u00b7 2026", font=F_DATE,
           fill=CREAM, anchor="ma")
    d.line([(212, 128), (812, 128)], fill=GOLD, width=2)

    # ---- globe ----
    # NOTE: PIL ImageDraw REPLACES pixels on RGBA instead of blending, so every
    # semi-transparent element goes on its own overlay layer, alpha-composited.
    globe = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(globe)
    for r in range(R, 0, -2):
        g.ellipse([CX - r, CY - r, CX + r, CY + r],
                  fill=lerp(OCEAN_EDGE, OCEAN_CTR, 1 - r / R) + (255,))
    # graticule (overlay, blended)
    grat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gg = ImageDraw.Draw(grat)
    for lon in range(-180, 181, 30):
        pts = [project(lon, la) for la in range(-80, 81, 2)]
        pts = [p for p in pts if p]
        if len(pts) > 1:
            gg.line(pts, fill=(255, 255, 255, 42), width=1)
    for la in range(-60, 61, 30):
        pts = [project(lo, la) for lo in range(-180, 181, 2)]
        pts = [p for p in pts if p]
        if len(pts) > 1:
            gg.line(pts, fill=(255, 255, 255, 42), width=1)
    globe.alpha_composite(grat)
    g = ImageDraw.Draw(globe)
    # continents
    for poly in CONTINENTS:
        pts = [project(lo, la) for lo, la in densify(poly)]
        pts = [p for p in pts if p]
        if len(pts) > 2:
            g.polygon(pts, fill=LAND + (255,), outline=LAND_EDGE + (255,))
    # soft light from top-left (overlay, blended)
    light = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(light).ellipse([CX - R, CY - R, CX + R // 3, CY + R // 3],
                                  fill=(255, 255, 255, 18))
    globe.alpha_composite(light)
    g = ImageDraw.Draw(globe)
    g.ellipse([CX - R, CY - R, CX + R, CY + R], outline=GOLD + (255,), width=3)
    img.paste(globe, (0, 0), globe)
    d = ImageDraw.Draw(img, "RGBA")

    # ---- markers + leader lines ----
    marker_xy = {}
    for st in STORIES:
        p = project(st["lon"], st["lat"])
        marker_xy[st["n"]] = p
        cx0, cy0 = st["card"]
        ex = cx0 + (252 if cx0 < CX else 0)
        ey = min(max(p[1], cy0 + 14), cy0 + 156 - 14)
        d.line([p, (ex, ey)], fill=GOLD + (200,), width=2)
    for st in STORIES:
        p = marker_xy[st["n"]]
        d.ellipse([p[0] - 12, p[1] - 12, p[0] + 12, p[1] + 12],
                  fill=GOLD, outline=(255, 255, 255, 255), width=2)
        d.text(p, str(st["n"]), font=F_NUM, fill=INK, anchor="mm")

    # ---- callout cards ----
    for st in STORIES:
        x, y = st["card"]
        d.rounded_rectangle([x, y, x + 252, y + 156], radius=14,
                            fill=CARD_BG, outline=CARD_EDGE, width=2)
        d.ellipse([x + 12, y + 12, x + 36, y + 36], fill=GOLD)
        d.text((x + 24, y + 24), str(st["n"]), font=F_NUM, fill=INK, anchor="mm")
        d.text((x + 44, y + 14), st["tag"], font=F_TAG, fill=GOLD)
        lines = wrap(st["head"], F_HEAD, 224)
        yy = y + 44
        for ln in lines[:2]:
            d.text((x + 14, yy), ln, font=F_HEAD, fill=CREAM)
            yy += 25
        yy += 4
        # Body may use up to 3 lines: a 2-line cap dropped words (card 1
        # lost "grounded" in v1). 2-line heads + 3-line bodies still fit
        # the 156 px card (last baseline y+138, text bottom ~y+153).
        for ln in wrap(st["body"], F_BODY, 224)[:3]:
            d.text((x + 14, yy), ln, font=F_BODY, fill=MUTED)
            yy += 20

    # ---- footer ----
    d.line([(312, 848), (712, 848)], fill=GOLD, width=1)
    d.text((CX, 862), "Six stories \u00b7 One day \u00b7 Reported around the world",
           font=F_FOOT, fill=CREAM, anchor="ma")
    d.text((CX, 892), "Sources: Reuters \u00b7 Fox News \u00b7 Federal Register",
           font=F_SRC, fill=MUTED, anchor="ma")
    d.text((CX, 918), "make.fun \u2014 news-image-20261127 \u00b7 @berkahmuse",
           font=F_SRC, fill=MUTED, anchor="ma")

    img.save(OUT, format="PNG", compress_level=6)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()

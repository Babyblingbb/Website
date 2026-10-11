#!/usr/bin/env python3
"""Normalise the eight shirt cut-outs into a consistent grid set.

The product-page heroes are deliberately individual — each was rendered with its
own slight tilt. Side by side in a grid that reads as sloppy, so this builds a
second set for the collection page only:

  1. de-skew  — fit a line to the hem and rotate it level
  2. rescale  — every shirt ends up the same shoulder width
  3. re-frame — identical square canvas, hem on the same baseline

Originals are untouched; output goes to assets-grid/.
"""
import io, os, math
from PIL import Image

SRC = [("bb", "assets/shirt.webp"),
       ("bk", "assets-kite/bk-shirt.webp"),
       ("bs", "assets-story/bs-grid.webp"),
       ("bp", "assets-pink/bp-grid.webp"),
       ("bd", "assets-dino/bd-grid.webp"),
       ("bn", "assets-shin/bn-grid.webp"),
       ("bl", "assets-blk/bl-grid.webp"),
       ("bg", "assets-sea/bg-grid.webp"),
       ("bw", "assets-beach/bw-shirt.webp"),
       ("bc", "assets-beige/bc-shirt.webp"),
       ("bf", "assets-white/bf-shirt.webp")]

CANVAS   = 1000     # output width
CANVAS_H = 1100     # output height (shirts are taller than wide once scaled up)
SHOULDER = 930      # shirt fills most of the tile
HEM_Y    = 0.975

os.makedirs("assets-grid", exist_ok=True)


def alpha_cols(a, thresh=150):
    """max opaque y per column, and min opaque y per column."""
    w, h = a.size
    px = a.load()
    bot, top = {}, {}
    for x in range(w):
        ys = [y for y in range(h) if px[x, y] > thresh]
        if ys:
            bot[x] = ys[-1]
            top[x] = ys[0]
    return bot, top


def hem_angle(a):
    """Least-squares slope of the hem across the central 60% of the width."""
    bot, _ = alpha_cols(a)
    if not bot:
        return 0.0
    xs = sorted(bot)
    lo, hi = xs[0], xs[-1]
    span = hi - lo
    keep = [x for x in xs if lo + .20 * span <= x <= lo + .80 * span]
    # the hem is the lowest band; drop columns far above it (sleeves, gaps)
    ymax = max(bot[x] for x in keep)
    keep = [x for x in keep if bot[x] > ymax - 0.12 * a.size[1]]
    if len(keep) < 20:
        return 0.0
    n = len(keep)
    mx = sum(keep) / n
    my = sum(bot[x] for x in keep) / n
    num = sum((x - mx) * (bot[x] - my) for x in keep)
    den = sum((x - mx) ** 2 for x in keep)
    if den == 0:
        return 0.0
    return math.degrees(math.atan(num / den))


def shoulder_width(a, thresh=150):
    """Widest opaque row in the upper half — the shoulder line."""
    w, h = a.size
    px = a.load()
    best = 0
    for y in range(int(h * .10), int(h * .55)):
        xs = [x for x in range(w) if px[x, y] > thresh]
        if xs:
            best = max(best, xs[-1] - xs[0])
    return best or w


def run():
    rows = []
    for tag, path in SRC:
        im = Image.open(path).convert("RGBA")
        ang = hem_angle(im.split()[3])
        ang = max(-12.0, min(12.0, ang))          # a sane correction only
        if abs(ang) > 0.3:
            im = im.rotate(ang, resample=Image.BICUBIC, expand=True)
        bb = im.split()[3].point(lambda v: 255 if v > 12 else 0).getbbox()
        im = im.crop(bb)

        sw = shoulder_width(im.split()[3])
        k = SHOULDER / sw
        im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
        if im.width > CANVAS - 10 or im.height > CANVAS_H - 10:
            k2 = min((CANVAS - 10) / im.width, (CANVAS_H - 10) / im.height)
            im = im.resize((round(im.width * k2), round(im.height * k2)), Image.LANCZOS)

        out = Image.new("RGBA", (CANVAS, CANVAS_H), (0, 0, 0, 0))
        x = (CANVAS - im.width) // 2
        y = int(CANVAS_H * HEM_Y) - im.height
        out.alpha_composite(im, (x, max(0, y)))
        out.save(f"assets-grid/g-{tag}.webp", "WEBP", quality=88, method=6)
        rows.append((tag, round(ang, 2), sw, im.size))
        print(f"  g-{tag}  deskew {ang:+.2f}deg  shoulder {sw} -> {SHOULDER}  final {im.size}")
    return rows


if __name__ == "__main__":
    run()
    # contact sheet on a flat sky so misalignment is obvious
    tiles = []
    for tag, _ in SRC:
        im = Image.open(f"assets-grid/g-{tag}.webp").convert("RGBA")
        bg = Image.new("RGBA", im.size, (150, 205, 245, 255))
        bg.alpha_composite(im)
        tiles.append(bg.convert("RGB").resize((250, 275), Image.LANCZOS))
    sheet = Image.new("RGB", (250 * 4, 275 * 2), (255, 255, 255))
    for i, t in enumerate(tiles):
        sheet.paste(t, (250 * (i % 4), 275 * (i // 4)))
    sheet.save("assets-grid/_sheet.jpg", quality=88)
    print("sheet -> assets-grid/_sheet.jpg")

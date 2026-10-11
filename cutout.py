#!/usr/bin/env python3
"""Background knockout for product shots.

Background is detected as achromatic AND bright, so a coloured garment survives
while white / grey / warm-neutral studio backdrops go transparent. The flood fill
starts at the border and cannot reach interior whites (a white cloud embroidery,
a woven label) through the garment, so those stay opaque. Finally any residual
soft drop-shadow below the hem is cropped and cleared.
"""
from PIL import Image, ImageFilter
from collections import deque


def cutout(path, bg_chroma=16, bg_min=196, erode=7, bg_test=None):
    """bg_test(r,g,b) -> True for backdrop, overriding the achromatic test.
    Use it for coloured backdrops, e.g. a warm beige behind a cool blue shirt:
        bg_test=lambda r, g, b: r > b + 12
    """
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()

    ap = [[255] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            mn, mx = min(r, g, b), max(r, g, b)
            bg = bg_test(r, g, b) if bg_test else ((mx - mn) < bg_chroma and mn > bg_min)
            if bg:
                ap[y][x] = 0 if (bg_test or mn > 232) else int((232 - mn) / max(1, 232 - bg_min) * 255)

    seen = bytearray(w * h)
    dq = deque()
    out = [[False] * w for _ in range(h)]
    for x in range(w):
        dq.append((x, 0)); dq.append((x, h - 1))
    for y in range(h):
        dq.append((0, y)); dq.append((w - 1, y))
    while dq:
        x, y = dq.popleft()
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        if ap[y][x] > 70:
            continue
        out[y][x] = True
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                dq.append((nx, ny))

    al = Image.new("L", (w, h), 255)
    f = al.load()
    for y in range(h):
        for x in range(w):
            if out[y][x]:
                f[x, y] = ap[y][x]
    al = (al.filter(ImageFilter.MedianFilter(5))
            .filter(ImageFilter.MinFilter(erode))
            .filter(ImageFilter.GaussianBlur(1.0)))
    res = im.convert("RGBA")
    res.putalpha(al)
    res = res.crop(al.point(lambda v: 255 if v > 12 else 0).getbbox())

    # crop off the soft shadow that sits below the hem
    px2 = res.load()
    last = 0
    for y in range(res.height):
        for x in range(0, res.width, 2):
            r, g, b, a = px2[x, y]
            # with a custom backdrop test, opacity alone marks the garment (white/cream
            # shirts have almost no chroma and would otherwise be cropped away)
            if a > 140 and (bg_test is not None or (max(r, g, b) - min(r, g, b)) > 22 or (min(r, g, b) < 95 and a > 200)):
                last = y
                break
    res = res.crop((0, 0, res.width, min(res.height, last + 6)))

    # Clear leftover backdrop ONLY where it connects to the border. A global
    # sweep would also erase interior whites (white cloud embroidery, the woven
    # label), which is exactly what it must not touch.
    w2, h2 = res.size
    px2 = res.load()
    seen2 = bytearray(w2 * h2)
    dq2 = deque()
    for x in range(w2):
        dq2.append((x, 0)); dq2.append((x, h2 - 1))
    for y in range(h2):
        dq2.append((0, y)); dq2.append((w2 - 1, y))
    while dq2:
        x, y = dq2.popleft()
        i = y * w2 + x
        if seen2[i]:
            continue
        seen2[i] = 1
        r, g, b, a = px2[x, y]
        leftover = bg_test(r, g, b) if bg_test else             ((max(r, g, b) - min(r, g, b)) < bg_chroma and min(r, g, b) > 200)
        if a > 150 and not leftover:
            continue                      # hit the garment, stop here
        px2[x, y] = (r, g, b, 0)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w2 and 0 <= ny < h2 and not seen2[ny * w2 + nx]:
                dq2.append((nx, ny))

    # keep only the tallest contiguous band of opaque rows: a floor shadow sitting
    # below the hem, separated by a clear gap, is dropped
    a2 = res.split()[3].point(lambda v: 255 if v > 40 else 0)
    W2, H2 = a2.size; pa = a2.load()
    rows = [any(pa[x, y] for x in range(0, W2, 3)) for y in range(H2)]
    best, cur, start = (0, 0, 0), 0, 0
    for y, on in enumerate(rows + [False]):
        if on:
            if cur == 0: start = y
            cur += 1
        else:
            if cur > best[0]: best = (cur, start, y)
            cur = 0
    if best[0]:
        res = res.crop((0, best[1], W2, best[2]))
    bb = res.split()[3].point(lambda v: 255 if v > 12 else 0).getbbox()
    return res.crop(bb)


def preview(img, path, bg=(120, 196, 246, 255), scale=2):
    canvas = Image.new("RGBA", (img.width + 80, img.height + 80), bg)
    canvas.alpha_composite(img, (40, 40))
    canvas.convert("RGB").resize((canvas.width // scale, canvas.height // scale)).save(path)

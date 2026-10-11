#!/usr/bin/env python3
"""index.html (peach / Balloon Bicycle)  ->  index-sea.html (sage / Little Gardener).

The shirt is pale sage with dark green botanical embroidery, so the sky goes the
other way: a warm terracotta evening. Complementary to the green stitching, and
the hero band is kept light enough for the navy headline and body copy.
"""
import io, re

s = io.open("index.html", encoding="utf-8").read()
n0 = len(s)

def rep(a, b, why, count=1):
    global s
    assert a in s, "MISSING (%s): %s" % (why, a[:70])
    s = s.replace(a, b, count)

def soft(a, b):
    global s
    s = s.replace(a, b)

# ── assets ──────────────────────────────────────────────────────────────────
for old, new in {"shirt":"bg-shirt", "back":"bg-back", "d-collar":"bg-d-collar",
                 "d-buttons":"bg-d-buttons", "d-embroidery":"bg-d-plant",
                 "d-patch":"bg-d-can", "lifestyle":"bg-lifestyle",
                 "folded":"bg-clouds"}.items():
    rep("assets/%s.webp" % old, "assets-sea/%s.webp" % new, "asset " + old, count=99)

rep('<button class="bvt"     data-src="assets-sea/bg-clouds.webp"       aria-label="Folded"><img src="assets-sea/bg-clouds.webp" alt="" loading="lazy"></button>',
    '<button class="bvt"     data-src="assets-sea/bg-clouds.webp"   aria-label="In the sky"><img src="assets-sea/bg-clouds.webp" alt="" loading="lazy"></button>\n'
    '        <button class="bvt"     data-src="assets-sea/bg-folded.webp"   aria-label="Folded"><img src="assets-sea/bg-folded.webp" alt="" loading="lazy"></button>',
    "extra thumb")

# ── hero geometry (bg-shirt is 883x824) ────────────────────────────────────
rep("aspect-ratio:778/835", "aspect-ratio:883/824", "aspect")
rep('width="778" height="835"', 'width="883" height="824"', "img dims", count=99)

# ── terracotta evening ─────────────────────────────────────────────────────
rep("  --sky-0:#5FB9F5; --sky-1:#8FD2FA; --sky-2:#BFE7FE; --sky-3:#E4F5FF;",
    "  --sky-0:#C0653F; --sky-1:#DB9670; --sky-2:#EFC0A4; --sky-3:#FAE6D8;", "sky vars")
rep("""    #4FB2F3 0%, #79C9F8 8%, #A8DEFC 17%,
    #D2EEFE 27%, #EAF7FF 34%, #D6F0FF 42%,
    #B9E4FD 52%, #E6F6FF 62%, #FFF1E4 70%,
    #FFE3D2 76%, #D8EEFE 85%, #A6DBFB 93%, #74C4F7 100%)}""",
    """    #F4D6C2 0%, #F0CCB4 8%, #ECC2A6 17%,
    #E7B795 27%, #E3AE88 34%, #DFA47C 42%,
    #D89568 52%, #E9BB9E 62%, #FBE4D4 70%,
    #F6CDB6 76%, #E6B597 85%, #CE7E55 93%, #BC6440 100%)}""", "sky gradient")
rep("background:radial-gradient(circle,rgba(255,250,225,.95),rgba(255,238,195,.55) 32%,rgba(255,232,180,0) 66%);",
    "background:radial-gradient(circle,rgba(255,240,215,.95),rgba(252,206,164,.55) 34%,rgba(248,190,150,0) 68%);", "sun")
rep("box-shadow:inset 0 -16px 26px -16px rgba(120,180,220,.42)}",
    "box-shadow:inset 0 -16px 26px -16px rgba(190,115,80,.44)}", "cloud underside")
rep(".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px rgba(240,170,140,.34)}",
    ".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px rgba(214,128,92,.38)}", "warm cloud")
rep("drop-shadow(0 14px 22px rgba(46,116,168,.20))}",
    "drop-shadow(0 14px 22px rgba(150,80,50,.22))}", "cloud shadow css")
rep("'drop-shadow(0 14px 22px rgba(46,116,168,'+(layer===2?.10:.04)+'))'+",
    "'drop-shadow(0 14px 22px rgba(150,80,50,'+(layer===2?.12:.05)+'))'+", "cloud shadow js")
rep('<meta name="theme-color" content="#8FD2FA">',
    '<meta name="theme-color" content="#E3AE88">', "theme colour")
rep("h1 .line2{display:block;background:linear-gradient(100deg,#C93026 6%,#EE5A2E 42%,#2450BE 94%);",
    "h1 .line2{display:block;background:linear-gradient(100deg,#1F5138 6%,#7A4A2A 44%,#234C5C 94%);", "h1 gradient")

# ── copy ───────────────────────────────────────────────────────────────────
rep("<title>Balloon Bicycle Embroidered Linen Shirt | Baby Bling</title>",
    "<title>Little Gardener Embroidered Linen Shirt | Baby Bling</title>", "title")
rep('content="A soft pink linen Cuban collar shirt with a hand-embroidered bicycle carrying red and blue balloons. Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">',
    'content="A pale sage linen Cuban collar shirt with a hand-embroidered houseplant and watering can in dark green thread. Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">', "description")
rep('<meta property="og:title" content="Balloon Bicycle Embroidered Linen Shirt — Baby Bling">',
    '<meta property="og:title" content="Little Gardener Embroidered Linen Shirt — Baby Bling">', "og")
soft("Balloon Bicycle Embroidered Linen Shirt", "Little Gardener Embroidered Linen Shirt")
rep("Balloon Bicycle Linen Shirt", "Little Gardener Linen Shirt", "short name", count=99)

rep("""<h1>Balloon Bicycle<span class="line2">Shirt</span></h1>""",
    """<h1>Little Gardener<span class="line2">Shirt</span></h1>""", "h1")
rep("So light, they forget it's on.", 'So light, the garden comes along.', "tagline")
rep("Breathable linen, coconut wood buttons, and a bicycle stitched on by hand.",
    "Breathable sage linen, coconut wood buttons, and a garden stitched on by hand.", "hero sub")
rep('<span class="em">🧵</span> Hand embroidered', '<span class="em">🌿</span> Hand embroidered', "pill")
rep("Let them go<br>ride the balloons.", "Let them go<br>dig something up.", "final h2")
rep("<h2>Made for exactly those days.</h2>", "<h2>Made for the outdoor days.</h2>", "why h2")
rep("Embroidered by hand, in small batches", "Every leaf embroidered by hand, in small batches", "urgency")
rep("Peach Sorbet", "Pale Sage", "colour name", count=99)

rep("<h3>Hand-stitched bicycle</h3><p>Thread on thread — no plastic print to crack, peel or fade in the wash.</p>",
    "<h3>Hand-stitched houseplant</h3><p>Broad leaves in dark green outline stitch, rising from a little speckled pot — no plastic print to crack or peel.</p>", "card3")
rep("<h3>The Bling patch</h3><p>Our woven signature at the hem. Small, but it's how you know it's real.</p>",
    "<h3>The watering can</h3><p>A daisy on its side and a long spout, stitched at the chest — the other half of the story.</p>", "card4")

rep('<span style="font-size:1.6rem">🚲</span>', '<span style="font-size:1.6rem">🌿</span>', "why icon 1")
rep("<p>A whimsical bicycle carrying one red and one blue balloon, stitched thread-on-thread. There is no print to crack, peel or fade in the wash.</p>",
    "<p>A potted plant and a watering can, outlined in dark green thread-on-thread. There is no print to crack, peel or fade in the wash.</p>", "why 1")
rep("<p>Soft pink linen in an open Cuban collar cut — as comfortable as it is charming, for playdates, outings, or making an ordinary day feel magical.</p>",
    "<p>Pale sage linen in an open Cuban collar cut — as comfortable as it is charming, for playdates, outings, or making an ordinary day feel magical.</p>", "why 2")
rep('alt="Baby Bling peach linen cotton kids shirt with hand-embroidered bicycle and balloons"',
    'alt="Baby Bling pale sage linen kids shirt with a hand-embroidered houseplant and watering can"', "hero alt")
soft('alt="A child holding up the Baby Bling Balloon Ride Shirt"',
     'alt="A child holding up the Baby Bling Little Gardener shirt"')

# ── decorative balloons -> falling leaves ──────────────────────────────────
def _leaf(cls, col, vein):
    return ('<svg class="bln %s" viewBox="0 0 56 88" aria-hidden="true">'
            '<path d="M28 6C10 20 6 42 28 58 50 42 46 20 28 6Z" fill="%s"/>'
            '<path d="M28 8V58M28 22 16 30M28 22 40 30M28 36 18 44M28 36 38 44" stroke="%s" '
            'stroke-width="1.8" stroke-linecap="round" fill="none"/>'
            '<path d="M28 58c6 8-6 12-1 22" stroke="#0E2F4C" stroke-width="1.5" fill="none" '
            'stroke-linecap="round" opacity=".35"/></svg>') % (cls, col, vein)

blns = re.findall(r'<svg class="bln [abc]".*?</svg>', s, re.S)
assert len(blns) == 3, "expected 3 decorative shapes, found %d" % len(blns)
for old_svg, new_svg in zip(blns, [_leaf("a", "#2E6B45", "#8FBF9C"),
                                   _leaf("b", "#4F8A5C", "#D8EBDC"),
                                   _leaf("c", "#1F5138", "#7FB08D")]):
    s = s.replace(old_svg, new_svg, 1)
rep(".bln{position:absolute;width:clamp(30px,7vw,54px);",
    ".bln{position:absolute;width:clamp(22px,5vw,40px);", "leaf size")

io.open("index-sea.html", "w", encoding="utf-8").write(s)
print("index-sea.html written (%d -> %d bytes)" % (n0, len(s)))

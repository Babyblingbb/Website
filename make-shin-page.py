#!/usr/bin/env python3
"""index.html (peach / Balloon Bicycle)  ->  index-shin.html (cream / Shinchan).

This shirt's embroidery is licensed cartoon characters, so every image on this
page is the brand's own photography — no AI renders were generated for it. The
hero is a background-knockout of the real front shot instead.

Cream needs a saturated sky to separate: a bright cornflower blue with a warm
sun band, kept mid-tone across the hero so the navy headline still reads.
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

# ── assets (all real photography) ───────────────────────────────────────────
for old, new in {"shirt":"bn-shirt", "back":"bn-back", "d-collar":"bn-d-dog",
                 "d-buttons":"bn-d-buttons", "d-embroidery":"bn-d-shin",
                 "d-patch":"bn-d-robot", "lifestyle":"bn-lifestyle",
                 "folded":"bn-macro"}.items():
    rep("assets/%s.webp" % old, "assets-shin/%s.webp" % new, "asset " + old, count=99)
rep('aria-label="Folded"', 'aria-label="Embroidery"', "thumb label")

# ── hero geometry (bn-shirt is 936x923) ────────────────────────────────────
rep("aspect-ratio:778/835", "aspect-ratio:956/926", "aspect")
rep('width="778" height="835"', 'width="956" height="926"', "img dims", count=99)

# ── sunny cornflower sky ───────────────────────────────────────────────────
rep("  --sky-0:#5FB9F5; --sky-1:#8FD2FA; --sky-2:#BFE7FE; --sky-3:#E4F5FF;",
    "  --sky-0:#3E72D6; --sky-1:#74A0EA; --sky-2:#A9C8F6; --sky-3:#DCE9FC;", "sky vars")
rep("""    #4FB2F3 0%, #79C9F8 8%, #A8DEFC 17%,
    #D2EEFE 27%, #EAF7FF 34%, #D6F0FF 42%,
    #B9E4FD 52%, #E6F6FF 62%, #FFF1E4 70%,
    #FFE3D2 76%, #D8EEFE 85%, #A6DBFB 93%, #74C4F7 100%)}""",
    """    #A9C8F6 0%, #9CBFF3 8%, #8DB4F0 17%,
    #7FA9ED 27%, #74A0EA 34%, #6B98E7 42%,
    #6291E5 52%, #93B8F1 62%, #FFE9C9 70%,
    #FFD9A8 76%, #B6CDF2 85%, #6A93E6 93%, #3E72D6 100%)}""", "sky gradient")
rep("background:radial-gradient(circle,rgba(255,250,225,.95),rgba(255,238,195,.55) 32%,rgba(255,232,180,0) 66%);",
    "background:radial-gradient(circle,rgba(255,245,200,.98),rgba(255,222,140,.6) 32%,rgba(255,212,120,0) 68%);", "sun")
rep("box-shadow:inset 0 -16px 26px -16px rgba(120,180,220,.42)}",
    "box-shadow:inset 0 -16px 26px -16px rgba(90,140,215,.44)}", "cloud underside")
rep(".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px rgba(240,170,140,.34)}",
    ".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px rgba(245,200,120,.38)}", "warm cloud")
rep("drop-shadow(0 14px 22px rgba(46,116,168,.20))}",
    "drop-shadow(0 14px 22px rgba(40,85,175,.22))}", "cloud shadow css")
rep("'drop-shadow(0 14px 22px rgba(46,116,168,'+(layer===2?.10:.04)+'))'+",
    "'drop-shadow(0 14px 22px rgba(40,85,175,'+(layer===2?.12:.05)+'))'+", "cloud shadow js")
rep('<meta name="theme-color" content="#8FD2FA">',
    '<meta name="theme-color" content="#74A0EA">', "theme colour")
rep("h1 .line2{display:block;background:linear-gradient(100deg,#C93026 6%,#EE5A2E 42%,#2450BE 94%);",
    "h1 .line2{display:block;background:linear-gradient(100deg,#CE2222 6%,#D98A14 44%,#17703F 94%);", "h1 gradient")

# ── copy ───────────────────────────────────────────────────────────────────
rep("<title>Balloon Bicycle Embroidered Linen Shirt | Baby Bling</title>",
    "<title>Shinchan Embroidered Linen Shirt | Baby Bling</title>", "title")
rep('content="A soft pink linen Cuban collar shirt with a hand-embroidered bicycle carrying red and blue balloons. Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">',
    'content="A cream linen Cuban collar shirt with hand-embroidered cartoon characters, a little white dog, a robot and scattered stars. Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">', "description")
rep('<meta property="og:title" content="Balloon Bicycle Embroidered Linen Shirt — Baby Bling">',
    '<meta property="og:title" content="Shinchan Embroidered Linen Shirt — Baby Bling">', "og")
soft("Balloon Bicycle Embroidered Linen Shirt", "Shinchan Embroidered Linen Shirt")
rep("Balloon Bicycle Linen Shirt", "Shinchan Linen Shirt", "short name", count=99)

rep("""<h1>Balloon Bicycle<span class="line2">Shirt</span></h1>""",
    """<h1>Shinchan<span class="line2">Shirt</span></h1>""", "h1")
rep("So light, they forget it's on.", "So light, you'll never get it back.", "tagline")
rep("Breathable linen, coconut wood buttons, and a bicycle stitched on by hand.",
    "Breathable cream linen, coconut wood buttons, and his favourite friends stitched on by hand.", "hero sub")
rep('<span class="em">🧵</span> Hand embroidered', '<span class="em">🖍️</span> Hand embroidered', "pill")
rep("Let them go<br>ride the balloons.", "Let them go<br>be the main character.", "final h2")
rep("<h2>Made for exactly those days.</h2>", "<h2>Made for the loudest days.</h2>", "why h2")
rep("Embroidered by hand, in small batches", "Every character embroidered by hand, in small batches", "urgency")
rep("Peach Sorbet", "Natural Cream", "colour name", count=99)

rep("<h3>Camp collar</h3><p>Soft, open and unstructured — with our woven label and a printed size tag, so nothing scratches the neck.</p>",
    "<h3>A little white dog</h3><p>Stitched mid-trot across the chest, ears up, in fine black outline thread.</p>", "card1")
rep("<h3>Hand-stitched bicycle</h3><p>Thread on thread — no plastic print to crack, peel or fade in the wash.</p>",
    "<h3>Hand-stitched characters</h3><p>Dense satin-stitch in red, yellow and black — thread on thread, no plastic print to crack or peel.</p>", "card3")
rep("<h3>The Bling patch</h3><p>Our woven signature at the hem. Small, but it's how you know it's real.</p>",
    "<h3>Robo &amp; the patch</h3><p>A green robot guarding our woven signature at the hem — the bit they'll show their friends.</p>", "card4")

rep('<span style="font-size:1.6rem">🚲</span>', '<span style="font-size:1.6rem">🖍️</span>', "why icon 1")
rep("<p>A whimsical bicycle carrying one red and one blue balloon, stitched thread-on-thread. There is no print to crack, peel or fade in the wash.</p>",
    "<p>Favourite characters, a little dog, a robot and scattered stars — all stitched thread-on-thread. There is no print to crack, peel or fade in the wash.</p>", "why 1")
rep("<p>Soft pink linen in an open Cuban collar cut — as comfortable as it is charming, for playdates, outings, or making an ordinary day feel magical.</p>",
    "<p>Natural cream linen in an open Cuban collar cut — as comfortable as it is charming, for playdates, outings, or making an ordinary day feel magical.</p>", "why 2")
rep('alt="Baby Bling peach linen cotton kids shirt with hand-embroidered bicycle and balloons"',
    'alt="Baby Bling cream linen kids shirt with hand-embroidered cartoon characters, a dog and a robot"', "hero alt")
soft('alt="A child holding up the Baby Bling Balloon Ride Shirt"',
     'alt="A child holding up the Baby Bling Shinchan shirt"')

# ── decorative balloons -> little stars (the shirt has them too) ───────────
def _star(cls, col):
    return ('<svg class="bln %s" viewBox="0 0 56 80" aria-hidden="true">'
            '<path d="M28 4 35 22 54 24 40 37 44 56 28 46 12 56 16 37 2 24 21 22Z" fill="%s" '
            'stroke="rgba(14,47,76,.35)" stroke-width="1.6"/>'
            '<path d="M28 56c6 8-6 12-1 20" stroke="#0E2F4C" stroke-width="1.5" fill="none" '
            'stroke-linecap="round" opacity=".35"/></svg>') % (cls, col)

blns = re.findall(r'<svg class="bln [abc]".*?</svg>', s, re.S)
assert len(blns) == 3, "expected 3 decorative shapes, found %d" % len(blns)
for old_svg, new_svg in zip(blns, [_star("a", "#F5C518"), _star("b", "#E8452C"),
                                   _star("c", "#F5C518")]):
    s = s.replace(old_svg, new_svg, 1)
rep(".bln{position:absolute;width:clamp(30px,7vw,54px);",
    ".bln{position:absolute;width:clamp(22px,5vw,38px);", "star size")

io.open("index-shin.html", "w", encoding="utf-8").write(s)
print("index-shin.html written (%d -> %d bytes)" % (n0, len(s)))

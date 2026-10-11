#!/usr/bin/env python3
"""index.html (peach / Balloon Bicycle)  ->  index-pink.html (blush / Hearts).

Pink on a pink-ish sky would vanish, so this page gets a fresh mint morning sky.
Written out in full; every substitution asserts via rep().
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
for old, new in {"shirt":"bp-shirt", "back":"bp-back", "d-collar":"bp-d-collar",
                 "d-buttons":"bp-d-buttons", "d-embroidery":"bp-d-hearts",
                 "d-patch":"bp-d-patch", "lifestyle":"bp-lifestyle",
                 "folded":"bp-clouds"}.items():
    rep("assets/%s.webp" % old, "assets-pink/%s.webp" % new, "asset " + old, count=99)

rep('<button class="bvt"     data-src="assets-pink/bp-clouds.webp"       aria-label="Folded"><img src="assets-pink/bp-clouds.webp" alt="" loading="lazy"></button>',
    '<button class="bvt"     data-src="assets-pink/bp-clouds.webp"   aria-label="In the sky"><img src="assets-pink/bp-clouds.webp" alt="" loading="lazy"></button>\n'
    '        <button class="bvt"     data-src="assets-pink/bp-folded.webp"   aria-label="Folded"><img src="assets-pink/bp-folded.webp" alt="" loading="lazy"></button>',
    "extra thumb")

# ── hero geometry (bp-shirt is 735x785) ────────────────────────────────────
rep("aspect-ratio:778/835", "aspect-ratio:735/785", "aspect")
rep('width="778" height="835"', 'width="735" height="785"', "img dims", count=99)

# ── mint morning sky ───────────────────────────────────────────────────────
rep("  --sky-0:#5FB9F5; --sky-1:#8FD2FA; --sky-2:#BFE7FE; --sky-3:#E4F5FF;",
    "  --sky-0:#7FCFC0; --sky-1:#A8E0D4; --sky-2:#CFEFE7; --sky-3:#EFFAF6;", "sky vars")
rep("""    #4FB2F3 0%, #79C9F8 8%, #A8DEFC 17%,
    #D2EEFE 27%, #EAF7FF 34%, #D6F0FF 42%,
    #B9E4FD 52%, #E6F6FF 62%, #FFF1E4 70%,
    #FFE3D2 76%, #D8EEFE 85%, #A6DBFB 93%, #74C4F7 100%)}""",
    """    #63C2B2 0%, #85D2C4 8%, #A9E0D5 17%,
    #CBEFE7 27%, #E6F8F3 34%, #CFEFE6 42%,
    #AEE2D7 52%, #E4F7F2 62%, #FFF2F3 70%,
    #FBDCE2 76%, #D6EEE9 85%, #A5DDD1 93%, #7CCBBC 100%)}""", "sky gradient")
rep("background:radial-gradient(circle,rgba(255,250,225,.95),rgba(255,238,195,.55) 32%,rgba(255,232,180,0) 66%);",
    "background:radial-gradient(circle,rgba(255,252,240,.95),rgba(225,245,232,.55) 34%,rgba(215,242,228,0) 68%);", "sun")
rep("box-shadow:inset 0 -16px 26px -16px rgba(120,180,220,.42)}",
    "box-shadow:inset 0 -16px 26px -16px rgba(110,180,165,.42)}", "cloud underside")
rep(".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px rgba(240,170,140,.34)}",
    ".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px rgba(240,165,180,.34)}", "warm cloud")
rep("drop-shadow(0 14px 22px rgba(46,116,168,.20))}",
    "drop-shadow(0 14px 22px rgba(60,145,130,.20))}", "cloud shadow css")
rep("'drop-shadow(0 14px 22px rgba(46,116,168,'+(layer===2?.10:.04)+'))'+",
    "'drop-shadow(0 14px 22px rgba(60,145,130,'+(layer===2?.10:.04)+'))'+", "cloud shadow js")
rep('<meta name="theme-color" content="#8FD2FA">',
    '<meta name="theme-color" content="#A8E0D4">', "theme colour")
rep("h1 .line2{display:block;background:linear-gradient(100deg,#C93026 6%,#EE5A2E 42%,#2450BE 94%);",
    "h1 .line2{display:block;background:linear-gradient(100deg,#B82A55 6%,#D94A72 44%,#1F7F6E 94%);", "h1 gradient")

# ── copy ───────────────────────────────────────────────────────────────────
rep("<title>Balloon Bicycle Embroidered Linen Shirt | Baby Bling</title>",
    "<title>Hearts Embroidered Linen Shirt | Baby Bling</title>", "title")
rep('content="A soft pink linen Cuban collar shirt with a hand-embroidered bicycle carrying red and blue balloons. Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">',
    'content="A blush pink linen Cuban collar shirt scattered with hand-embroidered outline hearts. Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">', "description")
rep('<meta property="og:title" content="Balloon Bicycle Embroidered Linen Shirt — Baby Bling">',
    '<meta property="og:title" content="Hearts Embroidered Linen Shirt — Baby Bling">', "og")
soft("Balloon Bicycle Embroidered Linen Shirt", "Hearts Embroidered Linen Shirt")
rep("Balloon Bicycle Linen Shirt", "Hearts Linen Shirt", "short name", count=99)

rep("""<h1>Balloon Bicycle<span class="line2">Shirt</span></h1>""",
    """<h1>Hearts<span class="line2">Shirt</span></h1>""", "h1")
rep("So light, they forget it's on.", "So light, it's all heart.", "tagline")
rep("Breathable linen, coconut wood buttons, and a bicycle stitched on by hand.",
    "Breathable pink linen, coconut wood buttons, and hearts stitched on by hand.", "hero sub")
rep('<span class="em">🧵</span> Hand embroidered', '<span class="em">💗</span> Hand embroidered', "pill")
rep("Let them go<br>ride the balloons.", "Let them go<br>love it to bits.", "final h2")
rep("<h2>Made for exactly those days.</h2>", "<h2>Made for the soft days.</h2>", "why h2")
rep("Embroidered by hand, in small batches", "Every heart embroidered by hand, in small batches", "urgency")
rep("Peach Sorbet", "Blush Pink", "colour name", count=99)

rep("<h3>Hand-stitched bicycle</h3><p>Thread on thread — no plastic print to crack, peel or fade in the wash.</p>",
    "<h3>Hand-stitched hearts</h3><p>Single-line outlines in deeper rose thread, scattered by hand — no plastic print to crack or peel.</p>", "card3")
rep('<span style="font-size:1.6rem">🚲</span>', '<span style="font-size:1.6rem">💗</span>', "why icon 1")
rep("<p>A whimsical bicycle carrying one red and one blue balloon, stitched thread-on-thread. There is no print to crack, peel or fade in the wash.</p>",
    "<p>Hearts of every size scattered across the front, each one a single line of running stitch. There is no print to crack, peel or fade in the wash.</p>", "why 1")
rep('alt="Baby Bling peach linen cotton kids shirt with hand-embroidered bicycle and balloons"',
    'alt="Baby Bling blush pink linen kids shirt scattered with hand-embroidered hearts"', "hero alt")
soft('alt="A child holding up the Baby Bling Balloon Ride Shirt"',
     'alt="A child holding up the Baby Bling Hearts shirt"')

# ── decorative balloons -> hearts ──────────────────────────────────────────
def _heart(cls, fill):
    return ('<svg class="bln %s" viewBox="0 0 64 84" aria-hidden="true">'
            '<path d="M32 26C32 14 20 8 13 15 5 23 10 36 32 54 54 36 59 23 51 15 44 8 32 14 32 26Z" '
            'fill="%s"/><path d="M20 20c-4 2-5 7-2 11" stroke="#fff" stroke-width="2.4" '
            'fill="none" stroke-linecap="round" opacity=".5"/>'
            '<path d="M32 54c5 8-6 12-1 22" stroke="#0E2F4C" stroke-width="1.5" fill="none" '
            'stroke-linecap="round" opacity=".4"/></svg>') % (cls, fill)

blns = re.findall(r'<svg class="bln [abc]".*?</svg>', s, re.S)
assert len(blns) == 3, "expected 3 decorative shapes, found %d" % len(blns)
for old_svg, new_svg in zip(blns, [_heart("a", "#D94A72"), _heart("b", "#F2909F"),
                                   _heart("c", "#B82A55")]):
    s = s.replace(old_svg, new_svg, 1)
rep(".bln{position:absolute;width:clamp(30px,7vw,54px);",
    ".bln{position:absolute;width:clamp(22px,5vw,40px);", "heart size")

io.open("index-pink.html", "w", encoding="utf-8").write(s)
print("index-pink.html written (%d -> %d bytes)" % (n0, len(s)))

#!/usr/bin/env python3
"""index.html (peach / Balloon Bicycle)  ->  index-dino.html (cream / Dino).

Cream on a cream sky would vanish, so this page gets a jade-to-teal jungle sky.
The gradient is kept mid-tone across the hero band: dark enough that a cream
shirt separates, light enough that the navy headline still reads on it.
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
for old, new in {"shirt":"bd-shirt", "back":"bd-back", "d-collar":"bd-d-collar",
                 "d-buttons":"bd-d-cloud", "d-embroidery":"bd-d-dino",
                 "d-patch":"bd-d-fern", "lifestyle":"bd-lifestyle",
                 "folded":"bd-clouds"}.items():
    rep("assets/%s.webp" % old, "assets-dino/%s.webp" % new, "asset " + old, count=99)

rep('<button class="bvt"     data-src="assets-dino/bd-clouds.webp"       aria-label="Folded"><img src="assets-dino/bd-clouds.webp" alt="" loading="lazy"></button>',
    '<button class="bvt"     data-src="assets-dino/bd-clouds.webp"   aria-label="In the sky"><img src="assets-dino/bd-clouds.webp" alt="" loading="lazy"></button>\n'
    '        <button class="bvt"     data-src="assets-dino/bd-folded.webp"   aria-label="Folded"><img src="assets-dino/bd-folded.webp" alt="" loading="lazy"></button>',
    "extra thumb")

# ── hero geometry (bd-shirt is 847x849) ────────────────────────────────────
rep("aspect-ratio:778/835", "aspect-ratio:853/855", "aspect")
rep('width="778" height="835"', 'width="853" height="855"', "img dims", count=99)

# ── jungle sky ─────────────────────────────────────────────────────────────
rep("  --sky-0:#5FB9F5; --sky-1:#8FD2FA; --sky-2:#BFE7FE; --sky-3:#E4F5FF;",
    "  --sky-0:#3E9C94; --sky-1:#7FC0B2; --sky-2:#A6D2C6; --sky-3:#DCEFE6;", "sky vars")
rep("""    #4FB2F3 0%, #79C9F8 8%, #A8DEFC 17%,
    #D2EEFE 27%, #EAF7FF 34%, #D6F0FF 42%,
    #B9E4FD 52%, #E6F6FF 62%, #FFF1E4 70%,
    #FFE3D2 76%, #D8EEFE 85%, #A6DBFB 93%, #74C4F7 100%)}""",
    """    #B8DCD1 0%, #A6D2C6 8%, #93C9BC 17%,
    #7FC0B2 27%, #6FB7AA 34%, #5FAEA1 42%,
    #4FA396 52%, #86C3B5 62%, #E9DFC4 70%,
    #EBD3A8 76%, #A9CBBE 85%, #5FA79C 93%, #3E9C94 100%)}""", "sky gradient")
rep("background:radial-gradient(circle,rgba(255,250,225,.95),rgba(255,238,195,.55) 32%,rgba(255,232,180,0) 66%);",
    "background:radial-gradient(circle,rgba(255,244,205,.95),rgba(246,214,140,.5) 34%,rgba(240,205,130,0) 68%);", "sun")
rep("box-shadow:inset 0 -16px 26px -16px rgba(120,180,220,.42)}",
    "box-shadow:inset 0 -16px 26px -16px rgba(60,135,125,.44)}", "cloud underside")
rep(".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px rgba(240,170,140,.34)}",
    ".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px rgba(222,186,120,.38)}", "warm cloud")
rep("drop-shadow(0 14px 22px rgba(46,116,168,.20))}",
    "drop-shadow(0 14px 22px rgba(25,95,88,.22))}", "cloud shadow css")
rep("'drop-shadow(0 14px 22px rgba(46,116,168,'+(layer===2?.10:.04)+'))'+",
    "'drop-shadow(0 14px 22px rgba(25,95,88,'+(layer===2?.12:.05)+'))'+", "cloud shadow js")
rep('<meta name="theme-color" content="#8FD2FA">',
    '<meta name="theme-color" content="#7FC0B2">', "theme colour")
rep("h1 .line2{display:block;background:linear-gradient(100deg,#C93026 6%,#EE5A2E 42%,#2450BE 94%);",
    "h1 .line2{display:block;background:linear-gradient(100deg,#C2611A 6%,#E0892A 42%,#12554F 94%);", "h1 gradient")

# ── copy ───────────────────────────────────────────────────────────────────
rep("<title>Balloon Bicycle Embroidered Linen Shirt | Baby Bling</title>",
    "<title>Dino Adventure Embroidered Linen Shirt | Baby Bling</title>", "title")
rep('content="A soft pink linen Cuban collar shirt with a hand-embroidered bicycle carrying red and blue balloons. Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">',
    'content="A cream linen Cuban collar shirt with a whole hand-embroidered scene — a long-necked dinosaur, a sun, a cloud and a little fern. Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">', "description")
rep('<meta property="og:title" content="Balloon Bicycle Embroidered Linen Shirt — Baby Bling">',
    '<meta property="og:title" content="Dino Adventure Embroidered Linen Shirt — Baby Bling">', "og")
soft("Balloon Bicycle Embroidered Linen Shirt", "Dino Adventure Embroidered Linen Shirt")
rep("Balloon Bicycle Linen Shirt", "Dino Adventure Linen Shirt", "short name", count=99)

rep("""<h1>Balloon Bicycle<span class="line2">Shirt</span></h1>""",
    """<h1>Dino Adventure<span class="line2">Shirt</span></h1>""", "h1")
rep("So light, they forget it's on.", 'So light, the adventure keeps up.', "tagline")
rep("Breathable linen, coconut wood buttons, and a bicycle stitched on by hand.",
    "Breathable cream linen, coconut wood buttons, and a whole world stitched on by hand.", "hero sub")
rep('<span class="em">🧵</span> Hand embroidered', '<span class="em">🦕</span> Hand embroidered', "pill")
rep("Let them go<br>ride the balloons.", "Let them go<br>explore something.", "final h2")
rep("<h2>Made for exactly those days.</h2>", "<h2>Made for the muddy ones.</h2>", "why h2")
rep("Embroidered by hand, in small batches", "Every dinosaur embroidered by hand, in small batches", "urgency")
rep("Peach Sorbet", "Natural Cream", "colour name", count=99)

rep("<h3>Coconut wood buttons</h3><p>Real wood, smooth-sanded edges, stitched twice over so they stay put.</p>",
    "<h3>Sun &amp; cloud</h3><p>A yellow sun and a blue outline cloud sit above the placket, right where a small person will find them.</p>", "card2")
rep("<h3>Hand-stitched bicycle</h3><p>Thread on thread — no plastic print to crack, peel or fade in the wash.</p>",
    "<h3>Hand-stitched dinosaur</h3><p>A long-necked friend outlined in blue with yellow spots — thread on thread, no plastic print to crack or peel.</p>", "card3")
rep("<h3>The Bling patch</h3><p>Our woven signature at the hem. Small, but it's how you know it's real.</p>",
    "<h3>A whole little world</h3><p>A fern, a tiny snail, a star and our woven patch — the details they'll keep finding.</p>", "card4")

rep('<span style="font-size:1.6rem">🚲</span>', '<span style="font-size:1.6rem">🦕</span>', "why icon 1")
rep("<p>A whimsical bicycle carrying one red and one blue balloon, stitched thread-on-thread. There is no print to crack, peel or fade in the wash.</p>",
    "<p>A dinosaur, a sun, a cloud, a fern and a snail — a whole scene stitched thread-on-thread. There is no print to crack, peel or fade in the wash.</p>", "why 1")
rep("<p>Soft pink linen in an open Cuban collar cut — as comfortable as it is charming, for playdates, outings, or making an ordinary day feel magical.</p>",
    "<p>Natural cream linen in an open Cuban collar cut — as comfortable as it is charming, for playdates, outings, or making an ordinary day feel magical.</p>", "why 2")
rep('alt="Baby Bling peach linen cotton kids shirt with hand-embroidered bicycle and balloons"',
    'alt="Baby Bling cream linen kids shirt with a hand-embroidered dinosaur, sun and cloud"', "hero alt")
soft('alt="A child holding up the Baby Bling Balloon Ride Shirt"',
     'alt="A child holding up the Baby Bling Dino Adventure shirt"')

# ── decorative balloons -> fern fronds ─────────────────────────────────────
def _fern(cls, col):
    return ('<svg class="bln %s" viewBox="0 0 54 96" aria-hidden="true">'
            '<path d="M27 92V16" stroke="%s" stroke-width="3" stroke-linecap="round"/>'
            '<path d="M27 26c-8-6-16-6-20-2 4 6 12 8 20 2Zm0 0c8-6 16-6 20-2-4 6-12 8-20 2Z" fill="%s"/>'
            '<path d="M27 44c-7-5-14-5-18-1 4 5 11 7 18 1Zm0 0c7-5 14-5 18-1-4 5-11 7-18 1Z" fill="%s"/>'
            '<path d="M27 62c-6-4-12-4-15-1 3 5 9 6 15 1Zm0 0c6-4 12-4 15-1-3 5-9 6-15 1Z" fill="%s"/>'
            '</svg>') % (cls, col, col, col, col)

blns = re.findall(r'<svg class="bln [abc]".*?</svg>', s, re.S)
assert len(blns) == 3, "expected 3 decorative shapes, found %d" % len(blns)
for old_svg, new_svg in zip(blns, [_fern("a", "#2E8B6F"), _fern("b", "#5FAE7A"),
                                   _fern("c", "#1F7A78")]):
    s = s.replace(old_svg, new_svg, 1)
rep(".bln{position:absolute;width:clamp(30px,7vw,54px);",
    ".bln{position:absolute;width:clamp(24px,5.5vw,44px);", "fern size")

io.open("index-dino.html", "w", encoding="utf-8").write(s)
print("index-dino.html written (%d -> %d bytes)" % (n0, len(s)))

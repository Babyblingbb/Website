#!/usr/bin/env python3
"""index.html (peach / Balloon Bicycle)  ->  index-story.html (maroon / Storytelling).

Deep maroon needs a light, cool backdrop to separate, and the shirt's embroidery
(camera, books, a steaming cup) is a story-time motif — so this page gets a soft
twilight sky: periwinkle through lavender to a dusty-rose horizon.

Every substitution goes through rep(), which asserts. An unchecked str.replace
here once failed silently and shipped the wrong prompt into a render.
"""
import io, re

s = io.open("index.html", encoding="utf-8").read()
n0 = len(s)

def rep(a, b, why, count=1):
    global s
    assert a in s, "MISSING (%s): %s" % (why, a[:70])
    s = s.replace(a, b, count)

def soft(a, b):
    """For strings an earlier rep() may already have consumed."""
    global s
    s = s.replace(a, b)

# ── 1. assets ───────────────────────────────────────────────────────────────
ASSET_MAP = {
    "shirt":        "bs-shirt",       # AI 3D ghost-mannequin cut-out
    "back":         "bs-back",        # real back view, cut out
    "d-collar":     "bs-d-collar",    # real collar + woven label
    "d-buttons":    "bs-d-buttons",   # real coconut buttons
    "d-embroidery": "bs-d-camera",    # real camera embroidery
    "d-patch":      "bs-d-books",     # real books + coffee cup
    "lifestyle":    "bs-lifestyle",   # real photo of a child holding it
    "folded":       "bs-clouds",      # AI twilight render
}
for old, new in ASSET_MAP.items():
    rep("assets/%s.webp" % old, "assets-story/%s.webp" % new, "asset " + old, count=99)

# two extra gallery views
rep('<button class="bvt"     data-src="assets-story/bs-clouds.webp"       aria-label="Folded"><img src="assets-story/bs-clouds.webp" alt="" loading="lazy"></button>',
    '<button class="bvt"     data-src="assets-story/bs-clouds.webp"   aria-label="In the sky"><img src="assets-story/bs-clouds.webp" alt="" loading="lazy"></button>\n'
    '        <button class="bvt"     data-src="assets-story/bs-folded.webp"   aria-label="Folded"><img src="assets-story/bs-folded.webp" alt="" loading="lazy"></button>\n'
    '        <button class="bvt"     data-src="assets-story/bs-d-macro.webp"  aria-label="Stitch close-up"><img src="assets-story/bs-d-macro.webp" alt="" loading="lazy"></button>',
    "extra thumbs")

# ── 2. hero geometry (bs-shirt is 865x847) ─────────────────────────────────
rep("aspect-ratio:778/835", "aspect-ratio:865/847", "aspect")
rep('width="778" height="835"', 'width="865" height="847"', "img dims", count=99)

# ── 3. twilight sky ────────────────────────────────────────────────────────
rep("  --sky-0:#5FB9F5; --sky-1:#8FD2FA; --sky-2:#BFE7FE; --sky-3:#E4F5FF;",
    "  --sky-0:#8C86C9; --sky-1:#B3A7DA; --sky-2:#D9CEEA; --sky-3:#F3EAF7;", "sky vars")
rep("""    #4FB2F3 0%, #79C9F8 8%, #A8DEFC 17%,
    #D2EEFE 27%, #EAF7FF 34%, #D6F0FF 42%,
    #B9E4FD 52%, #E6F6FF 62%, #FFF1E4 70%,
    #FFE3D2 76%, #D8EEFE 85%, #A6DBFB 93%, #74C4F7 100%)}""",
    """    #6E68B8 0%, #8C86C9 8%, #AEA3D8 17%,
    #CFC4E6 27%, #E8DCEF 34%, #D8C6E4 42%,
    #C3A9D6 52%, #E9D9EC 62%, #FBE3DE 70%,
    #F7CFCB 76%, #D9C8E8 85%, #A99DD2 93%, #8079C0 100%)}""", "sky gradient")
rep("background:radial-gradient(circle,rgba(255,250,225,.95),rgba(255,238,195,.55) 32%,rgba(255,232,180,0) 66%);",
    "background:radial-gradient(circle,rgba(255,231,210,.95),rgba(255,198,180,.5) 34%,rgba(250,190,180,0) 68%);", "sun")
rep("box-shadow:inset 0 -16px 26px -16px rgba(120,180,220,.42)}",
    "box-shadow:inset 0 -16px 26px -16px rgba(150,120,185,.44)}", "cloud underside")
rep(".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px rgba(240,170,140,.34)}",
    ".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px rgba(228,150,155,.38)}", "warm cloud")
rep("drop-shadow(0 14px 22px rgba(46,116,168,.20))}",
    "drop-shadow(0 14px 22px rgba(120,95,165,.20))}", "cloud shadow css")
rep("'drop-shadow(0 14px 22px rgba(46,116,168,'+(layer===2?.10:.04)+'))'+",
    "'drop-shadow(0 14px 22px rgba(120,95,165,'+(layer===2?.10:.04)+'))'+", "cloud shadow js")
rep('<meta name="theme-color" content="#8FD2FA">',
    '<meta name="theme-color" content="#B3A7DA">', "theme colour")
# headline gradient in the shirt's own palette
rep("h1 .line2{display:block;background:linear-gradient(100deg,#C93026 6%,#EE5A2E 42%,#2450BE 94%);",
    "h1 .line2{display:block;background:linear-gradient(100deg,#6F1628 6%,#9E2F45 44%,#3B2E78 94%);", "h1 gradient")

# ── 4. copy ────────────────────────────────────────────────────────────────
rep("<title>Balloon Bicycle Embroidered Linen Shirt | Baby Bling</title>",
    "<title>Storytelling Embroidered Linen Shirt | Baby Bling</title>", "title")
rep('content="A soft pink linen Cuban collar shirt with a hand-embroidered bicycle carrying red and blue balloons. Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">',
    'content="A deep maroon linen Cuban collar shirt with a hand-embroidered film camera, a stack of storybooks and a steaming cup. Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">', "description")
rep('<meta property="og:title" content="Balloon Bicycle Embroidered Linen Shirt — Baby Bling">',
    '<meta property="og:title" content="Storytelling Embroidered Linen Shirt — Baby Bling">', "og")
soft("Balloon Bicycle Embroidered Linen Shirt", "Storytelling Embroidered Linen Shirt")
rep("Balloon Bicycle Linen Shirt", "Storytelling Linen Shirt", "short name", count=99)

rep("""<h1>Balloon Bicycle<span class="line2">Shirt</span></h1>""",
    """<h1>Storytelling<span class="line2">Shirt</span></h1>""", "h1")
rep("So light, they forget it's on.", 'So light, one more story is easy.', "tagline")
rep("Breathable linen, coconut wood buttons, and a bicycle stitched on by hand.",
    "Breathable maroon linen, coconut wood buttons, and a camera stitched on by hand.", "hero sub")
rep('<span class="em">🧵</span> Hand embroidered', '<span class="em">📷</span> Hand embroidered', "pill")
rep("Let them go<br>chase the wind.", "Let them go<br>collect the stories.", "final h2") \
    if "Let them go<br>chase the wind." in s else \
    rep("Let them go<br>ride the balloons.", "Let them go<br>collect the stories.", "final h2")
rep("<h2>Made for exactly those days.</h2>", "<h2>Made for the long stories.</h2>", "why h2")
rep("Embroidered by hand, in small batches", "Every camera embroidered by hand, in small batches", "urgency")
rep("Peach Sorbet", "Deep Maroon", "colour name", count=99)

# details cards
rep("<h3>Hand-stitched bicycle</h3><p>Thread on thread — no plastic print to crack, peel or fade in the wash.</p>",
    "<h3>Hand-stitched camera</h3><p>A little film camera in fine cream outline stitch — thread on thread, no plastic print to crack or peel.</p>", "card3")
rep("<h3>The Bling patch</h3><p>Our woven signature at the hem. Small, but it's how you know it's real.</p>",
    "<h3>Books &amp; a hot cup</h3><p>A stack of storybooks with a steaming cup on top — for the ones who never want the chapter to end.</p>", "card4")

# "why this shirt" cards
rep('<span style="font-size:1.6rem">🚲</span>', '<span style="font-size:1.6rem">📷</span>', "why icon 1")
rep("<p>A whimsical bicycle carrying one red and one blue balloon, stitched thread-on-thread. There is no print to crack, peel or fade in the wash.</p>",
    "<p>A film camera, a stack of books and a steaming cup, all outlined in fine cream thread. There is no print to crack, peel or fade in the wash.</p>", "why 1")
rep("<p>Soft pink linen in an open Cuban collar cut — as comfortable as it is charming, for playdates, outings, or making an ordinary day feel magical.</p>",
    "<p>Deep maroon linen in an open Cuban collar cut — as comfortable as it is charming, for playdates, outings, or making an ordinary day feel magical.</p>", "why 2")

# alt text
rep('alt="Baby Bling peach linen cotton kids shirt with hand-embroidered bicycle and balloons"',
    'alt="Baby Bling deep maroon linen kids shirt with a hand-embroidered camera, books and cup"', "hero alt")
rep('alt="A child holding up the Baby Bling Balloon Ride Shirt"',
    'alt="A child holding up the Baby Bling Storytelling shirt"', "fabric alt") \
    if 'alt="A child holding up the Baby Bling Balloon Ride Shirt"' in s else None

# ── 5. decorative balloons -> tiny books ───────────────────────────────────
def _book(cls, cover, pages):
    return ('<svg class="bln %s" viewBox="0 0 64 88" aria-hidden="true">'
            '<path d="M8 16h22v46H8z" fill="%s"/><path d="M34 16h22v46H34z" fill="%s"/>'
            '<path d="M30 14h4v50h-4z" fill="rgba(14,47,76,.45)"/>'
            '<path d="M12 26h14M12 34h14M38 26h14M38 34h14" stroke="rgba(14,47,76,.28)" stroke-width="1.6"/>'
            '<path d="M32 64c6 8-6 13-1 22" stroke="#0E2F4C" stroke-width="1.5" fill="none" '
            'stroke-linecap="round" opacity=".45"/></svg>') % (cls, cover, pages)

blns = re.findall(r'<svg class="bln [abc]".*?</svg>', s, re.S)
assert len(blns) == 3, "expected 3 decorative shapes, found %d" % len(blns)
for old_svg, new_svg in zip(blns, [_book("a", "#8E2740", "#F3E7D8"),
                                   _book("b", "#5B4B9E", "#F3E7D8"),
                                   _book("c", "#C0495B", "#FBF2E6")]):
    s = s.replace(old_svg, new_svg, 1)
rep(".bln{position:absolute;width:clamp(30px,7vw,54px);",
    ".bln{position:absolute;width:clamp(24px,5.5vw,42px);", "book size")

io.open("index-story.html", "w", encoding="utf-8").write(s)
print("index-story.html written (%d -> %d bytes)" % (n0, len(s)))

#!/usr/bin/env python3
"""index.html (peach / Balloon Bicycle)  ->  index-kite.html (blue / Kite Dreams).

A pale blue shirt on a pale blue sky has almost no contrast, so this page gets a
warm golden-hour sky instead. Everything structural is shared with the peach page.
"""
import io, re

s = io.open("index.html", encoding="utf-8").read()
n = len(s)

def rep(a, b, why, count=1):
    global s
    assert a in s, "MISSING (%s): %s" % (why, a[:70])
    s = s.replace(a, b, count)

# ── 1. assets ────────────────────────────────────────────────────────────────
ASSET_MAP = {
    "shirt":        "bk-shirt",      # AI 3D ghost-mannequin cut-out
    "back":         "bk-back",       # real back view, cut out
    "d-collar":     "bk-d-cloud",    # details card 1 -> cloud embroidery
    "d-buttons":    "bk-d-buttons",
    "d-embroidery": "bk-d-kite",     # details card 3 + gallery
    "d-patch":      "bk-d-patch",
    "lifestyle":    "bk-folded",     # fabric panel + gallery
    "folded":       "bk-clouds",     # gallery
}
for old, new in ASSET_MAP.items():
    s = s.replace("assets/%s.webp" % old, "assets-kite/%s.webp" % new)

# one extra gallery view: the real collar + woven label
rep('<button class="bvt"     data-src="assets-kite/bk-clouds.webp"       aria-label="Folded"><img src="assets-kite/bk-clouds.webp" alt="" loading="lazy"></button>',
    '<button class="bvt"     data-src="assets-kite/bk-clouds.webp"    aria-label="In the sky"><img src="assets-kite/bk-clouds.webp" alt="" loading="lazy"></button>\n'
    '        <button class="bvt"     data-src="assets-kite/bk-d-collar.webp"  aria-label="Collar"><img src="assets-kite/bk-d-collar.webp" alt="" loading="lazy"></button>',
    "collar thumb")

# ── 2. hero geometry (bk-shirt is 777x855) ──────────────────────────────────
rep("aspect-ratio:778/835", "aspect-ratio:777/855", "aspect")
s = s.replace('width="778" height="835"', 'width="777" height="855"')

# ── 3. warm golden-hour sky so the blue shirt separates ─────────────────────
rep("""  --sky-0:#5FB9F5; --sky-1:#8FD2FA; --sky-2:#BFE7FE; --sky-3:#E4F5FF;""",
    """  --sky-0:#F7B27A; --sky-1:#FBD3A5; --sky-2:#FDE8CC; --sky-3:#FFF6EA;""", "sky vars")
rep("""    #4FB2F3 0%, #79C9F8 8%, #A8DEFC 17%,
    #D2EEFE 27%, #EAF7FF 34%, #D6F0FF 42%,
    #B9E4FD 52%, #E6F6FF 62%, #FFF1E4 70%,
    #FFE3D2 76%, #D8EEFE 85%, #A6DBFB 93%, #74C4F7 100%)}""",
    """    #7CC4F0 0%, #A9DAF3 8%, #CFE9F6 16%,
    #F3DFC2 26%, #FBEAD3 33%, #FDDCB4 41%,
    #F8C58F 50%, #FDE7CE 60%, #FFF4E6 68%,
    #FBD9B4 76%, #EED9F0 85%, #BFD8F5 93%, #8CC6EF 100%)}""", "sky gradient")
rep("""background:radial-gradient(circle,rgba(255,250,225,.95),rgba(255,238,195,.55) 32%,rgba(255,232,180,0) 66%);""",
    """background:radial-gradient(circle,rgba(255,244,205,.98),rgba(255,214,150,.6) 34%,rgba(255,200,130,0) 68%);""", "sun")
# clouds pick up a warm underside
rep("box-shadow:inset 0 -16px 26px -16px rgba(120,180,220,.42)}",
    "box-shadow:inset 0 -16px 26px -16px rgba(226,168,120,.44)}", "cloud underside")
rep(".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px rgba(240,170,140,.34)}",
    ".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px rgba(236,146,96,.40)}", "warm cloud")
rep("drop-shadow(0 14px 22px rgba(46,116,168,.20))}", "drop-shadow(0 14px 22px rgba(196,132,84,.20))}", "cloud shadow css")
rep("'drop-shadow(0 14px 22px rgba(46,116,168,'+(layer===2?.10:.04)+'))'+",
    "'drop-shadow(0 14px 22px rgba(196,132,84,'+(layer===2?.10:.04)+'))'+", "cloud shadow js")
rep("<meta name=\"theme-color\" content=\"#8FD2FA\">", "<meta name=\"theme-color\" content=\"#FBD3A5\">", "theme colour")

# ── 4. copy ─────────────────────────────────────────────────────────────────
rep("<title>Balloon Bicycle Embroidered Linen Shirt | Baby Bling</title>",
    "<title>Kite Dreams Embroidered Linen Shirt | Baby Bling</title>", "title")
rep('content="A soft pink linen Cuban collar shirt with a hand-embroidered bicycle carrying red and blue balloons. Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">',
    'content="A sky-blue linen Cuban collar shirt with a hand-embroidered kite trailing a looping string past two puffy clouds. Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">', "description")
rep('<meta property="og:title" content="Balloon Bicycle Embroidered Linen Shirt — Baby Bling">',
    '<meta property="og:title" content="Kite Dreams Embroidered Linen Shirt — Baby Bling">', "og")
s = s.replace("Balloon Bicycle Embroidered Linen Shirt", "Kite Dreams Embroidered Linen Shirt")
s = s.replace("Balloon Bicycle Linen Shirt", "Kite Dreams Linen Shirt")

rep("""<h1>Balloon Bicycle<span class="line2">Shirt</span></h1>""",
    """<h1>Kite Dreams<span class="line2">Shirt</span></h1>""", "h1")
rep("So light, they forget it's on.", 'So light, it flies with them.', "tagline")
rep("Breathable linen, coconut wood buttons, and a bicycle stitched on by hand.",
    "Breathable sky-blue linen, coconut wood buttons, and a kite stitched on by hand.", "hero sub")
rep('<span class="em">🧵</span> Hand embroidered', '<span class="em">🪁</span> Hand embroidered', "pill")
rep("Let them go<br>ride the balloons.", "Let them go<br>chase the wind.", "final h2")
rep("<h2>Made for exactly those days.</h2>", "<h2>Made for the windy ones.</h2>", "why h2")
rep("Embroidered by hand, in small batches", "Every kite embroidered by hand, in small batches", "urgency")

# details cards
rep("<h3>Camp collar</h3><p>Soft, open and unstructured — with our woven label and a printed size tag, so nothing scratches the neck.</p>",
    "<h3>Cloud embroidery</h3><p>Two puffy clouds in dense white satin stitch, raised off the linen so you can feel them.</p>", "card1")
rep("<h3>Hand-stitched bicycle</h3><p>Thread on thread — no plastic print to crack, peel or fade in the wash.</p>",
    "<h3>Hand-stitched kite</h3><p>Red, yellow and blue thread on thread, with a looping navy string — no plastic print to crack or peel.</p>", "card3")
rep("<h2>The bits nobody else bothers with.</h2>", "<h2>The bits nobody else bothers with.</h2>", "noop")

# "why this shirt" cards
rep("<span style=\"font-size:1.6rem\">🚲</span>", "<span style=\"font-size:1.6rem\">🪁</span>", "why icon 1")
rep("<h3 style=\"font-size:1.05rem\">Hand-embroidered, not printed</h3>\n        <p>A whimsical bicycle carrying one red and one blue balloon, stitched thread-on-thread. There is no print to crack, peel or fade in the wash.</p>",
    "<h3 style=\"font-size:1.05rem\">Hand-embroidered, not printed</h3>\n        <p>A little kite climbing past two clouds on a looping string, stitched thread-on-thread. There is no print to crack, peel or fade in the wash.</p>", "why 1")
rep("<h3 style=\"font-size:1.05rem\">Breathable linen, Cuban collar</h3>\n        <p>Soft pink linen in an open Cuban collar cut — as comfortable as it is charming, for playdates, outings, or making an ordinary day feel magical.</p>",
    "<h3 style=\"font-size:1.05rem\">Breathable linen, Cuban collar</h3>\n        <p>Soft sky-blue linen in an open Cuban collar cut — as comfortable as it is charming, for playdates, outings, or making an ordinary day feel magical.</p>", "why 2")

# fabric panel
rep("Linen that behaves<br>like it's been loved<br>for years.",
    "Linen that behaves<br>like it's been loved<br>for years.", "noop2")
rep('alt="A child holding up the Baby Bling Balloon Ride Shirt"',
    'alt="The Baby Bling Kite Dreams shirt folded on linen"', "fabric alt")

# alt text on the hero + gallery
s = s.replace('alt="Baby Bling peach linen cotton kids shirt with hand-embroidered bicycle and balloons"',
              'alt="Baby Bling sky-blue linen kids shirt with a hand-embroidered kite and clouds"')
s = s.replace('alt="The Kite Dreams Embroidered Linen Shirt in Peach Sorbet, front view"',
              'alt="The Kite Dreams shirt, front view"')
s = s.replace("Peach Sorbet", "Sky Blue")

# ── 5. decorative balloons -> little kites ──────────────────────────────────
def _kite(cls, c1, c2, c3, flip=False):
    sx = ' transform="scale(-1,1) translate(-60,0)"' if flip else ''
    return ('<svg class="bln %s" viewBox="0 0 60 110" aria-hidden="true"><g%s>'
            '<path d="M30 6 50 34 30 62 10 34Z" fill="%s"/>'
            '<path d="M30 6 50 34 30 34Z" fill="%s"/>'
            '<path d="M10 34 30 34 30 62Z" fill="%s"/>'
            '<path d="M30 6 30 62M10 34 50 34" stroke="rgba(14,47,76,.35)" stroke-width="1.4"/>'
            '<path d="M30 62c7 9-7 15-1 26" stroke="#0E2F4C" stroke-width="1.5" fill="none" '
            'stroke-linecap="round" opacity=".5"/>'
            '<path d="M26 72h8M24 84h8" stroke="#D63B31" stroke-width="2.4" stroke-linecap="round"/>'
            '</g></svg>') % (cls, sx, c1, c2, c3)

blns = re.findall(r'<svg class="bln [abc]".*?</svg>', s, re.S)
assert len(blns) == 3, "expected 3 decorative balloons, found %d" % len(blns)
for old_svg, new_svg in zip(blns, [_kite("a", "#D63B31", "#F5B942", "#2F63D8"),
                                   _kite("b", "#2F63D8", "#FFFFFF", "#D63B31", flip=True),
                                   _kite("c", "#F5B942", "#D63B31", "#2F63D8")]):
    s = s.replace(old_svg, new_svg, 1)
rep(".bln{position:absolute;width:clamp(30px,7vw,54px);",
    ".bln{position:absolute;width:clamp(26px,6vw,46px);", "kite size")

io.open("index-kite.html", "w", encoding="utf-8").write(s)
print("index-kite.html written (%d -> %d bytes)" % (n, len(s)))

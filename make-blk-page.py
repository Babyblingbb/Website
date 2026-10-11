#!/usr/bin/env python3
"""index.html (peach / Balloon Bicycle)  ->  index-blk.html (black / Rocket Launch).

Black wants the lightest sky of the set, so this page gets a pale champagne dawn:
the shirt reads almost as a silhouette against it, and the navy headline still sits
comfortably on the warm cream.
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
for old, new in {"shirt":"bl-shirt", "back":"bl-back", "d-collar":"bl-d-collar",
                 "d-buttons":"bl-d-button", "d-embroidery":"bl-d-rocket",
                 "d-patch":"bl-d-planets", "lifestyle":"bl-lifestyle",
                 "folded":"bl-clouds"}.items():
    rep("assets/%s.webp" % old, "assets-blk/%s.webp" % new, "asset " + old, count=99)

rep('<button class="bvt"     data-src="assets-blk/bl-clouds.webp"       aria-label="Folded"><img src="assets-blk/bl-clouds.webp" alt="" loading="lazy"></button>',
    '<button class="bvt"     data-src="assets-blk/bl-clouds.webp"   aria-label="In the sky"><img src="assets-blk/bl-clouds.webp" alt="" loading="lazy"></button>\n'
    '        <button class="bvt"     data-src="assets-blk/bl-folded.webp"   aria-label="Folded"><img src="assets-blk/bl-folded.webp" alt="" loading="lazy"></button>',
    "extra thumb")

# ── hero geometry (bl-shirt is 802x803) ────────────────────────────────────
rep("aspect-ratio:778/835", "aspect-ratio:802/803", "aspect")
rep('width="778" height="835"', 'width="802" height="803"', "img dims", count=99)

# ── pale champagne dawn ────────────────────────────────────────────────────
rep("  --sky-0:#5FB9F5; --sky-1:#8FD2FA; --sky-2:#BFE7FE; --sky-3:#E4F5FF;",
    "  --sky-0:#DCBE8E; --sky-1:#EED8B6; --sky-2:#F6E8D2; --sky-3:#FDF8F0;", "sky vars")
rep("""    #4FB2F3 0%, #79C9F8 8%, #A8DEFC 17%,
    #D2EEFE 27%, #EAF7FF 34%, #D6F0FF 42%,
    #B9E4FD 52%, #E6F6FF 62%, #FFF1E4 70%,
    #FFE3D2 76%, #D8EEFE 85%, #A6DBFB 93%, #74C4F7 100%)}""",
    """    #F6E8D2 0%, #F2DFC2 8%, #EED8B6 17%,
    #F5E7D2 27%, #FBF3E6 34%, #F3E2CB 42%,
    #EBD6B4 52%, #F8EEDE 62%, #FDE8D8 70%,
    #F7D9C4 76%, #F0E0C8 85%, #E6CDA4 93%, #DCBE8E 100%)}""", "sky gradient")
rep("background:radial-gradient(circle,rgba(255,250,225,.95),rgba(255,238,195,.55) 32%,rgba(255,232,180,0) 66%);",
    "background:radial-gradient(circle,rgba(255,248,226,.98),rgba(250,222,166,.6) 32%,rgba(246,210,150,0) 68%);", "sun")
rep("box-shadow:inset 0 -16px 26px -16px rgba(120,180,220,.42)}",
    "box-shadow:inset 0 -16px 26px -16px rgba(198,164,118,.44)}", "cloud underside")
rep(".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px rgba(240,170,140,.34)}",
    ".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px rgba(232,176,136,.38)}", "warm cloud")
rep("drop-shadow(0 14px 22px rgba(46,116,168,.20))}",
    "drop-shadow(0 14px 22px rgba(160,125,80,.20))}", "cloud shadow css")
rep("'drop-shadow(0 14px 22px rgba(46,116,168,'+(layer===2?.10:.04)+'))'+",
    "'drop-shadow(0 14px 22px rgba(160,125,80,'+(layer===2?.10:.04)+'))'+", "cloud shadow js")
rep('<meta name="theme-color" content="#8FD2FA">',
    '<meta name="theme-color" content="#F2DFC2">', "theme colour")
rep("h1 .line2{display:block;background:linear-gradient(100deg,#C93026 6%,#EE5A2E 42%,#2450BE 94%);",
    "h1 .line2{display:block;background:linear-gradient(100deg,#B5340C 6%,#D9701C 44%,#123A63 94%);", "h1 gradient")

# ── copy ───────────────────────────────────────────────────────────────────
rep("<title>Balloon Bicycle Embroidered Linen Shirt | Baby Bling</title>",
    "<title>Rocket Launch Embroidered Linen Shirt | Baby Bling</title>", "title")
rep('content="A soft pink linen Cuban collar shirt with a hand-embroidered bicycle carrying red and blue balloons. Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">',
    'content="A black linen Cuban collar shirt with a hand-embroidered rocket, a ringed planet and a scatter of tiny stars. Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">', "description")
rep('<meta property="og:title" content="Balloon Bicycle Embroidered Linen Shirt — Baby Bling">',
    '<meta property="og:title" content="Rocket Launch Embroidered Linen Shirt — Baby Bling">', "og")
soft("Balloon Bicycle Embroidered Linen Shirt", "Rocket Launch Embroidered Linen Shirt")
rep("Balloon Bicycle Linen Shirt", "Rocket Launch Linen Shirt", "short name", count=99)

rep("""<h1>Balloon Bicycle<span class="line2">Shirt</span></h1>""",
    """<h1>Rocket Launch<span class="line2">Shirt</span></h1>""", "h1")
rep("So light, they forget it's on.", 'So light, it might take off.', "tagline")
rep("Breathable linen, coconut wood buttons, and a bicycle stitched on by hand.",
    "Breathable black linen, coconut wood buttons, and a rocket stitched on by hand.", "hero sub")
rep('<span class="em">🧵</span> Hand embroidered', '<span class="em">🚀</span> Hand embroidered', "pill")
rep("Let them go<br>ride the balloons.", "Let them go<br>aim a bit higher.", "final h2")
rep("<h2>Made for exactly those days.</h2>", "<h2>Made for big ideas.</h2>", "why h2")
rep("Embroidered by hand, in small batches", "Every rocket embroidered by hand, in small batches", "urgency")
rep("Peach Sorbet", "Midnight Black", "colour name", count=99)

rep("<h3>Hand-stitched bicycle</h3><p>Thread on thread — no plastic print to crack, peel or fade in the wash.</p>",
    "<h3>Hand-stitched rocket</h3><p>White dashed running stitch with red-orange flames at the base — thread on thread, no plastic print to crack or peel.</p>", "card3")
rep("<h3>The Bling patch</h3><p>Our woven signature at the hem. Small, but it's how you know it's real.</p>",
    "<h3>A little solar system</h3><p>Planets, moons and tiny stars scattered toward the hem, with our woven patch tucked in among them.</p>", "card4")

rep('<span style="font-size:1.6rem">🚲</span>', '<span style="font-size:1.6rem">🚀</span>', "why icon 1")
rep("<p>A whimsical bicycle carrying one red and one blue balloon, stitched thread-on-thread. There is no print to crack, peel or fade in the wash.</p>",
    "<p>A rocket mid-launch, a ringed planet and a scatter of tiny stars, all stitched thread-on-thread. There is no print to crack, peel or fade in the wash.</p>", "why 1")
rep("<p>Soft pink linen in an open Cuban collar cut — as comfortable as it is charming, for playdates, outings, or making an ordinary day feel magical.</p>",
    "<p>Deep black linen in an open Cuban collar cut — as comfortable as it is charming, for playdates, outings, or making an ordinary day feel magical.</p>", "why 2")
rep('alt="Baby Bling peach linen cotton kids shirt with hand-embroidered bicycle and balloons"',
    'alt="Baby Bling black linen kids shirt with a hand-embroidered rocket and planets"', "hero alt")
soft('alt="A child holding up the Baby Bling Balloon Ride Shirt"',
     'alt="A child holding up the Baby Bling Rocket Launch shirt"')

# ── decorative balloons -> ringed planets ──────────────────────────────────
def _planet(cls, body, ring):
    return ('<svg class="bln %s" viewBox="0 0 70 80" aria-hidden="true">'
            '<ellipse cx="35" cy="32" rx="20" ry="20" fill="%s"/>'
            '<ellipse cx="28" cy="25" rx="6" ry="5" fill="#fff" opacity=".25"/>'
            '<ellipse cx="35" cy="34" rx="32" ry="9" fill="none" stroke="%s" stroke-width="3.5" '
            'transform="rotate(-18 35 34)"/>'
            '<path d="M35 54c6 8-6 12-1 20" stroke="#0E2F4C" stroke-width="1.5" fill="none" '
            'stroke-linecap="round" opacity=".35"/></svg>') % (cls, body, ring)

blns = re.findall(r'<svg class="bln [abc]".*?</svg>', s, re.S)
assert len(blns) == 3, "expected 3 decorative shapes, found %d" % len(blns)
for old_svg, new_svg in zip(blns, [_planet("a", "#D9701C", "#B5340C"),
                                   _planet("b", "#123A63", "#2E6FA8"),
                                   _planet("c", "#C9A227", "#8C6D12")]):
    s = s.replace(old_svg, new_svg, 1)
rep(".bln{position:absolute;width:clamp(30px,7vw,54px);",
    ".bln{position:absolute;width:clamp(26px,6vw,46px);", "planet size")

io.open("index-blk.html", "w", encoding="utf-8").write(s)
print("index-blk.html written (%d -> %d bytes)" % (n0, len(s)))

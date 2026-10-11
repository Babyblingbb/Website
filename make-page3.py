#!/usr/bin/env python3
"""One generator for Sail Away (beach), Rock Pool (beige) and Weekend Doodles (white).
  python make-page3.py beach beige white
Every substitution asserts via rep().
"""
import io, re, sys
from PIL import Image

BASE_GRAD = """    #4FB2F3 0%, #79C9F8 8%, #A8DEFC 17%,
    #D2EEFE 27%, #EAF7FF 34%, #D6F0FF 42%,
    #B9E4FD 52%, #E6F6FF 62%, #FFF1E4 70%,
    #FFE3D2 76%, #D8EEFE 85%, #A6DBFB 93%, #74C4F7 100%)}"""
CARD1 = "<h3>Camp collar</h3><p>Soft, open and unstructured — with our woven label and a printed size tag, so nothing scratches the neck.</p>"
CARD2 = "<h3>Coconut wood buttons</h3><p>Real wood, smooth-sanded edges, stitched twice over so they stay put.</p>"
CARD3 = "<h3>Hand-stitched bicycle</h3><p>Thread on thread — no plastic print to crack, peel or fade in the wash.</p>"
CARD4 = "<h3>The Bling patch</h3><p>Our woven signature at the hem. Small, but it's how you know it's real.</p>"
WHY1  = "<p>A whimsical bicycle carrying one red and one blue balloon, stitched thread-on-thread. There is no print to crack, peel or fade in the wash.</p>"
WHY2  = "<p>Soft pink linen in an open Cuban collar cut — as comfortable as it is charming, for playdates, outings, or making an ordinary day feel magical.</p>"
TAIL  = " — as comfortable as it is charming, for playdates, outings, or making an ordinary day feel magical.</p>"

def sailboat(cls, hull, sail):
    return ('<svg class="bln %s" viewBox="0 0 60 70" aria-hidden="true"><path d="M30 6v40" stroke="#0E2F4C" '
            'stroke-width="2"/><path d="M31 8 50 40H31Z" fill="%s"/><path d="M29 14 14 40h15Z" fill="#fff" '
            'opacity=".9"/><path d="M6 46h48l-7 12H13Z" fill="%s"/></svg>') % (cls, sail, hull)

def star(cls, col):
    return ('<svg class="bln %s" viewBox="0 0 56 60" aria-hidden="true"><path d="M28 4 35 22 54 24 40 37 44 56 '
            '28 46 12 56 16 37 2 24 21 22Z" fill="%s" stroke="rgba(14,47,76,.3)" stroke-width="1.6"/></svg>') % (cls, col)

CFG = {
 "beach": dict(dir="assets-beach", p="bw",
   slots={"d-collar":"d-collar","d-buttons":"d-buttons","d-embroidery":"d-waves","d-patch":"d-patch"},
   sky=("#2FA3A8","#6FC9C6","#A9E3DD","#E2F7F4"),
   grad="#BDEBE6 0%, #A9E3DD 8%, #93DAD4 17%,\n    #7FD0CA 27%, #72C9C3 34%, #65C1BB 42%,\n    #56B7B1 52%, #8ED6CF 62%, #E9F8F0 70%,\n    #FFE9D6 76%, #B8E6DF 85%, #5DB8B2 93%, #2FA3A8 100%)}",
   under="rgba(70,160,160,.42)", warm="rgba(245,190,150,.34)", shadow="30,110,115", theme="#7FD0CA",
   h1g="#1D5D8C 6%,#C9302C 44%,#0E6B6E 94%",
   name="Sail Away", tag="So light, it catches the breeze.",
   desc="A crisp white linen Cuban collar shirt with hand-embroidered blue ocean waves and a little red sailboat.",
   sub="Breathable white linen, coconut wood buttons, and a sea stitched on by hand.", emoji="⛵",
   final="Let them go<br>find the shore.", why="Made for beach days.", urg="Every wave", colour="Crisp White",
   c1=None, c2=None,
   c3="<h3>Hand-stitched waves</h3><p>Rolling blue running-stitch waves with a little red sailboat on top — no plastic print to crack or peel.</p>",
   c4=None, w1="Rolling waves and a little red sailboat", fabric="Crisp white linen",
   deco=[sailboat("a","#1D5D8C","#C9302C"), sailboat("b","#C9302C","#FFFFFF"), sailboat("c","#0E6B6E","#F5C518")]),
 "beige": dict(dir="assets-beige", p="bc",
   slots={"d-collar":"d-collar","d-buttons":"d-turtle","d-embroidery":"d-crab","d-patch":"d-shells"},
   sky=("#E0766A","#F0A095","#F8C8BF","#FDEBE6"),
   grad="#FAD7CF 0%, #F7CBC1 8%, #F4BEB3 17%,\n    #F0B0A4 27%, #ECA497 34%, #E8988B 42%,\n    #E38C7F 52%, #F2B8AD 62%, #FFF0E0 70%,\n    #FFE2C8 76%, #F4C4BA 85%, #E48A7E 93%, #D8705F 100%)}",
   under="rgba(205,120,105,.42)", warm="rgba(240,170,120,.36)", shadow="170,80,65", theme="#F0B0A4",
   h1g="#1F6B4A 6%,#B8342A 44%,#7A3B2E 94%",
   name="Rock Pool", tag="So light, the tide won't notice.",
   desc="A cream linen Cuban collar shirt scattered with hand-embroidered sea creatures — a turtle, crabs, shells and a starfish.",
   sub="Breathable cream linen, coconut wood buttons, and a rock pool stitched on by hand.", emoji="🐢",
   final="Let them go<br>turn over a stone.", why="Made for seaside days.", urg="Every crab", colour="Natural Cream",
   c1=None,
   c2="<h3>A green turtle</h3><p>Shell and flippers in dark green outline stitch, paddling across the chest.</p>",
   c3="<h3>Hand-stitched crabs</h3><p>Red outline crabs, claws up — thread on thread, no plastic print to crack or peel.</p>",
   c4="<h3>Shells &amp; a starfish</h3><p>Scallops, a spiral conch and a starfish scattered toward the hem, with our woven patch among them.</p>",
   w1="A turtle, crabs, shells and a starfish", fabric="Natural cream linen",
   deco=[star("a","#E8743B"), star("b","#D8705F"), star("c","#F2A541")]),
 "white": dict(dir="assets-white", p="bf",
   slots={"d-collar":"d-pizza","d-buttons":"d-coffee","d-embroidery":"d-stamp","d-patch":"d-fries"},
   sky=("#E9A92A","#F4C766","#F9DFA0","#FEF4DA"),
   grad="#FBE7B4 0%, #F9DFA0 8%, #F7D68C 17%,\n    #F5CD79 27%, #F3C56B 34%, #F0BC5E 42%,\n    #EDB252 52%, #F6D38A 62%, #FFF6E2 70%,\n    #FFEBC8 76%, #F6D895 85%, #EDB04A 93%, #E39E22 100%)}",
   under="rgba(200,150,60,.42)", warm="rgba(235,150,90,.36)", shadow="160,110,30", theme="#F5CD79",
   h1g="#B8342A 6%,#D96A18 44%,#2A4A7A 94%",
   name="Weekend Doodles", tag="So light, weekends feel longer.",
   desc="A cream linen Cuban collar shirt scattered with hand-embroidered doodles — pizza, coffee, headphones, fries and a heart stamp.",
   sub="Breathable cream linen, coconut wood buttons, and a weekend stitched on by hand.", emoji="🍕",
   final="Let them go<br>make a plan.", why="Made for lazy Sundays.", urg="Every doodle", colour="Natural Cream",
   c1="<h3>A slice of pizza</h3><p>Yellow crust, red toppings, stitched right on the chest.</p>",
   c2="<h3>Coffee &amp; buttons</h3><p>A steaming cup in black outline beside real coconut wood buttons.</p>",
   c3="<h3>Hand-stitched doodles</h3><p>Headphones, glasses, a flower and a heart stamp — thread on thread, no plastic print to crack or peel.</p>",
   c4="<h3>Fries on the hem</h3><p>Red-and-yellow fries tucked low on the front — the one they'll point at first.</p>",
   w1="Pizza, fries, coffee, headphones and a heart stamp", fabric="Natural cream linen",
   deco=[star("a","#F5C518"), star("b","#E8452C"), star("c","#F5C518")]),
}

def build(key):
    c = CFG[key]; d, p = c["dir"], c["p"]
    s = io.open("index.html", encoding="utf-8").read()
    def rep(a, b, why, count=1):
        nonlocal s
        assert a in s, "MISSING (%s/%s): %s" % (key, why, a[:60]); s = s.replace(a, b, count)
    amap = {"shirt":"shirt","back":"back","lifestyle":"lifestyle","folded":"extra", **c["slots"]}
    for old, new in amap.items():
        rep("assets/%s.webp" % old, "%s/%s-%s.webp" % (d, p, new), "asset " + old, 99)
    w, h = Image.open("%s/%s-shirt.webp" % (d, p)).size
    rep("aspect-ratio:778/835", "aspect-ratio:%d/%d" % (w, h), "aspect")
    rep('width="778" height="835"', 'width="%d" height="%d"' % (w, h), "dims", 99)
    rep("  --sky-0:#5FB9F5; --sky-1:#8FD2FA; --sky-2:#BFE7FE; --sky-3:#E4F5FF;",
        "  --sky-0:%s; --sky-1:%s; --sky-2:%s; --sky-3:%s;" % c["sky"], "sky vars")
    rep(BASE_GRAD, "    " + c["grad"], "gradient")
    rep("box-shadow:inset 0 -16px 26px -16px rgba(120,180,220,.42)}", "box-shadow:inset 0 -16px 26px -16px %s}" % c["under"], "under")
    rep(".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px rgba(240,170,140,.34)}",
        ".cl.warm i{background:#fff;box-shadow:inset 0 -18px 30px -16px %s}" % c["warm"], "warm")
    rep("drop-shadow(0 14px 22px rgba(46,116,168,.20))}", "drop-shadow(0 14px 22px rgba(%s,.20))}" % c["shadow"], "shadow css")
    rep("'drop-shadow(0 14px 22px rgba(46,116,168,'", "'drop-shadow(0 14px 22px rgba(%s,'" % c["shadow"], "shadow js")
    rep('<meta name="theme-color" content="#8FD2FA">', '<meta name="theme-color" content="%s">' % c["theme"], "theme")
    rep("linear-gradient(100deg,#C93026 6%,#EE5A2E 42%,#2450BE 94%)", "linear-gradient(100deg,%s)" % c["h1g"], "h1g")
    full = c["name"] + " Embroidered Linen Shirt"
    rep("Balloon Bicycle Embroidered Linen Shirt", full, "full name", 99)
    rep("Balloon Bicycle Linen Shirt", c["name"] + " Linen Shirt", "short name", 99)
    rep('content="A soft pink linen Cuban collar shirt with a hand-embroidered bicycle carrying red and blue balloons. Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">',
        'content="%s Breathable linen, coconut wood buttons, itch-free patch. By Baby Bling.">' % c["desc"], "desc")
    rep('<h1>Balloon Bicycle<span class="line2">Shirt</span></h1>', '<h1>%s<span class="line2">Shirt</span></h1>' % c["name"], "h1")
    rep("So light, they forget it's on.", c["tag"], "tag")
    rep("Breathable linen, coconut wood buttons, and a bicycle stitched on by hand.", c["sub"], "sub")
    rep('<span class="em">🧵</span> Hand embroidered', '<span class="em">%s</span> Hand embroidered' % c["emoji"], "pill")
    rep("Let them go<br>ride the balloons.", c["final"], "final")
    rep("<h2>Made for exactly those days.</h2>", "<h2>%s</h2>" % c["why"], "why")
    rep("Embroidered by hand, in small batches", c["urg"] + " embroidered by hand, in small batches", "urg")
    rep("Peach Sorbet", c["colour"], "colour", 99)
    for old, k in [(CARD1,"c1"),(CARD2,"c2"),(CARD3,"c3"),(CARD4,"c4")]:
        if c[k]: rep(old, c[k], k)
    rep('<span style="font-size:1.6rem">🚲</span>', '<span style="font-size:1.6rem">%s</span>' % c["emoji"], "why icon")
    rep(WHY1, "<p>%s, all stitched thread-on-thread. There is no print to crack, peel or fade in the wash.</p>" % c["w1"], "why1")
    rep(WHY2, "<p>%s in an open Cuban collar cut%s" % (c["fabric"], TAIL), "why2")
    rep('alt="Baby Bling peach linen cotton kids shirt with hand-embroidered bicycle and balloons"',
        'alt="Baby Bling %s shirt"' % c["name"], "alt")
    s = s.replace('alt="A child holding up the Baby Bling Balloon Ride Shirt"', 'alt="Baby Bling %s shirt"' % c["name"])
    blns = re.findall(r'<svg class="bln [abc]".*?</svg>', s, re.S); assert len(blns) == 3
    for o, n in zip(blns, c["deco"]): s = s.replace(o, n, 1)
    rep(".bln{position:absolute;width:clamp(30px,7vw,54px);", ".bln{position:absolute;width:clamp(24px,5.5vw,42px);", "deco")
    io.open("index-%s.html" % key, "w", encoding="utf-8").write(s)
    print("index-%s.html  hero %dx%d" % (key, w, h))

for k in sys.argv[1:] or list(CFG):
    build(k)

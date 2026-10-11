"""Post-build patch for every custom template (run after any build):  python patch-layout.py [files...]
- stays {% layout none %} but loads content_for_header + Shiprocket Fastrr snippet
- checkout -> Fastrr buyCart, native /checkout fallback
- internal links: logo, nav, footer, legal row"""
import io, glob, re, sys
GO = ("function goCheckout(e){ if(window.shiprocketCheckoutEvents&&shiprocketCheckoutEvents.buyCart){ try{ shiprocketCheckoutEvents.buyCart(e||null); return; }catch(err){} } "
      "location.href='/checkout'; }")
FOOT = ('<div><h4>Shop</h4><ul><li><a href="/collections/shirts">All shirts</a></li><li><a href="/#shop">Bestsellers</a></li>'
        '<li><a href="/pages/size-guide">Size guide</a></li><li><a href="/#fabric">The fabric</a></li></ul></div>\n'
        '      <div><h4>Help</h4><ul><li><a href="/pages/shipping">Shipping</a></li><li><a href="/policies/refund-policy">Returns &amp; exchanges</a></li>'
        '<li><a href="/pages/track-order">Track order</a></li><li><a href="/pages/contact">Contact us</a></li></ul></div>\n'
        '      <div><h4>Baby Bling</h4><ul><li><a href="/pages/about">Our story</a></li><li><a href="/#made">How it&#39;s made</a></li>'
        '<li><a href="https://www.instagram.com/thebabybling/" target="_blank" rel="noopener">Instagram @thebabybling</a></li><li><a href="mailto:thebabyblingco@gmail.com">thebabyblingco@gmail.com</a></li></ul></div>')
LEGAL = ('<span><a href="/policies/privacy-policy">Privacy</a> · <a href="/policies/terms-of-service">Terms</a> · '
         '<a href="/policies/refund-policy">Refunds</a></span>')
HOMENAV = ('<nav class="nav-links"><a href="/collections/shirts">Shop</a><a href="/#fabric">The Fabric</a>'
           '<a href="/#made">How it&#39;s made</a><a href="/pages/size-guide">Size guide</a><a href="/#faq">FAQ</a></nav>')
FOOT_RE = re.compile(r'<div><h4>Shop</h4>.*?</div>\n\s*<div><h4>Help</h4>.*?</div>\n\s*<div><h4>(?:Say hi|Baby Bling)</h4>.*?</div>', re.S)

def links(s, fname):
    s = s.replace('href="#" class="logo"', 'href="/" class="logo"')
    s = FOOT_RE.sub(lambda m: FOOT, s)
    s = s.replace('<span>Privacy · Terms · Refunds</span>', LEGAL)
    if "/product." in fname:
        s = s.replace('<nav class="nav-links">\n      <a href="#fabric">',
                      '<nav class="nav-links">\n      <a href="/collections/shirts">All shirts</a><a href="#fabric">', 1)
    elif "/index." not in fname:
        s = re.sub(r'<nav class="nav-links">.*?</nav>', lambda m: HOMENAV, s, count=1, flags=re.S)
        s = s.replace('href="#faq"', 'href="/#faq"').replace('href="#buy"', 'href="/collections/shirts"')
    return s

TRUST = '<style id="bb-trust">' + io.open('bbstyle.css', encoding='utf-8').read() + '</style>'
PBEN = ('\n      <div class="p-ben"><span><i>🌿</i>Itch-free</span><span><i>💧</i>Anti-sweat</span>'
        '<span><i>👶</i>Baby-skin safe</span><span><i>🪶</i>Featherlight</span></div>')
LAB_PAGES = ['product']   # all product pages (approved on Sail Away)
LAB = '<style id="bb-lab">' + io.open('bbstyle-lab.css', encoding='utf-8').read() + '</style>'

from menu import menu_patch
from sizechart import sc_patch
from coupons import cp_patch

def patch(s, fname=""):
    s = menu_patch(s)
    s = sc_patch(s)
    s = cp_patch(s, fname)
    s = s.replace('<div class="em">🇮🇳</div>', '<div class="em">🧵</div>').replace('<div class="em">↩︎</div>', '<div class="em">🔄</div>')
    s = re.sub(r'<style id="bb-(?:trust|lab)">.*?</style>\n', '', s, flags=re.S)
    s = s.replace("</head>", TRUST + "\n</head>", 1)
    lab = any(fname.startswith("/" + p + ".") for p in LAB_PAGES)
    if lab: s = s.replace("</head>", LAB + "\n</head>", 1)
    s = re.sub(r'\n\s*<div class="p-ben">.*?</div>', '', s)
    if lab: s = re.sub(r'(<p class="tax-note">.*?</p>)', lambda m: m.group(1) + PBEN, s, count=1)
    s = s.replace("{% layout 'bb' %}", "{% layout none %}", 1)
    if "content_for_header" not in s: s = s.replace("</head>", "{{ content_for_header }}\n</head>", 1)
    if "'sr-checkout'" not in s: s = s.replace("</body>", "{% render 'sr-checkout' %}\n</body>", 1)
    if "function goCheckout" in s: s = re.sub(r"function goCheckout\(\w*\)\{.*?\}\s*\}?\n", lambda m: GO + "\n", s)
    s = re.sub(r'<form action="/cart" method="post" id="bbCoForm".*?</form>\n', "", s)
    return links(s, fname)

for f in sys.argv[1:] or glob.glob("shopify/templates/*.liquid"):
    s = io.open(f, encoding="utf-8").read()
    io.open(f, "w", encoding="utf-8").write(patch(s, "/" + f.replace("\\", "/").split("/")[-1]))

"""Homepage: index-peach.html shell + shop grid -> shopify/templates/index.liquid (+ bh-*.webp staged)."""
import io, re, os
from PIL import Image
P = io.open("index-peach.html", encoding="utf-8").read()
S = io.open("index-shop.html", encoding="utf-8").read()
def cut(s, a, b): m = re.search(re.escape(a) + r".*?(?=" + re.escape(b) + ")", s, re.S); assert m, a; return m.group(0)

style = re.search(r"<style>(.*?)</style>", P, re.S).group(1)
gridcss = cut(S, "/* ══════════════════════════ SHOP GRID", "</style>")
ticker = cut(P, "<!-- ══════════════ TICKER", "<!-- ══════════════ NAV")
strip  = cut(P, "<!-- ══════════════ MARQUEE", "<!-- ══════════════ STATS")
stats  = cut(P, "<!-- ══════════════ STATS", "<!-- ══════════════ FABRIC: FEATHER")
fabric = cut(P, "<!-- ══════════════ FABRIC: FEATHER", "<!-- ══════════════ DETAILS")
faq    = cut(P, "<!-- ══════════════ FAQ", "<!-- ══════════════ FINAL CTA")
trust  = re.search(r'<div class="trust".*?\n    </div>\n', P, re.S).group(0)
footer = cut(P, "<!-- ══════════════ FOOTER", "<!-- ══════════════ STICKY")
js = lambda a, b: cut(P, a, b)
JS = (js("/* ═══════════ FULL-PAGE CLOUD FIELD", "/* ═══════════ 3D shirt tilt")
    + js("/* ═══════════ origin swipe dots", "/* ═══════════ product ═══"))

fabric = fabric.replace('<section class="feather-sec">', '<section class="feather-sec" id="fabric">')
footer = (footer.replace('<li><a href="#buy">Balloon Bicycle Linen Shirt</a></li><li><a href="#">New arrivals</a></li><li><a href="#">Gift sets</a></li>',
                         '<li><a href="/collections/shirts">All shirts</a></li><li><a href="/products/peach-linen-shirt">Balloon Bicycle</a></li><li><a href="/products/blue-linen-shirt">Kite Dreams</a></li>')
          .replace('href="#" class="logo"', 'href="/" class="logo"'))

ROWS = [("peach-linen-shirt","g-bb","#D63B31","Balloon Bicycle"),("blue-linen-shirt","g-bk","#2F63D8","Kite Dreams"),
        ("baby-pink-linen-shirt","g-bp","#D94A72","Hearts"),("dino-linen-shirt","g-bd","#1F7A78","Dino Adventure"),
        ("storytelling-linen-shirt","g-bs","#8E2740","Storytelling"),("shinchan-linen-shirt","g-bn","#CE2222","Shinchan"),
        ("black-linen-shirt","g-bl","#B5340C","Rocket Launch"),("beach-linen-shirt","g-bw","#1D5D8C","Sail Away")]
spec = ",".join("|".join(r) for r in ROWS)
grid = ("<div class=\"grid\">\n      {%- assign rows = '" + spec + "' | split: ',' -%}\n"
 "      {%- for row in rows -%}{%- assign f = row | split: '|' -%}{%- assign p = all_products[f[0]] -%}{%- if p.title != blank -%}\n"
 "        <a class=\"sh rev\" href=\"{{ p.url }}\"><span class=\"sh-stage\"><img src=\"{{ f[1] | append: '.webp' | asset_url }}\" alt=\"{{ f[3] | escape }} shirt\" loading=\"lazy\" decoding=\"async\"><span class=\"gr\"></span></span>"
 "<span class=\"sh-name\" style=\"color:{{ f[2] }}\">{{ f[3] }}</span><span class=\"sh-price\">{{ p.price | money_without_trailing_zeros }}</span></a>\n"
 "      {%- endif -%}{%- endfor -%}\n    </div>")

STEPS = [("p1","01","Pulled from the field","Flax is harvested by hand and retted slowly, so the long fibres stay fine and strong."),
         ("p2","02","Spun thin","Linen and cotton are spun together into a fine yarn — cool like linen, soft like cotton."),
         ("p3","03","Woven light","Loomed into a 120 GSM open weave that lets the breeze straight through."),
         ("p4","04","Finished by hand","Every motif is embroidered thread by thread, then pre-washed before it's cut.")]
steps = "\n".join(f'''      <div class="mk rev d{i+1}"><div class="mk-img"><img src="assets-home/{k}.webp" width="1000" height="1250" loading="lazy" alt="{t}"><b>{n}</b></div>
        <h3>{t}</h3><p>{d}</p></div>''' for i, (k, n, t, d) in enumerate(STEPS))

CSS = """
/* ══════════════════════════ HOME ══════════════════════════ */
.h-hero{overflow-x:clip;padding:clamp(6px,2vw,30px) 0 clamp(20px,4vw,60px)}
.h-in{display:grid;align-items:center;gap:clamp(6px,2vw,40px)}
@media(min-width:960px){.h-in{grid-template-columns:.9fr 1.1fr}}
.h-copy{text-align:center}
@media(min-width:960px){.h-copy{text-align:left}}
.h-copy h1{font-size:clamp(2.6rem,9.5vw,5rem);letter-spacing:-.04em;line-height:.98;text-shadow:0 2px 30px rgba(255,255,255,.9)}
.h-copy h1 em{font-style:normal;background:linear-gradient(90deg,#FF7A59,#F0508A 50%,#3D7BF0);-webkit-background-clip:text;background-clip:text;color:transparent}
.h-copy .sub{margin:16px auto 0;color:var(--ink-2);font-size:clamp(1rem,2.6vw,1.18rem);max-width:34ch}
@media(min-width:960px){.h-copy .sub{margin-left:0}}
.h-cta{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px;justify-content:center}
@media(min-width:960px){.h-cta{justify-content:flex-start}}
.h-ben{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:22px auto 0;max-width:440px}
.h-ben span{display:flex;flex-direction:column;align-items:center;gap:6px;font-size:.8rem;font-weight:600;color:var(--ink);line-height:1.2;text-align:center}
.h-ben i{font-style:normal;font-size:2.3rem;line-height:1;display:block;
  filter:drop-shadow(0 8px 10px rgba(20,70,110,.18));animation:hBob 3.2s ease-in-out infinite}
.h-ben span:nth-child(2) i{animation-delay:-.8s}.h-ben span:nth-child(3) i{animation-delay:-1.6s}.h-ben span:nth-child(4) i{animation-delay:-2.4s}
@keyframes hBob{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-6px) rotate(-6deg)}}
@media(prefers-reduced-motion:reduce){.h-ben i{animation:none}}
.h-ben span{font-size:.86rem!important}
@media(min-width:960px){.h-ben{margin-left:0}}
.h-rate{margin-top:16px;font-size:.88rem;color:var(--ink-2);font-weight:500}
.trio{position:relative;aspect-ratio:1.25/1;width:100%;max-width:760px;margin-inline:auto}
.trio a{position:absolute;display:block}
.trio img{width:100%;height:auto;display:block;animation:floaty 7s ease-in-out infinite;
  filter:drop-shadow(0 30px 26px rgba(20,70,110,.26)) drop-shadow(0 8px 10px rgba(20,70,110,.10))}
.trio .t1{width:50%;left:-2%;top:16%;rotate:-9deg;z-index:1}
.trio .t2{width:60%;left:20%;top:0;z-index:3}
.trio .t3{width:50%;right:-2%;top:16%;rotate:9deg;z-index:2}
.trio .t1 img{animation-delay:-2.2s}.trio .t3 img{animation-delay:-4.4s}
.trio .gr{position:absolute;left:50%;bottom:0;width:70%;height:26px;translate:-50% 0;border-radius:50%;
  background:radial-gradient(ellipse,rgba(20,70,110,.24),rgba(20,70,110,0) 70%);filter:blur(9px);animation:shadowPulse 7s ease-in-out infinite}
@media(max-width:959px){.trio{order:0;margin-top:22px}.h-copy{order:1;margin-top:-6px}.h-foot{order:2}}
.h-foot{text-align:center}
@media(min-width:960px){.h-foot{display:none}}
@media(max-width:959px){.h-copy .h-cta,.h-copy .h-ben{display:none}}
.see-all{display:flex;justify-content:center;margin-top:clamp(26px,4vw,44px)}
.made{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(12px,1.6vw,22px)}
.mk-img{position:relative;border-radius:var(--r-m,24px);overflow:hidden;aspect-ratio:4/5;box-shadow:var(--shadow-m)}
.mk-img img{width:100%;height:100%;object-fit:cover;transition:transform .8s cubic-bezier(.22,1,.36,1)}
@media(hover:hover){.mk:hover .mk-img img{transform:scale(1.06)}}
.mk-img b{position:absolute;left:14px;top:12px;font-family:'Fredoka';font-size:1rem;background:rgba(255,255,255,.85);
  backdrop-filter:blur(6px);padding:4px 11px;border-radius:999px;color:var(--ink)}
.mk h3{margin-top:14px;font-size:1.12rem}
.mk p{margin-top:6px;color:var(--ink-2);font-size:.95rem}
@media(max-width:860px){
  .made{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:12px;margin-inline:calc(-1 * var(--pad));
    padding-inline:var(--pad);scrollbar-width:none}
  .made::-webkit-scrollbar{display:none}
  .mk{flex:0 0 74%;scroll-snap-align:center}
}
"""

page = f"""{{% layout none %}}<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Baby Bling | Featherlight linen shirts for kids</title>
<meta name="description" content="Featherlight linen-cotton shirts for kids — hand-embroidered, coconut wood buttons, pre-washed soft. Free shipping over ₹999, cash on delivery.">
<meta name="theme-color" content="#8FD2FA">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎈</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
{{{{ content_for_header }}}}
<style>
{style}
{gridcss}
{CSS}
</style>
</head>
<body>
<div id="skybg" aria-hidden="true"><div id="grad"></div><div id="sun"></div><div id="cloudfield"></div></div>
{ticker}<header id="nav">
  <div class="wrap nav-in">
    <a href="/" class="logo"><span class="dot"></span><b>Baby&nbsp;Bling</b></a>
    <nav class="nav-links"><a href="/collections/shirts">Shop</a><a href="#fabric">The Fabric</a><a href="#made">How it's made</a><a href="#faq">FAQ</a></nav>
    <div class="nav-cta">
      <a href="/collections/shirts" class="btn btn-dark" style="padding:11px 20px;font-size:.88rem">Shop now</a>
      <a class="cart-btn" href="/cart" aria-label="Cart">
        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
        <i class="cnt{{% if cart.item_count > 0 %}} on{{% endif %}}" id="cartCount">{{{{ cart.item_count }}}}</i>
      </a>
    </div>
  </div>
</header>

<section class="h-hero">
  <div class="wrap h-in">
    <div class="h-copy">
      <p class="eyebrow">Featherlight linen for kids</p>
      <h1 style="margin-top:10px">So light,<br>they <em>forget</em><br>it's on.</h1>
      <p class="sub">Linen-cotton shirts, hand-embroidered and pre-washed soft — for kids who never sit still.</p>
      <div class="h-cta"><a href="/collections/shirts" class="btn btn-primary">Shop all shirts</a><a href="#fabric" class="btn btn-ghost">Feel the fabric</a></div>
      <div class="h-ben"><span><i>🌿</i>Itch-free</span><span><i>💧</i>Anti-sweat</span><span><i>👶</i>Baby-skin safe</span><span><i>🪶</i>Featherlight</span></div>
    </div>
    <div class="trio">
      <a class="t1" href="/products/peach-linen-shirt" aria-label="Balloon Bicycle shirt"><img src="{{{{ 'g-bb.webp' | asset_url }}}}" alt="Balloon Bicycle linen shirt" fetchpriority="high"></a>
      <a class="t2" href="/products/blue-linen-shirt" aria-label="Kite Dreams shirt"><img src="{{{{ 'g-bk.webp' | asset_url }}}}" alt="Kite Dreams linen shirt" fetchpriority="high"></a>
      <a class="t3" href="/products/baby-pink-linen-shirt" aria-label="Hearts shirt"><img src="{{{{ 'g-bp.webp' | asset_url }}}}" alt="Hearts linen shirt" fetchpriority="high"></a>
      <span class="gr"></span>
    </div>
    <div class="h-foot">
      <div class="h-cta"><a href="/collections/shirts" class="btn btn-primary">Shop all shirts</a><a href="#fabric" class="btn btn-ghost">Feel the fabric</a></div>
      <div class="h-ben"><span><i>🌿</i>Itch-free</span><span><i>💧</i>Anti-sweat</span><span><i>👶</i>Baby-skin safe</span><span><i>🪶</i>Featherlight</span></div>
    </div>
  </div>
</section>

{strip}
<section class="sec" id="shop">
  <div class="wrap">
    <div class="sec-head rev"><p class="eyebrow">Bestsellers</p><h2>Pick their favourite.</h2>
      <p>Every shirt is hand-embroidered, with coconut wood buttons and a soft Cuban collar.</p></div>
    {grid}
    <div class="see-all"><a href="/collections/shirts" class="btn btn-dark">See all shirts →</a></div>
  </div>
</section>

{fabric}
<section class="sec" id="made">
  <div class="wrap">
    <div class="sec-head rev"><p class="eyebrow">How it's made</p><h2>From field to shirt.</h2>
      <p>Slow, careful and mostly by hand — that's why it feels the way it does.</p></div>
    <div class="made">
{steps}
    </div>
  </div>
</section>

{stats}
<section class="sec" style="padding-top:0"><div class="wrap">
    {trust}</div></section>

{faq}
<section class="final">
  <div class="wrap rev">
    <p class="eyebrow">One shirt. Every summer memory.</p>
    <h2 style="margin-top:14px">Let them go<br>chase the clouds.</h2>
    <p>Free shipping over ₹999 · cash on delivery · 7-day returns.</p>
    <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:26px">
      <a href="/collections/shirts" class="btn btn-primary">Shop all shirts</a>
    </div>
  </div>
</section>

{footer}
<script>
(function(){{
'use strict';
var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
{JS}
}})();
</script>
</body>
</html>
"""
# asset paths -> asset_url, stage home images
os.makedirs("shopify/assets", exist_ok=True)
for k, w in [("hero", 1920), ("p1", 1000), ("p2", 1000), ("p3", 1000), ("p4", 1000)]:
    im = Image.open(f"assets-home/{k}.png").convert("RGB"); im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(f"assets-home/{k}.webp", "WEBP", quality=84, method=6)
    im.save(f"shopify/assets/bh-{k}.webp", "WEBP", quality=84, method=6)
page = re.sub(r"assets-home/([\w-]+)\.webp", r"{{ 'bh-\1.webp' | asset_url }}", page)
page = re.sub(r"assets/([\w-]+)\.webp", r"{{ 'bb-\1.webp' | asset_url }}", page)
page = page.replace("url('assets/shirt.webp')", "url({{ 'bb-shirt.webp' | asset_url }})")
assert "assets/" not in page.replace("/assets/", ""), re.findall(r".{30}assets/.{30}", page)[:3]
io.open("shopify/templates/index.liquid", "w", encoding="utf-8").write(page)
print("index.liquid", len(page))

import subprocess as _sp; _sp.run(["python","patch-layout.py"])

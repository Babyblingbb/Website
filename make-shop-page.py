#!/usr/bin/env python3
"""Build the all-products page (index-shop.html) from index.html's shell.

Reuses the product page's tokens, sky, ticker, nav and footer verbatim, then
drops in a grid of floating cut-out shirts — no cards, no boxes, no plinths.
Two per row on phones, three on tablets, four on desktop.
"""
import io, re

src = io.open("index.html", encoding="utf-8").read()

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
js    = re.search(r"<script>\n(?:window\.__BB__.*?\n\};\n)?\(function\(\)\{(.*?)\n\}\)\(\);\n</script>", src, re.S).group(1)

def seg(start, end):
    m = re.search(re.escape(start) + r"(.*?)" + re.escape(end), js, re.S)
    assert m, "missing JS segment: " + start
    return start + m.group(1)

clouds = seg("/* ═══════════ FULL-PAGE CLOUD FIELD ═══════════ */",
             "/* ═══════════ 3D shirt tilt ═══════════ */")
reveal = seg("/* ═══════════ reveal ═══════════ */",
             "/* ═══════════ FAQ ═══════════ */")

# the eight shirts: handle, cut-out asset, display name, accent for the name
SHIRTS = [
 ("peach-linen-shirt",        "assets-grid/g-bb.webp", "Balloon Bicycle", "#D63B31"),
 ("blue-linen-shirt",         "assets-grid/g-bk.webp", "Kite Dreams",     "#2F63D8"),
 ("storytelling-linen-shirt", "assets-grid/g-bs.webp", "Storytelling",    "#8E2740"),
 ("baby-pink-linen-shirt",    "assets-grid/g-bp.webp", "Hearts",          "#D94A72"),
 ("dino-linen-shirt",         "assets-grid/g-bd.webp", "Dino Adventure",  "#1F7A78"),
 ("shinchan-linen-shirt",     "assets-grid/g-bn.webp", "Shinchan",        "#CE2222"),
 ("black-linen-shirt",        "assets-grid/g-bl.webp", "Rocket Launch",   "#B5340C"),
 ("sea-green-linen-shirt",    "assets-grid/g-bg.webp", "Little Gardener", "#1F5138"),
 ("beach-linen-shirt",        "assets-grid/g-bw.webp", "Sail Away",       "#1D5D8C"),
 ("beige-linen-shirt",        "assets-grid/g-bc.webp", "Rock Pool",       "#B8342A"),
 ("white-logo-linen-shirt",   "assets-grid/g-bf.webp", "Weekend Doodles", "#D96A18"),
]

GRID_CSS = """
/* ══════════════════════════ SHOP GRID ══════════════════════════ */
.shop-head{text-align:center;max-width:640px;margin:0 auto clamp(26px,5vw,52px)}
.shop-head h1{font-size:clamp(2.1rem,7vw,3.6rem);letter-spacing:-.03em;
  text-shadow:0 2px 26px rgba(255,255,255,.85)}
.shop-head p{margin-top:12px;color:var(--ink-2);font-size:1.02rem}

.grid{display:grid;grid-template-columns:repeat(2,1fr);
  column-gap:clamp(6px,2vw,28px);row-gap:clamp(22px,4vw,52px)}
@media(max-width:679px){.grid{margin-inline:calc(-1 * var(--pad) + 4px);column-gap:2px}}
@media(min-width:680px){.grid{grid-template-columns:repeat(3,1fr)}}
@media(min-width:1000px){.grid{grid-template-columns:repeat(4,1fr)}}

.sh{display:flex;flex-direction:column;align-items:center;text-align:center;
  padding:4px 2px 0;border-radius:var(--r-m);
  transition:transform .35s cubic-bezier(.22,1,.36,1)}
.sh:active{transform:scale(.97)}
@media(hover:hover){.sh:hover{transform:translateY(-8px)}}

.sh-stage{position:relative;width:100%;aspect-ratio:10/11;display:grid;place-items:center}
.sh-stage img{width:100%;height:100%;object-fit:contain;position:relative;z-index:2;
  animation:floaty 7s ease-in-out infinite;
  filter:drop-shadow(0 26px 22px rgba(20,70,110,.24)) drop-shadow(0 6px 8px rgba(20,70,110,.10));
  transition:filter .35s}
@media(hover:hover){.sh:hover .sh-stage img{
  filter:drop-shadow(0 38px 30px rgba(20,70,110,.30)) drop-shadow(0 8px 10px rgba(20,70,110,.12))}}
.sh-stage .gr{position:absolute;left:50%;bottom:4%;width:52%;height:18px;translate:-50% 0;
  border-radius:50%;background:radial-gradient(ellipse,rgba(20,70,110,.26),rgba(20,70,110,0) 70%);
  filter:blur(7px);animation:shadowPulse 7s ease-in-out infinite}

.sh-name{margin-top:6px;font-family:'Fredoka';font-weight:600;line-height:1.15;
  font-size:clamp(.95rem,2.9vw,1.14rem);letter-spacing:-.01em}
.sh-price{margin-top:3px;font-size:clamp(.82rem,2.4vw,.95rem);color:var(--ink-2);font-weight:500}
.sh-price s{opacity:.55;margin-left:6px;font-weight:400}

/* stagger the float so the grid never pulses in unison */
.sh:nth-child(8n+2) .sh-stage img{animation-delay:-1.1s}
.sh:nth-child(8n+3) .sh-stage img{animation-delay:-2.3s}
.sh:nth-child(8n+4) .sh-stage img{animation-delay:-3.4s}
.sh:nth-child(8n+5) .sh-stage img{animation-delay:-4.2s}
.sh:nth-child(8n+6) .sh-stage img{animation-delay:-5.1s}
.sh:nth-child(8n+7) .sh-stage img{animation-delay:-2.8s}
.sh:nth-child(8n+8) .sh-stage img{animation-delay:-3.9s}
.sh:nth-child(2n) .sh-stage .gr{animation-delay:-2s}
.sh:nth-child(3n) .sh-stage .gr{animation-delay:-4s}
"""

def card(handle, asset, name, accent, i=0):
    # only eight images and they are the whole page, so the first row loads eagerly
    load = 'fetchpriority="high"' if i < 4 else 'loading="lazy"'
    return f"""        <a class="sh rev" href="/products/{handle}">
          <span class="sh-stage"><img src="{asset}" alt="{name} shirt" {load} decoding="async"><span class="gr"></span></span>
          <span class="sh-name" style="color:{accent}">{name}</span>
          <span class="sh-price">₹1,699</span>
        </a>"""

cards = "\n".join(card(*x, i=i) for i, x in enumerate(SHIRTS))

ticker = re.search(r'<!-- ══════════════ TICKER ══════════════ -->.*?</div>\n\n', src, re.S).group(0)
nav    = re.search(r'<!-- ══════════════ NAV ══════════════ -->.*?</header>\n', src, re.S).group(0)
footer = re.search(r'<!-- ══════════════ FOOTER ══════════════ -->.*?</footer>\n', src, re.S).group(0)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>All Shirts | Baby Bling</title>
<meta name="description" content="Every Baby Bling shirt — featherlight linen, hand-embroidered, coconut wood buttons. Free shipping over ₹999.">
<meta name="theme-color" content="#8FD2FA">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎈</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
{style}
{GRID_CSS}
</style>
</head>
<body>

<div id="skybg" aria-hidden="true">
  <div id="grad"></div>
  <div id="sun"></div>
  <div id="cloudfield"></div>
</div>

{ticker}{nav}
<section class="sec" style="padding-top:clamp(24px,4vw,56px)">
  <div class="wrap">
    <div class="shop-head rev">
      <h1>All the shirts.</h1>
      <p>Featherlight linen, hand-embroidered, coconut wood buttons. Every one of them.</p>
    </div>
    <div class="grid">
{cards}
    </div>
  </div>
</section>

{footer}
<script>
(function(){{
'use strict';
var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

{clouds}
{reveal}
/* ═══════════ nav ═══════════ */
var nav=document.getElementById('nav');
addEventListener('scroll',function(){{ nav.classList.toggle('stuck', scrollY>16); }},{{passive:true}});

/* cart icon -> Shopify cart, with live count */
var cb=document.getElementById('openCart');
if(cb){{ cb.addEventListener('click',function(){{ location.href='/cart'; }});
  fetch('/cart.js').then(function(r){{return r.json();}}).then(function(c){{ var n=document.getElementById('cartCount');
    if(n&&c.item_count){{ n.textContent=c.item_count; n.classList.add('on'); }} }}).catch(function(){{}}); }}
document.getElementById('yr').textContent=new Date().getFullYear();
}})();
</script>
</body>
</html>
"""

io.open("index-shop.html", "w", encoding="utf-8").write(page)
print("index-shop.html written (%d bytes, %d shirts)" % (len(page), len(SHIRTS)))

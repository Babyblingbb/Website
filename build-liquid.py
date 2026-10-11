#!/usr/bin/env python3
"""index.html -> Shopify product template (templates/product.balloon-shirt.liquid).
Re-runnable: edit index.html, run this, then upload.py."""
import io, re, os, shutil, glob, sys

# build-liquid.py [src.html] [template-name] [asset-dir] [prefix]
SRC       = sys.argv[1] if len(sys.argv) > 1 else "index.html"
TPL_NAME  = sys.argv[2] if len(sys.argv) > 2 else "balloon-shirt"
ASSET_DIR = sys.argv[3] if len(sys.argv) > 3 else "assets"
PREFIX    = sys.argv[4] if len(sys.argv) > 4 else "bb-"
OUT = "shopify/templates/product.%s.liquid" % TPL_NAME
os.makedirs("shopify/templates", exist_ok=True)
os.makedirs("shopify/assets", exist_ok=True)

s = io.open(SRC, encoding="utf-8").read()

def rep(a, b, why):
    global s
    assert a in s, "MISSING (" + why + "): " + a[:70]
    s = s.replace(a, b, 1)

# 1 ── assets -> Liquid asset_url, and stage a copy for upload
pat = re.escape(ASSET_DIR) + r"/([a-z0-9\-]+)\.webp"
for n in sorted(set(re.findall(pat, s))):
    s = s.replace("%s/%s.webp" % (ASSET_DIR, n), "{{ '%s%s.webp' | asset_url }}" % (PREFIX, n))
    shutil.copy("%s/%s.webp" % (ASSET_DIR, n), "shopify/assets/%s%s.webp" % (PREFIX, n))

# 2 ── standalone layout, product context
s = ("{% layout none %}\n"
     "{%- assign p = product -%}\n"
     "{%- assign v = product.selected_or_first_available_variant | default: product.variants.first -%}\n"
     + s)

# 3 ── live product payload
rep("<script>\n(function(){\n'use strict';", """<script>
window.__BB__ = {
  handle:    {{ p.handle | json }},
  title:     {{ p.title | json }},
  variantId: {{ v.id | default: 0 | json }},
  price:     {{ v.price | default: 0 | json }},
  available: {{ v.available | default: false | json }},
  optionNames: {{ p.options | json }},
  variants: [
    {%- for var in p.variants -%}
    { id: {{ var.id }}, title: {{ var.title | json }}, price: {{ var.price }},
      available: {{ var.available | json }}, options: {{ var.options | json }} }{%- unless forloop.last -%},{%- endunless -%}
    {%- endfor -%}
  ]
};
(function(){
'use strict';""", "payload")

# 4 ── price from Shopify (fallback only while the product is unpriced)
rep("var PRICE=1699, FREE_AT=999;", """var BB = window.__BB__ || {};
var FALLBACK_PRICE = 1699;                 /* used only if Shopify price is 0 */
var PRICE = (BB.price || 0)/100;
if (PRICE <= 0) PRICE = FALLBACK_PRICE;
var FREE_AT = 999;
function inrRaw(n){ return '\\u20b9'+Number(n).toLocaleString('en-IN'); }
document.querySelectorAll('.price').forEach(function(el){
  el.textContent = PRICE > 0 ? inrRaw(PRICE) : 'Price coming soon'; });""", "price")

# 5 ── Shopify AJAX cart instead of permalinks
old = re.search(r"/\* ── Checkout.*?\nfunction goCheckout\(\)\{.*?\n\}\n", s, re.S)
if not old:
    old = re.search(r"var SHOP_DOMAIN.*?\nfunction goCheckout\(\)\{.*?\n\}\n", s, re.S)
assert old, "MISSING: checkout block"
s = s.replace(old.group(0), """/* ── Shopify AJAX cart: real line items, real checkout ── */
function shopAdd(size, qty){
  return fetch('/cart/add.js',{
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ items:[{ id: (state.variantId || BB.variantId), quantity: qty,
      properties: (state.variantId ? {} : (size ? { 'Size': size } : {})) }] })
  }).then(function(r){ return r.ok ? r.json() : r.json().then(function(e){ throw e; }); });
}
function shopCart(){ return fetch('/cart.js').then(function(r){ return r.json(); }); }
function goCheckout(){ location.href = '/checkout'; }
""")

# 6 ── state + variant-driven size picker
m = re.search(r"var state=\{size:null,qty:1,colour:'([^']*)',items:\[\]\};", s)
assert m, "MISSING: state line"
s = s.replace(m.group(0),
    "var state={size:null,qty:1,colour:'%s',variantId:0,sizeIndex:-1};" % m.group(1), 1)

rep("var sizesEl=document.getElementById('sizes');",
    """var sizesEl=document.getElementById('sizes');
/* Real Size option in Shopify? Build the picker from the actual variants. */
(function(){
  var names=(BB.optionNames||[]).map(function(o){return (o.name||o).toString().toLowerCase();});
  var ix=names.indexOf('size');
  if(ix<0 || !(BB.variants||[]).length || BB.variants.length<2) return;
  state.sizeIndex=ix;
  sizesEl.innerHTML = BB.variants.map(function(vr){
    var label=(vr.options[ix]||vr.title||'').toString();
    var num=label.replace(/\\s*years?\\s*/i,'').trim()||label;
    return '<button class="size'+(vr.available?'':' out')+'" data-size="'+label+
           '" data-vid="'+vr.id+'"'+(vr.available?'':' disabled')+'>'+num+
           '<small>'+(vr.available?'years':'sold out')+'</small></button>';
  }).join('');
})();""", "picker")

rep("  state.size=b.dataset.size;", """  state.size=b.dataset.size;
  if(b.dataset.vid){
    state.variantId=+b.dataset.vid;
    var chosen=(BB.variants||[]).filter(function(x){return x.id===state.variantId;})[0];
    if(chosen){ PRICE=chosen.price/100; BB.available=chosen.available;
      document.querySelectorAll('.price').forEach(function(el){
        el.textContent=PRICE>0?inrRaw(PRICE):'Price coming soon'; });
      syncAddBtn(); }
  }""", "variant select")

# 7 ── cart drawer from /cart.js
old = re.search(r"function renderCart\(\)\{.*?\n\}\n", s, re.S).group(0)
s = s.replace(old, """function renderCart(cart){
  var body=document.getElementById('cartBody');
  var cc=document.getElementById('cartCount');
  var items=(cart&&cart.items)||[];
  var n=(cart&&cart.item_count)||0;
  var sub=((cart&&cart.total_price)||0)/100;
  cc.textContent=n; cc.classList.toggle('on',n>0);
  document.getElementById('subTot').textContent=inr(sub);
  document.getElementById('freeFill').style.width=Math.min(100, FREE_AT?sub/FREE_AT*100:0)+'%';
  document.getElementById('freeNote').innerHTML = sub>=FREE_AT
    ? '\\ud83c\\udf89 You\\u2019ve unlocked <b>free shipping</b>!'
    : 'Add <b>'+inr(Math.max(0,FREE_AT-sub))+'</b> more for free shipping';
  if(!items.length){ body.innerHTML='<div class="cart-empty">Your bag is feeling light.<br>Just like the shirt.</div>'; return; }
  body.innerHTML = items.map(function(i){
    var size=(i.properties&&i.properties.Size)?i.properties.Size:(i.variant_title||'');
    var img=i.image ? i.image.replace(/(\\.[a-z]+)(\\?|$)/i,'_160x$1$2') : '';
    return '<div class="ci"><img src="'+img+'" alt=""><div class="info"><b>'+i.product_title+'</b>'+
      '<small>'+size+'</small><div class="row"><span>'+inr(i.line_price/100)+' \\u00d7 '+i.quantity+'</span>'+
      '<button class="rm" data-key="'+i.key+'">Remove</button></div></div></div>';
  }).join('<div style="height:10px"></div>');
  body.querySelectorAll('.rm').forEach(function(b){
    b.onclick=function(){
      fetch('/cart/change.js',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({id:b.dataset.key,quantity:0})})
        .then(function(r){return r.json();}).then(renderCart);
    };
  });
}
""")

# 8 ── add to cart -> Shopify
old = re.search(r"function addToCart\(ev\)\{.*?\n\}\n", s, re.S).group(0)
s = s.replace(old, """function addToCart(ev){
  if(!state.size){
    document.getElementById('sizes').scrollIntoView({behavior:reduce?'auto':'smooth',block:'center'});
    setTimeout(function(){
      sizesEl.classList.add('shake');
      setTimeout(function(){sizesEl.classList.remove('shake');},500);
    }, reduce?0:520);
    return Promise.resolve(false);
  }
  if(!(state.variantId||BB.variantId) || !BB.available){
    alert('This size isn\\u2019t available to order right now.');
    return Promise.resolve(false);
  }
  var btn=ev&&ev.currentTarget, txt=btn&&btn.textContent;
  if(btn){ btn.disabled=true; btn.textContent='Adding\\u2026'; }
  return shopAdd(state.size, state.qty)
    .then(shopCart)
    .then(function(cart){
      renderCart(cart); openCart();
      if(ev&&ev.clientX) balloonBurst(ev.clientX,ev.clientY);
      return true;
    })
    .catch(function(e){ alert((e&&e.description)||'Could not add to cart.'); return false; })
    .finally(function(){ if(btn){ btn.disabled=false; btn.textContent=txt; } });
}
""")

rep("document.getElementById('buyNow').addEventListener('click',function(e){ addToCart(e); setTimeout(goCheckout,650); });",
    "document.getElementById('buyNow').addEventListener('click',function(e){ addToCart(e).then(function(ok){ if(ok) goCheckout(); }); });",
    "buynow")

rep("document.getElementById('yr').textContent=new Date().getFullYear();",
    "shopCart().then(renderCart).catch(function(){});\ndocument.getElementById('yr').textContent=new Date().getFullYear();",
    "hydrate")

rep("function syncAddBtn(){ document.getElementById('addBtn').textContent='Add to cart — '+inr(PRICE*state.qty); }",
    "function syncAddBtn(){ document.getElementById('addBtn').textContent = PRICE>0 ? ('Add to cart — '+inr(PRICE*state.qty)) : 'Add to cart'; }",
    "addbtn")

io.open(OUT, "w", encoding="utf-8").write(s)
print("built %s  (%d bytes)" % (OUT, len(s)))
print("staged %d assets" % len(glob.glob("shopify/assets/%s*.webp" % (PREFIX or "bk-"))))

import subprocess as _sp; _sp.run(["python","patch-layout.py"])

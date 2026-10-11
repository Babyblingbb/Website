"""Mobile header: hamburger left, logo centred, Shop-now + cart hidden (<920px); slide-in menu drawer."""
import re

MENU_CSS = """<style id="bb-menu">.burger{display:none}
@media(max-width:919px){.nav-in{display:grid!important;grid-template-columns:44px 1fr 44px;align-items:center}
 .nav-cta{display:none!important}.nav-in>.logo{justify-self:center}
 .burger{display:grid;place-items:center;width:44px;height:44px;border:0;background:none;padding:0;cursor:pointer;color:var(--ink)}}
#mMenu{position:fixed;inset:0;z-index:200;pointer-events:none}
#mMenu .scr{position:absolute;inset:0;background:rgba(10,30,50,.35);opacity:0;transition:opacity .3s}
#mMenu nav{position:absolute;left:0;top:0;bottom:0;width:min(84vw,340px);background:#fff;transform:translateX(-102%);
 transition:transform .35s cubic-bezier(.22,1,.36,1);padding:22px 24px;display:flex;flex-direction:column;overflow:auto;box-shadow:20px 0 60px rgba(10,30,50,.2)}
#mMenu.on{pointer-events:auto}#mMenu.on .scr{opacity:1}#mMenu.on nav{transform:none}
#mMenu .mh{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
#mMenu .mx{border:0;background:none;font-size:1.4rem;cursor:pointer;color:var(--ink)}
#mMenu a.ml{font-family:'Fredoka';font-weight:500;font-size:1.2rem;padding:12px 0;border-bottom:1px solid rgba(20,70,110,.08);color:var(--ink)}
#mMenu a.ms{font-size:.95rem;padding:9px 0;color:var(--ink-2)}#mMenu .sp{height:14px}
</style>"""

BURGER = ('<button class="burger" id="burger" aria-label="Open menu"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" '
          'stroke="currentColor" stroke-width="2.1" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>\n    ')

MENU = """<div id="mMenu" aria-hidden="true"><div class="scr" data-x></div><nav aria-label="Menu">
 <div class="mh"><a href="/" class="logo"><span class="dot"></span><b>Baby&nbsp;Bling</b></a><button class="mx" data-x aria-label="Close menu">✕</button></div>
 <a class="ml" href="/">Home</a><a class="ml" href="/collections/shirts">Shop all shirts</a><a class="ml" href="/#shop">Bestsellers</a>
 <a class="ml" href="/#fabric">The fabric</a><a class="ml" href="/#made">How it&#39;s made</a><a class="ml" href="/cart">Cart <span id="mCnt"></span></a>
 <div class="sp"></div>
 <a class="ms" href="/pages/size-guide">Size guide</a><a class="ms" href="/pages/shipping">Shipping</a><a class="ms" href="/policies/refund-policy">Returns &amp; exchanges</a>
 <a class="ms" href="/pages/track-order">Track order</a><a class="ms" href="/pages/contact">Contact us</a><a class="ms" href="https://www.instagram.com/thebabybling/" target="_blank" rel="noopener">Instagram @thebabybling</a>
 <a href="/collections/shirts" class="btn btn-primary btn-block" style="margin-top:22px">Shop now</a>
</nav></div>
<script>(function(){var m=document.getElementById('mMenu'),b=document.getElementById('burger');if(!m||!b)return;
function t(o){m.classList.toggle('on',o);m.setAttribute('aria-hidden',!o);document.body.style.overflow=o?'hidden':'';
 if(o)fetch('/cart.js').then(function(r){return r.json()}).then(function(c){document.getElementById('mCnt').textContent=c.item_count?'('+c.item_count+')':''}).catch(function(){});}
b.onclick=function(){t(true)};m.querySelectorAll('[data-x]').forEach(function(x){x.onclick=function(){t(false)}});
m.querySelectorAll('nav a').forEach(function(a){a.addEventListener('click',function(){t(false)})});})();</script>
</body>"""

def menu_patch(s):
    s = re.sub(r'<style id="bb-menu">.*?</style>\n', '', s, flags=re.S)
    s = s.replace("</head>", MENU_CSS + "\n</head>", 1)
    if 'id="burger"' not in s:
        s = re.sub(r'(<header id="nav">\s*<div class="wrap nav-in">\s*)', lambda m: m.group(1) + BURGER, s, count=1)
    s = re.sub(r'<div id="mMenu".*?</script>\n</body>', lambda m: MENU, s, flags=re.S)
    if 'id="mMenu"' not in s:
        s = s.replace("</body>", MENU, 1)
    return s

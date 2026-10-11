"""Two coupon tickets under the Buy-now button. Pilot pages only until approved.
NOTE: FIRST10 must exist as a Shopify/Shiprocket discount code; prepaid 5% must be enabled in Shiprocket Checkout settings."""
import re

COUPON_PAGES = ["product"]   # all product pages

CSS = """<style id="bb-cp">
.cpns{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px}
.cpn{position:relative;display:flex;flex-direction:column;gap:3px;padding:12px 12px 11px 16px;border-radius:16px;text-align:left;
  background:linear-gradient(135deg,#FFF6E5,#FFE7C2);border:1.5px dashed #E8A54B;color:#5b3a00;overflow:hidden}
.cpn.pp{background:linear-gradient(135deg,#E9F8EF,#CDEFD9);border-color:#3FA46A;color:#11502c}
.cpn::before,.cpn::after{content:"";position:absolute;left:-9px;top:50%;width:16px;height:16px;margin-top:-8px;border-radius:50%;background:var(--cp-bg,#e8f4fb)}
.cpn::after{left:auto;right:-9px}
.cpn .off{font-family:'Fredoka';font-weight:700;font-size:1.25rem;line-height:1.05}
.cpn .why{font-size:.74rem;font-weight:500;opacity:.85;line-height:1.25}
.cpn .code{margin-top:6px;display:flex;align-items:center;justify-content:space-between;gap:6px;font-size:.74rem}
.cpn .code b{font-family:ui-monospace,Menlo,Consolas,monospace;letter-spacing:.06em;font-size:.8rem;background:rgba(255,255,255,.75);padding:3px 7px;border-radius:7px}
.cpn button{border:0;background:#5b3a00;color:#fff;font-size:.7rem;font-weight:700;padding:5px 9px;border-radius:99px;cursor:pointer}
.cpn .auto{font-weight:700;font-size:.72rem;background:rgba(255,255,255,.75);padding:3px 8px;border-radius:7px}
@media(max-width:360px){.cpn .off{font-size:1.1rem}}
</style>"""

HTML = """
      <div class="cpns" id="cpns">
        <div class="cpn"><span class="off">10% OFF</span><span class="why">First order? Flat 10% off</span>
          <span class="code"><b>FIRST10</b><button type="button" data-copy="FIRST10">Copy</button></span></div>
        <div class="cpn pp"><span class="off">+5% OFF</span><span class="why">Extra on prepaid orders</span>
          <span class="code"><span class="auto">Auto at checkout</span></span></div>
      </div>
      <script>document.querySelectorAll('#cpns [data-copy]').forEach(function(b){b.addEventListener('click',function(){var c=b.getAttribute('data-copy');
        (navigator.clipboard?navigator.clipboard.writeText(c):Promise.reject()).catch(function(){}).finally(function(){b.textContent='Copied ✓';setTimeout(function(){b.textContent='Copy'},1600);});});});</script>"""

def cp_patch(s, fname):
    s = re.sub(r'<style id="bb-cp">.*?</style>\n', '', s, flags=re.S)
    s = re.sub(r'\n\s*<div class="cpns" id="cpns">.*?</script>', '', s, flags=re.S)
    if any(fname.startswith("/" + p + ".") for p in COUPON_PAGES):
        s = s.replace("</head>", CSS + "\n</head>", 1)
        s = re.sub(r'(<button class="btn btn-dark btn-block" id="buyNow">.*?</button>)', lambda m: m.group(1) + HTML, s, count=1)
    return s

"""TEST ONLY: sample reviews section on Sail Away -> uploaded to the UNPUBLISHED theme for preview. Never ship to live."""
import io, sp
PREVIEW_THEME = 142438236263   # unpublished "Tinker"
src = io.open("shopify/templates/product.sail-shirt.liquid", encoding="utf-8").read()

CSS = """<style id="bb-rv">
.rv-row{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;margin-inline:calc(-1*var(--pad));padding:6px var(--pad) 18px;scrollbar-width:none}
.rv-row::-webkit-scrollbar{display:none}
.rv{flex:0 0 min(80%,330px);scroll-snap-align:center;background:#FFFDF8;border-radius:22px;padding:18px;box-shadow:0 14px 32px rgba(20,70,110,.14);position:relative}
.rv .top{display:flex;align-items:center;gap:10px}
.rv .av{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;font-family:'Fredoka';font-weight:600;color:#fff;background:var(--c)}
.rv .nm{font-weight:600;font-size:.95rem;color:var(--ink)}
.rv .rl{font-size:.78rem;color:var(--ink-2)}
.rv p{margin-top:12px;font-size:.9rem;line-height:1.5;color:var(--ink-2)}
.rv .meta{margin-top:10px;font-size:.74rem;color:var(--ink-2);opacity:.8}
.rv .smp{position:absolute;top:12px;right:12px;font-size:.62rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  background:#FFE6A8;color:#7a5600;padding:3px 8px;border-radius:99px}
</style>"""

R = [("V", "#F2A08F", "Vaibhav", "Rishi's father", "Mumbai · 5–6 years",
      "Super light — he wore it all day at the beach and didn't complain once. The embroidery is so neat."),
     ("N", "#8FCFB4", "Neha", "Aarav's mother", "Bengaluru · 7–8 years",
      "Soft from the first wash, no itchy tag. Fit is roomy, so we'll get two summers out of it."),
     ("K", "#B9A6EE", "Karan", "Myra's father", "Delhi · 4–5 years",
      "Coconut buttons are a lovely touch. Colour stayed bright after three washes."),
     ("S", "#7FB6F0", "Shruti", "Vihaan's mother", "Pune · 8–9 years",
      "Ordered for a birthday — looked premium out of the box. Delivery was quick too.")]

def card(a, c, n, rel, meta, t):
    return (f'      <div class="rv" style="--c:{c}"><span class="smp">Sample</span><div class="top"><span class="av">{a}</span>'
            f'<div><div class="nm">{n}</div><div class="rl">{rel}</div></div></div><p>{t}</p><div class="meta">{meta}</div></div>')

cards = "\n".join(card(*r) for r in R)
SEC = f"""<!-- ══════════════ SAMPLE REVIEWS (TEST) ══════════════ -->
<section class="sec" id="cust-reviews">
  <div class="wrap">
    <div class="sec-head rev"><p class="eyebrow">Parents say</p><h2>Loved on the playground.</h2></div>
    <div class="rv-row">
{cards}
    </div>
  </div>
</section>

"""
out = src.replace("</head>", CSS + "\n</head>", 1)
anchor = "<!-- ══════════════ FAQ"
assert anchor in out
out = out.replace(anchor, SEC + anchor, 1)
io.open("shopify/templates/_test-reviews.product.sail-shirt.liquid", "w", encoding="utf-8").write(out)
x = sp.call("PUT", f"themes/{PREVIEW_THEME}/assets.json", {"asset": {"key": "templates/product.sail-shirt.liquid", "value": out}})
print("preview upload", "_error" not in x, "" if "_error" not in x else str(x)[:300])
print(f"https://babybling.in/products/beach-linen-shirt?preview_theme_id={PREVIEW_THEME}")

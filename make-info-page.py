"""templates/page.bb.liquid — cloud-style info page (shipping, size guide, track order, about, faq).
Content picked by page.handle; unknown handles render page.content."""
import io, re
S = io.open("index-shop.html", encoding="utf-8").read()
head, rest = S.split("<body>", 1)
body_start = re.search(r"^.*?</header>\n", rest, re.S).group(0)          # sky + ticker + nav
footer_on = rest[rest.index("<!-- ══════════════ FOOTER"):]                 # footer + script + end

CSS = """<style>
.info{max-width:760px;margin:0 auto}
.info h1{font-size:clamp(2.2rem,7vw,3.4rem);letter-spacing:-.03em;text-align:center}
.info .lead{text-align:center;color:var(--ink-2);margin:12px auto 0;max-width:46ch}
.card{background:rgba(255,255,255,.78);backdrop-filter:blur(14px);border-radius:28px;padding:clamp(20px,4vw,40px);
  margin-top:clamp(22px,4vw,40px);box-shadow:0 20px 50px rgba(20,70,110,.10)}
.card h2{font-size:1.35rem;margin:22px 0 8px}.card h2:first-child{margin-top:0}
.card p,.card li{color:var(--ink-2);line-height:1.65}.card ul{padding-left:1.1em;margin:6px 0}
.card table{width:100%;border-collapse:collapse;margin-top:8px;font-size:.95rem}
.card th,.card td{padding:11px 8px;border-bottom:1px solid rgba(20,70,110,.12);text-align:left}
.card th{font-family:'Fredoka';font-weight:600}
.trk{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px}
.trk input{flex:1 1 220px;padding:15px 18px;border-radius:999px;border:1.5px solid rgba(20,70,110,.18);font:inherit;font-size:1rem;background:#fff}
.info-cta{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-top:28px}
</style>"""

CONTENT = {
"shipping": ("Shipping", "Packed within 24 hours, at your door in 2–5 days.", """
<h2>Dispatch</h2><p>Orders placed before 4 pm on a working day leave our studio the same day; everything else goes out within 24 hours.</p>
<h2>Delivery time</h2><ul><li>Metro cities: 2–3 working days</li><li>Rest of India: 3–5 working days</li><li>Remote pin codes: up to 7 working days</li></ul>
<h2>Charges</h2><p>Free shipping on orders over ₹999. A small flat fee applies below that and is shown at checkout.</p>
<h2>Cash on delivery</h2><p>Available across India. Prepaid orders are dispatched first.</p>
<h2>Tracking</h2><p>You'll get an SMS, WhatsApp and email with your tracking link as soon as the parcel ships. You can also <a href="/pages/track-order">track your order here</a>.</p>"""),
"size-guide": ("Size guide", "Our shirts run true to age with a relaxed, roomy fit — kids move.", """
<table><tr><th>Size</th><th>Child's age</th><th>Fits height</th></tr>
<tr><td>4–5 years</td><td>4 to 5</td><td>104–110 cm</td></tr><tr><td>5–6 years</td><td>5 to 6</td><td>110–116 cm</td></tr>
<tr><td>6–7 years</td><td>6 to 7</td><td>116–122 cm</td></tr><tr><td>7–8 years</td><td>7 to 8</td><td>122–128 cm</td></tr>
<tr><td>8–9 years</td><td>8 to 9</td><td>128–134 cm</td></tr><tr><td>9–10 years</td><td>9 to 10</td><td>134–140 cm</td></tr></table>
<h2>Between sizes?</h2><p>Size up. The fit is intentionally relaxed and the fabric is pre-shrunk, so the bigger size lasts a whole extra summer.</p>
<h2>Still unsure?</h2><p>Exchanges for a different size are free within 7 days — see our <a href="/policies/refund-policy">returns policy</a>.</p>"""),
"track-order": ("Track your order", "Enter the AWB / tracking number from your shipping SMS or email.", """
<form class="trk" onsubmit="event.preventDefault();var v=this.awb.value.trim();if(v)window.open('https://shiprocket.co/tracking/'+encodeURIComponent(v),'_blank');">
<input name="awb" placeholder="Tracking / AWB number" aria-label="Tracking number" required><button class="btn btn-primary" type="submit">Track</button></form>
<h2>Can't find it?</h2><p>Your tracking link is in the shipping SMS, WhatsApp and email we send on dispatch. If you've placed an order and haven't received it within 24 hours, <a href="/pages/contact">message us</a> with your order number.</p>
{% if customer %}<p><a href="/account">See all your orders →</a></p>{% else %}<p>Have an account? <a href="/account/login">Log in</a> to see all your orders.</p>{% endif %}"""),
"about": ("About Baby Bling", "Featherlight linen for kids who don't sit still.", """
<p>Baby Bling started with a simple frustration: kids' clothes that looked lovely and felt awful in an Indian summer. So we made the shirt we wanted — a fine linen-cotton blend woven thin on purpose, pre-washed until it's soft, and finished by hand.</p>
<h2>What goes into every shirt</h2><ul><li>A 120 GSM linen-cotton blend that breathes in 40°C</li><li>Motifs embroidered thread by thread — never printed</li><li>Coconut wood buttons, smooth-sanded and double-stitched</li><li>No itchy tags at the neck — just a soft woven patch at the hem</li></ul>
<h2>Made in India</h2><p>Every shirt is cut, stitched and embroidered in India, in small batches, by hands we know.</p>"""),
}
branches = "\n".join(
    f"{{%- when '{h}' -%}}<h1>{t}</h1><p class=\"lead\">{l}</p><div class=\"card\">{c}</div>"
    for h, (t, l, c) in CONTENT.items())
MAIN = f"""
<section class="sec" style="padding-top:clamp(24px,4vw,56px)">
  <div class="wrap"><div class="info rev">
{{%- case page.handle -%}}
{branches}
{{%- else -%}}<h1>{{{{ page.title }}}}</h1><div class="card">{{{{ page.content }}}}</div>
{{%- endcase -%}}
    <div class="info-cta"><a href="/collections/shirts" class="btn btn-primary">Shop all shirts</a><a href="/pages/contact" class="btn btn-ghost">Contact us</a></div>
  </div></div>
</section>

"""
head = re.sub(r"<title>.*?</title>", "<title>{{ page.title }} | Baby Bling</title>", head)
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="{{ page.title }} — Baby Bling, featherlight linen shirts for kids.">', head)
head = head.replace("</head>", CSS + "\n</head>")
out = "{% layout none %}\n" + head + "<body>" + body_start + MAIN + footer_on
out = out.replace("url('assets/shirt.webp')", "url({{ 'bb-shirt.webp' | asset_url }})"); assert 'assets/' not in out.replace('/assets/','')
io.open("shopify/templates/page.bb.liquid", "w", encoding="utf-8").write(out)
import subprocess as _sp; _sp.run(["python", "patch-layout.py", "shopify/templates/page.bb.liquid"])
print("page.bb.liquid", len(out))

import io, re
s = io.open("index-shop.html", encoding="utf-8").read()
ROWS = [("peach-linen-shirt","g-bb","#D63B31","Balloon Bicycle"),("blue-linen-shirt","g-bk","#2F63D8","Kite Dreams"),
        ("storytelling-linen-shirt","g-bs","#8E2740","Storytelling"),("baby-pink-linen-shirt","g-bp","#D94A72","Hearts"),
        ("dino-linen-shirt","g-bd","#1F7A78","Dino Adventure"),("shinchan-linen-shirt","g-bn","#CE2222","Shinchan"),
        ("black-linen-shirt","g-bl","#B5340C","Rocket Launch"),("sea-green-linen-shirt","g-bg","#1F5138","Little Gardener"),("beach-linen-shirt","g-bw","#1D5D8C","Sail Away"),("beige-linen-shirt","g-bc","#B8342A","Rock Pool"),("white-logo-linen-shirt","g-bf","#D96A18","Weekend Doodles")]
grid = re.search(r'<div class="grid">\n(.*?)\n    </div>', s, re.S); assert grid
spec = ",".join("|".join(r) for r in ROWS)
liq = ("<div class=\"grid\">\n      {%- assign rows = '" + spec + "' | split: ',' -%}\n"
 "      {%- for row in rows -%}{%- assign f = row | split: '|' -%}{%- assign p = all_products[f[0]] -%}{%- if p.title != blank -%}\n"
 "        <a class=\"sh rev\" href=\"{{ p.url }}\"><span class=\"sh-stage\"><img src=\"{{ f[1] | append: '.webp' | asset_url }}\" alt=\"{{ f[3] | escape }} shirt\"{% if forloop.index <= 4 %} fetchpriority=\"high\"{% else %} loading=\"lazy\"{% endif %} decoding=\"async\"><span class=\"gr\"></span></span>"
 "<span class=\"sh-name\" style=\"color:{{ f[2] }}\">{{ f[3] }}</span><span class=\"sh-price\">{{ p.price | money_without_trailing_zeros }}</span></a>\n"
 "      {%- endif -%}{%- endfor -%}\n    </div>")
s = s.replace(grid.group(0), liq).replace("url('assets/shirt.webp')", "url({{ 'bb-shirt.webp' | asset_url }})")
assert 'src="assets' not in s
io.open("shopify/templates/collection.floating.liquid","w",encoding="utf-8").write("{% layout none %}\n"+s)
print("liquid ok")

import subprocess as _sp; _sp.run(["python","patch-layout.py"])

import sp, base64, os, glob
THEME = 142438236263
def put(key, path, binary):
    payload = {"asset": {"key": key, "attachment": base64.b64encode(open(path,'rb').read()).decode()}} if binary \
        else {"asset": {"key": key, "value": open(path, encoding='utf-8').read()}}
    r = sp.call("PUT", f"themes/{THEME}/assets.json", payload)
    ok = "_error" not in r
    print(f"  {'ok  ' if ok else 'FAIL'} {key:<40} {r.get('asset',{}).get('size', r.get('_body','')[:80])}")
    return ok
n = 0
for f in sorted(glob.glob("shopify/assets/bb-*.webp")):
    n += put("assets/"+os.path.basename(f), f, True)
n += put("templates/product.balloon-shirt.liquid", "shopify/templates/product.balloon-shirt.liquid", False)
print(f"{n}/8 uploaded")

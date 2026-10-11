"""Convert fabric renders, rebuild every product page with the fabric sections, upload."""
import subprocess, os, glob, shutil, base64, time, sys
from PIL import Image
from cutout import cutout
import sp
T = 142438236263
PAGES = [  # key, generator, html, template, asset dir, prefix, colour word
 ("peach",None,"index-peach.html","balloon-shirt","assets","","peach"),
 ("kite","make-kite-page.py","index-kite.html","kite-shirt","assets-kite","bk-","sky-blue"),
 ("story","make-story-page.py","index-story.html","story-shirt","assets-story","bs-","maroon"),
 ("pink","make-pink-page.py","index-pink.html","hearts-shirt","assets-pink","bp-","blush pink"),
 ("dino","make-dino-page.py","index-dino.html","dino-shirt","assets-dino","bd-","cream"),
 ("shin","make-shin-page.py","index-shin.html","shin-shirt","assets-shin","bn-","cream"),
 ("blk","make-blk-page.py","index-blk.html","rocket-shirt","assets-blk","bl-","black"),
 ("sea","make-sea-page.py","index-sea.html","garden-shirt","assets-sea","bg-","sage"),
 ("beach","page3","index-beach.html","sail-shirt","assets-beach","bw-","white"),
 ("beige","page3","index-beige.html","rockpool-shirt","assets-beige","bc-","cream"),
 ("white","page3","index-white.html","doodles-shirt","assets-white","bf-","cream")]
def py(*a): r=subprocess.run(["python",*a],capture_output=True,text=True); assert r.returncode==0, (a, r.stderr[-400:])
def put(key, path, binary=True):
    pl={"asset":{"key":key,"attachment":base64.b64encode(open(path,"rb").read()).decode()}} if binary \
        else {"asset":{"key":key,"value":open(path,encoding="utf-8").read()}}
    for _ in range(3):
        if "_error" not in sp.call("PUT",f"themes/{T}/assets.json",pl): return 1
        time.sleep(2)
    print("  UPLOAD FAIL",key); return 0
up=0
for k,gen,html,tpl,d,p,col in PAGES:
    if k!="peach":
        for n,w in [("fabric-feather",1800),("fabric-weave",2000)]:
            src=f"{d}/{p}{n}.png"
            if not os.path.exists(src): print("MISSING",src); continue
            im=Image.open(src).convert("RGB"); im.resize((w,round(w*im.height/im.width)),Image.LANCZOS).save(f"{d}/{p}{n}.webp","WEBP",quality=84,method=6)
        sw=f"{d}/{p}swatch.png"
        if os.path.exists(sw):
            test=(lambda r,g,b: r>g+12 and min(r,g,b)>170) if k=="kite" else (lambda r,g,b: b>r+12 and min(r,g,b)>165)
            cutout(sw,bg_test=test,erode=3).save(f"{d}/{p}swatch.webp","WEBP",quality=90,method=6)
        for n in ["flax","cotton"]: shutil.copy(f"assets/{n}.webp", f"{d}/{p}{n}.webp")
        if gen=="page3": py("make-page3.py",k)
        else: py(gen)
        py("add-fabric.py",html,html,d,col,p)
        py("build-liquid.py",html,tpl,d,"")
    else:
        py("add-fabric.py","index.html","index-peach.html","assets","peach","")
        py("build-liquid.py","index-peach.html","balloon-shirt","assets","bb-")
    pre = "bb-" if k=="peach" else p
    for n in ["fabric-feather","fabric-weave","swatch","flax","cotton"]:
        f=f"shopify/assets/{pre}{n}.webp"
        if os.path.exists(f): up+=put(f"assets/{pre}{n}.webp",f)
    up+=put(f"templates/product.{tpl}.liquid",f"shopify/templates/product.{tpl}.liquid",False)
    print(f"  {k:<6} built + uploaded", flush=True)
py("make-shop-page.py"); py("build-shop-liquid.py")
up+=put("templates/collection.floating.liquid","shopify/templates/collection.floating.liquid",False)
print("total uploads", up)

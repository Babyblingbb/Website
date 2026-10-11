"""Per-shirt fabric renders: feather, weave macro, swatch.  python gen-fabric.py [key ...]"""
import subprocess, sys, os
G = "C:/Users/Mudit Sharma/.claude/scripts/gen-image.py"
S = {  # key: (asset dir, prefix, colour words, colour ref)
 "kite": ("assets-kite","bk-","pale sky-blue","ref-kite/front.jpg"),
 "story":("assets-story","bs-","deep maroon / burgundy","ref-story/front.jpg"),
 "pink": ("assets-pink","bp-","soft blush pink","ref-pink/front.jpg"),
 "dino": ("assets-dino","bd-","natural cream / oatmeal","ref-dino/front.jpg"),
 "shin": ("assets-shin","bn-","natural cream","ref-shin/front.jpg"),
 "blk":  ("assets-blk","bl-","deep black","ref-blk/front.jpg"),
 "sea":  ("assets-sea","bg-","very pale sage / oatmeal","ref-sea/front.jpg"),
 "beach":("assets-beach","bw-","crisp white","ref-beach/3.jpg"),
 "beige":("assets-beige","bc-","natural cream","ref-beige/3.jpg"),
 "white":("assets-white","bf-","natural cream","ref-white/3.jpg")}
def run(p, out, ref, aspect):
    if os.path.exists(out): return
    import time
    for t in range(4):
        subprocess.run(["python",G,p,out,"--ref",ref,"--aspect",aspect,"--model","gemini-3-pro-image"],capture_output=True)
        if os.path.exists(out): break
        time.sleep(25*(t+1))
    print(("ok  " if os.path.exists(out) else "FAIL")+" "+out, flush=True)
for k in sys.argv[1:] or S:
    d,p,c,ref = S[k]; C=c.upper()
    run(f"Luxury editorial photograph. A large, gossamer-light piece of fine {C} linen, the exact colour of the reference garment, billows and ripples softly in mid-air like a sheer curtain caught in a breeze — thin, soft folds, never stiff, never flat, never paper-like. A single pure white downy feather drifts beside it at the same height, as if both weigh nothing. Soft golden backlight glows through the fabric so the fine weave is faintly visible and the fold edges are luminous. Background: soft out-of-focus pale blue sky with blurred white clouds. Shallow depth of field, dreamy, calm, very premium, minimal, empty space on the left. No text, no hands, no embroidery, no buttons.", f"{d}/{p}fabric-feather.png", ref, "16:9")
    run(f"Extreme macro photograph of FINE, lightweight, soft {C} linen, the exact colour of the reference garment: delicate thin threads in a fine plain weave with gentle natural slubs, a soft subtle sheen on the fibres, tiny pin-point gaps between threads glowing faintly with warm backlight, a few wisps of soft fibre catching the light. Smooth, supple and soft — NOT coarse, NOT burlap, NOT jute, NOT canvas. A gentle soft fold runs diagonally across the frame. Luxury textile photography, tack-sharp on the fold, fabric fills the frame edge to edge. No embroidery, no buttons, no text.", f"{d}/{p}fabric-weave.png", ref, "16:9")
    bgw = "pastel PINK background (#F6D5DC)" if k=="kite" else "pastel BLUE background (#CFE6F7)"
    run(f"A small square piece of very FINE, feather-light {C} linen-cotton fabric, the exact colour of the reference garment, softly draped in a loose gentle S-shaped wave as if floating, delicate fine even weave visible, soft natural sheen, thin and supple, finely finished edges, never stiff, never coarse. Luxury textile product photograph, soft diffused studio light from the upper left, gentle self-shadowing in the folds. Centred with space around it. Isolated on a perfectly flat, plain, uniform {bgw}, nothing else in frame, no shadow on the background, no text, no embroidery.", f"{d}/{p}swatch.png", ref, "1:1")

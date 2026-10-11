#!/usr/bin/env python3
"""3D renders for the Blue Kite linen shirt — Cosmic View Vertex (mudit@thecosmicview.com).
Refs are the real Shopify product photos in ref-kite/.

  python gen3d-kite.py            # all shots
  python gen3d-kite.py hero
"""
import subprocess, sys, os

SCRIPT = r"C:\Users\Mudit Sharma\.claude\scripts\gen-image.py"   # Cosmic View, own credits
MODEL  = "gemini-3-pro-image"                                     # NO -preview on this project
OUT    = "gen-kite"
os.makedirs(OUT, exist_ok=True)

PRODUCT = (
 "The garment must match the reference photographs EXACTLY: a child's pale sky-blue LINEN "
 "short-sleeve shirt with an open Cuban camp collar and five round coconut-wood buttons down "
 "the centre front placket. Embroidered on the front: a small diamond kite in red, yellow and "
 "blue at the upper right chest, with a long fine navy dashed string that loops and curls down "
 "and across the shirt, plus two puffy WHITE embroidered clouds — one small in the middle, one "
 "larger toward the lower left. A small square cream woven patch with two tiny embroidered "
 "children sits low on the right front. Keep the visible linen weave, the exact pale blue "
 "colour, the white cloud embroidery and every stitch detail identical to the references. Do "
 "not add, remove, restyle or reposition any design element. No text or watermark beyond the "
 "small woven neck label shown."
)

SHOTS = {
 "hero": dict(refs=["ref-kite/front.jpg", "ref-kite/kite.jpg"], aspect="1:1", prompt=(
   "Ultra high resolution ghost-mannequin (invisible mannequin) e-commerce product photograph. "
   + PRODUCT +
   " The shirt holds full three-dimensional volume exactly as if worn by an invisible child: the "
   "camp collar stands open with a soft roll, chest and shoulders filled out, both short sleeves "
   "rounded with air, hem falling with a natural gentle drape. It hovers weightlessly, tilted a "
   "few degrees as though caught mid-float in a light breeze. Soft diffused studio light from the "
   "upper left, delicate self-shadowing inside the collar and under the sleeves, a faint soft "
   "contact shadow far below. Crisp, tactile, hyper-detailed, professional apparel catalogue "
   "photography. Isolated on a pure flat plain white background, nothing else in frame.")),

 "clouds": dict(refs=["ref-kite/front.jpg", "ref-kite/kite.jpg"], aspect="1:1", prompt=(
   "A dreamy 3D product render of a child's pale blue linen shirt floating high in a bright "
   "summer sky among soft rounded puffy white cartoon clouds. " + PRODUCT +
   " The shirt has full ghost-mannequin volume as if worn by an invisible child, drifting "
   "weightlessly with a gentle tilt, sleeves lifted by the breeze. A real diamond kite flies "
   "nearby on a long string, echoing the embroidered one. Warm sunlight from the upper left, "
   "soft rim-light along the shoulders, gentle ambient bounce from the clouds below. Clean, "
   "playful, premium childrenswear brand imagery. Bright, airy, cheerful.")),

 "detail": dict(refs=["ref-kite/kite.jpg", "ref-kite/cloud.jpg"], aspect="1:1", prompt=(
   "Extreme close-up macro product photograph of hand embroidery on pale sky-blue linen fabric. "
   "A small diamond kite embroidered in red, yellow and blue satin stitch, with a fine navy "
   "dashed string curling away from it, and a puffy white embroidered cloud nearby in dense "
   "raised stitching. A coconut-wood button sits on the placket. Raking side light reveals the "
   "raised texture of every individual embroidery thread and the open weave of the linen. "
   "Shallow depth of field, tack-sharp on the embroidery. Match the reference exactly in colour, "
   "stitch style and layout. Luxury craft photography, no text or watermark.")),

 "folded": dict(refs=["ref-kite/front.jpg", "ref-kite/cloud.jpg"], aspect="4:3", prompt=(
   "Elegant flat-lay product photograph, shot straight down. " + PRODUCT +
   " The shirt is neatly folded into a soft rectangle with the embroidered kite and white clouds "
   "clearly visible on top, one sleeve softly turned to show the linen weave. It rests on a warm "
   "off-white linen surface. A few tiny dried flowers and a length of natural twine sit beside "
   "it. Soft natural window light from the left, gentle shadows. Calm, premium, editorial "
   "childrenswear styling.")),
}

def run(name, cfg):
    out = os.path.join(OUT, name + ".png")
    cmd = ["python", SCRIPT, cfg["prompt"], out, "--ref"] + cfg["refs"] + ["--model", MODEL]
    if cfg.get("aspect"):
        cmd += ["--aspect", cfg["aspect"]]
    print("\n=== %s -> %s ===" % (name, out))
    r = subprocess.run(cmd, capture_output=True, text=True)
    tail = (r.stdout or "").strip().splitlines()[-2:] + (r.stderr or "").strip().splitlines()[-3:]
    print("\n".join(tail) or "(no output)")
    ok = os.path.exists(out) and os.path.getsize(out) > 20000
    print("  ->", "OK %d KB" % (os.path.getsize(out)//1024) if ok else "FAILED")
    return ok

if __name__ == "__main__":
    want = sys.argv[1:] or list(SHOTS)
    good = sum(run(n, SHOTS[n]) for n in want if n in SHOTS)
    print("\n%d/%d generated" % (good, len(want)))

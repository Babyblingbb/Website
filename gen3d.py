#!/usr/bin/env python3
"""Generate 3D product renders for the Balloon Bicycle shirt via Hourglass Vertex.
Refs are the real Shopify product photos in ref/.

  python gen3d.py            # all shots
  python gen3d.py hero       # just one
"""
import subprocess, sys, os

SCRIPT = r"C:\Users\Mudit Sharma\Desktop\HG Claude\scripts\gen-vertex-image.py"
OUT    = "gen"
os.makedirs(OUT, exist_ok=True)

PRODUCT = (
 "The garment must match the reference photographs EXACTLY: a child's soft peach / pale "
 "salmon LINEN short-sleeve shirt with an open Cuban camp collar, five round coconut-wood "
 "buttons down the centre front placket, a delicate hand-embroidered black line-art bicycle "
 "on the lower right front carrying one red and one blue embroidered balloon on fine strings, "
 "and a small square cream woven patch with two tiny embroidered children near the lower left "
 "hem with red and blue corner stitches. Keep the visible linen weave texture, the exact peach "
 "colour, and every embroidery detail identical to the references. Do not add, remove, restyle "
 "or reposition any design element. No text, no watermark, no logos other than those shown."
)

SHOTS = {
 "hero": dict(refs=["ref/src2.jpg", "ref/src0.jpg"], aspect="1:1", prompt=(
   "Ultra high resolution ghost-mannequin (invisible mannequin) e-commerce product photograph. "
   + PRODUCT +
   " The shirt holds full three-dimensional volume exactly as if worn by an invisible child: the "
   "camp collar stands open with a soft roll, the chest and shoulders are filled out, both short "
   "sleeves are rounded with air, and the hem falls with a natural gentle drape. It hovers, "
   "weightless, tilted a few degrees as though caught mid-float in a light breeze. Soft diffused "
   "studio light from the upper left, delicate self-shadowing inside the collar and under the "
   "sleeves, a faint soft contact shadow far below. Crisp, tactile, hyper-detailed, professional "
   "apparel catalogue photography. Isolated on a pure flat plain white background, nothing else "
   "in frame.")),

 "clouds": dict(refs=["ref/src2.jpg", "ref/src0.jpg"], aspect="1:1", prompt=(
   "A dreamy 3D product render of a child's linen shirt floating high in a bright blue summer sky "
   "among soft, rounded, puffy white cartoon clouds. " + PRODUCT +
   " The shirt has full ghost-mannequin volume as if worn by an invisible child, drifting "
   "weightlessly with a gentle tilt, sleeves lifted by the breeze. Two small helium balloons, one "
   "red and one blue, drift nearby on fine strings. Warm sunlight from the upper left, soft "
   "rim-light along the shoulders, gentle ambient bounce from the clouds below. Clean, playful, "
   "premium childrenswear brand imagery. Bright, airy, cheerful.")),

 "detail": dict(refs=["ref/src0.jpg"], aspect="1:1", prompt=(
   "Extreme close-up macro product photograph of hand embroidery on peach linen fabric. A black "
   "line-art bicycle embroidered in fine satin stitch carries one red and one blue embroidered "
   "balloon on delicate strings. A coconut-wood button sits nearby on the placket. Raking side "
   "light reveals the raised texture of every individual embroidery thread and the open weave of "
   "the linen. Shallow depth of field, tack-sharp on the embroidery. Match the reference exactly "
   "in colour, stitch style and layout. Luxury craft photography, no text or watermark.")),

 "folded": dict(refs=["ref/src2.jpg", "ref/src0.jpg"], aspect="4:3", prompt=(
   "Elegant flat-lay product photograph, shot straight down. " + PRODUCT +
   " The shirt is neatly folded into a soft rectangle with the embroidered bicycle and balloons "
   "clearly visible on top and one sleeve softly turned to show the linen weave. It rests on a "
   "warm off-white linen surface. A few tiny dried flowers and a length of natural twine sit "
   "beside it. Soft natural window light from the left, gentle shadows. Calm, premium, editorial "
   "childrenswear styling.")),
}

def run(name, cfg):
    out = os.path.join(OUT, name + ".png")
    cmd = ["python", SCRIPT, cfg["prompt"], out, "--ref"] + cfg["refs"]
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

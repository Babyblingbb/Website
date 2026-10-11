#!/usr/bin/env python3
"""3D renders for the black Space linen shirt — Cosmic View Vertex.
Refs: ref-blk/. Written out in full, never patched from a sibling script.

  python gen3d-blk.py [shot ...]
"""
import subprocess, sys, os

SCRIPT = r"C:\Users\Mudit Sharma\.claude\scripts\gen-image.py"
MODEL  = "gemini-3-pro-image"
OUT    = "gen-blk"
os.makedirs(OUT, exist_ok=True)

PRODUCT = (
 "The garment must match the reference photographs EXACTLY: a child's BLACK linen short-sleeve "
 "shirt with an open Cuban camp collar and five round light TAN coconut-wood buttons down the "
 "centre front placket. A space scene is hand-embroidered across the front in fine WHITE / cream "
 "dashed running stitch: a tall rocket with small RED-ORANGE flames at its base on the LEFT side "
 "of the front; a ringed planet at the upper RIGHT; and a scatter of small planets, moons and "
 "tiny stars across the lower RIGHT. A small square cream woven patch with two tiny embroidered "
 "children sits low on the RIGHT front. Keep the visible linen weave, the deep black colour and "
 "every white dashed stitch identical to the references in size and placement. Do not add, "
 "remove, restyle or reposition any design element. This shirt has ONLY that space scene: there "
 "is NO kite, NO camera, NO books, NO hearts, NO dinosaur and NO cartoon character. No text or "
 "watermark beyond the small woven neck label shown."
)

VOLUME = (
 " STRONGLY three-dimensional — unmistakably a filled-out garment, never a flat lay. The chest "
 "and shoulders are rounded and full as if on an invisible child's body, the camp collar is "
 "rolled open so its underside is visible, both short sleeves are distinctly tubular with a "
 "hollow at each opening, the front placket curves over the chest, and the hem flares with a "
 "natural drape. Clear self-shadowing separates the sleeves from the body, and a soft rim-light "
 "along the shoulders keeps the black fabric readable rather than flat."
)

NEG = (" Nothing pink, nothing cream-coloured as the main fabric, no kite, no camera, no books, "
       "no hearts, no dinosaur anywhere in the image.")

SHOTS = {
 "hero": dict(refs=["ref-blk/front.jpg", "ref-blk/collar.jpg"], aspect="1:1", prompt=(
   "Ultra high resolution ghost-mannequin (invisible mannequin) e-commerce product photograph. "
   + PRODUCT + VOLUME +
   " It hovers weightlessly, tilted a few degrees as though caught mid-float in a light breeze. "
   "Soft diffused studio light from the upper left, a faint soft contact shadow far below. Crisp, "
   "tactile, hyper-detailed, professional apparel catalogue photography. Isolated on a pure flat "
   "plain white background, nothing else in frame." + NEG)),

 "clouds": dict(refs=["ref-blk/front.jpg", "ref-blk/collar.jpg"], aspect="1:1", prompt=(
   "A dreamy 3D product render of a child's BLACK linen shirt floating in a pale champagne dawn "
   "sky among rounded puffy white clouds tinted ivory and soft peach. " + PRODUCT + VOLUME +
   " It drifts weightlessly with a gentle tilt, sleeves lifted by the breeze. A small toy rocket "
   "and one tiny ringed planet drift nearby among the clouds. Warm low dawn light from the upper "
   "left, strong rim-light along the shoulders, gentle ivory ambient bounce from the clouds "
   "below. Calm, adventurous, premium childrenswear brand imagery." + NEG)),

 "detail": dict(refs=["ref-blk/front.jpg", "ref-blk/collar.jpg"], aspect="1:1", prompt=(
   "Extreme close-up macro product photograph of hand embroidery on BLACK linen fabric. A rocket "
   "outlined in fine WHITE dashed running stitch with small red-orange satin-stitch flames at its "
   "base, and a light tan coconut-wood button on the placket nearby. Raking side light reveals "
   "the raised texture of every individual embroidery thread and the weave of the black linen. "
   "Shallow depth of field, tack-sharp on the stitching. Match the reference exactly in colour "
   "and stitch style. Luxury craft photography." + NEG)),

 "folded": dict(refs=["ref-blk/front.jpg", "ref-blk/lifestyle.jpg"], aspect="4:3", prompt=(
   "Elegant flat-lay product photograph, shot straight down. " + PRODUCT +
   " The shirt is neatly folded into a soft rectangle with the embroidered rocket and ringed "
   "planet clearly visible on top, one sleeve softly turned to show the linen weave. It rests on "
   "a warm off-white linen surface beside a small brass compass and a length of natural twine. "
   "Soft natural window light from the left, gentle shadows. Calm, premium, editorial "
   "childrenswear styling." + NEG)),
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
    print("  ->", "OK %d KB" % (os.path.getsize(out) // 1024) if ok else "FAILED")
    return ok

if __name__ == "__main__":
    want = sys.argv[1:] or list(SHOTS)
    good = sum(run(n, SHOTS[n]) for n in want if n in SHOTS)
    print("\n%d/%d generated" % (good, len(want)))

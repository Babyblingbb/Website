#!/usr/bin/env python3
"""3D renders for the baby pink Hearts linen shirt — Cosmic View Vertex.
Refs: ref-pink/. Written out in full rather than patched from a sibling script —
sed/str.replace edits have twice left another shirt's motif in a prompt.

  python gen3d-pink.py [shot ...]
"""
import subprocess, sys, os

SCRIPT = r"C:\Users\Mudit Sharma\.claude\scripts\gen-image.py"
MODEL  = "gemini-3-pro-image"
OUT    = "gen-pink"
os.makedirs(OUT, exist_ok=True)

PRODUCT = (
 "The garment must match the reference photographs EXACTLY: a child's soft mid-PINK linen "
 "short-sleeve shirt with an open Cuban camp collar and five round coconut-wood buttons down the "
 "centre front placket. Embroidered across the front: several OUTLINE HEARTS of varying sizes in "
 "a slightly deeper rose-pink thread, scattered informally over both sides of the front, each a "
 "simple single-line heart outline, not filled. A small square cream woven patch with two tiny "
 "embroidered children sits low on the RIGHT front near the hem. Keep the visible linen weave, "
 "the exact pink colour and every embroidered heart identical to the references in size, count "
 "and placement. Do not add, remove, restyle or reposition any design element. This shirt has "
 "ONLY hearts: there is NO kite, NO camera, NO books, NO coffee cup, NO bicycle and NO cloud "
 "embroidery. No text or watermark beyond the small woven neck label shown."
)

VOLUME = (
 " STRONGLY three-dimensional — unmistakably a filled-out garment, never a flat lay. The chest "
 "and shoulders are rounded and full as if on an invisible child's body, the camp collar is "
 "rolled open so its underside is visible, both short sleeves are distinctly tubular with a dark "
 "hollow at each opening, the front placket curves over the chest, and the hem flares with a "
 "natural drape. Clear self-shadowing separates the sleeves from the body."
)

NEG = " Nothing maroon, nothing blue, no camera, no books, no kite anywhere in the image."

SHOTS = {
 "hero": dict(refs=["ref-pink/front.jpg", "ref-pink/patch.jpg"], aspect="1:1", prompt=(
   "Ultra high resolution ghost-mannequin (invisible mannequin) e-commerce product photograph. "
   + PRODUCT + VOLUME +
   " It hovers weightlessly, tilted a few degrees as though caught mid-float in a light breeze. "
   "Soft diffused studio light from the upper left, a faint soft contact shadow far below. Crisp, "
   "tactile, hyper-detailed, professional apparel catalogue photography. Isolated on a pure flat "
   "plain white background, nothing else in frame." + NEG)),

 "clouds": dict(refs=["ref-pink/front.jpg", "ref-pink/patch.jpg"], aspect="1:1", prompt=(
   "A dreamy 3D product render of a child's SOFT PINK linen shirt floating in a fresh morning sky "
   "among rounded puffy white clouds, the air tinted pale mint and cream. "
   + PRODUCT + VOLUME +
   " It drifts weightlessly with a gentle tilt, sleeves lifted by the breeze. A few small paper "
   "hearts drift nearby among the clouds. Soft morning sunlight from the upper left, gentle "
   "rim-light along the shoulders, pale mint ambient bounce from the clouds below. Fresh, tender, "
   "premium childrenswear brand imagery." + NEG)),

 "detail": dict(refs=["ref-pink/front.jpg", "ref-pink/patch.jpg"], aspect="1:1", prompt=(
   "Extreme close-up macro product photograph of hand embroidery on SOFT PINK linen fabric. Two "
   "outline hearts stitched in a deeper rose-pink thread — simple single-line heart outlines with "
   "the tiny running stitches clearly visible — and a coconut-wood button on the placket nearby. "
   "Raking side light reveals the raised texture of every individual embroidery thread and the "
   "weave of the pink linen. Shallow depth of field, tack-sharp on the stitching. Match the "
   "reference exactly in colour and stitch style. Luxury craft photography." + NEG)),

 "folded": dict(refs=["ref-pink/front.jpg", "ref-pink/lifestyle.jpg"], aspect="4:3", prompt=(
   "Elegant flat-lay product photograph, shot straight down. " + PRODUCT +
   " The shirt is neatly folded into a soft rectangle with the embroidered hearts clearly visible "
   "on top, one sleeve softly turned to show the linen weave. It rests on a warm off-white linen "
   "surface beside a few tiny dried flowers and a length of natural twine. Soft natural window "
   "light from the left, gentle shadows. Calm, premium, editorial childrenswear styling." + NEG)),
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

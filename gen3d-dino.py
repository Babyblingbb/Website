#!/usr/bin/env python3
"""3D renders for the cream Dino linen shirt — Cosmic View Vertex.
Refs: ref-dino/. Written out in full, never patched from a sibling script.

  python gen3d-dino.py [shot ...]
"""
import subprocess, sys, os

SCRIPT = r"C:\Users\Mudit Sharma\.claude\scripts\gen-image.py"
MODEL  = "gemini-3-pro-image"
OUT    = "gen-dino"
os.makedirs(OUT, exist_ok=True)

PRODUCT = (
 "The garment must match the reference photographs EXACTLY: a child's CREAM / oatmeal natural "
 "linen short-sleeve shirt with an open Cuban camp collar and five round coconut-wood buttons "
 "down the centre front placket. A whole little scene is hand-embroidered across the front in "
 "fine outline stitch: upper LEFT, a pale BLUE outline cloud with a small YELLOW sun beside it; "
 "on the RIGHT, a long-necked brontosaurus dinosaur outlined in BLUE with small YELLOW spots "
 "along its body; lower LEFT, a yellow-green fern plant; a tiny yellow snail near the hem; and a "
 "small yellow star. A small square cream woven patch with two tiny embroidered children sits low "
 "on the front. Keep the visible slubby linen weave, the exact cream colour and every embroidered "
 "element identical to the references in colour, size and placement. Do not add, remove, restyle "
 "or reposition any design element. This shirt has ONLY that dinosaur scene: there is NO kite, NO "
 "camera, NO books, NO hearts and NO bicycle. No text or watermark beyond the small woven neck "
 "label shown."
)

VOLUME = (
 " STRONGLY three-dimensional — unmistakably a filled-out garment, never a flat lay. The chest "
 "and shoulders are rounded and full as if on an invisible child's body, the camp collar is "
 "rolled open so its underside is visible, both short sleeves are distinctly tubular with a dark "
 "hollow at each opening, the front placket curves over the chest, and the hem flares with a "
 "natural drape. Clear self-shadowing separates the sleeves from the body."
)

NEG = (" Nothing pink, nothing maroon, no kite, no camera, no books, no hearts anywhere in the "
       "image. The fabric stays cream, never white and never beige-grey.")

SHOTS = {
 "hero": dict(refs=["ref-dino/front.jpg", "ref-dino/collar.jpg"], aspect="1:1", prompt=(
   "Ultra high resolution ghost-mannequin (invisible mannequin) e-commerce product photograph. "
   + PRODUCT + VOLUME +
   " It hovers weightlessly, tilted a few degrees as though caught mid-float in a light breeze. "
   "Soft diffused studio light from the upper left, a faint soft contact shadow far below. Crisp, "
   "tactile, hyper-detailed, professional apparel catalogue photography. Isolated on a pure flat "
   "plain white background, nothing else in frame." + NEG)),

 "clouds": dict(refs=["ref-dino/front.jpg", "ref-dino/collar.jpg"], aspect="1:1", prompt=(
   "A dreamy 3D product render of a child's CREAM linen shirt floating in a lush tropical sky — "
   "deep teal above, softening to jade and warm sand near the horizon — among rounded puffy "
   "clouds tinted cream and pale gold. " + PRODUCT + VOLUME +
   " It drifts weightlessly with a gentle tilt, sleeves lifted by the breeze. A few oversized "
   "green fern fronds and one small friendly cartoon dinosaur drift nearby among the clouds. Warm "
   "sunlight from the upper left, soft rim-light along the shoulders, gentle jade ambient bounce "
   "from below. Playful, adventurous, premium childrenswear brand imagery." + NEG)),

 "detail": dict(refs=["ref-dino/front.jpg", "ref-dino/collar.jpg"], aspect="1:1", prompt=(
   "Extreme close-up macro product photograph of hand embroidery on CREAM / oatmeal linen fabric. "
   "The long neck and spotted back of a brontosaurus outlined in fine BLUE thread with small "
   "YELLOW satin-stitch spots, and a coconut-wood button on the placket nearby. Raking side light "
   "reveals the raised texture of every individual embroidery thread and the slubby weave of the "
   "cream linen. Shallow depth of field, tack-sharp on the stitching. Match the reference exactly "
   "in colour and stitch style. Luxury craft photography." + NEG)),

 "folded": dict(refs=["ref-dino/front.jpg", "ref-dino/lifestyle.jpg"], aspect="4:3", prompt=(
   "Elegant flat-lay product photograph, shot straight down. " + PRODUCT +
   " The shirt is neatly folded into a soft rectangle with the embroidered dinosaur and cloud "
   "clearly visible on top, one sleeve softly turned to show the linen weave. It rests on a warm "
   "off-white linen surface beside a couple of small green fern fronds and a length of natural "
   "twine. Soft natural window light from the left, gentle shadows. Calm, premium, editorial "
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

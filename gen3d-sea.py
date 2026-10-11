#!/usr/bin/env python3
"""3D renders for the pale sage Garden linen shirt — Cosmic View Vertex.
Refs: ref-sea/. Written out in full, never patched from a sibling script.

  python gen3d-sea.py [shot ...]
"""
import subprocess, sys, os

SCRIPT = r"C:\Users\Mudit Sharma\.claude\scripts\gen-image.py"
MODEL  = "gemini-3-pro-image"
OUT    = "gen-sea"
os.makedirs(OUT, exist_ok=True)

PRODUCT = (
 "The garment must match the reference photographs EXACTLY: a child's very pale SAGE / oatmeal "
 "linen short-sleeve shirt with an open Cuban camp collar and five round coconut-wood buttons "
 "down the centre front placket. Embroidered on the front in fine DARK GREEN outline stitch: on "
 "the LEFT side, a potted houseplant with tall broad banana-like leaves rising from a small "
 "speckled pot; at the upper RIGHT, a watering can seen from the side with a daisy flower motif "
 "on its body and a long spout. A small square cream woven patch with two tiny embroidered "
 "children sits low on the RIGHT front. Keep the visible slubby linen weave, the exact pale sage "
 "colour and every dark green outline stitch identical to the references in size and placement. "
 "Do not add, remove, restyle or reposition any design element. This shirt has ONLY that garden "
 "scene: there is NO kite, NO camera, NO rocket, NO hearts, NO dinosaur and NO cartoon character. "
 "No text or watermark beyond the small woven neck label shown."
)

VOLUME = (
 " STRONGLY three-dimensional — unmistakably a filled-out garment, never a flat lay. The chest "
 "and shoulders are rounded and full as if on an invisible child's body, the camp collar is "
 "rolled open so its underside is visible, both short sleeves are distinctly tubular with a dark "
 "hollow at each opening, the front placket curves over the chest, and the hem flares with a "
 "natural drape. Clear self-shadowing separates the sleeves from the body."
)

NEG = (" Nothing pink, nothing black, no kite, no camera, no rocket, no hearts, no dinosaur "
       "anywhere in the image.")

SHOTS = {
 "hero": dict(refs=["ref-sea/front.jpg", "ref-sea/macro.jpg"], aspect="1:1", prompt=(
   "Ultra high resolution ghost-mannequin (invisible mannequin) e-commerce product photograph. "
   + PRODUCT + VOLUME +
   " It hovers weightlessly, tilted a few degrees as though caught mid-float in a light breeze. "
   "Soft diffused studio light from the upper left, a faint soft contact shadow far below. Crisp, "
   "tactile, hyper-detailed, professional apparel catalogue photography. Isolated on a pure flat "
   "plain white background, nothing else in frame." + NEG)),

 "clouds": dict(refs=["ref-sea/front.jpg", "ref-sea/macro.jpg"], aspect="1:1", prompt=(
   "A dreamy 3D product render of a child's pale SAGE linen shirt floating in a warm terracotta "
   "evening sky among rounded puffy clouds tinted clay, apricot and soft rose. " + PRODUCT + VOLUME +
   " It drifts weightlessly with a gentle tilt, sleeves lifted by the breeze. A small terracotta "
   "plant pot and one green watering can drift nearby among the clouds. Warm low sunlight from "
   "the upper left, soft rim-light along the shoulders, gentle clay ambient bounce from the "
   "clouds below. Calm, botanical, premium childrenswear brand imagery." + NEG)),

 "detail": dict(refs=["ref-sea/macro.jpg", "ref-sea/front.jpg"], aspect="1:1", prompt=(
   "Extreme close-up macro product photograph of hand embroidery on very pale SAGE linen fabric. "
   "The tall broad leaves of a potted houseplant outlined in fine DARK GREEN thread, with the "
   "speckled pot below, and a coconut-wood button on the placket nearby. Raking side light "
   "reveals the raised texture of every individual embroidery thread and the slubby weave of the "
   "sage linen. Shallow depth of field, tack-sharp on the stitching. Match the reference exactly "
   "in colour and stitch style. Luxury craft photography." + NEG)),

 "folded": dict(refs=["ref-sea/front.jpg", "ref-sea/lifestyle.jpg"], aspect="4:3", prompt=(
   "Elegant flat-lay product photograph, shot straight down. " + PRODUCT +
   " The shirt is neatly folded into a soft rectangle with the embroidered plant and watering can "
   "clearly visible on top, one sleeve softly turned to show the linen weave. It rests on a warm "
   "off-white linen surface beside a tiny terracotta pot and a length of natural twine. Soft "
   "natural window light from the left, gentle shadows. Calm, premium, editorial childrenswear "
   "styling." + NEG)),
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

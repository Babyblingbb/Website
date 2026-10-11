#!/usr/bin/env python3
"""3D renders for the maroon Storytelling linen shirt — Cosmic View Vertex.
Refs are the real Shopify product photos in ref-story/.

  python gen3d-story.py            # all shots
  python gen3d-story.py hero
"""
import subprocess, sys, os

SCRIPT = r"C:\Users\Mudit Sharma\.claude\scripts\gen-image.py"   # Cosmic View, own credits
MODEL  = "gemini-3-pro-image"                                     # no -preview on this project
OUT    = "gen-story"
os.makedirs(OUT, exist_ok=True)

PRODUCT = (
 "The garment must match the reference photographs EXACTLY: a child's deep maroon / burgundy "
 "LINEN short-sleeve shirt with an open Cuban camp collar and five round coconut-wood buttons "
 "down the centre front placket. Embroidered on the front in fine CREAM / off-white outline "
 "stitch: a vintage film camera on the LEFT side of the front as the viewer sees it, and on the "
 "RIGHT side a stack of three books with a steaming cup of coffee resting on top and small curls "
 "of steam. A small square cream woven patch with two tiny embroidered children sits low on the "
 "LEFT front near the hem. Keep the visible slubby linen weave, the exact deep maroon colour and "
 "every cream outline stitch identical to the references. Do not add, remove, restyle or "
 "reposition any design element. There is NO kite and NO cloud embroidery on this shirt. No text "
 "or watermark beyond the small woven neck label shown."
)

VOLUME = (
 " STRONGLY three-dimensional — unmistakably a filled-out garment, never a flat lay. The chest "
 "and shoulders are rounded and full as if on an invisible child's body, the camp collar is "
 "rolled open so its underside is visible, both short sleeves are distinctly tubular with a dark "
 "hollow at each opening, the front placket curves over the chest, and the hem flares with a "
 "natural drape. Clear self-shadowing separates the sleeves from the body."
)

SHOTS = {
 "hero": dict(refs=["ref-story/front.jpg", "ref-story/collar.jpg"], aspect="1:1", prompt=(
   "Ultra high resolution ghost-mannequin (invisible mannequin) e-commerce product photograph. "
   + PRODUCT + VOLUME +
   " It hovers weightlessly, tilted a few degrees as though caught mid-float in a light breeze. "
   "Soft diffused studio light from the upper left, a faint soft contact shadow far below. Crisp, "
   "tactile, hyper-detailed, professional apparel catalogue photography. Isolated on a pure flat "
   "plain white background, nothing else in frame.")),

 "clouds": dict(refs=["ref-story/front.jpg", "ref-story/collar.jpg"], aspect="1:1", prompt=(
   "A dreamy 3D product render of a child's deep maroon linen shirt floating in a soft TWILIGHT "
   "sky among rounded puffy clouds tinted lavender, dusty rose and warm cream by the setting sun. "
   + PRODUCT + VOLUME +
   " It drifts weightlessly with a gentle tilt, sleeves lifted by the breeze. An open storybook "
   "and a small vintage camera drift nearby among the clouds. Warm low sunlight from the upper "
   "left, soft rim-light along the shoulders, gentle lavender ambient bounce from the clouds "
   "below. Calm, story-time, premium childrenswear brand imagery. There must be no kite anywhere "
   "in the image.")),

 "detail": dict(refs=["ref-story/front.jpg", "ref-story/collar.jpg"], aspect="1:1", prompt=(
   "Extreme close-up macro product photograph of hand embroidery on DEEP MAROON / burgundy linen "
   "fabric. A vintage film camera outlined in fine CREAM thread, and beside it a stack of books "
   "with a steaming coffee cup on top, all in delicate cream outline stitch. A coconut-wood "
   "button sits on the placket. Raking side light reveals the raised texture of every individual "
   "embroidery thread and the slubby weave of the maroon linen. Shallow depth of field, tack-sharp "
   "on the embroidery. Match the reference exactly in colour, stitch style and layout. Luxury "
   "craft photography. No kite, no clouds, no blue fabric, no text or watermark.")),

 "folded": dict(refs=["ref-story/front.jpg", "ref-story/lifestyle.jpg"], aspect="4:3", prompt=(
   "Elegant flat-lay product photograph, shot straight down. " + PRODUCT +
   " The shirt is neatly folded into a soft rectangle with the embroidered camera and stacked "
   "books clearly visible on top, one sleeve softly turned to show the linen weave. It rests on a "
   "warm off-white linen surface beside a small stack of worn hardback books and a length of "
   "natural twine. Soft natural window light from the left, gentle shadows. Calm, premium, "
   "editorial childrenswear styling.")),
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

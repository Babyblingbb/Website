"""Re-render shirts in the exact pose of the Balloon Bicycle hero (the house style).
usage: python gen-pose.py story pink"""
import importlib.util, subprocess, os, sys
from cutout import cutout
POSE_REF = "gen/hero.png"        # Balloon Bicycle ghost-mannequin = the house pose
JOBS = {"story": ("gen3d-story.py", ["ref-story/front.jpg","ref-story/collar.jpg"], "assets-story/bs-grid"),
        "pink":  ("gen3d-pink.py",  ["gen-pink/hero.png","ref-pink/patch.jpg"],    "assets-pink/bp-grid"),
        "dino":  ("gen3d-dino.py",  ["gen-dino/hero.png","ref-dino/collar.jpg"],  "assets-dino/bd-grid"),
        "blk":   ("gen3d-blk.py",   ["ref-blk/front.jpg","ref-blk/collar.jpg"],    "assets-blk/bl-grid"),
        "shin":  ("gen3d-shin.py",  ["ref-shin/front.jpg","ref-shin/macro.jpg"],  "assets-shin/bn-grid"),
        "beach": ("gen3d-beach.py", ["ref-beach/3.jpg","assets-beach/bw-d-waves.webp"], "assets-beach/bw-shirt"),
        "beige": ("gen3d-beige.py", ["ref-beige/3.jpg","ref-beige/1.jpg"], "assets-beige/bc-shirt"),
        "white": ("gen3d-white.py", ["ref-white/3.jpg","ref-white/0.jpg"], "assets-white/bf-shirt"),
        "sea":   ("gen3d-sea.py",   ["gen-sea/hero.png","ref-sea/macro.jpg"],     "assets-sea/bg-grid")}
HOW = ("IMAGE 1 IS A POSE AND STYLE REFERENCE ONLY — a different shirt. Copy from it EXACTLY: the camera "
       "angle, the slight three-quarter turn of the body, the angle and fullness of both sleeves, the open "
       "rolled camp collar, the ghost-mannequin volume, the gentle float and tilt, the soft studio lighting, "
       "the framing and the faint contact shadow. The garment must have the SAME PROPORTIONS as image 1: slightly taller than wide, full body length down to the hem, sleeves angled down and forward at the same angle, never boxy, never cropped short, never flat. Do NOT copy its colour, fabric colour, embroidery, balloons "
       "or bicycle. IMAGES 2 AND 3 ARE THE ACTUAL GARMENT: copy its colour, fabric and every embroidered "
       "element exactly from them. ")
for key in sys.argv[1:]:
    mod, refs, out = JOBS[key]
    spec = importlib.util.spec_from_file_location("m", mod); m = importlib.util.module_from_spec(spec)
    sys.argv = ["x"]; spec.loader.exec_module(m)
    prompt = (HOW + "Ultra high resolution ghost-mannequin e-commerce product photograph. " + m.PRODUCT +
              " Pure flat plain white background, nothing else in frame. No balloons, no bicycle." + getattr(m, "NEG", ""))
    png = out + ".png"
    subprocess.run(["python", m.SCRIPT, prompt, png, "--ref", POSE_REF] + refs +
                   ["--model", m.MODEL, "--aspect", "1:1"], capture_output=True)
    if not os.path.exists(png): print("FAILED", key); continue
    WHITE = lambda r,g,b: min(r,g,b) >= 251 and (max(r,g,b)-min(r,g,b)) <= 3
    c = (cutout(png, bg_test=WHITE, erode=5) if key in ("dino","sea","shin","beach","beige","white") else cutout(png)); c.save(out + ".webp", "WEBP", quality=88, method=6)
    print("ok", key, c.size)

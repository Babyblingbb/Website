import importlib.util, subprocess, os, sys
from cutout import cutout
POSE=(" CAMERA: perfectly straight-on front view at chest height, shirt upright, perfectly symmetrical,"
      " ZERO tilt, ZERO rotation, ZERO three-quarter turn, both sleeves level and equal, hem horizontal,"
      " centred in frame. Ghost-mannequin volume. Pure flat plain white background, nothing else in frame.")
JOBS=[("gen3d-story.py","ref-story/front.jpg","ref-story/collar.jpg","assets-story/bs-grid.webp"),
      ("gen3d-sea.py","ref-sea/front.jpg","ref-sea/macro.jpg","assets-sea/bg-grid.webp")]
WHITE=lambda r,g,b: min(r,g,b)>=251 and (max(r,g,b)-min(r,g,b))<=3
for mod,r1,r2,out in JOBS:
    spec=importlib.util.spec_from_file_location("m",mod); m=importlib.util.module_from_spec(spec)
    sys.argv=["x"]; spec.loader.exec_module(m)
    png=out.replace(".webp",".png")
    p=("Ultra high resolution e-commerce ghost-mannequin product photograph. "+m.PRODUCT+POSE+getattr(m,"NEG",""))
    subprocess.run(["python",m.SCRIPT,p,png,"--ref",r1,r2,"--model",m.MODEL,"--aspect","1:1"],capture_output=True)
    if not os.path.exists(png): print("FAILED",out); continue
    c=cutout(png,bg_test=WHITE,erode=5); c.save(out,"WEBP",quality=88,method=6); print("ok",out,c.size)

"""Homepage renders -> assets-home/*.png"""
import subprocess, os, time, sys
G="C:/Users/Mudit Sharma/.claude/scripts/gen-image.py"
ST="Luxury editorial documentary photograph, warm soft natural light, shallow depth of field, calm, premium, muted natural palette with soft pastel sky tones. No text, no logos, no watermarks."
J={
"hero":("Three small children's short-sleeve linen shirts floating weightlessly in a bright pastel blue sky among soft white fluffy clouds, arranged in a gentle staggered trio (centre one slightly larger and in front), each shirt EXACTLY matching its reference image in colour, print, embroidery, collar and coconut buttons — reproduce each garment faithfully. Ghost-mannequin 3D shape, soft realistic shadows, dreamy, magical, premium kidswear campaign. Keep the top-left third of the frame as open sky for headline text. No people, no text.","16:9",["assets-grid/g-bb.webp","assets-grid/g-bk.webp","assets-grid/g-bp.webp"]),
"p1":("Close-up of hands gently gathering freshly harvested golden flax stalks in a sunlit flax field at golden hour, pale blue flax flowers softly blurred in the background. "+ST,"4:5",[]),
"p2":("Close-up of an artisan's hands spinning fine natural linen-cotton yarn on a wooden spinning wheel, soft ivory thread glowing in window backlight, fibres floating in the light. "+ST,"4:5",[]),
"p3":("Close-up of a traditional wooden handloom weaving very fine, delicate, feather-light ivory linen-cotton fabric; hundreds of thin taut warp threads, the shuttle mid-pass, soft backlight glowing through the thin woven cloth. Fine and soft, not coarse, not burlap. "+ST,"4:5",[]),
"p4":("Top-down close-up of an artisan's hands with a needle mid-stitch, hand-embroidering a CLEARLY VISIBLE, half-finished red and blue balloon motif in thick cotton thread (satin stitch, colourful and crisp) with fine cotton thread onto a soft pastel peach children's linen shirt held in a wooden embroidery hoop, coconut shell buttons nearby on the table. "+ST,"4:5",[]),
}
for k in sys.argv[1:] or J:
    p,a,refs=J[k]; out=f"assets-home/{k}.png"
    for t in range(4):
        if os.path.exists(out): break
        cmd=["python",G,p,out,"--aspect",a,"--model","gemini-3-pro-image"]+(["--ref",*refs] if refs else [])
        r=subprocess.run(cmd,capture_output=True,text=True)
        if not os.path.exists(out): print(r.stderr[-300:],flush=True); time.sleep(25*(t+1))
    print(("ok  " if os.path.exists(out) else "FAIL")+" "+out,flush=True)

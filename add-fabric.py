#!/usr/bin/env python3
"""index.html -> index-peach.html with the two fabric sections (feather test + weave lens).
Kept out of the shared base on purpose: the images are peach-specific, so other pages
only get this once they have their own fabric renders.
  python add-fabric.py [src] [out] [asset-dir] [fabric-colour-word]
"""
import io, sys
SRC = sys.argv[1] if len(sys.argv) > 1 else "index.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "index-peach.html"
AD  = sys.argv[3] if len(sys.argv) > 3 else "assets"
COL = sys.argv[4] if len(sys.argv) > 4 else "peach"
PX  = sys.argv[5] if len(sys.argv) > 5 else ""
s = io.open(SRC, encoding="utf-8").read()

def rep(a, b, why):
    global s
    assert a in s, "MISSING: " + why
    s = s.replace(a, b, 1)

CSS = """
/* ══════════════════════════ FABRIC: FEATHER + WEAVE LENS ══════════════════════════ */
.feather-sec{padding-block:clamp(20px,5vw,60px)}
.feather{position:relative;margin:0;border-radius:var(--r-xl);overflow:hidden;box-shadow:var(--shadow-l);aspect-ratio:16/9}
.feather-img{position:absolute;left:0;top:-8%;width:100%;height:116%;object-fit:cover;object-position:62% 50%;will-change:transform}
.feather::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(90deg,rgba(255,255,255,.62) 0%,rgba(255,255,255,.22) 34%,rgba(255,255,255,0) 52%)}
.feather-copy{position:absolute;z-index:2;left:clamp(22px,5vw,64px);top:50%;translate:0 -50%;max-width:min(420px,78%)}
.feather-copy h2{font-size:clamp(2rem,5.6vw,3.4rem);margin-top:8px}
.feather-copy .fc-body{margin-top:12px;color:var(--ink-2);font-size:clamp(.92rem,1vw + .7rem,1.05rem)}
.fc-stats{display:flex;gap:10px;margin-top:16px;flex-wrap:wrap}
.fc-stats span{background:rgba(255,255,255,.85);backdrop-filter:blur(8px);border-radius:999px;padding:7px 13px;
  font-size:.78rem;font-weight:600;box-shadow:var(--shadow-s)}
@media(max-width:700px){
  .feather{aspect-ratio:4/5}
  .feather-img{object-position:92% 60%}
  .feather::after{background:linear-gradient(180deg,rgba(255,255,255,.78) 0%,rgba(255,255,255,.5) 30%,rgba(255,255,255,0) 50%)}
  .feather-copy{top:24px;left:20px;right:20px;translate:none;max-width:none}
}
.weave{position:relative;border-radius:var(--r-xl);overflow:hidden;box-shadow:var(--shadow-l);aspect-ratio:16/9;
  touch-action:none;cursor:crosshair;-webkit-user-select:none;user-select:none}
.weave img{width:100%;height:100%;object-fit:cover;display:block;pointer-events:none}
.lens{position:absolute;left:62%;top:50%;width:clamp(118px,24vw,230px);aspect-ratio:1;border-radius:50%;
  translate:-50% -50%;pointer-events:none;background-repeat:no-repeat;z-index:4;
  box-shadow:0 0 0 3px rgba(255,255,255,.96),0 20px 44px -12px rgba(20,40,70,.6),inset 0 0 24px rgba(0,0,0,.14)}
.lens::after{content:"";position:absolute;inset:0;border-radius:50%;
  background:radial-gradient(circle at 32% 28%,rgba(255,255,255,.35),rgba(255,255,255,0) 42%)}
.wtag{position:absolute;z-index:3;background:rgba(255,255,255,.9);backdrop-filter:blur(8px);border-radius:999px;
  padding:7px 13px;font-size:.78rem;font-weight:600;color:var(--ink);box-shadow:var(--shadow-s);pointer-events:none}
.wtag.t1{left:4%;top:7%}.wtag.t2{right:4%;bottom:8%}.wtag.t3{left:4%;bottom:8%}
.weave-hint{text-align:center;margin-top:12px;font-size:.84rem;color:var(--ink-2)}

/* ── where it comes from: swipeable floating plants ── */
.origin-row{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(12px,3vw,40px);margin-top:clamp(18px,3vw,32px)}
.origin{text-align:center;display:flex;flex-direction:column;align-items:center}
.origin-img{position:relative;width:100%;aspect-ratio:1/1;display:grid;place-items:center}
.origin-img img{max-width:96%;max-height:96%;object-fit:contain;animation:floaty 8s ease-in-out infinite;
  filter:drop-shadow(0 22px 20px rgba(20,70,110,.20))}
.origin:nth-child(2) .origin-img img{animation-delay:-2.6s}.origin:nth-child(3) .origin-img img{animation-delay:-5.1s}
.origin-img .gr{position:absolute;left:50%;bottom:3%;width:46%;height:16px;translate:-50% 0;border-radius:50%;
  background:radial-gradient(ellipse,rgba(20,70,110,.22),rgba(20,70,110,0) 70%);filter:blur(6px)}
.origin h3{margin-top:10px;font-size:1.12rem}
.origin h3 span{color:var(--ink-3);font-weight:500}
.origin p{margin-top:6px;font-size:.9rem;color:var(--ink-2);max-width:30ch}
.origin-dots{display:none}
@media(max-width:760px){
  .origin-row{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:10px;
    margin-inline:calc(-1 * var(--pad));padding:4px var(--pad) 6px;scrollbar-width:none;-webkit-overflow-scrolling:touch}
  .origin-row::-webkit-scrollbar{display:none}
  .origin{flex:0 0 78%;scroll-snap-align:center}
  .origin-dots{display:flex;justify-content:center;gap:7px;margin-top:10px}
  .origin-dots i{width:7px;height:7px;border-radius:50%;background:rgba(14,47,76,.2);transition:.25s}
  .origin-dots i.on{width:20px;border-radius:4px;background:var(--ink)}
}

@media(max-width:700px){.weave{aspect-ratio:4/3}.wtag{font-size:.72rem;padding:6px 11px}}
"""

HTML = """<!-- ══════════════ FABRIC: FEATHER TEST ══════════════ -->
<section class="feather-sec">
  <div class="wrap">
    <figure class="feather rev">
      <img class="feather-img" src="%(ad)s/%(p)sfabric-feather.webp" width="1800" height="1005" loading="lazy"
           alt="A billowing piece of %(col)s linen drifting beside a white feather">
      <figcaption class="feather-copy">
        <p class="eyebrow">The feather test</p>
        <h2>Lighter than<br>it looks.</h2>
        <p class="fc-body">Fine linen-cotton, woven thin on purpose. It drifts, it breathes, and they forget it's on.</p>
        <div class="fc-stats"><span>🪶 120 GSM</span><span>🌬️ Open weave</span><span>☁️ Pre-washed soft</span></div>
      </figcaption>
    </figure>
  </div>
</section>

<!-- ══════════════ FABRIC: WEAVE LENS ══════════════ -->
<section class="sec" style="padding-top:clamp(28px,5vw,64px)">
  <div class="wrap">
    <div class="sec-head rev"><p class="eyebrow">The blend</p><h2>Linen × Cotton.</h2>
      <p>Linen for the breeze, cotton for the softness — blended so it breathes like linen and feels like their softest tee.</p></div>
    <div class="weave rev" id="weaveBox">
      <img src="%(ad)s/%(p)sfabric-weave.webp" width="2000" height="1116" loading="lazy" alt="Macro of the %(col)s linen weave">
      <div class="lens" id="lens" aria-hidden="true"></div>
      <span class="wtag t1">🌿 Linen · airy &amp; cool</span><span class="wtag t2">☁️ Cotton · soft on skin</span><span class="wtag t3">🤲 Blend · no itch</span>
    </div>
    <p class="weave-hint">Drag across the fabric to look closer</p>
    <p class="eyebrow" style="text-align:center;margin-top:clamp(40px,7vw,80px)">Where it comes from</p>
    <div class="origin-row" id="originRow">
      <div class="origin"><div class="origin-img"><img src="%(ad)s/%(p)sflax.webp" alt="Flax plant with blue flowers" loading="lazy"><span class="gr"></span></div>
        <h3>Flax <span>→ linen</span></h3><p>Long, hollow fibres that let air straight through. The cool part.</p></div>
      <div class="origin"><div class="origin-img"><img src="%(ad)s/%(p)scotton.webp" alt="Open cotton bolls on a stem" loading="lazy"><span class="gr"></span></div>
        <h3>Cotton <span>→ softness</span></h3><p>Fluffy, gentle fibres that sit kindly on sensitive little skin.</p></div>
      <div class="origin"><div class="origin-img"><img src="%(ad)s/%(p)sswatch.webp" alt="A feather-light piece of the linen-cotton blend" loading="lazy"><span class="gr"></span></div>
        <h3>Together <span>→ the blend</span></h3><p>Woven, then pre-washed — breathes like linen, feels like cotton from day one.</p></div>
    </div>
    <div class="origin-dots" id="originDots"><i class="on"></i><i></i><i></i></div>
  </div>
</section>

""" % {"ad": AD, "col": COL, "p": PX}

JS = """/* ═══════════ origin swipe dots ═══════════ */
(function(){ var row=document.getElementById('originRow'), dots=document.querySelectorAll('#originDots i');
  if(!row||!dots.length) return;
  row.addEventListener('scroll',function(){ var kids=row.children, c=row.scrollLeft+row.clientWidth/2, best=0, bd=1e9;
    for(var i=0;i<kids.length;i++){ var k=kids[i], m=k.offsetLeft+k.offsetWidth/2, d=Math.abs(m-c); if(d<bd){bd=d;best=i;} }
    dots.forEach(function(d,i){ d.classList.toggle('on',i===best); }); },{passive:true});
})();

/* ═══════════ fabric: feather parallax + weave lens ═══════════ */
(function(){
  var fb=document.querySelector('.feather'), fi=document.querySelector('.feather-img');
  if(fb && fi && !reduce){
    var tick=false;
    addEventListener('scroll',function(){ if(tick) return; tick=true; requestAnimationFrame(function(){
      tick=false; var r=fb.getBoundingClientRect(); if(r.bottom<0||r.top>innerHeight) return;
      var p=(r.top+r.height/2-innerHeight/2)/innerHeight;
      fi.style.transform='translate3d(0,'+(p*-7).toFixed(2)+'%,0)'; }); },{passive:true});
  }
  var box=document.getElementById('weaveBox'), lens=document.getElementById('lens');
  if(!box||!lens) return;
  var img=box.querySelector('img'), Z=2.6, set=false;
  function geo(){ var r=box.getBoundingClientRect(), iw=img.naturalWidth||2000, ih=img.naturalHeight||1116;
    var k=Math.max(r.width/iw, r.height/ih); return {r:r, w:iw*k, h:ih*k, ox:(r.width-iw*k)/2, oy:(r.height-ih*k)/2}; }
  function place(cx,cy){
    var g=geo(), x=Math.max(0,Math.min(g.r.width,cx-g.r.left)), y=Math.max(0,Math.min(g.r.height,cy-g.r.top));
    if(!set){ lens.style.backgroundImage='url("'+(img.currentSrc||img.src)+'")'; set=true; }
    var L=lens.offsetWidth;
    lens.style.left=x+'px'; lens.style.top=y+'px';
    lens.style.backgroundSize=(g.w*Z)+'px '+(g.h*Z)+'px';
    lens.style.backgroundPosition=(-((x-g.ox)*Z-L/2))+'px '+(-((y-g.oy)*Z-L/2))+'px';
  }
  function centre(){ var r=box.getBoundingClientRect(); place(r.left+r.width*.62, r.top+r.height*.5); }
  box.addEventListener('pointermove',function(e){ place(e.clientX,e.clientY); });
  box.addEventListener('pointerdown',function(e){ place(e.clientX,e.clientY); });
  box.addEventListener('pointerleave',function(e){ if(e.pointerType==='mouse') centre(); });
  addEventListener('resize',centre,{passive:true});
  if(img.complete && img.naturalWidth) centre(); else img.addEventListener('load',centre);
  new IntersectionObserver(function(en){ en.forEach(function(e){ if(e.isIntersecting) centre(); }); }).observe(box);
})();

"""

rep("/* ══════════════════════════ STICKY BUY BAR", CSS + "\n/* ══════════════════════════ STICKY BUY BAR", "css anchor")
rep("<!-- ══════════════ DETAILS ══════════════ -->", HTML + "<!-- ══════════════ DETAILS ══════════════ -->", "html anchor")
rep("/* ═══════════ reveal ═══════════ */", JS + "/* ═══════════ reveal ═══════════ */", "js anchor")
io.open(OUT, "w", encoding="utf-8").write(s)
print("%s written" % OUT)

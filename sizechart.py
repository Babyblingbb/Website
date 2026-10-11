"""Size-chart popup (from Downloads/BB size chart.png). Opens from any 'Size guide' link / [data-sc]."""
import re

SIZES = ["4–5 Y", "5–6 Y", "6–7 Y", "7–8 Y", "8–9 Y", "9–10 Y"]
ROWS = [("Chest / Bust",   ["36", "38", "39", "41", "42", "45"]),
        ("Shoulder Width", ["32", "34", "35", "37", "38", "41"]),
        ("Sleeve Length",  ["13.5", "14.5", "15.5", "16.5", "17.5", "18.5"]),
        ("Neck Width",     ["15", "16", "16.5", "17.5", "18", "19"]),
        ("Hem / Bottom",   ["38", "40", "41", "43", "44", "47"]),
        ("Shirt Length",   ["44", "46.5", "49", "51.5", "54", "56.5"])]

head = "".join(f"<th>{s}</th>" for s in SIZES)
body = "".join(f"<tr><td>{n}</td>" + "".join(f"<td>{v}</td>" for v in vals) + "</tr>" for n, vals in ROWS)

CSS = """<style id="bb-sc">
#scModal{position:fixed;inset:0;z-index:210;display:grid;place-items:center;padding:16px;pointer-events:none}
#scModal .scr{position:absolute;inset:0;background:rgba(10,30,50,.45);opacity:0;transition:opacity .25s}
#scModal .box{position:relative;width:min(760px,100%);max-height:calc(100vh - 32px);overflow:auto;background:#F7F3EC;border-radius:24px;
  padding:22px 18px 18px;box-shadow:0 30px 80px rgba(10,30,50,.35);transform:translateY(16px) scale(.98);opacity:0;transition:transform .3s cubic-bezier(.22,1,.36,1),opacity .25s}
#scModal.on{pointer-events:auto}#scModal.on .scr{opacity:1}#scModal.on .box{transform:none;opacity:1}
#scModal .x{position:absolute;top:12px;right:12px;width:36px;height:36px;border:0;border-radius:50%;background:#E8E0D5;color:#333;font-size:1rem;cursor:pointer}
#scModal h3{font-family:'Fredoka';font-size:1.45rem;text-align:center;color:#333;letter-spacing:.01em}
#scModal .sub{text-align:center;color:#6b645b;font-size:.9rem;margin-top:4px}
#scModal .tw{margin-top:16px;overflow-x:auto;border-radius:16px;border:1px solid #DDD5CA;background:#fff}
#scModal table{border-collapse:collapse;width:100%;min-width:520px;font-size:.88rem;text-align:center}
#scModal th{background:#4B4F48;color:#fff;font-weight:600;padding:11px 8px;white-space:nowrap}
#scModal td{padding:11px 8px;color:#333;border-top:1px solid #EDE6DC}
#scModal tr:nth-child(even) td{background:#F1ECE5}
#scModal th:first-child,#scModal td:first-child{text-align:left;position:sticky;left:0;z-index:1;white-space:nowrap;padding-left:12px}
#scModal td:first-child{background:#fff;font-weight:500}#scModal tr:nth-child(even) td:first-child{background:#F1ECE5}
#scModal th:first-child{background:#4B4F48}
#scModal .notes{margin-top:14px;color:#5e574e;font-size:.84rem;line-height:1.55;padding-left:1.1em}
#scModal .notes b{display:block;margin:0 0 4px -1.1em;color:#4B4F48;font-size:.8rem;letter-spacing:.06em}
#scModal .hint{display:none;text-align:center;font-size:.74rem;color:#8a8278;margin-top:6px}
@media(max-width:600px){#scModal .hint{display:block}}
</style>"""

MODAL = f"""<div id="scModal" aria-hidden="true" role="dialog" aria-label="Shirt size chart"><div class="scr" data-scx></div><div class="box">
 <button class="x" data-scx aria-label="Close size chart">✕</button>
 <h3>Shirt size chart</h3><p class="sub">Find the right fit for your little one</p>
 <div class="tw"><table><thead><tr><th>Measurement (cm)</th>{head}</tr></thead><tbody>{body}</tbody></table></div>
 <p class="hint">Swipe the table to see all sizes →</p>
 <ul class="notes"><b>SIZE GUIDE NOTES</b><li>All measurements are in centimetres (cm).</li>
  <li>For the best fit, compare these measurements with a shirt that fits your child well.</li>
  <li>If your child is between sizes, consider sizing up for a more relaxed fit.</li></ul>
</div></div>
<script>(function(){{var m=document.getElementById('scModal');if(!m)return;
function t(o){{m.classList.toggle('on',o);m.setAttribute('aria-hidden',!o);document.body.style.overflow=o?'hidden':'';}}
document.addEventListener('click',function(e){{var a=e.target.closest('[data-sc],a[href="/pages/size-guide"],a[href="#size-chart"]');
 if(a){{e.preventDefault();var mm=document.getElementById('mMenu');if(mm&&mm.classList.contains('on'))mm.classList.remove('on');t(true);return;}}
 if(e.target.closest('[data-scx]'))t(false);}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')t(false);}});
if(location.hash==='#size-chart')t(true);}})();</script>
</body>"""

def sc_patch(s):
    s = re.sub(r'<style id="bb-sc">.*?</style>\n', '', s, flags=re.S)
    s = s.replace("</head>", CSS + "\n</head>", 1)
    s = re.sub(r'<div id="scModal".*?</script>\n</body>', lambda m: MODAL, s, flags=re.S)
    if 'id="scModal"' not in s:
        s = s.replace("</body>", MODAL, 1)
    s = s.replace('<a href="#faq">Size guide</a>', '<a href="#size-chart" data-sc>Size guide</a>')
    return s

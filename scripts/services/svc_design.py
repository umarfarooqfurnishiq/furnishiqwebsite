"""Services, Interior Design: every surface, specified.

A finished room beside its material key. Choosing a material (or its numbered marker on the photo)
dims the room and moves a sharp viewfinder frame onto where that material is used. The swatches are
cut from the same photograph (see README), so the key shows the room's actual surfaces.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/services/svc_design.py
"""
import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
IMG = "courtyard-residence-formal-dining-room"
# swatch key, frame on the photo as (left, top, width, height) in % of the image
MATS = [
    ("stone", (0.0, 2.0, 26.0, 80.0)),
    ("walnut", (71.0, 1.0, 28.5, 80.0)),
    ("screen", (32.0, 24.0, 36.5, 38.0)),
    ("boucle", (41.5, 76.0, 18.0, 23.5)),
    ("light", (42.0, 9.0, 16.0, 25.0)),
]
C = {
    "en": dict(
        eyebrow="Our Interior Design Services", h2="Where Inspiration Becomes Your Reality",
        body="At FurnishIQ, we redefine the interior design experience by bridging the gap between high-level architectural vision and livable, bespoke artistry. We believe a space should be more than just aesthetic; it must be a personalized solution that optimizes your daily life or business operations, with every detail — from the flow of a room to the texture of a material — crafted with purpose.",
        key="Every surface, specified", cta="Explore Interior Design", href="/services-interior-design",
        cats=["Stone", "Timber", "Screens", "Textile", "Light"],
        names=["Travertine wall cladding with brass inlay", "Fluted walnut panelling and joinery",
               "Timber mashrabiya screens", "Bouclé upholstered dining chairs", "Linear pendant lighting"],
        alt="Formal dining room with travertine walls, walnut panelling and mashrabiya screens",
        cap="Courtyard Residence · Formal dining room · Concept visualisation", hint="Select a material",
    ),
    "ar": dict(
        eyebrow="خدمات التصميم الداخلي لدينا", h2="حيث يتحول الإلهام إلى واقعك",
        body="في FurnishIQ، نعيد تعريف تجربة التصميم الداخلي بردم الفجوة بين الرؤية المعمارية رفيعة المستوى والحرفية المخصصة القابلة للعيش. نؤمن بأن المساحة يجب أن تكون أكثر من مجرد جمالية؛ يجب أن تكون حلاً شخصياً يُحسّن حياتك اليومية أو عملياتك التجارية، مع صياغة كل تفصيلة — من تدفق الغرفة إلى ملمس المادة — بهدف واضح.",
        key="كل سطح، محدد بعناية", cta="استكشف التصميم الداخلي", href="/ar/services-interior-design",
        cats=["الحجر", "الخشب", "المشربيات", "الأقمشة", "الإضاءة"],
        names=["تكسية جدارية من الترافرتين بتطعيمات نحاسية", "ألواح وأعمال نجارة مضلعة من خشب الجوز",
               "مشربيات خشبية", "كراسي طعام منجدة بقماش البوكليه", "إضاءة معلقة طولية"],
        alt="غرفة طعام رسمية بجدران من الترافرتين وألواح من خشب الجوز ومشربيات",
        cap="منزل الفناء · غرفة الطعام الرسمية · تصور مفاهيمي", hint="اختر مادة",
    ),
}
ARROW_EN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
ARROW_AR = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>'


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    srcset = ", ".join(f"uploads/{IMG}-{w}.webp {w}w" for w in (1280, 1920, 2752))
    items, marks = [], []
    for i, (k, (x, y, w, h)) in enumerate(MATS):
        frame = f'data-f="{x},{y},{w},{h}" data-label="0{i + 1} · {c["cats"][i]}"'
        items.append(f'''        <li><button type="button" class="sd-item" {frame} aria-pressed="false">
          <img class="sd-sw" src="uploads/services-material-swatch-{k}.webp" alt="" width="160" height="160" loading="lazy" decoding="async">
          <span class="sd-txt"><span class="sd-cat"><b>0{i + 1}</b>{c['cats'][i]}</span><span class="sd-name">{c['names'][i]}</span></span>
        </button></li>''')
        marks.append(f'<button type="button" class="sd-mark" style="left:{x + w / 2:.1f}%;top:{y + h / 2:.1f}%;" data-i="{i}" aria-label="{c["cats"][i]}: {c["names"][i]}">0{i + 1}</button>')
    items = "\n".join(items)
    marks = "".join(marks)
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1. INTERIOR DESIGN ━ -->
<section id="interior-design" data-screen-label="Interior Design" data-svc-design{' dir="rtl"' if ar else ''} style="scroll-margin-top:var(--fiq-svc-offset,132px);background:#F5F2ED;color:#3A2D25;position:relative;padding:clamp(64px,8vw,100px) clamp(24px,5vw,80px);overflow:clip;">
  <style>
    [data-svc-design] .sd-wrap{{max-width:1280px;margin:0 auto;}}
    [data-svc-design] .sd-head{{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(32px,5vw,88px);align-items:end;margin-bottom:clamp(40px,4.4vw,64px);}}
    [data-svc-design] .sd-eyebrow{{display:flex;align-items:center;gap:16px;margin-bottom:24px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    [data-svc-design] .sd-eyebrow i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    [data-svc-design] .sd-h2{{font-family:{font};font-weight:500;font-size:clamp(32px,3.8vw,54px);line-height:1.08;letter-spacing:{'0' if ar else '-0.015em'};color:#1F1F1F;margin:0;text-wrap:balance;}}
    [data-svc-design] .sd-body{{font-family:{font};font-size:{'16px' if ar else '15px'};line-height:1.85;color:#5B4636;margin:0;}}
    [data-svc-design] .sd-main{{display:grid;grid-template-columns:minmax(0,8fr) minmax(0,4fr);gap:clamp(28px,3.4vw,48px);align-items:stretch;}}
    [data-svc-design] .sd-fig{{margin:0;margin-inline-start:calc(var(--sd-bleed,0px) * -1);}}
    [data-svc-design] .sd-photo{{position:relative;aspect-ratio:1920/1072;overflow:hidden;background:#3A2D25;}}
    [data-svc-design] .sd-photo>img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scale(1.04);transition:transform 2.4s {EASE};}}
    [data-svc-design].is-in .sd-photo>img{{transform:none;}}
    [data-svc-design] .sd-frame{{position:absolute;left:var(--x,40%);top:var(--y,40%);width:var(--w,20%);height:var(--h,20%);border:1px solid rgba(245,242,237,0.9);box-shadow:0 0 0 200vmax rgba(18,13,9,0);opacity:0;pointer-events:none;transition:left 0.9s {EASE},top 0.9s {EASE},width 0.9s {EASE},height 0.9s {EASE},box-shadow 0.7s {EASE},opacity 0.5s {EASE};}}
    [data-svc-design].has-pick .sd-frame{{opacity:1;box-shadow:0 0 0 200vmax rgba(18,13,9,0.56);}}
    [data-svc-design] .sd-zoom{{position:absolute;inset:0;overflow:hidden;}}
    [data-svc-design] .sd-zoom img{{position:absolute;max-width:none;transition:left 0.9s {EASE},top 0.9s {EASE},width 0.9s {EASE},height 0.9s {EASE};}}
    [data-svc-design] .sd-frame::before,[data-svc-design] .sd-frame::after{{content:"";position:absolute;width:14px;height:14px;border-color:#D6C2A8;border-style:solid;}}
    [data-svc-design] .sd-frame::before{{top:-4px;left:-4px;border-width:2px 0 0 2px;}}
    [data-svc-design] .sd-frame::after{{bottom:-4px;right:-4px;border-width:0 2px 2px 0;}}
    [data-svc-design] .sd-chip{{position:absolute;top:-1px;left:-1px;transform:translateY(-100%);white-space:nowrap;padding:7px 10px;background:#F5F2ED;font-family:{font};font-size:{'12px' if ar else '9px'};letter-spacing:{'normal' if ar else '0.22em'};text-transform:uppercase;color:#3A2D25;}}
    [data-svc-design] .sd-frame.is-top .sd-chip{{top:auto;bottom:-1px;transform:translateY(100%);}}
    [data-svc-design] .sd-mark{{position:absolute;z-index:1;transform:translate(-50%,-50%);width:30px;height:30px;display:grid;place-items:center;padding:0;border:1px solid rgba(245,242,237,0.85);background:rgba(30,22,16,0.55);color:#F5F2ED;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.08em;cursor:pointer;backdrop-filter:blur(4px);transition:opacity 0.5s {EASE},background 0.3s {EASE},color 0.3s {EASE};}}
    [data-svc-design] .sd-mark:hover,[data-svc-design] .sd-mark:focus-visible{{background:#F5F2ED;color:#3A2D25;outline:none;}}
    [data-svc-design].has-pick .sd-mark{{opacity:0;pointer-events:none;}}
    [data-svc-design].has-pick .sd-photo:hover .sd-mark{{opacity:1;pointer-events:auto;}}
    [data-svc-design].has-pick .sd-photo:hover .sd-mark.is-on{{opacity:0;pointer-events:none;}}
    [data-svc-design] .sd-cap{{display:flex;justify-content:space-between;gap:16px;margin-top:14px;padding-inline-start:var(--sd-bleed,0px);font-family:{font};font-size:{'12px' if ar else '11px'};color:#8B6B4A;}}
    [data-svc-design] .sd-side{{display:flex;flex-direction:column;}}
    [data-svc-design] .sd-keyh{{font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;margin:0 0 6px;}}
    [data-svc-design] .sd-key{{list-style:none;margin:0;padding:0;flex:1;display:flex;flex-direction:column;}}
    [data-svc-design] .sd-key li{{flex:1;border-bottom:1px solid rgba(58,45,37,0.14);}}
    [data-svc-design] .sd-item{{position:relative;width:100%;height:100%;display:flex;align-items:center;gap:18px;padding:12px 0;background:none;border:0;text-align:start;cursor:pointer;color:inherit;font:inherit;transition:opacity 0.4s {EASE};}}
    [data-svc-design] .sd-item::before{{content:"";position:absolute;inset-inline-start:0;bottom:-1px;height:1px;width:100%;background:#8B6B4A;transform:scaleX(0);transform-origin:{'100%' if ar else '0%'} 50%;transition:transform 0.7s {EASE};}}
    [data-svc-design].has-pick .sd-item{{opacity:0.5;}}
    [data-svc-design] .sd-item.is-on{{opacity:1!important;}}
    [data-svc-design] .sd-item.is-on::before{{transform:scaleX(1);}}
    [data-svc-design] .sd-item:focus-visible{{outline:1px solid #8B6B4A;outline-offset:2px;}}
    [data-svc-design] .sd-sw{{flex:none;width:56px;height:56px;object-fit:cover;transition:transform 0.6s {EASE};}}
    [data-svc-design] .sd-item.is-on .sd-sw{{transform:scale(1.08);}}
    [data-svc-design] .sd-txt{{display:flex;flex-direction:column;gap:6px;min-width:0;}}
    [data-svc-design] .sd-cat{{display:flex;gap:10px;font-family:{font};font-size:{'12px' if ar else '9px'};letter-spacing:{'normal' if ar else '0.24em'};text-transform:uppercase;color:#8B6B4A;}}
    [data-svc-design] .sd-cat b{{font-family:'Lama Sans',sans-serif;font-weight:500;letter-spacing:0.12em;}}
    [data-svc-design] .sd-name{{font-family:{font};font-size:{'15px' if ar else '14px'};line-height:1.45;color:#3A2D25;}}
    [data-svc-design] .sd-cta{{align-self:flex-start;margin-top:28px;display:inline-flex;align-items:center;gap:12px;padding:17px 30px;background:#3A2D25;color:#F5F2ED;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;border:1px solid #3A2D25;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-design] .sd-cta:hover,[data-svc-design] .sd-cta:focus-visible{{background:transparent;color:#3A2D25;}}
    [data-svc-design] .sd-rise{{opacity:0;transform:translateY(24px);transition:opacity 0.9s {EASE},transform 0.9s {EASE};}}
    [data-svc-design].is-in .sd-rise{{opacity:1;transform:none;}}
    [data-svc-design].is-in .sd-rise--2{{transition-delay:0.12s;}}
    [data-svc-design].is-in .sd-rise--3{{transition-delay:0.24s;}}
    @media(max-width:960px){{
      [data-svc-design] .sd-head,[data-svc-design] .sd-main{{grid-template-columns:1fr;}}
      [data-svc-design] .sd-key li{{flex:none;}}
      [data-svc-design] .sd-fig{{margin-inline:calc(clamp(24px,5vw,80px) * -1);}}
      [data-svc-design] .sd-cap{{padding-inline:clamp(24px,5vw,80px);}}
    }}
    @media(max-width:600px){{
      [data-svc-design] .sd-mark{{width:26px;height:26px;font-size:9px;}}
      [data-svc-design] .sd-cap{{flex-direction:column;gap:4px;}}
      [data-svc-design] .sd-cta{{align-self:stretch;justify-content:center;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-svc-design] *{{transition:none!important;}}
      [data-svc-design] .sd-rise{{opacity:1;transform:none;}}
    }}
  </style>
  <div class="sd-wrap">
    <div class="sd-head">
      <div class="sd-rise">
        <div class="sd-eyebrow"><i></i>{c['eyebrow']}</div>
        <h2 class="sd-h2">{c['h2']}</h2>
      </div>
      <p class="sd-body sd-rise sd-rise--2">{c['body']}</p>
    </div>
    <div class="sd-main">
      <figure class="sd-fig sd-rise sd-rise--2">
        <div class="sd-photo">
          <img src="uploads/{IMG}-1920.webp" srcset="{srcset}" sizes="(max-width:960px) 100vw, 960px" alt="{c['alt']}" width="1920" height="1072" loading="lazy" decoding="async">
          <span class="sd-frame" aria-hidden="true"><span class="sd-zoom"><img src="uploads/{IMG}-1920.webp" srcset="{srcset}" sizes="(max-width:960px) 200vw, 2000px" alt="" loading="lazy" decoding="async"></span><span class="sd-chip"></span></span>
          {marks}
        </div>
        <figcaption class="sd-cap"><span>{c['cap']}</span><span>{c['hint']}</span></figcaption>
      </figure>
      <div class="sd-side sd-rise sd-rise--3">
        <p class="sd-keyh">{c['key']}</p>
        <ol class="sd-key">
{items}
        </ol>
        <a class="sd-cta" href="{c['href']}">{c['cta']}{ARROW_AR if ar else ARROW_EN}</a>
      </div>
    </div>
  </div>
</section>
"""


JS = """    // ── SERVICES, INTERIOR DESIGN: MATERIAL KEY AND VIEWFINDER ───────────────
    {
      const sec = document.querySelector('[data-svc-design]');
      if (sec) {
        const items = Array.from(sec.querySelectorAll('.sd-item'));
        const frame = sec.querySelector('.sd-frame'), chip = sec.querySelector('.sd-chip');
        const photo = sec.querySelector('.sd-photo'), loupe = sec.querySelector('.sd-zoom img');
        const marks = Array.from(sec.querySelectorAll('.sd-mark'));
        let auto = !reduced, timer = null, idx = 0, visible = false, cur = null, over = false;
        // loupe: only while the pointer is over the photo, the copy inside the frame zooms around its centre
        const zoom = () => {
          if (cur === null) return;
          const [x, y, w, h] = items[cur].dataset.f.split(',').map(Number), k = over ? 1.6 : 1;
          const cx = x + w / 2, cy = y + h / 2;
          loupe.style.width = (k * 100 / w * 100) + '%'; loupe.style.height = (k * 100 / h * 100) + '%';
          loupe.style.left = ((w / 2 - k * cx) / w * 100) + '%'; loupe.style.top = ((h / 2 - k * cy) / h * 100) + '%';
        };
        photo.addEventListener('mouseenter', () => { over = true; zoom(); });
        photo.addEventListener('mouseleave', () => { over = false; zoom(); });
        // the photo runs out to the screen edge on the reading-start side
        const bleed = () => {
          const r = sec.querySelector('.sd-wrap').getBoundingClientRect();
          const b = sec.getAttribute('dir') === 'rtl' ? document.documentElement.clientWidth - r.right : r.left;
          sec.style.setProperty('--sd-bleed', Math.max(0, b) + 'px');
        };
        bleed(); window.addEventListener('resize', bleed);
        const pick = (n) => {
          cur = n;
          items.forEach((b, i) => { b.classList.toggle('is-on', i === n); b.setAttribute('aria-pressed', i === n ? 'true' : 'false'); });
          marks.forEach((m, i) => m.classList.toggle('is-on', i === n));
          sec.classList.toggle('has-pick', n !== null);
          if (n === null) return;
          const [x, y, w, h] = items[n].dataset.f.split(',').map(Number);
          frame.style.setProperty('--x', x + '%'); frame.style.setProperty('--y', y + '%');
          frame.style.setProperty('--w', w + '%'); frame.style.setProperty('--h', h + '%');
          frame.classList.toggle('is-top', y < 8);
          chip.textContent = items[n].dataset.label;
          zoom();
        };
        const stop = () => { auto = false; clearInterval(timer); };
        const tick = () => { if (auto && visible) { pick(idx % items.length); idx++; } };
        items.forEach((b, i) => {
          b.addEventListener('mouseenter', () => { stop(); pick(i); });
          b.addEventListener('focus', () => { stop(); pick(i); });
          b.addEventListener('click', () => { stop(); pick(i); });
        });
        sec.querySelectorAll('.sd-mark').forEach((m) => m.addEventListener('click', () => { stop(); pick(Number(m.dataset.i)); }));
        new IntersectionObserver((es) => {
          es.forEach((e) => {
            visible = e.isIntersecting;
            if (visible) {
              sec.classList.add('is-in');
              if (auto && !timer) setTimeout(() => { tick(); timer = setInterval(tick, 3200); }, 1400);
            }
          });
        }, { threshold: 0.25 }).observe(sec);
      }
    }

"""
MARK = "    // ── SCROLL REVEAL"

for path, lang in [("services.dc.html", "en"), ("services.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ 1\. INTERIOR DESIGN ━ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── SERVICES, INTERIOR DESIGN:"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

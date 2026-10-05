"""Services, Engineering & MEP: the invisible systems.

The finished office with a square inspection hatch that follows the pointer. Inside the hatch the same
floor appears before fit-out (same camera), so the ductwork, cable trays and sprinkler mains above the
ceiling show exactly where they run. Each service is labelled when the hatch passes over it; the key
below glides the hatch to a service, and while nobody interacts the hatch tours the four on its own.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/services/svc_mep.py
"""
import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
SHELL = "office-shell-and-core-before-fit-out-riyadh"
DONE = "luxury-office-fit-out-riyadh"
POINTS = [(44.0, 10.0), (69.0, 9.0), (20.0, 8.5), (91.0, 8.0)]  # service positions in % of the photo
C = {
    "en": dict(
        eyebrow="Our Engineering Services", h2="The Foundation of High-Performance Environments",
        body="True luxury and functionality depend on the invisible systems that keep a building running. Our Engineering &amp; MEP (Mechanical, Electrical, and Plumbing) services provide the high-performance infrastructure required to bring your interior vision to life, seamlessly integrated into every design and fit-out we deliver.",
        cta="Explore Engineering &amp; MEP", href="/services-mep",
        cats=["Air", "Power &amp; data", "Fire protection", "Extract"],
        names=["Supply air ductwork", "Cable trays", "Sprinkler mains", "Spiral extract ductwork"],
        lens="Above the ceiling", hint="Move across the ceiling to look above it", hint_touch="Drag the hatch across the ceiling",
        alt="Finished office floor with a walnut slatted ceiling",
        cap="The same office floor, below and above the ceiling · Concept visualisation",
    ),
    "ar": dict(
        eyebrow="خدماتنا الهندسية", h2="أساس البيئات عالية الأداء",
        body="تعتمد الفخامة الحقيقية والوظائفية على الأنظمة غير المرئية التي تُبقي المبنى يعمل. تقدم خدماتنا الهندسية والأنظمة الكهروميكانيكية (الميكانيكية والكهربائية والصحية) البنية التحتية عالية الأداء اللازمة لتحقيق رؤيتك الداخلية، مدمجة بسلاسة في كل تصميم وتشطيب ننفذه.",
        cta="استكشف الهندسة والأنظمة الكهروميكانيكية", href="/ar/services-mep",
        cats=["الهواء", "الطاقة والبيانات", "الحماية من الحريق", "الشفط"],
        names=["مجاري الهواء المكيّف", "حوامل الكابلات", "خطوط الرشاشات الرئيسية", "مجاري الشفط الحلزونية"],
        lens="فوق السقف", hint="مرّر المؤشر على السقف لترى ما فوقه", hint_touch="اسحب الفتحة على السقف",
        alt="طابق مكاتب مكتمل بسقف من شرائح خشب الجوز",
        cap="طابق المكاتب نفسه، تحت السقف وفوقه · تصور مفاهيمي",
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

    def srcset(base):
        return ", ".join(f"uploads/{base}-{w}.webp {w}w" for w in (1280, 1920, 2560))

    pins = "".join(
        f'<span class="sm-pin" data-x="{x}" data-y="{y}"><i></i><span>{c["names"][i]}</span></span>'
        for i, (x, y) in enumerate(POINTS))
    keys = "\n".join(
        f'        <li><button type="button" class="sm-key" data-i="{i}"><b>0{i + 1}</b><span class="sm-cat">{c["cats"][i]}</span><span class="sm-name">{c["names"][i]}</span></button></li>'
        for i in range(len(POINTS)))
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━ 3. ENGINEERING & MEP ━ -->
<section id="mep" data-screen-label="Engineering &amp; MEP" data-svc-mep{' dir="rtl"' if ar else ''} style="scroll-margin-top:var(--fiq-svc-offset,132px);background:#F5F2ED;color:#3A2D25;position:relative;padding:clamp(64px,8vw,100px) clamp(24px,5vw,80px);overflow:clip;">
  <style>
    [data-svc-mep] .sm-wrap{{max-width:1280px;margin:0 auto;}}
    [data-svc-mep] .sm-head{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:clamp(32px,5vw,88px);align-items:end;margin-bottom:clamp(40px,4.4vw,64px);}}
    [data-svc-mep] .sm-eyebrow{{display:flex;align-items:center;gap:16px;margin-bottom:24px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    [data-svc-mep] .sm-eyebrow i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    [data-svc-mep] .sm-h2{{font-family:{font};font-weight:500;font-size:clamp(32px,3.8vw,54px);line-height:1.08;letter-spacing:{'0' if ar else '-0.015em'};color:#1F1F1F;margin:0;text-wrap:balance;}}
    [data-svc-mep] .sm-body{{font-family:{font};font-size:{'16px' if ar else '15px'};line-height:1.85;color:#5B4636;margin:0 0 28px;}}
    [data-svc-mep] .sm-cta{{display:inline-flex;align-items:center;gap:12px;padding:17px 30px;background:#3A2D25;color:#F5F2ED;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;border:1px solid #3A2D25;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-mep] .sm-cta:hover,[data-svc-mep] .sm-cta:focus-visible{{background:transparent;color:#3A2D25;}}
    [data-svc-mep] .sm-stage{{--L:clamp(170px,19vw,280px);position:relative;aspect-ratio:21/9;overflow:hidden;background:#1E1610;cursor:none;touch-action:pan-y;user-select:none;-webkit-user-select:none;}}
    [data-svc-mep] .sm-stage img{{position:absolute;left:0;top:0;width:100%;height:auto;pointer-events:none;}}
    [data-svc-mep] .sm-shell{{clip-path:inset(0 100% 100% 0);}}
    [data-svc-mep] .sm-hatch{{position:absolute;left:0;top:0;width:var(--L);height:var(--L);border:1px solid #F5F2ED;box-shadow:0 0 0 1px rgba(18,13,9,0.25),0 24px 80px rgba(58,45,37,0.2);pointer-events:none;opacity:0;transition:opacity 0.6s {EASE};}}
    [data-svc-mep].is-live .sm-hatch{{opacity:1;}}
    [data-svc-mep] .sm-hatch::before,[data-svc-mep] .sm-hatch::after{{content:"";position:absolute;width:16px;height:16px;border-color:#D6C2A8;border-style:solid;}}
    [data-svc-mep] .sm-hatch::before{{top:-5px;left:-5px;border-width:2px 0 0 2px;}}
    [data-svc-mep] .sm-hatch::after{{bottom:-5px;right:-5px;border-width:0 2px 2px 0;}}
    [data-svc-mep] .sm-hatch span{{position:absolute;left:-1px;bottom:-1px;transform:translateY(100%);white-space:nowrap;padding:6px 10px;background:#F5F2ED;color:#3A2D25;font-family:{font};font-size:{'12px' if ar else '9px'};letter-spacing:{'normal' if ar else '0.22em'};text-transform:uppercase;}}
    [data-svc-mep] .sm-pin{{position:absolute;z-index:1;display:flex;align-items:center;gap:8px;pointer-events:none;opacity:0;transform:translateY(4px);transition:opacity 0.4s {EASE},transform 0.4s {EASE};}}
    [data-svc-mep] .sm-pin.is-seen{{opacity:1;transform:none;}}
    [data-svc-mep] .sm-pin.is-label span{{opacity:1;}}
    [data-svc-mep] .sm-pin i{{flex:none;width:9px;height:9px;margin:-4.5px 0 0 -4.5px;background:#D6C2A8;outline:1px solid rgba(18,13,9,0.6);}}
    [data-svc-mep] .sm-pin span{{opacity:0;transition:opacity 0.3s {EASE};white-space:nowrap;padding:5px 9px;background:rgba(18,13,9,0.78);color:#F5F2ED;font-family:{font};font-size:{'12px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.08em'};}}
    [data-svc-mep] .sm-hint{{position:absolute;bottom:16px;left:50%;transform:translateX(-50%);padding:8px 14px;background:rgba(18,13,9,0.6);backdrop-filter:blur(6px);font-family:{font};font-size:{'12px' if ar else '9px'};letter-spacing:{'normal' if ar else '0.24em'};text-transform:uppercase;color:#D6C2A8;white-space:nowrap;pointer-events:none;transition:opacity 0.6s {EASE};}}
    [data-svc-mep].is-held .sm-hint{{opacity:0;}}
    [data-svc-mep] .sm-hint--touch{{display:none;}}
    [data-svc-mep] .sm-keys{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-bottom:1px solid rgba(58,45,37,0.14);}}
    [data-svc-mep] .sm-key{{position:relative;display:grid;grid-template-columns:auto 1fr;column-gap:12px;row-gap:6px;width:100%;padding:22px 16px 22px 0;background:none;border:0;text-align:start;cursor:pointer;font:inherit;color:inherit;opacity:0.6;transition:opacity 0.4s {EASE};}}
    [data-svc-mep] .sm-key::before{{content:"";position:absolute;top:0;inset-inline:0;height:2px;background:#8B6B4A;transform:scaleX(0);transform-origin:{'100%' if ar else '0%'} 50%;transition:transform 0.6s {EASE};}}
    [data-svc-mep] .sm-key.is-on{{opacity:1;}}
    [data-svc-mep] .sm-key.is-on::before{{transform:scaleX(1);}}
    [data-svc-mep] .sm-key:hover{{opacity:1;}}
    [data-svc-mep] .sm-key:focus-visible{{outline:1px solid #8B6B4A;outline-offset:2px;}}
    [data-svc-mep] .sm-key b{{grid-row:span 2;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:11px;letter-spacing:0.18em;color:#8B6B4A;padding-top:2px;}}
    [data-svc-mep] .sm-cat{{font-family:{font};font-size:{'12px' if ar else '9px'};letter-spacing:{'normal' if ar else '0.24em'};text-transform:uppercase;color:#8B6B4A;}}
    [data-svc-mep] .sm-name{{font-family:{font};font-size:{'15px' if ar else '14px'};color:#3A2D25;}}
    [data-svc-mep] .sm-cap{{margin:14px 0 0;font-family:{font};font-size:{'12px' if ar else '11px'};color:#8B6B4A;}}
    [data-svc-mep] .sm-rise{{opacity:0;transform:translateY(24px);transition:opacity 0.9s {EASE},transform 0.9s {EASE};}}
    [data-svc-mep].is-in .sm-rise{{opacity:1;transform:none;}}
    [data-svc-mep].is-in .sm-rise--2{{transition-delay:0.12s;}}
    @media(hover:none){{
      [data-svc-mep] .sm-stage{{cursor:auto;}}
      [data-svc-mep] .sm-hint--mouse{{display:none;}}
      [data-svc-mep] .sm-hint--touch{{display:block;}}
    }}
    @media(max-width:900px){{
      [data-svc-mep] .sm-head{{grid-template-columns:1fr;}}
      [data-svc-mep] .sm-stage{{--L:clamp(110px,34vw,170px);aspect-ratio:1920/1072;margin-inline:calc(clamp(24px,5vw,80px) * -1);}}
      [data-svc-mep] .sm-keys{{grid-template-columns:repeat(2,minmax(0,1fr));}}
    }}
    @media(max-width:600px){{
      [data-svc-mep] .sm-cta{{width:100%;justify-content:center;box-sizing:border-box;}}
      [data-svc-mep] .sm-pin span{{font-size:{'11px' if ar else '9px'};}}
      [data-svc-mep] .sm-hint{{display:none!important;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-svc-mep] *{{transition:none!important;}}
      [data-svc-mep] .sm-rise{{opacity:1;transform:none;}}
    }}
  </style>
  <div class="sm-wrap">
    <div class="sm-head">
      <div class="sm-rise">
        <div class="sm-eyebrow"><i></i>{c['eyebrow']}</div>
        <h2 class="sm-h2">{c['h2']}</h2>
      </div>
      <div class="sm-rise sm-rise--2">
        <p class="sm-body">{c['body']}</p>
        <a class="sm-cta" href="{c['href']}">{c['cta']}{ARROW_AR if ar else ARROW_EN}</a>
      </div>
    </div>
    <div class="sm-stage sm-rise" data-sm-stage>
      <img src="uploads/{DONE}-1920.webp" srcset="{srcset(DONE)}" sizes="(max-width:900px) 140vw, 1280px" alt="{c['alt']}" width="1920" height="1072" loading="lazy" decoding="async">
      <img class="sm-shell" src="uploads/{SHELL}-1920.webp" srcset="{srcset(SHELL)}" sizes="(max-width:900px) 140vw, 1280px" alt="" width="1920" height="1072" loading="lazy" decoding="async">
      {pins}
      <span class="sm-hatch" aria-hidden="true"><span>{c['lens']}</span></span>
      <span class="sm-hint sm-hint--mouse" aria-hidden="true">{c['hint']}</span>
      <span class="sm-hint sm-hint--touch" aria-hidden="true">{c['hint_touch']}</span>
    </div>
    <ol class="sm-keys">
{keys}
    </ol>
    <p class="sm-cap">{c['cap']}</p>
  </div>
</section>
"""


JS = """    // ── SERVICES, MEP: AN INSPECTION HATCH THROUGH THE CEILING ──────────────
    {
      const sec = document.querySelector('[data-svc-mep]');
      if (sec) {
        const stage = sec.querySelector('[data-sm-stage]'), shell = sec.querySelector('.sm-shell');
        const hatch = sec.querySelector('.sm-hatch'), img = stage.querySelector('img');
        const pins = Array.from(sec.querySelectorAll('.sm-pin')), keys = Array.from(sec.querySelectorAll('.sm-key'));
        // the photo is drawn at full width from the top; points are % of the photo
        const pt = (el) => { const w = stage.clientWidth, h = w * 1072 / 1920; return [Number(el.dataset.x) / 100 * w, Number(el.dataset.y) / 100 * h]; };
        let tx = 0, ty = 0, x = 0, y = 0, raf = null, held = false, auto = !reduced, tour = 0, timer = null, visible = false;
        const lensSize = () => hatch.offsetWidth;
        const clampXY = () => {
          const L = lensSize(), w = stage.clientWidth, h = stage.clientHeight;
          tx = Math.min(w - L / 2, Math.max(L / 2, tx)); ty = Math.min(h - L / 2, Math.max(L / 2, ty));
        };
        const draw = () => {
          const L = lensSize();
          const l = x - L / 2, t = y - L / 2;
          hatch.style.transform = 'translate(' + l + 'px,' + t + 'px)';
          // clip-path insets are measured on the photo, which runs taller than the stage
          const iw = shell.offsetWidth, ih = shell.offsetHeight;
          shell.style.clipPath = 'inset(' + t + 'px ' + (iw - l - L) + 'px ' + (ih - t - L) + 'px ' + l + 'px)';
          // every service inside the hatch shows its marker; only the one nearest its centre is named
          let near = null, best = Infinity;
          pins.forEach((p) => {
            const [px, py] = pt(p);
            p.style.left = px + 'px'; p.style.top = py + 'px';
            const inside = px > l && px < l + L && py > t && py < t + L;
            p.classList.toggle('is-seen', inside);
            const d = (px - x) ** 2 + (py - y) ** 2;
            if (inside && d < best) { best = d; near = p; }
          });
          pins.forEach((p) => p.classList.toggle('is-label', p === near));
        };
        const loop = () => {
          const k = reduced ? 1 : 0.14;
          x += (tx - x) * k; y += (ty - y) * k; draw();
          raf = (Math.abs(tx - x) > 0.3 || Math.abs(ty - y) > 0.3) ? requestAnimationFrame(loop) : null;
        };
        const go = (nx, ny) => { tx = nx; ty = ny; clampXY(); if (!raf) raf = requestAnimationFrame(loop); };
        const focusKey = (i) => {
          keys.forEach((k, j) => k.classList.toggle('is-on', j === i));
          const [px, py] = pt(pins[i]); go(px, py + lensSize() * 0.18);
        };
        const stopTour = () => { auto = false; clearInterval(timer); };
        const hold = () => { if (!held) { held = true; sec.classList.add('is-held'); } stopTour(); };
        const local = (e) => { const r = stage.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };
        stage.addEventListener('pointermove', (e) => {
          if (e.pointerType === 'mouse' || dragging) { hold(); keys.forEach((k) => k.classList.remove('is-on')); go(...local(e)); }
        });
        let dragging = false;
        stage.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') { dragging = true; hold(); go(...local(e)); } });
        const end = () => { dragging = false; };
        stage.addEventListener('pointerup', end); stage.addEventListener('pointercancel', end);
        keys.forEach((k, i) => k.addEventListener('click', () => { hold(); focusKey(i); }));
        const start = () => {
          sec.classList.add('is-live');
          const [px, py] = pt(pins[0]); x = tx = px; y = ty = py + lensSize() * 0.18; clampXY(); x = tx; y = ty; draw();
          if (auto) timer = setInterval(() => { if (auto && visible) { tour = (tour + 1) % pins.length; focusKey(tour); } }, 2600);
          focusKey(0);
        };
        let started = false;
        new IntersectionObserver((es) => {
          es.forEach((e) => {
            visible = e.isIntersecting;
            if (visible) { sec.classList.add('is-in'); if (!started) { started = true; if (img.complete) start(); else img.addEventListener('load', start, { once: true }); } }
          });
        }, { threshold: 0.2 }).observe(sec);
        window.addEventListener('resize', () => { if (started) { clampXY(); x = tx; y = ty; draw(); } });
      }
    }

"""
MARK = "    // ── SCROLL REVEAL"

for path, lang in [("services.dc.html", "en"), ("services.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ 3\. ENGINEERING & MEP ━ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── SERVICES, MEP:"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

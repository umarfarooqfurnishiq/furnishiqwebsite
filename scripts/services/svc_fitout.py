"""Services, Fit-Out: drag the floor through its fit-out.

The same tower floor from the same camera, as a raw shell and as the finished office. A divider wipes
between them; the finished floor spreads from the reading-start side as the divider moves, so the drag
reads as time. A five-phase timeline below lights up as the divider passes each phase. Scrolling drives
the wipe until the visitor takes hold of the handle, a phase, or the keyboard.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/services/svc_fitout.py
"""
import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
BEFORE = "office-shell-and-core-before-fit-out-riyadh"
AFTER = "luxury-office-fit-out-riyadh"
C = {
    "en": dict(
        eyebrow="Our Fit-Out Services", h2="Total Spatial Transformation",
        body="From raw shell to turnkey space, on schedule and without compromise.",
        cta="Explore Fit-Out", href="/services-fitout",
        before="Shell &amp; core", after="Turnkey handover", drag="Drag through the fit-out",
        phases=["Shell &amp; core", "Partitions &amp; ceilings", "Services rough-in", "Finishes &amp; joinery", "Furniture &amp; handover"],
        alt_b="Raw office floor in a tower with exposed ducts, sprinkler pipes and bare concrete",
        alt_a="The same office floor after fit-out, with a walnut slatted ceiling, workstations and a lounge",
        cap="One office floor, before and after · Concept visualisation", slider="Fit-out progress",
    ),
    "ar": dict(
        eyebrow="خدمات التشطيبات لدينا", h2="تحول مكاني كامل",
        body="من الهيكل الخام إلى مساحة جاهزة للتسليم، في الموعد ودون تنازل.",
        cta="استكشف التشطيبات", href="/ar/services-fitout",
        before="الهيكل الخام", after="تسليم جاهز", drag="اسحب عبر مراحل التشطيب",
        phases=["الهيكل الخام", "القواطع والأسقف", "تمديدات الأنظمة", "التشطيبات والنجارة", "الأثاث والتسليم"],
        alt_b="طابق مكاتب خام في برج بمجاري هواء وأنابيب رش ظاهرة وخرسانة مكشوفة",
        alt_a="الطابق نفسه بعد التشطيب بسقف من شرائح خشب الجوز ومحطات عمل وجلسة استقبال",
        cap="طابق مكاتب واحد، قبل وبعد · تصور مفاهيمي", slider="تقدم أعمال التشطيب",
    ),
}
ARROW_EN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
ARROW_AR = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>'
GRIP = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" aria-hidden="true"><polyline points="9 6 3 12 9 18"/><polyline points="15 6 21 12 15 18"/></svg>'


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    side = "clamp(24px,5vw,80px)"

    def srcset(base, ws=(1280, 1920, 2560)):
        return ", ".join(f"uploads/{base}-{w}.webp {w}w" for w in ws)

    n = len(c["phases"])
    phases = "\n".join(
        f'        <li><button type="button" class="sf-ph" data-at="{round(i * 100 / (n - 1))}"><b>0{i + 1}</b><span>{p}</span></button></li>'
        for i, p in enumerate(c["phases"]))
    # the finished floor is uncovered from the reading-start side
    clip = "inset(0 0 0 calc(100% - var(--p) * 1%))" if ar else "inset(0 calc(100% - var(--p) * 1%) 0 0)"
    pos = "right:calc(var(--p) * 1%)" if ar else "left:calc(var(--p) * 1%)"
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2. FIT-OUT ━ -->
<section id="fitout" data-screen-label="Fit-Out" data-svc-fitout{' dir="rtl"' if ar else ''} style="scroll-margin-top:var(--fiq-svc-offset,132px);background:#1E1610;color:#F5F2ED;position:relative;padding:0 {side} clamp(64px,8vw,100px);overflow:clip;">
  <style>
    [data-svc-fitout]{{--p:6;}}
    [data-svc-fitout] .sf-wrap{{max-width:1280px;margin:0 auto;}}
    [data-svc-fitout] .sf-head{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:clamp(32px,5vw,88px);align-items:end;max-width:1280px;margin:0 auto;}}
    [data-svc-fitout] .sf-eyebrow{{display:flex;align-items:center;gap:16px;margin-bottom:24px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#D6C2A8;}}
    [data-svc-fitout] .sf-eyebrow i{{display:block;width:32px;height:1px;background:#D6C2A8;}}
    [data-svc-fitout] .sf-h2{{font-family:{font};font-weight:500;font-size:clamp(34px,4.4vw,64px);line-height:1.04;letter-spacing:{'0' if ar else '-0.02em'};color:#F5F2ED;margin:0;}}
    [data-svc-fitout] .sf-body{{font-family:{font};font-weight:500;font-size:{'clamp(22px,2vw,28px)' if ar else 'clamp(20px,1.9vw,26px)'};line-height:1.4;letter-spacing:{'0' if ar else '-0.005em'};text-wrap:balance;max-width:{'18em' if ar else '30ch'};color:#F5F2ED;margin:0 0 28px;}}
    [data-svc-fitout] .sf-cta{{display:inline-flex;align-items:center;gap:12px;padding:17px 30px;background:#D6C2A8;color:#1E1610;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;border:1px solid #D6C2A8;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-fitout] .sf-cta:hover,[data-svc-fitout] .sf-cta:focus-visible{{background:transparent;color:#D6C2A8;}}
    [data-svc-fitout] .sf-stage{{position:relative;margin-inline:calc(50% - 50vw);width:100vw;height:max(640px,calc(100vh - var(--fiq-svc-offset,132px)));overflow:hidden;background:#120D09;}}
    [data-svc-fitout] .sf-view{{position:absolute;inset:0;cursor:ew-resize;touch-action:pan-y;user-select:none;-webkit-user-select:none;}}
    [data-svc-fitout] .sf-shade{{position:absolute;inset:0;background:rgba(18,13,9,0.34);pointer-events:none;}}
    [data-svc-fitout] .sf-over{{position:absolute;inset-inline:0;top:0;z-index:2;padding:clamp(64px,8vw,100px) {side} 0;pointer-events:none;text-shadow:0 1px 24px rgba(18,13,9,0.55);}}
    [data-svc-fitout] .sf-over .sf-cta{{pointer-events:auto;text-shadow:none;}}
    [data-svc-fitout] .sf-view img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;pointer-events:none;}}
    [data-svc-fitout] .sf-after{{clip-path:{clip};}}
    [data-svc-fitout] .sf-line{{position:absolute;top:0;bottom:0;{pos};width:1px;margin-inline-start:-0.5px;background:#D6C2A8;pointer-events:none;}}
    [data-svc-fitout] .sf-grip{{position:absolute;top:50%;{pos};width:56px;height:56px;transform:translate({'50%' if ar else '-50%'},-50%);display:grid;place-items:center;background:#D6C2A8;color:#1E1610;border:0;padding:0;cursor:ew-resize;transition:background 0.3s {EASE},color 0.3s {EASE};}}
    [data-svc-fitout] .sf-grip:hover,[data-svc-fitout].is-drag .sf-grip{{background:#F5F2ED;}}
    [data-svc-fitout] .sf-grip:focus-visible{{outline:1px solid #F5F2ED;outline-offset:4px;}}
    [data-svc-fitout] .sf-tag{{position:absolute;bottom:clamp(18px,2vw,28px);padding:8px 12px;background:rgba(18,13,9,0.6);backdrop-filter:blur(6px);font-family:{font};font-size:{'12px' if ar else '9px'};letter-spacing:{'normal' if ar else '0.24em'};text-transform:uppercase;color:#F5F2ED;transition:opacity 0.4s {EASE};pointer-events:none;}}
    [data-svc-fitout] .sf-tag--a{{inset-inline-start:max({side},calc((100% - 1280px) / 2));}}
    [data-svc-fitout] .sf-tag--b{{inset-inline-end:max({side},calc((100% - 1280px) / 2));}}
    [data-svc-fitout] .sf-hint{{position:absolute;bottom:clamp(18px,2vw,28px);left:50%;transform:translateX(-50%);padding:8px 14px;background:rgba(18,13,9,0.6);backdrop-filter:blur(6px);font-family:{font};font-size:{'12px' if ar else '9px'};letter-spacing:{'normal' if ar else '0.24em'};text-transform:uppercase;color:#D6C2A8;white-space:nowrap;pointer-events:none;transition:opacity 0.6s {EASE};}}
    [data-svc-fitout].is-held .sf-hint{{opacity:0;}}
    [data-svc-fitout] .sf-time{{position:relative;list-style:none;margin:clamp(24px,2.6vw,36px) 0 0;padding:0;display:grid;grid-template-columns:repeat({n},minmax(0,1fr));}}
    [data-svc-fitout] .sf-time::before,[data-svc-fitout] .sf-time::after{{content:"";position:absolute;top:0;inset-inline-start:0;height:1px;}}
    [data-svc-fitout] .sf-time::before{{width:100%;background:rgba(214,194,168,0.2);}}
    [data-svc-fitout] .sf-time::after{{width:calc(var(--p) * 1%);background:#D6C2A8;}}
    [data-svc-fitout] .sf-ph{{display:flex;flex-direction:column;gap:8px;width:100%;padding:18px 12px 0 0;background:none;border:0;text-align:start;cursor:pointer;font:inherit;color:rgba(245,242,237,0.42);transition:color 0.5s {EASE};}}
    [data-svc-fitout] .sf-ph b{{font-family:'Lama Sans',sans-serif;font-weight:500;font-size:11px;letter-spacing:0.2em;}}
    [data-svc-fitout] .sf-ph span{{font-family:{font};font-size:{'14px' if ar else '13px'};line-height:1.4;}}
    [data-svc-fitout] .sf-ph.is-done{{color:#F5F2ED;}}
    [data-svc-fitout] .sf-ph.is-done b{{color:#D6C2A8;}}
    [data-svc-fitout] .sf-ph:focus-visible{{outline:1px solid #D6C2A8;outline-offset:4px;}}
    [data-svc-fitout] .sf-cap{{margin:18px 0 0;font-family:{font};font-size:{'12px' if ar else '11px'};color:rgba(214,194,168,0.6);}}
    [data-svc-fitout] .sf-rise{{opacity:0;transform:translateY(24px);transition:opacity 0.9s {EASE},transform 0.9s {EASE};}}
    [data-svc-fitout].is-in .sf-rise{{opacity:1;transform:none;}}
    [data-svc-fitout].is-in .sf-rise--2{{transition-delay:0.12s;}}
    @media(max-width:900px){{
      [data-svc-fitout] .sf-head{{grid-template-columns:1fr;}}
      [data-svc-fitout] .sf-stage{{height:auto;overflow:visible;background:none;display:flex;flex-direction:column;}}
      [data-svc-fitout] .sf-over{{order:-1;position:static;padding:clamp(64px,8vw,100px) {side} 40px;text-shadow:none;}}
      [data-svc-fitout] .sf-view{{position:relative;inset:auto;aspect-ratio:4/3;overflow:hidden;}}
      [data-svc-fitout] .sf-shade{{display:none;}}
      [data-svc-fitout] .sf-tag{{top:12px;bottom:auto;}}
      [data-svc-fitout] .sf-time{{grid-template-columns:repeat({n},minmax(110px,1fr));overflow-x:auto;scrollbar-width:none;}}
    }}
    @media(max-width:600px){{
      [data-svc-fitout] .sf-grip{{width:46px;height:46px;}}
      [data-svc-fitout] .sf-cta{{width:100%;justify-content:center;box-sizing:border-box;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-svc-fitout] *{{transition:none!important;}}
      [data-svc-fitout] .sf-rise{{opacity:1;transform:none;}}
    }}
  </style>
  <div class="sf-stage">
    <div class="sf-view" data-sf-stage>
      <img src="uploads/{BEFORE}-1920.webp" srcset="{srcset(BEFORE)}" sizes="100vw" alt="{c['alt_b']}" width="1920" height="1072" loading="lazy" decoding="async">
      <img class="sf-after" src="uploads/{AFTER}-1920.webp" srcset="{srcset(AFTER)}" sizes="100vw" alt="{c['alt_a']}" width="1920" height="1072" loading="lazy" decoding="async">
      <span class="sf-shade" aria-hidden="true"></span>
      <span class="sf-tag sf-tag--a" aria-hidden="true">{c['after']}</span>
      <span class="sf-tag sf-tag--b" aria-hidden="true">{c['before']}</span>
      <span class="sf-line" aria-hidden="true"></span>
      <button type="button" class="sf-grip" role="slider" aria-label="{c['slider']}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="6">{GRIP}</button>
      <span class="sf-hint" aria-hidden="true">{c['drag']}</span>
    </div>
    <div class="sf-over">
      <div class="sf-head">
        <div class="sf-rise">
          <div class="sf-eyebrow"><i></i>{c['eyebrow']}</div>
          <h2 class="sf-h2">{c['h2']}</h2>
        </div>
        <div class="sf-rise sf-rise--2">
          <p class="sf-body">{c['body']}</p>
          <a class="sf-cta" href="{c['href']}">{c['cta']}{ARROW_AR if ar else ARROW_EN}</a>
        </div>
      </div>
    </div>
  </div>
  <div class="sf-wrap">
    <ol class="sf-time">
{phases}
    </ol>
    <p class="sf-cap">{c['cap']}</p>
  </div>
</section>
"""


JS = """    // ── SERVICES, FIT-OUT: THE FLOOR THROUGH ITS FIT-OUT ────────────────────
    {
      const sec = document.querySelector('[data-svc-fitout]');
      if (sec) {
        const stage = sec.querySelector('[data-sf-stage]'), grip = sec.querySelector('.sf-grip');
        const phases = Array.from(sec.querySelectorAll('.sf-ph'));
        const rtl = sec.getAttribute('dir') === 'rtl';
        const tags = sec.querySelectorAll('.sf-tag');
        let held = false, p = 6, anim = null;
        const clamp = (v) => Math.min(100, Math.max(0, v));
        const set = (v) => {
          p = clamp(v);
          sec.style.setProperty('--p', p.toFixed(2));
          grip.setAttribute('aria-valuenow', Math.round(p));
          phases.forEach((b) => b.classList.toggle('is-done', p >= Number(b.dataset.at) - 0.5));
          tags[0].style.opacity = p > 14 ? 1 : 0;   // finished floor tag shows once there is finished floor
          tags[1].style.opacity = p < 86 ? 1 : 0;   // shell tag shows while some shell remains
        };
        const hold = () => { if (!held) { held = true; sec.classList.add('is-held'); } };
        const glide = (to) => {
          cancelAnimationFrame(anim);
          if (reduced) { set(to); return; }
          const from = p, t0 = performance.now(), dur = 900;
          const step = (t) => { const k = Math.min(1, (t - t0) / dur), e = k * k * (3 - 2 * k); set(from + (to - from) * e); if (k < 1) anim = requestAnimationFrame(step); };
          anim = requestAnimationFrame(step);
        };
        const fromPointer = (x) => { const r = stage.getBoundingClientRect(); const f = (x - r.left) / r.width * 100; return rtl ? 100 - f : f; };
        let dragging = false;
        stage.addEventListener('pointerdown', (e) => {
          if (e.pointerType === 'mouse' && e.button !== 0) return;
          dragging = true; hold(); cancelAnimationFrame(anim); sec.classList.add('is-drag');
          stage.setPointerCapture(e.pointerId); set(fromPointer(e.clientX));
        });
        stage.addEventListener('pointermove', (e) => { if (dragging) set(fromPointer(e.clientX)); });
        const end = () => { dragging = false; sec.classList.remove('is-drag'); };
        stage.addEventListener('pointerup', end); stage.addEventListener('pointercancel', end);
        grip.addEventListener('keydown', (e) => {
          const fwd = rtl ? 'ArrowLeft' : 'ArrowRight', back = rtl ? 'ArrowRight' : 'ArrowLeft';
          let to = null;
          if (e.key === fwd || e.key === 'ArrowUp') to = p + 5;
          else if (e.key === back || e.key === 'ArrowDown') to = p - 5;
          else if (e.key === 'Home') to = 0; else if (e.key === 'End') to = 100;
          if (to !== null) { e.preventDefault(); hold(); glide(clamp(to)); }
        });
        phases.forEach((b) => b.addEventListener('click', () => { hold(); glide(Number(b.dataset.at)); }));
        // until someone takes hold, scrolling carries the floor through its fit-out
        let ticking = false;
        const onScroll = () => {
          ticking = false;
          if (held) return;
          const r = stage.getBoundingClientRect(), vh = window.innerHeight;
          // from the stage entering at the bottom to the stage sitting centred on screen
          const start = vh * 0.9, end = Math.max(0, (vh - r.height) / 2);
          const t = Math.min(1, Math.max(0, (start - r.top) / (start - end || 1)));
          set(6 + t * 88);
        };
        window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
        onScroll();
        new IntersectionObserver((es) => { es.forEach((e) => { if (e.isIntersecting) sec.classList.add('is-in'); }); }, { threshold: 0.12 }).observe(sec);
      }
    }

"""
MARK = "    // ── SCROLL REVEAL"

for path, lang in [("services.dc.html", "en"), ("services.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ 2\. FIT-OUT ━ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── SERVICES, FIT-OUT:"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

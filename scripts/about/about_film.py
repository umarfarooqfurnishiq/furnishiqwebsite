import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
SCENES = [
    ("courtyard-residence-grand-majlis-riyadh", "50% 55%", "30% 40%"),
    ("desert-stone-resort-arrival-court", "50% 50%", "50% 70%"),
    ("executive-floors-sky-lobby-reception-riyadh", "50% 50%", "60% 45%"),
]
C = {
    "en": dict(
        eyebrow="About FurnishIQ", h1=["Where vision", "meets precision."],
        desc="A Saudi-based design-build studio delivering interior design, fit-out, engineering and furniture solutions from concept to handover.",
        cta="Book Free Consultation", cta_href="/contact", story="See More",
        scenes=[("Design", "Grand majlis"), ("Build", "Desert stone resort, AlUla"), ("Deliver", "Executive floors, Riyadh")],
        concept="Concept visualisations",
        facts=[("15", "+", "Years of practice"), ("40", "+", "Completed projects"), ("20", "+", "Team members"),
               ("25", "+", "Clients served")],
    ),
    "ar": dict(
        eyebrow="عن فيرنيش آي كيو", h1=["حيث تلتقي الرؤية", "بالدقة."],
        desc="استوديو تصميم وتنفيذ سعودي يقدم التصميم الداخلي والتشطيبات والهندسة وحلول الأثاث من الفكرة وحتى التسليم.",
        cta="احجز استشارة مجانية", cta_href="/ar/contact", story="شاهد المزيد",
        scenes=[("التصميم", "المجلس الكبير"), ("التنفيذ", "منتجع الحجر الصحراوي، العُلا"), ("التسليم", "الطوابق التنفيذية، الرياض")],
        concept="تصورات تصميمية",
        facts=[("15", "+", "عاماً من الخبرة"), ("40", "+", "مشروعاً منجزاً"), ("20", "+", "عضواً في فريقنا"),
               ("25", "+", "عميلاً")],
    ),
}
ARROW = '<svg width="16" height="6" viewBox="0 0 16 6" fill="none" aria-hidden="true" style="transform:{flip};flex-shrink:0;"><path d="M0 3H14M14 3L11.5 1M14 3L11.5 5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
DOWN = '<svg width="10" height="14" viewBox="0 0 10 14" fill="none" aria-hidden="true"><path d="M5 0V12M5 12L1.5 8.5M5 12L8.5 8.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"></path></svg>'


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    flip = "scaleX(-1)" if ar else "none"

    slides = ""
    for i, (img, o1, o2) in enumerate(SCENES):
        srcset = ", ".join(f"uploads/{img}-{w}.webp {w}w" for w in (1280, 1920, 2752))
        slides += f"""
    <div class="sf-slide{' is-active' if i == 0 else ''}" data-sf-slide style="--o1:{o1};--o2:{o2};"><img src="uploads/{img}-1920.webp" srcset="{srcset}" sizes="100vw" alt="{c['scenes'][i][1]}" {'fetchpriority="high"' if i == 0 else 'loading="lazy"'} decoding="async"></div>"""
    tabs = "".join(f"""
          <button type="button" class="sf-tab{' is-active' if i == 0 else ''}" data-sf-tab aria-label="{k} — {v}"><span class="sf-bar"><span></span></span><span class="sf-tab-k"><span dir="ltr">0{i + 1}</span> {k}</span><span class="sf-tab-v">{v}</span></button>""" for i, (k, v) in enumerate(c["scenes"]))
    facts = "".join(f"""
      <div class="ah-fact"><span class="ah-num" dir="ltr"><span data-count="{n}">{'2007' if n == '2007' else '0'}</span>{plus}</span><span class="ah-label">{label}</span></div>""" for n, plus, label in c["facts"])
    h1 = "".join(f'<span style="display:block;overflow:hidden;padding-bottom:0.14em;margin-bottom:-0.14em;"><span data-hero-word style="display:block;transform:translateY(112%);transition:transform 1.1s {EASE};{"color:#D6C2A8;" if i else ""}">{t}</span></span>' for i, t in enumerate(c["h1"]))

    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ PAGE HERO ━ -->
<section data-about-hero{' dir="rtl"' if ar else ''} style="position:relative;background:#120D09;height:100vh;min-height:720px;overflow:hidden;display:flex;flex-direction:column;">
  <style>
    [data-about-hero] .sf-slide{{position:absolute;inset:0;opacity:0;transition:opacity 1.8s {EASE};}}
    [data-about-hero] .sf-slide.is-active{{opacity:1;}}
    [data-about-hero] .sf-slide img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:var(--o1);transform:scale(1.02);}}
    /* layer order: slides 1-2, veil and fade 3, copy 4, opening doors 6 */
    [data-about-hero] .sf-slide.is-leaving{{z-index:1;}}
    [data-about-hero] .sf-slide.is-active{{z-index:2;}}
    [data-about-hero] .sf-slide.is-active img,[data-about-hero] .sf-slide.is-leaving img{{animation:sf-drift 10s linear forwards;}}
    @keyframes sf-drift{{from{{transform:scale(1.02);object-position:var(--o1);}}to{{transform:scale(1.14);object-position:var(--o2);}}}}
    [data-about-hero] .sf-veil{{position:absolute;inset:0;z-index:3;background:rgba(18,13,9,0.46);}}
    [data-about-hero] .sf-door{{position:absolute;left:0;right:0;height:50.5%;background:#120D09;z-index:6;transition:transform 1.6s cubic-bezier(0.77,0,0.18,1) 0.15s;}}
    [data-about-hero] .sf-door--t{{top:0;transform-origin:top;}}
    [data-about-hero] .sf-door--b{{bottom:0;transform-origin:bottom;}}
    [data-about-hero] .sf-door::after{{content:"";position:absolute;left:0;right:0;height:1px;background:rgba(214,194,168,0.6);transform:scaleX(0);transition:transform 0.9s {EASE};}}
    [data-about-hero] .sf-door--t::after{{bottom:0;}}
    [data-about-hero] .sf-door--b::after{{top:0;}}
    [data-about-hero].is-ready .sf-door::after{{transform:scaleX(1);}}
    [data-about-hero].is-open .sf-door--t{{transform:translateY(-101%);}}
    [data-about-hero].is-open .sf-door--b{{transform:translateY(101%);}}
    [data-about-hero] .sf-body{{position:relative;z-index:4;flex:1;max-width:1280px;width:100%;margin:0 auto;padding:clamp(120px,18vh,180px) clamp(24px,5vw,80px) clamp(32px,5vh,56px);box-sizing:content-box;display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);align-items:end;gap:clamp(32px,5vw,96px);}}
    [data-about-hero] .sf-h1{{font-family:{font};font-size:clamp(46px,6.4vw,112px);font-weight:500;line-height:{'1.2' if ar else '0.98'};letter-spacing:{'normal' if ar else '-0.03em'};color:#FFFFFF;margin:0;}}
    [data-about-hero] .sf-side{{padding-bottom:0.5em;}}
    [data-about-hero] .sf-desc{{font-family:{font};font-size:{'17px' if ar else '16px'};line-height:1.8;color:rgba(245,242,237,0.86);margin:0;max-width:440px;}}
    [data-about-hero] .sf-ctas{{display:flex;align-items:center;gap:28px;flex-wrap:wrap;margin-top:32px;}}
    [data-about-hero] .sf-cta{{display:inline-flex;align-items:center;gap:14px;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;color:#3A2D25;background:#D6C2A8;padding:18px 30px;text-decoration:none;transition:background 0.4s {EASE};}}
    [data-about-hero] .sf-cta:hover,[data-about-hero] .sf-cta:focus-visible{{background:#FFFFFF;}}
    [data-about-hero] .sf-story{{display:inline-flex;align-items:center;gap:12px;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;color:#FFFFFF;text-decoration:none;padding-bottom:6px;border-bottom:1px solid rgba(255,255,255,0.45);transition:border-color 0.4s {EASE};}}
    [data-about-hero] .sf-story:hover,[data-about-hero] .sf-story:focus-visible{{border-color:#D6C2A8;}}
    [data-about-hero] .sf-story svg{{animation:sf-bob 2.4s {EASE} infinite;}}
    @keyframes sf-bob{{0%,100%{{transform:translateY(-2px)}}50%{{transform:translateY(4px)}}}}
    [data-about-hero] .sf-tabs{{position:relative;z-index:4;max-width:1280px;width:100%;margin:0 auto;padding:0 clamp(24px,5vw,80px) clamp(22px,3.4vh,34px);box-sizing:content-box;display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) auto;gap:clamp(16px,2.4vw,40px);align-items:end;}}
    [data-about-hero] .sf-tab{{display:flex;flex-direction:column;gap:10px;background:none;border:none;padding:0;cursor:pointer;text-align:start;color:rgba(245,242,237,0.55);transition:color 0.4s {EASE};}}
    [data-about-hero] .sf-tab.is-active,[data-about-hero] .sf-tab:hover,[data-about-hero] .sf-tab:focus-visible{{color:#FFFFFF;}}
    [data-about-hero] .sf-bar{{display:block;height:1px;background:rgba(245,242,237,0.25);}}
    [data-about-hero] .sf-bar span{{display:block;height:100%;width:0;background:#D6C2A8;}}
    [data-about-hero] .sf-tab.is-active .sf-bar span{{animation:sf-fill 7s linear forwards;}}
    [data-about-hero].is-paused .sf-tab.is-active .sf-bar span{{animation:none;width:100%;}}
    @keyframes sf-fill{{from{{width:0}}to{{width:100%}}}}
    [data-about-hero] .sf-tab-k{{font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#D6C2A8;}}
    [data-about-hero] .sf-tab-k [dir]{{font-family:'Lama Sans',sans-serif;letter-spacing:0.2em;}}
    [data-about-hero] .sf-tab-v{{font-family:{font};font-size:{'14px' if ar else '13px'};}}
    [data-about-hero] .sf-concept{{font-family:{font};font-size:{'11px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.08em'};color:rgba(245,242,237,0.5);white-space:nowrap;padding-bottom:2px;}}
    [data-about-hero] .ah-facts{{position:relative;z-index:4;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));}}
    [data-about-hero] .sf-fade{{position:absolute;left:0;right:0;bottom:0;z-index:3;height:min(42%,380px);background:linear-gradient(to top,#261C16 0%,rgba(38,28,22,0.88) 22%,rgba(38,28,22,0.55) 55%,rgba(38,28,22,0) 100%);pointer-events:none;z-index:1;}}
    [data-about-hero] .ah-fact{{display:flex;flex-direction:column;align-items:center;text-align:center;gap:10px;padding:clamp(20px,2.8vh,30px) clamp(20px,3vw,56px) clamp(22px,3.2vh,34px);border-inline-start:1px solid rgba(214,194,168,0.5);}}
    [data-about-hero] .ah-fact:first-child{{border-inline-start:none;}}
    [data-about-hero] .ah-num{{font-family:'Lama Sans',sans-serif;font-size:clamp(28px,2.8vw,44px);line-height:1;color:#FFFFFF;letter-spacing:-0.01em;}}
    [data-about-hero] .ah-label{{font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:rgba(214,194,168,0.75);line-height:1.6;}}
    [data-about-hero] .sf-reveal{{opacity:0;transform:translateY(16px);transition:opacity 1s {EASE},transform 1s {EASE};}}
    [data-about-hero].is-open .sf-reveal{{opacity:1;transform:none;}}
    [data-about-hero].is-open .sf-reveal--1{{transition-delay:1.5s;}}
    [data-about-hero].is-open .sf-reveal--2{{transition-delay:1.75s;}}
    [data-about-hero].is-open .sf-reveal--3{{transition-delay:1.95s;}}
    @media(max-width:900px){{
      [data-about-hero]{{height:auto!important;min-height:100svh!important;}}
      [data-about-hero] .sf-body{{grid-template-columns:1fr;padding-top:120px;align-content:end;}}
      [data-about-hero] .sf-body,[data-about-hero] .sf-tabs{{box-sizing:border-box;}}
      [data-about-hero] .sf-h1{{font-size:clamp(40px,11vw,64px);}}
      [data-about-hero] .sf-tabs{{grid-template-columns:repeat(3,minmax(0,1fr));}}
      [data-about-hero] .sf-tab-v,[data-about-hero] .sf-concept{{display:none;}}
      [data-about-hero] .ah-facts{{grid-template-columns:repeat(2,minmax(0,1fr));}}
      [data-about-hero] .ah-fact{{padding:14px;}}
      [data-about-hero] .ah-fact:nth-child(3){{border-inline-start:none;}}
      [data-about-hero] .ah-fact:nth-child(n+3){{border-top:1px solid rgba(214,194,168,0.3);}}
      [data-about-hero] .ah-num{{font-size:24px;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-about-hero] .sf-door{{display:none;}}
      [data-about-hero] .sf-slide,[data-about-hero] .sf-reveal{{transition:none;}}
      [data-about-hero] .sf-slide.is-active img,[data-about-hero] .sf-slide.is-leaving img,[data-about-hero] .sf-story svg{{animation:none;}}
    }}
  </style>{slides}
  <span class="sf-veil" aria-hidden="true"></span><span class="sf-fade" aria-hidden="true"></span>
  <div class="sf-body">
    <div>
      <div data-hero-eyebrow style="opacity:0;transition:opacity 0.6s {EASE} 1.2s;display:flex;align-items:center;gap:16px;margin-bottom:30px;">
        <span data-hero-eyebrow-line style="display:block;width:0px;height:1px;background:#D6C2A8;flex-shrink:0;transition:width 0.7s {EASE} 1.3s;"></span>
        <span style="font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:rgba(214,194,168,0.9);">{c['eyebrow']}</span>
      </div>
      <h1 class="sf-h1">{h1}</h1>
    </div>
    <div class="sf-side sf-reveal sf-reveal--1">
      <p class="sf-desc">{c['desc']}</p>
      <div class="sf-ctas">
        <a class="sf-cta" href="{c['cta_href']}">{c['cta']}{ARROW.format(flip=flip)}</a>
        <a class="sf-story" href="#why">{c['story']}{DOWN}</a>
      </div>
    </div>
  </div>
  <div class="sf-tabs sf-reveal sf-reveal--2" role="group">{tabs}
    <span class="sf-concept">{c['concept']}</span>
  </div>
  <div class="ah-facts sf-reveal sf-reveal--3">{facts}
  </div>
  <span class="sf-door sf-door--t" aria-hidden="true"></span><span class="sf-door sf-door--b" aria-hidden="true"></span>
</section>
"""


JS = """    // ── HERO: STUDIO FILM (aperture opens, scenes dissolve) ──────────────────
    {
      const ah = document.querySelector('[data-about-hero]');
      if (ah) {
        const slides = [...ah.querySelectorAll('[data-sf-slide]')];
        const tabs = [...ah.querySelectorAll('[data-sf-tab]')];
        const counts = [...ah.querySelectorAll('[data-count]')].filter(el => el.dataset.count !== '2007');
        let current = 0, timer = null;
        const leaveTimers = new Map();
        const show = (n) => {
          if (n === current && slides[n].classList.contains('is-active')) return;
          current = n;
          slides.forEach((s, k) => {
            const on = k === n, was = s.classList.contains('is-active');
            if (on && !was) {
              clearTimeout(leaveTimers.get(s)); s.classList.remove('is-leaving');
              const im = s.querySelector('img'); im.style.animation = 'none'; void im.offsetWidth; im.style.animation = '';
            }
            // the outgoing scene keeps its slow zoom while it dissolves, instead of snapping back
            if (!on && was) {
              s.classList.add('is-leaving');
              clearTimeout(leaveTimers.get(s));
              leaveTimers.set(s, setTimeout(() => s.classList.remove('is-leaving'), 1900));
            }
            s.classList.toggle('is-active', on);
          });
          tabs.forEach((t, k) => {
            t.classList.toggle('is-active', k === n);
            const bar = t.querySelector('.sf-bar span'); bar.style.animation = 'none'; void bar.offsetWidth; bar.style.animation = '';
          });
        };
        const schedule = () => {
          clearTimeout(timer);
          if (reduced || ah.classList.contains('is-paused')) return;
          timer = setTimeout(() => { show((current + 1) % slides.length); schedule(); }, 7000);
        };
        tabs.forEach((t, i) => t.addEventListener('click', () => { ah.classList.add('is-paused'); show(i); clearTimeout(timer); }));
        const countUp = () => {
          if (reduced) { counts.forEach(el => { el.textContent = el.dataset.count; }); return; }
          const t0 = performance.now(), dur = 1600;
          const tick = (now) => { const p = Math.min((now - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3); counts.forEach(el => { el.textContent = Math.round(+el.dataset.count * e); }); if (p < 1) requestAnimationFrame(tick); };
          requestAnimationFrame(tick);
        };
        const first = slides[0].querySelector('img');
        const open = () => {
          if (ah.classList.contains('is-open')) return;
          ah.classList.add('is-ready');
          setTimeout(() => ah.classList.add('is-open'), reduced ? 0 : 500);
          setTimeout(countUp, reduced ? 0 : 2300);
          schedule();
        };
        if (first.complete) open(); else { first.addEventListener('load', open); setTimeout(open, 1800); }
        document.addEventListener('visibilitychange', () => { if (document.hidden) clearTimeout(timer); else schedule(); });
      }
    }

"""
MARK = "    // ── FADE-IN ON LOAD (lazy images)"
OLD = ("    // ── HERO: ARCH REVEAL", "    // ── HERO: ENTER THE SPACE", "    // ── HERO: FROSTED GLASS",
       "    // ── HERO: BLUEPRINT TO REALITY", "    // ── HERO: STUDIO FILM")

for path, lang in [("about-us.dc.html", "en"), ("about-us.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ PAGE HERO ━ -->\n<section data-about-hero.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    for old in OLD:
        if old in s:
            a = s.index(old)
            b = s.index(chr(10) + "    // ── ", a + 1) + 1   # end of this block = start of the next marked block
            s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

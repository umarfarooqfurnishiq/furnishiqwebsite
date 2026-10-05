import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
PILLAR_IMGS = ["pillar-end-to-end-delivery-key-handover", "pillar-design-build-sketch-materials", "pillar-quality-assurance-level-inspection", "pillar-project-management-riyadh-timeline"]
C = {
    "en": dict(
        label="Why Choose FurnishIQ", h2=["Four pillars.", "One roof."],
        lead="We help clients build spaces that perform, inspire, and endure.",
        pillars=[("End-to-End Delivery", "Single point of responsibility from concept to completion."),
                 ("Design &amp; Build Expertise", "Creative design and construction expertise combined under one roof."),
                 ("Quality Assurance", "Checkpoints at every stage catch issues before the client ever does."),
                 ("Project Management", "Schedules, budgets, and coordination managed with full transparency.")],
        body="One accountable team takes every project from first sketch to final handover, so ambitious spaces arrive on time, on budget and without compromise.",
        cta="Book Free Consultation", href="/contact", caption="Obhur beach estate, Jeddah. Concept visualisation", cue="Scroll to build",
    ),
    "ar": dict(
        label="لماذا تختار فيرنيش آي كيو", h2=["أربع ركائز.", "سقف واحد."],
        lead="نساعد عملاءنا على بناء مساحات تُؤدي وتُلهم وتدوم.",
        pillars=[("تسليم متكامل من البداية للنهاية", "جهة مسؤولة واحدة من الفكرة وحتى الإنجاز."),
                 ("خبرة في التصميم والتنفيذ", "خبرة إبداعية في التصميم والبناء مجتمعة تحت سقف واحد."),
                 ("ضمان الجودة", "نقاط تفتيش في كل مرحلة ترصد المشكلات قبل أن يلاحظها العميل."),
                 ("إدارة المشاريع", "إدارة الجداول الزمنية والميزانيات والتنسيق بشفافية كاملة.")],
        body="فريق واحد مسؤول يتولى كل مشروع من الرسم الأول حتى التسليم النهائي، لتصل المساحات الطموحة في الوقت المحدد وضمن الميزانية ودون أي تنازلات.",
        cta="احجز استشارة مجانية", href="/ar/contact", caption="عقار شاطئ أبحر، جدة. تصور تصميمي", cue="مرّر للبناء",
    ),
}


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    flip = "scaleX(-1)" if ar else "none"
    arrow = f'<svg width="16" height="6" viewBox="0 0 16 6" fill="none" aria-hidden="true" style="transform:{flip};"><path d="M0 3H14M14 3L11.5 1M14 3L11.5 5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
    cols, caps = "", ""
    for i, (title, desc) in enumerate(c["pillars"]):
        im = PILLAR_IMGS[i]
        cols += f"""
      <div class="pl-col" data-pl-col><img src="uploads/{im}-1536.webp" srcset="uploads/{im}-900.webp 900w, uploads/{im}-1536.webp 1536w" sizes="(max-width:900px) 50vw, 25vw" alt="" loading="lazy" decoding="async"></div>"""
        caps += f"""
      <div class="pl-cap" data-pl-cap>
        <span class="pl-num" dir="ltr">0{i + 1}</span>
        <h3 class="pl-title">{title}</h3>
        <p class="pl-desc">{desc}</p>
      </div>"""
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ WHY FURNISHIQ ━ -->
<section id="why" data-pillars{' dir="rtl"' if ar else ''} style="position:relative;background:#2B211B;height:300vh;">
  <style>
    #why .pl-stage{{position:sticky;top:0;height:100vh;min-height:640px;overflow:hidden;}}
    #why .pl-cols{{position:absolute;inset:0;display:grid;grid-template-columns:repeat(4,1fr);}}
    #why .pl-col{{position:relative;overflow:hidden;}}
    #why .pl-col + .pl-col::before{{content:"";position:absolute;top:0;bottom:0;inset-inline-start:0;width:1px;background:rgba(214,194,168,var(--seam,0.5));z-index:2;}}
    #why .pl-col img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 40%;will-change:transform;}}
    #why .pl-col::after{{content:"";position:absolute;inset:0;background:rgba(30,22,16,var(--tint,0.42));}}
    #why .pl-head{{position:absolute;top:clamp(110px,15vh,150px);left:0;right:0;padding:0 clamp(24px,5vw,80px);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(32px,5vw,96px);align-items:start;}}
    #why .pl-label{{display:flex;align-items:center;gap:16px;margin-bottom:22px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#D6C2A8;}}
    #why .pl-label i{{display:block;width:32px;height:1px;background:#D6C2A8;}}
    #why .pl-h2{{font-family:{font};font-size:clamp(40px,5vw,84px);font-weight:500;line-height:{'1.2' if ar else '1.0'};letter-spacing:{'normal' if ar else '-0.025em'};color:#FFFFFF;margin:0;}}
    #why .pl-h2 span{{display:block;}}
    #why .pl-h2 span + span{{color:#D6C2A8;}}
    #why .pl-lead{{font-family:{font};font-size:{'17px' if ar else '16px'};line-height:1.7;color:rgba(245,242,237,0.85);margin:22px 0 0;max-width:460px;}}
    #why .pl-end{{justify-self:end;max-width:400px;opacity:0;transform:translateY(16px);}}
    #why .pl-body{{font-family:{font};font-size:{'16px' if ar else '15px'};line-height:1.8;color:rgba(245,242,237,0.88);margin:0;}}
    #why .pl-link{{display:inline-flex;align-items:center;gap:14px;margin-top:22px;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;color:#3A2D25;background:#D6C2A8;padding:16px 26px;text-decoration:none;transition:background 0.4s {EASE};}}
    #why .pl-link:hover,#why .pl-link:focus-visible{{background:#FFFFFF;}}
    #why .pl-caps{{position:absolute;left:0;right:0;bottom:0;display:grid;grid-template-columns:repeat(4,1fr);}}
    #why .pl-cap{{margin:0 clamp(18px,2.2vw,40px);padding:0 0 clamp(28px,5vh,52px);opacity:0;transform:translateY(18px);}}
    #why .pl-cap{{border-top:1px solid rgba(214,194,168,0.6);}}
    #why .pl-num{{display:block;text-align:end;font-family:'Lama Sans',sans-serif;font-size:clamp(56px,5.6vw,104px);line-height:1;letter-spacing:-0.03em;color:rgba(214,194,168,0.28);margin:10px 0 6px;}}
    #why .pl-title{{font-family:{font};font-size:clamp(17px,1.4vw,22px);font-weight:500;line-height:1.25;color:#FFFFFF;margin:0;}}
    #why .pl-desc{{font-family:{font};font-size:{'14px' if ar else '13px'};line-height:1.65;color:rgba(245,242,237,0.78);margin:8px 0 0;max-width:300px;}}
    #why .pl-cue{{position:absolute;bottom:clamp(28px,5vh,52px);left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:12px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:rgba(214,194,168,0.7);}}
    #why .pl-cue i{{display:block;width:1px;height:40px;background:rgba(214,194,168,0.35);position:relative;overflow:hidden;}}
    #why .pl-cue i::after{{content:"";position:absolute;inset:0;background:#D6C2A8;animation:pl-cue 2.2s {EASE} infinite;}}
    @keyframes pl-cue{{0%{{transform:translateY(-100%)}}100%{{transform:translateY(100%)}}}}
    @media(max-width:900px){{
      #why{{height:auto!important;}}
      #why .pl-stage{{position:relative;height:auto;min-height:0;padding:clamp(64px,8vw,100px) clamp(24px,5vw,80px);}}
      #why .pl-cols{{position:relative;inset:auto;grid-template-columns:1fr 1fr;grid-auto-rows:62vw;margin:32px calc(-1 * clamp(24px,5vw,80px));}}
      #why .pl-col img{{transform:none!important;}}
      #why .pl-head{{position:static;padding:0;grid-template-columns:1fr;gap:24px;}}
      #why .pl-end{{justify-self:start;opacity:1;transform:none;order:3;}}
      #why .pl-caps{{position:static;grid-template-columns:1fr 1fr;gap:28px 20px;}}
      #why .pl-cap{{margin:0;padding:0 0 4px;opacity:1;transform:none;}}
      #why .pl-num{{font-size:44px;}}
      #why .pl-cue{{display:none;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      #why{{height:auto!important;}}
      #why .pl-stage{{position:relative;height:100vh;}}
      #why .pl-cue{{display:none;}}
    }}
  </style>
  <div class="pl-stage">
    <div class="pl-cols" aria-hidden="true">{cols}
    </div>
    <div class="pl-head">
      <div>
        <div class="pl-label"><i></i>{c['label']}</div>
        <h2 class="pl-h2"><span>{c['h2'][0]}</span><span>{c['h2'][1]}</span></h2>
        <p class="pl-lead">{c['lead']}</p>
      </div>
      <div class="pl-end">
        <p class="pl-body">{c['body']}</p>
        <a class="pl-link" href="{c['href']}">{c['cta']}{arrow}</a>
      </div>
    </div>
    <div class="pl-caps">{caps}
    </div>
    <div class="pl-cue" aria-hidden="true"><span>{c['cue']}</span><i></i></div>
  </div>
</section>
"""


JS = """    // ── WHY: FOUR PILLARS, ONE ROOF (pillars rise and align on scroll) ──────
    {
      const pl = document.querySelector('[data-pillars]');
      if (pl) {
        const cols = [...pl.querySelectorAll('[data-pl-col]')], caps = [...pl.querySelectorAll('[data-pl-cap]')];
        const end = pl.querySelector('.pl-end'), cue = pl.querySelector('.pl-cue');
        const lead = pl.querySelector('.pl-lead');
        const START = [0.78, 0.52, 0.92, 0.64];      // how far below its place each pillar starts (fraction of height)
        const clamp = (v) => Math.min(Math.max(v, 0), 1);
        const ease = (t) => 1 - Math.pow(1 - t, 3);
        const mobile = () => window.innerWidth <= 900;
        let ticking = false;
        const update = () => {
          ticking = false;
          if (mobile()) { cols.forEach(c => c.querySelector('img').style.transform = ''); return; }
          const vh = window.innerHeight, total = pl.offsetHeight - vh;
          const p = reduced ? 1 : clamp(-pl.getBoundingClientRect().top / (total || 1));
          cols.forEach((c, i) => {
            const t = ease(clamp((p - 0.04 - i * 0.11) / 0.36));
            c.querySelector('img').style.transform = `translateY(${(START[i] * (1 - t) * 100).toFixed(2)}%)`;
            const cap = caps[i], ct = clamp((t - 0.82) / 0.18);
            cap.style.opacity = ct.toFixed(3);
            cap.style.transform = `translateY(${(18 * (1 - ct)).toFixed(1)}px)`;
          });
          const done = clamp((p - 0.74) / 0.16);
          pl.style.setProperty('--seam', '0.45');
          pl.style.setProperty('--tint', (0.42 + 0.16 * clamp((p - 0.3) / 0.4)).toFixed(3));
          end.style.opacity = done.toFixed(3);
          end.style.transform = `translateY(${(16 * (1 - done)).toFixed(1)}px)`;
          cue.style.opacity = (1 - clamp(p / 0.08)).toFixed(3);
        };
        const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
        update();
        window.addEventListener('scroll', onScroll, { passive: true });
        window.addEventListener('resize', onScroll);
      }
    }

"""
MARK = "    // ── FADE-IN ON LOAD (lazy images)"
OLD = ("    // ── WHY: COLONNADE", "    // ── WHY: FOUR PILLARS")

for path, lang in [("about-us.dc.html", "en"), ("about-us.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ WHY FURNISHIQ ━ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
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

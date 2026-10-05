import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
C = {
    "en": dict(
        label="Our Commitments", h2="The FurnishIQ Edge",
        intro="Three checkpoints built into every FurnishIQ project, placed exactly where decisions become hardest to reverse.",
        stages=["Brief", "Planning", "Design", "Procurement", "Build", "Handover"], gate="Checkpoint",
        cards=[
            ("Strategic DNA &amp; Brand-Led Planning", "Before any layout is drawn",
             "We study how a space will actually be used: footfall, service routes, staff movement and guest experience. The finished plan still works once the photographs are taken and the space is in daily use."),
            ("Photoreal Visual Certainty", "Before anything is purchased",
             "Every material, finish and light source is modelled and reviewed with you before it becomes a purchase order, because reworking a finished space costs far more than revising a render. Approvals happen on screen, not on site."),
            ("The Zero-Snag Promise", "At every phase of the build",
             "Snagging is treated as a design failure, not an expected final step. Our site teams inspect against the approved specification throughout the build, not only at handover, so the final walkthrough is simply a formality."),
        ],
    ),
    "ar": dict(
        label="التزاماتنا", h2="ميزة فيرنيش آي كيو",
        intro="ثلاث نقاط تحقق مدمجة في كل مشروع من مشاريع فيرنيش آي كيو، في اللحظات التي يصعب فيها التراجع عن القرار.",
        stages=["الإحاطة", "التخطيط", "التصميم", "التوريد", "التنفيذ", "التسليم"], gate="نقطة تحقق",
        cards=[
            ("الحمض النووي الاستراتيجي والتخطيط القائم على الهوية", "قبل رسم أي مخطط",
             "ندرس كيفية الاستخدام الفعلي للمساحة: حركة الزوار، ومسارات الخدمة، وتنقل الموظفين، وتجربة الضيوف. لتظل الخطة النهائية فعّالة بعد التقاط الصور وبدء الاستخدام اليومي للمساحة."),
            ("يقين بصري واقعي", "قبل أي عملية شراء",
             "يتم تصميم ومراجعة كل مادة وتشطيب ومصدر إضاءة معك قبل أن يتحول إلى أمر شراء، لأن إعادة العمل في مساحة منجزة تكلف أكثر بكثير من تعديل تصور رقمي. تتم الموافقات على الشاشة، لا في الموقع."),
            ("وعد الخلو التام من العيوب", "في كل مرحلة من مراحل التنفيذ",
             "نتعامل مع العيوب باعتبارها إخفاقاً في التصميم، لا خطوة نهائية متوقعة. تفحص فرقنا الميدانية المطابقة للمواصفات المعتمدة طوال التنفيذ، وليس فقط عند التسليم، بحيث تصبح الجولة النهائية مجرد إجراء شكلي."),
        ],
    ),
}


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    cards = "".join(f"""
      <article class="gt-card" style="--i:{i};">
        <div class="gt-top"><span class="gt-when">{when}</span><span class="gt-num" dir="ltr">0{i + 1}</span></div>
        <h3 class="gt-t">{t}</h3>
        <p class="gt-d">{d}</p>
        <span class="gt-stem" aria-hidden="true"></span>
      </article>""" for i, (t, when, d) in enumerate(c["cards"]))
    marks = "".join(f'<span class="gt-mark" style="--i:{i};"><i></i><b>{c["gate"]} <span dir="ltr">0{i + 1}</span></b></span>' for i in range(3))
    stages = "".join(f'<span class="gt-stage">{s}</span>' for s in c["stages"])
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ THREE PILLARS ━ -->
<section id="edge-gates" data-gates{' dir="rtl"' if ar else ''} style="position:relative;background:#3A2D25;color:#F5F2ED;padding:clamp(64px,8vw,100px) clamp(24px,5vw,80px);overflow:hidden;">
  <style>
    #edge-gates .gt-wrap{{position:relative;z-index:2;max-width:1280px;margin:0 auto;}}
    #edge-gates .gt-bg{{position:absolute;left:0;right:0;top:-12%;height:124%;z-index:0;pointer-events:none;will-change:transform;}}
    #edge-gates .gt-bg img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 55%;{'transform:scaleX(-1) scale(1.12);' if ar else 'transform:scale(1.12);'}transition:transform 2.8s {EASE};}}
    #edge-gates.is-in .gt-bg img{{{'transform:scaleX(-1) scale(1);' if ar else 'transform:scale(1);'}}}
    #edge-gates .gt-shade{{position:absolute;inset:0;z-index:1;background:rgba(38,28,22,0.8);pointer-events:none;}}
    #edge-gates .gt-head{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,5fr);gap:clamp(32px,5vw,96px);align-items:end;margin-bottom:clamp(48px,6vw,80px);}}
    #edge-gates .gt-label{{display:flex;align-items:center;gap:16px;margin-bottom:20px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#D6C2A8;}}
    #edge-gates .gt-label i{{display:block;width:32px;height:1px;background:#D6C2A8;}}
    #edge-gates .gt-h2{{font-family:{font};font-size:clamp(30px,3.6vw,56px);font-weight:500;line-height:1.1;letter-spacing:{'normal' if ar else '-0.02em'};color:#FFFFFF;margin:0;}}
    #edge-gates .gt-intro{{font-family:{font};font-size:{'17px' if ar else '16px'};line-height:1.75;color:rgba(245,242,237,0.7);margin:0;max-width:440px;}}
    #edge-gates .gt-cards{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(20px,2.4vw,40px);}}
    #edge-gates .gt-card{{position:relative;display:flex;flex-direction:column;padding:clamp(24px,2.4vw,36px) clamp(20px,2vw,32px) clamp(28px,2.8vw,40px);border:1px solid rgba(214,194,168,0.2);background:rgba(30,22,16,0.5);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);opacity:0;transform:translateY(24px);transition:opacity 0.8s {EASE} calc(0.6s + var(--i) * 0.8s),transform 0.8s {EASE} calc(0.6s + var(--i) * 0.8s),border-color 0.4s {EASE},background 0.4s {EASE};}}
    #edge-gates .gt-card:hover{{border-color:rgba(214,194,168,0.5);background:rgba(30,22,16,0.68);}}
    #edge-gates .gt-top{{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin-bottom:clamp(16px,1.6vw,24px);}}
    #edge-gates .gt-num{{font-family:'Lama Sans',sans-serif;font-size:clamp(44px,4vw,68px);line-height:0.8;letter-spacing:-0.03em;color:rgba(214,194,168,0.18);flex-shrink:0;}}
    #edge-gates .gt-when{{font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#D6C2A8;padding-top:4px;line-height:1.6;}}
    #edge-gates .gt-t{{font-family:{font};font-size:clamp(19px,1.6vw,24px);font-weight:500;line-height:1.3;color:#FFFFFF;margin:0;}}
    #edge-gates .gt-d{{font-family:{font};font-size:{'15px' if ar else '14px'};line-height:1.75;color:rgba(245,242,237,0.66);margin:16px 0 0;}}
    #edge-gates .gt-stem{{position:absolute;top:100%;left:50%;width:1px;height:clamp(36px,4vw,56px);background:rgba(214,194,168,0.5);transform:scaleY(0);transform-origin:top;transition:transform 0.6s {EASE} calc(0.35s + var(--i) * 0.8s);}}
    #edge-gates .gt-line{{position:relative;margin-top:clamp(36px,4vw,56px);height:1px;}}
    #edge-gates .gt-line::before{{content:"";position:absolute;inset:0;background:rgba(214,194,168,0.18);}}
    #edge-gates .gt-line::after{{content:"";position:absolute;inset:0;background:#D6C2A8;transform:scaleX(0);transform-origin:{'right' if ar else 'left'};transition:transform 2.6s cubic-bezier(0.45,0,0.55,1) 0.2s;}}
    #edge-gates .gt-marks{{position:absolute;inset:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(20px,2.4vw,40px);}}
    #edge-gates .gt-mark{{position:relative;display:flex;justify-content:center;}}
    #edge-gates .gt-mark i{{position:absolute;top:-7px;width:14px;height:14px;transform:rotate(45deg) scale(0.6);border:1px solid rgba(214,194,168,0.5);background:#2A1F18;transition:transform 0.5s {EASE} calc(0.6s + var(--i) * 0.8s),background 0.5s {EASE} calc(0.6s + var(--i) * 0.8s),box-shadow 0.5s {EASE} calc(0.6s + var(--i) * 0.8s);}}
    #edge-gates .gt-mark b{{position:absolute;top:18px;font-weight:500;white-space:nowrap;font-family:{font};font-size:{'11px' if ar else '9px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;color:#D6C2A8;opacity:0;transition:opacity 0.5s {EASE} calc(0.8s + var(--i) * 0.8s);}}
    #edge-gates .gt-stages{{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));margin-top:clamp(48px,5vw,64px);}}
    #edge-gates .gt-stage{{position:relative;padding-top:14px;text-align:center;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;color:rgba(245,242,237,0.45);}}
    #edge-gates .gt-stage::before{{content:"";position:absolute;top:0;left:50%;width:1px;height:8px;background:rgba(214,194,168,0.35);}}
    #edge-gates .gt-stages-wrap{{position:relative;}}
    #edge-gates .gt-stages-wrap::before{{content:"";position:absolute;top:0;left:0;right:0;height:1px;background:rgba(214,194,168,0.12);}}
    #edge-gates.is-in .gt-card{{opacity:1;transform:none;}}
    #edge-gates.is-in .gt-stem{{transform:scaleY(1);}}
    #edge-gates.is-in .gt-line::after{{transform:scaleX(1);}}
    #edge-gates.is-in .gt-mark i{{transform:rotate(45deg) scale(1);background:#D6C2A8;box-shadow:0 0 0 6px rgba(214,194,168,0.14);}}
    #edge-gates.is-in .gt-mark b{{opacity:1;}}
    @media(max-width:900px){{
      #edge-gates .gt-head{{grid-template-columns:1fr;gap:20px;}}
      #edge-gates .gt-cards{{grid-template-columns:1fr;gap:20px;}}
      #edge-gates .gt-stem,#edge-gates .gt-line,#edge-gates .gt-stages{{display:none;}}
      #edge-gates .gt-card{{border-inline-start:2px solid #D6C2A8;}}
      #edge-gates .gt-shade{{background:rgba(38,28,22,0.84);}}
    }}
    @media(prefers-reduced-motion:reduce){{
      #edge-gates *{{transition:none!important;}}
    }}
  </style>
  <div class="gt-bg" aria-hidden="true"><img src="uploads/about-edge-najdi-colonnade-checkpoints-2560.webp" srcset="uploads/about-edge-najdi-colonnade-checkpoints-1200.webp 1200w, uploads/about-edge-najdi-colonnade-checkpoints-2560.webp 2560w" sizes="100vw" alt="" width="2560" height="1429" loading="lazy" decoding="async"></div>
  <span class="gt-shade" aria-hidden="true"></span>
  <div class="gt-wrap">
    <div class="gt-head" data-reveal style="opacity:0;transform:translateY(18px);transition:opacity 0.8s {EASE},transform 0.8s {EASE};">
      <div>
        <div class="gt-label"><i></i>{c['label']}</div>
        <h2 class="gt-h2">{c['h2']}</h2>
      </div>
      <p class="gt-intro">{c['intro']}</p>
    </div>
    <div class="gt-cards">{cards}
    </div>
    <div class="gt-line" aria-hidden="true"><div class="gt-marks">{marks}</div></div>
    <div class="gt-stages-wrap" aria-hidden="true"><div class="gt-stages">{stages}</div></div>
  </div>
</section>
"""


JS = """    // ── EDGE: THREE CHECKPOINTS ON THE PROJECT TIMELINE ──────────────────────
    {
      const gt = document.querySelector('[data-gates]');
      if (gt) {
        if (reduced) gt.classList.add('is-in');
        else {
          const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { gt.classList.add('is-in'); io.disconnect(); } }, { threshold: 0.3 });
          io.observe(gt.querySelector('.gt-cards'));
          // background drifts slower than the page
          const bg = gt.querySelector('.gt-bg');
          let ticking = false;
          const drift = () => {
            ticking = false;
            const r = gt.getBoundingClientRect(), vh = window.innerHeight;
            if (r.bottom < 0 || r.top > vh) return;
            const p = (vh - r.top) / (vh + r.height) - 0.5;
            bg.style.transform = 'translate3d(0,' + (p * r.height * 0.18).toFixed(1) + 'px,0)';
          };
          drift();
          window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(drift); } }, { passive: true });
          window.addEventListener('resize', drift);
        }
      }
    }

"""
MARK = "    // ── FADE-IN ON LOAD (lazy images)"

for path, lang in [("about-us.dc.html", "en"), ("about-us.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ THREE PILLARS ━ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── EDGE: THREE CHECKPOINTS"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

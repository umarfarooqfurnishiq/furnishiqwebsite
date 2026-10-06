import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
C = {
    "en": dict(
        label="Our Methodology", h2="A Transparent<br>Journey", hint="Scroll to build the room", cta1="Book a Consultation", cta2="Discover Projects", pre="",
        steps=[
            ("Discover", "Site survey", "Goal setting, thorough site surveys, and budget alignment to ensure your project is grounded in reality from day one."),
            ("Design", "Design intent", "Development of layouts and mood boards, culminating in high-definition 3D visuals required for your final approval."),
            ("Build", "On site", "Our team takes over the site with strict programme certainty, maintaining the highest quality standards and safety protocols throughout construction."),
            ("Handover", "Handed over", "A zero-snag completion followed by dedicated aftercare, ensuring your new environment performs perfectly from the first day."),
        ],
        alt="Grand majlis with travertine walls, walnut coffered ceiling and carved timber arches",
    ),
    "ar": dict(
        label="منهجيتنا", h2="رحلة شفافة", hint="مرّر لبناء المساحة", cta1="احجز استشارة", cta2="اكتشف مشاريعنا", pre="/ar",
        steps=[
            ("الاكتشاف", "المسح الميداني", "تحديد الأهداف، ومسوحات ميدانية شاملة، ومواءمة الميزانية لضمان أن يكون مشروعك قائماً على أساس واقعي منذ اليوم الأول."),
            ("التصميم", "فكرة التصميم", "تطوير المخططات ولوحات الإلهام، وصولاً إلى تصورات ثلاثية الأبعاد عالية الدقة اللازمة لاعتمادك النهائي."),
            ("التنفيذ", "قيد التنفيذ", "يتولى فريقنا الموقع بضمان صارم للجدول الزمني، مع الحفاظ على أعلى معايير الجودة وبروتوكولات السلامة طوال مدة البناء."),
            ("التسليم", "تم التسليم", "إنجاز خالٍ تماماً من العيوب تتبعه رعاية مخصصة بعد التسليم، لضمان أداء بيئتك الجديدة بشكل مثالي منذ اليوم الأول."),
        ],
        alt="مجلس كبير بجدران من الترافرتين وسقف من خشب الجوز وأقواس خشبية منحوتة",
    ),
}

# survey overlay, drawn on the same 1920x1072 frame as the photo and the line drawing
P = 'pathLength="1"'
SURVEY = f"""
          <path {P} d="M667 313H1233V653H667Z"/>
          <path {P} d="M667 313L320 0M1233 313L1600 0M667 653L213 1020M1233 653L1707 1027"/>
          <path {P} class="jr-dim" d="M667 270H1233M667 256V284M1233 256V284"/>
          <path {P} class="jr-dim" d="M622 313V653M608 313H636M608 653H636"/>
          <path {P} class="jr-datum" d="M0 560H1920"/>
          <path {P} class="jr-x" d="M653 313H681M667 299V327M1219 313H1247M1233 299V327M653 653H681M667 639V667M1219 653H1247M1233 639V667"/>
          <circle {P} class="jr-x" cx="667" cy="313" r="16"/><circle {P} class="jr-x" cx="1233" cy="313" r="16"/>
          <circle {P} class="jr-x" cx="667" cy="653" r="16"/><circle {P} class="jr-x" cx="1233" cy="653" r="16"/>
"""
TEXTS = [(636, 300, "A"), (1254, 300, "B"), (1254, 684, "C"), (636, 684, "D"), (944, 252, "W"), (590, 490, "H"), (40, 548, "DATUM")]


def survey(ar):
    if not ar:
        tx = "".join(f'<text x="{x}" y="{y}">{t}</text>' for x, y, t in TEXTS)
        return SURVEY + f'\n          <g class="jr-tx">{tx}</g>'
    # mirrored room: geometry flips, labels are re-placed so they still read left to right
    tx = "".join(f'<text x="{1920 - x - (90 if t == "DATUM" else 14)}" y="{y}">{t}</text>' for x, y, t in TEXTS)
    return f'\n          <g transform="translate(1920 0) scale(-1 1)">{SURVEY}\n          </g>\n          <g class="jr-tx">{tx}</g>'


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    steps = "".join(f"""
        <li class="jr-step" data-jr-step style="--k:{i};">
          <span class="jr-bar"><i></i></span>
          <div class="jr-sh"><span class="jr-n" dir="ltr">0{i + 1}</span><h3 class="jr-t">{t}</h3></div>
          <p class="jr-d">{d}</p>
        </li>""" for i, (t, _, d) in enumerate(c["steps"]))
    stamps = "".join(f'<span class="jr-stamp{" is-active" if i == 0 else ""}" data-jr-stamp><b dir="ltr">0{i + 1} / 04</b>{s}</span>' for i, (_, s, _) in enumerate(c["steps"]))
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ FOUR-STEP PROCESS ━ -->
<section id="journey-section" data-journey{' dir="rtl"' if ar else ''} style="position:relative;background:#1E1610;height:540vh;">
  <style>
    #journey-section .jr-stage{{position:sticky;top:0;height:100vh;min-height:600px;display:flex;flex-direction:column;padding-top:80px;box-sizing:border-box;overflow:hidden;}}
    #journey-section .jr-view{{position:relative;flex:1;min-height:0;overflow:hidden;background:#1E1610;}}
    #journey-section .jr-view img,#journey-section .jr-survey{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 50%;}}
    #journey-section .jr-draw{{{'transform:scaleX(-1);' if ar else ''}opacity:var(--draw,0.22);mix-blend-mode:screen;z-index:2;}}
    #journey-section .jr-photo{{z-index:1;clip-path:inset(calc(var(--rise,100) * 1%) 0 0 0);filter:grayscale(var(--gray,1)) sepia(calc(var(--gray,1) * 0.25)) brightness(calc(0.72 + 0.28 * (1 - var(--gray,1)))) contrast(calc(0.9 + 0.1 * (1 - var(--gray,1))));transform:{'scaleX(-1) ' if ar else ''}scale(calc(1.06 - 0.06 * var(--settle,0)));}}
    #journey-section .jr-rise{{position:absolute;z-index:3;left:0;right:0;top:calc(var(--rise,100) * 1%);height:1px;background:#D6C2A8;opacity:var(--edge,0);box-shadow:0 0 0 1px rgba(214,194,168,0.12);}}
    #journey-section .jr-survey{{direction:ltr;z-index:4;opacity:var(--survey-o,1);fill:none;stroke:#D6C2A8;stroke-width:1.6;vector-effect:non-scaling-stroke;}}
    #journey-section .jr-survey path,#journey-section .jr-survey circle{{stroke-dasharray:1;stroke-dashoffset:calc(1 - var(--survey,0));}}
    #journey-section .jr-survey .jr-dim{{stroke-width:1;}}
    #journey-section .jr-survey .jr-datum{{stroke:#C9A27A;stroke-width:1;}}
    #journey-section .jr-survey .jr-x{{stroke:#F5F2ED;stroke-width:1.4;}}
    #journey-section .jr-tx{{fill:#D6C2A8;stroke:none;font-family:'Lama Sans',sans-serif;font-size:20px;letter-spacing:0.2em;opacity:var(--survey,0);}}
    #journey-section .jr-head{{position:absolute;z-index:5;top:80px;inset-inline-start:0;padding:clamp(24px,3.4vw,48px) clamp(24px,5vw,80px);max-width:86%;}}
    #journey-section .jr-label{{display:flex;align-items:center;gap:16px;margin-bottom:14px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:var(--ink2,#D6C2A8);}}
    #journey-section .jr-label i{{display:block;width:32px;height:1px;background:var(--ink2,#D6C2A8);}}
    #journey-section .jr-h2{{font-family:{font};font-size:clamp(28px,3.2vw,52px);font-weight:500;line-height:{'1.35' if ar else '1.08'};letter-spacing:{'normal' if ar else '-0.02em'};color:var(--ink,#FFFFFF);margin:0;}}
    #journey-section .jr-status{{display:grid;margin-top:18px;}}
    #journey-section .jr-cta{{display:inline-grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:clamp(20px,2.4vw,30px);opacity:var(--cta,0);transform:translateY(calc((1 - var(--cta,0)) * 36px));visibility:hidden;}}
    #journey-section.has-cta .jr-cta{{visibility:visible;}}
    #journey-section .jr-btn{{display:flex;align-items:center;justify-content:center;white-space:nowrap;gap:12px;padding:15px 26px;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;text-decoration:none;transition:gap 0.4s {EASE},background 0.4s {EASE},color 0.4s {EASE},border-color 0.4s {EASE};}}
    #journey-section .jr-btn--solid{{background:var(--ink,#FFFFFF);color:#F5F2ED;border:1px solid var(--ink,#FFFFFF);}}
    #journey-section .jr-btn--solid:hover,#journey-section .jr-btn--solid:focus-visible{{background:#8B6B4A;border-color:#8B6B4A;gap:18px;}}
    #journey-section .jr-btn--line{{color:var(--ink,#FFFFFF);border:1px solid var(--ink,#FFFFFF);}}
    #journey-section .jr-btn--line:hover,#journey-section .jr-btn--line:focus-visible{{background:var(--ink,#FFFFFF);color:#F5F2ED;}}
    #journey-section .jr-hint{{grid-area:1/1;display:flex;align-items:center;gap:12px;font-family:{font};font-size:{'12px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;color:var(--ink,#FFFFFF);opacity:calc(1 - var(--hint,0));}}
    #journey-section .jr-hint svg{{animation:jrBob 2.4s {EASE} infinite;}}
    @keyframes jrBob{{0%,100%{{transform:translateY(-2px);}}50%{{transform:translateY(3px);}}}}
    #journey-section .jr-stamps{{grid-area:1/1;display:grid;opacity:var(--hint,0);}}
    #journey-section .jr-stamp{{grid-area:1/1;justify-self:start;display:flex;align-items:center;gap:14px;padding:0;font-family:{font};font-size:{'13px' if ar else '11px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;color:var(--ink,#FFFFFF);opacity:0;transform:translateY(-6px);transition:opacity 0.5s {EASE},transform 0.5s {EASE};white-space:nowrap;}}
    #journey-section .jr-stamp.is-active{{opacity:1;transform:none;}}
    #journey-section .jr-stamp b{{font-family:'Lama Sans',sans-serif;font-weight:500;font-size:10px;letter-spacing:0.2em;color:var(--ink2,#D6C2A8);}}
    #journey-section .jr-steps{{list-style:none;margin:0;padding:clamp(22px,3vh,34px) clamp(24px,5vw,80px) clamp(26px,3.6vh,40px);display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(20px,2.6vw,48px);background:#1E1610;border-top:1px solid rgba(214,194,168,0.14);}}
    #journey-section .jr-step{{opacity:0.38;transition:opacity 0.6s {EASE};}}
    #journey-section .jr-step.is-done{{opacity:0.62;}}
    #journey-section .jr-step.is-active{{opacity:1;}}
    #journey-section .jr-bar{{display:block;height:2px;background:rgba(214,194,168,0.16);margin-bottom:clamp(14px,2vh,22px);overflow:hidden;}}
    #journey-section .jr-bar i{{display:block;height:100%;background:#D6C2A8;transform-origin:{'right' if ar else 'left'};transform:scaleX(var(--fill,0));}}
    #journey-section .jr-sh{{display:flex;align-items:baseline;gap:14px;}}
    #journey-section .jr-n{{font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.2em;color:#D6C2A8;}}
    #journey-section .jr-t{{font-family:{font};font-size:clamp(20px,1.8vw,28px);font-weight:500;letter-spacing:{'normal' if ar else '-0.015em'};color:#FFFFFF;margin:0;}}
    #journey-section .jr-d{{font-family:{font};font-size:{'14px' if ar else '13px'};line-height:1.7;color:rgba(245,242,237,0.66);margin:10px 0 0;max-width:340px;}}
    @media(max-width:900px){{
      #journey-section .jr-steps{{grid-template-columns:1fr;padding:20px 24px 26px;}}
      #journey-section .jr-step{{grid-area:1/1;opacity:0;transition:opacity 0.5s {EASE};}}
      #journey-section .jr-step.is-done{{opacity:0;}}
      #journey-section .jr-step.is-active{{opacity:1;}}
      #journey-section{{--ink:#FFFFFF!important;--ink2:#D6C2A8!important;}}
      #journey-section .jr-head{{position:relative;top:auto;max-width:none;padding:20px 24px 18px;background:#1E1610;}}
      #journey-section .jr-d{{max-width:none;}}
      #journey-section .jr-btn--solid{{background:#D6C2A8;border-color:#D6C2A8;color:#3A2D25;}}
      #journey-section .jr-btn{{padding:15px 20px;}}
      #journey-section .jr-cta{{display:grid;grid-template-columns:1fr;width:100%;}}
      #journey-section .jr-btn--line:hover,#journey-section .jr-btn--line:focus-visible{{background:#FFFFFF;color:#1E1610;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      #journey-section .jr-hint svg{{animation:none;}}
      #journey-section *{{transition:none!important;}}
    }}
  </style>
  <div class="jr-stage">
    <div class="jr-head">
      <div class="jr-label"><i></i>{c['label']}</div>
      <h2 class="jr-h2">{c['h2']}</h2>
      <div class="jr-status" aria-hidden="true">
      <div class="jr-hint"><svg width="12" height="16" viewBox="0 0 12 16" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M6 1v13M1.5 9.5L6 14l4.5-4.5"/></svg>{c['hint']}</div>
      <div class="jr-stamps">{stamps}</div>
      </div>
      <div class="jr-cta" data-jr-cta>
        <a class="jr-btn jr-btn--solid" href="{c['pre']}/contact">{c['cta1']}{('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>' if ar else '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>')}</a>
        <a class="jr-btn jr-btn--line" href="{c['pre']}/projects">{c['cta2']}</a>
      </div>
    </div>
    <div class="jr-view">
      <img class="jr-photo" src="uploads/courtyard-residence-grand-majlis-riyadh-1920.webp" srcset="uploads/courtyard-residence-grand-majlis-riyadh-1280.webp 1280w, uploads/courtyard-residence-grand-majlis-riyadh-1920.webp 1920w, uploads/courtyard-residence-grand-majlis-riyadh-2752.webp 2752w" sizes="100vw" alt="{c['alt']}" width="1920" height="1072" loading="lazy" decoding="async">
      <img class="jr-draw" src="uploads/grand-majlis-line-drawing-1920.webp" srcset="uploads/grand-majlis-line-drawing-1920.webp 1920w, uploads/grand-majlis-line-drawing-2752.webp 2752w" sizes="100vw" alt="" aria-hidden="true" width="1920" height="1072" loading="lazy" decoding="async">
      <span class="jr-rise" aria-hidden="true"></span>
      <svg class="jr-survey" viewBox="0 0 1920 1072" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{survey(ar)}
      </svg>
    </div>
    <ol class="jr-steps">{steps}
    </ol>
  </div>
</section>
"""


JS = """    // ── JOURNEY: ONE ROOM, FOUR STATES (scroll scrubs survey → drawing → build → handover) ──
    {
      const jr = document.querySelector('[data-journey]');
      if (jr) {
        const steps = [...jr.querySelectorAll('[data-jr-step]')], stamps = [...jr.querySelectorAll('[data-jr-stamp]')];
        const clamp = (v) => Math.min(Math.max(v, 0), 1);
        const ease = (t) => t * t * (3 - 2 * t);
        const seg = (p, a, b) => ease(clamp((p - a) / (b - a)));
        let cur = -1, ticking = false;
        const update = () => {
          ticking = false;
          const r = jr.getBoundingClientRect(), total = jr.offsetHeight - window.innerHeight;
          // the room builds over the first 80% of the scroll; the last stretch brings in the call to action
          const P = clamp(-r.top / (total || 1)), p = clamp(P / 0.8);
          const s = jr.style;
          const cta = seg(P, 0.84, 0.96);
          s.setProperty('--cta', cta.toFixed(4));
          jr.classList.toggle('has-cta', cta > 0.02);
          s.setProperty('--survey', seg(p, 0.02, 0.2).toFixed(4));
          s.setProperty('--survey-o', (1 - seg(p, 0.26, 0.36)).toFixed(4));
          s.setProperty('--hint', seg(p, 0.01, 0.08).toFixed(4));
          s.setProperty('--draw', (0.22 + 0.78 * seg(p, 0.24, 0.36) - seg(p, 0.66, 0.84)).toFixed(4));
          const rise = seg(p, 0.5, 0.72);
          s.setProperty('--rise', (100 - rise * 100).toFixed(3));
          s.setProperty('--edge', (rise > 0 && rise < 1 ? 1 : 0));
          s.setProperty('--gray', (1 - seg(p, 0.76, 0.92)).toFixed(4));
          s.setProperty('--settle', seg(p, 0.76, 1).toFixed(4));
          // text over the image: white on the dark drawing, walnut once the finished room is lit
          const t = seg(p, 0.8, 0.9), mix = (a, b) => a.map((v, i) => Math.round(v + (b[i] - v) * t)).join(',');
          s.setProperty('--ink', 'rgb(' + mix([255, 255, 255], [58, 45, 37]) + ')');
          s.setProperty('--ink2', 'rgb(' + mix([214, 194, 168], [91, 70, 54]) + ')');
          steps.forEach((st, k) => st.style.setProperty('--fill', clamp(p * 4 - k).toFixed(4)));
          const n = Math.min(Math.floor(p * 4), 3);
          if (n !== cur) {
            cur = n;
            steps.forEach((st, k) => { st.classList.toggle('is-active', k === n); st.classList.toggle('is-done', k < n); });
            stamps.forEach((st, k) => st.classList.toggle('is-active', k === n));
          }
        };
        update();
        // one wheel notch, one state: survey, drawing, build, handover, then the call (STEP SNAP)
        (window.fiqSnap = window.fiqSnap || []).push({ on: () => matchMedia('(min-width:901px) and (min-height:600px)').matches, geo: () => { const a = jr.getBoundingClientRect().top + window.scrollY, total = jr.offsetHeight - window.innerHeight; return { a, b: a + total, stops: [0.16, 0.352, 0.592, 0.8, 1].map((t) => a + total * t) }; } });
        window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
        window.addEventListener('resize', update);
      }
    }

"""
MARK = "    // ── FADE-IN ON LOAD (lazy images)"

for path, lang in [("about-us.dc.html", "en"), ("about-us.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ FOUR-STEP PROCESS ━ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── JOURNEY: ONE ROOM"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

"""Services hero: four disciplines, one roof.

Four tall image panels, one per service, rise in like curtains with the headline across them.
The panel under the pointer (or focus) widens and shows its tagline; while nobody interacts,
the panels take turns so the hero reads as something to explore. Each panel jumps to its section.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/services/svc_hero.py
"""
import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
PANELS = [  # (section id, image base, available widths, object-position, image aspect ratio)
    ("interior-design", "luxury-interior-design-material-board-riyadh", (600, 900, 1200), "50% 50%", 1.333),
    ("fitout", "luxury-villa-fit-out-travertine-staircase-walnut-wall-riyadh", (800, 1200, 1600), "40% 50%", 1.301),
    ("mep", "mep-ceiling-services-installation-riyadh", (600, 900, 1200), "50% 40%", 1.333),
    ("furniture", "furniture-gallery-living-room-set", (1280, 1920), "55% 50%", 1.791),
]
C = {
    "en": dict(
        eyebrow="What We Do", h1="Our Services",
        intro="Interior Design, Fit-Out, Engineering &amp; MEP, and Furniture Solutions — one integrated design-build studio, delivered end to end.",
        home="Home", here="Services", pre="", explore="Explore",
        names=["Interior Design", "Fit-Out", "Engineering &amp; MEP", "Furniture Solutions"],
        tags=["Where Inspiration Becomes Your Reality", "Total Spatial Transformation",
              "The Foundation of High-Performance Environments", "The Final Layer of Spatial Perfection"],
        alts=["Material board of stone, timber and fabric samples for a Riyadh interior",
              "Villa fit-out with a travertine staircase and walnut wall, Riyadh",
              "Ceiling services being installed above an interior, Riyadh",
              "Furnished living room set in a furniture gallery"],
        hint="Four disciplines. One roof.",
    ),
    "ar": dict(
        eyebrow="ما نقدمه", h1="خدماتنا",
        intro="التصميم الداخلي، التشطيبات، الهندسة والأنظمة الكهروميكانيكية، وحلول الأثاث — استوديو واحد متكامل للتصميم والتنفيذ، يُنجز كل شيء من البداية إلى النهاية.",
        home="الرئيسية", here="الخدمات", pre="/ar", explore="استكشف",
        names=["التصميم الداخلي", "التشطيبات", "الهندسة والأنظمة الكهروميكانيكية", "حلول الأثاث"],
        tags=["حيث يتحول الإلهام إلى واقعك", "تحول مكاني كامل",
              "أساس البيئات عالية الأداء", "الطبقة الأخيرة من الكمال المكاني"],
        alts=["لوحة مواد من الحجر والخشب والأقمشة لمشروع داخلي في الرياض",
              "تشطيب فيلا بدرج من الترافرتين وجدار من خشب الجوز، الرياض",
              "تركيب الأنظمة فوق السقف في مشروع داخلي، الرياض",
              "غرفة معيشة مؤثثة في معرض أثاث"],
        hint="أربعة تخصصات. سقف واحد.",
    ),
}
ARROW = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    panels = []
    for i, (sid, base, widths, pos, aspect) in enumerate(PANELS):
        ext = "webp"
        srcset = ", ".join(f"uploads/{base}-{w}.{ext} {w}w" for w in widths)
        mid = widths[-1] if len(widths) < 3 else widths[-2]
        panels.append(f'''      <a class="sh-p" href="#{sid}" data-sh-panel style="--i:{i};">
        <span class="sh-img"><img src="uploads/{base}-{mid}.{ext}" srcset="{srcset}" sizes="(max-width:760px) 100vw, {round(aspect * 100)}vh" alt="{c['alts'][i]}" style="object-position:{pos};" {'fetchpriority="high"' if i < 2 else 'loading="eager"'} decoding="async"></span>
        <span class="sh-veil" aria-hidden="true"></span>
        <span class="sh-meta">
          <span class="sh-n">0{i + 1}</span>
          <span class="sh-name">{c['names'][i]}</span>
          <span class="sh-more"><span class="sh-more-in"><span class="sh-tag">{c['tags'][i]}</span><span class="sh-go">{c['explore']}<span class="sh-arrow">{ARROW}</span></span></span></span>
        </span>
      </a>''')
    panels = "\n".join(panels)
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ HERO ━━ -->
<section data-svc-hero data-screen-label="Hero"{' dir="rtl"' if ar else ''} style="position:relative;background:#120D09;overflow:hidden;">
  <style>
    [data-svc-hero]{{height:100vh;min-height:680px;}}
    [data-svc-hero] .sh-panels{{position:absolute;inset:0;display:flex;}}
    [data-svc-hero] .sh-p{{position:relative;flex:1 1 0;min-width:0;overflow:hidden;display:block;color:#F5F2ED;text-decoration:none;clip-path:inset(100% 0 0 0);transition:flex-grow 1s {EASE},clip-path 1.3s cubic-bezier(0.77,0,0.18,1) calc(var(--i) * 0.14s);}}
    [data-svc-hero].is-ready .sh-p{{clip-path:inset(0 0 0 0);}}
    [data-svc-hero] .sh-p+.sh-p{{border-inline-start:1px solid rgba(214,194,168,0.16);}}
    [data-svc-hero] .sh-p.is-on{{flex-grow:2.3;}}
    [data-svc-hero] .sh-img{{position:absolute;inset:0;}}
    [data-svc-hero] .sh-img img{{width:100%;height:100%;object-fit:cover;transform:scale(1.12);transition:transform 1.8s {EASE};}}
    [data-svc-hero].is-ready .sh-img img{{transform:scale(1.04);}}
    [data-svc-hero] .sh-p.is-on .sh-img img{{transform:scale(1);}}
    [data-svc-hero] .sh-veil{{position:absolute;inset:0;background:rgba(18,13,9,0.66);transition:background 0.9s {EASE};}}
    [data-svc-hero] .sh-p.is-on .sh-veil{{background:rgba(18,13,9,0.38);}}
    [data-svc-hero] .sh-meta{{position:absolute;inset-inline:0;bottom:0;z-index:1;display:flex;flex-direction:column;gap:10px;padding:clamp(24px,2.6vw,44px);}}
    [data-svc-hero] .sh-n{{font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.2em;color:#D6C2A8;}}
    [data-svc-hero] .sh-name{{font-family:{font};font-size:clamp(18px,1.6vw,26px);line-height:1.25;color:#F5F2ED;}}
    [data-svc-hero] .sh-more{{display:grid;grid-template-rows:0fr;transition:grid-template-rows 0.8s {EASE};}}
    [data-svc-hero] .sh-p.is-on .sh-more{{grid-template-rows:1fr;}}
    [data-svc-hero] .sh-more-in{{overflow:hidden;display:flex;flex-direction:column;gap:18px;opacity:0;transform:translateY(12px);transition:opacity 0.6s {EASE},transform 0.6s {EASE};}}
    [data-svc-hero] .sh-p.is-on .sh-more-in{{opacity:1;transform:none;transition-delay:0.25s;}}
    [data-svc-hero] .sh-tag{{font-family:{font};font-size:{'16px' if ar else '15px'};line-height:1.6;color:rgba(245,242,237,0.82);max-width:30ch;}}
    [data-svc-hero] .sh-go{{display:inline-flex;align-items:center;gap:12px;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;color:#D6C2A8;}}
    [data-svc-hero] .sh-arrow{{display:inline-flex;transform:{'scaleX(-1)' if ar else 'none'};}}
    [data-svc-hero] .sh-p:focus-visible{{outline:1px solid #D6C2A8;outline-offset:-8px;}}
    [data-svc-hero] .sh-head{{position:absolute;inset-inline:0;top:clamp(130px,21vh,210px);z-index:2;pointer-events:none;padding:0 clamp(24px,5vw,80px);}}
    [data-svc-hero] .sh-head-in{{max-width:1280px;margin:0 auto;}}
    [data-svc-hero] .sh-eyebrow{{display:flex;align-items:center;gap:16px;margin-bottom:26px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:rgba(214,194,168,0.85);}}
    [data-svc-hero] .sh-eyebrow i{{display:block;width:32px;height:1px;background:#D6C2A8;}}
    [data-svc-hero] .sh-h1{{font-family:{font};font-weight:500;font-size:clamp(52px,8.4vw,136px);line-height:0.98;letter-spacing:{'0' if ar else '-0.025em'};color:#F5F2ED;margin:0;text-shadow:0 2px 40px rgba(18,13,9,0.45);}}
    [data-svc-hero] .sh-line{{display:block;overflow:hidden;padding-bottom:0.12em;margin-bottom:-0.12em;}}
    [data-svc-hero] .sh-line span{{display:block;transform:translateY(110%);transition:transform 1.2s {EASE} 0.55s;}}
    [data-svc-hero].is-ready .sh-line span{{transform:none;}}
    [data-svc-hero] .sh-intro{{max-width:520px;margin:clamp(22px,2.4vw,32px) 0 0;font-family:{font};font-size:{'17px' if ar else '15px'};line-height:1.85;color:rgba(245,242,237,0.82);text-shadow:0 1px 18px rgba(18,13,9,0.6);}}
    [data-svc-hero] .sh-crumb{{display:flex;align-items:center;gap:12px;margin-top:24px;pointer-events:auto;font-family:{font};font-size:{small};letter-spacing:{'normal' if ar else '0.26em'};text-transform:uppercase;}}
    [data-svc-hero] .sh-crumb a{{color:rgba(214,194,168,0.65);text-decoration:none;transition:color 0.3s {EASE};}}
    [data-svc-hero] .sh-crumb a:hover{{color:#D6C2A8;}}
    [data-svc-hero] .sh-crumb span{{color:rgba(214,194,168,0.9);}}
    [data-svc-hero] .sh-fade{{opacity:0;transform:translateY(16px);transition:opacity 0.9s {EASE} 0.95s,transform 0.9s {EASE} 0.95s;}}
    [data-svc-hero].is-ready .sh-fade{{opacity:1;transform:none;}}
    [data-svc-hero] .sh-roof{{position:absolute;top:calc(clamp(130px,21vh,210px) + 2px);inset-inline-end:max(clamp(24px,5vw,80px),calc((100% - 1280px) / 2));z-index:2;display:flex;align-items:center;gap:16px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:rgba(214,194,168,0.85);pointer-events:none;}}
    [data-svc-hero] .sh-roof i{{display:block;width:32px;height:1px;background:#D6C2A8;}}
    @media(max-width:760px){{
      [data-svc-hero]{{height:auto;min-height:0;display:flex;flex-direction:column;}}
      [data-svc-hero] .sh-head{{position:relative;top:auto;order:-1;padding:clamp(120px,18vh,150px) 24px 40px;}}
      [data-svc-hero] .sh-roof{{display:none;}}
      [data-svc-hero] .sh-panels{{position:relative;inset:auto;flex-direction:column;}}
      [data-svc-hero] .sh-p{{flex:none;height:104px;}}
      [data-svc-hero] .sh-p+.sh-p{{border-inline-start:none;border-top:1px solid rgba(214,194,168,0.16);}}
      [data-svc-hero] .sh-p.is-on{{flex-grow:0;}}
      [data-svc-hero] .sh-meta{{top:0;flex-direction:row;align-items:center;gap:18px;padding:0 24px;}}
      [data-svc-hero] .sh-more{{display:none;}}
      [data-svc-hero] .sh-p::after{{content:"";position:absolute;inset-inline-end:24px;top:50%;width:9px;height:9px;border-top:1px solid #D6C2A8;border-inline-end:1px solid #D6C2A8;transform:translateY(-50%) rotate({'-45deg' if ar else '45deg'});}}
      [data-svc-hero] .sh-veil,[data-svc-hero] .sh-p.is-on .sh-veil{{background:rgba(18,13,9,0.58);}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-svc-hero] *{{transition:none!important;}}
      [data-svc-hero] .sh-p{{clip-path:none;}}
      [data-svc-hero] .sh-line span,[data-svc-hero] .sh-fade{{transform:none;opacity:1;}}
    }}
  </style>
  <div class="sh-panels">
{panels}
  </div>
  <div class="sh-head">
    <div class="sh-head-in">
      <div class="sh-eyebrow sh-fade"><i></i>{c['eyebrow']}</div>
      <h1 class="sh-h1"><span class="sh-line"><span>{c['h1']}</span></span></h1>
      <p class="sh-intro sh-fade">{c['intro']}</p>
      <nav class="sh-crumb sh-fade" aria-label="Breadcrumb"><a href="{c['pre'] or '/'}">{c['home']}</a><span aria-hidden="true">/</span><span>{c['here']}</span></nav>
    </div>
  </div>
  <span class="sh-roof sh-fade" aria-hidden="true">{c['hint']}<i></i></span>
</section>
"""


JS = """    // ── SERVICES HERO: FOUR PANELS, ONE ROOF ─────────────────────────────────
    {
      const hero = document.querySelector('[data-svc-hero]');
      if (hero) {
        const panels = Array.from(hero.querySelectorAll('[data-sh-panel]'));
        const wide = window.matchMedia('(min-width: 761px)');
        let auto = !reduced, timer = null, idx = 0, visible = true;
        const set = (p) => panels.forEach((q) => q.classList.toggle('is-on', q === p));
        const step = () => { if (!auto || !visible || !wide.matches) return; set(panels[idx % panels.length]); idx++; };
        const stopAuto = () => { auto = false; clearInterval(timer); };
        panels.forEach((p) => {
          p.addEventListener('mouseenter', () => { stopAuto(); if (wide.matches) set(p); });
          p.addEventListener('focus', () => { stopAuto(); set(p); });
          p.addEventListener('click', (e) => {
            const t = document.getElementById(p.getAttribute('href').slice(1));
            if (t) { e.preventDefault(); t.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' }); }
          });
        });
        hero.querySelector('.sh-panels').addEventListener('mouseleave', () => { if (wide.matches) set(null); });
        new IntersectionObserver((es) => { visible = es[0].isIntersecting; }).observe(hero);
        requestAnimationFrame(() => requestAnimationFrame(() => hero.classList.add('is-ready')));
        if (auto) setTimeout(() => { step(); timer = setInterval(step, 3800); }, reduced ? 0 : 2300);
      }
    }

"""
MARK = "    // ── SCROLL REVEAL"

for path, lang in [("services.dc.html", "en"), ("services.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ HERO ━+ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── SERVICES HERO:"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

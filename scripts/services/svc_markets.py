"""Services, Markets We Serve: four sectors, one team.

A full-width accordion of the four sectors, each a panel lit by one of its concept projects. One panel is
open at a time: it widens to show the sector, a line on what it asks of a space, its concept projects with
their locations, and a link to that sector in the portfolio; the others narrow to tall slivers carrying
their name. A mouse resting on a panel opens it, as do a click, a tap and the arrow keys. On phones the
panels stack and open in height. The project list mirrors the portfolio, every entry labelled Concept.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/services/svc_markets.py
"""
import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
SECTORS = [  # filter key, image base, object-position, projects (slug)
    ("Residential", "courtyard-residence-grand-majlis-riyadh", "50% 50%", ["the-courtyard-residence", "obhur-beach-estate", "penthouse-above-the-wadi"]),
    ("Hospitality", "desert-stone-resort-lobby-lounge-alula", "55% 50%", ["desert-stone-resort", "roastery-house-flagship"]),
    ("Workplace", "executive-floors-sky-lobby-reception-riyadh", "45% 50%", ["the-executive-floors", "family-office-hq"]),
    ("Retail", "maison-joaillerie-main-salon-jeddah", "55% 50%", ["maison-de-joaillerie", "central-commons", "the-furniture-gallery"]),
]
C = {
    "en": dict(
        eyebrow="Markets We Serve", h2="One integrated team, delivering across every sector.",
        body="Four sectors, one team, accountable from concept to handover.",
        cta="View All Projects", href="/projects", base="",
        names=["Residential", "Hospitality", "Workplace", "Retail"],
        descs=["Villas, penthouses and family residences, planned around how a household lives, from the majlis to the private wing.",
               "Resorts, cafés and restaurants where atmosphere is part of the offer, built to perform through every service.",
               "Headquarters and executive floors that carry the brand and support the working day.",
               "Boutiques, galleries and destinations where the space presents the product and the brand."],
        go="View {} Projects", label="Concept projects", concept="Concept",
        projects={"the-courtyard-residence": ("The Courtyard Residence", "North Riyadh"), "obhur-beach-estate": ("Obhur Beach Estate", "North Jeddah"),
                  "penthouse-above-the-wadi": ("Penthouse Above the Wadi", "West Riyadh"), "desert-stone-resort": ("Desert Stone Resort", "AlUla"),
                  "roastery-house-flagship": ("Roastery House Flagship", "North Riyadh"), "the-executive-floors": ("The Executive Floors", "North Riyadh"),
                  "family-office-hq": ("Family Office HQ", "West Riyadh"), "maison-de-joaillerie": ("Maison de Joaillerie", "Jeddah"),
                  "central-commons": ("Central Commons", "Olaya, Riyadh"), "the-furniture-gallery": ("The Furniture Gallery", "North Riyadh")},
        alts=["Grand majlis with long linen seating beneath a coffered ceiling, The Courtyard Residence",
              "Resort lounge with full-height glazing onto the AlUla rocks, Desert Stone Resort",
              "Sky lobby reception with a walnut ceiling and the Riyadh skyline, The Executive Floors",
              "Jewellery salon with lit vitrines and a sculptural stair, Maison de Joaillerie"],
        list="Sectors",
    ),
    "ar": dict(
        eyebrow="القطاعات التي نخدمها", h2="فريق واحد متكامل، يُنجز في كل قطاع.",
        body="أربعة قطاعات وفريق واحد، مسؤول من المفهوم حتى التسليم.",
        cta="عرض جميع المشاريع", href="/ar/projects", base="/ar",
        names=["سكني", "ضيافة", "أماكن العمل", "تجزئة"],
        descs=["فلل وبنتهاوسات ومساكن عائلية، مخططة حول طريقة عيش الأسرة، من المجلس إلى الجناح الخاص.",
               "منتجعات ومقاهٍ ومطاعم تكون الأجواء فيها جزءاً من التجربة، ومُنفّذة لتؤدي في كل خدمة.",
               "مقرات رئيسية وطوابق تنفيذية تحمل هوية العلامة وتدعم يوم العمل.",
               "متاجر ومعارض ووجهات تقدم فيها المساحةُ المنتجَ والعلامة التجارية."],
        go="عرض مشاريع {}", label="تصورات تصميمية", concept="تصور تصميمي",
        projects={"the-courtyard-residence": ("مسكن الفناء", "شمال الرياض"), "obhur-beach-estate": ("دارة شاطئ أبحر", "شمال جدة"),
                  "penthouse-above-the-wadi": ("بنتهاوس فوق الوادي", "غرب الرياض"), "desert-stone-resort": ("منتجع الحجر الصحراوي", "العُلا"),
                  "roastery-house-flagship": ("بيت المحمصة — الفرع الرئيسي", "شمال الرياض"), "the-executive-floors": ("الطوابق التنفيذية", "شمال الرياض"),
                  "family-office-hq": ("مقر المكتب العائلي", "غرب الرياض"), "maison-de-joaillerie": ("دار المجوهرات", "جدة"),
                  "central-commons": ("الساحة المركزية", "العليا، الرياض"), "the-furniture-gallery": ("معرض الأثاث", "شمال الرياض")},
        alts=["مجلس كبير بجلسات طويلة من الكتان تحت سقف مُقسّم، مسكن الفناء",
              "صالة منتجع بواجهات زجاجية كاملة تطل على صخور العلا، منتجع الحجر الصحراوي",
              "استقبال الردهة العلوية بسقف من خشب الجوز وأفق الرياض، الطوابق التنفيذية",
              "صالون مجوهرات بواجهات عرض مضاءة ودرج منحوت، دار المجوهرات"],
        list="القطاعات",
    ),
}
ARROW_EN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
ARROW_AR = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>'


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    caps = "normal" if ar else "0.22em"
    small = "12px" if ar else "9px"
    arrow = ARROW_AR if ar else ARROW_EN
    panels = []
    for i, (key, img, pos, slugs) in enumerate(SECTORS):
        items = "".join(
            f'<li><a href="{c["base"]}/project-detail?project={s}" tabindex="-1"><span class="mk-pn">{c["projects"][s][0]}</span><span class="mk-pl">{c["concept"]} · {c["projects"][s][1]}</span></a></li>'
            for s in slugs)
        panels.append(f'''      <article class="mk-panel{' is-on' if i == 0 else ''}" data-mk="{i}">
        <img class="mk-img" src="uploads/{img}-1280.webp" srcset="uploads/{img}-1280.webp 1280w, uploads/{img}-1920.webp 1920w, uploads/{img}-2752.webp 2752w" sizes="(max-width:900px) 100vw, 64vw" alt="{c['alts'][i]}" style="object-position:{pos};" loading="lazy" decoding="async">
        <i class="mk-tint" aria-hidden="true"></i>
        <button type="button" class="mk-head" id="mk-head-{i}" aria-expanded="{'true' if i == 0 else 'false'}" aria-controls="mk-body-{i}"><span class="mk-n" dir="ltr">0{i + 1}</span><span class="mk-name">{c['names'][i]}</span></button>
        <div class="mk-body" id="mk-body-{i}" role="region" aria-labelledby="mk-head-{i}"{'' if i == 0 else ' aria-hidden="true"'}>
          <h3 class="mk-title">{c['names'][i]}</h3>
          <p class="mk-desc">{c['descs'][i]}</p>
          <p class="mk-label">{c['label']}</p>
          <ul class="mk-list">{items}</ul>
          <a class="mk-go" href="{c['base']}/projects?category={key}" tabindex="-1">{c['go'].format(c['names'][i])}{arrow}</a>
        </div>
      </article>''')
    panels = "\n".join(panels)
    PAD = "clamp(24px,5vw,80px)"
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5. MARKETS WE SERVE ━ -->
<section id="markets" data-screen-label="Markets We Serve" data-svc-markets{' dir="rtl"' if ar else ''} style="scroll-margin-top:var(--fiq-svc-offset,132px);background:#FFFFFF;color:#3A2D25;position:relative;padding:clamp(64px,8vw,100px) {PAD} 0;overflow:clip;">
  <style>
    [data-svc-markets] .mk-wrap{{max-width:1280px;margin:0 auto;}}
    [data-svc-markets] .mk-headrow{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:clamp(32px,5vw,88px);align-items:end;margin-bottom:clamp(40px,4.4vw,64px);}}
    [data-svc-markets] .mk-eyebrow{{display:flex;align-items:center;gap:16px;margin-bottom:24px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    [data-svc-markets] .mk-eyebrow i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    [data-svc-markets] .mk-h2{{font-family:{font};font-weight:500;font-size:clamp(32px,3.8vw,54px);line-height:1.08;letter-spacing:{'0' if ar else '-0.015em'};color:#1F1F1F;margin:0;text-wrap:balance;}}
    [data-svc-markets] .mk-intro{{font-family:{font};font-weight:500;font-size:{'clamp(22px,2vw,28px)' if ar else 'clamp(20px,1.9vw,26px)'};line-height:1.4;letter-spacing:{'0' if ar else '-0.005em'};text-wrap:balance;max-width:30ch;color:#3A2D25;margin:0 0 28px;}}
    [data-svc-markets] .mk-cta{{display:inline-flex;align-items:center;gap:12px;padding:17px 30px;background:#3A2D25;color:#F5F2ED;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;border:1px solid #3A2D25;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-markets] .mk-cta:hover,[data-svc-markets] .mk-cta:focus-visible{{background:transparent;color:#3A2D25;}}
    [data-svc-markets] .mk-rise{{opacity:0;transform:translateY(24px);transition:opacity 0.9s {EASE},transform 0.9s {EASE};}}
    [data-svc-markets].is-in .mk-rise{{opacity:1;transform:none;}}
    [data-svc-markets].is-in .mk-rise--2{{transition-delay:0.12s;}}
    [data-svc-markets].is-in .mk-rise--3{{transition-delay:0.24s;}}
    [data-svc-markets] .mk-row{{display:flex;height:clamp(520px,calc(100svh - var(--fiq-svc-offset,132px)),860px);margin-inline:calc(50% - 50vw + var(--mk-sb,0px) / 2);background:#1F1F1F;}}
    [data-svc-markets] .mk-panel{{position:relative;flex:1 1 0;min-width:0;overflow:hidden;border-inline-start:1px solid rgba(245,242,237,0.14);transition:flex-grow 0.9s {EASE};}}
    [data-svc-markets] .mk-panel:first-child{{border-inline-start:0;}}
    [data-svc-markets] .mk-panel.is-on{{flex-grow:3.4;}}
    /* the photograph keeps the open panel's width at all times, so it never rescales as the panels move */
    [data-svc-markets] .mk-img{{position:absolute;top:0;left:50%;height:100%;width:max(100%,64vw);object-fit:cover;transform:translateX(-50%) scale(1.04);transition:transform 1.6s {EASE};}}
    [data-svc-markets] .mk-panel.is-on .mk-img{{transform:translateX(-50%) scale(1);}}
    [data-svc-markets] .mk-tint{{position:absolute;inset:0;background:rgba(31,31,31,0.58);transition:background 0.9s {EASE};}}
    [data-svc-markets] .mk-panel:hover .mk-tint{{background:rgba(31,31,31,0.42);}}
    [data-svc-markets] .mk-panel.is-on .mk-tint{{background:rgba(31,31,31,0.12);}}
    [data-svc-markets] .mk-head{{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:space-between;align-items:flex-start;padding:clamp(24px,2.6vw,40px) clamp(20px,2vw,32px);border:0;background:none;color:#F5F2ED;text-align:start;cursor:pointer;}}
    [data-svc-markets] .mk-panel.is-on .mk-head{{cursor:default;}}
    [data-svc-markets] .mk-head:focus-visible{{outline:1px solid #D6C2A8;outline-offset:-8px;}}
    [data-svc-markets] .mk-n{{font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.22em;color:#D6C2A8;}}
    [data-svc-markets] .mk-name{{font-family:{font};font-weight:500;font-size:clamp(20px,1.8vw,26px);line-height:1.15;transition:opacity 0.4s {EASE};}}
    [data-svc-markets] .mk-panel.is-on .mk-name{{opacity:0;}}
    [data-svc-markets] .mk-body{{position:absolute;bottom:clamp(20px,2.4vw,36px);inset-inline-start:clamp(20px,2.4vw,36px);width:min(440px,calc(100% - 2 * clamp(20px,2.4vw,36px)));padding:clamp(24px,2.4vw,34px);background:rgba(31,31,31,0.78);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);color:#F5F2ED;opacity:0;visibility:hidden;transform:translateY(14px);transition:opacity 0.5s {EASE},transform 0.5s {EASE},visibility 0s linear 0.5s;}}
    [data-svc-markets] .mk-panel.is-on .mk-body{{opacity:1;visibility:visible;transform:none;transition-delay:0.45s,0.45s,0s;}}
    [data-svc-markets] .mk-title{{margin:0 0 12px;font-family:{font};font-weight:500;font-size:clamp(28px,2.8vw,40px);line-height:1.1;color:#F5F2ED;}}
    [data-svc-markets] .mk-desc{{margin:0 0 22px;font-family:{font};font-size:{'14px' if ar else '13px'};line-height:1.7;color:rgba(245,242,237,0.78);}}
    [data-svc-markets] .mk-label{{margin:0 0 6px;font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;color:#C4A882;}}
    [data-svc-markets] .mk-list{{list-style:none;margin:0 0 24px;padding:0;}}
    [data-svc-markets] .mk-list a{{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:11px 0;border-bottom:1px solid rgba(245,242,237,0.14);color:#F5F2ED;text-decoration:none;transition:color 0.3s {EASE},padding 0.4s {EASE};}}
    [data-svc-markets] .mk-list a:hover,[data-svc-markets] .mk-list a:focus-visible{{color:#D6C2A8;padding-inline-start:6px;}}
    [data-svc-markets] .mk-pn{{font-family:{font};font-size:{'15px' if ar else '14px'};}}
    [data-svc-markets] .mk-pl{{flex:none;font-family:{font};font-size:{'12px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.08em'};color:rgba(245,242,237,0.55);}}
    [data-svc-markets] .mk-go{{display:inline-flex;align-items:center;gap:12px;padding:15px 24px;background:#F5F2ED;color:#1F1F1F;border:1px solid #F5F2ED;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-markets] .mk-go:hover,[data-svc-markets] .mk-go:focus-visible{{background:transparent;color:#F5F2ED;}}
    @media(max-width:900px){{
      [data-svc-markets] .mk-headrow{{grid-template-columns:1fr;}}
      [data-svc-markets] .mk-row{{flex-direction:column;height:auto;}}
      [data-svc-markets] .mk-panel{{flex:none;height:96px;border-inline-start:0;border-top:1px solid rgba(245,242,237,0.14);transition:height 0.8s {EASE};}}
      [data-svc-markets] .mk-panel:first-child{{border-top:0;}}
      [data-svc-markets] .mk-panel.is-on{{height:min(640px,calc(100svh - 120px));}}
      [data-svc-markets] .mk-img{{width:100%;}}
      [data-svc-markets] .mk-head{{flex-direction:row;justify-content:flex-start;align-items:center;gap:16px;bottom:auto;height:96px;padding:0 24px;}}
      [data-svc-markets] .mk-panel.is-on .mk-name{{opacity:1;}}
      [data-svc-markets] .mk-body{{inset-inline:14px;bottom:14px;width:auto;}}
      [data-svc-markets] .mk-title{{display:none;}}
    }}
    @media(max-width:600px){{
      [data-svc-markets] .mk-cta{{width:100%;justify-content:center;box-sizing:border-box;}}
      [data-svc-markets] .mk-pl{{display:none;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-svc-markets] *{{transition:none!important;}}
      [data-svc-markets] .mk-rise{{opacity:1;transform:none;}}
    }}
  </style>
  <div class="mk-wrap">
    <div class="mk-headrow">
      <div class="mk-rise">
        <div class="mk-eyebrow"><i></i>{c['eyebrow']}</div>
        <h2 class="mk-h2">{c['h2']}</h2>
      </div>
      <div class="mk-rise mk-rise--2">
        <p class="mk-intro">{c['body']}</p>
        <a class="mk-cta" href="{c['href']}">{c['cta']}{arrow}</a>
      </div>
    </div>
    <div class="mk-row mk-rise mk-rise--3" aria-label="{c['list']}">
{panels}
    </div>
  </div>
</section>
"""


JS = """    // ── SERVICES, MARKETS: FOUR SECTORS, ONE TEAM ───────────────────────────
    {
      const sec = document.querySelector('[data-svc-markets]');
      if (sec) {
        const panels = Array.from(sec.querySelectorAll('.mk-panel')), heads = panels.map((p) => p.querySelector('.mk-head'));
        const rtl = sec.getAttribute('dir') === 'rtl';
        let idx = 0, settle = 0;
        const open = (i) => {
          if (i === idx) return;
          idx = i;
          panels.forEach((p, k) => {
            const on = k === i, body = p.querySelector('.mk-body');
            p.classList.toggle('is-on', on);
            heads[k].setAttribute('aria-expanded', on ? 'true' : 'false');
            body.setAttribute('aria-hidden', on ? 'false' : 'true');
            body.querySelectorAll('a').forEach((a) => { a.tabIndex = on ? 0 : -1; });
          });
        };
        open(-1); open(0);
        panels.forEach((p, k) => {
          // a mouse resting on a panel opens it after a beat, so sweeping across does not flicker through them all
          p.addEventListener('pointerenter', (e) => { if (e.pointerType !== 'mouse') return; clearTimeout(settle); settle = setTimeout(() => open(k), 140); });
          p.addEventListener('pointerleave', () => clearTimeout(settle));
          heads[k].addEventListener('click', () => open(k));
          heads[k].addEventListener('keydown', (e) => {
            const d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
            if (!d) return;
            e.preventDefault();
            const n = (k + ((rtl && (e.key === 'ArrowRight' || e.key === 'ArrowLeft')) ? -d : d) + panels.length) % panels.length;
            open(n); heads[n].focus();
          });
        });
        // 100vw counts the scrollbar; take it back out so the row meets both edges exactly
        const fit = () => sec.style.setProperty('--mk-sb', (window.innerWidth - document.documentElement.clientWidth) + 'px');
        fit();
        window.addEventListener('resize', fit);
        new IntersectionObserver((es, o) => { es.forEach((e) => { if (e.isIntersecting) { sec.classList.add('is-in'); o.disconnect(); } }); }, { rootMargin: '0px 0px -15% 0px' }).observe(sec);
      }
    }

"""
MARK = "    // ── SCROLL REVEAL"

for path, lang in [("services.dc.html", "en"), ("services.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ 5\. MARKETS WE SERVE ━ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── SERVICES, MARKETS:"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

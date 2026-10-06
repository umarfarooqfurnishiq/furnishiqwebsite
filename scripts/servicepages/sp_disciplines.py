"""Service pages, the disciplines: the designer's desk.

The template for the six-discipline section of the four service pages. One photograph, shot from above, of a
designer's desk holding an object for each discipline. The whole desk is shown at its own shape, never
cropped or enlarged, beside an index on dark walnut. The section holds while the page scrolls: a spotlight
travels from object to object, the rest of the desk dims, and the index shows that discipline's number, name
and description, with all six listed beneath to choose from. The desk opens and closes fully lit; once it closes, the sixth stays in the index and a call to book a
consultation fades up.
Shown at about 1100px wide from a 2400px photograph, it stays sharp on high-density screens. Pinned and
scroll-driven on desktop; on phones the desk sits above the text and the six play on their own.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/servicepages/sp_disciplines.py [page ...]
"""
import re, sys

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
PAGE = {
    "services-interior-design": dict(
        img="interior-design-disciplines-designer-desk", widths=(1280, 1920, 2400), size=(2400, 1792),
        # each object on the desk as (left, top, width, height) in % of the photograph
        spots=[(4.5, 8, 30.5, 36), (40.5, 11.4, 24.3, 25.4), (72, 9.7, 25, 30.5),
               (5, 56.6, 25, 33.2), (37.7, 63, 25.8, 26.8), (70, 62.6, 26, 27.2)],
        en=dict(
            eyebrow="Our Design Disciplines", h2="Every Detail, Considered.",
            sub="Six disciplines on one desk, one team accountable from first plan to final styling.",
            names=["Space Planning & Layout", "Photoreal 3D Visualization", "Material & Finish Selection",
                   "Lighting Design", "Color & Mood Board Curation", "Styling & Detailing"],
            descs=["Functional layouts, spatial flow, and circulation studies built around how you live and work.",
                   "High-definition renders and virtual walkthroughs for full design approval before a single wall comes down.",
                   "Stone, wood, tile, and texture curation, from sample boards through to final client sign-off.",
                   "Ambient, task, and accent lighting strategies, from fixture selection to final placement.",
                   "Curated palettes and concept presentations, aligned to your brand from the first mood board.",
                   "Final detailing, art and decor curation, and a dedicated aftercare walkthrough."],
            alt="A designer's walnut desk from above: a majlis floor plan, a tablet showing a render, travertine, walnut, boucle and brass samples, a brass lamp with its specification sheet, a mood board, and a vase, books and a bronze bowl",
            tabs="Design disciplines", cta="Book Free Consultation", cta_href="#contact"),
        ar=dict(
            eyebrow="تخصصات التصميم لدينا", h2="كل تفصيلة، بعناية.",
            sub="ستة تخصصات على طاولة واحدة، وفريق واحد مسؤول من المخطط الأول حتى التنسيق النهائي.",
            names=["تخطيط المساحات والتصميم", "تصور ثلاثي الأبعاد واقعي", "اختيار المواد والتشطيبات",
                   "تصميم الإضاءة", "اختيار الألوان ولوحات الإلهام", "التنسيق والتفاصيل النهائية"],
            descs=["تصاميم وظيفية، وتدفق مكاني، ودراسات حركة مبنية على أسلوب حياتك وعملك.",
                   "عروض عالية الدقة وجولات افتراضية لاعتماد التصميم كاملاً قبل هدم أي جدار.",
                   "اختيار الحجر والخشب والبلاط والملمس، من لوحات العينات وحتى الاعتماد النهائي للعميل.",
                   "استراتيجيات إضاءة محيطية ووظيفية وتركيزية، من اختيار التجهيزات إلى التموضع النهائي.",
                   "لوحات ألوان منسقة وعروض مفاهيمية متوافقة مع هويتك منذ أول لوحة إلهام.",
                   "التفاصيل النهائية، وتنسيق الأعمال الفنية والديكور، وجولة عناية مخصصة بعد التسليم."],
            alt="طاولة مصمم من خشب الجوز من الأعلى: مخطط مجلس، وجهاز لوحي يعرض تصوراً، وعينات ترافرتين وجوز وبوكليه ونحاس، ومصباح نحاسي مع ورقة مواصفاته، ولوحة إلهام، ومزهرية وكتب ووعاء برونزي",
            tabs="تخصصات التصميم", cta="احجز استشارة مجانية", cta_href="#contact"),
    ),
    "services-fitout": dict(
        img="fitout-disciplines-site-desk", widths=(1280, 1920, 2400), size=(2400, 1792),
        spots=[(3, 6, 32, 58), (37.6, 8.2, 29.2, 29), (71.8, 7.4, 24, 39.6),
               (3.8, 67, 33.8, 24.6), (41, 60.6, 30.2, 31), (74.8, 62.2, 20.2, 28.2)],
        en=dict(
            eyebrow="Our Fit-Out Scope", h2="Every Phase, In-House.",
            sub="Six fit-out disciplines on one desk, one site team accountable from first partition to final styling.",
            names=["Space Planning & Layout", "Partitions, Walls & Ceilings", "Flooring & Wall Finishes",
                   "Joinery & Millwork", "MEP Coordination", "Furniture, FF&E & Styling"],
            descs=["Brand-led layouts, zoning, and photoreal 3D visualization before a single wall is built.",
                   "Gypsum partitions, suspended ceilings, acoustic treatment, and fire-rated assemblies.",
                   "Natural stone, timber, decorative cladding, and protective sealing across every surface.",
                   "Bespoke cabinetry, reception counters, custom hardware, and built-in storage.",
                   "Electrical, HVAC, plumbing, and fire safety systems coordinated in-house from day one.",
                   "Procurement, fixtures, soft furnishings, and final styling through to handover."],
            alt="A walnut desk from above: a zoned floor plan with a scale ruler, a gypsum and stud sample on a ceiling tile, travertine, oak and mosaic floor samples, a walnut drawer front with a brass pull, an MEP drawing with a pipe elbow, and a fabric swatch with a model chair",
            tabs="Fit-out disciplines", cta="Request a Fit-Out Quote", cta_href="#contact"),
        ar=dict(
            eyebrow="نطاق التشطيبات لدينا", h2="كل مرحلة، داخلياً.",
            sub="ستة تخصصات تشطيب على طاولة واحدة، وفريق موقع واحد مسؤول من أول قاطع حتى التنسيق النهائي.",
            names=["تخطيط المساحات والتوزيع", "القواطع والجدران والأسقف", "الأرضيات وتشطيبات الجدران",
                   "النجارة والأعمال الخشبية", "تنسيق الأنظمة الكهروميكانيكية", "الأثاث والتجهيزات والتنسيق النهائي"],
            descs=["تخطيطات قائمة على الهوية، تقسيم للمناطق، وتصور ثلاثي الأبعاد واقعي قبل بناء أي جدار.",
                   "قواطع الجبس، الأسقف المعلقة، المعالجة الصوتية، وتجميعات مقاومة للحريق.",
                   "الحجر الطبيعي، الخشب، الكسوة الزخرفية، والعزل الحمائي لكل سطح.",
                   "خزائن مصممة خصيصًا، مكاتب استقبال، تجهيزات مخصصة، وحلول تخزين مدمجة.",
                   "أنظمة الكهرباء والتكييف والسباكة والسلامة من الحرائق منسّقة داخليًا منذ اليوم الأول.",
                   "التوريد، التجهيزات، المفروشات، والتنسيق النهائي وصولاً إلى التسليم."],
            alt="طاولة من خشب الجوز من الأعلى: مخطط موزّع بالألوان مع مسطرة قياس، وعينة جبس ومقطع معدني على بلاطة سقف، وعينات أرضيات من الترافرتين والبلوط والفسيفساء، وواجهة درج من الجوز بمقبض نحاسي، ومخطط أنظمة كهروميكانيكية مع كوع أنبوب، وعينة قماش مع نموذج كرسي",
            tabs="تخصصات التشطيب", cta="اطلب عرض سعر للتشطيب", cta_href="#contact"),
    ),
}

ARROW = {
    "en": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
    "ar": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>',
}


def build(page, lang):
    ar = lang == "ar"
    P = PAGE[page]
    c = P[lang]
    n = len(P["spots"])
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    PAD = "clamp(24px,5vw,80px)"
    W, H = P["size"]
    srcset = ", ".join(f"uploads/{P['img']}-{w}.webp {w}w" for w in P["widths"])
    spots = "|".join(",".join(str(v) for v in s) for s in P["spots"])
    panes = "\n".join(f'''          <div class="dk-pane" data-dk-pane="{k}">
            <h3 class="dk-name">{c['names'][k]}</h3>
            <p class="dk-desc">{c['descs'][k]}</p>
          </div>''' for k in range(n))
    items = "\n".join(f'''          <li><button type="button" class="dk-tab" data-dk-tab="{k}"><i class="dk-prog" aria-hidden="true"></i><span class="dk-n" dir="ltr">0{k + 1}</span><span class="dk-t">{c['names'][k]}</span></button></li>''' for k in range(n))
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ SCOPE ━━━━━━━━━━━━━ -->
<section id="disciplines" data-screen-label="Scope" data-sp-disc{' dir="rtl"' if ar else ''} style="scroll-margin-top:80px;background:#F5F2ED;color:#3A2D25;position:relative;padding:clamp(80px,10vw,128px) {PAD} 0;overflow:clip;">
  <style>
    [data-sp-disc] .dk-wrap{{max-width:1280px;margin:0 auto;}}
    [data-sp-disc] .dk-head{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:clamp(32px,5vw,88px);align-items:end;margin-bottom:clamp(40px,4.4vw,64px);}}
    [data-sp-disc] .dk-eyebrow{{display:flex;align-items:center;gap:16px;margin:0 0 24px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    [data-sp-disc] .dk-eyebrow i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    [data-sp-disc] .dk-h2{{margin:0;font-family:{font};font-weight:500;font-size:clamp(32px,3.8vw,54px);line-height:1.08;letter-spacing:{'0' if ar else '-0.015em'};color:#1F1F1F;text-wrap:balance;}}
    [data-sp-disc] .dk-sub{{margin:0;max-width:{'18em' if ar else '30ch'};font-family:{font};font-weight:500;font-size:{'clamp(22px,2vw,28px)' if ar else 'clamp(20px,1.9vw,26px)'};line-height:1.4;letter-spacing:{'0' if ar else '-0.005em'};color:#3A2D25;text-wrap:balance;}}
    [data-sp-disc] .dk-rise{{opacity:0;transform:translateY(24px);transition:opacity 0.9s {EASE},transform 0.9s {EASE};}}
    [data-sp-disc].is-in .dk-rise{{opacity:1;transform:none;}}
    [data-sp-disc].is-in .dk-rise--2{{transition-delay:0.12s;}}
    [data-sp-disc].is-in .dk-rise--3{{transition-delay:0.24s;}}
    /* the block: the whole desk at its own shape beside the index, on dark walnut */
    [data-sp-disc] .dk-block{{position:relative;margin-inline:calc(50% - 50vw + var(--dk-sb,0px) / 2);background:#2B211A;}}
    [data-sp-disc] .dk-stage{{display:flex;align-items:center;gap:clamp(32px,4.4vw,88px);height:calc(100vh - 80px);height:calc(100svh - 80px);min-height:560px;padding:clamp(24px,4vh,48px) {PAD};padding-inline-start:clamp(24px,3vw,56px);box-sizing:border-box;}}
    [data-sp-disc] .dk-photo{{position:relative;flex:none;width:min(62%,calc((100svh - 80px - 2 * clamp(24px,4vh,48px)) * {W} / {H}));aspect-ratio:{W}/{H};overflow:hidden;box-shadow:0 24px 80px rgba(0,0,0,0.35);}}
    [data-sp-disc] .dk-photo img{{position:absolute;inset:0;width:100%;height:100%;display:block;}}
    [data-sp-disc] .dk-spot{{position:absolute;left:var(--sx,0%);top:var(--sy,0%);width:var(--sw,100%);height:var(--sh,100%);box-shadow:0 0 0 300vmax rgba(20,15,11,var(--dim,0));transition:left 0.9s {EASE},top 0.9s {EASE},width 0.9s {EASE},height 0.9s {EASE},box-shadow 0.8s {EASE};pointer-events:none;}}
    [data-sp-disc] .dk-spot::before,[data-sp-disc] .dk-spot::after{{content:"";position:absolute;width:18px;height:18px;border:0 solid #D6C2A8;opacity:var(--mk,0);transition:opacity 0.5s {EASE};}}
    [data-sp-disc] .dk-spot::before{{top:-5px;left:-5px;border-width:1.5px 0 0 1.5px;}}
    [data-sp-disc] .dk-spot::after{{bottom:-5px;right:-5px;border-width:0 1.5px 1.5px 0;}}
    /* the index */
    [data-sp-disc] .dk-side{{flex:1;min-width:0;max-width:520px;display:flex;flex-direction:column;color:#F5F2ED;}}
    [data-sp-disc] .dk-count{{margin:0 0 clamp(14px,2vh,22px);font-family:'Lama Sans',sans-serif;font-size:12px;letter-spacing:0.2em;color:rgba(245,242,237,0.5);}}
    [data-sp-disc] .dk-count b{{display:inline-block;min-width:1.4em;font-weight:500;font-size:clamp(40px,3.6vw,60px);letter-spacing:-0.02em;color:#D6C2A8;margin-inline-end:6px;}}
    [data-sp-disc] .dk-panes{{display:grid;min-height:clamp(120px,16vh,160px);}}
    /* the closing call, which fades up once the desk is lit again after the sixth */
    [data-sp-disc] .dk-end{{margin-top:clamp(16px,2.4vh,28px);opacity:0;visibility:hidden;transform:translateY(14px);transition:opacity 0.7s {EASE},transform 0.7s {EASE},visibility 0s linear 0.7s;}}
    [data-sp-disc].is-end .dk-end{{opacity:1;visibility:visible;transform:none;transition-delay:0.2s,0.2s,0s;}}
    [data-sp-disc] .dk-cta{{display:inline-flex;align-items:center;gap:14px;padding:17px 30px;background:#D6C2A8;color:#1F1F1F;border:1px solid #D6C2A8;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-sp-disc] .dk-cta:hover,[data-sp-disc] .dk-cta:focus-visible{{background:transparent;color:#D6C2A8;}}
    [data-sp-disc] .dk-pane{{grid-area:1/1;opacity:0;visibility:hidden;transform:translateY(10px);transition:opacity 0.5s {EASE},transform 0.5s {EASE},visibility 0s linear 0.5s;}}
    [data-sp-disc] .dk-pane.is-on{{opacity:1;visibility:visible;transform:none;transition-delay:0.15s,0.15s,0s;}}
    [data-sp-disc] .dk-name{{margin:0 0 12px;font-family:{font};font-weight:500;font-size:clamp(26px,2.5vw,40px);line-height:1.15;color:#F5F2ED;text-wrap:balance;}}
    [data-sp-disc] .dk-desc{{margin:0;font-family:{font};font-size:{'16px' if ar else '15px'};line-height:1.75;color:rgba(245,242,237,0.78);}}
    [data-sp-disc] .dk-list{{list-style:none;margin:clamp(20px,3vh,36px) 0 0;padding:0;border-top:1px solid rgba(245,242,237,0.12);}}
    [data-sp-disc] .dk-tab{{position:relative;display:flex;align-items:baseline;gap:16px;width:100%;padding:clamp(9px,1.3vh,14px) 0;border:0;border-bottom:1px solid rgba(245,242,237,0.12);background:none;color:rgba(245,242,237,0.45);text-align:start;cursor:pointer;transition:color 0.4s {EASE};}}
    [data-sp-disc] .dk-tab:hover,[data-sp-disc] .dk-tab.is-on{{color:#F5F2ED;}}
    [data-sp-disc] .dk-tab:focus-visible{{outline:1px solid #D6C2A8;outline-offset:2px;}}
    [data-sp-disc] .dk-prog{{position:absolute;inset-inline:0;bottom:-1px;height:1px;background:#D6C2A8;transform:scaleX(var(--p,0));transform-origin:{'100%' if ar else '0%'} 50%;}}
    [data-sp-disc] .dk-n{{flex:none;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.2em;color:#D6C2A8;}}
    [data-sp-disc] .dk-t{{font-family:{font};font-size:{'15px' if ar else '14px'};line-height:1.4;}}
    @media(min-width:901px) and (min-height:600px){{
      [data-sp-disc] .dk-block{{position:sticky;top:80px;}}
      [data-sp-disc] .dk-spacer{{height:{(n + 2) * 50}vh;}}
    }}
    @media(max-width:900px){{
      [data-sp-disc] .dk-head{{grid-template-columns:1fr;}}
      [data-sp-disc] .dk-stage{{flex-direction:column;align-items:stretch;height:auto;min-height:0;padding:0 0 28px;gap:24px;}}
      [data-sp-disc] .dk-photo{{width:100%;box-shadow:none;}}
      [data-sp-disc] .dk-side{{max-width:none;padding:0 clamp(24px,5vw,80px);}}
      [data-sp-disc] .dk-panes{{min-height:0;}}
      [data-sp-disc] .dk-end{{display:none;}}
      [data-sp-disc] .dk-list{{display:grid;grid-template-columns:repeat({n},1fr);border:0;}}
      [data-sp-disc] .dk-tab{{justify-content:center;border-bottom:0;border-top:2px solid rgba(245,242,237,0.12);padding:12px 0 0;}}
      [data-sp-disc] .dk-prog{{top:-2px;bottom:auto;height:2px;}}
      [data-sp-disc] .dk-t{{display:none;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-sp-disc] *{{transition:none!important;}}
      [data-sp-disc] .dk-rise{{opacity:1;transform:none;}}
    }}
  </style>
  <div class="dk-wrap">
    <div class="dk-head">
      <div class="dk-rise">
        <p class="dk-eyebrow"><i></i>{c['eyebrow']}</p>
        <h2 class="dk-h2">{c['h2']}</h2>
      </div>
      <p class="dk-sub dk-rise dk-rise--2">{c['sub']}</p>
    </div>
    <div class="dk-track">
    <div class="dk-block dk-rise dk-rise--3">
      <div class="dk-stage" data-dk-stage data-spots="{spots}">
        <div class="dk-photo">
          <img src="uploads/{P['img']}-1920.webp" srcset="{srcset}" sizes="(max-width:900px) 100vw, 62vw" alt="{c['alt']}" loading="lazy" decoding="async">
          <span class="dk-spot" aria-hidden="true"></span>
        </div>
        <div class="dk-side">
          <p class="dk-count"><span dir="ltr"><b class="dk-cur">00</b> / 0{n}</span></p>
          <div class="dk-panes" aria-live="polite">
{panes}
          </div>
          <div class="dk-end"><a class="dk-cta" href="{c['cta_href']}">{c['cta']}{ARROW[lang]}</a></div>
          <ol class="dk-list" aria-label="{c['tabs']}">
{items}
          </ol>
        </div>
      </div>
    </div>
    <div class="dk-spacer" aria-hidden="true"></div>
    </div>
  </div>
</section>
"""


JS = """    // ── SERVICE PAGES, DISCIPLINES: THE DESIGNER'S DESK ─────────────────────
    {
      const sec = document.querySelector('[data-sp-disc]');
      if (sec) {
        const stage = sec.querySelector('[data-dk-stage]'), block = sec.querySelector('.dk-block'), track = sec.querySelector('.dk-track');
        const photo = sec.querySelector('.dk-photo'), cur = sec.querySelector('.dk-cur');
        const panes = Array.from(sec.querySelectorAll('[data-dk-pane]')), tabs = Array.from(sec.querySelectorAll('[data-dk-tab]'));
        const spots = stage.dataset.spots.split('|').map((s) => s.split(',').map(Number));
        const N = spots.length, PAD = 1.6;   // the spotlight's margin round each object, in % of the photograph
        const pinMQ = matchMedia('(min-width:901px) and (min-height:600px)');
        let pinned = pinMQ.matches, idx = -2, ticking = false, jump = null, auto = !reduced, visible = false, then = 0, acc = 0, raf = 0;
        const HOLD = 4200;
        // i = -1: the whole desk, lit, before the first; 0..N-1: one object in the spotlight; -2: the desk lit again
        // after the sixth, which keeps the sixth's words and offers the closing call
        const show = (i) => {
          if (i === idx) return;
          idx = i;
          const v = (k, val) => photo.style.setProperty(k, val);
          if (i < 0) { v('--sx', '0%'); v('--sy', '0%'); v('--sw', '100%'); v('--sh', '100%'); v('--dim', 0); v('--mk', 0); }
          else {
            const [x, y, w, h] = spots[i];
            v('--sx', (x - PAD) + '%'); v('--sy', (y - PAD) + '%'); v('--sw', (w + 2 * PAD) + '%'); v('--sh', (h + 2 * PAD) + '%');
            v('--dim', 0.7); v('--mk', 1);
          }
          const end = i === -2, k = end ? N - 1 : Math.max(0, i);
          sec.classList.toggle('is-end', end);
          cur.textContent = '0' + (k + 1);
          panes.forEach((p, j) => p.classList.toggle('is-on', j === k));
          tabs.forEach((t, j) => { t.classList.toggle('is-on', j === i); t.setAttribute('aria-pressed', j === i ? 'true' : 'false'); });
        };
        const geo = () => { const top = parseFloat(getComputedStyle(block).top) || 0; return { start: track.getBoundingClientRect().top + window.scrollY - top, dist: Math.max(1, track.offsetHeight - block.offsetHeight) }; };
        // N + 2 equal steps: the lit desk, the six objects, the lit desk again
        const onScroll = () => {
          ticking = false;
          if (!pinned) return;
          const g = geo(), x = Math.min(N + 1.9999, Math.max(0, (window.scrollY - g.start) / g.dist) * (N + 2)), s = Math.floor(x) - 1;
          const i = s >= N ? -2 : s;
          if (jump !== null) { if (i === jump) jump = null; else return; }
          show(i);
          tabs.forEach((t, k) => t.style.setProperty('--p', k < s ? 1 : k === s ? (x - Math.floor(x)).toFixed(4) : 0));
        };
        window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
        // one wheel notch, one object: the page's step snap (STEP SNAP) holds the desk to its eight steps
        const stop = (j, g) => g.start + g.dist * (j + 0.5) / (N + 2);
        (window.fiqSnap = window.fiqSnap || []).push({ on: () => pinned, geo: () => { const g = geo(); return { a: g.start, b: g.start + g.dist, stops: Array.from({ length: N + 2 }, (_, j) => stop(j, g)) }; } });
        tabs.forEach((t, k) => t.addEventListener('click', () => {
          auto = false;
          if (pinned) { const g = geo(), to = stop(k + 1, g); jump = k; show(k); if (window.fiqGlide) window.fiqGlide(to); else window.scrollTo({ top: to, behavior: reduced ? 'instant' : 'smooth' }); }
          else { acc = 0; show(k); tabs.forEach((tb, j) => tb.style.setProperty('--p', j === k ? 1 : 0)); }
        }));
        const fit = () => sec.style.setProperty('--dk-sb', (window.innerWidth - document.documentElement.clientWidth) + 'px');
        fit();
        window.addEventListener('resize', () => { fit(); onScroll(); });
        pinMQ.addEventListener('change', () => { pinned = pinMQ.matches; jump = null; idx = -2; if (pinned) onScroll(); else show(0); });
        // phones: the six take their turn while the desk is in view
        document.addEventListener('visibilitychange', () => { then = 0; });
        const loop = (now) => {
          // real time between frames, so a throttled frame rate does not slow the turn
          const dt = then ? now - then : 0; then = now;
          if (!pinned && auto && !document.hidden) {
            acc += dt;
            if (idx >= 0) tabs[idx].style.setProperty('--p', Math.min(1, acc / HOLD).toFixed(4));
            if (acc >= HOLD) { acc = 0; tabs.forEach((t) => t.style.setProperty('--p', 0)); show((Math.max(0, idx) + 1) % N); }
          }
          raf = visible ? requestAnimationFrame(loop) : 0;
        };
        new IntersectionObserver((es, o) => { es.forEach((e) => { if (e.isIntersecting) { sec.classList.add('is-in'); o.disconnect(); } }); }, { rootMargin: '0px 0px -15% 0px' }).observe(sec);
        new IntersectionObserver((es) => { es.forEach((e) => { visible = e.isIntersecting; if (visible && !raf) { then = 0; raf = requestAnimationFrame(loop); } }); }, { threshold: 0.3 }).observe(stage);
        if (pinned) { show(-1); onScroll(); } else show(0);
      }
    }

"""
MARK = "    // ── SCROLL REVEAL"

pages = sys.argv[1:] or list(PAGE)
for page in pages:
    for name, lang in [(f"{page}.dc.html", "en"), (f"{page}.ar.dc.html", "ar")]:
        s = open(name, encoding="utf-8").read()
        s, k = re.subn(r"<!-- ━+ SCOPE ━+ -->\n<section [^>]*data-screen-label=\"Scope\".*?\n</section>\n", lambda m: build(page, lang), s, count=1, flags=re.S)
        assert k == 1, name
        old = "    // ── SERVICE PAGES, DISCIPLINES:"
        if old in s:
            a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
            s = s[:a] + s[b:]
        assert s.count(MARK) == 1, name
        s = s.replace(MARK, JS + MARK)
        open(name, "w", encoding="utf-8", newline="").write(s)
        print(name, "ok")

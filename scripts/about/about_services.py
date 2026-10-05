import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
IMG = [
    ("luxury-interior-design-material-board-riyadh", [600, 900, 1200]),
    ("office-fit-out-walnut-wall-panel-installation-riyadh", [600, 900, 1200]),
    ("mep-ceiling-services-installation-riyadh", [600, 900, 1200]),
    ("furniture-gallery-living-room-set", [1280, 1920, 2752]),
]
SLUG = ["services-interior-design", "services-fitout", "services-mep", "services-furniture"]
C = {
    "en": dict(
        label="Our Disciplines", h2="Integrated Expertise.<br>Total Accountability.",
        intro="Design, fit-out, engineering and furniture under one roof, so your vision is never lost between the first sketch and the final handover.",
        roof="Four disciplines. One roof.", link="Explore the service", pre="",
        items=[
            ("Architecture & Interior Design", "Bespoke spaces that maximise property value",
             "Every FurnishIQ project begins with a rigorous discovery of your brief, your brand, and the behaviours of the people who will inhabit the space. Our design team translates that understanding into bespoke spatial concepts, developing layouts, material specifications and lighting strategies that balance aesthetic ambition with practical performance. Full photoreal 3D renders are produced for client approval before construction begins, so the final environment is built exactly as envisioned.",
             "Material board with walnut, travertine and fabric samples beside an interior sketch"),
            ("Fit-Out & Turnkey Solutions", "Raw shells transformed into masterpieces",
             "FurnishIQ takes complete responsibility for the build, from initial partitioning, flooring and ceilings through to bespoke joinery, specialist finishes and final handover. Because our fit-out team works alongside our designers and engineers under one roof, coordination is resolved in the model rather than on site, protecting both programme and budget. Every project closes with a structured snagging process and a defined aftercare period.",
             "Craftsman installing fluted walnut wall panels during an office fit-out in Riyadh"),
            ("Engineering & MEP", "The precision backbone of every space",
             "Mechanical, electrical and plumbing engineering is delivered by the same integrated team responsible for your design and fit-out, not an external subcontractor working from a separate drawing set. Clashes are eliminated before they reach the site, and every electrical system, HVAC installation, plumbing network, fire-fighting provision and low-current infrastructure is designed as one coherent whole, then tested, commissioned and documented to Saudi and international standards.",
             "Exposed ceiling services with cable trays and ductwork above a timber slat ceiling"),
            ("Furniture Solutions", "Sourced to your scale, budget and aesthetic",
             "Furniture selections are developed in parallel with spatial planning, not after it, so every piece is aligned with the design intent, the end-user requirement and the project budget from the outset. We source across the full market, from bespoke joinery to internationally procured FF&amp;E, and manage the entire process in-house: purchase orders, delivery scheduling, quality inspection, warehousing and installation.",
             "Furnished living room with a sand sofa, boucle armchairs and an oak coffee table"),
        ],
    ),
    "ar": dict(
        label="تخصصاتنا", h2="خبرة متكاملة.<br>مسؤولية شاملة.",
        intro="التصميم والتشطيب والهندسة والأثاث تحت سقف واحد، حتى لا تضيع رؤيتك بين أول رسم تخطيطي والتسليم النهائي.",
        roof="أربعة تخصصات. سقف واحد.", link="استكشف الخدمة", pre="/ar",
        items=[
            ("العمارة والتصميم الداخلي", "مساحات مخصصة تُعظّم قيمة العقار",
             "يبدأ كل مشروع لدى فيرنيش آي كيو باكتشاف دقيق لمتطلباتك وهويتك التجارية وسلوكيات من سيشغل المساحة. يترجم فريق التصميم لدينا هذا الفهم إلى مفاهيم مكانية مخصصة، من خلال تطوير المخططات ومواصفات المواد واستراتيجيات الإضاءة التي توازن بين الطموح الجمالي والأداء العملي. يتم إنتاج تصورات ثلاثية الأبعاد واقعية بالكامل لاعتماد العميل قبل بدء البناء، لضمان تنفيذ البيئة النهائية تماماً كما تم تصورها.",
             "لوحة مواد تضم عينات من خشب الجوز والترافرتين والأقمشة بجانب رسم تخطيطي داخلي"),
            ("التشطيبات والحلول الجاهزة", "هياكل خام تتحول إلى تحف معمارية",
             "تتحمل فيرنيش آي كيو المسؤولية الكاملة عن التنفيذ، من الفواصل الأولية والأرضيات والأسقف وصولاً إلى الأعمال الخشبية المخصصة والتشطيبات المتخصصة والتسليم النهائي. ولأن فريق التشطيبات لدينا يعمل جنباً إلى جنب مع المصممين والمهندسين تحت سقف واحد، يتم حل التنسيق في النموذج بدلاً من الموقع، ما يحافظ على الجدول الزمني والميزانية. يُختتم كل مشروع بعملية منظمة لمعالجة العيوب وفترة رعاية محددة بعد التسليم.",
             "حرفي يركّب ألواح جدارية مضلعة من خشب الجوز أثناء تشطيب مكتب في الرياض"),
            ("الهندسة والأنظمة الكهروميكانيكية", "العمود الفقري الدقيق لكل مساحة",
             "تُنفَّذ أعمال الهندسة الميكانيكية والكهربائية والسباكة من قبل الفريق المتكامل نفسه المسؤول عن التصميم والتشطيب، وليس من قبل مقاول من الباطن يعمل وفق مخططات منفصلة. يزيل هذا التنسيق الداخلي أي تعارضات قبل وصولها إلى الموقع، ويضمن تصميم كل نظام كهربائي وتكييف وسباكة ومكافحة حريق وتيار منخفض ككل متكامل، ثم اختباره وتشغيله وتوثيقه وفق المعايير السعودية والدولية.",
             "خدمات سقف مكشوفة مع حوامل كابلات ومجاري هواء فوق سقف من الشرائح الخشبية"),
            ("حلول الأثاث", "توريد يتوافق مع حجم مشروعك وميزانيتك وطابعك",
             "يتم تطوير اختيارات الأثاث بالتوازي مع التخطيط المكاني، وليس بعده، لضمان توافق كل قطعة مع نية التصميم واحتياجات المستخدم النهائي وميزانية المشروع منذ البداية. نقوم بالتوريد من كامل السوق، من الأعمال الخشبية المخصصة إلى الأثاث والتجهيزات المستوردة عالمياً، وندير العملية بأكملها داخلياً: أوامر الشراء، جدولة التسليم، فحص الجودة، التخزين، والتركيب.",
             "غرفة معيشة مفروشة بأريكة رملية وكراسي بوكليه وطاولة قهوة من خشب البلوط"),
        ],
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
    arrow = ARROW_AR if ar else ARROW_EN
    hidden_clip = "inset(0 0 0 100%)" if ar else "inset(0 100% 0 0)"
    tabs, frames = "", ""
    for i, (title, tag, body, alt) in enumerate(c["items"]):
        on = i == 0
        tabs += f"""
      <div class="sv-item{' is-active' if on else ''}" data-sv-item>
        <button type="button" class="sv-tab" role="tab" id="sv-tab-{i}" aria-controls="sv-panel-{i}" aria-selected="{'true' if on else 'false'}" tabindex="{'0' if on else '-1'}" data-sv-tab="{i}">
          <span class="sv-n" dir="ltr">0{i + 1}</span><span class="sv-t">{title}</span><span class="sv-plus" aria-hidden="true"></span>
        </button>
        <div class="sv-panel" role="tabpanel" id="sv-panel-{i}" aria-labelledby="sv-tab-{i}">
          <div class="sv-panel-in">
            <p class="sv-body">{body}</p>
            <a class="sv-link" href="{c['pre']}/{SLUG[i]}">{c['link']}{arrow}</a>
          </div>
        </div>
      </div>"""
        name, ws = IMG[i]
        srcset = ", ".join(f"uploads/{name}-{w}.webp {w}w" for w in ws)
        frames += f"""
      <figure class="sv-frame{' is-active' if on else ''}" data-sv-frame>
        <img src="uploads/{name}-{ws[-1]}.webp" srcset="{srcset}" sizes="(max-width:900px) 100vw, 60vw" alt="{alt}" width="1200" height="900" loading="lazy" decoding="async">
      </figure>"""
    chips = "".join(f'<span class="sv-chip{" is-active" if i == 0 else ""}" data-sv-chip><b dir="ltr">0{i + 1} / 04</b>{t}</span>' for i, (_, t, _, _) in enumerate(c["items"]))
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ INTEGRATED SERVICES ━━ -->
<section id="disciplines" data-svc{' dir="rtl"' if ar else ''} style="position:relative;background:#F5F2ED;padding:clamp(64px,8vw,100px) clamp(24px,5vw,80px);overflow:clip;">
  <style>
    #disciplines .sv-wrap{{max-width:1280px;margin:0 auto;}}
    @media(min-width:901px){{
      #disciplines{{min-height:100vh;box-sizing:border-box;display:flex;flex-direction:column;}}
      #disciplines .sv-wrap{{width:100%;flex:1;display:flex;flex-direction:column;}}
      #disciplines .sv-grid{{flex:1;}}
    }}
    #disciplines .sv-head{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,7fr);gap:clamp(40px,5vw,88px);align-items:end;margin-bottom:clamp(24px,3.5vh,48px);}}
    #disciplines .sv-label{{display:flex;align-items:center;gap:16px;margin-bottom:20px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    #disciplines .sv-label i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    #disciplines .sv-h2{{font-family:{font};font-size:clamp(30px,2.9vw,46px);font-weight:500;line-height:{'1.35' if ar else '1.1'};letter-spacing:{'normal' if ar else '-0.02em'};color:#3A2D25;margin:0;}}
    #disciplines .sv-intro{{font-family:{font};font-size:{'17px' if ar else '16px'};line-height:1.8;color:#5B4636;margin:0;max-width:460px;}}
    #disciplines .sv-grid{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,7fr);gap:clamp(40px,5vw,88px);align-items:stretch;}}
    #disciplines .sv-list{{border-top:1px solid rgba(58,45,37,0.16);}}
    #disciplines .sv-item{{position:relative;border-bottom:1px solid rgba(58,45,37,0.16);}}
    #disciplines .sv-item::before{{content:"";position:absolute;top:-1px;bottom:-1px;inset-inline-start:0;width:2px;background:#8B6B4A;transform:scaleY(0);transform-origin:top;transition:transform 0.7s {EASE};}}
    #disciplines .sv-item.is-active::before{{transform:scaleY(1);}}
    #disciplines .sv-tab{{all:unset;box-sizing:border-box;width:100%;display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:baseline;gap:clamp(14px,1.6vw,24px);padding:clamp(12px,1.9vh,22px) 0;padding-inline-start:clamp(18px,1.8vw,28px);cursor:pointer;}}
    #disciplines .sv-tab:focus-visible{{outline:1px solid #8B6B4A;outline-offset:-1px;}}
    #disciplines .sv-n{{font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.2em;color:#8B6B4A;}}
    #disciplines .sv-t{{font-family:{font};font-size:clamp(19px,1.6vw,26px);font-weight:500;line-height:1.25;letter-spacing:{'normal' if ar else '-0.015em'};color:rgba(58,45,37,0.4);transition:color 0.5s {EASE};}}
    #disciplines .sv-tab:hover .sv-t{{color:rgba(58,45,37,0.75);}}
    #disciplines .sv-item.is-active .sv-t{{color:#3A2D25;}}
    #disciplines .sv-plus{{position:relative;width:14px;height:14px;align-self:center;}}
    #disciplines .sv-plus::before,#disciplines .sv-plus::after{{content:"";position:absolute;top:50%;left:0;width:14px;height:1px;background:#8B6B4A;transition:transform 0.5s {EASE};}}
    #disciplines .sv-plus::after{{transform:rotate(90deg);}}
    #disciplines .sv-item.is-active .sv-plus::after{{transform:rotate(0deg);}}
    #disciplines .sv-panel{{display:grid;grid-template-rows:0fr;transition:grid-template-rows 0.7s {EASE};}}
    #disciplines .sv-item.is-active .sv-panel{{grid-template-rows:1fr;}}
    #disciplines .sv-panel-in{{overflow:hidden;min-height:0;padding-inline-start:clamp(18px,1.8vw,28px);}}
    #disciplines .sv-panel-in > *{{opacity:0;transform:translateY(10px);transition:opacity 0.4s {EASE},transform 0.4s {EASE};}}
    #disciplines .sv-item.is-active .sv-panel-in > *{{opacity:1;transform:none;transition:opacity 0.7s {EASE} 0.25s,transform 0.7s {EASE} 0.25s;}}
    #disciplines .sv-tag{{font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;color:#8B6B4A;margin:0 0 14px;}}
    #disciplines .sv-body{{font-family:{font};font-size:{'15px' if ar else '14px'};line-height:1.75;color:#5B4636;margin:0;max-width:540px;}}
    #disciplines .sv-link{{display:inline-flex;align-items:center;gap:12px;margin:18px 0 clamp(18px,2.6vh,28px);font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;color:#3A2D25;text-decoration:none;padding-bottom:6px;border-bottom:1px solid #8B6B4A;transition:color 0.4s {EASE},gap 0.4s {EASE};}}
    #disciplines .sv-link:hover,#disciplines .sv-link:focus-visible{{color:#8B6B4A;gap:18px;}}
    #disciplines .sv-media{{position:relative;margin-inline-end:calc(-1 * var(--sv-bleed, max(clamp(24px,5vw,80px), (100vw - 1280px) / 2)));}}
    #disciplines .sv-stage{{position:absolute;inset:0;min-height:360px;background:#E5DCD0;overflow:hidden;}}
    #disciplines .sv-frame{{position:absolute;inset:0;margin:0;overflow:hidden;clip-path:{hidden_clip};transition:clip-path 1.1s {EASE};}}
    #disciplines .sv-frame.is-active{{clip-path:inset(0 0 0 0);z-index:2;}}
    #disciplines .sv-frame.is-leaving{{z-index:1;clip-path:inset(0 0 0 0);}}
    #disciplines .sv-frame img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scale(1.08);transition:transform 2.2s {EASE};}}
    #disciplines .sv-frame.is-active img{{transform:scale(1);}}
    #disciplines .sv-cap{{position:absolute;z-index:3;bottom:0;inset-inline-start:0;display:grid;background:#3A2D25;}}
    #disciplines .sv-chip{{grid-area:1/1;display:flex;align-items:center;gap:18px;padding:18px 26px;font-family:{font};font-size:{'14px' if ar else '13px'};color:#F5F2ED;opacity:0;transform:translateY(8px);transition:opacity 0.4s {EASE},transform 0.4s {EASE};}}
    #disciplines .sv-chip.is-active{{opacity:1;transform:none;transition:opacity 0.6s {EASE} 0.5s,transform 0.6s {EASE} 0.5s;}}
    #disciplines .sv-chip b{{font-family:'Lama Sans',sans-serif;font-weight:500;font-size:10px;letter-spacing:0.2em;color:#D6C2A8;}}
    #disciplines .sv-roof{{position:absolute;z-index:3;top:0;inset-inline-end:0;display:flex;align-items:center;gap:14px;padding:16px 22px;background:#F5F2ED;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#3A2D25;}}
    #disciplines .sv-roof i{{display:flex;gap:4px;}}
    #disciplines .sv-roof i span{{display:block;width:14px;height:2px;background:rgba(58,45,37,0.18);transition:background 0.5s {EASE};}}
    #disciplines .sv-roof i span.is-active{{background:#8B6B4A;}}
    @media(max-width:900px){{
      #disciplines .sv-grid{{grid-template-columns:1fr;gap:0;}}
      #disciplines .sv-head{{grid-template-columns:1fr;gap:20px;margin-bottom:32px;}}
      #disciplines .sv-media{{order:-1;margin:0 calc(-1 * clamp(24px,5vw,80px)) 32px;}}
      #disciplines .sv-stage{{position:relative;inset:auto;min-height:0;aspect-ratio:4/3;}}
      #disciplines .sv-roof{{display:none;}}
      #disciplines .sv-chip{{padding:14px 18px;font-size:12px;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      #disciplines *{{transition:none!important;}}
    }}
  </style>
  <div class="sv-wrap">
    <div class="sv-head" data-reveal style="opacity:0;transform:translateY(18px);transition:opacity 0.8s {EASE},transform 0.8s {EASE};">
      <div>
        <div class="sv-label"><i></i>{c['label']}</div>
        <h2 class="sv-h2">{c['h2']}</h2>
      </div>
      <p class="sv-intro">{c['intro']}</p>
    </div>
    <div class="sv-grid">
      <div class="sv-side">
      <div class="sv-list" role="tablist" aria-orientation="vertical" data-reveal style="opacity:0;transform:translateY(18px);transition:opacity 0.8s {EASE} 0.1s,transform 0.8s {EASE} 0.1s;">{tabs}
      </div>
      </div>
      <div class="sv-media" data-reveal style="opacity:0;transform:translateY(18px);transition:opacity 0.9s {EASE} 0.2s,transform 0.9s {EASE} 0.2s;">
        <div class="sv-stage">{frames}
        <div class="sv-roof" aria-hidden="true"><i><span class="is-active"></span><span></span><span></span><span></span></i>{c['roof']}</div>
        <div class="sv-cap" aria-hidden="true">{chips}</div>
        </div>
      </div>
    </div>
  </div>
</section>
"""


JS = """    // ── DISCIPLINES: TABS WITH WIPING IMAGE STAGE ────────────────────────────
    {
      const sv = document.querySelector('[data-svc]');
      if (sv) {
        const items = [...sv.querySelectorAll('[data-sv-item]')], tabs = [...sv.querySelectorAll('[data-sv-tab]')];
        const frames = [...sv.querySelectorAll('[data-sv-frame]')], chips = [...sv.querySelectorAll('[data-sv-chip]')], bars = [...sv.querySelectorAll('.sv-roof i span')];
        let cur = 0, leaveTimer;
        // image bleeds exactly to the viewport edge (clientWidth excludes the scrollbar)
        const wrap = sv.querySelector('.sv-wrap');
        const bleed = () => sv.style.setProperty('--sv-bleed', Math.max(0, (document.documentElement.clientWidth - wrap.offsetWidth) / 2) + 'px');
        // the list always reserves room for its tallest description, so switching tabs never changes the section height
        const list = sv.querySelector('.sv-list'), inners = [...sv.querySelectorAll('.sv-panel-in')];
        const fit = () => {
          bleed();
          if (window.innerWidth <= 900) { list.style.minHeight = ''; return; }
          const tabsH = tabs.reduce((a, t) => a + t.offsetHeight, 0) + items.length + 4;
          list.style.minHeight = (tabsH + Math.max(...inners.map(x => x.scrollHeight))) + 'px';
        };
        fit(); window.addEventListener('resize', fit);
        if (document.fonts) document.fonts.ready.then(fit);
        const show = (n, focus) => {
          if (n === cur) return;
          const prev = cur; cur = n;
          clearTimeout(leaveTimer);
          frames.forEach((f, k) => { f.classList.toggle('is-leaving', k === prev); f.classList.toggle('is-active', k === n); });
          leaveTimer = setTimeout(() => frames[prev].classList.remove('is-leaving'), 1150);
          items.forEach((it, k) => it.classList.toggle('is-active', k === n));
          tabs.forEach((t, k) => { t.setAttribute('aria-selected', k === n ? 'true' : 'false'); t.tabIndex = k === n ? 0 : -1; });
          chips.forEach((c, k) => c.classList.toggle('is-active', k === n));
          bars.forEach((b, k) => b.classList.toggle('is-active', k <= n));
          if (focus) tabs[n].focus();
        };
        tabs.forEach((t, i) => {
          t.addEventListener('click', () => show(i));
          t.addEventListener('keydown', (e) => {
            const d = e.key === 'ArrowDown' || e.key === 'ArrowRight' ? 1 : e.key === 'ArrowUp' || e.key === 'ArrowLeft' ? -1 : 0;
            if (e.key === 'Home') { e.preventDefault(); show(0, true); }
            else if (e.key === 'End') { e.preventDefault(); show(tabs.length - 1, true); }
            else if (d) { e.preventDefault(); show((cur + d + tabs.length) % tabs.length, true); }
          });
        });
      }
    }

"""
MARK = "    // ── FADE-IN ON LOAD (lazy images)"

for path, lang in [("about-us.dc.html", "en"), ("about-us.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ INTEGRATED SERVICES ━+ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── DISCIPLINES: TABS"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

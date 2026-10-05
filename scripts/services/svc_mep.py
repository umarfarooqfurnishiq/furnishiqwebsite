"""Services, Engineering & MEP: engineering you feel, not see.

A showcase rail of tall image cards that runs off the edge of the screen. Each card leads with what the
client experiences in a finished space, then names the discipline behind it with the description from the
MEP detail page. The rail scrolls by drag, swipe, wheel or the arrow buttons, and snaps card by card.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/services/svc_mep.py
"""
import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
CARDS = [  # image base, available widths, object-position
    ("penthouse-wadi-double-height-living-riyadh", (1280, 1920), "62% 50%"),
    ("executive-floors-walnut-ceiling-detail", (1200, 2400), "50% 50%"),
    ("penthouse-wadi-master-suite-spa-bath", (1280, 2752), "52% 50%"),
    ("desert-stone-resort-lobby-lounge-alula", (1280, 1920), "40% 50%"),
    ("executive-floors-boardroom-walnut-table", (1280, 1920), "55% 50%"),
    ("pillar-quality-assurance-level-inspection", (900, 1536), "50% 50%"),
]
C = {
    "en": dict(
        eyebrow="Our Engineering Services", h2="The Foundation of High-Performance Environments",
        body="True luxury and functionality depend on the invisible systems that keep a building running. Our Engineering &amp; MEP (Mechanical, Electrical, and Plumbing) services provide the high-performance infrastructure required to bring your interior vision to life, seamlessly integrated into every design and fit-out we deliver.",
        cta="Explore Engineering &amp; MEP", href="/services-mep",
        feel=["Comfort, in every volume", "Light, layered with intent", "Water, exactly where it belongs",
              "Protection that stays out of sight", "Connected, quietly", "Proven before handover"],
        names=["HVAC Systems", "Electrical Systems", "Plumbing Systems", "Fire Fighting Systems",
               "Low Current Systems", "Testing &amp; Commissioning"],
        descs=["Air conditioning, ventilation, ductwork, and testing for consistent year-round comfort.",
               "Power distribution, lighting, emergency power, and cable management, engineered to code.",
               "Water supply, drainage, sewage, and pump installations engineered for reliability.",
               "Fire alarms, suppression, sprinkler networks, and full Civil Defense compliance.",
               "Structured cabling, CCTV, access control, and smart building integration.",
               "Functional testing, performance validation, and certified handover documentation."],
        alts=["Double-height living room with an onyx wall and a view over the wadi",
              "Walnut slatted ceiling with linear lighting along a corridor",
              "Master suite with a freestanding stone bath beside the bed",
              "Resort lobby lounge with full-height glazing onto the AlUla rocks",
              "Boardroom with a long walnut table and a screen at the far wall",
              "Gloved hand checking a travertine wall with a brass spirit level"],
        prev="Previous", next="Next", rail="MEP disciplines", cap="Engineering you feel, not see · Concept visualisations",
    ),
    "ar": dict(
        eyebrow="خدماتنا الهندسية", h2="أساس البيئات عالية الأداء",
        body="تعتمد الفخامة الحقيقية والوظائفية على الأنظمة غير المرئية التي تُبقي المبنى يعمل. تقدم خدماتنا الهندسية والأنظمة الكهروميكانيكية (الميكانيكية والكهربائية والصحية) البنية التحتية عالية الأداء اللازمة لتحقيق رؤيتك الداخلية، مدمجة بسلاسة في كل تصميم وتشطيب ننفذه.",
        cta="استكشف الهندسة والأنظمة الكهروميكانيكية", href="/ar/services-mep",
        feel=["راحة في كل مساحة", "إضاءة مدروسة بطبقات", "المياه، حيث يجب أن تكون",
              "حماية لا تُرى", "اتصال بهدوء", "مُختبر قبل التسليم"],
        names=["أنظمة التكييف والتهوية", "الأنظمة الكهربائية", "أنظمة السباكة", "أنظمة مكافحة الحريق",
               "أنظمة التيار المنخفض", "الاختبار والتشغيل"],
        descs=["التكييف والتهوية ومجاري الهواء والاختبار لراحة دائمة على مدار العام.",
               "توزيع الطاقة والإنارة وطاقة الطوارئ وإدارة الكابلات، وفق الأكواد المعتمدة.",
               "إمدادات المياه والصرف والصرف الصحي وتركيب المضخات بموثوقية عالية.",
               "إنذار الحريق والإطفاء وشبكات الرشاشات والامتثال الكامل لاشتراطات الدفاع المدني.",
               "الكابلات المهيكلة وكاميرات المراقبة والتحكم في الدخول وتكامل المباني الذكية.",
               "الاختبار الوظيفي والتحقق من الأداء ووثائق التسليم المعتمدة."],
        alts=["غرفة معيشة بارتفاع مزدوج بجدار من العقيق وإطلالة على الوادي",
              "سقف من شرائح خشب الجوز بإضاءة خطية على امتداد ممر",
              "جناح رئيسي بحوض استحمام حجري قائم بجانب السرير",
              "صالة استقبال منتجع بواجهات زجاجية كاملة تطل على صخور العلا",
              "قاعة اجتماعات بطاولة طويلة من خشب الجوز وشاشة في الجدار البعيد",
              "يد بقفاز تفحص جداراً من الترافرتين بميزان تسوية نحاسي"],
        prev="السابق", next="التالي", rail="تخصصات الأنظمة الكهروميكانيكية", cap="هندسة تُحَس ولا تُرى · تصورات مفاهيمية",
    ),
}
ARROW_EN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
ARROW_AR = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>'
CHEV_L = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" aria-hidden="true"><polyline points="15 5 8 12 15 19"/></svg>'
CHEV_R = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" aria-hidden="true"><polyline points="9 5 16 12 9 19"/></svg>'


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    n = len(CARDS)
    cards = []
    for i, (base, widths, pos) in enumerate(CARDS):
        srcset = ", ".join(f"uploads/{base}-{w}.webp {w}w" for w in widths)
        cards.append(f'''      <li class="mr-card" style="--i:{i};">
        <figure class="mr-fig"><img src="uploads/{base}-{widths[0]}.webp" srcset="{srcset}" sizes="(max-width:600px) 80vw, 420px" alt="{c['alts'][i]}" style="object-position:{pos};" loading="lazy" decoding="async" draggable="false"></figure>
        <p class="mr-tag"><b>0{i + 1}</b>{c['names'][i]}</p>
        <h3 class="mr-feel">{c['feel'][i]}</h3>
        <p class="mr-desc">{c['descs'][i]}</p>
      </li>''')
    cards = "\n".join(cards)
    # arrows point the way the rail moves: in Arabic "next" goes left
    prev_icon, next_icon = (CHEV_R, CHEV_L) if ar else (CHEV_L, CHEV_R)
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━ 3. ENGINEERING & MEP ━ -->
<section id="mep" data-screen-label="Engineering &amp; MEP" data-svc-mep{' dir="rtl"' if ar else ''} style="scroll-margin-top:var(--fiq-svc-offset,132px);background:#F5F2ED;color:#3A2D25;position:relative;padding:clamp(64px,8vw,100px) clamp(24px,5vw,80px);overflow:clip;">
  <style>
    [data-svc-mep] .mr-wrap{{max-width:1280px;margin:0 auto;}}
    [data-svc-mep] .mr-head{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:clamp(32px,5vw,88px);align-items:end;margin-bottom:clamp(40px,4.4vw,64px);}}
    [data-svc-mep] .mr-eyebrow{{display:flex;align-items:center;gap:16px;margin-bottom:24px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    [data-svc-mep] .mr-eyebrow i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    [data-svc-mep] .mr-h2{{font-family:{font};font-weight:500;font-size:clamp(32px,3.8vw,54px);line-height:1.08;letter-spacing:{'0' if ar else '-0.015em'};color:#1F1F1F;margin:0;text-wrap:balance;}}
    [data-svc-mep] .mr-body{{font-family:{font};font-size:{'16px' if ar else '15px'};line-height:1.85;color:#5B4636;margin:0 0 28px;}}
    [data-svc-mep] .mr-cta{{display:inline-flex;align-items:center;gap:12px;padding:17px 30px;background:#3A2D25;color:#F5F2ED;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;border:1px solid #3A2D25;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-mep] .mr-cta:hover,[data-svc-mep] .mr-cta:focus-visible{{background:transparent;color:#3A2D25;}}
    [data-svc-mep] .mr-rail{{list-style:none;margin:0 calc(var(--mr-bleed,0px) * -1);padding:0 var(--mr-bleed,0px);display:flex;gap:clamp(18px,2vw,28px);overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding-inline:var(--mr-bleed,0px);scrollbar-width:none;cursor:grab;user-select:none;-webkit-user-select:none;}}
    [data-svc-mep] .mr-rail::-webkit-scrollbar{{display:none;}}
    [data-svc-mep] .mr-rail.is-drag{{cursor:grabbing;scroll-snap-type:none;}}
    [data-svc-mep] .mr-card{{flex:0 0 clamp(270px,27vw,400px);scroll-snap-align:start;opacity:0;transform:translateY(32px);transition:opacity 0.9s {EASE} calc(var(--i) * 0.09s),transform 0.9s {EASE} calc(var(--i) * 0.09s);}}
    [data-svc-mep].is-in .mr-card{{opacity:1;transform:none;}}
    [data-svc-mep] .mr-fig{{position:relative;margin:0;aspect-ratio:4/5;overflow:hidden;background:#3A2D25;}}
    [data-svc-mep] .mr-fig img{{width:100%;height:100%;object-fit:cover;transform:scale(1.02);transition:transform 1.4s {EASE};pointer-events:none;}}
    [data-svc-mep] .mr-card:hover .mr-fig img{{transform:scale(1.08);}}
    [data-svc-mep] .mr-tag{{display:flex;align-items:center;gap:12px;margin:22px 0 10px;font-family:{font};font-size:{'12px' if ar else '9px'};letter-spacing:{'normal' if ar else '0.24em'};text-transform:uppercase;color:#8B6B4A;}}
    [data-svc-mep] .mr-tag b{{font-family:'Lama Sans',sans-serif;font-weight:500;font-size:11px;letter-spacing:0.18em;}}
    [data-svc-mep] .mr-feel{{position:relative;display:inline-block;margin:0 0 12px;padding-bottom:10px;font-family:{font};font-weight:500;font-size:clamp(20px,1.7vw,25px);line-height:1.25;color:#1F1F1F;}}
    [data-svc-mep] .mr-feel::after{{content:"";position:absolute;bottom:0;inset-inline-start:0;width:100%;height:1px;background:#8B6B4A;transform:scaleX(0);transform-origin:{'100%' if ar else '0%'} 50%;transition:transform 0.7s {EASE};}}
    [data-svc-mep] .mr-card:hover .mr-feel::after{{transform:scaleX(1);}}
    [data-svc-mep] .mr-desc{{margin:0;max-width:34ch;font-family:{font};font-size:{'14px' if ar else '13px'};line-height:1.7;color:#5B4636;}}
    [data-svc-mep] .mr-bar{{display:flex;align-items:center;gap:clamp(16px,2vw,28px);margin-top:clamp(32px,3.4vw,48px);}}
    [data-svc-mep] .mr-count{{font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.2em;color:#8B6B4A;white-space:nowrap;}}
    [data-svc-mep] .mr-track{{position:relative;flex:1;height:1px;background:rgba(58,45,37,0.18);}}
    [data-svc-mep] .mr-fill{{position:absolute;top:0;inset-inline-start:0;height:1px;width:100%;background:#3A2D25;transform:scaleX(var(--mr-p,0.17));transform-origin:{'100%' if ar else '0%'} 50%;transition:transform 0.3s {EASE};}}
    [data-svc-mep] .mr-nav{{display:flex;gap:8px;}}
    [data-svc-mep] .mr-btn{{width:52px;height:52px;display:grid;place-items:center;padding:0;background:transparent;border:1px solid rgba(58,45,37,0.35);color:#3A2D25;cursor:pointer;transition:background 0.4s {EASE},color 0.4s {EASE},border-color 0.4s {EASE},opacity 0.4s {EASE};}}
    [data-svc-mep] .mr-btn:hover,[data-svc-mep] .mr-btn:focus-visible{{background:#3A2D25;border-color:#3A2D25;color:#F5F2ED;}}
    [data-svc-mep] .mr-btn:disabled{{opacity:0.3;pointer-events:none;}}
    [data-svc-mep] .mr-cap{{margin:18px 0 0;font-family:{font};font-size:{'12px' if ar else '11px'};color:#8B6B4A;}}
    [data-svc-mep] .mr-rise{{opacity:0;transform:translateY(24px);transition:opacity 0.9s {EASE},transform 0.9s {EASE};}}
    [data-svc-mep].is-in .mr-rise{{opacity:1;transform:none;}}
    [data-svc-mep].is-in .mr-rise--2{{transition-delay:0.12s;}}
    @media(max-width:900px){{
      [data-svc-mep] .mr-head{{grid-template-columns:1fr;}}
    }}
    @media(max-width:600px){{
      [data-svc-mep] .mr-card{{flex-basis:78vw;}}
      [data-svc-mep] .mr-cta{{width:100%;justify-content:center;box-sizing:border-box;}}
      [data-svc-mep] .mr-nav{{display:none;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-svc-mep] *{{transition:none!important;}}
      [data-svc-mep] .mr-rise,[data-svc-mep] .mr-card{{opacity:1;transform:none;}}
    }}
  </style>
  <div class="mr-wrap">
    <div class="mr-head">
      <div class="mr-rise">
        <div class="mr-eyebrow"><i></i>{c['eyebrow']}</div>
        <h2 class="mr-h2">{c['h2']}</h2>
      </div>
      <div class="mr-rise mr-rise--2">
        <p class="mr-body">{c['body']}</p>
        <a class="mr-cta" href="{c['href']}">{c['cta']}{ARROW_AR if ar else ARROW_EN}</a>
      </div>
    </div>
    <ul class="mr-rail" data-mr-rail aria-label="{c['rail']}">
{cards}
    </ul>
    <div class="mr-bar">
      <span class="mr-count" dir="ltr"><span data-mr-now>01</span> / 0{n}</span>
      <span class="mr-track" aria-hidden="true"><span class="mr-fill"></span></span>
      <span class="mr-nav"><button type="button" class="mr-btn" data-mr-prev aria-label="{c['prev']}">{prev_icon}</button><button type="button" class="mr-btn" data-mr-next aria-label="{c['next']}">{next_icon}</button></span>
    </div>
    <p class="mr-cap">{c['cap']}</p>
  </div>
</section>
"""


JS = """    // ── SERVICES, MEP: ENGINEERING YOU FEEL, NOT SEE ────────────────────────
    {
      const sec = document.querySelector('[data-svc-mep]');
      if (sec) {
        const rail = sec.querySelector('[data-mr-rail]'), cards = Array.from(rail.children);
        const prev = sec.querySelector('[data-mr-prev]'), next = sec.querySelector('[data-mr-next]'), now = sec.querySelector('[data-mr-now]');
        const rtl = sec.getAttribute('dir') === 'rtl';
        // the rail starts on the content grid and runs out to the screen edge
        const bleed = () => {
          const r = sec.querySelector('.mr-wrap').getBoundingClientRect();
          sec.style.setProperty('--mr-bleed', Math.max(0, rtl ? document.documentElement.clientWidth - r.right : r.left) + 'px');
        };
        const max = () => rail.scrollWidth - rail.clientWidth;
        const pos = () => Math.abs(rail.scrollLeft);  // RTL scrollLeft runs negative
        const sync = () => {
          const m = max(), p = m > 0 ? pos() / m : 1;
          sec.style.setProperty('--mr-p', Math.max(1 / cards.length, p).toFixed(3));
          const step = cards[1] ? Math.abs(cards[1].offsetLeft - cards[0].offsetLeft) : 1;
          const i = m - pos() < 4 ? cards.length - 1 : Math.round(pos() / step);
          now.textContent = String(Math.min(cards.length, i + 1)).padStart(2, '0');
          prev.disabled = pos() < 4; next.disabled = m - pos() < 4;
        };
        const go = (dir) => {
          const step = cards[1] ? Math.abs(cards[1].offsetLeft - cards[0].offsetLeft) : rail.clientWidth;
          rail.scrollBy({ left: dir * step * (rtl ? -1 : 1), behavior: reduced ? 'auto' : 'smooth' });
        };
        prev.addEventListener('click', () => go(-1));
        next.addEventListener('click', () => go(1));
        rail.addEventListener('scroll', () => requestAnimationFrame(sync), { passive: true });
        // drag to scroll with a mouse; touch keeps its native swipe
        let down = false, sx = 0, sl = 0, moved = false;
        rail.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse' || e.button !== 0) return; down = true; moved = false; sx = e.clientX; sl = rail.scrollLeft; });
        window.addEventListener('pointermove', (e) => {
          if (!down) return;
          const dx = e.clientX - sx;
          if (!moved && Math.abs(dx) > 4) { moved = true; rail.classList.add('is-drag'); }
          if (moved) rail.scrollLeft = sl - dx;
        });
        window.addEventListener('pointerup', () => {
          if (!down) return; down = false;
          if (moved) {
            rail.classList.remove('is-drag');
            const step = cards[1] ? Math.abs(cards[1].offsetLeft - cards[0].offsetLeft) : 1;
            rail.scrollTo({ left: (rtl ? -1 : 1) * Math.round(pos() / step) * step, behavior: reduced ? 'auto' : 'smooth' });
          }
        });
        bleed(); sync();
        window.addEventListener('resize', () => { bleed(); sync(); });
        new IntersectionObserver((es) => { es.forEach((e) => { if (e.isIntersecting) sec.classList.add('is-in'); }); }, { threshold: 0.15 }).observe(sec);
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

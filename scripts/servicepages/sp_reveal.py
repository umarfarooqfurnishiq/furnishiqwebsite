"""Service pages, intro: the reveal.

The template for the intro of the four service pages: one picture changes state as the page scrolls. The page's
first image (a line drawing, a bare shell) holds; then its second (the render, the finished space) resolves over
it tile by tile, the way a render engine fills its buckets, spiralling out from the centre, with corner
brackets on the tiles in progress and a percentage readout; then the readout signs it off. The two images must
align pixel for pixel. A band below names the three states.
Interior Design: the grand majlis drawn, rendered, approved for build.
Fit-Out: a raw shell, built out, handed over.
Pinned and scroll-driven on desktop; on phones it plays on its own and answers to the band.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/servicepages/sp_reveal.py [page ...]
"""
import re, sys

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
# the "before" of every reveal is monochrome and turns to full colour as the work completes: the design drawing is
# already cream on walnut, and the other pages' before images are toned to the same warm walnut-to-cream duotone
# (baked into the -toned files, so every browser shows the same picture)
PAGE = {
  "services-interior-design": dict(
    a="grand-majlis-line-drawing", aw=[1920, 2752], b="courtyard-residence-grand-majlis-riyadh", bw=[1280, 1920, 2752], size=(1920, 1072),
    C={
    "en": dict(
        eyebrow="Our Interior Design Services", h2="Where Inspiration Becomes Your Reality",
        sub="Every room designed, rendered and approved before a single wall is built.",
        drawing="Line drawing", rendering="Rendering", approved="Approved for build",
        names=["Drawn", "Rendered", "Approved"],
        descs=["Plan, elevations and every joinery detail, drawn to scale.",
               "Materials, light and furniture resolved in a photoreal render.",
               "Signed off on screen, so the build matches it exactly."],
        cap="Courtyard Residence · Grand majlis · Concept visualisation", tabs="Design stages",
        alt="The grand majlis of the Courtyard Residence, first as a line drawing, then as a photoreal render",
    ),
    "ar": dict(
        eyebrow="خدمات التصميم الداخلي لدينا", h2="حيث يتحول الإلهام إلى واقعك",
        sub="كل مساحة تُصمَّم وتُجسَّد وتُعتمد قبل بناء أي جدار.",
        drawing="رسم خطي", rendering="جارٍ التجسيد", approved="معتمد للتنفيذ",
        names=["مرسوم", "مُجسَّد", "معتمد"],
        descs=["المخطط والواجهات وكل تفاصيل النجارة، مرسومة بمقياس دقيق.",
               "الخامات والإضاءة والأثاث في تصور واقعي ثلاثي الأبعاد.",
               "اعتماد على الشاشة، ليطابق التنفيذ التصور تماماً."],
        cap="منزل الفناء · المجلس الكبير · تصور تصميمي", tabs="مراحل التصميم",
        alt="المجلس الكبير في منزل الفناء، أولاً رسماً خطياً ثم تصوراً واقعياً",
    ),
  }),
  "services-fitout": dict(
    a="fitout-reveal-hotel-lobby-shell-toned", aw=[1280, 1920, 2400], b="fitout-reveal-hotel-lobby-finished", bw=[1280, 1920, 2400], size=(2400, 1792),
    C={
    "en": dict(
        eyebrow="Our Fit-Out Services", h2="Total Spatial Transformation",
        sub="From raw shell to finished space, delivered turnkey by one accountable team.",
        drawing="Raw shell", rendering="Building", approved="Handed over",
        names=["Shell", "Built", "Handed over"],
        descs=["Bare slab, exposed services and open glazing, surveyed before work begins.",
               "Partitions, ceilings, finishes and joinery installed by one site team.",
               "Inspected against the approved design and handed over ready for use."],
        cap="Hotel lobby fit-out · Concept visualisation", tabs="Fit-out stages",
        alt="A double-height hotel lobby, first as a raw concrete shell, then finished in walnut, travertine and bronze",
    ),
    "ar": dict(
        eyebrow="خدمات التشطيبات لدينا", h2="تحول شامل للمساحة",
        sub="من الهيكل الخام إلى المساحة المنجزة، تسليم على المفتاح بفريق واحد مسؤول.",
        drawing="هيكل خام", rendering="جارٍ التنفيذ", approved="تم التسليم",
        names=["الهيكل", "التنفيذ", "التسليم"],
        descs=["بلاطة خرسانية وأنظمة مكشوفة وواجهات زجاجية، تُمسح قبل بدء العمل.",
               "القواطع والأسقف والتشطيبات والنجارة بفريق موقع واحد.",
               "فحص مطابق للتصميم المعتمد، وتسليم المساحة جاهزة للاستخدام."],
        cap="تشطيب ردهة فندق · تصور تصميمي", tabs="مراحل التشطيب",
        alt="ردهة فندق بارتفاع مزدوج، أولاً هيكلاً خرسانياً خاماً، ثم مُشطّبة بخشب الجوز والترافرتين والبرونز",
    ),
  }),
}
PAGE["services-mep"] = dict(
    a="mep-reveal-executive-lounge-services-open-toned", aw=[1280, 1920, 2400], b="mep-reveal-executive-lounge-finished", bw=[1280, 1920, 2400], size=(2400, 1792),
    C={
    "en": dict(
        eyebrow="Our Engineering Services", h2="The Foundation of High-Performance Environments",
        sub="Every system coordinated above the ceiling, so nothing shows below it.",
        drawing="Services open", rendering="Closing up", approved="Commissioned",
        names=["Open", "Closed", "Commissioned"],
        descs=["Ducts, cable trays, sprinkler mains and pipework, coordinated in the ceiling void.",
               "Ceiling, diffusers, lights and sprinkler heads set in one aligned line.",
               "Every system tested, balanced and certified before handover."],
        cap="Executive lounge · Concept visualisation", tabs="Engineering stages",
        alt="An executive lounge in Riyadh, first with its ceiling open on ducts, cable trays and sprinkler pipes, then closed in walnut and finished",
    ),
    "ar": dict(
        eyebrow="خدماتنا الهندسية", h2="الأساس المتين للبيئات عالية الأداء",
        sub="كل نظام منسّق فوق السقف، فلا يظهر شيء تحته.",
        drawing="الأنظمة مكشوفة", rendering="جارٍ الإغلاق", approved="تم التشغيل",
        names=["مكشوف", "مُغلق", "مُشغَّل"],
        descs=["مجاري الهواء وحوامل الكابلات وخطوط الرشاشات والأنابيب، منسّقة في فراغ السقف.",
               "السقف وفتحات التكييف والإضاءة ورؤوس الرشاشات في خط واحد متناسق.",
               "كل نظام يُختبر ويُوازن ويُعتمد قبل التسليم."],
        cap="صالة تنفيذية · تصور تصميمي", tabs="مراحل التنفيذ الهندسي",
        alt="صالة تنفيذية في الرياض، أولاً بسقف مفتوح على مجاري الهواء وحوامل الكابلات وأنابيب الرشاشات، ثم مغلقاً بخشب الجوز ومُشطّباً",
    ),
  })
PAGE["services-furniture"] = dict(
    a="furniture-reveal-villa-lounge-empty-toned", aw=[1280, 1920, 2400], b="furniture-reveal-villa-lounge-furnished", bw=[1280, 1920, 2400], size=(2400, 1792),
    C={
    "en": dict(
        eyebrow="Our Furniture Solutions", h2="The Final Layer of Spatial Perfection",
        sub="Every piece sourced and placed to match the approved render.",
        drawing="Empty room", rendering="Placing", approved="Styled",
        names=["Empty", "Placed", "Styled"],
        descs=["The finished room, measured and ready for its furniture.",
               "Every piece delivered, assembled and set where the render placed it.",
               "Textiles, lighting and objects layered in, and the room handed over."],
        cap="Villa family lounge · Concept visualisation", tabs="Furniture stages",
        alt="A villa family lounge under timber beams, first empty on its travertine floor, then furnished with a bouclé sofa, leather lounge chairs, a travertine table and linen curtains",
    ),
    "ar": dict(
        eyebrow="حلول الأثاث لدينا", h2="الطبقة الأخيرة من الكمال المكاني",
        sub="كل قطعة تُورَّد وتوضع مطابقة للتصور المعتمد.",
        drawing="غرفة فارغة", rendering="جارٍ التوزيع", approved="مُنسَّقة",
        names=["فارغة", "مؤثثة", "مُنسَّقة"],
        descs=["الغرفة المنجزة، مقاسة وجاهزة لأثاثها.",
               "كل قطعة تُسلَّم وتُركَّب وتوضع حيث حددها التصور.",
               "الأقمشة والإضاءة والقطع الفنية تكتمل، وتُسلَّم الغرفة."],
        cap="صالة عائلية في فيلا · تصور تصميمي", tabs="مراحل الأثاث",
        alt="صالة عائلية في فيلا تحت عوارض خشبية، أولاً فارغة على أرضيتها من الترافرتين، ثم مؤثثة بأريكة بوكليه وكراسٍ جلدية وطاولة ترافرتين وستائر كتان",
    ),
  })
TICK = '<svg class="ir-tick" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="4 12.5 9.5 18 20 6"/></svg>'


def build(page, lang):
    ar = lang == "ar"
    P = PAGE[page]
    c = P["C"][lang]
    imgs = f'data-a="{P["a"]}" data-aw="{",".join(map(str, P["aw"]))}" data-b="{P["b"]}" data-bw="{",".join(map(str, P["bw"]))}" data-iw="{P["size"][0]}" data-ih="{P["size"][1]}"'
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    caps = "normal" if ar else "0.22em"
    small = "12px" if ar else "9px"
    PAD = "clamp(24px,5vw,80px)"
    tabs = "\n".join(f'''        <button type="button" class="ir-tab" data-ir-tab="{k}"><i class="ir-prog" aria-hidden="true"></i><span class="ir-n" dir="ltr">0{k + 1}</span><span class="ir-tx"><b>{c['names'][k]}</b><span>{c['descs'][k]}</span></span></button>''' for k in range(3))
    labels = f'data-l0="{c["drawing"]}" data-l1="{c["rendering"]}" data-l2="{c["approved"]}"'
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ INTRO ━━━━━ -->
<section id="id-render" data-screen-label="Intro" data-id-render{' dir="rtl"' if ar else ''} style="scroll-margin-top:80px;background:#F5F2ED;color:#3A2D25;position:relative;padding:clamp(64px,8vw,100px) {PAD} 0;overflow:clip;">
  <style>
    [data-id-render] .ir-wrap{{max-width:1280px;margin:0 auto;}}
    [data-id-render] .ir-head{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:clamp(32px,5vw,88px);align-items:end;margin-bottom:clamp(40px,4.4vw,64px);}}
    [data-id-render] .ir-eyebrow{{display:flex;align-items:center;gap:16px;margin-bottom:24px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    [data-id-render] .ir-eyebrow i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    [data-id-render] .ir-h2{{font-family:{font};font-weight:500;font-size:clamp(32px,3.8vw,54px);line-height:1.08;letter-spacing:{'0' if ar else '-0.015em'};color:#1F1F1F;margin:0;text-wrap:balance;}}
    [data-id-render] .ir-sub{{font-family:{font};font-weight:500;font-size:{'clamp(22px,2vw,28px)' if ar else 'clamp(20px,1.9vw,26px)'};line-height:1.4;letter-spacing:{'0' if ar else '-0.005em'};text-wrap:balance;max-width:{'18em' if ar else '30ch'};color:#3A2D25;margin:0;}}
    [data-id-render] .ir-rise{{opacity:0;transform:translateY(24px);transition:opacity 0.9s {EASE},transform 0.9s {EASE};}}
    [data-id-render].is-in .ir-rise{{opacity:1;transform:none;}}
    [data-id-render].is-in .ir-rise--2{{transition-delay:0.12s;}}
    [data-id-render].is-in .ir-rise--3{{transition-delay:0.24s;}}
    [data-id-render] .ir-block{{margin-inline:calc(50% - 50vw + var(--ir-sb,0px) / 2);background:#3A2D25;}}
    [data-id-render] .ir-stage{{position:relative;height:min(calc(100vh - 80px - var(--ir-band,104px)),55.84vw);height:min(calc(100svh - 80px - var(--ir-band,104px)),55.84vw);min-height:440px;overflow:hidden;background:#1F1F1F;}}
    [data-id-render] .ir-canvas{{position:absolute;inset:0;width:100%;height:100%;display:block;}}
    [data-id-render] .ir-in{{position:absolute;inset:0;width:min(1280px,calc(100% - 2 * {PAD}));margin:0 auto;pointer-events:none;}}
    [data-id-render] .ir-chip{{position:absolute;top:clamp(16px,2.2vw,32px);inset-inline-start:0;display:inline-flex;align-items:center;gap:12px;padding:11px 16px;background:rgba(31,31,31,0.72);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);color:#F5F2ED;font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;transition:background 0.6s {EASE},color 0.6s {EASE};}}
    [data-id-render] .ir-dot{{width:7px;height:7px;flex:none;border-radius:50%;background:#D6C2A8;animation:irPulse 1.4s {EASE} infinite;}}
    @keyframes irPulse{{0%,100%{{opacity:1;}}50%{{opacity:0.25;}}}}
    [data-id-render] .ir-pct{{font-family:'Lama Sans',sans-serif;letter-spacing:0.12em;color:#D6C2A8;}}
    [data-id-render] .ir-tick{{display:none;}}
    [data-id-render] .ir-chip.is-drawn .ir-dot,[data-id-render] .ir-chip.is-drawn .ir-pct{{display:none;}}
    [data-id-render] .ir-chip.is-done{{background:#D6C2A8;color:#1F1F1F;}}
    [data-id-render] .ir-chip.is-done .ir-dot,[data-id-render] .ir-chip.is-done .ir-pct{{display:none;}}
    [data-id-render] .ir-chip.is-done .ir-tick{{display:block;}}
    [data-id-render] .ir-cap{{position:absolute;bottom:clamp(14px,2vw,24px);inset-inline-end:0;margin:0;padding:7px 12px;background:rgba(31,31,31,0.62);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);color:rgba(245,242,237,0.85);font-family:{font};font-size:{'12px' if ar else '10.5px'};}}
    [data-id-render] .ir-tabs{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));width:min(1280px,calc(100% - 2 * {PAD}));margin:0 auto;}}
    [data-id-render] .ir-tab{{position:relative;display:flex;align-items:flex-start;gap:16px;padding:24px clamp(14px,1.8vw,26px) 26px;border:0;border-inline-start:1px solid rgba(245,242,237,0.12);background:transparent;color:rgba(245,242,237,0.5);text-align:start;cursor:pointer;transition:color 0.4s {EASE},background 0.4s {EASE};}}
    [data-id-render] .ir-tab:first-child{{border-inline-start:0;}}
    [data-id-render] .ir-tab:hover{{color:#F5F2ED;background:rgba(245,242,237,0.04);}}
    [data-id-render] .ir-tab:focus-visible{{outline:1px solid #D6C2A8;outline-offset:-4px;}}
    [data-id-render] .ir-tab.is-on{{color:#F5F2ED;}}
    [data-id-render] .ir-prog{{position:absolute;top:0;left:0;right:0;height:2px;background:rgba(245,242,237,0.1);}}
    [data-id-render] .ir-prog::after{{content:"";position:absolute;inset:0;background:#D6C2A8;transform:scaleX(var(--p,0));transform-origin:{'100%' if ar else '0%'} 50%;}}
    [data-id-render] .ir-n{{flex:none;padding-top:2px;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.2em;color:#D6C2A8;}}
    [data-id-render] .ir-tx{{display:flex;flex-direction:column;gap:6px;}}
    [data-id-render] .ir-tx b{{font-weight:500;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.18em'};text-transform:uppercase;}}
    [data-id-render] .ir-tx span{{font-family:{font};font-size:{'14px' if ar else '13px'};line-height:1.6;color:rgba(245,242,237,0.6);}}
    @media(min-width:901px) and (min-height:600px){{
      [data-id-render] .ir-block{{position:sticky;top:80px;}}
      [data-id-render] .ir-spacer{{height:220vh;}}
    }}
    @media(max-width:900px){{
      [data-id-render] .ir-head{{grid-template-columns:1fr;}}
      [data-id-render] .ir-stage{{height:auto;min-height:0;aspect-ratio:1920/1072;}}
      [data-id-render] .ir-in{{width:auto;inset:0 12px;}}
      [data-id-render] .ir-chip{{top:12px;padding:8px 12px;}}
      [data-id-render] .ir-cap{{display:none;}}
      [data-id-render] .ir-tabs{{width:100%;}}
      [data-id-render] .ir-tab{{padding:18px 14px 20px;gap:10px;}}
      [data-id-render] .ir-tx span{{display:none;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-id-render] .ir-rise{{opacity:1;transform:none;transition:none;}}
      [data-id-render] .ir-dot{{animation:none;}}
    }}
  </style>
  <div class="ir-wrap">
    <div class="ir-head">
      <div class="ir-rise">
        <div class="ir-eyebrow"><i></i>{c['eyebrow']}</div>
        <h2 class="ir-h2">{c['h2']}</h2>
      </div>
      <p class="ir-sub ir-rise ir-rise--2">{c['sub']}</p>
    </div>
    <div class="ir-track">
    <div class="ir-block ir-rise ir-rise--3">
      <div class="ir-stage" data-ir-stage>
        <canvas class="ir-canvas" role="img" aria-label="{c['alt']}" {imgs}></canvas>
        <div class="ir-in">
          <p class="ir-chip" aria-live="polite" {labels}><i class="ir-dot" aria-hidden="true"></i><span class="ir-lbl">{c['rendering']}</span><span class="ir-pct" dir="ltr">000%</span>{TICK}</p>
          <p class="ir-cap">{c['cap']}</p>
        </div>
      </div>
      <div class="ir-band"><div class="ir-tabs" role="group" aria-label="{c['tabs']}">
{tabs}
      </div></div>
    </div>
    <div class="ir-spacer" aria-hidden="true"></div>
    </div>
  </div>
</section>
"""


JS = """    // ── SERVICE PAGES, INTRO: THE REVEAL ────────────────────────────────────
    {
      const sec = document.querySelector('[data-id-render]');
      if (sec) {
        const stage = sec.querySelector('[data-ir-stage]'), canvas = sec.querySelector('.ir-canvas'), ctx = canvas.getContext('2d');
        const block = sec.querySelector('.ir-block'), track = sec.querySelector('.ir-track');
        const chip = sec.querySelector('.ir-chip'), lbl = chip.querySelector('.ir-lbl'), pctEl = chip.querySelector('.ir-pct');
        const tabs = Array.from(sec.querySelectorAll('[data-ir-tab]'));
        const pinMQ = matchMedia('(min-width:901px) and (min-height:600px)');
        const COLS = 16, ROWS = 9, N = COLS * ROWS;
        const A = 0.1, B = 0.86;   // the line drawing holds until A; the tiles resolve until B; approved after
        // buckets in a square spiral out from the centre, the order a render engine fills them
        const order = [];
        {
          let c = Math.floor(COLS / 2) - 1, r = Math.floor(ROWS / 2), dc = 1, dr = 0, run = 1;
          const seen = new Set();
          while (order.length < N) {
            for (let twice = 0; twice < 2; twice++) {
              for (let s = 0; s < run; s++) {
                if (c >= 0 && c < COLS && r >= 0 && r < ROWS && !seen.has(r * COLS + c)) { seen.add(r * COLS + c); order.push([c, r]); }
                c += dc; r += dr;
              }
              [dc, dr] = [-dr, dc];
            }
            run++;
          }
        }
        const line = new Image(), ren = new Image();
        let p = 0, pinned = pinMQ.matches, ticking = false, auto = !reduced, visible = false, then = 0, t = 0, raf = 0;
        const pick = (base, ws) => { const want = stage.clientWidth * Math.min(2, devicePixelRatio || 1); return 'uploads/' + base + '-' + (ws.find((w) => w >= want) || ws[ws.length - 1]) + '.webp'; };
        const load = () => {
          if (line.src) return;
          line.onload = ren.onload = () => draw();
          const d = canvas.dataset, ws = (v) => v.split(',').map(Number);
          line.src = pick(d.a, ws(d.aw));
          ren.src = pick(d.b, ws(d.bw));
        };
        const size = () => {
          const d = Math.min(2, devicePixelRatio || 1);
          canvas.width = Math.round(stage.clientWidth * d); canvas.height = Math.round(stage.clientHeight * d);
          sec.style.setProperty('--ir-sb', (window.innerWidth - document.documentElement.clientWidth) + 'px');
          sec.style.setProperty('--ir-band', sec.querySelector('.ir-band').offsetHeight + 'px');
          draw();
        };
        const clamp = (v) => Math.min(1, Math.max(0, v));
        function draw() {
          const W = canvas.width, H = canvas.height;
          ctx.fillStyle = '#1F1F1F'; ctx.fillRect(0, 0, W, H);
          const iw = +canvas.dataset.iw, ih = +canvas.dataset.ih, s = Math.max(W / iw, H / ih), ox = (W - iw * s) / 2, oy = (H - ih * s) / 2;
          const r = clamp((p - A) / (B - A)), k = r * N;
          if (line.complete && line.naturalWidth) ctx.drawImage(line, ox, oy, iw * s, ih * s);
          if (ren.complete && ren.naturalWidth) {
            const sx = ren.naturalWidth / iw;
            if (r >= 1) ctx.drawImage(ren, ox, oy, iw * s, ih * s);
            else {
              const cw = iw / COLS, ch = ih / ROWS;
              for (let i = 0; i < Math.min(N, Math.ceil(k)); i++) {
                const [c, rr] = order[i], a = clamp((k - i) / 3);
                // shared, rounded edges so neighbouring tiles meet without seams
                const x0 = Math.round(ox + c * cw * s), x1 = Math.round(ox + (c + 1) * cw * s), y0 = Math.round(oy + rr * ch * s), y1 = Math.round(oy + (rr + 1) * ch * s);
                const u0 = (x0 - ox) / s, u1 = (x1 - ox) / s, v0 = (y0 - oy) / s, v1 = (y1 - oy) / s;
                ctx.globalAlpha = a;
                ctx.drawImage(ren, u0 * sx, v0 * sx, (u1 - u0) * sx, (v1 - v0) * sx, x0, y0, x1 - x0, y1 - y0);
              }
              ctx.globalAlpha = 1;
              // corner brackets on the buckets in progress
              if (r > 0) {
                ctx.strokeStyle = '#D6C2A8'; ctx.lineWidth = Math.max(1.5, W / 900);
                for (let i = Math.floor(k); i < Math.min(N, Math.floor(k) + 4); i++) {
                  const [c, rr] = order[i], x = ox + c * cw * s, y = oy + rr * ch * s, w = cw * s, h = ch * s, L = Math.min(w, h) * 0.24, g = ctx.lineWidth;
                  ctx.beginPath();
                  ctx.moveTo(x + g, y + L); ctx.lineTo(x + g, y + g); ctx.lineTo(x + L, y + g);
                  ctx.moveTo(x + w - L, y + g); ctx.lineTo(x + w - g, y + g); ctx.lineTo(x + w - g, y + L);
                  ctx.moveTo(x + w - g, y + h - L); ctx.lineTo(x + w - g, y + h - g); ctx.lineTo(x + w - L, y + h - g);
                  ctx.moveTo(x + L, y + h - g); ctx.lineTo(x + g, y + h - g); ctx.lineTo(x + g, y + h - L);
                  ctx.stroke();
                }
              }
            }
          }
          // readout and band
          const st = p < A ? 0 : p < B ? 1 : 2;
          chip.classList.toggle('is-drawn', st === 0); chip.classList.toggle('is-done', st === 2);
          lbl.textContent = chip.dataset['l' + st];
          pctEl.textContent = String(Math.round(r * 100)).padStart(3, '0') + '%';
          tabs.forEach((tb, i) => {
            tb.classList.toggle('is-on', i === st);
            tb.style.setProperty('--p', (i === 0 ? clamp(p / A) : i === 1 ? r : clamp((p - B) / (1 - B) * 1.6)).toFixed(4));
          });
        }
        const geo = () => ({ start: track.getBoundingClientRect().top + window.scrollY - 80, dist: Math.max(1, track.offsetHeight - block.offsetHeight) });
        const onScroll = () => {
          ticking = false;
          if (!pinned) return;
          const g = geo();
          p = clamp((window.scrollY - g.start) / g.dist);
          draw();
        };
        window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
        const TARGET = [A * 0.5, (A + B) / 2, 1];
        // one wheel notch, one stage: drawn, rendering, approved (STEP SNAP)
        (window.fiqSnap = window.fiqSnap || []).push({ on: () => pinned, geo: () => { const g = geo(); return { a: g.start, b: g.start + g.dist, stops: TARGET.map((t) => g.start + g.dist * t) }; } });
        tabs.forEach((tb, i) => tb.addEventListener('click', () => {
          auto = false;
          if (pinned) { const g = geo(); window.scrollTo({ top: g.start + g.dist * Math.min(0.999, TARGET[i]), behavior: reduced ? 'auto' : 'smooth' }); }
          else { p = TARGET[i]; draw(); }
        }));
        // phones: the render plays through, holds on the approved room, and starts again
        const PLAY = 7000, HOLD = 3200;
        document.addEventListener('visibilitychange', () => { then = 0; });
        const loop = (now) => {
          // real time between frames, so a throttled frame rate does not slow the cycle
          const dt = then ? now - then : 0; then = now;
          if (!pinned && auto && !document.hidden) {
            t = (t + dt) % (PLAY + HOLD);
            p = clamp(t / PLAY);
            draw();
          }
          raf = visible ? requestAnimationFrame(loop) : 0;
        };
        new IntersectionObserver((es, o) => { es.forEach((e) => { if (e.isIntersecting) { sec.classList.add('is-in'); load(); o.disconnect(); } }); }, { rootMargin: '0px 0px 25% 0px' }).observe(sec);
        new IntersectionObserver((es) => {
          es.forEach((e) => { visible = e.isIntersecting; if (visible && !raf) { then = 0; raf = requestAnimationFrame(loop); } });
        }, { threshold: 0.3 }).observe(stage);
        pinMQ.addEventListener('change', () => { pinned = pinMQ.matches; if (pinned) onScroll(); });
        if (reduced && !pinned) p = 1;
        window.addEventListener('resize', size);
        if (document.fonts) document.fonts.ready.then(size);
        size(); onScroll();
      }
    }

"""
MARK = "    // ── SCROLL REVEAL"

pages = sys.argv[1:] or list(PAGE)
for page in pages:
    for path, lang in [(f"{page}.dc.html", "en"), (f"{page}.ar.dc.html", "ar")]:
        s = open(path, encoding="utf-8").read()
        s, n = re.subn(r"<!-- ━+ INTRO ━+ -->\n<section [^>]*data-screen-label=\"Intro\".*?\n</section>\n", lambda m: build(page, lang), s, count=1, flags=re.S)
        assert n == 1, path
        for old in ("    // ── INTERIOR DESIGN, INTRO:", "    // ── SERVICE PAGES, INTRO:"):
            if old in s:
                a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
                s = s[:a] + s[b:]
        assert s.count(MARK) == 1, path
        s = s.replace(MARK, JS + MARK)
        open(path, "w", encoding="utf-8", newline="").write(s)
        print(path, "ok")

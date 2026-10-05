import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
CATS = ["Residential", "Hospitality", "Workplace", "Retail"]
IMGS = [
    ["penthouse-wadi-double-height-living-riyadh", "obhur-estate-great-room-red-sea-jeddah", "courtyard-residence-formal-dining-room"],
    ["desert-stone-resort-lobby-lounge-alula", "roastery-house-espresso-bar-travertine", "desert-stone-resort-signature-restaurant"],
    ["executive-floors-boardroom-walnut-table", "family-office-council-room-oak-table", "executive-floors-client-majlis"],
    ["maison-joaillerie-main-salon-jeddah", "central-commons-covered-galleria", "maison-joaillerie-private-salon"],
]
C = {
    "en": dict(
        label="Markets We Serve", h2="One integrated team, delivering across every sector.",
        note="Hover a market to preview concept work.", link="View projects", cap="Concept visualisation", pre="",
        rows=[("Residential", "Villas, palaces, penthouses and family estates."),
              ("Hospitality", "Resorts, hotels, restaurants and cafés."),
              ("Workplace", "Headquarters, executive floors and family offices."),
              ("Retail", "Flagship stores, boutiques and destination malls.")],
    ),
    "ar": dict(
        label="الأسواق التي نخدمها", h2="فريق متكامل واحد، يُنجز عبر كل قطاع.",
        note="مرّر المؤشر على أي قطاع لمعاينة أعمال مفاهيمية.", link="عرض المشاريع", cap="تصور مفاهيمي", pre="/ar",
        rows=[("سكني", "الفلل والقصور والشقق الفاخرة والمجمعات العائلية."),
              ("ضيافة", "المنتجعات والفنادق والمطاعم والمقاهي."),
              ("مكاتب", "المقرات الرئيسية والطوابق التنفيذية ومكاتب العائلات."),
              ("تجزئة", "المتاجر الرئيسية والبوتيكات ومراكز التسوق.")],
    ),
}
ARROW_EN = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
ARROW_AR = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>'


def img(name, cls="", lazy=True):
    return (f'<img{(" class=" + chr(34) + cls + chr(34)) if cls else ""} src="uploads/{name}-1280.webp" alt="" width="1280" height="714"'
            f'{" loading=" + chr(34) + "lazy" + chr(34) if lazy else ""} decoding="async">')


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    arrow = ARROW_AR if ar else ARROW_EN
    rows, sets = "", ""
    for i, (word, desc) in enumerate(c["rows"]):
        strip = "".join(img(n) for n in IMGS[i])
        rows += f"""
      <a class="mk-row" href="{c['pre']}/projects?category={CATS[i]}" data-mk-row style="--i:{i};">
        <span class="mk-n" dir="ltr">0{i + 1}</span>
        <span class="mk-mask"><span class="mk-word">{word}</span></span>
        <span class="mk-desc">{desc}</span>
        <span class="mk-go">{c['link']}{arrow}</span>
        <span class="mk-strip" aria-hidden="true">{strip}</span>
      </a>"""
        sets += f"""
        <span class="mk-set" data-mk-set>{"".join(img(n, "is-front" if k == 0 else "") for k, n in enumerate(IMGS[i]))}</span>"""
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ MARKETS WE SERVE ━ -->
<section id="markets" data-markets{' dir="rtl"' if ar else ''} style="position:relative;background:#FFFFFF;padding:clamp(64px,8vw,100px) clamp(24px,5vw,80px);overflow:clip;">
  <style>
    #markets .mk-wrap{{max-width:1280px;margin:0 auto;}}
    #markets .mk-head{{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,4fr);gap:clamp(32px,5vw,96px);align-items:end;margin-bottom:clamp(36px,4.5vw,64px);}}
    #markets .mk-label{{display:flex;align-items:center;gap:16px;margin-bottom:20px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    #markets .mk-label i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    #markets .mk-h2{{font-family:{font};font-size:clamp(28px,3.2vw,50px);font-weight:500;line-height:{'1.4' if ar else '1.12'};letter-spacing:{'normal' if ar else '-0.02em'};color:#3A2D25;margin:0;max-width:760px;}}
    #markets .mk-note{{font-family:{font};font-size:{'14px' if ar else '13px'};line-height:1.7;color:#8B6B4A;margin:0;justify-self:end;text-align:end;}}
    #markets .mk-list{{position:relative;border-bottom:1px solid rgba(58,45,37,0.16);}}
    #markets .mk-row{{position:relative;display:grid;grid-template-columns:clamp(40px,4vw,64px) minmax(0,1fr) minmax(0,300px) auto;align-items:center;column-gap:clamp(16px,2.4vw,40px);padding:clamp(14px,1.6vw,22px) clamp(12px,1.6vw,24px);text-decoration:none;color:#3A2D25;border-top:1px solid rgba(58,45,37,0.16);isolation:isolate;outline:none;}}
    #markets .mk-row::before{{content:"";position:absolute;inset:-1px 0;z-index:-1;background:#3A2D25;transform:scaleX(0);transform-origin:{'right' if ar else 'left'};transition:transform 0.6s {EASE};}}
    #markets .mk-row.is-hot::before{{transform:scaleX(1);}}
    #markets .mk-n{{font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.2em;color:#8B6B4A;transition:color 0.5s {EASE};}}
    #markets .mk-mask{{display:block;overflow:hidden;padding-bottom:0.06em;}}
    #markets .mk-word{{display:block;font-family:{font};font-size:clamp(38px,5.4vw,92px);font-weight:500;line-height:{'1.25' if ar else '1'};letter-spacing:{'normal' if ar else '-0.04em'};color:#3A2D25;transform:translateY(105%);transition:transform 1s {EASE} calc(var(--i) * 0.12s),color 0.5s {EASE};}}
    #markets .mk-row.is-in .mk-word{{transform:none;}}
    #markets .mk-desc{{font-family:{font};font-size:{'15px' if ar else '14px'};line-height:1.7;color:#5B4636;transition:color 0.5s {EASE};}}
    #markets .mk-go{{display:inline-flex;align-items:center;gap:12px;white-space:nowrap;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;color:#3A2D25;transition:color 0.5s {EASE},gap 0.5s {EASE};}}
    #markets .mk-row.is-hot .mk-word{{color:#F5F2ED;}}
    #markets .mk-row.is-hot .mk-desc{{color:rgba(245,242,237,0.75);}}
    #markets .mk-row.is-hot .mk-n,#markets .mk-row.is-hot .mk-go{{color:#D6C2A8;}}
    #markets .mk-row.is-hot .mk-go{{gap:18px;}}
    #markets .mk-row:focus-visible{{outline:1px solid #8B6B4A;outline-offset:-1px;}}
    #markets .mk-strip{{display:none;}}
    #markets .mk-card{{position:absolute;z-index:3;top:0;left:0;width:clamp(240px,21vw,340px);aspect-ratio:4/5;pointer-events:none;overflow:hidden;background:#E5DCD0;box-shadow:0 24px 80px rgba(58,45,37,0.2);clip-path:inset(50% 50% 50% 50%);transition:clip-path 0.55s {EASE};will-change:transform;}}
    #markets .mk-card.is-on{{clip-path:inset(0 0 0 0);}}
    #markets .mk-set{{position:absolute;inset:0;display:none;}}
    #markets .mk-set.is-active{{display:block;}}
    #markets .mk-set img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.08);transition:opacity 0.5s {EASE},transform 1.6s {EASE};}}
    #markets .mk-set img.is-front{{opacity:1;transform:scale(1);}}
    #markets .mk-cap{{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:10px 14px;background:rgba(30,22,16,0.72);font-family:{font};font-size:{'12px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.18em'};text-transform:uppercase;color:#F5F2ED;}}
    @media(max-width:900px),(hover:none){{
      #markets .mk-head{{grid-template-columns:1fr;gap:16px;}}
      #markets .mk-note{{display:none;}}
      #markets .mk-card{{display:none;}}
      #markets .mk-row{{grid-template-columns:auto minmax(0,1fr);row-gap:10px;padding:24px 0;}}
      #markets .mk-row::before{{display:none;}}
      #markets .mk-desc,#markets .mk-go{{grid-column:2;}}
      #markets .mk-strip{{grid-column:1 / -1;display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;margin:8px calc(-1 * clamp(24px,5vw,80px)) 0;padding:0 clamp(24px,5vw,80px);scrollbar-width:none;}}
      #markets .mk-strip::-webkit-scrollbar{{display:none;}}
      #markets .mk-strip img{{flex:0 0 58%;height:auto;align-self:flex-start;aspect-ratio:4/3;object-fit:cover;scroll-snap-align:start;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      #markets *{{transition:none!important;}}
      #markets .mk-word{{transform:none;}}
    }}
  </style>
  <div class="mk-wrap">
    <div class="mk-head" data-reveal style="opacity:0;transform:translateY(18px);transition:opacity 0.8s {EASE},transform 0.8s {EASE};">
      <div>
        <div class="mk-label"><i></i>{c['label']}</div>
        <h2 class="mk-h2">{c['h2']}</h2>
      </div>
      <p class="mk-note">{c['note']}</p>
    </div>
    <div class="mk-list" data-mk-list>{rows}
      <div class="mk-card" aria-hidden="true">{sets}
        <span class="mk-cap">{c['cap']}</span>
      </div>
    </div>
  </div>
</section>
"""


JS = """    // ── MARKETS: INDEX ROWS WITH A FLOATING FLIPBOOK PREVIEW ─────────────────
    {
      const mk = document.querySelector('[data-markets]');
      if (mk) {
        const list = mk.querySelector('[data-mk-list]'), rows = [...mk.querySelectorAll('[data-mk-row]')];
        const card = mk.querySelector('.mk-card'), sets = [...mk.querySelectorAll('[data-mk-set]')];
        if (reduced) rows.forEach(r => r.classList.add('is-in'));
        else {
          const io = new IntersectionObserver((es) => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -12% 0px' });
          rows.forEach(r => io.observe(r));
        }
        const fine = window.matchMedia('(hover:hover) and (pointer:fine) and (min-width:901px)');
        let active = -1, tx = 0, ty = 0, x = 0, y = 0, raf = 0, flip = 0, shown = false;
        const loop = () => {
          x += (tx - x) * 0.14; y += (ty - y) * 0.14;
          const tilt = Math.max(-7, Math.min(7, (tx - x) * 0.05));
          card.style.transform = 'translate3d(' + (x - card.offsetWidth / 2).toFixed(1) + 'px,' + (y - card.offsetHeight / 2).toFixed(1) + 'px,0) rotate(' + tilt.toFixed(2) + 'deg)';
          raf = Math.abs(tx - x) + Math.abs(ty - y) > 0.3 ? requestAnimationFrame(loop) : 0;
        };
        const kick = () => { if (!raf) raf = requestAnimationFrame(loop); };
        const play = (n) => {
          clearInterval(flip);
          const imgs = [...sets[n].querySelectorAll('img')]; let k = 0;
          imgs.forEach((im, j) => im.classList.toggle('is-front', j === 0));
          if (!reduced) flip = setInterval(() => { k = (k + 1) % imgs.length; imgs.forEach((im, j) => im.classList.toggle('is-front', j === k)); }, 950);
        };
        const activate = (n) => {
          rows.forEach((r, k) => r.classList.toggle('is-hot', k === n));
          if (n === active) return;
          active = n;
          sets.forEach((s, k) => s.classList.toggle('is-active', k === n));
          play(n);
        };
        const release = () => {
          rows.forEach(r => r.classList.remove('is-hot'));
          card.classList.remove('is-on'); shown = false; active = -1; clearInterval(flip);
        };
        const rtl = mk.dir === 'rtl';
        const aim = (cx, cy, snap) => {
          const r = list.getBoundingClientRect(), w = card.offsetWidth, h = card.offsetHeight;
          const side = (w / 2 + 32) * (rtl ? -1 : 1);
          tx = Math.min(Math.max(cx - r.left + side, w / 2), r.width - w / 2);
          ty = Math.min(Math.max(cy - r.top, h / 2 - 40), r.height - h / 2 + 40);
          if (snap) { x = tx; y = ty; }
          kick();
        };
        rows.forEach((row, n) => {
          row.addEventListener('pointerenter', (e) => {
            if (!fine.matches || reduced) { if (fine.matches) activate(n); return; }
            activate(n);
            aim(e.clientX, e.clientY, !shown);
            shown = true; card.classList.add('is-on');
          });
          row.addEventListener('focus', () => {
            activate(n);
            if (!fine.matches || reduced) return;
            const r = row.getBoundingClientRect();
            aim(r.left + r.width * (rtl ? 0.45 : 0.55), r.top + r.height / 2, !shown);
            shown = true; card.classList.add('is-on');
          });
          row.addEventListener('blur', release);
        });
        list.addEventListener('pointermove', (e) => { if (shown) aim(e.clientX, e.clientY, false); });
        list.addEventListener('pointerleave', release);
      }
    }

"""
MARK = "    // ── FADE-IN ON LOAD (lazy images)"

for path, lang in [("about-us.dc.html", "en"), ("about-us.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ MARKETS WE SERVE ━ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── MARKETS: INDEX ROWS"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

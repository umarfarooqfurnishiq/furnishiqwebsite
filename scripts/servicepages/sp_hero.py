"""Service pages, hero: one sheet of the drawing set.

The template hero for the four service pages, drawn as a sheet from an architect's set. A charcoal sheet
with a faint grid carries the service photograph, plotted onto it with crop marks and a dimension line naming
the project; the title sits large on the sheet and runs onto the photograph's edge, with the slogan and two
calls to action. Along the bottom, the sheet's title block is the index of the set: ID-01 Interior Design,
FO-02 Fit-Out, ME-03 Engineering & MEP, FF-04 Furniture, this page's sheet filled in and the others links to
theirs. Each service page is another sheet of the same set.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/servicepages/sp_hero.py [page ...]
"""
import re, sys

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
# the set, in the Services order: page, sheet code, names, the thumbnail in its title-block cell
SET = [
    ("services-interior-design", "ID-01", "Interior Design", "التصميم الداخلي", "luxury-interior-design-material-board-riyadh-600"),
    ("services-fitout", "FO-02", "Fit-Out", "التشطيبات", "luxury-villa-fit-out-travertine-staircase-walnut-wall-riyadh-800"),
    ("services-mep", "ME-03", "Engineering & MEP", "الهندسة والأنظمة الكهروميكانيكية", "mep-ceiling-services-installation-riyadh-600"),
    ("services-furniture", "FF-04", "Furniture", "حلول الأثاث", "furniture-gallery-living-room-set-1280"),
]
# each sheet: its photograph, the project it shows, the slogan, and the link down into the page
PAGE = {
    "services-interior-design": dict(
        img="courtyard-residence-central-courtyard-reflecting-pool", widths=(1280, 1920, 2752), pos="50% 55%",
        project=("Courtyard Residence · Concept visualisation", "منزل الفناء · تصور تصميمي"),
        slogan=("Architectural vision, tailored to the way you live and work.", "رؤية معمارية مصممة على طريقة عيشك وعملك."),
        more=("See how we design", "شاهد كيف نصمم"), anchor="#id-render",
        alt=("A courtyard at dusk: a reflecting pool and an olive tree between lit timber mashrabiya screens",
             "فناء عند الغسق: حوض عاكس وشجرة زيتون بين مشربيات خشبية مضاءة")),
    "services-fitout": dict(
        img="roastery-house-espresso-bar-travertine", widths=(1280, 1920, 2752), pos="50% 50%",
        project=("Roastery House Flagship · Concept visualisation", "بيت المحمصة · تصور تصميمي"),
        slogan=("From raw shell to turnkey space, on schedule and without compromise.", "من الهيكل الخام إلى مساحة جاهزة للتسليم، في موعدها ودون أي تنازلات."),
        more=("See the transformation", "شاهد التحول"), anchor="#id-render",
        alt=("A travertine espresso bar with walnut joinery and brass detailing, fitted out and finished",
             "بار إسبريسو من الترافرتين بأعمال نجارة من الجوز وتفاصيل نحاسية، بعد التشطيب")),
}
T = {
    "en": dict(sheet="Sheet", services="Services", cta="Book Free Consultation", set_a="Drawing set", set_b="FurnishIQ Services", index="Service pages"),
    "ar": dict(sheet="اللوحة", services="الخدمات", cta="احجز استشارة مجانية", set_a="مجموعة اللوحات", set_b="خدمات FurnishIQ", index="صفحات الخدمات"),
}
ARROW = {
    "en": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
    "ar": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>',
}
DOWN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="5 12 12 19 19 12"/></svg>'


def srcset(base, ws):
    return ", ".join(f"uploads/{base}-{w}.webp {w}w" for w in ws)


def build(page, lang):
    ar = lang == "ar"
    t, p = T[lang], PAGE[page]
    L = 1 if ar else 0
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    caps = "normal" if ar else "0.22em"
    base = "/ar" if ar else ""
    PAD = "clamp(24px,5vw,80px)"
    me = next(i for i, s in enumerate(SET) if s[0] == page)
    code = SET[me][1]
    name = SET[me][3 if ar else 2].replace("&", "&amp;")
    cells = []
    for i, (pg, cd, en, arn, thumb) in enumerate(SET):
        label = (arn if ar else en).replace("&", "&amp;")
        inner = f'<span class="hs-code" dir="ltr">{cd}</span><span class="hs-cname">{label}</span><img class="hs-thumb" src="uploads/{thumb}.webp" alt="" loading="lazy" decoding="async">'
        if i == me:
            cells.append(f'      <span class="hs-cell is-current" aria-current="page">{inner}</span>')
        else:
            cells.append(f'      <a class="hs-cell" href="{base}/{pg}">{inner}</a>')
    cells = "\n".join(cells)
    flip = "scaleX(-1)" if ar else "none"
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ HERO ━━ -->
<section data-screen-label="Hero" data-sp-hero{' dir="rtl"' if ar else ''} style="position:relative;background:#1F1F1F;color:#F5F2ED;overflow:hidden;">
  <style>
    /* the hero's links land below the fixed 80px header */
    #contact{{scroll-margin-top:80px;}}
    [data-sp-hero]{{min-height:max(720px,100vh);min-height:max(720px,100svh);display:flex;flex-direction:column;}}
    [data-sp-hero] .hs-grid{{position:absolute;inset:0;width:100%;height:100%;color:rgba(245,242,237,0.05);opacity:0;transition:opacity 1.6s {EASE};}}
    [data-sp-hero].is-ready .hs-grid{{opacity:1;}}
    [data-sp-hero] .hs-sheet{{position:relative;flex:1;display:grid;grid-template-rows:minmax(0,1fr) auto;gap:clamp(28px,4vh,44px);width:100%;max-width:1440px;margin:0 auto;padding:clamp(108px,15vh,136px) {PAD} clamp(20px,3vh,32px);box-sizing:border-box;}}
    [data-sp-hero] .hs-main{{position:relative;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);align-items:stretch;min-height:0;}}
    /* the photograph, plotted on the sheet */
    [data-sp-hero] .hs-plot{{position:relative;grid-column:2;margin:22px 0 0;min-height:0;}}
    [data-sp-hero] .hs-photo{{position:absolute;inset:0;overflow:hidden;background:#120D09;clip-path:inset(0 {'0 0 100%' if ar else '100% 0 0'});transition:clip-path 1.5s cubic-bezier(0.77,0,0.18,1) 0.25s;}}
    [data-sp-hero].is-ready .hs-photo{{clip-path:inset(0 0 0 0);}}
    [data-sp-hero] .hs-photo img{{width:100%;height:100%;object-fit:cover;transform:scale(1.08);transition:transform 2.4s {EASE} 0.25s;}}
    [data-sp-hero].is-ready .hs-photo img{{transform:scale(1.02);animation:hsDrift 26s cubic-bezier(0.45,0,0.55,1) 2.7s infinite alternate;}}
    @keyframes hsDrift{{from{{transform:scale(1.02) translate3d(0,0,0);}}to{{transform:scale(1.09) translate3d({'1.2%' if ar else '-1.2%'},-0.8%,0);}}}}
    [data-sp-hero] .hs-mark{{position:absolute;width:18px;height:18px;border:0 solid #D6C2A8;opacity:0;transition:opacity 0.6s {EASE} 1.5s;}}
    [data-sp-hero].is-ready .hs-mark{{opacity:1;}}
    [data-sp-hero] .hs-mark--tl{{top:-10px;left:-10px;border-width:1px 0 0 1px;}}
    [data-sp-hero] .hs-mark--tr{{top:-10px;right:-10px;border-width:1px 1px 0 0;}}
    [data-sp-hero] .hs-mark--bl{{bottom:-10px;left:-10px;border-width:0 0 1px 1px;}}
    [data-sp-hero] .hs-mark--br{{bottom:-10px;right:-10px;border-width:0 1px 1px 0;}}
    [data-sp-hero] .hs-dim{{position:absolute;top:-24px;left:0;right:0;height:9px;}}
    [data-sp-hero] .hs-dim i{{position:absolute;top:4px;left:0;right:0;height:1px;background:rgba(214,194,168,0.55);transform:scaleX(0);transform-origin:{'100%' if ar else '0%'} 50%;transition:transform 1.2s {EASE} 0.9s;}}
    [data-sp-hero].is-ready .hs-dim i{{transform:none;}}
    [data-sp-hero] .hs-dim::before,[data-sp-hero] .hs-dim::after{{content:"";position:absolute;top:0;width:1px;height:9px;background:rgba(214,194,168,0.55);}}
    [data-sp-hero] .hs-dim::before{{left:0;}}
    [data-sp-hero] .hs-dim::after{{right:0;}}
    [data-sp-hero] .hs-dim span{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);padding:0 14px;background:#1F1F1F;white-space:nowrap;font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;color:rgba(214,194,168,0.85);opacity:0;transition:opacity 0.6s {EASE} 1.6s;}}
    [data-sp-hero].is-ready .hs-dim span{{opacity:1;}}
    /* the type, on the sheet; the title runs onto the photograph */
    [data-sp-hero] .hs-text{{position:relative;z-index:2;grid-column:1;grid-row:1;align-self:end;display:flex;flex-direction:column;padding-bottom:clamp(8px,2vh,24px);}}
    [data-sp-hero] .hs-eyebrow{{display:flex;align-items:center;gap:14px;margin:0 0 26px;font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{'normal' if ar else '0.3em'};text-transform:uppercase;color:rgba(214,194,168,0.9);}}
    [data-sp-hero] .hs-eyebrow i{{display:block;width:32px;height:1px;background:#D6C2A8;}}
    [data-sp-hero] .hs-eyebrow [dir="ltr"]{{font-family:'Lama Sans',sans-serif;letter-spacing:0.2em;color:#D6C2A8;}}
    [data-sp-hero] .hs-eyebrow a{{color:inherit;text-decoration:none;}}
    [data-sp-hero] .hs-eyebrow a:hover{{color:#F5F2ED;}}
    [data-sp-hero] .hs-h1{{margin:0 0 0;margin-inline-end:-46%;font-family:{font};font-weight:500;font-size:{'clamp(46px,6.2vw,104px)' if ar else 'clamp(54px,7.8vw,132px)'};line-height:{'1.12' if ar else '0.96'};letter-spacing:{'0' if ar else '-0.03em'};color:#F5F2ED;text-shadow:0 2px 50px rgba(18,13,9,0.55);text-wrap:balance;}}
    [data-sp-hero] .hs-line{{display:block;overflow:hidden;padding:{'0.1em 0 0.48em' if ar else '0 0 0.12em'};margin-bottom:{'-0.48em' if ar else '-0.12em'};}}
    [data-sp-hero] .hs-line>span{{display:block;transform:translateY(110%);transition:transform 1.2s {EASE} 0.7s;}}
    [data-sp-hero].is-ready .hs-line>span{{transform:none;}}
    [data-sp-hero] .hs-slogan{{margin:clamp(22px,2.6vh,32px) 0 0;max-width:{'480px' if ar else '26ch'};font-family:{font};font-weight:500;font-size:{'clamp(20px,1.8vw,26px)' if ar else 'clamp(18px,1.7vw,24px)'};line-height:1.45;letter-spacing:{'0' if ar else '-0.005em'};color:rgba(245,242,237,0.86);text-wrap:balance;}}
    [data-sp-hero] .hs-ctas{{display:flex;align-items:center;flex-wrap:wrap;gap:16px 30px;margin-top:clamp(26px,3.4vh,40px);}}
    [data-sp-hero] .hs-cta{{display:inline-flex;align-items:center;gap:14px;padding:18px 32px;background:#D6C2A8;color:#1F1F1F;border:1px solid #D6C2A8;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-sp-hero] .hs-cta:hover,[data-sp-hero] .hs-cta:focus-visible{{background:transparent;color:#D6C2A8;}}
    [data-sp-hero] .hs-more{{display:inline-flex;align-items:center;gap:12px;padding-bottom:6px;border-bottom:1px solid rgba(214,194,168,0.45);color:#F5F2ED;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;transition:border-color 0.4s {EASE},color 0.4s {EASE};}}
    [data-sp-hero] .hs-more:hover,[data-sp-hero] .hs-more:focus-visible{{color:#D6C2A8;border-color:#D6C2A8;}}
    [data-sp-hero] .hs-more svg{{transition:transform 0.4s {EASE};}}
    [data-sp-hero] .hs-more:hover svg{{transform:translateY(3px);}}
    [data-sp-hero] .hs-fade{{opacity:0;transform:translateY(14px);transition:opacity 0.9s {EASE} 1.05s,transform 0.9s {EASE} 1.05s;}}
    [data-sp-hero].is-ready .hs-fade{{opacity:1;transform:none;}}
    /* the title block: the index of the set */
    [data-sp-hero] .hs-block{{display:grid;grid-template-columns:minmax(0,1.1fr) repeat(4,minmax(0,1fr));border:1px solid rgba(214,194,168,0.28);opacity:0;transform:translateY(14px);transition:opacity 0.9s {EASE} 1.3s,transform 0.9s {EASE} 1.3s;}}
    [data-sp-hero].is-ready .hs-block{{opacity:1;transform:none;}}
    [data-sp-hero] .hs-cell{{position:relative;display:flex;flex-direction:column;justify-content:center;gap:6px;min-height:76px;padding:14px clamp(14px,1.4vw,22px);padding-inline-end:76px;border-inline-start:1px solid rgba(214,194,168,0.28);color:#F5F2ED;text-decoration:none;overflow:hidden;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-sp-hero] .hs-set{{display:flex;flex-direction:column;justify-content:center;gap:6px;padding:14px clamp(14px,1.4vw,22px);font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;color:rgba(214,194,168,0.75);}}
    [data-sp-hero] .hs-set b{{font-weight:500;color:#F5F2ED;}}
    [data-sp-hero] .hs-code{{font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.2em;color:#D6C2A8;}}
    [data-sp-hero] .hs-cname{{font-family:{font};font-size:{'15px' if ar else '14px'};line-height:1.3;}}
    [data-sp-hero] .hs-thumb{{position:absolute;top:50%;inset-inline-end:14px;width:46px;height:46px;object-fit:cover;transform:translateY(-50%);opacity:0.4;filter:saturate(0.6);transition:opacity 0.4s {EASE},filter 0.4s {EASE};}}
    [data-sp-hero] a.hs-cell:hover,[data-sp-hero] a.hs-cell:focus-visible{{background:rgba(245,242,237,0.06);}}
    [data-sp-hero] a.hs-cell:hover .hs-thumb,[data-sp-hero] a.hs-cell:focus-visible .hs-thumb{{opacity:1;filter:none;}}
    [data-sp-hero] a.hs-cell:focus-visible{{outline:1px solid #D6C2A8;outline-offset:-5px;}}
    [data-sp-hero] .hs-cell.is-current{{background:#D6C2A8;color:#1F1F1F;}}
    [data-sp-hero] .hs-cell.is-current .hs-code{{color:#5B4636;}}
    [data-sp-hero] .hs-cell.is-current .hs-thumb{{opacity:1;filter:none;}}
    @media(max-width:900px){{
      [data-sp-hero]{{min-height:0;}}
      [data-sp-hero] .hs-sheet{{padding-top:112px;gap:32px;}}
      [data-sp-hero] .hs-main{{grid-template-columns:1fr;gap:44px;}}
      [data-sp-hero] .hs-text{{grid-column:1;grid-row:1;padding:0;}}
      [data-sp-hero] .hs-h1{{margin-inline-end:0;}}
      [data-sp-hero] .hs-plot{{grid-column:1;grid-row:2;aspect-ratio:4/3;margin-top:24px;}}
      [data-sp-hero] .hs-cta{{width:100%;justify-content:center;box-sizing:border-box;}}
      [data-sp-hero] .hs-block{{grid-template-columns:1fr 1fr;}}
      [data-sp-hero] .hs-set{{display:none;}}
      [data-sp-hero] .hs-cell{{border-top:1px solid rgba(214,194,168,0.28);}}
      [data-sp-hero] .hs-cell:nth-of-type(odd){{border-inline-start:0;}}
      [data-sp-hero] .hs-cell:nth-of-type(-n+2){{border-top:0;}}
      [data-sp-hero] .hs-thumb{{display:none;}}
      [data-sp-hero] .hs-dim span{{font-size:{'11px' if ar else '8.5px'};letter-spacing:{'normal' if ar else '0.14em'};padding:0 10px;max-width:calc(100% - 40px);overflow:hidden;text-overflow:ellipsis;}}
      [data-sp-hero] .hs-cell{{padding-inline-end:clamp(14px,1.4vw,22px);}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-sp-hero] *{{transition:none!important;animation:none!important;}}
      [data-sp-hero] .hs-photo{{clip-path:none;}}
      [data-sp-hero] .hs-line>span,[data-sp-hero] .hs-fade,[data-sp-hero] .hs-block{{transform:none;opacity:1;}}
      [data-sp-hero] .hs-grid,[data-sp-hero] .hs-mark,[data-sp-hero] .hs-dim span{{opacity:1;}}
      [data-sp-hero] .hs-dim i{{transform:none;}}
    }}
  </style>
  <svg class="hs-grid" aria-hidden="true"><defs><pattern id="hs-grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40,0V40M0,40H40" fill="none" stroke="currentColor" stroke-width="1"/></pattern></defs><rect width="100%" height="100%" fill="url(#hs-grid)"/></svg>
  <div class="hs-sheet">
    <div class="hs-main">
      <div class="hs-text">
        <p class="hs-eyebrow hs-fade"><i></i><a href="{base}/services">{t['services']}</a><span>·</span>{t['sheet']} <span dir="ltr">{code}</span></p>
        <h1 class="hs-h1"><span class="hs-line"><span>{name}</span></span></h1>
        <p class="hs-slogan hs-fade">{p['slogan'][L]}</p>
        <div class="hs-ctas hs-fade">
          <a class="hs-cta" href="#contact">{t['cta']}{ARROW[lang]}</a>
          <a class="hs-more" href="{p['anchor']}">{p['more'][L]}{DOWN}</a>
        </div>
      </div>
      <figure class="hs-plot">
        <div class="hs-dim" aria-hidden="true"><i></i><span>{p['project'][L]}</span></div>
        <div class="hs-photo"><img src="uploads/{p['img']}-{p['widths'][1]}.webp" srcset="{srcset(p['img'], p['widths'])}" sizes="(max-width:900px) 100vw, 58vw" alt="{p['alt'][L]}" style="object-position:{p['pos']};" fetchpriority="high" decoding="async"></div>
        <i class="hs-mark hs-mark--tl" aria-hidden="true"></i><i class="hs-mark hs-mark--tr" aria-hidden="true"></i><i class="hs-mark hs-mark--bl" aria-hidden="true"></i><i class="hs-mark hs-mark--br" aria-hidden="true"></i>
      </figure>
    </div>
    <nav class="hs-block" aria-label="{t['index']}">
      <span class="hs-set"><span>{t['set_a']}</span><b>{t['set_b']}</b></span>
{cells}
    </nav>
  </div>
</section>
"""


JS = """    // ── SERVICE PAGES, HERO: ONE SHEET OF THE DRAWING SET ───────────────────
    {
      const hero = document.querySelector('[data-sp-hero]');
      if (hero) {
        requestAnimationFrame(() => requestAnimationFrame(() => hero.classList.add('is-ready')));
        // the in-page links land the section's top just under the fixed 80px header
        hero.querySelectorAll('a[href^="#"]').forEach((a) => a.addEventListener('click', (e) => {
          const el = document.getElementById(a.getAttribute('href').slice(1));
          if (!el) return;
          e.preventDefault();
          window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 80, behavior: reduced ? 'instant' : 'smooth' });
          history.replaceState(null, '', a.getAttribute('href'));
        }));
      }
    }

"""
MARK = "    // ── SCROLL REVEAL"

pages = sys.argv[1:] or list(PAGE)
for page in pages:
    for name, lang in [(f"{page}.dc.html", "en"), (f"{page}.ar.dc.html", "ar")]:
        s = open(name, encoding="utf-8").read()
        s, n = re.subn(r"<!-- ━+ HERO ━+ -->\n<section [^>]*data-screen-label=\"Hero\".*?\n</section>\n", lambda m: build(page, lang), s, count=1, flags=re.S)
        assert n == 1, name
        old = "    // ── SERVICE PAGES, HERO:"
        if old in s:
            a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
            s = s[:a] + s[b:]
        assert s.count(MARK) == 1, name
        s = s.replace(MARK, JS + MARK)
        open(name, "w", encoding="utf-8", newline="").write(s)
        print(name, "ok")

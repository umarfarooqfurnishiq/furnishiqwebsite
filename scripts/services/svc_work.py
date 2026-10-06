"""Services, Selected Work: the work, in motion, and the page's closing call.

The close of the services page. Three concept projects from three sectors, none of them pictured elsewhere on
the page: one fills the width and drifts slowly, then crossfades to the next, with its sector, location and
a link to the project over it and a band of three to switch between them. The drift is a CSS transform on the
high-resolution still, not a video: transforms move in sub-pixel steps, where the zoom baked into the
project films snaps to whole pixels and judders. Reduced motion keeps the stills still. Below, the page's
finale: a blank stone sheet on a faint drafting grid, where a dimension line marked stage 01, the brief, draws
itself in under the line that every space shown began as a blank sheet. It offers the consultation and the
studio's real channels: call, WhatsApp and email.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/services/svc_work.py
"""
import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
FILMS = [("penthouse-wadi-double-height-living-riyadh", "penthouse-above-the-wadi", "50% 60%"),
         ("roastery-house-roasting-hall-riyadh", "roastery-house-flagship", "50% 55%"),
         ("central-commons-plaza-dusk-riyadh", "central-commons", "50% 60%")]
C = {
    "en": dict(
        eyebrow="Selected Work", h2="The work, in motion.",
        sub="Three concept projects across three sectors, from first sketch to finished space.",
        all="View All Projects", all_href="/projects", base="",
        names=["Penthouse Above the Wadi", "Roastery House Flagship", "Central Commons"],
        metas=["Concept · Residential · West Riyadh", "Concept · Hospitality · North Riyadh", "Concept · Retail · Olaya, Riyadh"],
        sectors=["Residential", "Hospitality", "Retail"],
        view="View Project", films="Selected projects", alts=["Double-height living room with a backlit onyx wall and full-height glazing onto Wadi Hanifa", "Roasting hall with a central roaster behind glass and a long brass-edged bar", "Retail plaza at dusk beneath a patterned bronze canopy, with reflecting pools and palms"],
        end_eyebrow="The next project", end_h="Every space on this page began as a blank sheet.", end_em="The next one is yours.",
        end_dim="Stage 01 · The brief", end_cta="Book Free Consultation", end_href="/contact",
        ch=[("Call", "+966 58 033 0627", "tel:+966580330627", True), ("WhatsApp", "Message the studio", "https://wa.me/966580330627", False), ("Email", "info@furnishiq.net", "mailto:info@furnishiq.net", True)],
    ),
    "ar": dict(
        eyebrow="أعمال مختارة", h2="أعمالنا، في حركة.",
        sub="ثلاثة تصورات تصميمية في ثلاثة قطاعات، من الرسم الأول حتى المساحة المنجزة.",
        all="عرض جميع المشاريع", all_href="/ar/projects", base="/ar",
        names=["بنتهاوس فوق الوادي", "بيت المحمصة — الفرع الرئيسي", "الساحة المركزية"],
        metas=["تصور تصميمي · سكني · غرب الرياض", "تصور تصميمي · ضيافة · شمال الرياض", "تصور تصميمي · تجزئة · العليا، الرياض"],
        sectors=["سكني", "ضيافة", "تجزئة"],
        view="عرض المشروع", films="مشاريع مختارة", alts=["غرفة معيشة بارتفاع مزدوج بجدار عقيق مضاء وواجهات زجاجية كاملة تطل على وادي حنيفة", "قاعة تحميص بمحمصة مركزية خلف الزجاج وبار طويل بحواف نحاسية", "ساحة تجارية عند الغسق تحت مظلة برونزية مزخرفة مع أحواض عاكسة ونخيل"],
        end_eyebrow="المشروع التالي", end_h="كل مساحة في هذه الصفحة بدأت بورقة بيضاء.", end_em="والمساحة التالية لك.",
        end_dim="المرحلة 01 · الإحاطة", end_cta="احجز استشارة مجانية", end_href="/ar/contact",
        ch=[("اتصل بنا", "+966 58 033 0627", "tel:+966580330627", True), ("واتساب", "راسل الاستوديو", "https://wa.me/966580330627", False), ("البريد الإلكتروني", "info@furnishiq.net", "mailto:info@furnishiq.net", True)],
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
    PAD = "clamp(24px,5vw,80px)"
    n = len(FILMS)
    chans = "".join(f'<li><span class="wk-ch-l">{l}</span><a class="wk-ch-v" href="{h}"{chr(32) + 'dir="ltr"' if ltr else ''}{'' if h.startswith(('tel', 'mailto')) else ' target="_blank" rel="noopener"'}>{v}</a></li>' for l, v, h, ltr in c['ch'])
    films = "\n".join(f'''        <img class="wk-film{' is-on' if i == 0 else ''}" data-wk="{i}" src="uploads/{f}-1920.webp" srcset="uploads/{f}-1280.webp 1280w, uploads/{f}-1920.webp 1920w, uploads/{f}-2752.webp 2752w" sizes="100vw" alt="{c['alts'][i]}" style="object-position:{pos};" loading="lazy" decoding="async">''' for i, (f, _, pos) in enumerate(FILMS))
    captions = "\n".join(f'''          <div class="wk-cap{' is-on' if i == 0 else ''}" data-cap="{i}" id="wk-pane-{i}" role="tabpanel" aria-labelledby="wk-tab-{i}">
            <p class="wk-meta">{c['metas'][i]}</p>
            <h3 class="wk-name">{c['names'][i]}</h3>
            <a class="wk-view" href="{c['base']}/project-detail?project={slug}"{'' if i == 0 else ' tabindex="-1"'}>{c['view']}{arrow}</a>
          </div>''' for i, (_, slug, _) in enumerate(FILMS))
    tabs = "\n".join(f'''        <button type="button" class="wk-tab" role="tab" id="wk-tab-{i}" data-wk-tab="{i}" aria-selected="{'true' if i == 0 else 'false'}" aria-controls="wk-pane-{i}" tabindex="{0 if i == 0 else -1}"><i class="wk-prog" aria-hidden="true"></i><span class="wk-n" dir="ltr">0{i + 1}</span><span class="wk-t">{c['names'][i]}</span><span class="wk-s">{c['sectors'][i]}</span></button>''' for i in range(n))
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ PORTFOLIO ━━━━━━━━ -->
<section id="portfolio" data-svc-work{' dir="rtl"' if ar else ''} style="background:#3A2D25;color:#F5F2ED;position:relative;padding:clamp(64px,8vw,100px) {PAD} 0;overflow:clip;">
  <style>
    [data-svc-work] .wk-wrap{{max-width:1280px;margin:0 auto;}}
    [data-svc-work] .wk-head{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:clamp(32px,5vw,88px);align-items:end;margin-bottom:clamp(40px,4.4vw,64px);}}
    [data-svc-work] .wk-eyebrow{{display:flex;align-items:center;gap:16px;margin-bottom:24px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#D6C2A8;}}
    [data-svc-work] .wk-eyebrow i{{display:block;width:32px;height:1px;background:#D6C2A8;}}
    [data-svc-work] .wk-h2{{font-family:{font};font-weight:500;font-size:clamp(32px,3.8vw,54px);line-height:1.08;letter-spacing:{'0' if ar else '-0.015em'};color:#F5F2ED;margin:0;text-wrap:balance;}}
    [data-svc-work] .wk-sub{{font-family:{font};font-weight:500;font-size:{'clamp(22px,2vw,28px)' if ar else 'clamp(20px,1.9vw,26px)'};line-height:1.4;letter-spacing:{'0' if ar else '-0.005em'};text-wrap:balance;max-width:30ch;color:#F5F2ED;margin:0 0 24px;}}
    [data-svc-work] .wk-all{{display:inline-flex;align-items:center;gap:12px;padding-bottom:6px;border-bottom:1px solid rgba(214,194,168,0.45);color:#D6C2A8;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;transition:color 0.4s {EASE},border-color 0.4s {EASE};}}
    [data-svc-work] .wk-all:hover,[data-svc-work] .wk-all:focus-visible{{color:#F5F2ED;border-color:#F5F2ED;}}
    [data-svc-work] .wk-rise{{opacity:0;transform:translateY(24px);transition:opacity 0.9s {EASE},transform 0.9s {EASE};}}
    [data-svc-work].is-in .wk-rise{{opacity:1;transform:none;}}
    [data-svc-work].is-in .wk-rise--2{{transition-delay:0.12s;}}
    [data-svc-work].is-in .wk-rise--3{{transition-delay:0.24s;}}
    [data-svc-work] .wk-block{{margin-inline:calc(50% - 50vw + var(--wk-sb,0px) / 2);background:#1F1F1F;}}
    [data-svc-work] .wk-stage{{position:relative;height:min(calc(100svh - var(--fiq-svc-offset,132px) - var(--wk-band,96px)),56.25vw);min-height:440px;overflow:hidden;background:#1F1F1F;}}
    [data-svc-work] .wk-film{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.09) translate3d(-1.2%,0,0);transition:opacity 1.4s {EASE},transform 0s linear 1.4s;will-change:transform,opacity;backface-visibility:hidden;}}
    [data-svc-work] .wk-film.is-on{{opacity:1;transform:scale(1.02) translate3d(0,0,0);transition:opacity 1.4s {EASE},transform 10.5s cubic-bezier(0.33,0,0.25,1);}}
    [data-svc-work] .wk-in{{position:absolute;inset:0;width:min(1280px,calc(100% - 2 * {PAD}));margin:0 auto;pointer-events:none;}}
    [data-svc-work] .wk-caps{{position:absolute;bottom:clamp(20px,3vw,44px);inset-inline-start:0;display:grid;width:min(460px,60%);}}
    [data-svc-work] .wk-cap{{grid-area:1/1;align-self:end;padding:clamp(22px,2.2vw,30px);background:rgba(31,31,31,0.72);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);pointer-events:auto;opacity:0;visibility:hidden;transform:translateY(12px);transition:opacity 0.6s {EASE},transform 0.6s {EASE},visibility 0s linear 0.6s;}}
    [data-svc-work] .wk-cap.is-on{{opacity:1;visibility:visible;transform:none;transition-delay:0.3s,0.3s,0s;}}
    [data-svc-work] .wk-meta{{margin:0 0 10px;font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;color:#C4A882;}}
    [data-svc-work] .wk-name{{margin:0 0 18px;font-family:{font};font-weight:500;font-size:clamp(26px,2.6vw,38px);line-height:1.1;color:#F5F2ED;}}
    [data-svc-work] .wk-view{{display:inline-flex;align-items:center;gap:12px;padding:14px 22px;background:#F5F2ED;color:#1F1F1F;border:1px solid #F5F2ED;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-work] .wk-view:hover,[data-svc-work] .wk-view:focus-visible{{background:transparent;color:#F5F2ED;}}
    [data-svc-work] .wk-tabs{{display:grid;grid-template-columns:repeat({n},minmax(0,1fr));width:min(1280px,calc(100% - 2 * {PAD}));margin:0 auto;}}
    [data-svc-work] .wk-tab{{position:relative;display:grid;grid-template-columns:auto minmax(0,1fr);column-gap:14px;row-gap:4px;align-items:baseline;padding:24px clamp(14px,1.6vw,22px) 26px;border:0;border-inline-start:1px solid rgba(245,242,237,0.1);background:transparent;color:rgba(245,242,237,0.5);text-align:start;cursor:pointer;transition:color 0.4s {EASE},background 0.4s {EASE};}}
    [data-svc-work] .wk-tab:first-child{{border-inline-start:0;}}
    [data-svc-work] .wk-tab:hover{{color:#F5F2ED;background:rgba(245,242,237,0.03);}}
    [data-svc-work] .wk-tab:focus-visible{{outline:1px solid #D6C2A8;outline-offset:-4px;}}
    [data-svc-work] .wk-tab[aria-selected="true"]{{color:#F5F2ED;}}
    [data-svc-work] .wk-prog{{position:absolute;top:0;left:0;right:0;height:2px;background:rgba(245,242,237,0.1);}}
    [data-svc-work] .wk-prog::after{{content:"";position:absolute;inset:0;background:#D6C2A8;transform:scaleX(var(--p,0));transform-origin:{'100%' if ar else '0%'} 50%;}}
    [data-svc-work] .wk-n{{grid-row:span 2;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.2em;color:#D6C2A8;}}
    [data-svc-work] .wk-t{{font-family:{font};font-size:{'14px' if ar else '13px'};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
    [data-svc-work] .wk-s{{font-family:{font};font-size:{'11px' if ar else '9px'};letter-spacing:{caps};text-transform:uppercase;color:rgba(245,242,237,0.45);}}
    /* finale: a blank sheet on a drafting grid; the first line of the next project draws itself in */
    [data-svc-work] .wk-end{{position:relative;margin-inline:calc(50% - 50vw + var(--wk-sb,0px) / 2);padding:clamp(88px,11vw,160px) {PAD} clamp(80px,9vw,128px);background:#F5F2ED;color:#1F1F1F;overflow:hidden;}}
    [data-svc-work] .wk-grid{{position:absolute;inset:0;width:100%;height:100%;color:rgba(58,45,37,0.07);}}
    [data-svc-work] .wk-end-in{{position:relative;max-width:1280px;margin:0 auto;}}
    [data-svc-work] .wk-end-eyebrow{{display:flex;align-items:center;gap:16px;margin:0 0 28px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    [data-svc-work] .wk-end-eyebrow i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    [data-svc-work] .wk-end-h{{margin:0;max-width:19ch;font-family:{font};font-weight:500;font-size:clamp(36px,5.2vw,78px);line-height:1.06;letter-spacing:{'0' if ar else '-0.02em'};color:#1F1F1F;text-wrap:balance;}}
    [data-svc-work] .wk-end-h em{{display:block;font-style:normal;color:#8B6B4A;}}
    [data-svc-work] .wk-dim{{position:relative;margin:clamp(48px,5.6vw,80px) 0 clamp(36px,4vw,56px);height:24px;color:#5B4636;}}
    [data-svc-work] .wk-dim::before,[data-svc-work] .wk-dim::after{{content:"";position:absolute;top:2px;bottom:2px;width:1.2px;background:currentColor;opacity:0;transition:opacity 0.4s {EASE};}}
    [data-svc-work] .wk-dim::before{{inset-inline-start:0;}}
    [data-svc-work] .wk-dim::after{{inset-inline-end:0;transition-delay:1.3s;}}
    [data-svc-work] .wk-dim i{{position:absolute;top:50%;left:0;right:0;height:1.2px;margin-top:-0.6px;background:currentColor;transform:scaleX(0);transform-origin:{'100%' if ar else '0%'} 50%;transition:transform 1.6s {EASE};}}
    [data-svc-work] .wk-dim span{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);padding:0 18px;background:#F5F2ED;white-space:nowrap;font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;color:#8B6B4A;opacity:0;transition:opacity 0.6s {EASE} 0.9s;}}
    [data-svc-work] .wk-end.is-drawn .wk-dim i{{transform:none;}}
    [data-svc-work] .wk-end.is-drawn .wk-dim::before,[data-svc-work] .wk-end.is-drawn .wk-dim::after{{opacity:1;}}
    [data-svc-work] .wk-end.is-drawn .wk-dim span{{opacity:1;}}
    [data-svc-work] .wk-end-row{{display:flex;align-items:center;justify-content:space-between;gap:clamp(32px,5vw,80px);flex-wrap:wrap;}}
    [data-svc-work] .wk-cta{{flex:none;display:inline-flex;align-items:center;gap:14px;padding:22px 40px;background:#3A2D25;color:#F5F2ED;border:1px solid #3A2D25;text-decoration:none;font-family:{font};font-size:{'14px' if ar else '11px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-work] .wk-cta:hover,[data-svc-work] .wk-cta:focus-visible{{background:transparent;color:#3A2D25;}}
    [data-svc-work] .wk-cta svg{{transition:transform 0.4s {EASE};}}
    [data-svc-work] .wk-cta:hover svg{{transform:translateX({'-4px' if ar else '4px'});}}
    [data-svc-work] .wk-ch{{list-style:none;margin:0;padding:0;display:flex;gap:clamp(28px,4vw,64px);}}
    [data-svc-work] .wk-ch li{{display:flex;flex-direction:column;gap:8px;padding-inline-start:clamp(16px,1.6vw,24px);border-inline-start:1px solid rgba(58,45,37,0.2);}}
    [data-svc-work] .wk-ch-l{{font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;color:#8B6B4A;}}
    [data-svc-work] .wk-ch-v{{align-self:flex-start;font-family:{font};font-size:{'17px' if ar else '16px'};color:#1F1F1F;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:6px;text-decoration-color:transparent;transition:text-decoration-color 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-work] .wk-ch-v[dir="ltr"]{{font-family:'Lama Sans',sans-serif;}}
    [data-svc-work] .wk-ch-v:hover,[data-svc-work] .wk-ch-v:focus-visible{{text-decoration-color:currentColor;color:#5B4636;}}
    [data-svc-work] .wk-end .wk-up{{opacity:0;transform:translateY(24px);transition:opacity 0.9s {EASE},transform 0.9s {EASE};}}
    [data-svc-work] .wk-end.is-drawn .wk-up{{opacity:1;transform:none;}}
    [data-svc-work] .wk-end.is-drawn .wk-up--2{{transition-delay:0.12s;}}
    [data-svc-work] .wk-end.is-drawn .wk-up--3{{transition-delay:1.1s;}}
    @media(max-width:900px){{
      [data-svc-work] .wk-head{{grid-template-columns:1fr;}}
      [data-svc-work] .wk-stage{{height:auto;min-height:0;aspect-ratio:4/3;}}
      [data-svc-work] .wk-in{{width:auto;inset:0;}}
      [data-svc-work] .wk-caps{{inset-inline:12px;bottom:12px;width:auto;}}
      [data-svc-work] .wk-cap{{padding:16px 18px;}}
      [data-svc-work] .wk-name{{font-size:22px;margin-bottom:12px;}}
      [data-svc-work] .wk-view{{padding:11px 16px;}}
      [data-svc-work] .wk-tabs{{width:100%;}}
      [data-svc-work] .wk-t{{display:none;}}
      [data-svc-work] .wk-end-row{{flex-direction:column;align-items:stretch;}}
      [data-svc-work] .wk-ch{{flex-direction:column;gap:22px;}}
    }}
    @media(max-width:600px){{
      [data-svc-work] .wk-tab{{padding:18px 12px 20px;}}
      [data-svc-work] .wk-end-h{{font-size:{'32px' if ar else '34px'};max-width:none;}}
      [data-svc-work] .wk-cta{{width:100%;justify-content:center;box-sizing:border-box;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-svc-work] *{{transition:none!important;}}
      [data-svc-work] .wk-rise,[data-svc-work] .wk-end .wk-up{{opacity:1;transform:none;}}
      [data-svc-work] .wk-dim i{{transform:none;}}
      [data-svc-work] .wk-dim::before,[data-svc-work] .wk-dim::after{{opacity:1;}}
      [data-svc-work] .wk-dim span{{opacity:1;}}
    }}
  </style>
  <div class="wk-wrap">
    <div class="wk-head">
      <div class="wk-rise">
        <div class="wk-eyebrow"><i></i>{c['eyebrow']}</div>
        <h2 class="wk-h2">{c['h2']}</h2>
      </div>
      <div class="wk-rise wk-rise--2">
        <p class="wk-sub">{c['sub']}</p>
        <a class="wk-all" href="{c['all_href']}">{c['all']}{arrow}</a>
      </div>
    </div>
    <div class="wk-block wk-rise wk-rise--3">
      <div class="wk-stage" data-wk-stage>
{films}
        <div class="wk-in">
          <div class="wk-caps" aria-live="polite">
{captions}
          </div>
        </div>
      </div>
      <div class="wk-band"><div class="wk-tabs" role="tablist" aria-label="{c['films']}">
{tabs}
      </div></div>
    </div>
    <div class="wk-end" data-wk-end>
      <svg class="wk-grid" aria-hidden="true"><defs><pattern id="wk-grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40,0V40M0,40H40" fill="none" stroke="currentColor" stroke-width="1"/></pattern></defs><rect width="100%" height="100%" fill="url(#wk-grid)"/></svg>
      <div class="wk-end-in">
        <p class="wk-end-eyebrow wk-up"><i></i>{c['end_eyebrow']}</p>
        <h2 class="wk-end-h wk-up wk-up--2">{c['end_h']} <em>{c['end_em']}</em></h2>
        <div class="wk-dim" aria-hidden="true">
          <i></i>
          <span>{c['end_dim']}</span>
        </div>
        <div class="wk-end-row wk-up wk-up--3">
          <a class="wk-cta" href="{c['end_href']}">{c['end_cta']}{arrow}</a>
          <ul class="wk-ch">{chans}</ul>
        </div>
      </div>
    </div>
  </div>
</section>
"""


JS = """    // ── SERVICES, SELECTED WORK: THE WORK, IN MOTION ───────────────────────
    {
      const sec = document.querySelector('[data-svc-work]');
      if (sec) {
        const stage = sec.querySelector('[data-wk-stage]'), block = sec.querySelector('.wk-block');
        const films = Array.from(sec.querySelectorAll('.wk-film')), caps = Array.from(sec.querySelectorAll('.wk-cap'));
        const tabs = Array.from(sec.querySelectorAll('[data-wk-tab]')), rtl = sec.getAttribute('dir') === 'rtl';
        const HOLD = 9000;  // each film's turn
        let idx = 0, auto = true, visible = false, hover = false, acc = 0, then = 0, raf = 0;
        const show = (i) => {
          idx = i; acc = 0;
          films.forEach((v, k) => v.classList.toggle('is-on', k === i));
          caps.forEach((cp, k) => { cp.classList.toggle('is-on', k === i); cp.querySelector('a').tabIndex = k === i ? 0 : -1; });
          tabs.forEach((t, k) => { t.setAttribute('aria-selected', k === i ? 'true' : 'false'); t.tabIndex = k === i ? 0 : -1; t.style.setProperty('--p', k === i && !auto ? 1 : 0); });
        };
        const take = (i) => { auto = false; show(i); };
        tabs.forEach((t, k) => {
          t.addEventListener('click', () => take(k));
          t.addEventListener('keydown', (e) => {
            const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
            if (!d) return;
            e.preventDefault();
            const nx = (k + (rtl ? -d : d) + tabs.length) % tabs.length;
            take(nx); tabs[nx].focus();
          });
        });
        // 100vw counts the scrollbar; the band's real height sizes the stage so the two fill the screen
        const fit = () => {
          sec.style.setProperty('--wk-sb', (window.innerWidth - document.documentElement.clientWidth) + 'px');
          sec.style.setProperty('--wk-band', sec.querySelector('.wk-band').offsetHeight + 'px');
        };
        fit();
        window.addEventListener('resize', fit);
        if (document.fonts) document.fonts.ready.then(fit);
        block.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') hover = true; });
        block.addEventListener('pointerleave', () => { hover = false; });
        document.addEventListener('visibilitychange', () => { then = 0; });
        const loop = (now) => {
          // real time between frames, so a throttled frame rate does not slow the turn
          const dt = then ? now - then : 0; then = now;
          if (auto && !hover && !document.hidden && !reduced) {
            acc += dt;
            tabs[idx].style.setProperty('--p', Math.min(1, acc / HOLD).toFixed(4));
            if (acc >= HOLD) show((idx + 1) % films.length);
          }
          raf = visible ? requestAnimationFrame(loop) : 0;
        };
        new IntersectionObserver((es, o) => { es.forEach((e) => { if (e.isIntersecting) { sec.classList.add('is-in'); o.disconnect(); } }); }, { rootMargin: '0px 0px -15% 0px' }).observe(sec);
        new IntersectionObserver((es) => {
          es.forEach((e) => {
            visible = e.isIntersecting;
            if (visible && !raf) { then = 0; raf = requestAnimationFrame(loop); }
          });
        }, { threshold: 0.3 }).observe(stage);
        // the finale draws its first line once it is well in view
        const end = sec.querySelector('[data-wk-end]');
        new IntersectionObserver((es, o) => { es.forEach((e) => { if (e.isIntersecting) { end.classList.add('is-drawn'); o.disconnect(); } }); }, { threshold: 0.35 }).observe(end);
        show(0);
      }
    }

"""
MARK = "    // ── SCROLL REVEAL"

for path, lang in [("services.dc.html", "en"), ("services.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ PORTFOLIO ━+ -->\n<section id=\"portfolio\".*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── SERVICES, SELECTED WORK:"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

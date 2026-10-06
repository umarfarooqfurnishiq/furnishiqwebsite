"""Services, Furniture: from render to room.

One living room across the full width, shown first empty with dashed outlines where every piece is
planned. Category by category the pieces arrive: five frames of the same room from one camera, each adding
a category, crossfade in turn and the new pieces are tagged, until the room is complete, exactly as
rendered, with the call to book a consultation. The light counterpart to the MEP stage above: a stone
panel, a walnut band of categories, and an Empty / Furnished switch. The categories and their descriptions are the ones on the furniture detail
page. On larger screens the block pins and the scroll runs it; on phones it cycles on its own.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/services/svc_furniture.py
"""
import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
# the same room, one category added per frame; one camera, toned to match, so each step is a clean crossfade
FRAMES = ["0-empty-room", "1-seating", "2-tables-lighting", "3-soft-furnishings", "4-styled"]
W, H = 1280, 714  # the space the pieces are traced in

# every piece, traced on the photograph
POLYS = {
    "sofa": [(484, 383), (512, 372), (545, 352), (612, 350), (660, 366), (990, 369), (1098, 355), (1178, 361), (1213, 397), (1218, 600), (905, 603), (902, 528), (780, 525), (512, 524), (486, 470)],
    "chair_l": [(92, 398), (112, 383), (200, 380), (250, 387), (266, 410), (268, 450), (305, 456), (318, 488), (316, 530), (300, 548), (205, 553), (140, 552), (118, 540), (122, 505), (100, 470)],
    "chair_r": [(291, 390), (305, 374), (350, 370), (410, 372), (424, 390), (424, 425), (455, 430), (468, 462), (466, 496), (450, 508), (380, 510), (330, 509), (305, 496), (300, 440)],
    "table": [(446, 486), (470, 478), (560, 462), (812, 468), (806, 478), (752, 520), (750, 582), (682, 588), (520, 575), (520, 505), (448, 499)],
    "lamp": [(437, 246), (483, 246), (501, 290), (468, 290), (469, 470), (457, 470), (458, 290), (420, 290)],
    "rug": [(38, 568), (110, 548), (300, 500), (470, 497), (1210, 520), (1224, 714), (420, 714)],
    "sheer": [(0, 28), (102, 40), (108, 538), (0, 545)],
    "drape": [(318, 84), (450, 104), (452, 432), (322, 422)],
    "niche_l": [(704, 276), (746, 276), (746, 322), (704, 322)],
    "niche_r": [(880, 268), (946, 268), (946, 322), (880, 322)],
    "vases": [(548, 402), (610, 400), (668, 404), (670, 470), (612, 480), (550, 480)],
    "books": [(626, 448), (780, 452), (780, 500), (626, 500)],
}
# each category: its pieces, and its tags (anchor on the piece, in the traced space)
STEPS = [
    (("sofa", "chair_l", "chair_r"), [((850, 372), "sofa"), ((182, 384), "chairs")]),
    (("table", "lamp", "vases", "books"), [((690, 470), "table"), ((460, 250), "lamp")]),
    (("rug", "sheer", "drape"), [((820, 650), "rug"), ((70, 150), "sheer")]),
    (("niche_l", "niche_r"), [((728, 282), "niche")]),
]
C = {
    "en": dict(
        eyebrow="Our Furniture Solutions", h2="The Final Layer of Spatial Perfection",
        body="The final layer, curated and placed exactly as rendered.",
        cta="Explore Furniture", href="/services-furniture",
        names=["Lounge &amp; Reception Seating", "Bespoke &amp; Artisanal Pieces", "Soft Furnishings &amp; Textiles", "Styling &amp; Placement"],
        feel=["Seating that sets the tone", "Made for this room alone", "Softness, layered in", "Placed, styled, handed over"],
        descs=["Statement sofas, reception counters, and breakout seating that set the tone on arrival.",
               "Custom-made furniture, handcrafted details, and statement lighting for standout spaces.",
               "Curtains, rugs, cushions, and upholstery selected to complete every room.",
               "Professional installation, final arrangement, and dedicated aftercare through handover."],
        tags=dict(sofa="Modular sofa", chairs="Bouclé armchairs", table="Travertine coffee table", lamp="Statement floor lamp",
                  rug="Textured rug", sheer="Sheers and drapes", niche="Ceramics in the niche", objects="Table styling"),
        intro_k="From render to room", intro_t="Every piece begins in the render",
        intro_d="Furniture is planned against the materials, lighting, and scale of your approved photoreal 3D renders, then sourced and placed category by category.",
        close_k="The final layer", close_t="Exactly as rendered",
        close_d="Every piece fits its room with precision before it ever arrives, so the space you approve is the space you receive.",
        close_cta="Book a Furniture Consultation", close_href="/contact",
        steps="Furniture categories", alt="Living room with a modular linen sofa, two bouclé armchairs, a travertine coffee table, a floor lamp and an arched niche of ceramics",
        cap="Concept visualisation", view="View", render="Empty", room="Furnished",
    ),
    "ar": dict(
        eyebrow="حلول الأثاث لدينا", h2="الطبقة الأخيرة من الكمال المكاني",
        body="الطبقة الأخيرة، منتقاة وموضوعة تماماً كما في التصور.",
        cta="استكشف الأثاث", href="/ar/services-furniture",
        names=["مقاعد الصالات والاستقبال", "قطع مخصصة وحرفية", "المفروشات والأقمشة", "التنسيق والتموضع"],
        feel=["مقاعد تمنح الانطباع الأول", "صُنعت لهذه الغرفة وحدها", "نعومة تكتمل بطبقات", "تموضع وتنسيق حتى التسليم"],
        descs=["أرائك مميزة، وطاولات استقبال، ومقاعد استراحة تمنح الانطباع الأول المناسب.",
               "أثاث مصنوع حسب الطلب، وتفاصيل حرفية، وإضاءة مميزة للمساحات الاستثنائية.",
               "ستائر، وسجاد، ووسائد، وأقمشة تنجيد مختارة لإكمال كل غرفة.",
               "تركيب احترافي، وترتيب نهائي، ورعاية مخصصة حتى التسليم."],
        tags=dict(sofa="أريكة معيارية", chairs="مقعدان من البوكليه", table="طاولة قهوة من الترافرتين", lamp="مصباح أرضي مميز",
                  rug="سجادة بملمس بارز", sheer="ستائر شفافة وثقيلة", niche="خزفيات في الكوة", objects="تنسيق الطاولة"),
        intro_k="من التصور إلى الغرفة", intro_t="كل قطعة تبدأ في التصور",
        intro_d="يُخطَّط الأثاث وفق الخامات والإضاءة والمقاييس المعتمدة في تصوراتك ثلاثية الأبعاد الواقعية، ثم يُورَّد ويُوضَع فئةً بعد فئة.",
        close_k="الطبقة الأخيرة", close_t="تماماً كما في التصور",
        close_d="تتناسب كل قطعة مع مساحتها بدقة قبل وصولها، فتستلم المساحة التي اعتمدتها كما هي.",
        close_cta="احجز استشارة للأثاث", close_href="/ar/contact",
        steps="فئات الأثاث", alt="غرفة معيشة بأريكة معيارية من الكتان ومقعدين من البوكليه وطاولة قهوة من الترافرتين ومصباح أرضي وكوة مقوسة تضم خزفيات",
        cap="تصور مفاهيمي", view="طريقة العرض", render="فارغة", room="مؤثثة",
    ),
}
ARROW_EN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
ARROW_AR = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>'


def pts(name):
    return " ".join(f"{x},{y}" for x, y in POLYS[name])


def stage_svg():
    # dashed outlines mark the pieces still to come: on the empty room they read as the plan in the render
    # each outline is drawn twice: a soft stone halo under a walnut dash, so it reads on light wall and dark floor alike
    def shape(p):
        return f'<polygon class="fu-halo" points="{pts(p)}"/><polygon class="fu-dash" points="{pts(p)}"/>'
    outlines = "".join(f'<g class="fu-line" data-k="{k}">' + "".join(shape(p) for p in pieces) + "</g>"
                       for k, (pieces, _) in enumerate(STEPS))
    return f'''          <svg class="fu-svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true" focusable="false">{outlines}</svg>'''


def frames(alt):
    return "\n".join(
        f'''            <img class="fu-shot{' on' if j == 0 else ''}" data-f="{j}" src="uploads/furniture-render-to-room-{f}-1280.webp" srcset="uploads/furniture-render-to-room-{f}-1280.webp 1280w, uploads/furniture-render-to-room-{f}-2400.webp 2400w" sizes="100vw" alt="{alt if j == len(FRAMES) - 1 else ''}"{'' if j == len(FRAMES) - 1 else ' aria-hidden="true"'} loading="lazy" decoding="async">'''
        for j, f in enumerate(FRAMES))


def tags(c):
    out = []
    for k, (_, tg) in enumerate(STEPS):
        for (x, y), key in tg:
            side = "is-left" if x > W * 0.52 else ""
            out.append(f'<span class="fu-tag {side}" data-k="{k}" style="left:{x / W * 100:.2f}%;top:{y / H * 100:.2f}%;"><i></i><b>{c["tags"][key]}</b></span>')
    return "\n            ".join(out)


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    caps = "normal" if ar else "0.22em"
    small = "12px" if ar else "9px"
    n = len(STEPS)
    arrow = ARROW_AR if ar else ARROW_EN
    PAD = "clamp(24px,5vw,80px)"
    panes = [f'''          <div class="fu-pane is-on" data-i="-1"><p class="fu-count"><span dir="ltr">00 / 0{n}</span></p><p class="fu-kick">{c['intro_k']}</p><h3 class="fu-title">{c['intro_t']}</h3><p class="fu-text">{c['intro_d']}</p></div>''']
    panes += [f'''          <div class="fu-pane" data-i="{k}" id="fu-pane-{k}" role="tabpanel" aria-labelledby="fu-tab-{k}"><p class="fu-count"><span dir="ltr">0{k + 1} / 0{n}</span></p><p class="fu-kick">{c['names'][k]}</p><h3 class="fu-title">{c['feel'][k]}</h3><p class="fu-text">{c['descs'][k]}</p></div>''' for k in range(n)]
    panes.append(f'''          <div class="fu-pane" data-i="-2"><p class="fu-kick">{c['close_k']}</p><h3 class="fu-title">{c['close_t']}</h3><p class="fu-text">{c['close_d']}</p><a class="fu-go" href="{c['close_href']}" tabindex="-1">{c['close_cta']}{arrow}</a></div>''')
    tabs = [f'''        <button type="button" class="fu-tab" role="tab" id="fu-tab-{k}" data-fu-tab="{k}" aria-selected="false" aria-controls="fu-pane-{k}" tabindex="{0 if k == 0 else -1}"><i class="fu-prog" aria-hidden="true"></i><span class="fu-n" dir="ltr">0{k + 1}</span><span class="fu-t">{c['names'][k]}</span><i class="fu-tick" aria-hidden="true"></i></button>''' for k in range(n)]
    panes, tabs = "\n".join(panes), "\n".join(tabs)
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4. FURNITURE ━ -->
<section id="furniture" data-screen-label="Furniture" data-svc-furn{' dir="rtl"' if ar else ''} style="scroll-margin-top:var(--fiq-svc-offset,132px);background:#F5F2ED;color:#3A2D25;position:relative;padding:clamp(64px,8vw,100px) {PAD} 0;overflow:clip;">
  <style>
    [data-svc-furn] .fu-wrap{{max-width:1280px;margin:0 auto;}}
    [data-svc-furn] .fu-head{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:clamp(32px,5vw,88px);align-items:end;margin-bottom:clamp(40px,4.4vw,64px);}}
    [data-svc-furn] .fu-eyebrow{{display:flex;align-items:center;gap:16px;margin-bottom:24px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    [data-svc-furn] .fu-eyebrow i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    [data-svc-furn] .fu-h2{{font-family:{font};font-weight:500;font-size:clamp(32px,3.8vw,54px);line-height:1.08;letter-spacing:{'0' if ar else '-0.015em'};color:#1F1F1F;margin:0;text-wrap:balance;}}
    [data-svc-furn] .fu-body{{font-family:{font};font-weight:500;font-size:{'clamp(22px,2vw,28px)' if ar else 'clamp(20px,1.9vw,26px)'};line-height:1.4;letter-spacing:{'0' if ar else '-0.005em'};text-wrap:balance;max-width:30ch;color:#3A2D25;margin:0 0 28px;}}
    [data-svc-furn] .fu-cta{{display:inline-flex;align-items:center;gap:12px;padding:17px 30px;background:#3A2D25;color:#F5F2ED;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;border:1px solid #3A2D25;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-furn] .fu-cta:hover,[data-svc-furn] .fu-cta:focus-visible{{background:transparent;color:#3A2D25;}}
    [data-svc-furn] .fu-rise{{opacity:0;transform:translateY(24px);transition:opacity 0.9s {EASE},transform 0.9s {EASE};}}
    [data-svc-furn].is-in .fu-rise{{opacity:1;transform:none;}}
    [data-svc-furn].is-in .fu-rise--2{{transition-delay:0.12s;}}
    [data-svc-furn].is-in .fu-rise--3{{transition-delay:0.24s;}}
    [data-svc-furn] .fu-block{{margin-inline:calc(50% - 50vw + var(--fu-sb,0px) / 2);background:#3A2D25;}}
    [data-svc-furn] .fu-frame{{position:relative;}}
    [data-svc-furn] .fu-stage{{position:relative;height:min(calc(100vh - var(--fiq-svc-offset,132px) - var(--fu-band,92px)),55.8vw);height:min(calc(100svh - var(--fiq-svc-offset,132px) - var(--fu-band,92px)),55.8vw);min-height:440px;overflow:hidden;background:#E8DFD8;container-type:size;}}
    /* the photograph, the traced pieces and the tags share one box that covers the stage, so they crop as one */
    [data-svc-furn] .fu-cover{{position:absolute;left:50%;top:50%;width:max(100cqw,calc(100cqh * {W} / {H}));height:max(100cqh,calc(100cqw * {H} / {W}));transform:translate(-50%,-50%);}}
    [data-svc-furn] .fu-shot{{position:absolute;inset:0;width:100%;height:100%;opacity:0;transition:opacity 1.1s {EASE};}}
    [data-svc-furn] .fu-shot.on{{opacity:1;}}
    [data-svc-furn] .fu-svg{{position:absolute;inset:0;width:100%;height:100%;}}
    [data-svc-furn] .fu-line polygon{{fill:none;vector-effect:non-scaling-stroke;stroke-linejoin:round;}}
    [data-svc-furn] .fu-halo{{stroke:rgba(245,242,237,0.75);stroke-width:4;}}
    [data-svc-furn] .fu-dash{{stroke:#3A2D25;stroke-width:1.6;stroke-dasharray:8 6;}}
    [data-svc-furn] .fu-line{{transition:opacity 0.5s {EASE};}}
    [data-svc-furn] .fu-line.on{{opacity:0;}}
    [data-svc-furn] .fu-tag{{position:absolute;display:flex;align-items:center;gap:8px;transform:translate(-5px,-50%);pointer-events:none;opacity:0;transition:opacity 0.5s {EASE};}}
    [data-svc-furn] .fu-tag.on{{opacity:1;transition-delay:0.7s;}}
    [data-svc-furn] .fu-tag i{{width:9px;height:9px;flex:none;border-radius:50%;background:#F5F2ED;box-shadow:0 0 0 1px #3A2D25,0 0 0 5px rgba(245,242,237,0.45);}}
    [data-svc-furn] .fu-tag b{{font-weight:500;padding:8px 12px;background:#1F1F1F;color:#F5F2ED;font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;white-space:nowrap;}}
    [data-svc-furn] .fu-tag.is-left{{flex-direction:row-reverse;transform:translate(calc(-100% + 5px),-50%);}}
    [data-svc-furn] .fu-in{{position:absolute;inset:0;width:min(1280px,calc(100% - 2 * {PAD}));margin:0 auto;pointer-events:none;}}
    [data-svc-furn] .fu-view{{position:absolute;top:clamp(16px,2.2vw,32px);left:0;display:flex;border:1px solid rgba(31,31,31,0.2);background:rgba(245,242,237,0.72);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);pointer-events:auto;}}
    [data-svc-furn] .fu-view button{{padding:11px 16px;border:0;background:transparent;color:rgba(31,31,31,0.6);font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;cursor:pointer;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-furn] .fu-view button:hover{{color:#1F1F1F;}}
    [data-svc-furn] .fu-view button[aria-pressed="true"]{{background:#1F1F1F;color:#F5F2ED;}}
    [data-svc-furn] .fu-panel{{position:absolute;top:clamp(16px,2.2vw,32px);right:0;width:min(400px,36%);display:grid;pointer-events:none;}}
    [data-svc-furn] .fu-pane{{grid-area:1/1;align-self:start;padding:clamp(22px,2.2vw,30px);background:rgba(245,242,237,0.86);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);box-shadow:0 24px 80px rgba(58,45,37,0.18);pointer-events:auto;opacity:0;visibility:hidden;transform:translateY(10px);transition:opacity 0.6s {EASE},transform 0.6s {EASE},visibility 0s linear 0.6s;}}
    [data-svc-furn] .fu-pane.is-on{{opacity:1;visibility:visible;transform:none;transition-delay:0.25s,0.25s,0s;}}
    [data-svc-furn] .fu-count{{margin:0 0 14px;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.24em;color:#8B6B4A;}}
    [data-svc-furn] .fu-kick{{margin:0 0 10px;font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;color:#8B6B4A;}}
    [data-svc-furn] .fu-title{{margin:0 0 12px;font-family:{font};font-weight:500;font-size:clamp(21px,2vw,28px);line-height:1.2;color:#1F1F1F;text-wrap:balance;}}
    [data-svc-furn] .fu-text{{margin:0;font-family:{font};font-size:{'14px' if ar else '13px'};line-height:1.7;color:#5B4636;}}
    [data-svc-furn] .fu-go{{display:inline-flex;align-items:center;gap:12px;margin-top:20px;padding:15px 24px;background:#3A2D25;color:#F5F2ED;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;border:1px solid #3A2D25;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-furn] .fu-go:hover,[data-svc-furn] .fu-go:focus-visible{{background:transparent;color:#3A2D25;}}
    [data-svc-furn] .fu-cap{{position:absolute;bottom:clamp(14px,2vw,24px);right:calc((100% - min(1280px,100% - 2 * {PAD})) / 2);margin:0;padding:7px 12px;background:rgba(31,31,31,0.62);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);color:rgba(245,242,237,0.85);font-family:{font};font-size:{'12px' if ar else '10.5px'};pointer-events:none;}}
    [data-svc-furn] .fu-tabs{{display:grid;grid-template-columns:repeat({n},minmax(0,1fr));width:min(1280px,calc(100% - 2 * {PAD}));margin:0 auto;}}
    [data-svc-furn] .fu-tab{{position:relative;display:flex;align-items:center;gap:14px;padding:26px clamp(14px,1.6vw,22px) 28px;border:0;border-inline-start:1px solid rgba(245,242,237,0.12);background:transparent;color:rgba(245,242,237,0.55);text-align:start;cursor:pointer;transition:color 0.4s {EASE},background 0.4s {EASE};}}
    [data-svc-furn] .fu-tab:first-child{{border-inline-start:0;}}
    [data-svc-furn] .fu-tab:hover{{color:#F5F2ED;background:rgba(245,242,237,0.04);}}
    [data-svc-furn] .fu-tab:focus-visible{{outline:1px solid #D6C2A8;outline-offset:-4px;}}
    [data-svc-furn] .fu-tab[aria-selected="true"]{{color:#F5F2ED;}}
    [data-svc-furn] .fu-prog{{position:absolute;top:0;left:0;right:0;height:2px;background:rgba(245,242,237,0.1);}}
    [data-svc-furn] .fu-prog::after{{content:"";position:absolute;inset:0;background:#D6C2A8;transform:scaleX(var(--p,0));transform-origin:{'100%' if ar else '0%'} 50%;}}
    [data-svc-furn] .fu-n{{flex:none;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.2em;color:#D6C2A8;}}
    [data-svc-furn] .fu-t{{flex:1;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.18em'};text-transform:uppercase;line-height:1.5;}}
    [data-svc-furn] .fu-tick{{flex:none;width:12px;height:7px;border-left:1.5px solid #D6C2A8;border-bottom:1.5px solid #D6C2A8;transform:rotate(-45deg) scale(0.6);opacity:0;margin-top:-4px;transition:opacity 0.4s {EASE},transform 0.4s {EASE};}}
    [data-svc-furn] .fu-tab.is-done .fu-tick{{opacity:1;transform:rotate(-45deg) scale(1);}}
    @media(min-width:901px) and (min-height:600px){{
      [data-svc-furn] .fu-block{{position:sticky;top:var(--fiq-svc-offset,132px);}}
      [data-svc-furn] .fu-spacer{{height:{(n + 2) * 45}vh;}}
    }}
    @media(max-width:900px){{
      [data-svc-furn] .fu-head{{grid-template-columns:1fr;}}
      [data-svc-furn] .fu-stage{{height:auto;min-height:0;aspect-ratio:4/3;}}
      [data-svc-furn] .fu-in{{position:static;width:auto;}}
      [data-svc-furn] .fu-view{{left:clamp(14px,2vw,24px);top:clamp(14px,2vw,24px);}}
      [data-svc-furn] .fu-panel{{position:relative;top:auto;right:auto;width:auto;}}
      [data-svc-furn] .fu-pane{{background:#F5F2ED;box-shadow:none;-webkit-backdrop-filter:none;backdrop-filter:none;}}
      [data-svc-furn] .fu-cap{{right:14px;bottom:12px;}}
      [data-svc-furn] .fu-tabs{{width:100%;grid-template-columns:repeat(2,minmax(0,1fr));}}
      [data-svc-furn] .fu-tab{{border-top:1px solid rgba(245,242,237,0.12);}}
      [data-svc-furn] .fu-tab:nth-child(2n+1){{border-inline-start:0;}}
      [data-svc-furn] .fu-tag b{{padding:5px 8px;font-size:{'11px' if ar else '8.5px'};}}
    }}
    @media(max-width:600px){{
      [data-svc-furn] .fu-stage{{aspect-ratio:1/1;}}
      [data-svc-furn] .fu-tag{{display:none;}}
      [data-svc-furn] .fu-view button{{padding:9px 12px;}}
      [data-svc-furn] .fu-tab{{padding:18px 12px 20px;}}
      [data-svc-furn] .fu-cta{{width:100%;justify-content:center;box-sizing:border-box;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-svc-furn] *,[data-svc-furn] *::after{{transition:none!important;}}
      [data-svc-furn] .fu-rise{{opacity:1;transform:none;}}
    }}
  </style>
  <div class="fu-wrap">
    <div class="fu-head">
      <div class="fu-rise">
        <div class="fu-eyebrow"><i></i>{c['eyebrow']}</div>
        <h2 class="fu-h2">{c['h2']}</h2>
      </div>
      <div class="fu-rise fu-rise--2">
        <p class="fu-body">{c['body']}</p>
        <a class="fu-cta" href="{c['href']}">{c['cta']}{arrow}</a>
      </div>
    </div>
    <div class="fu-track">
    <div class="fu-block fu-rise fu-rise--3">
      <div class="fu-frame">
        <div class="fu-stage" data-fu-stage>
          <div class="fu-cover">
{frames(c['alt'])}
{stage_svg()}
            {tags(c)}
          </div>
          <p class="fu-cap">{c['cap']}</p>
        </div>
        <div class="fu-in">
          <div class="fu-view" role="group" aria-label="{c['view']}"><button type="button" data-fu-view="render" aria-pressed="true">{c['render']}</button><button type="button" data-fu-view="room" aria-pressed="false">{c['room']}</button></div>
          <div class="fu-panel" aria-live="polite">
{panes}
          </div>
        </div>
      </div>
      <div class="fu-band"><div class="fu-tabs" role="tablist" aria-label="{c['steps']}">
{tabs}
      </div></div>
    </div>
    <div class="fu-spacer" aria-hidden="true"></div>
    </div>
  </div>
</section>
"""


JS = """    // ── SERVICES, FURNITURE: FROM RENDER TO ROOM ────────────────────────────
    {
      const sec = document.querySelector('[data-svc-furn]');
      if (sec) {
        const stage = sec.querySelector('[data-fu-stage]'), block = sec.querySelector('.fu-block'), track = sec.querySelector('.fu-track');
        const shots = Array.from(sec.querySelectorAll('.fu-shot')), lines = Array.from(sec.querySelectorAll('.fu-line'));
        const tags = Array.from(sec.querySelectorAll('.fu-tag')), panes = Array.from(sec.querySelectorAll('.fu-pane'));
        const tabs = Array.from(sec.querySelectorAll('[data-fu-tab]')), views = Array.from(sec.querySelectorAll('[data-fu-view]'));
        const go = sec.querySelector('.fu-go'), last = tabs.length - 1;
        const STEPS = tabs.length + 2;   // pinned: the render, each category, the finished room
        const HOLD = 5200, REST = 2600;  // phones: per category, and the render before each cycle
        const pinMQ = matchMedia('(min-width:901px) and (min-height:600px)');
        let pinned = pinMQ.matches, idx = -1, auto = !reduced, seen = false, visible = false, hover = false;
        let acc = 0, then = 0, raf = 0, ticking = false, jump = null, quiet = null;
        // i = -1 is the render; 0..3 places that category on top of the ones before; -2 is the finished room
        const show = (i) => {
          idx = i; acc = 0;
          const placed = (k) => i === -2 || k <= i;
          const f = i === -2 ? shots.length - 1 : i + 1;  // frames stack in order, so showing up to f crossfades just the newest
          shots.forEach((im) => im.classList.toggle('on', +im.dataset.f <= f));
          lines.forEach((g) => g.classList.toggle('on', placed(+g.dataset.k)));
          tags.forEach((t) => t.classList.toggle('on', +t.dataset.k === i));
          stage.classList.toggle('is-done', i === -2);
          panes.forEach((p) => p.classList.toggle('is-on', +p.dataset.i === i));
          tabs.forEach((t, k) => {
            t.setAttribute('aria-selected', k === i ? 'true' : 'false');
            t.classList.toggle('is-done', i === -2 || k < i);
            t.tabIndex = k === Math.max(i, 0) ? 0 : -1;
            if (!pinned) t.style.setProperty('--p', k === i && !auto ? 1 : 0);
          });
          views.forEach((v) => v.setAttribute('aria-pressed', (v.dataset.fuView === 'room') === (i === -2) ? 'true' : 'false'));
          go.tabIndex = i === -2 ? 0 : -1;
        };
        const geo = () => {
          const top = parseFloat(getComputedStyle(block).top) || 0;
          return { start: track.getBoundingClientRect().top + window.scrollY - top, dist: Math.max(1, track.offsetHeight - block.offsetHeight) };
        };
        const stateAt = () => {
          const g = geo(), x = Math.min(STEPS - 0.0001, Math.max(0, (window.scrollY - g.start) / g.dist) * STEPS), seg = Math.floor(x);
          return { i: seg === 0 ? -1 : seg === STEPS - 1 ? -2 : seg - 1, f: x - seg };
        };
        const goTo = (i) => { const g = geo(); window.scrollTo({ top: g.start + g.dist * (i + 1.5) / STEPS, behavior: reduced ? 'auto' : 'smooth' }); };
        const onScroll = () => {
          ticking = false;
          if (!pinned) return;
          const st = stateAt();
          if (jump !== null) { if (st.i === jump) jump = null; else return; }   // a click glides past the categories in between
          if (quiet !== null) { if (st.i !== quiet) quiet = null; else return; } // Render / Room holds until the scroll moves on
          if (st.i !== idx) show(st.i);
          tabs.forEach((t, k) => t.style.setProperty('--p', k === st.i ? st.f.toFixed(4) : 0));
        };
        window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
        const take = (i) => { auto = false; quiet = null; if (pinned) { jump = i; show(i); goTo(i); } else show(i); };
        tabs.forEach((t, k) => {
          t.addEventListener('click', () => take(k));
          t.addEventListener('keydown', (e) => {
            const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
            if (!d) return;
            e.preventDefault();
            const n = (k + (sec.getAttribute('dir') === 'rtl' ? -d : d) + tabs.length) % tabs.length;
            take(n); tabs[n].focus();
          });
        });
        // Empty shows the bare room with its plan, Furnished the finished one; either holds until the scroll moves on
        views.forEach((v) => v.addEventListener('click', () => {
          auto = false; jump = null;
          quiet = pinned ? stateAt().i : null;
          show(v.dataset.fuView === 'room' ? -2 : -1);
        }));
        // 100vw counts the scrollbar; the band's real height sizes the stage so the two fill the screen
        const fit = () => {
          sec.style.setProperty('--fu-sb', (window.innerWidth - document.documentElement.clientWidth) + 'px');
          sec.style.setProperty('--fu-band', sec.querySelector('.fu-band').offsetHeight + 'px');
        };
        fit();
        window.addEventListener('resize', fit);
        if (document.fonts) document.fonts.ready.then(fit);
        pinMQ.addEventListener('change', () => {
          pinned = pinMQ.matches; jump = quiet = null;
          if (pinned) onScroll(); else tabs.forEach((t, k) => t.style.setProperty('--p', k === idx ? 1 : 0));
        });
        block.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') hover = true; });  // a mouse resting on it pauses the cycle; taps do not
        block.addEventListener('pointerleave', () => { hover = false; });
        document.addEventListener('visibilitychange', () => { then = 0; });  // back from a hidden tab, time starts afresh
        const loop = (now) => {
          // real time between frames, so a throttled frame rate does not slow the cycle
          const dt = then ? now - then : 0; then = now;
          if (!pinned && auto && !hover && !document.hidden) {
            acc += dt;
            if (idx >= 0) tabs[idx].style.setProperty('--p', Math.min(1, acc / HOLD).toFixed(4));
            if (acc >= (idx === -1 ? REST : HOLD)) show(idx === last ? -2 : idx < 0 ? 0 : idx + 1);
          }
          raf = visible ? requestAnimationFrame(loop) : 0;
        };
        new IntersectionObserver((es, o) => { es.forEach((e) => { if (e.isIntersecting) { sec.classList.add('is-in'); o.disconnect(); } }); }, { rootMargin: '0px 0px -15% 0px' }).observe(sec);
        new IntersectionObserver((es) => {
          es.forEach((e) => {
            visible = e.isIntersecting;
            if (visible && !seen && !pinned) { seen = true; if (reduced) show(0); else acc = REST - 1400; }
            if (visible && !raf) { then = 0; raf = requestAnimationFrame(loop); }
          });
        }, { threshold: 0.4 }).observe(stage);
        onScroll();
      }
    }

"""
MARK = "    // ── SCROLL REVEAL"

for path, lang in [("services.dc.html", "en"), ("services.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ 4\. FURNITURE ━ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── SERVICES, FURNITURE:"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

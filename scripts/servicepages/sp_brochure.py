"""Service pages, the closing form: the studio edition.

The template for the last section of the four service pages: the service brochure, drawn as a printed book
beside the request form. When the section comes into view the cover swings open on its spine and shows the
first spread, a full-page photograph and a contents page listing what is inside. The form asks whether the
visitor wants the brochure or a consultation; the page's other "book a consultation" links arrive with the
second already chosen. The form's fields, bindings and submission are the page's own, kept as they were; the
request it sends now says which of the two was asked for.
The studio sends the brochure by email: no file is downloaded from the page.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/servicepages/sp_brochure.py [page ...]
"""
import re, sys

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
PAGE = {
    "services-interior-design": dict(
        cover="courtyard-residence-walnut-mashrabiya-detail", left="obhur-estate-teak-rawasheen-gallery", small="family-office-limestone-bronze-detail",
        en=dict(
            eyebrow="The Interior Design Brochure", h2="Take the studio home.",
            sub="How we plan, render and approve every space, in one brochure.",
            title="Interior Design", edition="The Studio Edition", contents="Contents",
            items=["Three pillars of design excellence", "Six design disciplines", "Concept projects in four sectors", "From first brief to handover"],
            want=("Send me the brochure", "Book a consultation"),
            label=("Request the Brochure", "Book a Design Consultation"),
            req=("Interior Design brochure", "Interior design consultation"),
            note="The studio emails the brochure, and replies to consultation requests personally.",
            first="First Name", last="Last Name", email="Email Address", phone="Phone Number",
            ph=("First name", "Last name", "you@company.com"),
            thanks="Thank you, your request has been received. The studio will be in touch shortly.",
            hp="Leave this field empty", sending="Sending…",
            missing="Please complete the following before submitting:", fail="Something went wrong. Please try again, or email us at info@furnishiq.net",
            fields=["First Name", "Last Name", "a valid Email Address", "Phone Number"],
            choose="What would you like?",
            alt="The Interior Design brochure, open on its first spread"),
        ar=dict(
            eyebrow="كتيّب التصميم الداخلي", h2="خذ الاستوديو معك.",
            sub="كيف نخطط لكل مساحة ونجسّدها ونعتمدها، في كتيّب واحد.",
            title="التصميم الداخلي", edition="إصدار الاستوديو", contents="المحتويات",
            items=["ثلاث ركائز للتميز في التصميم", "ستة تخصصات تصميمية", "تصورات تصميمية في أربعة قطاعات", "من الإحاطة الأولى حتى التسليم"],
            want=("أرسلوا لي الكتيّب", "احجز استشارة"),
            label=("اطلب الكتيّب", "احجز استشارة تصميم"),
            req=("كتيّب التصميم الداخلي", "استشارة تصميم داخلي"),
            note="يرسل الاستوديو الكتيّب عبر البريد الإلكتروني، ويرد شخصياً على طلبات الاستشارة.",
            first="الاسم الأول", last="اسم العائلة", email="البريد الإلكتروني", phone="رقم الهاتف",
            ph=("الاسم الأول", "اسم العائلة", "you@company.com"),
            thanks="شكراً لك، تم استلام طلبك. سيتواصل معك الاستوديو قريباً.",
            hp="اترك هذا الحقل فارغاً", sending="جارٍ الإرسال…",
            missing="يرجى إكمال ما يلي قبل الإرسال:", fail="حدث خطأ ما. يرجى المحاولة مرة أخرى، أو مراسلتنا على info@furnishiq.net",
            fields=["الاسم الأول", "اسم العائلة", "بريد إلكتروني صحيح", "رقم الهاتف"],
            choose="ماذا تفضّل؟",
            alt="كتيّب التصميم الداخلي، مفتوحاً على صفحته الأولى"),
    ),
}
_ID = PAGE["services-interior-design"]
PAGE["services-fitout"] = dict(
    cover="office-fit-out-walnut-wall-panel-installation-riyadh", left="desert-stone-resort-rammed-earth-detail", small="obhur-estate-coral-stone-detail",
    en=dict(_ID["en"], eyebrow="The Fit-Out Brochure", h2="See how a shell becomes a space.",
            sub="How we plan, build and hand over every fit-out, in one brochure.",
            title="Fit-Out",
            items=["Three pillars of fit-out excellence", "Six fit-out disciplines", "Concept projects in four sectors", "From raw shell to handover"],
            want=("Send me the brochure", "Request a quote"), label=("Request the Brochure", "Request a Fit-Out Quote"),
            req=("Fit-Out brochure", "Fit-out quote"),
            note="The studio emails the brochure, and replies to quote requests personally.",
            alt="The Fit-Out brochure, open on its first spread"),
    ar=dict(_ID["ar"], eyebrow="كتيّب التشطيبات", h2="شاهد كيف يتحول الهيكل إلى مساحة.",
            sub="كيف نخطط لكل مشروع تشطيب وننفّذه ونسلّمه، في كتيّب واحد.",
            title="التشطيبات",
            items=["ثلاث ركائز للتميز في التشطيبات", "ستة تخصصات في التشطيب", "تصورات تصميمية في أربعة قطاعات", "من الهيكل الخام حتى التسليم"],
            want=("أرسلوا لي الكتيّب", "اطلب عرض سعر"), label=("اطلب الكتيّب", "اطلب عرض سعر للتشطيب"),
            req=("كتيّب التشطيبات", "عرض سعر للتشطيب"),
            note="يرسل الاستوديو الكتيّب عبر البريد الإلكتروني، ويرد شخصياً على طلبات عروض الأسعار.",
            alt="كتيّب التشطيبات، مفتوحاً على صفحته الأولى"),
)
PAGE["services-mep"] = dict(
    cover="mep-pillar-utility-integration-ceiling-detail", left="mep-ceiling-services-installation-riyadh", small="mep-pillar-operational-integrity-plant-room",
    en=dict(_ID["en"], eyebrow="The Engineering Brochure", h2="See what sits behind the ceiling.",
            sub="How we design, install and commission every system, in one brochure.",
            title="Engineering &amp; MEP",
            items=["Three pillars of engineering excellence", "Six MEP disciplines", "Concept projects in four sectors", "From first drawing to commissioning"],
            want=("Send me the brochure", "Request a quote"), label=("Request the Brochure", "Request an Engineering Quote"),
            req=("Engineering & MEP brochure", "Engineering quote"),
            note="The studio emails the brochure, and replies to quote requests personally.",
            alt="The Engineering & MEP brochure, open on its first spread"),
    ar=dict(_ID["ar"], eyebrow="كتيّب الهندسة", h2="شاهد ما خلف السقف.",
            sub="كيف نصمم كل نظام ونركّبه ونشغّله، في كتيّب واحد.",
            title="الهندسة والأنظمة الكهروميكانيكية",
            items=["ثلاث ركائز للتميز الهندسي", "ستة تخصصات كهروميكانيكية", "تصورات تصميمية في أربعة قطاعات", "من المخطط الأول حتى التشغيل"],
            want=("أرسلوا لي الكتيّب", "اطلب عرض سعر"), label=("اطلب الكتيّب", "اطلب عرض سعر هندسي"),
            req=("كتيّب الهندسة والأنظمة الكهروميكانيكية", "عرض سعر هندسي"),
            note="يرسل الاستوديو الكتيّب عبر البريد الإلكتروني، ويرد شخصياً على طلبات عروض الأسعار.",
            alt="كتيّب الهندسة والأنظمة الكهروميكانيكية، مفتوحاً على صفحته الأولى"),
)
PAGE["services-furniture"] = dict(
    cover="bespoke-furniture-leather-lounge-chair-riyadh", left="furniture-gallery-oak-brass-detail", small="courtyard-residence-majlis-seating-detail",
    en=dict(_ID["en"], eyebrow="The Furniture Brochure", h2="See the room, finished.",
            sub="How we source, place and style every piece, in one brochure.",
            title="Furniture",
            items=["Three pillars of furniture excellence", "Six furniture categories", "Concept projects in four sectors", "From first render to final placement"],
            want=("Send me the brochure", "Request a quote"), label=("Request the Brochure", "Request a Furniture Quote"),
            req=("Furniture brochure", "Furniture quote"),
            note="The studio emails the brochure, and replies to quote requests personally.",
            alt="The Furniture brochure, open on its first spread"),
    ar=dict(_ID["ar"], eyebrow="كتيّب الأثاث", h2="شاهد الغرفة مكتملة.",
            sub="كيف نورّد كل قطعة ونضعها وننسّقها، في كتيّب واحد.",
            title="الأثاث",
            items=["ثلاث ركائز للتميز في الأثاث", "ست فئات للأثاث", "تصورات تصميمية في أربعة قطاعات", "من التصور الأول حتى التموضع النهائي"],
            want=("أرسلوا لي الكتيّب", "اطلب عرض سعر"), label=("اطلب الكتيّب", "اطلب عرض سعر للأثاث"),
            req=("كتيّب الأثاث", "عرض سعر للأثاث"),
            note="يرسل الاستوديو الكتيّب عبر البريد الإلكتروني، ويرد شخصياً على طلبات عروض الأسعار.",
            alt="كتيّب الأثاث، مفتوحاً على صفحته الأولى"),
)
ARROW = {
    "en": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
    "ar": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>',
}


def build(page, lang):
    ar = lang == "ar"
    P = PAGE[page]
    c = P[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    caps = "normal" if ar else "0.22em"
    small = "12px" if ar else "9px"
    PAD = "clamp(24px,5vw,80px)"
    side = "right" if ar else "left"         # the spine: the cover swings towards the reading start
    items = "".join(f'<li><span dir="ltr">0{k + 1}</span>{t}</li>' for k, t in enumerate(c["items"]))
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ CTA ━━━━━━━━━━━━━ -->
<section id="contact" data-screen-label="CTA" data-sp-bx{' dir="rtl"' if ar else ''} style="scroll-margin-top:80px;background:#3A2D25;color:#F5F2ED;position:relative;padding:clamp(64px,8vw,128px) {PAD};overflow:clip;">
  <style>
    [data-sp-bx] .bx-wrap{{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:minmax(0,8fr) minmax(0,5fr);gap:clamp(40px,5vw,96px);align-items:center;}}
    /* the book: two pages wide; closed, it sits centred, the cover over the second page */
    /* the book reaches into the page margin on its side, up to 200px, so it can grow without narrowing the form */
    [data-sp-bx] .bx-stage{{perspective:2600px;display:flex;justify-content:center;margin-inline-start:calc(-1 * clamp(0px,(100vw - 1280px) / 2 - 32px,200px));}}
    [data-sp-bx] .bx-book{{position:relative;width:min(100%,900px);aspect-ratio:3/2;transform:translateX({'25%' if ar else '-25%'}) rotateX(8deg);transform-style:preserve-3d;transition:transform 1.6s {EASE} 0.2s;}}
    [data-sp-bx].is-open .bx-book{{transform:none;}}
    [data-sp-bx] .bx-page{{position:absolute;top:0;width:50%;height:100%;overflow:hidden;background:#F5F2ED;box-shadow:0 30px 70px rgba(0,0,0,0.45);}}
    [data-sp-bx] .bx-r{{{'left' if ar else 'right'}:0;}}
    [data-sp-bx] .bx-cover{{position:absolute;top:0;{'left' if ar else 'right'}:0;width:50%;height:100%;transform-origin:{side} center;transform-style:preserve-3d;transition:transform 1.7s cubic-bezier(0.65,0,0.25,1) 0.5s;}}
    [data-sp-bx].is-open .bx-cover{{transform:rotateY({'180deg' if ar else '-180deg'});}}
    [data-sp-bx] .bx-face{{position:absolute;inset:0;overflow:hidden;backface-visibility:hidden;-webkit-backface-visibility:hidden;}}
    /* no shadow on the cover: a box-shadow widens the face's 3D layer past the spine, and as it swings the browser
       sorts the contents page over the cover's spine-side strip. The page beneath casts the closed book's shadow. */
    [data-sp-bx] .bx-front{{background:#1F1F1F;}}
    [data-sp-bx] .bx-back{{transform:rotateY(180deg);background:#3A2D25;}}
    [data-sp-bx] .bx-face img,[data-sp-bx] .bx-r>img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}}
    /* the cover: the logo on its charcoal band, the title over the photograph */
    [data-sp-bx] .bx-band{{position:absolute;inset:0 0 auto 0;z-index:1;display:flex;align-items:center;justify-content:center;height:16%;background:#1F1F1F;}}
    [data-sp-bx] .bx-band img{{position:static;width:auto;height:42%;object-fit:contain;}}
    [data-sp-bx] .bx-front .bx-photo{{position:absolute;inset:16% 0 0 0;}}
    [data-sp-bx] .bx-front .bx-photo::after{{content:"";position:absolute;inset:0;background:rgba(20,15,11,0.38);}}
    [data-sp-bx] .bx-ctitle{{position:absolute;inset:auto 9% 9% 9%;z-index:1;color:#F5F2ED;}}
    [data-sp-bx] .bx-ctitle b{{display:block;font-family:{font};font-weight:500;font-size:clamp(20px,2.4vw,42px);line-height:1.05;letter-spacing:{'0' if ar else '-0.02em'};}}
    [data-sp-bx] .bx-ctitle span{{display:block;margin-top:10px;font-family:{font};font-size:{'11px' if ar else '8px'};letter-spacing:{caps};text-transform:uppercase;color:#D6C2A8;}}
    [data-sp-bx] .bx-spine{{position:absolute;top:0;bottom:0;{side}:0;width:5px;background:rgba(0,0,0,0.35);z-index:2;}}
    /* the contents page */
    [data-sp-bx] .bx-text{{position:absolute;inset:0;padding:11% 10%;display:flex;flex-direction:column;color:#3A2D25;}}
    [data-sp-bx] .bx-text h3{{margin:0 0 7%;font-family:{font};font-weight:500;font-size:{'11px' if ar else '8px'};letter-spacing:{caps};text-transform:uppercase;color:#8B6B4A;}}
    [data-sp-bx] .bx-text ol{{list-style:none;margin:0;padding:0;}}
    [data-sp-bx] .bx-text li{{display:flex;gap:10px;padding:4.5% 0;border-bottom:1px solid rgba(58,45,37,0.14);font-family:{font};font-size:clamp(9px,0.9vw,15px);line-height:1.35;color:#1F1F1F;}}
    [data-sp-bx] .bx-text li span{{flex:none;font-family:'Lama Sans',sans-serif;font-size:0.8em;letter-spacing:0.12em;color:#8B6B4A;padding-top:0.15em;}}
    [data-sp-bx] .bx-thumb{{position:relative;margin-top:auto;aspect-ratio:3/2;overflow:hidden;}}
    [data-sp-bx] .bx-thumb img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}}
    [data-sp-bx] .bx-shadow{{position:absolute;inset:auto 6% -10% 6%;height:10%;background:rgba(0,0,0,0.5);filter:blur(24px);transform:translateZ(-1px);}}
    /* the form */
    [data-sp-bx] .bx-eyebrow{{display:flex;align-items:center;gap:16px;margin:0 0 22px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#D6C2A8;}}
    [data-sp-bx] .bx-eyebrow i{{display:block;width:32px;height:1px;background:#D6C2A8;}}
    [data-sp-bx] .bx-h2{{margin:0 0 14px;font-family:{font};font-weight:500;font-size:clamp(34px,3.8vw,56px);line-height:1.06;letter-spacing:{'0' if ar else '-0.02em'};color:#F5F2ED;}}
    [data-sp-bx] .bx-sub{{margin:0 0 clamp(28px,3vw,40px);max-width:{'18em' if ar else '30ch'};font-family:{font};font-weight:500;font-size:{'clamp(19px,1.6vw,22px)' if ar else 'clamp(17px,1.5vw,21px)'};line-height:1.45;color:rgba(245,242,237,0.8);text-wrap:balance;}}
    [data-sp-bx] .bx-want{{display:grid;grid-template-columns:1fr 1fr;margin:0 0 28px;padding:0;border:1px solid rgba(214,194,168,0.3);}}
    [data-sp-bx] .bx-want legend{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);}}
    [data-sp-bx] .bx-want label{{position:relative;cursor:pointer;}}
    [data-sp-bx] .bx-want input{{position:absolute;opacity:0;inset:0;margin:0;cursor:pointer;}}
    [data-sp-bx] .bx-want span{{display:block;padding:14px 12px;text-align:center;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.16em'};text-transform:uppercase;color:rgba(245,242,237,0.6);transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-sp-bx] .bx-want input:checked+span{{background:#D6C2A8;color:#1F1F1F;}}
    [data-sp-bx] .bx-want input:focus-visible+span{{outline:1px solid #D6C2A8;outline-offset:3px;}}
    [data-sp-bx] .bx-names{{display:grid;grid-template-columns:1fr 1fr;gap:24px;}}
    [data-sp-bx] .bx-field{{display:block;margin-bottom:24px;}}
    [data-sp-bx] .bx-field>span{{display:block;margin-bottom:6px;font-family:{font};font-size:{'12px' if ar else '9px'};letter-spacing:{caps};text-transform:uppercase;color:rgba(214,194,168,0.75);}}
    [data-sp-bx] .bx-field input,[data-sp-bx] .bx-tel{{width:100%;box-sizing:border-box;padding:10px 0;border:0;border-bottom:1px solid rgba(214,194,168,0.3);background:transparent;color:#F5F2ED;font-family:'Lama Sans',sans-serif;font-size:15px;outline:none;border-radius:0;transition:border-color 0.3s {EASE};}}
    [data-sp-bx] .bx-field input::placeholder{{color:rgba(245,242,237,0.3);}}
    [data-sp-bx] .bx-field input:focus{{border-bottom-color:#D6C2A8;}}
    [data-sp-bx] .bx-tel{{display:flex;align-items:center;gap:10px;padding:0;direction:ltr;}}
    [data-sp-bx] .bx-tel:focus-within{{border-bottom-color:#D6C2A8;}}
    [data-sp-bx] .bx-tel i{{width:1px;height:16px;background:rgba(214,194,168,0.3);}}
    [data-sp-bx] .bx-tel input{{border:0;padding:10px 0;}}
    [data-sp-bx] .bx-btn{{display:flex;align-items:center;justify-content:center;gap:14px;width:100%;margin-top:8px;padding:20px 28px;background:#D6C2A8;color:#1F1F1F;border:1px solid #D6C2A8;cursor:pointer;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-sp-bx] .bx-btn:hover,[data-sp-bx] .bx-btn:focus-visible{{background:transparent;color:#D6C2A8;}}
    [data-sp-bx] .bx-btn:disabled{{opacity:0.6;cursor:wait;}}
    [data-sp-bx] .bx-note{{margin:16px 0 0;font-family:{font};font-size:{'13px' if ar else '12px'};line-height:1.6;color:rgba(245,242,237,0.5);}}
    [data-sp-bx] .bx-thanks{{margin:16px 0 0;padding:14px 16px;border:1px solid rgba(214,194,168,0.3);font-family:{font};font-size:{'14px' if ar else '13px'};line-height:1.6;color:#D6C2A8;}}
    [data-sp-bx] .bx-hp{{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;}}
    [data-sp-bx] .bx-rise{{opacity:0;transform:translateY(24px);transition:opacity 0.9s {EASE},transform 0.9s {EASE};}}
    [data-sp-bx].is-in .bx-rise{{opacity:1;transform:none;}}
    [data-sp-bx].is-in .bx-rise--2{{transition-delay:0.15s;}}
    @media(max-width:900px){{
      [data-sp-bx] .bx-wrap{{grid-template-columns:1fr;gap:56px;}}
      [data-sp-bx] .bx-book{{width:100%;}}
      [data-sp-bx] .bx-stage{{margin-inline-start:0;}}
      [data-sp-bx] .bx-names{{grid-template-columns:1fr;gap:0;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-sp-bx] *{{transition:none!important;}}
      [data-sp-bx] .bx-rise{{opacity:1;transform:none;}}
    }}
  </style>
  <div class="bx-wrap">
    <div class="bx-stage bx-rise" role="img" aria-label="{c['alt']}">
      <div class="bx-book">
        <span class="bx-shadow" aria-hidden="true"></span>
        <div class="bx-page bx-r">
          <div class="bx-text">
            <h3>{c['contents']}</h3>
            <ol>{items}</ol>
            <div class="bx-thumb"><img src="uploads/{P['small']}-1200.webp" alt="" loading="lazy" decoding="async"></div>
          </div>
        </div>
        <div class="bx-cover">
          <div class="bx-face bx-front">
            <div class="bx-band"><img src="assets/logo-default.png" alt="FurnishIQ" width="264" height="90"></div>
            <div class="bx-photo"><img src="uploads/{P['cover']}-1200.webp" alt="" loading="lazy" decoding="async"></div>
            <p class="bx-ctitle"><b>{c['title']}</b><span>{c['edition']}</span></p>
            <i class="bx-spine" aria-hidden="true"></i>
          </div>
          <div class="bx-face bx-back"><img src="uploads/{P['left']}-1200.webp" alt="" loading="lazy" decoding="async"></div>
        </div>
      </div>
    </div>
    <div class="bx-rise bx-rise--2">
      <p class="bx-eyebrow"><i></i>{c['eyebrow']}</p>
      <h2 class="bx-h2">{c['h2']}</h2>
      <p class="bx-sub">{c['sub']}</p>
      <form id="id-brochure-form" onSubmit="{{{{ onBrochureSubmit }}}}" novalidate>
        <div class="bx-hp" aria-hidden="true"><label for="id-hp-field">{c['hp']}</label><input id="id-hp-field" type="text" tabindex="-1" autocomplete="off" value="{{{{ formHoneypot }}}}" onChange="{{{{ onHoneypotChange }}}}"></div>
        <fieldset class="bx-want"><legend>{c['choose']}</legend>
          <label><input type="radio" name="bx-want" value="{c['req'][0]}" data-bx-want="0" data-label="{c['label'][0]}"><span>{c['want'][0]}</span></label>
          <label><input type="radio" name="bx-want" value="{c['req'][1]}" data-bx-want="1" data-label="{c['label'][1]}"><span>{c['want'][1]}</span></label>
        </fieldset>
        <div class="bx-names">
          <label class="bx-field"><span>{c['first']} *</span><input type="text" required autocomplete="given-name" placeholder="{c['ph'][0]}" value="{{{{ formFirstName }}}}" onChange="{{{{ onFirstNameChange }}}}"></label>
          <label class="bx-field"><span>{c['last']} *</span><input type="text" required autocomplete="family-name" placeholder="{c['ph'][1]}" value="{{{{ formLastName }}}}" onChange="{{{{ onLastNameChange }}}}"></label>
        </div>
        <label class="bx-field"><span>{c['email']} *</span><input type="email" required autocomplete="email" dir="ltr" placeholder="{c['ph'][2]}" value="{{{{ formEmail }}}}" onChange="{{{{ onEmailChange }}}}"></label>
        <div class="bx-field"><span>{c['phone']} *</span>
          <div class="bx-tel" id="id-phone-wrapper">{{{{ phoneSelect }}}}<i aria-hidden="true"></i><input type="tel" required autocomplete="tel-national" placeholder="58 033 0627" value="{{{{ formPhone }}}}" onChange="{{{{ onPhoneChange }}}}" id="id-phone-input" aria-label="{c['phone']}"></div>
        </div>
        <button type="submit" class="bx-btn" id="id-download-btn"><span id="id-download-btn-label" data-idle="{c['label'][0]}">{c['label'][0]}</span>{ARROW[lang]}</button>
        <p class="bx-note">{c['note']}</p>
        <sc-if value="{{{{ brochureSuccess }}}}" hint-placeholder-val="{{{{ null }}}}">
          <p class="bx-thanks" role="status">{c['thanks']}</p>
        </sc-if>
      </form>
    </div>
  </div>
</section>
"""


JS = """    // ── SERVICE PAGES, CLOSING FORM: THE STUDIO EDITION ─────────────────────
    {
      const sec = document.querySelector('[data-sp-bx]');
      if (sec) {
        const wants = Array.from(sec.querySelectorAll('[data-bx-want]')), lbl = sec.querySelector('#id-download-btn-label');
        const pick = (k) => { wants[k].checked = true; lbl.dataset.idle = wants[k].dataset.label; lbl.textContent = wants[k].dataset.label; };
        wants.forEach((w, k) => w.addEventListener('change', () => pick(k)));
        pick(0);
        // the page's "book a consultation" links arrive with the consultation chosen
        document.querySelectorAll('a[href="#contact"]').forEach((a) => { if (!sec.contains(a)) a.addEventListener('click', () => pick(1)); });
        if (location.hash === '#contact') pick(1);
        new IntersectionObserver((es, o) => { es.forEach((e) => { if (e.isIntersecting) { sec.classList.add('is-in'); setTimeout(() => sec.classList.add('is-open'), reduced ? 0 : 300); o.disconnect(); } }); }, { threshold: 0.3 }).observe(sec);
      }
    }

"""
MARK = "    // ── SCROLL REVEAL"


def patch_logic(s, c, page):
    """The form's submission, which lives in the page's own logic: the request names what was chosen, and the
    messages follow the page's language."""
    reps = [
        (re.compile(r"request: '[^']*',"), "request: (document.querySelector('[data-bx-want]:checked') || {}).value || " + repr(c['req'][0]) + ","),
        # the old button's idle words, whatever they were (the sending line is matched next)
        (re.compile(r"if \(btnLabel\) btnLabel\.textContent = '(?!Sending…|جارٍ الإرسال…)[^']*';"), "if (btnLabel) btnLabel.textContent = btnLabel.dataset.idle;"),
        (re.compile(r"if \(btnLabel\) btnLabel\.textContent = '(?:Sending…|جارٍ الإرسال…)';"), f"if (btnLabel) btnLabel.textContent = {c['sending']!r};"),
        (re.compile(r"alert\('(?:Please complete the following before submitting:|يرجى إكمال ما يلي قبل الإرسال:)\\n\\n'"), f"alert({(c['missing'] + chr(10) + chr(10))!r}"),
        (re.compile(r"alert\('(?:Something went wrong[^']*|حدث خطأ ما[^']*)'\)"), f"alert({c['fail']!r})"),
    ]
    # the submit code looks the button up by the old form's ids (fit-, mep-, ...); the new form's are id-download-btn
    s = re.sub(r"getElementById\('[a-z]+-download-btn(-label)?'\)", lambda m: "getElementById('id-download-btn" + (m.group(1) or "") + "')", s)
    for rx, new in reps:
        if new in s:
            continue   # patched by an earlier run
        s, n = rx.subn(lambda m: new, s, count=1)
        assert n == 1, (page, rx.pattern)
    f = c["fields"]
    for i, (en, old_ar) in enumerate([("First Name", "الاسم الأول"), ("Last Name", "اسم العائلة"), ("a valid Email Address", "بريد إلكتروني صحيح"), ("Phone Number", "رقم الهاتف")]):
        for old in (en, old_ar):
            s = s.replace(f"missing.push('{old}')", f"missing.push({f[i]!r})", 1)
    return s


pages = sys.argv[1:] or list(PAGE)
for page in pages:
    for name, lang in [(f"{page}.dc.html", "en"), (f"{page}.ar.dc.html", "ar")]:
        s = open(name, encoding="utf-8").read()
        s, n = re.subn(r"<!-- ━+ CTA ━+ -->\n<section id=\"contact\".*?\n</section>\n", lambda m: build(page, lang), s, count=1, flags=re.S)
        assert n == 1, name
        s = patch_logic(s, PAGE[page][lang], name)
        # the old form's inline hover and focus colours would fight the new form's own styles
        for stale in ("    // ── DOWNLOAD BUTTON HOVER", "    // ── PHONE WRAPPER FOCUS"):
            if stale in s:
                a = s.index(stale); b = s.index(chr(10) + "    // ── ", a + 1) + 1
                s = s[:a] + s[b:]
        old = "    // ── SERVICE PAGES, CLOSING FORM:"
        if old in s:
            a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
            s = s[:a] + s[b:]
        assert s.count(MARK) == 1, name
        s = s.replace(MARK, JS + MARK)
        open(name, "w", encoding="utf-8", newline="").write(s)
        print(name, "ok")

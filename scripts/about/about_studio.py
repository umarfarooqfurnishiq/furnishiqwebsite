import json
import os
import re

ROADS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "studio_map_labels.json"), encoding="utf-8"))

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
IMG = "desert-stone-resort-arrival-court"
C = {
    "en": dict(
        label="Begin Your Project", h2="Ready to Visualise Your Space?",
        body="Receive a clear plan, photoreal visuals, and a comprehensive budget roadmap tailored to your brief.",
        cta1="Book a Consultation", cta2="Discover Projects", pre="",
        cap="Concept visualisation", alt="Stone arrival court leading to a timber entrance at dusk",
        studio="Visit Our Studio", hq="Headquarters", city="Riyadh, Kingdom of Saudi Arabia", local="Local time",
        phone="Phone", email="Email", wa="WhatsApp", wa_txt="Message the studio",
        call="Call the studio directly", write="Write to the studio", plate="Studio contact details",
        wa_sub="Open a conversation", day="The day in Riyadh",
        addr="First Plaza, Al Takhassousi, Al Mathar Ash Shamali, Riyadh", pin="FurnishIQ Studio", maps="Headquarters: open in Google Maps", osm="Map data © OpenStreetMap contributors",
    ),
    "ar": dict(
        label="ابدأ مشروعك", h2="هل أنت مستعد لتصور مساحتك؟",
        body="احصل على خطة واضحة، وتصورات بصرية واقعية، وخارطة طريق مالية شاملة مصممة خصيصاً لمتطلباتك.",
        cta1="احجز استشارة", cta2="اكتشف مشاريعنا", pre="/ar",
        cap="تصور مفاهيمي", alt="ممر حجري يقود إلى مدخل خشبي عند الغروب",
        studio="زُر استوديونا", hq="المقر الرئيسي", city="الرياض، المملكة العربية السعودية", local="التوقيت المحلي",
        phone="الهاتف", email="البريد الإلكتروني", wa="واتساب", wa_txt="راسل الاستوديو",
        call="اتصال مباشر بالاستوديو", write="راسل الاستوديو كتابياً", plate="بيانات التواصل مع الاستوديو",
        wa_sub="ابدأ محادثة", day="اليوم في الرياض",
        addr="فيرست بلازا، طريق التخصصي، المعذر الشمالي، الرياض", pin="استوديو FurnishIQ", maps="المقر الرئيسي: افتح في خرائط Google", osm="بيانات الخريطة © OpenStreetMap",
    ),
}
ARROW_EN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
ARROW_AR = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>'

GO = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" aria-hidden="true"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="8 7 17 7 17 16"/></svg>'

ICON = dict(  # drawn in the band's sand tone, never the services' own colours
    phone='<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    mail='<rect x="2" y="4" width="20" height="16"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    wa='<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><path transform="translate(7.6 7.4) scale(0.4)" stroke-width="1" d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
)


def ico(name):
    return f'<span class="th-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="0.4" stroke-linejoin="round">{ICON[name]}</svg></span>'


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    btn_track = "normal" if ar else "0.2em"
    btn_size = "13px" if ar else "10px"
    arrow = ARROW_AR if ar else ARROW_EN
    roads = "".join(f'<span class="th-road th-road--{i}" style="left:{r['xa' if ar else 'x']}px;top:{r['ya' if ar else 'y']}px;transform:translate(-50%,-50%) rotate({r['aa' if ar else 'a']}deg);">{r['ar'] if ar else r['en']}</span>' for i, r in enumerate(ROADS))
    srcset = ", ".join(f"uploads/{IMG}-{w}.webp {w}w" for w in (1280, 1920, 2752))
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ STUDIO / CONTACT ━ -->
<section id="threshold" data-threshold{' dir="rtl"' if ar else ''} style="position:relative;background:#1E1610;color:#F5F2ED;padding:clamp(64px,8vw,100px) clamp(24px,5vw,80px) 0;overflow:clip;">
  <style>
    #threshold .th-wrap{{max-width:1280px;margin:0 auto;}}
    #threshold .th-label{{display:flex;align-items:center;justify-content:center;gap:16px;margin-bottom:clamp(28px,3.4vw,44px);font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#D6C2A8;}}
    #threshold .th-label i{{display:block;width:32px;height:1px;background:#D6C2A8;}}
    #threshold .th-stage{{position:relative;height:clamp(520px,80vh,780px);}}
    #threshold .th-ghost{{position:absolute;left:50%;top:0;bottom:0;width:var(--w0);transform:translateX(-50%);border:1px solid rgba(214,194,168,0.45);border-bottom:none;border-radius:999px 999px 0 0;opacity:calc(1 - var(--e,0) * 1.4);pointer-events:none;}}
    #threshold .th-door{{position:absolute;left:50%;top:0;bottom:0;width:var(--w,36%);transform:translateX(-50%);overflow:hidden;border-radius:var(--r,999px) var(--r,999px) 0 0;background:#3A2D25;}}
    #threshold .th-door img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 60%;transform:scale(calc(1.18 - 0.18 * var(--e,0)));}}
    #threshold .th-tint{{position:absolute;inset:0;background:rgba(30,22,16,calc(0.18 + 0.4 * var(--e,0)));}}
    #threshold .th-copy{{position:absolute;left:0;right:0;bottom:0;padding:clamp(28px,4vw,64px);display:flex;flex-direction:column;align-items:center;text-align:center;opacity:0;transform:translateY(20px);transition:opacity 0.8s {EASE},transform 0.8s {EASE};pointer-events:none;}}
    #threshold.is-open .th-copy{{opacity:1;transform:none;pointer-events:auto;}}
    #threshold .th-h2{{font-family:{font};font-size:clamp(32px,4.4vw,72px);font-weight:500;line-height:{'1.35' if ar else '1.05'};letter-spacing:{'normal' if ar else '-0.03em'};color:#FFFFFF;margin:0;max-width:1000px;text-wrap:balance;}}
    #threshold .th-body{{font-family:{font};font-size:{'17px' if ar else '16px'};line-height:1.75;color:rgba(245,242,237,0.82);margin:clamp(16px,1.6vw,22px) 0 0;max-width:560px;}}
    #threshold .th-ctas{{display:inline-grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:clamp(24px,2.6vw,36px);}}
    #threshold .th-btn{{display:flex;align-items:center;justify-content:center;white-space:nowrap;gap:12px;padding:16px 30px;font-family:{font};font-size:{btn_size};letter-spacing:{btn_track};text-transform:uppercase;text-decoration:none;transition:background 0.4s {EASE},color 0.4s {EASE},border-color 0.4s {EASE},gap 0.4s {EASE};}}
    #threshold .th-btn--solid{{background:#D6C2A8;color:#3A2D25;border:1px solid #D6C2A8;}}
    #threshold .th-btn--solid:hover,#threshold .th-btn--solid:focus-visible{{background:#F5F2ED;border-color:#F5F2ED;gap:18px;}}
    #threshold .th-btn--line{{color:#F5F2ED;border:1px solid rgba(245,242,237,0.55);}}
    #threshold .th-btn--line:hover,#threshold .th-btn--line:focus-visible{{background:#F5F2ED;border-color:#F5F2ED;color:#3A2D25;}}
    #threshold .th-cap{{position:absolute;top:clamp(18px,2vw,28px);inset-inline-end:clamp(18px,2vw,28px);font-family:{font};font-size:{'12px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.18em'};text-transform:uppercase;color:rgba(245,242,237,0.75);opacity:var(--e,0);}}
    /* studio horizon: full-bleed band resting on the section's bottom edge */
    #threshold .th-band{{--side:clamp(24px,5vw,80px);position:relative;container-type:inline-size;overflow:hidden;display:grid;margin:clamp(64px,8vw,100px) calc(var(--side) * -1) 0;background:#3A2D25;}}
    #threshold .th-grid{{--out:max(var(--side),calc((100cqw - 1280px) / 2));display:grid;grid-template-columns:minmax(0,1.3fr) repeat(3,minmax(0,1fr));width:calc(100cqw - var(--out) * 2);margin-inline:auto;}}
    #threshold .th-band::before{{content:"";position:absolute;top:0;inset-inline:0;height:1px;background:rgba(214,194,168,0.3);transform:scaleX(0);transform-origin:{'100%' if ar else '0%'} 50%;transition:transform 1.2s {EASE};z-index:2;}}
    #threshold .th-band.is-in::before{{transform:scaleX(1);}}
    #threshold .th-cell{{position:relative;min-width:0;display:flex;flex-direction:column;justify-content:space-between;gap:clamp(40px,4.4vw,72px);min-height:clamp(250px,21vw,330px);padding:clamp(28px,2.8vw,44px) clamp(20px,2.2vw,36px);text-decoration:none;color:inherit;opacity:0;transform:translateY(24px);transition:opacity 0.8s {EASE},transform 0.8s {EASE};}}
    #threshold .th-cell:first-child{{padding-inline-start:0;}}
    #threshold .th-cell:last-child{{padding-inline-end:0;}}
    #threshold .th-cell+.th-cell{{border-inline-start:1px solid rgba(214,194,168,0.16);}}
    #threshold .th-band.is-in .th-cell{{opacity:1;transform:none;}}
    #threshold .th-band.is-in .th-cell:nth-child(2){{transition-delay:0.1s;}}
    #threshold .th-band.is-in .th-cell:nth-child(3){{transition-delay:0.2s;}}
    #threshold .th-band.is-in .th-cell:nth-child(4){{transition-delay:0.3s;}}
    #threshold .th-cell::before{{content:"";position:absolute;inset:0;background:#5B4636;transform:scaleY(0);transform-origin:50% 100%;transition:transform 0.7s {EASE};}}
    #threshold .th-cell::after{{content:"";position:absolute;top:0;inset-inline:0;height:2px;background:#D6C2A8;transform:scaleX(0);transform-origin:{'100%' if ar else '0%'} 50%;transition:transform 0.7s {EASE};z-index:1;}}
    #threshold .th-cell:first-child::before,#threshold .th-cell:first-child::after{{inset-inline-start:calc(var(--out) * -1);}}
    #threshold .th-cell:last-child::before,#threshold .th-cell:last-child::after{{inset-inline-end:calc(var(--out) * -1);}}
    #threshold a.th-cell:hover::before,#threshold a.th-cell:focus-visible::before{{transform:scaleY(1);}}
    #threshold a.th-cell:hover::after,#threshold a.th-cell:focus-visible::after{{transform:scaleX(1);}}
    #threshold a.th-cell:focus-visible{{outline:none;}}
    #threshold .th-top,#threshold .th-txt{{position:relative;z-index:1;}}
    #threshold .th-top{{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:44px;}}
    #threshold .th-k{{display:flex;align-items:center;gap:14px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#D6C2A8;}}
    #threshold .th-n{{font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.2em;color:rgba(214,194,168,0.6);}}
    #threshold .th-n::after{{content:"";display:inline-block;width:22px;height:1px;margin-inline-start:14px;vertical-align:middle;background:rgba(214,194,168,0.4);}}
    #threshold .th-go{{flex:none;display:grid;place-items:center;width:44px;height:44px;border:1px solid rgba(214,194,168,0.35);color:#F5F2ED;transition:background 0.5s {EASE},border-color 0.5s {EASE},color 0.5s {EASE};}}
    #threshold .th-go svg{{transform:{'scaleX(-1)' if ar else 'none'};transition:transform 0.5s {EASE};}}
    #threshold a.th-cell:hover .th-go,#threshold a.th-cell:focus-visible .th-go{{background:#D6C2A8;border-color:#D6C2A8;color:#1E1610;}}
    #threshold a.th-cell:hover .th-go svg,#threshold a.th-cell:focus-visible .th-go svg{{transform:{'scaleX(-1) ' if ar else ''}translate(2px,-2px);}}
    #threshold .th-v{{display:block;font-family:{font};font-size:clamp(19px,1.7vw,24px);line-height:1.25;color:#F5F2ED;overflow-wrap:anywhere;}}
    #threshold .th-s{{display:block;margin-top:12px;font-family:{font};font-size:{'13px' if ar else '12px'};color:rgba(245,242,237,0.55);}}
    #threshold .th-map{{position:absolute;top:0;bottom:0;inset-inline-start:calc(var(--out) * -1);inset-inline-end:0;overflow:hidden;pointer-events:none;}}
    #threshold .th-map-a{{position:absolute;top:29%;inset-inline-end:max(14%,min({'240px' if ar else '210px'},calc(100% - 190px)));width:0;height:0;}}
    #threshold .th-map-z{{position:absolute;left:-720px;top:-420px;width:1440px;height:840px;opacity:0;transform:scale(1.08);transition:opacity 1.6s {EASE},transform 2.4s {EASE};}}
    #threshold .th-map img{{position:absolute;inset:0;width:100%;height:100%;max-width:none;opacity:0.42;transition:opacity 0.9s {EASE};}}
    #threshold .th-road{{position:absolute;white-space:nowrap;font-family:{font};font-size:{'10px' if ar else '7.5px'};letter-spacing:{'normal' if ar else '0.18em'};text-transform:uppercase;color:rgba(214,194,168,0.72);text-shadow:0 0 3px #3A2D25,0 0 6px #3A2D25;}}
    #threshold .th-band.is-in .th-map-z{{opacity:1;transform:scale(1);}}
    #threshold a.th-cell--map:hover .th-map-z,#threshold a.th-cell--map:focus-visible .th-map-z{{transform:scale(1.05);transition-duration:0.9s,1.4s;}}
    #threshold a.th-cell--map:hover .th-map img,#threshold a.th-cell--map:focus-visible .th-map img{{opacity:0.8;}}
    #threshold .th-pin{{position:absolute;left:-5px;top:-5px;width:10px;height:10px;background:#D6C2A8;}}
    #threshold .th-pin::before,#threshold .th-pin::after{{content:"";position:absolute;inset:-1px;border:1px solid #D6C2A8;animation:th-ping 2.8s {EASE} infinite;}}
    #threshold .th-pin::after{{animation-delay:1.4s;}}
    @keyframes th-ping{{from{{transform:scale(1);opacity:0.9;}}to{{transform:scale(4.2);opacity:0;}}}}
    #threshold .th-tag{{position:absolute;top:-14px;right:18px;white-space:nowrap;padding:7px 10px;background:#1E1610;font-family:{font};font-size:{'12px' if ar else '9px'};letter-spacing:{track};text-transform:uppercase;color:#D6C2A8;}}
    #threshold .th-osm{{position:absolute;bottom:10px;inset-inline-end:14px;z-index:1;font-family:{font};font-size:{'10px' if ar else '9px'};color:rgba(214,194,168,0.4);}}
    #threshold .th-cell--map::before{{display:none;}}
    #threshold .th-cell--map .th-s{{max-width:30ch;}}
    #threshold .th-ico{{position:absolute;inset:0;overflow:hidden;pointer-events:none;}}
    #threshold .th-ico svg{{position:absolute;bottom:-16%;inset-inline-end:-9%;width:clamp(150px,15vw,232px);height:auto;color:#D6C2A8;opacity:0.07;transform:rotate({'8deg' if ar else '-8deg'});transition:opacity 0.8s {EASE},transform 1.1s {EASE};}}
    #threshold a.th-cell:hover .th-ico svg,#threshold a.th-cell:focus-visible .th-ico svg{{opacity:0.13;transform:rotate(0deg) translateY(-8px);}}
    #threshold .th-time{{display:block;text-align:{'right' if ar else 'left'};font-family:'Lama Sans',sans-serif;font-size:clamp(46px,5.4vw,80px);line-height:0.9;letter-spacing:-0.02em;font-variant-numeric:tabular-nums;color:#F5F2ED;}}
    #threshold .th-day{{display:flex;align-items:center;gap:12px;margin-top:clamp(18px,1.8vw,26px);font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.16em;color:rgba(214,194,168,0.6);}}
    #threshold .th-day i{{position:relative;flex:1;height:1px;background:rgba(214,194,168,0.22);}}
    #threshold .th-day i::before{{content:"";position:absolute;top:0;bottom:0;inset-inline-start:0;width:calc(var(--day,0) * 100%);background:#D6C2A8;}}
    #threshold .th-day b{{position:absolute;top:-3px;inset-inline-start:calc(var(--day,0) * 100% - 3px);width:7px;height:7px;background:#D6C2A8;}}
    @media(min-width:1101px) and (max-width:1279px){{
      #threshold .th-road--2{{display:none;}}
    }}
    @media(max-width:1100px){{
      #threshold .th-grid{{--out:0px;width:100%;grid-template-columns:repeat(2,minmax(0,1fr));}}
      #threshold .th-cell,#threshold .th-cell:first-child,#threshold .th-cell:last-child{{padding-inline:var(--side);}}
      #threshold .th-cell:nth-child(3){{border-inline-start:none;}}
      #threshold .th-cell:nth-child(n+3){{border-top:1px solid rgba(214,194,168,0.16);}}
{'      #threshold .th-road--2{display:none;}' + chr(10) if ar else ''}    }}
    @media(max-width:900px){{
      #threshold .th-stage{{height:clamp(520px,82vh,680px);}}
      #threshold .th-btn{{padding:15px 22px;}}
    }}
    @media(max-width:600px){{
      #threshold .th-copy{{align-items:stretch;}}
      #threshold .th-ctas{{display:grid;grid-template-columns:1fr;width:100%;}}
      #threshold .th-grid{{grid-template-columns:1fr;}}
      #threshold .th-cell{{min-height:0;gap:32px;}}
      #threshold .th-cell--map{{min-height:340px;}}
      #threshold .th-ico svg{{width:136px;bottom:-22%;}}
      #threshold .th-road--2{{display:none;}}
      #threshold .th-map-a{{top:30%;}}
      #threshold .th-cell+.th-cell{{border-inline-start:none;border-top:1px solid rgba(214,194,168,0.16);}}
    }}
    @media(prefers-reduced-motion:reduce){{
      #threshold *{{transition:none!important;}}
      #threshold .th-pin::before,#threshold .th-pin::after{{animation:none;opacity:0;}}
      #threshold .th-map-z{{opacity:1;transform:none;}}
      #threshold .th-cell{{opacity:1;transform:none;}}
      #threshold .th-band::before{{transform:none;}}
    }}
  </style>
  <div class="th-wrap">
    <div class="th-label"><i></i>{c['label']}<i></i></div>
    <div class="th-stage" data-th-stage>
      <span class="th-ghost" aria-hidden="true"></span>
      <div class="th-door">
        <img src="uploads/{IMG}-1920.webp" srcset="{srcset}" sizes="100vw" alt="{c['alt']}" width="1920" height="1071" loading="lazy" decoding="async">
        <span class="th-tint" aria-hidden="true"></span>
        <span class="th-cap" aria-hidden="true">{c['cap']}</span>
        <div class="th-copy">
          <h2 class="th-h2">{c['h2']}</h2>
          <p class="th-body">{c['body']}</p>
          <div class="th-ctas">
            <a class="th-btn th-btn--solid" href="{c['pre']}/contact">{c['cta1']}{arrow}</a>
            <a class="th-btn th-btn--line" href="{c['pre']}/projects">{c['cta2']}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="th-band" role="group" aria-label="{c['plate']}" data-th-info>
    <div class="th-grid">
    <a class="th-cell th-cell--map" href="https://www.google.com/maps?cid=2079283542092448688" target="_blank" rel="noopener" aria-label="{c['maps']}"><span class="th-map" aria-hidden="true"><span class="th-map-a"><span class="th-map-z"><img src="uploads/about-studio-map-riyadh.svg" alt="" width="2400" height="1400" loading="lazy" decoding="async">{roads}</span><span class="th-pin"></span><span class="th-tag" dir="{'rtl' if ar else 'ltr'}">{c['pin']}</span></span></span><div class="th-top"><span class="th-k"><span class="th-n">01</span>{c['hq']}</span><span class="th-go">{GO}</span></div><div class="th-txt"><span class="th-time" dir="ltr" data-th-time>--:--</span><span class="th-day" dir="ltr" aria-hidden="true" data-th-day><span>00</span><i><b></b></i><span>24</span></span><span class="th-s">{c['addr']}</span></div><span class="th-osm">{c['osm']}</span></a>
    <a class="th-cell" href="tel:+966580330627">{ico("phone")}<div class="th-top"><span class="th-k"><span class="th-n">02</span>{c['phone']}</span><span class="th-go">{GO}</span></div><div class="th-txt"><span class="th-v" dir="ltr">+966 58 033 0627</span><span class="th-s">{c['call']}</span></div></a>
    <a class="th-cell" href="mailto:info@furnishiq.net">{ico("mail")}<div class="th-top"><span class="th-k"><span class="th-n">03</span>{c['email']}</span><span class="th-go">{GO}</span></div><div class="th-txt"><span class="th-v" dir="ltr">info@furnishiq.net</span><span class="th-s">{c['write']}</span></div></a>
    <a class="th-cell" href="https://wa.me/966580330627" target="_blank" rel="noopener">{ico("wa")}<div class="th-top"><span class="th-k"><span class="th-n">04</span>{c['wa']}</span><span class="th-go">{GO}</span></div><div class="th-txt"><span class="th-v">{c['wa_txt']}</span><span class="th-s">{c['wa_sub']}</span></div></a>
    </div>
  </div>
</section>
"""


JS = """    // ── THRESHOLD: THE DOORWAY OPENS INTO THE SPACE ON SCROLL ────────────────
    {
      const th = document.querySelector('[data-threshold]');
      if (th) {
        const stage = th.querySelector('[data-th-stage]'), clock = th.querySelector('[data-th-time]');
        let ticking = false;
        const update = () => {
          ticking = false;
          const r = stage.getBoundingClientRect(), vh = window.innerHeight, W = stage.offsetWidth;
          const p = reduced ? 1 : Math.min(Math.max((vh - r.top) / (vh * 0.85), 0), 1);
          const e = p * p * (3 - 2 * p);
          const w0 = Math.min(W, Math.max(200, W * 0.34));
          const w = w0 + (W - w0) * e;
          th.style.setProperty('--w0', w0.toFixed(1) + 'px');
          th.style.setProperty('--w', w.toFixed(1) + 'px');
          th.style.setProperty('--r', ((w / 2) * (1 - e)).toFixed(1) + 'px');
          th.style.setProperty('--e', e.toFixed(4));
          th.classList.toggle('is-open', e > 0.82);
        };
        update();
        window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
        window.addEventListener('resize', update);
        // live Riyadh time, with the day track showing how far through the day it is
        if (clock) {
          const fmt = new Intl.DateTimeFormat('en-GB', { timeZone: 'Asia/Riyadh', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });
          const day = th.querySelector('[data-th-day]');
          const tick = () => {
            const t = fmt.format(new Date()); clock.textContent = t;
            const [h, m] = t.split(':').map(Number);
            if (day) day.style.setProperty('--day', ((h * 60 + m) / 1440).toFixed(4));
          };
          tick(); setInterval(tick, 30000);
        }
        // studio horizon: panels rise in once the band comes into view
        const info = th.querySelector('[data-th-info]');
        if (info) {
          if (reduced || !('IntersectionObserver' in window)) info.classList.add('is-in');
          else {
            const io = new IntersectionObserver((es) => { es.forEach((e) => { if (e.isIntersecting) { info.classList.add('is-in'); io.disconnect(); } }); }, { rootMargin: '0px 0px -12% 0px' });
            io.observe(info);
          }
        }
      }
    }

"""
MARK = "    // ── FADE-IN ON LOAD (lazy images)"

for path, lang in [("about-us.dc.html", "en"), ("about-us.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ STUDIO / CONTACT ━ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── THRESHOLD: THE DOORWAY"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

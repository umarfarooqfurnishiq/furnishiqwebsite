import re, math

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
C = {
    "en": dict(
        label="Our Story", h=["We saw a gap.", "We built FurnishIQ to close it."],
        k1="What clients were looking for", k2="What FurnishIQ delivers",
        s1="The market offered many design and construction solutions, yet discerning clients could not find spaces that reflected their", s2="FurnishIQ was established to close that gap with one integrated approach",
        needs=["Individuality", "Lifestyle", "Aspirations"], gives=["Design", "Build", "Manage"],
        p1="The market offered many design and construction solutions, yet discerning clients still could not find spaces that truly reflected <em>their individuality, lifestyle, and aspirations</em>.",
        p2="FurnishIQ was established to close that gap, delivering personalised, high-quality environments through <em>one integrated design, build, and management approach</em>.",
        gap_l="The market", gap_r="What clients needed",
        g_label="Part of Arsan Global", g_h=["One group.", "Four regions.", "Six sectors."],
        g_p1="FurnishIQ is the Design, Build, and Management subsidiary of Arsan Global, a diversified international holding group headquartered in the Kingdom of Saudi Arabia and established in 2007.",
        g_p2="Backed by the group's financial strength, international network, and multidisciplinary expertise, FurnishIQ combines creative vision, engineering excellence, and disciplined execution.",
        facts=[("Est.", "2007"), ("Headquarters", "Riyadh")],
        regions=["Middle East", "Europe", "North America", "Asia"],
        sectors=["Logistics", "Technology", "Real Estate", "Trading", "Business Consulting", "Integrated Projects"],
        core=["ARSAN", "GLOBAL", "EST. 2007"], fiq="FurnishIQ", fiq_sub="Design · Build · Manage",
        strengths=[("Integrated Ecosystem", "Access to a coordinated network of specialists and experts."),
                   ("Cross-Sector Expertise", "Knowledge built from experience across multiple sectors and geographies."),
                   ("Committed Partnership", "We build businesses, not transactions."),
                   ("Global Perspective", "Delivering solutions across markets with consistent excellence.")],
    ),
    "ar": dict(
        label="قصتنا", h=["رأينا فجوة.", "فأسسنا فيرنيش آي كيو لسدّها."],
        k1="ما كان يبحث عنه العملاء", k2="ما تقدمه فيرنيش آي كيو",
        s1="قدّم السوق العديد من حلول التصميم والبناء، لكن العملاء المميزين لم يجدوا مساحات تعكس", s2="تأسست فيرنيش آي كيو لسد هذه الفجوة عبر نهج واحد متكامل",
        needs=["فرديتهم", "أسلوب حياتهم", "طموحاتهم"], gives=["التصميم", "التنفيذ", "الإدارة"],
        p1="قدّم السوق العديد من حلول التصميم والبناء، لكن العملاء المميزين لم يجدوا بعد مساحات تعكس حقاً <em>فرديتهم وأسلوب حياتهم وطموحاتهم</em>.",
        p2="تأسست فيرنيش آي كيو لسد هذه الفجوة، من خلال تقديم بيئات مخصصة وعالية الجودة عبر <em>نهج متكامل للتصميم والتنفيذ والإدارة</em>.",
        gap_l="السوق", gap_r="ما يحتاجه العملاء",
        g_label="جزء من ارسان العالمية", g_h=["مجموعة واحدة.", "أربع مناطق.", "ستة قطاعات."],
        g_p1="فيرنيش آي كيو هي الذراع المتخصصة في التصميم والتنفيذ والإدارة التابعة لمجموعة ارسان العالمية، وهي مجموعة قابضة دولية متنوعة مقرها الرئيسي في المملكة العربية السعودية وتأسست عام 2007.",
        g_p2="بدعم من القوة المالية والشبكة الدولية والخبرات متعددة التخصصات للمجموعة، تجمع فيرنيش آي كيو بين الرؤية الإبداعية والتميز الهندسي والتنفيذ المنضبط.",
        facts=[("التأسيس", "2007"), ("المقر الرئيسي", "الرياض")],
        regions=["الشرق الأوسط", "أوروبا", "أمريكا الشمالية", "آسيا"],
        sectors=["الخدمات اللوجستية", "التقنية", "العقارات", "التجارة", "الاستشارات الإدارية", "المشاريع المتكاملة"],
        core=["ARSAN", "GLOBAL", "EST. 2007"], fiq="FurnishIQ", fiq_sub="تصميم · تنفيذ · إدارة",
        strengths=[("منظومة متكاملة", "الوصول إلى شبكة منسقة من المتخصصين والخبراء."),
                   ("خبرة متعددة القطاعات", "معرفة مبنية على خبرة عبر قطاعات وجغرافيات متعددة."),
                   ("شراكة ملتزمة", "نحن نبني أعمالاً، لا صفقات."),
                   ("منظور عالمي", "تقديم حلول عبر الأسواق بتميز ثابت.")],
    ),
}


def orbit(lang, c):
    ar = lang == "ar"
    tfont = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    cx = cy = 320
    R, r = 230, 128
    nodes, labels = "", ""
    for i, name in enumerate(c["sectors"]):
        a = math.radians(-90 + i * 60 + 30)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        lx, ly = cx + (R + 26) * math.cos(a), cy + (R + 26) * math.sin(a)
        anchor = "start" if math.cos(a) > 0.2 else ("end" if math.cos(a) < -0.2 else "middle")
        dy = 5 if abs(math.sin(a)) < 0.6 else (18 if math.sin(a) > 0 else -10)
        nodes += f'<g class="ob-node" style="--d:{0.9 + i * 0.12:.2f}s"><line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" class="ob-spoke"/><circle cx="{x:.1f}" cy="{y:.1f}" r="6" class="ob-dot"/></g>'
        labels += f'<text x="{lx:.1f}" y="{ly + dy:.1f}" text-anchor="{anchor}" class="ob-label" style="--d:{1.0 + i * 0.12:.2f}s" font-family="{tfont}">{name}</text>'
    # FurnishIQ on the inner ring
    a = math.radians(-90 + 0)
    fx, fy = cx + r * math.cos(a), cy + r * math.sin(a)
    fiq = (f'<g class="ob-fiq"><line x1="{cx}" y1="{cy}" x2="{fx:.1f}" y2="{fy:.1f}" class="ob-fiq-line"/>'
           f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="16" class="ob-fiq-halo"/><circle cx="{fx:.1f}" cy="{fy:.1f}" r="7" class="ob-fiq-dot"/>'
           f'<text x="{fx + 26:.1f}" y="{fy - 4:.1f}" class="ob-fiq-t" font-family="\'Lama Sans\',sans-serif">{c["fiq"]}</text>'
           f'<text x="{fx + 26:.1f}" y="{fy + 14:.1f}" class="ob-fiq-s" font-family="{tfont}">{c["fiq_sub"]}</text></g>')
    core = (f'<circle cx="{cx}" cy="{cy}" r="62" class="ob-core"/>'
            f'<text x="{cx}" y="{cy - 6}" text-anchor="middle" class="ob-core-t">{c["core"][0]}</text>'
            f'<text x="{cx}" y="{cy + 14}" text-anchor="middle" class="ob-core-s">{c["core"][1]}</text>'
            f'<text x="{cx}" y="{cy + 32}" text-anchor="middle" class="ob-core-y">{c["core"][2]}</text>')
    return f"""<svg class="ob-svg" viewBox="-40 -10 720 660" role="img" aria-label="Arsan Global and its sectors" direction="ltr">
          <circle cx="{cx}" cy="{cy}" r="{R + 62}" class="ob-ring ob-ring--outer" pathLength="1"/>
          <circle cx="{cx}" cy="{cy}" r="{R}" class="ob-ring" pathLength="1"/>
          <circle cx="{cx}" cy="{cy}" r="{r}" class="ob-ring ob-ring--inner" pathLength="1"/>
          {nodes}{fiq}{core}{labels}
        </svg>"""


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    strengths = "".join(f"""
      <div class="st-item" style="--i:{i};"><span class="st-num" dir="ltr">0{i + 1}</span><h3 class="st-t">{t}</h3><p class="st-d">{d}</p></div>""" for i, (t, d) in enumerate(c["strengths"]))
    facts = "".join(f'<div class="gp-fact"><span>{k}</span><strong>{v}</strong></div>' for k, v in c["facts"])
    regions = "".join(f"<li>{r}</li>" for r in c["regions"])
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ OUR STORY ━━━━━ -->
<section id="our-story" data-story{' dir="rtl"' if ar else ''} style="position:relative;background:#1E1610;color:#F5F2ED;padding:clamp(64px,8vw,100px) clamp(24px,5vw,80px);overflow:hidden;">
  <style>
    #our-story .sy-wrap{{max-width:1280px;margin:0 auto;position:relative;}}
    #our-story.is-in .sy-draw .ad{{stroke-dashoffset:0;transform:none;}}
    #our-story .sy-wrap{{z-index:1;}}
    #our-story .sy-year{{position:absolute;top:clamp(-20px,-1vw,0px);inset-inline-end:0;width:clamp(360px,46vw,820px);height:auto;pointer-events:none;overflow:visible;}}
    #our-story .sy-year .yr-base{{fill:none;stroke:rgba(214,194,168,0.13);stroke-width:1.2;stroke-linejoin:round;stroke-linecap:round;}}
    #our-story .sy-year .yr-spark{{fill:none;stroke:#FFF4E2;stroke-width:3.2;stroke-linecap:round;stroke-dasharray:0.0004 0.9996;stroke-dashoffset:0;opacity:0.42;filter:drop-shadow(0 0 2px rgba(255,244,226,0.9)) drop-shadow(0 0 6px rgba(214,194,168,0.5));animation:yr-run 16s linear infinite,yr-twinkle 1.8s ease-in-out infinite;}}
    @keyframes yr-twinkle{{0%,100%{{opacity:0.42}}50%{{opacity:0.22}}}}
    @keyframes yr-run{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-1}}}}
    #our-story .sy-label{{display:flex;align-items:center;gap:16px;margin-bottom:26px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#D6C2A8;}}
    #our-story .sy-label i{{display:block;width:32px;height:1px;background:#D6C2A8;}}
    #our-story .sy-h{{font-family:{font};font-size:clamp(34px,4.4vw,74px);font-weight:500;line-height:{'1.3' if ar else '1.04'};letter-spacing:{'normal' if ar else '-0.03em'};margin:0;max-width:1000px;}}
    #our-story .sy-h{{color:#FFFFFF;max-width:1240px;}}
    #our-story .sy-h .l2{{color:#D6C2A8;}}
    #our-story .sy-gap{{position:relative;height:56px;margin:clamp(40px,5vw,64px) 0;}}
    #our-story .sy-gap i{{position:absolute;top:27px;height:1px;width:50%;background:rgba(214,194,168,0.55);transition:transform 1.6s {EASE} 0.3s;}}
    #our-story .sy-gap i:nth-of-type(1){{inset-inline-start:0;transform:translateX({'18%' if ar else '-18%'});}}
    #our-story .sy-gap i:nth-of-type(2){{inset-inline-end:0;transform:translateX({'-18%' if ar else '18%'});}}
    #our-story .sy-gap b{{position:absolute;left:50%;top:21px;width:13px;height:13px;margin-left:-6.5px;border-radius:50%;background:#D6C2A8;box-shadow:0 0 0 6px rgba(214,194,168,0.14);transform:scale(0);transition:transform 0.7s {EASE} 1.7s;}}
    #our-story .sy-gap span{{position:absolute;top:0;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:rgba(214,194,168,0.6);transition:opacity 0.8s {EASE} 1.4s;}}
    #our-story .sy-gap span:nth-of-type(1){{inset-inline-start:0;}}
    #our-story .sy-gap span:nth-of-type(2){{inset-inline-end:0;}}
    #our-story.is-in .sy-gap i{{transform:none;}}
    #our-story.is-in .sy-gap b{{transform:scale(1);}}
    #our-story .sy-cols{{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);gap:clamp(28px,4vw,72px);align-items:center;}}
    #our-story .mp{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);column-gap:clamp(40px,8vw,160px);row-gap:clamp(28px,3vw,44px);}}
    #our-story .mp-head--r{{text-align:end;}}
    #our-story .mp-k{{display:block;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#D6C2A8;margin-bottom:12px;}}
    #our-story .mp-s{{font-family:{font};font-size:clamp(15px,1.15vw,17px);line-height:1.75;color:rgba(245,242,237,0.6);margin:0;max-width:440px;}}
    #our-story .mp-head--r .mp-s{{margin-inline-start:auto;}}
    #our-story .mp-rows{{grid-column:1/-1;display:flex;flex-direction:column;}}
    #our-story .mp-row{{display:grid;grid-template-columns:auto minmax(40px,1fr) auto;align-items:center;gap:clamp(16px,2vw,32px);padding:clamp(12px,1.4vw,20px) 0;border-bottom:1px solid rgba(214,194,168,0.14);}}
    #our-story .mp-need,#our-story .mp-give{{font-family:{font};font-size:clamp(30px,4.4vw,76px);font-weight:500;line-height:1.05;letter-spacing:{'normal' if ar else '-0.03em'};}}
    #our-story .mp-need{{color:transparent;-webkit-text-stroke:1px rgba(214,194,168,0.5);transition:color 0.9s {EASE} calc(1.1s + var(--i) * 0.35s),-webkit-text-stroke-color 0.9s {EASE} calc(1.1s + var(--i) * 0.35s);}}
    #our-story .mp-give{{color:#D6C2A8;opacity:0;transform:translateX({'-24px' if ar else '24px'});transition:opacity 0.8s {EASE} calc(0.8s + var(--i) * 0.35s),transform 0.8s {EASE} calc(0.8s + var(--i) * 0.35s);}}
    #our-story .mp-link{{position:relative;height:1px;}}
    #our-story .mp-link i{{position:absolute;inset:0;background:rgba(214,194,168,0.55);transform:scaleX(0);transform-origin:{'right' if ar else 'left'};transition:transform 0.9s {EASE} calc(0.3s + var(--i) * 0.35s);}}
    #our-story .mp-link::before,#our-story .mp-link::after{{content:"";position:absolute;top:-3px;width:7px;height:7px;border-radius:50%;background:#D6C2A8;opacity:0;transition:opacity 0.4s {EASE};}}
    #our-story .mp-link::before{{inset-inline-start:0;transition-delay:calc(0.3s + var(--i) * 0.35s);}}
    #our-story .mp-link::after{{inset-inline-end:0;transition-delay:calc(1.1s + var(--i) * 0.35s);}}
    #our-story .mp.is-in .mp-need{{color:#F5F2ED;-webkit-text-stroke-color:#F5F2ED;}}
    #our-story .mp.is-in .mp-give{{opacity:1;transform:none;}}
    #our-story .mp.is-in .mp-link i{{transform:scaleX(1);}}
    #our-story .mp.is-in .mp-link::before,#our-story .mp.is-in .mp-link::after{{opacity:1;}}
    #our-story .mp-row:hover .mp-link i{{background:#D6C2A8;}}
    #our-story .sy-k{{display:flex;align-items:center;gap:14px;margin-bottom:20px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:rgba(214,194,168,0.7);}}
    #our-story .sy-k b{{font-family:'Lama Sans',sans-serif;font-weight:500;font-size:11px;letter-spacing:0.2em;color:#D6C2A8;padding:6px 9px;border:1px solid rgba(214,194,168,0.35);}}
    #our-story .sy-big{{font-family:{font};font-size:clamp(19px,1.7vw,27px);line-height:1.55;letter-spacing:{'normal' if ar else '-0.005em'};color:rgba(245,242,237,0.62);margin:0;}}
    #our-story .sy-big em{{font-style:normal;color:#F5F2ED;border-bottom:1px solid rgba(214,194,168,0.45);}}
    #our-story .sy-col:last-child .sy-big em{{color:#D6C2A8;}}
    #our-story .sy-arrow{{display:block;width:clamp(48px,5vw,88px);height:1px;background:rgba(214,194,168,0.5);position:relative;{'transform:scaleX(-1);' if ar else ''}}}
    #our-story .sy-arrow::after{{content:"";position:absolute;right:0;top:-4px;width:9px;height:9px;border-top:1px solid rgba(214,194,168,0.7);border-right:1px solid rgba(214,194,168,0.7);transform:rotate(45deg);}}
    #our-story .sy-p{{font-family:{font};font-size:clamp(15px,1.15vw,17px);line-height:1.85;color:rgba(245,242,237,0.72);margin:0;}}
        #our-story .sy-elev{{position:absolute;left:0;bottom:0;width:100%;height:auto;z-index:0;pointer-events:none;}}
    #our-story .sy-elev .ad{{fill:none;stroke:rgba(214,194,168,0.16);stroke-width:1;vector-effect:non-scaling-stroke;stroke-dasharray:1;stroke-dashoffset:1;transform:translateY(18px);transition:stroke-dashoffset 2.2s {EASE} var(--d),transform 1.8s {EASE} var(--d);}}
    #our-story .sy-elev .ad-dim{{stroke:rgba(214,194,168,0.12);}}
    #our-story .sy-elev .ad-faint{{stroke:rgba(214,194,168,0.07);}}
    #our-story .sy-elev.is-in .ad{{stroke-dashoffset:0;transform:none;}}
    #our-story .gp{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,5fr);gap:clamp(40px,5vw,96px);align-items:center;margin-top:clamp(64px,8vw,100px);}}
    #our-story .ob-svg{{width:100%;height:auto;display:block;overflow:visible;}}
    #our-story .ob-ring{{fill:none;stroke:rgba(214,194,168,0.28);stroke-width:1;stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset 1.8s {EASE} 0.2s;}}
    #our-story .ob-ring--outer{{stroke:rgba(214,194,168,0.12);stroke-dasharray:0.004 0.008;stroke-dashoffset:0;opacity:0;transition:opacity 1s {EASE} 0.4s;transform-origin:320px 320px;animation:ob-spin 90s linear infinite;}}
    #our-story .ob-ring--inner{{stroke:rgba(214,194,168,0.2);}}
    @keyframes ob-spin{{to{{transform:rotate(360deg)}}}}
    #our-story.is-in .ob-ring{{stroke-dashoffset:0;}}
    #our-story.is-in .ob-ring--outer{{opacity:1;}}
    #our-story .ob-spoke{{stroke:rgba(214,194,168,0.12);stroke-width:1;}}
    #our-story .ob-dot{{fill:#1E1610;stroke:#D6C2A8;stroke-width:1.2;}}
    #our-story .ob-node,#our-story .ob-label{{opacity:0;transition:opacity 0.7s {EASE} var(--d);}}
    #our-story.is-in .ob-node,#our-story.is-in .ob-label{{opacity:1;}}
    #our-story .ob-label{{fill:rgba(245,242,237,0.78);font-size:{'17' if ar else '15'}px;}}
    #our-story .ob-core{{fill:#2B211B;stroke:#D6C2A8;stroke-width:1;}}
    #our-story .ob-core-t{{fill:#FFFFFF;font-family:'Lama Sans',sans-serif;font-size:20px;letter-spacing:2px;}}
    #our-story .ob-core-s{{fill:#D6C2A8;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:4px;}}
    #our-story .ob-core-y{{fill:rgba(214,194,168,0.55);font-family:'Lama Sans',sans-serif;font-size:9px;letter-spacing:2px;}}
    #our-story .ob-fiq{{opacity:0;transition:opacity 0.9s {EASE} 1.9s;}}
    #our-story.is-in .ob-fiq{{opacity:1;}}
    #our-story .ob-fiq-line{{stroke:#D6C2A8;stroke-width:1.2;}}
    #our-story .ob-fiq-halo{{fill:rgba(214,194,168,0.14);stroke:rgba(214,194,168,0.5);stroke-width:1;transform-origin:center;transform-box:fill-box;animation:ob-pulse 3s {EASE} infinite;}}
    @keyframes ob-pulse{{0%,100%{{transform:scale(0.85);opacity:0.6}}50%{{transform:scale(1.25);opacity:1}}}}
    #our-story .ob-fiq-dot{{fill:#D6C2A8;}}
    #our-story .ob-fiq-t{{fill:#FFFFFF;font-size:18px;}}
    #our-story .ob-fiq-s{{fill:#D6C2A8;font-size:{'13' if ar else '11'}px;}}
    #our-story .gp-h{{font-family:{font};font-size:clamp(32px,3.6vw,60px);font-weight:500;line-height:{'1.3' if ar else '1.04'};letter-spacing:{'normal' if ar else '-0.025em'};margin:0;}}
    #our-story .gp-h{{color:#FFFFFF;}}
    #our-story .gp-h .l2{{color:rgba(245,242,237,0.6);}}
    #our-story .gp-h .l3{{color:#D6C2A8;}}
    #our-story .gp .sy-p{{margin-top:22px;}}
    #our-story .gp-facts{{display:flex;gap:clamp(24px,3vw,48px);margin-top:32px;padding-top:24px;border-top:1px solid rgba(214,194,168,0.16);}}
    #our-story .gp-fact{{display:flex;flex-direction:column;gap:6px;}}
    #our-story .gp-fact span{{font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:rgba(214,194,168,0.6);}}
    #our-story .gp-fact strong{{font-family:{font};font-weight:500;font-size:clamp(22px,2vw,30px);color:#FFFFFF;}}
    #our-story .gp-regions{{list-style:none;margin:24px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:10px;}}
    #our-story .gp-regions li{{font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;color:#D6C2A8;padding:9px 14px;border:1px solid rgba(214,194,168,0.3);}}
    #our-story .st{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));margin-top:clamp(64px,8vw,112px);border-top:1px solid rgba(214,194,168,0.3);border-bottom:1px solid rgba(214,194,168,0.14);}}
    #our-story .st-item{{position:relative;display:flex;flex-direction:column;padding:clamp(28px,3vw,44px) clamp(20px,2.2vw,36px) clamp(32px,3.4vw,48px);border-inline-start:1px solid rgba(214,194,168,0.12);opacity:0;transform:translateY(16px);transition:opacity 0.8s {EASE} calc(0.3s + var(--i) * 0.12s),transform 0.8s {EASE} calc(0.3s + var(--i) * 0.12s),background 0.5s {EASE};}}
    #our-story .st-item:first-child{{border-inline-start:none;}}
    #our-story .st-item::before{{content:"";position:absolute;top:-1px;inset-inline:0;height:2px;background:#D6C2A8;transform:scaleX(0);transform-origin:{'right' if ar else 'left'};transition:transform 0.6s {EASE};}}
    #our-story .st-item:hover{{background:rgba(214,194,168,0.04);}}
    #our-story .st-item:hover::before{{transform:scaleX(1);}}
    #our-story .st.is-in .st-item{{opacity:1;transform:none;}}
    #our-story .st-num{{display:block;align-self:flex-end;font-family:'Lama Sans',sans-serif;font-size:clamp(44px,4vw,72px);line-height:0.9;letter-spacing:-0.03em;color:rgba(214,194,168,0.2);margin-bottom:clamp(24px,2.6vw,36px);transition:color 0.5s {EASE};}}
    #our-story .st-item:hover .st-num{{color:rgba(214,194,168,0.45);}}
    #our-story .st-t{{font-family:{font};font-size:clamp(17px,1.35vw,21px);font-weight:500;line-height:1.3;color:#FFFFFF;margin:0;padding-top:16px;border-top:1px solid rgba(214,194,168,0.18);}}
    #our-story .st-d{{font-family:{font};font-size:{'15px' if ar else '14px'};line-height:1.75;color:rgba(245,242,237,0.62);margin:10px 0 0;max-width:280px;}}
    @media(max-width:900px){{
      #our-story .sy-cols,#our-story .gp{{grid-template-columns:1fr;}}
      #our-story .mp{{grid-template-columns:1fr;}}
      #our-story .mp-head--r{{text-align:start;}}
      #our-story .mp-head--r .mp-s{{margin-inline-start:0;}}
      #our-story .mp-need,#our-story .mp-give{{font-size:clamp(22px,6.4vw,34px);}}
      #our-story .sy-arrow{{transform:rotate({'-90deg' if ar else '90deg'});margin:0 0 0 20px;width:40px;}}
      #our-story .st{{grid-template-columns:1fr 1fr;row-gap:32px;}}
      #our-story .st-item:nth-child(3){{border-inline-start:none;}}
      #our-story .st-item:nth-child(n+3){{border-top:1px solid rgba(214,194,168,0.12);}}
      #our-story .st{{row-gap:0!important;}}
      #our-story .sy-gap span{{display:none;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      #our-story *{{transition:none!important;animation:none!important;}}
      #our-story .yr-spark{{display:none;}}
      }}
  </style>
  <div class="sy-wrap">
    <svg class="sy-year" viewBox="-30 20 1010 360" aria-hidden="true"><path class="yr-base" d="M70.9 32.5 L58.0 37.7 L45.6 44.5 L34.2 53.0 L28.9 57.8 L19.2 68.8 L11.1 81.4 L4.8 95.5 L2.4 103.0 L-0.9 119.0 L-2.0 135.2 L46.0 136.8 L47.5 120.5 L51.5 107.9 L57.5 97.8 L65.3 89.5 L71.5 85.0 L78.5 81.1 L90.2 76.8 L103.0 74.5 L117.0 74.2 L130.8 76.2 L142.8 80.4 L153.0 86.4 L161.4 93.9 L168.0 103.0 L172.7 113.4 L175.4 125.3 L175.9 138.1 L175.0 146.0 L173.4 153.4 L170.9 160.6 L165.7 171.4 L155.6 186.4 L138.0 206.5 L115.8 228.3 L-49.5 374.0 L784.4 374.0 L970.0 26.0 L726.0 26.0 L726.0 74.0 L890.0 74.0 L755.6 326.0 L666.0 326.0 L674.9 312.7 L685.9 291.2 L694.4 267.8 L700.2 243.0 L703.4 217.4 L703.9 191.3 L701.6 165.4 L698.6 148.6 L691.8 124.2 L682.5 101.4 L670.7 80.6 L661.5 68.2 L651.2 57.0 L645.7 51.9 L634.0 43.0 L621.4 35.8 L614.8 32.8 L601.2 28.5 L587.1 26.3 L580.0 26.0 L572.9 26.3 L558.8 28.5 L551.9 30.4 L538.6 35.8 L526.0 43.0 L514.3 51.9 L508.8 57.0 L498.5 68.2 L489.3 80.6 L481.2 94.2 L474.1 108.8 L468.2 124.2 L463.4 140.3 L460.0 155.8 L456.6 140.3 L451.8 124.2 L442.5 101.4 L430.7 80.6 L416.5 62.4 L405.7 51.9 L400.0 47.3 L387.8 39.1 L381.4 35.8 L368.1 30.4 L361.2 28.5 L347.1 26.3 L332.9 26.3 L325.8 27.1 L311.9 30.4 L305.2 32.8 L292.2 39.1 L286.0 43.0 L274.3 51.9 L268.8 57.0 L258.5 68.2 L245.1 87.3 L234.1 108.8 L228.2 124.2 L223.9 138.5 L223.8 126.5 L221.9 112.0 L218.3 98.1 L212.8 85.0 L209.5 78.8 L201.6 67.2 L192.2 56.7 L181.4 47.7 L169.4 40.0 L156.3 34.0 L142.3 29.6 L127.5 26.9 L112.0 26.0 L98.1 26.7 L84.4 28.9Z M340.0 326.0 L333.3 325.5 L326.5 323.8 L319.6 321.1 L312.7 317.1 L305.7 311.7 L298.9 305.1 L292.4 297.2 L286.3 288.0 L280.7 277.7 L275.8 266.4 L269.9 247.8 L267.0 234.6 L265.1 220.9 L264.0 200.0 L265.1 179.1 L267.0 165.4 L269.9 152.2 L275.8 133.6 L280.7 122.3 L286.3 112.0 L292.4 102.8 L298.9 94.9 L305.7 88.3 L312.7 82.9 L319.6 78.9 L326.5 76.2 L333.3 74.5 L340.0 74.0 L346.7 74.5 L353.5 76.2 L360.4 78.9 L367.3 82.9 L374.3 88.3 L381.1 94.9 L387.6 102.8 L393.7 112.0 L399.3 122.3 L404.2 133.6 L410.1 152.2 L413.0 165.4 L414.9 179.1 L416.0 200.0 L414.9 220.9 L413.0 234.6 L410.1 247.8 L404.2 266.4 L399.3 277.7 L393.7 288.0 L387.6 297.2 L381.1 305.1 L374.3 311.7 L367.3 317.1 L360.4 321.1 L353.5 323.8 L346.7 325.5Z M426.0 326.0 L434.9 312.7 L445.9 291.2 L454.4 267.8 L460.0 244.2 L465.6 267.8 L474.1 291.2 L485.1 312.7 L494.0 326.0Z M580.0 326.0 L573.3 325.5 L566.5 323.8 L559.6 321.1 L552.7 317.1 L545.7 311.7 L538.9 305.1 L532.4 297.2 L526.3 288.0 L520.7 277.7 L515.8 266.4 L509.9 247.8 L507.0 234.6 L505.1 220.9 L504.0 200.0 L505.1 179.1 L507.0 165.4 L509.9 152.2 L515.8 133.6 L520.7 122.3 L526.3 112.0 L532.4 102.8 L538.9 94.9 L545.7 88.3 L552.7 82.9 L559.6 78.9 L566.5 76.2 L573.3 74.5 L580.0 74.0 L586.7 74.5 L593.5 76.2 L600.4 78.9 L607.3 82.9 L614.3 88.3 L621.1 94.9 L627.6 102.8 L633.7 112.0 L639.3 122.3 L644.2 133.6 L650.1 152.2 L653.0 165.4 L654.9 179.1 L656.0 200.0 L654.9 220.9 L653.0 234.6 L650.1 247.8 L644.2 266.4 L639.3 277.7 L633.7 288.0 L627.6 297.2 L621.1 305.1 L614.3 311.7 L607.3 317.1 L600.4 321.1 L593.5 323.8 L586.7 325.5Z M217.5 173.2 L216.1 191.3 L216.6 217.4 L219.8 243.0 L223.4 259.7 L231.0 283.6 L237.5 298.6 L245.1 312.7 L254.0 326.0 L77.5 326.0 L148.2 263.7 L168.0 244.4 L181.4 230.3 L193.6 215.8 L204.3 200.5 L213.1 184.1Z"/><path class="yr-spark" pathLength="1" d="M70.9 32.5 L58.0 37.7 L45.6 44.5 L34.2 53.0 L28.9 57.8 L19.2 68.8 L11.1 81.4 L4.8 95.5 L2.4 103.0 L-0.9 119.0 L-2.0 135.2 L46.0 136.8 L47.5 120.5 L51.5 107.9 L57.5 97.8 L65.3 89.5 L71.5 85.0 L78.5 81.1 L90.2 76.8 L103.0 74.5 L117.0 74.2 L130.8 76.2 L142.8 80.4 L153.0 86.4 L161.4 93.9 L168.0 103.0 L172.7 113.4 L175.4 125.3 L175.9 138.1 L175.0 146.0 L173.4 153.4 L170.9 160.6 L165.7 171.4 L155.6 186.4 L138.0 206.5 L115.8 228.3 L-49.5 374.0 L784.4 374.0 L970.0 26.0 L726.0 26.0 L726.0 74.0 L890.0 74.0 L755.6 326.0 L666.0 326.0 L674.9 312.7 L685.9 291.2 L694.4 267.8 L700.2 243.0 L703.4 217.4 L703.9 191.3 L701.6 165.4 L698.6 148.6 L691.8 124.2 L682.5 101.4 L670.7 80.6 L661.5 68.2 L651.2 57.0 L645.7 51.9 L634.0 43.0 L621.4 35.8 L614.8 32.8 L601.2 28.5 L587.1 26.3 L580.0 26.0 L572.9 26.3 L558.8 28.5 L551.9 30.4 L538.6 35.8 L526.0 43.0 L514.3 51.9 L508.8 57.0 L498.5 68.2 L489.3 80.6 L481.2 94.2 L474.1 108.8 L468.2 124.2 L463.4 140.3 L460.0 155.8 L456.6 140.3 L451.8 124.2 L442.5 101.4 L430.7 80.6 L416.5 62.4 L405.7 51.9 L400.0 47.3 L387.8 39.1 L381.4 35.8 L368.1 30.4 L361.2 28.5 L347.1 26.3 L332.9 26.3 L325.8 27.1 L311.9 30.4 L305.2 32.8 L292.2 39.1 L286.0 43.0 L274.3 51.9 L268.8 57.0 L258.5 68.2 L245.1 87.3 L234.1 108.8 L228.2 124.2 L223.9 138.5 L223.8 126.5 L221.9 112.0 L218.3 98.1 L212.8 85.0 L209.5 78.8 L201.6 67.2 L192.2 56.7 L181.4 47.7 L169.4 40.0 L156.3 34.0 L142.3 29.6 L127.5 26.9 L112.0 26.0 L98.1 26.7 L84.4 28.9Z"/></svg>
    <div class="sy-label"><i></i>{c['label']}</div>
    <h2 class="sy-h"><span class="l1">{c['h'][0]}</span><br><span class="l2">{c['h'][1]}</span></h2>
    <div class="sy-gap" aria-hidden="true"><span>{c['gap_l']}</span><span>{c['gap_r']}</span><i></i><i></i><b></b></div>
    <div class="mp" data-map>
      <div class="mp-head"><span class="mp-k">{c['k1']}</span><p class="mp-s">{c['s1']}</p></div>
      <div class="mp-head mp-head--r"><span class="mp-k">{c['k2']}</span><p class="mp-s">{c['s2']}</p></div>
      <div class="mp-rows">{''.join(f'<div class="mp-row" style="--i:{i};"><span class="mp-need">{n}</span><span class="mp-link"><i></i></span><span class="mp-give">{g}</span></div>' for i, (n, g) in enumerate(zip(c['needs'], c['gives'])))}</div>
    </div>
    <div class="gp">
      <div>{orbit(lang, c)}</div>
      <div>
        <div class="sy-label"><i></i>{c['g_label']}</div>
        <h2 class="gp-h">{'<br>'.join(f'<span class="l{i + 1}">{t}</span>' for i, t in enumerate(c['g_h']))}</h2>
        <p class="sy-p">{c['g_p1']}</p>
        <p class="sy-p">{c['g_p2']}</p>
        <div class="gp-facts">{facts}</div>
        <ul class="gp-regions">{regions}</ul>
      </div>
    </div>
  </div>
  <svg class="sy-elev" viewBox="0 0 2560 231" preserveAspectRatio="xMidYMid meet" aria-hidden="true"><g><path class="ad" pathLength="1" style="--d:0.00s" d="M0 230H1280"/><path class="ad" pathLength="1" style="--d:0.00s" d="M40 230V120H250V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.25s" d="M40 120L53.1 108L66.2 120L79.4 108L92.5 120L105.6 108L118.8 120L131.9 108L145.0 120L158.1 108L171.2 120L184.4 108L197.5 120L210.6 108L223.8 120L236.9 108L250.0 120"/><path class="ad ad-dim" pathLength="1" style="--d:0.40s" d="M80 230V183.0A23.0 23.0 0 0 1 126 183.0V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.40s" d="M150 230V183.0A23.0 23.0 0 0 1 196 183.0V230"/><path class="ad ad-faint" pathLength="1" style="--d:0.60s" d="M70 142L75 132L80 142Z"/><path class="ad ad-faint" pathLength="1" style="--d:0.60s" d="M130 142L135 132L140 142Z"/><path class="ad ad-faint" pathLength="1" style="--d:0.60s" d="M190 142L195 132L200 142Z"/><path class="ad" pathLength="1" style="--d:0.15s" d="M250 230V60H330V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.40s" d="M250 60L263.3 48L276.7 60L290.0 48L303.3 60L316.7 48L330.0 60"/><path class="ad ad-dim" pathLength="1" style="--d:0.55s" d="M272 230V158.0A18.0 18.0 0 0 1 308 158.0V230"/><path class="ad ad-faint" pathLength="1" style="--d:0.75s" d="M280 82L285 72L290 82Z"/><path class="ad ad-dim" pathLength="1" style="--d:0.55s" d="M262 60V40H318V60M290 40V20"/><path class="ad" pathLength="1" style="--d:0.30s" d="M330 230V140H620V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.55s" d="M330 140L343.2 128L356.4 140L369.5 128L382.7 140L395.9 128L409.1 140L422.3 128L435.5 140L448.6 128L461.8 140L475.0 128L488.2 140L501.4 128L514.5 140L527.7 128L540.9 140L554.1 128L567.3 140L580.5 128L593.6 140L606.8 128L620.0 140"/><path class="ad ad-dim" pathLength="1" style="--d:0.70s" d="M370 230V190.0A20.0 20.0 0 0 1 410 190.0V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.70s" d="M430 230V190.0A20.0 20.0 0 0 1 470 190.0V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.70s" d="M490 230V190.0A20.0 20.0 0 0 1 530 190.0V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.70s" d="M550 230V190.0A20.0 20.0 0 0 1 590 190.0V230"/><path class="ad ad-faint" pathLength="1" style="--d:0.90s" d="M360 162L365 152L370 162Z"/><path class="ad ad-faint" pathLength="1" style="--d:0.90s" d="M420 162L425 152L430 162Z"/><path class="ad ad-faint" pathLength="1" style="--d:0.90s" d="M480 162L485 152L490 162Z"/><path class="ad ad-faint" pathLength="1" style="--d:0.90s" d="M540 162L545 152L550 162Z"/><path class="ad" pathLength="1" style="--d:0.45s" d="M620 230V100H760V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.70s" d="M620 100L634.0 88L648.0 100L662.0 88L676.0 100L690.0 88L704.0 100L718.0 88L732.0 100L746.0 88L760.0 100"/><path class="ad ad-dim" pathLength="1" style="--d:0.85s" d="M660 230V150.0A30.0 30.0 0 0 1 720 150.0V230"/><path class="ad ad-faint" pathLength="1" style="--d:1.05s" d="M650 122L655 112L660 122Z"/><path class="ad ad-faint" pathLength="1" style="--d:1.05s" d="M710 122L715 112L720 122Z"/><path class="ad" pathLength="1" style="--d:0.60s" d="M760 230V135H1050V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.85s" d="M760 135L773.2 123L786.4 135L799.5 123L812.7 135L825.9 123L839.1 135L852.3 123L865.5 135L878.6 123L891.8 135L905.0 123L918.2 135L931.4 123L944.5 135L957.7 123L970.9 135L984.1 123L997.3 135L1010.5 123L1023.6 135L1036.8 123L1050.0 135"/><path class="ad ad-dim" pathLength="1" style="--d:1.00s" d="M800 230V190.0A20.0 20.0 0 0 1 840 190.0V230"/><path class="ad ad-dim" pathLength="1" style="--d:1.00s" d="M870 230V190.0A20.0 20.0 0 0 1 910 190.0V230"/><path class="ad ad-dim" pathLength="1" style="--d:1.00s" d="M940 230V190.0A20.0 20.0 0 0 1 980 190.0V230"/><path class="ad ad-faint" pathLength="1" style="--d:1.20s" d="M790 157L795 147L800 157Z"/><path class="ad ad-faint" pathLength="1" style="--d:1.20s" d="M850 157L855 147L860 157Z"/><path class="ad ad-faint" pathLength="1" style="--d:1.20s" d="M910 157L915 147L920 157Z"/><path class="ad ad-faint" pathLength="1" style="--d:1.20s" d="M970 157L975 147L980 157Z"/><path class="ad" pathLength="1" style="--d:0.75s" d="M1050 230V75H1130V230"/><path class="ad ad-dim" pathLength="1" style="--d:1.00s" d="M1050 75L1063.3 63L1076.7 75L1090.0 63L1103.3 75L1116.7 63L1130.0 75"/><path class="ad ad-dim" pathLength="1" style="--d:1.15s" d="M1072 230V168.0A18.0 18.0 0 0 1 1108 168.0V230"/><path class="ad ad-faint" pathLength="1" style="--d:1.35s" d="M1080 97L1085 87L1090 97Z"/><path class="ad" pathLength="1" style="--d:0.90s" d="M1130 230V125H1240V230"/><path class="ad ad-dim" pathLength="1" style="--d:1.15s" d="M1130 125L1143.8 113L1157.5 125L1171.2 113L1185.0 125L1198.8 113L1212.5 125L1226.2 113L1240.0 125"/><path class="ad ad-dim" pathLength="1" style="--d:1.30s" d="M1160 230V183.0A23.0 23.0 0 0 1 1206 183.0V230"/><path class="ad ad-faint" pathLength="1" style="--d:1.50s" d="M1160 147L1165 137L1170 147Z"/></g><g transform="translate(2560 0) scale(-1 1)"><path class="ad" pathLength="1" style="--d:0.15s" d="M0 230H1280"/><path class="ad" pathLength="1" style="--d:0.15s" d="M40 230V120H250V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.40s" d="M40 120L53.1 108L66.2 120L79.4 108L92.5 120L105.6 108L118.8 120L131.9 108L145.0 120L158.1 108L171.2 120L184.4 108L197.5 120L210.6 108L223.8 120L236.9 108L250.0 120"/><path class="ad ad-dim" pathLength="1" style="--d:0.55s" d="M80 230V183.0A23.0 23.0 0 0 1 126 183.0V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.55s" d="M150 230V183.0A23.0 23.0 0 0 1 196 183.0V230"/><path class="ad ad-faint" pathLength="1" style="--d:0.75s" d="M70 142L75 132L80 142Z"/><path class="ad ad-faint" pathLength="1" style="--d:0.75s" d="M130 142L135 132L140 142Z"/><path class="ad ad-faint" pathLength="1" style="--d:0.75s" d="M190 142L195 132L200 142Z"/><path class="ad" pathLength="1" style="--d:0.30s" d="M250 230V60H330V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.55s" d="M250 60L263.3 48L276.7 60L290.0 48L303.3 60L316.7 48L330.0 60"/><path class="ad ad-dim" pathLength="1" style="--d:0.70s" d="M272 230V158.0A18.0 18.0 0 0 1 308 158.0V230"/><path class="ad ad-faint" pathLength="1" style="--d:0.90s" d="M280 82L285 72L290 82Z"/><path class="ad ad-dim" pathLength="1" style="--d:0.70s" d="M262 60V40H318V60M290 40V20"/><path class="ad" pathLength="1" style="--d:0.45s" d="M330 230V140H620V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.70s" d="M330 140L343.2 128L356.4 140L369.5 128L382.7 140L395.9 128L409.1 140L422.3 128L435.5 140L448.6 128L461.8 140L475.0 128L488.2 140L501.4 128L514.5 140L527.7 128L540.9 140L554.1 128L567.3 140L580.5 128L593.6 140L606.8 128L620.0 140"/><path class="ad ad-dim" pathLength="1" style="--d:0.85s" d="M370 230V190.0A20.0 20.0 0 0 1 410 190.0V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.85s" d="M430 230V190.0A20.0 20.0 0 0 1 470 190.0V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.85s" d="M490 230V190.0A20.0 20.0 0 0 1 530 190.0V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.85s" d="M550 230V190.0A20.0 20.0 0 0 1 590 190.0V230"/><path class="ad ad-faint" pathLength="1" style="--d:1.05s" d="M360 162L365 152L370 162Z"/><path class="ad ad-faint" pathLength="1" style="--d:1.05s" d="M420 162L425 152L430 162Z"/><path class="ad ad-faint" pathLength="1" style="--d:1.05s" d="M480 162L485 152L490 162Z"/><path class="ad ad-faint" pathLength="1" style="--d:1.05s" d="M540 162L545 152L550 162Z"/><path class="ad" pathLength="1" style="--d:0.60s" d="M620 230V100H760V230"/><path class="ad ad-dim" pathLength="1" style="--d:0.85s" d="M620 100L634.0 88L648.0 100L662.0 88L676.0 100L690.0 88L704.0 100L718.0 88L732.0 100L746.0 88L760.0 100"/><path class="ad ad-dim" pathLength="1" style="--d:1.00s" d="M660 230V150.0A30.0 30.0 0 0 1 720 150.0V230"/><path class="ad ad-faint" pathLength="1" style="--d:1.20s" d="M650 122L655 112L660 122Z"/><path class="ad ad-faint" pathLength="1" style="--d:1.20s" d="M710 122L715 112L720 122Z"/><path class="ad" pathLength="1" style="--d:0.75s" d="M760 230V135H1050V230"/><path class="ad ad-dim" pathLength="1" style="--d:1.00s" d="M760 135L773.2 123L786.4 135L799.5 123L812.7 135L825.9 123L839.1 135L852.3 123L865.5 135L878.6 123L891.8 135L905.0 123L918.2 135L931.4 123L944.5 135L957.7 123L970.9 135L984.1 123L997.3 135L1010.5 123L1023.6 135L1036.8 123L1050.0 135"/><path class="ad ad-dim" pathLength="1" style="--d:1.15s" d="M800 230V190.0A20.0 20.0 0 0 1 840 190.0V230"/><path class="ad ad-dim" pathLength="1" style="--d:1.15s" d="M870 230V190.0A20.0 20.0 0 0 1 910 190.0V230"/><path class="ad ad-dim" pathLength="1" style="--d:1.15s" d="M940 230V190.0A20.0 20.0 0 0 1 980 190.0V230"/><path class="ad ad-faint" pathLength="1" style="--d:1.35s" d="M790 157L795 147L800 157Z"/><path class="ad ad-faint" pathLength="1" style="--d:1.35s" d="M850 157L855 147L860 157Z"/><path class="ad ad-faint" pathLength="1" style="--d:1.35s" d="M910 157L915 147L920 157Z"/><path class="ad ad-faint" pathLength="1" style="--d:1.35s" d="M970 157L975 147L980 157Z"/><path class="ad" pathLength="1" style="--d:0.90s" d="M1050 230V75H1130V230"/><path class="ad ad-dim" pathLength="1" style="--d:1.15s" d="M1050 75L1063.3 63L1076.7 75L1090.0 63L1103.3 75L1116.7 63L1130.0 75"/><path class="ad ad-dim" pathLength="1" style="--d:1.30s" d="M1072 230V168.0A18.0 18.0 0 0 1 1108 168.0V230"/><path class="ad ad-faint" pathLength="1" style="--d:1.50s" d="M1080 97L1085 87L1090 97Z"/><path class="ad" pathLength="1" style="--d:1.05s" d="M1130 230V125H1240V230"/><path class="ad ad-dim" pathLength="1" style="--d:1.30s" d="M1130 125L1143.8 113L1157.5 125L1171.2 113L1185.0 125L1198.8 113L1212.5 125L1226.2 113L1240.0 125"/><path class="ad ad-dim" pathLength="1" style="--d:1.45s" d="M1160 230V183.0A23.0 23.0 0 0 1 1206 183.0V230"/><path class="ad ad-faint" pathLength="1" style="--d:1.65s" d="M1160 147L1165 137L1170 147Z"/></g></svg>
</section>
"""


JS = """    // ── OUR STORY: GAP CLOSES, GROUP ORBIT DRAWS ─────────────────────────────
    {
      const sy = document.querySelector('[data-story]');
      if (sy) {
        const mp = sy.querySelector('[data-map]');
        if (mp) { if (reduced) mp.classList.add('is-in'); else { const io4 = new IntersectionObserver(([e]) => { if (e.isIntersecting) { mp.classList.add('is-in'); io4.disconnect(); } }, { threshold: 0.35 }); io4.observe(mp); } }
        if (reduced) { sy.classList.add('is-in'); sy.querySelector('.sy-elev').classList.add('is-in'); }
        else {
          const io2 = new IntersectionObserver((es) => { if (es.some(e => e.isIntersecting)) { sy.classList.add('is-in'); io2.disconnect(); } }, { threshold: 0.15 });
          io2.observe(sy.querySelector('.sy-gap'));
          io2.observe(sy.querySelector('.gp'));
          const el = sy.querySelector('.sy-elev'); const io3 = new IntersectionObserver(([e]) => { if (e.isIntersecting) { el.classList.add('is-in'); io3.disconnect(); } }, { threshold: 0.25 }); io3.observe(el);
        }
      }
    }

"""
MARK = "    // ── FADE-IN ON LOAD (lazy images)"

for path, lang in [("about-us.dc.html", "en"), ("about-us.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ OUR STORY ━+ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── OUR STORY: GAP CLOSES"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

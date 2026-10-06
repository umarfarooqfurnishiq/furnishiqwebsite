"""Service pages, the three pillars: three large cards beside a sticky index.

The template for the three-pillar section of the four service pages. The three pillars scroll by as large
cards on the reading-start side, each photograph running out to the screen edge and wiping in as it
arrives. On the other side, held in view while the section scrolls: the heading, a large numeral for the
pillar being read and an index of the three, each with a line that fills as its card passes; the link to
the projects closes it. It scrolls naturally: nothing is pinned,
since the section above already is. On phones the index and numeral step aside and the cards stack.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/servicepages/sp_pillars.py [page ...]
"""
import re, sys

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
PAGE = {
    "services-interior-design": dict(
        imgs=[("interior-design-pillar-visual-certainty-render-review", (1280, 1920, 2400)),
              ("interior-design-pillar-brand-led-planning-floor-plan", (1280, 1920, 2400)),
              ("interior-design-pillar-implementation-ready-joinery-drawing", (1280, 1920, 2400))],
        en=dict(
            eyebrow="The FurnishIQ Advantage", h2="Three Pillars of Design Excellence",
            short=["Visual certainty", "Brand-led planning", "Implementation-ready"],
            titles=["Visual Certainty: Approval with Absolute Confidence", "Strategic DNA: Brand-Led Planning", "Value-Driven & Implementation-Ready"],
            bodies=["We eliminate the uncertainty often associated with interior projects. By utilizing state-of-the-art Photoreal 3D Renders, we allow you to walk through your future space before a single brick is laid. You approve every light fixture, material, and color palette in a virtual environment, ensuring the final build matches your vision with absolute precision.",
                    "For our corporate and commercial clients, design is a strategic business asset. We practice Brand-Led Planning, where spatial flows are engineered to reflect your unique identity and enhance daily operational efficiency — designing for the humans who inhabit the space, balancing high-end aesthetics with practical functionality.",
                    "Our designs are not just “pretty pictures” — they are technical blueprints for success. We focus on providing creative, easy-to-implement, and cost-effective solutions."],
            points=[("Budget Alignment", "From the very first phase, we establish a firm budget roadmap to ensure our creative visions are achievable without unexpected financial surprises."),
                    ("Implementation-Ready", "Every design is a technical blueprint for success — creative, easy-to-implement, and cost-effective from day one.")],
            alts=["A client and a designer review a photoreal render of a majlis on screen, with its travertine, fluted walnut, boucle and brass samples on the table",
                  "A corporate floor plan with brand flow and visitor pathways sketched in bronze pencil, beside brand colour swatches and a white massing model",
                  "A joinery shop drawing of walnut wall panels with its cost and material schedule, laid beside the finished fluted panel on a workbench"],
            cta="Discover Projects", href="/projects", index="The three pillars"),
        ar=dict(
            eyebrow="ميزة FurnishIQ", h2="ثلاث ركائز للتميز في التصميم",
            short=["يقين بصري", "تخطيط قائم على الهوية", "جاهزية للتنفيذ"],
            titles=["يقين بصري: الموافقة بثقة مطلقة", "الحمض النووي الاستراتيجي: التخطيط القائم على الهوية", "قيمة عالية وجاهزية للتنفيذ"],
            bodies=["نُزيل عدم اليقين المرتبط عادة بمشاريع التصميم الداخلي. من خلال استخدام تصورات ثلاثية الأبعاد واقعية وحديثة، نتيح لك التجول في مساحتك المستقبلية قبل وضع أول طوبة. توافق على كل تجهيزة إضاءة ومادة ولوحة ألوان في بيئة افتراضية، مما يضمن مطابقة البناء النهائي لرؤيتك بدقة مطلقة.",
                    "بالنسبة لعملائنا من الشركات والقطاع التجاري، يُعد التصميم أصلاً استراتيجياً للأعمال. نمارس التخطيط القائم على الهوية، حيث تُصمم تدفقات المساحة لتعكس هويتك الفريدة وتُعزز الكفاءة التشغيلية اليومية — بتصميم موجّه لمن يسكن المساحة، موازناً بين الجماليات الراقية والوظائف العملية.",
                    "تصاميمنا ليست مجرد “صور جميلة” — بل هي مخططات تقنية للنجاح. نركز على تقديم حلول إبداعية، سهلة التنفيذ، وفعالة من حيث التكلفة."],
            points=[("مواءمة الميزانية", "منذ المرحلة الأولى، نضع خارطة طريق ثابتة للميزانية لضمان أن رؤيتنا الإبداعية قابلة للتحقيق دون مفاجآت مالية غير متوقعة."),
                    ("جاهز للتنفيذ", "كل تصميم هو مخطط تقني للنجاح — إبداعي، سهل التنفيذ، وفعال من حيث التكلفة منذ اليوم الأول.")],
            alts=["عميل ومصمم يراجعان تصوراً واقعياً لمجلس على الشاشة، وعلى الطاولة عينات الترافرتين والجوز المضلع والبوكليه والنحاس",
                  "مخطط مكتب لشركة رُسمت عليه مسارات الهوية والزوار بقلم برونزي، بجانب عينات ألوان الهوية ومجسم أبيض",
                  "رسم تنفيذي لألواح جدارية من خشب الجوز مع جدول التكاليف والمواد، بجانب اللوح المضلع المنجز على طاولة العمل"],
            cta="اكتشف مشاريعنا", href="/ar/projects", index="الركائز الثلاث"),
    ),
    # stand-in photographs until the page's own three arrive
    "services-fitout": dict(
        imgs=[("fitout-pillar-brand-led-planning-site-plan", (1280, 1920, 2400)),
              ("fitout-pillar-integrated-engineering-mep-ceiling", (1280, 1920, 2400)),
              ("fitout-pillar-zero-snag-level-check", (1280, 1920, 2400))],
        en=dict(
            eyebrow="The FurnishIQ Fit-Out Advantage", h2="Three Pillars of Fit-Out Excellence",
            short=["Brand-led planning", "Integrated engineering", "Zero-snag handover"],
            titles=["Strategic DNA: Brand-Led Planning", "Technical Backbone: Integrated Engineering", "The Zero-Snag Promise"],
            bodies=["We don’t just build walls; we engineer experiences. We practice Brand-Led Planning, where every layout and traffic flow is strategically designed to reflect your unique identity and optimize your daily operational efficiency. Whether for a high-traffic retail space or a private villa, the flow is tied directly to your specific needs.",
                    "A successful fit-out relies on what’s behind the walls. We ensure the seamless integration of Engineering and MEP services, providing the high-performance infrastructure — climate control, power, and plumbing — your project requires without technical conflicts.",
                    "Our hallmark is excellence in execution. Through rigorous Quality Assurance and Health, Safety, and Environment monitoring, we guarantee a “Clean Build” and a flawless, zero-snag handover every time."],
            points=[("Strict QA/QC", "Rigorous Quality Assurance and Quality Control protocols ensure every component meets industry benchmarks."),
                    ("HSE Monitoring", "Continuous Health, Safety, and Environment monitoring is mandatory throughout the installation phase.")],
            alts=["A colour-coded floor plan taped to a column on an open shell floor", "Ductwork, cable trays and sprinkler mains coordinated above the ceiling grid", "A brass spirit level reading true on a travertine counter"],
            cta="Discover Projects", href="/projects", index="The three pillars"),
        ar=dict(
            eyebrow="ميزة FurnishIQ في التشطيبات", h2="ثلاث ركائز للتميز في التشطيبات",
            short=["تخطيط قائم على الهوية", "هندسة متكاملة", "تسليم بلا ملاحظات"],
            titles=["الهوية الاستراتيجية: التخطيط القائم على العلامة التجارية", "العمود الفني: الهندسة المتكاملة", "وعد التسليم بلا ملاحظات"],
            bodies=["نحن لا نبني الجدران فحسب، بل نصمم التجارب. نتبع أسلوب التخطيط القائم على العلامة التجارية، حيث يُصمم كل تخطيط ومسار حركة بشكل استراتيجي ليعكس هويتك الفريدة ويحسّن كفاءتك التشغيلية اليومية. سواء لمساحة تجارية عالية الحركة أو فيلا خاصة، يرتبط التدفق مباشرة باحتياجاتك المحددة.",
                    "يعتمد نجاح أي مشروع تشطيب على ما يقع خلف الجدران. نضمن التكامل السلس بين خدمات الهندسة والأنظمة الكهروميكانيكية، لتوفير البنية التحتية عالية الأداء — التحكم بالمناخ والطاقة والسباكة — التي يحتاجها مشروعك دون أي تعارض فني.",
                    "تميزنا يكمن في التنفيذ المتقن. من خلال ضمان الجودة الصارم ومراقبة الصحة والسلامة والبيئة، نضمن “بناءً نظيفًا” وتسليمًا خاليًا من العيوب في كل مرة."],
            points=[("ضمان وضبط الجودة الصارم", "بروتوكولات صارمة لضمان الجودة وضبطها تكفل مطابقة كل عنصر لمعايير الصناعة."),
                    ("مراقبة الصحة والسلامة والبيئة", "مراقبة مستمرة للصحة والسلامة والبيئة إلزامية طوال مرحلة التنفيذ.")],
            alts=["مخطط ملوّن مثبّت على عمود في طابق خرساني مفتوح", "مجاري الهواء وحوامل الكابلات وخطوط الرشاشات منسّقة فوق شبكة السقف", "ميزان ماء نحاسي مستوٍ تماماً على طاولة من الترافرتين"],
            cta="اكتشف مشاريعنا", href="/ar/projects", index="الركائز الثلاث"),
    ),
}
PAGE["services-mep"] = dict(
    imgs=[("mep-pillar-utility-integration-ceiling-detail", (1280, 1920, 2400)),
          ("mep-pillar-operational-integrity-plant-room", (1280, 1920, 2400)),
          ("mep-pillar-safety-quality-pressure-test", (1280, 1920, 2400))],
    en=dict(
        eyebrow="The FurnishIQ Engineering Advantage", h2="Three Pillars of Engineering Excellence",
        short=["Utility integration", "Operational integrity", "Safety & quality"],
        titles=["Seamless Utility Integration", "Structural & Operational Integrity", "Uncompromising Safety & Quality"],
        bodies=["We eliminate the technical conflicts that often plague multi-vendor projects. By integrating Mechanical, Electrical, and Plumbing systems during the design phase, we ensure climate control, power distribution, and plumbing are perfectly aligned with your spatial layout — preventing costly on-site adjustments and keeping your design uncompromised.",
                "Our engineering team designs for the long term, enhancing building performance and energy efficiency while ensuring the structural integrity of your environment meets the highest professional standards.",
                "Every installation is governed by our signature standards, combining rigorous protocols with continuous on-site oversight from start to handover."],
        points=[("Strict QA/QC", "Rigorous Quality Assurance and Quality Control protocols ensure every component meets industry benchmarks."),
                ("HSE Monitoring", "Continuous Health, Safety, and Environment monitoring is mandatory throughout the installation phase.")],
        alts=["A linear diffuser, a downlight and a sprinkler head set in one line between walnut ceiling slats", "An orderly plant room: insulated pipework, pumps on concrete plinths and cable trays above", "A brass pressure gauge on a copper pipe under test, with an inspection tag and a gloved hand holding a clipboard"],
        cta="Discover Projects", href="/projects", index="The three pillars"),
    ar=dict(
        eyebrow="ميزة FurnishIQ الهندسية", h2="ثلاث ركائز للتميز الهندسي",
        short=["تكامل المرافق", "السلامة التشغيلية", "السلامة والجودة"],
        titles=["تكامل سلس للمرافق", "السلامة الإنشائية والتشغيلية", "سلامة وجودة دون أي تنازلات"],
        bodies=["نزيل التعارضات الفنية التي كثيراً ما تعاني منها المشاريع متعددة المقاولين. من خلال دمج الأنظمة الميكانيكية والكهربائية والسباكة أثناء مرحلة التصميم، نضمن توافق التحكم في المناخ وتوزيع الطاقة والسباكة تماماً مع مخططك المكاني — ما يمنع التعديلات المكلفة في الموقع ويحافظ على تصميمك دون أي تنازلات.",
                "يصمم فريقنا الهندسي بمنظور طويل الأمد، لتحسين أداء المبنى وكفاءة استهلاك الطاقة، مع ضمان توافق السلامة الإنشائية لبيئتك مع أعلى المعايير المهنية.",
                "يخضع كل تركيب لمعاييرنا المميزة، التي تجمع بين بروتوكولات صارمة ورقابة ميدانية مستمرة من البداية وحتى التسليم."],
        points=[("ضمان الجودة الصارم (QA/QC)", "بروتوكولات صارمة لضمان الجودة ومراقبتها تكفل مطابقة كل مكون لمعايير القطاع."),
                ("مراقبة الصحة والسلامة والبيئة (HSE)", "المراقبة المستمرة للصحة والسلامة والبيئة إلزامية طوال مرحلة التركيب.")],
        alts=["فتحة تكييف خطية وإضاءة مدمجة ورأس رشاش في خط واحد بين شرائح سقف من خشب الجوز", "غرفة معدات منظمة: أنابيب معزولة ومضخات على قواعد خرسانية وحوامل كابلات في الأعلى", "مقياس ضغط نحاسي على أنبوب نحاسي قيد الاختبار، مع بطاقة فحص ويد بقفاز تحمل لوحة ملاحظات"],
        cta="اكتشف مشاريعنا", href="/ar/projects", index="الركائز الثلاث"),
)
PAGE["services-furniture"] = dict(
    imgs=[("furniture-pillar-visual-certainty-render-and-chair", (1280, 1920, 2400)),
          ("furniture-pillar-global-access-craftsman-walnut-table", (1280, 1920, 2400)),
          ("furniture-pillar-brand-led-workplace", (1280, 1920, 2400))],
    en=dict(
        eyebrow="The FurnishIQ Advantage: Curation with Purpose", h2="Three Pillars of Furniture Excellence",
        short=["Visual certainty", "Global access", "Brand-led selection"],
        titles=["Bespoke Procurement & Visual Certainty", "Global Access, Local Expertise", "Strategic Brand-Led Selection"],
        bodies=["We eliminate the risk of mismatched items. Our team strategically sources and plans furniture that aligns perfectly with the materials, lighting, and scale established in your approved Photoreal 3D renders. This ensures that every piece — from a statement sofa to an ergonomic workstation — fits your environment with absolute precision before it ever arrives.",
                "Leveraging our deep industry connections, we provide access to high-quality pieces that meet your specific aesthetic, budget, and operational needs. Whether sourcing bespoke artisanal items for a luxury villa or durable assets for an industrial facility, we ensure a cohesive look from floor to ceiling.",
                "For our corporate and commercial clients, furniture is a tool for productivity and brand expression. We practice Brand-Led Planning, selecting furniture that reflects your corporate culture and is strategically engineered to optimize your daily operations."],
        points=[("Brand Alignment", "Furniture is selected to reflect your corporate culture and reinforce your brand identity."),
                ("Operational Efficiency", "Every selection is strategically engineered to optimize your daily operations and productivity.")],
        alts=["A walnut and bouclé lounge chair in front of its pinned render, matching it piece for piece", "A craftsman's hands finishing the edge of a solid walnut table in a sunlit workshop", "A workplace of walnut workstations and leather lounge seating above the Riyadh skyline"],
        cta="Discover Projects", href="/projects", index="The three pillars"),
    ar=dict(
        eyebrow="ميزة FurnishIQ: تنسيق بهدف", h2="ثلاث ركائز للتميز في الأثاث",
        short=["يقين بصري", "وصول عالمي", "اختيار قائم على الهوية"],
        titles=["توريد مخصص ويقين بصري", "وصول عالمي، خبرة محلية", "اختيار استراتيجي قائم على الهوية"],
        bodies=["نُزيل مخاطر عدم التناسق بين القطع. يقوم فريقنا باختيار وتخطيط الأثاث بشكل استراتيجي بما ينسجم تماماً مع الخامات والإضاءة والمقاييس المعتمدة في تصوراتك ثلاثية الأبعاد الواقعية. هذا يضمن أن كل قطعة — من أريكة مميزة إلى محطة عمل مريحة — تتناسب مع بيئتك بدقة مطلقة قبل وصولها.",
                "بالاستفادة من شبكة علاقاتنا العميقة في القطاع، نوفر إمكانية الوصول إلى قطع عالية الجودة تلبي هويتك الجمالية وميزانيتك واحتياجاتك التشغيلية. سواء كنا نُوَرِّد قطعاً حرفية مخصصة لفيلا فاخرة أو أصولاً متينة لمنشأة صناعية، فإننا نضمن مظهراً متناسقاً من الأرض إلى السقف.",
                "بالنسبة لعملائنا من المؤسسات والقطاع التجاري، يُعد الأثاث أداة للإنتاجية والتعبير عن الهوية. نتّبع أسلوب التخطيط القائم على الهوية، فنختار الأثاث الذي يعكس ثقافتكم المؤسسية ويُصمَّم استراتيجياً لتحسين عملياتكم اليومية."],
        points=[("الانسجام مع الهوية", "يُختار الأثاث بما يعكس ثقافتكم المؤسسية ويعزز هويتكم التجارية."),
                ("الكفاءة التشغيلية", "كل اختيار مُصمَّم استراتيجياً لتحسين عملياتكم اليومية وإنتاجيتكم.")],
        alts=["كرسي استرخاء من الجوز والبوكليه أمام تصوره المثبّت، مطابق له قطعةً بقطعة", "يدا حرفي تشطّبان حافة طاولة من خشب الجوز الصلب في ورشة مشمسة", "مكان عمل بمحطات من خشب الجوز ومقاعد استرخاء جلدية فوق أفق الرياض"],
        cta="اكتشف المشاريع", href="/ar/projects", index="الركائز الثلاث"),
)
ARROW = {
    "en": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
    "ar": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>',
}


def srcset(base, ws):
    return ", ".join(f"uploads/{base}-{w}.webp {w}w" for w in ws)


def build(page, lang):
    ar = lang == "ar"
    P = PAGE[page]
    c = P[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    caps = "normal" if ar else "0.22em"
    small = "12px" if ar else "9px"
    PAD = "clamp(24px,5vw,80px)"
    idx = "\n".join(f'''          <li><a class="pl-ix" href="#pl-{k}" data-pl-ix="{k}"><i class="pl-bar" aria-hidden="true"></i><span class="pl-ixn" dir="ltr">0{k + 1}</span><span class="pl-ixt">{c['short'][k]}</span></a></li>''' for k in range(3))
    cards = []
    for k in range(3):
        base, ws = P["imgs"][k]
        pts = ""
        if k == 2:
            pts = '\n          <div class="pl-pts">' + "".join(f'<div class="pl-pt"><p class="pl-ptt">{t}</p><p class="pl-ptx">{x}</p></div>' for t, x in c["points"]) + '</div>'
        cards.append(f'''        <article class="pl-card" id="pl-{k}" data-pl-card="{k}">
          <div class="pl-fig">
            <div class="pl-img"><img src="uploads/{base}-{ws[min(1, len(ws) - 1)]}.webp" srcset="{srcset(base, ws)}" sizes="(max-width:900px) 100vw, 72vw" alt="{c['alts'][k]}" loading="lazy" decoding="async"></div>
            <div class="pl-over">
              <span class="pl-num" aria-hidden="true">0{k + 1}</span>
              <h3 class="pl-t">{c['titles'][k]}</h3>
              <p class="pl-b">{c['bodies'][k]}</p>{pts}
            </div>
          </div>
        </article>''')
    cards = "\n".join(cards)
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ADVANTAGE ━━━━━━━ -->
<section id="pillars" data-screen-label="Advantage" data-sp-pillars{' dir="rtl"' if ar else ''} style="scroll-margin-top:80px;background:#FFFFFF;color:#3A2D25;position:relative;padding:clamp(64px,8vw,100px) {PAD};">
  <style>
    [data-sp-pillars] .pl-wrap{{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:minmax(0,8fr) minmax(0,4fr);gap:clamp(40px,6vw,104px);align-items:start;}}
    [data-sp-pillars] .pl-list{{grid-column:1;grid-row:1;}}
    [data-sp-pillars] .pl-side{{grid-column:2;grid-row:1;position:sticky;top:clamp(112px,16vh,148px);display:flex;flex-direction:column;}}
    [data-sp-pillars] .pl-eyebrow{{display:flex;align-items:center;gap:16px;margin:0 0 24px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    [data-sp-pillars] .pl-eyebrow i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    [data-sp-pillars] .pl-h2{{margin:0;font-family:{font};font-weight:500;font-size:clamp(30px,3vw,46px);line-height:1.08;letter-spacing:{'0' if ar else '-0.015em'};color:#1F1F1F;text-wrap:balance;max-width:{'none' if ar else '13ch'};}}
    /* the numeral of the pillar in view, rolling from one to the next */
    [data-sp-pillars] .pl-big{{position:relative;display:flex;align-items:flex-end;gap:14px;height:clamp(96px,10vw,148px);margin:clamp(32px,4vh,52px) 0 clamp(24px,3vh,36px);overflow:hidden;}}
    [data-sp-pillars] .pl-roll{{position:relative;height:100%;overflow:hidden;}}
    [data-sp-pillars] .pl-roll span{{display:block;height:100%;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(96px,10vw,148px);line-height:1;letter-spacing:-0.04em;color:#D6C2A8;transform:translateY(calc(var(--i,0) * -100%));transition:transform 0.8s {EASE};}}
    [data-sp-pillars] .pl-of{{padding-bottom:clamp(14px,1.4vw,22px);font-family:'Lama Sans',sans-serif;font-size:12px;letter-spacing:0.2em;color:#8B6B4A;}}
    [data-sp-pillars] .pl-index{{list-style:none;margin:0;padding:0;border-top:1px solid rgba(58,45,37,0.14);}}
    [data-sp-pillars] .pl-ix{{position:relative;display:flex;align-items:baseline;gap:18px;padding:18px 0;border-bottom:1px solid rgba(58,45,37,0.14);color:rgba(58,45,37,0.5);text-decoration:none;transition:color 0.4s {EASE};}}
    [data-sp-pillars] .pl-ix:hover,[data-sp-pillars] .pl-ix.is-on{{color:#1F1F1F;}}
    [data-sp-pillars] .pl-ix:focus-visible{{outline:1px solid #8B6B4A;outline-offset:4px;}}
    [data-sp-pillars] .pl-bar{{position:absolute;inset-inline:0;bottom:-1px;height:1px;background:#8B6B4A;transform:scaleX(var(--p,0));transform-origin:{'100%' if ar else '0%'} 50%;}}
    [data-sp-pillars] .pl-ixn{{font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.2em;color:#8B6B4A;}}
    [data-sp-pillars] .pl-ixt{{font-family:{font};font-size:{'17px' if ar else '16px'};}}
    [data-sp-pillars] .pl-cta{{align-self:flex-start;display:inline-flex;align-items:center;gap:12px;margin-top:clamp(28px,4vh,44px);padding:17px 30px;background:#3A2D25;color:#F5F2ED;border:1px solid #3A2D25;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-sp-pillars] .pl-cta:hover,[data-sp-pillars] .pl-cta:focus-visible{{background:transparent;color:#3A2D25;}}
    /* the cards */
    [data-sp-pillars] .pl-card{{scroll-margin-top:120px;}}
    [data-sp-pillars] .pl-card+.pl-card{{margin-top:clamp(88px,11vw,168px);}}
    [data-sp-pillars] .pl-fig{{position:relative;margin-inline-start:calc(var(--pl-bleed,0px) * -1);overflow:hidden;clip-path:inset(0 0 100% 0);transition:clip-path 1.3s cubic-bezier(0.77,0,0.18,1);}}
    [data-sp-pillars] .pl-card.is-in .pl-fig{{clip-path:inset(0 0 0 0);}}
    [data-sp-pillars] .pl-img{{aspect-ratio:4/3;overflow:hidden;background:#3A2D25;}}
    [data-sp-pillars] .pl-img img{{display:block;width:100%;height:100%;object-fit:cover;transform:scale(1.12);transition:transform 2s {EASE};}}
    [data-sp-pillars] .pl-card.is-in .pl-img img{{transform:scale(1);}}
    /* the text sits on the photograph's lower edge, over a soft warm fade, aligned to the page grid */
    [data-sp-pillars] .pl-over{{position:absolute;inset:auto 0 0 0;padding:clamp(96px,12vw,180px) clamp(28px,3.4vw,56px) clamp(28px,3vw,44px);padding-inline-start:calc(var(--pl-bleed,0px) + 0px);background:linear-gradient(0deg,rgba(18,13,9,0.9) 0%,rgba(18,13,9,0.72) 38%,rgba(18,13,9,0.32) 70%,rgba(18,13,9,0) 100%);}}
    [data-sp-pillars] .pl-num,[data-sp-pillars] .pl-t,[data-sp-pillars] .pl-b,[data-sp-pillars] .pl-pts{{opacity:0;transform:translateY(18px);transition:opacity 0.8s {EASE} 0.5s,transform 0.8s {EASE} 0.5s;}}
    [data-sp-pillars] .pl-card.is-in .pl-num,[data-sp-pillars] .pl-card.is-in .pl-t,[data-sp-pillars] .pl-card.is-in .pl-b,[data-sp-pillars] .pl-card.is-in .pl-pts{{opacity:1;transform:none;}}
    [data-sp-pillars] .pl-over>*{{position:relative;}}
    /* the numeral's baseline on the body's last baseline (0.046em: Lama Sans digits sit that far above the
       bottom of a 0.8 line box; 7px: the body's descent and half-leading), its edge 32px before the text column,
       falling back to the photograph's edge where the margin is too narrow to hold it */
    [data-sp-pillars] .pl-over>.pl-num{{position:absolute;bottom:calc(clamp(28px,3vw,44px) + 7px - 0.046em);{'left' if ar else 'right'}:min(calc(100% - var(--pl-bleed,0px) + 32px),calc(100% - 1.2em - 4px));font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(100px,10.5vw,196px);line-height:0.8;letter-spacing:-0.04em;color:rgba(245,242,237,0.14);pointer-events:none;user-select:none;}}
    [data-sp-pillars] .pl-t{{margin:0 0 12px;max-width:{'560px' if ar else '28ch'};font-family:{font};font-weight:500;font-size:clamp(22px,2vw,30px);line-height:1.2;color:#F5F2ED;text-wrap:balance;}}
    [data-sp-pillars] .pl-b{{margin:0;max-width:{'640px' if ar else '64ch'};font-family:{font};font-size:{'15px' if ar else '14px'};line-height:1.7;color:rgba(245,242,237,0.84);}}
    [data-sp-pillars] .pl-pts{{display:grid;grid-template-columns:1fr 1fr;gap:clamp(20px,3vw,40px);max-width:{'640px' if ar else '64ch'};margin-top:18px;padding-top:16px;border-top:1px solid rgba(245,242,237,0.22);}}
    [data-sp-pillars] .pl-ptt{{margin:0 0 6px;font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;color:#D6C2A8;}}
    [data-sp-pillars] .pl-ptx{{margin:0;font-family:{font};font-size:{'14px' if ar else '13px'};line-height:1.6;color:rgba(245,242,237,0.76);}}
    @media(max-width:900px){{
      [data-sp-pillars] .pl-wrap{{grid-template-columns:1fr;gap:44px;}}
      [data-sp-pillars] .pl-side,[data-sp-pillars] .pl-list{{grid-column:1;grid-row:auto;}}
      [data-sp-pillars] .pl-side{{position:static;}}
      [data-sp-pillars] .pl-fig{{margin-inline:calc(clamp(24px,5vw,80px) * -1);}}
      [data-sp-pillars] .pl-big,[data-sp-pillars] .pl-index{{display:none;}}
      [data-sp-pillars] .pl-cta{{order:9;}}
      [data-sp-pillars] .pl-pts{{grid-template-columns:1fr;border-top-color:rgba(58,45,37,0.14);}}
      [data-sp-pillars] .pl-over{{position:static;background:none;padding:28px clamp(24px,5vw,80px) 0;}}
      [data-sp-pillars] .pl-ptt{{color:#8B6B4A;}}
      /* on phones the text sits on white below the photograph: the numeral goes with it, faint bronze */
      [data-sp-pillars] .pl-over>.pl-num{{top:calc(75vw + 14px);bottom:auto;{'right:auto;left' if ar else 'left:auto;right'}:clamp(18px,5vw,40px);font-size:88px;color:rgba(139,107,74,0.16);}}
      [data-sp-pillars] .pl-t{{color:#1F1F1F;}}
      [data-sp-pillars] .pl-b,[data-sp-pillars] .pl-ptx{{color:#5B4636;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-sp-pillars] *{{transition:none!important;}}
      [data-sp-pillars] .pl-fig{{clip-path:none;}}
      [data-sp-pillars] .pl-img img,[data-sp-pillars] .pl-num,[data-sp-pillars] .pl-t,[data-sp-pillars] .pl-b,[data-sp-pillars] .pl-pts{{opacity:1;transform:none;}}
    }}
  </style>
  <div class="pl-wrap">
    <div class="pl-side">
      <p class="pl-eyebrow"><i></i>{c['eyebrow']}</p>
      <h2 class="pl-h2">{c['h2']}</h2>
      <div class="pl-big" aria-hidden="true"><span class="pl-roll"><span>01</span><span>02</span><span>03</span></span><span class="pl-of" dir="ltr">/ 03</span></div>
      <nav aria-label="{c['index']}"><ol class="pl-index">
{idx}
      </ol></nav>
      <a class="pl-cta" href="{c['href']}">{c['cta']}{ARROW[lang]}</a>
    </div>
    <div class="pl-list">
{cards}
    </div>
  </div>
</section>
"""


JS = """    // ── SERVICE PAGES, PILLARS: STICKY INDEX AND THREE CARDS ────────────────
    {
      const sec = document.querySelector('[data-sp-pillars]');
      if (sec) {
        const cards = Array.from(sec.querySelectorAll('[data-pl-card]')), ix = Array.from(sec.querySelectorAll('[data-pl-ix]'));
        const rolls = Array.from(sec.querySelectorAll('.pl-roll span'));
        const wrap = sec.querySelector('.pl-wrap'), rtl = sec.getAttribute('dir') === 'rtl';
        const bleed = () => { const r = wrap.getBoundingClientRect(); sec.style.setProperty('--pl-bleed', Math.max(0, rtl ? document.documentElement.clientWidth - r.right : r.left) + 'px'); };
        let ticking = false;
        const update = () => {
          ticking = false;
          const line = window.innerHeight * 0.55;
          let on = 0;
          cards.forEach((c, k) => {
            const r = c.getBoundingClientRect();
            if (r.top < line) on = k;
            // the index line fills as the card's reading line passes through it
            ix[k].style.setProperty('--p', Math.min(1, Math.max(0, (line - r.top) / r.height)).toFixed(4));
          });
          ix.forEach((a, k) => a.classList.toggle('is-on', k === on));
          rolls.forEach((s) => s.style.setProperty('--i', on));
        };
        window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
        window.addEventListener('resize', () => { bleed(); update(); });
        bleed();
        ix.forEach((a, k) => a.addEventListener('click', (e) => {
          e.preventDefault();
          window.scrollTo({ top: cards[k].getBoundingClientRect().top + window.scrollY - 120, behavior: reduced ? 'instant' : 'smooth' });
        }));
        const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -12% 0px' });
        cards.forEach((c) => io.observe(c));
        update();
      }
    }

"""
MARK = "    // ── SCROLL REVEAL"

pages = sys.argv[1:] or list(PAGE)
for page in pages:
    for name, lang in [(f"{page}.dc.html", "en"), (f"{page}.ar.dc.html", "ar")]:
        s = open(name, encoding="utf-8").read()
        s, n = re.subn(r"<!-- ━+ ADVANTAGE ━+ -->\n<section [^>]*data-screen-label=\"Advantage\".*?\n</section>\n", lambda m: build(page, lang), s, count=1, flags=re.S)
        assert n == 1, name
        old = "    // ── SERVICE PAGES, PILLARS:"
        if old in s:
            a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
            s = s[:a] + s[b:]
        assert s.count(MARK) == 1, name
        s = s.replace(MARK, JS + MARK)
        open(name, "w", encoding="utf-8", newline="").write(s)
        print(name, "ok")

"""Services, Engineering & MEP: the building's nervous system.

An architect's section through a two-storey building, drawn onto the page as it scrolls in. The five MEP
disciplines run where they would in reality: ducts and sprinkler mains in the ceiling voids, conduits to
light points, water from the roof tank, drainage to the sewer, data to access points and cameras. Choosing a
discipline fades the others and sets its lines flowing; Testing & Commissioning lights every system and
ticks each test point. The discipline names and descriptions are the ones on the MEP detail page.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/services/svc_mep.py
"""
import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
INK = "58,45,37"  # dark walnut, as rgb for the drawing's tints


# ── the drawing (viewBox 1200 x 650) ────────────────────────────────────────────
ARCH = [  # building fabric
    "M20 600 H1180", "M60 40 V60 M1140 40 V60", "M540 392 V470 H550 V392", "M760 124 V230 H770 V124",
]
CUT = [  # slabs and walls cut by the section: outlined, then filled (poché)
    "M60 600 H1140 V614 H60 Z", "M60 330 H1140 V344 H60 Z", "M60 60 H1140 V76 H60 Z",
    "M60 76 H74 V600 H60 Z", "M1126 76 H1140 V600 H1126 Z", "M540 392 V470 H550 V392 Z", "M760 124 V230 H770 V124 Z",
]
GROUND = " ".join(f"M{x} 618 l-12 12" for x in range(40, 1181, 16))
CEILINGS = ["M74 124 H1126", "M74 392 H1126"]
FURN = [  # quiet furniture outlines
    "M150 600 V560 H170 V545 H320 V560 H340 V600", "M170 575 H320", "M370 600 V578 H450 V600",  # living
    "M900 600 V545 H1110 V600 M900 556 H1110 M960 545 V538 H1000 V545", "M640 600 V560 H800 V600",  # kitchen
    "M200 330 V300 H215 V270 H230 V300 H420 V330 M230 300 H420", "M440 330 V306 H476 V330",  # bedroom
    "M980 330 V300 H1110 V330 M990 300 V310 H1100 V300", "M820 330 V286 H900 V330 M834 250 H886 V276 H834 Z",  # bath
]
ROOF = ["M940 24 H1010 V60 H940 Z", "M1030 24 H1100 V60 H1030 Z", "M975 42 m-12 0 a12 12 0 1 0 24 0 a12 12 0 1 0 -24 0",
        "M1065 42 m-12 0 a12 12 0 1 0 24 0 a12 12 0 1 0 -24 0", "M780 14 H860 V60 H780 Z", "M780 26 H860"]


def drops(xs, y1, y2, cap=0):
    out = []
    for x in xs:
        out.append(f"M{x} {y1} V{y2}")
        if cap:
            out.append(f"M{x - cap} {y2} H{x + cap}")
    return " ".join(out)


def heads(xs, y1, y2):
    return " ".join(f"M{x} {y1} V{y2} M{x - 5} {y2 + 6} L{x} {y2} L{x + 5} {y2 + 6}" for x in xs)


def lamps(xs, y1, y2):
    return " ".join(f"M{x} {y1} V{y2 - 5} M{x} {y2} m-5 0 a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0" for x in xs)


def boxes(xs, y, s=8):
    return " ".join(f"M{x - s / 2} {y} h{s} v{s} h-{s} Z" for x in xs)


SYSTEMS = [  # key, main runs (flow along these), fittings (drawn, never flow), stroke width, flow dash
    ("hvac",
     ["M1060 60 V356", "M1060 88 H110", "M1060 356 H110"],
     drops([220, 420, 620, 860], 88, 124, 16) + " " + drops([200, 400, 660, 900], 356, 392, 16),
     3.2, "10 12"),
    ("power",
     ["M1109 470 V110", "M1109 378 H130", "M1109 110 H130", "M1109 540 V580 H160"],
     "M1100 470 H1118 V540 H1100 Z " + lamps([240, 440, 700, 980], 378, 392) + " " + lamps([260, 520, 860, 1040], 110, 124)
     + " " + drops([300, 760], 580, 572) + " " + boxes([300, 760], 564),
     1.6, "3 9"),
    ("water",
     ["M820 60 V540 H1000 V560", "M820 300 H1040 V306", "M860 300 V286", "M1040 330 V630 H1180", "M860 330 V344 H1040", "M1000 600 V630"],
     "M1000 560 h-14 M1000 560 h14",
     2.2, "6 10"),
    ("fire",
     ["M96 614 V100 H1100", "M96 368 H1100"],
     heads([180, 380, 580, 800, 1000], 100, 118) + " " + heads([160, 360, 620, 840, 1040], 368, 386),
     2, "2 7"),
    ("data",
     ["M112 450 V116 H1100", "M112 384 H1150 V404", "M112 116 H40 V140"],
     "M80 450 H100 V540 H80 Z M86 470 H94 M86 490 H94 M86 510 H94 " + boxes([400, 900], 120) + " " + boxes([300, 820], 388)
     + " M1142 404 h18 v10 h-18 Z M32 140 h18 v10 h-18 Z M86 520 V528",
     1.3, "8 4 2 4"),
]
EQUIP = {  # where each discipline's plant is named, (x, y, anchor)
    "hvac": [(1020, 16, "middle")], "power": [(1094, 506, "end")], "water": [(770, 44, "end")],
    "fire": [(104, 470, "start")], "data": [(122, 500, "start")],
}
TICKS = [(1020, 72), (1109, 556), (820, 72), (96, 628), (90, 556)]  # commissioning points
ROOMS = [(300, 430), (840, 430), (360, 160), (950, 160)]


def drawing(c, ar):
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    fs = 18 if ar else 14
    g = ['<g class="mx-cut">' + "".join(f'<path d="{d}"/>' for d in CUT) + "</g>",
         f'<path class="mx-ground" d="{GROUND}"/>',
         '<g class="mx-arch">' + "".join(f'<path d="{d}" pathLength="1"/>' for d in ARCH + CUT + ROOF) + "</g>",
         '<g class="mx-ceil">' + "".join(f'<path d="{d}"/>' for d in CEILINGS) + "</g>",
         '<g class="mx-furn">' + "".join(f'<path d="{d}"/>' for d in FURN) + "</g>"]
    rooms = "".join(f'<text x="{x}" y="{y}" text-anchor="middle">{c["rooms"][i]}</text>' for i, (x, y) in enumerate(ROOMS))
    g.append(f'<g class="mx-rooms" style="font-family:{font};font-size:{fs}px">{rooms}</g>')
    for i, (key, runs, fit, w, dash) in enumerate(SYSTEMS):
        base = "".join(f'<path d="{d}" pathLength="1"/>' for d in runs)
        flow = "".join(f'<path d="{d}"/>' for d in runs)
        lab = "".join(f'<text x="{x}" y="{y}" text-anchor="{a}">{c["equip"][i]}</text>' for x, y, a in EQUIP[key])
        g.append(f'<g class="mx-sys mx-sys--{key}" style="--w:{w};--dash:{dash};--d:{0.5 + i * 0.25}s">'
                 f'<g class="mx-base">{base}</g><path class="mx-fit" d="{fit}"/><g class="mx-flow">{flow}</g>'
                 f'<g class="mx-lab" style="font-family:{font};font-size:{fs}px">{lab}</g></g>')
    ticks = "".join(f'<path d="M{x - 6} {y} l4 5 l9 -11" pathLength="1"/>' for x, y in TICKS)
    g.append(f'<g class="mx-ticks">{ticks}</g>')
    return f'<svg class="mx-svg" viewBox="0 0 1200 650" role="img" aria-label="{c["svg"]}">{"".join(g)}</svg>'


C = {
    "en": dict(
        eyebrow="Our Engineering Services", h2="The Foundation of High-Performance Environments",
        body="True luxury and functionality depend on the invisible systems that keep a building running. Our Engineering &amp; MEP (Mechanical, Electrical, and Plumbing) services provide the high-performance infrastructure required to bring your interior vision to life, seamlessly integrated into every design and fit-out we deliver.",
        cta="Explore Engineering &amp; MEP", href="/services-mep",
        keys=[("HVAC Systems", "Air conditioning, ventilation, ductwork, and testing for consistent year-round comfort."),
              ("Electrical Systems", "Power distribution, lighting, emergency power, and cable management, engineered to code."),
              ("Plumbing Systems", "Water supply, drainage, sewage, and pump installations engineered for reliability."),
              ("Fire Fighting Systems", "Fire alarms, suppression, sprinkler networks, and full Civil Defense compliance."),
              ("Low Current Systems", "Structured cabling, CCTV, access control, and smart building integration."),
              ("Testing &amp; Commissioning", "Functional testing, performance validation, and certified handover documentation.")],
        rooms=["Living", "Kitchen", "Bedroom", "Bath"],
        equip=["Condensing units", "Distribution board", "Water tank", "Fire riser", "Data cabinet"],
        sheet=["FurnishIQ", "Section A–A", "MEP coordination", "Concept"],
        svg="Section drawing of a two-storey building showing HVAC, electrical, plumbing, fire fighting and low current systems",
        scroll="Scroll the drawing sideways",
    ),
    "ar": dict(
        eyebrow="خدماتنا الهندسية", h2="أساس البيئات عالية الأداء",
        body="تعتمد الفخامة الحقيقية والوظائفية على الأنظمة غير المرئية التي تُبقي المبنى يعمل. تقدم خدماتنا الهندسية والأنظمة الكهروميكانيكية (الميكانيكية والكهربائية والصحية) البنية التحتية عالية الأداء اللازمة لتحقيق رؤيتك الداخلية، مدمجة بسلاسة في كل تصميم وتشطيب ننفذه.",
        cta="استكشف الهندسة والأنظمة الكهروميكانيكية", href="/ar/services-mep",
        keys=[("أنظمة التكييف والتهوية", "التكييف والتهوية ومجاري الهواء والاختبار لراحة دائمة على مدار العام."),
              ("الأنظمة الكهربائية", "توزيع الطاقة والإنارة وطاقة الطوارئ وإدارة الكابلات، وفق الأكواد المعتمدة."),
              ("أنظمة السباكة", "إمدادات المياه والصرف والصرف الصحي وتركيب المضخات بموثوقية عالية."),
              ("أنظمة مكافحة الحريق", "إنذار الحريق والإطفاء وشبكات الرشاشات والامتثال الكامل لاشتراطات الدفاع المدني."),
              ("أنظمة التيار المنخفض", "الكابلات المهيكلة وكاميرات المراقبة والتحكم في الدخول وتكامل المباني الذكية."),
              ("الاختبار والتشغيل", "الاختبار الوظيفي والتحقق من الأداء ووثائق التسليم المعتمدة.")],
        rooms=["المعيشة", "المطبخ", "غرفة النوم", "الحمام"],
        equip=["وحدات التكثيف", "لوحة التوزيع", "خزان المياه", "صاعد الحريق", "خزانة البيانات"],
        sheet=["FurnishIQ", "مقطع أ–أ", "تنسيق الأنظمة الكهروميكانيكية", "تصور مفاهيمي"],
        svg="مقطع لمبنى من طابقين يوضح أنظمة التكييف والكهرباء والسباكة ومكافحة الحريق والتيار المنخفض",
        scroll="اسحب الرسم أفقياً",
    ),
}
ARROW_EN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
ARROW_AR = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>'
TONES = ["#8B6B4A", "#1F1F1F", "#5B4636", "#3A2D25", "#8B6B4A"]  # one brand tone per discipline


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    keys = "\n".join(
        f'        <li><button type="button" class="mx-key" aria-pressed="false"><b>0{i + 1}</b><span class="mx-kt">{t}</span><span class="mx-kd"><span>{d}</span></span></button></li>'
        for i, (t, d) in enumerate(c["keys"]))
    tones = "\n".join(f"    [data-svc-mep] .mx-sys--{k}{{--tone:{TONES[i]};}}" for i, (k, *_) in enumerate(SYSTEMS))
    sheet = "".join(f"<span>{t}</span>" for t in c["sheet"])
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━ 3. ENGINEERING & MEP ━ -->
<section id="mep" data-screen-label="Engineering &amp; MEP" data-svc-mep{' dir="rtl"' if ar else ''} style="scroll-margin-top:var(--fiq-svc-offset,132px);background:#F5F2ED;color:#3A2D25;position:relative;padding:clamp(64px,8vw,100px) clamp(24px,5vw,80px);overflow:clip;">
  <style>
    [data-svc-mep] .mx-wrap{{max-width:1280px;margin:0 auto;}}
    [data-svc-mep] .mx-head{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:clamp(32px,5vw,88px);align-items:end;margin-bottom:clamp(40px,4.4vw,64px);}}
    [data-svc-mep] .mx-eyebrow{{display:flex;align-items:center;gap:16px;margin-bottom:24px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    [data-svc-mep] .mx-eyebrow i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    [data-svc-mep] .mx-h2{{font-family:{font};font-weight:500;font-size:clamp(32px,3.8vw,54px);line-height:1.08;letter-spacing:{'0' if ar else '-0.015em'};color:#1F1F1F;margin:0;text-wrap:balance;}}
    [data-svc-mep] .mx-body{{font-family:{font};font-size:{'16px' if ar else '15px'};line-height:1.85;color:#5B4636;margin:0 0 28px;}}
    [data-svc-mep] .mx-cta{{display:inline-flex;align-items:center;gap:12px;padding:17px 30px;background:#3A2D25;color:#F5F2ED;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;border:1px solid #3A2D25;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-mep] .mx-cta:hover,[data-svc-mep] .mx-cta:focus-visible{{background:transparent;color:#3A2D25;}}
    [data-svc-mep] .mx-sheet{{position:relative;border:1px solid rgba({INK},0.22);background:#FBF9F6;padding:clamp(16px,2vw,28px) clamp(16px,2vw,28px) 0;}}
    [data-svc-mep] .mx-pan{{overflow-x:auto;scrollbar-width:none;}}
    [data-svc-mep] .mx-pan::-webkit-scrollbar{{display:none;}}
    [data-svc-mep] .mx-svg{{display:block;width:100%;height:auto;min-width:720px;direction:ltr;overflow:visible;}}
    [data-svc-mep] .mx-svg path{{fill:none;stroke-linecap:square;stroke-linejoin:miter;}}
    [data-svc-mep] .mx-arch path{{stroke:rgba({INK},0.5);stroke-width:1.4;stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset 2.2s {EASE};}}
    [data-svc-mep].is-in .mx-arch path{{stroke-dashoffset:0;}}
    [data-svc-mep] .mx-svg .mx-cut path{{fill:rgba({INK},0.13);stroke:none;opacity:0;transition:opacity 1.2s {EASE} 1s;}}
    [data-svc-mep] .mx-svg .mx-ground{{stroke:rgba({INK},0.22);stroke-width:1;opacity:0;transition:opacity 1.2s {EASE} 1.2s;}}
    [data-svc-mep].is-in .mx-cut path,[data-svc-mep].is-in .mx-ground{{opacity:1;}}
    [data-svc-mep] .mx-ceil path{{stroke:rgba({INK},0.3);stroke-width:1;stroke-dasharray:6 6;opacity:0;transition:opacity 1s {EASE} 1.2s;}}
    [data-svc-mep] .mx-furn path{{stroke:rgba({INK},0.28);stroke-width:1;opacity:0;transition:opacity 1.2s {EASE} 1.4s;}}
    [data-svc-mep] .mx-rooms text{{fill:rgba({INK},0.5);letter-spacing:{'0' if ar else '0.2em'};text-transform:uppercase;opacity:0;transition:opacity 1s {EASE} 1.6s;}}
    [data-svc-mep].is-in .mx-ceil path,[data-svc-mep].is-in .mx-furn path,[data-svc-mep].is-in .mx-rooms text{{opacity:1;}}
{tones}
    [data-svc-mep] .mx-sys{{transition:opacity 0.6s {EASE};}}
    [data-svc-mep] .mx-base path{{stroke:var(--tone);stroke-width:var(--w);stroke-dasharray:1;stroke-dashoffset:1;opacity:0.55;transition:stroke-dashoffset 2s {EASE} var(--d),opacity 0.6s {EASE};}}
    [data-svc-mep].is-in .mx-base path{{stroke-dashoffset:0;}}
    [data-svc-mep] .mx-fit{{stroke:var(--tone);stroke-width:1.3;opacity:0;transition:opacity 0.8s {EASE} calc(var(--d) + 1.2s);}}
    [data-svc-mep].is-in .mx-fit{{opacity:0.55;}}
    [data-svc-mep] .mx-flow path{{stroke:var(--tone);stroke-width:calc(var(--w) * 1.5px + 1.6px);stroke-dasharray:var(--dash);opacity:0;animation:mx-flow 1.4s linear infinite;animation-play-state:paused;transition:opacity 0.5s {EASE};}}
    [data-svc-mep] .mx-lab text{{fill:var(--tone);letter-spacing:{'0' if ar else '0.16em'};text-transform:uppercase;opacity:0;transition:opacity 0.5s {EASE};}}
    @keyframes mx-flow{{to{{stroke-dashoffset:-44;}}}}
    [data-svc-mep].has-pick .mx-sys{{opacity:0.16;}}
    [data-svc-mep] .mx-sys.is-on{{opacity:1!important;}}
    [data-svc-mep] .mx-sys.is-on .mx-base path{{opacity:0.9;}}
    [data-svc-mep] .mx-sys.is-on .mx-fit{{opacity:1;transition-delay:0s;}}
    [data-svc-mep] .mx-sys.is-on .mx-flow path{{opacity:1;animation-play-state:running;}}
    [data-svc-mep] .mx-sys.is-on .mx-lab text{{opacity:1;}}
    [data-svc-mep] .mx-ticks path{{stroke:#8B6B4A;stroke-width:2.4;stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset 0.5s {EASE};}}
    [data-svc-mep].is-test .mx-ticks path{{stroke-dashoffset:0;}}
    [data-svc-mep].is-test .mx-ticks path:nth-child(2){{transition-delay:0.15s;}}
    [data-svc-mep].is-test .mx-ticks path:nth-child(3){{transition-delay:0.3s;}}
    [data-svc-mep].is-test .mx-ticks path:nth-child(4){{transition-delay:0.45s;}}
    [data-svc-mep].is-test .mx-ticks path:nth-child(5){{transition-delay:0.6s;}}
    [data-svc-mep] .mx-block{{display:flex;justify-content:flex-end;margin:0 calc(clamp(16px,2vw,28px) * -1);border-top:1px solid rgba({INK},0.22);}}
    [data-svc-mep] .mx-block span{{padding:10px 16px;border-inline-start:1px solid rgba({INK},0.22);font-family:{font};font-size:{'12px' if ar else '9px'};letter-spacing:{'normal' if ar else '0.22em'};text-transform:uppercase;color:#8B6B4A;white-space:nowrap;}}
    [data-svc-mep] .mx-block span:first-child{{margin-inline-end:auto;border-inline-start:0;color:#3A2D25;}}
    [data-svc-mep] .mx-scroll{{display:none;}}
    [data-svc-mep] .mx-main{{display:grid;grid-template-columns:minmax(0,8fr) minmax(0,4fr);gap:clamp(28px,3.4vw,48px);align-items:start;}}
    [data-svc-mep] .mx-keys{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;border-bottom:1px solid rgba({INK},0.18);}}
    [data-svc-mep] .mx-key{{position:relative;display:grid;grid-template-columns:auto 1fr;column-gap:14px;width:100%;padding:16px 0;background:none;border:0;border-top:1px solid rgba({INK},0.18);text-align:start;cursor:pointer;font:inherit;color:inherit;opacity:0.62;transition:opacity 0.4s {EASE};}}
    [data-svc-mep] .mx-key::before{{content:"";position:absolute;top:-1px;inset-inline:0;height:2px;background:#8B6B4A;transform:scaleX(0);transform-origin:{'100%' if ar else '0%'} 50%;transition:transform 0.6s {EASE};}}
    [data-svc-mep] .mx-key:hover,[data-svc-mep] .mx-key.is-on{{opacity:1;}}
    [data-svc-mep] .mx-key.is-on::before{{transform:scaleX(1);}}
    [data-svc-mep] .mx-key:focus-visible{{outline:1px solid #8B6B4A;outline-offset:4px;}}
    [data-svc-mep] .mx-key b{{font-family:'Lama Sans',sans-serif;font-weight:500;font-size:11px;letter-spacing:0.18em;color:#8B6B4A;padding-top:3px;}}
    [data-svc-mep] .mx-kt{{font-family:{font};font-size:{'15px' if ar else '14px'};line-height:1.35;color:#1F1F1F;}}
    [data-svc-mep] .mx-kd{{grid-column:2;display:grid;grid-template-rows:0fr;transition:grid-template-rows 0.6s {EASE};font-family:{font};font-size:{'13px' if ar else '12px'};line-height:1.6;color:#5B4636;}}
    [data-svc-mep] .mx-kd span{{overflow:hidden;}}
    [data-svc-mep] .mx-key.is-on .mx-kd{{grid-template-rows:1fr;}}
    [data-svc-mep] .mx-key.is-on .mx-kd span{{padding-top:8px;}}
    [data-svc-mep] .mx-rise{{opacity:0;transform:translateY(24px);transition:opacity 0.9s {EASE},transform 0.9s {EASE};}}
    [data-svc-mep].is-in .mx-rise{{opacity:1;transform:none;}}
    [data-svc-mep].is-in .mx-rise--2{{transition-delay:0.12s;}}
    @media(max-width:1100px){{
      [data-svc-mep] .mx-main{{grid-template-columns:1fr;}}
      [data-svc-mep] .mx-keys{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0 clamp(16px,2vw,28px);border-bottom:0;}}
      [data-svc-mep] .mx-kd{{grid-template-rows:1fr;}}
      [data-svc-mep] .mx-kd span{{padding-top:8px;}}
    }}
    @media(max-width:900px){{
      [data-svc-mep] .mx-head{{grid-template-columns:1fr;}}
      [data-svc-mep] .mx-scroll{{display:block;margin:10px 0 0;font-family:{font};font-size:{'12px' if ar else '10px'};color:#8B6B4A;}}
    }}
    @media(max-width:600px){{
      [data-svc-mep] .mx-keys{{grid-template-columns:repeat(2,minmax(0,1fr));}}
      [data-svc-mep] .mx-cta{{width:100%;justify-content:center;box-sizing:border-box;}}
      [data-svc-mep] .mx-block span:not(:first-child):not(:last-child){{display:none;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-svc-mep] *{{transition:none!important;animation:none!important;}}
      [data-svc-mep] .mx-rise{{opacity:1;transform:none;}}
    }}
  </style>
  <div class="mx-wrap">
    <div class="mx-head">
      <div class="mx-rise">
        <div class="mx-eyebrow"><i></i>{c['eyebrow']}</div>
        <h2 class="mx-h2">{c['h2']}</h2>
      </div>
      <div class="mx-rise mx-rise--2">
        <p class="mx-body">{c['body']}</p>
        <a class="mx-cta" href="{c['href']}">{c['cta']}{ARROW_AR if ar else ARROW_EN}</a>
      </div>
    </div>
    <div class="mx-main">
      <div>
        <div class="mx-sheet">
          <div class="mx-pan">{drawing(c, ar)}</div>
          <div class="mx-block" aria-hidden="true">{sheet}</div>
        </div>
        <p class="mx-scroll">{c['scroll']}</p>
      </div>
      <ol class="mx-keys">
{keys}
      </ol>
    </div>
  </div>
</section>
"""


JS = """    // ── SERVICES, MEP: THE BUILDING'S NERVOUS SYSTEM ────────────────────────
    {
      const sec = document.querySelector('[data-svc-mep]');
      if (sec) {
        const keys = Array.from(sec.querySelectorAll('.mx-key')), sys = Array.from(sec.querySelectorAll('.mx-sys'));
        const last = keys.length - 1;  // testing & commissioning lights every system
        let auto = !reduced, timer = null, idx = 0, visible = false;
        const pick = (n) => {
          keys.forEach((k, i) => { k.classList.toggle('is-on', i === n); k.setAttribute('aria-pressed', i === n ? 'true' : 'false'); });
          sys.forEach((g, i) => g.classList.toggle('is-on', n === last || i === n));
          sec.classList.toggle('has-pick', n !== null);
          sec.classList.toggle('is-test', n === last);
        };
        const stop = () => { auto = false; clearInterval(timer); };
        keys.forEach((k, i) => {
          k.addEventListener('mouseenter', () => { stop(); pick(i); });
          k.addEventListener('focus', () => { stop(); pick(i); });
          k.addEventListener('click', () => { stop(); pick(i); });
        });
        const tick = () => { if (auto && visible) { pick(idx % keys.length); idx++; } };
        new IntersectionObserver((es) => {
          es.forEach((e) => {
            visible = e.isIntersecting;
            if (visible) {
              sec.classList.add('is-in');
              if (auto && !timer) setTimeout(() => { tick(); timer = setInterval(tick, 3400); }, 3200);
            }
          });
        }, { threshold: 0.2 }).observe(sec);
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

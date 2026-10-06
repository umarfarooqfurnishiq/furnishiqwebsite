"""Services, Our Process: from a line on paper to a room you live in.

One project built live on a dark drafting board, scrubbed by the scroll. The drawing is the plan of the
council room of the Family Office concept, a workplace the rest of the page does not show. Brief: the shell
traces itself in with its dimensions and three notes from the brief. Planning: the walls fill, the windows onto
the courtyard and the far door cut in, and a circulation path runs in from the door. Design: the long table,
its chairs, the rug and the pendant draw in with a strip of the materials. Procurement: every piece takes its
schedule tag. Build: the beams and services overlay the plan and the inspection ticks land. Handover: the
plan tilts back and dissolves into the finished room. Earlier
stages stay on the board, dimmed, so the project visibly accumulates. A panel carries each stage, what
happens there and the disciplines involved; once the room is handed over, the panel offers the next step,
starting a project. On phones the stages play on their own and answer to the tabs.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/services/svc_process.py
"""
import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
N = 6
# the stages each discipline works in (1-based); every discipline is at the table from the brief
ROWS = [(1, 2, 3, 4), (1, 4, 5, 6), (1, 2, 3, 4, 5, 6), (1, 3, 4, 5, 6)]
PHOTO = "family-office-council-room-oak-table"
C = {
    "en": dict(
        eyebrow="Our Process", h2="A Proven Process, Refined on Every Project",
        sub="Six stages, one accountable team, whichever service leads.",
        stages=["Brief", "Planning", "Design", "Procurement", "Build", "Handover"],
        descs=["The space, the timeline, the budget and the ambition, agreed with every discipline at the table.",
               "How the space will be used, footfall, service routes and daily movement, studied before any layout is drawn.",
               "Layouts, materials, lighting and systems developed together into photoreal 3D renders you approve on screen.",
               "Every material, system and piece specified against the approved renders before a purchase order is raised.",
               "Fit-out and MEP works delivered by one site team and inspected against the approved specification throughout.",
               "Systems tested and commissioned, furniture placed and styled, and the space handed over ready for use."],
        rows=["Interior Design", "Fit-Out", "Engineering &amp; MEP", "Furniture"],
        involved="Disciplines involved", tabs="Project stages",
        notes=["ONE TABLE FOR THE COUNCIL", "LIGHT FROM THE COURTYARD", "A QUIET ROOM FOR DECISIONS"],
        zones=["COUNCIL", "COURTYARD"],
        mats=["OAK", "LIMESTONE", "LEATHER", "TIMBER", "WOOL RUG"],
        build=["TIMBER BEAMS", "LINEAR DIFFUSER", "INSPECTED"],
        sheet="CONCEPT · COUNCIL ROOM · PLAN", cap="Concept visualisation",
        alt="The finished council room: a long oak table with leather chairs beneath timber beams, and a window onto the olive courtyard",
        go="Start Your Project", go_href="/contact",
    ),
    "ar": dict(
        eyebrow="منهجية عملنا", h2="منهجية مُثبتة، تُصقل في كل مشروع",
        sub="ست مراحل وفريق واحد مسؤول، أياً كانت الخدمة التي تقود المشروع.",
        stages=["الإحاطة", "التخطيط", "التصميم", "التوريد", "التنفيذ", "التسليم"],
        descs=["المساحة والجدول الزمني والميزانية والطموح، يُتفق عليها بحضور كل التخصصات.",
               "دراسة طريقة استخدام المساحة، من حركة الزوار ومسارات الخدمة إلى الحركة اليومية، قبل رسم أي مخطط.",
               "تطوير المخططات والخامات والإضاءة والأنظمة معاً في تصورات ثلاثية الأبعاد واقعية تعتمدها على الشاشة.",
               "تحديد كل خامة ونظام وقطعة وفق التصورات المعتمدة قبل إصدار أي أمر شراء.",
               "أعمال التشطيب والأنظمة الكهروميكانيكية بفريق موقع واحد، مع فحص المطابقة للمواصفات المعتمدة طوال التنفيذ.",
               "اختبار الأنظمة وتشغيلها، وتموضع الأثاث وتنسيقه، وتسليم المساحة جاهزة للاستخدام."],
        rows=["التصميم الداخلي", "التشطيبات", "الهندسة والأنظمة الكهروميكانيكية", "الأثاث"],
        involved="التخصصات المشاركة", tabs="مراحل المشروع",
        notes=["طاولة واحدة للمجلس", "ضوء من الفناء", "غرفة هادئة للقرارات"],
        zones=["المجلس", "الفناء"],
        mats=["بلوط", "حجر جيري", "جلد", "خشب", "سجاد صوف"],
        build=["عوارض خشبية", "ناشر هواء خطي", "تم الفحص"],
        sheet="مفهوم · قاعة المجلس · مخطط", cap="تصور مفاهيمي",
        alt="قاعة المجلس المنجزة: طاولة طويلة من البلوط بمقاعد جلدية تحت عوارض خشبية، ونافذة تطل على فناء الزيتون",
        go="ابدأ مشروعك", go_href="/ar/contact",
    ),
}
ARROW_EN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
ARROW_AR = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>'


# ── The plan, in a 1000 x 640 sheet. The camera of the photograph stands at the left end looking along the room:
# walls 106..894 x 136..504, room 120..880 x 150..490; the courtyard windows on the bottom wall, the door far right
def d(path, k=0):  # a line that draws in with its stage
    return f'<path class="d" style="--o:{k}" d="{path}" pathLength="1"/>'


def f(inner, k=0, cls=""):  # marks that fade in once the stage's lines are down
    return f'<g class="f {cls}" style="--o:{k}">{inner}</g>'


def label(x, y, text, anchor="middle", cls="lb"):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{text}</text>'


def chair(x, y, side):  # a seat 30 x 26 with its back on the side away from the table
    by = y + 26 if side > 0 else y
    return f"M{x + 5},{y}H{x + 25}Q{x + 30},{y} {x + 30},{y + 5}V{y + 21}Q{x + 30},{y + 26} {x + 25},{y + 26}H{x + 5}Q{x},{y + 26} {x},{y + 21}V{y + 5}Q{x},{y} {x + 5},{y}ZM{x + 2},{by + (-3 if side > 0 else 3)}H{x + 28}"


def plan(c):
    G = []
    # 1 Brief: the shell, its dimensions, a north point and three notes from the brief
    n = c["notes"]
    G.append(
        d("M106,136H894V504H106Z", 0) + d("M106,108H894M106,102V114M894,102V114", 1) + d("M72,136V504M66,136H78M66,504H78", 1)
        + d("M952,178V146M944,158L952,146L960,158", 2)
        + f(label(952, 196, "N", cls="lb lb--n"), 2)
        + f('<circle cx="510" cy="320" r="3.5" class="dot"/><path d="M510,316V290"/>' + label(510, 278, n[0], cls="lb note"), 3, "nt")
        + f('<circle cx="430" cy="486" r="3.5" class="dot"/><path d="M430,482V456"/>' + label(430, 446, n[1], cls="lb note"), 4, "nt")
        + f('<circle cx="140" cy="184" r="3.5" class="dot"/><path d="M144,184H170"/>' + label(178, 188, n[2], "start", "lb note"), 5, "nt"))
    # 2 Planning: walls hatched, the courtyard windows, the far door and its swing, the arched recesses, the way in
    z = c["zones"]
    G.append(
        f('<path class="wall" d="M106,136H894V504H106ZM120,150V490H880V150Z" fill-rule="evenodd"/>', 0)
        + f('<rect class="cut" x="300" y="487" width="260" height="20"/><rect class="cut" x="650" y="487" width="60" height="20"/>'
            '<rect class="cut" x="740" y="487" width="60" height="20"/><rect class="cut" x="877" y="330" width="20" height="60"/>', 1)
        + d("M300,494H560M300,500H560M300,490V504M560,490V504", 1)
        + d("M650,497H710M740,497H800", 2) + f('<path d="M660,490V504M670,490V504M680,490V504M690,490V504M700,490V504M750,490V504M760,490V504M770,490V504M780,490V504M790,490V504"/>', 3)
        + d("M880,330H822", 2) + f('<path class="dash" d="M822,330A58,58 0 0 0 880,388"/>', 3)
        + d("M880,196h-10a10,10 0 0 1 0,-0.01M880,196V178h10V230h-10M880,248V300h10V248Z", 2)
        + d("M856,372C800,428 620,432 300,428", 4) + f('<path d="M312,420L298,428L312,436"/>', 5)
        + f('<circle cx="430" cy="562" r="28"/><circle cx="430" cy="562" r="14"/>' + label(560, 566, z[1], "start", "lb zone"), 4)
        + f(label(510, 458, z[0], cls="lb zone"), 5))
    # 3 Design: the rug, the long table and its chairs, the pendant, the coffee set, the limestone floor, the materials
    tiles = "".join(f"M{x},152V488" for x in range(158, 880, 38)) + "".join(f"M122,{y}H878" for y in range(188, 490, 38))
    xs = range(250, 750, 54)
    seats = "".join(chair(x, 256, -1) for x in xs) + "".join(chair(x, 358, 1) for x in xs)
    sw = [("#A57A4E", 0), ("#DCCDB2", 1), ("#5A3E2E", 2), ("#C8A67C", 3), ("#CBB89A", 4)]
    strip = "".join(f'<rect class="sw" x="{150 + i * 150}" y="598" width="16" height="16" style="fill:{col}"/>' + label(174 + i * 150, 611, c["mats"][i], "start", "lb mat") for col, i in sw)
    G.append(
        f(f'<path class="plank" d="{tiles}"/>', 0)
        + d("M180,235H840V405H180Z", 0) + f('<path class="dash" d="M194,249H826V391H194Z"/>', 3)
        + d("M230,290H800V350H230Z", 1) + f('<path class="dash" d="M238,298H792V342H238Z"/>', 3)
        + d(seats, 2) + d("M186,305H212V335H186ZM189,305V335", 2)
        + d("M569,320A9,9 0 1 1 551,320A9,9 0 1 1 569,320M554,320H566M560,314V326", 3)
        + f('<circle cx="470" cy="320" r="6"/><circle cx="486" cy="314" r="3.5"/><circle cx="486" cy="327" r="3.5"/>', 4)
        + f(strip, 5))
    # 4 Procurement: every piece takes its numbered schedule tag
    tags = [(628, 320), (373, 269), (628, 371), (206, 392), (560, 320), (470, 320), (725, 524)]
    nums = ["01", "02", "02", "03", "04", "05", "06"]
    G.append("".join(f(f'<circle class="tag" cx="{x}" cy="{y}" r="13"/>' + label(x, y + 4, nums[i], cls="lb tg"), i) for i, (x, y) in enumerate(tags))
             + d("M725,511V500", 5))
    # 5 Build: beams, diffusers, wall washers and floor boxes over the plan, and the inspections signed off
    b = c["build"]
    beams = "".join(f"M{x - 7},150V490M{x + 7},150V490" for x in (300, 500, 700))
    washers = "".join(f'<circle cx="{x}" cy="162" r="5"/>' for x in (200, 400, 600, 800))
    boxes = "".join(f'<path d="M{x - 6},{314}h12v12h-12zM{x - 6},314l12,12M{x + 6},314l-12,12"/>' for x in (340, 760))
    ticks = "".join(f'<circle class="ok" cx="{x}" cy="{y}" r="13"/><path d="M{x - 5},{y}L{x - 1.5},{y + 4}L{x + 5.5},{y - 4}"/>' for x, y in ((250, 212), (836, 212), (390, 454)))
    G.append(
        f(f'<path class="dash" d="{beams}"/>', 0) + d("M330,176H470M330,182H470M560,176H700M560,182H700", 1)
        + f(washers + boxes, 2)
        + f(label(600, 228, b[0], cls="lb sv") + label(400, 198, b[1], cls="lb sv"), 3)
        + f(ticks + label(836, 244, b[2], cls="lb sv"), 4))
    return "".join(f'<g class="pr-g" data-g="{k}">{g}</g>' for k, g in enumerate(G))


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    caps = "normal" if ar else "0.22em"
    small = "12px" if ar else "9px"
    arrow = ARROW_AR if ar else ARROW_EN
    PAD = "clamp(24px,5vw,80px)"
    go = f'\n            <a class="pr-go" href="{c["go_href"]}">{c["go"]}{arrow}</a>'
    panes = "\n".join(f'''          <div class="pr-pane{' is-on' if k == 0 else ''}" id="pr-pane-{k}" role="tabpanel" aria-labelledby="pr-tab-{k}" data-pane="{k}">
            <p class="pr-count"><span dir="ltr"><b>0{k + 1}</b> / 0{N}</span></p>
            <h3 class="pr-name">{c['stages'][k]}</h3>
            <p class="pr-desc">{c['descs'][k]}</p>
            <p class="pr-lbl">{c['involved']}</p>
            <ul class="pr-chips">{''.join(f'<li>{c["rows"][r]}</li>' for r, st in enumerate(ROWS) if k + 1 in st)}</ul>{go if k == N - 1 else ''}
          </div>''' for k in range(N))
    tabs = "\n".join(f'''          <button type="button" class="pr-tab" role="tab" id="pr-tab-{k}" data-pr="{k}" aria-selected="{'true' if k == 0 else 'false'}" aria-controls="pr-pane-{k}" tabindex="{0 if k == 0 else -1}"><i class="pr-bar" aria-hidden="true"></i><span class="pr-tn" dir="ltr">0{k + 1}</span><span class="pr-tt">{c['stages'][k]}</span></button>''' for k in range(N))
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6. OUR PROCESS ━ -->
<section id="process" data-screen-label="Our Process" data-svc-process{' dir="rtl"' if ar else ''} style="scroll-margin-top:var(--fiq-svc-offset,132px);background:#F5F2ED;color:#3A2D25;position:relative;padding:clamp(64px,8vw,100px) {PAD} 0;overflow:clip;">
  <style>
    @property --pr-t{{syntax:'<number>';inherits:true;initial-value:0;}}
    @property --pr-h{{syntax:'<number>';inherits:true;initial-value:0;}}
    [data-svc-process] .pr-wrap{{max-width:1280px;margin:0 auto;}}
    [data-svc-process] .pr-head{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:clamp(32px,5vw,88px);align-items:end;margin-bottom:clamp(40px,4.4vw,64px);}}
    [data-svc-process] .pr-eyebrow{{display:flex;align-items:center;gap:16px;margin-bottom:24px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    [data-svc-process] .pr-eyebrow i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    [data-svc-process] .pr-h2{{font-family:{font};font-weight:500;font-size:clamp(32px,3.8vw,54px);line-height:1.08;letter-spacing:{'0' if ar else '-0.015em'};color:#1F1F1F;margin:0;text-wrap:balance;}}
    [data-svc-process] .pr-sub{{font-family:{font};font-weight:500;font-size:{'clamp(22px,2vw,28px)' if ar else 'clamp(20px,1.9vw,26px)'};line-height:1.4;letter-spacing:{'0' if ar else '-0.005em'};text-wrap:balance;max-width:{'18em' if ar else '30ch'};color:#3A2D25;margin:0;}}
    [data-svc-process] .pr-rise{{opacity:0;transform:translateY(24px);transition:opacity 0.9s {EASE},transform 0.9s {EASE};}}
    [data-svc-process].is-in .pr-rise{{opacity:1;transform:none;}}
    [data-svc-process].is-in .pr-rise--2{{transition-delay:0.12s;}}
    [data-svc-process] .pr-block{{position:relative;margin-inline:calc(50% - 50vw + var(--pr-sb,0px) / 2);height:max(560px,calc(100svh - var(--fiq-svc-offset,132px)));background:#1F1F1F;color:#F5F2ED;overflow:hidden;}}
    /* the finished room, revealed as the plan tilts away at handover */
    [data-svc-process] .pr-photo{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:calc(min(1, max(0, (var(--pr-h,0) - 0.25) * 1.6)));transform:scale(calc(1.08 - var(--pr-h,0) * 0.08));}}
    [data-svc-process] .pr-in{{position:relative;height:100%;width:min(1280px,calc(100% - 2 * {PAD}));margin:0 auto;display:grid;grid-template-columns:minmax(0,1fr) min(400px,34%);gap:clamp(24px,3.6vw,64px);align-items:center;}}
    [data-svc-process] .pr-board{{position:relative;height:100%;display:flex;align-items:center;justify-content:center;padding:clamp(28px,4vh,56px) 0;perspective:1600px;}}
    [data-svc-process] .pr-sheet{{width:100%;max-height:100%;transform-origin:50% 100%;transform:rotateX(calc(var(--pr-h,0) * 62deg)) translateY(calc(var(--pr-h,0) * 8%)) scale(calc(1 - var(--pr-h,0) * 0.12));opacity:calc(1 - var(--pr-h,0) * 1.35);}}
    [data-svc-process] .pr-svg{{display:block;width:100%;height:auto;max-height:calc(100svh - var(--fiq-svc-offset,132px) - 120px);overflow:visible;}}
    [data-svc-process] .pr-svg path,[data-svc-process] .pr-svg rect,[data-svc-process] .pr-svg circle{{fill:none;stroke:currentColor;stroke-width:1.4;vector-effect:non-scaling-stroke;stroke-linecap:square;}}
    [data-svc-process] .pr-grid path{{stroke:rgba(245,242,237,0.05);stroke-width:1;}}
    [data-svc-process] .pr-g{{color:rgba(245,242,237,0.34);transition:color 0.6s {EASE};}}
    [data-svc-process] .pr-g.is-on{{color:#D6C2A8;}}
    [data-svc-process] .pr-g .d{{stroke-dasharray:1 1;stroke-dashoffset:calc(1 - min(1, max(0, var(--pr-t,0) * 1.6 - var(--o,0) * 0.12)));}}
    [data-svc-process] .pr-g .f{{opacity:calc(min(1, max(0, (var(--pr-t,0) - 0.35 - var(--o,0) * 0.08) * 3)));}}
    [data-svc-process] .pr-g.is-anim{{transition:--pr-t 1.8s {EASE},color 0.6s {EASE};}}
    [data-svc-process] .pr-svg .wall{{fill:url(#pr-hatch);stroke:none;}}
    [data-svc-process] .pr-svg .cut{{fill:#1F1F1F;stroke:none;}}
    [data-svc-process] .pr-svg .dash{{stroke-dasharray:5 5;}}
    [data-svc-process] .pr-svg .plank{{stroke:currentColor;opacity:0.22;stroke-width:1;}}
    [data-svc-process] .pr-svg .dot{{fill:currentColor;stroke:none;}}
    [data-svc-process] .pr-svg .tag{{fill:#1F1F1F;}}
    [data-svc-process] .pr-svg .ok{{fill:#1F1F1F;}}
    [data-svc-process] .pr-svg .sw{{stroke:rgba(245,242,237,0.4);}}
    [data-svc-process] .pr-svg text{{fill:currentColor;stroke:none;font-family:{font};}}
    [data-svc-process] .pr-svg .lb{{font-size:{'13px' if ar else '10.5px'};letter-spacing:{'0' if ar else '0.2em'};}}
    [data-svc-process] .pr-svg .note{{fill:#F5F2ED;}}
    [data-svc-process] .pr-g:not(.is-on) .nt{{opacity:0;transition:opacity 0.6s {EASE};}}
    [data-svc-process] .pr-svg .zone{{font-size:{'15px' if ar else '12px'};letter-spacing:{'0' if ar else '0.42em'};}}
    [data-svc-process] .pr-svg .tg{{font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.06em;}}
    [data-svc-process] .pr-svg .lb--n{{font-family:'Lama Sans',sans-serif;}}
    [data-svc-process] .pr-sheetname{{position:absolute;bottom:clamp(14px,2.2vh,24px);inset-inline-start:0;margin:0;font-family:{font};font-size:{'11px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;color:rgba(245,242,237,0.42);opacity:calc(1 - var(--pr-h,0) * 2);}}
    [data-svc-process] .pr-side{{position:relative;display:flex;flex-direction:column;gap:clamp(24px,3vh,40px);padding:clamp(24px,2.6vw,36px);background:rgba(31,31,31,calc(var(--pr-h,0) * 0.8));-webkit-backdrop-filter:blur(calc(var(--pr-h,0) * 12px));backdrop-filter:blur(calc(var(--pr-h,0) * 12px));}}
    [data-svc-process] .pr-panes{{display:grid;}}
    [data-svc-process] .pr-pane{{grid-area:1/1;opacity:0;visibility:hidden;transform:translateY(10px);transition:opacity 0.5s {EASE},transform 0.5s {EASE},visibility 0s linear 0.5s;}}
    [data-svc-process] .pr-pane.is-on{{opacity:1;visibility:visible;transform:none;transition-delay:0.12s,0.12s,0s;}}
    [data-svc-process] .pr-count{{margin:0 0 18px;font-family:'Lama Sans',sans-serif;font-size:12px;letter-spacing:0.2em;color:rgba(245,242,237,0.5);}}
    [data-svc-process] .pr-count b{{font-weight:500;font-size:clamp(44px,4.4vw,64px);letter-spacing:-0.02em;color:#D6C2A8;margin-inline-end:6px;}}
    [data-svc-process] .pr-name{{margin:0 0 14px;font-family:{font};font-weight:500;font-size:clamp(28px,2.8vw,40px);line-height:1.1;color:#F5F2ED;}}
    [data-svc-process] .pr-desc{{margin:0 0 24px;font-family:{font};font-size:{'15px' if ar else '14px'};line-height:1.75;color:rgba(245,242,237,0.74);}}
    [data-svc-process] .pr-lbl{{margin:0 0 10px;font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;color:#C4A882;}}
    [data-svc-process] .pr-chips{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px;}}
    [data-svc-process] .pr-chips li{{padding:8px 12px;border:1px solid rgba(245,242,237,0.22);font-family:{font};font-size:{'13px' if ar else '11px'};letter-spacing:{'normal' if ar else '0.06em'};color:#F5F2ED;}}
    [data-svc-process] .pr-tabs{{display:grid;grid-template-columns:repeat({N},minmax(0,1fr));gap:6px;}}
    [data-svc-process] .pr-tab{{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:4px;padding:14px 0 0;border:0;background:none;color:rgba(245,242,237,0.45);text-align:start;cursor:pointer;transition:color 0.4s {EASE};}}
    [data-svc-process] .pr-tab:hover,[data-svc-process] .pr-tab[aria-selected="true"]{{color:#F5F2ED;}}
    [data-svc-process] .pr-tab:focus-visible{{outline:1px solid #D6C2A8;outline-offset:3px;}}
    [data-svc-process] .pr-bar{{position:absolute;top:0;left:0;right:0;height:2px;background:rgba(245,242,237,0.14);}}
    [data-svc-process] .pr-bar::after{{content:"";position:absolute;inset:0;background:#D6C2A8;transform:scaleX(var(--p,0));transform-origin:{'100%' if ar else '0%'} 50%;}}
    [data-svc-process] .pr-tn{{font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.18em;color:#C4A882;}}
    [data-svc-process] .pr-tt{{display:none;font-family:{font};font-size:{'11px' if ar else '8.5px'};letter-spacing:{'normal' if ar else '0.14em'};text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%;}}
    [data-svc-process] .pr-cap{{position:absolute;bottom:clamp(14px,2.2vh,24px);inset-inline-end:calc((100% - min(1280px,100% - 2 * {PAD})) / 2);margin:0;padding:7px 12px;background:rgba(31,31,31,0.62);color:rgba(245,242,237,0.85);font-family:{font};font-size:{'12px' if ar else '10.5px'};opacity:calc(min(1, max(0, (var(--pr-h,0) - 0.6) * 2.5)));}}
    /* the next step, offered once the room has been handed over */
    [data-svc-process] .pr-go{{display:inline-flex;align-items:center;gap:12px;margin-top:28px;padding:17px 30px;background:#D6C2A8;color:#1F1F1F;text-decoration:none;white-space:nowrap;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;border:1px solid #D6C2A8;opacity:0;visibility:hidden;transform:translateY(10px);transition:opacity 0.6s {EASE},transform 0.6s {EASE},visibility 0s linear 0.6s,background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-process].is-done .pr-go{{opacity:1;visibility:visible;transform:none;transition-delay:0s,0s,0s,0s,0s;}}
    [data-svc-process] .pr-go:hover,[data-svc-process] .pr-go:focus-visible{{background:transparent;color:#D6C2A8;}}
    @media(min-width:901px) and (min-height:600px){{
      [data-svc-process] .pr-block{{position:sticky;top:var(--fiq-svc-offset,132px);}}
      [data-svc-process] .pr-spacer{{height:{N * 55}vh;}}
    }}
    @media(max-width:900px){{
      [data-svc-process] .pr-head{{grid-template-columns:1fr;}}
      [data-svc-process] .pr-block{{height:auto;}}
      [data-svc-process] .pr-in{{grid-template-columns:1fr;width:100%;gap:0;}}
      [data-svc-process] .pr-board{{aspect-ratio:1000/680;height:auto;padding:24px 16px;}}
      [data-svc-process] .pr-svg{{max-height:none;}}
      [data-svc-process] .pr-photo{{height:auto;aspect-ratio:1000/680;bottom:auto;}}
      [data-svc-process] .pr-side{{background:#1F1F1F;padding:28px 24px 32px;}}
      [data-svc-process] .pr-cap{{top:12px;bottom:auto;inset-inline-end:12px;}}
      [data-svc-process] .pr-sheetname{{display:none;}}
    }}
    @media(max-width:600px){{
      [data-svc-process] .pr-tt{{display:none;}}
      [data-svc-process] .pr-go{{width:100%;justify-content:center;box-sizing:border-box;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-svc-process] .pr-rise{{opacity:1;transform:none;transition:none;}}
      [data-svc-process] .pr-g.is-anim,[data-svc-process] .pr-pane,[data-svc-process] .pr-go{{transition:none;}}
    }}
  </style>
  <div class="pr-wrap">
    <div class="pr-head">
      <div class="pr-rise">
        <div class="pr-eyebrow"><i></i>{c['eyebrow']}</div>
        <h2 class="pr-h2">{c['h2']}</h2>
      </div>
      <p class="pr-sub pr-rise pr-rise--2">{c['sub']}</p>
    </div>
    <div class="pr-track">
    <div class="pr-block" data-pr-block>
      <img class="pr-photo" src="uploads/{PHOTO}-1280.webp" srcset="uploads/{PHOTO}-1280.webp 1280w, uploads/{PHOTO}-1920.webp 1920w, uploads/{PHOTO}-2752.webp 2752w" sizes="100vw" alt="{c['alt']}" loading="lazy" decoding="async">
      <div class="pr-in">
        <div class="pr-board">
          <div class="pr-sheet">
            <svg class="pr-svg" viewBox="0 0 1000 640" role="img" aria-label="{c['sheet']}" direction="ltr">
              <defs><pattern id="pr-hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0,0V8" style="stroke:currentColor;stroke-width:1.2;opacity:0.7"/></pattern></defs>
              <g class="pr-grid"><path d="{''.join(f'M{x},0V640' for x in range(0, 1001, 40))}{''.join(f'M0,{y}H1000' for y in range(0, 641, 40))}"/></g>
              {plan(c)}
            </svg>
          </div>
          <p class="pr-sheetname">{c['sheet']}</p>
        </div>
        <div class="pr-side">
          <div class="pr-panes" aria-live="polite">
{panes}
          </div>
          <div class="pr-tabs" role="tablist" aria-label="{c['tabs']}">
{tabs}
          </div>
        </div>
      </div>
      <p class="pr-cap">{c['cap']}</p>
    </div>
    <div class="pr-spacer" aria-hidden="true"></div>
    </div>
  </div>
</section>
"""


JS = """    // ── SERVICES, PROCESS: FROM A LINE ON PAPER TO A ROOM ───────────────────
    {
      const sec = document.querySelector('[data-svc-process]');
      if (sec) {
        const block = sec.querySelector('[data-pr-block]'), track = sec.querySelector('.pr-track');
        const groups = Array.from(sec.querySelectorAll('.pr-g')), panes = Array.from(sec.querySelectorAll('.pr-pane'));
        const tabs = Array.from(sec.querySelectorAll('[data-pr]')), strip = sec.querySelector('.pr-tabs');
        const rtl = sec.getAttribute('dir') === 'rtl', N = tabs.length;
        const pinMQ = matchMedia('(min-width:901px) and (min-height:600px)');
        let pinned = pinMQ.matches, idx = -1, ticking = false, jump = null, auto = !reduced, seen = false, visible = false, hover = false, acc = 0, then = 0, raf = 0, anim = 0;
        const HOLD = 4200;
        // stage i drawn to fraction f: earlier stages complete and dimmed, the current one live, the rest blank
        const paint = (i, f) => {
          groups.forEach((g, k) => g.style.setProperty('--pr-t', k < i ? 1 : k === i ? f : 0));
          block.style.setProperty('--pr-h', i === N - 1 ? f : 0);   // handover: the plan tilts away into the room
          tabs.forEach((t, k) => t.style.setProperty('--p', k < i ? 1 : k === i ? f : 0));
          if (!anim) done(i === N - 1 && f >= 1);
        };
        const done = (on) => sec.classList.toggle('is-done', on);   // the room is handed over: offer the next step
        const show = (i) => {
          if (i === idx) return;
          idx = i;
          groups.forEach((g, k) => g.classList.toggle('is-on', k === i));
          panes.forEach((p) => p.classList.toggle('is-on', +p.dataset.pane === i));
          tabs.forEach((t, k) => { t.setAttribute('aria-selected', k === i ? 'true' : 'false'); t.tabIndex = k === i ? 0 : -1; });
        };
        const geo = () => {
          const top = parseFloat(getComputedStyle(block).top) || 0;
          return { start: track.getBoundingClientRect().top + window.scrollY - top, dist: Math.max(1, track.offsetHeight - block.offsetHeight) };
        };
        const onScroll = () => {
          ticking = false;
          if (!pinned) return;
          const g = geo(), x = Math.min(N - 0.0001, Math.max(0, (window.scrollY - g.start) / g.dist) * N), i = Math.floor(x);
          if (jump !== null) { if (i === jump) jump = null; else return; }
          show(i);
          paint(i, Math.min(1, (x - i) / 0.75));   // each stage finishes drawing with a quarter of its scroll to spare
        };
        window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
        // one wheel notch, one stage, resting where it has finished drawing (STEP SNAP)
        (window.fiqSnap = window.fiqSnap || []).push({ on: () => pinned, geo: () => { const g = geo(); return { a: g.start, b: g.start + g.dist, stops: Array.from({ length: N }, (_, j) => g.start + g.dist * (j + 0.8) / N) }; } });
        // a click, a tab or a phone's cycle draws the stage in over a moment instead of with the scroll
        const play = (i) => {
          groups.forEach((g) => g.classList.add('is-anim'));
          block.style.transition = reduced ? 'none' : '--pr-h 1.8s cubic-bezier(0.25,0.46,0.45,0.94)';
          clearTimeout(anim); done(false);
          anim = setTimeout(() => { anim = 0; groups.forEach((g) => g.classList.remove('is-anim')); block.style.transition = ''; done(idx === N - 1); }, reduced ? 0 : 1900);
          show(i);
          requestAnimationFrame(() => paint(i, 1));
        };
        const take = (i) => {
          auto = false;
          if (pinned) {
            const g = geo();
            jump = i; play(i);
            window.scrollTo({ top: g.start + g.dist * (i + 0.8) / N, behavior: reduced ? 'auto' : 'smooth' });
          } else play(i);
        };
        tabs.forEach((t, k) => {
          t.addEventListener('click', () => take(k));
          t.addEventListener('keydown', (e) => {
            const dd = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
            if (!dd) return;
            e.preventDefault();
            const n = (k + (rtl ? -dd : dd) + N) % N;
            take(n); tabs[n].focus();
          });
        });
        const fit = () => sec.style.setProperty('--pr-sb', (window.innerWidth - document.documentElement.clientWidth) + 'px');
        fit();
        window.addEventListener('resize', () => { fit(); onScroll(); });
        pinMQ.addEventListener('change', () => { pinned = pinMQ.matches; jump = null; idx = -1; if (pinned) onScroll(); else play(Math.max(0, idx)); });
        block.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') hover = true; });
        block.addEventListener('pointerleave', () => { hover = false; });
        // phones: the stages play in turn while the board is in view
        document.addEventListener('visibilitychange', () => { then = 0; });  // back from a hidden tab, time starts afresh
        const loop = (now) => {
          // real time between frames, so a throttled frame rate does not slow the cycle
          const dt = then ? now - then : 0; then = now;
          if (!pinned && auto && !hover && !document.hidden) {
            acc += dt;
            if (acc >= (idx === N - 1 ? HOLD * 2 : HOLD)) { acc = 0; play((idx + 1) % N); }
          }
          raf = visible ? requestAnimationFrame(loop) : 0;
        };
        new IntersectionObserver((es, o) => { es.forEach((e) => { if (e.isIntersecting) { sec.classList.add('is-in'); o.disconnect(); } }); }, { rootMargin: '0px 0px -15% 0px' }).observe(sec);
        new IntersectionObserver((es) => {
          es.forEach((e) => {
            visible = e.isIntersecting;
            if (visible && !seen && !pinned) { seen = true; play(0); }
            if (visible && !raf) { then = 0; raf = requestAnimationFrame(loop); }
          });
        }, { threshold: 0.35 }).observe(block);
        show(0); paint(0, 0);
        onScroll();
      }
    }

"""
MARK = "    // ── SCROLL REVEAL"

for path, lang in [("services.dc.html", "en"), ("services.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+[^\n]*-->\n<section id=\"process\".*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── SERVICES, PROCESS:"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

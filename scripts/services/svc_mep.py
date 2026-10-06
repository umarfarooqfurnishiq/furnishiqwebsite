"""Services, Engineering & MEP: engineering you feel, not see.

One finished corridor, shown first as the client experiences it. Then the photograph dims and the
systems behind the finish draw themselves over it, one discipline at a time, traced in the photo's own
one-point perspective: supply ducts and the linear diffuser, lighting circuits and cable tray, water and
drainage in the wall, the sprinkler main and its heads, data and security, and finally every system at
once with its test points signed off. On larger screens the stage pins and the scroll runs it from the
finished space through all six and back; the tabs scroll to their discipline. On phones it cycles on its
own while in view. The tabs, the arrow keys and the Finished / Engineered switch take over in both.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/services/svc_mep.py
"""
import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
IMG = ("executive-floors-walnut-ceiling-detail", (1200, 2400))
C = {
    "en": dict(
        eyebrow="Our Engineering Services", h2="The Foundation of High-Performance Environments",
        body="The systems you never see, engineered so every space performs.",
        cta="Explore Engineering &amp; MEP", href="/services-mep",
        feel=["Comfort, in every volume", "Light, layered with intent", "Water, exactly where it belongs",
              "Protection that stays out of sight", "Connected, quietly", "Proven before handover"],
        names=["HVAC Systems", "Electrical Systems", "Plumbing Systems", "Fire Fighting Systems",
               "Low Current Systems", "Testing &amp; Commissioning"],
        descs=["Air conditioning, ventilation, ductwork, and testing for consistent year-round comfort.",
               "Power distribution, lighting, emergency power, and cable management, engineered to code.",
               "Water supply, drainage, sewage, and pump installations engineered for reliability.",
               "Fire alarms, suppression, sprinkler networks, and full Civil Defense compliance.",
               "Structured cabling, CCTV, access control, and smart building integration.",
               "Functional testing, performance validation, and certified handover documentation."],
        intro_t="Engineering you feel, not see",
        intro_d="Six disciplines run behind every finished interior. Select one to see where it lives.",
        alt="Walnut slatted ceiling with linear lighting along a corridor that ends in a full-height window",
        tabs="MEP disciplines", view="View", finished="Finished", engineered="Engineered",
        cap="Systems drawn over a concept visualisation, for illustration",
        start="Start Your Project", start_href="/contact",
        labels=dict(supply="SUPPLY AIR", diffuser="LINEAR DIFFUSER", ret="RETURN AIR", tray="CABLE TRAY",
                    circuits="LIGHTING CIRCUITS", emergency="EMERGENCY POWER", water="COLD / HOT WATER",
                    riser="RISER", drain="DRAINAGE", main="SPRINKLER MAIN", heads="PENDENT HEADS",
                    smoke="SMOKE DETECTION", cabling="STRUCTURED CABLING", cctv="CCTV",
                    wifi="WIRELESS ACCESS", access="ACCESS CONTROL", t_air="AIRFLOW", t_lux="LIGHT LEVELS",
                    t_pressure="PRESSURE TEST", t_flow="FLOW TEST", t_net="NETWORK", t_alarm="ALARM"),
    ),
    "ar": dict(
        eyebrow="خدماتنا الهندسية", h2="أساس البيئات عالية الأداء",
        body="أنظمة لا تُرى، مُهندسة لتعمل كل مساحة بكفاءة.",
        cta="استكشف الهندسة والأنظمة الكهروميكانيكية", href="/ar/services-mep",
        feel=["راحة في كل مساحة", "إضاءة مدروسة بطبقات", "المياه، حيث يجب أن تكون",
              "حماية لا تُرى", "اتصال بهدوء", "مُختبر قبل التسليم"],
        names=["أنظمة التكييف والتهوية", "الأنظمة الكهربائية", "أنظمة السباكة", "أنظمة مكافحة الحريق",
               "أنظمة التيار المنخفض", "الاختبار والتشغيل"],
        descs=["التكييف والتهوية ومجاري الهواء والاختبار لراحة دائمة على مدار العام.",
               "توزيع الطاقة والإنارة وطاقة الطوارئ وإدارة الكابلات، وفق الأكواد المعتمدة.",
               "إمدادات المياه والصرف والصرف الصحي وتركيب المضخات بموثوقية عالية.",
               "إنذار الحريق والإطفاء وشبكات الرشاشات والامتثال الكامل لاشتراطات الدفاع المدني.",
               "الكابلات المهيكلة وكاميرات المراقبة والتحكم في الدخول وتكامل المباني الذكية.",
               "الاختبار الوظيفي والتحقق من الأداء ووثائق التسليم المعتمدة."],
        intro_t="هندسة تُحَس ولا تُرى",
        intro_d="ستة تخصصات تعمل خلف كل مساحة منجزة. اختر تخصصاً لترى أين يقع.",
        alt="سقف من شرائح خشب الجوز بإضاءة خطية على امتداد ممر ينتهي بنافذة كاملة الارتفاع",
        tabs="تخصصات الأنظمة الكهروميكانيكية", view="طريقة العرض", finished="المساحة المنجزة", engineered="الأنظمة الخفية",
        cap="رسم توضيحي للأنظمة فوق تصور مفاهيمي",
        start="ابدأ مشروعك", start_href="/ar/contact",
        labels=dict(supply="هواء الإمداد", diffuser="ناشر هواء خطي", ret="الهواء الراجع", tray="حامل الكابلات",
                    circuits="دوائر الإنارة", emergency="طاقة الطوارئ", water="المياه الباردة والساخنة",
                    riser="الخط الصاعد", drain="الصرف", main="خط الرشاشات الرئيسي", heads="رؤوس الرشاشات",
                    smoke="كشف الدخان", cabling="الكابلات المهيكلة", cctv="كاميرات المراقبة",
                    wifi="الشبكة اللاسلكية", access="التحكم في الدخول", t_air="تدفق الهواء", t_lux="مستوى الإنارة",
                    t_pressure="اختبار الضغط", t_flow="اختبار التدفق", t_net="الشبكة", t_alarm="الإنذار"),
    ),
}
ARROW_EN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
ARROW_AR = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>'

# ── Perspective of the photograph, in its own 1200 x 670 pixel space ──────────────────────────
# Every line that runs down the corridor meets at the vanishing point. t = 1 is the near edge of the
# frame, smaller t is deeper; t = 1/z spaces repeated items evenly in depth.
VX, VY = 600, 476
T_CEIL, T_RIGHT, T_LEFT = 0.115, 0.1667, 0.1333   # where the ceiling, right wall and left wall meet the far wall


def ceil(x0, t):   # on the ceiling, along the line that leaves the top edge at x0
    return (VX + t * (x0 - VX), VY - VY * t)


def rwall(y0, t):  # on the right wall, along the line that leaves the right edge at y0
    return (VX + 600 * t, VY + t * (y0 - VY))


def lwall(y0, t):  # on the left wall, along the line that leaves the left edge at y0
    return (VX - 600 * t, VY + t * (y0 - VY))


def P(p):
    return f"{p[0]:.1f},{p[1]:.1f}"


def draw(*pts, k=0, close=False):  # a line that draws itself in
    d = "M" + "L".join(P(p) for p in pts) + ("Z" if close else "")
    return f'<path class="d" style="--k:{k}" d="{d}" pathLength="1"/>'


def fade(d, k=0, cls=""):  # dashed, dotted or filled marks that fade in once the lines are down
    return f'<path class="f {cls}" style="--k:{k}" d="{d}"/>'


def seg(a, b):
    return f"M{P(a)}L{P(b)}"


def ring(p, r, k=0, cls=""):
    return f'<circle class="f {cls}" style="--k:{k}" cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r:.1f}"/>'


def label(p, dx, dy, text):
    end = (p[0] + dx, p[1] + dy)
    anchor = "start" if dx > 0 else "end" if dx < 0 else "middle"
    tx = end[0] + (6 if dx > 0 else -6 if dx < 0 else 0)
    ty = end[1] + (3.5 if dx else (12 if dy > 0 else -6))
    return (f'<circle class="ld" cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="2.4"/>'
            f'<path d="{seg(p, end)}"/>'
            f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}">{text}</text>')


def tick(p, k):  # a signed-off test point
    x, y = p
    return (ring(p, 12, k, "chk") +
            f'<path class="d" style="--k:{k + 2}" d="M{x - 5:.1f},{y + 0.5:.1f}L{x - 1.5:.1f},{y + 4:.1f}L{x + 5.5:.1f},{y - 4:.1f}" pathLength="1"/>')


def systems(L):
    out = []

    # 01 HVAC: supply duct above the existing linear diffuser, airflow falling from it, return air opposite
    g, lab = [], []
    g.append(draw(ceil(885, 1), ceil(885, T_CEIL), ceil(1045, T_CEIL), ceil(1045, 1), k=0))
    for n, t in enumerate((0.78, 0.6, 0.46, 0.35, 0.27, 0.2, 0.155)):
        g.append(draw(ceil(885, t), ceil(1045, t), k=2 + n))
    g.append(draw(ceil(950, 0.81), ceil(950, 0.37), ceil(978, 0.37), ceil(978, 0.81), k=3, close=True))
    for n, t in enumerate((0.76, 0.62, 0.49)):
        x, y = ceil(964, t)
        g.append(fade(f"M{x:.1f},{y:.1f}Q{x + 8 * t:.1f},{y + 90 * t:.1f} {x - 70 * t:.1f},{y + 160 * t:.1f}", 6 + n, "dash"))
        g.append(fade(f"M{x:.1f},{y:.1f}Q{x + 20 * t:.1f},{y + 70 * t:.1f} {x + 10 * t:.1f},{y + 140 * t:.1f}", 7 + n, "dash"))
    g.append(draw(ceil(40, 1), ceil(40, T_CEIL), ceil(150, T_CEIL), ceil(150, 1), k=1))
    gr = [ceil(58, 0.68), ceil(132, 0.68), ceil(132, 0.56), ceil(58, 0.56)]
    g.append(draw(*gr, k=5, close=True))
    for n in range(1, 5):
        g.append(fade(seg(ceil(58 + n * 14.8, 0.68), ceil(58 + n * 14.8, 0.56)), 8))
    lab += [label(ceil(1045, 0.62), 46, -28, L["supply"]), label(ceil(964, 0.47), 70, 46, L["diffuser"]),
            label(ceil(95, 0.62), -30, 58, L["ret"])]
    out.append((g, lab))

    # 02 Electrical: the light lines themselves, a cable tray, and two buses feeding every run
    g, lab = [], []
    for n, x0 in enumerate((190, 420, 835, 895)):
        g.append(draw(ceil(x0, 1), ceil(x0, 0.2), k=n))
    g.append(draw(ceil(600, 0.454), ceil(600, 0.13), k=2))
    for x0 in (300, 330):
        g.append(draw(ceil(x0, 1), ceil(x0, T_CEIL), k=1))
    for n, t in enumerate((0.9, 0.72, 0.57, 0.45, 0.36, 0.29, 0.23, 0.18, 0.145)):
        g.append(fade(seg(ceil(300, t), ceil(330, t)), 3 + n))
    for n, t in enumerate((0.7, 0.38)):
        g.append(draw(ceil(190, t), ceil(895, t), k=5 + 2 * n))
        for x0 in (190, 420, 600, 835, 895):
            g.append(ring(ceil(x0, t), 3.2 * t + 1.2, 7 + 2 * n, "fill"))
    g.append(fade(seg(ceil(835, 1), ceil(835, 0.2)), 9, "em"))
    lab += [label(ceil(315, 0.42), -40, 46, L["tray"]), label(ceil(600, 0.7), 0, -46, L["circuits"]),
            label(ceil(895, 0.56), 74, -26, L["emergency"])]
    out.append((g, lab))

    # 03 Plumbing: cold and hot water in the right wall, a riser at the panel joint with its valve, drainage low
    g, lab = [], []
    g.append(draw(rwall(205, 1), rwall(205, T_RIGHT), k=0))
    g.append(draw(rwall(235, 1), rwall(235, T_RIGHT), k=1))
    for n, x in enumerate((934, 946)):
        t = (x - VX) / 600
        g.append(draw((x, 670), (x, rwall(205 + 30 * n, t)[1]), k=3 + n))
    g.append(fade("M928,508L952,528L952,508L928,528Z", 7))
    g.append(fade("M940,518L940,500M932,500L948,500", 7))
    t0 = (670 - VY) / (900 - VY)
    g.append(fade(seg(rwall(900, t0), rwall(900, T_RIGHT)), 5, "dash"))
    lab += [label(rwall(220, 0.8), 0, 44, L["water"]), label((946, 440), 44, 0, L["riser"]),
            label(rwall(900, 0.3), 60, 30, L["drain"])]
    out.append((g, lab))

    # 04 Fire fighting: sprinkler main down the corridor, pendent heads spaced in depth, smoke detectors
    g, lab = [], []
    g.append(draw(ceil(655, 1), ceil(655, T_CEIL), k=0))
    g.append(draw(ceil(655, 0.6), ceil(470, 0.6), k=2))
    g.append(draw(ceil(655, 0.32), ceil(470, 0.32), k=4))
    heads = [(655, t) for t in (0.82, 0.6, 0.44, 0.32, 0.23, 0.165)] + [(470, 0.6), (470, 0.32)]
    for n, (x0, t) in enumerate(heads):
        x, y = ceil(x0, t)
        h, w = 16 * t, 7 * t
        g.append(draw((x, y), (x, y + h), k=3 + n))
        g.append(draw((x - w, y + h), (x + w, y + h), k=4 + n))
        g.append(fade(f"M{x:.1f},{y + h:.1f}L{x - 46 * t:.1f},{y + h + 72 * t:.1f}M{x:.1f},{y + h:.1f}L{x + 46 * t:.1f},{y + h + 72 * t:.1f}M{x:.1f},{y + h:.1f}L{x:.1f},{y + h + 80 * t:.1f}", 6 + n, "dash"))
    for n, t in enumerate((0.75, 0.4)):
        p = ceil(250, t)
        g.append(ring(p, 10 * t, 4 + n))
        g.append(ring(p, 3 * t, 5 + n, "fill"))
    lab += [label(ceil(655, 0.9), 54, 22, L["main"]), label(ceil(655, 0.44), 66, 34, L["heads"]),
            label(ceil(250, 0.75), -26, 54, L["smoke"])]
    out.append((g, lab))

    # 05 Low current: data along the wall head, a wireless access point, CCTV down the corridor, a door reader
    g, lab = [], []
    g.append(draw(lwall(120, 1), lwall(120, T_LEFT), k=0))
    g.append(fade(seg(lwall(134, 1), lwall(134, T_LEFT)), 3, "dot"))
    g.append(draw(rwall(150, 1), rwall(150, T_RIGHT), k=1))
    g.append(draw((959, 455), (959, rwall(150, (959 - VX) / 600)[1]), k=4))
    g.append(draw((954, 455), (964, 455), (964, 476), (954, 476), k=6, close=True))
    ap = ceil(560, 0.55)
    g.append(draw(ceil(560, 1), ap, k=2))
    g.append(ring(ap, 6, 5, "fill"))
    g.append(fade(f"M{ap[0] - 13:.1f},{ap[1] + 10:.1f}Q{ap[0]:.1f},{ap[1] + 22:.1f} {ap[0] + 13:.1f},{ap[1] + 10:.1f}M{ap[0] - 22:.1f},{ap[1] + 15:.1f}Q{ap[0]:.1f},{ap[1] + 35:.1f} {ap[0] + 22:.1f},{ap[1] + 15:.1f}", 6))
    cam = (150, 76)
    g.append(draw((128, 54), cam, k=3))
    g.append(f'<g class="f" style="--k:5" transform="rotate(41 {cam[0]} {cam[1]})"><rect x="{cam[0]}" y="{cam[1] - 7}" width="32" height="14"/><path d="M{cam[0] + 32},{cam[1] - 4}L{cam[0] + 40},{cam[1] - 8}L{cam[0] + 40},{cam[1] + 8}L{cam[0] + 32},{cam[1] + 4}"/></g>')
    g.append(fade("M186,116L470,420M186,116L560,330", 7, "dash"))
    lab += [label(lwall(120, 0.62), 0, 50, L["cabling"]), label((166, 66), 56, -24, L["cctv"]),
            label(ap, -60, 50, L["wifi"]), label((964, 466), 44, 24, L["access"])]
    out.append((g, lab))

    # 06 Testing & commissioning: every system at once, signed off at its test point
    g, lab = [], []
    pts = [(ceil(964, 0.5), L["t_air"], 46, -34), (ceil(420, 0.62), L["t_lux"], -40, 44),
           ((940, 518), L["t_pressure"], 44, 30), (ceil(655, 0.44), L["t_flow"], 50, 40),
           (lwall(120, 0.62), L["t_net"], 0, 52), (ceil(250, 0.75), L["t_alarm"], -30, -30)]
    for n, (p, text, dx, dy) in enumerate(pts):
        g.append(tick(p, n * 2))
        lab.append(label((p[0] + (12 if dx > 0 else -12 if dx < 0 else 0), p[1] + (0 if dx else 12 if dy > 0 else -12)), dx, dy, text))
    out.append((g, lab))
    return out


def svg(L, font):
    groups = "\n".join(
        f'        <g class="mx-sys" data-sys="{i}">{"".join(g)}<g class="mx-lab" font-family="{font}">{"".join(lab)}</g></g>'
        for i, (g, lab) in enumerate(systems(L)))
    return f'''      <svg class="mx-svg" viewBox="0 0 1200 670" preserveAspectRatio="xMidYMin slice" direction="ltr" aria-hidden="true" focusable="false">
{groups}
      </svg>'''


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    caps = "normal" if ar else "0.22em"
    base, widths = IMG
    srcset = ", ".join(f"uploads/{base}-{w}.webp {w}w" for w in widths)
    n = len(c["names"])
    panes = [f'''        <div class="mx-pane is-on" data-i="-1"><p class="mx-count"><span dir="ltr">00 / 0{n}</span></p><h3 class="mx-feel">{c['intro_t']}</h3><p class="mx-desc">{c['intro_d']}</p></div>''']
    panes += [f'''        <div class="mx-pane" data-i="{i}" id="mx-pane-{i}" role="tabpanel" aria-labelledby="mx-tab-{i}"><p class="mx-count"><span dir="ltr">0{i + 1} / 0{n}</span></p><p class="mx-name">{c['names'][i]}</p><h3 class="mx-feel">{c['feel'][i]}</h3><p class="mx-desc">{c['descs'][i]}</p></div>''' for i in range(n)]
    tabs = [f'''      <button type="button" class="mx-tab" role="tab" id="mx-tab-{i}" data-mx-tab="{i}" aria-selected="false" aria-controls="mx-pane-{i}" tabindex="{0 if i == 0 else -1}"><i class="mx-prog" aria-hidden="true"></i><span class="mx-n" dir="ltr">0{i + 1}</span><span class="mx-t">{c['names'][i]}</span></button>''' for i in range(n)]
    panes, tabs = "\n".join(panes), "\n".join(tabs)
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━ 3. ENGINEERING & MEP ━ -->
<section id="mep" data-screen-label="Engineering &amp; MEP" data-svc-mep{' dir="rtl"' if ar else ''} style="scroll-margin-top:var(--fiq-svc-offset,132px);background:#F5F2ED;color:#3A2D25;position:relative;padding:clamp(64px,8vw,100px) clamp(24px,5vw,80px) 0;overflow:clip;">
  <style>
    [data-svc-mep] .mr-wrap{{max-width:1280px;margin:0 auto;}}
    [data-svc-mep] .mr-head{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:clamp(32px,5vw,88px);align-items:end;margin-bottom:clamp(40px,4.4vw,64px);}}
    [data-svc-mep] .mr-eyebrow{{display:flex;align-items:center;gap:16px;margin-bottom:24px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    [data-svc-mep] .mr-eyebrow i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    [data-svc-mep] .mr-h2{{font-family:{font};font-weight:500;font-size:clamp(32px,3.8vw,54px);line-height:1.08;letter-spacing:{'0' if ar else '-0.015em'};color:#1F1F1F;margin:0;text-wrap:balance;}}
    [data-svc-mep] .mr-body{{font-family:{font};font-weight:500;font-size:{'clamp(22px,2vw,28px)' if ar else 'clamp(20px,1.9vw,26px)'};line-height:1.4;letter-spacing:{'0' if ar else '-0.005em'};text-wrap:balance;max-width:{'18em' if ar else '30ch'};color:#3A2D25;margin:0 0 28px;}}
    [data-svc-mep] .mr-cta{{display:inline-flex;align-items:center;gap:12px;padding:17px 30px;background:#3A2D25;color:#F5F2ED;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;border:1px solid #3A2D25;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-mep] .mr-cta:hover,[data-svc-mep] .mr-cta:focus-visible{{background:transparent;color:#3A2D25;}}
    [data-svc-mep] .mr-rise{{opacity:0;transform:translateY(24px);transition:opacity 0.9s {EASE},transform 0.9s {EASE};}}
    [data-svc-mep].is-in .mr-rise{{opacity:1;transform:none;}}
    [data-svc-mep].is-in .mr-rise--2{{transition-delay:0.12s;}}
    [data-svc-mep].is-in .mr-rise--3{{transition-delay:0.24s;}}
    [data-svc-mep] .mx-block{{margin-inline:calc(50% - 50vw + var(--mx-sb,0px) / 2);background:#1F1F1F;}}
    [data-svc-mep] .mx-frame{{position:relative;}}
    [data-svc-mep] .mx-stage{{position:relative;width:100%;height:min(calc(100vh - var(--fiq-svc-offset,132px) - var(--mx-tabs,96px)),55.84vw);height:min(calc(100svh - var(--fiq-svc-offset,132px) - var(--mx-tabs,96px)),55.84vw);min-height:440px;overflow:hidden;background:#1F1F1F;}}
    [data-svc-mep] .mx-img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 0;transition:filter 1.4s {EASE},transform 2.4s {EASE};transform:scale(1.04);}}
    [data-svc-mep].is-in .mx-img{{transform:scale(1);}}
    [data-svc-mep] .mx-stage.is-xray .mx-img{{filter:brightness(0.42) saturate(0.55) contrast(1.06);}}
    [data-svc-mep] .mx-svg{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden;pointer-events:none;}}
    [data-svc-mep] .mx-svg path,[data-svc-mep] .mx-svg circle,[data-svc-mep] .mx-svg rect{{fill:none;stroke:#D6C2A8;stroke-width:calc(1.3px * var(--mx-u,1));stroke-linecap:square;stroke-linejoin:miter;}}
    [data-svc-mep] .mx-svg .fill{{fill:#D6C2A8;}}
    [data-svc-mep] .mx-svg .dash{{stroke-dasharray:4 5;stroke-width:calc(1px * var(--mx-u,1));}}
    [data-svc-mep] .mx-svg .dot{{stroke-dasharray:1 5;stroke-linecap:round;stroke-width:calc(1.7px * var(--mx-u,1));}}
    [data-svc-mep] .mx-svg .em{{stroke:#F5F2ED;stroke-dasharray:10 8;stroke-width:calc(1.7px * var(--mx-u,1));}}
    [data-svc-mep] .mx-svg .chk{{fill:rgba(31,31,31,0.6);stroke:#F5F2ED;}}
    [data-svc-mep] .mx-sys{{opacity:0;transition:opacity 0.6s {EASE};}}
    [data-svc-mep] .mx-sys .d{{stroke-dasharray:1 1;stroke-dashoffset:1;transition:stroke-dashoffset 1.3s {EASE} calc(var(--k,0) * 70ms);}}
    [data-svc-mep] .mx-sys .f{{opacity:0;transition:opacity 0.7s {EASE} calc(0.5s + var(--k,0) * 70ms);}}
    [data-svc-mep] .mx-sys.on,[data-svc-mep] .mx-sys.on .f{{opacity:1;}}
    [data-svc-mep] .mx-sys.on .d,[data-svc-mep] .mx-sys.ghost .d{{stroke-dashoffset:0;}}
    [data-svc-mep] .mx-sys.ghost{{opacity:0.32;}}
    [data-svc-mep] .mx-sys.ghost .f{{opacity:1;}}
    [data-svc-mep] .mx-lab{{opacity:0;transition:opacity 0.5s {EASE};}}
    [data-svc-mep] .mx-sys.on .mx-lab{{opacity:1;transition-delay:1.1s;}}
    [data-svc-mep] .mx-lab path{{stroke:rgba(245,242,237,0.7);stroke-width:calc(0.9px * var(--mx-u,1));}}
    [data-svc-mep] .mx-lab .ld{{fill:#F5F2ED;stroke:none;}}
    [data-svc-mep] .mx-lab text{{fill:#F5F2ED;stroke:rgba(31,31,31,0.55);stroke-width:calc(3px * var(--mx-u,1));paint-order:stroke;font-size:calc({'13px' if ar else '11px'} * var(--mx-u,1));letter-spacing:{'normal' if ar else '0.2em'};}}
    [data-svc-mep] .mx-in{{position:absolute;inset:0;width:min(1280px,calc(100% - 2 * clamp(24px,5vw,80px)));margin:0 auto;pointer-events:none;}}
    [data-svc-mep] .mx-view{{position:absolute;top:clamp(16px,2.2vw,32px);right:0;pointer-events:auto;display:flex;border:1px solid rgba(245,242,237,0.22);background:rgba(31,31,31,0.62);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);}}
    [data-svc-mep] .mx-view button{{padding:11px 16px;border:0;background:transparent;color:rgba(245,242,237,0.6);font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;cursor:pointer;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-mep] .mx-view button:hover{{color:#F5F2ED;}}
    [data-svc-mep] .mx-view button[aria-pressed="true"]{{background:#F5F2ED;color:#1F1F1F;}}
    [data-svc-mep] .mx-panel{{position:absolute;left:0;bottom:clamp(16px,2.6vw,40px);width:min(420px,40%);display:grid;color:#F5F2ED;pointer-events:none;}}
    [data-svc-mep] .mx-pane{{grid-area:1/1;align-self:end;padding:clamp(22px,2.2vw,30px);background:rgba(31,31,31,0.8);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);pointer-events:auto;opacity:0;visibility:hidden;transform:translateY(10px);transition:opacity 0.6s {EASE},transform 0.6s {EASE},visibility 0s linear 0.6s;}}
    [data-svc-mep] .mx-pane.is-on{{opacity:1;visibility:visible;transform:none;transition-delay:0.25s,0.25s,0s;}}
    [data-svc-mep] .mx-count{{margin:0 0 16px;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.24em;color:#C4A882;}}
    [data-svc-mep] .mx-name{{margin:0 0 10px;font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;color:#C4A882;}}
    [data-svc-mep] .mx-feel{{margin:0 0 12px;font-family:{font};font-weight:500;font-size:clamp(21px,2vw,28px);line-height:1.2;color:#F5F2ED;text-wrap:balance;}}
    [data-svc-mep] .mx-desc{{margin:0;font-family:{font};font-size:{'14px' if ar else '13px'};line-height:1.7;color:rgba(245,242,237,0.72);}}
    [data-svc-mep] .mx-tabs{{display:grid;grid-template-columns:repeat({n},minmax(0,1fr));width:min(1280px,calc(100% - 2 * clamp(24px,5vw,80px)));margin:0 auto;}}
    [data-svc-mep] .mx-tab{{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:10px;padding:22px clamp(14px,1.6vw,22px) 24px;border:0;border-inline-start:1px solid rgba(245,242,237,0.1);background:transparent;color:rgba(245,242,237,0.5);text-align:start;cursor:pointer;transition:color 0.4s {EASE},background 0.4s {EASE};}}
    [data-svc-mep] .mx-tab:first-child{{border-inline-start:0;}}
    [data-svc-mep] .mx-tab:hover{{color:#F5F2ED;background:rgba(245,242,237,0.03);}}
    [data-svc-mep] .mx-tab:focus-visible{{outline:1px solid #D6C2A8;outline-offset:-4px;}}
    [data-svc-mep] .mx-tab[aria-selected="true"]{{color:#F5F2ED;}}
    [data-svc-mep] .mx-prog{{position:absolute;top:0;left:0;right:0;height:2px;background:rgba(245,242,237,0.1);}}
    [data-svc-mep] .mx-prog::after{{content:"";position:absolute;inset:0;background:#D6C2A8;transform:scaleX(var(--p,0));transform-origin:{'100%' if ar else '0%'} 50%;}}
    [data-svc-mep] .mx-n{{font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.2em;color:#C4A882;}}
    [data-svc-mep] .mx-t{{font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.18em'};text-transform:uppercase;line-height:1.5;}}
    [data-svc-mep] .mr-cap{{position:absolute;bottom:clamp(16px,2.6vw,40px);right:calc((100% - min(1280px,100% - 2 * clamp(24px,5vw,80px))) / 2);margin:0;max-width:40%;padding:7px 12px;background:rgba(31,31,31,0.62);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);text-align:right;font-family:{font};font-size:{'12px' if ar else '10.5px'};line-height:1.5;color:rgba(245,242,237,0.78);pointer-events:none;}}
    [data-svc-mep] .mx-go{{position:absolute;inset:0;display:grid;place-items:center;pointer-events:none;}}
    [data-svc-mep] .mx-go a{{display:inline-flex;align-items:center;gap:14px;padding:22px 44px;background:#F5F2ED;color:#1F1F1F;border:1px solid #F5F2ED;text-decoration:none;font-family:{font};font-size:{'14px' if ar else '11px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;box-shadow:0 24px 80px rgba(31,31,31,0.35);opacity:0;visibility:hidden;transform:translateY(16px);transition:opacity 0.7s {EASE},transform 0.7s {EASE},visibility 0s linear 0.7s,background 0.4s {EASE},color 0.4s {EASE};}}
    [data-svc-mep] .mx-stage.is-end .mx-go a{{opacity:1;visibility:visible;transform:none;pointer-events:auto;transition-delay:0.3s,0.3s,0s,0s,0s;}}
    [data-svc-mep] .mx-go a:hover,[data-svc-mep] .mx-go a:focus-visible{{background:rgba(31,31,31,0.55);color:#F5F2ED;}}
    @media(min-width:901px) and (min-height:600px){{
      [data-svc-mep] .mx-spacer{{height:{(n + 2) * 50}vh;}}
      [data-svc-mep] .mx-block{{position:sticky;top:var(--fiq-svc-offset,132px);}}
    }}
    @media(max-width:900px){{
      [data-svc-mep] .mr-head{{grid-template-columns:1fr;}}
      [data-svc-mep] .mx-stage{{height:auto;min-height:0;aspect-ratio:4/3;}}
      [data-svc-mep] .mx-in{{position:static;width:auto;}}
      [data-svc-mep] .mx-view{{right:clamp(14px,2vw,24px);top:clamp(14px,2vw,24px);}}
      [data-svc-mep] .mx-tabs{{width:100%;}}
      [data-svc-mep] .mr-cap{{right:14px;bottom:12px;max-width:70%;}}
      [data-svc-mep] .mx-go a{{padding:18px 30px;}}
      [data-svc-mep] .mx-lab{{display:none;}}
      [data-svc-mep] .mx-panel{{position:relative;left:auto;bottom:auto;width:auto;background:#1F1F1F;-webkit-backdrop-filter:none;backdrop-filter:none;border-bottom:1px solid rgba(245,242,237,0.1);}}
      [data-svc-mep] .mx-pane{{background:#1F1F1F;-webkit-backdrop-filter:none;backdrop-filter:none;}}
      [data-svc-mep] .mx-tabs{{grid-template-columns:repeat(3,minmax(0,1fr));}}
      [data-svc-mep] .mx-tab{{border-top:1px solid rgba(245,242,237,0.1);}}
      [data-svc-mep] .mx-tab:nth-child(3n+1){{border-inline-start:0;}}
    }}
    @media(max-width:600px){{
      [data-svc-mep] .mx-stage{{aspect-ratio:1/1;}}
      [data-svc-mep] .mx-view button{{padding:9px 12px;}}
      [data-svc-mep] .mx-tab{{padding:18px 12px 20px;}}
      [data-svc-mep] .mr-cta{{width:100%;justify-content:center;box-sizing:border-box;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-svc-mep] *,[data-svc-mep] *::after{{transition:none!important;}}
      [data-svc-mep] .mr-rise{{opacity:1;transform:none;}}
      [data-svc-mep] .mx-img{{transform:none;}}
    }}
  </style>
  <div class="mr-wrap">
    <div class="mr-head">
      <div class="mr-rise">
        <div class="mr-eyebrow"><i></i>{c['eyebrow']}</div>
        <h2 class="mr-h2">{c['h2']}</h2>
      </div>
      <div class="mr-rise mr-rise--2">
        <p class="mr-body">{c['body']}</p>
        <a class="mr-cta" href="{c['href']}">{c['cta']}{ARROW_AR if ar else ARROW_EN}</a>
      </div>
    </div>
    <div class="mx-track">
    <div class="mx-block mr-rise mr-rise--3">
      <div class="mx-frame">
        <div class="mx-stage" data-mx-stage>
          <img class="mx-img" src="uploads/{base}-{widths[0]}.webp" srcset="{srcset}" sizes="100vw" alt="{c['alt']}" loading="lazy" decoding="async">
{svg(c['labels'], font)}
          <div class="mx-go"><a href="{c['start_href']}" tabindex="-1">{c['start']}{ARROW_AR if ar else ARROW_EN}</a></div>
          <p class="mr-cap">{c['cap']}</p>
        </div>
        <div class="mx-in">
        <div class="mx-view" role="group" aria-label="{c['view']}"><button type="button" data-mx-view="feel" aria-pressed="true">{c['finished']}</button><button type="button" data-mx-view="see" aria-pressed="false">{c['engineered']}</button></div>
        <div class="mx-panel" aria-live="polite">
{panes}
        </div>
        </div>
      </div>
      <div class="mx-tabbar"><div class="mx-tabs" role="tablist" aria-label="{c['tabs']}">
{tabs}
      </div></div>
    </div>
    <div class="mx-spacer" aria-hidden="true"></div>
    </div>
  </div>
</section>
"""


JS = """    // ── SERVICES, MEP: ENGINEERING YOU FEEL, NOT SEE ────────────────────────
    {
      const sec = document.querySelector('[data-svc-mep]');
      if (sec) {
        const stage = sec.querySelector('[data-mx-stage]'), block = sec.querySelector('.mx-block'), track = sec.querySelector('.mx-track');
        const go = sec.querySelector('.mx-go a'), sys = Array.from(sec.querySelectorAll('.mx-sys')), panes = Array.from(sec.querySelectorAll('.mx-pane'));
        const tabs = Array.from(sec.querySelectorAll('[data-mx-tab]')), views = Array.from(sec.querySelectorAll('[data-mx-view]'));
        const rtl = sec.getAttribute('dir') === 'rtl', last = tabs.length - 1;
        const STEPS = tabs.length + 2;   // pinned: finished, the six disciplines, finished again
        const HOLD = 6500, REST = 2600;  // phones: per discipline, and the clean photo between cycles
        const pinMQ = matchMedia('(min-width:901px) and (min-height:600px)');
        let pinned = pinMQ.matches, idx = -1, prev = 0, auto = !reduced, seen = false, visible = false, hover = false;
        let acc = 0, then = 0, raf = 0, ticking = false, jump = null, quiet = null;
        // i = -1 is the finished space; 0..5 draws that discipline, the last showing every system signed off;
        // -2 is the finished space again at the close, with the call to action
        const show = (i) => {
          idx = i; acc = 0;
          if (i >= 0) prev = i;
          stage.classList.toggle('is-xray', i >= 0);
          stage.classList.toggle('is-end', i === -2);
          go.tabIndex = i === -2 ? 0 : -1;
          sys.forEach((g, k) => { g.classList.toggle('on', k === i); g.classList.toggle('ghost', i === last && k < last); });
          panes.forEach((p) => p.classList.toggle('is-on', +p.dataset.i === (i === -2 && !pinned ? -1 : i)));
          tabs.forEach((t, k) => {
            t.setAttribute('aria-selected', k === i ? 'true' : 'false');
            t.tabIndex = k === Math.max(i, 0) ? 0 : -1;
            if (!pinned) t.style.setProperty('--p', k === i && !auto ? 1 : 0);
          });
          views.forEach((v) => v.setAttribute('aria-pressed', (v.dataset.mxView === 'see') === (i >= 0) ? 'true' : 'false'));
        };
        // pinned: where the track starts, how far it scrolls, and which state a scroll position falls in
        const geo = () => {
          const top = parseFloat(getComputedStyle(block).top) || 0;
          return { start: track.getBoundingClientRect().top + window.scrollY - top, dist: Math.max(1, track.offsetHeight - block.offsetHeight) };
        };
        const stateAt = () => {
          const g = geo(), x = Math.min(STEPS - 0.0001, Math.max(0, (window.scrollY - g.start) / g.dist) * STEPS), seg = Math.floor(x);
          return { i: seg === 0 ? -1 : seg === STEPS - 1 ? -2 : seg - 1, f: x - seg };
        };
        const goTo = (i) => { const g = geo(); window.scrollTo({ top: g.start + g.dist * (i + 1.5) / STEPS, behavior: reduced ? 'auto' : 'smooth' }); };
        // one wheel notch, one state (STEP SNAP)
        (window.fiqSnap = window.fiqSnap || []).push({ on: () => pinned, geo: () => { const g = geo(); return { a: g.start, b: g.start + g.dist, stops: Array.from({ length: STEPS }, (_, j) => g.start + g.dist * (j + 0.5) / STEPS) }; } });
        const onScroll = () => {
          ticking = false;
          if (!pinned) return;
          const st = stateAt();
          if (jump !== null) { if (st.i === jump) jump = null; else return; }   // a tab click glides past the states in between
          if (quiet !== null) { if (st.i !== quiet) quiet = null; else return; } // Finished holds until the scroll moves on
          if (st.i !== idx) show(st.i);
          tabs.forEach((t, k) => t.style.setProperty('--p', k === st.i ? st.f.toFixed(4) : 0));
        };
        window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
        const take = (i) => {
          auto = false;
          if (pinned && i >= 0) { quiet = null; jump = i; show(i); goTo(i); }
          else if (pinned) { quiet = stateAt().i; jump = null; show(-1); }
          else show(i);
        };
        tabs.forEach((t, k) => {
          t.addEventListener('click', () => take(k));
          t.addEventListener('keydown', (e) => {
            const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
            if (!d) return;
            e.preventDefault();
            const n = (k + (rtl ? -d : d) + tabs.length) % tabs.length;
            take(n); tabs[n].focus();
          });
        });
        views.forEach((v) => v.addEventListener('click', () => {
          if (v.dataset.mxView !== 'see') return take(-1);
          const st = pinned ? stateAt().i : -1;
          if (pinned && st >= 0) { quiet = null; show(st); } else take(prev);
        }));
        // labels and strokes keep one on-screen size however the photo is scaled and cropped;
        // 100vw counts the scrollbar; take it back out so the photo meets both edges exactly
        const fit = () => {
          sec.style.setProperty('--mx-tabs', sec.querySelector('.mx-tabbar').offsetHeight + 'px');  // stage + tabs fill the screen exactly
          sec.style.setProperty('--mx-sb', (window.innerWidth - document.documentElement.clientWidth) + 'px');
          sec.style.setProperty('--mx-u', (1 / Math.max(stage.clientWidth / 1200, stage.clientHeight / 670)).toFixed(4));
        };
        fit();
        window.addEventListener('resize', fit);
        if (document.fonts) document.fonts.ready.then(fit);  // the tab bar settles its height once the fonts are in
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
        // any part of the section on screen reveals it, even when the page opens part-way down the scroll track
        new IntersectionObserver((es, o) => { es.forEach((e) => { if (e.isIntersecting) { sec.classList.add('is-in'); o.disconnect(); } }); }, { rootMargin: '0px 0px -15% 0px' }).observe(sec);
        new IntersectionObserver((es) => {
          es.forEach((e) => {
            visible = e.isIntersecting;
            if (visible && !seen && !pinned) { seen = true; if (reduced) show(0); else acc = REST - 1200; }
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

"""Section headers across the site: the long paragraph beside a heading becomes one subtitle line.

The same treatment as the Services page: one sentence at subtitle size (Lama Sans 500, 20-26px; GE SS Two
22-28px in Arabic), balanced, about 30 characters to the line. Covers the Home disciplines, edge and Fit-Out
headers, the About gates and disciplines intros, and the intro of each service page.
Run from the repo root: PYTHONIOENCODING=utf-8 python scripts/site/header_subtitles.py
"""
import re

SITE = "Furnishiq.net/"


def sub(ar, color="#3A2D25", extra=""):
    size = "clamp(22px,2vw,28px)" if ar else "clamp(20px,1.9vw,26px)"
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    return (f"font-family:{font};font-size:{size};font-weight:500;line-height:1.4;"
            f"letter-spacing:{'0' if ar else '-0.005em'};color:{color};text-wrap:balance;max-width:{'18em' if ar else '30ch'};margin:0;{extra}")


def edit(name, fn):
    path = SITE + name
    s = open(path, encoding="utf-8").read()
    s2 = fn(s, ".ar." in name)
    assert s2 != s, name
    open(path, "w", encoding="utf-8", newline="").write(s2)
    print(name, "ok")


def one(s, a, b):
    assert s.count(a) == 1, (a[:90], s.count(a))
    return s.replace(a, b)


# ── service pages: the two intro paragraphs become one subtitle ─────────────────────────────────
SERVICE = {
    "services-interior-design": ("Every room designed, rendered and approved before a single wall is built.",
                                 "كل مساحة تُصمَّم وتُجسَّد وتُعتمد قبل بناء أي جدار."),
    "services-fitout": ("From raw shell to finished space, delivered turnkey by one accountable team.",
                        "من الهيكل الخام إلى المساحة المنجزة، تسليم على المفتاح بفريق واحد مسؤول."),
    "services-mep": ("The systems you never see, engineered into the design from day one.",
                     "الأنظمة التي لا تراها، مدمجة في التصميم منذ اليوم الأول."),
    "services-furniture": ("The final layer, sourced and placed to match the approved renders.",
                           "اللمسة الأخيرة، تُورَّد وتوضع مطابقة للتصورات المعتمدة."),
}
REVEAL = "opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);"
for page, (en, ar) in SERVICE.items():
    for lang, text in (("", en), (".ar", ar)):
        def fn(s, is_ar, text=text):
            s, n = re.subn(r'(<div style="flex:1;padding-top:clamp\(0px,3\.5vw,52px\);">)\s*<p\b[^>]*>.*?</p>\s*<p\b[^>]*>.*?</p>\s*(</div>)',
                           lambda m: f'{m.group(1)}\n        <p data-reveal data-reveal-delay="0.15" style="{REVEAL}{sub(is_ar)}">{text}</p>\n      {m.group(2)}',
                           s, count=1, flags=re.S)
            assert n == 1
            return s
        edit(f"{page}{lang}.dc.html", fn)

# ── Home: the disciplines and edge headers keep their sentence at subtitle size; Fit-Out gets one line ──
def home(s, ar):
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    old = f"font-family:{font};font-size:15px;line-height:1.8;color:#5B4636;max-width:400px;margin:0;"
    assert s.count(old) == 2, s.count(old)
    s = s.replace(old, sub(ar))
    fit = ("من الهيكل الخام إلى مساحة جاهزة للتسليم، مع تولّي كل التفاصيل الفنية عنك." if ar
           else "From raw shell to turnkey space, with every technical detail handled for you.")
    s, n = re.subn(r'<p style="font-family:[^"]*font-size:14px;line-height:1\.8;color:rgba\(214,194,168,0\.7\);margin-bottom:14px;">.*?</p>\s*'
                   r'<p style="font-family:[^"]*font-size:14px;line-height:1\.8;color:rgba\(214,194,168,0\.7\);margin-bottom:44px;">.*?</p>',
                   lambda m: f'<p style="{sub(ar, "#F5F2ED", "margin-bottom:44px;")}">{fit}</p>', s, count=1, flags=re.S)
    assert n == 1
    return s

edit("home.dc.html", home)
edit("home.ar.dc.html", home)

# ── About: the gates and disciplines intros, shorter and at subtitle size ─────────────────────────
def about(s, ar):
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    size = "clamp(22px,2vw,28px)" if ar else "clamp(20px,1.9vw,26px)"
    ls = "0" if ar else "-0.005em"
    s, n = re.subn(r"    #edge-gates \.gt-intro\{[^}]*\}",
                   f"    #edge-gates .gt-intro{{font-family:{font};font-size:{size};font-weight:500;line-height:1.4;letter-spacing:{ls};color:#F5F2ED;text-wrap:balance;margin:0;max-width:{'18em' if ar else '30ch'};}}", s, count=1)
    assert n == 1
    s, n = re.subn(r"    #disciplines \.sv-intro\{[^}]*\}",
                   f"    #disciplines .sv-intro{{font-family:{font};font-size:{size};font-weight:500;line-height:1.4;letter-spacing:{ls};color:#3A2D25;text-wrap:balance;margin:0;max-width:{'18em' if ar else '30ch'};}}", s, count=1)
    assert n == 1
    gates = ("ثلاث نقاط تحقق، في اللحظات التي يصعب فيها التراجع عن القرار." if ar
             else "Three checkpoints, placed where decisions become hardest to reverse.")
    disc = ("أربعة تخصصات تحت سقف واحد، حتى لا تضيع رؤيتك في أي مرحلة." if ar
            else "Four disciplines under one roof, so your vision is never lost along the way.")
    s, n = re.subn(r'(<p class="gt-intro"[^>]*>).*?(</p>)', lambda m: m.group(1) + gates + m.group(2), s, count=1, flags=re.S); assert n == 1
    s, n = re.subn(r'(<p class="sv-intro"[^>]*>).*?(</p>)', lambda m: m.group(1) + disc + m.group(2), s, count=1, flags=re.S); assert n == 1
    return s

edit("about-us.dc.html", about)
edit("about-us.ar.dc.html", about)

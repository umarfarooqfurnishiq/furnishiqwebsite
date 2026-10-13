"""Arabic project page: the story, the facts band, the closing draw and the portfolio corridor, as on the English page.

The English generators (pd_story.py, pd_cta.py, pd_next.py) are the master. This takes their sections and scripts,
puts the words into Arabic, sets the CSS for Arabic with ar_common.arabize() (GE SS Two, no letter-spacing, small sizes
brought up, more line-height for the headings) and turns round what is written with a physical left or right. The
Arabic page keeps its own data (titles, paragraphs, captions) and its slugs; the six views of every project are the
same pictures in the same order, so the parts point at the same gallery views.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/projects/pd_ar.py
"""
import io, os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "site"))
sys.path.insert(0, os.path.join(HERE, "..", "blog"))
import pd_story as S
import pd_cta as C
import pd_next as N
import draw_cta as D
from ar_common import arabize

PAGE = "project-detail.ar.dc.html"

# Arabic titles in the English portfolio order (the two PROJECTS lists share it)
TITLES = {
    "The Courtyard Residence": "مسكن الفناء",
    "Family Office HQ": "مقر المكتب العائلي",
    "Central Commons": "الساحة المركزية",
    "Obhur Beach Estate": "دارة شاطئ أبحر",
    "Desert Stone Resort": "منتجع الحجر الصحراوي",
    "The Executive Floors": "الطوابق التنفيذية",
    "Penthouse Above the Wadi": "بنتهاوس فوق الوادي",
    "Roastery House Flagship": "بيت المحمصة — الفرع الرئيسي",
    "Maison de Joaillerie": "دار المجوهرات",
    "The Furniture Gallery": "معرض الأثاث",
}
# the six part titles of every project, in the order of S.CHAPTERS
PARTS = {
    "The Courtyard Residence": ["ثلاثة أجنحة وفناء واحد", "جناح المجلس", "لوحة مواد محدودة", "هندسة في فواصل الظل", "أثاث مصنوع للغرف", "نطاق العمل"],
    "Family Office HQ": ["جدار هادئ نحو الشارع", "كل الغرف تطل على الفناء", "البناء النجدي بقراءة جديدة", "قاعة المجلس والمكتبة", "خصوصية تصنعها الهندسة", "أثاث يدوم جيلًا"],
    "Central Commons": ["الفضاء العام", "ساحة مصممة للمناخ", "الممر التجاري والردهة", "قاعة مطاعم لستمئة ضيف", "هندسة بحجم الفضاء العام", "عائلة واحدة من الأثاث"],
    "Obhur Beach Estate": ["ثلاثة مبانٍ على محور واحد", "القاعة الكبرى المطلة على البحر", "رواشين من خشب الساج", "لوحة مواد للساحل", "مصممة لهواء البحر المالح", "أثاث للساحل"],
    "Desert Stone Resort": ["مسار الضيف", "إطلالة واحدة في كل مرة", "لوحة مواد من الموقع", "المطعم وشرفة النار", "هندسة للصحراء", "أثاث من المكان"],
    "The Executive Floors": ["ثمانية طوابق في تنظيم عمودي", "وصول فوق المدينة", "مجلس الإدارة والأجنحة التنفيذية", "سقف خشب الجوز", "طوابق لتسعمئة موظف", "أثاث من المواد نفسها"],
    "Penthouse Above the Wadi": ["في مواجهة الوادي", "طابقان: للضيافة وللعائلة", "تضيئه السماء", "الدرج", "مناخ خلف الزجاج", "جلسات منخفضة"],
    "Roastery House Flagship": ["التحميص على مرأى الضيوف", "بار بطول أربعة عشر مترًا", "لوحة مواد من القهوة", "الطابق المعلّق", "إبعاد الدخان", "أثاث لضيوف يطيلون البقاء"],
    "Maison de Joaillerie": ["خلف حاجز برونزي", "الصالون الرئيسي", "الصالونات الخاصة", "مواد تُبرز الجمال", "الأمان والضوء", "مصنوع للدار"],
    "The Furniture Gallery": ["تسلسل من الغرف", "الردهة", "غرف معروضة كمساحات حقيقية", "استوديو التصميم", "صالة عرض تعيش على إضاءتها", "العرض كقطعة أثاث"],
}
CHAPTERS = {TITLES[en]: [(PARTS[en][i],) + tuple(c[1:]) for i, c in enumerate(rows)] for en, rows in S.CHAPTERS.items()}

FLIP = '<svg style="transform:scaleX(-1);" '


def swap(s, pairs, name):
    for o, n in pairs:
        assert o in s, (name, o)
        s = s.replace(o, n)
    return s


# ── the story ──
STORY = arabize(swap(S.SECTION, [
    ("The concept in six parts", "التصور في ستة أجزاء"),
    ('aria-label="In view"', 'aria-label="في الإطار"'),
    ("<i></i>In view</div>", "<i></i>في الإطار</div>"),
    ('<span class="pds-count" data-pds-count>', '<span class="pds-count" data-pds-count dir="ltr">'),
    ("Open this view full screen", "افتح هذه اللقطة بملء الشاشة"),
    ("{{ firstCaption }}, concept visualisation", "{{ firstCaption }}، تصور تصميمي"),
    ('aria-label="Parts"', 'aria-label="الأجزاء"'),
    ('aria-label="Part {{ ch.num }}: ', 'aria-label="الجزء {{ ch.num }}: '),
    ("<i></i>FurnishIQ scope</div><small>Lit: at work in this part</small>", "<i></i>نطاق عمل FurnishIQ</div><small>المضاء: حاضر في هذا الجزء</small>"),
    ('<li data-pds-d="d">Interior Design</li>', '<li data-pds-d="d">التصميم الداخلي</li>'),
    ('<li data-pds-d="f">Fit-Out</li>', '<li data-pds-d="f">التشطيبات</li>'),
    ('<li data-pds-d="m">MEP Engineering</li>', '<li data-pds-d="m">الهندسة الكهروميكانيكية</li>'),
    ('<li data-pds-d="u">Bespoke Furniture</li>', '<li data-pds-d="u">الأثاث المخصص</li>'),
    ('<a href="/contact" class="pds-cta" data-pd-similar>Discuss a similar project <svg ', '<a href="/ar/contact" class="pds-cta" data-pd-similar>ناقش مشروعاً مشابهاً ' + FLIP),
    # the paragraph hangs off the number column, on the right
    ("[data-pd-story] .pds-ch p{margin:0 0 0 56px;", "[data-pd-story] .pds-ch p{margin:0 56px 0 0;"),
    ("[data-pd-story] .pds-ch p{margin-left:0;}", "[data-pd-story] .pds-ch p{margin-right:0;}"),
], "story"), {
    "line-height:1.25;letter-spacing:-0.02em;color:rgba(245,242,237,0.5)": "line-height:1.5;letter-spacing:-0.02em;color:rgba(245,242,237,0.5)",
})
STORY_JS = swap(S.JS, [("imgs[k].dataset.cap + ', concept visualisation'", "imgs[k].dataset.cap + '، تصور تصميمي'")], "story js")

# ── the facts band ──
TB = arabize(swap(S.TITLEBLOCK, [
    ('<span class="ptb-k">Location</span>', '<span class="ptb-k">الموقع</span>'),
    ('<span class="ptb-k">Built-up area</span>', '<span class="ptb-k">المساحة المبنية</span>'),
    ('<span class="ptb-k">Status</span>', '<span class="ptb-k">الحالة</span>'),
    ('<span class="ptb-k">Scope</span>', '<span class="ptb-k">النطاق</span>'),
    # the Arabic scope is longer: below the one-row band it may wrap
    ("[data-pd-tb] .ptb-f{padding:0;}", "[data-pd-tb] .ptb-f{padding:0;}\n      [data-pd-tb] .ptb-v{white-space:normal;}"),
    ("[data-pd-tb] .ptb-f:nth-child(4) .ptb-v{white-space:nowrap;}", "[data-pd-tb] .ptb-f:nth-child(4) .ptb-v{white-space:normal;}"),
], "facts"))

# ── the closing draw ──
CA = dict(
    eyebrow="ابدأ مشروعاً", h1="أعجبك هذا التصور؟", h2="التصور التالي لك.",
    sub="يبدأ كل مشروع من FurnishIQ بورقة بيضاء وحديث.",
    cta="احجز استشارة مجانية", wa="راسل الاستوديو عبر واتساب",
    final="مشروعك · من التصور حتى التسليم", yours="مشروعك",
    services="تصميم داخلي · تشطيبات · أنظمة كهروميكانيكية · أثاث",
    again="أعد السحب", frame="اللوحة الحادية عشرة: مشروعك. اختر لإعادة السحب.",
)


def draw():
    text = f"""      <p class="pc-eyebrow"><i></i>{CA['eyebrow']}</p>
      <h2 class="pc-h2">{CA['h1']}<span>{CA['h2']}</span></h2>
      <p class="pc-sub">{CA['sub']}</p>
      <div class="pc-ctas">
        <a class="pc-cta" href="/ar/contact" data-pd-similar>{CA['cta']}{D.ARROW['ar']}</a>
        <a class="pc-wa" href="{{{{ waHref }}}}" target="_blank" rel="noopener">{CA['wa']}</a>
      </div>"""
    s = D.section("ar", label="CTA", text_html=text, items=[("@", "@")] * C.VIEWS, big="11", you=CA["yours"], svc=CA["services"],
                  final=CA["final"], frame_aria=CA["frame"], again=CA["again"], rounds=2)
    one = '          <img class="pc-img" data-src="@" data-cap="@" alt="" decoding="async">'
    assert s.count(one) == C.VIEWS
    loop = ('          <sc-for list="{{ gallery }}" as="shot" hint-placeholder-count="6">\n'
            '          <img class="pc-img" data-src="{{ shot.image }}" data-cap="{{ shot.caption }} · تصور" alt="" decoding="async">\n'
            '          </sc-for>')
    s = s.replace("\n".join([one] * C.VIEWS), loop)
    s = s.replace('<li><span dir="ltr">%02d</span></li>' % (C.VIEWS + 1), '<li><span dir="ltr">11</span></li>')
    return C.MARK + s


# ── the portfolio corridor ──
NEXT = arabize(swap(N.SECTION, [
    ("<i></i>The portfolio</div>", "<i></i>الأعمال</div>"),
    ("Ten concepts. <span>Next, {{ next.num }}.</span>", "عشرة تصورات. <span>التالي: {{ next.num }}.</span>"),
    ('<a class="pn-all" href="/projects">All projects <svg ', '<a class="pn-all" href="/ar/projects">كل المشاريع ' + FLIP),
    ('aria-label="The portfolio"', 'aria-label="الأعمال"'),
    ("{{ s.location }} · Concept</span>", "{{ s.location }} · تصور</span>"),
    ('<span class="pn-go">{{ s.go }} <svg ', '<span class="pn-go">{{ s.go }} ' + FLIP),
    ("<span>Point at any concept to open it.</span><span>{{ projNum }} / {{ projTotal }} · You are here</span>",
     '<span>أشر إلى أي تصور لفتحه.</span><span><span dir="ltr">{{ projNum }} / {{ projTotal }}</span> · أنت هنا</span>'),
    # the caption box, and the phone rows, sit on the right
    ("[data-pd-next] .pn-c{position:absolute;left:clamp(20px,2.4vw,36px);", "[data-pd-next] .pn-c{position:absolute;right:clamp(20px,2.4vw,36px);"),
    ("[data-pd-next] .pn-n{top:50%;left:20px;right:auto;", "[data-pd-next] .pn-n{top:50%;right:20px;left:auto;"),
    ("bottom:50%;left:64px;", "bottom:50%;left:auto;right:64px;"),
    ('.pn-tag{top:50%;inset-inline-start:auto;right:16px;', '.pn-tag{top:50%;inset-inline-start:auto;left:16px;'),
    ("[data-pd-next] .pn-c{left:12px;", "[data-pd-next] .pn-c{right:12px;"),
    # "Here", centred on its slice: from the right edge, the shift runs the other way
    ("inset-inline-start:50%;transform:translateX(-50%);", "inset-inline-start:50%;transform:translateX(50%);"),
], "corridor"), {
    "font-size:clamp(30px,3.4vw,50px);line-height:1.05;": "font-size:clamp(30px,3.4vw,50px);line-height:1.3;",
    "font-size:clamp(26px,2.6vw,40px);line-height:1.05;": "font-size:clamp(26px,2.6vw,40px);line-height:1.35;",
})
NEXT_CALC = swap(N.CALC, [
    ("href: `/project-detail?project=${this.slugify(p.title)}`", "href: `/ar/project-detail?project=${p.slug}`"),
    ("tag: state === 'here' ? 'Here' : state === 'next' ? 'Next' : ''", "tag: state === 'here' ? 'هنا' : state === 'next' ? 'التالي' : ''"),
    ("go: state === 'here' ? 'Back to the top' : 'View the concept'", "go: state === 'here' ? 'العودة إلى الأعلى' : 'شاهد التصور'"),
], "corridor calc")

SCOPE_SHORT = ("      scopeShort: ((det && det.scope) || '').replace('التصميم الداخلي', 'تصميم').replace('التشطيبات', 'تشطيبات')"
               ".replace('الهندسة الكهروميكانيكية', 'كهروميكانيك').replace('الأثاث المخصص', 'أثاث'),\n")
WA = ("      waHref: 'https://wa.me/966580330627?text=' + encodeURIComponent('مرحبًا FurnishIQ، شاهدت تصور «' + proj.title + '» على موقعكم وأرغب في مناقشة مشروع مشابه.'),\n")


def main():
    s = io.open(PAGE, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    s = s.replace("\r\n", "\n")

    # the story in place of the paragraphs and the facts sidebar
    a = s.index('<section data-screen-label="Project Body"') if '<section data-screen-label="Project Body"' in s else s.index("<!-- The story: six numbered parts")
    b = s.index("</section>", a) + len("</section>\n")
    s = s[:a] + STORY + s[b:]
    data = "  CHAPTERS = " + json.dumps({k: [list(c) for c in v] for k, v in CHAPTERS.items()}, ensure_ascii=False) + ";\n\n"
    if "  CHAPTERS = " in s:
        s = re.sub(r"  CHAPTERS = .*?;\n\n", lambda m: data, s, count=1, flags=re.S)
    else:
        i = s.index("  slugify(t)")
        s = s[:i] + data + s[i:]
    if "const chapters = (det" not in s:
        assert s.count(S.RENDER_OLD) == 1
        s = s.replace(S.RENDER_OLD, S.RENDER_NEW)
    if "PROJECT STORY" not in s:
        i = s.index("    // ── GALLERY LIGHTBOX")
        s = s[:i] + STORY_JS + s[i:]

    # the facts band over the foot of a full-height hero
    a = s.index('<section data-screen-label="Meta Strip"')
    c = s.rfind("<!-- The title block", 0, a)
    if c != -1 and a - c < 120:
        a = c
    b = s.index("</section>", a) + len("</section>\n")
    s = s[:a] + TB + s[b:]
    for o, n in [
        ('<section data-screen-label="Hero" style="position:relative;height:82vh;', '<section data-screen-label="Hero" class="fiq-pd-hero" style="position:relative;height:82vh;'),
        ('<a href="/ar/projects" style="position:absolute;top:104px;right:clamp(24px,5vw,80px);', '<a href="/ar/projects" style="position:absolute;top:104px;right:max(clamp(24px,5vw,80px),calc((100% - 1280px) / 2));'),
        ('<div style="position:absolute;left:0;right:0;bottom:0;z-index:1;max-width:1280px;margin:0 auto;width:100%;padding:0 clamp(24px,5vw,80px)',
         '<div class="fiq-pd-hero-text" style="position:absolute;left:0;right:0;bottom:0;z-index:1;max-width:1280px;box-sizing:content-box;margin:0 auto;padding:0 clamp(24px,5vw,80px)'),
    ]:
        if o in s:
            s = s.replace(o, n)
    assert 'class="fiq-pd-hero"' in s and 'class="fiq-pd-hero-text"' in s
    s = re.sub(r"      scopeShort: [^\n]*\n", "", s)
    s = s.replace("      chapters,\n", "      chapters,\n" + SCOPE_SHORT, 1)
    if "projNum:" not in s:
        s = s.replace("      chapters,\n", "      chapters,\n      projNum: String(this.PROJECTS.indexOf(proj) + 1).padStart(2, '0'),\n      projTotal: String(this.PROJECTS.length).padStart(2, '0'),\n", 1)
    if "TITLE BLOCK:" not in s:
        i = s.index("    // ── PROJECT STORY")
        s = s[:i] + S.TB_JS + s[i:]

    # the closing draw in place of the brochure form
    a = s.index(C.MARK) if C.MARK in s else s.index('<section data-screen-label="CTA"')
    b = s.index("</section>\n", a) + len("</section>\n")
    s = s[:a] + draw() + s[b:]
    s = C.BROCHURE_JS.sub("", s, count=1)
    assert "id-brochure-btn" not in s
    if "waHref:" not in s:
        s = s.replace("      chapters,\n", "      chapters,\n" + WA, 1)
    s = D.inject_js(s, "    // ── GALLERY LIGHTBOX", PAGE)

    # the portfolio corridor in place of the related projects
    for mark in (N.MARK, N.MARK_NEW):
        if mark in s:
            a = s.index(mark)
            b = s.index("</section>\n", a) + len("</section>\n")
            break
    else:
        a = s.index('<sc-if value="{{ hasRelated }}"')
        b = s.index("</sc-if>\n", a) + len("</sc-if>\n")
    s = s[:a] + NEXT + s[b:]
    if N.CALC_RE.search(s):
        s = N.CALC_RE.sub(lambda m: NEXT_CALC, s, count=1)
    else:
        assert s.count(N.CALC_ANCHOR) == 1
        s = s.replace(N.CALC_ANCHOR, NEXT_CALC + N.CALC_ANCHOR)
    if "      strip,\n" not in s:
        s = s.replace("      chapters,\n", "      chapters,\n      next: card(nextP),\n      strip,\n", 1)

    # styles of the old sections
    s = re.sub(r"\n\s*\.fiq-pd-(body|sidebar|meta|related)\{[^\n]*", "", s)
    for t in CHAPTERS:
        assert '"%s": {' % t in s, t
    io.open(PAGE, "w", encoding="utf-8", newline="").write(s.replace("\n", "\r\n") if crlf else s)
    print(PAGE, "story, facts band, closing draw and corridor built for", len(CHAPTERS), "projects")


if __name__ == "__main__":
    main()

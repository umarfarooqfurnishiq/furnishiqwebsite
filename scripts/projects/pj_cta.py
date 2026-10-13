"""Projects page, closing call: Project 11.

The grid above ends at ten concepts. The closing section draws the eleventh: the shared closing draw
(scripts/site/draw_cta.py) shuffles through the ten concept covers, numbered 01 to 10 and captioned as concepts, and
always comes to rest on 11, a blank sheet that reads "Your project". Beside it, the call: ten concepts above, the
eleventh is yours, with a consultation and WhatsApp.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/projects/pj_cta.py
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site"))
import draw_cta as D

# the ten concepts, in the grid's order: cover, English name, Arabic name
PROJECTS = [
    ("courtyard-residence-grand-majlis-riyadh", "The Courtyard Residence", "مسكن الفناء"),
    ("desert-stone-resort-lobby-lounge-alula", "Desert Stone Resort", "منتجع الحجر الصحراوي"),
    ("obhur-estate-great-room-red-sea-jeddah", "Obhur Beach Estate", "دارة شاطئ أبحر"),
    ("executive-floors-sky-lobby-reception-riyadh", "The Executive Floors", "الطوابق التنفيذية"),
    ("roastery-house-roasting-hall-riyadh", "Roastery House Flagship", "بيت المحمصة"),
    ("maison-joaillerie-main-salon-jeddah", "Maison de Joaillerie", "دار المجوهرات"),
    ("central-commons-plaza-dusk-riyadh", "Central Commons", "الساحة المركزية"),
    ("penthouse-wadi-double-height-living-riyadh", "Penthouse Above the Wadi", "بنتهاوس فوق الوادي"),
    ("family-office-courtyard-olive-tree-riyadh", "Family Office HQ", "مقر المكتب العائلي"),
    ("furniture-gallery-atrium-stair-riyadh", "The Furniture Gallery", "معرض الأثاث"),
]
C = {
    "en": dict(
        eyebrow="Start a Project", h1="Ten concepts above.", h2="The eleventh is yours.",
        sub="Every one of them began as a blank sheet and a conversation.",
        cta="Book Free Consultation", cta_href="/contact", wa="WhatsApp",
        concept="Concept", yours="Your project", final="Your project · Concept to handover",
        services="Interior Design · Fit-Out · MEP · Furniture",
        again="Draw again", frame="The eleventh sheet: your project. Select to draw again.",
    ),
    "ar": dict(
        eyebrow="ابدأ مشروعاً", h1="عشرة تصورات في الأعلى.", h2="والحادي عشر لك.",
        sub="بدأ كلٌّ منها بورقة بيضاء وحديث.",
        cta="احجز استشارة مجانية", cta_href="/ar/contact", wa="واتساب",
        concept="تصور", yours="مشروعك", final="مشروعك · من التصور حتى التسليم",
        services="تصميم داخلي · تشطيبات · أنظمة كهروميكانيكية · أثاث",
        again="أعد السحب", frame="اللوحة الحادية عشرة: مشروعك. اختر لإعادة السحب.",
    ),
}


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    text = f"""      <p class="pc-eyebrow"><i></i>{c['eyebrow']}</p>
      <h2 class="pc-h2">{c['h1']}<span>{c['h2']}</span></h2>
      <p class="pc-sub">{c['sub']}</p>
      <div class="pc-ctas">
        <a class="pc-cta" href="{c['cta_href']}">{c['cta']}{D.ARROW[lang]}</a>
        <a class="pc-wa" href="https://wa.me/966580330627" target="_blank" rel="noopener">{c['wa']}</a>
      </div>"""
    items = [(f"uploads/{b}-1280.webp", f"{c['concept']} · {an if ar else en}") for b, en, an in PROJECTS]
    return "<!-- ━━━━━━━━━━━━━━━━━━━━━ CTA BAND ━━━━━━━━━━━━━━━━━━━ -->\n" + D.section(
        lang, label="CTA", text_html=text, items=items, big=f"{len(PROJECTS) + 1:02d}", you=c["yours"], svc=c["services"],
        final=c["final"], frame_aria=c["frame"], again=c["again"])


OLD_BTN = re.compile(r"    const ctaBtn = document\.getElementById\('id-cta-btn'\);\n    if \(ctaBtn\) \{\n.*?\n    \}\n\n", re.S)
ANCHOR = "    document.addEventListener('mouseover', (e) => {\n      const el = e.target.closest && (e.target.closest('[data-detail-close]')"

if __name__ == "__main__":
    for name, lang in [("projects.dc.html", "en"), ("projects.ar.dc.html", "ar")]:
        s = open(name, encoding="utf-8").read()
        s, n = re.subn(r"<!-- ━+ CTA BAND ━+ -->\n<section data-screen-label=\"CTA\".*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
        assert n == 1, name
        s = OLD_BTN.sub("", s, count=1)   # the old band's button hover; the new call styles its own
        s = D.inject_js(s, ANCHOR, name)
        open(name, "w", encoding="utf-8", newline="").write(s)
        print(name, "ok")

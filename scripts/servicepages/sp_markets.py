"""Service pages, markets: the services page's sector accordion, lit for this service.

The same four-panel accordion as the services page (scripts/services/svc_markets.py, imported, not copied),
so the sectors read as one system across the site. Each service page gives it its own photographs, chosen
from the concept projects to show that service and to repeat nothing on the page or on the services page's
own panels, and its own heading.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/servicepages/sp_markets.py [page ...]
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "services"))
import svc_markets as M

PROJECTS = {k: p for k, _, _, p in M.SECTORS}
PAGE = {
    "services-interior-design": dict(
        sectors=[("Residential", "obhur-estate-master-suite-sea-view", "50% 50%"),
                 ("Hospitality", "desert-stone-resort-library-lounge", "50% 50%"),
                 ("Workplace", "executive-floors-boardroom-walnut-table", "50% 50%"),
                 ("Retail", "maison-joaillerie-private-salon", "50% 50%")],
        over=dict(
            en=dict(eyebrow="Markets We Serve", h2="Interior design across four sectors.",
                    body="Every sector, designed in-house and approved on screen before it is built.",
                    alts=["Master suite opening onto the Red Sea, Obhur Beach Estate",
                          "Library lounge in rammed earth and timber, Desert Stone Resort",
                          "Boardroom with a long walnut table, The Executive Floors",
                          "Private salon for jewellery viewings, Maison de Joaillerie"]),
            ar=dict(eyebrow="القطاعات التي نخدمها", h2="تصميم داخلي في أربعة قطاعات.",
                    body="كل قطاع يُصمَّم داخلياً ويُعتمد على الشاشة قبل التنفيذ.",
                    alts=["جناح رئيسي يطل على البحر الأحمر، دارة شاطئ أبحر",
                          "صالة مكتبة من التراب المدكوك والخشب، منتجع الحجر الصحراوي",
                          "قاعة اجتماعات بطاولة طويلة من خشب الجوز، الطوابق التنفيذية",
                          "صالون خاص لعرض المجوهرات، دار المجوهرات"]),
        )),
    "services-fitout": dict(
        sectors=[("Residential", "penthouse-wadi-oak-bronze-staircase-detail", "50% 50%"),
                 ("Hospitality", "roastery-house-leather-banquettes", "50% 50%"),
                 ("Workplace", "family-office-library-archive", "50% 50%"),
                 ("Retail", "maison-joaillerie-spiral-stair", "50% 50%")],
        over=dict(
            en=dict(eyebrow="Markets We Serve", h2="Fit-out across four sectors.",
                    body="Every sector, built by one site team and handed over ready for use.",
                    alts=["Oak and bronze staircase, Penthouse Above the Wadi",
                          "Leather banquettes and timber joinery, Roastery House Flagship",
                          "Library and archive in oak, Family Office HQ",
                          "Sculptural spiral stair, Maison de Joaillerie"]),
            ar=dict(eyebrow="القطاعات التي نخدمها", h2="تشطيبات في أربعة قطاعات.",
                    body="كل قطاع يُنفّذه فريق موقع واحد ويُسلَّم جاهزاً للاستخدام.",
                    alts=["درج من البلوط والبرونز، بنتهاوس فوق الوادي",
                          "مقاعد جلدية وأعمال نجارة خشبية، بيت المحمصة",
                          "مكتبة وأرشيف من البلوط، مقر المكتب العائلي",
                          "درج حلزوني منحوت، دار المجوهرات"]),
        )),
}

pages = sys.argv[1:] or list(PAGE)
for page in pages:
    P = PAGE[page]
    sectors = [(k, img, pos, PROJECTS[k]) for k, img, pos in P["sectors"]]
    for name, lang in [(f"{page}.dc.html", "en"), (f"{page}.ar.dc.html", "ar")]:
        s = open(name, encoding="utf-8").read()
        html = M.build(lang, sectors=sectors, over=P["over"], offset="80px")
        # the page's own markets block, or the accordion placed by an earlier run
        s, n = re.subn(r"<!-- ━+ (?:5\. )?MARKETS WE SERVE ━+ -->\n<section [^>]*data-screen-label=\"Markets(?: We Serve)?\".*?\n</section>\n", lambda m: html, s, count=1, flags=re.S)
        assert n == 1, name
        s = M.inject_js(s, name)
        open(name, "w", encoding="utf-8", newline="").write(s)
        print(name, "ok")

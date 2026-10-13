"""Arabic Insights page, in the English page's gallery-wall layout.

blog.dc.html is the master: a white masthead with one word set large, the three articles hung on a shared baseline,
largest first, each with its museum caption, then the archive. This rebuilds blog.ar.dc.html from it: the same CSS set
for Arabic (ar_common.arabize), the hero and entrance script lifted from the English page, the Arabic words supplied here.
The Arabic page is dir="rtl", so the largest article hangs at the right and the grid reads right to left.
Titles are the articles' own h1s, so the wall, the archive and the related cards agree.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/blog/blog_ar.py
"""
import io, re, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ar_common as C

EN, AR = "blog.dc.html", "blog.ar.dc.html"
HERO_A = "<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ HERO ━━ -->"
HERO_B = "<!-- ━━━━━━━━━━━━━━━━━━━━━━━━ ALL POSTS"

WALL = [
    # href, image, srcset/sizes, alt, number · category, name, sub
    ("/ar/insights/material-honesty", "uploads/penthouse-wadi-oak-bronze-staircase-detail-1200.webp",
     ' srcset="uploads/penthouse-wadi-oak-bronze-staircase-detail-1200.webp 1200w, uploads/penthouse-wadi-oak-bronze-staircase-detail-2400.webp 2400w" sizes="(max-width:960px) 100vw, 640px"',
     "تفصيل درج من خشب البلوط والبرونز", "01 · التصميم الداخلي", "الصدق في المواد", "لماذا التشطيبات التي تلمسها أهم من التي تراها"),
    ("/ar/insights/the-90-day-office", "uploads/executive-floors-boardroom-walnut-table-1280.webp", "",
     "طاولة اجتماعات من خشب الجوز في مكتب تنفيذي", "02 · التشطيبات", "مكتب في 90 يوماً", ""),
    ("/ar/insights/invisible-infrastructure", "uploads/executive-floors-walnut-ceiling-detail-1200.webp", "",
     "سقف من شرائح خشب الجوز يُخفي أنظمة المبنى", "03 · الهندسة", "البنية التحتية الخفية", ""),
]
POSTS_AR = {   # the articles' own titles
    "href: '/ar/insights/material-honesty'": "الصدق في المواد: لماذا التشطيبات التي تلمسها أهم من التي تراها",
    "href: '/ar/insights/the-90-day-office'": "مكتب في 90 يوماً: تقليص الجداول الزمنية للتشطيبات دون التنازل عن الجودة",
    "href: '/ar/insights/invisible-infrastructure'": "البنية التحتية الخفية: أنظمة كهروميكانيكية لن تلاحظها أبداً",
}


def hero(en):
    css = C.read_between(en, "  <style>\n    [data-blog-hero]{", "  </style>\n")[len("  <style>\n"):]
    css = C.arabize(css, {
        "line-height:0.86;": "line-height:1.12;",
        "font-size:min(11vw,15vh,168px);": "font-size:min(14vw,19vh,215px);",
        "line-height:1.75;color:#5B4636;}": "line-height:1.95;color:#5B4636;}",
        "font-weight:500;font-size:16px;line-height:1.35;": "font-weight:500;font-size:16px;line-height:1.55;",
        "font-size:14px;line-height:1.6;color:#8B6B4A;}": "font-size:14px;line-height:1.8;color:#8B6B4A;}",
    })
    cards = []
    for i, (href, img, ss, alt, meta, name, sub) in enumerate(WALL):
        n, _, cat = meta.partition(" · ")
        cards.append('''      <a href="%s" class="gw-card gw-in" style="--d:%ss;">
        <div class="gw-frame"><img src="%s"%s alt="%s"%s decoding="async"></div>
        <div class="gw-cap">
          <div class="gw-meta"><span>%s · %s</span><span>%s</span></div>
          <span class="gw-name">%s</span>%s
        </div>
      </a>''' % (href, ("0.3", "0.42", "0.54")[i], img, ss, alt, ' fetchpriority="high"' if i == 0 else "", n, cat, C.READ, name,
                 ('\n          <span class="gw-sub">%s</span>' % sub) if sub else ""))
    return '''<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ HERO ━━ -->
<!-- The gallery wall: one word, and the three articles hung on a shared baseline, largest first, each with its caption -->
<section data-screen-label="Hero" data-blog-hero style="position:relative;background:#FFFFFF;border-bottom:1px solid #E8DFD8;">
  <style>
%s  </style>

  <div class="gw-wrap">
    <div class="gw-head">
      <div class="gw-title gw-in" style="--d:0.05s;">
        <div class="gw-label"><i></i>مجلة FurnishIQ</div>
        <h1 class="gw-h1">رؤى<sup>03</sup></h1>
      </div>
      <div class="gw-intro gw-in" style="--d:0.2s;">
        <p>ملاحظات من استوديونا حول التصميم الداخلي والتشطيبات والهندسة، والتفاصيل التي تفرق بين المساحات الجيدة والمساحات الاستثنائية.</p>
        <div class="gw-topics">
          <a href="#archive" data-topic="التصميم الداخلي">التصميم الداخلي</a>
          <a href="#archive" data-topic="التشطيبات">التشطيبات</a>
          <a href="#archive" data-topic="الهندسة والأنظمة الكهروميكانيكية">الهندسة والأنظمة الكهروميكانيكية</a>
        </div>
      </div>
    </div>

    <div class="gw-wall">
%s
    </div>
  </div>
</section>

''' % (css, "\n".join(cards))


def main():
    en = io.open(EN, encoding="utf-8", newline="").read().replace("\r\n", "\n")
    s = io.open(AR, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    s = s.replace("\r\n", "\n")
    a, b = s.index(HERO_A), s.index(HERO_B)
    rebuilt = 'class="gw-wrap"' in s[a:b]
    s = s[:a] + hero(en) + s[b:]
    if rebuilt:   # already done once: only the hero is regenerated
        io.open(AR, "w", encoding="utf-8", newline="").write(s.replace(chr(10), chr(13)+chr(10)) if crlf else s)
        print(AR, "hero regenerated")
        return
    # the archive is where the topic links land
    old = '<section data-screen-label="All Posts" style="background:#FFFFFF;'
    assert s.count(old) == 1
    s = s.replace(old, '<section data-screen-label="All Posts" id="archive" style="scroll-margin-top:80px;background:#FFFFFF;')
    # old responsive rules for the replaced sections
    s, n = re.subn(r"\n\s*\.fiq-(blog-hero-grid|blog-hero-side|feat-hero|feat-img|feat-panel|featured-duo|feat-stagger)\{[^\n]*", "", s)
    assert n == 7, n
    s = C.dark_nav(s, AR)
    # script: the English page's entrance and topic links, in place of the word-by-word reveal
    j = en[en.index("    // ── HERO ENTRANCE + TOPIC LINKS"):en.index("    // ── CLOSING DRAW")]
    a, b = s.index("    // ── HERO ENTRANCE"), s.index("    // ── CLOSING DRAW")
    s = s[:a] + j + s[b:]
    a, b = s.index("    // ── FEATURE CARD HOVERS"), s.index("    // ── POST ROW HOVERS")
    s = s[:a] + s[b:]
    s = s.replace("a.style.transform = 'translateX(4px)'", "a.style.transform = 'translateX(-4px)'")
    # the articles' own titles, and one category list
    for key, title in POSTS_AR.items():
        i = s.index(key)
        a = s.rindex("      title: '", 0, i)   # this post's own title line, the nearest one above its href
        b = s.index("',\n", a)
        s = s[:a] + "      title: '" + title + s[b:]
    io.open(AR, "w", encoding="utf-8", newline="").write(s.replace("\n", "\r\n") if crlf else s)
    print(AR, "rebuilt")


if __name__ == "__main__":
    main()

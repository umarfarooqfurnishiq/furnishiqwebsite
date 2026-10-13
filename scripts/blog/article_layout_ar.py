"""Arabic article pages, in the English articles' editorial layout.

The English pages are the master (scripts/blog/article_layout.py). This rebuilds each blog-*.ar.dc.html body from the
words already on the page: a white masthead with the title set large, a wide plate with a museum caption, a sticky
contents rail, a reading column that figures and the pull quote break out of, a short-version panel, the closing call,
a sign-off, then the related articles as captioned frames. The CSS is the English CSS set for Arabic (ar_common.arabize).
The page is dir="rtl": the rail sits at the right and the arrows point the other way.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/blog/article_layout_ar.py
"""
import io, re, os, sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ar_common as C
import article_layout as A

PAGES = {
    "blog-material-honesty.ar.dc.html": "تفصيل درج من خشب البلوط والبرونز",
    "blog-the-90-day-office.ar.dc.html": "طاولة اجتماعات من خشب الجوز في مكتب تنفيذي",
    "blog-invisible-infrastructure.ar.dc.html": "سقف من شرائح خشب الجوز يُخفي أنظمة المبنى",
}
# the articles' own titles (their h1s): the related cards use them too
TITLES = {
    "material-honesty": "الصدق في المواد: لماذا التشطيبات التي تلمسها أهم من التي تراها",
    "the-90-day-office": "مكتب في 90 يوماً: تقليص الجداول الزمنية للتشطيبات دون التنازل عن الجودة",
    "invisible-infrastructure": "البنية التحتية الخفية: أنظمة كهروميكانيكية لن تلاحظها أبداً",
}
CTA = {
    "blog-material-honesty.ar.dc.html": ("الصدق في المواد", "هل تخطط لمساحة تهمّ فيها التفاصيل؟",
        "تحدد FurnishIQ كل تشطيب في متناول اليد.", "التصميم الداخلي", "/ar/services-interior-design"),
    "blog-the-90-day-office.ar.dc.html": ("مكتب في 90 يوماً", "هل تعمل ضمن موعد افتتاح ثابت؟",
        "تضع FurnishIQ البرنامج الزمني معك منذ المخطط الأول.", "التشطيبات", "/ar/services-fitout"),
    "blog-invisible-infrastructure.ar.dc.html": ("البنية التحتية الخفية", "هل تنسّق الأنظمة الكهروميكانيكية لمشروعك القادم؟",
        "تهندسها FurnishIQ داخلياً، جنباً إلى جنب مع التصميم.", "الهندسة والأنظمة الكهروميكانيكية", "/ar/services-mep"),
}
MONTHS = "يناير|فبراير|مارس|أبريل|مايو|يونيو|يوليو|أغسطس|سبتمبر|أكتوبر|نوفمبر|ديسمبر"
FWD, BACK = A.ARROW_L, A.ARROW_R   # in RTL, forward points left
HERO_MARK = "<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ HERO ━━ -->"
ART_MARK = "<!-- ━━━━━━━━━━━━━━━━━━━━━━━━ ARTICLE"
FOOT_MARK = "<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ FOOTER"

CSS = C.arabize(A.CSS, {
    "line-height:1.02;letter-spacing:-0.035em;": "line-height:1.3;letter-spacing:-0.035em;",
    "max-width:16.5em;": "max-width:15em;",
    "font-size:clamp(20px,1.75vw,25px);line-height:1.6;": "font-size:clamp(21px,1.9vw,26px);line-height:1.8;",
    "font-size:17px;line-height:1.85;color:#3A2D25;": "font-size:18px;line-height:2;color:#3A2D25;",
    "font-size:clamp(25px,2.3vw,34px);line-height:1.2;": "font-size:clamp(25px,2.3vw,34px);line-height:1.5;",
    "line-height:1.18!important;": "line-height:1.5!important;",
    "line-height:1.12;letter-spacing:-0.025em;color:#F5F2ED;": "line-height:1.5;letter-spacing:-0.025em;color:#F5F2ED;",
    "font-size:clamp(30px,3.6vw,56px);line-height:1;": "font-size:clamp(30px,3.6vw,56px);line-height:1.4;",
    "margin-right:8px;": "margin-inline-end:8px;",
    "translateX(4px)": "translateX(-4px)",
    "line-height:1.35;letter-spacing:-0.01em;color:#1F1F1F;text-wrap:balance;}": "line-height:1.55;letter-spacing:-0.01em;color:#1F1F1F;text-wrap:balance;}",
    "font-size:14px;line-height:1.6;color:#1F1F1F;}": "font-size:14px;line-height:1.8;color:#1F1F1F;}",
    "font-size:13.5px;line-height:1.65;color:#5B4636;}": "font-size:13.5px;line-height:1.85;color:#5B4636;}",
    "font-size:13.5px;line-height:1.45;color:#8B7A6B;": "font-size:13.5px;line-height:1.65;color:#8B7A6B;",
})


def parse(page):
    hero = page[page.index(HERO_MARK):page.index(ART_MARK)]
    d = {}
    d["category"] = A.text(re.findall(r'<span style="[^"]*color:rgba\(214,194,168,0\.9\);">(.*?)</span>', hero)[0])
    h1 = hero[hero.index("<h1"):hero.index("</h1>")].split(">", 1)[1]
    d["title"] = re.sub(r"\s+", " ", A.text(h1.replace("</span></span>", " "))).strip()
    d["date"] = re.search(r"\d+ (%s) \d{4}" % MONTHS, hero).group(0)
    d["image"] = re.search(r"url\('(uploads/[^']+)'\)", hero).group(1)
    art = page[page.index("<article>") + 9:page.index("<!-- AUTHOR -->")]
    blocks, i = [], 0
    while True:
        m = re.compile(r"\S").search(art, i)
        if not m:
            break
        i = m.start()
        if art.startswith("<p", i):
            j = A.block_end(art, i, "p")
            chunk = art[i:j]
            inner = chunk.split(">", 1)[1][:-4]
            blocks.append(("lead" if "font-weight:500" in chunk.split(">", 1)[0] and not blocks else "p", inner.strip()))
        elif art.startswith("<h2", i):
            j = A.block_end(art, i, "h2")
            chunk = art[i:j]
            hid = re.search(r'id="([^"]+)"', chunk).group(1)
            num = A.text(re.search(r"<span[^>]*>(.*?)</span>", chunk).group(1))
            title = A.text(re.sub(r"<span[^>]*>.*?</span>", "", chunk.split(">", 1)[1]))
            blocks.append(("h2", (hid, num, title)))
        elif art.startswith("<figure", i):
            j = A.block_end(art, i, "figure")
            chunk = art[i:j]
            attrs = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', re.search(r"<img ([^>]*)>", chunk).group(1)))
            blocks.append(("fig", (attrs["src"], attrs.get("srcset", ""), attrs.get("alt", ""), A.text(re.search(r"<figcaption[^>]*>(.*?)</figcaption>", chunk, re.S).group(1)))))
        elif art.startswith("<blockquote", i):
            j = A.block_end(art, i, "blockquote")
            chunk = art[i:j]
            blocks.append(("quote", (A.text(re.search(r"<p[^>]*>(.*?)</p>", chunk, re.S).group(1)), A.text(re.search(r"<footer[^>]*>(.*?)</footer>", chunk, re.S).group(1)))))
        elif art.startswith("<div", i):
            chunk = art[i:]
            label = A.text(re.search(r'text-transform:uppercase;color:#8B6B4A;">(.*?)</span>', chunk).group(1))
            blocks.append(("short", (label, [A.text(x) for x in re.findall(r"<p[^>]*>(.*?)</p>", chunk, re.S)])))
            break
        else:
            raise ValueError("unexpected block at: " + art[i:i + 80])
        i = j
    d["blocks"] = blocks
    auth = page[page.index("<!-- AUTHOR -->"):page.index("</article>")]
    d["author_desc"] = A.text(re.search(r"<p[^>]*>(.*?)</p>", auth, re.S).group(1))
    return d


def share():
    return ('<div class="pa-share"><span class="pa-share-label">مشاركة</span>'
            '<a href="#" data-share="x" target="_blank" rel="noopener" aria-label="مشاركة على X">%s</a>'
            '<a href="#" data-share="linkedin" target="_blank" rel="noopener" aria-label="مشاركة على LinkedIn">%s</a>'
            '<button type="button" data-share="copy" aria-label="نسخ الرابط">%s</button></div>') % (A.ICON_X, A.ICON_IN, A.ICON_LINK)


def build(d, hero_alt, cta):
    short, question, answer, service, service_href = cta
    wa = A.WA + quote('مرحباً FurnishIQ، قرأت "%s" وأرغب في مناقشة مشروعي.' % short)
    main, _, rest = d["title"].partition(":")
    img = d["image"]
    base = re.sub(r"-\d+\.webp$", "", img)
    srcset = "%s-1200.webp 1200w, %s 2400w" % (base, img)
    esc = A.esc
    h = []
    h.append(HERO_MARK)
    h.append('<!-- The masthead: back to Insights, the facts, the title set large, the byline, and the plate with its caption -->')
    h.append('<section data-screen-label="Post Hero" class="ph" data-post-hero>' + CSS)
    h.append('  <div class="ph-wrap">')
    h.append('    <div class="ph-top ph-in" style="--d:0.05s;">')
    h.append('      <a href="/ar/insights" class="ph-back">%sرؤى</a>' % BACK)
    h.append('      <div class="ph-meta"><span>%s</span><span>%s</span><span>%s</span></div>' % (esc(d["category"]), d["date"], C.READ))
    h.append('    </div>')
    h.append('    <h1 class="ph-h1 ph-in" style="--d:0.15s;"><span class="ph-h1-main">%s:</span> <span class="ph-h1-sub">%s</span></h1>' % (esc(main.strip()), esc(rest.strip())))
    h.append('    <div class="ph-by ph-in" style="--d:0.3s;">')
    h.append('      <div class="ph-author"><span class="ph-mark">IQ</span><div><b>استوديو FurnishIQ</b><small>فريق التصميم والتنفيذ</small></div></div>')
    h.append('      ' + share())
    h.append('    </div>')
    h.append('  </div>')
    h.append('  <figure class="ph-plate ph-in" style="--d:0.4s;">')
    h.append('    <div class="ph-frame"><img src="%s" srcset="%s" sizes="(max-width:1360px) 100vw, 1280px" alt="%s" fetchpriority="high" decoding="async"></div>' % (img, srcset, hero_alt))
    h.append('    <figcaption class="pa-cap">%s، تصور تصميمي.</figcaption>' % hero_alt)
    h.append('  </figure>')
    h.append('</section>')
    h.append('')
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━━━━ ARTICLE ━━━━━━━━━━━━━━━━━ -->')
    h.append('<section data-screen-label="Article" class="pa" id="article">')
    h.append('  <div class="pa-grid">')
    h.append('    <aside class="pa-rail">')
    h.append('      <div class="pa-label">في هذه المقالة</div>')
    h.append('      <nav aria-label="المحتويات"><ol class="pa-toc">')
    for kind, v in d["blocks"]:
        if kind == "h2":
            h.append('        <li><a href="#%s" data-toc data-toc-target="%s"><span>%s</span>%s</a></li>' % (v[0], v[0], v[1], esc(v[2])))
    h.append('      </ol></nav>')
    h.append('      <div class="pa-talk">')
    h.append('        <div class="pa-label">ناقش مشروعك</div>')
    h.append('        <p>تحدث مع الاستوديو عن مساحتك.</p>')
    h.append('        <a href="/ar/contact" data-blog-cta="consultation" data-cta-place="rail">احجز استشارة مجانية %s</a>' % FWD)
    h.append('        <a href="%s" target="_blank" rel="noopener" data-blog-cta="whatsapp" data-cta-place="rail">واتساب %s</a>' % (wa, FWD))
    h.append('      </div>')
    h.append('    </aside>')
    h.append('')
    h.append('    <article class="pa-body">')
    for kind, v in d["blocks"]:
        if kind == "lead":
            h.append('      <p class="pa-lead">%s</p>' % v)
        elif kind == "p":
            h.append('      <p>%s</p>' % v)
        elif kind == "h2":
            h.append('      <h2 id="%s" class="pa-h2"><span>%s</span>%s</h2>' % (v[0], v[1], esc(v[2])))
        elif kind == "fig":
            src, ss, alt, cap = v
            h.append('      <figure class="pa-fig pa-wide">')
            h.append('        <div class="pa-frame"><img src="%s"%s sizes="(max-width:960px) 100vw, 980px" alt="%s" loading="lazy" decoding="async"></div>' % (src, (' srcset="%s"' % ss) if ss else "", alt))
            h.append('        <figcaption class="pa-cap">%s</figcaption>' % esc(cap))
            h.append('      </figure>')
        elif kind == "quote":
            h.append('      <blockquote class="pa-quote pa-wide">')
            h.append('        <p>%s</p>' % esc(v[0]))
            h.append('        <footer>%s</footer>' % esc(v[1]))
            h.append('      </blockquote>')
        elif kind == "short":
            label, items = v
            h.append('      <aside class="pa-short">')
            h.append('        <div class="pa-label">%s</div>' % esc(label))
            h.append('        <ol>')
            for k, it in enumerate(items, 1):
                h.append('          <li><span>%02d</span>%s</li>' % (k, esc(it)))
            h.append('        </ol>')
            h.append('      </aside>')
    h.append('')
    h.append('      <aside class="pa-cta pa-wide" aria-label="اعمل مع FurnishIQ">')
    h.append('        <div>')
    h.append('          <div class="pa-label"><i></i>اعمل مع FurnishIQ</div>')
    h.append('          <div class="pa-cta-q">%s<span>%s</span></div>' % (esc(question), esc(answer)))
    h.append('        </div>')
    h.append('        <div class="pa-cta-acts">')
    h.append('          <a href="/ar/contact" class="pa-cta-btn" data-blog-cta="consultation" data-cta-place="end">احجز استشارة مجانية %s</a>' % FWD)
    h.append('          <a href="%s" class="pa-cta-link" data-blog-cta="service" data-cta-place="end">خدمات %s %s</a>' % (service_href, service, FWD))
    h.append('        </div>')
    h.append('      </aside>')
    h.append('')
    h.append('      <footer class="pa-sign">')
    h.append('        <div class="pa-sign-who"><span class="ph-mark">IQ</span><div><small>بقلم</small><b>استوديو FurnishIQ</b><span>%s</span></div></div>' % esc(d["author_desc"]))
    h.append('        ' + share())
    h.append('      </footer>')
    h.append('    </article>')
    h.append('  </div>')
    h.append('</section>')
    h.append('')
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━ RELATED ━━━━━━━━━━━━━━━━━━━━ -->')
    h.append('<section data-screen-label="Related" class="pr">')
    h.append('  <div class="pr-wrap">')
    h.append('    <div class="pr-head">')
    h.append('      <div><div class="pa-label">واصل القراءة</div><h2 class="pr-h2">المزيد من المجلة.</h2></div>')
    h.append('      <a href="/ar/insights" class="pr-all">جميع الرؤى %s</a>' % FWD)
    h.append('    </div>')
    h.append('    <div class="pr-grid">')
    h.append('      <sc-for list="{{ related }}" as="post" hint-placeholder-count="2">')
    h.append('        <a href="{{ post.href }}" class="pr-card">')
    h.append('          <div class="pa-frame"><img src="{{ post.image }}" alt="{{ post.title }}" loading="lazy" decoding="async"></div>')
    h.append('          <div class="pr-cap"><div class="pr-meta">{{ post.category }} · {{ post.read }}</div><span class="pr-t">{{ post.title }}</span></div>')
    h.append('        </a>')
    h.append('      </sc-for>')
    h.append('    </div>')
    h.append('  </div>')
    h.append('</section>')
    h.append('')
    return "\n".join(h) + "\n"


def main():
    for name, hero_alt in PAGES.items():
        s = io.open(name, encoding="utf-8", newline="").read()
        crlf = "\r\n" in s
        s = s.replace("\r\n", "\n")
        if 'class="ph"' in s:
            print(name, "already rebuilt")
            continue
        d = parse(s)
        a, b = s.index(HERO_MARK), s.index(FOOT_MARK)
        s = s[:a] + build(d, hero_alt, CTA[name]) + s[b:]
        s = re.sub(r"\n\s*\.fiq-(article-grid|article-rail|related-grid|author-card)\{[^\n]*", "", s)
        s = C.dark_nav(s, name)
        a = s.index(A.JS_HERO_OLD_START)
        b = s.index("    // ── SCROLL REVEAL")
        s = s[:a] + A.JS_HERO_NEW + s[b:]
        a = s.index("    // ── TOC ACTIVE STATE")
        b = s.index("</script>", a) + len("</script>")
        s = s[:a] + A.JS_TOC.replace("'Link copied'", "'تم نسخ الرابط'") + s[b:]
        # related cards: the articles' own titles and the honest read time
        for slug, t in TITLES.items():
            s = re.sub(r"(title: \")[^\"]*(\",\n\s*image: [^\n]*\n\s*href: '/ar/insights/%s')" % slug, lambda m: m.group(1) + t + m.group(2), s)
        s = re.sub(r'read: "\d+ دقائق قراءة"', 'read: "%s"' % C.READ, s)
        io.open(name, "w", encoding="utf-8", newline="").write(s.replace("\n", "\r\n") if crlf else s)
        print(name, "rebuilt:", sum(1 for k, _ in d["blocks"] if k == "p"), "paragraphs,", sum(1 for k, _ in d["blocks"] if k == "h2"), "sections |", d["title"])


if __name__ == "__main__":
    main()

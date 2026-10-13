"""Project page, closing call: the next one is yours.

The page closed on an MEP brochure form, which was off-subject on most project pages. It now closes on the shared
closing draw (scripts/site/draw_cta.py), as the projects page and the Insights page do: the drafting frame shuffles
through this project's own six views, twice, slowing, and always comes to rest on a blank sheet numbered 11, the
eleventh project after the portfolio's ten, which is the visitor's. Beside it: a consultation, and WhatsApp with a
message that names the project being looked at.
The views come from the page's own gallery data, so every project draws its own rooms.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/projects/pd_cta.py
"""
import io, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site"))
import draw_cta as D

PAGE = "project-detail.dc.html"
VIEWS = 6   # every project has six views
C = dict(
    eyebrow="Start a Project", h1="Like this concept?", h2="The next one is yours.",
    sub="Every FurnishIQ project begins with a blank sheet and a conversation.",
    cta="Book Free Consultation", wa="WhatsApp the studio",
    final="Your project · Concept to handover", yours="Your project",
    services="Interior Design · Fit-Out · MEP · Furniture",
    again="Draw again", frame="The eleventh sheet: your project. Select to draw again.",
)
MARK = "<!-- ━━━━━━━━━━━━━━━━━━━━━ CTA BAND ━━━━━━━━━━━━━━━━━━━ -->\n"


def build():
    text = f"""      <p class="pc-eyebrow"><i></i>{C['eyebrow']}</p>
      <h2 class="pc-h2">{C['h1']}<span>{C['h2']}</span></h2>
      <p class="pc-sub">{C['sub']}</p>
      <div class="pc-ctas">
        <a class="pc-cta" href="/contact" data-pd-similar>{C['cta']}{D.ARROW['en']}</a>
        <a class="pc-wa" href="{{{{ waHref }}}}" target="_blank" rel="noopener">{C['wa']}</a>
      </div>"""
    items = [("@", "@")] * VIEWS
    s = D.section("en", label="CTA", text_html=text, items=items, big="11", you=C["yours"], svc=C["services"],
                  final=C["final"], frame_aria=C["frame"], again=C["again"], rounds=2)
    # the six views come from the page's gallery, not a fixed list
    one = '          <img class="pc-img" data-src="@" data-cap="@" alt="" decoding="async">'
    assert s.count(one) == VIEWS
    loop = ('          <sc-for list="{{ gallery }}" as="shot" hint-placeholder-count="6">\n'
            '          <img class="pc-img" data-src="{{ shot.image }}" data-cap="{{ shot.caption }} · Concept" alt="" decoding="async">\n'
            '          </sc-for>')
    s = s.replace("\n".join([one] * VIEWS), loop)
    # the last tick is the eleventh sheet
    s = s.replace('<li><span dir="ltr">%02d</span></li>' % (VIEWS + 1), '<li><span dir="ltr">11</span></li>')
    return MARK + s


BROCHURE_JS = re.compile(r"    const ctaBtn = document\.getElementById\('id-brochure-btn'\);\n    if \(ctaBtn\) \{\n.*?\n    \}\n\n", re.S)
RENDER_OLD = "      chapters,\n"
RENDER_NEW = ("      chapters,\n"
              "      waHref: 'https://wa.me/966580330627?text=' + encodeURIComponent('Hello FurnishIQ, I saw the ' + proj.title + ' concept on your website and would like to discuss a similar project.'),\n")


def main():
    s = io.open(PAGE, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    s = s.replace("\r\n", "\n")
    if MARK in s:   # rebuilt before
        a = s.index(MARK)
    else:
        a = s.index('<section data-screen-label="CTA"')
    b = s.index("</section>\n", a) + len("</section>\n")
    s = s[:a] + build() + s[b:]
    s = BROCHURE_JS.sub("", s, count=1)   # the brochure form's script went with the form
    assert "id-brochure-btn" not in s
    if "waHref:" not in s:
        assert s.count(RENDER_OLD) == 1
        s = s.replace(RENDER_OLD, RENDER_NEW)
    s = D.inject_js(s, "    // ── GALLERY LIGHTBOX", PAGE)
    io.open(PAGE, "w", encoding="utf-8", newline="").write(s.replace("\n", "\r\n") if crlf else s)
    print(PAGE, "closing draw built")


if __name__ == "__main__":
    main()

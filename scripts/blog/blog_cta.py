"""Insights page, closing call: the next insight is yours.

The newsletter band, in the projects page's closing draw (scripts/site/draw_cta.py): the frame shuffles through the
published articles' covers, captioned with their category and short title, runs through them twice while there are
few of them, and always comes to rest on the next number, a blank sheet that reads "The next insight · in your inbox".
Beside it, the sign-up: the page's own newsletter form, its bindings unchanged.
The articles are read from the page's own POSTS list, so the count and the next number stay right as articles are
added: rerun after publishing one.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/blog/blog_cta.py
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site"))
import draw_cta as D

WORDS = {
    "en": {3: ("Three", "fourth"), 4: ("Four", "fifth"), 5: ("Five", "sixth"), 6: ("Six", "seventh"), 7: ("Seven", "eighth"), 8: ("Eight", "ninth"), 9: ("Nine", "tenth")},
    "ar": {3: ("ثلاث", "الرابعة"), 4: ("أربع", "الخامسة"), 5: ("خمس", "السادسة"), 6: ("ست", "السابعة"), 7: ("سبع", "الثامنة"), 8: ("ثماني", "التاسعة"), 9: ("تسع", "العاشرة")},
}
C = {
    "en": dict(
        eyebrow="Join the IQ", h1="{n} insights above.", h2="The {nth} arrives by email.",
        sub="One thoughtful email a month. No noise, ever.",
        ph="Your email address", btn="Subscribe", ok="Thank you — monthly insights, strictly no spam.",
        you="The next insight", svc="In your inbox, once a month", final="Insight {k} · In your inbox",
        frame="The next insight arrives by email. Select to draw again.", again="Draw again",
    ),
    "ar": dict(
        eyebrow="انضم إلى IQ", h1="{n} رؤى في الأعلى.", h2="و{nth} تصلك بالبريد.",
        sub="بريد إلكتروني مدروس شهرياً. دون أي إزعاج، أبداً.",
        ph="بريدك الإلكتروني", btn="اشترك", ok="شكراً لك — رؤى شهرية، دون أي رسائل مزعجة.",
        you="الرؤية التالية", svc="في بريدك، مرة كل شهر", final="الرؤية {k} · في بريدك",
        frame="الرؤية التالية تصلك بالبريد. اختر لإعادة السحب.", again="أعد السحب",
    ),
}
POST = re.compile(r"category: '([^']*)',[^\n]*\n\s*title: '((?:[^'\\]|\\.)*)',.*?image: '([^']*)'", re.S)


def posts(s):
    block = s[s.index("POSTS = ["):s.index("];", s.index("POSTS = ["))]
    out = []
    for cat, title, img in POST.findall(block):
        short = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), title.split(":")[0]).strip()
        out.append((img, f"{cat} · {short}"))
    return out


def build(lang, items):
    c = C[lang]
    n = len(items)
    count, nth = WORDS[lang].get(n, (str(n), ""))
    h2 = c["h2"].format(nth=nth) if nth else ("The next arrives by email." if lang == "en" else "والتالية تصلك بالبريد.")
    text = f"""      <p class="pc-eyebrow"><i></i>{c['eyebrow']}</p>
      <h2 class="pc-h2">{c['h1'].format(n=count)}<span>{h2}</span></h2>
      <p class="pc-sub">{c['sub']}</p>
      <div class="pc-form">
        <input type="email" placeholder="{c['ph']}" aria-label="{c['ph']}" autocomplete="email" dir="ltr" value="{{{{ newsletterEmail }}}}" onChange="{{{{ onNewsletterChange }}}}">
        <button type="button" onClick="{{{{ onNewsletterSubmit }}}}">{c['btn']}{D.ARROW[lang]}</button>
      </div>
      <sc-if value="{{{{ newsletterStatus }}}}" hint-placeholder-val="{{{{ null }}}}">
        <p class="pc-ok" role="status">{c['ok']}</p>
      </sc-if>"""
    k = f"{n + 1:02d}"
    return "<!-- ━━━━━━━━━━━━━━━━━━━━━ NEWSLETTER BAND ━━━━━━━━━━━━ -->\n" + D.section(
        lang, label="Newsletter", text_html=text, items=items, big=k, you=c["you"], svc=c["svc"],
        final=c["final"].format(k=k), frame_aria=c["frame"], again=c["again"], rounds=2 if n < 5 else 1)


if __name__ == "__main__":
    for name, lang in [("blog.dc.html", "en"), ("blog.ar.dc.html", "ar")]:
        s = open(name, encoding="utf-8").read()
        items = posts(s)
        assert len(items) >= 2, (name, items)
        s, n = re.subn(r"<!-- ━+ NEWSLETTER BAND ━+ -->\n<section data-screen-label=\"Newsletter\".*?\n</section>\n", lambda m: build(lang, items), s, count=1, flags=re.S)
        assert n == 1, name
        s = D.inject_js(s, "    // ── SCROLL REVEAL", name)
        open(name, "w", encoding="utf-8", newline="").write(s)
        print(name, "ok", len(items), "articles:", " | ".join(cap for _, cap in items))

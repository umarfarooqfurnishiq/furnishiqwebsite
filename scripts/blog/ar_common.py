"""Shared by the Arabic Insights and article generators: the English page's CSS, set for Arabic.

The English pages are the master. An Arabic page takes the same CSS and changes only what Arabic needs: GE SS Two for
Lama Sans, no letter-spacing (it breaks the joined letters), the small caps-size labels brought up to a size the script
can carry, and anything that points left or right turned round. The page is dir="rtl", so grids and flex rows already
mirror; only the things written with a physical direction need the turn.
"""
import re

FONT_EN = "'Lama Sans',sans-serif"
FONT_AR = "'GE SS Two','Arial',sans-serif"
READ = "3 دقائق قراءة"   # 390-450 Arabic words: under three minutes at about 170 words a minute


def _size(m):
    v = float(m.group(1))
    if v < 13:
        v = max(12, v + 2.5)
    elif v <= 17:
        v += 1.5
    return "font-size:%gpx" % (round(v * 2) / 2)


def arabize(css, lines=None):
    for old, new in (lines or {}).items():   # written against the English CSS
        assert old in css, old
        css = css.replace(old, new)
    css = css.replace(FONT_EN, FONT_AR)
    css = re.sub(r"letter-spacing:[^;}\"]*;?", "", css)
    css = re.sub(r"font-size:(\d+(?:\.\d+)?)px", _size, css)
    return css.replace("transform-origin:left", "transform-origin:right")


def read_between(s, a, b):
    i = s.index(a)
    return s[i:s.index(b, i)]


NAV_PAIRS = [
    ("      const s = window.scrollY > 60;\n      if (!nav) return;\n",
     "      const s = window.scrollY > 60;\n      if (!nav) return;\n      const dark = s || nav.hasAttribute('data-nav-dark');   // white hero: dark text from the top\n"),
    ("      if (logoW) logoW.style.opacity = s ? '0' : '1';\n      if (logoD) logoD.style.opacity = s ? '1' : '0';",
     "      if (logoW) logoW.style.opacity = dark ? '0' : '1';\n      if (logoD) logoD.style.opacity = dark ? '1' : '0';"),
    ("        l.style.color = s ? '#1F1F1F' : '#FFFFFF';\n        if (l !== navBlogLink) l.style.opacity = s ? '1' : '0.8';",
     "        l.style.color = dark ? '#1F1F1F' : '#FFFFFF';\n        if (l !== navBlogLink) l.style.opacity = dark ? '1' : '0.8';"),
    ("        navCta.style.color = s ? '#1F1F1F' : '#FFFFFF';\n        navCta.style.borderColor = s ? 'rgba(91,70,54,0.35)' : 'rgba(214,194,168,0.5)';",
     "        navCta.style.color = dark ? '#1F1F1F' : '#FFFFFF';\n        navCta.style.borderColor = dark ? 'rgba(91,70,54,0.35)' : 'rgba(214,194,168,0.5)';"),
    ("l.style.opacity = window.scrollY > 60 ? '1' : '0.8';",
     "l.style.opacity = (window.scrollY > 60 || nav.hasAttribute('data-nav-dark')) ? '1' : '0.8';"),
    ("navCta.style.background = window.scrollY > 60 ? '#3A2D25' : 'rgba(255,255,255,0.1)';",
     "navCta.style.background = (window.scrollY > 60 || nav.hasAttribute('data-nav-dark')) ? '#3A2D25' : 'rgba(255,255,255,0.1)';"),
]


def dark_nav(s, name):
    """The nav starts dark over a white masthead, as on the English pages."""
    assert s.count('<nav id="id-nav" style=') == 1, name
    s = s.replace('<nav id="id-nav" style=', '<nav id="id-nav" data-nav-dark style=')
    for o, n in NAV_PAIRS:
        assert s.count(o) == 1, (name, o)
        s = s.replace(o, n)
    return s

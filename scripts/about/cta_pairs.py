"""Site-wide button pairs: equal width, full width on phones, inverse hover on the outlined button."""
import re

CSS = """<style data-fiq-pair>
  /* button pairs: both buttons share one width; stacked full width on phones */
  .fiq-pair{display:inline-grid!important;grid-template-columns:1fr 1fr!important;flex-direction:row!important;}
  .fiq-pair>a{display:flex!important;align-items:center;justify-content:center!important;text-align:center;white-space:nowrap;box-sizing:border-box;}
  @media(max-width:600px){.fiq-pair{display:grid!important;grid-template-columns:1fr!important;width:100%!important;}.fiq-pair>a{width:100%!important;}}
  /* outlined button inverts on hover: it fills with its own line colour */
  .fiq-btn-ghost:hover,.fiq-btn-ghost:focus-visible{background:var(--ghost-bg,#D6C2A8)!important;color:var(--ghost-fg,#1E1610)!important;border-color:var(--ghost-bg,#D6C2A8)!important;}
</style>
"""


def add_class(tag, cls):
    if re.search(r'\sclass="', tag):
        return re.sub(r'\sclass="', f' class="{cls} ', tag, count=1)
    return tag.replace("<a ", f'<a class="{cls}" ', 1).replace("<div ", f'<div class="{cls}" ', 1)


def patch(path, edits):
    s = open(path, encoding="utf-8").read()
    if "data-fiq-pair" not in s:
        assert s.count("</head>") == 1, path
        s = s.replace("</head>", CSS + "</head>")
    for pat, cls in edits:
        m = list(re.finditer(pat, s))
        assert len(m) == 1, (path, pat, len(m))
        t = m[0].group(0)
        if cls in t:
            continue
        s = s[:m[0].start()] + add_class(t, cls) + s[m[0].end():]
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")


for suf in ("", ".ar"):
    # home hero: Visualize Your Project | View Our Portfolio
    patch(f"home{suf}.dc.html", [
        (r'<div data-reveal data-reveal-delay="0\.3" style="[^"]*display:flex;gap:14px;flex-wrap:wrap;pointer-events:auto;">(?=\s*<a [^>]*id="cta-primary")', "fiq-pair"),
        (r'<a [^>]*id="cta-secondary"[^>]*>', "fiq-btn-ghost"),
    ])
    # projects detail panel: Start Your Project | View Details
    patch(f"projects{suf}.dc.html", [
        (r'<div style="display:flex;gap:14px;flex-wrap:wrap;">(?=\s*<a [^>]*data-detail-wa)', "fiq-pair"),
        (r'<a [^>]*data-detail-contact[^>]*>', "fiq-btn-ghost"),
    ])
    # thank-you: Back to Home | View Our Projects
    patch(f"thank-you{suf}.dc.html", [
        (r'<div class="fiq-ty-actions"[^>]*>', "fiq-pair"),
        (r'<a [^>]*background:transparent;padding:19px 36px;border:1px solid rgba\(214,194,168,0\.4\)[^>]*>', "fiq-btn-ghost"),
    ])

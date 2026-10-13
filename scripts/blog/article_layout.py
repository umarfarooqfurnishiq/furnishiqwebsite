"""Article pages, editorial layout.

Rebuilds the body of each English article page (hero, article, related) from the content already on the
page, in the layout the Insights page uses: a white masthead with the title set large, a wide photographic plate with
a museum caption, a sticky numbered contents rail, a 46rem reading column that figures and the pull quote break out
of, a short-version panel, a sign-off, then the related articles as captioned frames. The newsletter band goes: the footer carries the working sign-up.
The words are lifted from the page as it stands, so rerunning it on an already rebuilt page is a no-op on content.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/blog/article_layout.py
"""
import io, re, html
from urllib.parse import quote

PAGES = {
    "blog-material-honesty.dc.html": "Oak and bronze staircase detail",
    "blog-the-90-day-office.dc.html": "Walnut boardroom table in an executive office",
    "blog-invisible-infrastructure.dc.html": "Walnut slatted ceiling concealing building services",
}
READ = "3 min read"   # every article is 430-550 words: under three minutes at 200 words a minute
RELATED_TITLES = {
    "Material Honesty: Why the Finishes You Touch Matter More Than the Ones You See": "Material honesty: why the finishes you touch matter more than the ones you see",
    "The 90-Day Office: Compressing Commercial Fit-Out Timelines Without Cutting Corners": "The 90-day office: compressing commercial fit-out timelines without cutting corners",
    "Invisible Infrastructure: Designing MEP Systems You'll Never Notice, By Design": "Invisible infrastructure: designing MEP systems you'll never notice, by design",
}
# The closing call, in the article's own subject: the question it leaves, the consultation, and the service it belongs to.
# It offers only what the site already offers (a free consultation), with no figures or promises of its own.
CTA = {
    "blog-material-honesty.dc.html": ("Material honesty", "Planning a space where the details matter?",
        "FurnishIQ specifies every finish within reach.", "Interior Design", "/services-interior-design"),
    "blog-the-90-day-office.dc.html": ("The 90-day office", "Working to a fixed opening date?",
        "FurnishIQ plans the programme with you from the first drawing.", "Fit-Out", "/services-fitout"),
    "blog-invisible-infrastructure.dc.html": ("Invisible infrastructure", "Coordinating MEP on your next project?",
        "FurnishIQ engineers it in-house, alongside the design.", "Engineering &amp; MEP", "/services-mep"),
}
WA = "https://wa.me/966580330627?text="

ARROW_R = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>'
ARROW_L = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>'
ICON_X = '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.9 1.15h3.68l-8.04 9.19L24 22.85h-7.41l-5.8-7.58-6.64 7.58H.47l8.6-9.83L0 1.15h7.59l5.24 6.93 6.07-6.93Zm-1.29 19.5h2.04L6.49 3.24H4.3l13.31 17.41Z"></path></svg>'
ICON_IN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28ZM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13ZM7.12 20.45H3.55V9h3.57v11.45ZM22.22 0H1.77C.79 0 0 .77 0 1.72v20.55C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.72C24 .77 23.2 0 22.22 0Z"></path></svg>'
ICON_LINK = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>'

CSS = r"""
  <style>
    /* ── article page: editorial layout ── */
    :root{--pa-ease:cubic-bezier(0.25,0.46,0.45,0.94);}
    .ph{position:relative;background:#FFFFFF;}
    .ph-wrap,.pa-grid,.pr-wrap{max-width:1280px;margin:0 auto;box-sizing:border-box;}
    .ph-wrap{padding:clamp(120px,15vh,150px) 0 0;}
    .ph-top{display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap;padding-bottom:clamp(28px,4vh,44px);}
    .ph-back{display:inline-flex;align-items:center;gap:12px;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.22em;text-transform:uppercase;color:#1F1F1F;text-decoration:none;transition:gap 0.4s var(--pa-ease),color 0.3s var(--pa-ease);}
    .ph-back:hover,.ph-back:focus-visible{gap:18px;color:#8B6B4A;}
    .ph-meta{display:flex;flex-wrap:wrap;gap:6px 0;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.22em;text-transform:uppercase;color:#8B6B4A;}
    .ph-meta span+span::before{content:"";display:inline-block;width:18px;height:1px;margin:0 14px;vertical-align:middle;background:#D9CDBF;}
    .ph-h1{margin:0;max-width:16.5em;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(38px,5vw,80px);line-height:1.02;letter-spacing:-0.035em;color:#1F1F1F;text-wrap:balance;}
    .ph-h1-main{display:block;}
    .ph-h1-sub{display:block;color:#8B6B4A;}
    .ph-by{display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap;margin-top:clamp(32px,5vh,52px);padding:20px 0;border-top:1px solid #E8DFD8;}
    .ph-author{display:flex;align-items:center;gap:14px;}
    .ph-mark{display:flex;align-items:center;justify-content:center;width:40px;height:40px;flex:none;background:#1F1F1F;font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.08em;color:#D6C2A8;}
    .ph-author b{display:block;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:14px;color:#1F1F1F;}
    .ph-author small{display:block;margin-top:2px;font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.18em;text-transform:uppercase;color:#B8A08C;}
    .pa-share{display:flex;align-items:center;gap:8px;}
    .pa-share-label{margin-right:8px;font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.22em;text-transform:uppercase;color:#8B6B4A;}
    .pa-share a,.pa-share button{position:relative;display:flex;align-items:center;justify-content:center;width:38px;height:38px;padding:0;border:1px solid #E8DFD8;background:transparent;color:#5B4636;cursor:pointer;text-decoration:none;transition:background 0.3s var(--pa-ease),color 0.3s var(--pa-ease),border-color 0.3s var(--pa-ease);}
    .pa-share a:hover,.pa-share a:focus-visible,.pa-share button:hover,.pa-share button:focus-visible{background:#1F1F1F;border-color:#1F1F1F;color:#D6C2A8;}
    .pa-share button[data-copied]::after{content:attr(data-copied);position:absolute;top:calc(100% + 8px);left:50%;transform:translateX(-50%);white-space:nowrap;padding:6px 10px;background:#1F1F1F;color:#D6C2A8;font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.16em;text-transform:uppercase;}
    .ph-plate{max-width:1280px;margin:clamp(8px,1.5vh,16px) auto 0;}
    .ph-frame{position:relative;overflow:hidden;aspect-ratio:21/9;background:#F5F2ED;}
    .ph-frame img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scale(1.06);transition:transform 1.8s var(--pa-ease);}
    .ph.is-ready .ph-frame img{transform:scale(1);}
    .pa-cap{display:flex;align-items:center;gap:12px;margin-top:14px;font-family:'Lama Sans',sans-serif;font-size:12px;letter-spacing:0.04em;color:#8B6B4A;}
    .pa-cap::before{content:"";display:block;width:20px;height:1px;flex:none;background:#B8A08C;}
    .ph-in{opacity:0;transform:translateY(18px);transition:opacity 0.9s var(--pa-ease) var(--d,0s),transform 0.9s var(--pa-ease) var(--d,0s);}
    .ph.is-ready .ph-in{opacity:1;transform:none;}
    /* article */
    .pa{background:#FFFFFF;padding:clamp(64px,9vw,120px) 0 clamp(72px,9vw,128px);}
    .pa-grid{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:0 32px;align-items:start;}
    .pa-rail{grid-column:1/4;position:sticky;top:120px;}
    .pa-label{font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.28em;text-transform:uppercase;color:#8B6B4A;margin-bottom:18px;}
    .pa-toc{list-style:none;margin:0;padding:0;border-top:1px solid #E8DFD8;}
    .pa-toc a{position:relative;display:grid;grid-template-columns:28px 1fr;gap:6px;padding:13px 0;border-bottom:1px solid #E8DFD8;font-family:'Lama Sans',sans-serif;font-size:13.5px;line-height:1.45;color:#8B7A6B;text-decoration:none;transition:color 0.3s var(--pa-ease);}
    .pa-toc a span{font-size:11px;letter-spacing:0.08em;color:#B8A08C;padding-top:2px;}
    .pa-toc a::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:1px;background:#1F1F1F;transform:scaleX(0);transform-origin:left;transition:transform 0.6s var(--pa-ease);}
    .pa-toc a:hover,.pa-toc a:focus-visible,.pa-toc a.is-on{color:#1F1F1F;}
    .pa-toc a.is-on span{color:#8B6B4A;}
    .pa-toc a.is-on::after{transform:scaleX(1);}
    .pa-body{grid-column:4/13;min-width:0;}
    .pa-body>*{max-width:46rem;}
    .pa-body>.pa-wide{max-width:none;}
    .pa-lead{margin:0 0 clamp(40px,5vw,56px);font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(20px,1.75vw,25px);line-height:1.6;letter-spacing:-0.01em;color:#1F1F1F;}
    .pa-body p{font-family:'Lama Sans',sans-serif;font-size:17px;line-height:1.85;color:#3A2D25;margin:0 0 24px;}
    .pa-body p em{font-style:normal;color:#1F1F1F;border-bottom:1px solid #D6C2A8;}
    .pa-h2{display:grid;grid-template-columns:auto 1fr;gap:4px 18px;align-items:baseline;margin:clamp(56px,6vw,80px) 0 26px;padding-top:28px;border-top:1px solid #E8DFD8;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(25px,2.3vw,34px);line-height:1.2;letter-spacing:-0.02em;color:#1F1F1F;scroll-margin-top:120px;text-wrap:balance;}
    .pa-h2 span{font-size:12px;letter-spacing:0.12em;color:#8B6B4A;}
    .pa-lead+.pa-h2{margin-top:0;}
    .pa-fig{margin:clamp(40px,5vw,64px) 0;}
    .pa-fig .pa-frame{position:relative;overflow:hidden;aspect-ratio:16/9;background:#F5F2ED;}
    .pa-fig img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}
    .pa-quote{margin:clamp(48px,6vw,80px) 0;padding:clamp(28px,3vw,40px) 0 0;border-top:1px solid #1F1F1F;display:grid;grid-template-columns:minmax(0,9fr) minmax(0,3fr);gap:24px 32px;align-items:end;}
    .pa-quote p{margin:0!important;max-width:none;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(26px,2.9vw,44px)!important;line-height:1.18!important;letter-spacing:-0.025em;color:#1F1F1F!important;text-wrap:balance;}
    .pa-quote footer{font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.24em;text-transform:uppercase;color:#8B6B4A;padding-bottom:0.6em;}
    .pa-short{margin:clamp(48px,6vw,72px) 0 0;padding:clamp(28px,3.4vw,44px);background:#F5F2ED;}
    .pa-short ol{list-style:none;margin:0;padding:0;}
    .pa-short li{display:grid;grid-template-columns:36px 1fr;gap:8px;padding:16px 0;border-top:1px solid #E2D7CA;font-family:'Lama Sans',sans-serif;font-size:16px;line-height:1.6;color:#1F1F1F;}
    .pa-short li span{font-size:11px;letter-spacing:0.1em;color:#8B6B4A;padding-top:4px;}
    /* the closing call */
    .pa-cta{margin:clamp(48px,6vw,72px) 0 0;padding:clamp(36px,4.4vw,64px);background:#1F1F1F;display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:32px 48px;align-items:end;}
    .pa-cta .pa-label{color:#D6C2A8;display:flex;align-items:center;gap:16px;}
    .pa-cta .pa-label i{display:block;width:32px;height:1px;background:#D6C2A8;}
    .pa-cta-q{margin:0;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(26px,2.6vw,40px);line-height:1.12;letter-spacing:-0.025em;color:#F5F2ED;text-wrap:balance;}
    .pa-cta-q span{display:block;color:rgba(214,194,168,0.75);}
    .pa-cta-acts{display:flex;flex-direction:column;align-items:flex-start;gap:22px;}
    .pa-cta-btn{display:inline-flex;align-items:center;gap:14px;white-space:nowrap;padding:18px 30px;background:#D6C2A8;border:1px solid #D6C2A8;color:#1F1F1F;text-decoration:none;font-family:'Lama Sans',sans-serif;font-size:10.5px;letter-spacing:0.2em;text-transform:uppercase;transition:background 0.4s var(--pa-ease),color 0.4s var(--pa-ease),gap 0.4s var(--pa-ease);}
    .pa-cta-btn:hover,.pa-cta-btn:focus-visible{background:transparent;color:#D6C2A8;gap:20px;}
    .pa-cta-link{position:relative;display:inline-flex;align-items:center;gap:12px;padding-bottom:6px;color:#F5F2ED;text-decoration:none;font-family:'Lama Sans',sans-serif;font-size:10.5px;letter-spacing:0.2em;text-transform:uppercase;transition:gap 0.4s var(--pa-ease),color 0.3s var(--pa-ease);}
    .pa-cta-link::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:rgba(214,194,168,0.45);}
    .pa-cta-link:hover,.pa-cta-link:focus-visible{gap:18px;color:#D6C2A8;}
    /* the rail note: the conversation, one step away while reading */
    .pa-talk{margin-top:36px;padding-top:24px;border-top:1px solid #1F1F1F;}
    .pa-talk p{margin:0 0 16px;font-family:'Lama Sans',sans-serif;font-size:14px;line-height:1.6;color:#1F1F1F;}
    .pa-talk a{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid #E8DFD8;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.2em;text-transform:uppercase;color:#1F1F1F;text-decoration:none;transition:color 0.3s var(--pa-ease);}
    .pa-talk a svg{transition:transform 0.4s var(--pa-ease);}
    .pa-talk a:hover,.pa-talk a:focus-visible{color:#8B6B4A;}
    .pa-talk a:hover svg,.pa-talk a:focus-visible svg{transform:translateX(4px);}
    .pa-sign{display:flex;justify-content:space-between;align-items:center;gap:28px;flex-wrap:wrap;margin-top:clamp(48px,6vw,72px);padding-top:28px;border-top:1px solid #E8DFD8;}
    .pa-sign .ph-mark{width:52px;height:52px;font-size:13px;}
    .pa-sign-who{display:flex;align-items:center;gap:18px;max-width:30rem;}
    .pa-sign-who small{display:block;margin-bottom:4px;font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.24em;text-transform:uppercase;color:#8B6B4A;}
    .pa-sign-who b{display:block;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:16px;color:#1F1F1F;}
    .pa-sign-who div>span{display:block;margin-top:4px;font-family:'Lama Sans',sans-serif;font-size:13.5px;line-height:1.65;color:#5B4636;}
    /* related */
    .pr{background:#F5F2ED;padding:clamp(64px,8vw,112px) 0;}
    .pr-head{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;margin-bottom:clamp(36px,4.5vw,56px);}
    .pr-h2{margin:0;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(30px,3.6vw,56px);line-height:1;letter-spacing:-0.035em;color:#1F1F1F;}
    .pr-all{position:relative;display:inline-flex;align-items:center;gap:12px;padding-bottom:6px;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.22em;text-transform:uppercase;color:#1F1F1F;text-decoration:none;transition:gap 0.4s var(--pa-ease);}
    .pr-all::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:#8B6B4A;}
    .pr-all:hover,.pr-all:focus-visible{gap:18px;}
    .pr-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px;}
    .pr-card{display:block;text-decoration:none;color:inherit;transition:opacity 0.6s var(--pa-ease);}
    .pr-grid:hover .pr-card:not(:hover){opacity:0.5;}
    .pr-card .pa-frame{position:relative;overflow:hidden;aspect-ratio:3/2;background:#E8DFD8;}
    .pr-card img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--pa-ease);}
    .pr-card:hover img,.pr-card:focus-visible img{transform:scale(1.035);}
    .pr-cap{position:relative;margin-top:16px;padding-top:16px;}
    .pr-cap::before,.pr-cap::after{content:"";position:absolute;top:0;left:0;right:0;height:1px;background:#D9CDBF;}
    .pr-cap::after{background:#1F1F1F;transform:scaleX(0);transform-origin:left;transition:transform 0.8s var(--pa-ease);}
    .pr-card:hover .pr-cap::after,.pr-card:focus-visible .pr-cap::after{transform:scaleX(1);}
    .pr-meta{font-family:'Lama Sans',sans-serif;font-size:9.5px;letter-spacing:0.2em;text-transform:uppercase;color:#8B6B4A;}
    .pr-t{display:block;margin-top:10px;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(18px,1.5vw,22px);line-height:1.35;letter-spacing:-0.01em;color:#1F1F1F;text-wrap:balance;}
    @media(max-width:1360px){.ph-wrap,.pa-grid,.pr-wrap,.ph-plate{max-width:none;padding-left:clamp(24px,5vw,80px);padding-right:clamp(24px,5vw,80px);}}
    @media(max-width:960px){
      .pa-grid{display:block;}
      .pa-rail{display:none;}
      .pa-cta{grid-template-columns:1fr;padding:32px 24px;}
      .pa-cta-btn{padding:16px 20px;letter-spacing:0.16em;}
      .pa-body>*{max-width:none;}
      .ph-frame{aspect-ratio:4/3;}
      .pa-quote{grid-template-columns:1fr;}
      .ph-meta span:first-child{flex-basis:100%;margin-bottom:4px;}
      .ph-meta span:nth-child(2)::before{display:none;}
      .pr-grid{grid-template-columns:1fr;gap:44px;}
      .pr-grid:hover .pr-card:not(:hover){opacity:1;}
    }
    @media(prefers-reduced-motion:reduce){
      .ph-in{opacity:1;transform:none;transition:none;}
      .ph-frame img,.pr-card img{transform:none!important;transition:none;}
    }
  </style>
"""


def text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def esc(s):
    return html.escape(s, quote=False)


def block_end(s, i, tag):
    j = s.index("</%s>" % tag, i)
    return j + len(tag) + 3


def parse(page):
    hero = page[page.index("<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ HERO ━━ -->"):page.index("<!-- ━━━━━━━━━━━━━━━━━━━━━━━━ ARTICLE")]
    d = {}
    d["category"] = text(re.findall(r'<span style="[^"]*color:rgba\(214,194,168,0\.9\);">(.*?)</span>', hero)[0])
    d["title"] = re.sub(r"\s+", " ", text(hero[hero.index("<h1"):hero.index("</h1>")].split(">", 1)[1]))
    d["date"] = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December) \d+, \d{4}", hero).group(0)
    d["image"] = re.search(r"url\('(uploads/[^']+)'\)", hero).group(1)
    art = page[page.index("<article>") + 9:page.index("<!-- AUTHOR -->")]
    blocks, i = [], 0
    while True:
        m = re.compile(r"\S").search(art, i)
        if not m:
            break
        i = m.start()
        if art.startswith("<p", i):
            j = block_end(art, i, "p")
            chunk = art[i:j]
            inner = chunk.split(">", 1)[1][:-4]
            blocks.append(("lead" if "font-weight:500" in chunk.split(">", 1)[0] and not blocks else "p", inner.strip()))
        elif art.startswith("<h2", i):
            j = block_end(art, i, "h2")
            chunk = art[i:j]
            hid = re.search(r'id="([^"]+)"', chunk).group(1)
            num = text(re.search(r"<span[^>]*>(.*?)</span>", chunk).group(1))
            title = text(re.sub(r"<span[^>]*>.*?</span>", "", chunk.split(">", 1)[1]))
            blocks.append(("h2", (hid, num, title)))
        elif art.startswith("<figure", i):
            j = block_end(art, i, "figure")
            chunk = art[i:j]
            img = re.search(r"<img ([^>]*)>", chunk).group(1)
            attrs = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', img))
            blocks.append(("fig", (attrs["src"], attrs.get("srcset", ""), attrs.get("alt", ""), text(re.search(r"<figcaption[^>]*>(.*?)</figcaption>", chunk, re.S).group(1)))))
        elif art.startswith("<blockquote", i):
            j = block_end(art, i, "blockquote")
            chunk = art[i:j]
            blocks.append(("quote", (text(re.search(r"<p[^>]*>(.*?)</p>", chunk, re.S).group(1)), text(re.search(r"<footer[^>]*>(.*?)</footer>", chunk, re.S).group(1)))))
        elif art.startswith("<div", i):
            chunk = art[i:]
            label = text(re.search(r'text-transform:uppercase;color:#8B6B4A;">(.*?)</span>', chunk).group(1))
            items = [text(x) for x in re.findall(r"<p[^>]*>(.*?)</p>", chunk, re.S)]
            blocks.append(("short", (label, items)))
            break
        else:
            raise ValueError("unexpected block at: " + art[i:i + 80])
        i = j
    d["blocks"] = blocks
    auth = page[page.index("<!-- AUTHOR -->"):page.index("</article>")]
    d["author_desc"] = text(re.search(r"<p[^>]*>(.*?)</p>", auth, re.S).group(1))
    return d


def share(cls=""):
    return ('<div class="pa-share%s"><span class="pa-share-label">Share</span>'
            '<a href="#" data-share="x" target="_blank" rel="noopener" aria-label="Share on X">%s</a>'
            '<a href="#" data-share="linkedin" target="_blank" rel="noopener" aria-label="Share on LinkedIn">%s</a>'
            '<button type="button" data-share="copy" aria-label="Copy link">%s</button></div>') % (cls, ICON_X, ICON_IN, ICON_LINK)


def build(d, hero_alt, cta):
    short, question, answer, service, service_href = cta
    wa = WA + quote('Hello FurnishIQ, I read "%s" and would like to discuss my project.' % short)
    main, _, rest = d["title"].partition(":")
    img = d["image"]
    base = re.sub(r"-\d+\.webp$", "", img)
    srcset = "%s-1200.webp 1200w, %s 2400w" % (base, img)
    h = []
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ HERO ━━ -->')
    h.append('<!-- The masthead: back to Insights, the facts, the title set large, the byline, and the plate with its caption -->')
    h.append('<section data-screen-label="Post Hero" class="ph" data-post-hero>' + CSS)
    h.append('  <div class="ph-wrap">')
    h.append('    <div class="ph-top ph-in" style="--d:0.05s;">')
    h.append('      <a href="/insights" class="ph-back">%sInsights</a>' % ARROW_L)
    h.append('      <div class="ph-meta"><span>%s</span><span>%s</span><span>%s</span></div>' % (esc(d["category"]), d["date"], READ))
    h.append('    </div>')
    h.append('    <h1 class="ph-h1 ph-in" style="--d:0.15s;"><span class="ph-h1-main">%s:</span> <span class="ph-h1-sub">%s</span></h1>' % (esc(main.strip()), esc(rest.strip())))
    h.append('    <div class="ph-by ph-in" style="--d:0.3s;">')
    h.append('      <div class="ph-author"><span class="ph-mark">IQ</span><div><b>FurnishIQ Studio</b><small>Design &amp; Build Team</small></div></div>')
    h.append('      ' + share())
    h.append('    </div>')
    h.append('  </div>')
    h.append('  <figure class="ph-plate ph-in" style="--d:0.4s;">')
    h.append('    <div class="ph-frame"><img src="%s" srcset="%s" sizes="(max-width:1360px) 100vw, 1280px" alt="%s" fetchpriority="high" decoding="async"></div>' % (img, srcset, hero_alt))
    h.append('    <figcaption class="pa-cap">%s, concept visualisation.</figcaption>' % hero_alt)
    h.append('  </figure>')
    h.append('</section>')
    h.append('')
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━━━━ ARTICLE ━━━━━━━━━━━━━━━━━ -->')
    h.append('<section data-screen-label="Article" class="pa" id="article">')
    h.append('  <div class="pa-grid">')
    h.append('    <aside class="pa-rail">')
    h.append('      <div class="pa-label">Contents</div>')
    h.append('      <nav aria-label="Contents"><ol class="pa-toc">')
    for kind, v in d["blocks"]:
        if kind == "h2":
            h.append('        <li><a href="#%s" data-toc data-toc-target="%s"><span>%s</span>%s</a></li>' % (v[0], v[0], v[1], esc(v[2])))
    h.append('      </ol></nav>')
    h.append('      <div class="pa-talk">')
    h.append('        <div class="pa-label">Discuss your project</div>')
    h.append('        <p>Speak with the studio about your space.</p>')
    h.append('        <a href="/contact" data-blog-cta="consultation" data-cta-place="rail">Book free consultation %s</a>' % ARROW_R)
    h.append('        <a href="%s" target="_blank" rel="noopener" data-blog-cta="whatsapp" data-cta-place="rail">WhatsApp %s</a>' % (wa, ARROW_R))
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
    h.append('      <aside class="pa-cta pa-wide" aria-label="Work with FurnishIQ">')
    h.append('        <div>')
    h.append('          <div class="pa-label"><i></i>Work with FurnishIQ</div>')
    h.append('          <div class="pa-cta-q">%s<span>%s</span></div>' % (esc(question), esc(answer)))
    h.append('        </div>')
    h.append('        <div class="pa-cta-acts">')
    h.append('          <a href="/contact" class="pa-cta-btn" data-blog-cta="consultation" data-cta-place="end">Book free consultation %s</a>' % ARROW_R)
    h.append('          <a href="%s" class="pa-cta-link" data-blog-cta="service" data-cta-place="end">%s services %s</a>' % (service_href, service, ARROW_R))
    h.append('        </div>')
    h.append('      </aside>')
    h.append('')
    h.append('      <footer class="pa-sign">')
    h.append('        <div class="pa-sign-who"><span class="ph-mark">IQ</span><div><small>Written by</small><b>FurnishIQ Studio</b><span>%s</span></div></div>' % esc(d["author_desc"]))
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
    h.append('      <div><div class="pa-label">Continue reading</div><h2 class="pr-h2">More from the journal.</h2></div>')
    h.append('      <a href="/insights" class="pr-all">All insights %s</a>' % ARROW_R)
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


JS_HERO_OLD_START = "    // ── HERO PARALLAX + WORDS"
JS_HERO_NEW = """    // ── HERO ENTRANCE ──────────────────────────────────────
    const postHero = document.querySelector('[data-post-hero]');
    if (postHero) requestAnimationFrame(() => requestAnimationFrame(() => postHero.classList.add('is-ready')));

"""
JS_TOC = """    // ── TOC ACTIVE STATE ───────────────────────────────────
    const tocLinks = [...document.querySelectorAll('[data-toc]')];
    const sections = tocLinks.map(l => document.getElementById(l.dataset.tocTarget)).filter(Boolean);
    const syncToc = () => {
      let active = 0;
      sections.forEach((s, i) => { if (s.getBoundingClientRect().top < window.innerHeight * 0.35) active = i; });
      tocLinks.forEach((l, i) => l.classList.toggle('is-on', i === active));
    };
    window.addEventListener('scroll', syncToc, { passive: true });
    syncToc();

    // ── SHARE ──────────────────────────────────────────────
    const canon = document.querySelector('link[rel="canonical"]');
    const pageUrl = canon ? canon.href : location.href.split('#')[0];
    const pageTitle = (document.querySelector('h1') || {}).textContent || document.title;
    document.querySelectorAll('[data-share]').forEach(el => {
      const kind = el.dataset.share;
      if (kind === 'x') el.href = 'https://twitter.com/intent/tweet?url=' + encodeURIComponent(pageUrl) + '&text=' + encodeURIComponent(pageTitle.replace(/\\s+/g, ' ').trim());
      if (kind === 'linkedin') el.href = 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(pageUrl);
      if (kind === 'copy') el.addEventListener('click', () => {
        const done = () => { el.setAttribute('data-copied', 'Link copied'); setTimeout(() => el.removeAttribute('data-copied'), 1800); };
        if (navigator.clipboard) navigator.clipboard.writeText(pageUrl).then(done, () => {}); else done();
      });
    });
  }
}
</script>"""

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


def main():
    for name, hero_alt in PAGES.items():
        s = io.open(name, encoding="utf-8", newline="").read()
        crlf = "\r\n" in s
        s = s.replace("\r\n", "\n")
        if 'class="ph"' in s:
            print(name, "already rebuilt")
            continue
        d = parse(s)
        a = s.index("<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ HERO ━━ -->")
        b = s.index("<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ FOOTER")
        s = s[:a] + build(d, hero_alt, CTA[name]) + s[b:]
        # old responsive rules for the replaced sections
        s = re.sub(r"\n\s*\.fiq-(article-grid|article-rail|related-grid|author-card)\{[^\n]*", "", s)
        # nav starts dark over the white masthead
        assert s.count('<nav id="id-nav" style=') == 1
        s = s.replace('<nav id="id-nav" style=', '<nav id="id-nav" data-nav-dark style=')
        for o, n in NAV_PAIRS:
            assert s.count(o) == 1, (name, o)
            s = s.replace(o, n)
        # script: entrance instead of parallax, class-based contents, working share links
        a = s.index(JS_HERO_OLD_START)
        b = s.index("    // ── SCROLL REVEAL")
        s = s[:a] + JS_HERO_NEW + s[b:]
        a = s.index("    // ── TOC ACTIVE STATE")
        b = s.index("</script>", a) + len("</script>")
        s = s[:a] + JS_TOC + s[b:]
        # related cards: the honest read time, and the titles as the articles set them
        for t_old, t_new in RELATED_TITLES.items():
            s = s.replace('title: "%s"' % t_old, 'title: "%s"' % t_new)
        # related cards: the honest read time
        s = re.sub(r'read: "\d+ min read"', 'read: "%s"' % READ, s)
        io.open(name, "w", encoding="utf-8", newline="").write(s.replace("\n", "\r\n") if crlf else s)
        print(name, "rebuilt:", sum(1 for k, _ in d["blocks"] if k == "p"), "paragraphs,", sum(1 for k, _ in d["blocks"] if k == "h2"), "sections")


if __name__ == "__main__":
    main()

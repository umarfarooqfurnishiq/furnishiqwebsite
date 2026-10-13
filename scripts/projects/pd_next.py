"""Project page, the way on: the portfolio as a corridor of ten doors.

The page ended on "More <category> projects", one to three small cards, which often left two thirds of the row empty.
It now ends on the whole portfolio, edge to edge: ten tall slices side by side, one per concept, in the portfolio's
order. The next concept (10 leads back to 01) stands open, wide, with its caption and "View the concept"; the others
are narrow, dimmed, numbered and titled on their side; the one being read is marked "You are here". Pointing at any
slice, or tabbing to it, swings it open and the others narrow, so the visitor sees where they are, what comes next
and what else there is, in one band. On phones the slices stack, the next one open.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/projects/pd_next.py
"""
import io, re

PAGE = "project-detail.dc.html"
ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>'
MARK = "<!-- The way on: the next project in the portfolio, then two more -->\n"
MARK_NEW = "<!-- The way on: the portfolio as ten doors, the next one open -->\n"

SECTION = MARK_NEW + """<section data-screen-label="Next Project" data-pd-next>
  <style>
    [data-pd-next]{--e:cubic-bezier(0.25,0.46,0.45,0.94);--open:8;background:#1F1F1F;border-top:1px solid rgba(214,194,168,0.12);padding:clamp(72px,9vw,120px) 0 clamp(64px,8vw,104px);}
    [data-pd-next] .pn-grid{max-width:1280px;margin:0 auto;padding:0 clamp(24px,5vw,80px);box-sizing:content-box;}
    [data-pd-next] .pn-head{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;margin-bottom:clamp(28px,3.4vw,44px);}
    [data-pd-next] .pn-label{display:flex;align-items:center;gap:16px;margin-bottom:16px;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.28em;text-transform:uppercase;color:rgba(214,194,168,0.7);}
    [data-pd-next] .pn-label i{display:block;width:32px;height:1px;background:#D6C2A8;flex:none;}
    [data-pd-next] .pn-h2{margin:0;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(30px,3.4vw,50px);line-height:1.05;letter-spacing:-0.03em;color:#F5F2ED;}
    [data-pd-next] .pn-h2 span{color:#D6C2A8;}
    [data-pd-next] .pn-all{position:relative;display:inline-flex;align-items:center;gap:12px;padding-bottom:6px;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.22em;text-transform:uppercase;color:#F5F2ED;text-decoration:none;transition:gap 0.4s var(--e),color 0.3s var(--e);}
    [data-pd-next] .pn-all::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:rgba(214,194,168,0.5);}
    [data-pd-next] .pn-all:hover,[data-pd-next] .pn-all:focus-visible{gap:18px;color:#D6C2A8;}
    /* the corridor: ten slices edge to edge, one open */
    [data-pd-next] .pn-strip{display:flex;gap:2px;height:min(76vh,760px);min-height:460px;background:#1F1F1F;}
    [data-pd-next] .pn-s{position:relative;flex:1 1 0;min-width:0;overflow:hidden;color:#F5F2ED;text-decoration:none;outline:none;background:#26201A;transition:flex-grow 0.9s var(--e);}
    [data-pd-next] .pn-s img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(0.42) saturate(0.75);transform:scale(1.04);transition:filter 0.9s var(--e),transform 1.6s var(--e);}
    [data-pd-next] .pn-n{position:absolute;top:22px;left:0;right:0;text-align:center;font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.14em;color:rgba(245,242,237,0.75);transition:opacity 0.5s var(--e);}
    [data-pd-next] .pn-v{position:absolute;bottom:26px;left:50%;writing-mode:vertical-rl;transform:translateX(-50%) rotate(180deg);white-space:nowrap;max-height:calc(100% - 96px);overflow:hidden;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:15px;letter-spacing:0.02em;color:#F5F2ED;transition:opacity 0.5s var(--e);}
    [data-pd-next] .pn-tag{position:absolute;top:20px;inset-inline-start:24px;padding:7px 11px;background:#D6C2A8;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.24em;text-transform:uppercase;color:#1F1F1F;opacity:0;transition:opacity 0.5s var(--e);}
    [data-pd-next] .pn-s[data-state="other"] .pn-tag{display:none;}
    [data-pd-next] .pn-c{position:absolute;left:clamp(20px,2.4vw,36px);bottom:clamp(20px,2.4vw,36px);width:min(560px,calc(100% - 2 * clamp(20px,2.4vw,36px)));box-sizing:border-box;padding:clamp(20px,2vw,28px) clamp(22px,2.4vw,32px);background:rgba(31,31,31,0.84);opacity:0;transform:translateY(12px);transition:opacity 0.4s var(--e),transform 0.4s var(--e);pointer-events:none;}
    [data-pd-next] .pn-meta{display:block;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.22em;text-transform:uppercase;color:rgba(214,194,168,0.8);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
    [data-pd-next] .pn-title{display:block;margin-top:10px;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(26px,2.6vw,40px);line-height:1.05;letter-spacing:-0.03em;color:#F5F2ED;}
    [data-pd-next] .pn-go{display:inline-flex;align-items:center;gap:14px;margin-top:18px;font-family:'Lama Sans',sans-serif;font-size:10.5px;letter-spacing:0.2em;text-transform:uppercase;color:#D6C2A8;}
    /* which slice is open: the next one, until another is pointed at or focused */
    [data-pd-next] .pn-s[data-state="next"],
    [data-pd-next] .pn-strip:hover .pn-s:hover,
    [data-pd-next] .pn-strip:focus-within .pn-s:focus-visible{flex-grow:var(--open);}
    [data-pd-next] .pn-strip:hover .pn-s[data-state="next"]:not(:hover),
    [data-pd-next] .pn-strip:focus-within .pn-s[data-state="next"]:not(:focus-visible){flex-grow:1;}
    [data-pd-next] .pn-s[data-state="next"] img,[data-pd-next] .pn-strip:hover .pn-s:hover img,[data-pd-next] .pn-strip:focus-within .pn-s:focus-visible img{filter:none;transform:none;}
    [data-pd-next] .pn-strip:hover .pn-s[data-state="next"]:not(:hover) img,[data-pd-next] .pn-strip:focus-within .pn-s[data-state="next"]:not(:focus-visible) img{filter:brightness(0.42) saturate(0.75);transform:scale(1.04);}
    [data-pd-next] .pn-s[data-state="next"] .pn-c,[data-pd-next] .pn-strip:hover .pn-s:hover .pn-c,[data-pd-next] .pn-strip:focus-within .pn-s:focus-visible .pn-c{opacity:1;transform:none;transition-delay:0.35s;}
    [data-pd-next] .pn-strip:hover .pn-s[data-state="next"]:not(:hover) .pn-c,[data-pd-next] .pn-strip:focus-within .pn-s[data-state="next"]:not(:focus-visible) .pn-c{opacity:0;transform:translateY(12px);transition-delay:0s;}
    [data-pd-next] .pn-s[data-state="next"] .pn-v,[data-pd-next] .pn-strip:hover .pn-s:hover .pn-v,[data-pd-next] .pn-strip:focus-within .pn-s:focus-visible .pn-v,
    [data-pd-next] .pn-s[data-state="next"] .pn-n,[data-pd-next] .pn-strip:hover .pn-s:hover .pn-n,[data-pd-next] .pn-strip:focus-within .pn-s:focus-visible .pn-n{opacity:0;}
    [data-pd-next] .pn-strip:hover .pn-s[data-state="next"]:not(:hover) .pn-v,[data-pd-next] .pn-strip:hover .pn-s[data-state="next"]:not(:hover) .pn-n,
    [data-pd-next] .pn-strip:focus-within .pn-s[data-state="next"]:not(:focus-visible) .pn-v,[data-pd-next] .pn-strip:focus-within .pn-s[data-state="next"]:not(:focus-visible) .pn-n{opacity:1;}
    [data-pd-next] .pn-s[data-state="next"] .pn-tag,[data-pd-next] .pn-strip:hover .pn-s:hover .pn-tag,[data-pd-next] .pn-strip:focus-within .pn-s:focus-visible .pn-tag{opacity:1;transition-delay:0.35s;}
    [data-pd-next] .pn-strip:hover .pn-s[data-state="next"]:not(:hover) .pn-tag{opacity:0;transition-delay:0s;}
    /* the one being read: marked, darker, and not a way on */
    [data-pd-next] .pn-s[data-state="here"]{background:#1F1F1F;}
    [data-pd-next] .pn-s[data-state="here"] img{filter:brightness(0.22) saturate(0.4);}
    [data-pd-next] .pn-s[data-state="here"]::after{content:"";position:absolute;inset:0;border:1px solid rgba(214,194,168,0.45);pointer-events:none;}
    [data-pd-next] .pn-s[data-state="here"] .pn-n{color:#D6C2A8;}
    /* its marker shows whether it is open or not */
    [data-pd-next] .pn-s[data-state="here"] .pn-tag{opacity:1;top:50px;inset-inline-start:50%;transform:translateX(-50%);padding:5px 7px;font-size:9px;letter-spacing:0.18em;background:transparent;border:1px solid rgba(214,194,168,0.6);color:#D6C2A8;}
    [data-pd-next] .pn-strip:hover .pn-s[data-state="here"]:hover .pn-tag{inset-inline-start:24px;transform:none;}
    [data-pd-next] .pn-foot{display:flex;justify-content:space-between;gap:24px;margin-top:18px;font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.04em;color:rgba(214,194,168,0.55);}
    @media(max-width:768px){
      [data-pd-next] .pn-strip{flex-direction:column;height:auto;min-height:0;gap:2px;}
      [data-pd-next] .pn-s{flex:none;height:64px;transition:height 0.6s var(--e);}
      [data-pd-next] .pn-s[data-state="next"]{height:min(110vw,440px);}
      [data-pd-next] .pn-strip:hover .pn-s[data-state="next"]:not(:hover){flex-grow:0;}
      [data-pd-next] .pn-n{top:50%;left:20px;right:auto;transform:translateY(-50%);}
      [data-pd-next] .pn-v{writing-mode:horizontal-tb;transform:translateY(50%);bottom:50%;left:64px;max-height:none;max-width:calc(100% - 84px);text-overflow:ellipsis;}
      [data-pd-next] .pn-tag{inset-inline-start:20px;}
      [data-pd-next] .pn-s[data-state="here"] .pn-tag{top:50%;inset-inline-start:auto;right:16px;transform:translateY(-50%);}
      [data-pd-next] .pn-c{left:12px;bottom:12px;width:calc(100% - 24px);}
      [data-pd-next] .pn-foot span:first-child{display:none;}
    }
    @media(prefers-reduced-motion:reduce){
      [data-pd-next] .pn-s,[data-pd-next] .pn-s img,[data-pd-next] .pn-c,[data-pd-next] .pn-v,[data-pd-next] .pn-n,[data-pd-next] .pn-tag{transition:none!important;}
    }
  </style>
  <div class="pn-grid">
    <div class="pn-head">
      <div><div class="pn-label"><i></i>The portfolio</div><h2 class="pn-h2">Ten concepts. <span>Next, {{ next.num }}.</span></h2></div>
      <a class="pn-all" href="/projects">All projects {ARROW}</a>
    </div>
  </div>
  <nav class="pn-strip" aria-label="The portfolio">
    <sc-for list="{{ strip }}" as="s" hint-placeholder-count="10">
      <a class="pn-s" href="{{ s.href }}" data-state="{{ s.state }}" aria-label="{{ s.num }}, {{ s.title }}, {{ s.category }}, {{ s.location }}">
        <img src="{{ s.image }}" alt="" loading="lazy" decoding="async">
        <span class="pn-n" aria-hidden="true">{{ s.num }}</span>
        <span class="pn-v" aria-hidden="true">{{ s.title }}</span>
        <span class="pn-tag" aria-hidden="true">{{ s.tag }}</span>
        <span class="pn-c" aria-hidden="true">
          <span class="pn-meta">{{ s.num }} · {{ s.category }} · {{ s.location }} · Concept</span>
          <span class="pn-title">{{ s.title }}</span>
          <span class="pn-go">{{ s.go }} {ARROW}</span>
        </span>
      </a>
    </sc-for>
  </nav>
  <div class="pn-grid">
    <div class="pn-foot"><span>Point at any concept to open it.</span><span>{{ projNum }} / {{ projTotal }} · You are here</span></div>
  </div>
</section>
""".replace("{ARROW}", ARROW)

CALC_ANCHOR = "    // the story: each paragraph as a numbered part, paired with the view it describes\n"
CALC_RE = re.compile(r"    // the way on: .*?\n\n", re.S)
CALC = """    // the way on: the whole portfolio as a row of doors, the next concept open and this one marked
    const at = this.PROJECTS.indexOf(proj);
    const nextP = this.PROJECTS[(at + 1) % this.PROJECTS.length];
    const card = (p) => ({ ...p, num: String(this.PROJECTS.indexOf(p) + 1).padStart(2, '0'), href: `/project-detail?project=${this.slugify(p.title)}` });
    const strip = this.PROJECTS.map((p) => {
      const state = p === proj ? 'here' : p === nextP ? 'next' : 'other';
      return { ...card(p), state, tag: state === 'here' ? 'Here' : state === 'next' ? 'Next' : '', go: state === 'here' ? 'Back to the top' : 'View the concept' };
    });

"""
RENDER_RE = re.compile(r"      next: card\(nextP\),\n(?:      others,\n      alsoLabel,\n|      strip,\n)")


def main():
    s = io.open(PAGE, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    s = s.replace("\r\n", "\n")
    for mark in (MARK, MARK_NEW):
        if mark in s:
            a = s.index(mark)
            b = s.index("</section>\n", a) + len("</section>\n")
            break
    else:
        a = s.index('<sc-if value="{{ hasRelated }}"')
        b = s.index("</sc-if>\n", a) + len("</sc-if>\n")
    s = s[:a] + SECTION + s[b:]
    s = re.sub(r"\n\s*\.fiq-pd-related\{[^\n]*", "", s)
    # data: replace an earlier version of the calculation, or add it
    if CALC_RE.search(s):
        s = CALC_RE.sub(lambda m: CALC, s, count=1)
    else:
        assert s.count(CALC_ANCHOR) == 1
        s = s.replace(CALC_ANCHOR, CALC + CALC_ANCHOR)
    if RENDER_RE.search(s):
        s = RENDER_RE.sub("      next: card(nextP),\n      strip,\n", s, count=1)
    else:
        s = s.replace("      chapters,\n", "      chapters,\n      next: card(nextP),\n      strip,\n", 1)
    io.open(PAGE, "w", encoding="utf-8", newline="").write(s.replace("\n", "\r\n") if crlf else s)
    print(PAGE, "portfolio corridor built")


if __name__ == "__main__":
    main()

"""Project page, the story: six numbered parts read beside a viewfinder.

The project text was six plain paragraphs beside a sidebar that repeated the facts strip above it. Each project's six
paragraphs already walk the same route (the idea, the plan, the palette, a signature room, the engineering, the
furniture), and each project has six captioned views. This pairs them: every paragraph becomes a numbered part with a
short title, and the sticky sidebar becomes a viewfinder that shows the room the reader is reading about, with its
museum caption. Under it, the four FurnishIQ disciplines light up for the ones at work in that part, so the page shows
what the studio does in the order a client would meet it. Six ticks under the frame jump between parts; the frame opens
that view in the page's lightbox. On phones the viewfinder gives way to a photograph inside each part.

The facts strip is set on the same 1280px edge as the story below it.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/projects/pd_story.py
"""
import io, re, json

PAGE = "project-detail.dc.html"

# per project: (title, gallery view shown, disciplines at work) for each of the six paragraphs, in order.
# d = Interior Design, f = Fit-Out, m = MEP Engineering, u = Bespoke Furniture, all = the whole scope
CHAPTERS = {
    "The Courtyard Residence": [
        ("Three wings, one courtyard", 1, "d"),
        ("The majlis wing", 0, "d f"),
        ("A narrow palette", 2, "d f"),
        ("Engineering in the shadow gaps", 5, "m"),
        ("Furniture made for the rooms", 3, "u"),
        ("The scope", 4, "all"),
    ],
    "Family Office HQ": [
        ("A quiet wall to the street", 0, "d"),
        ("Every room faces the courtyard", 3, "d f"),
        ("Najdi building, reinterpreted", 5, "d f"),
        ("The council room and library", 1, "d f"),
        ("Privacy, engineered", 2, "m"),
        ("Furniture for a generation", 4, "all"),
    ],
    "Central Commons": [
        ("The public realm", 0, "d"),
        ("A square built for the climate", 5, "d m"),
        ("Galleria and atrium", 1, "d f"),
        ("A food hall for 600", 3, "d f"),
        ("Engineering at public scale", 2, "m"),
        ("One family of furniture", 4, "all"),
    ],
    "Obhur Beach Estate": [
        ("Three buildings on one axis", 1, "d"),
        ("The sea-facing great room", 0, "d f"),
        ("Rawasheen, in teak", 2, "d f"),
        ("A palette for the coast", 3, "d"),
        ("Built for salt air", 4, "m"),
        ("Furniture for the coast", 5, "all"),
    ],
    "Desert Stone Resort": [
        ("The guest's route", 1, "d"),
        ("One view at a time", 0, "d"),
        ("A palette from the site", 5, "d f"),
        ("Restaurant and fire-pit terrace", 2, "d f"),
        ("Engineering for the desert", 3, "m"),
        ("Furniture of the landscape", 4, "all"),
    ],
    "The Executive Floors": [
        ("Eight floors, organised vertically", 0, "d"),
        ("Arrival above the city", 4, "d f"),
        ("Boardroom and executive suites", 1, "d f"),
        ("The walnut ceiling", 5, "f m"),
        ("Floors for 900 people", 2, "m"),
        ("Furniture in the same materials", 3, "all"),
    ],
    "Penthouse Above the Wadi": [
        ("Facing the wadi", 0, "d"),
        ("Two levels: hosting and family", 1, "d f"),
        ("Lit by the sky", 2, "d"),
        ("The staircase", 3, "f u"),
        ("Climate behind glass", 5, "m"),
        ("Seating kept low", 4, "all"),
    ],
    "Roastery House Flagship": [
        ("Roasting on show", 0, "d"),
        ("A 14-metre bar", 1, "d f"),
        ("A palette from the coffee", 5, "d"),
        ("The mezzanine", 2, "d f"),
        ("Keeping the smoke away", 3, "m"),
        ("Furniture for guests who stay", 4, "all"),
    ],
    "Maison de Joaillerie": [
        ("Behind a bronze screen", 1, "d"),
        ("The main salon", 0, "d f"),
        ("The private salons", 3, "d u"),
        ("Materials that flatter", 4, "d"),
        ("Security and light", 5, "m"),
        ("Made for the house", 2, "all"),
    ],
    "The Furniture Gallery": [
        ("A sequence of rooms", 1, "d"),
        ("The atrium", 0, "d f"),
        ("Room-sets as real interiors", 3, "d f"),
        ("The design studio", 2, "d"),
        ("A showroom lives on its lighting", 4, "m"),
        ("Display as furniture", 5, "all"),
    ],
}

ARROW = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>'

SECTION = """<!-- The story: six numbered parts, and a viewfinder that shows the room each part describes -->
<section data-screen-label="Project Story" data-pd-story>
  <style>
    [data-pd-story]{--e:cubic-bezier(0.25,0.46,0.45,0.94);background:#1F1F1F;padding:clamp(72px,9vw,128px) clamp(24px,5vw,80px);}
    [data-pd-story] .pds-grid{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:0 32px;align-items:start;}
    [data-pd-story] .pds-text{grid-column:1/8;min-width:0;}
    [data-pd-story] .pds-side{grid-column:9/13;position:sticky;top:112px;min-width:0;}
    [data-pd-story] .pds-label{display:flex;align-items:center;gap:16px;margin:0 0 clamp(20px,2.4vw,32px);font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.28em;text-transform:uppercase;color:rgba(214,194,168,0.7);}
    [data-pd-story] .pds-label i{display:block;width:32px;height:1px;background:#D6C2A8;flex:none;}
    /* the parts */
    [data-pd-story] .pds-ch{position:relative;padding:clamp(26px,3vw,34px) 0 clamp(40px,4.4vw,56px);}
    [data-pd-story] .pds-ch::before,[data-pd-story] .pds-ch::after{content:"";position:absolute;top:0;left:0;right:0;height:1px;background:rgba(214,194,168,0.14);}
    [data-pd-story] .pds-ch::after{background:#D6C2A8;transform:scaleX(0);transform-origin:left;transition:transform 0.9s var(--e);}
    [data-pd-story] .pds-ch.is-on::after{transform:scaleX(1);}
    [data-pd-story] .pds-h{display:grid;grid-template-columns:56px 1fr;align-items:baseline;margin:0 0 18px;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(22px,2vw,28px);line-height:1.25;letter-spacing:-0.02em;color:rgba(245,242,237,0.5);text-wrap:balance;transition:color 0.6s var(--e);}
    [data-pd-story] .pds-h .pds-n{font-size:11px;letter-spacing:0.16em;color:rgba(214,194,168,0.45);transition:color 0.6s var(--e);}
    [data-pd-story] .pds-ch.is-on .pds-h{color:#F5F2ED;}
    [data-pd-story] .pds-ch.is-on .pds-h .pds-n{color:#D6C2A8;}
    [data-pd-story] .pds-ch p{margin:0 0 0 56px;max-width:38rem;font-family:'Lama Sans',sans-serif;font-size:16px;line-height:1.95;color:rgba(232,223,216,0.72);}
    [data-pd-story] .pds-ch:first-of-type p{font-size:clamp(18px,1.5vw,21px);line-height:1.75;color:rgba(245,242,237,0.88);}
    [data-pd-story] .pds-inline{display:none;}
    /* the viewfinder */
    [data-pd-story] .pds-top{display:flex;justify-content:space-between;align-items:baseline;gap:16px;margin-bottom:16px;}
    [data-pd-story] .pds-top .pds-label{margin:0;}
    [data-pd-story] .pds-count{font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.14em;color:#F5F2ED;}
    [data-pd-story] .pds-frame{position:relative;display:block;aspect-ratio:4/3;max-height:max(200px,calc(100vh - 520px));background:#26201A;cursor:zoom-in;outline:none;}
    [data-pd-story] .pds-frame:focus-visible{outline:1px solid #D6C2A8;outline-offset:12px;}
    [data-pd-story] .pds-view{position:absolute;inset:0;overflow:hidden;}
    [data-pd-story] .pds-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.04);transition:opacity 0.8s var(--e),transform 1.6s var(--e);}
    [data-pd-story] .pds-img.is-on{opacity:1;transform:none;}
    [data-pd-story] .pds-frame:hover .pds-img.is-on{transform:scale(1.02);}
    [data-pd-story] .pds-mark{position:absolute;width:14px;height:14px;border:0 solid #D6C2A8;pointer-events:none;}
    [data-pd-story] .pds-mark--tl{top:-8px;left:-8px;border-width:1px 0 0 1px;}
    [data-pd-story] .pds-mark--tr{top:-8px;right:-8px;border-width:1px 1px 0 0;}
    [data-pd-story] .pds-mark--bl{bottom:-8px;left:-8px;border-width:0 0 1px 1px;}
    [data-pd-story] .pds-mark--br{bottom:-8px;right:-8px;border-width:0 1px 1px 0;}
    [data-pd-story] .pds-cap{display:flex;align-items:center;gap:12px;min-height:18px;margin:20px 0 0;font-family:'Lama Sans',sans-serif;font-size:12px;letter-spacing:0.02em;color:rgba(214,194,168,0.8);}
    [data-pd-story] .pds-cap::before{content:"";display:block;width:20px;height:1px;flex:none;background:rgba(214,194,168,0.6);}
    [data-pd-story] .pds-ticks{display:flex;gap:4px;margin:22px 0 0;padding:0;list-style:none;}
    [data-pd-story] .pds-ticks li{flex:1;}
    [data-pd-story] .pds-ticks button{display:block;width:100%;padding:10px 0 0;background:none;border:0;border-top:1px solid rgba(214,194,168,0.22);cursor:pointer;font-family:'Lama Sans',sans-serif;font-size:9px;letter-spacing:0.12em;color:rgba(214,194,168,0.4);transition:color 0.3s var(--e),border-color 0.3s var(--e);}
    [data-pd-story] .pds-ticks button.is-past{border-color:rgba(214,194,168,0.55);}
    [data-pd-story] .pds-ticks button.is-on{color:#F5F2ED;border-color:#F5F2ED;}
    [data-pd-story] .pds-ticks button:hover,[data-pd-story] .pds-ticks button:focus-visible{color:#F5F2ED;}
    /* the scope */
    [data-pd-story] .pds-scope{margin-top:32px;}
    [data-pd-story] .pds-scope-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding-bottom:12px;border-bottom:1px solid rgba(214,194,168,0.14);}
    [data-pd-story] .pds-scope-head .pds-label{margin:0;}
    [data-pd-story] .pds-scope-head small{font-family:'Lama Sans',sans-serif;font-size:11px;color:rgba(214,194,168,0.45);}
    [data-pd-story] .pds-scope ul{margin:0;padding:0;list-style:none;}
    [data-pd-story] .pds-scope li{display:flex;align-items:center;gap:14px;padding:12px 0;border-bottom:1px solid rgba(214,194,168,0.1);font-family:'Lama Sans',sans-serif;font-size:14px;color:rgba(245,242,237,0.38);transition:color 0.5s var(--e);}
    [data-pd-story] .pds-scope li::before{content:"";display:block;width:7px;height:7px;flex:none;border:1px solid rgba(214,194,168,0.4);transition:background 0.5s var(--e),border-color 0.5s var(--e);}
    [data-pd-story] .pds-scope li.is-on{color:#F5F2ED;}
    [data-pd-story] .pds-scope li.is-on::before{background:#D6C2A8;border-color:#D6C2A8;}
    [data-pd-story] .pds-cta{display:flex;align-items:center;justify-content:center;gap:12px;margin-top:28px;padding:17px 20px;background:#D6C2A8;border:1px solid #D6C2A8;color:#1F1F1F;text-decoration:none;font-family:'Lama Sans',sans-serif;font-size:10.5px;letter-spacing:0.2em;text-transform:uppercase;transition:background 0.4s var(--e),color 0.4s var(--e),gap 0.4s var(--e);}
    [data-pd-story] .pds-cta:hover,[data-pd-story] .pds-cta:focus-visible{background:transparent;color:#D6C2A8;gap:18px;}
    /* short laptop screens: the whole sidebar stays in view */
    @media(min-width:961px) and (max-height:860px){
      [data-pd-story] .pds-side{top:100px;}
      [data-pd-story] .pds-cap{margin-top:12px;}
      [data-pd-story] .pds-ticks{margin-top:14px;}
      [data-pd-story] .pds-scope{margin-top:20px;}
      [data-pd-story] .pds-scope li{padding:7px 0;}
      [data-pd-story] .pds-cta{margin-top:18px;padding:13px 20px;}
    }
    @media(max-width:960px){
      [data-pd-story] .pds-grid{display:block;}
      [data-pd-story] .pds-side{position:static;margin-top:16px;}
      [data-pd-story] .pds-top,[data-pd-story] .pds-frame,[data-pd-story] .pds-cap,[data-pd-story] .pds-ticks{display:none;}
      [data-pd-story] .pds-scope{margin-top:0;}
      [data-pd-story] .pds-h{grid-template-columns:40px 1fr;}
      [data-pd-story] .pds-ch p{margin-left:0;}
      [data-pd-story] .pds-inline{display:block;width:100%;aspect-ratio:3/2;object-fit:cover;margin:0 0 20px;background:#26201A;}
      [data-pd-story] .pds-h,[data-pd-story] .pds-h .pds-n{color:#F5F2ED;}
      [data-pd-story] .pds-h .pds-n{color:#D6C2A8;}
    }
    @media(prefers-reduced-motion:reduce){
      [data-pd-story] .pds-img,[data-pd-story] .pds-ch::after,[data-pd-story] .pds-h{transition:none;}
      [data-pd-story] .pds-img,[data-pd-story] .pds-frame:hover .pds-img.is-on{transform:none;}
    }
  </style>

  <div class="pds-grid">
    <div class="pds-text">
      <div class="pds-label"><i></i>The concept in six parts</div>
      <sc-for list="{{ chapters }}" as="ch" hint-placeholder-count="6">
        <article class="pds-ch" id="{{ ch.anchor }}" data-pds-ch data-shot="{{ ch.shot }}" data-disc="{{ ch.disc }}">
          <h2 class="pds-h"><span class="pds-n">{{ ch.num }}</span>{{ ch.title }}</h2>
          <img class="pds-inline" src="{{ ch.image }}" alt="{{ ch.caption }}" data-pos="{{ ch.pos }}" loading="lazy" decoding="async">
          <p>{{ ch.text }}</p>
        </article>
      </sc-for>
    </div>

    <aside id="pd-details-anchor" class="pds-side" aria-label="In view">
      <div class="pds-top"><div class="pds-label"><i></i>In view</div><span class="pds-count" data-pds-count>01 / 06</span></div>
      <div class="pds-frame" data-pds-frame role="button" tabindex="0" aria-label="Open this view full screen">
        <div class="pds-view">
          <sc-for list="{{ chapters }}" as="ch" hint-placeholder-count="6">
            <img class="pds-img" src="{{ ch.image }}" alt="{{ ch.caption }}" data-cap="{{ ch.caption }}" data-pos="{{ ch.pos }}" loading="lazy" decoding="async">
          </sc-for>
        </div>
        <i class="pds-mark pds-mark--tl"></i><i class="pds-mark pds-mark--tr"></i><i class="pds-mark pds-mark--bl"></i><i class="pds-mark pds-mark--br"></i>
      </div>
      <p class="pds-cap" data-pds-cap aria-live="polite">{{ firstCaption }}, concept visualisation</p>
      <ol class="pds-ticks" aria-label="Parts">
        <sc-for list="{{ chapters }}" as="ch" hint-placeholder-count="6">
          <li><button type="button" data-pds-tick aria-label="Part {{ ch.num }}: {{ ch.title }}">{{ ch.num }}</button></li>
        </sc-for>
      </ol>
      <div class="pds-scope">
        <div class="pds-scope-head"><div class="pds-label"><i></i>FurnishIQ scope</div><small>Lit: at work in this part</small></div>
        <ul>
          <li data-pds-d="d">Interior Design</li>
          <li data-pds-d="f">Fit-Out</li>
          <li data-pds-d="m">MEP Engineering</li>
          <li data-pds-d="u">Bespoke Furniture</li>
        </ul>
      </div>
      <a href="/contact" class="pds-cta" data-pd-similar>Discuss a similar project {ARROW}</a>
    </aside>
  </div>
</section>
""".replace("{ARROW}", ARROW)

# The facts strip: a museum label that completes the first screen. On desktop the photograph and this stone band fill
# the window exactly. Five facts, each with a fine-line drawing in a square tile, a small label and its value, divided
# by hairlines that draw in; the one action, a charcoal button, at the end.
ICON = {
    "category": '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/>',
    "location": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "area": '<path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.41 2.41 0 0 1 0-3.4l2.6-2.6a2.41 2.41 0 0 1 3.4 0Z"/><path d="m14.5 12.5 2-2"/><path d="m11.5 9.5 2-2"/><path d="m8.5 6.5 2-2"/><path d="m17.5 15.5 2-2"/>',
    "status": '<path d="M15.707 21.293a1 1 0 0 1-1.414 0l-1.586-1.586a1 1 0 0 1 0-1.414l5.586-5.586a1 1 0 0 1 1.414 0l1.586 1.586a1 1 0 0 1 0 1.414z"/><path d="m18 13-1.375-6.874a1 1 0 0 0-.746-.776L3.235 2.028a1 1 0 0 0-1.207 1.207L5.35 15.879a1 1 0 0 0 .776.746L13 18"/><path d="m2.3 2.3 7.286 7.286"/><circle cx="11" cy="11" r="2"/>',
    "scope": '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
}


def fact(key, label, value, d):
    svg = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % ICON[key]
    return ('    <div class="ptb-f ptb-in" style="--d:%ss;"><span class="ptb-i">%s</span><span class="ptb-t"><span class="ptb-k">%s</span><span class="ptb-v">%s</span></span></div>'
            % (d, svg, label, value))


TB_H = 144   # the band's height on desktop; the hero takes the rest of the window
TITLEBLOCK = """<!-- The title block: the project's facts as a museum label that completes the first screen -->
<section data-screen-label="Meta Strip" data-pd-tb>
  <style>
    /* the first screen: photograph and label together fill the window on desktop */
    @media(min-width:1261px){
      .fiq-pd-hero{height:100vh!important;height:100svh!important;min-height:640px!important;}
      .fiq-pd-hero .fiq-pd-hero-text{padding-bottom:calc(clamp(48px,6vw,72px) + {H}px)!important;}
      .fiq-pd-hero [data-pd-drift-toggle]{bottom:calc(clamp(48px,6vw,72px) + {H}px)!important;}
      [data-pd-tb]{margin-top:-{H}px;z-index:2;background:linear-gradient(to top,#1F1F1F 0%,#1F1F1F 38%,rgba(31,31,31,0.82) 68%,rgba(31,31,31,0) 100%)!important;}
    }
    [data-pd-tb]{--e:cubic-bezier(0.25,0.46,0.45,0.94);position:relative;background:#1F1F1F;color:#F5F2ED;padding:0 clamp(24px,5vw,80px);}
    [data-pd-tb] .ptb{max-width:1280px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;min-height:{H}px;box-sizing:border-box;}
    [data-pd-tb] .ptb-f{position:relative;display:flex;align-items:center;gap:16px;flex:none;padding:0 clamp(18px,2vw,28px);}
    [data-pd-tb] .ptb-f:last-child{padding-inline-end:0;}
    [data-pd-tb] .ptb-f:first-child{padding-inline-start:0;}
    [data-pd-tb] .ptb-f+.ptb-f::before{content:"";position:absolute;inset-inline-start:0;top:50%;width:1px;height:56px;margin-top:-28px;background:rgba(214,194,168,0.28);transform:scaleY(0);transition:transform 0.8s var(--e) calc(var(--d,0s) + 0.3s);}
    [data-pd-tb].is-in .ptb-f+.ptb-f::before{transform:scaleY(1);}
    [data-pd-tb] .ptb-i{display:flex;align-items:center;justify-content:center;flex:none;width:56px;height:56px;border:1px solid rgba(214,194,168,0.45);color:#D6C2A8;background:rgba(31,31,31,0.35);}
    [data-pd-tb] .ptb-t{display:flex;flex-direction:column;gap:8px;min-width:0;}
    [data-pd-tb] .ptb-k{font-family:'Lama Sans',sans-serif;font-size:10.5px;letter-spacing:0.24em;text-transform:uppercase;color:rgba(214,194,168,0.8);white-space:nowrap;}
    [data-pd-tb] .ptb-v{font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(17px,1.5vw,21px);line-height:1.2;letter-spacing:-0.01em;color:#F5F2ED;white-space:nowrap;}
    [data-pd-tb] .ptb-go{display:inline-flex;align-items:center;gap:14px;flex:none;margin-inline-start:auto;padding:17px 22px;background:#D6C2A8;border:1px solid #D6C2A8;color:#1F1F1F;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.2em;text-transform:uppercase;text-decoration:none;white-space:nowrap;transition:background 0.4s var(--e),color 0.4s var(--e),gap 0.4s var(--e);}
    [data-pd-tb] .ptb-go:hover,[data-pd-tb] .ptb-go:focus-visible{background:transparent;color:#D6C2A8;gap:20px;}
    /* entrance: the facts in order, the dividers drawn between them */
    [data-pd-tb] .ptb-in{opacity:0;transform:translateY(8px);transition:opacity 0.8s var(--e) var(--d,0s),transform 0.8s var(--e) var(--d,0s);}
    [data-pd-tb].is-in .ptb-in{opacity:1;transform:none;}
    @media(max-width:1366px) and (min-width:1261px){
      [data-pd-tb] .ptb-i{width:48px;height:48px;}
      [data-pd-tb] .ptb-f{gap:13px;padding:0 20px;}
    }
    @media(max-width:1260px){
      [data-pd-tb] .ptb{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px 20px;padding:clamp(28px,4vw,40px) 0;min-height:0;}
      [data-pd-tb] .ptb-f{padding:0;}
      [data-pd-tb] .ptb-f+.ptb-f::before{display:none;}
      [data-pd-tb] .ptb-go{grid-column:1/-1;justify-self:start;margin:4px 0 0;}
    }
    @media(max-width:600px){
      [data-pd-tb] .ptb{grid-template-columns:1fr 1fr;}
      [data-pd-tb] .ptb-i{width:38px;height:38px;}
      [data-pd-tb] .ptb-v{white-space:normal;}
      [data-pd-tb] .ptb-f:nth-child(4){grid-column:1/-1;}
      [data-pd-tb] .ptb-f:nth-child(4) .ptb-v{white-space:nowrap;}
      [data-pd-tb] .ptb-go{justify-self:stretch;justify-content:center;}
    }
    @media(prefers-reduced-motion:reduce){
      [data-pd-tb] .ptb-in{opacity:1;transform:none;transition:none;}
      [data-pd-tb] .ptb-f+.ptb-f::before{transform:none;transition:none;}
    }
  </style>
  <div class="ptb">
{FACTS}
  </div>
</section>
""".replace("{H}", str(TB_H)).replace("{FACTS}", "\n".join([
    fact("location", "Location", "{{ location }}", "0.1"),
    fact("area", "Built-up area", "{{ area }}", "0.15"),
    fact("status", "Status", "{{ date }}", "0.2"),
    fact("scope", "Scope", "{{ scopeShort }}", "0.25"),
])).replace("{ARROW}", ARROW)

TB_JS = """    // ── TITLE BLOCK: the cells come in once the block is on screen ──
    (() => {
      const tb = document.querySelector('[data-pd-tb]');
      if (!tb) return;
      new IntersectionObserver((es, o) => { es.forEach((e) => { if (e.isIntersecting) { tb.classList.add('is-in'); o.disconnect(); } }); }, { threshold: 0.2 }).observe(tb);
    })();

"""

JS = """    // ── PROJECT STORY: the viewfinder shows the room each part describes ──
    (() => {
      let tries = 0;
      const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const setup = () => {
        const sec = document.querySelector('[data-pd-story]');
        const chs = sec ? Array.from(sec.querySelectorAll('[data-pds-ch]')) : [];
        if (!chs.length || chs[0].dataset.shot.indexOf('{') !== -1) { if (tries++ < 40) setTimeout(setup, 100); return; }
        if (sec.dataset.ready) return;
        sec.dataset.ready = '1';
        const imgs = Array.from(sec.querySelectorAll('.pds-img'));
        const ticks = Array.from(sec.querySelectorAll('[data-pds-tick]'));
        const scope = Array.from(sec.querySelectorAll('[data-pds-d]'));
        const cap = sec.querySelector('[data-pds-cap]');
        const count = sec.querySelector('[data-pds-count]');
        const frame = sec.querySelector('[data-pds-frame]');
        const pad = (n) => String(n).padStart(2, '0');
        sec.querySelectorAll('[data-pos]').forEach((im) => { if (im.dataset.pos.indexOf('{') === -1) im.style.objectPosition = im.dataset.pos; });
        let cur = -1;
        const set = (k) => {
          if (k === cur) return;
          cur = k;
          chs.forEach((c, j) => c.classList.toggle('is-on', j === k));
          imgs.forEach((im, j) => im.classList.toggle('is-on', j === k));
          ticks.forEach((t, j) => { t.classList.toggle('is-on', j === k); t.classList.toggle('is-past', j < k); });
          const disc = (chs[k].dataset.disc || '').split(' ');
          scope.forEach((li) => li.classList.toggle('is-on', disc.indexOf('all') !== -1 || disc.indexOf(li.dataset.pdsD) !== -1));
          if (cap && imgs[k]) cap.textContent = imgs[k].dataset.cap + ', concept visualisation';
          if (count) count.textContent = pad(k + 1) + ' / ' + pad(chs.length);
        };
        // the part being read is the last one whose top has passed 45% of the screen
        const sync = () => {
          const line = window.innerHeight * 0.45;
          let k = 0;
          chs.forEach((c, j) => { if (c.getBoundingClientRect().top < line) k = j; });
          set(k);
        };
        window.addEventListener('scroll', sync, { passive: true });
        window.addEventListener('resize', sync);
        sync();
        ticks.forEach((t, j) => t.addEventListener('click', () => {
          const y = chs[j].getBoundingClientRect().top + window.scrollY - window.innerHeight * 0.3;
          window.scrollTo({ top: y, behavior: still ? 'auto' : 'smooth' });
        }));
        // the frame opens the same view in the page's lightbox
        const open = () => {
          const tile = document.querySelectorAll('.fiq-pd-tile')[+chs[cur].dataset.shot];
          if (tile) tile.click();
        };
        frame.addEventListener('click', open);
        frame.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
      };
      setup();
    })();

"""

RENDER_OLD = """    return {
      title: proj.title,"""
RENDER_NEW = """    // the story: each paragraph as a numbered part, paired with the view it describes
    const gal = (det && det.gallery) || [];
    const parts = this.CHAPTERS[proj.title] || [];
    const chapters = (det ? det.paras : []).map((text, i) => {
      const [title, shot, disc] = parts[i] || ['', i % Math.max(gal.length, 1), 'all'];
      const view = gal[shot] || {};
      return { num: String(i + 1).padStart(2, '0'), anchor: 'part-' + (i + 1), title, text, shot, disc, image: view.image || proj.image, caption: view.caption || proj.title, pos: view.pos || 'center' };
    });

    return {
      chapters,
      firstCaption: chapters.length ? chapters[0].caption : proj.title,
      title: proj.title,"""


def main():
    s = io.open(PAGE, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    s = s.replace("\r\n", "\n")
    # the facts strip on the same 1280px edge as the story
    old = ('<section data-screen-label="Meta Strip" style="background:#1F1F1F;border-bottom:1px solid rgba(214,194,168,0.12);">\n'
           '  <div class="fiq-pd-meta" style="max-width:1280px;margin:0 auto;padding:clamp(28px,3vw,40px) clamp(24px,5vw,80px);')
    if old in s:
        s = s.replace(old, '<section data-screen-label="Meta Strip" style="background:#1F1F1F;border-bottom:1px solid rgba(214,194,168,0.12);padding:0 clamp(24px,5vw,80px);">\n'
                           '  <div class="fiq-pd-meta" style="max-width:1280px;margin:0 auto;padding:clamp(28px,3vw,40px) 0;')
    # the story in place of the paragraphs and the facts sidebar
    a = s.index('<section data-screen-label="Project Body"') if '<section data-screen-label="Project Body"' in s else s.index("<!-- The story: six numbered parts")
    b = s.index("</section>", a) + len("</section>\n")
    s = s[:a] + SECTION + s[b:]
    s = re.sub(r"\n\s*\.fiq-pd-(body|sidebar)\{[^\n]*", "", s)
    # data: the six parts of every project
    data = "  CHAPTERS = " + json.dumps({k: [list(c) for c in v] for k, v in CHAPTERS.items()}, ensure_ascii=False, indent=None) + ";\n\n"
    if "  CHAPTERS = " in s:
        s = re.sub(r"  CHAPTERS = .*?;\n\n", lambda m: data, s, count=1, flags=re.S)
    else:
        i = s.index("  slugify(t)")
        s = s[:i] + data + s[i:]
    if "const chapters = (det" not in s:
        assert s.count(RENDER_OLD) == 1
        s = s.replace(RENDER_OLD, RENDER_NEW)
    if "PROJECT STORY" not in s:
        i = s.index("    // ── GALLERY LIGHTBOX")
        s = s[:i] + JS + s[i:]
    # the facts strip, as a title block
    a = s.index('<section data-screen-label="Meta Strip"')
    c = s.rfind("<!-- The title block", 0, a)
    if c != -1 and a - c < 120:   # rebuilt before: replace from its comment
        a = c
    b = s.index("</section>", a) + len("</section>\n")
    s = s[:a] + TITLEBLOCK + s[b:]
    s = re.sub(r"\n\s*\.fiq-pd-meta\{[^\n]*", "", s)
    old_hero = '<div style="position:absolute;left:0;right:0;bottom:0;z-index:1;max-width:1280px;margin:0 auto;width:100%;padding:0 clamp(24px,5vw,80px)'
    if old_hero in s:
        s = s.replace(old_hero, '<div style="position:absolute;left:0;right:0;bottom:0;z-index:1;max-width:1280px;box-sizing:content-box;margin:0 auto;padding:0 clamp(24px,5vw,80px)')
    hero_old = '<section data-screen-label="Hero" style="position:relative;height:82vh;'
    if hero_old in s:
        s = s.replace(hero_old, '<section data-screen-label="Hero" class="fiq-pd-hero" style="position:relative;height:82vh;')
    back_old = '<a href="/projects" style="position:absolute;top:104px;left:clamp(24px,5vw,80px);'
    if back_old in s:
        s = s.replace(back_old, '<a href="/projects" style="position:absolute;top:104px;left:max(clamp(24px,5vw,80px),calc((100% - 1280px) / 2));')
    text_old = '<div style="position:absolute;left:0;right:0;bottom:0;z-index:1;max-width:1280px;'
    if text_old in s:   # a hook for the full-screen rule; the runtime rewrites inline styles, so match a class
        s = s.replace(text_old, '<div class="fiq-pd-hero-text" style="position:absolute;left:0;right:0;bottom:0;z-index:1;max-width:1280px;')
    if "scopeShort:" not in s:   # the four disciplines in a word each; "Fit-Out" never breaks at its hyphen
        s = s.replace("      chapters,\n", "      chapters,\n      scopeShort: ((det && det.scope) || '').replace('Interior Design', 'Design').replace('MEP Engineering', 'MEP').replace('Bespoke Furniture', 'Furniture').replace(/-/g, '\\u2011'),\n", 1)
    if "scopeLine:" not in s:   # "Fit-Out" never breaks at its hyphen
        s = s.replace("      chapters,\n", "      chapters,\n      scopeLine: ((det && det.scope) || '').replace(/-/g, '\\u2011'),\n", 1)
    if "areaNum:" not in s:
        s = s.replace("      chapters,\n", "      chapters,\n      areaNum: (det ? det.area : '').replace(/\\s*m²$/, ''),\n", 1)
    if "projNum:" not in s:
        s = s.replace("      chapters,\n", "      chapters,\n      projNum: String(this.PROJECTS.indexOf(proj) + 1).padStart(2, '0'),\n      projTotal: String(this.PROJECTS.length).padStart(2, '0'),\n", 1)
    if "TITLE BLOCK:" not in s:
        i = s.index("    // ── PROJECT STORY")
        s = s[:i] + TB_JS + s[i:]
    for name in CHAPTERS:
        assert '"%s": {' % name in s, name
    io.open(PAGE, "w", encoding="utf-8", newline="").write(s.replace("\n", "\r\n") if crlf else s)
    print(PAGE, "story built for", len(CHAPTERS), "projects")


if __name__ == "__main__":
    main()

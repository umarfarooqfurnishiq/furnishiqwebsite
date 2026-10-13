"""Site: the closing draw. A call to action that draws the next one, and it is always yours.

The section's text sits beside a drafting frame that shuffles through a page's items (the projects page's ten
concepts, the insights page's articles), numbered and captioned, slowing like a draw, and always comes to rest on the
last sheet: a blank grid with its number, which is the visitor's (Project 11, the next insight). A strip of ticks
follows the draw. Clicking the sheet draws again, and it lands there again. Reduced motion shows the last sheet at
once; on phones the frame sits below the text. Used by scripts/projects/pj_cta.py and scripts/blog/blog_cta.py.
"""
import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
ARROW = {
    "en": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
    "ar": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>',
}
AGAIN = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>'




def section(lang, *, label, text_html, items, big, you, svc, final, frame_aria, again, rounds=1):
    """items: (image path, caption) pairs, in order."""
    ar = lang == "ar"
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    caps = "normal" if ar else "0.22em"
    small = "12px" if ar else "9.5px"
    PAD = "clamp(24px,5vw,80px)"
    imgs = "\n".join(f'          <img class="pc-img" data-src="{src}" data-cap="{cap}" alt="" decoding="async">' for src, cap in items)
    ticks = "\n".join(f'        <li><span dir="ltr">{i:02d}</span></li>' for i in range(1, len(items) + 2))
    return f"""<section data-screen-label="{label}" data-pj-cta{' dir="rtl"' if ar else ''} style="background:#3A2D25;color:#F5F2ED;border-top:1px solid rgba(214,194,168,0.12);padding:clamp(64px,8vw,128px) {PAD};overflow:hidden;">
  <style>
    [data-pj-cta] .pc-wrap{{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(40px,6vw,104px);align-items:center;}}
    [data-pj-cta] .pc-eyebrow{{display:flex;align-items:center;gap:16px;margin:0 0 26px;font-family:{font};font-size:{small};letter-spacing:{'normal' if ar else '0.3em'};text-transform:uppercase;color:rgba(214,194,168,0.75);}}
    [data-pj-cta] .pc-eyebrow i{{display:block;width:32px;height:1px;background:#D6C2A8;}}
    [data-pj-cta] .pc-h2{{margin:0;font-family:{font};font-weight:500;font-size:{'clamp(32px,3.4vw,50px)' if ar else 'clamp(34px,3.8vw,58px)'};line-height:{'1.3' if ar else '1.06'};letter-spacing:{'0' if ar else '-0.02em'};color:#F5F2ED;text-wrap:balance;}}
    [data-pj-cta] .pc-h2 span{{display:block;color:#D6C2A8;}}
    [data-pj-cta] .pc-sub{{margin:clamp(20px,2.4vw,28px) 0 0;max-width:{'20em' if ar else '30ch'};font-family:{font};font-size:{'clamp(17px,1.4vw,20px)' if ar else 'clamp(16px,1.3vw,19px)'};line-height:1.6;color:rgba(245,242,237,0.66);}}
    [data-pj-cta] .pc-ctas{{display:flex;align-items:center;flex-wrap:wrap;gap:16px 28px;margin-top:clamp(30px,3.4vw,44px);}}
    [data-pj-cta] .pc-cta{{display:inline-flex;align-items:center;gap:14px;padding:19px 34px;background:#D6C2A8;color:#1F1F1F;border:1px solid #D6C2A8;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10.5px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;transition:background 0.4s {EASE},color 0.4s {EASE};}}
    [data-pj-cta] .pc-cta:hover,[data-pj-cta] .pc-cta:focus-visible{{background:transparent;color:#D6C2A8;}}
    [data-pj-cta] .pc-wa{{display:inline-flex;align-items:center;gap:12px;padding-bottom:6px;border-bottom:1px solid rgba(214,194,168,0.45);color:#F5F2ED;text-decoration:none;font-family:{font};font-size:{'13px' if ar else '10.5px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;transition:color 0.4s {EASE},border-color 0.4s {EASE};}}
    [data-pj-cta] .pc-wa:hover,[data-pj-cta] .pc-wa:focus-visible{{color:#D6C2A8;border-color:#D6C2A8;}}
    /* a sign-up form in the text column */
    [data-pj-cta] .pc-form{{display:flex;margin-top:clamp(30px,3.4vw,44px);max-width:480px;border:1px solid rgba(214,194,168,0.3);transition:border-color 0.4s {EASE};}}
    [data-pj-cta] .pc-form:focus-within{{border-color:#D6C2A8;}}
    [data-pj-cta] .pc-form input{{flex:1;min-width:0;background:transparent;border:0;outline:none;padding:18px 20px;font-family:{font};font-size:15px;color:#F5F2ED;}}
    [data-pj-cta] .pc-form input::placeholder{{color:rgba(245,242,237,0.45);}}
    [data-pj-cta] .pc-form button{{flex:none;display:inline-flex;align-items:center;gap:12px;padding:0 28px;background:#D6C2A8;border:0;cursor:pointer;font-family:{font};font-size:{'13px' if ar else '10.5px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;color:#1F1F1F;transition:background 0.4s {EASE};}}
    [data-pj-cta] .pc-form button:hover,[data-pj-cta] .pc-form button:focus-visible{{background:#F5F2ED;}}
    [data-pj-cta] .pc-ok{{margin:14px 0 0;font-family:{font};font-size:13px;color:rgba(214,194,168,0.75);}}
    /* the drafting frame */
    [data-pj-cta] .pc-stage{{position:relative;padding-top:26px;}}
    [data-pj-cta] .pc-dim{{position:absolute;top:0;left:0;right:0;height:9px;}}
    [data-pj-cta] .pc-dim::before,[data-pj-cta] .pc-dim::after{{content:"";position:absolute;top:0;width:1px;height:9px;background:rgba(214,194,168,0.5);}}
    [data-pj-cta] .pc-dim::before{{left:0;}}
    [data-pj-cta] .pc-dim::after{{right:0;}}
    [data-pj-cta] .pc-dim i{{position:absolute;top:4px;left:0;right:0;height:1px;background:rgba(214,194,168,0.5);}}
    [data-pj-cta] .pc-cap{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);padding:0 14px;background:#3A2D25;white-space:nowrap;font-family:{font};font-size:{small};letter-spacing:{caps};text-transform:uppercase;color:rgba(214,194,168,0.9);}}
    [data-pj-cta] .pc-frame{{position:relative;display:block;margin:0;aspect-ratio:4/3;cursor:pointer;outline:none;}}
    [data-pj-cta] .pc-frame:focus-visible{{outline:1px solid #D6C2A8;outline-offset:14px;}}
    [data-pj-cta] .pc-view{{position:absolute;inset:0;overflow:hidden;background:#1F1712;box-shadow:0 24px 80px rgba(0,0,0,0.35);}}
    [data-pj-cta] .pc-img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;}}
    [data-pj-cta] .pc-img.is-on{{opacity:1;}}
    [data-pj-cta] .pc-sheet{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:clamp(10px,1.4vw,18px);opacity:0;}}
    [data-pj-cta] .pc-sheet svg.pc-grid{{position:absolute;inset:0;width:100%;height:100%;color:rgba(214,194,168,0.07);}}
    /* the sheet fades in as the draw lands on it, and is gone at once when a draw begins */
    [data-pj-cta] .is-yours .pc-sheet{{opacity:1;transition:opacity 0.9s {EASE};}}
    [data-pj-cta] .pc-eleven{{position:relative;font-family:'Lama Sans',sans-serif;font-weight:500;font-size:clamp(96px,11vw,176px);line-height:0.9;letter-spacing:-0.04em;color:#D6C2A8;transform:translateY(14px);opacity:0;transition:opacity 0.9s {EASE} 0.15s,transform 0.9s {EASE} 0.15s;}}
    [data-pj-cta] .pc-you{{position:relative;font-family:{font};font-size:{'15px' if ar else '11px'};letter-spacing:{caps};text-transform:uppercase;color:#F5F2ED;opacity:0;transition:opacity 0.9s {EASE} 0.35s;}}
    [data-pj-cta] .pc-svc{{position:relative;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.16em'};text-transform:uppercase;color:rgba(214,194,168,0.6);opacity:0;transition:opacity 0.9s {EASE} 0.5s;text-align:center;padding:0 16px;}}
    [data-pj-cta] .is-yours .pc-eleven{{opacity:1;transform:none;}}
    [data-pj-cta] .is-yours .pc-you,[data-pj-cta] .is-yours .pc-svc{{opacity:1;}}
    [data-pj-cta] .pc-num{{position:absolute;bottom:14px;inset-inline-end:16px;z-index:2;padding:6px 10px;background:rgba(31,31,31,0.62);font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.2em;color:#F5F2ED;transition:opacity 0.5s {EASE};}}
    [data-pj-cta] .is-yours .pc-num{{opacity:0;}}
    [data-pj-cta] .pc-mark{{position:absolute;width:18px;height:18px;border:0 solid #D6C2A8;}}
    [data-pj-cta] .pc-mark--tl{{top:-10px;left:-10px;border-width:1px 0 0 1px;}}
    [data-pj-cta] .pc-mark--tr{{top:-10px;right:-10px;border-width:1px 1px 0 0;}}
    [data-pj-cta] .pc-mark--bl{{bottom:-10px;left:-10px;border-width:0 0 1px 1px;}}
    [data-pj-cta] .pc-mark--br{{bottom:-10px;right:-10px;border-width:0 1px 1px 0;}}
    /* one tick per item, and a longer last one for the sheet the draw lands on */
    [data-pj-cta] .pc-foot{{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-top:26px;}}
    [data-pj-cta] .pc-ticks{{display:flex;flex:1;gap:4px;margin:0;padding:0;list-style:none;}}
    [data-pj-cta] .pc-ticks li{{flex:1;padding-top:10px;border-top:1px solid rgba(214,194,168,0.22);font-family:'Lama Sans',sans-serif;font-size:9px;letter-spacing:0.12em;color:rgba(214,194,168,0.38);text-align:center;transition:color 0.2s,border-color 0.2s;}}
    [data-pj-cta] .pc-ticks li.is-on{{color:#F5F2ED;border-color:#F5F2ED;}}
    [data-pj-cta] .pc-ticks li:last-child{{flex:1.6;}}
    [data-pj-cta] .is-yours .pc-ticks li:last-child{{color:#D6C2A8;border-color:#D6C2A8;}}
    [data-pj-cta] .pc-again{{flex:none;display:inline-flex;align-items:center;gap:8px;padding:0;background:none;border:0;cursor:pointer;font-family:{font};font-size:{'12px' if ar else '9.5px'};letter-spacing:{caps};text-transform:uppercase;color:rgba(214,194,168,0.7);transition:color 0.3s;}}
    [data-pj-cta] .pc-again:hover,[data-pj-cta] .pc-again:focus-visible{{color:#F5F2ED;}}
    [data-pj-cta] .pc-again:disabled{{opacity:0.35;cursor:default;}}
    @media(max-width:900px){{
      [data-pj-cta] .pc-wrap{{grid-template-columns:1fr;}}
      [data-pj-cta] .pc-cta{{width:100%;justify-content:center;box-sizing:border-box;}}
      [data-pj-cta] .pc-ticks li{{font-size:0;padding-top:8px;}}
      [data-pj-cta] .pc-cap{{max-width:calc(100% - 40px);overflow:hidden;text-overflow:ellipsis;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      [data-pj-cta] *{{transition:none!important;}}
    }}
  </style>
  <div class="pc-wrap">
    <div class="pc-text">
{text_html}
    </div>
    <div class="pc-stage" data-pc-stage data-rounds="{rounds}">
      <div class="pc-dim" aria-hidden="true"><i></i><span class="pc-cap" data-pc-cap>{final}</span></div>
      <figure class="pc-frame" data-pc-frame role="button" tabindex="0" aria-label="{frame_aria}" data-final="{final}">
        <div class="pc-view">
{imgs}
          <div class="pc-sheet" aria-hidden="true">
            <svg class="pc-grid"><defs><pattern id="pc-grid-{lang}" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32,0V32M0,32H32" fill="none" stroke="currentColor" stroke-width="1"/></pattern></defs><rect width="100%" height="100%" fill="url(#pc-grid-{lang})"/></svg>
            <span class="pc-eleven" dir="ltr">{big}</span>
            <span class="pc-you">{you}</span>
            <span class="pc-svc">{svc}</span>
          </div>
          <span class="pc-num" data-pc-num dir="ltr" aria-hidden="true">01</span>
        </div>
        <i class="pc-mark pc-mark--tl" aria-hidden="true"></i><i class="pc-mark pc-mark--tr" aria-hidden="true"></i><i class="pc-mark pc-mark--bl" aria-hidden="true"></i><i class="pc-mark pc-mark--br" aria-hidden="true"></i>
      </figure>
      <div class="pc-foot">
        <ol class="pc-ticks" aria-hidden="true">
{ticks}
        </ol>
        <button type="button" class="pc-again" data-pc-again>{AGAIN}{again}</button>
      </div>
    </div>
  </div>
</section>
"""


JS = """    // ── CLOSING DRAW: THE NEXT ONE IS YOURS ───────────────────────────────
    {
      const sec = document.querySelector('[data-pj-cta]');
      if (sec) {
        const stage = sec.querySelector('[data-pc-stage]'), frame = sec.querySelector('[data-pc-frame]'), again = sec.querySelector('[data-pc-again]');
        const imgs = Array.from(sec.querySelectorAll('.pc-img')), ticks = Array.from(sec.querySelectorAll('.pc-ticks li'));
        const cap = sec.querySelector('[data-pc-cap]'), num = sec.querySelector('[data-pc-num]'), N = imgs.length;
        const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
        let timer = 0, running = false, ready = null;
        // the covers are fetched as the section nears, and the draw waits for them (2.5s at most), so it never shuffles blanks
        const load = () => {
          if (!ready) {
            imgs.forEach((im) => { im.src = im.dataset.src; });
            ready = Promise.race([Promise.all(imgs.map((im) => im.decode().catch(() => {}))), new Promise((r) => setTimeout(r, 2500))]);
          }
          return ready;
        };
        const R = Math.max(1, +stage.dataset.rounds || 1), S = N * R;   // the items, run through R times
        const step = (k) => {   // k < S: item k % N on the sheet; k = S: the sheet the draw lands on
          k = k < S ? k % N : N;
          imgs.forEach((im, j) => im.classList.toggle('is-on', j === k));
          ticks.forEach((t, j) => t.classList.toggle('is-on', j <= k));
          stage.classList.toggle('is-yours', k === N);
          cap.textContent = k === N ? frame.dataset.final : imgs[k].dataset.cap;
          num.textContent = String(k + 1).padStart(2, '0');
        };
        const settle = () => { clearTimeout(timer); running = false; again.disabled = false; step(S); };
        // the draw: through the items, quick at first and slowing, and it always comes to rest on the last sheet
        const draw = async () => {
          if (running) return;
          if (still) { load(); settle(); return; }
          running = true; again.disabled = true;
          await load();
          let k = 0, wait = 80;
          const grow = Math.pow(7, 1 / S);   // the last wait is about seven times the first, however many steps
          const next = () => {
            step(k);
            if (k === S) { running = false; again.disabled = false; return; }
            k += 1; wait *= grow;
            timer = setTimeout(next, wait);
          };
          next();
        };
        step(S);   // until the section is reached, and without script, the last sheet shows
        new IntersectionObserver((es, o) => { es.forEach((e) => { if (e.isIntersecting) { load(); o.disconnect(); } }); }, { rootMargin: '0px 0px 60% 0px' }).observe(sec);
        new IntersectionObserver((es, o) => { es.forEach((e) => { if (e.isIntersecting) { draw(); o.disconnect(); } }); }, { threshold: 0.45 }).observe(stage);
        frame.addEventListener('click', draw);
        frame.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); draw(); } });
        again.addEventListener('click', draw);
        document.addEventListener('visibilitychange', () => { if (document.hidden && running) settle(); });
      }
    }

"""
HEAD = "    // ── CLOSING DRAW: THE NEXT ONE IS YOURS"


def inject_js(s, anchor, name):
    """The draw's script, once, before anchor; an earlier copy (or the projects page's first one) is replaced."""
    for head in (HEAD, "    // ── PROJECTS, CLOSING: PROJECT 11"):
        if head in s:
            a = s.index(head); b = s.index("\n\n", s.index("\n    }\n", a)) + 2
            s = s[:a] + s[b:]
    assert s.count(anchor) == 1, name
    return s.replace(anchor, JS + anchor)

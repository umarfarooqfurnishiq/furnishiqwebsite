import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
IMGS = [("about-mission-majlis-drawing-to-reality", [1200, 1792]),
        ("about-vision-desert-sunrise-lounge", [1200, 1792]),
        ("about-values-walnut-dovetail-craft", [1200, 1792])]
C = {
    "en": dict(
        label="Who We Are", h2="Redefining the design-build landscape in Saudi Arabia.",
        rows=[("Mission", "To deliver bespoke Design, Build, and Management solutions that transform ideas into meaningful environments.", None),
              ("Vision", "To redefine the way people experience spaces by creating environments that express individuality, inspire excellence, and enrich everyday life.", None),
              ("Values", None, ["Integrity", "Quality", "Innovation", "Client Focus"])],
        prefix="Our", v2030_k="Vision 2030",
        v2030="Aligned with Saudi Arabia's Vision 2030, we are committed to delivering world-class solutions that contribute to a thriving and sustainable future.",
        cta="View Our Projects", href="/projects",
        caps=["From drawing to majlis, concept visualisation", "A view of what is possible, concept visualisation", "Hand-cut walnut joinery, concept visualisation"],
    ),
    "ar": dict(
        label="من نحن", h2="إعادة تعريف قطاع التصميم والتنفيذ في المملكة العربية السعودية.",
        rows=[("رسالتنا", "تقديم حلول تصميم وتنفيذ وإدارة مخصصة تُحوّل الأفكار إلى بيئات ذات معنى.", None),
              ("رؤيتنا", "إعادة تعريف الطريقة التي يختبر بها الناس المساحات من خلال خلق بيئات تعبر عن الفردية، وتُلهم التميز، وتُثري الحياة اليومية.", None),
              ("قيمنا", None, ["النزاهة", "الجودة", "الابتكار", "التركيز على العميل"])],
        prefix="", v2030_k="رؤية 2030",
        v2030="انسجاماً مع رؤية المملكة العربية السعودية 2030، نلتزم بتقديم حلول عالمية المستوى تسهم في مستقبل مزدهر ومستدام.",
        cta="شاهد مشاريعنا", href="/ar/projects",
        caps=["من المخطط إلى المجلس، تصور تصميمي", "إطلالة على الممكن، تصور تصميمي", "وصلات من خشب الجوز مشغولة يدوياً، تصور تصميمي"],
    ),
}


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    flip = "scaleX(-1)" if ar else "none"
    arrow = f'<svg width="16" height="6" viewBox="0 0 16 6" fill="none" aria-hidden="true" style="transform:{flip};"><path d="M0 3H14M14 3L11.5 1M14 3L11.5 5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
    ss = lambda img, ws: ", ".join(f"uploads/{img}-{w}.webp {w}w" for w in ws)

    frames = ""
    for i, (img, ws) in enumerate(IMGS):
        frames += f"""
        <figure class="cp-frame{' is-active' if i == 0 else ''}" data-cp-frame><img src="uploads/{img}-{ws[-1]}.webp" srcset="{ss(img, ws)}" sizes="(max-width:900px) 100vw, 42vw" alt="{c['caps'][i]}" loading="lazy" decoding="async"><figcaption>{c['caps'][i]}</figcaption></figure>"""
    rows = ""
    for i, ((word, text, values), (img, ws)) in enumerate(zip(c["rows"], IMGS)):
        body = f'<p class="cp-text">{text}</p>' if text else '<ul class="cp-values">' + "".join(f"<li>{v}</li>" for v in values) + "</ul>"
        pre = f'<span class="cp-pre">{c["prefix"]}</span>' if c["prefix"] else ""
        rows += f"""
        <article class="cp-row{' is-active' if i == 0 else ''}" data-cp-row>
          <img class="cp-mimg" src="uploads/{img}-{ws[0]}.webp" alt="" loading="lazy" decoding="async">
          <span class="cp-num" dir="ltr">0{i + 1}</span>
          <div class="cp-head">{pre}<h3 class="cp-word">{word}</h3></div>
          {body}
        </article>"""

    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ BRAND STATEMENT ━━━ -->
<section id="who" data-compass{' dir="rtl"' if ar else ''} style="position:relative;background:#F5F2ED;height:320vh;">
  <style>
    #who .cp-stage{{position:sticky;top:0;height:100vh;min-height:620px;overflow:hidden;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);}}
    #who .cp-media{{position:relative;}}
    #who .cp-frame{{position:absolute;inset:0;margin:0;overflow:hidden;opacity:0;clip-path:inset(0 0 100% 0);transition:clip-path 1.1s {EASE},opacity 0s linear 1.1s;}}
    #who .cp-frame.is-active{{opacity:1;clip-path:inset(0 0 0 0);z-index:2;transition:clip-path 1.1s {EASE},opacity 0s;}}
    #who .cp-frame img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scale(1.08);transition:transform 2.4s {EASE};}}
    #who .cp-frame.is-active img{{transform:scale(1);}}
    #who .cp-frame figcaption{{position:absolute;bottom:0;inset-inline-end:0;padding:12px 18px;background:rgba(30,22,16,0.72);font-family:{font};font-size:{'13px' if ar else '12px'};letter-spacing:{'normal' if ar else '0.06em'};color:#F5F2ED;}}
    #who .cp-body{{display:flex;flex-direction:column;justify-content:space-between;gap:24px;padding:clamp(104px,14vh,140px) clamp(24px,5vw,80px) clamp(64px,8vw,100px);padding-inline-start:clamp(40px,5vw,96px);}}
    #who .cp-label{{display:flex;align-items:center;gap:16px;margin-bottom:18px;font-family:{font};font-size:9px;letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    #who .cp-label i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    #who .cp-h2{{font-family:{font};font-size:{'clamp(24px,2.3vw,38px)' if ar else 'clamp(26px,2.6vw,42px)'};font-weight:500;line-height:{'1.4' if ar else '1.12'};letter-spacing:{'normal' if ar else '-0.02em'};color:#1F1F1F;margin:0;max-width:640px;}}
    #who .cp-slot{{position:relative;display:grid;align-items:center;border-top:1px solid rgba(58,45,37,0.18);border-bottom:1px solid rgba(58,45,37,0.18);padding:clamp(20px,3vh,36px) 0;padding-inline-end:28px;}}
    #who .cp-row{{grid-area:1/1;display:grid;grid-template-columns:auto minmax(0,1fr);column-gap:clamp(16px,2vw,32px);align-items:start;opacity:0;transform:translateY(28px);pointer-events:none;transition:opacity 0.6s {EASE},transform 0.8s {EASE};}}
    #who .cp-row.is-active{{opacity:1;transform:none;pointer-events:auto;transition-delay:0.15s;}}
    #who .cp-row.is-past{{transform:translateY(-28px);}}
    #who .cp-mimg{{display:none;}}
    #who .cp-num{{grid-row:1 / span 2;font-family:'Lama Sans',sans-serif;font-size:clamp(64px,6.4vw,120px);line-height:0.85;letter-spacing:-0.04em;color:rgba(139,107,74,0.28);}}
    #who .cp-head{{display:flex;align-items:baseline;gap:14px;}}
    #who .cp-pre{{font-family:{font};font-size:clamp(18px,1.6vw,24px);color:#8B6B4A;}}
    #who .cp-word{{font-family:{font};font-size:clamp(46px,5.2vw,92px);font-weight:500;line-height:1.05;letter-spacing:{'normal' if ar else '-0.035em'};margin:0;color:#3A2D25;}}
    #who .cp-text{{grid-column:2;font-family:{font};font-size:clamp(16px,1.25vw,19px);line-height:1.7;color:#5B4636;margin:18px 0 0;max-width:540px;}}
    #who .cp-values{{grid-column:2;list-style:none;margin:20px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:10px 12px;}}
    #who .cp-values li{{font-family:{font};font-size:{'14px' if ar else '11px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;color:#3A2D25;padding:11px 18px;border:1px solid rgba(58,45,37,0.3);}}
    #who .cp-dots{{position:absolute;inset-inline-end:0;top:50%;transform:translateY(-50%);display:flex;flex-direction:column;gap:10px;}}
    #who .cp-dots i{{display:block;width:2px;height:28px;background:rgba(58,45,37,0.18);cursor:pointer;transition:background 0.5s {EASE};position:relative;}}
    #who .cp-dots i::before{{content:"";position:absolute;inset:-6px -10px;}}
    #who .cp-dots i.is-active{{background:#8B6B4A;}}
    #who .cp-foot{{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:16px 24px;align-items:center;}}
    #who .cp-badge{{font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#F5F2ED;background:#3A2D25;padding:10px 14px;white-space:nowrap;}}
    #who .cp-2030{{font-family:{font};font-size:{'15px' if ar else '14px'};line-height:1.7;color:#5B4636;margin:0;max-width:520px;}}
    #who .cp-link{{display:inline-flex;align-items:center;gap:14px;white-space:nowrap;font-family:{font};font-size:{'13px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.2em'};text-transform:uppercase;color:#3A2D25;text-decoration:none;padding-bottom:6px;border-bottom:1px solid #8B6B4A;transition:color 0.4s {EASE},border-color 0.4s {EASE};}}
    #who .cp-link:hover,#who .cp-link:focus-visible{{color:#8B6B4A;border-color:#3A2D25;}}
    @media(min-width:901px) and (max-height:760px){{
      #who .cp-body{{padding-top:96px;}}
      #who .cp-h2{{font-size:clamp(22px,2.1vw,32px);}}
      #who .cp-label{{margin-bottom:12px;}}
      #who .cp-slot{{padding:16px 0;}}
      #who .cp-word{{font-size:clamp(40px,4.4vw,68px);}}
      #who .cp-num{{font-size:clamp(52px,5vw,84px);}}
      #who .cp-text{{margin-top:12px;font-size:16px;}}
      #who .cp-values{{margin-top:14px;}}
      #who .cp-values li{{padding:9px 14px;}}
    }}
    @media(max-width:900px){{
      #who{{height:auto!important;padding:clamp(64px,8vw,100px) clamp(24px,5vw,80px);}}
      #who .cp-stage{{position:static;height:auto;min-height:0;display:block;overflow:visible;}}
      #who .cp-media,#who .cp-dots{{display:none;}}
      #who .cp-body{{padding:0;gap:32px;}}
      #who .cp-slot{{display:block;border:none;padding:0;}}
      #who .cp-row{{opacity:1;transform:none;pointer-events:auto;padding:28px 0;border-top:1px solid rgba(58,45,37,0.18);}}
      #who .cp-mimg{{display:block;grid-column:1/-1;width:100%;aspect-ratio:4/3;object-fit:cover;margin-bottom:20px;}}
      #who .cp-row{{display:block;}}
      #who .cp-num{{display:block;font-size:48px;margin-bottom:6px;}}
      #who .cp-text,#who .cp-values{{max-width:none;}}
      #who .cp-foot{{grid-template-columns:1fr;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      #who .cp-frame,#who .cp-frame img,#who .cp-row{{transition:none;}}
    }}
  </style>
  <div class="cp-stage">
    <div class="cp-media">{frames}
    </div>
    <div class="cp-body">
      <div>
        <div class="cp-label"><i></i>{c['label']}</div>
        <h2 class="cp-h2">{c['h2']}</h2>
      </div>
      <div class="cp-slot">{rows}
        <span class="cp-dots" aria-hidden="true"><i class="is-active"></i><i></i><i></i></span>
      </div>
      <div class="cp-foot">
        <span class="cp-badge">{c['v2030_k']}</span>
        <p class="cp-2030">{c['v2030']}</p>
        <a class="cp-link" href="{c['href']}">{c['cta']}{arrow}</a>
      </div>
    </div>
  </div>
</section>
"""


JS = """    // ── WHO WE ARE: COMPASS (pinned stage, statements swap in place) ─────────
    {
      const cp = document.querySelector('[data-compass]');
      if (cp) {
        const rows = [...cp.querySelectorAll('[data-cp-row]')], frames = [...cp.querySelectorAll('[data-cp-frame]')], dots = [...cp.querySelectorAll('.cp-dots i')];
        let cur = -1, ticking = false;
        const pick = (n) => {
          if (n === cur) return; cur = n;
          rows.forEach((r, k) => { r.classList.toggle('is-active', k === n); r.classList.toggle('is-past', k < n); });
          frames.forEach((f, k) => f.classList.toggle('is-active', k === n));
          dots.forEach((d, k) => d.classList.toggle('is-active', k === n));
        };
        const update = () => {
          ticking = false;
          if (window.innerWidth <= 900) return;
          const total = cp.offsetHeight - window.innerHeight;
          const p = Math.min(Math.max(-cp.getBoundingClientRect().top / (total || 1), 0), 0.999);
          pick(Math.floor(p * rows.length));
        };
        dots.forEach((d, i) => d.addEventListener('click', () => {
          const total = cp.offsetHeight - window.innerHeight;
          window.scrollTo({ top: cp.offsetTop + total * (i + 0.5) / rows.length, behavior: reduced ? 'auto' : 'smooth' });
        }));
        pick(0); update();
        // one wheel notch, one statement (STEP SNAP)
        (window.fiqSnap = window.fiqSnap || []).push({ on: () => matchMedia('(min-width:901px) and (min-height:600px)').matches, geo: () => { const a = cp.getBoundingClientRect().top + window.scrollY, total = cp.offsetHeight - window.innerHeight; return { a, b: a + total, stops: rows.map((_, i) => a + total * (i + 0.5) / rows.length) }; } });
        window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
        window.addEventListener('resize', update);
      }
    }

"""
MARK = "    // ── FADE-IN ON LOAD (lazy images)"

for path, lang in [("about-us.dc.html", "en"), ("about-us.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ BRAND STATEMENT ━+ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── WHO WE ARE: COMPASS"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

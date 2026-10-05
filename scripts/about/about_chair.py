import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
C = {
    "en": dict(
        label="Message from the Chairman",
        quote=["At", "FurnishIQ,", "we", "believe", "exceptional", "spaces", "begin", "with", "a", "deep", "understanding", "of", "our", "clients’", "aspirations.",
               "We", "don’t", "just", "design.", "*We", "*build", "*trust", "*and", "*create", "*lasting", "*value."],
        name="Adel bin Ali Al Tamimi", role="Chairman, FurnishIQ",
        alt="Adel bin Ali Al Tamimi, Chairman of FurnishIQ",
    ),
    "ar": dict(
        label="كلمة رئيس مجلس الإدارة",
        quote=["في", "فيرنيش", "آي", "كيو،", "نؤمن", "بأن", "المساحات", "الاستثنائية", "تبدأ", "بفهم", "عميق", "لتطلعات", "عملائنا.",
               "نحن", "لا", "نكتفي", "بالتصميم،", "*بل", "*نبني", "*الثقة", "*ونخلق", "*قيمة", "*دائمة."],
        name="عادل بن علي التميمي", role="رئيس مجلس الإدارة، فيرنيش آي كيو",
        alt="عادل بن علي التميمي، رئيس مجلس إدارة فيرنيش آي كيو",
    ),
}


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    words = " ".join(
        f'<span class="ch-w{" ch-hl" if w.startswith("*") else ""}">{w.lstrip("*")}</span>' for w in c["quote"])
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ MESSAGE FROM CEO ━━━━━ -->
<section id="chairman" data-chair{' dir="rtl"' if ar else ''} style="position:relative;background:#F5F2ED;padding:clamp(64px,8vw,100px) clamp(24px,5vw,80px);overflow:hidden;">
  <style>
    #chairman .ch-grid{{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(48px,7vw,128px);align-items:center;}}
    #chairman .ch-portrait{{position:relative;justify-self:center;width:min(100%,460px);aspect-ratio:800/1096;}}
    #chairman .ch-outline{{position:absolute;inset:0;transform:translate({'-22px' if ar else '22px'},22px);border:1px solid rgba(139,107,74,0.5);border-radius:1000px 1000px 0 0;opacity:0;transition:opacity 1s {EASE} 0.9s,transform 1.2s {EASE} 0.9s;}}
    #chairman .ch-arch{{position:absolute;inset:0;overflow:hidden;border-radius:1000px 1000px 0 0;background:#E5DCD0;clip-path:inset(100% 0 0 0);transition:clip-path 1.4s {EASE} 0.2s;}}
    #chairman .ch-arch img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 20%;transform:scale(1.1);transition:transform 2.4s {EASE} 0.2s;}}
    #chairman.is-in .ch-arch{{clip-path:inset(0 0 0 0);}}
    #chairman.is-in .ch-arch img{{transform:scale(1);}}
    #chairman.is-in .ch-outline{{opacity:1;transform:translate({'-14px' if ar else '14px'},14px);}}
    #chairman .ch-label{{display:flex;align-items:center;gap:16px;margin-bottom:clamp(28px,3vw,44px);font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    #chairman .ch-label i{{display:block;width:32px;height:1px;background:#8B6B4A;}}
    #chairman .ch-mark{{display:block;font-family:'Lama Sans',sans-serif;font-size:clamp(96px,10vw,160px);line-height:0.6;height:0.42em;color:#D6C2A8;margin-bottom:clamp(8px,1vw,16px);{'transform:scaleX(-1);' if ar else ''}}}
    #chairman .ch-q{{font-family:{font};font-size:clamp(26px,2.7vw,44px);font-weight:500;line-height:{'1.6' if ar else '1.3'};letter-spacing:{'normal' if ar else '-0.015em'};margin:0;}}
    #chairman .ch-w{{color:rgba(31,31,31,0.14);transition:color 0.4s {EASE};}}
    #chairman .ch-w.is-on{{color:#1F1F1F;}}
    #chairman .ch-w.ch-hl.is-on{{color:#8B6B4A;}}
    #chairman .ch-sign{{display:flex;align-items:center;gap:20px;margin-top:clamp(36px,4vw,56px);}}
    #chairman .ch-sign i{{display:block;width:56px;height:1px;background:#3A2D25;transform:scaleX(0);transform-origin:{'right' if ar else 'left'};transition:transform 1s {EASE} 0.6s;}}
    #chairman.is-signed .ch-sign i{{transform:scaleX(1);}}
    #chairman .ch-name{{font-family:{font};font-size:clamp(18px,1.5vw,22px);font-weight:500;color:#1F1F1F;}}
    #chairman .ch-role{{display:block;margin-top:6px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#8B6B4A;}}
    #chairman .ch-sign div{{opacity:0;transform:translateY(10px);transition:opacity 0.8s {EASE} 0.9s,transform 0.8s {EASE} 0.9s;}}
    #chairman.is-signed .ch-sign div{{opacity:1;transform:none;}}
    @media(max-width:900px){{
      #chairman .ch-grid{{grid-template-columns:1fr;}}
      #chairman .ch-portrait{{width:min(78%,360px);}}
    }}
    @media(prefers-reduced-motion:reduce){{
      #chairman *{{transition:none!important;}}
    }}
  </style>
  <div class="ch-grid">
    <div class="ch-portrait">
      <span class="ch-outline" aria-hidden="true"></span>
      <div class="ch-arch"><img src="assets/ceo-photo.webp" alt="{c['alt']}" width="800" height="1096" loading="lazy" decoding="async"></div>
    </div>
    <div>
      <div class="ch-label"><i></i>{c['label']}</div>
      <span class="ch-mark" aria-hidden="true">&ldquo;</span>
      <blockquote class="ch-q" style="margin:0;">{words}</blockquote>
      <div class="ch-sign"><i></i><div><span class="ch-name">{c['name']}</span><span class="ch-role">{c['role']}</span></div></div>
    </div>
  </div>
</section>
"""


JS = """    // ── CHAIRMAN: ARCH PORTRAIT, QUOTE READS ITSELF ON SCROLL ────────────────
    {
      const ch = document.querySelector('[data-chair]');
      if (ch) {
        const words = [...ch.querySelectorAll('.ch-w')];
        const q = ch.querySelector('.ch-q');
        let ticking = false;
        const update = () => {
          ticking = false;
          const r = q.getBoundingClientRect(), vh = window.innerHeight;
          // words light up from when the quote enters until its last line sits at 75% of the viewport
          const p = reduced ? 1 : Math.min(Math.max((vh * 0.92 - r.top) / (vh * 0.12 + r.height * 0.8), 0), 1);
          const n = Math.round(p * words.length);
          words.forEach((w, i) => w.classList.toggle('is-on', i < n));
          ch.classList.toggle('is-signed', n >= words.length);
        };
        const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { ch.classList.add('is-in'); io.disconnect(); } }, { threshold: 0.25 });
        io.observe(ch);
        if (reduced) ch.classList.add('is-in');
        update();
        window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
        window.addEventListener('resize', update);
      }
    }

"""
MARK = "    // ── FADE-IN ON LOAD (lazy images)"

for path, lang in [("about-us.dc.html", "en"), ("about-us.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ MESSAGE FROM CEO ━+ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── CHAIRMAN: ARCH PORTRAIT"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

import re

EASE = "cubic-bezier(0.25,0.46,0.45,0.94)"
IMG = "desert-stone-resort-arrival-court"
C = {
    "en": dict(
        label="Begin Your Project", h2="Ready to Visualise Your Space?",
        body="Receive a clear plan, photoreal visuals, and a comprehensive budget roadmap tailored to your brief.",
        cta1="Book a Consultation", cta2="Discover Projects", pre="",
        cap="Concept visualisation", alt="Stone arrival court leading to a timber entrance at dusk",
        studio="Visit Our Studio", hq="Headquarters", city="Riyadh, Kingdom of Saudi Arabia", local="Local time",
        phone="Phone", email="Email", wa="WhatsApp", wa_txt="Message the studio",
    ),
    "ar": dict(
        label="ابدأ مشروعك", h2="هل أنت مستعد لتصور مساحتك؟",
        body="احصل على خطة واضحة، وتصورات بصرية واقعية، وخارطة طريق مالية شاملة مصممة خصيصاً لمتطلباتك.",
        cta1="احجز استشارة", cta2="اكتشف مشاريعنا", pre="/ar",
        cap="تصور مفاهيمي", alt="ممر حجري يقود إلى مدخل خشبي عند الغروب",
        studio="زُر استوديونا", hq="المقر الرئيسي", city="الرياض، المملكة العربية السعودية", local="التوقيت المحلي",
        phone="الهاتف", email="البريد الإلكتروني", wa="واتساب", wa_txt="راسل الاستوديو",
    ),
}
ARROW_EN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
ARROW_AR = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 5 5 12 12 19"/></svg>'


def build(lang):
    ar = lang == "ar"
    c = C[lang]
    font = "'GE SS Two','Arial',sans-serif" if ar else "'Lama Sans',sans-serif"
    track = "normal" if ar else "0.3em"
    small = "12px" if ar else "9px"
    btn_track = "normal" if ar else "0.2em"
    btn_size = "13px" if ar else "10px"
    arrow = ARROW_AR if ar else ARROW_EN
    srcset = ", ".join(f"uploads/{IMG}-{w}.webp {w}w" for w in (1280, 1920, 2752))
    return f"""<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ STUDIO / CONTACT ━ -->
<section id="threshold" data-threshold{' dir="rtl"' if ar else ''} style="position:relative;background:#1E1610;color:#F5F2ED;padding:clamp(64px,8vw,100px) clamp(24px,5vw,80px);overflow:clip;">
  <style>
    #threshold .th-wrap{{max-width:1280px;margin:0 auto;}}
    #threshold .th-label{{display:flex;align-items:center;justify-content:center;gap:16px;margin-bottom:clamp(28px,3.4vw,44px);font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#D6C2A8;}}
    #threshold .th-label i{{display:block;width:32px;height:1px;background:#D6C2A8;}}
    #threshold .th-stage{{position:relative;height:clamp(520px,80vh,780px);}}
    #threshold .th-ghost{{position:absolute;left:50%;top:0;bottom:0;width:var(--w0);transform:translateX(-50%);border:1px solid rgba(214,194,168,0.45);border-bottom:none;border-radius:999px 999px 0 0;opacity:calc(1 - var(--e,0) * 1.4);pointer-events:none;}}
    #threshold .th-door{{position:absolute;left:50%;top:0;bottom:0;width:var(--w,36%);transform:translateX(-50%);overflow:hidden;border-radius:var(--r,999px) var(--r,999px) 0 0;background:#3A2D25;}}
    #threshold .th-door img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 60%;transform:scale(calc(1.18 - 0.18 * var(--e,0)));}}
    #threshold .th-tint{{position:absolute;inset:0;background:rgba(30,22,16,calc(0.18 + 0.4 * var(--e,0)));}}
    #threshold .th-copy{{position:absolute;left:0;right:0;bottom:0;padding:clamp(28px,4vw,64px);display:flex;flex-direction:column;align-items:center;text-align:center;opacity:0;transform:translateY(20px);transition:opacity 0.8s {EASE},transform 0.8s {EASE};pointer-events:none;}}
    #threshold.is-open .th-copy{{opacity:1;transform:none;pointer-events:auto;}}
    #threshold .th-h2{{font-family:{font};font-size:clamp(32px,4.4vw,72px);font-weight:500;line-height:{'1.35' if ar else '1.05'};letter-spacing:{'normal' if ar else '-0.03em'};color:#FFFFFF;margin:0;max-width:1000px;text-wrap:balance;}}
    #threshold .th-body{{font-family:{font};font-size:{'17px' if ar else '16px'};line-height:1.75;color:rgba(245,242,237,0.82);margin:clamp(16px,1.6vw,22px) 0 0;max-width:560px;}}
    #threshold .th-ctas{{display:inline-grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:clamp(24px,2.6vw,36px);}}
    #threshold .th-btn{{display:flex;align-items:center;justify-content:center;white-space:nowrap;gap:12px;padding:16px 30px;font-family:{font};font-size:{btn_size};letter-spacing:{btn_track};text-transform:uppercase;text-decoration:none;transition:background 0.4s {EASE},color 0.4s {EASE},border-color 0.4s {EASE},gap 0.4s {EASE};}}
    #threshold .th-btn--solid{{background:#D6C2A8;color:#3A2D25;border:1px solid #D6C2A8;}}
    #threshold .th-btn--solid:hover,#threshold .th-btn--solid:focus-visible{{background:#F5F2ED;border-color:#F5F2ED;gap:18px;}}
    #threshold .th-btn--line{{color:#F5F2ED;border:1px solid rgba(245,242,237,0.55);}}
    #threshold .th-btn--line:hover,#threshold .th-btn--line:focus-visible{{background:#F5F2ED;border-color:#F5F2ED;color:#3A2D25;}}
    #threshold .th-cap{{position:absolute;top:clamp(18px,2vw,28px);inset-inline-end:clamp(18px,2vw,28px);font-family:{font};font-size:{'12px' if ar else '10px'};letter-spacing:{'normal' if ar else '0.18em'};text-transform:uppercase;color:rgba(245,242,237,0.75);opacity:var(--e,0);}}
    #threshold .th-info{{--gap:clamp(28px,3.6vw,56px);display:grid;grid-template-columns:minmax(0,1.3fr) repeat(3,minmax(0,1fr));column-gap:var(--gap);row-gap:clamp(28px,4vw,40px);margin-top:clamp(40px,4.4vw,64px);padding-top:clamp(26px,2.6vw,36px);border-top:1px solid rgba(214,194,168,0.2);}}
    #threshold .th-cell{{position:relative;min-width:0;text-decoration:none;color:inherit;}}
    #threshold .th-cell+.th-cell::before{{content:"";position:absolute;top:0;bottom:0;inset-inline-start:calc(var(--gap) / -2);width:1px;background:rgba(214,194,168,0.14);}}
    #threshold .th-k{{display:block;margin-bottom:12px;font-family:{font};font-size:{small};letter-spacing:{track};text-transform:uppercase;color:#D6C2A8;}}
    #threshold .th-v{{display:block;font-family:{font};font-size:clamp(15px,1.25vw,18px);line-height:1.5;color:#F5F2ED;transition:color 0.4s {EASE};}}
    #threshold .th-s{{display:block;margin-top:6px;font-family:{font};font-size:{'13px' if ar else '12px'};color:rgba(245,242,237,0.55);}}
    #threshold a.th-cell:hover .th-v,#threshold a.th-cell:focus-visible .th-v{{color:#D6C2A8;}}
    @media(max-width:900px){{
      #threshold .th-stage{{height:clamp(520px,82vh,680px);}}
      #threshold .th-info{{grid-template-columns:repeat(2,minmax(0,1fr));}}
      #threshold .th-cell:nth-child(3)::before{{display:none;}}
      #threshold .th-btn{{padding:15px 22px;}}
    }}
    @media(max-width:600px){{
      #threshold .th-copy{{align-items:stretch;}}
      #threshold .th-ctas{{display:grid;grid-template-columns:1fr;width:100%;}}
    }}
    @media(prefers-reduced-motion:reduce){{
      #threshold *{{transition:none!important;}}
    }}
  </style>
  <div class="th-wrap">
    <div class="th-label"><i></i>{c['label']}<i></i></div>
    <div class="th-stage" data-th-stage>
      <span class="th-ghost" aria-hidden="true"></span>
      <div class="th-door">
        <img src="uploads/{IMG}-1920.webp" srcset="{srcset}" sizes="100vw" alt="{c['alt']}" width="1920" height="1071" loading="lazy" decoding="async">
        <span class="th-tint" aria-hidden="true"></span>
        <span class="th-cap" aria-hidden="true">{c['cap']}</span>
        <div class="th-copy">
          <h2 class="th-h2">{c['h2']}</h2>
          <p class="th-body">{c['body']}</p>
          <div class="th-ctas">
            <a class="th-btn th-btn--solid" href="{c['pre']}/contact">{c['cta1']}{arrow}</a>
            <a class="th-btn th-btn--line" href="{c['pre']}/projects">{c['cta2']}</a>
          </div>
        </div>
      </div>
    </div>
    <div class="th-info" aria-label="{c['studio']}">
      <div class="th-cell"><span class="th-k">{c['hq']}</span><span class="th-v">{c['city']}</span><span class="th-s">{c['local']} <span dir="ltr" data-th-time>--:--</span></span></div>
      <a class="th-cell" href="tel:+966580330627"><span class="th-k">{c['phone']}</span><span class="th-v" dir="ltr">+966 58 033 0627</span></a>
      <a class="th-cell" href="mailto:info@furnishiq.net"><span class="th-k">{c['email']}</span><span class="th-v" dir="ltr">info@furnishiq.net</span></a>
      <a class="th-cell" href="https://wa.me/966580330627" target="_blank" rel="noopener"><span class="th-k">{c['wa']}</span><span class="th-v">{c['wa_txt']}</span></a>
    </div>
  </div>
</section>
"""


JS = """    // ── THRESHOLD: THE DOORWAY OPENS INTO THE SPACE ON SCROLL ────────────────
    {
      const th = document.querySelector('[data-threshold]');
      if (th) {
        const stage = th.querySelector('[data-th-stage]'), clock = th.querySelector('[data-th-time]');
        let ticking = false;
        const update = () => {
          ticking = false;
          const r = stage.getBoundingClientRect(), vh = window.innerHeight, W = stage.offsetWidth;
          const p = reduced ? 1 : Math.min(Math.max((vh - r.top) / (vh * 0.85), 0), 1);
          const e = p * p * (3 - 2 * p);
          const w0 = Math.min(W, Math.max(200, W * 0.34));
          const w = w0 + (W - w0) * e;
          th.style.setProperty('--w0', w0.toFixed(1) + 'px');
          th.style.setProperty('--w', w.toFixed(1) + 'px');
          th.style.setProperty('--r', ((w / 2) * (1 - e)).toFixed(1) + 'px');
          th.style.setProperty('--e', e.toFixed(4));
          th.classList.toggle('is-open', e > 0.82);
        };
        update();
        window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
        window.addEventListener('resize', update);
        // live Riyadh time beside the headquarters
        if (clock) {
          const fmt = new Intl.DateTimeFormat('en-GB', { timeZone: 'Asia/Riyadh', hour: '2-digit', minute: '2-digit' });
          const tick = () => { clock.textContent = fmt.format(new Date()); };
          tick(); setInterval(tick, 30000);
        }
      }
    }

"""
MARK = "    // ── FADE-IN ON LOAD (lazy images)"

for path, lang in [("about-us.dc.html", "en"), ("about-us.ar.dc.html", "ar")]:
    s = open(path, encoding="utf-8").read()
    s, n = re.subn(r"<!-- ━+ STUDIO / CONTACT ━ -->\n<section.*?\n</section>\n", lambda m: build(lang), s, count=1, flags=re.S)
    assert n == 1, path
    old = "    // ── THRESHOLD: THE DOORWAY"
    if old in s:
        a = s.index(old); b = s.index(chr(10) + "    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, path
    s = s.replace(MARK, JS + MARK)
    open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "ok")

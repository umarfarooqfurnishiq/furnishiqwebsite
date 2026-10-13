"""Arabic contact page: the same design as contact_layout.py, mirrored for right to left.

The letter, the studio's clock and card, the staircase of next steps, and the visit over the live map, with Arabic
copy (the letter itself is written by contact-letter.js, which reads <html lang>). Right to left: the grid places the
intro on the right; the mashrabiya photograph is the mirrored -rtl file, anchored right; the staircase climbs from
right to left; the map's pin sits in the left half, beside the glass panel on the right; arrows turn to face the
reading direction. Arabic text is set in GE SS Two with no letter-spacing; addresses and numbers run left to right.
Run from Furnishiq.net: PYTHONIOENCODING=utf-8 python ../scripts/site/contact_layout_ar.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contact_layout as C

AR_CSS = """    /* ── Arabic, right to left ── */
    .ct *,.cd *,.cn *,.cv *{font-family:'GE SS Two','Arial',sans-serif!important;letter-spacing:normal!important;text-transform:none!important;}
    /* what is Latin by nature (addresses, phone numbers, the dialling code) keeps the Latin face and its digits */
    .ct .lt-phone,.ct .lt-phone *,.ct .lt-input[data-key="email"],.cd .cd-v b[dir="ltr"],.ct .lt-input[data-key="size"]{font-family:'Lama Sans',sans-serif!important;}
    /* the stair's outlined numerals are drawn, not read: they keep the Latin face, as on the English page */
    .cn .cn-n{font-family:'Lama Sans',sans-serif!important;letter-spacing:-0.04em!important;}
    .lt-p{line-height:1.95;}
    .lw-bg img{left:auto;right:-2%;object-position:right 40%;animation-name:lw-drift-rtl;}
    @keyframes lw-drift-rtl{from{transform:translate3d(0,0,0);}to{transform:translate3d(2%,1.2%,0);}}
    .lt-send svg,.lt-wa svg,.lt-done svg,.vs-cta svg,.cd-act svg,.cv-link svg{transform:scaleX(-1);}
    .ck-ruler em{left:auto;right:37.5%;}
    .ck-scale span{transform:translateX(50%);}
    .ck-scale span:first-child{transform:none;}
    .ck-scale span:last-child{transform:translateX(100%);}
    .cv-map-bg iframe{left:auto;right:0;}
    .cn-node{left:auto;right:0;}
    @media(min-width:961px){
      .lt-note{text-align:left;}
      .cn-step:first-child::before{left:-16px;right:0;}
      .cn-step:last-child::before{left:0;right:-16px;}
      .cn-step + .cn-step::after{left:auto;right:-16px;}
    }
    @media(max-width:960px){
      .lt-note{text-align:right;}
      .cv-map-bg iframe{right:auto;left:0;}
    }
"""
CSS = C.CSS.replace("  </style>\n", AR_CSS + "  </style>\n")
assert CSS != C.CSS
reveal, ARROW_UR, MAP_CID = C.reveal, C.ARROW_UR, C.MAP_CID


def build():
    h = []
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ HERO ━━ -->')
    h.append('<!-- The letter: the blanks are the form (contact-letter.js fills #letter-root, in Arabic) -->')
    h.append('<section id="form" data-screen-label="Contact" class="ct lw-sec" data-contact-hero>')
    h.append(CSS)
    h.append('  <div class="lw-bg" aria-hidden="true"><img src="uploads/mashrabiya-light-limewash-wall-texture-rtl-1920.webp" alt="" fetchpriority="high" decoding="async"></div>')
    h.append('  <div class="ct-wrap lw">')
    h.append('    <div class="lw-intro">')
    h.append('      <div class="c-label ct-in" style="--d:0.05s;"><i></i>تواصل مع FurnishIQ</div>')
    h.append('      <h1 class="lw-h1 ct-in" style="--d:0.12s;">اكتب إلى <span>الاستوديو.</span></h1>')
    h.append('      <p class="lw-status ct-in" id="letter-status" style="--d:0.2s;">يرد عليك استشاري أول خلال يوم عمل واحد.</p>')
    h.append('      <p class="lw-how ct-in" style="--d:0.28s;">اضغط على أي فراغ لتختار، واكتب حيث يُطلب منك، ثم أرسل الرسالة كما هي. لا شيء آخر لتعبئته.</p>')
    h.append('    </div>')
    h.append('    <div id="letter-root" class="lw-letter ct-in" style="--d:0.3s;"></div>')
    h.append('  </div>')
    h.append('</section>')
    h.append('')
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━━━━ DIRECT LINES ━━━━━━━━━━━━ -->')
    h.append('<!-- The studio, right now: its clock in Riyadh (contact-letter.js fills #direct-clock), and its card -->')
    h.append('<section data-screen-label="Direct" class="cd">')
    h.append('  <div class="cd-wrap">')
    h.append('    <div class="cd-clock">')
    h.append('      <div class="c-label rv"%s><i></i>تفضّل التواصل المباشر؟</div>' % reveal())
    h.append('      <h2 class="cd-h2 rv"%s>الاستوديو، <span>الآن.</span></h2>' % reveal("0.08"))
    h.append('      <div id="direct-clock" class="ck rv"%s><p class="ck-state">من الأحد إلى الخميس، من 9:00 إلى 18:00 بتوقيت الرياض.</p></div>' % reveal("0.14"))
    h.append('    </div>')
    h.append('    <div class="cd-card rv"%s>' % reveal("0.12"))
    h.append('      <div class="cd-card-head"><img src="assets/logo-default.png" width="264" height="90" alt="FurnishIQ" loading="lazy"><span>الاستوديو · الرياض</span></div>')
    h.append('      <ul class="cd-lines">')
    h.append('        <li class="cd-line"><small>البريد الإلكتروني</small><a class="cd-v" href="mailto:info@furnishiq.net"><b dir="ltr">info@furnishiq.net</b><em>الملخصات والمخططات وطلبات العروض</em></a><button type="button" class="cd-act" data-copy="info@furnishiq.net">نسخ</button></li>')
    h.append('        <li class="cd-line"><small>الهاتف</small><a class="cd-v" href="tel:+966580330627"><b dir="ltr">+966 58 033 0627</b><em>إبراهيم العلي، المشاريع</em></a><a class="cd-act" href="tel:+966580330627">اتصال %s</a></li>' % ARROW_UR)
    h.append('        <li class="cd-line"><small>واتساب</small><a class="cd-v" href="https://wa.me/966580330627" target="_blank" rel="noopener" id="id-contact-wa"><b>راسلنا مباشرة</b><em>أسرع رد أولي</em></a><a class="cd-act" href="https://wa.me/966580330627" target="_blank" rel="noopener">فتح %s</a></li>' % ARROW_UR)
    h.append('      </ul>')
    h.append('      <div class="cd-card-foot"><span>التغطية <b>جميع مناطق المملكة العربية السعودية</b></span><span>اللغات <b>العربية والإنجليزية</b></span></div>')
    h.append('    </div>')
    h.append('  </div>')
    h.append('</section>')
    h.append('')
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━━━━ WHAT HAPPENS NEXT ━━━━━━━ -->')
    h.append('<!-- A staircase in section, climbing from right to left: each step treads and rises, from the first conversation to the proposal -->')
    h.append('<section data-screen-label="Next Steps" class="cn">')
    h.append('  <div class="cn-wrap">')
    h.append('    <div class="cn-head">')
    h.append('      <div><div class="c-label rv"%s><i></i>بعد تواصلك معنا</div><h2 class="cn-h2 rv"%s>ماذا يحدث بعد ذلك.</h2></div>' % (reveal(), reveal("0.08")))
    h.append('      <p class="cn-note rv"%s>دون أي التزام في أي خطوة: يأتي العرض قبل أي التزام.</p>' % reveal("0.12"))
    h.append('    </div>')
    h.append('    <ol class="cn-steps">')
    steps = [
        ("01", "نستمع", "خلال يوم عمل واحد", "يراجع استشاري أول، وليس مركز اتصال، طلبك ويحدد موعداً لمحادثة استكشافية في الوقت الذي يناسبك.",
         "executive-floors-client-majlis-1280.webp", "مجلس مهيأ لحوار"),
        ("02", "نزور", "الموقع والنطاق", "نعاين المساحة، ونفهم كيف ستستخدمها، ونتفق على الطموح والقيود والجدول الزمني، وجهاً لوجه كلما أمكن.",
         "fitout-pillar-brand-led-planning-site-plan-1280.webp", "موقع قيد المعاينة ومخططه مثبت على عمود"),
        ("03", "نقترح", "الخطة وخارطة الطريق", "تحصل على عرض واضح: النطاق، والتوجه البصري الواقعي، وخارطة طريق مالية شاملة، قبل الالتزام بأي شيء.",
         "interior-design-pillar-visual-certainty-render-review-1280.webp", "عميل ومصمم يراجعان تصوراً ثلاثي الأبعاد"),
    ]
    for k, (n, t, tag, p, img, alt) in enumerate(steps):
        h.append('      <li class="cn-step rv"%s>' % reveal("%.2f" % (0.12 * k) if k else None))
        h.append('        <span class="cn-node" aria-hidden="true"></span>')
        h.append('        <div class="cn-meta"><span class="cn-n">%s</span><span class="cn-tag">%s</span></div>' % (n, tag))
        h.append('        <div class="cn-frame"><img src="uploads/%s" alt="%s" loading="lazy" decoding="async"></div>' % (img, alt))
        h.append('        <h3>%s</h3>' % t)
        h.append('        <p>%s</p>' % p)
        h.append('      </li>')
    h.append('    </ol>')
    h.append('  </div>')
    h.append('</section>')
    h.append('')
    h.append('<!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ VISIT ━━━━━━━━━━━━━━━ -->')
    h.append('<section data-screen-label="Visit" class="cv">')
    h.append('  <div class="cv-map-bg"><iframe src="https://www.google.com/maps?cid=%s&amp;z=16&amp;hl=ar&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="استوديو FurnishIQ على خرائط Google"></iframe></div>' % MAP_CID)
    h.append('  <div class="cv-wrap">')
    h.append('    <div class="cv-text rv"%s>' % reveal())
    h.append('      <div class="c-label"><i></i>زر الاستوديو</div>')
    h.append('      <h2 class="cv-h2">شاهد المواد. <span>المس التشطيبات.</span></h2>')
    h.append('      <p class="cv-p">بعض القرارات تستحق أن تُتخذ حضورياً. احجز جلسة في الاستوديو لاستكشاف مكتبات المواد، وعينات التشطيبات، وأعمال المشاريع السابقة.</p>')
    h.append('      <div class="cv-facts"><div><small>العنوان</small><span>التخصصي، الرياض</span></div><div><small>بموعد مسبق</small><span>الأحد – الخميس · <span dir="ltr">9:00 – 18:00</span></span></div></div>')
    h.append('      <div id="visit-root"></div>')
    h.append('      <div class="cv-maplink"><span class="cv-cap">الاستوديو محدد على الخريطة</span><a href="https://www.google.com/maps?cid=%s&amp;hl=ar" target="_blank" rel="noopener" class="cv-link">افتح في خرائط Google %s</a></div>' % (MAP_CID, ARROW_UR))
    h.append('    </div>')
    h.append('  </div>')
    h.append('</section>')
    h.append('')
    return "\n".join(h) + "\n"


if __name__ == "__main__":
    C.PAGE = "contact.ar.dc.html"
    C.build = build
    C.main()

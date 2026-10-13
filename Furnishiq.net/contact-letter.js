// Contact page (English and Arabic): the letter, the studio's clock, and the studio-visit request.
// FIQLetter fills #letter-root with a letter to the studio whose blanks are the form: choices open a small menu in
// place, text blanks are inputs set inside the sentence, and the "feel" line takes up to three material swatches.
// It sends the letter as written (POST /api/send-email, formType "contact") or opens WhatsApp with it.
// FIQDirect fills #direct-clock with Riyadh time, open or closed, the working week and a 24-hour ruler.
// FIQVisit fills #visit-root with the next five working days and three times of day, read in Riyadh time, and turns
// the choice into a visit request by WhatsApp or email (a request, not a booking).
// The words come from T, chosen by <html lang>: the Arabic letter is written as Arabic sentences, not translated word
// for word; the email's service and budget fields stay in English (the same values from both pages).
// The page calls the three from its componentDidMount; if this file loads after that render, the page leaves
// FIQLetterPending / FIQDirectPending / FIQVisitPending and they start from here.
(function () {
  if (window.FIQLetter) return;

  var AR = (document.documentElement.lang || '').slice(0, 2) === 'ar';
  var WA_NUMBER = '966580330627';
  var EMAIL = 'info@furnishiq.net';
  var STORE = 'fiq-letter-v1';     // shared by both pages: the options are the same, in the same order
  var WORKDAYS = [0, 1, 2, 3, 4], OPEN = 9, CLOSE = 18;   // Sunday to Thursday, 9:00 to 18:00, Riyadh
  var LOCALE = AR ? 'ar-u-ca-gregory-nu-latn' : 'en-GB';  // the Arabic site: Gregorian dates, Western digits
  var MATERIAL_FILES = ['services-material-swatch-walnut.webp', 'contact-material-oak.webp', 'services-material-swatch-stone.webp',
    'contact-material-limestone.webp', 'services-material-swatch-boucle.webp', 'contact-material-leather.webp',
    'contact-material-onyx.webp', 'contact-material-terracotta.webp', 'contact-material-earth.webp'];
  // what the email's fields say, whichever page sent it
  var FIELD = {
    type: ['Villa', 'Residence', 'Office', 'Retail', 'Restaurant / café', 'Hospitality', 'Commercial', 'Other'],
    help: ['Interior Design', 'Fit-Out', 'Engineering & MEP', 'Furniture', 'Full Turnkey'],
    budget: ['Under 250K', '250K – 1M', '1M – 5M', '5M+', 'Prefer to discuss'],
  };
  var CODES = ['+966', '+971', '+974', '+965', '+973', '+968', '+20', '+962', '+44', '+1'];
  var MAX_MATERIALS = 3;

  var T = AR ? {
    type: ['فيلا', 'مسكن عائلي', 'مكتب', 'متجر', 'مطعم أو مقهى', 'فندق أو منتجع', 'مساحة تجارية', 'من نوع آخر'],
    city: ['الرياض', 'جدة', 'المنطقة الشرقية', 'العُلا', 'مدينة سعودية أخرى', 'إحدى دول الخليج'],
    time: ['خلال ثلاثة أشهر', 'خلال ستة أشهر', 'خلال عام', 'بعد أكثر من عام', 'في الوقت المناسب'],
    help: ['التصميم الداخلي', 'التشطيبات', 'الأعمال الهندسية والكهروميكانيكية', 'الأثاث', 'المشروع كاملاً حتى التسليم'],
    budget: ['أقل من 250 ألف ريال', 'من 250 ألف ريال إلى مليون', 'من مليون إلى 5 ملايين ريال', 'أكثر من 5 ملايين ريال', 'لم تُحدَّد بعد'],
    materials: ['خشب الجوز', 'خشب البلوط', 'الترافرتين', 'الحجر الجيري', 'قماش البوكليه', 'الجلد', 'الأونيكس', 'التيراكوتا', 'الطين المدكوك'],
    placeholder: { type: 'نوع المساحة', city: 'المدينة', time: 'الموعد', help: 'ما تحتاجه', budget: 'النطاق', materials: 'ثلاث خامات' },
    hintMaterials: 'اختر حتى ثلاث خامات. سترافق رسالتك.', hintHelp: 'اختر كل ما ينطبق.', done: 'تم',
    to: 'إلى استوديو FurnishIQ، الرياض', salute: 'عزيزي فريق FurnishIQ،',
    // the sentences, with their blanks: {c: choice} {i: input} {phone: the phone pair}
    p1: ['أخطط لمشروع ', { c: 'type' }, ' في ', { c: 'city' }, '، بمساحة تقارب ', { i: 'size' }, ' م²، وأودّ أن يكتمل ', { c: 'time' }, '.'],
    p2: ['وأحتاج إلى مساعدتكم في ', { c: 'help' }, '، والميزانية التي أفكر فيها ', { c: 'budget' }, '.'],
    p3: ['وأودّ أن يحمل المكان إحساس ', { c: 'materials' }, '.'],
    p4: ['يمكنكم التواصل معي عبر ', { i: 'email' }, ' أو على الرقم ', { phone: true }, '.'],
    ps: 'ملاحظة:', notesPh: 'أي تفاصيل أخرى: الموقع، طراز تحبه، موعد مهم.',
    regards: 'مع خالص التحية،', namePh: 'اسمك', companyPh: 'الشركة (اختياري)',
    emailPh: 'بريدك الإلكتروني', sizeLabel: 'المساحة التقريبية بالمتر المربع', emailLabel: 'البريد الإلكتروني', phoneLabel: 'رقم الهاتف، اختياري',
    nameLabel: 'اسمك', companyLabel: 'الشركة، اختياري', codeLabel: 'رمز الدولة',
    send: 'أرسل الرسالة', sending: 'جارٍ الإرسال…', wa: 'أرسل عبر واتساب', fine: 'تبقى بياناتك لدى FurnishIQ فقط. لا نشاركها ولا نرسل رسائل مزعجة.',
    need: { type: 'نوع المساحة', city: 'المدينة', help: 'ما تحتاجه', email: 'بريداً إلكترونياً صحيحاً', name: 'اسمك' },
    almost: function (list) { return 'تبقّى القليل: يُرجى إضافة ' + list + '.'; },
    failed: 'حدث خطأ ما. يُرجى المحاولة مرة أخرى، أو الإرسال عبر واتساب، أو مراسلتنا على ' + EMAIL + '.',
    thanks: '/ar/thank-you?name=',
    join: function (list) { return list.join(' و'); },   // the Arabic "and" joins the next word
    text: function (S, v) {   // the letter as text, only what was filled in
      var L = ['عزيزي فريق FurnishIQ،', ''];
      var p1 = 'أخطط لمشروع' + (v.type ? ' ' + v.type : '') + (v.city ? ' في ' + v.city : '');
      if (v.size) p1 += '، بمساحة تقارب ' + v.size + ' م²';
      if (v.time) p1 += '، وأودّ أن يكتمل ' + v.time;
      L.push(p1 + '.');
      var p2 = v.help ? 'وأحتاج إلى مساعدتكم في ' + v.help : '';
      if (v.budget) p2 += (p2 ? '، والميزانية' : 'والميزانية') + ' التي أفكر فيها ' + v.budget;
      if (p2) L.push(p2 + '.');
      if (v.materials) L.push('وأودّ أن يحمل المكان إحساس ' + v.materials + '.');
      if (v.email && v.phone) L.push('يمكنكم التواصل معي عبر ' + v.email + ' أو على الرقم ' + v.phone + '.');
      else if (v.email) L.push('يمكنكم التواصل معي عبر ' + v.email + '.');
      else if (v.phone) L.push('يمكنكم التواصل معي على الرقم ' + v.phone + '.');
      if (v.notes) L.push('', 'ملاحظة: ' + v.notes);
      L.push('', 'مع خالص التحية،', (v.name || '—') + (v.company ? '، ' + v.company : ''));
      return L.join('\n');
    },
    open: function (c) { return 'الاستوديو مفتوح الآن · ' + c + ' بتوقيت الرياض. نرد خلال يوم عمل واحد.'; },
    closed: function (c, when) { return 'الاستوديو مغلق الآن · ' + c + ' بتوقيت الرياض. يفتح ' + when + ' الساعة 9:00، وستكون رسالتك أول ما نقرأ.'; },
    today: 'اليوم', tomorrow: 'غداً', sunday: 'يوم الأحد',
    clockLabel: 'بتوقيت الرياض', openNow: 'مفتوح الآن · يغلق الساعة ' + CLOSE + ':00',
    closedNow: function (when) { return 'مغلق الآن · يفتح ' + when + ' الساعة ' + OPEN + ':00'; },
    days: ['أحد', 'اثنين', 'ثلاثاء', 'أربعاء', 'خميس', 'جمعة', 'سبت'], dayOff: 'مغلق', weekLabel: 'أيام العمل: من الأحد إلى الخميس',
    copy: 'نسخ', copied: 'تم النسخ',
    slots: [['الصباح', 'في الصباح'], ['الظهيرة', 'وقت الظهيرة'], ['بعد الظهر', 'بعد الظهر']],
    pickDay: 'اختر يوماً', pickTime: 'ثم الوقت', chooseDay: 'اختر يوماً', chooseTime: 'اختر الوقت',
    request: function (when, slot) { return 'اطلب زيارة ' + when + '، ' + slot; },
    visitText: function (when, slot, range) { return 'مرحباً FurnishIQ، أودّ زيارة الاستوديو ' + when + ' ' + slot + ' (' + range + '). أرجو إعلامي إن كان الموعد مناسباً.'; },
    visitSubject: function (when) { return 'طلب زيارة الاستوديو: ' + when; },
    byMail: 'أو اطلبها بالبريد الإلكتروني', visitFine: 'طلب وليس حجزاً: يؤكّد الاستوديو الموعد معك.',
    dayLabel: 'اليوم', timeLabel: 'وقت اليوم',
  } : {
    type: ['a villa', 'a family residence', 'an office', 'a retail store', 'a restaurant or café', 'a hotel or resort', 'a commercial space', 'something else'],
    city: ['Riyadh', 'Jeddah', 'the Eastern Province', 'AlUla', 'another Saudi city', 'the wider GCC'],
    time: ['within three months', 'within six months', 'within a year', 'in more than a year', 'whenever the time is right'],
    help: ['the interior design', 'the fit-out', 'engineering and MEP', 'the furniture', 'everything, turnkey'],
    budget: ['under SAR 250,000', 'SAR 250,000 to 1 million', 'SAR 1 to 5 million', 'above SAR 5 million', 'still open'],
    materials: ['walnut', 'oak', 'travertine', 'limestone', 'bouclé', 'leather', 'onyx', 'terracotta', 'rammed earth'],
    placeholder: { type: 'a kind of space', city: 'a city', time: 'by a date', help: 'what you need', budget: 'a range', materials: 'three materials' },
    hintMaterials: 'Choose up to three. They travel with your letter.', hintHelp: 'Choose all that apply.', done: 'Done',
    to: 'To FurnishIQ Studio, Riyadh', salute: 'Dear FurnishIQ,',
    p1: ['I’m planning ', { c: 'type' }, ' in ', { c: 'city' }, ', about ', { i: 'size' }, ' m², and I’d like it ready ', { c: 'time' }, '.'],
    p2: ['I’d like your help with ', { c: 'help' }, ', and the budget I have in mind is ', { c: 'budget' }, '.'],
    p3: ['I’d like it to feel like ', { c: 'materials' }, '.'],
    p4: ['You can reach me at ', { i: 'email' }, ' or on ', { phone: true }, '.'],
    ps: 'P.S.', notesPh: 'anything else: the site, a style you love, a key date.',
    regards: 'Warm regards,', namePh: 'your name', companyPh: 'company (optional)',
    emailPh: 'your email', sizeLabel: 'Approximate area in square metres', emailLabel: 'Email address', phoneLabel: 'Phone number, optional',
    nameLabel: 'Your name', companyLabel: 'Company, optional', codeLabel: 'Country code',
    send: 'Send letter', sending: 'Sending…', wa: 'Send on WhatsApp', fine: 'Your details stay with FurnishIQ. Never shared, never spammed.',
    need: { type: 'the kind of space', city: 'the city', help: 'what you need', email: 'a valid email', name: 'your name' },
    almost: function (list) { return 'Almost there: please add ' + list + '.'; },
    failed: 'Something went wrong. Please try again, send it on WhatsApp, or email us at ' + EMAIL + '.',
    thanks: '/thank-you?name=',
    join: function (list) { return list.length < 2 ? (list[0] || '') : list.slice(0, -1).join(', ') + ' and ' + list[list.length - 1]; },
    text: function (S, v) {
      var L = ['Dear FurnishIQ,', ''];
      var p1 = 'I’m planning ' + (v.type || 'a project') + (v.city ? ' in ' + v.city : '');
      if (v.size) p1 += ', about ' + v.size + ' m²';
      if (v.time) p1 += ', and I’d like it ready ' + v.time;
      L.push(p1 + '.');
      var p2 = v.help ? 'I’d like your help with ' + v.help : '';
      if (v.budget) p2 += (p2 ? ', and the' : 'The') + ' budget I have in mind is ' + v.budget;
      if (p2) L.push(p2 + '.');
      if (v.materials) L.push('I’d like it to feel like ' + v.materials + '.');
      // only the ways of reaching the writer that were given (on WhatsApp the number comes with the message)
      if (v.email && v.phone) L.push('You can reach me at ' + v.email + ' or on ' + v.phone + '.');
      else if (v.email || v.phone) L.push('You can reach me ' + (v.email ? 'at ' + v.email : 'on ' + v.phone) + '.');
      if (v.notes) L.push('', 'P.S. ' + v.notes);
      L.push('', 'Warm regards,', (v.name || '—') + (v.company ? ', ' + v.company : ''));
      return L.join('\n');
    },
    open: function (c) { return 'The studio is open · ' + c + ' in Riyadh. Replies within one working day.'; },
    closed: function (c, when) { return 'The studio is closed · ' + c + ' in Riyadh. It opens ' + when + ' at 9:00, and your letter will be first in line.'; },
    today: 'today', tomorrow: 'tomorrow', sunday: 'on Sunday',
    clockLabel: 'Riyadh time', openNow: 'Open now · closes at ' + CLOSE + ':00',
    closedNow: function (when) { return 'Closed now · opens ' + when.replace(/^on /, '') + ' at ' + OPEN + ':00'; },
    days: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], dayOff: 'closed', weekLabel: 'Working days: Sunday to Thursday',
    copy: 'Copy', copied: 'Copied',
    slots: [['Morning', 'in the morning'], ['Midday', 'around midday'], ['Afternoon', 'in the afternoon']],
    pickDay: 'Choose a day', pickTime: 'And a time', chooseDay: 'Choose a day', chooseTime: 'Choose a time of day',
    request: function (when, slot) { return 'Request ' + when + ', ' + slot; },
    visitText: function (when, slot, range) { return 'Hello FurnishIQ, I would like to visit the studio on ' + when + ', ' + slot + ' (' + range + '). Please let me know if that suits.'; },
    visitSubject: function (when) { return 'Studio visit request: ' + when; },
    byMail: 'or request by email', visitFine: 'A request, not a booking: the studio confirms the time with you.',
    dayLabel: 'Day', timeLabel: 'Time of day',
  };

  var ARROW = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>';

  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      var v = attrs[k];
      if (k === 'text') n.textContent = v;
      else if (k === 'html') n.innerHTML = v;
      else if (k.slice(0, 2) === 'on') n.addEventListener(k.slice(2), v);
      else if (v !== null && v !== undefined && v !== false) n.setAttribute(k, v === true ? '' : v);
    });
    (kids || []).forEach(function (c) { if (c) n.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return n;
  }
  function push(o) { window.dataLayer = window.dataLayer || []; window.dataLayer.push(o); }
  function store(key, val) { try { if (val === undefined) return JSON.parse(sessionStorage.getItem(key) || 'null'); sessionStorage.setItem(key, JSON.stringify(val)); } catch (e) { return null; } }
  function fmtDate(d0, o) { return new Date(d0).toLocaleDateString(LOCALE, Object.assign({ timeZone: 'UTC' }, o)); }

  // ── Riyadh time ─────────────────────────────────────────
  function riyadh() {
    var parts = new Intl.DateTimeFormat('en-GB', { timeZone: 'Asia/Riyadh', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
    var g = function (t) { return +(parts.find(function (p) { return p.type === t; }) || {}).value; };
    var gs = function (t) { return (parts.find(function (p) { return p.type === t; }) || {}).value; };
    var day0 = Date.UTC(g('year'), g('month') - 1, g('day'));
    return { day0: day0, weekday: new Date(day0).getUTCDay(), h: g('hour') % 24, m: g('minute'), clock: gs('hour') + ':' + gs('minute') };
  }
  function isOpen(t) { return WORKDAYS.indexOf(t.weekday) > -1 && t.h >= OPEN && t.h < CLOSE; }
  function nextOpening(t) { return (WORKDAYS.indexOf(t.weekday) > -1 && t.h < OPEN) ? T.today : (t.weekday >= 4 ? T.sunday : T.tomorrow); }

  // ═════════════════════════════════════════ THE LETTER ══
  window.FIQLetter = function () {
    var root = document.getElementById('letter-root');
    if (!root || root.dataset.ready) return;
    root.dataset.ready = '1';
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var S = Object.assign({ type: null, city: null, size: '', time: null, help: [], budget: null, materials: [],
      email: '', code: '+966', phone: '', notes: '', name: '', company: '' }, store(STORE) || {});
    var fresh = !S.phone && S.code === '+966';
    function save() { store(STORE, S); }

    var status = document.getElementById('letter-status');
    function syncStatus() { if (!status) return; var t = riyadh(), o = isOpen(t); status.textContent = o ? T.open(t.clock) : T.closed(t.clock, nextOpening(t)); status.classList.toggle('is-open', o); }
    syncStatus(); setInterval(syncStatus, 30000);

    // ── blanks ──
    var blanks = {};          // key → the element that shows it
    var menu = null, menuFor = null;
    var LISTS = { type: T.type, city: T.city, time: T.time, help: T.help, budget: T.budget, materials: T.materials };

    function choiceLabel(key) {
      if (key === 'help' || key === 'materials') return T.join(S[key].map(function (i) { return LISTS[key][i]; }));
      return S[key] !== null ? LISTS[key][S[key]] : '';
    }
    function choice(key) {
      var b = el('button', { type: 'button', 'class': 'lt-blank', 'aria-haspopup': 'true', 'aria-expanded': 'false', 'data-key': key });
      b.addEventListener('click', function () { if (menuFor === key) closeMenu(); else openMenu(key, b); });
      blanks[key] = b;
      return b;
    }
    function input(key, attrs) {
      var i = el('input', Object.assign({ 'class': 'lt-input', 'data-key': key, spellcheck: 'false' }, attrs));
      i.value = S[key];
      i.addEventListener('input', function () { S[key] = i.value; i.classList.remove('is-missing'); fit(i); save(); });
      i.addEventListener('change', function () { if (i.value.trim()) push({ event: 'letter_field', field: key }); });
      blanks[key] = i;
      return i;
    }
    // an input as wide as what is written in it (or its placeholder), so it reads as part of the sentence
    var ruler = el('span', { 'class': 'lt-ruler', 'aria-hidden': 'true' });
    root.appendChild(ruler);
    function fit(i) {
      // measured in the field's own type (the signature is set larger than the body; on the Arabic page addresses and
      // numbers keep the Latin face): important, so no page-wide font rule can override the measurement
      var cs = getComputedStyle(i);
      ruler.style.setProperty('font', cs.font, 'important');
      ruler.style.setProperty('letter-spacing', cs.letterSpacing, 'important');
      ruler.textContent = i.value || i.placeholder || '';
      i.style.width = Math.ceil(ruler.getBoundingClientRect().width + 6) + 'px';
    }

    function paintChoice(key) {
      var b = blanks[key], txt = choiceLabel(key);
      b.innerHTML = '';
      b.classList.toggle('is-set', !!txt);
      if (key === 'materials' && S.materials.length) {
        var parts = S.materials.map(function (i) { return el('span', { 'class': 'lt-chip' }, [el('img', { src: 'uploads/' + MATERIAL_FILES[i], alt: '' }), T.materials[i]]); });
        parts.forEach(function (chip, k) {
          if (k) b.appendChild(document.createTextNode(AR ? ' و' : (k === parts.length - 1 ? ' and ' : ', ')));
          b.appendChild(chip);
        });
      } else b.textContent = txt || T.placeholder[key];
    }
    function paintAll() { ['type', 'city', 'time', 'help', 'budget', 'materials'].forEach(paintChoice); }

    // ── the menu that opens under a choice ──
    function closeMenu(refocus) {
      if (!menu) return;
      var key = menuFor;
      menu.remove(); menu = null; menuFor = null;
      blanks[key].setAttribute('aria-expanded', 'false');
      if (refocus) blanks[key].focus();
    }
    function openMenu(key, anchor) {
      closeMenu();
      menuFor = key;
      anchor.setAttribute('aria-expanded', 'true');
      var many = key === 'help' || key === 'materials';
      menu = el('div', { 'class': 'lt-menu' + (key === 'materials' ? ' is-swatches' : ''), role: 'group', 'aria-label': T.placeholder[key] });
      if (key === 'materials') menu.appendChild(el('p', { 'class': 'lt-menu-hint', text: T.hintMaterials }));
      if (key === 'help') menu.appendChild(el('p', { 'class': 'lt-menu-hint', text: T.hintHelp }));
      var opts = el('div', { 'class': 'lt-opts' });
      LISTS[key].forEach(function (label, i) {
        var on = many ? S[key].indexOf(i) > -1 : S[key] === i;
        var btn = el('button', { type: 'button', 'class': 'lt-opt', 'aria-pressed': on ? 'true' : 'false' });
        if (key === 'materials') btn.appendChild(el('span', { 'class': 'lt-sw' }, [el('img', { src: 'uploads/' + MATERIAL_FILES[i], alt: '' })]));
        btn.appendChild(el('span', { 'class': 'lt-opt-t', text: label }));
        btn.addEventListener('click', function () {
          if (many) {
            var at = S[key].indexOf(i);
            if (at > -1) S[key].splice(at, 1);
            else { if (key === 'materials' && S[key].length >= MAX_MATERIALS) S[key].shift(); S[key].push(i); }
            [].forEach.call(opts.children, function (b2, j) { b2.setAttribute('aria-pressed', S[key].indexOf(j) > -1 ? 'true' : 'false'); });
            anchor.classList.remove('is-missing');
            paintChoice(key); save();
          } else {
            S[key] = i; anchor.classList.remove('is-missing'); paintChoice(key); save();
            push({ event: 'letter_field', field: key });
            closeMenu(); nextBlank(key);
          }
        });
        opts.appendChild(btn);
      });
      menu.appendChild(opts);
      if (many) menu.appendChild(el('button', { type: 'button', 'class': 'lt-done', html: T.done + ARROW, onclick: function () {
        if (S[key].length) push({ event: 'letter_field', field: key });
        closeMenu(); nextBlank(key);
      } }));
      // under the blank, inside the letter, kept within its width; in Arabic it hangs from the blank's right edge
      var sheet = root.querySelector('.lt-sheet');
      sheet.appendChild(menu);
      var a = anchor.getBoundingClientRect(), s = sheet.getBoundingClientRect();
      var w = Math.min(menu.offsetWidth, s.width - 32);
      if (AR) menu.style.right = Math.max(16, Math.min(s.right - a.right, s.width - w - 16)) + 'px';
      else menu.style.left = Math.max(16, Math.min(a.left - s.left, s.width - w - 16)) + 'px';
      menu.style.top = (a.bottom - s.top + 10) + 'px';
      if (!reduced) requestAnimationFrame(function () { menu && menu.classList.add('is-in'); }); else menu.classList.add('is-in');
      var first = menu.querySelector('.lt-opt[aria-pressed="true"]') || menu.querySelector('.lt-opt');
      if (first) first.focus({ preventScroll: true });
    }
    document.addEventListener('click', function (e) {
      if (menu && !menu.contains(e.target) && !(blanks[menuFor] && blanks[menuFor].contains(e.target))) closeMenu();
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu) closeMenu(true); });

    // after a choice, the eye moves on: focus the next blank that is still open
    var ORDER = ['type', 'city', 'size', 'time', 'help', 'budget', 'materials', 'email', 'phone', 'name'];
    function filled(key) {
      if (key === 'help' || key === 'materials') return S[key].length > 0;
      if (['type', 'city', 'time', 'budget'].indexOf(key) > -1) return S[key] !== null;
      return !!String(S[key]).trim();
    }
    function nextBlank(from) {
      var k = ORDER.indexOf(from);
      for (var j = k + 1; j < ORDER.length; j++) if (!filled(ORDER[j])) { blanks[ORDER[j]].focus({ preventScroll: true }); return; }
    }

    // ── the letter ──
    var t = riyadh();
    var code = el('select', { 'class': 'lt-code', 'aria-label': T.codeLabel, onchange: function () { S.code = code.value; save(); } },
      CODES.map(function (c) { return el('option', { value: c, text: c }); }));
    code.value = S.code;
    var notes = el('textarea', { 'class': 'lt-notes', rows: '1', placeholder: T.notesPh, 'data-key': 'notes' });
    notes.value = S.notes;
    function growNotes() { notes.style.height = 'auto'; notes.style.height = notes.scrollHeight + 'px'; }
    notes.addEventListener('input', function () { S.notes = notes.value; growNotes(); save(); });
    blanks.notes = notes;
    var hp = el('input', { type: 'text', tabindex: '-1', autocomplete: 'off', id: 'id-hp-field' });

    // a sentence from its pieces; addresses and numbers run left to right inside the Arabic sentence
    var INPUTS = {
      size: function () { return input('size', { type: 'text', inputmode: 'numeric', placeholder: '600', 'aria-label': T.sizeLabel, maxlength: '7', dir: 'ltr' }); },
      email: function () { return input('email', { type: 'email', autocomplete: 'email', placeholder: T.emailPh, 'aria-label': T.emailLabel, dir: AR ? 'auto' : null }); },
    };
    function sentence(parts) {
      return el('p', { 'class': 'lt-p' }, parts.map(function (p) {
        if (typeof p === 'string') return p;
        if (p.c) return choice(p.c);
        if (p.i) return INPUTS[p.i]();
        return el('span', { 'class': 'lt-phone', dir: 'ltr' }, [code,
          input('phone', { type: 'tel', autocomplete: 'tel-national', placeholder: '5X XXX XXXX', 'aria-label': T.phoneLabel })]);
      }));
    }
    var sheet = el('div', { 'class': 'lt-sheet' }, [
      el('div', { 'class': 'lt-head' }, [el('span', { text: T.to }), el('span', { text: fmtDate(t.day0, { day: 'numeric', month: 'long', year: 'numeric' }) })]),
      el('p', { 'class': 'lt-p lt-salute', text: T.salute }),
      sentence(T.p1), sentence(T.p2), sentence(T.p3), sentence(T.p4),
      el('p', { 'class': 'lt-p lt-ps' }, [el('span', { 'class': 'lt-ps-k', text: T.ps }), notes]),
      el('div', { 'class': 'lt-hp', 'aria-hidden': 'true' }, [el('label', { 'for': 'id-hp-field', text: 'Leave this field empty' }), hp]),
    ]);
    root.appendChild(sheet);

    // the close of the letter: the signature, and beside it the two ways to send it
    var note = el('p', { 'class': 'lt-note', role: 'alert' });
    var sendBtn = el('button', { type: 'button', 'class': 'lt-send', id: 'id-submit-btn' }, [el('span', { id: 'id-submit-btn-label', text: T.send })]);
    sendBtn.insertAdjacentHTML('beforeend', ARROW);
    var wa = el('a', { 'class': 'lt-wa', href: '#', target: '_blank', rel: 'noopener', id: 'id-letter-wa' }, [T.wa]);
    wa.insertAdjacentHTML('beforeend', ARROW);
    sheet.insertBefore(el('div', { 'class': 'lt-end' }, [
      el('div', { 'class': 'lt-sign' }, [
        el('span', { 'class': 'lt-regards', text: T.regards }),
        input('name', { type: 'text', autocomplete: 'name', placeholder: T.namePh, 'aria-label': T.nameLabel, 'class': 'lt-input lt-name' }),
        el('span', { 'class': 'lt-company' }, [input('company', { type: 'text', autocomplete: 'organization', placeholder: T.companyPh, 'aria-label': T.companyLabel })]),
      ]),
      el('div', { 'class': 'lt-end-acts' }, [
        el('div', { 'class': 'lt-acts' }, [wa, sendBtn]),
        el('p', { 'class': 'lt-fine', text: T.fine }),
      ]),
    ]), sheet.querySelector('.lt-hp'));
    sheet.appendChild(note);

    paintAll();
    [].forEach.call(sheet.querySelectorAll('.lt-input'), fit);
    growNotes();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { [].forEach.call(sheet.querySelectorAll('.lt-input'), fit); });

    // ── the letter as text: only what was filled in ──
    function letterText() {
      return T.text(S, {
        type: S.type !== null ? T.type[S.type] : '', city: S.city !== null ? T.city[S.city] : '', size: String(S.size).trim(),
        time: S.time !== null ? T.time[S.time] : '', help: choiceLabel('help'), budget: S.budget !== null ? T.budget[S.budget] : '',
        materials: choiceLabel('materials'), email: S.email.trim(), phone: S.phone.trim() ? S.code + ' ' + S.phone.trim() : '',
        notes: S.notes.trim(), name: S.name.trim(), company: S.company.trim(),
      });
    }

    function missing() {
      var need = [];
      if (S.type === null) need.push('type');
      if (S.city === null) need.push('city');
      if (!S.help.length) need.push('help');
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(S.email.trim())) need.push('email');
      // sent by email, the email is what the reply goes to; the phone is welcome but optional
      if (!S.name.trim()) need.push('name');
      return need;
    }
    function flag(need) {
      need.forEach(function (k) { blanks[k].classList.add('is-missing'); });
      note.textContent = T.almost(T.join(need.map(function (k) { return T.need[k]; })));
      blanks[need[0]].focus();
    }

    sendBtn.addEventListener('click', function () {
      if (hp.value) return;   // a bot filled the hidden field: drop it quietly
      var need = missing();
      if (need.length) { flag(need); return; }
      note.textContent = '';
      sendBtn.disabled = true;
      document.getElementById('id-submit-btn-label').textContent = T.sending;
      var payload = {
        formType: 'contact', name: S.name.trim(), company: S.company.trim() || '—', email: S.email.trim(), phone: S.phone.trim() ? S.code + ' ' + S.phone.trim() : 'Not given',
        service: S.help.map(function (i) { return FIELD.help[i]; }).join(', ') || 'Not specified',
        budget: S.budget !== null ? FIELD.budget[S.budget] : 'Not specified',
        message: letterText(), honeypot: hp.value,
      };
      fetch('/api/send-email', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
        .then(function (r) {
          if (!r.ok) throw new Error('Network error');
          push({ event: 'generate_lead', form_name: 'contact', service: payload.service, project_type: S.type !== null ? FIELD.type[S.type] : 'Not specified' });
          try { sessionStorage.removeItem(STORE); } catch (e) {}
          window.location.href = T.thanks + encodeURIComponent(payload.name);
        })
        .catch(function () {
          sendBtn.disabled = false;
          document.getElementById('id-submit-btn-label').textContent = T.send;
          note.textContent = T.failed;
        });
    });

    // the WhatsApp link always carries the letter as it stands (so the site-wide whatsapp_click sees a wa.me link)
    function syncWa() { wa.href = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(letterText()); }
    root.addEventListener('input', syncWa);
    root.addEventListener('click', function () { setTimeout(syncWa, 0); });
    syncWa();
    wa.addEventListener('click', function (e) {
      syncWa();
      if (!S.name.trim()) { e.preventDefault(); flag(['name']); return; }
      push({ event: 'letter_whatsapp', project_type: S.type !== null ? FIELD.type[S.type] : 'Not specified' });
    });

    // the phone code from where the visitor is (+966 otherwise)
    if (fresh) {
      fetch('https://ipapi.co/json/').then(function (r) { return r.json(); }).then(function (d) {
        var cc = d && d.country_calling_code; if (!cc) return;
        cc = cc.charAt(0) === '+' ? cc : '+' + cc;
        if (CODES.indexOf(cc) > -1) { S.code = cc; code.value = cc; save(); syncWa(); }
      }).catch(function () {});
    }
  };

  // ═════════════════════════════════════ THE VISIT ══
  window.FIQVisit = function () {
    var root = document.getElementById('visit-root');
    if (!root || root.dataset.ready) return;
    root.dataset.ready = '1';
    var HOURS = [[9, 12], [12, 15], [15, 18]];
    var now = riyadh();
    // the next five working days, today included while a slot is still ahead
    var days = [];
    for (var k = 0; days.length < 5 && k < 14; k++) {
      var d0 = now.day0 + k * 86400000, wd = new Date(d0).getUTCDay();
      if (WORKDAYS.indexOf(wd) < 0) continue;
      if (k === 0 && now.h >= CLOSE - 2) continue;
      days.push({ d0: d0, today: k === 0 });
    }
    var pick = { day: null, slot: null };

    var dayRow = el('div', { 'class': 'vs-days', role: 'group', 'aria-label': T.dayLabel });
    var slotRow = el('div', { 'class': 'vs-slots', role: 'group', 'aria-label': T.timeLabel });
    var cta = el('a', { 'class': 'vs-cta is-off', href: '#', target: '_blank', rel: 'noopener', 'aria-disabled': 'true', id: 'id-visit-cta' });
    var mail = el('a', { 'class': 'vs-mail', href: '#' }, [T.byMail]);

    days.forEach(function (d, i) {
      dayRow.appendChild(el('button', { type: 'button', 'class': 'vs-day', 'aria-pressed': 'false', onclick: function () { pick.day = i; if (pick.slot !== null && !slotOk(pick.slot)) pick.slot = null; paint(); } }, [
        el('small', { text: d.today ? (AR ? T.today : 'Today') : fmtDate(d.d0, { weekday: AR ? 'long' : 'short' }) }),
        el('b', { text: fmtDate(d.d0, { day: 'numeric' }) }),
        el('span', { text: fmtDate(d.d0, { month: AR ? 'long' : 'short' }) }),
      ]));
    });
    HOURS.forEach(function (h, i) {
      slotRow.appendChild(el('button', { type: 'button', 'class': 'vs-slot', 'aria-pressed': 'false', onclick: function () { pick.slot = i; paint(); } }, [
        el('b', { text: T.slots[i][0] }), el('span', { text: h[0] + ':00 – ' + h[1] + ':00', dir: 'ltr' }),
      ]));
    });
    function slotOk(i) { var d = days[pick.day]; return !d || !d.today || HOURS[i][1] - 1 > now.h; }   // today: at least an hour of the slot ahead

    function paint() {
      [].forEach.call(dayRow.children, function (b, i) { b.setAttribute('aria-pressed', pick.day === i ? 'true' : 'false'); });
      [].forEach.call(slotRow.children, function (b, i) { b.setAttribute('aria-pressed', pick.slot === i ? 'true' : 'false'); b.disabled = !slotOk(i); });
      var ready = pick.day !== null && pick.slot !== null;
      cta.classList.toggle('is-off', !ready);
      cta.setAttribute('aria-disabled', ready ? 'false' : 'true');
      if (!ready) {
        cta.textContent = pick.day === null ? T.chooseDay : T.chooseTime;
        cta.href = '#'; mail.href = '#'; mail.hidden = true;
        return;
      }
      var d = days[pick.day], h = HOURS[pick.slot];
      var when = fmtDate(d.d0, { weekday: 'long', day: 'numeric', month: 'long' });
      var slot = T.slots[pick.slot][1], range = h[0] + ':00 – ' + h[1] + ':00';
      cta.innerHTML = '';
      cta.appendChild(document.createTextNode(T.request(when, slot)));
      cta.insertAdjacentHTML('beforeend', ARROW);
      var text = T.visitText(when, slot, range);
      cta.href = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(text);
      mail.hidden = false;
      mail.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(T.visitSubject(when)) + '&body=' + encodeURIComponent(text);
    }
    cta.addEventListener('click', function (e) {
      if (cta.classList.contains('is-off')) { e.preventDefault(); return; }
      push({ event: 'visit_request', channel: 'whatsapp' });
    });
    mail.addEventListener('click', function (e) {
      if (mail.getAttribute('href') === '#') { e.preventDefault(); return; }
      push({ event: 'visit_request', channel: 'email' });
    });

    root.appendChild(el('div', { 'class': 'vs-label', text: T.pickDay }));
    root.appendChild(dayRow);
    root.appendChild(el('div', { 'class': 'vs-label', text: T.pickTime }));
    root.appendChild(slotRow);
    root.appendChild(el('div', { 'class': 'vs-acts' }, [cta, mail]));
    root.appendChild(el('p', { 'class': 'vs-fine', text: T.visitFine }));
    paint();
  };

  // ═════════════════════════════════ THE STUDIO, RIGHT NOW ══
  // #direct-clock: Riyadh time set large, open or closed, the working week with today marked, and a 24-hour ruler
  // with the studio's hours and a marker at now (it runs right to left on the Arabic page). The card's Copy button
  // copies the email address.
  window.FIQDirect = function () {
    var root = document.getElementById('direct-clock');
    if (!root || root.dataset.ready) return;
    root.dataset.ready = '1';
    var side = AR ? 'right' : 'left';
    var time = el('b', { dir: 'ltr' }), state = el('p', { 'class': 'ck-state' }), marker = el('u', { 'aria-hidden': 'true' });
    var week = el('div', { 'class': 'ck-week', 'aria-label': T.weekLabel }, T.days.map(function (d, i) {
      var on = WORKDAYS.indexOf(i) > -1;
      return el('span', { 'class': 'ck-day' + (on ? '' : ' is-off') }, [d, el('small', { text: on ? '9 – 18' : T.dayOff, dir: on ? 'ltr' : null })]);
    }));
    var scale = el('div', { 'class': 'ck-scale', 'aria-hidden': 'true' }, [[0, '0:00'], [OPEN, OPEN + ':00'], [CLOSE, CLOSE + ':00'], [24, '24:00']].map(function (m) {
      return el('span', { text: m[1], style: side + ':' + (m[0] / 24 * 100) + '%' });
    }));
    root.innerHTML = '';
    root.appendChild(el('div', { 'class': 'ck-time' }, [time, el('span', { text: T.clockLabel })]));
    root.appendChild(state);
    root.appendChild(week);
    root.appendChild(el('div', { 'class': 'ck-ruler', 'aria-hidden': 'true' }, [el('i'), el('em'), marker]));
    root.appendChild(scale);
    function tick() {
      var t = riyadh(), o = isOpen(t);
      time.textContent = t.clock;
      state.textContent = o ? T.openNow : T.closedNow(nextOpening(t));
      state.classList.toggle('is-open', o);
      [].forEach.call(week.children, function (d, i) { d.classList.toggle('is-today', i === t.weekday); });
      marker.style[side] = ((t.h + t.m / 60) / 24 * 100) + '%';
    }
    tick(); setInterval(tick, 20000);
    [].forEach.call(document.querySelectorAll('[data-copy]'), function (b) {
      b.addEventListener('click', function () {
        var done = function () { b.textContent = T.copied; setTimeout(function () { b.textContent = T.copy; }, 1800); };
        if (navigator.clipboard) navigator.clipboard.writeText(b.dataset.copy).then(done, function () {}); else done();
        push({ event: 'contact_copy_email' });
      });
    });
  };

  if (window.FIQLetterPending) { window.FIQLetterPending = false; window.FIQLetter(); }
  if (window.FIQDirectPending) { window.FIQDirectPending = false; window.FIQDirect(); }
  if (window.FIQVisitPending) { window.FIQVisitPending = false; window.FIQVisit(); }
})();

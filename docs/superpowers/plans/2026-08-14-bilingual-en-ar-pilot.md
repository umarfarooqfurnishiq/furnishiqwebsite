# Bilingual EN/AR Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `furnishiq.net/en` and `furnishiq.net/ar` as working bilingual entry points for the two currently-live pages (home, contact), with infrastructure generic enough that the other 9 pages can be added later without a redesign.

**Architecture:** Two new static files (`home.ar.dc.html`, `contact.ar.dc.html`) mirror the existing English pages with RTL text direction, GE SS Two font, and translated copy. `vercel.json` gains rewrites so `/en/*` aliases the existing English files and `/ar/*` serves the new Arabic files, plus redirects so the 9 still-hidden pages keep 301-ing home under both new prefixes exactly as they do today. No build step, no framework — this is a pure static HTML/CSS/JS site (`CLAUDE.md`).

**Tech Stack:** Static HTML with inline CSS/JS (the project's existing "x-dc" component pattern), Node.js one-off scripts for scripted find-replace (matching the pattern already used in this repo for the clean-URL and lazy-loading migrations), Playwright for verification (no permanent test suite exists in this repo — verification scripts live in the scratchpad directory, not committed).

**Spec:** `docs/superpowers/specs/2026-08-14-bilingual-en-ar-pilot-design.md`

## Global Constraints

- Pure static HTML/CSS/JS. No CMS, no backend beyond the existing `/api/send-email` endpoint, no build step (`CLAUDE.md`).
- Design system colors/fonts only: Walnut `#5B4636`, Dark Walnut `#3A2D25`, Bronze `#8B6B4A`, Stone `#F5F2ED`, Charcoal `#1F1F1F`, champagne accent `#D6C2A8`. `border-radius:0` everywhere. English text: `'Lama Sans',sans-serif`. Arabic text: `'GE SS Two','Arial',sans-serif` (font file already exists at `Furnishiq.net/_ds/furnishiq-design-system-ea658a9e-dd64-48ad-ab93-f0196a53ec9c/uploads/GE_SS_Two_Medium_Arabic.otf`, already wired into `typography.css` via `--font-arabic`, currently unused).
- RTL scope is **typography only**, not macro-layout — see spec section 3. Do not flip which side images/columns sit on.
- Brand name "FurnishIQ" stays in Latin script in Arabic copy (not transliterated), matching how the logo itself is a Latin wordmark.
- Numerals stay Western digits (`01`, `02`, `250K`) in Arabic copy too — the design system's own style guide (`_ds/.../readme.md:54`) specifies "Arabic numerals for all figures" meaning the digit system generally, and the brand's own copy examples use Western digits.
- No exclamation marks, no emoji, authoritative/refined tone — same brand voice rules as the English copy, adapted for Arabic (`CLAUDE.md`).
- The 9 hidden pages (about-us, blog, portfolio, project-detail, single-post, services-fitout, services-furniture, services-interior-design, services-mep) are **not** touched by this plan. Their existing redirect-to-home behavior must be preserved, now under `/en/*` and `/ar/*` too.
- `/en/*` is a pure alias — same file, same response, same embedded canonical tag as the bare path. It gets no separate sitemap entry.

---

## File Structure

| File | Action | Responsibility |
|---|---|---|
| `Furnishiq.net/home.dc.html` | Modify | Add hreflang alternates + language-switcher link to `/ar` |
| `Furnishiq.net/contact.dc.html` | Modify | Add hreflang alternates + language-switcher link to `/ar/contact` |
| `Furnishiq.net/home.ar.dc.html` | Create | Arabic, RTL mirror of home.dc.html |
| `Furnishiq.net/contact.ar.dc.html` | Create | Arabic, RTL mirror of contact.dc.html |
| `Furnishiq.net/floating-buttons.js` | Modify | WhatsApp pre-filled message switches to Arabic when `document.documentElement.lang === 'ar'` |
| `vercel.json` | Modify | `/en`, `/en/contact`, `/ar`, `/ar/contact` rewrites; 18 hidden-page redirects under both prefixes |
| `Furnishiq.net/robots.txt` | Modify | Disallow the 18 hidden-page paths under `/en/` and `/ar/` |
| `Furnishiq.net/sitemap.xml` | Modify | Add `/ar` and `/ar/contact` (not `/en/*` — see constraint above) |

No test/ directory exists in this repo (static site, no test runner). "Test" steps below are Playwright verification scripts written to the scratchpad directory and run against a local `python -m http.server` — the same pattern used for every prior change in this project (mobile nav, floating buttons, lazy-loading, clean URLs).

---

### Task 1: Add hreflang + language switcher to the English pages

**Files:**
- Modify: `Furnishiq.net/home.dc.html`
- Modify: `Furnishiq.net/contact.dc.html`

**Interfaces:**
- Produces: the `.fiq-nav-links` container in both files now contains an extra `<a>` for the language switcher — Task 4 and 5's mobile-nav verification depends on this link being present and cloned into the mobile overlay by the existing `nav-mobile.js`.

- [ ] **Step 1: Add hreflang alternates to `home.dc.html`**

In `Furnishiq.net/home.dc.html`, find line 9 (`<link rel="canonical" href="https://www.furnishiq.net/">`) and insert immediately after it:

```html
<link rel="alternate" hreflang="en" href="https://www.furnishiq.net/">
<link rel="alternate" hreflang="ar" href="https://www.furnishiq.net/ar">
<link rel="alternate" hreflang="x-default" href="https://www.furnishiq.net/">
```

- [ ] **Step 2: Add hreflang alternates to `contact.dc.html`**

In `Furnishiq.net/contact.dc.html`, find line 9 (`<link rel="canonical" href="https://www.furnishiq.net/contact">`) and insert immediately after it:

```html
<link rel="alternate" hreflang="en" href="https://www.furnishiq.net/contact">
<link rel="alternate" hreflang="ar" href="https://www.furnishiq.net/ar/contact">
<link rel="alternate" hreflang="x-default" href="https://www.furnishiq.net/contact">
```

- [ ] **Step 3: Add the language switcher link to `home.dc.html`**

In `Furnishiq.net/home.dc.html`, find the nav links container (line 92-97):

```html
    <div class="fiq-nav-links" style="display:flex;gap:clamp(24px,3.5vw,48px);align-items:center;flex:1;justify-content:center;">
      <a href="#services" data-nav-link style="font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.18em;text-transform:uppercase;color:#FFFFFF;text-decoration:none;transition:color 0.25s,opacity 0.25s;opacity:0.8;">Services</a>
      <a href="#portfolio" data-nav-link style="font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.18em;text-transform:uppercase;color:#FFFFFF;text-decoration:none;transition:color 0.25s,opacity 0.25s;opacity:0.8;">Portfolio</a>
      <a href="#process" data-nav-link style="font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.18em;text-transform:uppercase;color:#FFFFFF;text-decoration:none;transition:color 0.25s,opacity 0.25s;opacity:0.8;">Process</a>
      <a href="#blog" data-nav-link style="font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.18em;text-transform:uppercase;color:#FFFFFF;text-decoration:none;transition:color 0.25s,opacity 0.25s;opacity:0.8;">Insights</a>
    </div>
```

Add a language-switcher `<a>` right after the "Insights" link, still inside the `.fiq-nav-links` div (so it's included when `nav-mobile.js` clones this container into the mobile overlay):

```html
      <a href="/ar" data-nav-link data-lang-switch style="font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.18em;text-transform:uppercase;color:#FFFFFF;text-decoration:none;transition:color 0.25s,opacity 0.25s;opacity:0.8;">عربي</a>
```

- [ ] **Step 4: Add the language switcher link to `contact.dc.html`**

Same pattern in `Furnishiq.net/contact.dc.html`'s nav links container (line 59-64), add after the "Insights" link:

```html
      <a href="/ar/contact" data-nav-link data-lang-switch style="font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.18em;text-transform:uppercase;color:#FFFFFF;text-decoration:none;transition:color 0.25s,opacity 0.25s;opacity:0.8;">عربي</a>
```

- [ ] **Step 5: Verify with a local server**

```bash
python -m http.server 8532 --directory Furnishiq.net
```

```bash
curl -s http://localhost:8532/home.dc.html | grep -c 'hreflang'
```
Expected: `3` (en, ar, x-default)

```bash
curl -s http://localhost:8532/home.dc.html | grep -o '<a href="/ar"[^>]*>عربي</a>'
```
Expected: the switcher link, present exactly once.

Repeat both checks against `contact.dc.html`, expecting `href="/ar/contact"`.

- [ ] **Step 6: Commit**

```bash
git add Furnishiq.net/home.dc.html Furnishiq.net/contact.dc.html
git commit -m "Add hreflang alternates and language switcher to home + contact"
```

---

### Task 2: Update `vercel.json` routing

**Files:**
- Modify: `vercel.json`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: `/en`, `/en/contact`, `/ar`, `/ar/contact` resolve; `/en/<hidden-page>` and `/ar/<hidden-page>` 301 to `/` for all 9 hidden pages, matching current bare-path behavior exactly.

- [ ] **Step 1: Add the 4 new rewrites**

In `vercel.json`, inside the `"rewrites"` array, add these entries immediately after the existing `{ "source": "/", "destination": "/Furnishiq.net/home.dc.html" }` line:

```json
    { "source": "/en", "destination": "/Furnishiq.net/home.dc.html" },
    { "source": "/en/contact", "destination": "/Furnishiq.net/contact.dc.html" },
    { "source": "/ar", "destination": "/Furnishiq.net/home.ar.dc.html" },
    { "source": "/ar/contact", "destination": "/Furnishiq.net/contact.ar.dc.html" },
```

- [ ] **Step 2: Add the 18 hidden-page redirects**

In `vercel.json`, inside the `"redirects"` array, add these entries (after the existing hidden-page redirects, before the `/contact.dc.html` redirect):

```json
    { "source": "/en/about-us", "destination": "/", "permanent": true },
    { "source": "/ar/about-us", "destination": "/", "permanent": true },
    { "source": "/en/blog", "destination": "/", "permanent": true },
    { "source": "/ar/blog", "destination": "/", "permanent": true },
    { "source": "/en/portfolio", "destination": "/", "permanent": true },
    { "source": "/ar/portfolio", "destination": "/", "permanent": true },
    { "source": "/en/project-detail", "destination": "/", "permanent": true },
    { "source": "/ar/project-detail", "destination": "/", "permanent": true },
    { "source": "/en/single-post", "destination": "/", "permanent": true },
    { "source": "/ar/single-post", "destination": "/", "permanent": true },
    { "source": "/en/services-interior-design", "destination": "/", "permanent": true },
    { "source": "/ar/services-interior-design", "destination": "/", "permanent": true },
    { "source": "/en/services-fitout", "destination": "/", "permanent": true },
    { "source": "/ar/services-fitout", "destination": "/", "permanent": true },
    { "source": "/en/services-mep", "destination": "/", "permanent": true },
    { "source": "/ar/services-mep", "destination": "/", "permanent": true },
    { "source": "/en/services-furniture", "destination": "/", "permanent": true },
    { "source": "/ar/services-furniture", "destination": "/", "permanent": true },
```

- [ ] **Step 3: Verify JSON validity and counts**

```bash
node -e "const c = require('./vercel.json'); console.log('redirects:', c.redirects.length, 'rewrites:', c.rewrites.length);"
```
Expected: `redirects: 37 rewrites: 17` (19 original redirects + 18 new; 13 original rewrites + 4 new).

- [ ] **Step 4: Commit**

```bash
git add vercel.json
git commit -m "Add /en and /ar routing for the bilingual pilot"
```

---

### Task 3: Update `robots.txt` and `sitemap.xml`

**Files:**
- Modify: `Furnishiq.net/robots.txt`
- Modify: `Furnishiq.net/sitemap.xml`

**Interfaces:**
- Consumes: nothing from other tasks.

- [ ] **Step 1: Add Disallow rules to `robots.txt`**

In `Furnishiq.net/robots.txt`, after the existing `Disallow: /services-furniture` line and before the blank line + `Sitemap:` line, add:

```
Disallow: /en/about-us
Disallow: /ar/about-us
Disallow: /en/blog
Disallow: /ar/blog
Disallow: /en/portfolio
Disallow: /ar/portfolio
Disallow: /en/project-detail
Disallow: /ar/project-detail
Disallow: /en/single-post
Disallow: /ar/single-post
Disallow: /en/services-interior-design
Disallow: /ar/services-interior-design
Disallow: /en/services-fitout
Disallow: /ar/services-fitout
Disallow: /en/services-mep
Disallow: /ar/services-mep
Disallow: /en/services-furniture
Disallow: /ar/services-furniture
```

- [ ] **Step 2: Add sitemap entries**

In `Furnishiq.net/sitemap.xml`, after the `<url><loc>https://www.furnishiq.net/contact</loc></url>` entry and before `</urlset>`, add:

```xml
  <url>
    <loc>https://www.furnishiq.net/ar</loc>
  </url>
  <url>
    <loc>https://www.furnishiq.net/ar/contact</loc>
  </url>
```

- [ ] **Step 3: Verify**

```bash
grep -c 'Disallow: /en/\|Disallow: /ar/' Furnishiq.net/robots.txt
```
Expected: `18`

```bash
node -e "require('fs').readFileSync('Furnishiq.net/sitemap.xml','utf8').includes('/ar/contact') || process.exit(1)"
```
Expected: exit code 0 (no output).

- [ ] **Step 4: Commit**

```bash
git add Furnishiq.net/robots.txt Furnishiq.net/sitemap.xml
git commit -m "Update robots.txt and sitemap.xml for the bilingual pilot"
```

---

### Task 4: Create `home.ar.dc.html`

**Files:**
- Create: `Furnishiq.net/home.ar.dc.html`

**Interfaces:**
- Consumes: `Furnishiq.net/home.dc.html` (Task 1's version, with hreflang + switcher already added) as the source to duplicate.
- Produces: a fully translated, RTL Arabic homepage at this path, which Task 2's `/ar` rewrite serves.

- [ ] **Step 1: Duplicate the source file**

```bash
cp Furnishiq.net/home.dc.html Furnishiq.net/home.ar.dc.html
```

- [ ] **Step 2: Apply mechanical RTL/meta transforms**

Create `scripts/ar-transform-home.js` (temporary, in the scratchpad directory, not committed) with this exact content:

```js
const fs = require('fs');
const fp = 'Furnishiq.net/home.ar.dc.html';
let c = fs.readFileSync(fp, 'utf8');

// 1. RTL + lang on <html>
c = c.replace('<html>', '<html dir="rtl" lang="ar">');

// 2. Font swap — every inline font-family declaration becomes Arabic
c = c.split("font-family:'Lama Sans',sans-serif").join("font-family:'GE SS Two','Arial',sans-serif");

// 3. Meta: title, description, canonical, OG, Twitter
c = c.replace(
  '<title>FurnishIQ | Luxury Interior Design &amp; Fit-Out in Saudi Arabia</title>',
  '<title>FurnishIQ | تصميم داخلي وتشطيبات فاخرة في المملكة العربية السعودية</title>'
);
c = c.replace(
  '<meta name="description" content="FurnishIQ crafts integrated interior design, fit-out, engineering, and furniture solutions for villas and commercial spaces across Saudi Arabia.">',
  '<meta name="description" content="تصمم FurnishIQ حلولاً متكاملة للتصميم الداخلي والتشطيبات والهندسة والأثاث للفلل والمساحات التجارية في جميع أنحاء المملكة العربية السعودية.">'
);
c = c.replace(
  '<link rel="canonical" href="https://www.furnishiq.net/">',
  '<link rel="canonical" href="https://www.furnishiq.net/ar">'
);
c = c.replace(
  '<link rel="alternate" hreflang="en" href="https://www.furnishiq.net/">\n<link rel="alternate" hreflang="ar" href="https://www.furnishiq.net/ar">\n<link rel="alternate" hreflang="x-default" href="https://www.furnishiq.net/">',
  '<link rel="alternate" hreflang="en" href="https://www.furnishiq.net/">\n<link rel="alternate" hreflang="ar" href="https://www.furnishiq.net/ar">\n<link rel="alternate" hreflang="x-default" href="https://www.furnishiq.net/">'
);
c = c.replace(
  '<meta property="og:url" content="https://www.furnishiq.net/">',
  '<meta property="og:url" content="https://www.furnishiq.net/ar">'
);
c = c.replace(
  /<meta property="og:title" content="FurnishIQ \| Luxury Interior Design &amp; Fit-Out in Saudi Arabia">/,
  '<meta property="og:title" content="FurnishIQ | تصميم داخلي وتشطيبات فاخرة في المملكة العربية السعودية">'
);
c = c.replace(
  /<meta property="og:description" content="FurnishIQ crafts integrated interior design, fit-out, engineering, and furniture solutions for villas and commercial spaces across Saudi Arabia\.">/,
  '<meta property="og:description" content="تصمم FurnishIQ حلولاً متكاملة للتصميم الداخلي والتشطيبات والهندسة والأثاث للفلل والمساحات التجارية في جميع أنحاء المملكة العربية السعودية.">'
);
c = c.replace(
  /<meta name="twitter:title" content="FurnishIQ \| Luxury Interior Design &amp; Fit-Out in Saudi Arabia">/,
  '<meta name="twitter:title" content="FurnishIQ | تصميم داخلي وتشطيبات فاخرة في المملكة العربية السعودية">'
);
c = c.replace(
  /<meta name="twitter:description" content="FurnishIQ crafts integrated interior design, fit-out, engineering, and furniture solutions for villas and commercial spaces across Saudi Arabia\.">/,
  '<meta name="twitter:description" content="تصمم FurnishIQ حلولاً متكاملة للتصميم الداخلي والتشطيبات والهندسة والأثاث للفلل والمساحات التجارية في جميع أنحاء المملكة العربية السعودية.">'
);

// 4. Internal links stay in Arabic — lock them to /ar equivalents.
//    MUST run before the switcher flip below: both target bare href="/",
//    so locking first (while the switcher still reads href="/ar" from the
//    source copy) means the switcher is untouched by this blanket rule.
c = c.split('href="/contact"').join('href="/ar/contact"');
c = c.split('href="/"').join('href="/ar"'); // logo + footer logo links

// 5. Language switcher now points back to English. Runs last, using a
//    match string specific enough (data-lang-switch) not to collide with
//    the logo links step 4 also touched.
c = c.replace(
  '<a href="/ar" data-nav-link data-lang-switch',
  '<a href="/" data-nav-link data-lang-switch'
);
c = c.replace('>عربي</a>', '>English</a>');

fs.writeFileSync(fp, c, 'utf8');
console.log('mechanical transform applied');
```

Run it:
```bash
node scripts/ar-transform-home.js
```

- [ ] **Step 3: Verify the mechanical transform**

```bash
grep -c 'dir="rtl" lang="ar"' Furnishiq.net/home.ar.dc.html
```
Expected: `1`

```bash
grep -c "GE SS Two" Furnishiq.net/home.ar.dc.html
```
Expected: a large number (matches every text element that had the font declaration — sanity check it's non-zero and roughly matches the ~70 occurrences of `font-family:'Lama Sans'` in the original file).

```bash
grep -c "Lama Sans" Furnishiq.net/home.ar.dc.html
```
Expected: `0` (every instance was swapped — if this is non-zero, the font swap step missed something and must be fixed before continuing).

- [ ] **Step 4: Translate the copy**

Create `scripts/ar-translate-home.js` (temporary, scratchpad, not committed) with this exact content — the full English→Arabic dictionary for every visible string on the homepage:

```js
const fs = require('fs');
const fp = 'Furnishiq.net/home.ar.dc.html';
let c = fs.readFileSync(fp, 'utf8');

const pairs = [
  // Nav
  ['>Services</a>', '>الخدمات</a>'],
  ['>Portfolio</a>', '>أعمالنا</a>'],
  ['>Process</a>', '>منهجيتنا</a>'],
  ['>Insights</a>', '>المقالات</a>'],
  ['>Request a Consultation</a>', '>اطلب استشارة</a>'],
  // Hero
  ['>Finished Build</span>', '>التنفيذ النهائي</span>'],
  ['>3D Render</span>', '>تصور ثلاثي الأبعاد</span>'],
  ['>FLOOR PLAN — LEVEL 01 · SCALE 1:50</span>', '>المخطط الأرضي — الطابق 01 · المقياس 1:50</span>'],
  ['>Design — Build — Deliver</span>', '>تصميم — تنفيذ — تسليم</span>'],
  ['Where Vision<br>Meets Precision.', 'حيث تلتقي الرؤية<br>بالدقة.'],
  ["We don't just design; we deliver. FurnishIQ provides integrated Design–Build solutions that turn ambitious architectural concepts into functional, inspiring realities across Saudi Arabia.",
   'نحن لا نكتفي بالتصميم؛ بل نُنجز. تقدم FurnishIQ حلول تصميم وتنفيذ متكاملة تُحوّل المفاهيم المعمارية الطموحة إلى واقع وظيفي وملهم في جميع أنحاء المملكة العربية السعودية.'],
  ['>Visualize Your Project</a>', '>تصوّر مشروعك</a>'],
  ['>View Our Portfolio</a>', '>استعرض أعمالنا</a>'],
  ['>Scroll</span>', '>مرر للأسفل</span>'],
  // Services grid
  ['>What We Do</span>', '>ماذا نقدم</span>'],
  ['Integrated Expertise.<br>Exceptional Results.', 'خبرة متكاملة.<br>نتائج استثنائية.'],
  ['>Interior Design</h3>', '>التصميم الداخلي</h3>'],
  ['>Thoughtful, Bespoke &amp; Visionary</p>', '>مدروس، مخصص، ورؤيوي</p>'],
  ['We create personalised, livable environments balancing high-end aesthetics with practical functionality. Full Photoreal 3D visuals before any construction begins, so you approve every detail with absolute confidence.',
   'نصمم بيئات معيشية مخصصة توازن بين الجماليات الراقية والوظائف العملية. تصورات ثلاثية الأبعاد فوتوغرافية الواقعية قبل بدء أي أعمال إنشائية، لتعتمد كل تفصيلة بثقة تامة.'],
  ['>Fit-Out</h3>', '>التشطيبات</h3>'],
  ['>Turning Raw Shells into Masterpieces</p>', '>نحوّل الهياكل الخام إلى تحف معمارية</p>'],
  ['The core of our business. Complete transformation of raw shells into fully functional, turnkey environments through Brand-Led Planning and our hallmark Zero-Snag Promise — every finish meeting the highest standard.',
   'جوهر عملنا. تحويل كامل للهياكل الخام إلى بيئات جاهزة وظيفياً بالكامل من خلال التخطيط الموجّه بالهوية التجارية والتزامنا المميز بخلوّ العيوب — بحيث تلبي كل تشطيبة أعلى المعايير.'],
  ['>Engineering &amp; MEP</h3>', '>الهندسة والأنظمة الكهروميكانيكية</h3>'],
  ['>The Precision Backbone</p>', '>العمود الفقري للدقة</p>'],
  ['True luxury depends on invisible systems. Our MEP (Mechanical, Electrical, and Plumbing) services provide high-performance infrastructure seamlessly integrated into the architectural fabric — maximising efficiency and comfort.',
   'الفخامة الحقيقية تعتمد على أنظمة غير مرئية. توفر خدماتنا الكهروميكانيكية (الميكانيكية والكهربائية والصحية) بنية تحتية عالية الأداء تندمج بسلاسة في النسيج المعماري — لتعزيز الكفاءة والراحة.'],
  ['>Furniture Solutions</h3>', '>حلول الأثاث</h3>'],
  ['>Strategic Sourcing &amp; Curation</p>', '>توريد وانتقاء استراتيجي</p>'],
  ['We strategically source furniture aligned with your approved 3D renders. Leveraging global industry connections, we procure high-quality pieces matching your aesthetic, budget, and operational needs — floor to ceiling coherence.',
   'نقوم بتوريد الأثاث بشكل استراتيجي بما يتماشى مع تصوراتك ثلاثية الأبعاد المعتمدة. وبالاستفادة من علاقاتنا العالمية في هذا المجال، نوفر قطعاً عالية الجودة تناسب ذوقك وميزانيتك واحتياجاتك التشغيلية — بانسجام تام من الأرضية إلى السقف.'],
  ['>Explore Service</span>', '>استكشف الخدمة</span>'],
  // Fit-out feature
  ['>Shell → Masterpiece</div>', '>هيكل خام ← تحفة معمارية</div>'],
  ['>Featured Service</span>', '>خدمة مميزة</span>'],
  ['Turn Any Shell Into<br>a Masterpiece.', 'حوّل أي هيكل خام<br>إلى تحفة معمارية.'],
  ['Our Fit-Out services are the core of our business. We take raw, structural shells and transform them into fully functional, turnkey environments.',
   'خدمات التشطيبات لدينا هي جوهر عملنا. نأخذ الهياكل الإنشائية الخام ونحوّلها إلى بيئات جاهزة وظيفياً بالكامل.'],
  ['From intricate MEP integration to bespoke finishing, we manage the technical complexity so you can focus on your business or home.',
   'من التكامل الدقيق للأنظمة الكهروميكانيكية إلى التشطيبات المخصصة، نتولى التعقيدات الفنية لتتفرغ أنت لعملك أو منزلك.'],
  ['>Request a Fit-Out Quote</a>', '>اطلب عرض سعر للتشطيبات</a>'],
  // Process
  ['>Our Process</span>', '>منهجية عملنا</span>'],
  ['>A Transparent Process.</span>', '>منهجية شفافة.</span>'],
  ['>No Surprises.</span>', '>بلا مفاجآت.</span>'],
  ['>Discover</h4>', '>الاكتشاف</h4>'],
  ['We align on your goals, conduct site surveys, and establish a firm budget roadmap.',
   'نتفق على أهدافك، نُجري مسوحات الموقع، ونضع خارطة طريق مالية واضحة.'],
  ['>Design</h4>', '>التصميم</h4>'],
  ['We develop layouts and mood boards, culminating in high-definition 3D visuals for your approval.',
   'نطوّر المخططات ولوحات الإلهام، وصولاً إلى تصورات ثلاثية الأبعاد عالية الدقة لاعتمادها.'],
  ['>Build</h4>', '>التنفيذ</h4>'],
  ['Our team takes over with strict program certainty and continuous HSE safety monitoring throughout.',
   'يتولى فريقنا التنفيذ بالتزام صارم بالجدول الزمني ومراقبة مستمرة للصحة والسلامة والبيئة.'],
  ['>Handover</h4>', '>التسليم</h4>'],
  ['Experience a Zero-Snag completion backed by dedicated aftercare and complete documentation.',
   'استلم مشروعك بإنجاز خالٍ من العيوب، مدعوماً برعاية لاحقة مخصصة وتوثيق كامل.'],
  // Value proposition
  ['>The FurnishIQ Edge</span>', '>تميّز FurnishIQ</span>'],
  ['Why We Are the New Standard</span></div>', 'لماذا نحن المعيار الجديد</span></div>'],
  ['in KSA Interiors.</span></div>', 'للتصميم الداخلي في المملكة.</span></div>'],
  ['>Visual Certainty</h3>', '>يقين بصري</h3>'],
  ['Decide with total confidence. We provide full Photoreal 3D Renders of every floor and landscape before a single brick is laid, ensuring your vision is captured perfectly.',
   'قرر بثقة تامة. نوفر تصورات ثلاثية الأبعاد فوتوغرافية الواقعية الكاملة لكل طابق ومساحة خارجية قبل وضع أول لبنة، لضمان تجسيد رؤيتك بدقة.'],
  ['>Full 3D Visualization</span>', '>تصور ثلاثي الأبعاد كامل</span>'],
  ['>Strategic DNA</h3>', '>بصمة استراتيجية</h3>'],
  ['We practice Brand-Led Planning. Every layout and spatial flow is strategically engineered to reflect your brand identity and optimize your daily operations.',
   'نتبع أسلوب التخطيط الموجّه بالهوية التجارية. كل مخطط وتدفق مكاني مصمم استراتيجياً ليعكس هوية علامتك التجارية ويُحسّن عملياتك اليومية.'],
  ['>Brand-Led Planning</span>', '>تخطيط موجّه بالهوية التجارية</span>'],
  ['>Zero-Snag Promise</h3>', '>التزام خلوّ العيوب</h3>'],
  ['Our hallmark is excellence in execution. Through rigorous QA/QC and HSE monitoring, we guarantee a "Clean Build" and a flawless, zero-snag handover every time.',
   'سمتنا المميزة هي التميز في التنفيذ. من خلال مراقبة صارمة للجودة والسلامة، نضمن "بناءً نظيفاً" وتسليماً خالياً من العيوب في كل مرة.'],
  ['>Clean Build Guarantee</span>', '>ضمان البناء النظيف</span>'],
  // Portfolio
  ['>Selected Work</span>', '>أعمال مختارة</span>'],
  ['Transforming the Kingdom,<br>One Space at a Time.', 'نُحوّل المملكة،<br>مساحة تلو الأخرى.'],
  ['>View All Projects</a>', '>عرض جميع المشاريع</a>'],
  ['>Hospitality · Jeddah</div>', '>الضيافة · جدة</div>'],
  ['>Jeddah Boutique Hotel</h3>', '>فندق بوتيك جدة</h3>'],
  ['>Redefining commercial hospitality.</p>', '>إعادة تعريف الضيافة التجارية.</p>'],
  ['>Residential · Riyadh</div>', '>سكني · الرياض</div>'],
  ['>Wadi Villas, Riyadh</h3>', '>فلل وادي، الرياض</h3>'],
  ['>Luxury residential living at its finest.</p>', '>معيشة سكنية فاخرة بأرقى صورها.</p>'],
  ['>Architecture · KSA</div>', '>العمارة · المملكة العربية السعودية</div>'],
  ['>Ali Saleh Altamimi Villa</h3>', '>فيلا علي صالح التميمي</h3>'],
  ['>Full-scale architectural and landscape design.</p>', '>تصميم معماري وتنسيق مواقع شامل.</p>'],
  // Blog
  ['>From the Studio</span>', '>من الاستوديو</span>'],
  ['>Expertise Shared.</h2>', '>خبرة نتشاركها.</h2>'],
  ['>All Articles</a>', '>جميع المقالات</a>'],
  ['>Design Strategy</div>', '>استراتيجية التصميم</div>'],
  ['>The Science of Spatial Flow: How Layouts Affect Your Brand.</h3>', '>علم تدفق المساحات: كيف تؤثر المخططات على علامتك التجارية.</h3>'],
  ['>Understanding how physical space shapes human behaviour, perception, and brand experience.</p>', '>فهم كيف تُشكّل المساحة المادية السلوك البشري والإدراك وتجربة العلامة التجارية.</p>'],
  ['>Read Article</span>', '>اقرأ المقال</span>'],
  ['>Furniture</div>', '>الأثاث</div>'],
  ['>How to Choose Furniture That Scales With Your Home.</h3>', '>كيف تختار أثاثاً يتناسب مع منزلك مع مرور الوقت.</h3>'],
  ['>Strategic principles for selecting pieces that grow gracefully with your lifestyle and living space.</p>', '>مبادئ استراتيجية لاختيار قطع تتناسب بسلاسة مع أسلوب حياتك ومساحتك المعيشية.</p>'],
  ['>Kitchen Design</div>', '>تصميم المطابخ</div>'],
  ['>Top 10 Tips for Modern Kitchen Design in Saudi Arabia.</h3>', '>أفضل 10 نصائح لتصميم المطابخ العصرية في المملكة العربية السعودية.</h3>'],
  ['>From material selection to spatial planning — how to design a kitchen that performs beautifully.</p>', '>من اختيار المواد إلى التخطيط المكاني — كيف تصمم مطبخاً يؤدي وظيفته بجمال.</p>'],
  // Contact banner
  ['>Ready to Begin</div>', '>جاهزون للبدء</div>'],
  ["Let's Build Something<br>Extraordinary.", 'لنبنِ معاً<br>شيئاً استثنائياً.'],
  ['Open WhatsApp', 'افتح واتساب'],
  ['>Call +966 58 033 0627</a>', '>اتصل +966 58 033 0627</a>'],
  // Footer
  ['Integrated Design–Build solutions transforming ambitious architectural concepts into inspiring realities across Saudi Arabia.',
   'حلول تصميم وتنفيذ متكاملة تُحوّل المفاهيم المعمارية الطموحة إلى واقع ملهم في جميع أنحاء المملكة العربية السعودية.'],
  ['>Join the IQ</div>', '>انضم إلى IQ</div>'],
  ['placeholder="Your email address"', 'placeholder="بريدك الإلكتروني"'],
  ['>Subscribe</button>', '>اشترك</button>'],
  ['>Thank you — monthly updates, strictly no spam.</p>', '>شكراً لك — تحديثات شهرية، دون أي رسائل مزعجة.</p>'],
  ['>Services</div>', '>الخدمات</div>'],
  ['>Interior Design</a>', '>التصميم الداخلي</a>'],
  ['>Fit-Out</a>', '>التشطيبات</a>'],
  ['>Engineering &amp; MEP</a>', '>الهندسة والأنظمة الكهروميكانيكية</a>'],
  ['>Furniture Solutions</a>', '>حلول الأثاث</a>'],
  ['>Project Management</a>', '>إدارة المشاريع</a>'],
  ['>Company</div>', '>الشركة</div>'],
  ['>About Us</a>', '>من نحن</a>'],
  ['>All Services</a>', '>جميع الخدمات</a>'],
  ['>Terms &amp; Conditions</a>', '>الشروط والأحكام</a>'],
  ['>Contact</a>', '>تواصل معنا</a>'],
  ['>Find Us</div>', '>موقعنا</div>'],
  ['>Address</div>', '>العنوان</div>'],
  ['>Riyadh, KSA.</p>', '>الرياض، المملكة العربية السعودية.</p>'],
  ['>Email</div>', '>البريد الإلكتروني</div>'],
  ['>Phone — Ibrahim Al Ali</div>', '>الهاتف — إبراهيم العلي</div>'],
  ['>© 2026 FurnishIQ. All rights reserved.</p>', '>© 2026 FurnishIQ. جميع الحقوق محفوظة.</p>'],
  ['>Crafted with precision in Saudi Arabia.</p>', '>صُنع بدقة في المملكة العربية السعودية.</p>'],
];

// Note: >Interior Design</h3> / >Fit-Out</h3> / etc. (the services-grid
// headings) and >Interior Design</a> / >Fit-Out</a> / etc. (the footer
// links) are DIFFERENT substrings (different closing tag) and both need
// their own pair — that's intentional, not a duplicate.

let missed = [];
for (const [en, ar] of pairs) {
  if (!c.includes(en)) { missed.push(en); continue; }
  c = c.split(en).join(ar);
}

fs.writeFileSync(fp, c, 'utf8');
if (missed.length) {
  console.log('MISSED (string not found, check exact match):');
  missed.forEach(m => console.log(' -', m));
  process.exit(1);
} else {
  console.log('all', pairs.length, 'pairs applied');
}
```

Run it:
```bash
node scripts/ar-translate-home.js
```

If it reports any `MISSED` entries, open `home.ar.dc.html`, find why the exact substring didn't match (usually whitespace or an HTML entity difference from the source read earlier in this plan), fix the pair in the script, and re-run against a fresh `cp` of the file from Step 1 (re-running on an already-transformed file is safe for entries that already matched, since `.split().join()` on a string that's already been replaced simply won't find the old English text again — but always re-check the MISSED list is empty before moving on).

- [ ] **Step 5: Verify no untranslated marketing copy remains**

```bash
grep -oE '>[A-Za-z][A-Za-z ,.\x27&;-]{15,}<' Furnishiq.net/home.ar.dc.html
```

Expected: no output, or only lines that are legitimately meant to stay in Latin script (email addresses, phone number labels already translated with the number itself in Latin digits, `FurnishIQ` brand mentions, the `English` switcher label). Anything else is a missed translation — go back to Step 4 and add the missing pair.

- [ ] **Step 6: Visual + functional verification**

Write `test-ar-home.js` to the scratchpad directory:

```js
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });

  await page.goto('http://localhost:8532/home.ar.dc.html', { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);

  const dir = await page.evaluate(() => document.documentElement.getAttribute('dir'));
  console.log('dir attribute:', dir);

  const h1Text = await page.locator('h1').first().textContent();
  console.log('h1 text:', h1Text);

  const switchLink = await page.locator('[data-lang-switch]').first().getAttribute('href');
  console.log('switcher href:', switchLink);

  await page.screenshot({ path: 'home-ar.png', fullPage: false });
  console.log('console/page errors:', JSON.stringify(errors));
  await browser.close();
})();
```

Run against the local server (start it if not already running):
```bash
python -m http.server 8532 --directory Furnishiq.net &
node test-ar-home.js
```

Expected: `dir attribute: rtl`, `h1 text` contains the Arabic headline, `switcher href: /`, zero errors. View the screenshot and visually confirm the page reads right-to-left, the champagne/walnut palette is unchanged, and no Latin placeholder text (like an untranslated "Lorem" or leftover English sentence) is visible.

- [ ] **Step 7: Commit**

```bash
git add Furnishiq.net/home.ar.dc.html
git commit -m "Add home.ar.dc.html — Arabic RTL homepage"
```

---

### Task 5: Create `contact.ar.dc.html`

**Files:**
- Create: `Furnishiq.net/contact.ar.dc.html`

**Interfaces:**
- Consumes: `Furnishiq.net/contact.dc.html` (Task 1's version) as the source to duplicate.
- Produces: a fully translated, RTL Arabic contact page at this path, which Task 2's `/ar/contact` rewrite serves.

- [ ] **Step 1: Duplicate the source file**

```bash
cp Furnishiq.net/contact.dc.html Furnishiq.net/contact.ar.dc.html
```

- [ ] **Step 2: Apply mechanical RTL/meta transforms**

Create `scripts/ar-transform-contact.js` in the scratchpad directory:

```js
const fs = require('fs');
const fp = 'Furnishiq.net/contact.ar.dc.html';
let c = fs.readFileSync(fp, 'utf8');

c = c.replace('<html>', '<html dir="rtl" lang="ar">');
c = c.split("font-family:'Lama Sans',sans-serif").join("font-family:'GE SS Two','Arial',sans-serif");

c = c.replace(
  '<title>Contact FurnishIQ | Start Your Design Project</title>',
  '<title>تواصل مع FurnishIQ | ابدأ مشروع التصميم الخاص بك</title>'
);
c = c.replace(
  '<meta name="description" content="Get in touch with FurnishIQ\'s design-build team in Saudi Arabia. Share your project and receive a response from a senior consultant within one working day.">',
  '<meta name="description" content="تواصل مع فريق التصميم والتنفيذ في FurnishIQ بالمملكة العربية السعودية. شاركنا تفاصيل مشروعك واحصل على رد من استشاري أول خلال يوم عمل واحد.">'
);
c = c.replace(
  '<link rel="canonical" href="https://www.furnishiq.net/contact">',
  '<link rel="canonical" href="https://www.furnishiq.net/ar/contact">'
);

// Internal links stay in Arabic — lock them to /ar equivalents.
// MUST run before the switcher flip below, for the same reason as
// home.ar.dc.html's transform script: both target bare href="/", so
// locking first (while the switcher still reads href="/ar/contact" from
// the source copy) means the switcher is untouched by this blanket rule.
c = c.split('href="/contact"').join('href="/ar/contact"');
c = c.split('href="/"').join('href="/ar"');

// Language switcher now points back to English. Runs last.
c = c.replace(
  '<a href="/ar/contact" data-nav-link data-lang-switch',
  '<a href="/contact" data-nav-link data-lang-switch'
);
c = c.replace('>عربي</a>', '>English</a>');

fs.writeFileSync(fp, c, 'utf8');
console.log('mechanical transform applied');
```

Run it:
```bash
node scripts/ar-transform-contact.js
```

- [ ] **Step 3: Verify the mechanical transform**

```bash
grep -c 'dir="rtl" lang="ar"' Furnishiq.net/contact.ar.dc.html
```
Expected: `1`

```bash
grep -c "Lama Sans" Furnishiq.net/contact.ar.dc.html
```
Expected: `0`

- [ ] **Step 4: Translate the copy**

Create `scripts/ar-translate-contact.js` in the scratchpad directory:

```js
const fs = require('fs');
const fp = 'Furnishiq.net/contact.ar.dc.html';
let c = fs.readFileSync(fp, 'utf8');

const pairs = [
  // Nav (shared labels with home)
  ['>Services</a>', '>الخدمات</a>'],
  ['>Portfolio</a>', '>أعمالنا</a>'],
  ['>Process</a>', '>منهجيتنا</a>'],
  ['>Insights</a>', '>المقالات</a>'],
  ['>Request a Consultation</a>', '>اطلب استشارة</a>'],
  // Hero
  ['>Contact FurnishIQ</span>', '>تواصل مع FurnishIQ</span>'],
  ['Every great space</span>', 'كل مساحة استثنائية</span>'],
  ['begins with a</span>', 'تبدأ</span>'],
  ['conversation.</span>', 'بحوار.</span>'],
  ['>Now accepting projects</span>', '>نستقبل مشاريع جديدة حالياً</span>'],
  ["Tell us what you're planning — a villa, an office, a full commercial fit-out. A senior consultant replies within one working day.",
   'أخبرنا بما تخطط له — فيلا، مكتب، أو تشطيب تجاري متكامل. يرد عليك استشاري أول خلال يوم عمل واحد.'],
  ['>Home</a>', '>الرئيسية</a>'],
  ['>Contact</span>', '>تواصل معنا</span>'],
  // Channel strip
  ['>Email</div>', '>البريد الإلكتروني</div>'],
  ['>Briefs, drawings &amp; RFPs</div>', '>الملخصات والمخططات وطلبات العروض</div>'],
  ['>Phone</div>', '>الهاتف</div>'],
  ['>Ibrahim Al Ali — Projects</div>', '>إبراهيم العلي — المشاريع</div>'],
  ['>WhatsApp</div>', '>واتساب</div>'],
  ['>Message us directly</div>', '>راسلنا مباشرة</div>'],
  ['>Fastest first response</div>', '>أسرع رد أولي</div>'],
  ['>Studio Hours</div>', '>ساعات العمل</div>'],
  ['>Sun – Thu · 9:00 – 18:00</div>', '>الأحد – الخميس · 9:00 – 18:00</div>'],
  ['>Riyadh, Saudi Arabia (AST)</div>', '>الرياض، المملكة العربية السعودية (بتوقيت السعودية)</div>'],
  // Form section
  ['>Start Your Project</span>', '>ابدأ مشروعك</span>'],
  [">Tell us about the space you're imagining.</h2>", '>أخبرنا عن المساحة التي تتخيلها.</h2>'],
  ["Share a few details and we'll come back with a clear point of view — scope, timeline, and a budget roadmap. No obligation, no generic sales deck.",
   'شاركنا بعض التفاصيل وسنعود إليك برؤية واضحة — النطاق، الجدول الزمني، وخارطة طريق مالية. دون أي التزام، ودون عروض تسويقية عامة.'],
  ['>Response</span>', '>الرد</span>'],
  ['>Within one working day</span>', '>خلال يوم عمل واحد</span>'],
  ['>Coverage</span>', '>التغطية</span>'],
  ['>All regions of Saudi Arabia</span>', '>جميع مناطق المملكة العربية السعودية</span>'],
  ['>Languages</span>', '>اللغات</span>'],
  ['>English &amp; العربية</span>', '>العربية والإنجليزية</span>'],
  [">I'm interested in *</div>", '>أنا مهتم بـ *</div>'],
  ["SERVICES = ['Interior Design', 'Fit-Out', 'Engineering & MEP', 'Furniture', 'Full Turnkey'];",
   "SERVICES = ['التصميم الداخلي', 'التشطيبات', 'الهندسة والأنظمة الكهروميكانيكية', 'الأثاث', 'التسليم المتكامل'];"],
  ["BUDGETS = ['Under 250K', '250K – 1M', '1M – 5M', '5M+'];",
   "BUDGETS = ['أقل من 250 ألف', '250 ألف – 1 مليون', '1 مليون – 5 ملايين', 'أكثر من 5 ملايين'];"],
  ['>Full Name *</label>', '>الاسم الكامل *</label>'],
  ['placeholder="Sarah Al-Rashid"', 'placeholder="سارة الراشد"'],
  ['>Company <span', '>الشركة <span'],
  ['>(optional)</span>', '>(اختياري)</span>'],
  ['placeholder="Company name"', 'placeholder="اسم الشركة"'],
  ['>Email Address *</label>', '>البريد الإلكتروني *</label>'],
  ['>Phone Number *</label>', '>رقم الهاتف *</label>'],
  ['>Estimated budget <span', '>الميزانية التقديرية <span'],
  ['>(SAR, optional)</span>', '>(ريال سعودي، اختياري)</span>'],
  ['>About your project *</label>', '>عن مشروعك *</label>'],
  ["placeholder=\"Location, approximate size, and what you'd like to achieve…\"",
   'placeholder="الموقع، المساحة التقريبية، وما ترغب في تحقيقه…"'],
  ['id="id-submit-btn-label">Send Inquiry</span>', 'id="id-submit-btn-label">إرسال الطلب</span>'],
  ["btnLabel.textContent = 'Sending…';", "btnLabel.textContent = 'جارٍ الإرسال…';"],
  ["btnLabel.textContent = 'Send Inquiry';", "btnLabel.textContent = 'إرسال الطلب';"],
  ['>Your details stay with FurnishIQ. Never shared, never spammed.</p>',
   '>تبقى بياناتك لدى FurnishIQ فقط. لا تتم مشاركتها أو استخدامها لإرسال رسائل مزعجة.</p>'],
  ['>Thank you, {{ doneName }}.</h3>', '>شكراً لك، {{ doneName }}.</h3>'],
  ["|| 'friend';", "|| 'صديقنا';"],
  ['>Your inquiry is with our consulting team. Expect a personal reply within one working day — usually much sooner.</p>',
   '>طلبك الآن لدى فريق الاستشارات لدينا. توقع رداً شخصياً خلال يوم عمل واحد — وغالباً أسرع من ذلك.</p>'],
  ['>Send another inquiry</button>', '>إرسال طلب آخر</button>'],
  ["alert('Something went wrong — please try again or email us directly at info@furnishiq.net');",
   "alert('حدث خطأ ما — يرجى المحاولة مرة أخرى أو مراسلتنا مباشرة على info@furnishiq.net');"],
  // What happens next
  ['>After You Reach Out</span>', '>بعد تواصلك معنا</span>'],
  ['>What happens next.</h2>', '>ماذا يحدث بعد ذلك.</h2>'],
  ['>We Listen</h4>', '>نستمع</h4>'],
  ['>Within 24 Hours</p>', '>خلال 24 ساعة</p>'],
  ['A senior consultant — not a call center — reviews your inquiry and schedules a discovery conversation at a time that suits you.',
   'يراجع استشاري أول — وليس مركز اتصال — طلبك ويحدد موعداً لمحادثة استكشافية في الوقت الذي يناسبك.'],
  ['>We Visit</h4>', '>نزور</h4>'],
  ['>Site &amp; Scope</p>', '>الموقع والنطاق</p>'],
  ["We survey the space, understand how you'll use it, and align on ambition, constraints, and timeline — face to face where possible.",
   'نعاين المساحة، نفهم كيفية استخدامك لها، ونتفق على الطموح والقيود والجدول الزمني — وجهاً لوجه كلما أمكن.'],
  ['>We Propose</h4>', '>نقترح</h4>'],
  ['>Plan &amp; Roadmap</p>', '>الخطة وخارطة الطريق</p>'],
  ['You receive a clear proposal — scope, photoreal direction, and a comprehensive budget roadmap — before committing to anything.',
   'تحصل على عرض واضح — النطاق، التوجه التصويري الواقعي، وخارطة طريق مالية شاملة — قبل الالتزام بأي شيء.'],
  // Visit section
  ['>Visit the Studio</span>', '>زر الاستوديو</span>'],
  ['See materials.<br>Touch finishes.', 'شاهد المواد.<br>المس التشطيبات.'],
  ['Some decisions deserve to be made in person. Book a studio session to explore material libraries, finish samples, and past project work.',
   'بعض القرارات تستحق أن تُتخذ حضورياً. احجز جلسة في الاستوديو لاستكشاف مكتبات المواد، عينات التشطيبات، وأعمال المشاريع السابقة.'],
  ['>Address</div>', '>العنوان</div>'],
  ['>Riyadh, Kingdom of Saudi Arabia</p>', '>الرياض، المملكة العربية السعودية</p>'],
  ['>By Appointment</div>', '>بموعد مسبق</div>'],
  ['>Sunday – Thursday · 9:00 – 18:00</p>', '>الأحد – الخميس · 9:00 – 18:00</p>'],
  ['Book a Studio Visit', 'احجز زيارة للاستوديو'],
  ['>Riyadh · 24.7136° N, 46.6753° E</span>', '>الرياض · 24.7136° شمالاً، 46.6753° شرقاً</span>'],
  // Footer (shared with home)
  ['Integrated Design–Build solutions transforming ambitious architectural concepts into inspiring realities across Saudi Arabia.',
   'حلول تصميم وتنفيذ متكاملة تُحوّل المفاهيم المعمارية الطموحة إلى واقع ملهم في جميع أنحاء المملكة العربية السعودية.'],
  ['>Join the IQ</div>', '>انضم إلى IQ</div>'],
  ['placeholder="Your email address"', 'placeholder="بريدك الإلكتروني"'],
  ['>Subscribe</button>', '>اشترك</button>'],
  ['>Thank you — monthly updates, strictly no spam.</p>', '>شكراً لك — تحديثات شهرية، دون أي رسائل مزعجة.</p>'],
  ['>Services</div>', '>الخدمات</div>'],
  ['>Interior Design</a>', '>التصميم الداخلي</a>'],
  ['>Fit-Out</a>', '>التشطيبات</a>'],
  ['>Engineering &amp; MEP</a>', '>الهندسة والأنظمة الكهروميكانيكية</a>'],
  ['>Furniture Solutions</a>', '>حلول الأثاث</a>'],
  ['>Project Management</a>', '>إدارة المشاريع</a>'],
  ['>Company</div>', '>الشركة</div>'],
  ['>About Us</a>', '>من نحن</a>'],
  ['>All Services</a>', '>جميع الخدمات</a>'],
  ['>Terms &amp; Conditions</a>', '>الشروط والأحكام</a>'],
  ['>Contact</a>', '>تواصل معنا</a>'],
  ['>Find Us</div>', '>موقعنا</div>'],
  ['>Riyadh, KSA.</p>', '>الرياض، المملكة العربية السعودية.</p>'],
  ['>Phone — Ibrahim Al Ali</div>', '>الهاتف — إبراهيم العلي</div>'],
  ['>© 2026 FurnishIQ. All rights reserved.</p>', '>© 2026 FurnishIQ. جميع الحقوق محفوظة.</p>'],
  ['>Crafted with precision in Saudi Arabia.</p>', '>صُنع بدقة في المملكة العربية السعودية.</p>'],
];

// Note: >Insights</a> is intentionally listed only once, in the nav
// section above — the footer's "Insights" link is the identical
// substring, and .split().join() replaces every occurrence globally in
// one pass, so a second identical pair here would find nothing left to
// replace and wrongly trip the MISSED check below. Same reasoning covers
// >Portfolio</a> and >Contact</a>: >Contact</a> above handles the
// footer's self-link (the nav breadcrumb uses >Contact</span>, a
// different substring, already covered separately).

let missed = [];
for (const [en, ar] of pairs) {
  if (!c.includes(en)) { missed.push(en); continue; }
  c = c.split(en).join(ar);
}

fs.writeFileSync(fp, c, 'utf8');
if (missed.length) {
  console.log('MISSED (string not found, check exact match):');
  missed.forEach(m => console.log(' -', m));
  process.exit(1);
} else {
  console.log('all', pairs.length, 'pairs applied');
}
```

Run it:
```bash
node scripts/ar-translate-contact.js
```

Fix any `MISSED` entries the same way as Task 4 Step 4.

- [ ] **Step 5: Verify no untranslated marketing copy remains**

```bash
grep -oE '>[A-Za-z][A-Za-z ,.\x27&;-]{15,}<' Furnishiq.net/contact.ar.dc.html
```

Expected: no output beyond legitimate Latin exceptions (see Task 4 Step 5). Fix any real misses found here.

- [ ] **Step 6: Visual + functional verification**

Write `test-ar-contact.js` to the scratchpad directory:

```js
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });

  await page.goto('http://localhost:8532/contact.ar.dc.html', { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);

  console.log('dir attribute:', await page.evaluate(() => document.documentElement.getAttribute('dir')));

  // Fill and check the form renders with Arabic labels, without actually submitting
  // (submitting would hit the real /api/send-email endpoint).
  const nameLabel = await page.locator('label').first().textContent();
  console.log('first form label:', nameLabel);

  const switchLink = await page.locator('[data-lang-switch]').first().getAttribute('href');
  console.log('switcher href:', switchLink);

  await page.screenshot({ path: 'contact-ar.png', fullPage: false });
  console.log('console/page errors:', JSON.stringify(errors));
  await browser.close();
})();
```

```bash
node test-ar-contact.js
```

Expected: `dir attribute: rtl`, Arabic form label, `switcher href: /contact`, zero errors. View the screenshot.

- [ ] **Step 7: Commit**

```bash
git add Furnishiq.net/contact.ar.dc.html
git commit -m "Add contact.ar.dc.html — Arabic RTL contact page"
```

---

### Task 6: Arabic WhatsApp pre-fill in the shared floating button

**Files:**
- Modify: `Furnishiq.net/floating-buttons.js`

**Interfaces:**
- Consumes: `document.documentElement.lang`, set to `"ar"` by Task 4/5's `<html dir="rtl" lang="ar">` transform.
- Produces: no change to the function signature `window.FIQMobileNav` consumers rely on elsewhere — this only changes the WhatsApp `href` value computed inside `floating-buttons.js`'s own `init()`.

- [ ] **Step 1: Add the Arabic message variant**

In `Furnishiq.net/floating-buttons.js`, find:

```js
  var WA_NUMBER = '966580330627';
  var WA_TEXT = encodeURIComponent('Hello FurnishIQ, I would like to know more about your design and fit-out services.');
```

Replace with:

```js
  var WA_NUMBER = '966580330627';
  var WA_TEXT_EN = 'Hello FurnishIQ, I would like to know more about your design and fit-out services.';
  var WA_TEXT_AR = 'مرحباً FurnishIQ، أود معرفة المزيد عن خدمات التصميم والتشطيبات لديكم.';
  var WA_TEXT = encodeURIComponent(document.documentElement.lang === 'ar' ? WA_TEXT_AR : WA_TEXT_EN);
```

- [ ] **Step 2: Verify**

```bash
grep -c "WA_TEXT_AR" Furnishiq.net/floating-buttons.js
```
Expected: `2` (one declaration, one usage in the ternary).

Write a quick check to the scratchpad and run it:

```js
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:8532/home.ar.dc.html', { waitUntil: 'networkidle' });
  const href = await page.locator('.fiq-float-wa').getAttribute('href');
  console.log('AR page WhatsApp href:', decodeURIComponent(href));
  await browser.close();
})();
```
Expected: the href contains the Arabic message text.

Re-run the existing `test-floating.js` (from the floating-buttons feature work) against `home.dc.html` to confirm the English page still gets the English message — this is a shared file, so a regression here would break every page, not just the Arabic ones.

- [ ] **Step 3: Commit**

```bash
git add Furnishiq.net/floating-buttons.js
git commit -m "Use Arabic WhatsApp pre-fill message on Arabic pages"
```

---

### Task 7: End-to-end regression across all 4 pilot page variants

**Files:**
- None modified — verification only.

**Interfaces:**
- Consumes: all of Tasks 1-6.

- [ ] **Step 1: Full regression sweep**

Write `test-bilingual-pilot.js` to the scratchpad directory:

```js
const { chromium } = require('playwright');

const pages = ['home.dc.html', 'home.ar.dc.html', 'contact.dc.html', 'contact.ar.dc.html'];

(async () => {
  const browser = await chromium.launch();
  let allOk = true;

  for (const p of pages) {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    const errors = [];
    page.on('pageerror', e => errors.push('pageerror: ' + e.message));
    page.on('console', m => { if (m.type() === 'error' && !m.text().includes('ipapi.co') && !m.text().includes('404')) errors.push('console: ' + m.text()); });

    await page.goto('http://localhost:8532/' + p, { waitUntil: 'networkidle' });
    await page.waitForTimeout(400);

    const dir = await page.evaluate(() => document.documentElement.getAttribute('dir') || 'ltr');
    const toggle = page.locator('.fiq-nav-toggle');
    const toggleVisible = await toggle.first().isVisible().catch(() => false);
    let overlayOpen = false, switcherHref = null;
    if (await toggle.count()) {
      await toggle.first().click();
      await page.waitForTimeout(400);
      overlayOpen = await page.locator('.fiq-nav-overlay').evaluate(el => el.classList.contains('fiq-nav-overlay--open'));
      switcherHref = await page.locator('.fiq-nav-overlay-links [data-lang-switch]').getAttribute('href').catch(() => null);
    }
    const waHref = await page.locator('.fiq-float-wa').getAttribute('href').catch(() => null);

    const ok = toggleVisible && overlayOpen && switcherHref && waHref && errors.length === 0;
    if (!ok) allOk = false;
    console.log((ok ? 'PASS' : 'FAIL') + '  ' + p + '  dir=' + dir + ' overlayOpen=' + overlayOpen + ' switcherHref=' + switcherHref + (errors.length ? '  ERRORS: ' + JSON.stringify(errors) : ''));
    await page.close();
  }

  await browser.close();
  console.log(allOk ? '\nALL PAGES PASS' : '\nSOME PAGES FAILED');
})();
```

```bash
node test-bilingual-pilot.js
```

Expected: `ALL PAGES PASS`, with `home.dc.html`/`contact.dc.html` showing `dir=ltr` and their mobile-overlay switcher pointing to the `/ar` equivalents, and `home.ar.dc.html`/`contact.ar.dc.html` showing `dir=rtl` with the switcher pointing back to the English paths.

- [ ] **Step 2: Confirm `vercel.json` still parses and the routing counts are what Task 2 expects**

```bash
node -e "const c = require('./vercel.json'); console.log(c.redirects.length, c.rewrites.length);"
```
Expected: `37 17`

- [ ] **Step 3: Stop the local server, report done**

```bash
lsof -ti:8532 -sTCP:LISTEN | xargs -r kill 2>/dev/null || true
```

(No commit — this task is verification-only. If any check fails, return to the relevant earlier task, fix, and re-run this sweep before considering the plan complete.)

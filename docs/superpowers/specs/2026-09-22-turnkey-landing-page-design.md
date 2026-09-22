# Turnkey Landing Page — Design Spec

Date: 2026-09-22

## Purpose

Build a new, standalone landing page for FurnishIQ based on the client-provided
"Furnish IQ Landing Page" / "Sila Creative Landing Page" PDF spec. It is a
campaign-style page (e.g. for paid traffic) promoting the "Integrated Turnkey
Engineering Package" (design → fit-out → furnishing, delivered by a single
partner). It coexists with the existing homepage — it does not replace it.

Source content: `Furnish IQ Landing Page.pdf` (provided by the user), which
contains both the Arabic copy (primary) and an English translation of the same
structure.

## Output

Two new bilingual page files, following the site's existing page-pair
convention (see `contact.dc.html` / `contact.ar.dc.html`):

- `Furnishiq.net/landing-turnkey.dc.html` — English
- `Furnishiq.net/landing-turnkey.ar.dc.html` — Arabic (`dir="rtl"`, primary
  per the PDF)

No plain (non-`.dc.html`) sibling is required — every other page pair in the
repo ships only the `.dc.html` variant.

## Platform constraint (critical — confirmed by codebase research)

Every `.dc.html` page on this site runs on a real, load-bearing micro
component-runtime implemented in `support.js` ("dc-runtime"), NOT plain
static HTML. This is not optional scaffolding — it is the actual rendering
engine:

- `support.js` loads React 18 + ReactDOM, waits for `DOMContentLoaded`, finds
  the page's `<x-dc>...</x-dc>` block plus a sibling
  `<script type="text/x-dc" data-dc-script>`, compiles the `<x-dc>` markup
  into render functions (resolving `{{ expr }}` bindings, `sc-if`/`sc-for`
  directives, camelCase event attrs like `onSubmit`/`onClick`), and mounts a
  React root replacing `<x-dc>`.
- The `data-dc-script` block contains exactly one
  `class Component extends DCLogic { state = {...}; renderVals() {...};
  componentDidMount() {...} }`. `renderVals()` returns the object whose keys
  (`onFormSubmit`, `formNotDone`, etc.) the `{{ }}` bindings in the template
  resolve to. `componentDidMount()` holds real vanilla-DOM logic (nav scroll
  sync, `IntersectionObserver` for `data-reveal`, event listeners) even
  though it executes inside a React lifecycle hook.
- `<helmet>` (first child of `<x-dc>`) holds all `<style>` blocks — it gets
  hoisted into `<head>` by the runtime.

**Both new pages must follow this exact pattern** — `<x-dc>` wrapper,
`<helmet>` with design-token `:root` CSS copied verbatim from an existing
page (e.g. `contact.dc.html`), then markup, then a single
`class Component extends DCLogic` in a `data-dc-script` block. Do not attempt
a plain-HTML/vanilla-`<script>` version — it will not render (raw `{{ }}`
template syntax would show up broken on the page).

## Required includes (in `<head>`, matching every existing page)

```
<script src="./support.js" defer></script>
<script src="./nav-mobile.js" defer></script>
<script src="./floating-buttons.js" defer></script>
<script src="./analytics-events.js" defer></script>
<link rel="preload" as="font" type="font/ttf" href="_ds/furnishiq-design-system-.../LamaSans-Medium_English.ttf" crossorigin>
```

Plus standard `<meta charset>`, viewport, canonical/hreflang pair
(`landing-turnkey` EN ↔ `ar/landing-turnkey` AR, `x-default` → EN), and a
`<title>`/`<meta name="description">` written for this page (not copy-pasted
from contact).

Tracking snippets (GTM, Meta Pixel, LinkedIn Insight Tag) at the top of
`<head>`/`<body>` should be copied verbatim from `contact.dc.html` — they are
site-wide, not page-specific.

`floating-buttons.js` (sticky WhatsApp + back-to-top) needs no extra markup —
it self-mounts. This directly satisfies the PDF's "Sticky WhatsApp Button"
technical note; nothing new needs to be built for it.

## Nav header

Reuse the existing nav markup/behavior verbatim from `contact.dc.html`
(`id="id-nav"`, `id-logo-w`/`id-logo-d` logo swap, `data-nav-link` items,
language-switch link, CTA button) and the `syncNav()` logic in
`componentDidMount`. Links: Home, About Us, Services, Projects, Insights,
language switch, CTA → `#form`.

## Sections (content from the PDF; Arabic verbatim, English is the PDF's own translation)

1. **Hero**
   - Headline (AR): "في الـ96... من المخطط إلى تسليم المفتاح."
   - Sub: "كل احتياجات مساحتك من التصميم الداخلي، التشطيبات الفاخرة
     (Fit-out)، والتأثيث المتكامل.. مع جهة واحدة تضمن لك دقة التنفيذ
     والتطابق التام مع رؤيتك."
   - CTA 1 (primary): "ابدأ مشروعك مع فرينيش آي كيو" → `#form`
   - CTA 2 (secondary): "اكتشف خدماتنا" → `#services`
   - Style: dark walnut/charcoal background, warm interior photo (Unsplash
     set already used sitewide), `data-reveal` word-by-word headline
     animation matching `contact.dc.html`'s hero pattern.

2. **Needs section** (`id="needs"`) — headline "وش تحتاج فرينيش آي كيو تنجز
   لمساحتك؟" + 3 cards in a grid (no carousel library exists on the site;
   3 items read fine as a static 3-up grid — avoids introducing new JS):
   - "أبغى تجهيز مساحتي بالكامل.. من التصميم إلى تسليم المفتاح." →
     "احصل على استشارة" (→ `#form`)
   - "أبغى تصميم داخلي" → "اكتشف الخدمة" (→ `#service`)
   - "عندي مساحة (عظم) وأبحث عن تشطيب (Fit-out) وتأثيث فاخر." →
     "احصل على استشارة" (→ `#form`)

3. **Service/Package section** (`id="service"`) — headline "الباقة الهندسية
   المتكاملة (تسليم مفتاح)". Body: "ندير كافة مراحل تجهيز مساحتك من الفكرة
   إلى الواقع." + pricing line "باقات التصميم الداخلي السكني فقط تبدأ من
   29.99 ريال/م²." + disclaimer "(يتم تقديم عروض منفصلة لخدمات التنفيذ،
   التشطيبات، والتأثيث حسب نطاق ومتطلبات مشروعك)." Then 3 distinct
   inclusions (dedupe the PDF's accidental repeat of the first bullet) as an
   icon+text list:
   - تصميم داخلي 3D واقعي
   - تنفيذ وتشطيبات (Fit-out) فاخرة
   - توريد وتأثيث متكامل
   - CTA: "احصل على استشارة هندسية مجانية الان" → `#form`

4. **Video/media section** — no real video asset exists on the site
   (confirmed — no `<video>`/mp4/YouTube/Vimeo usage anywhere). Build as a
   static full-bleed image (Unsplash interior photo) with a centered,
   non-functional play-button overlay styled per the design system, plus the
   PDF's copy: headline "تصميم تراه.. وواقع تعيش فخامته", body "شاهد كيف
   نترجم المخططات الهندسية إلى مساحات تنبض بالحياة..." CTA "احجز استشارتك
   الهندسية" → `#form`.

5. **Our Work** (`id="work"`) — headline "أعمال صُممت لتُعاش", sub "شوف كيف
   تتحول أفكارنا إلى مشاريع". 3–4 image tiles using the site's existing
   curated Unsplash interior-photography set (same URLs already used on
   `projects.dc.html`/`contact.dc.html`, picking ones not already used
   elsewhere on this new page), each linking to `/projects`.

6. **USP's** (`id="usps"`) — headline "ليش تختار فرينيش آي كيو؟", sub
   "مساحتك بالكامل.. تحت إشراف جهة هندسية واحدة لتجربة تسليم مفتاح خالية من
   التشتت." Dark charcoal background (matches PDF's dark USP mockup), 5
   value props as icon cards:
   - منظومة هندسية متكاملة
   - جهة واحدة من التصميم للتشطيب
   - دقة وتنسيق بتقنية (BIM)
   - حلول مخصصة لمساحتك
   - ابدأ مشروعك بأفضل قيمة (29.99 ريال/م²، تسعير منفصل للتنفيذ/التشطيب/التأثيث)

7. **Form section** (`id="form"`) — headline "جاهز تبدأ رحلة تجهيز
   مساحتك؟", sub per PDF. Fields: Full name, phone number, "وش تحتاج؟"
   dropdown with options (Integrated turnkey / Interior design only /
   Fit-out for existing blueprint / Luxury furniture / Other). CTA: "ابدأ
   مشروعك مع فرينيش آي كيو".
   - Submission: same pattern as `contact.dc.html`'s `onFormSubmit` —
     client-side validation, honeypot field, `fetch('/api/send-email', {
     method: 'POST', headers: {'Content-Type': 'application/json'}, body:
     JSON.stringify(payload) })`, GTM `dataLayer.push({event:
     'generate_lead', form_name: 'landing_turnkey', ...})` on success.
   - On success: **inline thank-you state** (per user decision — matches
     existing contact form's UX pattern of swapping form content in place),
     using the PDF's thank-you copy: "تم استلام طلبك" / "مساحتك أخذت أول
     خطوة نحو الفخامة مع فرينيش آي كيو." / body about the engineering team
     reviewing details. Do NOT redirect to a separate thank-you page for
     this form (contact.dc.html actually redirects to `/thank-you`, but the
     user's decision for this page was an inline message — implement inline
     `setState`-driven success view instead of `window.location.href`
     redirect).

8. Floating WhatsApp + back-to-top — free via `floating-buttons.js`, no
   additional work.

## Design system compliance

Apply `CLAUDE.md`'s mandatory rules throughout: Walnut/Dark Walnut/Bronze/
Stone/Charcoal palette only, no gradients, no cool greys, Lama Sans (EN) /
GE SS Two (AR) only, `border-radius: 0` everywhere, section padding
64–128px, luxury-ease motion (`cubic-bezier(0.25,0.46,0.45,0.94)`,
200–700ms, fade+translateY only, respecting `prefers-reduced-motion`), CTAs
uppercase with `letter-spacing: 0.2em`, section labels uppercase 10–11px,
no exclamation marks/superlatives/emoji, Brand Green reserved for logo only.

## Arabic (RTL) page specifics

- `<html lang="ar" dir="rtl">`
- Body/headings use `--font-arabic` (GE SS Two) instead of `--font-display`/
  `--font-body`
- Mirror layout per existing `.ar.dc.html` pages (check `contact.ar.dc.html`
  for the established RTL adaptation pattern — flipped nav order, mirrored
  spacing, etc.) rather than reinventing RTL handling from scratch.
- hreflang / canonical pointing at `/ar/landing-turnkey`.

## Out of scope

- No real video asset/embed (placeholder image section only, per user
  decision — can be swapped for a real embed later).
- No new JS carousel library — Needs and Our Work sections use static
  grids, not sliders, since the PDF's mockup carousels are inspirational
  references, not literal implementation requirements, and the site has no
  existing carousel dependency to reuse.
- No changes to the existing homepage or any other existing page.
- No backend work — `/api/send-email` endpoint already exists and is reused
  as-is.

## Testing / verification

Since there's no build step, verification is manual: open both new pages
directly in a browser, confirm:
- `<x-dc>` renders correctly (no raw `{{ }}` template syntax visible)
- nav scroll behavior, language switch link, mobile nav
- `data-reveal` animations fire on scroll
- form validation, submission (can stub/inspect the `fetch` call), and the
  inline thank-you state
- floating WhatsApp button appears and works on both pages
- RTL layout on the Arabic page (text direction, mirrored spacing, correct
  font)
- responsive check at mobile width per CLAUDE.md's phone-width requirement

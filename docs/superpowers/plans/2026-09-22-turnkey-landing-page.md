# Turnkey Landing Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a new bilingual campaign landing page pair (`landing-turnkey.dc.html` EN, `landing-turnkey.ar.dc.html` AR) for FurnishIQ's Integrated Turnkey Engineering Package, matching the PDF brief's content and the site's real design/runtime conventions.

**Architecture:** Two `.dc.html` pages built on the site's existing `x-dc`/`DCLogic` React-based component runtime (`support.js`) — each page is one `class Component extends DCLogic` with `state`/`renderVals()`/`componentDidMount()`, templated via `<x-dc>` markup using `{{ }}` bindings, exactly like `contact.dc.html`. No new JS libraries, no build step, no backend changes (`/api/send-email` already exists).

**Tech Stack:** Static HTML/CSS + the site's `support.js` dc-runtime (React 18 loaded from unpkg by that runtime), `nav-mobile.js`, `floating-buttons.js`, `analytics-events.js` — all already in the repo.

**Spec:** `docs/superpowers/specs/2026-09-22-turnkey-landing-page-design.md`

## Global Constraints

- Pages must use the `<x-dc>` / `<helmet>` / `class Component extends DCLogic` pattern verbatim — plain static HTML will render broken `{{ }}` template text (spec, "Platform constraint").
- Design tokens (colors, fonts, spacing) copied verbatim from an existing page's `<helmet><style>` `:root` block — do not redefine values (spec, "Required includes").
- Colors: Walnut `#5B4636`, Dark Walnut `#3A2D25`, Bronze `#8B6B4A`, Stone `#F5F2ED`, Charcoal `#1F1F1F` only; Brand Green `#1C6B35` reserved for logo; no gradients, no cool greys (CLAUDE.md).
- Fonts: Lama Sans Medium 500 (English, local `@font-face`), GE SS Two Medium 500 (Arabic, always with `dir="rtl"`) — never CDN fonts, never serif/Jost/Inter/Roboto/Arial as primary (CLAUDE.md).
- `border-radius: 0` by default; section padding 64–128px; motion is fade+translateY only using `cubic-bezier(0.25,0.46,0.45,0.94)` 200–700ms, respecting `prefers-reduced-motion` (CLAUDE.md).
- CTAs uppercase with `letter-spacing: 0.2em`; section labels uppercase 10–11px; no exclamation marks, superlatives, or emoji (CLAUDE.md).
- Required `<head>` includes on both pages: `support.js`, `nav-mobile.js`, `floating-buttons.js`, `analytics-events.js` (all `defer`), plus the Lama Sans font preload (spec, "Required includes").
- Nav must use `.fiq-nav-links` class on the links container and a link/button with a class containing `nav-cta` — `nav-mobile.js` queries these selectors directly (`nav-mobile.js:57-58`).
- No real video embed — video section is a static image + non-functional play button overlay (spec, "Out of scope").
- No carousel library — Needs/Our Work sections are static grids (spec, "Out of scope").
- Form success state is **inline** (state-driven swap), not a redirect to `/thank-you` (spec, Section 7 — this differs from `contact.dc.html`, which does redirect).
- No changes to any existing file except `sitemap.xml` (add the two new URLs) — verify with `git status` before committing each task.

## Review Focus

- **Missing/renamed image URLs:** every Unsplash URL used must be one already proven to load elsewhere on the site (copy exact URLs from `contact.dc.html`/`projects.dc.html`, don't hand-type new Unsplash photo IDs) — a typo'd photo ID silently 404s with no visible error.
- **Empty or unsubmittable form:** dropdown with no options selected, or all fields empty — `onFormSubmit` must validate and show field errors instead of silently calling `/api/send-email` with blank data (mirror `contact.dc.html`'s validation pattern).
- **Raw template syntax visible on page:** if the `data-dc-script` block has a syntax error or the `<x-dc>` wrapper is malformed, `{{ expr }}` text renders literally instead of being evaluated — every task's verification step must screenshot/snapshot the rendered page, not just check the file compiles conceptually.
- **RTL page reusing LTR-only assumptions:** the Arabic page must not hardcode `lang="en"`, must use `--font-arabic` for text, and must not carry over any hardcoded left/right positioning that would look mirrored-wrong under `dir="rtl"` (e.g. floating WhatsApp button position — confirm `floating-buttons.js` already handles this via `document.documentElement.lang`, not page markup).
- **Broken internal links:** CTA `href="#form"`/`#service`/`#work` anchors and "Our Work" tile links to `/projects` must resolve to real IDs actually present in the same page (typo'd anchor = dead CTA button).

---

## File Structure

- Create: `Furnishiq.net/landing-turnkey.dc.html` — English landing page (full page: head, nav, 7 sections, form, DCLogic class)
- Create: `Furnishiq.net/landing-turnkey.ar.dc.html` — Arabic landing page (RTL mirror of the above, translated copy)
- Modify: `Furnishiq.net/sitemap.xml` — add both new URLs

Both `.dc.html` files are self-contained single files (matching every existing page in this repo — no shared partials/includes exist for page bodies), so there is no additional file decomposition; the "files" are the tasks' actual deliverables.

---

### Task 1: EN page scaffold — head, nav, DCLogic skeleton, hero section

**Files:**
- Create: `Furnishiq.net/landing-turnkey.dc.html`

**Interfaces:**
- Produces: `class Component extends DCLogic` with `state = { formName: '', formPhone: '', selectedNeed: '', formHoneypot: '', fieldErrors: {}, submitted: false }` and `renderVals()` returning at least `{ onFormSubmit, onNameChange, onPhoneChange, onNeedChange }` (stubs in this task; wired for real in Task 4). Later tasks in this same file append markup between the hero and the closing `</x-dc>`, and add more keys to `renderVals()`'s returned object — they don't touch Task 1's head/nav markup.

- [ ] **Step 1: Copy the head/tracking/font-face boilerplate from `contact.dc.html`**

Read `Furnishiq.net/contact.dc.html` lines 1-73 (GTM, Meta Pixel, LinkedIn Insight Tag, meta tags, font preload) and lines 74-172 (`<x-dc><helmet><style>` opening through the `@font-face` blocks and color/typography `:root` tokens). Copy this verbatim into the new file, with these changes only:
- `<title>` → `FurnishIQ | Integrated Turnkey Engineering Package`
- `<meta name="description">` → `From plan to turnkey handover in 96 days. Interior design, luxury fit-out, and furnishing — delivered by one partner, from 29.99 SAR/m².`
- `<link rel="canonical" href="https://www.furnishiq.net/landing-turnkey">`
- `<link rel="alternate" hreflang="en" href="https://www.furnishiq.net/landing-turnkey">`
- `<link rel="alternate" hreflang="ar" href="https://www.furnishiq.net/ar/landing-turnkey">`
- `<link rel="alternate" hreflang="x-default" href="https://www.furnishiq.net/landing-turnkey">`
- `<html lang="en">` (unchanged from contact.dc.html)

Keep all `<script src="./support.js" defer>`, `<script src="./nav-mobile.js" defer>`, `<script src="./floating-buttons.js" defer>`, `<script src="./analytics-events.js" defer>`, and the font preload tag exactly as in `contact.dc.html`.

- [ ] **Step 2: Copy remaining design-token CSS and nav markup**

Read `Furnishiq.net/contact.dc.html` lines 173-460 (remaining `:root` spacing/effects tokens, base element styles) and the nav header markup (search for `id="id-nav"` through the end of the `<nav>` element, roughly lines 559-650 based on prior exploration — read the actual file to get exact line numbers). Copy both verbatim into the new file's `<helmet><style>` block and immediately after `</helmet>`, respectively. Keep `id="id-nav"`, `id-logo-w`/`id-logo-d`, `data-nav-link`, `.fiq-nav-links`, `id="id-nav-cta"` (with a class containing `nav-cta`) exactly as-is — `nav-mobile.js` and the `syncNav()` logic (Task 1 Step 4) depend on these exact hooks. Update the language-switch link (`data-lang-switch`) href to `/ar/landing-turnkey`. Update all nav `href`s to point at this page's own section IDs where they'd currently point at contact-page anchors (Home → `/`, About Us → `/about-us`, Services → `/services`, Projects → `/projects`, Insights → `/blog` — these are unchanged from contact.dc.html since they're global nav links).

- [ ] **Step 3: Add the hero section**

Immediately after the nav, add:

```html
<section id="hero" data-screen-label="Hero" style="position:relative;min-height:88vh;display:flex;align-items:center;background:#1F1F1F;overflow:hidden;">
  <div style="position:absolute;inset:0;background-image:url('https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=2400&q=30');background-size:cover;background-position:center;opacity:0.28;pointer-events:none;"></div>
  <div style="position:relative;z-index:1;max-width:1280px;margin:0 auto;padding:clamp(140px,14vw,180px) clamp(24px,5vw,80px) clamp(80px,8vw,120px);width:100%;">
    <span data-reveal style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);display:block;font-family:'Lama Sans',sans-serif;font-size:9px;letter-spacing:0.3em;text-transform:uppercase;color:rgba(214,194,168,0.8);margin-bottom:20px;">Turnkey Delivery</span>
    <h1 data-reveal data-reveal-delay="0.08" style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);font-family:'Lama Sans',sans-serif;font-size:clamp(34px,4.4vw,64px);font-weight:500;color:#FFFFFF;line-height:1.1;letter-spacing:-0.015em;max-width:900px;margin-bottom:24px;text-wrap:balance;">From Concept to Turnkey Delivery.</h1>
    <p data-reveal data-reveal-delay="0.16" style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);font-family:'Lama Sans',sans-serif;font-size:clamp(16px,1.6vw,19px);color:rgba(255,255,255,0.82);line-height:1.6;max-width:640px;margin-bottom:40px;">All your space needs&mdash;interior design, luxury fit-out, and turnkey furnishing&mdash;managed by a single partner dedicated to precision execution and bringing your vision to life.</p>
    <div data-reveal data-reveal-delay="0.24" style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);display:flex;gap:16px;flex-wrap:wrap;">
      <a href="#form" style="font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.2em;text-transform:uppercase;color:#1F1F1F;background:#D6C2A8;padding:19px 36px;border:1px solid #D6C2A8;text-decoration:none;transition:all 0.3s cubic-bezier(0.25,0.46,0.45,0.94);">Start Your Project with FurnishIQ</a>
      <a href="#service" style="font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.2em;text-transform:uppercase;color:#FFFFFF;background:transparent;padding:19px 36px;border:1px solid rgba(255,255,255,0.4);text-decoration:none;transition:all 0.3s cubic-bezier(0.25,0.46,0.45,0.94);">Discover Our Services</a>
    </div>
  </div>
</section>
```

- [ ] **Step 4: Add the closing `</x-dc>` and the `data-dc-script` DCLogic class**

Immediately after the hero section (content from later tasks will be inserted between hero and this closing tag), add:

```html
</x-dc>
<script type="text/x-dc" data-dc-script>
class Component extends DCLogic {
  state = {
    formName: '',
    formPhone: '',
    selectedNeed: '',
    formHoneypot: '',
    fieldErrors: {},
    submitted: false,
  };

  renderVals() {
    const self = this;
    return {
      formName: self.state.formName,
      onNameChange: (e) => self.setState({ formName: e.target.value }),
      formPhone: self.state.formPhone,
      onPhoneChange: (e) => self.setState({ formPhone: e.target.value }),
      selectedNeed: self.state.selectedNeed,
      onNeedChange: (e) => self.setState({ selectedNeed: e.target.value }),
      formHoneypot: self.state.formHoneypot,
      onHoneypotChange: (e) => self.setState({ formHoneypot: e.target.value }),
      fieldErrors: self.state.fieldErrors,
      submitted: self.state.submitted,
      onFormSubmit: (e) => {
        e.preventDefault();
      },
    };
  }

  componentDidMount() {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const nav = document.getElementById('id-nav');
    if (window.FIQMobileNav) window.FIQMobileNav(nav);
    const logoW = document.getElementById('id-logo-w');
    const logoD = document.getElementById('id-logo-d');
    const navLinks = document.querySelectorAll('[data-nav-link]');
    const navCta = document.getElementById('id-nav-cta');

    const syncNav = () => {
      const s = window.scrollY > 60;
      if (!nav) return;
      nav.style.background = s ? 'rgba(255,255,255,0.96)' : 'transparent';
      nav.style.borderBottomColor = s ? '#D6C2A8' : 'transparent';
      nav.style.backdropFilter = s ? 'blur(16px)' : 'none';
      nav.style.boxShadow = s ? '0 2px 16px rgba(58,45,37,0.06)' : 'none';
      if (logoW) logoW.style.opacity = s ? '0' : '1';
      if (logoD) logoD.style.opacity = s ? '1' : '0';
      navLinks.forEach((l) => {
        l.style.color = s ? '#1F1F1F' : '#FFFFFF';
        l.style.opacity = s ? '1' : '0.8';
      });
      if (navCta) {
        navCta.style.color = s ? '#1F1F1F' : '#FFFFFF';
        navCta.style.borderColor = s ? 'rgba(91,70,54,0.35)' : 'rgba(214,194,168,0.5)';
      }
    };
    window.addEventListener('scroll', syncNav, { passive: true });
    syncNav();

    const revealEls = document.querySelectorAll('[data-reveal]');
    if (reduced || !('IntersectionObserver' in window)) {
      revealEls.forEach((el) => {
        el.style.opacity = '1';
        el.style.transform = 'none';
      });
    } else {
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.style.opacity = '1';
              entry.target.style.transform = 'none';
              io.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.15, rootMargin: '0px 0px -60px 0px' }
      );
      revealEls.forEach((el) => io.observe(el));
    }
  }
}
</script>
```

- [ ] **Step 5: Verify the scaffold renders without errors**

Use the Playwright browser tool: navigate to `file:///D:/ProjectsClaude/FurnishIQ/Furnishiq.net/landing-turnkey.dc.html`, then check `browser_console_messages` for errors and take a `browser_snapshot`. Confirm:
- No raw `{{ }}` text visible anywhere on the page
- No console errors
- Hero headline, sub-copy, and both CTAs are visible
- Nav bar is present and its background changes on scroll (scroll down, re-snapshot)

- [ ] **Step 6: Commit**

```bash
git add "Furnishiq.net/landing-turnkey.dc.html"
git commit -m "Add turnkey landing page scaffold with hero section (EN)"
```

---

### Task 2: EN Needs + Service/Package sections

**Files:**
- Modify: `Furnishiq.net/landing-turnkey.dc.html` (insert between hero `</section>` and `</x-dc>`)

**Interfaces:**
- Consumes: `data-reveal` animation mechanism from Task 1 (already wired via `componentDidMount`, no new JS needed — just add the attribute to new elements)
- Produces: `id="needs"` and `id="service"` sections for later tasks' nav/CTA anchors to link to (already referenced by hero's `#service` CTA from Task 1)

- [ ] **Step 1: Add the Needs section**

Insert after the hero `</section>`:

```html
<section id="needs" data-screen-label="Needs" style="background:#FFFFFF;padding:clamp(80px,10vw,128px) clamp(24px,5vw,80px);">
  <div style="max-width:1280px;margin:0 auto;">
    <h2 data-reveal style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);font-family:'Lama Sans',sans-serif;font-size:clamp(28px,3.2vw,44px);font-weight:500;color:#1F1F1F;line-height:1.15;letter-spacing:-0.015em;text-align:center;max-width:760px;margin:0 auto 56px;text-wrap:balance;">What would you like FurnishIQ to achieve for your space?</h2>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:32px;">
      <div data-reveal style="opacity:0;transform:translateY(20px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);background:#F5F2ED;padding:clamp(32px,3vw,44px) clamp(28px,2.6vw,36px);display:flex;flex-direction:column;min-height:220px;">
        <p style="font-family:'Lama Sans',sans-serif;font-size:18px;color:#1F1F1F;line-height:1.5;flex:1;margin-bottom:28px;">Complete end-to-end transformation&mdash;from initial design to turnkey handover.</p>
        <a href="#form" style="font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.2em;text-transform:uppercase;color:#5B4636;text-decoration:none;border-bottom:1px solid #5B4636;padding-bottom:4px;align-self:flex-start;">Get a Consultation</a>
      </div>
      <div data-reveal data-reveal-delay="0.08" style="opacity:0;transform:translateY(20px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);background:#F5F2ED;padding:clamp(32px,3vw,44px) clamp(28px,2.6vw,36px);display:flex;flex-direction:column;min-height:220px;">
        <p style="font-family:'Lama Sans',sans-serif;font-size:18px;color:#1F1F1F;line-height:1.5;flex:1;margin-bottom:28px;">Bespoke interior design services.</p>
        <a href="#service" style="font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.2em;text-transform:uppercase;color:#5B4636;text-decoration:none;border-bottom:1px solid #5B4636;padding-bottom:4px;align-self:flex-start;">Explore Service</a>
      </div>
      <div data-reveal data-reveal-delay="0.16" style="opacity:0;transform:translateY(20px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);background:#F5F2ED;padding:clamp(32px,3vw,44px) clamp(28px,2.6vw,36px);display:flex;flex-direction:column;min-height:220px;">
        <p style="font-family:'Lama Sans',sans-serif;font-size:18px;color:#1F1F1F;line-height:1.5;flex:1;margin-bottom:28px;">Shell and core space needing premium fit-out and luxury furnishing.</p>
        <a href="#form" style="font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.2em;text-transform:uppercase;color:#5B4636;text-decoration:none;border-bottom:1px solid #5B4636;padding-bottom:4px;align-self:flex-start;">Get a Consultation</a>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add the Service/Package section**

Insert after the Needs section:

```html
<section id="service" data-screen-label="Service Package" style="background:#F5F2ED;padding:clamp(80px,10vw,128px) clamp(24px,5vw,80px);">
  <div style="max-width:900px;margin:0 auto;text-align:center;">
    <span data-reveal style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);display:block;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.3em;text-transform:uppercase;color:#8B6B4A;margin-bottom:18px;">The Package</span>
    <h2 data-reveal data-reveal-delay="0.08" style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);font-family:'Lama Sans',sans-serif;font-size:clamp(28px,3.2vw,44px);font-weight:500;color:#1F1F1F;line-height:1.15;letter-spacing:-0.015em;margin-bottom:24px;text-wrap:balance;">Integrated Turnkey Engineering Package</h2>
    <p data-reveal data-reveal-delay="0.16" style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);font-family:'Lama Sans',sans-serif;font-size:16px;color:#5B4636;line-height:1.6;margin-bottom:8px;">We manage every phase of your space creation, from concept to reality.</p>
    <p data-reveal data-reveal-delay="0.2" style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);font-family:'Lama Sans',sans-serif;font-size:16px;color:#1F1F1F;font-weight:500;margin-bottom:8px;">Residential interior design packages starting from 29.99 SAR/m&sup2;.</p>
    <p data-reveal data-reveal-delay="0.24" style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);font-family:'Lama Sans',sans-serif;font-size:13px;color:#8B6B4A;line-height:1.6;margin-bottom:48px;">(Separate quotes provided for execution, fit-out, and furnishing based on your project scope and requirements.)</p>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px;text-align:left;margin-bottom:48px;">
      <div data-reveal style="opacity:0;transform:translateY(20px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);background:#FFFFFF;padding:28px;">
        <h3 style="font-family:'Lama Sans',sans-serif;font-size:15px;font-weight:500;color:#1F1F1F;margin-bottom:10px;">Photorealistic 3D Interior Design</h3>
        <p style="font-family:'Lama Sans',sans-serif;font-size:14px;color:#5B4636;line-height:1.6;">Intelligently crafted spaces reflecting your unique identity, meeting practical needs, and elevating lifestyle.</p>
      </div>
      <div data-reveal data-reveal-delay="0.08" style="opacity:0;transform:translateY(20px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);background:#FFFFFF;padding:28px;">
        <h3 style="font-family:'Lama Sans',sans-serif;font-size:15px;font-weight:500;color:#1F1F1F;margin-bottom:10px;">Luxury Fit-Out &amp; Execution</h3>
        <p style="font-family:'Lama Sans',sans-serif;font-size:14px;color:#5B4636;line-height:1.6;">Translating blueprints into reality using premium materials under rigorous engineering supervision.</p>
      </div>
      <div data-reveal data-reveal-delay="0.16" style="opacity:0;transform:translateY(20px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);background:#FFFFFF;padding:28px;">
        <h3 style="font-family:'Lama Sans',sans-serif;font-size:15px;font-weight:500;color:#1F1F1F;margin-bottom:10px;">Complete Furnishing &amp; Procurement</h3>
        <p style="font-family:'Lama Sans',sans-serif;font-size:14px;color:#5B4636;line-height:1.6;">Bespoke furniture pieces matching approved designs and spatial dimensions with 100% precision.</p>
      </div>
    </div>
    <a href="#form" data-reveal style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);display:inline-block;font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.2em;text-transform:uppercase;color:#FFFFFF;background:#3A2D25;padding:19px 40px;border:1px solid #3A2D25;text-decoration:none;">Get Your Free Engineering Consultation</a>
  </div>
</section>
```

- [ ] **Step 3: Verify**

Navigate the Playwright browser to the file, `browser_snapshot`, confirm both new sections render with no `{{ }}` artifacts, the pricing line reads "29.99 SAR/m²", and clicking "Explore Service" (`#service` link in Needs) scrolls to the Service section.

- [ ] **Step 4: Commit**

```bash
git add "Furnishiq.net/landing-turnkey.dc.html"
git commit -m "Add Needs and Service/Package sections to turnkey landing page (EN)"
```

---

### Task 3: EN Video/media + Our Work sections

**Files:**
- Modify: `Furnishiq.net/landing-turnkey.dc.html` (insert after Service section, before `</x-dc>`)

**Interfaces:**
- Produces: `id="work"` section for the nav/CTA references

- [ ] **Step 1: Add the static video/media section**

```html
<section id="media" data-screen-label="Media" style="position:relative;background:#1F1F1F;min-height:60vh;display:flex;align-items:center;justify-content:center;overflow:hidden;padding:clamp(80px,10vw,128px) clamp(24px,5vw,80px);">
  <div style="position:absolute;inset:0;background-image:url('https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=2400&q=30');background-size:cover;background-position:center;opacity:0.5;pointer-events:none;"></div>
  <div style="position:relative;z-index:1;max-width:760px;text-align:center;">
    <div data-reveal style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);width:76px;height:76px;border:1px solid rgba(255,255,255,0.6);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 36px;">
      <svg width="26" height="26" viewBox="0 0 24 24" fill="#FFFFFF"><path d="M8 5v14l11-7z"/></svg>
    </div>
    <h2 data-reveal data-reveal-delay="0.08" style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);font-family:'Lama Sans',sans-serif;font-size:clamp(26px,3vw,40px);font-weight:500;color:#FFFFFF;line-height:1.2;margin-bottom:20px;text-wrap:balance;">Envision the Design.. Experience the Luxury.</h2>
    <p data-reveal data-reveal-delay="0.16" style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);font-family:'Lama Sans',sans-serif;font-size:15px;color:rgba(255,255,255,0.82);line-height:1.7;margin-bottom:32px;">Watch how we transform engineering schematics into living, breathing spaces. At FurnishIQ, we offer more than visionary ideas&mdash;we deliver a seamless journey spanning bespoke interior design, MEP installation, luxury fit-out, and 100% design-matched turnkey furnishing.</p>
    <a href="#form" data-reveal data-reveal-delay="0.24" style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);display:inline-block;font-family:'Lama Sans',sans-serif;font-size:11px;letter-spacing:0.2em;text-transform:uppercase;color:#1F1F1F;background:#D6C2A8;padding:19px 36px;border:1px solid #D6C2A8;text-decoration:none;">Book Your Engineering Consultation</a>
  </div>
</section>
```

- [ ] **Step 2: Add the Our Work section**

Use these four Unsplash URLs already established elsewhere on the site (copied verbatim from `Furnishiq.net/projects.dc.html`, so they're proven to load): `photo-1497215728101-856f4ea42174`, `photo-1552566626-52f8b828add9`, `photo-1590490360182-c33d57733427`, `photo-1604328698692-f76ea9498e76` (each with `?auto=format&fit=crop&w=900&q=30`).

```html
<section id="work" data-screen-label="Our Work" style="background:#FFFFFF;padding:clamp(80px,10vw,128px) clamp(24px,5vw,80px);">
  <div style="max-width:1280px;margin:0 auto;">
    <div style="text-align:center;margin-bottom:56px;">
      <h2 data-reveal style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);font-family:'Lama Sans',sans-serif;font-size:clamp(28px,3.2vw,44px);font-weight:500;color:#1F1F1F;margin-bottom:14px;">Spaces Designed to be Lived In</h2>
      <p data-reveal data-reveal-delay="0.08" style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);font-family:'Lama Sans',sans-serif;font-size:16px;color:#5B4636;">See how our ideas turn into real-world projects</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:24px;">
      <a href="/projects" data-reveal style="opacity:0;transform:translateY(20px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);display:block;aspect-ratio:3/4;background-image:url('https://images.unsplash.com/photo-1497215728101-856f4ea42174?auto=format&fit=crop&w=900&q=30');background-size:cover;background-position:center;"></a>
      <a href="/projects" data-reveal data-reveal-delay="0.06" style="opacity:0;transform:translateY(20px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);display:block;aspect-ratio:3/4;background-image:url('https://images.unsplash.com/photo-1552566626-52f8b828add9?auto=format&fit=crop&w=900&q=30');background-size:cover;background-position:center;"></a>
      <a href="/projects" data-reveal data-reveal-delay="0.12" style="opacity:0;transform:translateY(20px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);display:block;aspect-ratio:3/4;background-image:url('https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=900&q=30');background-size:cover;background-position:center;"></a>
      <a href="/projects" data-reveal data-reveal-delay="0.18" style="opacity:0;transform:translateY(20px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);display:block;aspect-ratio:3/4;background-image:url('https://images.unsplash.com/photo-1604328698692-f76ea9498e76?auto=format&fit=crop&w=900&q=30');background-size:cover;background-position:center;"></a>
    </div>
  </div>
</section>
```

- [ ] **Step 3: Verify**

Playwright: navigate, `browser_snapshot`, confirm all 4 work tiles show loaded background images (not broken), video section copy renders, play-button icon is visible and centered.

- [ ] **Step 4: Commit**

```bash
git add "Furnishiq.net/landing-turnkey.dc.html"
git commit -m "Add media and Our Work sections to turnkey landing page (EN)"
```

---

### Task 4: EN USP's + Form section with real submit/validation/thank-you logic

**Files:**
- Modify: `Furnishiq.net/landing-turnkey.dc.html`

**Interfaces:**
- Consumes: `state`/`renderVals()` skeleton from Task 1 Step 4 — this task replaces the `onFormSubmit` stub and adds the real fields to the template.
- Produces: fully working form (final piece of the EN page's functional surface).

- [ ] **Step 1: Add the USP's section**

```html
<section id="usps" data-screen-label="USPs" style="background:#1F1F1F;padding:clamp(80px,10vw,128px) clamp(24px,5vw,80px);">
  <div style="max-width:1280px;margin:0 auto;">
    <div style="text-align:center;margin-bottom:56px;">
      <h2 data-reveal style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);font-family:'Lama Sans',sans-serif;font-size:clamp(28px,3.2vw,44px);font-weight:500;color:#FFFFFF;margin-bottom:14px;">Why Choose FurnishIQ?</h2>
      <p data-reveal data-reveal-delay="0.08" style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);font-family:'Lama Sans',sans-serif;font-size:15px;color:rgba(255,255,255,0.7);max-width:640px;margin:0 auto;line-height:1.7;">Your complete space supervised by a single engineering authority for a hassle-free turnkey experience.</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:20px;">
      <div data-reveal style="opacity:0;transform:translateY(20px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);border:1px solid rgba(255,255,255,0.12);padding:24px 20px;">
        <h3 style="font-family:'Lama Sans',sans-serif;font-size:14px;font-weight:500;color:#D6C2A8;margin-bottom:10px;">Integrated Engineering System</h3>
        <p style="font-family:'Lama Sans',sans-serif;font-size:13px;color:rgba(255,255,255,0.65);line-height:1.6;">Managing your project journey from innovative interior design to turnkey handover.</p>
      </div>
      <div data-reveal data-reveal-delay="0.06" style="opacity:0;transform:translateY(20px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);border:1px solid rgba(255,255,255,0.12);padding:24px 20px;">
        <h3 style="font-family:'Lama Sans',sans-serif;font-size:14px;font-weight:500;color:#D6C2A8;margin-bottom:10px;">Single Partner, Concept to Completion</h3>
        <p style="font-family:'Lama Sans',sans-serif;font-size:13px;color:rgba(255,255,255,0.65);line-height:1.6;">We design, engineer MEP systems, execute fit-outs, and completely furnish your space.</p>
      </div>
      <div data-reveal data-reveal-delay="0.12" style="opacity:0;transform:translateY(20px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);border:1px solid rgba(255,255,255,0.12);padding:24px 20px;">
        <h3 style="font-family:'Lama Sans',sans-serif;font-size:14px;font-weight:500;color:#D6C2A8;margin-bottom:10px;">Precision with BIM Technology</h3>
        <p style="font-family:'Lama Sans',sans-serif;font-size:13px;color:rgba(255,255,255,0.65);line-height:1.6;">Advanced Building Information Modeling prevents clashes between design and utilities.</p>
      </div>
      <div data-reveal data-reveal-delay="0.18" style="opacity:0;transform:translateY(20px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);border:1px solid rgba(255,255,255,0.12);padding:24px 20px;">
        <h3 style="font-family:'Lama Sans',sans-serif;font-size:14px;font-weight:500;color:#D6C2A8;margin-bottom:10px;">Tailored Solutions</h3>
        <p style="font-family:'Lama Sans',sans-serif;font-size:13px;color:rgba(255,255,255,0.65);line-height:1.6;">100% exact match between 3D renderings and reality, curated with high-grade materials.</p>
      </div>
      <div data-reveal data-reveal-delay="0.24" style="opacity:0;transform:translateY(20px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);border:1px solid rgba(255,255,255,0.12);padding:24px 20px;">
        <h3 style="font-family:'Lama Sans',sans-serif;font-size:14px;font-weight:500;color:#D6C2A8;margin-bottom:10px;">Exceptional Value</h3>
        <p style="font-family:'Lama Sans',sans-serif;font-size:13px;color:rgba(255,255,255,0.65);line-height:1.6;">Residential design packages starting from just 29.99 SAR/m&sup2;.</p>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add the form section markup**

```html
<section id="form" data-screen-label="Form" style="background:#F5F2ED;padding:clamp(80px,10vw,136px) clamp(24px,5vw,80px);">
  <div style="max-width:560px;margin:0 auto;">
    <div style="text-align:center;margin-bottom:44px;">
      <h2 data-reveal style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);font-family:'Lama Sans',sans-serif;font-size:clamp(28px,3.2vw,44px);font-weight:500;color:#1F1F1F;margin-bottom:16px;text-wrap:balance;">Ready to Start Transforming Your Space?</h2>
      <p data-reveal data-reveal-delay="0.08" style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);font-family:'Lama Sans',sans-serif;font-size:15px;color:#5B4636;line-height:1.7;">Whether seeking an exceptional interior design or full shell-and-core turnkey fit-out and furnishing, begin your journey with FurnishIQ.</p>
    </div>

    <div sc-if="!submitted">
      <form onSubmit="{{ onFormSubmit }}" style="display:flex;flex-direction:column;gap:20px;">
        <input type="text" value="{{ formHoneypot }}" onChange="{{ onHoneypotChange }}" name="company_website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0;">
        <div>
          <label style="display:block;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.16em;text-transform:uppercase;color:#5B4636;margin-bottom:8px;">Full Name</label>
          <input type="text" value="{{ formName }}" onChange="{{ onNameChange }}" style="width:100%;padding:16px 18px;border:1px solid #D6C2A8;background:#FFFFFF;font-family:'Lama Sans',sans-serif;font-size:15px;color:#1F1F1F;">
          <span sc-if="fieldErrors.name" style="display:block;font-family:'Lama Sans',sans-serif;font-size:12px;color:#B33A3A;margin-top:6px;">{{ fieldErrors.name }}</span>
        </div>
        <div>
          <label style="display:block;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.16em;text-transform:uppercase;color:#5B4636;margin-bottom:8px;">Phone Number</label>
          <input type="tel" value="{{ formPhone }}" onChange="{{ onPhoneChange }}" style="width:100%;padding:16px 18px;border:1px solid #D6C2A8;background:#FFFFFF;font-family:'Lama Sans',sans-serif;font-size:15px;color:#1F1F1F;">
          <span sc-if="fieldErrors.phone" style="display:block;font-family:'Lama Sans',sans-serif;font-size:12px;color:#B33A3A;margin-top:6px;">{{ fieldErrors.phone }}</span>
        </div>
        <div>
          <label style="display:block;font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.16em;text-transform:uppercase;color:#5B4636;margin-bottom:8px;">What do you need?</label>
          <select value="{{ selectedNeed }}" onChange="{{ onNeedChange }}" style="width:100%;padding:16px 18px;border:1px solid #D6C2A8;background:#FFFFFF;font-family:'Lama Sans',sans-serif;font-size:15px;color:#1F1F1F;">
            <option value="">Select an option</option>
            <option value="turnkey">Integrated Turnkey Package (Design, Fit-Out &amp; Furnishing)</option>
            <option value="design_only">Interior Design Only</option>
            <option value="fit_out">Fit-Out Execution for Existing Blueprints</option>
            <option value="furniture">Luxury Furniture Procurement</option>
            <option value="other">Other Services</option>
          </select>
          <span sc-if="fieldErrors.need" style="display:block;font-family:'Lama Sans',sans-serif;font-size:12px;color:#B33A3A;margin-top:6px;">{{ fieldErrors.need }}</span>
        </div>
        <button type="submit" id="id-submit-btn" style="font-family:'Lama Sans',sans-serif;font-size:10px;letter-spacing:0.22em;text-transform:uppercase;color:#FFFFFF;background:#3A2D25;padding:19px 36px;border:1px solid #3A2D25;cursor:pointer;width:100%;transition:all 0.3s cubic-bezier(0.25,0.46,0.45,0.94);">
          <span id="id-submit-btn-label">Start Your Project with FurnishIQ</span>
        </button>
      </form>
    </div>

    <div sc-if="submitted" data-reveal style="opacity:0;transform:translateY(18px);transition:opacity 0.8s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);text-align:center;background:#FFFFFF;padding:clamp(40px,4vw,56px) clamp(28px,3vw,40px);">
      <h3 style="font-family:'Lama Sans',sans-serif;font-size:22px;font-weight:500;color:#1F1F1F;margin-bottom:16px;">Your Request Has Been Received</h3>
      <p style="font-family:'Lama Sans',sans-serif;font-size:15px;color:#5B4636;line-height:1.7;margin-bottom:12px;">Your space has taken its first step toward luxury with FurnishIQ.</p>
      <p style="font-family:'Lama Sans',sans-serif;font-size:15px;color:#5B4636;line-height:1.7;">Our engineering team is currently reviewing your project details. One of our specialists will reach out shortly to discuss your needs and begin turning your vision into a meticulously executed reality.</p>
    </div>
  </div>
</section>
```

- [ ] **Step 3: Replace the `onFormSubmit` stub and add validation to `renderVals()`**

In the `data-dc-script` block from Task 1, replace the `onFormSubmit: (e) => { e.preventDefault(); },` stub with:

```javascript
      onFormSubmit: (e) => {
        e.preventDefault();
        if (self.state.formHoneypot) return;
        const errors = {
          name: self.state.formName.trim() ? '' : 'Please enter your full name.',
          phone: self.state.formPhone.trim() ? '' : 'Please enter your phone number.',
          need: self.state.selectedNeed ? '' : 'Please select what you need.',
        };
        if (errors.name || errors.phone || errors.need) {
          self.setState({ fieldErrors: errors });
          return;
        }
        const btn = document.getElementById('id-submit-btn');
        const btnLabel = document.getElementById('id-submit-btn-label');
        if (btn) btn.disabled = true;
        if (btnLabel) btnLabel.textContent = 'Sending…';
        const payload = {
          formType: 'landing_turnkey',
          name: self.state.formName,
          phone: self.state.formPhone,
          need: self.state.selectedNeed,
          honeypot: self.state.formHoneypot,
        };
        fetch('/api/send-email', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
          .then((r) => {
            if (!r.ok) throw new Error('Network error');
            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({ event: 'generate_lead', form_name: 'landing_turnkey', need: self.state.selectedNeed });
            self.setState({ submitted: true, fieldErrors: {} });
          })
          .catch(() => {
            if (btn) btn.disabled = false;
            if (btnLabel) btnLabel.textContent = 'Start Your Project with FurnishIQ';
            alert('Something went wrong — please try again or email us directly at info@furnishiq.net');
          });
      },
```

- [ ] **Step 4: Verify with Playwright — empty submit shows validation errors**

Navigate to the page, `browser_snapshot` to find the form's submit button, click it without filling any field. Re-snapshot and confirm the three `fieldErrors` messages ("Please enter your full name.", "Please enter your phone number.", "Please select what you need.") are now visible, and no `fetch` request was attempted (check `browser_network_requests` shows no `/api/send-email` call yet).

- [ ] **Step 5: Verify with Playwright — filled submit shows inline thank-you**

Fill in name, phone, and select a dropdown option via `browser_fill_form`/`browser_select_option`, then click submit. Re-snapshot and confirm the thank-you block ("Your Request Has Been Received") is now visible in place of the form (the `/api/send-email` call will fail in this local/offline context — that's expected; if it fails, confirm the button re-enables and the alert path is reachable, and note in your report that full end-to-end submission can only be confirmed once `/api/send-email` is reachable, matching how `contact.dc.html` already behaves in this same environment).

- [ ] **Step 6: Commit**

```bash
git add "Furnishiq.net/landing-turnkey.dc.html"
git commit -m "Add USPs and working form section to turnkey landing page (EN)"
```

---

### Task 5: EN page full-page QA pass

**Files:**
- Modify: `Furnishiq.net/landing-turnkey.dc.html` (fixes only, if issues found)
- Modify: `Furnishiq.net/sitemap.xml`

**Interfaces:**
- Consumes: the complete page from Tasks 1-4.

- [ ] **Step 1: Full-page Playwright pass**

Navigate to `file:///D:/ProjectsClaude/FurnishIQ/Furnishiq.net/landing-turnkey.dc.html`. Take a full-page `browser_take_screenshot`. Check `browser_console_messages` for any errors or warnings. Scroll through the whole page and confirm every section (`hero`, `needs`, `service`, `media`, `work`, `usps`, `form`) is present, in order, with no raw `{{ }}` text, no broken images, and the floating WhatsApp button is visible in the bottom-left corner throughout scroll.

- [ ] **Step 2: Mobile viewport check**

Use `browser_resize` to set the viewport to 375x812 (iPhone-sized), re-screenshot the hero, needs grid, and form sections. Confirm no horizontal scroll appears and text/CTAs remain legible (per CLAUDE.md's phone-width requirement). Fix any overflow issues found (e.g. change `grid-template-columns:repeat(3,1fr)` sections to stack via a `@media` query added to the `<helmet><style>` block if needed) — read the existing `@media(max-width:600px)` patterns already present in the copied CSS from Task 1 Step 2 and extend them rather than inventing a new breakpoint convention.

- [ ] **Step 3: Design-system compliance checklist**

Grep the file for violations and fix any found:

```bash
grep -n "border-radius" "Furnishiq.net/landing-turnkey.dc.html"
grep -niE "gradient|#1C6B35" "Furnishiq.net/landing-turnkey.dc.html"
grep -n "!" "Furnishiq.net/landing-turnkey.dc.html"
```

Confirm: no `border-radius` other than `0` or the pre-existing nav/card patterns copied from `contact.dc.html` (those already comply), no `gradient` anywhere, `#1C6B35` (brand green) does not appear outside the logo image, and no `!` appears in visible copy text (exclamation marks in JS code like `!submitted` are fine — only check user-facing text nodes).

- [ ] **Step 4: Add both URLs to sitemap.xml**

Read `Furnishiq.net/sitemap.xml` to see the existing `<url>` entry format (matching `contact`'s entry), then add two new `<url>` entries for `https://www.furnishiq.net/landing-turnkey` and `https://www.furnishiq.net/ar/landing-turnkey`, following the exact same `<loc>`/`<changefreq>`/`<priority>` structure as the existing `contact` entries.

- [ ] **Step 5: Commit**

```bash
git add "Furnishiq.net/landing-turnkey.dc.html" "Furnishiq.net/sitemap.xml"
git commit -m "QA pass and sitemap entries for EN turnkey landing page"
```

---

### Task 6: AR page — full RTL build

**Files:**
- Create: `Furnishiq.net/landing-turnkey.ar.dc.html`

**Interfaces:**
- Consumes: the finished `landing-turnkey.dc.html` from Tasks 1-5 as its structural template.

- [ ] **Step 1: Copy the EN file as the starting point**

```bash
cp "Furnishiq.net/landing-turnkey.dc.html" "Furnishiq.net/landing-turnkey.ar.dc.html"
```

- [ ] **Step 2: Apply RTL/language changes**

Edit `Furnishiq.net/landing-turnkey.ar.dc.html`:
- `<html lang="en">` → `<html dir="rtl" lang="ar">`
- `<title>` → `فرينيش آي كيو | الباقة الهندسية المتكاملة (تسليم مفتاح)`
- `<meta name="description">` → `في الـ96... من المخطط إلى تسليم المفتاح. تصميم داخلي، تشطيبات فاخرة، وتأثيث متكامل مع جهة واحدة. باقات تبدأ من 29.99 ريال/م².`
- canonical/hreflang block → `canonical` and `hreflang="ar"` both point at `https://www.furnishiq.net/ar/landing-turnkey`; `hreflang="en"` points at `https://www.furnishiq.net/landing-turnkey`; `hreflang="x-default"` points at the English URL (matching `contact.ar.dc.html`'s pattern — read that file's head to confirm exact structure before editing).
- Everywhere `font-family:'Lama Sans',sans-serif` is used for body copy/headings/labels/buttons, change to `font-family:'GE SS Two',sans-serif` (do a project-wide find/replace within this file only — do not touch `landing-turnkey.dc.html`).
- Language-switch nav link (`data-lang-switch`) href → `/landing-turnkey` (pointing back to English), and its label text → `English`.

- [ ] **Step 3: Translate all visible copy to the PDF's Arabic text**

Replace every English text node with the corresponding Arabic copy from the spec/PDF, section by section:
- Hero: label "تسليم مفتاح", headline "في الـ96... من المخطط إلى تسليم المفتاح.", sub "كل احتياجات مساحتك من التصميم الداخلي، التشطيبات الفاخرة (Fit-out)، والتأثيث المتكامل.. مع جهة واحدة تضمن لك دقة التنفيذ والتطابق التام مع رؤيتك.", CTAs "ابدأ مشروعك مع فرينيش آي كيو" / "اكتشف خدماتنا"
- Needs: headline "وش تحتاج فرينيش آي كيو تنجز لمساحتك؟", card copy/CTAs exactly as listed in the spec's Section 2
- Service: "الباقة الهندسية المتكاملة (تسليم مفتاح)", body/pricing/disclaimer and 3 inclusion cards exactly as in the spec's Section 3, CTA "احصل على استشارة هندسية مجانية الان"
- Media: "تصميم تراه.. وواقع تعيش فخامته" + body + CTA "احجز استشارتك الهندسية"
- Our Work: "أعمال صُممت لتُعاش" / "شوف كيف تتحول أفكارنا إلى مشاريع"
- USPs: "ليش تختار فرينيش آي كيو؟" + sub + 5 cards exactly as in the spec's Section 6
- Form: "جاهز تبدأ رحلة تجهيز مساحتك؟" + sub, labels "الإسم بالكامل" / "رقم الجوال" / "وش تحتاج؟", dropdown options ("تصميم، تشطيب، وتأثيث متكامل (تسليم مفتاح)" / "تصميم داخلي فقط" / "تنفيذ وتشطيبات (Fit-out) لمخطط جاهز" / "توريد أثاث فاخر" / "خدمة أخرى"), CTA "ابدأ مشروعك مع فرينيش آي كيو", validation messages and thank-you copy ("تم استلام طلبك" / "مساحتك أخذت أول خطوة نحو الفخامة مع فرينيش آي كيو." / the review-team paragraph from the spec) translated accordingly.
- In the `data-dc-script` block: update the three validation error strings and the `alert(...)` fallback message text to Arabic; keep all field/variable/function names in English (they're code, not copy) — do not translate identifiers.
- Update `payload.formType` to `'landing_turnkey_ar'` so leads are distinguishable by language in the backend.

- [ ] **Step 4: Verify Arabic rendering and RTL layout with Playwright**

Navigate to `file:///D:/ProjectsClaude/FurnishIQ/Furnishiq.net/landing-turnkey.ar.dc.html`. `browser_snapshot` and confirm: no raw `{{ }}` text, no leftover English copy in body sections (nav global links like "About Us"/"Services" staying in Arabic or transliterated form should match how `contact.ar.dc.html` already handles them — check that file for the actual Arabic nav labels and mirror them exactly rather than guessing), text visually flows right-to-left, and the page title bar/console show no errors. Confirm the floating WhatsApp button still renders bottom-left (per `floating-buttons.js`'s existing lang-aware text, already confirmed independent of layout direction).

- [ ] **Step 5: Verify AR form validation and submission flow**

Repeat Task 4 Steps 4-5's empty-submit and filled-submit checks on this Arabic page, confirming Arabic validation messages appear and the Arabic thank-you block appears on successful state transition.

- [ ] **Step 6: Commit**

```bash
git add "Furnishiq.net/landing-turnkey.ar.dc.html"
git commit -m "Add Arabic (RTL) version of turnkey landing page"
```

---

### Task 7: Cross-page final QA

**Files:**
- Modify: `Furnishiq.net/landing-turnkey.dc.html`, `Furnishiq.net/landing-turnkey.ar.dc.html`, `Furnishiq.net/sitemap.xml` (fixes only, if issues found)

**Interfaces:**
- Consumes: both finished pages.

- [ ] **Step 1: Verify the language switch links work both directions**

Playwright: on the EN page, click the "عربي" language-switch nav link, confirm it navigates to `landing-turnkey.ar.dc.html` (or the equivalent local path) and the AR page loads correctly. From the AR page, click "English" and confirm it returns to the EN page.

- [ ] **Step 2: Re-run the mobile viewport check (Task 5 Step 2) on the AR page**

Resize to 375x812, screenshot the AR hero/needs/form sections, confirm no horizontal scroll and RTL text remains legible.

- [ ] **Step 3: Confirm sitemap.xml validity**

```bash
grep -c "<url>" "Furnishiq.net/sitemap.xml"
grep -c "</url>" "Furnishiq.net/sitemap.xml"
```

Confirm counts match (no broken XML from the Task 5 edit) and both new URLs are present:

```bash
grep -n "landing-turnkey" "Furnishiq.net/sitemap.xml"
```

- [ ] **Step 4: Final git status check**

```bash
git status
```

Confirm only the four expected files (`landing-turnkey.dc.html`, `landing-turnkey.ar.dc.html`, `sitemap.xml`, and this plan/spec's own docs files from earlier commits) show as changed/created — no unrelated files were accidentally modified.

- [ ] **Step 5: Commit any final fixes**

```bash
git add -A "Furnishiq.net/landing-turnkey.dc.html" "Furnishiq.net/landing-turnkey.ar.dc.html" "Furnishiq.net/sitemap.xml"
git commit -m "Final cross-page QA fixes for turnkey landing page pair"
```

(If Step 1-3 found no issues, skip this commit — nothing to commit.)

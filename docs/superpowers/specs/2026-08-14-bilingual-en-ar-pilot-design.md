# Bilingual EN/AR Pilot — Design Spec

**Date:** 2026-08-14
**Status:** Approved for planning
**Scope:** Pilot on the two currently-live pages (home, contact). Infrastructure built generically so the other 9 pages (about-us, blog, portfolio, project-detail, single-post, services-fitout, services-furniture, services-interior-design, services-mep) can be added later with translation + two rewrite lines — no redesign.

## Goal

Add `furnishiq.net/en` and `furnishiq.net/ar` as the bilingual entry points the user asked for, with every subpage following that prefix pattern, starting with the two pages that are actually live today (home, contact). The 9 pages still hidden behind the July 28 "hide until ready" redirect stay hidden, in every language, until the user unhides them individually.

## Non-goals (out of scope for this pilot)

- Arabic content for the 9 hidden pages — infrastructure is ready for them, content is not.
- Full RTL *macro-layout* mirroring (flipping which side images/columns sit on). See "RTL scope" below for why, and what we do instead.
- A CMS, translation management system, or any tooling beyond static HTML files — the site remains pure static HTML/CSS/JS per `CLAUDE.md`.

## 1. Routing

`vercel.json` gains:

**Rewrites** (4 new, English-alias + Arabic-real):
```
/en           -> /Furnishiq.net/home.dc.html      (same file as /)
/en/contact   -> /Furnishiq.net/contact.dc.html   (same file as /contact)
/ar           -> /Furnishiq.net/home.ar.dc.html    (new file)
/ar/contact   -> /Furnishiq.net/contact.ar.dc.html (new file)
```

**Redirects** (18 new — one per hidden page × {`/en/`, `/ar/`} prefix), mirroring the existing bare-path hidden redirects exactly:
```
/en/about-us -> /     (permanent)
/ar/about-us -> /     (permanent)
... same pair for blog, portfolio, project-detail, single-post,
    services-interior-design, services-fitout, services-mep, services-furniture
```

This keeps `/en/*` and `/ar/*` behaviorally identical to today's bare paths for every hidden page — visiting `/ar/portfolio` 301s home exactly like `/portfolio` does today, not a 404. Vercel evaluates redirects before rewrites, so these explicit rules are required (there's no wildcard fallback that would apply parity automatically).

Existing `/`, `/contact`, and all their current behavior (including the `.dc.html` → clean-URL redirects shipped earlier) are untouched.

## 2. Files

Two new files:
- `Furnishiq.net/home.ar.dc.html`
- `Furnishiq.net/contact.ar.dc.html`

No new English files — `/en/*` reuses `home.dc.html` and `contact.dc.html` as-is via rewrite.

Each `.ar.dc.html` file is a full duplicate of its English counterpart with:
- `<html dir="rtl" lang="ar">`
- All visible copy translated to Arabic (see Translation section)
- Every inline `font-family:'Lama Sans',sans-serif` swapped to `font-family:'GE SS Two','Arial',sans-serif` — this has to be a literal find/replace through the file's inline styles, not a CSS cascade override, because the existing markup sets `font-family` inline on nearly every text element (inline styles beat a blanket stylesheet rule). The font file and CSS variable (`--font-arabic`) already exist in the design system, unused until now.
- Canonical/OG/Twitter meta translated and pointed at the `/ar/...` URL
- `hreflang` alternates added (see SEO section)
- CTA visual emphasis: Arabic has no letter case, so the "UPPERCASE, letter-spacing 0.2em" CTA treatment doesn't translate literally — Arabic CTAs keep the bold weight and letter-spacing but skip the case transform.

## 3. RTL scope — text direction, not macro-layout

The codebase authors layout via inline styles with hardcoded physical properties (`left`, `margin-left`, explicit column proportions like `grid-template-columns:1.6fr 1fr`), not CSS logical properties. Fully mirroring the macro-layout (nav order, hero grid, which side an image sits on) for every section of every page would mean re-authoring the layout of both pilot pages a second time — a much bigger project than "add Arabic."

**Decision:** Arabic pages get correct RTL *text* rendering — `dir="rtl"`, GE SS Two font, right-to-left reading flow, Arabic numerals per the brand style guide — but the page skeleton (which side things visually sit on) stays the same arrangement as the English version. This matches the design system's own spec, which specifies `dir="rtl"` at the element level, not page mirroring. CSS's `text-align` initial value is direction-aware, so unstyled paragraphs/headings align correctly automatically; any element with an explicit hardcoded `text-align:left` gets checked and flipped by hand during the translation pass if it reads wrong.

Full macro-layout mirroring can be a separate future project if real usage justifies the investment.

## 4. Language switcher

A small "EN / عربي" link added inside each page's `.fiq-nav-links` container, next to the existing nav links. Placing it inside that specific container means it's automatically picked up by the existing mobile off-canvas menu (`nav-mobile.js` clones `.fiq-nav-links` into the mobile overlay already) — no changes needed to the shared nav script.

- On `home.dc.html` / `contact.dc.html`: link points to `/ar` / `/ar/contact`.
- On `home.ar.dc.html` / `contact.ar.dc.html`: link points to `/` / `/contact`.

## 5. SEO

Each of the 4 pilot page-variants (`/`, `/contact`, `/ar`, `/ar/contact`) gets `hreflang` alternates in `<head>`:
```html
<link rel="alternate" hreflang="en" href="https://www.furnishiq.net/...">
<link rel="alternate" hreflang="ar" href="https://www.furnishiq.net/ar...">
<link rel="alternate" hreflang="x-default" href="https://www.furnishiq.net/...">
```

`/en` and `/en/contact` are **not** added to `sitemap.xml` and get no separate canonical — they serve the byte-identical file as `/` and `/contact` (same rewrite target), so the canonical tag already embedded in that response correctly points back to the bare URL regardless of which path was used to reach it. Submitting `/en/*` to the sitemap would create a contradictory signal (sitemap says "index this," the page's own canonical tag says "no, index that one instead"). `/ar` and `/ar/contact` are genuinely distinct content and get their own sitemap entries.

`robots.txt` gets the same 18 `Disallow` additions as the redirects above (`/en/about-us`, `/ar/about-us`, etc.) for consistency with the existing bare-path Disallow rules, even though the redirect alone likely prevents indexing.

## 6. Translation

Copy is translated directly (no external API) following the existing brand tone rules (authoritative, refined, third-person, no exclamation marks) adapted for Arabic where the English-specific rules don't transfer literally (e.g. uppercase CTAs, noted above).

**Caveat to flag once implementation is done, not on the live site:** this is a first-pass AI translation. It'll be grammatically correct and shippable, but brand-voice copy this deliberate ("Where Vision Meets Precision") deserves a native Arabic speaker's review before being treated as final.

## 7. Testing

Same approach used throughout this project: local static server + Playwright — screenshot both language versions, verify RTL rendering visually, verify the language switcher round-trips correctly in both directions, verify the mobile nav overlay still works with the switcher link included, verify hreflang tags are present and correctly paired, verify zero new console errors.

## Extension path for the other 9 pages (future work, not this pass)

Per page, once ready to unhide: (1) create `<page>.ar.dc.html` following this same pattern, (2) remove that page's `/en/<page>` and `/ar/<page>` redirect-to-home lines, (3) add the corresponding `/en/<page>` and `/ar/<page>` rewrite lines, (4) add hreflang + sitemap entries. No infrastructure redesign needed.

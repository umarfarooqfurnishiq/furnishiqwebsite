# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**FurnishIQ** is a static website and design system for a Saudi-based luxury interior design, fit-out, and furniture company serving the GCC region.

**Stack:** Pure HTML/CSS/JavaScript — no framework, no build tooling, no npm.

## Running the Site

Open `Furnishiq.net/FurnishIQ Home.html` directly in a browser. There is no build step. The `.dc.html` variant is a compressed version of the same page.

## Repository Structure

```
Furnishiq.net/
├── FurnishIQ Home.html          ← Full website (~2.4MB)
├── FurnishIQ Home.dc.html       ← Compressed variant
├── support.js                   ← Interactive behaviour (hero slider, scroll nav)
├── assets/                      ← Logo variants (PNG)
├── uploads/                     ← Project photography
└── _ds/furnishiq-design-system-*/
    ├── styles.css               ← Entry point (imports only)
    ├── tokens/                  ← CSS custom properties (load order matters)
    │   ├── colors.css
    │   ├── typography.css
    │   ├── spacing.css
    │   ├── effects.css
    │   └── base.css
    ├── uploads/                 ← Local font files
    ├── readme.md                ← Full design system documentation
    └── _ds_manifest.json        ← Component & token registry
```

## Design System — Mandatory Rules

The full spec lives in `_ds/.../readme.md`. Key constraints:

**Colors**
- Walnut `#5B4636` · Dark Walnut `#3A2D25` · Bronze `#8B6B4A`
- Stone `#F5F2ED` (secondary backgrounds) · Charcoal `#1F1F1F` (dark surfaces)
- Brand Green `#1C6B35` — **logo only**, never in UI or copy
- No gradients. No cool-grey tones.

**Typography**
- English (all weights): **Lama Sans Medium 500** — loaded from local `@font-face`, never CDN
- Arabic (all uses): **GE SS Two Medium 500** — always `dir="rtl"` on the element
- Never use: serif fonts (Cormorant, Georgia, Times), Jost, Inter, Roboto, Arial, or Google Fonts

**Layout**
- `border-radius: 0` everywhere by default (sharp corners)
- 12-column grid, 32px gutter, 1440px max container, 1280px max content
- Section padding: min 64px top/bottom, ideal 96–128px

**Motion**
- Luxury ease: `cubic-bezier(0.25, 0.46, 0.45, 0.94)`, 200–700ms
- Fade + translateY entrance only — no bounce, no spring
- Always respect `prefers-reduced-motion`

**Shadows** — warm-toned only:
```css
--shadow-sm:      0 2px 8px rgba(58,45,37,0.08)
--shadow-md:      0 4px 20px rgba(58,45,37,0.10)
--shadow-luxury:  0 24px 80px rgba(58,45,37,0.20)
```

**Icons:** Lucide Icons (if needed) via CDN — 1.5px stroke, geometric.

## Copy & Tone

- Authoritative, refined, visionary — comparable to Armani Casa / Minotti
- Third-person brand voice for institutional copy: *"FurnishIQ crafts…"*
- No exclamation marks. No superlatives without evidence.
- No emoji anywhere.
- CTAs: UPPERCASE, letter-spacing 0.2em
- Section labels: UPPERCASE, 10–11px, letter-spacing 0.2em

## Logo

Use only the provided PNG files (`logo-default.png`, `logo-dark.png`, `logo-scrolled.png`). Never recreate, recolour, or modify the logo. Approved backgrounds: white, charcoal, brand green.

# FurnishIQ Design System

> Premium interior design, fit-out & furniture brand — Saudi Arabia / GCC

---

## About the Brand

**FurnishIQ** is a Saudi-based design-build company specialising in interior design, turnkey fit-out, furniture solutions, and project management. They create exceptional environments across commercial, hospitality, residential, and government sectors, transforming ideas into functional, inspiring, and enduring spaces across the GCC.

**Key differentiator:** Integrated fit-out, MEP, and FF&E — engineered for performance and delivered by one coordinated team.

**Services:** Interior Design · Fit-Out · MEP · Furniture Solutions · Project Management

**Sectors:** Commercial · Hospitality · Residential · Government

**Geography:** Kingdom of Saudi Arabia, GCC region

### Sources Provided

- `uploads/FurnishIQ Logo.png` — default logo (white mark, transparent BG)
- `uploads/FurnishIQ Logo Black.png` — dark variant (white mark on charcoal)
- `uploads/FurnishIQ Logo Green.png` — green variant (white mark on brand green)
- `uploads/Brand Guideline (1).pdf` — original brand guidelines (Adobe Illustrator PDF, binary-compressed; visual analysis performed from logos)

---

## ⚠ Mandatory Brand Governance

> **All subsequent brand assets, presentations, marketing materials, websites, social media creatives, proposals, and digital experiences must follow both the visual brand guidelines documented here and the machine-readable AI Brand Implementation Instructions contained in the AI BRAND IMPLEMENTATION section of this document.**

This instruction applies to every human designer, developer, and AI system that works with the FurnishIQ brand.

---

## Content Fundamentals

### Tone of Voice

- **Authoritative** — confident expertise, never arrogance
- **Refined** — precise, considered language; never casual or generic
- **Visionary** — possibility-driven; we transform, craft, create
- **Warmth** — human connections behind every space

### Language Rules

- Write in third-person brand voice for institutional copy: *"FurnishIQ crafts…"*
- Use first-person plural for project narratives: *"We designed…"*
- **No exclamation marks.** Confidence doesn't need them.
- **No superlatives without evidence.** Never "world-class," "best-in-class."
- **Title case** for service names and section headings.
- **Sentence case** for body paragraphs.
- No emoji in brand communications.
- Arabic numerals for all figures: 1,200 m² not twelve hundred square metres.

### Copy Style

| Element | Style | Example |
| --- | --- | --- |
| Hero headline | Lama Sans, 2–5 words, evocative | *"Crafted for Permanence"* |
| Section label | UPPERCASE, 2–3 words | *INTERIOR DESIGN* |
| Body paragraph | Sentence case, 2–3 sentences | *"We approach every project…"* |
| CTA | UPPERCASE verb phrase | *REQUEST A CONSULTATION* |
| Project title | Title Case | *Riyadh Royal Residences* |

---

## Visual Foundations

### Colors

The FurnishIQ brand palette moves away from the original brand green for UI/print applications, adopting a **luxury walnut and bronze system** inspired by premium materials: walnut timber, travertine stone, burnished bronze, and natural leather.

- **Primary surface:** White (`#FFFFFF`) — clean, editorial
- **Secondary surface:** Stone (`#F5F2ED`) — warm off-white for sections
- **Dark surface:** Charcoal (`#1F1F1F`) — for hero backgrounds, inverted sections
- **Brand accent:** Walnut (`#5B4636`) — primary CTAs, key headings
- **Bronze:** `#8B6B4A` — secondary accents, hover states
- **Logo Green** (`#1C6B35`) — **logo use only**, never in UI

### Typography

Two-font system — both fonts provided as brand-owned local files:

- **Display / Headings (English):** Lama Sans Medium 500 — refined geometric sans-serif. Precise, modern, architectural. File: `uploads/LamaSans-Medium_English.ttf`
- **Body / UI (English):** Lama Sans Medium 500 — same family, consistent weight across all English text.
- **Arabic (all uses):** GE SS Two Medium 500 — matching Arabic companion for bilingual Saudi/GCC layouts. File: `uploads/GE_SS_Two_Medium_Arabic.otf`
- Fonts loaded via local `@font-face` — no external CDN dependency.

### Backgrounds

- Primarily white or stone — editorial white-space is a luxury signal
- Dark walnut (`#3A2D25`) for full-bleed hero and impact sections
- Never gradients — solid, flat, intentional color blocks
- No textures or patterns in UI; material photography handles texture

### Animation & Motion

- **Easing:** Luxury ease `cubic-bezier(0.25, 0.46, 0.45, 0.94)` — smooth, deliberate
- **Duration:** 200ms base, 700ms for luxury/page transitions
- **Fade + translate:** Preferred entrance — opacity 0→1 + translateY 20px→0
- **No bounce, no spring** — gravity exists for luxury brands
- **Reduced motion:** Respect `prefers-reduced-motion`

### Borders & Corners

- **Sharp corners by default** (`border-radius: 0`) — architectural precision
- Subtle `2px` radius allowed for small UI elements only
- Border color: Champagne (`#D6C2A8`) for light surfaces; bronze-tinted on dark

### Cards & Containers

- Minimal: thin 1px champagne border, no shadow (or subtle warm shadow)
- Generous padding: 28–48px
- Never rounded-corner cards with colored left-border accent — avoid

### Shadows

Warm-toned only — no cold grey shadows:

```
--shadow-sm:  0 2px 8px rgba(58,45,37,0.08)
--shadow-md:  0 4px 20px rgba(58,45,37,0.10)
--shadow-luxury: 0 24px 80px rgba(58,45,37,0.20)
```

### Hover & Interaction States

- Buttons: background darkens (walnut → walnut-dark)
- Links: color shifts walnut → walnut-dark; underline appears
- Cards (clickable): shadow deepens sm → md
- No opacity-based hover — color-based only

### Imagery

- Luxury interiors, bespoke furniture, architectural detail
- Warm color grading — amber/golden tones, never cool-blue
- High contrast, editorial composition
- Never stock-photo-looking; always aspirational and specific
- Aspect ratios: 16:9 for landscape, 3:4 for portrait project cards

---

## Iconography

- **No icon font bundled.** FurnishIQ does not use an icon library by default.
- Use **Lucide Icons** (CDN) for any UI icons needed: clean, 1.5px stroke, geometric — matches the brand's architectural precision. Load via: `https://unpkg.com/lucide@latest/dist/umd/lucide.min.js`
- **No emoji** in brand communications.
- Directional indicators: use simple SVG arrows (thin, sharp) rather than chevrons.
- Decorative elements: diamond `◆` (rotated square), thin horizontal lines — geometric, minimal.

---

## File Index

```
/
├── styles.css                    ← Entry point (import only)
├── tokens/
│   ├── colors.css                ← Brand + semantic color tokens
│   ├── typography.css            ← Font imports + type scale
│   ├── spacing.css               ← 4px base spacing system
│   ├── effects.css               ← Shadows, radii, transitions
│   └── base.css                  ← Global reset & element defaults
├── assets/
│   ├── logo-default.png          ← White mark, transparent BG
│   ├── logo-dark.png             ← White mark on charcoal
│   └── logo-green.png            ← White mark on brand green
├── components/
│   ├── core/
│   │   ├── Button.jsx/.d.ts      ← 6 variants, 4 sizes
│   │   ├── Card.jsx/.d.ts        ← 5 variants
│   │   ├── Badge.jsx/.d.ts       ← 7 variants, 3 sizes
│   │   └── Divider.jsx/.d.ts     ← line, ornamental, labeled
│   ├── forms/
│   │   ├── Input.jsx/.d.ts       ← label, hint, error, disabled
│   │   ├── Select.jsx/.d.ts      ← dropdown with custom arrow
│   │   └── Textarea.jsx/.d.ts    ← multi-line input
│   └── navigation/
│       └── Nav.jsx/.d.ts         ← light, dark, transparent
├── guidelines/                   ← @dsCard specimen files
│   ├── colors-brand.card.html
│   ├── colors-semantic.card.html
│   ├── colors-tints.card.html
│   ├── type-display.card.html
│   ├── type-body.card.html
│   ├── type-scale.card.html
│   ├── spacing.card.html
│   ├── spacing-layout.card.html
│   ├── effects.card.html
│   ├── brand-logo.card.html
│   └── brand-voice.card.html
├── ui_kits/
│   └── website/
│       └── index.html            ← Interactive website prototype
├── readme.md                     ← This file
└── SKILL.md                      ← AI agent skill definition
```

---

## AI Brand Implementation Instructions

```markdown
# FurnishIQ AI Brand Implementation Instructions
# Version 1.0 — June 2025
# Use this block when generating any FurnishIQ brand asset with AI.

## Brand Personality
- Premium luxury interior design & fit-out company
- Saudi-based, GCC-focused
- Authoritative, refined, visionary, warmly human
- Comparable feel to: Armani Casa, Minotti, Poliform — never startup, never corporate-generic

## Tone of Voice
- Confident, never boastful
- Precise and considered — every word earns its place
- No exclamation marks. No superlatives without evidence.
- Third-person brand, first-person project team
- No emoji in any brand communication

## Typography Rules
- English Display/Headlines: Lama Sans Medium 500
- English Body/UI: Lama Sans Medium 500
- Arabic (all uses): GE SS Two Medium 500 — always RTL, `dir="rtl"` on the element
- All CTAs: uppercase, letter-spacing 0.2em
- Section labels: uppercase, 10–11px, letter-spacing 0.2em, Lama Sans Medium
- Font files: `LamaSans-Medium_English.ttf` and `GE_SS_Two_Medium_Arabic.otf` (brand-owned, local)
- ONLY these two fonts are permitted for ALL FurnishIQ materials:
  documentation, websites, marketing posts, ads, social media,
  proposals, presentations, and any other written or digital content.
- The logo wordmark appears in a condensed bold geometric style.
  It is NOT a typeface. Do NOT use or recreate it as body/headline type.
  Do NOT use serif fonts to match or approximate the logo lettering.
- Never use Cormorant Garamond, Georgia, Times New Roman, or any serif typeface
- Never use Jost, Inter, Roboto, Arial, or any non-brand font
- Never load fonts from Google Fonts CDN — use local @font-face only

## Color Usage Rules
- Primary palette: Walnut #5B4636, Dark Walnut #3A2D25, Bronze #8B6B4A
- Supporting: Taupe #B8A08C, Champagne #D6C2A8, Stone #F5F2ED
- Text: Charcoal #1F1F1F on light; Champagne #D6C2A8 on dark
- Brand Green #1C6B35: LOGO ONLY — never use in UI, print, or digital design
- Never use gradients. Never use cool grey tones.
- White backgrounds by default; Stone for secondary surfaces

## Logo Usage Rules
- Use provided PNG files only: logo-default.png, logo-dark.png, logo-green.png
- Never recreate, redraw, recolour, or modify the logo
- Approved backgrounds: white, charcoal (#1F1F1F), brand green (#1C6B35)
- Minimum clear space: equal to the height of the "F" in FURNISH IQ on all sides
- Never place on busy imagery without a solid protection zone

## Layout Rules
- White space is a luxury signal — be generous
- Minimum section padding: 64px top/bottom; ideal 96–128px
- Sharp corners (border-radius: 0) as the default for all containers
- Editorial grid: 12-column, 32px gutter
- Container max-width: 1440px; content max-width: 1280px
- Horizontal padding: min 20px mobile, max 80px desktop (fluid)

## Photography Rules
- Warm color grading: amber/golden tones — never cool-blue
- High-contrast, editorial composition — never flat, never stock-photo-looking
- Subject: luxury interiors, bespoke furniture, architectural detail, material craft
- Aspect ratios: 16:9 landscape, 3:4 portrait project cards
- Always specific and aspirational — never generic

## Social Media Rules
- Square format: 1:1 (1080×1080px)
- Stories: 9:16 (1080×1920px)
- Background: always white, stone, charcoal, or walnut — never bright colors
- Typography: Lama Sans for English headline and caption; GE SS Two for any Arabic text
- Logo: always use the appropriate variant for the background
- No emoji, no gradient backgrounds, no clip-art

## Website Design Rules
- Full-width hero with dark overlay (charcoal or walnut-dark background)
- Navigation: 80px height, thin bottom border, logo left, links center, CTA right
- Service sections: alternate white and stone backgrounds
- Project cards: 3:4 portrait image + minimal text overlay
- Footer: dark walnut background, champagne text
- Mobile: single column, 20px gutter, stack all grid layouts

## Proposal Design Rules
- Cover: dark walnut background, Lama Sans headline, centered logo
- Interior pages: white background, generous margins (min 40mm)
- Section dividers: thin champagne line + diamond ornament
- Typography hierarchy: H1 Lama Sans, H2 Lama Sans, body Lama Sans; Arabic text uses GE SS Two throughout
- Color accents: walnut and bronze only — never green in proposals

## Presentation Design Rules
- Slide size: 1920×1080px (16:9)
- Background: white or dark walnut alternating for section breaks
- Minimum font size: 24px for body, 48px+ for headlines
- Consistent left-aligned text; right-aligned for pull quotes
- One key point per slide — never text-heavy

## Marketing Design Rules
- Lead with imagery — 60% of composition should be visual
- Headline: short, evocative, Lama Sans display
- Body copy: 14–16px Lama Sans, max 2–3 sentences
- CTA: uppercase button, walnut fill
- No busy backgrounds, no competing focal points

## Interior Design Portfolio Rules
- Project name: Lama Sans Medium 500, large
- Location + area: Lama Sans caption, bronze color
- Sector badge: uppercase, champagne or walnut variant
- Image grid: masonry or 2–3 column editorial
- Client attribution: only with explicit permission

## UI/UX Design Rules
- Sharp corners everywhere (no rounded cards)
- Form fields: 1px champagne border, 50px height default
- Buttons: uppercase, 0.2em letter-spacing, sharp corners
- Loading states: thin bronze animated underline
- Error states: warm red #9B2C2C (never neon red)
- Focus states: 2px walnut border, no blue outline

## Do Not Rules
- ✗ Do not use gradients of any kind
- ✗ Do not use bright, saturated colors
- ✗ Do not use emoji in any brand touchpoint
- ✗ Do not use rounded corners as the default
- ✗ Do not use Cormorant Garamond, Georgia, Times New Roman, or any serif typeface
- ✗ Do not use Jost, Inter, Roboto, Arial, or any non-brand font as primary fonts
- ✗ Do not load fonts from Google Fonts CDN — use local brand font files only
- ✗ Do not use the logo wordmark style (condensed bold geometric) as a typeface for content
- ✗ Do not recreate or mimic the logo lettering with serif or display fonts
- ✗ Do not use the brand green (#1C6B35) anywhere except the logo
- ✗ Do not recreate or modify the logo in any way
- ✗ Do not use exclamation marks in copy
- ✗ Do not use "world-class" or "best-in-class" without evidence
- ✗ Do not use cool-grey shadows or cold image grading
- ✗ Do not use startup or technology visual aesthetics
- ✗ Do not use cards with colored left-border only (generic corporate)

## AI Content Generation Rules
- Always reference this document before generating any FurnishIQ asset
- Maintain walnut/bronze/champagne/stone palette strictly
- Match Lama Sans (English) + GE SS Two (Arabic) typography system — local font files only, no Google Fonts
- ONLY Lama Sans and GE SS Two are permitted — this applies to ALL content types:
  websites, marketing, ads, social media, documentation, proposals, presentations
- The FurnishIQ logo contains a condensed geometric wordmark. This is the logo only.
  Never use a serif font to recreate or approximate the logo style in any content.
- Write in the brand's authoritative, refined tone
- Verify logo usage rules before placing any logo
- When in doubt: more white space, less decoration, sharper corners
```

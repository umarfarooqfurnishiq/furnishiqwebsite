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



# Debugging & Feedback Rules

Read when fixing a bug (reported or found in testing) or when handed raw error
output. The two load-bearing rules in the global core — manual verification beats
tests, and no self-declared completion — apply throughout this file.

## 1. Debugging Protocol (mandatory sequence)

No shortcuts, no exceptions.

```
1. REPRODUCE   → trigger the bug in the running app; confirm it exists
2. PROVE       → trace to root cause in code; verify the hypothesis before touching anything
3. FIX         → apply the targeted change only
4. DEMONSTRATE → re-run, trigger the same scenario, confirm the bug is gone
5. REPORT      → root cause, what changed, how you confirmed the fix
```

Never apply a speculative fix and declare victory. If you haven't reproduced and
proved it, you haven't fixed it.

- Do not repeat a failed fix. If a fix failed once, re-analyse from scratch — do
  not reapply the same change.
- Do not paper over failures. If something cannot be fixed, say so clearly rather
  than hiding it behind a workaround.
- One anecdotal match is not a root cause. A single old Stack Overflow or GitHub
  issue that resembles the symptom is not proof. Before declaring a known issue,
  verify: did more than one person report it? Is it recent and relevant? Does the
  evidence actually match the current symptom? Challenge "found it, just downgrade
  X" hard.
- Prove the cause before fixing and the fix after: reproduce consistently →
  identify root cause → show that this specific cause produces the bug → fix →
  show the same scenario now works consistently. Document each step.

## 2. Handling Feedback

- Treat a list of issues as a prioritised work queue — address each explicitly and
  in order.
- Apply UI feedback (colours, layout, sizing) literally, then confirm.
- After each fix, run the app and verify before reporting. Do not bundle multiple
  fixes into one report without confirming each one individually.
- Raw error output (terminal errors, stack traces, console logs) with no
  explanation is a bug report. Apply the protocol in Section 1; only ask for more
  context if the error is genuinely undiagnosable.

## 3. Recording Lessons

After a non-trivial fix, record the lesson so it survives context compaction or a
chat reset — but **not** in CLAUDE.md, which is human-owned and gitignored.
Write a brief note to the project's `docs/lessons.md` (create it if absent). This
keeps the lesson committed and visible to the team, without self-authoring the
instructions you operate under.

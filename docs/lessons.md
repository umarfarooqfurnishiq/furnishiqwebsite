# Lessons

## Mandatory scroll-snap breaks short carousels (2026-09-24)

**Symptom:** On the Arabic turnkey landing page's services carousel, "next" took several clicks to move, and "previous" could not get back to the start at 1440px wide.

**Root cause:** The track used `scroll-snap-type: x mandatory` with a snap point at each card. At wide viewports the cards overflowed by only 152px, which is less than one card step (about 364px). No second snap point was reachable, so the browser kept snapping back to the only valid position.

**Fix:** Removed scroll-snap from carousels that overflow by less than a card at common widths. The arrows use `scrollBy` with a card-width step, so snapping isn't needed.

**Testing note:** In the Playwright browser these `.dc.html` pages render at about 2fps (a blank page runs at 60), so smooth scrolls land seconds late and timing-based checks give misleading results. The committed baseline shows the same, so it predates this work. Emulate `prefers-reduced-motion: reduce` so scrolls happen instantly when checking carousel logic.

## Use relative asset paths (`uploads/…`, `assets/…`), never root-absolute (`/uploads/…`)
Pages are also opened straight from disk (file://). A root-absolute `/uploads/x.jpg` then resolves to the drive root (`D:/uploads/x.jpg`) and the image breaks, while a local http server and Vercel both hide the bug. Relative paths work in all three: on Vercel, `/ar/<slug>` pages resolve `uploads/x.jpg` to `/ar/uploads/x.jpg`, which the `/ar/:path*` rewrite maps back to `Furnishiq.net/uploads/`.

## Clone-loop carousels break if the cards get too narrow
The looping carousels (`[clones][originals][clones]`) only wrap if one set of cards is wider than the visible track plus one gap: `set >= trackWidth + gap - 2`. Below that, the track's max scroll (`3*set - trackWidth - gap`) is smaller than the jump-back point (`2*set - 2`), so the normaliser never fires and "next" sticks at the end. Shrinking the package cards to fit short screens hit this. The fix was a CSS width floor (`track/3 - 12px`). When resizing any looping card, check `scrollWidth - clientWidth >= 2*set - 2` at several viewports, and click through past the end in both directions.

## Scroll reveals: never observe an element that is fully clipped by its own clip-path
- Symptom: on the English turnkey landing page, a "wipe" reveal (`clip-path: inset(0 0 100% 0)` → `inset(0)`) never played, so the image stayed invisible forever, along with anything nested inside it.
- Cause: Chrome's IntersectionObserver applies the target's own clip-path; a fully clipped element has zero visible area and is never reported as intersecting.
- Fix: observe the element's container instead (a target → element map), and reveal nested reveal elements together with the wipe.
- Rule: any start state that hides an element's box entirely (clip-path, `scale(0)`) must be triggered from an unclipped container. Opacity and translate start states are fine to observe directly.

## Don't start the hero headline or intro at opacity 0
- Symptom: on the turnkey landing pages, mobile LCP was 3.8s (EN) and 9.5s (AR). Lighthouse attributed 1.7s and 4.0s of that to "element render delay".
- Cause: the LCP element (the hero H1 or intro paragraph) had an entrance animation starting at `opacity:0`. Chrome ignores invisible text for LCP, so LCP waited for the JS reveal plus its delay and transition.
- Fix: the hero text uses a `sharpen` reveal (`opacity:1`, blur and offset only). Render delay dropped to 0.3–0.4s.
- Rule: animate above-the-fold text with transform/filter only. Keep fade-from-zero for content below the fold.

## Inline `display` beats a stylesheet rule
- Symptom: `.fiq-vid-slide[data-video-src=""] .fiq-vid-play{display:none}` matched but had no effect.
- Cause: the buttons carry `display:flex` inline.
- Rule: when hiding an element whose layout is set in a `style=""` attribute, use `!important` (or move its layout into the stylesheet).

## Video seeking fails under `python -m http.server` (2026-09-29)
- Symptom: the landing-page video plays, but dragging the progress bar snaps back to ~0s.
- Cause: Python's `http.server` ignores `Range` requests (returns 200, no `Accept-Ranges`), so `video.seekable` is `[0,0]`. Vercel serves ranges, so production seeks fine.
- Test video seeking locally with a range-capable server, e.g. `npx http-server -p 8766 -s -c-1`.
- Related: the site-wide form input style adds a 1px border to every `<input>`, including `type="range"`; the custom seek bar needs `border:none!important`.

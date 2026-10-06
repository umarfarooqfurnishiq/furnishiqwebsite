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

## Template renderer drops `muted` and `loop` on `<video>` (2026-10-04)
- Symptom: the project-page hero film loaded but never autoplayed (worked on one desktop test, failed on mobile and in a normal browser).
- Cause: the `.dc.html` template renderer leaves `video.muted === false` even when the markup says `muted`. Browsers only autoplay muted video, so `play()` is rejected. Chrome's media-engagement score on localhost can hide this during testing.
- Fix: set `v.muted = true; v.defaultMuted = true; v.loop = true;` in JS before calling `play()`. Assume any boolean attribute may be dropped and set it as a property.
- Also: Windows "Animation effects" off sets `prefers-reduced-motion: reduce`. The owner chose to autoplay project films regardless (2026-10-04), so a visible pause button is mandatory. Never ship looping video without one.

## Project-detail pages lacked mobile footer rules (2026-10-04)
- Symptom: on phones the Arabic project page shifted about 95px sideways, cutting off the hero title.
- Cause: `.fiq-footer-grid` (4 columns) had no `@media` override on `project-detail(.ar).dc.html`; every other page has one.
- When creating a new page from a template, copy the full `@media(max-width:960px)` and `@media(max-width:600px)` blocks, including the footer rules.

## Scrolling to an element that is still animating in (2026-10-04)
- Symptom: opening a project quick view on `projects(.ar).dc.html` left its top ~45px hidden under the fixed nav.
- Cause: `scrollToDetail` used `getBoundingClientRect().top` 60ms after insertion, while the `fiqDetailIn` slide-in (`translateY(64px)`) was still running. The rect included about 55px of transform, so the target was too low.
- Fix: sum `offsetTop` up the `offsetParent` chain (layout position, ignores transforms) and subtract the real nav height (`#id-nav.offsetHeight`).

## The template renderer rewrites inline `style` attributes (2026-10-04)
- Symptom: a phone-only rule written as `.fiq-detail-scroll > div[style*="gap:14px"]{flex-wrap:wrap}` matched in the source file but never applied in the browser.
- Cause: the `.dc.html` renderer re-serialises inline styles (`gap:14px` becomes `gap: 14px`), so a selector that matches the style text finds nothing.
- Rule: never select elements by their `style` attribute text. Add a class (here `.fiq-detail-meta`) and target that.
- Related: bound attributes such as `srcset="{{ project.srcset }}"` log "Dropped srcset candidate" warnings while the template placeholder is on screen. They are harmless; the bound value loads correctly once rendered.

## Pages under a nested URL need a matching asset rewrite (2026-10-05)
- Pages load `./support.js`, `uploads/...` and `_ds/...` with relative paths, so a page served at `/blog/<slug>` asks for `/blog/support.js`.
- Fix: every nested prefix needs a catch-all rewrite to the site root, placed after its specific page rewrites and before the broader catch-alls (`/blog/:path*` and `/ar/blog/:path*` → `/Furnishiq.net/:path*`, like the existing `/ar/:path*`).
- Check with `curl` on `/<prefix>/support.js` and one image under the prefix; both should return 200.

## The template renderer drops the boolean `hidden` attribute (2026-10-05)
- Symptom: the footer newsletter "Thank you" line showed on page load on every page.
- Cause: `<p hidden ...>` lost its `hidden` attribute when the `.dc.html` renderer rebuilt the DOM.
- Rule: hide template-rendered elements with an inline `style="display:none"` and toggle `style.display` in script.

## Replacing the site footer: match the site footer, not any `<footer>` (2026-10-05)
- Symptom: on article pages the new footer appeared inside the pull quote and the old footer stayed at the bottom, widening the article on phones.
- Cause: a quote attribution `<footer>` inside `<blockquote>` came before the site footer, and the replacement matched the first `<footer>`.
- Rule: select the site footer by `id="fiq-footer"` or its own `background:#1F1F1F` style, and confirm each page ends with exactly one `#fiq-footer`.

## Section spacing standard (2026-10-05)
- Every content section uses `padding: clamp(64px,8vw,100px)` top and bottom (100px on desktop, 64px minimum on phones), with `clamp(24px,5vw,80px)` at the sides.
- Exceptions: page heroes (the first section, which also clears the fixed header) and full-bleed layouts that carry their spacing on inner elements.
- When adding a section, use the standard value; do not reintroduce 120/128/136px variants.

## Uncommitted pages can be wiped by an abrupt shutdown (2026-10-05)
- Symptom: after the session ended abruptly, `about-us.dc.html`, `about-us.ar.dc.html` and one build script kept their byte length but every byte was zero. A day of uncommitted About page work was gone from disk.
- Recovery: restore the pages from the last commit, rerun each section's build script (each rebuilds its whole section), then replay the few direct page edits recorded in the session transcript.
- Rule: keep generated sections reproducible from scripts, and commit (or copy) work-in-progress pages after each approved section instead of leaving a whole page's redesign uncommitted.

## Adding z-index to one layer can bury its unindexed siblings (2026-10-05)
- Symptom: on the About hero, the headline, labels and figures lost contrast. The photo looked bright and the text faded into it.
- Cause: the crossfade fix gave the slides `z-index:1`/`2`. The dark veil and the bottom fade sat after them in the markup with no z-index, so the slides now painted above both.
- Fix: give every layer in the stack an explicit place (slides 1–2, veil and fade 3, copy 4, opening doors 6), noted in a comment next to the rules.
- Rule: when adding z-index to an element, check every positioned sibling in the same container, and confirm the result with `document.elementsFromPoint` rather than by eye.

## A sed that appends a comment can swallow the rest of the line (2026-10-06)
- Symptom: on phones the Services autoplay (MEP, Furniture, Process) stopped advancing; the first stage drew in and nothing followed.
- Cause: the loop line held two statements, `const dt = ...; then = now;`. A sed replacement put a `//` comment after the first statement, which commented out `then = now`, so `then` stayed 0 and `dt` was always 0. It was introduced while chasing a different stall: the test browser was rendering at about 1 frame per second, which the old 100 ms cap per frame made look like a broken cycle.
- Fix: one statement per line, the comment on its own line above; time the cycle from the real gap between frames and reset it on `visibilitychange` rather than capping each frame.
- Rule: never append a comment with sed to a line that may hold more than one statement; re-read the generated line after any sed edit. When a timed loop stalls in Playwright, measure the frame rate (`requestAnimationFrame` count over 2 s) before changing the code.

## A stretched SVG line with pathLength dashes stops short (2026-10-06)
On the Services finale, a dimension line drawn as `<svg preserveAspectRatio="none">` with `pathLength="1"`,
`stroke-dasharray:1 1` and `vector-effect:non-scaling-stroke` finished its draw-in about 280px short of the
end tick at 1440px. With a non-scaling stroke, Chrome measures the dash in screen space while `pathLength`
normalises in user space, so a non-uniformly stretched path never fully dashes in. For a straight line that
must span a fluid width, use a CSS element animated with `transform:scaleX(0 → 1)` instead; keep the SVG
dash technique for paths drawn at a uniform scale (`meet`/`slice`).

## `@property` registrations are global: namespace them (2026-10-06)
The Services Process section registered `@property --h { syntax:'<number>' }` to animate its handover. The
registration applies to the whole document, so the Interior Design section's viewfinder, which sets
`--h: 80%` for its height, became invalid at computed-value time and fell back to the initial `0`: the frame
collapsed to a 2px line and its dimming shadow darkened the whole photo. Generic one-letter custom
properties are fine while unregistered, but any property passed to `@property` must carry a section prefix
(`--pr-h`, `--pr-t`). Before registering one, grep the page for other uses of the name.

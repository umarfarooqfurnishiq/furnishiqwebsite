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

# Lessons

## Mandatory scroll-snap breaks short carousels (2026-09-24)

**Symptom:** On the Arabic turnkey landing page's services carousel, "next" took several clicks to move, and "previous" could not get back to the start at 1440px wide.

**Root cause:** The track used `scroll-snap-type: x mandatory` with a snap point at each card. At wide viewports the cards overflowed by only 152px, which is less than one card step (about 364px). No second snap point was reachable, so the browser kept snapping back to the only valid position.

**Fix:** Removed scroll-snap from carousels that overflow by less than a card at common widths. The arrows use `scrollBy` with a card-width step, so snapping isn't needed.

**Testing note:** In the Playwright browser these `.dc.html` pages render at about 2fps (a blank page runs at 60), so smooth scrolls land seconds late and timing-based checks give misleading results. The committed baseline shows the same, so it predates this work. Emulate `prefers-reduced-motion: reduce` so scrolls happen instantly when checking carousel logic.

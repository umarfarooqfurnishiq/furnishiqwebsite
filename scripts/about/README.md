# About page build scripts

Each script rebuilds one section of the About page, in both `about-us.dc.html` (English) and `about-us.ar.dc.html` (Arabic). It replaces that section's markup and its script block, so running it again is safe.

Run from the `Furnishiq.net` folder:

```
cd Furnishiq.net
PYTHONIOENCODING=utf-8 python ../scripts/about/about_journey.py
```

| Script | Section (marker comment in the page) |
|---|---|
| `about_film.py` | PAGE HERO: studio film slides |
| `about_pillars.py` | WHY FURNISHIQ: four pillars |
| `about_compass.py` | BRAND STATEMENT: mission, vision, values |
| `about_story.py` | OUR STORY: 2007, needs map, Arsan Global orbit |
| `about_chair.py` | MESSAGE FROM CEO |
| `about_gates.py` | THREE PILLARS: The FurnishIQ Edge checkpoints |
| `about_services.py` | INTEGRATED SERVICES: discipline tabs |
| `about_journey.py` | FOUR-STEP PROCESS: one room, four states |
| `about_markets.py` | MARKETS WE SERVE |
| `about_studio.py` | STUDIO / CONTACT: the threshold |

Running all ten in the order above reproduces both pages. Only the order of the script blocks near the end of each page changes, because each run moves its own block last; behaviour is unaffected.

Helpers:
- `yr_outline.py` generates the double-line outline of "2007" used in `about_story.py` (needs `shapely`).
- `cta_pairs.py` applies the site-wide button-pair rules (equal width, full width on phones, inverse hover on the outlined button) to the home, projects and thank-you pages.
- `cta_audit.py` lists every container on a page that holds two or more button-style links.

Edit a section by changing its script and rerunning it. Edits made directly in the page are overwritten the next time that section's script runs.

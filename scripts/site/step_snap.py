"""Site: step snap. One wheel notch, one step, in every section that pins and plays in steps.

A pinned section played in steps (the services page's MEP, furniture and process; the service pages' reveal
and designer's desk; the about page's compass and journey) registers its scroll range and the scroll position
of each step with one shared block on the page. Inside a registered section a wheel notch, or an arrow, page or
space key, glides to the next step and then waits for the wheel to settle, so a fast notch or a trackpad's
run-on never skips a step. Past the first or the last step the page scrolls on as usual. A scroll that ends
between two steps, from the scrollbar or anything else, settles on the nearer.
Sections that scrub continuously (the about page's pillars, threshold and chairman's quote, the home page's
stacked floors) keep plain scrolling.

This script adds the shared block to each page, and adds each section's registration to its page and to the
generator that builds it, so a later run of that generator keeps it.
Run from the repository root: PYTHONIOENCODING=utf-8 python scripts/site/step_snap.py
"""
import io, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SITE = os.path.join(ROOT, "Furnishiq.net")
MARK = "    // ── SCROLL REVEAL"
HEAD = "    // ── STEP SNAP: ONE WHEEL NOTCH, ONE STEP"
WIDE = "matchMedia('(min-width:901px) and (min-height:600px)').matches"

HELPER = HEAD + """ ──────────────────────────────
    // Sections pinned and played in steps register in window.fiqSnap as { on, geo }: on() says whether the
    // section is pinned now, geo() gives a..b, the scroll range it holds, and stops, the scroll position of
    // each step. Inside one, a wheel notch or an arrow, page or space key glides to the next step, then waits
    // for the wheel to settle, so a fast notch or a trackpad's run-on never skips a step. Past the first or the
    // last step the page scrolls on. A scroll that ends between two steps settles on the nearer.
    {
      const reg = window.fiqSnap = window.fiqSnap || [];
      let gliding = false, held = false, lastWheel = 0;
      const glide = window.fiqGlide = (to) => {
        held = true;
        if (reduced) { window.scrollTo({ top: to, behavior: 'instant' }); return; }
        gliding = true;
        const from = window.scrollY, d = to - from, t0 = performance.now(), T = 650;
        const frame = (now) => {
          const t = Math.min(1, (now - t0) / T);
          window.scrollTo({ top: from + d * t * (2 - t), behavior: 'instant' });
          if (t < 1) requestAnimationFrame(frame); else gliding = false;
        };
        requestAnimationFrame(frame);
      };
      // the registered section holding the page now
      const here = () => {
        const y = window.scrollY;
        for (const s of reg) { if (!s.on()) continue; const g = s.geo(); if (y >= g.a - 1 && y <= g.b + 1) return g; }
        return null;
      };
      const next = (g, dir) => {
        const y = window.scrollY;
        if (dir > 0) { for (const v of g.stops) if (v > y + 4) return v; }
        else { for (let j = g.stops.length - 1; j >= 0; j--) if (g.stops[j] < y - 4) return g.stops[j]; }
        return null;
      };
      window.addEventListener('wheel', (e) => {
        if (e.ctrlKey || Math.abs(e.deltaY) < Math.abs(e.deltaX)) return;
        // the gap between notches as the hand made them, not as a busy page got round to them
        const now = e.timeStamp || performance.now(), quiet = now - lastWheel > 200;
        lastWheel = now;
        const g = here();
        if (gliding || (held && !quiet)) { if (g) e.preventDefault(); return; }
        held = false;
        if (!g) return;
        const to = next(g, Math.sign(e.deltaY));
        if (to === null) return;
        e.preventDefault(); glide(to);
      }, { passive: false });
      window.addEventListener('keydown', (e) => {
        if (e.altKey || e.ctrlKey || e.metaKey) return;
        const el = document.activeElement;
        if (el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName) || (e.key === ' ' && /^(BUTTON|A)$/.test(el.tagName)))) return;
        const dir = { ArrowDown: 1, PageDown: 1, ArrowUp: -1, PageUp: -1, ' ': e.shiftKey ? -1 : 1 }[e.key];
        if (!dir) return;
        const g = here();
        if (!g) return;
        if (gliding) { e.preventDefault(); return; }
        const to = next(g, dir);
        if (to === null) return;
        e.preventDefault(); glide(to);
      });
      window.addEventListener('scrollend', () => {
        if (gliding) return;
        const g = here();
        if (!g) return;
        const y = window.scrollY, n = g.stops.length;
        if (y <= g.stops[0] + 1 || y >= g.stops[n - 1] - 1) return;
        const to = g.stops.reduce((m, v) => (Math.abs(v - y) < Math.abs(m - y) ? v : m));
        if (Math.abs(to - y) > 2) glide(to);
      });
    }

"""

# (block header, line in that block to register after, the registration, generator, pages)
SVC = ["services.dc.html", "services.ar.dc.html"]
SP = [f"{p}{l}.dc.html" for p in ("services-interior-design", "services-fitout", "services-mep", "services-furniture") for l in ("", ".ar")]
ABOUT = ["about-us.dc.html", "about-us.ar.dc.html"]
STEPPED = "(window.fiqSnap = window.fiqSnap || []).push({ on: () => pinned, geo: () => { const g = geo(); return { a: g.start, b: g.start + g.dist, stops: Array.from({ length: STEPS }, (_, j) => g.start + g.dist * (j + 0.5) / STEPS) }; } });"
SCROLL = "        window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });\n"
GOTO = "        const goTo = (i) => { const g = geo(); window.scrollTo({ top: g.start + g.dist * (i + 1.5) / STEPS, behavior: reduced ? 'auto' : 'smooth' }); };\n"
PATCHES = [
    ("    // ── SERVICES, MEP:", GOTO,
     "        // one wheel notch, one state (STEP SNAP)\n        " + STEPPED + "\n",
     "services/svc_mep.py", SVC),
    ("    // ── SERVICES, FURNITURE:", GOTO,
     "        // one wheel notch, one state (STEP SNAP)\n        " + STEPPED + "\n",
     "services/svc_furniture.py", SVC),
    ("    // ── SERVICES, PROCESS:", SCROLL,
     "        // one wheel notch, one stage, resting where it has finished drawing (STEP SNAP)\n"
     "        (window.fiqSnap = window.fiqSnap || []).push({ on: () => pinned, geo: () => { const g = geo(); return { a: g.start, b: g.start + g.dist, stops: Array.from({ length: N }, (_, j) => g.start + g.dist * (j + 0.8) / N) }; } });\n",
     "services/svc_process.py", SVC),
    ("    // ── SERVICE PAGES, INTRO: THE REVEAL", "        const TARGET = [A * 0.5, (A + B) / 2, 1];\n",
     "        // one wheel notch, one stage: drawn, rendering, approved (STEP SNAP)\n"
     "        (window.fiqSnap = window.fiqSnap || []).push({ on: () => pinned, geo: () => { const g = geo(); return { a: g.start, b: g.start + g.dist, stops: TARGET.map((t) => g.start + g.dist * t) }; } });\n",
     "servicepages/sp_reveal.py", SP),
    ("    // ── WHO WE ARE: COMPASS", "        pick(0); update();\n",
     "        // one wheel notch, one statement (STEP SNAP)\n"
     "        (window.fiqSnap = window.fiqSnap || []).push({ on: () => " + WIDE + ", geo: () => { const a = cp.getBoundingClientRect().top + window.scrollY, total = cp.offsetHeight - window.innerHeight; return { a, b: a + total, stops: rows.map((_, i) => a + total * (i + 0.5) / rows.length) }; } });\n",
     "about/about_compass.py", ABOUT),
    ("    // ── JOURNEY: ONE ROOM", "        update();\n",
     "        // one wheel notch, one state: survey, drawing, build, handover, then the call (STEP SNAP)\n"
     "        (window.fiqSnap = window.fiqSnap || []).push({ on: () => " + WIDE + ", geo: () => { const a = jr.getBoundingClientRect().top + window.scrollY, total = jr.offsetHeight - window.innerHeight; return { a, b: a + total, stops: [0.16, 0.352, 0.592, 0.8, 1].map((t) => a + total * t) }; } });\n",
     "about/about_journey.py", ABOUT),
]


def register(s, head, anchor, reg, where):
    a = s.index(head)
    ends = [i for i in (s.find("\n    // ── ", a + 1), s.find('"""', a + 1)) if i != -1]
    b = min(ends)
    block = s[a:b]
    if "fiqSnap" in block:
        return s
    assert anchor in block, (where, head)
    k = a + block.index(anchor) + len(anchor)
    return s[:k] + reg + s[k:]


def helper(s, where):
    if HEAD in s:
        a = s.index(HEAD); b = s.index("\n    // ── ", a + 1) + 1
        s = s[:a] + s[b:]
    assert s.count(MARK) == 1, where
    return s.replace(MARK, HELPER + MARK)


def rw(path, fn):
    s = io.open(path, encoding="utf-8").read()
    t = fn(s)
    if t != s:
        io.open(path, "w", encoding="utf-8", newline="").write(t)
    print(os.path.relpath(path, ROOT), "ok" if t != s else "unchanged")


if __name__ == "__main__":
    pages = sorted({p for *_, ps in PATCHES for p in ps})
    for head, anchor, reg, gen, ps in PATCHES:
        rw(os.path.join(ROOT, "scripts", gen), lambda s: register(s, head, anchor, reg, gen))
        for p in ps:
            rw(os.path.join(SITE, p), lambda s: register(s, head, anchor, reg, p))
    for p in pages:
        rw(os.path.join(SITE, p), lambda s: helper(s, p))

"""Replace every Unsplash photo on the live pages with the studio's own photography.

Each Unsplash image is one "slot": an <img> (src and srcset together), a CSS url(), a JS string or a
share-image meta tag. An <img> takes the local photograph matched to its alt text; anything without a
telling alt takes the photograph matched to the Unsplash photo it replaces. The Arabic page of each pair
takes the English page's choices slot by slot, since its alt texts are translated. srcsets are rebuilt
from the widths that exist locally; share images get a 1200 x 630 JPEG cut from the largest file.
Run from the repo root: PYTHONIOENCODING=utf-8 python scripts/site/replace_unsplash.py
"""
import os, re
from collections import Counter
from PIL import Image

SITE = "Furnishiq.net"
UP = os.path.join(SITE, "uploads")
PAGES = ["home", "about-us", "contact", "projects", "project-detail", "services-fitout", "services-furniture",
         "services-interior-design", "services-mep", "thank-you"]

BY_ALT = {
    "Retail": "maison-joaillerie-main-salon-jeddah",
    "Soft Furnishings &amp; Textiles": "furniture-gallery-bedroom-suite",
    "Artisanal furniture sourced globally": "bespoke-furniture-leather-lounge-chair-riyadh",
    "Bespoke &amp; Artisanal Pieces": "furniture-gallery-oak-brass-detail",
    "Plumbing Systems": "penthouse-wadi-master-suite-spa-bath",
    "Structural architecture": "office-shell-and-core-before-fit-out-riyadh",
    "Brand-led interior layout planning": "luxury-office-fit-out-riyadh",
    "Brand-led office interior design": "executive-floors-client-majlis",
    "MEP systems integrated into a space": "mep-ceiling-services-installation-riyadh",
    "Workplace": "executive-floors-sky-lobby-reception-riyadh",
    "Fire Fighting Systems": "mep-ceiling-services-installation-riyadh",
    "On-site quality and safety oversight": "pillar-quality-assurance-level-inspection",
    "Brand-led corporate furniture selection": "executive-floors-boardroom-walnut-table",
    "Outdoor &amp; Hospitality Furniture": "obhur-estate-beach-pavilion-lounge",
    "Engineering and MEP integrated behind the finish": "mep-ceiling-services-installation-riyadh",
    "Low Current Systems": "central-commons-office-lobby",
    "Workstations &amp; Office Furniture": "executive-floors-chairman-office",
    "Electrical Systems": "executive-floors-walnut-ceiling-detail",
    "MEP Coordination": "pillar-project-management-riyadh-timeline",
    "Furniture curated to the approved 3D renders": "furniture-render-to-room-4-styled",
    "Styling &amp; Placement": "furniture-gallery-living-room-set",
    "Color &amp; Mood Board Curation": "luxury-interior-design-material-board-riyadh",
    "Hospitality": "desert-stone-resort-lobby-lounge-alula",
    "Lounge &amp; Reception Seating": "desert-stone-resort-library-lounge",
    "Space Planning &amp; Layout": "about-mission-majlis-drawing-to-reality",
    "Partitions, Walls &amp; Ceilings": "luxury-villa-fit-out-travertine-staircase-walnut-wall-riyadh",
    "Residential": "courtyard-residence-grand-majlis-riyadh",
    "HVAC Systems": "central-commons-covered-galleria",
    "Joinery &amp; Millwork": "office-fit-out-walnut-wall-panel-installation-riyadh",
    "Flooring &amp; Wall Finishes": "family-office-limestone-bronze-detail",
    "Hand-finished walnut joinery detail": "about-values-walnut-dovetail-craft",
    "Material &amp; Finish Selection": "furniture-gallery-design-studio-material-library",
    "Photoreal 3D Visualization": "courtyard-residence-formal-dining-room",
    "Finished interior handed over to zero-snag standard": "pillar-end-to-end-delivery-key-handover",
    "Furniture, FF&amp;E &amp; Styling": "furniture-gallery-dining-room-set",
    "Styling &amp; Detailing": "courtyard-residence-majlis-seating-detail",
    "Implementation-ready design blueprint": "grand-majlis-line-drawing",
    "Lighting Design": "penthouse-wadi-backlit-onyx-detail",
    "Testing &amp; Commissioning": "pillar-quality-assurance-level-inspection",
}
BY_ID = {
    "1615874959474-d609969a20ed": "courtyard-residence-formal-dining-room",
    "1618221195710-dd6b41faaea6": "luxury-office-fit-out-riyadh",
    "1503387762-592deb58ef4e": "mep-ceiling-services-installation-riyadh",
    "1600210492486-724fe5c67fb0": "furniture-gallery-living-room-set",
    "1600607687939-ce8a6c25118c": "about-vision-desert-sunrise-lounge",
    "1581092160562-40aa08e78837": "mep-ceiling-services-installation-riyadh",
    "1555041469-a586c61ea9bc": "furniture-gallery-dining-room-set",
    "1600585154340-be6161a56a0c": "courtyard-residence-central-courtyard-reflecting-pool",
    "1521737604893-d14cc237f11d": "about-mission-majlis-drawing-to-reality",
    "1497366216548-37526070297c": "luxury-office-fit-out-riyadh",
    "1541976590-713941681591": "penthouse-wadi-double-height-living-riyadh",
    "1504307651254-35680f356dfd": "office-shell-and-core-before-fit-out-riyadh",
    "1590490360182-c33d57733427": "desert-stone-resort-lobby-lounge-alula",
    "1497366754035-f200968a6e72": "executive-floors-sky-lobby-reception-riyadh",
    "1441986300917-64674bd600d8": "maison-joaillerie-main-salon-jeddah",
    "1615529182904-14819c35db37": "luxury-interior-design-material-board-riyadh",
    "1618219740975-d40978bb7378": "grand-majlis-line-drawing",
    "1616486338812-3dadae4b4ace": "obhur-estate-great-room-red-sea-jeddah",
    "1586023492125-27b2c045efd7": "furniture-render-to-room-4-styled",
    "1524758631624-e2822e304c36": "executive-floors-boardroom-walnut-table",
    "1487958449943-2429e8be8625": "office-shell-and-core-before-fit-out-riyadh",
    "1449247709967-d4461a6a6103": "bespoke-furniture-leather-lounge-chair-riyadh",
    "1567016432779-094069958ea5": "executive-floors-chairman-office",
    "1613977257365-aaae5a9817ff": "office-fit-out-walnut-wall-panel-installation-riyadh",
    "1600607687920-4e2a09cf159d": "central-commons-covered-galleria",
    "1566073771259-6a8506099945": "central-commons-office-lobby",
    "1541888946425-d81bb19240f5": "mep-ceiling-services-installation-riyadh",
}

# per page, slot number -> photograph, where the alt or photo choice would repeat an image on the page
# (slots 0 and 1 are the paired share-image tags, slot 2 the hero, the last one the closing band)
SLOT_FIX = {
    "services-fitout": {0: "luxury-office-fit-out-riyadh", 1: "luxury-office-fit-out-riyadh", 2: "luxury-office-fit-out-riyadh",
                        3: "family-office-principal-office"},
    "services-furniture": {0: "furniture-gallery-atrium-stair-riyadh", 1: "furniture-gallery-atrium-stair-riyadh",
                           2: "furniture-gallery-atrium-stair-riyadh", 16: "roastery-house-leather-banquettes"},
    "services-interior-design": {0: "courtyard-residence-central-courtyard-reflecting-pool", 1: "courtyard-residence-central-courtyard-reflecting-pool",
                                 2: "courtyard-residence-central-courtyard-reflecting-pool", 3: "penthouse-wadi-double-height-living-riyadh",
                                 16: "family-office-guest-majlis"},
    "services-mep": {0: "office-shell-and-core-before-fit-out-riyadh", 1: "office-shell-and-core-before-fit-out-riyadh",
                     2: "office-shell-and-core-before-fit-out-riyadh", 4: "central-commons-central-atrium",
                     5: "pillar-project-management-riyadh-timeline", 9: "roastery-house-roasting-hall-riyadh",
                     16: "penthouse-wadi-oak-bronze-staircase-detail"},
}

U = r"https://images\.unsplash\.com/photo-([0-9a-f]+-[0-9a-f]+)(\?[^\"')\s,]*)?"
SLOT = re.compile(
    r"<img\b[^>]*images\.unsplash\.com[^>]*>"                      # an image, src and srcset
    r"|<meta\b[^>]*images\.unsplash\.com[^>]*>"                    # a share image
    r"|" + U)                                                      # a bare URL: CSS or JS


def widths(base):
    out = {}
    for f in os.listdir(UP):
        m = re.fullmatch(re.escape(base) + r"-(\d{3,4})\.(webp|jpg)", f)
        if m and (int(m.group(1)) not in out or m.group(2) == "webp"):
            out[int(m.group(1))] = f
    assert out, f"no local files for {base}"
    return dict(sorted(out.items()))


def pick(base, want):
    w = widths(base)
    return w[next((k for k in w if k >= want), max(w))]


def og(base):
    name = f"{base}-og.jpg"
    path = os.path.join(UP, name)
    if not os.path.exists(path):
        im = Image.open(os.path.join(UP, pick(base, 9999))).convert("RGB")
        r = 1200 / 630
        w, h = im.size
        if w / h > r: nw = int(h * r); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else: nh = int(w / r); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        im.resize((1200, 630), Image.LANCZOS).save(path, "JPEG", quality=86, optimize=True, progressive=True)
    return f"https://www.furnishiq.net/uploads/{name}"


def want_w(q):
    m = re.search(r"[?&]w=(\d+)", q or "")
    return int(m.group(1)) if m else 1600


def first_id(text):
    return re.search(U, text).group(1)


def choose(slot, en=True):
    alt = re.search(r'\balt="([^"]*)"', slot) if slot.startswith("<img") else None
    if en and alt and alt.group(1) in BY_ALT:
        return BY_ALT[alt.group(1)]
    return BY_ID[first_id(slot)]


def render(slot, base):
    if slot.startswith("<meta"):
        return re.sub(U, lambda m: og(base), slot)
    if slot.startswith("<img"):
        w = widths(base)
        srcset = ", ".join(f"uploads/{f} {k}w" for k, f in w.items())
        s = re.sub(r'\ssrcset="[^"]*"', f' srcset="{srcset}"', slot) if " srcset=" in slot else slot
        return re.sub(U, lambda m: "uploads/" + pick(base, want_w(m.group(2))), s)
    return "uploads/" + pick(base, want_w(re.match(U, slot).group(2)))


def process(text, plan=None, page=""):
    slots = [m for m in SLOT.finditer(text)]
    ids = [first_id(m.group(0)) for m in slots]
    if plan is None or [i for i, _ in plan] != ids:
        if plan is not None:
            print("   slot order differs from the English page: choosing by photo")
        plan = [(i, choose(m.group(0), en=plan is None)) for i, m in zip(ids, slots)]
        plan = [(i, SLOT_FIX.get(page, {}).get(k, b)) for k, (i, b) in enumerate(plan)]
    out, last = [], 0
    for m, (_, base) in zip(slots, plan):
        out.append(text[last:m.start()]); out.append(render(m.group(0), base)); last = m.end()
    out.append(text[last:])
    text = "".join(out)
    text = re.sub(r'\s*<link[^>]*(preconnect|dns-prefetch)[^>]*images\.unsplash\.com[^>]*>', "", text)
    return text, plan


for p in PAGES:
    plan = None
    for name in (f"{p}.dc.html", f"{p}.ar.dc.html"):
        path = os.path.join(SITE, name)
        s = open(path, encoding="utf-8").read()
        found = [m.group(0) for m in SLOT.finditer(s)]
        n, metas = len(found), [f.startswith("<meta") for f in found]
        s, plan = process(s, plan, p)
        left = s.count("unsplash")
        open(path, "w", encoding="utf-8", newline="").write(s)
        imgs = [b for m, (_, b) in zip(metas, plan) if not m]  # the paired share tags may repeat
        dup = {b: c for b, c in Counter(imgs).items() if c > 1}
        print(f"{name}: {n} slots, {left} unsplash left" + (f", repeats {dup}" if dup else ""))

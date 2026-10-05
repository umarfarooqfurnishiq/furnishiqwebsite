"""Draws the line map behind the About page headquarters panel.

Reads OpenStreetMap ways around the studio (fetched with Overpass, see README) and writes
uploads/about-studio-map-riyadh.svg: sand-coloured streets and building outlines on a
transparent ground, with the studio at the exact centre of the drawing.
Map data (c) OpenStreetMap contributors, ODbL.
"""
import json
import math
import sys

LAT0, LON0 = 24.6759459, 46.6749853      # First Plaza, Al Takhassousi (Google place cid 2079283542092448688)
W, H = 2400, 1400                        # drawing size in px; the studio sits at (W/2, H/2)
M_PER_PX = 1.2
KX = math.cos(math.radians(LAT0)) * 111320 / M_PER_PX
KY = 110540 / M_PER_PX

ROADS = {  # highway class -> (stroke width px, opacity)
    "motorway": (9, 0.55), "trunk": (9, 0.55), "motorway_link": (4, 0.4), "trunk_link": (4, 0.4),
    "primary": (6, 0.5), "primary_link": (3, 0.38), "secondary": (4.5, 0.42), "secondary_link": (2.5, 0.34),
    "tertiary": (3.5, 0.36), "tertiary_link": (2, 0.3), "residential": (2, 0.26), "unclassified": (2, 0.26),
    "living_street": (1.6, 0.22), "service": (1.2, 0.16),
}


def xy(p):
    return (W / 2 + (p["lon"] - LON0) * KX, H / 2 - (p["lat"] - LAT0) * KY)


def path(geom, close=False):
    pts = [xy(p) for p in geom]
    if all(x < -50 or x > W + 50 for x, _ in pts) or all(y < -50 or y > H + 50 for _, y in pts):
        return ""
    d = "M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
    return d + ("Z" if close else "")


def main(highway_json, building_json, out):
    roads = json.load(open(highway_json, encoding="utf-8"))["elements"]
    blds = json.load(open(building_json, encoding="utf-8"))["elements"]
    b = "".join(path(e["geometry"], True) for e in blds if "geometry" in e)
    groups = {}
    for e in roads:
        cls = e.get("tags", {}).get("highway")
        if cls in ROADS and "geometry" in e:
            groups.setdefault(ROADS[cls], []).append(path(e["geometry"]))
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
           '<!-- Map data (c) OpenStreetMap contributors, ODbL -->',
           f'<path d="{b}" fill="#D6C2A8" fill-opacity="0.06" stroke="#D6C2A8" stroke-opacity="0.16" stroke-width="1"/>']
    for (w, o), ds in sorted(groups.items()):
        svg.append(f'<path d="{"".join(ds)}" fill="none" stroke="#D6C2A8" stroke-opacity="{o}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    svg.append("</svg>")
    open(out, "w", encoding="utf-8").write("\n".join(svg))
    print(out, "written")


if __name__ == "__main__":
    main(*sys.argv[1:4])

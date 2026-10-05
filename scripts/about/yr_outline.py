"""Build a double-line outline of a connected '2007' by buffering its centre-line.
Prints: exterior ring path (spark loop, starting at the curve of the 2) and hole paths."""
import math, sys
from shapely.geometry import LineString
from shapely.ops import unary_union

def ellipse(cx, cy, rx, ry, start_deg, n=120):
    pts = []
    for i in range(n + 1):
        a = math.radians(start_deg + 360 * i / n)
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    return pts

def cubic(p0, p1, p2, p3, n=24):
    out = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        out.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0], u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
    return out

# centre-line, same geometry as before (viewBox 950x400)
pts = []
pts += cubic((22,136),(22,78),(66,50),(112,50))
pts += cubic((112,50),(164,50),(200,86),(200,134))[1:]
pts += cubic((200,134),(200,178),(172,208),(132,246))[1:]
pts += [(14,350),(340,350)]
z1 = ellipse(340, 200, 100, 150, 90)          # starts at bottom (340,350), full loop
pts += z1[1:]
pts += [(580,350)]
z2 = ellipse(580, 200, 100, 150, 90)
pts += z2[1:]
pts += [(770,350),(930,50),(726,50)]

W = float(sys.argv[1]) if len(sys.argv) > 1 else 11
poly = LineString(pts).buffer(W, cap_style=2, join_style=2, mitre_limit=3).simplify(0.4)
poly = unary_union(poly)

def ring_d(coords):
    c = list(coords)
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in c[:-1]) + "Z"

ext = list(poly.exterior.coords)[:-1]
# rotate exterior so it starts at the point closest to the top of the 2's curve (≈ 60,60)
k = min(range(len(ext)), key=lambda i: (ext[i][0]-70)**2 + (ext[i][1]-45)**2)
ext = ext[k:] + ext[:k]
ext.append(ext[0])
print("EXT=" + ring_d(ext))
print("HOLES=" + " ".join(ring_d(h.coords) for h in poly.interiors))

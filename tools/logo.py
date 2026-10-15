"""Logo SVG (absolute M/L/C/Z, even-odd fill) -> polygons with holes, in mm."""
import re, os
from shapely.geometry import Polygon
from shapely.ops import unary_union

SVG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hardware", "artwork", "heronidas_logo.svg")


def rings(path_d, steps=8):
    out, cur, pos = [], [], None
    for cmd, args in re.findall(r"([MLCZ])([^MLCZ]*)", path_d):
        v = [float(x) for x in re.findall(r"-?\d+\.?\d*", args)]
        if cmd == "M":
            if len(cur) > 2: out.append(cur)
            pos = (v[0], v[1]); cur = [pos]
            for i in range(2, len(v), 2): pos = (v[i], v[i + 1]); cur.append(pos)
        elif cmd == "L":
            for i in range(0, len(v), 2): pos = (v[i], v[i + 1]); cur.append(pos)
        elif cmd == "C":
            for i in range(0, len(v), 6):
                p0, p1, p2, p3 = pos, (v[i], v[i + 1]), (v[i + 2], v[i + 3]), (v[i + 4], v[i + 5])
                for k in range(1, steps + 1):
                    t = k / steps; u = 1 - t
                    cur.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                                u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
                pos = p3
        elif cmd == "Z":
            if len(cur) > 2: out.append(cur)
            cur = []
    if len(cur) > 2: out.append(cur)
    return out


def polygons(size_mm, cx, cy, mirror=False):
    """Even-odd filled logo, scaled to size_mm, centred on (cx, cy); mirror for the bottom side."""
    s = open(SVG).read()
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    k = size_mm / vb[2]
    geo = None
    for d in re.findall(r' d="([^"]+)"', s):
        for r in rings(d):
            p = Polygon(r).buffer(0)
            geo = p if geo is None else geo.symmetric_difference(p)
    geo = unary_union(geo)
    polys = geo.geoms if hasattr(geo, "geoms") else [geo]
    def tf(x, y):
        x = (x - vb[2] / 2) * k; y = (y - vb[3] / 2) * k
        return (cx - x if mirror else cx + x, cy + y)
    res = []
    for p in polys:
        res.append(([tf(*c) for c in p.exterior.coords[:-1]], [[tf(*c) for c in h.coords[:-1]] for h in p.interiors]))
    return res


if __name__ == "__main__":
    ps = polygons(26, 0, 0)
    print(len(ps), "polygons", sum(len(h) for _, h in ps), "holes")

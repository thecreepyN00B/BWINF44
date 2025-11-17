from itertools import combinations
from math import hypot
import sys

"""
hypot spart Satz des Pythagoras und combinations spart Kombinatorik
"""

def distance(p, q):
    return hypot(p[0] - q[0], p[1] - q[1])

def point_to_line_height(a, b, p):
    """Shoelace"""
    ax, ay = a; bx, by = b; px, py = p
    vx, vy = bx - ax, by - ay
    cross = abs(vx * (py - ay) - vy * (px - ax))
    base = hypot(vx, vy)
    return cross / base if base else float("inf")

def safe_triangle_distance(a, b, p):
    """
    check if triang obt or acu
    """
    ax, ay = a; bx, by = b; px, py = p
    vx, vy = bx - ax, by - ay
    wx, wy = px - ax, py - ay
    vv = vx*vx + vy*vy
    if vv == 0:
        return distance(p, a)
    t = (wx*vx + wy*vy) / vv
    if 0 <= t <= 1:
        return point_to_line_height(a, b, p)
    return min(distance(p, a), distance(p, b))

def _min_height_one_direction(base_points, other_points):
    """
    all combinations of points from sets lake, path
    """
    best = float("inf")
    best_triplet = None
    for a, b in combinations(base_points, 2):
        for p in other_points:
            d = safe_triangle_distance(a, b, p)
            if d < best:
                best = d
                best_triplet = (a, b, p)
    return best, best_triplet

def max_safe_leash_by_triangles(lake_points, path_points):
    best1, tri1 = _min_height_one_direction(lake_points, path_points)
    best2, tri2 = _min_height_one_direction(path_points, lake_points)

    if best1 <= best2:
        return {
            "min_distance": best1,
            "which_base": "lake",
            "triangle": tri1
        }
    else:
        return {
            "min_distance": best2,
            "which_base": "path",
            "triangle": tri2
        }

def _min_height_segments(segments, other_points):
    best = float("inf")
    best_triplet = None
    for a, b in segments:
        for p in other_points:
            d = safe_triangle_distance(a, b, p)
            if d < best:
                best = d
                best_triplet = (a, b, p)
                if best == 0.0:
                    return best, best_triplet
    return best, best_triplet

def max_safe_leash_segments(lake_points, path_points, lake_segments, path_segments):
    best1, tri1 = _min_height_segments(lake_segments, path_points)
    best2, tri2 = _min_height_segments(path_segments, lake_points)
    if best1 <= best2:
        return {
            "min_distance": best1,
            "which_base": "lake",
            "triangle": tri1
        }
    else:
        return {
            "min_distance": best2,
            "which_base": "path",
            "triangle": tri2
        }

def load_park_with_segments(datei):
    with open(datei, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    it = iter(lines)

    k = int(next(it))
    path_points = []
    path_segments = []
    for _ in range(k):
        x1, y1, x2, y2 = map(float, next(it).split())
        a = (x1, y1)
        b = (x2, y2)
        path_points.append(a)
        path_points.append(b)
        path_segments.append((a, b))

    s = int(next(it))
    lake_points = []
    lake_segments = []
    for _ in range(s):
        n = int(next(it))
        vertices = []
        for _ in range(n):
            x, y = map(float, next(it).split())
            p = (x, y)
            vertices.append(p)
            lake_points.append(p)
        if len(vertices) >= 2:
            for i in range(len(vertices) - 1):
                lake_segments.append((vertices[i], vertices[i+1]))
            if vertices[0] != vertices[-1]:
                lake_segments.append((vertices[-1], vertices[0]))

    return lake_points, path_points, lake_segments, path_segments

if __name__ == "__main__":
    datei = sys.argv[1]
    lakes, paths, lake_segments, path_segments = load_park_with_segments(datei)

    result = max_safe_leash_segments(lakes, paths, lake_segments, path_segments)
    print(f"Die Leine ist {result['min_distance']:.3f} LE lang")


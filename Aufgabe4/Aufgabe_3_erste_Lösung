from itertools import combinations
from math import hypot

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
    # obt-tr
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

if __name__ == "__main__":
    lakes = [(12, -2), (14, -2), (14, 2), (12, 2)]
    paths = [(0, 0), (10, 0), (10, 4), (5, 4)]

    result = max_safe_leash_by_triangles(lakes, paths)
    print(f"leash has to be about {result['min_distance']:.3f} LE long")

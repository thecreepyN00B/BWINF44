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
    ax, ay = a
    bx, by = b
    px, py = p

    vx, vy = bx - ax, by - ay
    cross = abs(vx * (py - ay) - vy * (px - ax))
    base = hypot(vx, vy)

    return cross / base if base else float("inf")


def safe_triangle_distance(a, b, p):
    """
    check if triang obt or acu
    """
    ax, ay = a
    bx, by = b
    px, py = p

    vx, vy = bx - ax, by - ay
    wx, wy = px - ax, py - ay

    vv = vx * vx + vy * vy
    if vv == 0:
        return distance(p, a)

    t = (wx * vx + wy * vy) / vv

    if 0 <= t <= 1:
        return point_to_line_height(a, b, p)

    return min(distance(p, a), distance(p, b))


def _min_height_one_direction(base_points, other_points):
    """
    all combinations of points from sets lake, path
    """
    best_distance = float("inf")
    best_triplet = None

    for a, b in combinations(base_points, 2):
        for p in other_points:
            d = safe_triangle_distance(a, b, p)
            if d < best_distance:
                best_distance = d
                best_triplet = (a, b, p)

    return best_distance, best_triplet


def max_safe_leash_by_triangles(lake_points, path_points):
    best_lake, tri_lake = _min_height_one_direction(lake_points, path_points)
    best_path, tri_path = _min_height_one_direction(path_points, lake_points)

    if best_lake <= best_path:
        return {
            "min_distance": best_lake,
            "which_base": "lake",
            "triangle": tri_lake
        }

    return {
        "min_distance": best_path,
        "which_base": "path",
        "triangle": tri_path
    }


def load_park(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    it = iter(lines)

    k = int(next(it))
    path_points = []

    for _ in range(k):
        x1, y1, x2, y2 = map(float, next(it).split())
        path_points.append((x1, y1))
        path_points.append((x2, y2))

    s = int(next(it))
    lake_points = []

    for _ in range(s):
        n = int(next(it))
        for _ in range(n):
            x, y = map(float, next(it).split())
            lake_points.append((x, y))

    return lake_points, path_points


if __name__ == "__main__":
    filename = sys.argv[1]
    lakes, paths = load_park(filename)

    result = max_safe_leash_by_triangles(lakes, paths)
    print(f"Die Leine muss so {result['min_distance']:.3f} LE lang sein")


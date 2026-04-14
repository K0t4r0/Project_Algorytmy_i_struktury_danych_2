import math
import matplotlib.pyplot as plt

def show(points, hull_graham, hull_jarvis):
    x, y = zip(*points)
    plt.scatter(x, y, color='red', label='All points')

    if hull_graham:
        hx, hy = zip(*(hull_graham + [hull_graham[0]]))
        plt.plot(hx, hy, 'g--', label='Graham', alpha=0.6)

    if hull_jarvis:
        jx, jy = zip(*(hull_jarvis + [hull_jarvis[0]]))
        plt.plot(jx, jy, 'b:', label='Jarvis', alpha=0.6)

    plt.legend()
    plt.grid(True)
    plt.title("Comparison")
    plt.show()

def get_orientation(p, q, r):
    """
    0 -> Straight
    1 -> Right
    2 -> Left
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0
    return 1 if val > 0 else 2

def dist_sq(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def graham_scan(points):
    n = len(points)
    if n < 3: return points

    start_point = min(points, key=lambda p: (p[1], p[0]))
    
    points_without_start = [p for p in points if p != start_point]

    sorted_points = sorted(
        points_without_start, 
        key=lambda p: (math.atan2(p[1] - start_point[1], p[0] - start_point[0]), dist_sq(start_point, p))
    )

    hull = [start_point]
    for p in sorted_points:
        while len(hull) >= 2 and get_orientation(hull[-2], hull[-1], p) != 2:
            hull.pop()
        hull.append(p)
    
    return hull

def jarvis(points):
    n = len(points)
    if n < 3: return points
    
    start_point = min(points, key=lambda p: (p[0], p[1])) 

    hull = []
    p = start_point
    while True:
        hull.append(p)

        q = None

        for r in points:
            if r == p:
                continue
            if q is None:
                q = r
                continue

            orientation = get_orientation(p, q, r)

            if orientation == 2 or (orientation == 0 and dist_sq(p, r) > dist_sq(p, q)):
                q = r
        p = q

        if p == start_point:
            break

    return hull

n = int(input())

if n < 3:
    print("Need at least 3 points")
else:
    points_array = []
    for _ in range(n):
        coords = tuple(map(int, input().split()))
        points_array.append(coords)

    hull_g = graham_scan(points_array)
    hull_j = jarvis(points_array)

    print("\n--- Graham ---")
    print(hull_g)

    print("\n--- Jarvis ---")
    print(hull_j)
    
    show(points_array, hull_g, hull_j)
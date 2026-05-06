import math


def run_hull_example():
    return "Hull algorithm running..."

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
    current_p = start_point
    
    while True:
        hull.append(current_p)
        q = None
        for r in points:
            if r == current_p: continue

            yield (list(hull), r)
            
            if q is None:
                q = r
                continue
            orientation = get_orientation(current_p, q, r)
            if orientation == 2 or (orientation == 0 and dist_sq(current_p, r) > dist_sq(current_p, q)):
                q = r
        
        current_p = q
        if current_p == start_point: break

    final = hull + [hull[0]]
    yield (final, None)

def jarvis_generator(points):
    n = len(points)
    if n < 3: 
        yield (points, None)
        return
    
    start_point = min(points, key=lambda p: (p[0], p[1])) 
    hull = []
    current_p = start_point
    
    while True:
        hull.append(current_p)
        q = None
        for r in points:
            if r == current_p: continue
            
            yield (list(hull), r)
            
            if q is None:
                q = r
                continue
            orientation = get_orientation(current_p, q, r)
            if orientation == 2 or (orientation == 0 and dist_sq(current_p, r) > dist_sq(current_p, q)):
                q = r
        
        current_p = q
        if current_p == start_point: break

    yield (hull + [hull[0]], None)

def graham_generator(points):
    if len(points) < 3:
        yield (points, None)
        return

    start_point = min(points, key=lambda p: (p[1], p[0]))
    points_without_start = [p for p in points if p != start_point]
    sorted_points = sorted(
        points_without_start, 
        key=lambda p: (math.atan2(p[1] - start_point[1], p[0] - start_point[0]), dist_sq(start_point, p))
    )

    hull = [start_point]
    for p in sorted_points:
        yield (list(hull), p)
        
        while len(hull) >= 2 and get_orientation(hull[-2], hull[-1], p) != 2:
            hull.pop()
            yield (list(hull), p)
        
        hull.append(p)
        yield (list(hull), None)
    
    yield (hull + [hull[0]], None)

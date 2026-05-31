from algorithms.royal_border_patrol import RoyalBorderPatrol
from tools.data_manager import DataManager
from data_classes.classes import *
from bisect import bisect_right
import math


# Returns mines located on the convex hull border
def get_border_mines(path):
    patrol = RoyalBorderPatrol()
    d = DataManager()
    d.load_from_json(path)

    points = d.mines
    guards = d.guards

    patrol.load_data([mine.pos for mine in points])
    hull_points = patrol.get_border_route("graham")

    pos_to_mine = {mine.pos: mine for mine in points}
    hull_mines = [pos_to_mine[p] for p in hull_points]

    return hull_mines, guards

# Calculates distance between two positions
def get_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

# Creates edge list for convex hull border

def place_guards(hull_mines, guards):
    dist = 0.0
    edge_starts = []
    edge_ranges = {}
    edge_map = {}

    for i in range(len(hull_mines)):
        a = hull_mines[i]
        b = hull_mines[(i + 1) % len(hull_mines)]

        edge_map[(a.id, b.id)] = i
        edge_starts.append(dist)
        dist += get_distance(a.pos, b.pos)

    step = dist / len(guards)

    for i, guard in enumerate(guards):
        pos = i * step
        edge_idx = bisect_right(edge_starts, pos) - 1

        guard.position_meters = pos
        guard.edge_index = edge_idx

        if edge_idx not in edge_ranges:
            edge_ranges[edge_idx] = [i, i]
        else:
            edge_ranges[edge_idx][1] = i

    return step, edge_ranges, edge_map

def get_perimeter(hull_mines):    
    perimeter = 0.0

    for i in range(len(hull_mines)):
        a = hull_mines[i]
        b = hull_mines[(i + 1) % len(hull_mines)]

        perimeter += get_distance(a.pos, b.pos)

    return perimeter

class SparseTable:
    def __init__(self, guards: list):
        self.guards = guards
        n = len(guards)
        
        if n == 0:
            self.st = []
            return
        
        levels = math.floor(math.log2(n)) + 1
        
        self.st = [[0] * n for _ in range(levels)]
        
        for i in range(n):
            self.st[0][i] = i
        
        for k in range(1, levels):
            block = 2 ** (k - 1)
            for i in range(n - 2 ** k + 1):
                left  = self.st[k-1][i]
                right = self.st[k-1][i + block]
                self.st[k][i] = left if guards[left].loudness >= guards[right].loudness else right

    def query(self, l, r):
        if l > r:
            return None
        k = math.floor(math.log2(r - l + 1))
        left  = self.st[k][l]
        right = self.st[k][r - 2 ** k + 1]
        idx = left if self.guards[left].loudness >= self.guards[right].loudness else right
        return self.guards[idx]
    
class SegmentTree:
    def __init__(self, guards: list):
        self.guards = guards
        self.n = len(guards)
        self.tree = [0] * (4 * self.n)
        if self.n > 0:
            self._build(0, 0, self.n - 1)

    def _louder(self, a: int, b: int):
        return a if self.guards[a].loudness >= self.guards[b].loudness else b

    def _build(self, node: int, start: int, end: int):
        if start == end:
            self.tree[node] = start
            return
        mid = (start + end) // 2
        self._build(2 * node + 1, start, mid)
        self._build(2 * node + 2, mid + 1, end)
        self.tree[node] = self._louder(self.tree[2 * node + 1],
                                        self.tree[2 * node + 2])

    def query(self, l: int, r: int):
        if l > r:
            return None
        idx = self._query(0, 0, self.n - 1, l, r)
        return self.guards[idx]

    def _query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        if r < start or end < l:
            return -1
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        left_idx  = self._query(2 * node + 1, start, mid, l, r)
        right_idx = self._query(2 * node + 2, mid + 1, end, l, r)
        if left_idx  == -1: return right_idx
        if right_idx == -1: return left_idx
        return self._louder(left_idx, right_idx)
    
def find_loudest_by_edge(table, edge_ranges, edge_map, edge_from, edge_to):
    edge_idx = edge_map.get((edge_from.id, edge_to.id))

    if edge_idx is None:
        return None

    if edge_idx not in edge_ranges:
        return None

    l, r = edge_ranges[edge_idx]

    return table.query(l, r)

def find_loudest_by_meters(guards, table, step, from_m, to_m):
    n = len(guards)
    if n == 0:
        return None, "No guards available"

    perimeter = n * step

    from_m = from_m % perimeter
    to_m = to_m % perimeter

    if from_m > to_m:
        l_a = math.ceil(from_m / step)
        r_a = n - 1
        winner_a = table.query(l_a, r_a) if l_a <= r_a else None

        l_b = 0
        r_b = math.floor(to_m / step)
        winner_b = table.query(l_b, r_b) if l_b <= r_b else None

        if winner_a and winner_b:
            return (winner_a if winner_a.loudness >= winner_b.loudness else winner_b), None
        elif winner_a:
            return winner_a, None
        elif winner_b:
            return winner_b, None
        else:
            return None, f"No guards between {from_m:.1f}m and {to_m:.1f}m"
    else:
        l = math.ceil(from_m / step)
        r = math.floor(to_m / step)

        l = max(0, l)
        r = min(n - 1, r)

        if l > r:
            return None, f"No guards between {from_m:.1f}m and {to_m:.1f}m"

        return table.query(l, r), None
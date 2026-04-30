import math
from data_classes.classes import *
from tools.data_manager import DataManager
from algorithms.shortest_path import bellman_ford


class MCMF:
    def __init__(self, dwarves: List[Dwarf], mines: List[Mine]):
        self.dwarves = dwarves
        self.mines = mines
        
        self.S = 0
        self.T = len(dwarves) + len(mines) + 1
        self.nodes_count = self.T + 1
        self.graph = [] # [u, v, capacity, cost, reverse_edge_index]

    def add_edge(self, u, v, cap, cost):
        self.graph.append([u, v, cap, cost, len(self.graph) + 1])
        self.graph.append([v, u, 0, -cost, len(self.graph) - 1])

    def get_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]):
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def build_network(self):
        for i, dwarf in enumerate(self.dwarves, 1):
            self.add_edge(self.S, i, 1, 0)
            
            for j, mine in enumerate(self.mines, 1):
                if mine.mine_type in dwarf.skills:
                    dist = self.get_distance(dwarf.home_pos, mine.pos)
                    mine_node = len(self.dwarves) + j
                    self.add_edge(i, mine_node, 1, dist)

        for j, mine in enumerate(self.mines, 1):
            mine_node = len(self.dwarves) + j
            self.add_edge(mine_node, self.T, mine.capacity, 0)

    def solve(self): 
        while True:
            result = bellman_ford(self.graph, self.nodes_count, self.S, self.T)
            
            if result is None:
                raise RuntimeError("Bellman-Ford: the graph contains a negative cycle")
                
            dist, parent, edge_from = result
            if dist[self.T] == float('inf'):
                break
            
            curr = self.T
            while curr != self.S:
                idx = edge_from[curr]
                rev_idx = self.graph[idx][4]
                
                self.graph[idx][2] -= 1
                self.graph[rev_idx][2] += 1
                curr = parent[curr]
        
        assignments = []
        num_dwarves = len(self.dwarves)
        
        for u, v, cap, cost, rev in self.graph:
            if 1 <= u <= num_dwarves and num_dwarves < v < self.T:
                if cap == 0:
                    dwarf_idx = u - 1
                    mine_idx = v - num_dwarves - 1
                    assignments.append({
                        "dwarf": self.dwarves[dwarf_idx],
                        "mine": self.mines[mine_idx],
                        "distance": cost
                    })
                
        return assignments

# Example
if __name__ == "__main__":
    dm = DataManager()
    if not dm.load_from_json("json/test1.json"):
        raise IOError("Problem with json/test1.json")

    solver = MCMF(dm.dwarves, dm.mines)
    solver.build_network()

    results = solver.solve()

    for res in results:
        for key in res:
            print(f"{key}: {res[key]}")
        print()

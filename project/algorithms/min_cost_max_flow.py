import math
from data_classes.classes import *
from tools.data_manager import DataManager
from algorithms.shortest_path import bellman_ford
from tools.data_manager import data_store


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
        #Calculating position for s, t (gui)
        all_x = [d.home_pos[0] for d in self.dwarves] + [m.pos[0] for m in self.mines]
        all_y = [d.home_pos[1] for d in self.dwarves] + [m.pos[1] for m in self.mines]

        data_store.s_pos = (min(all_x) - 10, sum(all_y) / len(all_y))
        data_store.t_pos = (max(all_x) + 10, sum(all_y) / len(all_y))

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

    #Saving paths (gui)
    def update_store_paths(self):
        paths = []
        num_dwarves = len(self.dwarves)
        num_mines = len(self.mines)

        for u, v, cap, cost, rev_idx in self.graph:
            flow_in_edge = self.graph[rev_idx][2]

            if flow_in_edge > 0 and cost >= 0:
                start_pos = None
                end_pos = None

                # S -> Drawrf
                if u == self.S and 1 <= v <= num_dwarves:
                    start_pos = data_store.s_pos
                    end_pos = self.dwarves[v - 1].home_pos

                # Drawrf -> Mine
                elif 1 <= u <= num_dwarves and num_dwarves < v <= (num_dwarves + num_mines):
                    start_pos = self.dwarves[u - 1].home_pos
                    mine_idx = v - num_dwarves - 1
                    if 0 <= mine_idx < num_mines:
                        end_pos = self.mines[mine_idx].pos

                # Mine -> T
                elif num_dwarves < u <= (num_dwarves + num_mines) and v == self.T:
                    mine_idx = u - num_dwarves - 1
                    if 0 <= mine_idx < num_mines:
                        start_pos = self.mines[mine_idx].pos
                        end_pos = data_store.t_pos

                if start_pos and end_pos:
                    paths.append((start_pos, end_pos))

        data_store.flow_paths = paths

    def solve_generator(self):
        while True:
            result = bellman_ford(self.graph, self.nodes_count, self.S, self.T)
            if result is None or result[0][self.T] == float('inf'):
                break
                
            dist, parent, edge_from = result
            curr = self.T
            while curr != self.S:
                idx = edge_from[curr]
                rev_idx = self.graph[idx][4]
                self.graph[idx][2] -= 1
                self.graph[rev_idx][2] += 1
                curr = parent[curr]
                
            self.update_store_paths()
            current_step_paths = list(data_store.flow_paths)
            yield current_step_paths

from algorithms.hull import *

class RoyalBorderPatrol:
    def __init__(self, points=None):
        self.points = points if points else []

    def load_data(self, points):
        self.points = points

    def add_mine(self, x, y):
        self.points.append((x, y))

    def get_border_route(self, algorithm="graham"):
        alg = algorithm.lower()
        if alg == "graham":
            return graham_scan(self.points)
        elif alg == "jarvis":
            return jarvis(self.points)
        else:
            raise ValueError("Unknown algorithm. Select “graham” or “jarvis”.")
        
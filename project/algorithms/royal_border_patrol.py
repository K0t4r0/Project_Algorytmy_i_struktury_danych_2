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
        

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from tools.data_manager import *

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

    r = RoyalBorderPatrol()
    d = DataManager()
    d.load_from_json("json/test1.json")

    points = []
    for m in d.mines:
        points.append(m.pos)

    r.load_data(points)
    show(points, r.get_border_route(), r.get_border_route("jarvis"))

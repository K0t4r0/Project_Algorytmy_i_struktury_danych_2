import json
from data_classes.classes import Dwarf, Mine

class DataManager:
    def __init__(self):
        self.dwarves = []
        self.mines = []
        self.guards = []

    def load_from_json(self, file_path : str) -> bool:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.dwarves = [Dwarf(d["id"], d["name"], d["skills"], d["value"], tuple(d["home_pos"])) for d in data["dwarves"]]
            self.mines = [Mine(m["id"], m["type"], m["capacity"], tuple(m["pos"])) for m in data["mines"]]
            self.guards = data.get('guards', [])
            return True
        except Exception as e:
            print("Loading error:", e)
            return False
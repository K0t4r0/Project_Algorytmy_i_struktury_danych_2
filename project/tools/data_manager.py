import json
from data_classes.classes import Dwarf, Mine, BorderGuard
import re
from pathlib import Path

# Get all json files in project
def get_json_files():
    examples_path = Path("json/")

    return sorted(
        examples_path.glob("*.json"),
        key=lambda p: int(re.search(r"\d+", p.stem).group())
    )

class DataManager:
    def __init__(self):
        self.dwarves = []
        self.mines = []
        self.guards = []
        
        self.hull_points = []
        self.flow_paths = []
        self.s_pos = []
        self.t_pos = []
        self.mode = None
        self.show_st = True

    def load_from_json(self, file_path : str) -> bool:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.dwarves = [Dwarf(d["id"], d["name"], d["skills"], tuple(d["home_pos"])) for d in data["dwarves"]]
            self.mines = [Mine(m["id"], m["mine_type"], m["capacity"], tuple(m["pos"])) for m in data["mines"]]
            self.guards = [BorderGuard(g["id"], g["name"], g["loudness"]) for g in data.get("guards", [])]

            self.mode = data.get("mode", "MCMF")
            self.clear
            
            return True
        except Exception as e:
            print("Loading error:", e)
            return False

    def clear(self):
        self.dwarves = []
        self.mines = []
        self.flow_paths = []
        self.s_pos = None
        self.t_pos = None
        self.hull_points = []
    
    def get_mine_type(self, m_id):
        for m in self.mines:
            if m.id == m_id:
                return m.mine_type
        return "default"
    
data_store = DataManager()
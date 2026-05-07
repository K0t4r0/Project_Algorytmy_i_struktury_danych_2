import math
import json
import random

class DwarfDataGenerator:
    def __init__(self, names_file="tools/names.json", custom_config=None):
        self.config = {
            "min_dwarves": 10,
            "max_dwarves": 50,
            "min_mines": 5,
            "max_mines": 20,
            "min_guards": 10,
            "max_guards": 50,
            "grid_size": 100, # Max X, Y
            "min_distance": 5,
            "mine_types": ["gold", "iron", "coal", "copper"],
            "min_skills": 1,
            "max_skills": 3,
            "min_value": 50,
            "max_value": 150,
            "min_capacity": 1,
            "max_capacity": 10,
            "min_loudness": 30,
            "max_loudness": 120
        }
        
        if custom_config:
            self.config.update(custom_config)
            
        self.names = self._load_names(names_file)

    def _load_names(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "dwarf_names" in data:
                    return data["dwarf_names"]
                elif isinstance(data, list):
                    return data
                else:
                    raise ValueError("ERROR: Unknown data type in json file")
        except FileNotFoundError:
            raise FileNotFoundError(f"ERROR: File {file_path} not found")

    def _random_pos(self):
        return [
            random.randint(0, self.config["grid_size"]),
            random.randint(0, self.config["grid_size"])
        ]

    def _get_valid_pos(self, occupied_positions):
        min_dist = self.config.get("min_distance", 0)
        max_attempts = 100

        for _ in range(max_attempts):
            pos = self._random_pos()
            
            too_close = False
            for occ_pos in occupied_positions:
                dist = math.hypot(pos[0] - occ_pos[0], pos[1] - occ_pos[1])
                if dist < min_dist:
                    too_close = True
                    break
            
            if not too_close:
                return pos
                
        print(f"Warning: The map is too dense! Unable to find a position with a distance of {min_dist}.")
        return pos

    def generate(self):
        num_dwarves = random.randint(self.config["min_dwarves"], self.config["max_dwarves"])
        num_mines = random.randint(self.config["min_mines"], self.config["max_mines"])
        num_guards = random.randint(self.config["min_guards"], self.config["max_guards"])

        available_names = list(self.names)
        random.shuffle(available_names)

        occupied_positions = []
        dwarves = []

        for i in range(1, num_dwarves + 1):
            name = available_names.pop() if available_names else f"Dwarf_{i}"
            
            num_skills = random.randint(self.config["min_skills"], self.config["max_skills"])
            skills = random.sample(self.config["mine_types"], k=min(num_skills, len(self.config["mine_types"])))
            
            pos = self._get_valid_pos(occupied_positions)
            occupied_positions.append(pos)
            
            dwarves.append({
                "id": i,
                "name": name,
                "skills": skills,
                "value": random.randint(self.config["min_value"], self.config["max_value"]),
                "home_pos": pos
            })

        mines = []
        for i in range(1, num_mines + 1):
            pos = self._get_valid_pos(occupied_positions)
            occupied_positions.append(pos)
            
            mines.append({
                "id": f"M-{i:02d}",
                "mine_type": random.choice(self.config["mine_types"]),
                "capacity": random.randint(self.config["min_capacity"], self.config["max_capacity"]),
                "pos": pos
            })

        guards = [random.randint(self.config["min_loudness"], self.config["max_loudness"]) for _ in range(num_guards)]

        return {
            "dwarves": dwarves,
            "mines": mines,
            "guards": guards
        }

    def generate_and_save(self, output_file="json/generator_test.json"):
        data = self.generate()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"The data has been successfully generated and saved in '{output_file}'")
        return data


# ==========================================
# Example
# ==========================================
if __name__ == "__main__":
    generator = DwarfDataGenerator() 
    # if you want to use custom config
    # create dict 
    # conf = {
    #         "min_dwarves": 100,
    #         "max_dwarves": 500,
    #         "min_mines": 50,
    #         "max_mines": 200,
    #         "min_guards": 100,
    #         "max_guards": 500,
    #         "grid_size": 1000,
    # }
    # and use custom_config=...
    # ... = DwarfDataGenerator(custom_config=conf) 

    generator.generate_and_save() # You can use output_file="..."

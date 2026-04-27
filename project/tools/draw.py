import json
from ui.colors import *
from pathlib import Path
from tools.data_manager import data_store

examples_path = Path("json/")
json_files = list(examples_path.glob("*.json"))

def select_example(json_path, canvas):
    data_store.load_from_json(json_path)
    draw_world(canvas)

def draw_world(canvas):
    canvas.delete("all")
    s = get_scale(canvas, data_store)

    mines = data_store.get_mine_positions()
    for id, pos in mines.items():
        mx, my = pos[0] * s, pos[1] * s
    
        mine_type = data_store.get_mine_type(id)
        m_color = MINE_COLORS.get(mine_type)
        
        canvas.create_oval(
            mx - 10, my - 10,
            mx + 10, my + 10, 
            fill=m_color, 
            outline="black", 
            width=2
        )

    homes = data_store.get_home_positions()
    for id, pos in homes.items():
        dx, dy = pos[0] * s, pos[1] * s
        
        canvas.create_oval(
            dx - 10, dy - 10, 
            dx + 10, dy + 10, 
            fill=DWARF_HOME, 
            outline="#ffffff"
        )

def get_scale(canvas, data_store):
    all_x = [d.home_pos[0] for d in data_store.dwarves] + [m.pos[0] for m in data_store.mines]
    all_y = [d.home_pos[1] for d in data_store.dwarves] + [m.pos[1] for m in data_store.mines]
    
    if not all_x or not all_y: return 1

    max_x, max_y = max(all_x), max(all_y)
    
    canvas.update()
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    
    scale_x = (w * 0.9) / max_x if max_x > 0 else 1
    scale_y = (h * 0.9) / max_y if max_y > 0 else 1

    return min(scale_x, scale_y)

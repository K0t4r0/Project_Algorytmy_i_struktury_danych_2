from ui.colors import *
from pathlib import Path
from tools.data_manager import data_store

examples_path = Path("json/")
json_files = list(examples_path.glob("*.json"))

def select_example(json_path, canvas):
    data_store.clear
    data_store.load_from_json(json_path)
    draw_world(canvas)

def draw_world(canvas):
    ax = canvas.figure.axes[0]

    ax.clear()
    ax.set_facecolor(BG_THIRDY)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='white')
    ax.xaxis.grid(True, linestyle='--', alpha=0.3, color='white')

    ax.tick_params(axis='both', colors='white')
    for side in ['top', 'right']:
        ax.spines[side].set_visible(False)
    for side in ['left', 'bottom']:
        ax.spines[side].set_color('white')

    added_mine_types = set()
    for m in data_store.mines:

        mine_type = data_store.get_mine_type(m.id)
        m_color = MINE_COLORS.get(mine_type)

        label = mine_type if mine_type not in added_mine_types else "_"
        ax.plot(m.pos[0], m.pos[1], 'o', color=m_color, ms=14, mec='white', mew=1, label=label)
        added_mine_types.add(mine_type)
    
    for d in data_store.dwarves:
        ax.plot(d.home_pos[0], d.home_pos[1], 'o', color=DWARF_HOME, ms=14, mec='white', mew=1)
    ax.plot([], [], 'o', color=DWARF_HOME, ms=14, mec='white', label="Dwarf")
    
    ax.legend(loc='upper left', 
              bbox_to_anchor=(1, 1), 
              facecolor=BG_THIRDY, 
              labelcolor='white', 
              frameon=False, 
              fontsize=10,
              labelspacing=1.2)

    canvas.draw()
    canvas.figure.tight_layout()
        
def draw_flow(canvas):
    ax = canvas.figure.axes[0]
    draw_world(canvas)

    if data_store.s_pos:
        ax.plot(*data_store.s_pos, '^', color='green', ms=15, label="Source (S)")
    if data_store.t_pos:
        ax.plot(*data_store.t_pos, 'v', color='red', ms=15, label="Sink (T)")

    ax.legend(loc='upper left', 
              bbox_to_anchor=(1, 1), 
              frameon=False, 
              labelcolor='white',
              labelspacing=1.2)
        
    for start, end in data_store.flow_paths:
        ax.annotate("", 
                    xy=end, 
                    xytext=start, 
                    arrowprops=dict(
                        arrowstyle="->", 
                        color='white', 
                        lw=1.5, 
                        alpha=0.6,
                        shrinkA=10,
                        shrinkB=10  
                    ),
                    zorder=2)

    canvas.figure.tight_layout()
    canvas.draw()


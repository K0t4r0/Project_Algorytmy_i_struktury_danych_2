import random
import hashlib
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ui.colors import *
from tools.draw import get_json_files
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from tools.data_manager import data_store
from algorithms.segment import get_border_mines, place_guards, SparseTable, find_loudest_by_edge, find_loudest_by_meters, get_perimeter
import os
from algorithms.hull import jarvis

import threading
import tempfile
import datetime
import json
from tools.compression_manager import CompManager

class SegmentPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)

        self.hull_mines = []
        self.guards = []
        self.step_m = 1.0
        self.table = None
        self.current_path = None
        self.current_log_name = None

        # Left frame (examples)
        left_frame = ctk.CTkFrame(self, width=200, fg_color=BG_SECONDARY, corner_radius=0)
        left_frame.pack(fill="y", side="left")

        ctk.CTkLabel(left_frame, text="Border Guards", font=("Arial", 30, "bold")).pack(pady=20)

        self.scroll = ctk.CTkScrollableFrame(left_frame, fg_color=BG_SECONDARY)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(5, 5))

        # Examples
        self.refresh_examples()

        ctk.CTkButton(left_frame, text="Back", font=("Arial", 20),
                      command=lambda: controller.show_frame("MainMenu")
                      ).pack(pady=10)

        # Main frame (graph)
        main_frame = ctk.CTkFrame(self, fg_color=BG_SECONDARY)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        mid_frame = ctk.CTkFrame(main_frame, fg_color=BG_THIRDY)
        mid_frame.pack(padx=15, pady=15, side="left", fill="both", expand=True)

        graph_frame = ctk.CTkFrame(mid_frame)
        graph_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        self.fig = Figure(figsize=(6, 4), dpi=100, facecolor=BG_THIRDY)
        self.ax  = self.fig.add_subplot(111)
        self.fig.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08)

        self.canvas = FigureCanvasTkAgg(self.fig, graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Attack button below the graph
        controls_frame = ctk.CTkFrame(mid_frame, height=60, fg_color="transparent")
        controls_frame.propagate(False)
        controls_frame.pack(fill="x", padx=20, pady=(5, 15), side="bottom")

        self.attack_btn = ctk.CTkButton(
            controls_frame,
            text="ATTACK!",
            font=("Arial", 18, "bold"),
            height=30,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            #command=self.simulate_edge_attack,
            command=self.simulate_attack_by_meters,
            state="disabled"
        )
        self.attack_btn.pack(fill="x", padx=20, pady=(8,0))

        # Right frame (info)
        right_frame = ctk.CTkFrame(main_frame, fg_color=BG_SECONDARY, width=230)
        right_frame.pack(padx=5, fill="y", side="right")
        right_frame.pack_propagate(False)

        ctk.CTkLabel(right_frame, text="Info", font=("Arial", 20, "bold")).pack(pady=(14, 4))

        self.info_box = ctk.CTkTextbox(
            right_frame,
            font=("Arial", 13),
            fg_color=BG_SECONDARY,
            text_color="white",
            wrap="word",
            state="disabled"
        )
        self.info_box.pack(fill="both", expand=True, padx=10, pady=(4, 14))

        self._set_info("Load an example to begin.")

        self._style_axes()
        self.canvas.draw()

    def _style_axes(self):
        ax = self.ax
        ax.set_facecolor(BG_THIRDY)
        ax.tick_params(axis='both', colors='white', labelsize=8)
        ax.grid(True, linestyle='--', alpha=0.3, color='white')
        for spine in ax.spines.values():
            spine.set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    def _set_info(self, text: str):
        self.info_box.configure(state="normal")
        self.info_box.delete("1.0", "end")
        self.info_box.insert("end", text)
        self.info_box.configure(state="disabled")

    def load_example(self, path):
        self.current_path = path
        data_store.load_from_json(path)

        self.hull_mines, self.guards = get_border_mines(path)
        self.step_m = place_guards(self.hull_mines, self.guards)
        self.table  = SparseTable(self.guards)

        self.attack_btn.configure(state="normal")
        self._set_info(
            f"Example loaded.\n\n"
            f"Hull mines: {len(self.hull_mines)}\n"
            f"Guards: {len(self.guards)}\n"
            f"Step: {self.step_m:.2f} m\n\n"
            f"Press ATTACK to simulate an apple-smuggling raid."
        )
        self._draw_border()

        initial_data = {
            "inputs": {
                "dwarves": getattr(data_store, "dwarves", []),
                "mines": getattr(data_store, "mines", []),
                "guards": getattr(data_store, "guards", [])
            },
            "outputs": {
                "hull_mines": self.hull_mines,
                "placed_guards": self.guards,
                "step_meters": self.step_m
            }
        }
        hash_str = json.dumps(initial_data, ensure_ascii=False, sort_keys=True, default=lambda o: o.__dict__)
        data_hash = hashlib.sha256(hash_str.encode('utf-8')).hexdigest()[:16]
        self.current_log_name = f"segment_result_{data_hash}.json"

        if self.guards and self.hull_mines:
            threading.Thread(target=self.background_save_task, args=[None], daemon=True).start()

    def _draw_legend(self, ax, show_attack=False, show_winner=False):
        entries = []
        # border
        entries.append(Line2D([0], [0], color="#00FF7F", lw=1.8,
                            alpha=0.85, label="Border"))

        # attacked segment
        if show_attack:
            entries.append(Line2D([0], [0], color="#FF3030", lw=3.0,
                                label="Attacked segment"))

        # guard
        entries.append(Line2D([0], [0], marker='o', color='w',
                            markerfacecolor="#88CCFF", markeredgecolor='white',
                            markersize=7, label="Border guard"))

        # winner
        if show_winner:
            entries.append(Line2D([0], [0], marker='*', color='w',
                                markerfacecolor="#FFD700", markeredgecolor='white',
                                markersize=12, label="Commander"))

        ax.legend(
            handles=entries,
            loc="upper right",
            fontsize=7,
            framealpha=0.25,
            facecolor=BG_THIRDY,
            edgecolor="white",
            labelcolor="white"
        )

    # Base drawing method
    def _draw_border(self):
        ax = self.ax
        ax.clear()
        self._style_axes()
        if not self.hull_mines:
            self.canvas.draw()
            return

        self._draw_mines(ax)

        n = len(self.hull_mines)
        for i in range(n):
            a = self.hull_mines[i]
            b = self.hull_mines[(i + 1) % n]
            ax.plot([a.pos[0], b.pos[0]], [a.pos[1], b.pos[1]],
                    '-', color="#00FF7F", lw=1.8, alpha=0.55, zorder=2)

        self._draw_hull_fill(ax)
        self._draw_guards(ax, None)
        self._draw_legend(ax, show_attack=False, show_winner=False)
        self.canvas.draw()

    # Drawing mines
    def _draw_mines(self, ax):
        points = [m.pos for m in data_store.mines]
        mines =  jarvis(points)

        for m in mines:
            ax.plot(m[0], m[1], 'o',
                    color="gray", ms=14, mec='white', mew=1, zorder=3)

    # Drawing hull filling
    def _draw_hull_fill(self, ax):
        xs = [m.pos[0] for m in self.hull_mines]
        ys = [m.pos[1] for m in self.hull_mines]
        ax.fill(xs, ys, color="#00FF7F", alpha=0.06, zorder=1)

    # Drawing dwarfs (guards)
    def _draw_guards(self, ax, winner=None):
        guard_xs, guard_ys = [], []
        for g in self.guards:
            gx, gy = self._guard_coords(g)
            guard_xs.append(gx)
            guard_ys.append(gy)
        ax.scatter(guard_xs, guard_ys,
                marker='o', s=40, color="#88CCFF",
                edgecolors='white', linewidths=0.4, zorder=4)
        if winner is not None:
            wx, wy = self._guard_coords(winner)
            ax.scatter([wx], [wy], marker='*', s=320,
                    color="#FFD700", edgecolors='white', linewidths=0.8, zorder=6)
            ax.annotate(winner.name, xy=(wx, wy),
                        xytext=(6, 6), textcoords='offset points',
                        color="#FFD700", fontsize=9, fontweight='bold', zorder=7)

    # Convertion guard position (meters) to (x, y)
    def _guard_coords(self, guard):
        n = len(self.hull_mines)
        cumulative = 0.0
        for i in range(n):
            a = self.hull_mines[i]
            b = self.hull_mines[(i + 1) % n]
            dx = b.pos[0] - a.pos[0]
            dy = b.pos[1] - a.pos[1]
            edge_len = (dx**2 + dy**2) ** 0.5

            if i == guard.edge_index:
                offset = guard.position_meters - cumulative
                t = offset / edge_len if edge_len > 0 else 0
                return a.pos[0] + t * dx, a.pos[1] + t * dy

            cumulative += edge_len

        return self.hull_mines[0].pos

    # Simulation of attack on the edge
    def _draw_border_edge_attack(self, highlight_edge_idx=None, winner=None):
        ax = self.ax
        ax.clear()
        self._style_axes()
        if not self.hull_mines:
            self.canvas.draw()
            return

        self._draw_mines(ax)

        n = len(self.hull_mines)
        for i in range(n):
            a = self.hull_mines[i]
            b = self.hull_mines[(i + 1) % n]
            is_attacked = (i == highlight_edge_idx)
            color = "#FF3030" if is_attacked else "#00FF7F"
            lw    = 3.0       if is_attacked else 1.8
            alpha = 1.0       if is_attacked else 0.55
            ax.plot([a.pos[0], b.pos[0]], [a.pos[1], b.pos[1]],
                    '-', color=color, lw=lw, alpha=alpha, zorder=2)

        self._draw_hull_fill(ax)
        self._draw_guards(ax, winner)
        self._draw_legend(ax, show_attack=True, show_winner=winner is not None)
        self.canvas.draw()

    # Simulation of attack with meters
    def _draw_border_meter_attack(self, from_m, to_m, winner=None):
        ax = self.ax
        ax.clear()
        self._style_axes()
        if not self.hull_mines:
            self.canvas.draw()
            return

        self._draw_mines(ax)

        n = len(self.hull_mines)
        perimeter = get_perimeter(self.hull_mines)
        
        from_m = from_m % perimeter
        to_m = to_m % perimeter

        intervals = []
        if from_m > to_m:
            intervals.append((from_m, perimeter))
            intervals.append((0.0, to_m))
        else:
            intervals.append((from_m, to_m))

        cumulative = 0.0
        for i in range(n):
            a = self.hull_mines[i]
            b = self.hull_mines[(i + 1) % n]
            dx = b.pos[0] - a.pos[0]
            dy = b.pos[1] - a.pos[1]
            edge_len = (dx**2 + dy**2) ** 0.5
            edge_start = cumulative
            edge_end   = cumulative + edge_len

            ax.plot([a.pos[0], b.pos[0]], [a.pos[1], b.pos[1]],
                    '-', color="#00FF7F", lw=1.8, alpha=0.55, zorder=2)

            for f_m, t_m in intervals:
                if f_m < edge_end and t_m > edge_start:
                    clip_start = max(f_m, edge_start) - edge_start
                    clip_end   = min(t_m,   edge_end)   - edge_start

                    t0 = clip_start / edge_len if edge_len > 0 else 0
                    t1 = clip_end   / edge_len if edge_len > 0 else 1

                    x0, y0 = a.pos[0] + t0 * dx, a.pos[1] + t0 * dy
                    x1, y1 = a.pos[0] + t1 * dx, a.pos[1] + t1 * dy

                    ax.plot([x0, x1], [y0, y1],
                            '-', color="#FF3030", lw=3.5, alpha=1.0, zorder=3)

            cumulative += edge_len

        self._draw_hull_fill(ax)
        self._draw_guards(ax, winner)
        self._draw_legend(ax, show_attack=True, show_winner=winner is not None)
        self.canvas.draw()

    def simulate_edge_attack(self):
        if not self.hull_mines or not self.guards or self.table is None:
            return

        n = len(self.hull_mines)
        edges_with_guards = list({g.edge_index for g in self.guards})
        if not edges_with_guards:
            return

        edge_idx = random.choice(edges_with_guards)
        mine_from = self.hull_mines[edge_idx]
        mine_to   = self.hull_mines[(edge_idx + 1) % n]

        winner = find_loudest_by_edge(
            self.guards, self.table,
            self.hull_mines, mine_from, mine_to
        )

        self._draw_border_edge_attack(highlight_edge_idx=edge_idx, winner=winner)

        if winner:
            info = (
                f"ATTACK ON EDGE {mine_from.id} → {mine_to.id}\n\n"
                f"Commander chosen: {winner.name}\n"
                f"Loudness: {winner.loudness}\n"
                f"Position: {winner.position_meters:.1f} m\n"
            )
            log_msg = f"Attack on edge {mine_from.id} -> {mine_to.id}. Defended by Commander {winner.name} (Loudness: {winner.loudness})."
        else:
            info = f"ATTACK ON EDGE {mine_from.id} → {mine_to.id}\n\nNo guards on this edge."
            log_msg = f"Attack on edge {mine_from.id} -> {mine_to.id}. Breach! No guards found on this edge."
            
        self._set_info(info)

        attack_event = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "edge_attack",
            "details": f"Edge index {edge_idx}",
            "log": log_msg
        }
        threading.Thread(target=self.background_save_task, args=[attack_event], daemon=True).start()
    
    def simulate_attack_by_meters(self):
        if not self.hull_mines or not self.guards or self.table is None:
            return

        perimeter = get_perimeter(self.hull_mines)
        
        from_m = random.uniform(0, perimeter)
        to_m = (from_m + random.uniform(5, perimeter * 0.3)) % perimeter

        winner, error = find_loudest_by_meters(
            self.guards, self.table, self.step_m, from_m, to_m
        )

        self._draw_border_meter_attack(from_m, to_m, winner=winner)

        if winner:
            info = (
                f"ATTACK [{from_m:.1f}m → {to_m:.1f}m]\n\n"
                f"Commander chosen: {winner.name}\n"
                f"Loudness: {winner.loudness}\n"
                f"Position: {winner.position_meters:.1f} m\n\n"
                f"{winner.name}: Archers! Draw! Fire!"
            )
            log_msg = f"Attack range [{from_m:.1f}m -> {to_m:.1f}m]. Defended by Commander {winner.name} (Loudness: {winner.loudness})."
        else:
            info = (
                f"ATTACK [{from_m:.1f}m → {to_m:.1f}m]\n\n"
                f"No guards on this segment!\n\n"
                f"{error if error else 'Empty range'}"
            )
            log_msg = f"Attack range [{from_m:.1f}m -> {to_m:.1f}m]. Breach! Segment unprotected. Error: {error if error else 'Empty range'}."

        self._set_info(info)

        attack_event = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "meter_attack",
            "details": f"Range {from_m:.1f}m to {to_m:.1f}m",
            "log": log_msg
        }
        threading.Thread(target=self.background_save_task, args=[attack_event], daemon=True).start()

    def refresh_examples(self):

        for widget in self.scroll.winfo_children():
            widget.destroy()

        for json_path in get_json_files():
            filename = os.path.splitext(os.path.basename(json_path))[0]

            ctk.CTkButton(
                self.scroll,
                text=filename,
                font=("Arial", 15),
                height=30,
                fg_color=SECONDARY,
                command=lambda p=json_path: self.load_example(p)
            ).pack(pady=5, padx=(5, 10), fill="x")

    def background_save_task(self, attack_event=None):
        if not self.current_log_name:
            return

        final_kra_name = self.current_log_name.replace(".", "_", 1) + ".kra"
        final_kra_path = os.path.join("compressed_data", final_kra_name)
        
        decompressed_read_name = final_kra_name.replace(".kra", "").replace("_", ".", 1)
        decompressed_dir = "decompressed_data"
        decompressed_read_path = os.path.join(decompressed_dir, decompressed_read_name)

        decompressed_write_path = os.path.join(decompressed_dir, self.current_log_name)

        file_data = None

        try:
            if os.path.exists(final_kra_path):
                CompManager.decompress_one_file(final_kra_path)
                
                if os.path.exists(decompressed_read_path):
                    with open(decompressed_read_path, 'r', encoding='utf-8') as f:
                        file_data = json.load(f)
                    
                    os.remove(decompressed_read_path)
        except Exception as e:
            print("Error during reading old archive:", e)

        if not file_data:
            file_data = {
                "inputs": {
                    "dwarves": getattr(data_store, "dwarves", []),
                    "mines": getattr(data_store, "mines", []),
                    "guards": getattr(data_store, "guards", [])
                },
                "outputs": {
                    "hull_mines": self.hull_mines,
                    "placed_guards": self.guards,
                    "step_meters": self.step_m,
                    "attacks_history": []
                }
            }

        if "outputs" not in file_data: 
            file_data["outputs"] = {}
        if "attacks_history" not in file_data["outputs"]: 
            file_data["outputs"]["attacks_history"] = []

        if attack_event:
            file_data["outputs"]["attacks_history"].append(attack_event)

        try:
            os.makedirs(decompressed_dir, exist_ok=True)
            
            with open(decompressed_write_path, 'w', encoding='utf-8') as f:
                json.dump(file_data, f, ensure_ascii=False, indent=4, default=lambda o: o.__dict__)
            
            CompManager.compress_one_file(decompressed_write_path)
            
        except Exception as e:
            import traceback
            print(f"Segment BG append task ERROR: {e}")
            traceback.print_exc()
            
        finally:
            if os.path.exists(decompressed_write_path):
                os.remove(decompressed_write_path)
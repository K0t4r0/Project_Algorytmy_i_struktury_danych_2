import datetime
import tempfile
import json
import threading
import customtkinter as ctk
from tools.compression_manager import CompManager
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ui.colors import *
from tools.draw import select_example, draw_flow, draw_world, get_json_files
from algorithms.min_cost_max_flow import MCMF
from tools.data_manager import data_store, DataManager
import os
import copy
import hashlib


class FlowPage(ctk.CTkFrame):
    
    #Left frame (examples)
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)
        self.history = [[]]
        self.current_idx = 0
        self.is_animating = False
        self.solver_gen = None
        self.json_path = None

        left_frame = ctk.CTkFrame(self, 
                     width=200,
                     fg_color=BG_SECONDARY,
                     corner_radius=0
                     )
        left_frame.pack(fill="y", side="left")

        ctk.CTkLabel(left_frame, text="Flow", font=("Arial", 30, "bold")).pack(pady=20)

        #Scrollbar frame
        self.scroll = ctk.CTkScrollableFrame(left_frame, fg_color=BG_SECONDARY)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(5,5))

        #Examples
        self.refresh_examples()

        #Return button to Main menu
        ctk.CTkButton(left_frame,
                        text="Back",
                        font=("Arial", 20),
                        command=lambda: controller.show_frame("MainMenu")
                        ).pack(pady=10)
        

        main_frame = ctk.CTkFrame(self,
                                  fg_color=BG_SECONDARY)
        main_frame.pack(padx=20,pady=20, fill="both", expand=True)


        #Middle frame (graph)
        mid_frame = ctk.CTkFrame(main_frame, fg_color=BG_THIRDY)
        mid_frame.pack(padx=15,pady=15, side="left", fill="both", expand=True)

        #Slider with steps of algorithm and control button (start/stop)
        controls_frame = ctk.CTkFrame(mid_frame, height=80)
        controls_frame.propagate(False)
        controls_frame.pack(fill="x", padx=20, pady=(20,10), side="bottom")

        self.slider = ctk.CTkSlider(controls_frame, from_=0.1, to=2)
        self.slider.pack(pady=10, padx=10, fill="x")

        btns_container = ctk.CTkFrame(controls_frame, fg_color="transparent")
        btns_container.pack(pady=10, padx=10)

        self.back_btn = ctk.CTkButton(btns_container, text="<", width=40, command=self.step_backward)
        self.back_btn.pack(side="left", padx=5)

        self.toggle_btn = ctk.CTkButton(
            btns_container,
            text="Start Animation",
            width=150,
            command=self.toggle_animation_button
        )
        self.toggle_btn.pack(padx=5, side="left")

        self.next_btn = ctk.CTkButton(btns_container, text=">", width=40, command=self.step_forward)
        self.next_btn.pack(side="left", padx=5)
    
        #Graph frame (matplot)
        graph_frame = ctk.CTkFrame(mid_frame)
        graph_frame.pack(fill="both", expand=True, padx=20, pady=(20,10))

        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor=BG_THIRDY)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(BG_THIRDY)
        self.fig.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08)
        
        self.canvas = FigureCanvasTkAgg(self.fig, graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.ax.tick_params(axis='both', colors='white')

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        self.ax.spines['left'].set_color('white')
        self.ax.spines['bottom'].set_color('white')

        self.ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='white')
        self.ax.xaxis.grid(True, linestyle='--', alpha=0.3, color='white')
        
    #Functions for animation
    def toggle_animation_button(self):
        if self.toggle_btn.cget("text") == "Reset":
            self.reset_logic()
            ax = self.canvas.figure.axes[0]
            ax.clear()
            draw_world(self.canvas)
        elif not self.is_animating:
            self.start_animation()
        else:
            self.stop_animation()

    def start_animation(self):
        self.is_animating = True
        self.toggle_btn.configure(text="Stop Animation")
        self.run_animation_loop()

    def stop_animation(self):
        self.is_animating = False
        self.toggle_btn.configure(text="Start Animation")

    def run_animation_loop(self):
        if self.is_animating:
            if self.step_forward():
                slider_min = self.slider.cget("from_")
                slider_max = self.slider.cget("to")
                current_val = self.slider.get()
                
                inverted_delay = (slider_max + slider_min) - current_val
                delay = int(inverted_delay * 500)
                self.after(delay, self.run_animation_loop)
            else:
                self.is_animating = False
                self.toggle_btn.configure(text="Reset")

    def step_forward(self):
        if self.current_idx < len(self.history) - 1:
            self.current_idx += 1
            self.apply_step()
            return True
        
        if self.solver_gen is None:
            self.solver = MCMF(data_store.dwarves, data_store.mines, data_store)
            self.solver.build_network()
            self.solver_gen = self.solver.solve_generator()

            data_store_copy = copy.deepcopy(data_store)

            threading.Thread(
                target=self.background_save_task,
                args=[data_store_copy],
                daemon=True
            ).start()

        try:
            new_paths = next(self.solver_gen)
            self.history.append(new_paths)
            self.current_idx += 1
            self.apply_step()
            return True
        except StopIteration:
            return False

    def step_backward(self):
        if self.current_idx > 0:
            self.stop_animation()
            self.current_idx -= 1
            self.apply_step()

    def apply_step(self):
        if not self.history or not self.history[self.current_idx]:
            data_store.flow_paths = []
            draw_flow(self.canvas)
            return
            
        step_data = self.history[self.current_idx]
        
        if isinstance(step_data, dict):
            data_store.flow_paths = step_data["paths"]
        else:
            data_store.flow_paths = step_data 
            
        draw_flow(self.canvas)

    def reset_logic(self):
        self.history = [[]]
        self.current_idx = 0
        self.is_animating = False
        self.solver_gen = None
        self.toggle_btn.configure(text="Start Animation")

    def refresh_examples(self):

        for widget in self.scroll.winfo_children():
            widget.destroy()

        for json_path in get_json_files():
            filename = os.path.splitext(os.path.basename(json_path))[0]
            self.json_path = json_path

            ctk.CTkButton(
                self.scroll,
                text=filename,
                font=("Arial", 15),
                height=30,
                fg_color=SECONDARY,
                command=lambda p=json_path: [self.reset_logic(), select_example(p, self.canvas)]
            ).pack(pady=5, padx=(5, 10), fill="x")
        

    def background_save_task(self, data_store_copy):
        bg_solver = MCMF(data_store_copy.dwarves, data_store_copy.mines, data_store_copy)
        bg_solver.build_network()
        
        bg_history = [[]]
        for paths in bg_solver.solve_generator(is_use_gui=False):
            bg_history.append(paths)

        data_to_save = {
            "inputs": {
                "dwarves": data_store_copy.dwarves,
                "mines": data_store_copy.mines
            },
            "outputs": {
                "history": bg_history,
                "final_paths": bg_history[-1] if bg_history else []
            }
        }

        data_str = json.dumps(data_to_save, ensure_ascii=False, sort_keys=True, default=lambda o: o.__dict__)
        data_hash = hashlib.sha256(data_str.encode('utf-8')).hexdigest()[:16]

        final_kra_name = f"flow_result_{data_hash}_json.kra"
        final_kra_path = os.path.join("compressed_data", final_kra_name)

        if os.path.exists(final_kra_path):
            print(f"The {final_kra_name} archive already exists")
            return

        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"flow_result_{data_hash}.json")
        
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(data_str)
            
            CompManager.compress_one_file(temp_path)
            print(f"The new archive has been successfully compressed and saved: {final_kra_name}")
            
        except Exception as e:
            print(f"BG save task ERROR: {e}")
            
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
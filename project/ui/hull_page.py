import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ui.colors import *
from tools.draw import draw_sub_hull, get_json_files
from tools.data_manager import data_store
from algorithms.hull import graham_generator, jarvis_generator, jarvis, graham_scan
import os
import time

import threading
import tempfile
import datetime
import json
from tools.compression_manager import CompManager

class HullPage(ctk.CTkFrame):
    
    #Left frame (examples)
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)
        self.history = [(([], None), ([], None))]
        self.current_idx = 0
        self.is_animating = False
        self.hull_gen = None
        self.selected_alg = "graham"
        self.res1, self.res2 = 0, 0

        left_frame = ctk.CTkFrame(self, 
                     width=200,
                     fg_color=BG_SECONDARY,
                     corner_radius=0
                     )
        left_frame.pack(fill="y", side="left")

        ctk.CTkLabel(left_frame, text="Convex Hull", font=("Arial", 30, "bold")).pack(pady=20)

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


        #Right frame (information)
        right_frame = ctk.CTkFrame(main_frame,
                                   fg_color=BG_SECONDARY,
                                    width=220
                                    )
        right_frame.pack(padx=5, fill="y", side="right")
        right_frame.pack_propagate(False)

        ctk.CTkLabel(right_frame, text="Info", font=("Arial", 20, "bold")).pack(pady=10)

        self.info_label = ctk.CTkLabel(
            right_frame,
            text="Choose example",
            wraplength=200
        )

        self.info_label.pack(pady=10, padx=10)


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

        self.fig = Figure(figsize=(5, 8), dpi=100, facecolor=BG_THIRDY)
        self.ax_graham = self.fig.add_subplot(211)
        self.ax_jarvis = self.fig.add_subplot(212) 
        self.fig.subplots_adjust(hspace=0.5, left=0.05, right=0.95, top=0.90, bottom=0.05)
        
        self.canvas = FigureCanvasTkAgg(self.fig, graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.apply_step()


    # Functions for animation
    def load_new_example(self, path):
        self.reset_logic()
        
        data_store.load_from_json(path)
        points = [m.pos for m in data_store.mines]

        start_j = time.time()
        jarvis(points)
        end_j = time.time()
        self.res1 = end_j - start_j

        start_g = time.time()
        graham_scan(points)
        end_g = time.time()
        self.res2 = end_g - start_g

        if self.res1 < self.res2:
            diff = self.res2 - self.res1
            ratio = self.res2 / self.res1 if self.res1 > 0 else 0
            faster = f"Jarvis is {ratio:.2f}x faster\n({diff:.6f} sec difference)"
        elif self.res2 < self.res1:
            diff = self.res1 - self.res2
            ratio = self.res1 / self.res2 if self.res2 > 0 else 0
            faster = f"Graham is {ratio:.2f}x faster\n({diff:.6f} sec difference)"
        else:
            faster = "Algorithms have equal time"
        self.info_label.configure(
            text=(
                f"Jarvis: {self.res1:.6f} sec\n"
                f"Graham: {self.res2:.6f} sec\n\n"
                f"{faster}"
            )
        )

        self.apply_step()

    # Toggle button for switching modes
    def toggle_animation_button(self):
        if self.toggle_btn.cget("text") == "Reset":
            self.reset_logic()
            self.apply_step()
        elif not self.is_animating:
            self.is_animating = True
            self.toggle_btn.configure(text="Stop Animation")
            self.run_animation_loop()
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
                delay = int(((self.slider.cget("to") + self.slider.cget("from_")) - self.slider.get()) * 1000)
                self.after(delay, self.run_animation_loop)
            else:
                self.is_animating = False
                self.toggle_btn.configure(text="Reset")

    def step_forward(self):
        if self.current_idx < len(self.history) - 1:
            self.current_idx += 1
            self.apply_step()
            return True

        if self.graham_gen is None or self.jarvis_gen is None:
            points = [m.pos for m in data_store.mines]
            if not points: return False
            self.graham_gen = graham_generator(points)
            self.jarvis_gen = jarvis_generator(points)

            threading.Thread(target=self.background_save_task, daemon=True).start()

        try:
            prev_g, prev_j = self.history[-1]
            step_g = next(self.graham_gen, prev_g)
            step_j = next(self.jarvis_gen, prev_j)

            if step_g == prev_g and step_j == prev_j and self.current_idx > 0:
                return False

            self.history.append((step_g, step_j))
            self.current_idx += 1
            self.apply_step()
            return True
        except (StopIteration, Exception):
            return False

    def step_backward(self):
        if self.current_idx > 0:
            self.stop_animation()
            self.current_idx -= 1
            self.apply_step()

    #
    def apply_step(self):
        if self.history and self.current_idx < len(self.history):   
            state_g, state_j = self.history[self.current_idx]
        else:
            state_g, state_j = ([], None), ([], None)

        draw_sub_hull(self.ax_graham, state_g, "Graham Scan", "#00FF7F")
        draw_sub_hull(self.ax_jarvis, state_j, "Jarvis March", "#FFD700")
        self.canvas.draw()

    def reset_logic(self):
        self.history = [(([], None), ([], None))]
        self.current_idx = 0
        self.is_animating = False
        self.graham_gen = None
        self.jarvis_gen = None
        self.toggle_btn.configure(text="Start Animation")
    
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
                command=lambda p=json_path: self.load_new_example(p)
            ).pack(pady=5, padx=(5, 10), fill="x")

    def background_save_task(self):
        points = [m.pos for m in data_store.mines]
        if not points:
            return

        bg_graham_gen = graham_generator(points)
        bg_jarvis_gen = jarvis_generator(points)
        
        bg_history = [(([], None), ([], None))]

        while True:
            try:
                prev_g, prev_j = bg_history[-1]
                step_g = next(bg_graham_gen, prev_g)
                step_j = next(bg_jarvis_gen, prev_j)

                if step_g == prev_g and step_j == prev_j and len(bg_history) > 1:
                    break

                bg_history.append((step_g, step_j))
            except (StopIteration, Exception):
                break

        data_to_save = {
            "inputs": {
                "dwarves": data_store.dwarves,
                "mines": data_store.mines
            },
            "outputs": {
                "history": bg_history,
                "final_state": bg_history[-1] if bg_history else None,
                "performance": {
                    "jarvis_sec": self.res1,
                    "graham_sec": self.res2
                }
            }
        }

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"hull_result_{current_time}.json")
        
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4, default=lambda o: o.__dict__)
            
            CompManager.compress_one_file(temp_path)
            
        except Exception as e:
            import traceback
            print(f"Hull BG save task ERROR: {e}")
            traceback.print_exc()
            
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
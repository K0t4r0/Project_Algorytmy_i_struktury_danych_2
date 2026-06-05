import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ui.colors import *
from tools.draw import draw_sub_hull
from tools.data_manager import data_store, get_json_files
from algorithms.hull import graham_generator, jarvis_generator, jarvis, graham_scan
import os
import time
from tools.graph_navigation import connect_navigation
import threading
import tempfile
import hashlib
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
        self.animated = True
        self.graph_state_graham = {"drag_start": None}
        self.graph_state_jarvis = {"drag_start": None}

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

        #Toggle button for off/on animation
        self.anim_mode_btn = ctk.CTkButton(
            left_frame,
            text="Animation: ON",
            font=("Arial", 15),
            width=140,
            command=self.toggle_anim_mode
        )
        self.anim_mode_btn.pack(pady=(0, 5), padx=8)
        self.default_fg = self.anim_mode_btn.cget("fg_color")

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

        connect_navigation(self.canvas, {
            self.ax_graham: self.graph_state_graham,
            self.ax_jarvis: self.graph_state_jarvis,
        })

        self.apply_step()

    #Function for toggle button (off/on)
    def toggle_anim_mode(self):
        self.animated = not self.animated
        
        self.anim_mode_btn.configure(
            text=f"Animation: {'ON' if self.animated else 'OFF'}",
            fg_color=self.default_fg if self.animated else "#555555"
        )
        state = "normal" if self.animated else "disabled"
        self.toggle_btn.configure(
            text="Start Animation" if self.animated else "Start"
        )
        self.back_btn.configure(state=state)
        self.next_btn.configure(state=state)

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
            if not points:
                return False
            self.graham_gen = graham_generator(points)
            self.jarvis_gen = jarvis_generator(points)

            threading.Thread(target=self.background_save_task, daemon=True).start()

            if not self.animated:
                final_g, final_j = ([], None), ([], None)
                while True:
                    prev_g, prev_j = final_g, final_j
                    step_g = next(self.graham_gen, prev_g)
                    step_j = next(self.jarvis_gen, prev_j)
                    if step_g == prev_g and step_j == prev_j:
                        break
                    final_g, final_j = step_g, step_j

                self.history.append((final_g, final_j))
                self.current_idx += 1
                self.apply_step()
                self.graham_gen = None
                self.jarvis_gen = None
                self.toggle_btn.configure(text="Reset")
                return False

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
        
        bg_history = []
        step_count = 1

        while True:
            try:
                if bg_history:
                    prev_g, prev_j = bg_history[-1]["state"]
                else:
                    prev_g, prev_j = ([], None), ([], None)

                step_g = next(bg_graham_gen, prev_g)
                step_j = next(bg_jarvis_gen, prev_j)

                if step_g == prev_g and step_j == prev_j and len(bg_history) > 0:
                    break

                graham_points = step_g[0]
                jarvis_points = step_j[0]

                g_action = f"Graham Scan: Hull contains {len(graham_points)} points."
                if step_g[1]:
                    g_action += f" Testing point at {step_g[1]}."

                j_action = f"Jarvis March: Hull contains {len(jarvis_points)} points."
                if step_j[1]:
                    j_action += f" Scanning current point at {step_j[1]}."

                step_data = {
                    "step": step_count,
                    "graham_log": g_action,
                    "jarvis_log": j_action,
                    "state": (step_g, step_j)
                }

                bg_history.append(step_data)
                step_count += 1

            except (StopIteration, Exception):
                break

        bg_history.insert(0, {
            "step": 0,
            "graham_log": "Graham Scan initialized.",
            "jarvis_log": "Jarvis March initialized.",
            "state": (([], None), ([], None))
        })

        data_to_save = {
            "inputs": {
                "dwarves": data_store.dwarves,
                "mines": data_store.mines
            },
            "outputs": {
                "history": bg_history,
                "final_state": bg_history[-1]["state"] if bg_history else None,
                "performance": {
                    "jarvis_sec": self.res1,
                    "graham_sec": self.res2
                }
            }
        }

        hash_str = json.dumps(data_to_save, ensure_ascii=False, sort_keys=True, separators=(',', ':'), default=lambda o: o.__dict__)
        data_hash = hashlib.sha256(hash_str.encode('utf-8')).hexdigest()[:16]

        final_kra_name = f"hull_result_{data_hash}_json.kra"
        final_kra_path = os.path.join("compressed_data", final_kra_name)

        if os.path.exists(final_kra_path):
            print(f"The {final_kra_name} archive already exists")
            return

        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"hull_result_{data_hash}.json")
        
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4, default=lambda o: o.__dict__)
            
            CompManager.compress_one_file(temp_path)
            print(f"The new archive has been successfully compressed and saved: {final_kra_name}")
            
        except Exception as e:
            import traceback
            print(f"Hull BG save task ERROR: {e}")
            traceback.print_exc()
            
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
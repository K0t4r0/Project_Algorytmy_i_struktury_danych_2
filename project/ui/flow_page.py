import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ui.colors import *
from tools.draw import select_example, json_files, draw_flow, draw_world
from algorithms.min_cost_max_flow import MCMF
from tools.data_manager import data_store

class FlowPage(ctk.CTkFrame):
    
    #Left frame (examples)
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)
        self.history = [[]]
        self.current_idx = 0
        self.is_animating = False
        self.solver_gen = None

        left_frame = ctk.CTkFrame(self, 
                     width=200,
                     fg_color=BG_SECONDARY,
                     corner_radius=0
                     )
        left_frame.pack(fill="y", side="left")

        ctk.CTkLabel(left_frame, text="Flow", font=("Arial", 30, "bold")).pack(pady=20)

        #Scrollbar frame
        scroll = ctk.CTkScrollableFrame(left_frame, fg_color=BG_SECONDARY)
        scroll.pack(fill="both", expand=True, padx=20, pady=(5,5))

        #Examples
        for i, json_path in enumerate(json_files, 1):
            ctk.CTkButton(scroll, 
                        text=f"Example {i}",
                        font=("Arial", 15),  
                        height=30, 
                        fg_color=SECONDARY,
                        command=lambda p=json_path: [self.reset_logic(), select_example(p, self.canvas)]
                        ).pack(pady=5, padx=(5,10), fill="x")

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
                delay = int(inverted_delay * 1000)
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
            self.solver = MCMF(data_store.dwarves, data_store.mines)
            self.solver.build_network()
            self.solver_gen = self.solver.solve_generator()

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
        data_store.flow_paths = self.history[self.current_idx]
        draw_flow(self.canvas)

    def reset_logic(self):
        self.history = [[]]
        self.current_idx = 0
        self.is_animating = False
        self.solver_gen = None
        self.toggle_btn.configure(text="Start Animation")
        
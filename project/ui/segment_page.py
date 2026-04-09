import customtkinter as ctk
from ui.colors import *
#from algorithms.flow import run_flow_example

class SegmentPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)

        left_frame = ctk.CTkFrame(self, 
                     width=200,
                     fg_color=BG_SECONDARY,
                     corner_radius=0
                     )
        left_frame.pack(fill="y", side="left")

        ctk.CTkLabel(left_frame, text="Segment Tree", font=("Arial", 30, "bold")).pack(pady=20)

        scroll = ctk.CTkScrollableFrame(left_frame, fg_color=BG_SECONDARY)
        scroll.pack(fill="both", expand=True, padx=20, pady=(5,5))

        for i in range(1, 31):
            ctk.CTkButton(scroll, 
                        text=f"Example {i}",
                        font=("Arial", 15),  
                        height=30, 
                        fg_color=SECONDARY,
                        #command=lambda i=i: self.run_example(i)).pack(pady=5, padx=10, fill="x"
                        )

        ctk.CTkButton(left_frame,
                        text="Back",
                        font=("Arial", 20),
                        command=lambda: controller.show_frame("MainMenu")
                        ).pack(pady=10)
        
        main_frame = ctk.CTkFrame(self,
                                  fg_color=BG_SECONDARY)
        main_frame.pack(padx=20,pady=20, fill="both", expand=True)

        mid_frame = ctk.CTkFrame(main_frame, fg_color=BG_THIRDY)
        mid_frame.pack(padx=15,pady=15, side="left", fill="both", expand=True)

        graph_frame = ctk.CTkFrame(mid_frame)
        graph_frame.pack(fill="both", expand=True, padx=20, pady=(20,10))

        controls_frame = ctk.CTkFrame(mid_frame, height=100)
        controls_frame.pack(fill="x", padx=20, pady=(20,10))

        self.canvas = ctk.CTkCanvas(graph_frame, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.slider = ctk.CTkSlider(controls_frame, from_=0.1, to=2)
        self.slider.pack(pady=10, padx=10, fill="x")

        self.start_btn = ctk.CTkButton(
            controls_frame,
            text="Start Animation",
            #command=self.start_animation
        )
        self.start_btn.pack(pady=10)

        right_frame = ctk.CTkFrame(main_frame,
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
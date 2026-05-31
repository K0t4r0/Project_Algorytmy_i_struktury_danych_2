import customtkinter as ctk

from ui.main_menu import MainMenu
from ui.flow_page import FlowPage
from ui.hull_page import HullPage
from ui.segment_page import SegmentPage
from ui.compression_page import CompressionPage
from ui.generate_page import GeneratorPage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Algorytmy Projekt")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainMenu, FlowPage, HullPage, SegmentPage, CompressionPage, GeneratorPage):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")
    def center_window(self, width, height):
        self.update_idletasks()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2)) - 50

        self.geometry(f"{width}x{height}+{x}+{y}")
    def show_frame(self, name):
        frame = self.frames[name]
        if hasattr(frame, "refresh_examples"):
            frame.refresh_examples()
        frame.tkraise()

        if name == "MainMenu":
            self.center_window(600, 500)
        elif name == "GeneratorPage":
            self.center_window(710, 590)
        else:
            self.center_window(1400, 650)
        self.update_idletasks()
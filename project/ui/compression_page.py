import os
import textwrap
import customtkinter as ctk

from tools.compression_manager import CompManager 
from algorithms.search import kmp_file_search
from ui.colors import *

class CompressionPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)
        
        self.controller = controller
        self.current_results = []
        self.current_search_index = -1
        self.pattern_length = 0

        self.setup_left_frame()
        self.setup_main_frame()
        
        self.refresh_file_list()

    def setup_left_frame(self):
        self.left_frame = ctk.CTkFrame(self, width=200, fg_color=BG_SECONDARY, corner_radius=0)
        self.left_frame.pack(fill="y", side="left")

        ctk.CTkLabel(self.left_frame, text="Files", font=("Arial", 30, "bold")).pack(pady=20)

        self.scroll = ctk.CTkScrollableFrame(self.left_frame, fg_color=BG_SECONDARY)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(5,5))

        ctk.CTkButton(self.left_frame, text="Refresh", font=("Arial", 15),
                      command=self.refresh_file_list).pack(pady=(0, 5), padx=20, fill="x")

        ctk.CTkButton(self.left_frame, text="Back", font=("Arial", 20),
                      command=lambda: self.controller.show_frame("MainMenu")).pack(pady=10)

    def setup_main_frame(self):
        main_frame = ctk.CTkFrame(self, fg_color=BG_SECONDARY)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        mid_frame = ctk.CTkFrame(main_frame, fg_color=BG_THIRDY)
        mid_frame.pack(padx=15, pady=15, side="left", fill="both", expand=True)

        text_frame = ctk.CTkFrame(mid_frame)
        text_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        self.textbox = ctk.CTkTextbox(text_frame, wrap="none", font=("Consolas", 14))
        self.textbox.pack(fill="both", expand=True)
        self.textbox.tag_config("highlight", background="yellow", foreground="black")
        self.textbox.tag_config("active_highlight", background="orange", foreground="black")

        controls_frame = ctk.CTkFrame(mid_frame, height=50)
        controls_frame.pack(fill="x", padx=20, pady=(10, 20))

        self.search_entry = ctk.CTkEntry(controls_frame, placeholder_text="Enter pattern to search...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=10)

        self.search_btn = ctk.CTkButton(controls_frame, text="Search", width=80, command=self.perform_search)
        self.search_btn.pack(side="left", padx=(0, 10))

        self.prev_btn = ctk.CTkButton(controls_frame, text="<", width=30, command=self.prev_result)
        self.prev_btn.pack(side="left", padx=(0, 5))
        
        self.result_label = ctk.CTkLabel(controls_frame, text="0/0", width=40)
        self.result_label.pack(side="left", padx=(0, 5))

        self.next_btn = ctk.CTkButton(controls_frame, text=">", width=30, command=self.next_result)
        self.next_btn.pack(side="left", padx=(0, 10))

        right_frame = ctk.CTkFrame(main_frame, fg_color=BG_SECONDARY, width=220)
        right_frame.pack(padx=5, fill="y", side="right")
        right_frame.pack_propagate(False)

        ctk.CTkLabel(right_frame, text="Info", font=("Arial", 20, "bold")).pack(pady=10)

        self.info_label = ctk.CTkLabel(right_frame, text="Choose a file to decompress", wraplength=200)
        self.info_label.pack(pady=10, padx=10)

    def refresh_file_list(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        compressed_dir = "compressed_data"
        if not os.path.exists(compressed_dir):
            os.makedirs(compressed_dir, exist_ok=True)
            return

        files = [f for f in os.listdir(compressed_dir) if f.endswith(".kra")]
        for f in files:
            display_text = textwrap.fill(f, width=20, break_long_words=True)

            ctk.CTkButton(
                self.scroll, 
                text=display_text, 
                font=("Arial", 15),  
                height=30, 
                fg_color=SECONDARY,
                command=lambda fname=f: self.load_and_decompress(fname)
            ).pack(pady=5, padx=10, fill="x")

    def load_and_decompress(self, filename):
        kra_path = os.path.join("compressed_data", filename)
        
        self.info_label.configure(text=f"Decompressing {filename}...")
        self.update()

        try:
            CompManager.decompress_one_file(kra_path)
            out_name = filename.replace(".kra", "").replace("_", ".", 1)
            self.current_decompressed_path = os.path.join("decompressed_data", out_name)

            with open(self.current_decompressed_path, 'r', encoding='utf-8') as f:
                content = f.read()

            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", content)
            self.info_label.configure(text=f"Loaded:\n{out_name}\n\nSize: {len(content)} chars")
            
            self.clear_search()

        except Exception as e:
            self.info_label.configure(text=f"Error:\n{str(e)}")


    def perform_search(self):
        pattern = self.search_entry.get()
        if not pattern or not hasattr(self, 'current_decompressed_path'):
            return

        self.info_label.configure(text=f"Searching for '{pattern}'...")
        self.update()

        self.current_results = kmp_file_search(self.current_decompressed_path, pattern)
        self.pattern_length = len(pattern)
        
        self.textbox.tag_remove("highlight", "1.0", "end")
        self.textbox.tag_remove("active_highlight", "1.0", "end")

        if self.current_results:
            self.current_search_index = 0
            
            for idx in self.current_results:
                start_pos = f"1.0 + {idx} chars"
                end_pos = f"1.0 + {idx + self.pattern_length} chars"
                self.textbox.tag_add("highlight", start_pos, end_pos)
            
            self.update_highlight()
            self.info_label.configure(text=f"Found {len(self.current_results)} matches.")
        else:
            self.current_search_index = -1
            self.info_label.configure(text="No matches found.")
            
        self.update_search_ui()

    def update_highlight(self):
        self.textbox.tag_remove("active_highlight", "1.0", "end")
        
        if self.current_results and self.current_search_index >= 0:
            idx = self.current_results[self.current_search_index]
            start_pos = f"1.0 + {idx} chars"
            end_pos = f"1.0 + {idx + self.pattern_length} chars"
            
            self.textbox.tag_add("active_highlight", start_pos, end_pos)
            self.textbox.see(start_pos)

    def prev_result(self):
        if self.current_results:
            self.current_search_index = (self.current_search_index - 1) % len(self.current_results)
            self.update_highlight()
            self.update_search_ui()

    def next_result(self):
        if self.current_results:
            self.current_search_index = (self.current_search_index + 1) % len(self.current_results)
            self.update_highlight()
            self.update_search_ui()

    def update_search_ui(self):
        if not self.current_results:
            self.result_label.configure(text="0/0")
        else:
            self.result_label.configure(text=f"{self.current_search_index + 1}/{len(self.current_results)}")

    def clear_search(self):
        self.current_results = []
        self.current_search_index = -1
        self.search_entry.delete(0, "end")
        self.update_search_ui()
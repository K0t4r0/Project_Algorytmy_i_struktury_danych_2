import os
import re
import json
import datetime
import customtkinter as ctk

from tools.compression_manager import CompManager 
from algorithms.search import rabin_karp_file_search
from ui.colors import *

class CompressionPage(ctk.CTkFrame):
    JSON_TOKEN_RE = re.compile(r'''
        (?P<string>"(?:\\.|[^"\\])*")
    | (?P<number>-?\d+\.?\d*(?:[eE][+-]?\d+)?)
    | (?P<bool>\btrue\b|\bfalse\b|\bnull\b)
    | (?P<brace>[\{\}\[\]])
    ''', re.VERBOSE)

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)
        
        self.controller = controller
        self.current_results = []
        self.current_search_index = -1
        self.pattern_length = 0

        self.setup_left_frame()
        self.refresh_examples()
        self.setup_main_frame()

    def setup_left_frame(self):
        self.left_frame = ctk.CTkFrame(self, width=200, fg_color=BG_SECONDARY, corner_radius=0)
        self.left_frame.pack(fill="y", side="left")

        ctk.CTkLabel(self.left_frame, text="Files", font=("Arial", 30, "bold")).pack(pady=20)

        self.scroll = ctk.CTkScrollableFrame(self.left_frame, fg_color=BG_SECONDARY)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(5,5))

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
        self.textbox.tag_config("json_key",    foreground="#6FB3FF")
        self.textbox.tag_config("json_string", foreground="#98C379")
        self.textbox.tag_config("json_number", foreground="#D19A66")
        self.textbox.tag_config("json_bool",   foreground="#C678DD")
        self.textbox.tag_config("json_brace",  foreground="#ABB2BF")

        self.textbox.tag_raise("highlight")
        self.textbox.tag_raise("active_highlight")

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

        self.jump_output_btn = ctk.CTkButton(
            controls_frame,
            text="Output",
            width=90,
            fg_color=SECONDARY,
            command=self.jump_to_output
        )
        self.jump_output_btn.pack(side="left", padx=(10, 0))

        right_frame = ctk.CTkFrame(main_frame, fg_color=BG_SECONDARY, width=220)
        right_frame.pack(padx=5, fill="y", side="right")
        right_frame.pack_propagate(False)

        ctk.CTkLabel(right_frame, text="Info", font=("Arial", 20, "bold")).pack(pady=10)

        self.info_label = ctk.CTkLabel(right_frame, text="Choose a file to decompress", wraplength=200)
        self.info_label.pack(pady=10, padx=10)

    def refresh_examples(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        compressed_dir = "compressed_data"
        if not os.path.exists(compressed_dir):
            os.makedirs(compressed_dir, exist_ok=True)
            return

        files = [f for f in os.listdir(compressed_dir) if f.endswith(".kra")]
        for f in files:
            filename = os.path.basename(f)

            if filename.startswith("flow_"):
                alg_name = "Flow (MCMF)"
            elif filename.startswith("hull_"):
                alg_name = "Convex Hull"
            elif filename.startswith("segment_"):
                alg_name = "Border Guards"
            else:
                alg_name = "Unknown Algorithm"

            try:
                timestamp = os.path.getctime(os.path.join(compressed_dir, f))
                date_str = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d at %H:%M:%S")
            except Exception as e:
                print("WRONG timestamp in comp page:", e)
                date_str = "Unknown Date"

            display_text = f"{alg_name}\n\n{date_str}"

            ctk.CTkButton(
                self.scroll, 
                text=display_text, 
                font=("Arial", 14), 
                height=70,          
                fg_color=SECONDARY,
                anchor="w", 
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

            try:
                with open(self.current_decompressed_path, 'r', encoding='utf-8') as f:
                    raw_content = f.read()

                parsed_json = json.loads(raw_content)
                content = json.dumps(parsed_json, indent=4, ensure_ascii=False)

                with open(self.current_decompressed_path, 'w', encoding='utf-8') as f:
                    f.write(content)

            except json.JSONDecodeError:
                content = raw_content
            except Exception as e:
                content = f"Error reading file: {e}"

            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", content)
            self._highlight_json() 

            comp_size = os.stat(kra_path).st_size
            decomp_size = os.stat(os.path.join("decompressed_data", out_name)).st_size
            info_label_text = f"Loaded:\n{out_name}\n\nSize: {len(content)} chars\n\n"

            info_label_text += f"Original size = {(decomp_size / 1024):.4f} KB\n"
            info_label_text += f"Compressed size = {(comp_size / 1024):.4f} KB\n\n"

            if decomp_size > comp_size:
                info_label_text += f"Compressed file is {(decomp_size / comp_size):.2f}x smaller than original one\n"

            self.info_label.configure(text=info_label_text)
            
            self.clear_search()

        except Exception as e:
            self.info_label.configure(text=f"Error:\n{str(e)}")


    def perform_search(self):
        pattern = self.search_entry.get()
        if not pattern or not hasattr(self, 'current_decompressed_path'):
            return

        self.info_label.configure(text=f"Searching for '{pattern}'...")
        self.update()

        self.current_results = rabin_karp_file_search(self.current_decompressed_path, pattern)
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

    def _highlight_json(self):
        content = self.textbox.get("1.0", "end-1c")

        for tag in ("json_key", "json_string", "json_number", "json_bool", "json_brace"):
            self.textbox.tag_remove(tag, "1.0", "end")

        for m in self.JSON_TOKEN_RE.finditer(content):
            kind = m.lastgroup
            start, end = m.start(), m.end()

            if kind == "string":
                rest = content[end:end+2]
                is_key = rest.lstrip().startswith(":")
                tag = "json_key" if is_key else "json_string"
            elif kind == "number":
                tag = "json_number"
            elif kind == "bool":
                tag = "json_bool"
            else:
                tag = "json_brace"

            start_pos = f"1.0 + {start} chars"
            end_pos   = f"1.0 + {end} chars"
            self.textbox.tag_add(tag, start_pos, end_pos)

    def jump_to_output(self):
        content = self.textbox.get("1.0", "end-1c")
        idx = content.find('"outputs"')
        if idx == -1:
            return

        start_pos = f"1.0 + {idx} chars"
        end_pos   = f"1.0 + {idx + len('\"outputs\"')} chars"

        self.textbox.see(start_pos)
        self.textbox.mark_set("insert", start_pos)

        self.textbox.tag_remove("active_highlight", "1.0", "end")
        self.textbox.tag_add("active_highlight", start_pos, end_pos)
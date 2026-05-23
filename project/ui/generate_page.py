import random
import customtkinter as ctk
from ui.colors import *
from tools.generator import DwarfDataGenerator

FIELDS = [
    ("Min dwarves",   "min_dwarves",   1,    500),
    ("Max dwarves",   "max_dwarves",   1,    500),
    ("Min mines",     "min_mines",     2,    200),
    ("Max mines",     "max_mines",     2,    200),
    ("Min guards",    "min_guards",    1,    500),
    ("Max guards",    "max_guards",    1,    500),
    ("Grid size",     "grid_size",     10,   2000),
    ("Min distance",  "min_distance",  1,    100),
    ("Min skills",    "min_skills",    1,    4),
    ("Max skills",    "max_skills",    1,    4),
    ("Min value",     "min_value",     1,    1000),
    ("Max value",     "max_value",     1,    1000),
    ("Min capacity",  "min_capacity",  1,    50),
    ("Max capacity",  "max_capacity",  1,    50),
    ("Min loudness",  "min_loudness",  1,    200),
    ("Max loudness",  "max_loudness",  1,    200),
]


class GeneratorPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_MAIN)

        self._entries = {} 

        ctk.CTkLabel(self, text="Data Generator", font=("Arial", 32, "bold")).pack(pady=(28, 4))
        ctk.CTkLabel(self, text="Configure parameters, then press Random or Generate.", font=("Arial", 14), text_color="gray").pack(pady=(0, 16))

        card = ctk.CTkFrame(self, fg_color=BG_SECONDARY, corner_radius=12)
        card.pack(padx=60, pady=(0, 10), fill="both", expand=True)

        scroll = ctk.CTkScrollableFrame(card, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=16)

        for idx, (label, key, lo, hi) in enumerate(FIELDS):
            row = idx // 2
            col = idx %  2

            cell = ctk.CTkFrame(scroll, fg_color="transparent")
            cell.grid(row=row, column=col, padx=20, pady=6, sticky="w")

            ctk.CTkLabel(cell, text=label,
                         font=("Arial", 13), width=120,
                         anchor="w").pack(side="left")

            entry = ctk.CTkEntry(cell, width=90,
                                 font=("Arial", 13),
                                 fg_color=BG_THIRDY,
                                 border_color=SECONDARY)
            entry.pack(side="left", padx=(8, 0))

            default = DwarfDataGenerator.__init__.__defaults__ 
            entry.insert(0, str(self._default(key)))

            self._entries[key] = entry

        self._status = ctk.CTkLabel(card, text="",
                                    font=("Arial", 13),
                                    text_color="gray")
        self._status.pack(pady=(0, 6))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(6, 24))

        ctk.CTkButton(btn_row, text="Back",
                      width=120, height=38,
                      font=("Arial", 15),
                      fg_color=SECONDARY,
                      command=lambda: controller.show_frame("MainMenu")
                      ).pack(side="left", padx=10)

        ctk.CTkButton(btn_row, text="Random",
                      width=140, height=38,
                      font=("Arial", 15),
                      fg_color=SECONDARY,
                      hover_color=PRIMARY_HOVER,
                      command=self._fill_random
                      ).pack(side="left", padx=10)

        ctk.CTkButton(btn_row, text="Generate",
                      width=160, height=38,
                      font=("Arial", 15, "bold"),
                      fg_color=PRIMARY,
                      hover_color=PRIMARY_HOVER,
                      command=self._generate
                      ).pack(side="left", padx=10)

    def _default(self, key):
        defaults = {
            "min_dwarves": 10, "max_dwarves": 50,
            "min_mines":    5, "max_mines":   20,
            "min_guards":  10, "max_guards":  50,
            "grid_size":  100, "min_distance": 5,
            "min_skills":   1, "max_skills":   3,
            "min_value":   50, "max_value":  150,
            "min_capacity": 1, "max_capacity": 10,
            "min_loudness":30, "max_loudness":120,
        }
        return defaults.get(key, 1)

    def _fill_random(self):
        r = {
            "min_dwarves":  random.randint(5,  30),
            "max_dwarves":  random.randint(31, 100),
            "min_mines":    random.randint(3,  10),
            "max_mines":    random.randint(11, 40),
            "min_guards":   random.randint(5,  20),
            "max_guards":   random.randint(21, 80),
            "grid_size":    random.choice([100, 200, 500]),
            "min_distance": random.randint(3,  8),
            "min_skills":   1,
            "max_skills":   random.randint(2, 4),
            "min_value":    random.randint(10, 60),
            "max_value":    random.randint(80, 200),
            "min_capacity": 1,
            "max_capacity": random.randint(3, 15),
            "min_loudness": random.randint(10, 40),
            "max_loudness": random.randint(80, 150),
        }
        for key, val in r.items():
            entry = self._entries[key]
            entry.delete(0, "end")
            entry.insert(0, str(val))

        self._set_status("Random values filled — press Generate to create the file.", "gray")

    def _read_config(self):
        config = {}
        for label, key, lo, hi in FIELDS:
            raw = self._entries[key].get().strip()
            if not raw.isdigit():
                self._set_status(f"'{label}' must be an integer.", "#FF6060")
                return None
            val = int(raw)
            if not (lo <= val <= hi):
                self._set_status(f"'{label}' must be between {lo} and {hi}.", "#FF6060")
                return None
            config[key] = val

        pairs = [
            ("min_dwarves", "max_dwarves", "Min dwarves ≤ Max dwarves"),
            ("min_mines",   "max_mines",   "Min mines ≤ Max mines"),
            ("min_guards",  "max_guards",  "Min guards ≤ Max guards"),
            ("min_skills",  "max_skills",  "Min skills ≤ Max skills"),
            ("min_value",   "max_value",   "Min value ≤ Max value"),
            ("min_capacity","max_capacity","Min capacity ≤ Max capacity"),
            ("min_loudness","max_loudness","Min loudness ≤ Max loudness"),
        ]
        for lo_key, hi_key, msg in pairs:
            if config[lo_key] > config[hi_key]:
                self._set_status(f"Invalid range: {msg}.", "#FF6060")
                return None

        return config

    def _generate(self):
        config = self._read_config()
        if config is None:
            return

        try:
            gen = DwarfDataGenerator(custom_config=config)
            path, _ = gen.generate_and_save()
            self._set_status(f"Saved to {path}", "#66CC66")
        except Exception as e:
            self._set_status(f"Error: {e}", "#FF6060")

    def _set_status(self, msg: str, color: str = "gray"):
        self._status.configure(text=msg, text_color=color)
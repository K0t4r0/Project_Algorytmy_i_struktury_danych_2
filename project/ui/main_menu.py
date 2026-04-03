import customtkinter as ctk

class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ctk.CTkLabel(
            self,
            text="Main Menu",
            font=("Arial", 42, "bold")
        ).pack(pady=(40, 10))

        ctk.CTkLabel(
            self,
            text="Choose an algorithm to visualize",
            font=("Arial", 18)
        ).pack(pady=(0, 30))

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True)

        items = [
            ("Flow", "Max flow algorithms", "FlowPage"),
            ("Convex Hull", "Geometry algorithms", "HullPage"),
            ("Segment Tree", "Range queries", "SegmentPage"),
            ("Compression", "Union-Find & paths", "CompressionPage")
        ]

        for i, (title, desc, page) in enumerate(items):
            card = ctk.CTkFrame(
                container,
                width=260,
                height=140,
                corner_radius=15
            )
            card.grid(row=i//2, column=i%2, padx=20, pady=20)
            card.grid_propagate(False)

            ctk.CTkLabel(
                card,
                text=title,
                font=("Arial", 18, "bold")
            ).pack(pady=(15, 5))

            ctk.CTkLabel(
                card,
                text=desc,
                font=("Arial", 14)
            ).pack(pady=(0, 10))

            ctk.CTkButton(
                card,
                text="Open",
                command=lambda p=page: controller.show_frame(p)
            ).pack(pady=(5, 10), padx=10)
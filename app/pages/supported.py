# app/pages/supported.py
import customtkinter as ctk
from converters.registry import REGISTRY

class SupportedPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        # Page Title
        self.label = ctk.CTkLabel(
            self, 
            text="📋 Supported Formats & Capabilities", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.label.pack(pady=(35, 15), padx=40, anchor="w")

        # Scrollable area for the categories
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=40, pady=(0, 30))

        # Build category sections from central registry
        for cat_key, cat_data in REGISTRY.items():
            self._build_category_section(cat_data)

    def _build_category_section(self, cat_data):
        """Creates a visual block for a category with input and output pills."""
        section = ctk.CTkFrame(self.scroll_frame, fg_color=("gray90", "gray14"), corner_radius=12)
        section.pack(fill="x", pady=8)

        # Header with icon and description
        header_frame = ctk.CTkFrame(section, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 6))

        title_text = f"{cat_data.get('icon', '📁')}  {cat_data['title']}"
        title_lbl = ctk.CTkLabel(header_frame, text=title_text, font=ctk.CTkFont(size=17, weight="bold"))
        title_lbl.pack(side="left")

        desc_lbl = ctk.CTkLabel(
            section, 
            text=cat_data.get('description', ''), 
            text_color="gray60", 
            font=ctk.CTkFont(size=12)
        )
        desc_lbl.pack(anchor="w", padx=20, pady=(0, 8))

        # Inputs Row
        self._create_pill_row(section, "Can read:", cat_data["inputs"], pill_color="#1f538d")
        
        # Outputs Row
        outputs_with_dots = [f".{out.lower()}" for out in cat_data["outputs"]]
        self._create_pill_row(section, "Converts to:", outputs_with_dots, pill_color="#2FA572")
        
        # Spacer at bottom of card
        ctk.CTkFrame(section, height=6, fg_color="transparent").pack()

    def _create_pill_row(self, parent, label_text, items, pill_color):
        """Helper to create a row of styled extension pills."""
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", padx=20, pady=3)

        lbl = ctk.CTkLabel(row_frame, text=label_text, width=100, anchor="w", text_color="gray70", font=ctk.CTkFont(size=12))
        lbl.pack(side="left")

        pills_container = ctk.CTkFrame(row_frame, fg_color="transparent")
        pills_container.pack(side="left", fill="x", expand=True)

        for item in items:
            pill = ctk.CTkLabel(
                pills_container, 
                text=item.upper(), 
                fg_color=pill_color, 
                text_color="white",
                corner_radius=6,
                padx=8,
                pady=2,
                font=ctk.CTkFont(size=11, weight="bold")
            )
            pill.pack(side="left", padx=3, pady=2)
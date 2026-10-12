# app/pages/settings.py
import customtkinter as ctk
from tkinter import filedialog
from app.config_manager import get_config, save_config
from converters.registry import check_system_tools

class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        # Page Title
        self.label = ctk.CTkLabel(self, text="⚙️ Settings & System Status", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=(35, 20), padx=40, anchor="w")

        # Scrollable area
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        # --- Output Directory Setting Card ---
        dir_card = ctk.CTkFrame(self.scroll, fg_color=("gray90", "gray14"), corner_radius=12)
        dir_card.pack(fill="x", pady=10)

        out_title = ctk.CTkLabel(dir_card, text="📁 Default Output Directory", font=ctk.CTkFont(size=16, weight="bold"))
        out_title.pack(anchor="w", padx=20, pady=(15, 5))

        out_desc = ctk.CTkLabel(
            dir_card, 
            text="Where converted files are saved. If left blank, files are saved in the same directory as the source.", 
            text_color="gray60",
            font=ctk.CTkFont(size=12)
        )
        out_desc.pack(anchor="w", padx=20, pady=(0, 10))

        out_input_frame = ctk.CTkFrame(dir_card, fg_color="transparent")
        out_input_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.out_dir_entry = ctk.CTkEntry(out_input_frame, placeholder_text="Default: Source file directory")
        self.out_dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.out_dir_btn = ctk.CTkButton(out_input_frame, text="Browse", width=80, command=self.choose_directory)
        self.out_dir_btn.pack(side="left", padx=(0, 5))

        self.clear_btn = ctk.CTkButton(
            out_input_frame, 
            text="Reset", 
            width=60, 
            fg_color="transparent", 
            border_width=1, 
            command=self.clear_directory
        )
        self.clear_btn.pack(side="left")

        # --- System Engine Diagnostics Card ---
        engine_card = ctk.CTkFrame(self.scroll, fg_color=("gray90", "gray14"), corner_radius=12)
        engine_card.pack(fill="x", pady=10)

        eng_title = ctk.CTkLabel(engine_card, text="🔧 External Conversion Engines", font=ctk.CTkFont(size=16, weight="bold"))
        eng_title.pack(anchor="w", padx=20, pady=(15, 5))

        eng_desc = ctk.CTkLabel(
            engine_card, 
            text="Tabular, images, and data work natively in Python. Rich media & PDF conversion utilize system utilities below (all included in Docker).", 
            text_color="gray60",
            font=ctk.CTkFont(size=12),
            wraplength=600,
            justify="left"
        )
        eng_desc.pack(anchor="w", padx=20, pady=(0, 15))

        tools = check_system_tools()
        for key, info in tools.items():
            self._render_engine_row(engine_card, info)

        ctk.CTkFrame(engine_card, height=10, fg_color="transparent").pack()

        # Load existing config on startup
        self.load_settings()

    def _render_engine_row(self, parent, info):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=4)

        status_icon = "✅" if info["available"] else "⚠️"
        status_color = "#2FA572" if info["available"] else "#D97706"
        status_text = "Detected" if info["available"] else "Not installed in PATH"

        title = ctk.CTkLabel(row, text=f"{status_icon} {info['name']}", font=ctk.CTkFont(size=13, weight="bold"), width=220, anchor="w")
        title.pack(side="left")

        badge = ctk.CTkLabel(row, text=status_text, text_color=status_color, font=ctk.CTkFont(size=11, weight="bold"), width=150, anchor="w")
        badge.pack(side="left")

        desc = ctk.CTkLabel(row, text=info["purpose"], text_color="gray60", font=ctk.CTkFont(size=11), anchor="w")
        desc.pack(side="left", fill="x", expand=True)

    def load_settings(self):
        config = get_config()
        saved_dir = config.get("default_output_dir", "")
        if saved_dir:
            self.out_dir_entry.delete(0, "end")
            self.out_dir_entry.insert(0, saved_dir)

    def choose_directory(self):
        selected_dir = filedialog.askdirectory(title="Select Default Output Folder")
        if selected_dir:
            self.out_dir_entry.delete(0, "end")
            self.out_dir_entry.insert(0, selected_dir)
            config = get_config()
            config["default_output_dir"] = selected_dir
            save_config(config)

    def clear_directory(self):
        self.out_dir_entry.delete(0, "end")
        config = get_config()
        config["default_output_dir"] = ""
        save_config(config)
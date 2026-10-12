# app/sidebar.py
import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, command, **kwargs):
        super().__init__(master, width=220, corner_radius=0, **kwargs)
        self.command = command

        # Title
        self.logo_label = ctk.CTkLabel(
            self, 
            text="🔄 OmniConverter", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(25, 25))

        # Navigation Buttons
        self.btn_convert = ctk.CTkButton(
            self, 
            text="⚡ Convert Files", 
            anchor="w",
            font=ctk.CTkFont(weight="bold"),
            command=lambda: self.command("convert")
        )
        self.btn_convert.grid(row=1, column=0, padx=20, pady=6, sticky="ew")

        self.btn_history = ctk.CTkButton(
            self, 
            text="📜 History", 
            anchor="w",
            command=lambda: self.command("history")
        )
        self.btn_history.grid(row=2, column=0, padx=20, pady=6, sticky="ew")
        
        self.btn_supported = ctk.CTkButton(
            self, 
            text="📋 Formats Matrix", 
            anchor="w",
            command=lambda: self.command("supported")
        )
        self.btn_supported.grid(row=3, column=0, padx=20, pady=6, sticky="ew")

        self.btn_settings = ctk.CTkButton(
            self, 
            text="⚙️ Settings", 
            anchor="w",
            command=lambda: self.command("settings")
        )
        self.btn_settings.grid(row=4, column=0, padx=20, pady=6, sticky="ew")

        # Spacer to push the theme toggle to the bottom
        self.grid_rowconfigure(5, weight=1)

        # Theme Toggle Button
        self.current_theme = "Dark" 
        ctk.set_appearance_mode(self.current_theme)
        
        self.btn_theme = ctk.CTkButton(
            self, 
            text="☀️ Light Mode", 
            fg_color="transparent", 
            border_width=1,
            text_color=("gray10", "#DCE4EE"),
            command=self.toggle_theme
        )
        self.btn_theme.grid(row=6, column=0, padx=20, pady=(10, 20), sticky="ew")

    def toggle_theme(self):
        if self.current_theme == "Dark":
            self.current_theme = "Light"
            ctk.set_appearance_mode("Light")
            self.btn_theme.configure(text="🌙 Dark Mode")
        else:
            self.current_theme = "Dark"
            ctk.set_appearance_mode("Dark")
            self.btn_theme.configure(text="☀️ Light Mode")
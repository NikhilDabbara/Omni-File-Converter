# app/components/dropzone.py
import re
import customtkinter as ctk
from tkinter import filedialog     # <-- NEW IMPORT
from tkinterdnd2 import DND_FILES

class DropZone(ctk.CTkFrame):
    def __init__(self, master, on_files_dropped_callback, **kwargs):
        super().__init__(master, border_width=2, border_color="gray50", corner_radius=15, **kwargs)
        self.on_files_dropped = on_files_dropped_callback

        # Inner label for instructions
        self.label = ctk.CTkLabel(
            self, 
            text="Drag & Drop files here\nor click to browse",
            font=ctk.CTkFont(size=18),
            text_color="gray60"
        )
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        # --- 1. Setup Drag and Drop ---
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.handle_drop)
        self.dnd_bind('<<DropEnter>>', self.handle_drag_enter)
        self.dnd_bind('<<DropLeave>>', self.handle_drag_leave)

        # --- 2. Setup Click-to-Browse ---
        # Bind the left mouse click to both the frame and the label
        self.bind("<Button-1>", self.open_file_browser)
        self.label.bind("<Button-1>", self.open_file_browser)
        
        # Change the mouse cursor to a pointing hand on hover to indicate it's clickable
        self.configure(cursor="hand2")
        self.label.configure(cursor="hand2")

    def open_file_browser(self, event=None):
        """Opens the OS file picker when the zone is clicked."""
        file_paths = filedialog.askopenfilenames(
            title="Select files to convert"
        )
        if file_paths:
            # Pass the selected files to the same callback as the drop event
            self.on_files_dropped(file_paths)

    def handle_drag_enter(self, event):
        self.configure(border_color="#1f538d", fg_color=("gray85", "gray25"))
        self.label.configure(text_color=("black", "white"))

    def handle_drag_leave(self, event):
        self.configure(border_color="gray50", fg_color=("gray90", "gray17"))
        self.label.configure(text_color="gray60")

    def handle_drop(self, event):
        self.handle_drag_leave(event)
        
        # Added a debug print to see what the OS is actually sending
        print(f"DEBUG - Dropped raw data: {event.data}")
        
        raw_data = event.data
        if '{' in raw_data:
            files = self.split_dnd_paths(raw_data)
        else:
            files = raw_data.split()
            
        self.on_files_dropped(files)

    def split_dnd_paths(self, data):
        return re.findall(r'\{.*?\}|\S+', data)
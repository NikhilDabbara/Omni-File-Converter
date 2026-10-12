# app/pages/history.py
import customtkinter as ctk
from app.history_manager import get_history, clear_history

class HistoryPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        # Header Area
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=40, pady=(35, 15))

        self.label = ctk.CTkLabel(self.header_frame, text="📜 Conversion History", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(side="left")

        # Buttons on right
        btn_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        btn_frame.pack(side="right")

        self.clear_btn = ctk.CTkButton(
            btn_frame, 
            text="🗑️ Clear", 
            width=70,
            fg_color="transparent",
            border_width=1,
            text_color=("gray20", "gray80"),
            command=self.clear_and_refresh
        )
        self.clear_btn.pack(side="left", padx=(0, 8))

        self.refresh_btn = ctk.CTkButton(
            btn_frame, 
            text="↻ Refresh", 
            width=80,
            command=self.load_history
        )
        self.refresh_btn.pack(side="left")

        # Scrollable area for history items
        self.history_list = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.history_list.pack(fill="both", expand=True, padx=40, pady=(0, 30))
        
        self.load_history()

    def clear_and_refresh(self):
        clear_history()
        self.load_history()

    def load_history(self):
        """Fetches data from the JSON log and populates the scrollable frame."""
        for widget in self.history_list.winfo_children():
            widget.destroy()

        history_data = get_history()

        if not history_data:
            empty_label = ctk.CTkLabel(
                self.history_list, 
                text="No conversions logged yet.\nConversions performed locally or via the converter will appear here.", 
                text_color="gray60",
                font=ctk.CTkFont(size=13)
            )
            empty_label.pack(pady=60)
            return

        for item in history_data:
            self.create_history_row(item)

    def create_history_row(self, item):
        """Creates a visual row for a single history record."""
        row = ctk.CTkFrame(self.history_list, fg_color=("gray90", "gray14"), corner_radius=10)
        row.pack(fill="x", pady=4)

        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", padx=15, pady=10, fill="x", expand=True)

        filename_lbl = ctk.CTkLabel(info_frame, text=item.get('filename', 'Unknown'), font=ctk.CTkFont(weight="bold"), anchor="w")
        filename_lbl.pack(fill="x")
        
        orig = item.get('original_ext', '')
        targ = item.get('target_ext', '')
        ext_text = f"{orig.upper()}  ➔  {targ.upper()}"
        ext_lbl = ctk.CTkLabel(info_frame, text=ext_text, text_color="gray60", font=ctk.CTkFont(size=12), anchor="w")
        ext_lbl.pack(fill="x")

        meta_frame = ctk.CTkFrame(row, fg_color="transparent")
        meta_frame.pack(side="right", padx=15, pady=10)

        date_val = item.get('date', '')
        time_val = item.get('time', '')
        time_text = f"{date_val} {time_val}"
        time_lbl = ctk.CTkLabel(meta_frame, text=time_text, text_color="gray60", font=ctk.CTkFont(size=11))
        time_lbl.pack(anchor="e")

        status_val = item.get('status', 'unknown')
        status_color = "#2FA572" if status_val == 'success' else "#EF5350"
        status_text = "SUCCESS" if status_val == 'success' else "FAILED"
        status_lbl = ctk.CTkLabel(meta_frame, text=status_text, text_color=status_color, font=ctk.CTkFont(size=11, weight="bold"))
        status_lbl.pack(anchor="e")
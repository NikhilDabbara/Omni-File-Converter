# app/components/format_picker.py
import customtkinter as ctk

class FormatPicker(ctk.CTkFrame):
    def __init__(self, master, on_format_selected, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_format_selected = on_format_selected
        self.selected_format = ""
        self.recommended_buttons = []

        # Container for recommendations
        self.rec_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.rec_frame.pack(fill="x", pady=(0, 10))

        self.rec_label = ctk.CTkLabel(
            self.rec_frame, 
            text="✨ Recommended:", 
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2FA572"
        )
        self.rec_label.pack(side="left", padx=(0, 10))

        self.rec_buttons_container = ctk.CTkFrame(self.rec_frame, fg_color="transparent")
        self.rec_buttons_container.pack(side="left", fill="x", expand=True)

        # Container for all options dropdown
        self.all_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.all_frame.pack(fill="x")

        self.all_label = ctk.CTkLabel(
            self.all_frame, 
            text="All Target Formats:", 
            font=ctk.CTkFont(size=13)
        )
        self.all_label.pack(side="left", padx=(0, 15))

        self.selector = ctk.CTkOptionMenu(
            self.all_frame, 
            values=["Select a file first"],
            command=self.handle_dropdown_selection,
            dynamic_resizing=False,
            width=160
        )
        self.selector.pack(side="left")

        self.reason_label = ctk.CTkLabel(
            self, 
            text="", 
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="gray70"
        )
        self.reason_label.pack(anchor="w", pady=(8, 0))

        self.set_enabled(False)

    def set_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.selector.configure(state=state)
        for btn in self.recommended_buttons:
            btn.configure(state=state)

    def handle_dropdown_selection(self, value):
        self.selected_format = value
        self.reason_label.configure(text=f"Selected target format: {value}")
        self.on_format_selected(value)

    def pick_recommended(self, fmt, reason=""):
        self.selected_format = fmt
        self.selector.set(fmt)
        if reason:
            self.reason_label.configure(text=f"✨ {fmt}: {reason}")
        else:
            self.reason_label.configure(text=f"Target format: {fmt}")
        self.on_format_selected(fmt)

    def enable_and_update(self, allowed_outputs: list, recommendations: list = None):
        """Called when a file is dropped or selected to update valid formats and recommendations."""
        # Clear old recommended buttons
        for widget in self.rec_buttons_container.winfo_children():
            widget.destroy()
        self.recommended_buttons = []

        if not allowed_outputs:
            self.set_enabled(False)
            return

        # Update Dropdown
        self.selector.configure(values=allowed_outputs)
        
        # Build Recommendation Pills
        if recommendations:
            for rec in recommendations:
                fmt = rec.get("format")
                badge = rec.get("badge", "")
                reason = rec.get("reason", "")
                
                btn_text = f"★ {fmt} ({badge})" if badge else fmt
                btn = ctk.CTkButton(
                    self.rec_buttons_container,
                    text=btn_text,
                    height=28,
                    fg_color="#1f538d",
                    hover_color="#14375e",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    command=lambda f=fmt, r=reason: self.pick_recommended(f, r)
                )
                btn.pack(side="left", padx=4)
                self.recommended_buttons.append(btn)

        # Select the first recommendation or first allowed output
        initial = recommendations[0]["format"] if (recommendations and len(recommendations) > 0) else allowed_outputs[0]
        initial_reason = recommendations[0].get("reason", "") if (recommendations and len(recommendations) > 0) else ""
        
        self.pick_recommended(initial, initial_reason)
        self.set_enabled(True)
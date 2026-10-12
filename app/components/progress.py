# app/components/progress.py
import customtkinter as ctk

class ProgressIndicator(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Status text above the bar
        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="gray60", font=ctk.CTkFont(size=12))
        self.status_label.pack(anchor="w", pady=(0, 5))
        
        # The progress bar itself
        self.progress_bar = ctk.CTkProgressBar(self, height=8, corner_radius=4)
        self.progress_bar.pack(fill="x")
        self.progress_bar.set(0) # Start at 0%
        
    def start_loading(self, text="Converting..."):
        """Switches to an animated, looping loading state."""
        self.status_label.configure(text=text, text_color=("black", "white"))
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        
    def finish(self, success=True, message="Conversion Complete!"):
        """Stops the animation and sets success/error colors."""
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(1) # Fill the bar
        
        # Green for success, Red for error
        color = "#2FA572" if success else "#EF5350" 
        
        self.status_label.configure(text=message, text_color=color)
        self.progress_bar.configure(progress_color=color)
        
    def reset(self):
        """Resets the UI back to the default state."""
        self.status_label.configure(text="Ready", text_color="gray60")
        # Revert to default CustomTkinter blue
        self.progress_bar.configure(mode="determinate", progress_color=["#3a7ebf", "#1f538d"])
        self.progress_bar.set(0)
# app/pages/convert.py
import os
import sys
import subprocess
import threading
from pathlib import Path
import customtkinter as ctk

from app.components.dropzone import DropZone
from app.components.format_picker import FormatPicker
from app.components.progress import ProgressIndicator
from app.history_manager import log_conversion
from app.config_manager import get_config

from converters.registry import (
    REGISTRY,
    get_category_key_for_extension,
    get_supported_outputs,
    get_recommendations,
    convert_file
)

class ConvertPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.selected_files = []
        self.target_format = ""
        self.current_category = None

        self.label = ctk.CTkLabel(self, text="Convert Files", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=(35, 15), padx=40, anchor="w")
        
        self.dropzone = DropZone(self, on_files_dropped_callback=self.process_dropped_files, height=180)
        self.dropzone.pack(fill="x", padx=40, pady=(0, 15))
        
        self.format_picker = FormatPicker(self, on_format_selected=self.set_target_format)
        
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        self.convert_btn = ctk.CTkButton(
            self.action_frame, 
            text="⚡ Start Conversion", 
            font=ctk.CTkFont(weight="bold"),
            height=40,
            state="disabled",
            command=self.run_conversion
        )
        
        self.progress = ProgressIndicator(self.action_frame)
        self.progress.pack(side="left", fill="x", expand=True)

        self.result_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        self.open_folder_btn = ctk.CTkButton(
            self.result_button_frame, 
            text="📂 Open Output Folder", 
            font=ctk.CTkFont(weight="bold"),
            height=40,
            fg_color="#2FA572", 
            hover_color="#25825a",
            command=self.open_output_directory
        )
        
        self.reset_btn = ctk.CTkButton(
            self.result_button_frame, 
            text="🔄 Convert Another", 
            font=ctk.CTkFont(weight="bold"),
            height=40,
            fg_color="#5c5c5c",
            hover_color="#454545",
            command=self.reset_ui
        )

    def process_dropped_files(self, file_paths):
        self.result_button_frame.pack_forget()
        self.convert_btn.pack(side="right", padx=(20, 0))

        self.selected_files = [path.strip("{}") for path in file_paths if path.strip("{}")]
        if not self.selected_files:
            return

        first_file = Path(self.selected_files[0])
        ext = first_file.suffix.lower()
        
        self.current_category = get_category_key_for_extension(ext)

        if self.current_category:
            allowed_outputs = get_supported_outputs(ext)
            recommendations = get_recommendations(ext)
            cat_title = REGISTRY[self.current_category]["title"]
            
            self.format_picker.pack(fill="x", padx=40, pady=(0, 15))
            self.action_frame.pack(fill="x", padx=40, pady=10)
            
            self.format_picker.enable_and_update(allowed_outputs, recommendations)
            self.convert_btn.configure(state="normal")
            self.progress.reset()
            
            file_count = len(self.selected_files)
            file_desc = f"{first_file.name}" if file_count == 1 else f"{file_count} files"
            self.dropzone.label.configure(
                text=f"Selected: {file_desc}\nCategory: {cat_title}"
            )
        else:
            self.format_picker.pack_forget()
            self.action_frame.pack_forget()
            self.dropzone.label.configure(
                text=f"Unsupported format '{ext}'\nPlease drag a supported file or check Formats Matrix."
            )

    def set_target_format(self, selected_format):
        self.target_format = selected_format

    def run_conversion(self):
        if not self.target_format or not self.selected_files:
            return
            
        self.convert_btn.configure(state="disabled")
        self.format_picker.set_enabled(False)
        self.progress.start_loading(f"Converting {len(self.selected_files)} file(s) to {self.target_format}...")
        threading.Thread(target=self._async_worker, daemon=True).start()

    def _async_worker(self):
        success_count = 0
        error_message = None
        
        config = get_config()
        default_dir = config.get("default_output_dir", "")
        
        for file_path in self.selected_files:
            if default_dir and os.path.isdir(default_dir):
                output_dir = default_dir
            else:
                output_dir = os.path.dirname(file_path)
            
            result = convert_file(
                input_path=file_path,
                output_format=self.target_format,
                output_dir=output_dir
            )
            
            log_conversion(file_path, self.target_format, result.status)

            if result.status == 'success':
                success_count += 1
            else:
                error_message = result.error
                break 

        if success_count == len(self.selected_files):
            self.after(0, lambda: self._ui_conversion_complete(True, f"Successfully converted {success_count} file(s)!"))
        else:
            self.after(0, lambda: self._ui_conversion_complete(False, f"Error: {error_message}"))

    def _ui_conversion_complete(self, success, message):
        self.progress.finish(success=success, message=message)
        
        self.convert_btn.pack_forget()
        self.result_button_frame.pack(pady=(15, 0))
        
        if success:
            self.open_folder_btn.pack(side="left", padx=10)
        else:
            self.open_folder_btn.pack_forget()
            
        self.reset_btn.pack(side="left", padx=10)
        self.format_picker.set_enabled(True)

    def reset_ui(self):
        """Clears all states and returns the UI to its initial view."""
        self.result_button_frame.pack_forget()
        self.format_picker.pack_forget()
        self.action_frame.pack_forget()
        
        self.dropzone.label.configure(text="Drag & Drop files here\nor click to browse")
        
        self.selected_files = []
        self.target_format = ""
        self.current_category = None
        self.convert_btn.pack(side="right", padx=(20, 0))

    def open_output_directory(self):
        if not self.selected_files:
            return
            
        config = get_config()
        default_dir = config.get("default_output_dir", "")
        
        if default_dir and os.path.isdir(default_dir):
            output_dir = default_dir
        else:
            output_dir = os.path.dirname(self.selected_files[0])
        
        try:
            if sys.platform == "win32":
                os.startfile(output_dir)
            elif sys.platform == "darwin": 
                subprocess.Popen(["open", output_dir])
            else: 
                subprocess.Popen(["xdg-open", output_dir])
        except Exception as e:
            print(f"Failed to open folder: {e}")
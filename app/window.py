# app/window.py
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD

from .sidebar import Sidebar
from .pages.convert import ConvertPage
from .pages.history import HistoryPage
from .pages.settings import SettingsPage
from .pages.supported import SupportedPage # <-- 1. NEW IMPORT

class TkinterDnD_CTk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class MainWindow(TkinterDnD_CTk):
    def __init__(self):
        super().__init__()

        self.title("File Converter")
        self.geometry("900x600")
        self.minsize(800, 500)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = Sidebar(self, command=self.switch_page)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.pages = {}
        
        self.pages["convert"] = ConvertPage(self)
        self.pages["convert"].grid(row=0, column=1, sticky="nsew")
        
        self.pages["history"] = HistoryPage(self)
        self.pages["history"].grid(row=0, column=1, sticky="nsew")
        
        # --- 2. INITIALIZE NEW PAGE ---
        self.pages["supported"] = SupportedPage(self)
        self.pages["supported"].grid(row=0, column=1, sticky="nsew")
        # ------------------------------
        
        self.pages["settings"] = SettingsPage(self)
        self.pages["settings"].grid(row=0, column=1, sticky="nsew")

        self.switch_page("convert")

    def switch_page(self, page_name: str):
        page = self.pages.get(page_name)
        if page:
            if hasattr(page, "load_history"):
                page.load_history()
            page.tkraise()
# main.py
import sys
import os
import subprocess

def run_web():
    """Runs the modern Streamlit web application."""
    print("Launching OmniConverter Web App on http://localhost:8501 ...")
    cmd = [sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port=8501"]
    subprocess.run(cmd)

def run_desktop():
    """Runs the CustomTkinter desktop application."""
    try:
        from app.window import MainWindow
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        # If desktop display is unavailable (e.g. running in headless Linux or Docker container),
        # fall back cleanly to the web application
        print(f"Desktop GUI unavailable ({e}). Falling back to Web Application...")
        run_web()

if __name__ == "__main__":
    if "--web" in sys.argv or "-w" in sys.argv:
        run_web()
    else:
        run_desktop()
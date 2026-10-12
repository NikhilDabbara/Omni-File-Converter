# app/history_manager.py
import json
import os
from datetime import datetime
from pathlib import Path

HISTORY_FILE = "conversion_history.json"

def log_conversion(input_path, output_format, status, output_path=None, size_bytes=None):
    """Saves a record of the conversion to a local JSON file."""
    filepath = Path(input_path)
    
    record = {
        "filename": filepath.name,
        "original_ext": filepath.suffix.lower(),
        "target_ext": f".{output_format.lower()}",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%I:%M %p"),
        "status": status,
        "output_path": str(output_path) if output_path else "",
        "size_bytes": size_bytes
    }

    history = get_history()
    history.insert(0, record)

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history[:100], f, indent=4)
    except Exception as e:
        print(f"Failed to write history: {e}")

def get_history():
    """Reads the history from the JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def clear_history():
    """Clears all conversion history."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
    except Exception as e:
        print(f"Failed to clear history: {e}")
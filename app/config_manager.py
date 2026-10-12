# app/config_manager.py
import json
import os

CONFIG_FILE = "config.json"

def get_config():
    """Reads the configuration from the JSON file."""
    if not os.path.exists(CONFIG_FILE):
        return {"default_output_dir": ""}
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"default_output_dir": ""}

def save_config(config_data):
    """Saves the configuration to the JSON file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)
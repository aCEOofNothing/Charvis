import requests
import json
from pathlib import Path

def is_flask_running():
    try:
        r = requests.get("http://127.0.0.1:5000/health", timeout=1)
        if r.status_code == 200:
            data = r.json()
            if data.get("app") == "Charvis Web UI" and data.get("status") == "running":
                return "RUNNING"
        return "OTHER_APP_RUNNING"
    except (requests.RequestException, ValueError):
        return "NOT_RUNNING"

def import_settings():
    BASE_DIR = Path(__file__).parent
    SETTINGS = BASE_DIR / "data" / "settings.json"
    with open(SETTINGS, "r") as file:
        settings = json.load(file)
    return settings

def save_settings(settings):
    BASE_DIR = Path(__file__).parent
    SETTINGS = BASE_DIR / "data" / "settings.json"
    with open(SETTINGS, "w") as file:
        json.dump(settings, file, indent=4)
import requests
import json
from pathlib import Path
import datetime

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

def import_data(path):
    BASE_DIR = Path(__file__).parent
    SETTINGS = BASE_DIR /path
    with open(SETTINGS, "r") as file:
        settings = json.load(file)
    return settings

def save_data(path, data):
    BASE_DIR = Path(__file__).parent
    SETTINGS = BASE_DIR /path
    with open(SETTINGS, "w") as file:
        json.dump(data, file, indent=4)

#def fehler_protokollieren(fehler):
 #   BASE_DIR = Path(__file__).parent
 #   FEHLERPROTOKOLL = BASE_DIR / "data" / "fehlerprotokoll.txt"
  #  nowtime = datetime.date(4, 4, 8)
 #   with open(FEHLERPROTOKOLL, "w") as file:
 #       file + " --- " + nowtime + fehler
#
#fehler_protokollieren("japadutesttest")




# Moduswechsel muss gefixt werden






#-----Grundanweisungen-----

import json
from pathlib import Path
import webbrowser
import subprocess
import requests


import core
import speech


#------Einstellungen importieren------
BASE_DIR = Path(__file__).parent
SETTINGS = BASE_DIR / "data" / "settings.json"
with open(SETTINGS, "r") as file:
    settings = json.load(file)



#-----Grundlogik-----

print("♾️    Charvis Ist Bereit!", end="\n\n")



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




def process_input(text):
    global mode

    BASE_DIR = Path(__file__).parent
    SETTINGS = BASE_DIR / "data" / "settings.json"
    with open(SETTINGS, "r") as file:
        settings = json.load(file)
    last_mode = mode
    mode = settings["triggerkey"]

    if "öffne die oberfläche" in text:
        flask_status = is_flask_running()
        if flask_status == "OTHER_APP_RUNNING":
            print("ACHTUNG: Port 5000 ist bereits besetzt, aber nicht von Charvis Web UI")
            print("Die Web UI kann nicht gestartet werden. Bitte schließe zuerst die andere App und versuche es dann nochmal.")
        else:
            if flask_status == "NOT_RUNNING":
                subprocess.Popen(["python", "gui/flaskgui.py"])
                print("Flaskserver für Charvis Web UI wird gestartet")
        
            print("Oberfläche wird geöffnet")
            webbrowser.open("http://127.0.0.1:5000", new=1)

    if "eingabe" in text:
        if "sprache" in text:
            mode = "speech"
            print("Zu Spracheingabe gewechselt")
            print("Halte NUMPAD-0 zum Sprechen...")
            settings["eingabemodus"] = "speech"
            with open(SETTINGS, "w") as file:
                json.dump(settings, file, indent=4)
        elif "terminal" in text:
            mode = "terminal"
            print("Zu Terminaleingabe gewechselt")
            settings["eingabemodus"] = "terminal"
            with open(SETTINGS, "w") as file:
                json.dump(settings, file, indent=4)
        else:
            print("❌ Bitte gib an, welchen Eingabemodus du öffnen möchtest ('Sprache' oder 'Terminal')")

    elif last_mode != mode:
        if mode == "speech":
            print("Zu Spracheingabe gewechselt")
            print("Halte NUMPAD-0 zum Sprechen...")
        elif mode == "terminal":
            print("Zu Terminaleingabe gewechselt")
        else:
            print("❌ Bitte gib an, welchen Eingabemodus du öffnen möchtest ('Sprache' oder 'Terminal')")

    else:
        core.handle_command(text)
    print("------")

def get_input(mode):
    if mode == "speech":
        return speech.listen()
    elif mode == "terminal":
        return input("> ")


global mode
mode = settings["eingabemodus"]
if mode == "speech":
    print("Halte NUMPAD-0 zum Sprechen...")

while True:
    text = get_input(mode)
    process_input(text)

    



#Japadapadu!
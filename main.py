#-----Grundanweisungen-----

import json
from pathlib import Path
import webbrowser
import subprocess


import core
import Input.speech as speech


#------Einstellungen importieren------
BASE_DIR = Path(__file__).parent
SETTINGS = BASE_DIR / "data" / "settings.json"
with open(SETTINGS, "r") as file:
    settings = json.load(file)



#-----Grundlogik-----

print("♾️    Charvis Ist Bereit!", end="\n\n")

def process_input(text):
    global mode

    BASE_DIR = Path(__file__).parent
    SETTINGS = BASE_DIR / "data" / "settings.json"
    with open(SETTINGS, "r") as file:
        settings = json.load(file)
    last_mode = mode
    mode = settings["triggerkey"]

    if "öffne die oberfläche" in text:
        subprocess.Popen(["Python", "gui/flaskgui.py"])
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
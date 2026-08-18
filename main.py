#-----Grundanweisungen-----

import json
from pathlib import Path
import webbrowser
import subprocess
import requests
import threading


import core
from input.speech import listen
from  assets import is_flask_running, import_settings, save_settings


print("♾️    Charvis Ist Bereit!", end="\n\n")

#-----Grundlogik-----

def process_input(text):
    global mode

    settings = import_settings()
    last_mode = mode
    mode = settings["eingabemodus"]

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

    elif "eingabe" in text:
        if "sprach" in text and "terminal" in text:
            print("Zu Sprach- und Terminaleingabe gewechselt")
            print("Halte NUMPAD-0 zum Sprechen...")
            mode = "speech+terminal"
            settings["eingabemodus"] = mode
            save_settings(settings)


        elif "sprache" in text:
            print("Zu Spracheingabe gewechselt")
            print("Halte NUMPAD-0 zum Sprechen...")
            mode = "speech"
            settings["eingabemodus"] = mode
            save_settings(settings)

        elif "terminal" in text:
            print("Zu Terminaleingabe gewechselt")
            mode = "terminal"
            settings["eingabemodus"] = mode
            save_settings(settings)

        else:
            print("❌ Bitte gib an, welchen Eingabemodus du öffnen möchtest ('Sprache', 'Terminal' oder 'Sprache und Terminal')")

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
        return listen()
    
    elif mode == "terminal":
        return input("> ")
    
    elif mode == "speech+terminal":
        threading.Thread(target=listen, daemon=True).start()
        return input("> ")


settings = import_settings()
mode = settings["eingabemodus"]
if mode == "speech":
    print("Halte NUMPAD-0 zum Sprechen...")






while True:
    text = get_input(mode)
    process_input(text)





#Japadapadu!
#-----Grundanweisungen-----

import json
from pathlib import Path


import core
import Input.speech as speech


#------Einstellungen importieren------
BASE_DIR = Path(__file__).parent
SETTINGS = BASE_DIR / "data" / "settings.json"
with open(SETTINGS, "r") as file:
    settings = json.load(file)



#-----Grundlogik-----

print("♾️    Charvis Ist Bereit!", end="\n\n")

def get_input(mode):
    if mode == "speech":
        return speech.listen()
    elif mode == "terminal":
        return input("> ")

mode = settings["eingabemodus"]
if mode == "speech":
    print("Halte NUMPAD-0 zum Sprechen...")

while True:
    text = get_input(mode)

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

    else:
        core.handle_command(text)
    print("------")



#Japadapadu!